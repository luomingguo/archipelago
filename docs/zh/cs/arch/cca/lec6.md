---
title: 流水线处理器
type: lecture
lecture: 6
tags: [pipelined-processor, raw-hazard, scoreboard, epoch-speculation, pipeline-fifo]
status: complete
---
# Lec 06 流水线处理器

## TL;DR

- 4 级流水线（IF-ID-EX-WB）借助级间弹性 Pipeline FIFO 将单周期巨型组合逻辑切分为均衡的独立阶段。
- 各流水级由独立并发触发的 BSV 规则承载，级间握手自动规避了传统 RTL 手写使能与停顿控制信号的复杂性。
- 数据冒险（RAW）通过计分板（Scoreboard）记录在飞指令的目标寄存器，并在译码端判定停顿或转发。
- 控制冒险通过纪元计数器（Epoch）进行推测执行与路径纠正，在 Execute 阶段发现分支失败时实现原子冲刷。

> MIT 6.1920 · Constructive Computer Architecture
> 讲师：Arvind · 日期：2024-02-22

## 1. 流水线的动机

$$\text{Time} = \frac{\text{Instructions}}{\text{Program}} \times \frac{\text{Cycles}}{\text{Instruction}} \times \frac{\text{Time}}{\text{Cycle}}$$

非流水线处理器 CPI ≈ 2–3；流水线目标：CPI → 1，使各阶段硬件同时忙碌。

::: definition
**定义 — 4 级流水线（*4-Stage Pipeline*）**

将指令执行分为 4 个流水级，每级用级间寄存器（*pipeline register*）暂存中间结果：

**Fetch（IF）→ Decode（ID）→ Execute（EX）→ Writeback（WB）**

访存（MEM）并入 Execute 或 Writeback 阶段。
:::

---

## 2. BSV 4 级流水线结构

流水线处理器将原本单周期的长组合路径打断，利用级间缓冲解耦各流水阶段的执行步调。

### 2.1 级间 FIFO

各阶段之间采用弹性 `PipelineFIFO` 作为流水线寄存器：

```bsv
FIFO#(Fetch2Decode)   f2d <- mkPipelineFIFO;
FIFO#(Decode2Execute) d2e <- mkPipelineFIFO;
FIFO#(Maybe#(Exec2WB)) e2w <- mkPipelineFIFO;
```

**级间通信与调度约束**：
- **流水线 FIFO 的必要性**：普通单元素 FIFO 存在 $enq$ 与 $deq$ 的同周期调度冲突（Conflict），当队列满时前级无法入队，会导致整条流水线在满载时永久停顿死锁。`mkPipelineFIFO` 支持 $deq < enq$ 语义，允许在下游出队的同时上游立即填入新指令，保证无冒险情况下每个周期持续吞吐一条指令。
- **级间数据包定义**：`f2d` 传递取出的指令与程序计数器；`d2e` 传递译码后的操作码、源操作数与分支预测信息；`e2w` 传递待写回的结果数据与目的寄存器编号。

### 2.2 各级规则

每个流水阶段均由一个独立的 BSV 规则表示，编译器在每个时钟周期自动并行调度这四个规则：

```bsv
rule fetch;
    iMem.enq(pc[1]);
    f2d.enq(Fetch2Decode{pc: pc[1], epoch: epoch[1]});
    pc[1] <= pc[1] + 4;
endrule

rule decode;
    let inst = iMem.first; iMem.deq;
    let x = f2d.first;   f2d.deq;
    let dInst = decode(inst);
    d2e.enq(Decode2Execute{dInst, pc: x.pc, epoch: x.epoch, ...});
endrule

rule execute;
    let x = d2e.first; d2e.deq;
    if (x.epoch != epoch[0])
        e2w.enq(Invalid);     // 冲刷无效指令
    else begin
        let eInst = exec(x.dInst, rVal1, rVal2, x.pc);
        if (mispredicted) begin pc[0] <= correct_pc; epoch[0] <= epoch[0]+1; end
        e2w.enq(Valid(Exec2WB{eInst, pc: x.pc}));
    end
endrule

rule writeback;
    let vx = e2w.first; e2w.deq;
    if (vx matches tagged Valid .x) begin
        if (isValid(x.eInst.dst)) rf.wr(...);
        if (x.eInst.iType == Ld) dMem.deq;
    end
    sb.remove;
endrule
```

**流水线规则并发执行特性**：
- **`fetch` 阶段**：从指令存储器发出请求，以当前 PC 与 epoch 构造控制包压入 `f2d`，并将 PC 递增 4。注意 `pc` 使用 EHR 端口 1，以便 Execute 阶段的纠错写（端口 0）具有更高优先级。
- **`decode` 阶段**：从 `f2d` 和 `iMem` 同时出队，展开指令译码，并检查计分板以判断是否存在数据冒险。若检测到冒险则规则守护条件失效并挂起（Stall）。
- **`execute` 阶段**：执行 ALU 计算与分支判定。若当前指令携带的 epoch 与系统全局 epoch 不一致，说明该指令属于已作废的分支错误推测路径，直接写入 `Invalid` 予以冲刷；若预测错误，则通过高优先级的 `pc[0]` 重设正确地址并递增全局 `epoch`。
- **`writeback` 阶段**：将有效结果打入通用寄存器堆，并从计分板中将该指令的目的寄存器注销释放。

**EHR 在流水线跨级通信中的定序角色**：
在上述四级流水线实现中，PC 寄存器与 Epoch 寄存器均被实例化为具有多端口的 EHR 原语。之所以 `fetch` 阶段写入 `pc[1]` 而 `execute` 阶段重定向写入 `pc[0]`，是因为 EHR 保证了端口 0 的写入对端口 1 的读取和写入具备严格的优先覆盖权（$port_0 < port_1$）。当 Execute 级在同一时钟周期发现分支预测失误时，它写入的新正确跳转地址能够在同一周期直接迫使 Fetch 级读取并装载该新地址，从而将分支失误的恢复惩罚（Misprediction Penalty）最小化为一个周期的流水线气泡，而不会发生写后读冲突。

---

## 3. 数据冒险（*Data Hazard*）

::: definition
**定义 — 读后写冒险（*RAW Hazard, Read-After-Write*）**

当指令 i2 的源寄存器与尚未写回的指令 i1 的目标寄存器相同时，出现 RAW 冒险。若不处理，i2 将读到旧值。
:::

### 3.1 计分板（*Scoreboard*）

计分板用于动态跟踪“哪些通用寄存器正在被当前流水线中在飞的未完成指令写入”：

```bsv
interface Scoreboard;
    method Action insert(Maybe#(RIndx) dst);   // 指令进入 Decode 时登记
    method Action remove;                        // 指令完成 Writeback 时释放
    method Bool search1(Maybe#(RIndx) src);     // 检查 src 是否"脏"
    method Bool search2(Maybe#(RIndx) src);
endinterface
```

**计分板硬件结构与冲突检测**：
- **在飞指令队列**：计分板内部维护一个固定深度（等于流水线最大容纳在飞指令数）的寄存器队列。当目的寄存器有效且不为 `$x0` 时，Decode 阶段调用 `insert` 将其存入队列末尾。
- **并发全比对网络**：方法 `search1` 与 `search2` 实现为组合逻辑比较树，将当前指令的源寄存器 `src1` 与 `src2` 并发比对计分板中的所有在飞槽位。若命中任何冲突条目，返回 `True` 触发暂停。
- **先进先出释放**：指令按顺序抵达 Writeback 阶段并写入寄存器堆后，调用 `remove` 移出队首的条目，释放对应的寄存器锁定状态。

Decode 阶段的冒险检测与背压控制：

```bsv
let stall = sb.search1(dInst.src1) || sb.search2(dInst.src2);
if (!stall) begin
    sb.insert(dInst.dst);
    d2e.enq(...);
    f2d.deq; iMem.deq;
end  // stall: 不 deq，保持 f2d 和 iMem 不动
```

**停顿与弹性背压传导**：
当 `stall` 为真时，Decode 阶段不仅拒绝将指令送往 Execute，同时**不从 `f2d` 和 `iMem` 执行 `deq` 出队操作**。这导致 `f2d` 级间 FIFO 保持满载状态；依托 `PipelineFIFO` 的流控机制，上游的 `fetch` 规则在尝试写入已满的 `f2d` 时将自动被硬件守护条件阻断，从而以全硬件方式自动实现了流水线前端的平滑冻结，无需设计者手写复杂的全局时钟门控（Clock Gating）控制网。

::: theorem
**推论 — 旁路（*Bypassing / Forwarding*）**　计分板 stall 会降低 CPI。旁路网络（forwarding network）将 EX/MEM 阶段的计算结果直接送回 Decode 或 Execute 阶段作为源操作数，消除大多数 RAW stall，使 CPI 接近 1。
:::

---

## 4. 控制冒险（*Control Hazard*）

::: definition
**定义 — 控制冒险与 Epoch（*Control Hazard & Epoch*）**

分支/跳转指令在 Execute 阶段才确定真实目标，而 Fetch 已提前取了下一条指令。若预测错误，需**冲刷（flush）**流水线中错误路径上的指令。BSV 用**纪元计数器（epoch）**标记每条指令所属时代，Execute 检测到错误预测时递增 epoch，后续各级遇到旧 epoch 的指令直接丢弃。
:::

冲刷机制流程：
1. Execute 发现 ppc ≠ 真实 nextPc
2. `pc[0] <= correct_pc; epoch[0] <= epoch[0] + 1;`
3. Decode / Writeback 中旧 epoch 指令 → `e2w.enq(Invalid)`
4. 计分板也需同步清理

---

## 5. 流水线性能

::: example 例题 — 流水线 CPI 估算

:::

假设：分支占 20%，预测全部 pc+4，分支实际 taken 60%；无 RAW stall（假设有旁路）：
- 分支错误率 = 20% × 60% = 12%
- 每次分支错误冲刷 3 条指令（4 级流水）
- CPI = $1 + 0.12 \times 3 = 1.36$

Sol：提升分支预测精度（加 BTB、BHT）可将 CPI 降低至接近 1。

---

## 核心机制小结与流水线冒险权衡

4 级 BSV 流水线通过级间 FIFO 和 epoch 机制实现正确的指令执行；计分板防止 RAW 冒险；epoch 机制处理控制冒险；旁路网络消除 stall，是提升 CPI 的关键硬件投入。

## 核心机制思考与底层洞察

::: insight 纪元计数（Epoch）与分布式冲刷的工程优雅性
在现代处理器架构中，分支预测错误时的流水线冲刷（Pipeline Flush）是设计最具挑战性的关键时序路径之一。对比传统手工 Verilog 与 BSV 的纪元（Epoch）机制，可以清晰看到抽象维度的升华：

1. **传统 RTL 的全局复位连线危机**：在手写 Verilog 状态机中，流水线冲刷通常依赖一条源自执行级的全局同步复位信号线（`flush`）。该信号必须在一个时钟周期内穿透物理芯片长距离广播给所有级间流水寄存器，强行清零有效位（`valid <= 0`）。随着流水线深度和时钟主频攀升，全局 `flush` 树的驱动扇出（Fanout）和布线延迟极其容易恶化为全芯片的严重时序违例（Timing Violation）。
2. **Epoch 机制将全局重置转化为分布式过滤**：BSV 引入的 `epoch` 机制优雅地化解了这一物理瓶颈。系统仅需维护一个低位宽（通常仅需 1 位或 2 位）的 `epoch` 寄存器。当分支预测失败时，Execute 级仅仅在本地将 `epoch` 计数器自增 1，并将纠错地址送回 Fetch 级。处于中途流水级中的在飞指令无需被即刻强力抹除；当它们按节奏流经后续各阶段时，每个流水级规则仅在本地比对携带的 epoch 标签：凡是与全局当前 epoch 不符的指令，被自然视为气泡（Poisoned/Invalid）静默丢弃。这种去中心化的局部决策彻底消除了全局强复位网络，体现了硬件构建中将空间物理约束转变为时间逻辑过滤的经典架构思想。
:::
