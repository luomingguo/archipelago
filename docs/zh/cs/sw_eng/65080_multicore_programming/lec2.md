---
title: 经典互斥算法与数学证明
type: lecture
lecture: 2
tags: [mutual-exclusion, peterson-lock, filter-lock, bakery-algorithm, lower-bounds]
status: complete
---

# Lec 2 经典互斥算法与数学证明（Classical Mutual Exclusion Algorithms）

## TL;DR

- 并发执行的时间本质由事件区间的偏序关系（$I_A \to I_B$）定义，无法由偏序定序的区间即构成并发。
- 经典两线程互斥中，LockOne 满足互斥但存在并发死锁，LockTwo 满足互斥但存在交替饥饿；Peterson 锁将二者精妙结合，实现了首个无死锁、无饥饿的严密互斥证明。
- 过滤锁（Filter Lock）通过 $n-1$ 层排他筛选与牺牲者机制将 Peterson 推广至任意 $n$ 线程。
- 兰伯特面包店算法（Lamport's Bakery Algorithm）通过分布式取号与字典序排队，奠定了首个具备先来先服务（FIFO）门厅公平性的 $n$ 线程锁。
- 覆盖状态定理严格证明：任何仅基于常规读写内存的 $n$ 线程无死锁互斥算法，必须占用至少 $\Omega(n)$ 个独立内存位置；这一理论下界直接驱动了现代硬件 RMW 原子指令的诞生。

## 时间、事件与偏序关系形式化

推理并发程序本质上是在对时间关系进行严谨推理。在多核异步环境中，不同线程的指令交错执行，我们必须引入精确的数学符号与语义模型来界定并发行为。

### 事件与时间区间

- **线程作为状态机**：每个线程被建模为一个顺序状态机，其状态跃迁被称为**事件（Event）**；
- **事件的瞬时性**：事件在时间轴上是瞬时的（Instantaneous）。在模型中，我们规定不同的事件发生在不同的离散时间点；若两事件物理间隔极短而无法测定先后，数学上可任意指定一个确定顺序；
- **符号表示**：设 $a_0, a_1$ 为某线程执行过程中的两个先后事件，记作 $a_0 \to a_1$（读作“$a_0$ 先于 $a_1$”）。事件 $a_0$ 到 $a_1$ 持续的时间范围构成了**时间区间（Time Interval）**：
  $$I = (a_0, a_1)$$
- **区间先于关系**：设区间 $I_A = (a_0, a_1)$，区间 $I_B = (b_0, b_1)$。当且仅当事件 $a_1 \to b_0$ 时，我们称区间 $I_A$ 严格先于区间 $I_B$，记作：
  $$I_A \to I_B$$
- **并发的数学定义**：区间上的先于关系 $\to$ 构成了一个严格偏序（Partial Order）。如果两个时间区间 $I_A$ 与 $I_B$ 之间既不存在 $I_A \to I_B$，也不存在 $I_B \to I_A$，则两区间在时间轴上存在物理重叠，称 $I_A$ 与 $I_B$ **并发（Concurrent）**，记作 $I_A \parallel I_B$。

## 临界区问题与三大判定准则

临界区（Critical Section, CS）是指一段在同一时刻至多只能被一个线程执行的代码区块。协调各线程访问临界区的行为称为互斥（Mutual Exclusion）。

一个严格正确的互斥锁算法必须满足以下三大特性：

1. **互斥性（Mutual Exclusion / Safety）**：
   - 设 $CS_A^k$ 与 $CS_B^m$ 分别代表线程 A 的第 $k$ 次临界区执行与线程 B 的第 $m$ 次临界区执行。互斥性要求任意两不同线程的临界区区间绝不并发：
     $$\forall A \neq B, \quad CS_A^k \to CS_B^m \quad \lor \quad CS_B^m \to CS_A^k$$
2. **死锁自由（Freedom from Deadlock / Liveness）**：
   - 若有线程试图获取锁，则必定有某个线程能够成功获取并退出锁。如果一个线程调用 `lock()` 或 `unlock()` 且永不返回，其他线程仍能无限次完成加锁与解锁操作。
3. **饥饿自由（Freedom from Starvation / Strong Liveness）**：
   - 每一个调用 `lock()` 的线程最终都能进入临界区并返回。饥饿自由直接蕴含了死锁自由。

## 双线程互斥算法演进与反证法证明

为了清晰展示互斥算法的设计思考，我们首先考察只有两个线程（ID 分别为 0 和 1）的场景。

### 1. LockOne 算法：基于标志位的互斥尝试

LockOne 算法为每个线程设置一个意愿标志位 `flag[i]`，加锁时举起自己的标志，并等待对方放下标志。

```java
public class LockOne implements Lock {
    private final boolean[] flag = new boolean[2];

    public void lock() {
        int i = ThreadID.get();
        int j = 1 - i;
        flag[i] = true; // 声明自己意图进入临界区
        while (flag[j]) {} // 自旋等待对方退出
    }

    public void unlock() {
        int i = ThreadID.get();
        flag[i] = false; // 离开临界区，放下标志
    }
}
```

::: theorem LockOne 满足互斥性
**反证法证明**：
假设互斥性不成立，即存在物理重叠的临界区 $CS_A \parallel CS_B$。
考察线程 A 和 B 在进入各自临界区之前最后一次执行的读写指令事件序列：
$$write_A(flag[A] = true) \to read_A(flag[B] == false) \to CS_A$$
$$write_B(flag[B] = true) \to read_B(flag[A] == false) \to CS_B$$
注意，当线程 B 将 $flag[B]$ 设为 true 后，该标志将一直维持为 true 直至其退出 $CS_B$。由于临界区重叠，A 读取 $flag[B] == false$ 的事件必定发生在 B 写入 $flag[B] = true$ 之前：
$$read_A(flag[B] == false) \to write_B(flag[B] = true)$$
同理，B 读取 $flag[A] == false$ 必须发生在 A 写入 $flag[A] = true$ 之前：
$$read_B(flag[A] == false) \to write_A(flag[A] = true)$$
将上述偏序关系链接：
$$write_A(flag[A] = true) \to read_A(flag[B] == false) \to write_B(flag[B] = true) \to read_B(flag[A] == false) \to write_A(flag[A] = true)$$
由此推导出 $write_A(flag[A] = true) \to write_A(flag[A] = true)$，在偏序关系上形成有向环，产生逻辑矛盾。因此假设不成立，LockOne 严格保证互斥性。
:::

::: pitfall LockOne 的致命死锁缺陷
尽管 LockOne 满足互斥性，但它**不满足死锁自由**。若线程 A 与线程 B 同时启动并交错执行：
$$write_A(flag[A] = true) \to write_B(flag[B] = true) \to read_A(flag[B] == true) \to read_B(flag[A] == true)$$
双方均举起标志且同时检测到对方为 true，两线程将在 `while` 循环中无限期自旋等待对方让步，系统彻底死锁。
:::

### 2. LockTwo 算法：基于牺牲者让步的互斥尝试

LockTwo 算法另辟蹊径：引入一个公共的 `victim`（牺牲者）变量。每个线程在加锁时将自己标记为牺牲者（礼让对方先行），并等待 `victim` 不再等于自己。

```java
public class LockTwo implements Lock {
    private volatile int victim;

    public void lock() {
        int i = ThreadID.get();
        victim = i; // 礼让：自认牺牲者，让对方先行
        while (victim == i) {} // 如果自己仍是牺牲者，自旋等待
    }

    public void unlock() {}
}
```

::: theorem LockTwo 满足互斥性
**反证法证明**：
假设临界区重叠 $CS_A \parallel CS_B$。进入临界区前各事件必须满足：
$$write_A(victim = A) \to read_A(victim == B) \to CS_A$$
$$write_B(victim = B) \to read_B(victim == A) \to CS_B$$
在事件 $write_A(victim = A)$ 与 $read_A(victim == B)$ 之间，B 必须执行过写入使得 $victim = B$；同理，A 必须在 B 写入后再次写入才能使 B 观测到 $victim = A$。单个物理变量的最后一次写入具有全局确定顺序，不可同时出现“A 后于 B 写”且“B 后于 A 写”，产生矛盾。故互斥性成立。
:::

::: pitfall LockTwo 的非并发死锁缺陷
LockTwo 具有一个怪异的性质：只有在两个线程真正发生并发冲突时，后写入的线程将前者的牺牲者身份覆盖，前者才能跳出循环成功进入临界区。若只有一个线程独占运行，它将自己置为牺牲者后，永远无法跳出 `victim == i` 的检查，从而陷入死锁。
:::

### 3. Peterson 锁：经典的双线程完美互斥

1981 年，Gary Peterson 提出将 LockOne 的“意愿标志位”与 LockTwo 的“牺牲者让步”精妙融合，创造出了计算机科学史上最著名的双线程无饥饿互斥算法——**Peterson 锁**。

```java
public class Peterson implements Lock {
    private final boolean[] flag = new boolean[2];
    private volatile int victim;

    public void lock() {
        int i = ThreadID.get();
        int j = 1 - i;
        flag[i] = true;  // 1. 声明自己的加锁意愿 (LockOne)
        victim = i;      // 2. 礼让对方先行 (LockTwo)
        // 只有当对方想进 且 自己是牺牲者时才等待
        while (flag[j] && victim == i) {}
    }

    public void unlock() {
        int i = ThreadID.get();
        flag[i] = false; // 退出临界区，撤销意愿
    }
}
```

::: theorem Peterson 算法满足互斥性与无饥饿性
**互斥性证明**：
假设 $CS_A \parallel CS_B$。不失一般性，假设线程 A 是最后一个写入 `victim` 的线程：
$$write_B(victim = B) \to write_A(victim = A)$$
由于 A 是最后写入者，当 A 执行到 `while` 条件时，它必观测到 $victim == A$。
然而 A 仍然成功进入了临界区，唯一可能是 A 观测到 $flag[B] == false$。
此时由于 B 试图进入临界区，早已执行过 $write_B(flag[B] = true)$。
将偏序链条连接：
$$write_B(flag[B] = true) \to write_B(victim = B) \to write_A(victim = A) \to read_A(flag[B] == false)$$
由此导出 $write_B(flag[B] = true) \to read_A(flag[B] == false)$。在没有其他线程将 $flag[B]$ 置为 false 的前提下，A 绝不可能读到 false，矛盾！故互斥性成立。

**无饥饿性证明**：
假设线程 A 在 `while` 中无限饥饿。这意味着必定持续满足 $flag[B] == true$ 且 $victim == A$。
如果线程 B 不在临界区内，它必已执行 `unlock()` 将 $flag[B]$ 置为 false，A 随即退出循环；
如果线程 B 频繁进出临界区，B 每次重新进入 `lock()` 时必会执行 $victim = B$。由于没有其他线程修改，`victim` 将被固化为 B，从而打破 A 的等待条件 $victim == A$。因此 A 必在有限步内获得锁，保证无饥饿性。
:::

## 过滤锁（Filter Lock）：拓展至 n 线程的互斥算法

为了将 Peterson 锁推广到任意 $n$ 个线程（$n > 2$），Peterson 提出了**过滤锁（Filter Lock）**。

### 核心设计机理

过滤锁在临界区之前建立了 $n - 1$ 个排他等待室，称为**级别（Levels）**，标记为 $0$ 到 $n-1$：
- 线程最初位于 Level 0，进入 Level $n-1$ 即代表正式进入临界区；
- 每个级别具有两个核心属性：
  1. 至少有一个试图进入 Level $\ell$ 的线程能够成功通过；
  2. 若有多个线程试图进入 Level $\ell$，则至少有一个线程被阻挡在该级别充当牺牲者。

![过滤器锁（Filter Lock）的 n-1 层排他级别与 victim 状态转移图](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66f56dd623f0a.png)

### 代码实现

在过滤锁的数据结构组织中：
- 数组 `level[n]` 记录每个线程当前所处的最高排他级别，初始全为 0。当线程成功晋升到 Level $n-1$ 时，即标志着其获得了临界区的独占执行权；
- 数组 `victim[n]` 为每个排他级别（索引从 1 到 $n-1$）设立了一个牺牲者指针。与 Peterson 锁类似，进入该级别的线程会将自身标记为当前层的牺牲者；
- 外层循环 `for (int i = 1; i < n; i++)` 驱动线程层层攀登，每次攀登必须通过内层自旋检查，确保在任何冲突发生时本级别至多只有部分线程能成功晋级。

```java
public class Filter implements Lock {
    private final int[] level;
    private final int[] victim;
    private final int n;

    public Filter(int n) {
        this.n = n;
        this.level = new int[n];
        this.victim = new int[n]; // 使用索引 1 到 n-1
    }

    public void lock() {
        int me = ThreadID.get();
        for (int i = 1; i < n; i++) {
            level[me] = i;
            victim[i] = me;
            // 当存在其他线程在当前层或更高层，且自己依然是当前层的牺牲者时，自旋等待
            for (int k = 0; k < n; k++) {
                while (k != me && level[k] >= i && victim[i] == me) {}
            }
        }
    }

    public void unlock() {
        int me = ThreadID.get();
        level[me] = 0; // 退出所有级别
    }
}
```

在上述算法执行中，每一层等待室都在执行一次微型的“淘汰筛选”：当多个线程几乎同时涌入 Level $i$ 时，它们相继向 `victim[i]` 写入自身线程 ID。由于物理内存单次写入必有确定先后顺序，最后一个将自己写入 `victim[i]` 的线程将被无情困在 `victim[i] == me` 的自旋循环中，而此前较早写入的线程则因牺牲者身份被覆盖而得以成功跳出循环、晋升至下一层 Level $i+1$。

通过严格的数学归纳法可以证明：在任意离散时刻，处于 Level $\ell$ 及以上级别的活跃线程数严格受限于 $n - \ell$。当线程通过层层筛选最终到达最高级别 $\ell = n - 1$ 时，处于该级别的线程数至多为 $n - (n - 1) = 1$，从而严密地保证了全局互斥性。在释放锁时，线程只需执行 `level[me] = 0`，即可一举退出所有竞争级别，使后续被阻塞的线程依次逐级解冻。

## 公平性与门厅（Doorway）机制

无饥饿性（Starvation-freedom）仅保证线程最终能够进入临界区，但并不保证“先来先服务（FCFS）”。例如在过滤锁中，一个新来的线程可能会由于调度交错而在高层级超车，导致先发起的线程被反复推迟。

为了严谨形式化公平性，我们将 `lock()` 方法拆分为两个逻辑区间：

1. **门厅区间（Doorway Section, $D$）**：
   - 执行步骤具有常数上界、保证在有限步内无循环完成的代码区域（即有限等待自由 Bounded Wait-Free）；
2. **等待区间（Waiting Section, $W$）**：
   - 包含 `while` 自旋等待、步数取决于外部竞争环境的代码区域。

::: definition 先来先服务（First-Come-First-Served, FCFS）公平性
设 $D_A^k$ 与 $CS_A^k$ 分别代表线程 A 的第 $k$ 次加锁门厅区间与临界区区间。
若线程 A 的门厅区间在线程 B 的门厅区间开始之前已经完全结束：
$$D_A^k \to D_B^m \implies CS_A^k \to CS_B^m$$
则称该锁算法具备先来先服务（FCFS）公平性。任何既满足死锁自由又满足 FCFS 公平性的互斥锁，必然自动满足无饥饿性。
:::

## 兰伯特面包店算法（Lamport's Bakery Algorithm）

Leslie Lamport 受日常生活中的面包店排队号票机启发，提出了经典的 $n$ 线程公平互斥算法——**面包店算法（Bakery Algorithm）**。

### 算法运行规则

1. **门厅取号**：线程进入门厅后，读取所有线程现存的号码，并选取一个严格大于已知最大号码的序号 $label[i] = 1 + \max(label)$ 作为自己的排队票号；
2. **打破对称性**：若两线程并发取号拿到了相同的数字，算法采用**字典序（Lexicographical Order）**比较票号与线程 ID：
   $$(label[i], i) < (label[j], j) \iff (label[i] < label[j]) \lor (label[i] == label[j] \land i < j)$$
3. **等待叫号**：线程在等待区循环轮询。只要存在某个线程的票号字典序比自己更小且意图进入，当前线程便自旋等待。

面包店算法的一大奇迹在于其对硬件内存读写弱一致性的极端鲁棒性：**即使线程在门厅读取其他线程的号票时发生了异步的瞬态混乱（各线程看到的数据在物理内存中从未同时存在），算法依然能在数学上证明其互斥性与 FCFS 公平性。**

## 空间复杂度理论下界与覆盖状态定理

面包店算法与过滤锁虽然在数学上无懈可击，但在现代高并发多核工程实践中却极少被直接采用。其根本瓶颈在于**空间开销与轮询带宽**：面包店算法和过滤锁需要分配并读写至少 $n$ 个独立内存槽位。

那么，是否存在某种仅利用常规内存读写指令、且空间复杂度低于 $O(n)$ 的巧妙互斥算法？答案是否定的。

### 不一致状态与覆盖状态形式化

- **系统全局状态**：由所有共享变量的状态与各线程内部程序计数器（PC）构成的笛卡尔积；
- **定义 2.9.1（不一致状态 Inconsistent State）**：若某个线程处于临界区内，而锁对象的所有共享内存状态呈现为“空闲且无线程正在或试图进入临界区”，则称该全局状态为不一致状态；
- **引理 2.9.2**：任何保证死锁自由的锁算法绝不可能进入不一致状态（否则另一个不相干线程观察到空闲会同时进入临界区，打破互斥）；
- **定义 2.9.3（覆盖状态 Covering State）**：若在某个系统状态 $s$ 下，至少有一个线程正停在即将向某个共享内存位置发起写操作的临界点上，但从共享内存视角看临界区仍呈空闲状态，称这些线程覆盖了对应的内存单元。

### 定理 2.9.4：读写互斥的空间下界

::: theorem 纯读写互斥锁的空间下界定理（Burns et al.）
任何仅通过读写共享内存单元来解决 $n$ 线程无死锁互斥问题的锁算法，在最坏情况下**必须至少使用 $n$ 个不同的内存位置**：
$$\text{Space Complexity} = \Omega(n)$$
:::

**定理直觉与证明思想（以 3 线程为例）**：
1. 假设存在仅用 2 个共享内存位置（$L_A, L_B$）即可解决 3 线程互斥的算法；
2. 依据死锁自由性质，单线程在没有竞争时必定能在有限步内进入临界区，且进入前必须至少向内存写入一次（否则系统直接陷入不一致状态）；
3. 我们可以精巧构造一种线程交错执行序列：令线程 A 运行至即将向 $L_A$ 写入的位置挂起，令线程 B 运行至即将向 $L_B$ 写入的位置挂起，此时系统达到针对 $L_A$ 与 $L_B$ 的“全覆盖状态”；
4. 此时令独立的第三个线程 C 独占运行，C 成功进入临界区并在此执行；
5. 此时强制唤醒 A 与 B 执行它们被挂起的写入。由于 A 写入 $L_A$、B 写入 $L_B$，两者的写操作将彻底**覆写（Overwrite）**掉线程 C 在进入临界区期间留下的所有内存足迹！
6. 覆写完成后，共享内存的状态被瞬间还原为“没有任何线程处于临界区”的不一致状态。此时若有其他线程发起加锁，将发生致命双重进入，互斥性崩溃！
7. 矛盾证明：2 个内存单元无法满足 3 线程互斥。同理可递推证明 $n$ 线程必须至少拥有 $n$ 个独立可覆盖的内存单元。

## 我的理解与体系启示

::: insight 纯软件互斥的数学挽歌与硬件原语的黎明
回顾从 LockOne、Peterson 到 Bakery 算法的探索历程，计算机科学家们在仅依赖“常规内存读（Load）与写（Store）”的纯软件环境下，将基于偏序与反证法的逻辑推理推向了极致。

然而，$\Omega(n)$ 的空间复杂度下界定理如同一道冰冷的物理铁幕：**如果底层硬件只提供普通的读写指令，那么构建一个支持 1000 线程并发的锁，每次加锁解锁就必须至少分配并扫描 1000 个内存位置！** 这在微秒必争的现代多核系统上是绝对不可接受的。

正是这一严格的数学绝境，迫使体系结构设计者与操作系统学者联合推动了硬件指令集的革命——**在 CPU 层面引入具备强共识能力的原子读-改-写指令（如 TAS、CAS、LL/SC）**。下一阶段基于硬件原语的自旋锁与队列锁（详见 [Lec 7 自旋锁与总线竞争优化](./lec7.md)），正是建立在对这一空间下界突破的历史必然之上。
:::
