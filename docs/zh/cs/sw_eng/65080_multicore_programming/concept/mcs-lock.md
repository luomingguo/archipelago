---
title: MCS 队列锁
type: concept
tags: [mcs-lock, spin-lock, numa, cache-coherence]
status: complete
---

# MCS 队列锁（MCS Queue Lock）

## 问题情境

在非一致性内存访问（NUMA）多处理器架构中，每个 CPU 核心访问挂载在本地插槽上的物理内存速度极快，而访问远程节点物理内存则需要穿越互连网络，延迟高且占用公共互连带宽。如果使用 CLH 等前驱自旋锁，等待线程必须频繁轮询前驱线程所在的内存地址；若前驱节点恰好分配在远程 NUMA 节点上，即便只是只读自旋，也会在互连总线上产生持续的远程访问流量。如何在多核及多插槽大型系统上，实现每个等待线程只在**属于自己本地节点的物理内存变量**上自旋，彻底切断对远程内存的轮询依赖？

## 概念界定

::: definition MCS 队列锁（MCS Lock）
MCS 锁（由 John Mellor-Crummey 和 Michael Scott 提出）是一种基于显式单向链表的可扩展自旋队列锁。每个线程分配一个属于本地内存的节点 `QNode`，并**仅在自身节点的 `locked` 字段上自旋等待**。前驱线程在释放锁时，通过显式 `next` 指针主动将后继节点的 `locked` 置为 false，实现真正的本地自旋（Local Spinning）与对 NUMA 拓扑的深度免疫。
:::

## 解释与依据

MCS 锁针对 NUMA 硬件拓扑进行了专门的算法架构设计：

1. **本地内存节点与显式后继链接**：
   节点结构包含 `volatile boolean locked` 和 `volatile QNode next`。加锁线程在自身局部内存中分配 `qnode`，通过原子交换将自身置为全局 `tail`。若此前队列非空（即存在前驱 `pred != null`），线程将自身 `locked` 置为 `true`，并将前驱的后继指针确立：`pred.next = qnode`。
2. **纯本地内存自旋（Local Spinning）**：
   完成入队后，线程执行 `while (qnode.locked) {}`。由于 `qnode` 由当前线程分配在自身插槽的本地内存中，无论是具备还是缺乏缓存一致性的 NUMA 系统，自旋轮询都严格在本地物理内存或本地 L1 缓存中完成，对外部互连网络产生零轮询通信。
3. **两阶段竞争解锁（Two-Phase CAS Release）**：
   释放锁时，持有者需要将交接信号传递给后继节点：
   - *无后继场景*：若 `qnode.next == null`，持有者尝试执行 `tail.compareAndSet(qnode, null)`。若成功，说明期间确无新线程入队，直接成功退出。
   - *后继确立中场景*：若 CAS 失败，说明正有后继线程入队（已修改 tail），但尚未执行完 `pred.next = qnode`。此时释放线程在本地进行极短暂的等待自旋（`while (qnode.next == null) {}`），直至后继指针就绪。
   - *后继已确立场景*：直接执行 `qnode.next.locked = false`，单播唤醒后继。

::: insight MCS 的后继单播与架构透明性
MCS 锁的精妙之处在于其逆向设计：它不是让后继去打探前驱的意图，而是由前驱主动将控制权推送给后继。通过显式后继指针，它将数据写入与控制流的传递方向完全统一，使得自旋等待完全隔离在每个线程自己的内存领地之内。
:::

## 边界与辨析

- **适用条件**：
  大规模多核心、多插槽 NUMA 服务器系统；缺乏硬件全局缓存一致性的分布式或异构共享内存系统。
- **与 CLH 锁的边界对比**：
  - *自旋位置*：CLH 在前驱节点自旋（依赖缓存一致性将其拉入本地缓存）；MCS 在自身本地节点自旋（天然本地化，无论有无硬件缓存）。
  - *释放开销*：CLH 释放锁只需一次简单的变量赋值（`myNode.locked = false`）；MCS 释放锁涉及两阶段检查，在无后继或后继正在链接时需要执行 CAS 操作或微小等待。
  - *实现复杂度*：MCS 节点包含后继指针且存在并发链接阶段，实现与正确性证明比 CLH 稍繁琐。

## 提取与迁移

- **主动唤醒思考题**：
  1. *在 MCS 锁的 `unlock()` 中，为什么当 `qnode.next == null` 且 CAS 失败时，释放线程需要循环等待 `qnode.next == null`？这会导致死锁吗？*
     - **参考答案**：CAS 失败意味着有新线程执行了 `tail.getAndSet(qnode)`，新线程已经宣称了队尾，但尚未执行下一条指令 `pred.next = qnode`。释放线程等待的是这一条微观指令的完成（仅耗费几个 CPU 时钟周期），后继线程在此期间绝不会被阻塞，因此绝不会发生死锁。
  2. *Linux 内核的 qspinlock（排队自旋锁）是如何融合 MCS 锁思想并解决其指针空间开销问题的？*
     - **参考答案**：传统 MCS 锁需要为每个等待者存储指针，开销较大。Linux 内核采用了一种紧凑的编码机制，将 MCS 队列节点的 CPU 编号和排队层级紧凑编码进一个 32 位的原子整数中，兼顾了 MCS 的本地自旋抗 NUMA 竞争优势与自旋锁的极小内存占用（4 字节）。

## 关联与来源

- **讲义关联**：
  - 详见 [Lec 2 互斥锁与自旋同步](../lec2.md) 第 8 节“MCS 队列锁：本地内存自旋与显式后继链接”。
- **延伸概念**：
  - [CLH 队列锁](./clh-lock.md)：隐式前驱自旋队列锁。
- **学术来源**：
  - Mellor-Crummey, J. M., & Scott, M. L. (1991). *Algorithms for scalable synchronization on shared-memory multiprocessors*. ACM Transactions on Computer Systems (TOCS).

## TL;DR

- MCS 锁通过显式单向链表实现严格的 FIFO 排队，彻底杜绝自旋饥饿。
- 核心创新在于本地内存自旋（Local Spinning），每个线程仅在自身分配的本地节点标志上轮询，完全免疫 NUMA 架构的跨节点互连通信开销。
- 解锁采用两阶段验证，通过显式 `next` 指针单播唤醒后继，是大规模多核系统中经典的高性能队列锁。
