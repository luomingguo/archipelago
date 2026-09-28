---
title: 多线程处理器
type: lecture
lecture: 10
tags: [hardware-multithreading, fgmt, cgmt, smt, barrel-processor]
status: complete
---
# Lec 10 多线程处理器

## TL;DR

- 硬件多线程通过在单个处理器核心内维护多套体系结构上下文，利用线程间并发隐藏高昂的访存与停顿延迟。
- 细粒度多线程（FGMT/桶形处理器）每周期轮询切换线程，彻底消除级间 RAW 数据冒险与旁路转发开销。
- 粗粒度多线程（CGMT）仅在发生长周期缺失事件时触发上下文切换，以极低的控制成本换取吞吐收益。
- 同时多线程（SMT/超标量超线程）允许同周期混合发射来自多个线程的独立指令，最大限度榨干执行单元算力。

> MIT 6.1920 · Constructive Computer Architecture
> 讲师：Arvind · 日期：2024-03-14

## 1. 多线程的动机

::: definition
**定义 — 硬件线程（*Hardware Thread*）**

硬件线程（*HW thread*）是处理器中独立维护一套体系结构状态（PC、寄存器堆、页表基址）的执行流。多个 HW 线程共享同一流水线的计算资源（ALU、缓存）和物理内存（通过虚拟内存隔离）。
:::

**单线程流水线的利用率问题**：缓存缺失时流水线停顿，硬件空闲 100–1000 个周期。多线程让其他线程的指令填补这些空洞。

---

## 2. 细粒度多线程（*Fine-Grained Multithreading, FGMT*）

::: definition
**定义 — 桶形处理器（*Barrel Processor*）**

FGMT 的极端形式：每个时钟周期轮流执行不同线程的指令（*round-robin*），流水线中没有两条来自同一线程的指令，因此绝对不存在 RAW 数据冒险（相邻指令来自不同线程）。
:::

**状态复制与微架构资源解耦**：
在细粒度多线程中，各硬件线程各自拥有独立的架构状态存储（包括私有的 PC 数组 `pc_per_thread` 与独立寄存器堆），但共享同一套取指、译码与执行数据通路：

```bsv
Reg#(ThreadId) curThread <- mkReg(0);  // 轮询计数

rule fetch;
    let pc = pc_per_thread[curThread];
    iMem.enq(pc);
    f2d.enq(F2D{thread: curThread, pc: pc, ...});
    pc_per_thread[curThread] <= pc + 4;
    curThread <= (curThread + 1) % numThreads;  // 轮换
endrule
```

**每线程独立队列与零冒险调度**：
- **天然规避 RAW 冒险**：由于每个时钟周期 `curThread` 强制轮询步进，进入流水线相邻级的指令属于不同线程，彼此之间没有任何数据相关性。若物理线程总数大于或等于流水线级数（$N_{threads} \ge N_{stages}$），当同一线程的下一条指令进入流水线时，该线程前一条指令必然已经完成写回。微架构不仅无需计分板（Scoreboard）产生停顿，甚至可以彻底拆除所有级间前向旁路（Forwarding Network），极大地简化了硬件布线。
- **独立队列隔离**：译码到执行采用线程专属的级间队列阵列，避免单线程阻塞阻碍其他线程推进：

```bsv
// Decode → Execute：按线程分队列
FIFO#(D2E) d2e_per_thread[numThreads] <- replicateM(mkPipelineFIFO);

rule execute;
    let tid = ...; // 从 d2e_per_thread 中选
    let x = d2e_per_thread[tid].first;
    ...
endrule
```

---

## 3. 粗粒度多线程（*Coarse-Grained Multithreading, CGMT*）

::: definition
**定义 — 粗粒度多线程（*CGMT*）**

一个线程持续执行直到遭遇长延迟事件（缓存缺失、I/O），此时切换到另一线程。每次切换需要冲刷流水线（*pipeline flush*），但切换频率低，适用于延迟较大（数百周期）的事件。
:::

优点：不需要针对每个周期都轮换；缺点：切换开销（flush），短暂停顿（< 切换开销）无法被隐藏。

---

## 4. 同时多线程（*Simultaneous Multithreading, SMT*）

::: definition
**定义 — SMT（*Simultaneous Multithreading*）**

SMT 在超标量处理器的基础上，每周期从多个线程中混合发射指令，充分利用超标量宽度。Intel 的*Hyper-Threading* 技术（HT）即为 2-way SMT：一个物理核心对操作系统呈现为 2 个逻辑核心。
:::

**SMT vs. FGMT 对比**：

| 维度 | FGMT | SMT |
|------|------|-----|
| 每周期发射 | 1 条（来自轮换线程）| 多条（来自多线程混合）|
| RAW 冒险 | 无（天然隔离）| 需计分板 |
| 硬件复杂度 | 低 | 高 |
| 适用场景 | GPU shader、嵌入式 | 现代服务器 CPU |

---

## 5. 虚拟内存简介

::: definition
**定义 — 虚拟内存（*Virtual Memory*）**

虚拟内存为每个线程（进程）提供独立的地址空间（*virtual address space*）。虚拟地址通过 TLB（*Translation Lookaside Buffer*，页表缓存）翻译为物理地址。多线程共享物理内存，但互不干扰（隔离），也可显式共享页面（进程间通信）。
:::

**TLB 缺失代价**：TLB 缺失需要访问页表（多级，数百周期），是 CGMT/SMT 的重要触发事件。

---

## 6. 多线程的资源分配

::: example 例题 — 多线程提升吞吐量

:::

假设单线程因缓存缺失，50% 的周期流水线空转：

- 1 个线程：利用率 50%
- 2 个线程（FGMT）：线程 1 停顿时线程 2 执行，理论利用率 → 100%

Sol：需要 $\lceil 1/\text{miss\_rate} \rceil$ 个线程才能完全隐藏延迟。对于 90% 命中率（10% 缺失率），需约 10 个线程。

::: theorem 推论 — 多线程不降低单线程延迟
多线程提高**吞吐量**（更多线程合计完成更多工作），但并不降低单条线程的延迟（因为每个线程分到的执行带宽减少）。数据中心场景（高并发服务器）受益最大。
:::

---

## 核心机制小结与多线程范式权衡

FGMT（桶形处理器）每周期轮换线程，天然消除 RAW 冒险，BSV 实现只需按线程分离寄存器状态；CGMT 在长延迟事件时切换线程；SMT 结合超标量宽度每周期混合多线程指令；虚拟内存通过 TLB 隔离各线程地址空间。多线程的核心价值是以面积换吞吐量。

## 核心机制思考与底层洞察

::: insight 延迟隐藏与延迟最小化的体系结构哲学分水岭
硬件多线程揭示了现代计算机体系结构在应对“内存墙（Memory Wall）”时两条截然不同的工程哲学路线：

1. **CPU 路线：延迟最小化（Latency Minimization）**：通用 CPU 致力于让单条线程以极限速度跑完。为此，设计者不惜耗费海量晶体管堆砌多级乱序执行窗口、巨型分支预测树、昂贵的动态旁路网络以及多级庞大缓存。其代价是极高的功耗和极其复杂的控制逻辑，一旦遭遇冷缓存缺失或不可预测分支，整个庞大核心依然可能陷入数百周期的冰冻。
2. **GPU / 桶形处理器路线：延迟隐藏（Latency Hiding）**：细粒度多线程（FGMT）和现代 GPU（Warp 调度器）彻底放弃了“拯救单线程延迟”的执念。它们砍掉了复杂的推测执行和前向旁路，转而将节省下来的硅片面积用于**大批量复制物理寄存器上下文**。当一个线程因为访存缺失挂起时，硬件调度器以零周期开销瞬间切换到下一个就绪线程继续喂饱 ALU。这种设计以单个任务的响应延迟换取芯片整体吞吐量的极致饱和，成为高吞吐量图形渲染与深度学习加速器的终极理论基石。
:::
