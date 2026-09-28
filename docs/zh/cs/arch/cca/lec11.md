---
title: 乱序执行
type: lecture
lecture: 11
tags: [out-of-order-execution, tomasulo-algorithm, register-renaming, reorder-buffer, precise-interrupts]
status: complete
---
# Lec 11 乱序执行

## TL;DR

- 乱序执行通过寄存器重命名彻底消除假数据依赖（WAR 与 WAW），仅保留指令间固有的真数据依赖（RAW）。
- 重排序缓冲区（ROB）以环形 FIFO 维护程序顺序，实现“乱序执行，顺序提交（In-Order Commit）”。
- 投机执行与精确中断机制依托 ROB 头部的原子提交判定，确保发生异常或预测失败时架构状态可无损回滚。
- BSV 中利用 Vector 与指示状态机将 Tomasulo 调度与 ROB 拆分为可形式化综合的解耦规则系统。

> MIT 6.1920 · Constructive Computer Architecture
> 讲师：Arvind · 日期：2024-03-21

## 1. 乱序执行的动机

::: definition 定义 — 数据冒险三类型
- **RAW（*Read After Write*，真依赖）**：i2 需要读取 i1 写的值。必须等待，是真正的依赖。

- **WAR（*Write After Read*，反依赖）**：i2 写入 i1 需要读取的寄存器。顺序执行中是伪依赖。

- **WAW（*Write After Write*，输出依赖）**：i1 和 i2 写同一寄存器。顺序执行中是伪依赖。

WAR 和 WAW 是*名字依赖（name dependency）*，可通过寄存器重命名消除。
:::

---

## 2. 顺序发射计分板（*In-Order Issue Scoreboard*）

```bsv
Bool  busy[32];   // Busy[r] = 某条在途指令将写寄存器 r
RIndx wp[32];     // 未使用（简单计分板只跟踪 busy）
```

Decode 阶段检查：

```bsv
let stall = busy[src1] || busy[src2];
if (!stall) begin
    busy[dst] <= True;   // 标记 dst 将被写
    发射指令到执行单元
end
```

Execute 完成后清除：`busy[dst] <= False;`

**问题**：顺序发射下，只要一条指令停顿，后面所有指令都必须等待，即使后面的指令与停顿指令无关。

---

## 3. Tomasulo 寄存器重命名（*Register Renaming*）

::: definition
**定义 — Tomasulo 算法（*Tomasulo Algorithm, 1967*）**

每条指令发射时，将其目标寄存器重命名为一个物理寄存器（*physical register*）或 ROB 项编号，消除 WAR/WAW 依赖；源寄存器若未就绪，记录"等待哪个物理寄存器的结果"，结果产生时通过公共数据总线（*Common Data Bus, CDB*）广播，等待者被唤醒。
:::

---

## 4. 重排序缓冲区（*Reorder Buffer, ROB*）

::: definition
**定义 — ROB（*Reorder Buffer*）**

ROB 是一个循环队列（FIFO），按程序顺序存储所有在途指令。指令可以乱序执行完成，但必须**按顺序提交（*in-order commit*）**——ROB 头部的指令完成后才能写回架构寄存器文件（*architectural register file*）并出队。ROB 实现精确中断（*precise interrupt*）的关键机制。
:::

**四个执行阶段**：

| 阶段 | 操作 |
|------|------|
| Fetch（取指）| 从 I-Cache 读取指令 |
| Decode/Rename（译码/重命名）| 分配 ROB 项，重命名目标寄存器 |
| Execute（执行）| 乱序执行，结果写 ROB 项 |
| Commit（提交）| 按顺序从 ROB 头提交，写架构 RF |

---

## 5. BSV 乱序处理器实现要点

在 BSV 中，乱序执行的核心是将动态数据流调度与顺序架构状态分离。

### 5.1 ROB 结构

重排序缓冲区被建模为一个定长环形缓冲队列，每个条目维护指令在飞期间的瞬态计算状态：

```bsv
typedef struct {
    RIndx    archDst;    // 架构目标寄存器
    Data     result;     // 计算结果（等待填入）
    Bool     done;       // 是否完成
    IType    iType;      // 指令类型
} ROBEntry;

// 循环队列
Vector#(ROBSize, Reg#(ROBEntry)) rob <- replicateM(mkRegU);
Reg#(ROBIndex) head <- mkReg(0);
Reg#(ROBIndex) tail <- mkReg(0);
```

**ROB 字段微架构职责**：
- **`archDst`**：记录指令原本要写入的逻辑架构寄存器编号（如 `$x1`）。
- **`result`**：暂存乱序算子计算完毕但尚未提交的临时计算结果。在指令真正提交前，该值决不能直接冲入架构寄存器堆。
- **`done` 标记**：执行完成标志位。初始置为 `False`；当执行单元完成运算并通过结果总线回传时，对应 ROB 项的 `done` 位置为 `True`。
- **双指针环形拓扑**：`tail` 指针由 Decode 阶段按程序顺序推进，负责入队；`head` 指针由 Commit 阶段按程序顺序推进，负责出队提交。

### 5.2 Decode/Rename 阶段

在译码阶段，硬件查阅寄存器重命名映射表（Rename Map Table, RMT），将架构寄存器名字解耦：

```bsv
rule decode;
    // 1. 查当前寄存器映射表 (rename map)：src → 最新 ROB 项编号 or 架构 RF
    // 2. 分配新 ROB 项（tail），将 dst 映射到该项
    // 3. 将指令和操作数发射到执行保留站
    rob[tail] <= ROBEntry{archDst: dInst.dst, done: False, ...};
    tail <= tail + 1;
endrule
```

**重命名与依赖消除机理**：
- **WAR/WAW 名字依赖消除**：若后续指令写入同一寄存器，硬件直接在 RMT 中将其重命名为新的 `tail` 项。先前的指令依然保留旧的 ROB 编号，各指令的写操作完全解耦到不同的物理条目中。
- **操作数捕获机制**：源操作数若在 RMT 中显示已被重命名为某个 ROB 槽位且尚未 `done`，则该指令进入保留站时仅记录该 ROB 标记（Tag），进入休眠等待广播唤醒。

### 5.3 Commit 阶段

提交阶段是乱序核心对外部世界的唯一同步窗口，负责维持冯·诺依曼串行执行语义：

```bsv
rule commit (rob[head].done);
    let entry = rob[head];
    rf.wr(entry.archDst, entry.result);  // 写回架构 RF
    head <= head + 1;
endrule
```

**顺序提交与精确状态沉淀**：
- **严格队首判定**：`commit` 规则的守护条件是 `rob[head].done`。即便处于队列中部的后续指令已经乱序计算完毕，只要处于队首的最老指令（`head`）尚未完成（例如正在等待长延迟访存），所有后续指令的提交动作全部挂起。
- **原子状态生效**：一旦队首指令完成，其结果被真正写入架构寄存器堆（Architectural Register File），指令安全退出流水线。

::: theorem 推论 — 精确中断的实现
当异常发生时（如访存错误），ROB 头部提交到异常指令处停止，尚未提交的指令被丢弃（ROB 清空），处理器状态恢复到精确的程序顺序点，再跳入中断处理程序。乱序执行仍然对软件完全透明。
:::

---

## 6. 乱序执行性能示例

::: example 例题 — 乱序 vs. 顺序执行

:::

```text
i1: lw  r1, 0(r0)   # 缓存缺失，延迟 200 周期
i2: add r3, r4, r5  # 无依赖
i3: add r6, r7, r8  # 无依赖
```

顺序发射（计分板）：i2、i3 因 i1 缺失停顿 → 约 202 周期
乱序执行（ROB）：i2、i3 在 i1 缺失期间继续执行 → 约 200 周期（i2/i3 仅需 1 周期）

Sol：乱序执行将无关指令的延迟隐藏在缓存缺失等待中，IPC 大幅提升。

## 核心机制小结与动态调度权衡

乱序执行消除伪依赖（WAR/WAW），通过寄存器重命名允许无关指令绕过停顿指令执行；ROB 按程序顺序提交，保证精确中断语义；现代高性能处理器（Intel Core, AMD Zen, Apple M 系列）均采用乱序 + ROB 设计，ROB 项数可达 256–512 条。

## 核心机制思考与底层洞察

::: insight 数据流激进调度与冯·诺依曼串行表象的精妙调和
乱序超标量处理器的核心成就，在于以极具创造性的微架构工程化解了“数据流并发”与“精确顺序语义”之间的世纪矛盾：

1. **执行核心的纯粹数据流本质**：在保留站与重命名映射表的驱动下，处理器的物理执行单元（ALU, FPU, AGU）本质上退化为一个个由操作数就绪信号驱动的纯数据流机（Dataflow Engine）。指令不再受程序代码物理排布顺序的束缚，只要源操作数被公共总线（CDB）广播点亮，硬件就会在下一个时钟周期立即激进点火执行。这种激进的动态调度最大限度地将程序的隐式指令级并行度（ILP）彻底榨取出来。
2. **ROB 维护的确定性串行幻象**：纯数据流机在历史上未能在通用计算领域取得统治地位，致命短板在于它无法向操作系统和程序员交付一个确定、精确的异常发生点。重排序缓冲区（ROB）在此充当了严格的纪律维护者：无论内部算子的执行次序如何混乱跳跃，状态对架构寄存器和内存的最终沉淀必须在 ROB 头（`head`）以绝对的单列顺序逐一发生。这种“内部彻底乱序、外部绝对顺序”的二元分离架构，既释放了硅片极限的并发吞吐，又保全了软件生态赖以生存的确定性图灵机模型。
:::
