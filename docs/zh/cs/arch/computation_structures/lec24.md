---
title: 并发与同步
type: lecture
lecture: 24
tags: [concurrency, synchronization, semaphores, deadlock, mutual-exclusion]
status: complete
---
# Lec 24 并发与同步

## TL;DR
- **并发与同步动因**：多核共享内存通过 load/store 隐式通信，若无同步约束将引发数据竞争、未定义时序与脏写覆盖。
- **信号量统一原语**：Dijkstra 计数信号量同时满足先后依赖（Precedence）与临界区互斥（Mutual Exclusion），构建生产者-消费者双变量不变量。
- **死锁防范准则**：死锁源于互斥、持有并等待、不可抢占与循环等待四大条件；打破循环等待最有效的方法是建立全局锁偏序获取协议。

---

## 并发多线程与系统同步模型

我们已经学习 OS 通过时间片轮转让多个进程共享 CPU，现在进一步在单个进程内划分多个线程。由于现代 CPU 是多核的，系统尽可能并行执行多个线程。为了能够正确地配合执行任务，**必须通过同步（Synchronization）机制协调通信**。

## 同步

我们可以将计算任务分配给多线程执行：

- 多个**独立（independent）**的顺序线程，它们竞争共享资源
- 多个**协作（cooperating）**的顺序线程，他们相互通信

同步模型有两种：

- 基于**共享内存模型（shared memory）**，所有线程**共享同一地址空间**，通过写入某个内存地址，另外一个线程读取该地址即可通信
  - 优点是实现简单，就是 load/store 操作
  - 缺点是容易踩脚，产生数据竞争或冲突。
- 基于**消息传递模型（Message Passing）**，各线程**地址空间不同**，需发送/接收显式消息。
  - 优点：内存隔离强，不易踩脚
  - 缺点：通信开销大，协议实现复杂。

每当系统中存在并行进程时，就需要同步：

- fork-join ：并行进程可能需要等待多个事件发生
- 生产者-消费者：消费者进程必须等到生产者进程生成数据
- 互斥：操作系统必须确保资源在给定时间内仅由一个进程使用

![多线程协作执行中的同步与资源互斥模型](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/68046895026b3.png)

> [!IMPORTANT]
>
> 线程安全（Thread-safe），是指并行程序的输出和在单处理器上某一个串行执行结果一致，换句话说，即使并发执行，结果也可预测、正确。

> 进程之间如何通信？

Solution: 大致有几种：

- 共享内存
- 同步指令（需要硬件支持）。比如锁、信号量、原子操作
- 系统调用

## 引例：有界缓冲区问题

### 单字符缓冲区

有两个线程：Producer（生产者）：执行一系列操作，生成一个字符 `c`，然后发送给消费者；Consumer（消费者）：接收字符 `c`，然后执行一系列操作。

![单字符缓冲区生产者消费者无同步时序冲突](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/68060a59402b2.png)

每个线程内部是顺序执行的，但跨线程之间没有同步机制，可能出现以下问题：消费者在数据还没被生产时就尝试读取；生产者在数据还没被消费完就覆盖已有数据。

我们使用符号 `≺`（"precede"）来表示先后约束：

- 约束 1：先生产再消费：`Send(i) ≺ Receive(i)`，即生产者必须先发送第 `i` 个字符，消费者才能接收。
- 约束 2：不能覆盖未消费的旧数据：`Receive(i) ≺ Send(i+1)`，即生产者在发送第 `i+1` 个字符前，消费者必须完成对第 `i` 个字符的接收。

### FIFO 缓冲区

![定长环形FIFO缓冲区的前驱后继约束放宽](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/68060aace0d6a.png)

使用 FIFO 缓冲区放松约束。使用大小为 `n` 的 FIFO 缓冲区：允许生产者**最多领先消费者 `n` 步**；新约束变为 `Receive(i) ≺ Send(i+n)`。在生产者发送第 `i+n` 个字符前，消费者必须接收完第 `i` 个字符。

通常来说，会把这个 buffer 实现成**环形缓冲区（Ring buffer）**，原理缓冲区首尾相连，写满后从头写，用两个指针：`in`：生产者写的位置； `out`：消费者读的位置。

**示例**：

假设缓冲区大小为 `3`，初始时 `in == out == 0`：

1. 生产者写入 `c0` → `in = 1`；
2. 写入 `c1` → `in = 2`；
3. 写入 `c2` → `in = 0`（回绕）；
4. 缓冲区满了，必须等待消费者读取至少一个；
5. 消费者读取 `c0` → `out = 1`，此时缓冲区腾出一个位置；
6. 生产者继续写入下一个字符到位置 `0`。

![环形缓冲区读写指针回绕与满空状态判定](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20250904004010029.png)

```c
// Shared memory
char buf[N];  // The buffer
int in = 0, out = 0;

// Producer
void send(char c) {
  buf[in] = c;
  in = (in + 1) % N;
}

// Consumer
char rcv() {
  char c;
  c = buf[out];
  out = (out + 1) % N;
  return c;
}
```

代码有什么问题？  不能保证 precedence 限制，比如 rcv()均可能在任何 send()之前调用。我们将会更改这个代码，满足这些约束条件，为此我们将引入一种新的**编程结构**——**信号量（Semaphores）**，用于实现适当的进程间同步。

### 信号量

Dijkstra 于 1962 年提出，**信号量（Semaphores）**是特殊整型变量，始终$\ge$ 0，用于控制资源访问的并发数量或实现某种执行顺序（precedence）约束。

```c
semaphore s = K; // initialize s to K
```

信号量操作

```python
wait(semaphore s):
	wait until s > 0  # 如果 s == 0，则阻塞
  s = s - 1					# 获取资源（或占用一个槽）
```

```python
signal(semaphore s):
	s = s + 1 				# 释放资源（或归还一个槽）
```

语义保证： 当信号量初始化为 K，这确保了“最多允许 K 个并发”，或说“最多允许领先 K 步”

$signal(s)_i \prec wait(s)_{i+K}$

#### 信号量资源池抽象与双变量不变量

信号量不仅用于控制并发线程数量，更是在抽象层面上对有限物理资源池状态的守卫。设资源池容量为 $N$，信号量的当前整数值在数学上严格代表“当前可用的空闲资源项数”。

在有界缓冲队列（Bounded Buffer）中，单纯使用一个信号量只能约束单向依赖。例如仅用 `chars` 跟踪可用字符：

```c
// shared memory
char buf[N];
int in = 0, out = 0;
samaphore chars = 0; // 当前队列中已就绪待读的字符数量

// producer
void send(char c) {
  buf[in] = c;
  in = (in + 1) % N;
  signal(chars);
}

// consumer
char recv() {
  char c;
  wait(chars);
  c = buf[out];
  out = (out + 1) % N;
  return c;
}
```

> **设计缺陷剖析**：上述朴素实现虽然保证了“先生产后消费”（$Send(i) \prec Receive(i)$），但完全丧失了对写指针溢出的保护！当生产者速度远高于消费者时，生产者会无限制推进 `in` 指针，覆盖尚未被消费的数据，破坏了 $Receive(i) \prec Send(i+N)$ 约束。

为了同时双向约束生产与消费，必须引入**成对的双计数信号量**：
- `chars`：跟踪有效数据项个数，初始为 $0$，由生产者的 `signal` 增加、消费者的 `wait` 消耗；
- `spaces`：跟踪剩余空槽位个数，初始为 $N$，由生产者的 `wait` 申请、消费者的 `signal` 归还。

系统在任意时刻均维持严格的不变量（Invariant）：
$$\text{chars} + \text{spaces} = N$$

这种对称结构将先后约束映射为计数守卫：生产者受限于可用空间（`spaces`），消费者受限于可用数据（`chars`），双方在各自的信号量上阻塞等待，消除了缓冲区上溢与下溢风险。

正确的完整双信号量实现如下：

```c
// shared memory
char buf[N];
int in = 0, out = 0;
samaphore chars = 0;  // 初始有效数据为 0
samaphore spaces = N; // 初始可用空间为 N

// producer
void send(char c) {
  wait(spaces);       // 申请空槽位：若无空间则阻塞
  buf[in] = c;
  in = (in + 1) % N;
  signal(chars);      // 生产完毕，唤醒等待数据的消费者
}

// consumer
char recv() {
  char c;
  wait(chars);        // 申请有效数据：若队列空则阻塞
  c = buf[out];
  out = (out + 1) % N;
  signal(spaces);     // 读取完毕，腾出一个空槽位
  return c;
}
```

对于单个生产者和消费者， 用信号量管理的资源：字符、空间都采用 FIFO 机制。 但如果是**多个生产者和消费者**呢？ 将会遇到互斥的问题

#### 互斥

编写并发程序时，尤其是在修改共享数据时，对于某些代码段（称为**临界区 critical sections**）， 我们希望确保任何两次执行都不会重叠，这种约束称为**互斥（mutual exclusion）**

解决方案：将临界区嵌入包装器（例如“事务”）中，以保证其原子性，即，使它们看起来像是单个、瞬时的操作。

下面是用信号量也可以实现互斥的例子

```c
semaphore mutex = 1;

void debit(int amount) {
  wait(mutex);        // wait for exclusive access
  int bal = account.balance;
  bal = bal - amount;
  account.balance = bal;

  signal(mutex);      // 离开临界区（解锁）
}

```

锁控制了临界区的使用。使用锁，需要**考虑粒度大小**，比如

- 所有账户共用一把锁？
- 为每个账户分配一把？
- 还是以 004 解决的账户共用一把锁？

如果我们考虑多消费者、多生产者的模型，就需要考虑 buffer 的临界区问题了，因此我们需要再一次改动前面的代码

```c
// shared memory
char buf[N];
int in = 0, out = 0;
samaphore chars = 0;
samaphore spaces = N;
samaphore lock = 1; // 只有一个能访问

// producer
void send(char c) {
  wait(spaces);
  wait(lock);
  buf[in] = c;
  in = (in + 1) % N;
  singal(lock);
  signal(chars);
}

// consumer
char recv() {
  char c;
  wait(chars);
  wait(lock);
  c = buf[out];
  out = (out + 1) % N;
  signal(lock);
  singal(spaces);
  return c;
}
```

综上我们发现信号量的强大，我们仅仅同个一个原语就能能保证**互斥**和**先后**关系。先后关系有$send(i) \prec recv(i)$ 、$recv(i) \prec send(i+K)$

#### 实现

信号量本身是共享数据，实现`wait` 和 `signal`操作需要 读/修改/写 三步骤，这些序列必须作为临界区执行。那么，如何在不使用信号量的情况下保证这个临界区的互斥呢？

实现方式是：

- 使用特殊的原子指令（比如，Test-and-Set 指令），由硬件直接支持，这是最常见的方法。
- 使用系统调用实现他们。 仅适用于单核处理器，其中内核不可中断。

示例： 基于 TAS 实现锁

```c
bool lock = false;
void acquire_lock() {
  while (test_and_set(lock));
}
void release_lock() {
  lock = false;
}
```

同步的阴暗面：死锁。

## 死锁问题与打破循环等待

并发系统中最棘手的故障模式是死锁（Deadlock）——两个或多个线程无限期地互相等待对方持有的锁释放，导致整个流水线永久停摆。典型案例如多账户间的并发交叉转账：

```c
void transfer(int account1, int account2, int amount) {
  wait(lock[account1]);
  wait(lock[account2]);
  balance[account1] = balance[account1] - amount;
  balance[account2] = balance[account2] + amount;
  signal(lock[account2]);
  signal(lock[account1]);
}
```

考虑以下交错时序：
- 线程 1 执行 `transfer(6031, 6004, 100)`：已成功获取 `lock[6031]`，进而申请 `lock[6004]`；
- 线程 2 执行 `transfer(6004, 6031, 200)`：已成功获取 `lock[6004]`，进而申请 `lock[6031]`；
- 此时线程 1 等待线程 2 释放 `lock[6004]`，而线程 2 等待线程 1 释放 `lock[6031]`，两个线程均无法继续推进，形成死锁（Deadlock）。

### 死锁的四个必要条件（Coffman 条件）

根据 Coffman 定理，死锁发生必须同时满足以下四个充分必要条件：

1. **互斥（Mutual Exclusion）**：每个临界资源（如账户锁、打印机）在任意时刻至多被一个线程独占持有。
2. **保持并等待（Hold and Wait）**：线程在持有至少一个资源的同时，又申请被其他线程独占持有的新资源。
3. **不可抢占（No Preemption）**：资源不能被强制剥夺，只能由持有它的线程在完成任务后主动释放。
4. **循环等待（Circular Wait）**：存在一组处于等待状态的线程 $\{T_0, T_1, \dots, T_n\}$，其中 $T_0$ 等待 $T_1$ 持有的资源，$T_1$ 等待 $T_2$ 持有的资源，$\dots$，$T_n$ 等待 $T_0$ 持有的资源，形成环路。

### 打破死锁：全局锁偏序获取协议

在工程实践中，预防死锁最鲁棒且开销最小的方法是**破坏循环等待条件**。系统设计者为所有互斥资源定义一个严格的**全局全序关系（Total Order）**（例如按照账户 ID 从小到大的顺序获取锁）：

```c
void transfer_safe(int account1, int account2, int amount) {
  int first = (account1 < account2) ? account1 : account2;
  int second = (account1 < account2) ? account2 : account1;
  wait(lock[first]);
  wait(lock[second]);
  balance[account1] -= amount;
  balance[account2] += amount;
  signal(lock[second]);
  signal(lock[first]);
}
```

通过强制规定“无论谁向谁转账，一律先锁较小 ID、再锁较大 ID”，使得资源分配图（Resource Allocation Graph）永远保持有向无环（DAG），从微架构与算法层面彻底杜绝了循环等待。

::: insight
并发同步的本质是对“时钟偏斜（Clock Skew）”与“乱序内存访问（Weak Memory Ordering）”在软件语义上的强制拉齐。单靠软件内存读写无法跨核构建正确的互斥协议（如 Dekker/Peterson 算法在现代乱序弱一致性多核上因 store buffer 重排而失效），必须依赖底层硬件提供的原子指令（如 RISC-V 的 LR/SC 或 TAS）以及内存屏障（FENCE）。从体系结构视角看，锁与信号量是用微架构的原子总线锁定与缓存行失效传播，换取上层应用可推理的因果串行化保证。
:::
