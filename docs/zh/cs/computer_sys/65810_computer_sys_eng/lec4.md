---
title: 有界缓冲区与并发锁
type: lecture
lecture: 4
tags: [concurrency, bounded-buffer, race-conditions, locks, deadlocks]
status: complete
---
# Lec 4 有界缓冲区与并发锁

> 阅读资料：
> - 教材：Saltzer & Kaashoek《Principles of Computer System Design》第 5 章（§5.1–§5.2）

## TL;DR

- **有界缓冲区模型**：作为生产者与消费者之间的解耦管道，基于定长环形队列与 `in/out` 游标吸收生产速率与消费速率的突发失配。
- **竞态条件与互斥锁**：多执行流并发交错读写共享游标将破坏状态一致性；互斥锁（Mutex）通过关键区序列化保证操作原子性。
- **持锁自旋死锁与两级加锁**：若在临界区内持锁自旋等待缓冲区空闲，将彻底阻塞对端消费者进入，导致永久死锁；必须在重试等待前临时释放锁（两级加锁模式）。
- **硬件原子指令基石**：纯软件标志位无法抵御指令乱序与并发读写，现代互斥锁依赖硬件级原子交换（`atomic_swap`）或比较并交换（CAS）指令实现无竞态抢占。

---

## 1. 为什么多执行流并发极度脆弱？

在现代计算机操作系统中，不同模块以完全不可预测的异步速率运行：
- 键盘控制器以物理中断频率产生击键事件，而文本编辑器按自己的调度节奏从缓冲区提取字符并渲染；
- 高速网卡以 10 Gbps 速率涌入数据包，用户态 Web 应用程序按需逐个拉取 HTTP 请求。

为了防止快端冲垮慢端，系统必须在生产者与消费者之间横插一个协调机制——**有界缓冲区（Bounded Buffer）**。然而，一旦多个并发执行流同时访问共享缓冲区，指令的任意交错重叠就会引发极其隐蔽的**竞态条件（Race Conditions）**。

---

## 2. 有界缓冲区抽象：环形队列模型

有界缓冲区是一个物理容量固定为 $N$ 的先进先出（FIFO）数据通道。为了避免数据在内存中反复搬迁，通常采用**环形队列（Circular Buffer）**实现：

```text
       in (下一个写入位置)
       │
       ▼
┌───┬───┬───┬───┬───┬───┬───┬───┐
│ D │ E │   │   │   │ A │ B │ C │  (容量 N = 8)
└───┴───┴───┴───┴───┴───┴───┴───┘
                      ▲
                      │
                     out (下一个读取位置)
```

系统维护两个单调递增的游标：
- `in`：累计已生产的消息总数（实际写入槽位为 `in mod N`）；
- `out`：累计已消费的消息总数（实际读取槽位为 `out mod N`）；
- **满队判定**：`in - out == N`（已无空槽，生产者必须阻塞等待）；
- **空队判定**：`in == out`（无未读数据，消费者必须阻塞等待）。

---

## 3. 竞态条件与加锁演进四重奏

### 3.1 版本 0：无并发控制下的数据踩踏

考虑最质朴的生产与消费逻辑：

```python
def send(message):
    while (in - out == N):
        pass  # 缓冲区满，忙等待
    buf[in mod N] = message
    in = in + 1

def receive():
    while (in == out):
        pass  # 缓冲区空，忙等待
    message = buf[out mod N]
    out = out + 1
    return message
```

::: pitfall 游标自增与非原子读写竞态
指令 `in = in + 1` 在底层通常被编译为三条机器指令：
1. `LOAD in -> R1`
2. `ADD 1 -> R1`
3. `STORE R1 -> in`

若两个生产者线程同时执行 `send`，线程 A 加载 `in=5` 后发生时钟中断被剥夺 CPU；线程 B 进入并执行完整三条指令，将 `in` 刷写为 6；线程 A 恢复后继续执行，将其本地寄存器的 6 再次写回内存。
**结果**：两条不同的消息被写入了同一个槽位，后一条消息被静默覆盖，且 `in` 仅递增了 1，导致缓冲区内部数据结构发生不可逆的致命损坏。
:::

### 3.2 版本 1：持锁自旋引发的致命死锁

为了解决竞态，引入**互斥锁（Mutual Exclusion Lock）**。最直观的写法是将整个方法体用锁包围：

```python
def send_flawed(message):
    acquire(lock)
    while (in - out == N):
        pass  # 致命死锁点！
    buf[in mod N] = message
    in = in + 1
    release(lock)
```

::: theorem 持锁忙等待死锁定理
若缓冲区已满（`in - out == N`），生产者获取了 `lock` 并进入 `while` 循环自旋；
此时消费者试图调用 `receive()` 读取数据以腾出空间，但在入口处的 `acquire(lock)` 被死死阻塞；
生产者持锁等待消费者腾出空间，消费者等待生产者释放锁才能读取数据。**系统陷入经典死锁，永久冻结！**
:::

### 3.3 版本 2：双层加锁与让权循环（Correct Spin-Locking）

为了打破版本 1 中的致命依赖，系统必须遵循一个深刻的准则：**当一个线程发现前置条件无法满足而必须等待时，绝不能霸占着排他锁不放；它必须在重试前把锁拱手让出，给能够改变条件的对端线程留出执行通道。**

这一思想催生了经典的两级加锁（Nested Acquire/Release）模型：

```python
def send(message):
    acquire(lock)
    while (in - out == N):
        release(lock)  # 临时释放锁，允许消费者进入腾挪空间
        acquire(lock)  # 重新尝试抢锁检查条件
    buf[in mod N] = message
    in = in + 1
    release(lock)

def receive():
    acquire(lock)
    while (in == out):
        release(lock)  # 临时释放锁，允许生产者进入写入新数据
        acquire(lock)
    message = buf[out mod N]
    out = out + 1
    release(lock)
    return message
```

这一精巧结构在工程逻辑上具有严密的层次分工：
- **外层 `acquire / release` 的职责**：严格保护共享临界区。它保证了无论何时，真正执行数据写入、读取、以及游标自增的操作都处于排他状态，杜绝任何中间不一致状态被其他并发执行流窥探或破坏。
- **内层 `release / acquire` 的职责**：打破自旋期间的闭环死锁。当生产者发现缓冲区已满时，通过内层 `release` 暂时放弃锁，使得消费者能够顺利进入其自身的临界区读取数据并推进 `out` 游标；随后的内层 `acquire` 则确保重新进入满/空判定前，本地读取到的状态依然受到锁的强一致性保护。
- **必须使用 `while` 而非 `if` 的原因**：在多生产者或多消费者并发环境中，当线程从内层 `release` 重新获取到锁时，网络状态可能已被其他并发竞争者再度抢占。因此线程必须在循环中反复重新评估断言条件，确认真正具备空闲槽位后方可落盘写入。

---

## 4. 互斥锁的底层硬件实现：原子交换（atomic_swap）

如果锁本身也是由普通的程序代码实现的，那么就会引出一个深刻的哲学与工程拷问：**用来保护锁变量自身的代码，又该如何防止并发竞态？**

在单机多核体系结构中，普通的内存读取与写入操作是相互独立的离散事件。如果底层没有硬件机制的兜底，任何纯软件维度的加锁尝试都会在指令交错与微架构乱序面前分崩离析。

### 4.1 纯软件标志位的死穴

初学者常试图利用一个简单的共享布尔变量 `held`（0 表示空闲，1 表示已加锁）来实现互斥：

```python
def acquire_software_broken(lock):
    while lock.held == 1:
        pass
    lock.held = 1  # 多个线程可能同时跳过 while 检查并同时将 held 置 1！
```

这段纯软件逻辑存在致命的“检查与赋值分离（Check-Then-Act）”漏洞：
假设线程 A 执行到 `while` 条件，发现 `lock.held == 0`，正准备退出循环去执行赋值；恰在此时，时钟中断发生，CPU 切换至线程 B。线程 B 同样执行 `while`，同样读到 `lock.held == 0` 并顺利退出循环将 `held` 置为 1；随后线程 A 恢复执行，毫无察觉地也将 `held` 置为 1 并进入临界区。
**结果**：两个线程同时获取了同一把锁，互斥承诺彻底破产。尽管历史上出现过 Peterson 算法与 Lamport 面包房算法等纯软件解法，但它们在现代处理器的多核乱序执行（Out-of-Order Execution）与写缓冲区（Store Buffers）面前效率极低且极度脆弱。

### 4.2 硬件原子交换指令（`atomic_swap`）

为了终结纯软件的困局，现代微处理器在硅片硬件电路层面提供了一组**原子读-改-写指令（Atomic Read-Modify-Write Instructions）**，例如 x86 架构下的 `XCHG` 或 `CMPXCHG`。

在系统抽象层，我们将其抽象为硬件原语 `atomic_swap`：

```text
atomic_swap(register, memory_address):
    [硬件总线锁或 MESI 缓存一致性协议保证原子性]
    temp = memory_address
    memory_address = register
    register = temp
```

`atomic_swap` 的核心魔力在于其**不可分割性（Atomicity）**：处理器硬件通过锁定总线或在 L1/L2 缓存一致性协议中独占缓存行（Cache Line），强制保证“读取内存旧值”与“写入新值”在单条不可中断的微指令周期内完成。在此期间，任何其他 CPU 核心都绝无可能插足或观测到中间状态。

基于这一硬件原语，工业级自旋互斥锁的实现变得极其坚如磐石：

```python
def acquire(lock):
    while atomic_swap(1, lock.held) == 1:
        pass  # 若原本为 1 表明被别人持有，自旋重试；若原本为 0 则成功置 1 并退出

def release(lock):
    lock.held = 0  # 单个对齐写指令在现代硬件上是天然原子的
```

当线程调用 `acquire` 时，它尝试用数字 1 交换 `lock.held` 的值：
- 若锁原本处于空闲状态（`held == 0`），交换后 `held` 变为 1，函数返回值 0，循环条件不成立，线程瞬间成功持锁退出；
- 若锁已被他人持有（`held == 1`），交换后 `held` 依然保持为 1，函数返回值为 1，循环继续自旋等待。整个过程完全由硬件电路闭环锁死，杜绝了一切竞争冒险。

```python
def acquire(lock):
    while atomic_swap(1, lock.held) == 1:
        pass  # 若原本为 1 表明被别人持有，自旋重试；若原本为 0 则成功置 1 并退出

def release(lock):
    lock.held = 0  # 单个写指令在对齐内存上是天然原子的
```

---

## 5. 死锁成因与资源分配全序防范法则

当系统演进为多锁环境时（例如在两个不同账户之间转账需要同时持有两把锁），死锁幽灵再次浮现：

```python
# 线程 1: A 转账给 B
acquire(lock_A)
acquire(lock_B)

# 线程 2: B 转账给 A (并发执行)
acquire(lock_B)
acquire(lock_A)
```

::: definition 死锁的四大必要条件（Coffman 条件）
1. **互斥条件（Mutual Exclusion）**：资源一次只能被一个执行流独占；
2. **持有并等待（Hold and Wait）**：执行流持有着已有资源，同时申请新资源；
3. **不可剥夺（No Preemption）**：资源不能被强制抢占；
4. **循环等待（Circular Wait）**：存在闭环等待链条（$T_1 \to T_2 \to \dots \to T_1$）。
:::

::: theorem 全局锁偏序破环法则（Lock Ordering）
为了从根本上消除死锁，系统必须建立全序规则（Global Strict Ordering）：
**为系统中的所有互斥锁分配一个全局唯一的整数编号（例如按内存物理地址或账户 ID 排序）。所有线程必须严格按照升序依次获取锁！**
因为任何线程都只能从小号向大号申请锁，拓扑上绝不可能形成有向闭环，彻底根绝循环等待。
:::

---

## 我的理解

::: insight 架构师见解：从自旋锁到同步原语的演进哲学
1. **忙等待的物理罪恶与条件变量的诞生**：在版本 2 的有界缓冲区中，虽然解除了死锁，但 `release(lock); acquire(lock)` 的紧凑自旋在单核或多核系统上会以 100% 负荷狂烧 CPU，极度浪费能耗。更理性的工程解法是将自旋升级为**事件通知机制（Condition Variables / `wait` & `notify`）**：当缓冲区满时，生产者将自身线程挂入等待队列并交出 CPU（调用操作系统的 `yield` 或让步中断），直到消费者读走数据后发送信号唤醒，实现真正的零 CPU 浪费阻塞。
2. **锁的颗粒度与扩展性博弈**：粗粒度锁（Coarse-Grained Lock）逻辑简单不易出错，但在多核并行场景下会彻底摧毁系统吞吐；细粒度锁（Fine-Grained Lock）虽能提升并发度，却成倍增加了死锁与内存乱序的治理复杂度。现代高性能无锁队列（Lock-Free Queues，如 LMAX Disruptor）更进一步，彻底抛弃互斥锁，转而基于环形数组配合单调递增序列号与原子 CAS 指令，实现了单机每秒吞吐数千万级消息的高并发奇迹。
:::
