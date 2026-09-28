---
title: Go 内存模型与并发重排序
type: lecture
lecture: 5
tags: [memory-model, sequential-consistency, happens-before, synchronization]
status: complete
---

# Go 内存模型与并发重排序

## TL;DR

- 硬件与编译器为提升执行性能广泛采用指令重排序与写缓冲（Store Buffer），使得并发程序背离直观的顺序一致性（SC）。
- DRF-SC（无数据竞争即顺序一致性）是现代语言共识：只要程序不存在未同步的并发读写竞争，其执行表现就等价于全局串行交错。
- 与 C/C++ 允许数据竞争引发任意未定义行为（Undefined Behavior / Catch Fire）不同，Go 拒绝“凭空产生值”（Out-Of-Thin-Air），并将并发冲突视为错误。
- Go 内存模型基于 Happens-Before 偏序关系定义跨 Goroutine 的可见性，覆盖了 Goroutine 生命周期、Channel 缓冲通信、`sync.Mutex` 与 `sync.Once` 的同步界限。

## 硬件内存一致性基线

在单核处理器上，由于硬件和编译器严格维护“单线程程序逻辑不变性”（As-If 规则），程序员无需关心底层重排序细节。然而在多核并发环境下，内存读写可见性变得极其微妙。

```c
// 假设全局变量 x = 0, done = 0
// 处理器 1 (Thread 1)        // 处理器 2 (Thread 2)
x = 1;                        while (done == 0) { /* 循环等待 */ }
done = 1;                     print(x);
```

在多核物理机上，Thread 2 最终打印出 `x` 的值是否可能为 `0`？
答案是：**完全可能**。在 ARM 或 POWER 架构弱内存模型下，或者当编译器将循环内的读操作提升到寄存器优化时，Thread 2 可能会观察到 `done == 1` 但读取到的 `x` 依然是初始值 `0`。

### 顺序一致性与试金测试（Litmus Test）

Leslie Lamport 在 1979 年提出了**顺序一致性（Sequential Consistency, SC）**模型：程序在多核环境下的所有可能执行结果，都等价于各个线程的操作按照某种全局顺序进行串行交错（Interleaving），且每个线程内部的操作严格维持源代码顺序。

为了判断特定硬件或运行时是否满足顺序一致性，计算机科学采用**试金测试（Litmus Test）**：

::: example 试金测试：消息传递（Message Passing）
```c
// 初始状态: x = 0, y = 0
// 线程 1                      // 线程 2
x = 1;                        r1 = y;
y = 1;                        r2 = x;
```
终态是否可能出现 $r_1 = 1 \land r_2 = 0$？
- **在顺序一致性硬件上**：绝不可能。因为 $r_1 = 1$ 意味着 `y = 1` 已经完成，根据程序顺序 `x = 1` 必先于 `y = 1` 发生，故读操作 $r_2$ 必将观察到 `x = 1`。
- **在 x86-TSO（Total Store Order）上**：不可能。x86 保留了全局总存储顺序。
- **在 ARM/POWER 宽容弱内存模型上**：**完全可能**。处理器允许写操作相互重排序，或者读操作提前投机执行。
:::

### x86-TSO 与写缓冲队列（Store Buffer）

现代主流服务器大多采用 x86-64 架构。x86 提供了较强的 TSO 模型：每个核心拥有一个私有的先进先出（FIFO）**写缓冲队列（Store Buffer）**。

核心发起的写操作首先进入本地 Store Buffer，随后立刻继续执行后续指令，而无需同步等待物理写入 DRAM 或 L3 缓存。由于每个核心仅能观察自己的写缓冲区，不能观察其他核心的缓冲区，导致了著名的**写缓冲测试（Store Buffer Test）**异常：

```c
// 初始状态: x = 0, y = 0
// 核心 1                      // 核心 2
x = 1;                        y = 1;
r1 = y;                       r2 = x;
```

在 x86 物理执行中，核心 1 和核心 2 都将写操作暂存于本地写队列，随后并行执行读指令从全局主存中读出旧值，导致观测到 $r_1 = 0 \land r_2 = 0$！
为了在关键时刻强制建立顺序，CPU 提供了**内存屏障（Memory Barrier / Fence）**指令（如 x86 的 `MFENCE`），清空写队列并强行刷新缓存一致性。

::: definition DRF-SC 定理（Data-Race-Free Sequential Consistency）
硬件与高级编程语言之间达成的核心契约：**只要程序员编写的并发程序中不存在任何未加同步的数据竞争（Data Race），那么编译器和硬件将联手保证该程序的执行行为与理想的顺序一致性（SC）完全一致。**
:::

## Go 语言内存哲学与竞争边界

与 C/C++11 内存模型将数据竞争归类为完全失控的未定义行为（Undefined Behavior，允许编译器假设竞争不可能发生从而抹除保护代码）不同，Go 坚持更保守实用的工程哲学：

1. **将竞争定性为程序缺陷**：Go 官方坚决推行“竞争即 Bug”理念，并提供高度集成的内存竞态检测器（`go test -race`），在开发测试期拦截潜在竞争。
2. **拒绝凭空捏造（No Out-Of-Thin-Air）**：即便存在数据竞争，Go 运行时对于机器字长（Word-sized）以内的内存读取，也坚决保证读取到的必须是某一个 Goroutine 真实写入过的有效值，严禁凭空伪造不受控的内存垃圾数据。

::: pitfall
对于大于一个机器字长的数据结构（如包含 3 个字段的 `slice` 头部，或由 `tab` 与 `data` 构成的 `interface`），如果发生非同步的并发读写，Goroutine 可能读取到**半更新的残缺结构体**（例如指向新数组的指针配合旧长度，或不匹配的类型元数据与数据指针），引发致命的内存段错误崩溃。
:::

## Happens-Before 偏序关系全集

Go 语言内存模型通过数学上的严格偏序关系定义事件的相对发生顺序：如果事件 $e_1$ 发生在事件 $e_2$ 之前，记作 $e_1 \prec e_2$（$e_1$ happens before $e_2$）。此时，$e_1$ 对内存的写入对 $e_2$ 绝对可见。

### 单 Goroutine 内部顺序

在单个 Goroutine 内部，读写操作严格遵循源代码顺序所体现的依赖结果：
$$W \prec R$$
编译器允许在单线程逻辑不变的前提下任意乱序重排，但多核并发视角下不可依赖此无锁假设。

### Goroutine 生命周期事件

1. **Goroutine 创建**：执行 `go` 关键字创建新 Goroutine 的语句，Happens-Before 该新 Goroutine 内部所有代码的物理开始执行：
   ```go
   var a string
   func f() {
       print(a) // 保证打印 "hello"
   }
   func main() {
       a = "hello"
       go f()
   }
   ```
2. **Goroutine 退出**：Goroutine 内部所有执行的完成，**并不保证** Happens-Before 外部观察者的任何事件。必须通过通道或锁显式等待。

### Channel 通信同步法则

Channel 是 Go 中最基础的 Happens-Before 关系构建者：

1. **无缓冲 Channel 同步交汇（Rendezvous）**：
   从无缓冲通道完成一次接收，Happens-Before 对应的发送操作返回；同时，发送操作准备就绪，Happens-Before 接收操作完成。两者构成硬性时间同步屏障。
2. **带缓冲 Channel 容量屏障**：
   向容量为 $C$ 的通道执行的**第 $k$ 次发送**，Happens-Before 从该通道完成的**第 $k$ 次接收**。反之，第 $k$ 次接收完成，Happens-Before 第 $k + C$ 次发送操作完成。
3. **通道关闭（Close）**：
   执行 `close(ch)` 操作，Happens-Before 任何接收者从该 Channel 读取到表示通道已关闭的零值返回值。

### 互斥锁与 sync 包机制

- **`sync.Mutex` / `sync.RWMutex`**：对同一把互斥锁的第 $n$ 次 `Unlock()` 调用，Happens-Before 任何后续发起的第 $n+1$ 次 `Lock()` 成功返回。
- **`sync.Once`**：`once.Do(f)` 中传入的函数 `f()` 执行完成，Happens-Before 任何后续并发或串行调用的 `once.Do(f)` 返回。调用返回时，`f` 的所有副作用对外部完全可见。

::: insight
Go 内存模型的终极指导思想只有一句话：“**永远不要依赖指令交错的侥幸心理来编写免锁并发代码**”。
许多开发者试图用无锁标志位（如 `for !flag {}`）进行跨 Goroutine 状态通知，这种写法由于缺乏显式的 Happens-Before 关系约束，在硬件弱内存架构和编译器激进优化下极易引发无限死循环或读取过期内存。正确姿势始终是使用 `sync/atomic` 强顺序原子指令、`sync.Mutex` 或显式 Channel 进行同步。
:::
