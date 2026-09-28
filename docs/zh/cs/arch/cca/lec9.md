---
title: 超标量处理器
type: lecture
lecture: 9
tags: [superscalar-processor, multi-issue, superfifo, structural-hazard, raw-hazard]
status: complete
---
# Lec 9 超标量处理器

## TL;DR

- 超标量微架构通过在单时钟周期内并发取指、译码、发射与执行多条指令，打破标量流水线 IPC $\le 1$ 的理论天花板。
- 前端取指依赖 SuperFIFO 解决跨边界与单周期多元素出入队，Fetch 逻辑根据缓存行对齐自适应提取 1 或 2 条指令。
- 译码发射级必须同时处理各在飞指令间的 RAW 寄存器依赖以及同组两指令间的胞内前后写读依赖（Partial Stall）。
- 执行与写回阶段受限于数据缓存端口与多写端口寄存器堆的结构冲突，典型微架构对纯 ALU 指令双发，复杂指令降级为单发。

> MIT 6.1920 · Constructive Computer Architecture
> 讲师：Martin Chan / Thomas Bourgeat · 日期：2024-03-07

## 1. 超标量的动机

提高 IPC（*Instructions Per Cycle*）的思路：

$$\text{Time} = \frac{\text{Instructions}}{\text{Program}} \times \frac{\text{Cycles}}{\text{Instruction}} \times \frac{\text{Time}}{\text{Cycle}}$$

前面各节解决了分支/缓存缺失等问题，但 IPC 仍 ≤ 1。超标量（*Superscalar*）的思路：**每周期同时发射（*issue*）和执行多条指令**。

::: definition
**定义 — 超标量（*Superscalar*）**

超标量处理器每周期可以取指、译码、执行、写回两条或更多条指令。宽度（*issue width*）为 2 的处理器称为 2-wide superscalar，理论 IPC 上限为 2。
:::

---

## 2. Fetch 阶段扩展

在双发射处理器中，Fetch 级每周期需要向指令缓存请求 2 条连续指令。然而物理存储器在行边界处存在固有的跨行访问约束：

```bsv
// 返回 1 或 2 条指令
typedef struct {Word ins1; Maybe#(Word) ins2;} OneOrTwoWords;

rule fetch;
    toImem.enq(pcf);
    f2d.enq1(F2D{pc: pcf, ppc: pcf+4, epoch: epoch});
    if (!notLineBoundary(pcf)) begin  // 同一缓存行
        f2d.enq2(F2D{pc: pcf+4, ppc: pcf+8, epoch: epoch});
        pcf <= pcf + 8;
    end else
        pcf <= pcf + 4;
endrule
```

**取指对齐与跨行处理**：
- **行边界约束（缓存行边界）**：指令缓存每次访问只能返回单个缓存行。若当前 PC 恰好位于该行最后一个 32 位字处，硬件无法在单周期内跨越两个物理行提取第二条指令。此时 Fetch 逻辑退化为单指令发射，仅提取第 1 条指令并将 PC 递增 4；只有当 PC 处在行内非末尾位置时，才允许并行抓取 2 条指令并将 PC 递增 8。

**超标量队列（SuperFIFO）原语**：
普通的单发射 FIFO 无法支持每周期可变数量（0、1 或 2）的入队与出队。微架构为此抽象出具备多元素原子操作的 `SuperFIFO`：

```bsv
interface SuperFIFO#(type t);
    method Action enq1(t x);
    method Action enq2(t x);   // 隐含 enq1 已调用
    method Action deq1;
    method Action deq2;         // 隐含 deq1 已调用
    method t first1;
    method t first2;
endinterface
```

**底层循环队列（Rotating FIFO）实现**：
在 BSV 中，`SuperFIFO` 通过内部双子队列配合同周期旋转指针实现。利用读写指针的动态模 2 切换，硬件能够自动将第 1 个和第 2 个槽位分派给不同的物理寄存器，从而支持 `enq1` 与 `enq2` 并发无冲突写入，提供超标量级间缓冲所需的弹性多宽度吞吐能力。

---

## 3. Decode 阶段扩展

同时译码两条指令，需处理指令间依赖：

```bsv
if (noDependency(ins1, sb) && noDependency(ins2, sb) && noDependencyBetween(ins1, ins2)) begin
    d2e.enq1("ins1");  d2e.enq2("ins2");
    f2d.deq1;          f2d.deq2;
end else if (noDependency(ins1, sb)) begin
    d2e.enq1("ins1");  f2d.deq1;    // 部分停顿（partial stall）
end
// else：完全停顿
```

**指令间依赖（*Inter-Instruction Dependency*）**：ins2 的源寄存器与 ins1 的目标寄存器相同时，ins2 必须等待 ins1 完成写回后才能读取正确值（或通过旁路解决）。

::: example 例题 — Decode 依赖矩阵

:::

对所有（ins1, ins2）情况分类：

| ins1 状态 | ins2 状态 | ins2 依赖 ins1？ | 操作 |
|----------|----------|---------------|------|
| 无依赖 | 无依赖 | 否 | 双发射 |
| 无依赖 | 无依赖 | **是** | 仅发射 ins1 |
| 有依赖（stall）| — | — | 停顿 |

Sol：覆盖所有 3×3 情况（ins1 ok/stall/cond × ins2 的对称情况），并在单元测试中逐一验证。

---

## 4. Execute 阶段扩展

在执行阶段，双发射处理器面临严重的硬件结构冒险（Structural Hazard）：

- **ALU 逻辑单元**：复制一套 32 位 ALU 的硬件面积与门电路代价极小，易于实现双并发。
- **访存接口（Load/Store）**：若支持同时执行两条访存指令，要求数据缓存提供双读写端口，这会导致 SRAM 晶体管数量翻倍并产生高昂的布线时序延迟。
- **控制流跳转（Branch/Jump）**：若允许两条指令均为分支，多分支目标重定向与 Epoch 仲裁逻辑复杂度急剧攀升。

**非对称执行单元与退化策略**：
为了平衡硅片面积与性能，实际微架构常采用非对称分派策略：
- 当两条指令均为纯 ALU 计算时 → **双并发发射**（Dual Issue）
- 当任一指令包含 Load/Store 访存或 Branch 分支时 → **退化为单发射**（Single Issue）

```bsv
let ins1 = d2e.first1();
let ins2 = d2e.first2();
d2e.deq1();  // 至少处理 ins1

if (ins1 epoch 错误 && ins2 epoch 错误) begin
    d2e.deq2();  squash both;
end else if (ins1 epoch 错误) begin
    squash ins1; // ins2 下周期重试
end else if (isALU(ins1) && isALU(ins2) && ins2 epoch 正确) begin
    d2e.deq2();
    // 双 ALU 执行
end
// 其他情况只执行 ins1
```

**分支与纪元冲刷交互**：
当 ins1 为分支指令且在执行阶段被判定为预测错误时，与其同周期处于 Execute 级的 ins2 必须被无条件作废（Squash），决不能允许其将脏数据写入写回队列或更新处理器架构状态；同时触发全局纪元更新，向 Fetch 发送正确的纠错目标地址。

---

## 5. Writeback 阶段扩展

- 寄存器文件需要 **2 个写端口**
- 计分板需要 **2 个 insert / 2 个 search**
- 若两条指令写同一寄存器：通常由硬件保证后者覆盖（ins2 > ins1）

**EHR 与多端口**：扩展 EHR 端口数以支持同周期多写，面积代价可通过 BRAM 替代 RegFile 来控制。

---

## 6. 性能提升

::: theorem 推论 — 超标量的实际 IPC 提升
理论 IPC 上限为发射宽度，但实际受限于指令间依赖（RAW）、结构冒险（访存）和控制流（分支）。ALU 密集型代码受益最大（科学计算、数值算法）；存储器密集型或分支密集型代码提升有限。
:::

未来方向：**同时多线程（*Simultaneous Multithreading, SMT*）** — 多个线程共享同一超标量处理器，每周期从不同线程发射指令，填充单线程无法利用的槽位。

---

## 核心机制小结与超标量瓶颈分析

超标量处理器在每个流水线阶段都需要宽化：SuperFIFO 支持多路 enq/deq，Decode 处理指令间依赖矩阵，Execute 通过双 ALU 实现双发射（访存/控制仍单发），Writeback 需要多写端口；EHR 是解决多端口读写冲突的关键 BSV 原语。

## 核心机制思考与底层洞察

::: insight 超标量微架构的平方级硬件开销复杂度（$O(N^2)$）
在微架构演进中，将发射宽度从标量 $N=1$ 拓宽到 $N=2$ 乃至 $N=4$ 是提升算力的直观思路，但硬件实现的复杂度并非线性增长：

1. **组合检查网络的平方级膨胀**：对于 $N$ 发射超标量处理器，译码阶段必须对同一发射包内的全部 $N$ 条候选指令进行跨指令依赖检测，比较器数量随 $O(N^2)$ 迅速激增；执行级的结果旁路网络（Forwarding MUXes）不仅要在级间传递，还必须跨并联执行单元交叉互联，其布线拥塞度与延迟呈 $O(N^2 \times \text{流水级数})$ 恶化。
2. **多端口寄存器堆的晶体管立方级开销**：一个 $N$ 发射核心要求通用寄存器堆提供 $2N$ 个读端口和 $N$ 个写端口。每个存储单元的物理面积与接触端口数的平方成正比，导致整个 Register File 的硅片面积以接近 $O(N^3)$ 的速度灾难性膨胀。
3. **顺序超标量在访存缺失下的脆弱性**：在顺序流水线中，由于程序指令无法跨越障碍乱序执行，一旦 ins1 遭遇 L1 缓存缺失或长延迟依赖，随后的 ins2 即便完全独立也必须连带停顿。这导致 2-wide 甚至 4-wide 顺序超标量在真实应用负载中的实际 IPC 往往只有 1.2–1.3，远未达到理想上限。这种投入产出比的断崖式下跌，直接催生了现代乱序执行（Out-of-Order）和多线程（SMT）技术的诞生。
:::
