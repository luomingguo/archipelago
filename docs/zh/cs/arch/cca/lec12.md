---
title: 同步与顺序一致性
type: lecture
lecture: 12
tags: [sequential-consistency, memory-models, tso, memory-barriers, lr-sc]
status: complete
---
# Lec 12 同步与顺序一致性

## TL;DR

- 顺序一致性（SC）要求多处理器执行等价于全局单串行交错序，且各核内部严格保持程序顺序。
- 存储缓冲区（Store Buffer）允许写操作异步排队，引入了 Store-Load 重排序并导致全存储定序（TSO）对 SC 的偏离。
- 内存屏障（Fence）通过排空本地存储缓冲区与阻断流水线重排，按需恢复临界区的数据可见性顺序。
- RISC-V 采用 Load-Reserved / Store-Conditional（LR/SC）指令对构造无锁原子原语（TAS/CAS），支撑高效自旋锁。

> MIT 6.1920 · Constructive Computer Architecture
> 讲师：Arvind · 日期：2024-03-26

## 1. 生产者-消费者同步问题

::: definition
**定义 — 同步（*Synchronization*）**

多线程程序中，当线程 A 生产数据、线程 B 消费数据时，B 必须等到 A 完成写入后才能读取，否则读到无效数据。同步机制确保线程间的执行顺序约束。
:::

**锁（*Lock*）的基本用法**：

```c
// 线程 A（生产者）
data = compute();
lock_release(&lock);   // 发布数据

// 线程 B（消费者）
lock_acquire(&lock);   // 等待数据就绪
use(data);
```

---

## 2. 原子操作（*Atomic Operations*）

普通 load/store 组合不是原子的（存在竞态条件），需要专用硬件指令：

::: definition
**定义 — Test-and-Set / Swap（*原子交换*）**

`TAS(addr)`：原子地读取地址 addr 的旧值，并写入 1，返回旧值。若旧值为 0（锁未占用），则当前线程获得锁；若旧值为 1，则自旋等待。

`SWAP(addr, val)`：原子地将 val 写入 addr，返回旧值。
:::

RISC-V 实现（LR/SC，*Load-Reserved / Store-Conditional*）：

```asm
lock_acquire:
    lr.w  t0, (a0)        # Load-Reserved：读锁，设监控位
    bnez  t0, lock_acquire # 锁被占用，自旋
    li    t1, 1
    sc.w  t1, t1, (a0)    # Store-Conditional：若监控位仍有效则写
    bnez  t1, lock_acquire # sc 失败（被抢占），重试
    ret
```

---

## 3. 顺序一致性（*Sequential Consistency, SC*）

::: definition
**定义 — 顺序一致性（*Lamport, 1979*）**

多处理器系统是*顺序一致的*，当且仅当：任意执行的结果，等价于所有处理器的操作按某个全局顺序（*total order*）交织执行，且每个处理器内的操作保持程序顺序（*program order*）。
:::

**SC 的两个条件**：
1. 每个处理器内部的操作按程序顺序执行
2. 内存操作是原子的（所有处理器同时看到相同的写结果）

**SC 违反示例**：

```text
初始：x = 0, y = 0
P1: x = 1; r1 = y;
P2: y = 1; r2 = x;
```

SC 保证：不可能出现 r1 = 0 且 r2 = 0（至少一个读到另一方的写）。

---

## 4. TSO 内存模型（*Total Store Order*）

::: definition
**定义 — TSO（*Total Store Order*）**

TSO 是 x86 和 SPARC 使用的放松内存模型：每个处理器有一个 FIFO Store 缓冲区（*store buffer*），Store 先进 STB 再异步写入共享内存。Load 先查自己的 STB，不命中再访问共享内存。</br>
TSO 允许后面的 Load 超越前面的 Store（Store-Load 重排序）。
:::

**TSO 违反 SC 的场景**：

```text
初始：x = 0, y = 0
P1: store x=1（进 STB，未写内存）; load y（读内存得 0）; r1=0
P2: store y=1（进 STB，未写内存）; load x（读内存得 0）; r2=0
结果：r1=0 且 r2=0 ← 在 SC 下不可能，但在 TSO 下可能！
```

---

## 5. 内存屏障（*Memory Fence*）

::: definition
**定义 — 内存屏障（*Memory Fence / Barrier*）**

内存屏障指令强制处理器在继续执行后续访存操作之前，先将 Store Buffer 中所有 pending 的 Store 写入共享内存（对 StoreLoad 屏障），或保证 Load 的全局可见性。RISC-V 使用 `fence` 指令。
:::

**RISC-V fence 语法**：

```asm
fence predecessor, successor
# predecessor: 屏障前的操作类型（r=load, w=store, rw=both）
# successor:   屏障后的操作类型
fence rw, rw   # 全屏障（最强，保证前后所有访存不重排）
fence r, r     # FenceLL（Load-Load 屏障）
fence w, w     # FenceSS（Store-Store 屏障）
```

修正 TSO 场景：

```asm
store x, 1
fence w, r     # 强制 store 刷新到内存后再 load
load r1, y
```

---

## 6. 锁实现对内存模型的依赖

::: example 例题 — 锁释放需要屏障吗？

:::

在 TSO 模型下：

```c
// 线程 A
data = 42;          // store data（进 STB）
lock = 0;           // store lock=0（进 STB）
// 若 STB 未立即刷新，线程 B 可能看到 lock=0 但 data 还是旧值！
```

Sol：`lock_release` 必须在 `store lock` 之前加 `fence w, w`（Store-Store 屏障），保证 data 写入先于 lock 的释放对所有核可见。

::: theorem 推论 — 内存模型越放松，性能越高但编程越复杂
SC 最简单但限制了 Store Buffer 等硬件优化；TSO 允许 Store Buffer 提升性能，但程序员/编译器必须在关键点插入 fence；ARMv8 的 RISC 内存模型更弱，需要更多 fence，但可获得更高并行度。
:::

## 核心机制小结与内存一致性权衡

顺序一致性（SC）是最直观的多处理器内存模型；TSO 通过 Store Buffer 提升性能但破坏 SC；内存屏障在必要时强制操作有序完成；LR/SC 原子对实现无锁正确的 mutex；了解内存模型对编写正确的多线程程序（无数据竞争）至关重要。

## 核心机制思考与底层洞察

::: insight 顺序一致性的理想假象与物理分布式的残酷现实
顺序一致性（SC）是程序员最渴望的心智模型，但在现代多核物理芯片上，强行维系 SC 是一场灾难性的性能妥协：

1. **共享存储器的非集中物理现实**：在逻辑抽象中，存储器仿佛是一个连接在单根无延迟总线上的全局单点。然而在真实的超标量多核处理器中，每个核心都配备了私有的写缓冲队列（Store Buffer）、非阻塞 L1/L2 缓存以及复杂的片上互连网络（NoC）。一次写操作从进入本地缓冲区到广播通知所有远端核心使旧缓存行失效，需要经历跨越芯片物理距离的漫长时钟周期。
2. **强制 SC 对微架构并发的毁灭性打击**：如果严格遵守 Lamport 的 SC 规范，CPU 在执行 Store 指令后，必须彻底暂停流水线并等待写数据在全芯片所有核上达成全局可见性确认，才能发射后续的任何 Load 操作。这相当于直接把数 GHz 的超标量乱序核心瞬间降速到微秒级片上互联的最慢往返延迟。
3. **弱内存模型的工程救赎**：TSO、Release Consistency 以及 RISC-V 弱内存模型的本质，是**将物理分布式的通信延迟如实向软件暴露**。硬件被允许在本地安全的前提下激进重排序访存操作（如让 Load 超越尚未刷入主存的 Store）；而当软件确实需要发布数据跨核同步时，再通过显式插入 `fence` 屏障指令，为特定的关键路径局部支付等待代价。这种“默认最大化物理并发，按需局部同步”的分离设计，构成了现代高性能多核架构的灵魂。
:::
