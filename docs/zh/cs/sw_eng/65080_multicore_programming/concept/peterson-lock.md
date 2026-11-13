---
title: Peterson 互斥锁
type: concept
tags: [peterson-lock, mutual-exclusion, spin-lock, concurrency]
status: complete
---

# Peterson 互斥锁（Peterson Lock）

## 问题情境

在多核编程的早期探索中，计算机科学家尝试仅使用常规的共享内存读写操作（不依赖硬件特殊原子指令）来解决双线程互斥问题。单纯基于意愿标志位的 LockOne 算法在并发时会由于双方同时举起标志而陷入死锁；单纯基于牺牲者让步的 LockTwo 算法在没有竞争并发时又会因为无法修改牺牲者而无法单独推进。如何在完全对称的并发世界中，用最简洁的纯软件逻辑打破僵局，构建一个既绝对互斥、又永不死锁和饥饿的双线程锁？

## 概念界定

::: definition Peterson 互斥算法（Peterson's Algorithm）
由 Gary L. Peterson 于 1981 年提出的双线程纯软件互斥锁算法。该算法将表示加锁意愿的布尔数组 `flag[2]` 与表示让步顺序的整数变量 `victim` 相结合。线程进入临界区前首先举起自己的标志，同时主动将自己登记为让步牺牲者；当且仅当“对方意图进入”且“自己仍是牺牲者”时自旋等待。Peterson 算法以极度简洁的代码同时严格保证了互斥性、死锁自由与饥饿自由。
:::

## 解释与依据

Peterson 算法的优雅在于其正交互补的状态约束机制：

```java
public class Peterson implements Lock {
    private final boolean[] flag = new boolean[2];
    private volatile int victim;

    public void lock() {
        int i = ThreadID.get();
        int j = 1 - i;
        flag[i] = true;  // 1. 举起意愿标志
        victim = i;      // 2. 礼让：自认牺牲者
        while (flag[j] && victim == i) {} // 双重条件等待
    }

    public void unlock() {
        int i = ThreadID.get();
        flag[i] = false; // 放下标志
    }
}
```

1. **反证法证明互斥性（Safety）**：
   假设两线程同时处于临界区 $CS_A \parallel CS_B$。不失一般性，设线程 A 是最后一个将自己写入 `victim` 的线程，即 $write_B(victim = B) \to write_A(victim = A)$。
   因为写入之后没有其他修改，A 在检查 `while` 循环时必定观测到 $victim == A$。
   如果 A 成功进入了临界区，说明 A 必定观测到 $flag[B] == false$。
   然而，线程 B 早在写入 $victim = B$ 之前就已经完成了 $write_B(flag[B] = true)$。
   综合偏序关系可得：$write_B(flag[B] = true) \to read_A(flag[B] == false)$。在 B 退出临界区前 $flag[B]$ 恒为 true，因此 A 绝不可能读到 false，假设推导出矛盾，互斥性成立。
2. **反证法证明无饥饿性（Liveness）**：
   假设线程 A 无限饥饿，则必有 $flag[B] == true$ 且 $victim == A$。
   若线程 B 未在临界区内，其必已调用 `unlock()` 将 $flag[B]$ 置为 false，A 随即进入；
   若线程 B 重复进入临界区，B 每次加锁必会执行 $victim = B$。此时 `victim` 变为 B 且不会被 A 再次覆盖，A 的等待条件 $victim == A$ 瞬间被打破并立即返回。因此系统保证无死锁与无饥饿。

::: insight 标志位与牺牲者的阴阳对称哲学
LockOne 表达的是“自私”（宣布自我意愿），LockTwo 表达的是“利他”（让对方先行）。两者单独使用均存在死锁奇点；而 Peterson 算法精妙地将二者串联——先宣布自己的意图，再将优先权拱手礼让给对方。正是这种“先宣示、后礼让”的时序打破了并发对称性，以最少的状态空间达成了无死锁的平衡。
:::

## 边界与辨析

- **线程数限制**：
  原始 Peterson 算法严格只适用于 $n = 2$ 个线程。推广到 $n > 2$ 个线程时，必须使用包含 $n-1$ 层排他等待室的过滤锁（Filter Lock）。
- **硬件内存重排陷阱**：
  在现代乱序执行与弱内存模型的 CPU（如 x86-64 或 ARM）上，指令重排（Store-Load Reordering）可能使 `victim = i` 先于 `flag[i] = true` 写入主内存。因此在实际工程中，必须配合内存屏障（如 Java 的 `volatile` 或 C++ 的 `std::memory_order_seq_cst`）来阻止指令重排。
- **空间开销瓶颈**：
  依据下界理论，纯读写互斥锁拓展到 $n$ 线程必须消耗 $\Omega(n)$ 个内存位置，难以应对大规模并发核心，因而被现代基于硬件 CAS 的自旋队列锁取代。

## 提取与迁移

- **主动唤醒思考题**：
  1. *如果将 Peterson 锁的加锁顺序颠倒，先执行 `victim = i` 再执行 `flag[i] = true`，算法还能保证互斥性吗？*
     - **参考答案**：不能。若顺序颠倒，线程 A 写入 $victim = A$ 后，线程 B 紧接着写入 $victim = B$。随后 B 写入 $flag[B] = true$ 并进入临界区（因为 $victim == B$ 已不成立）。此时 A 才写入 $flag[A] = true$，A 检查到 $victim == B$ 也直接进入临界区，互斥性彻底瓦解。
  2. *为什么 Peterson 算法在单核处理器上无需担心死锁，但在多核现代 CPU 上必须声明 `volatile`？*
     - **参考答案**：现代超标量 CPU 具有 Store Buffer，常规写入不会立即刷新至 L1 缓存或总线。如果不使用 `volatile`，读操作可能从 Store Buffer 中提前旁路读取，破坏了算法赖以证明成立的偏序时间关系链。

## 关联与来源

- **讲义关联**：
  - 详见 [Lec 2 经典互斥算法与数学证明](../lec2.md) 第 3 节“Peterson 锁”。
- **延伸概念**：
  - [线性化](./linearizability.md)：并发操作正确性的形式化基石。
  - [CLH 队列锁](./clh-lock.md)：基于硬件原子指令的可扩展自旋锁。
- **学术来源**：
  - Peterson, G. L. (1981). *Myths about the mutual exclusion problem*. Information Processing Letters, 12(3), 115-116.

## TL;DR

- Peterson 算法通过意愿标志数组与牺牲者变量的组合，实现了首个双线程纯软件无死锁、无饥饿互斥。
- 依赖“先宣示意愿、后礼让对方”的时序打破对称性，通过严密的反证法证明其安全性。
- 仅适用于双线程且依赖顺序一致性内存模型；在多核弱内存架构下必须显式施加内存屏障。
