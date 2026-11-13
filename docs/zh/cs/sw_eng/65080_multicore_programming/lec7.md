---
title: 自旋锁与总线竞争优化
type: lecture
lecture: 7
tags: [spin-lock, cache-coherence, numa, test-and-set, queue-lock]
status: complete
---

# Lec 7 自旋锁与总线竞争优化（Spin Locks and Contention）

## TL;DR

- 互斥锁必须严格保证互斥性（至多一线程在临界区）、死锁自由（系统整体持续推进）与饥饿自由（每个调用最终返回）。
- 等待策略权衡由预期等待时长决定：短临界区优先选择自旋等待（Spin），长阻塞优先选择休眠让步（Yield/Sleep）。
- TAS 自旋锁因频繁原子写入引发缓存行失效风暴与总线拥塞；TTAS 在本地缓存只读自旋，显著缓解自旋竞争，但释放时仍有瞬时失效风暴。
- 指数退避以随机延迟解耦争夺冲突，但依赖经验调参；CLH 与 MCS 队列锁通过排队将竞争广播收敛为单播通知。
- CLH 在前驱节点自旋且空间开销小，但在无缓存 NUMA 架构下遭遇严重的跨节点远程访问延迟；MCS 采用本地自旋与显式后继指针，完美消除 NUMA 瓶颈。

## 互斥锁的核心属性与正确性准则

在共享内存多核系统中，互斥锁（Mutex / Lock）是协调多个并发线程访问临界区（Critical Section）的最基础同步原语。一个在数学和工程上合法的互斥锁实现，必须满足以下三大核心性质：

1. **互斥性（Mutual Exclusion）**：
   - 在任意时刻，至多只有一个线程能够持有锁（即完成 `lock()` 且尚未完成 `unlock()`）。
2. **死锁自由（Freedom from Deadlock / Deadlock-Free）**：
   - 如果某个线程尝试获取锁（调用 `lock()`）或释放锁（调用 `unlock()`），系统整体必须保证持续推进：其他线程必须能够无限次地完成对 `lock()` 和 `unlock()` 的调用。
   - 换言之，系统不会因为线程相互等待或依赖环路而发生全局停滞。如果某个线程崩溃且永不返回，在没有死锁的设计中，其他非故障线程仍能继续获取和释放锁。
3. **饥饿自由（Freedom from Starvation / Starvation-Free）**：
   - 每一个调用 `lock()` 的线程最终都必定能够获得锁并成功返回。
   - 饥饿自由是一种强公平性（Fairness）保证，它排除了某个线程由于其他线程不断插队而无限期被推迟执行的可能。

::: definition 互斥锁的三大正确性准则
设线程集合为 $\mathcal{T}$。互斥锁必须无条件保证：
1. **安全性（Safety）**：互斥性，即处于临界区的线程数 $|\mathcal{T}_{\text{in-cs}}| \le 1$；
2. **弱活性（Weak Liveness）**：死锁自由，即只要有线程发起请求，临界区终将被某个线程进入；
3. **强活性（Strong Liveness）**：饥饿自由，即对于任意线程 $T_i \in \mathcal{T}$，其调用 `lock()` 的等待时间有限。
:::

## 自旋等待与阻塞休眠的架构权衡

当一个线程尝试获取锁但发现锁已被其他线程持有时，系统设计上有两种截然相反的等待策略：

### 策略对比

1. **自旋等待（Spinning / Busy-wait）**：
   - 线程在 CPU 核心上保持运行状态，通过紧凑的循环反复检查锁状态。
   - **适用场景**：临界区执行时间极短（纳秒级或几个微秒），预期等待时间短于操作系统上下文切换的开销。
   - **代价**：自旋期间持续独占 CPU 核心，消耗电力；在单核处理器上自旋毫无意义（自旋线程会剥夺持有锁线程运行所需的 CPU 时间）。
2. **放弃处理器（Yielding / Blocking / Sleep）**：
   - 线程主动发起系统调用进入睡眠状态，操作系统内核介入将该线程挂起，并将 CPU 核心调度给其他就绪线程运行；锁被释放时再由系统唤醒该线程。
   - **适用场景**：临界区执行时间长（毫秒级以上）或等待锁的线程发生 I/O 阻塞。
   - **代价**：涉及用户态到内核态的上下文切换、CPU 流水线清空与局部性缓存冷启动，单次切换开销通常在微秒级别（数千个时钟周期）。

![多处理器共享总线与缓存一致性架构示意图](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6654656055f72.png)

### 硬件优化的三个关键指标

在多核共享总线架构中，评价一个自旋锁算法性能优劣的核心指标包括：

- **自旋线程占用的总线带宽（Bus bandwidth used by spinning threads）**：
  若多个线程在自旋时频繁向总线发送通信请求，会严重挤占宝贵的总线带宽，拖慢其他核心正常计算的内存访问。
- **获取与释放延迟（Release/Acquire latency）**：
  持有者释放锁之后，等待线程感知到释放信号并成功夺得锁的时间差必须尽可能短。
- **空闲锁获取开销（Acquire latency for idle lock）**：
  在系统没有竞争、锁处于空闲状态时，单个线程获取锁的硬件指令开销（如单次无竞争 CAS）应保持在绝对最小值。

## Test-and-Set（TAS）与缓存失效风暴

### 硬件原子原语回顾

现代多处理器体系结构在指令集层面提供了原子读-改-写（Read-Modify-Write, RMW）硬件指令，例如 x86-64 架构下的带总线锁定前缀的交换指令（`LOCK XCHG` 或 `LOCK CMPXCHG`）。这类指令能够保证：在多个 CPU 核心同时访问同一内存地址时，硬件内存控制器会在总线或缓存一致性控制器层面将其串行化，确保读取、修改与写回操作作为一个不可分割的原子步骤完成。

在 Java 并发工具包中，硬件原子交换能力被直接封装在 `AtomicBoolean.getAndSet()` 中：

```java
// 硬件原子原语语义等价说明
public class AtomicBoolean {
    private boolean value;

    public synchronized boolean getAndSet(boolean newVal) {
        boolean prior = value;
        value = newVal;
        return prior;
    }
}
```

利用底层的原子交换原语，我们可以构造出概念上最直观的互斥锁——**Test-and-Set（TAS）自旋锁**。在该模型中，锁的状态由布尔变量 `state` 表达：`false` 表示锁处于空闲释放状态，`true` 表示锁已被某个线程持有。

在实现细节上，加锁与解锁的逻辑如下：

```java
public class TASLock implements Lock {
    private final AtomicBoolean state = new AtomicBoolean(false);

    public void lock() {
        // 原子写入 true，若返回的旧值为 true 则说明锁已被他人占用，循环自旋
        while (state.getAndSet(true)) {}
    }

    public void unlock() {
        // 释放锁时直接写入 false，恢复空闲状态
        state.set(false);
    }
}
```

在 `lock()` 方法中，线程反复调用 `state.getAndSet(true)`。如果返回的旧值（`prior`）为 `false`，说明该线程成功将锁从空闲状态修改为持有状态，夺锁成功并退出循环；如果返回的旧值为 `true`，说明此前锁已被其他线程持有，当前线程夺锁失败并继续在 `while` 循环中自旋。在 `unlock()` 方法中，持有者通过挥发写（Volatile Write）将 `state` 置为 `false`，Java 内存模型（JMM）的 Release 语义保证了临界区内的所有修改在锁释放前对后续获取者完全可见。

### 物理失效风暴（Invalidation Storm）

尽管 TAS 锁在代码逻辑上极其简短，但在真实的多核多处理器硬件上，其性能会发生剧烈崩溃。

::: theorem TAS 的缓存失效风暴机制
在现代基于 MESI 缓存一致性协议的多核系统中：
1. 每次调用 `getAndSet(true)` 属于**硬件原子写操作**；
2. 即使内存单元的值已经是 `true`，硬件也必须向互连总线广播缓存失效（Invalidate）消息，强制将所有其他核心缓存中对应的缓存行置为 Invalid；
3. 所有正在自旋的核心的 L1/L2 缓存行不断被击穿失效，核心必须反复向共享总线发送内存读写请求。
:::

这种架构级别的恶性循环导致了两个致命后果：
- **总线拥塞（Bus Saturation）**：所有自旋线程以纳秒级频率淹没总线，总线利用率迅速饱和；
- **释放延迟恶化（Delayed Behind Spinners）**：持有锁的线程在完成临界区试图调用 `unlock()` 时，其写入 `false` 的总线请求必须在总线仲裁队列中与海量自旋线程的 TAS 请求排队竞争。持有者无法及时释放锁，导致临界区人为延长。

## Test-and-Test-and-Set（TTAS）与读局部性

为了解决 TAS 锁不断向总线广播原子写的致命缺陷，Larry Rudolph 提出了经典的 **Test-and-Test-and-Set（TTAS）锁**。

### 潜伏与突袭两阶段机制

TTAS 锁将加锁逻辑解耦为两个阶段：

1. **潜伏阶段（Lurking Stage）**：
   - 线程在进入原子争抢前，先执行常规的只读检查 `while (state.get()) {}`。
   - 在 MESI 协议下，只读自旋会将锁变量加载到本核心的私有缓存中，缓存行状态保持为 Shared。
   - 只要锁处于被持有状态（值为 true），自旋线程完全在**本地缓存副本（Local Cache）**上命中读取，**对系统总线产生零网络通信流量**。
2. **突袭阶段（Pouncing Stage）**：
   - 一旦持有者释放锁将变量置为 false，该写入会触发总线单次失效广播。
   - 潜伏自旋的线程立即观察到本地缓存行失效并读取到 false，随即跳出内层循环，发起一次真正的 `state.getAndSet(true)` 突击夺锁。

```java
public class TTASLock implements Lock {
    private final AtomicBoolean state = new AtomicBoolean(false);

    public void lock() {
        while (true) {
            // 1. 潜伏阶段：在本地缓存行上只读自旋，不占用总线带宽
            while (state.get()) {}
            // 2. 突袭阶段：锁看起来空闲，尝试原子争夺
            if (!state.getAndSet(true)) {
                return;
            }
        }
    }

    public void unlock() {
        state.set(false);
    }
}
```

### TTAS 的残留缺陷

尽管 TTAS 解决了自旋期间的总线带宽消耗，但在**锁被释放的瞬间**依然存在严重的性能瓶颈：

- **释放瞬间的失效风暴（Invalidation Storm）**：
  当锁被释放的一瞬间，所有处于潜伏阶段的核心几乎同时被唤醒，并同时向总线发起 `getAndSet` 原子写指令。总线瞬间被并发请求打满。
- **串行化缓存行重填与静默延迟**：
  在多核竞争中只有一个核心能够获胜，其余落败的核心在恢复潜伏阶段前，必须依次通过总线串行重新拉取 Shared 缓存行。这一“平息冲突”的静默延迟与系统中的核心数量呈线性相关。

## 指数退避自旋锁（Exponential Backoff Lock）

### 算法设计动机

TTAS 突袭失败的根本原因在于所有等待者在同一微秒感知到锁释放，并在同一时间窗口向总线发起争夺。为了避免群体踩踏，受以太网冲突回退协议的启发，**指数退避自旋锁（Backoff Lock）**被引入到多核同步中。

其核心算法逻辑分为三个协同机制：
1. **潜伏检测**：线程首先在本地缓存中执行只读检查 `while (state.get()) {}`，直到锁看起来空闲；
2. **单次突袭**：执行一次 `state.getAndSet(true)` 夺锁；如果夺锁成功，立即进入临界区；
3. **随机指数退避**：如果突袭失败，说明同一时刻有多个核心在争抢。此时线程不立即重新回到潜伏或突袭循环，而是在区间 `[0, delay)` 内随机休眠一段时间；若连续争抢失败，则将随机区间的最大延迟翻倍（`delay = 2 * delay`），直至达到上限 `MAX_DELAY`。

通过引入随机延迟，原本集中在同一时刻的总线写请求被有效平摊在不同的时间点上，使得突发性总线风暴转变为平缓的错峰访问：

```java
public class BackoffLock implements Lock {
    private final AtomicBoolean state = new AtomicBoolean(false);
    private static final int MIN_DELAY = 32;
    private static final int MAX_DELAY = 1024;

    public void lock() {
        int delay = MIN_DELAY;
        while (true) {
            // 阶段一：在本地缓存中潜伏轮询
            while (state.get()) {}
            // 阶段二：发起单次原子争抢
            if (!state.getAndSet(true)) {
                return; // 夺锁成功，返回执行临界区
            }
            // 阶段三：争抢失败，执行随机退避以错开竞争时间点
            try {
                Thread.sleep(ThreadLocalRandom.current().nextInt(delay));
            } catch (InterruptedException ignored) {}
            // 失败次数越多，等待窗口指数级翻倍扩大
            if (delay * 2 <= MAX_DELAY) {
                delay = 2 * delay;
            }
        }
    }

    public void unlock() {
        state.set(false);
    }
}
```

在上述实现中，`MIN_DELAY` 与 `MAX_DELAY` 构成了退避锁的关键性能杠杆。若最小延迟设置过小，线程退避结束后依然大概率与其他竞争者相撞；若最大延迟设置过大，当锁早已释放时，线程仍在无谓休眠，导致核心空转并拉大锁获取延迟。

### 性能表现与局限性

![TAS、TTAS 与指数退避自旋锁在高并发下的执行时间性能对比图](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6654e5b458c88.png)

如上图测试结果所示：
- **优点**：退避自旋锁实现极其轻量，在高并发核心数激增时，执行时间显著平稳，性能全面压制原生的 TAS 与 TTAS 锁。
- **缺点**：
  1. **参数极其脆弱且不可移植**：`MIN_DELAY` 与 `MAX_DELAY` 的最优参数高度依赖于特定硬件 CPU 主频、总线仲裁协议和多核互连拓扑，在一个平台上表现良好的参数在另一个平台上可能导致吞吐断崖式下跌；
  2. **非 FIFO 顺序**：由于退避引入了随机性，后来的线程可能恰好在锁释放时退避结束而抢占成功，无法提供饥饿自由保证。

## CLH 队列锁：前驱自旋与单播通知

为了根除自旋锁在释放时的总线广播风暴并提供严格的先来先服务（FCFS）公平性，**队列锁（Queue Lock）**应运而生。由 Craig、Landin 和 Hagersten 联合发明的 **CLH 锁**是最具代表性的算法之一。

### 核心机制

CLH 锁维护一个逻辑等待队列：
- 每个请求锁的线程拥有一个 `QNode` 节点；
- 线程通过原子交换操作加入队列尾部，获取其**前驱节点（Predecessor Node）**的引用；
- 线程不监听全局变量，而是**专一在前驱节点的 `locked` 状态上进行自旋**；
- 锁释放时，前驱节点将自身标志置为 `false`，唯一直系后继线程感知变化并获得锁。锁的释放实现了点对点单播通知，总线广播通信完全降为零！

### 完整 7 步生命周期演化图谱

1. **初始状态**：全局 `tail` 指针指向一个 `locked = false` 的初始哨兵节点。
   ![CLH 锁初始状态：tail 指向空闲哨兵节点](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6654fa2f4dbd0.png)
2. **线程入队**：新线程构造节点并将 `locked` 置为 `true`，通过原子交换原子更新 `tail` 指向自己，并取得原哨兵节点的引用作为前驱。
   ![线程入队 CLH 锁：原子交换 tail 指针获取前驱引用](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6654fa474c790.png)
3. **前驱自旋**：线程在前驱节点的 `locked` 字段上自旋等待。由于此前驱已被置为 `false`，当前线程直接获得锁并进入临界区。
   ![前驱节点锁定：后继线程开始在前驱节点的 locked 字段上本地自旋](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6654fa5db62c2.png)
4. **队列级联构建**：后续线程相继到达，依次原子更新 `tail`，各线程在前驱节点的标志上自旋，队列形成隐式链表。
   ![多线程连续追加：队列形成隐式等待单向链表](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6654fb37b1c8b.png)
5. **持有者释放锁**：当前持有锁的线程执行完临界区后，将其持有的节点 `myNode.locked` 置为 `false`。
   ![持有者释放锁：将自身节点 locked 置为 false](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6654fba8548c5.png)
6. **直系后继唤醒**：后继线程检测到前驱节点变为 `false`，结束自旋并正式进入临界区。其他后续排队线程完全不受干扰。
   ![后继感知释放：前驱自旋结束并进入临界区](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6654fbc00e667.png)
7. **空间回收与复用**：为了防止反复创建节点的内存分配开销，释放线程直接将前驱节点的引用赋值给自己的 `myNode`，以供下次加锁时复用。
   ![节点空间复用：后继线程回收前驱节点作为未来请求的新节点](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6654fd13e3c4d.png)

### 代码实现

在 CLH 队列锁的具体实现中，数据结构的设计展现出极高的空间效率与算法简洁性：
- `QNode` 内部仅包含一个简单的 `volatile boolean locked` 状态标志。与显式链表不同，CLH 节点本身**完全不需要存储任何指向前驱或后继节点的指针**；
- 全局 `tail` 变量是一个指向 `QNode` 的原子引用（`AtomicReference<QNode>`），用于协调多线程在队尾的原子追加；
- 每个线程通过 `ThreadLocal` 分别维护属于自己的当前节点 `myNode` 以及所监视的前驱节点引用 `myPred`。

```java
public class CLHLock implements Lock {
    private static class QNode {
        volatile boolean locked = false;
    }

    private final AtomicReference<QNode> tail = new AtomicReference<>(new QNode());
    private final ThreadLocal<QNode> myNode = ThreadLocal.withInitial(QNode::new);
    private final ThreadLocal<QNode> myPred = new ThreadLocal<>();

    public void lock() {
        QNode qnode = myNode.get();
        qnode.locked = true;
        // 原子置换：将自身设为尾节点，并获得前驱节点的引用
        QNode pred = tail.getAndSet(qnode);
        myPred.set(pred);
        // 专一在前驱节点的 locked 字段上自旋
        while (pred.locked) {}
    }

    public void unlock() {
        QNode qnode = myNode.get();
        // 通知直系后继线程
        qnode.locked = false;
        // 内存回收机制：复用前驱节点作为本线程后续请求的新节点
        myNode.set(myPred.get());
    }
}
```

在执行 `lock()` 时，线程将自身节点标记为 `locked = true`，随后调用 `tail.getAndSet(qnode)`。这一单条原子指令同时完成了两项关键动作：一是将当前节点推入队尾，二是原子化地取得了原队尾节点的引用（即直接前驱节点 `pred`）。随后，线程进入 `while (pred.locked) {}`。由于现代处理器缓存一致性协议的存在，前驱节点的 `locked` 状态会被自动复制到当前核心的本地缓存中，后续的轮询完全在本地缓存内命中，总线上没有任何无谓的轮询流量。

在执行 `unlock()` 时，持有者只需将 `myNode.get().locked` 置为 `false`。此时，正在该节点上自旋的直系后继核心会感知到缓存失效并读取到新值，从而结束自旋进入临界区。为了避免高频加锁解锁引发的频繁内存分配与垃圾回收压力，CLH 锁引入了极具启发性的节点空间复用机制：`myNode.set(myPred.get())`。由于前驱节点此时已经完成了历史使命，且不再被任何线程监听，当前线程直接接管该节点作为自己下一次加锁的新节点，从而保证了空间复杂度恒定为 $O(L + N)$。

::: pitfall CLH 锁在非一致性 NUMA 架构下的性能陷阱
CLH 锁在具备缓存一致性（Cache-Coherent）的多核架构下表现优异，因为前驱节点的内存变量会被自动复制到当前核心的本地缓存中只读自旋。
然而，在**缺乏缓存的 NUMA 架构**（Non-Cache-Coherent NUMA）或者跨节点缓存同步代价极高的服务器架构上，前驱节点物理分布在远程节点的内存条上。当前核心反复跨 NUMA 互连总线轮询远程前驱节点，将导致严重的互连总线通信堵塞。
:::

## NUMA 与 cc-NUMA 体系结构对自旋锁的约束

为了理解 CLH 锁的瓶颈并引出 MCS 锁，必须深入理解现代多处理器的物理内存拓扑：

- **对称多处理架构（SMP, Symmetric Multiprocessing）**：
  所有 CPU 核心通过同一条全局物理总线访问集中式的统一内存，所有核心访问内存的延迟完全对称。当核心数超过几十个时，共享总线成为绝对瓶颈。
- **非一致性内存访问架构（NUMA, Non-Uniform Memory Access）**：
  系统被划分为多个物理 Node，每个 Node 包含一组 CPU 核心及挂载在其本地内存控制器上的本地物理内存。
- **缓存一致性 NUMA（cc-NUMA）**：
  硬件通过分布式目录协议在 NUMA 之上为软件提供了统一的平坦共享内存抽象。

![SMP 对称多处理与 NUMA 非一致性内存架构拓扑差异](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/665502c7046fb.png)

![cc-NUMA 架构下跨互连网络访问远程内存与缓存一致性开销](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/665502b150536.png)

在 NUMA 系统中，CPU 核心访问本地内存（Local Access）极快，而跨互连网络访问远程节点的物理内存（Remote Access）延迟可能高出 3 到 5 倍。因此，设计面向大规模多核架构自旋锁的黄金准则是：**等待线程必须在属于自己本地物理内存的变量上进行自旋（Local Spinning）！**

## MCS 队列锁：本地内存自旋与显式后继链接

为了在 NUMA 硬件上实现真正的本地自旋，John Mellor-Crummey 和 Michael Scott 设计了 **MCS 队列锁**。

### 核心架构思想

- **显式单向链表**：不同于 CLH 的隐式前驱链接，MCS 队列每个节点显式维护一个指向后继的 `next` 指针；
- **纯本地内存自旋（Local Spinning）**：每个线程在自身局部内存中分配 `QNode`，并**严格只在属于自己的本地节点的 `locked` 字段上自旋**！
- **前驱单播更新**：前驱线程在释放锁时，通过其持有的 `next` 指针，主动向后继节点的本地变量写入 `locked = false`。

### 状态演进图谱

1. **节点结构定义**：每个节点包含 `volatile boolean locked` 和 `volatile QNode next`。
   ![MCS 锁节点定义：包含 locked 标志与显式 next 后继指针](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66551324c6f6b.png)
2. **入队与尾指针置换**：申请线程创建本地节点，将其 `locked` 置为 `true`，通过原子交换抢占 `tail`。
   ![MCS 加锁第一步：分配节点并原子更新 tail 指针](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6655135feb953.png)
3. **显式后继链接**：如果此前队列非空（存在前驱），当前线程主动将前驱节点的 `next` 指针重定向指向自己。
   ![MCS 加锁第二步：将前驱的 next 指针指向自身](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6655138a0f68b.png)
4. **完全本地自旋**：前驱节点确立了后继位置后，后继线程完全在**自己本核心的节点内存上**自旋等待。
   ![MCS 加锁第三步：线程完全在本地节点的 locked 字段上自旋](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/665513a1a071f.png)
5. **后续节点接入**：新线程陆续到达，重复原子交换与后继链接步骤。
   ![MCS 多节点链入：后继节点相继确立 next 指针链接](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/665513b7728f3.png)
6. **链表拓扑确立**：整个等待队列由各核心本地节点串联而成，每个线程独享一个自旋内存行。
   ![MCS 完整队列状态：每个线程拥有独占的自旋目标](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/665513f23fa17.png)
7. **算法流程总览**：MCS 加锁算法实现了完美的本地化自旋。
   ![MCS 加锁算法流程总结与节点初始化细节](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6655171979343.png)

### 解锁时的两阶段竞争分析

MCS 锁的精妙与复杂之处在于释放锁（`unlock`）逻辑。当持有者准备离开临界区时，面临三种可能场景：

1. **场景一：队列只有自身一个节点，无后继竞争**：
   - 持有者发现 `qnode.next == null`；
   - 执行 CAS 操作：尝试将 `tail` 从自身还原为 `null`。若 CAS 成功，说明确实没有新线程排队，直接退出。
   ![MCS 解锁场景一：当前节点处于队尾且无后继，CAS 清空 tail](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6655196ad5b0e.png)
2. **场景二：后继线程已更新 tail，但尚未完成将前驱 next 指针指向自身**：
   - 此时 `tail != qnode`，因此场景一中的 CAS 失败；
   - 此时 `qnode.next` 依然为 `null`（后继已宣称队尾但还在执行赋值指令的间隙）；
   - 释放线程必须在本地短暂自旋等待后继线程追赶完成：`while (qnode.next == null) {}`。这一微观等待通常仅持续数个时钟周期。
   ![MCS 解锁场景二：后继正在更新 tail 但尚未赋值 next，释放线程自旋等待后继追赶](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66551b40dccdf.png)
3. **场景三：后继已确立，单播释放通知**：
   - 持有者直接将后继节点的标志置为可用：`qnode.next.locked = false`；
   - 后继线程在其本地内存中感知到状态变化，安全退出自旋进入临界区。
   ![MCS 解锁场景三：后继已确立，原子更新后继的 locked 标志为 false](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66551b5831cea.png)
   ![MCS 解锁完成：后继线程收到通知并安全退出自旋](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66551b70907b1.png)

### 代码实现

与 CLH 锁不同，MCS 队列锁必须维护显式的单向后继链表，以确保前驱持有者能够精准定位并主动通知后继线程。

在具体数据结构设计上：
- `QNode` 包含两个关键字段：用于指示等待状态的 `volatile boolean locked`，以及用于维系后继单向链接的 `volatile QNode next`；
- 全局 `tail` 初始为 `null`，代表队列当前处于完全空闲状态；
- 每个线程通过 `ThreadLocal` 维护一个属于当前线程本地物理内存的 `QNode`。

```java
public class MCSLock implements Lock {
    private static class QNode {
        volatile boolean locked = false;
        volatile QNode next = null;
    }

    private final AtomicReference<QNode> tail = new AtomicReference<>(null);
    private final ThreadLocal<QNode> myNode = ThreadLocal.withInitial(QNode::new);

    public void lock() {
        QNode qnode = myNode.get();
        QNode pred = tail.getAndSet(qnode);
        if (pred != null) {
            qnode.locked = true;
            pred.next = qnode; // 链接前驱与后继
            // 核心：严格只在本地节点的 locked 变量上自旋！
            while (qnode.locked) {}
        }
    }

    public void unlock() {
        QNode qnode = myNode.get();
        if (qnode.next == null) {
            // 尝试原子置空尾节点
            if (tail.compareAndSet(qnode, null)) {
                return;
            }
            // 存在后继正在接入但未完成 pred.next 赋值，短暂等待其追赶完成
            while (qnode.next == null) {}
        }
        // 单播通知直系后继
        qnode.next.locked = false;
        qnode.next = null; // 解除引用辅助 GC
    }
}
```

在执行 `lock()` 时，线程通过 `tail.getAndSet(qnode)` 将自身节点原子置换至队尾。若返回的前驱 `pred` 为 `null`，说明当前队列空闲，线程直接获取锁；若 `pred != null`，线程将自身的 `locked` 设为 `true`，并将前驱节点的 `next` 指针重定向指向自身（`pred.next = qnode`），随后在自己的节点上执行 `while (qnode.locked) {}`。由于 `qnode` 分配在当前核心插槽的本地内存中，轮询完全在本地发生，对 NUMA 互连总线通信造成零干扰。

在执行 `unlock()` 时，算法必须处理经典的两阶段竞争边界：
1. 若 `qnode.next == null`，线程首先尝试利用 `tail.compareAndSet(qnode, null)` 原子清空队尾。若 CAS 成功，证明队列中确实没有后继排队，解锁成功退出；
2. 若 CAS 失败，说明正有后继线程在并发执行 `tail.getAndSet(qnode)`，但该后继尚未完成 `pred.next = qnode` 的指针赋值。此时释放线程必须在本地短暂自旋 `while (qnode.next == null) {}` 等待后继确立指针；
3. 一旦 `qnode.next` 确立非空，释放线程直接将后继节点的标志置为 `false`（`qnode.next.locked = false`），实现精准的点对点单播唤醒。

## 可中断与带超时的队列锁

在真实的数据库与高可用分布式系统中，线程往往无法承担无休止死等锁的代价（例如事务发生超时回滚、系统调用收到中断信号或用户取消任务）。

### 队列锁的优雅脱钩挑战

- **退避锁的轻松打断**：
  在基于退避的自旋锁中，支持超时或中断极其简单——如果超时，线程只需直接从 `lock()` 方法返回失败即可，无需进行任何清理。
- **队列锁的断链危机**：
  队列锁由链表严格串联。如果队列中间的某个等待线程由于超时擅自退出，其后继线程将永远无法接收到前驱的解锁通知，导致后继节点发生致命的永久饥饿！

因此，支持超时的队列锁必须实现**优雅退出机制（Graceful Exit）**：
- 超时放弃的节点将其内部状态置为特殊的 `AVAILABLE` 或 `ABORTED`；
- 后继节点在自旋检测中若发现其前驱已放弃等待，必须自动跳过该节点并向前回溯寻找存活的前驱节点，重构单向链表拓扑；
- 复合锁状态机协同保证幽灵节点的安全清理。

![队列锁超时放弃机制：节点自旋超时后标记自身并脱落链表](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66551f4ba805f.png)

![可中断复合队列锁的状态机转移与幽灵节点清理](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66551f8143f44.png)

## 我的理解与体系启示

::: insight 自旋锁演进背后的通信物理学
纵观 TAS $\to$ TTAS $\to$ Backoff $\to$ CLH $\to$ MCS 的完整演进历程，驱动算法变革的底层力量本质上是**硬件总线通信拓扑的优化**：
1. **TAS** 采用暴力原子写入，使总线完全沦为通信瓶颈；
2. **TTAS** 利用缓存行只读共享将常规轮询限制在本地，但在释放瞬间依然引发 $O(N)$ 的瞬时总线雪崩；
3. **Backoff** 引入统计学上的时间分散策略缓解冲突，但参数调优极度依赖经验且缺乏可移植性；
4. **CLH** 用空间换取秩序，把广播彻底规约为前驱对后继的 $O(1)$ 单播通知，但在无缓存 NUMA 上暴露了远程跨节点轮询缺陷；
5. **MCS** 彻底把自旋目标固定在申请者本插槽的物理内存中，既享有严格的 FIFO 公平性与单播通知，又实现了对 NUMA 硬件拓扑的天然免疫。

这一技术进化清晰地表明：**优秀的并发算法从来不是对硬件特性的抽象遮蔽，而是对微架构物理约束的精准适应与主动利用。**
:::
