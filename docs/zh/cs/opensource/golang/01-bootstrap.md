---
title: 运行时启动流程与汇编自举
type: lecture
lecture: 1
tags: [runtime, assembly, bootstrap, sysmon]
status: complete
---

# 运行时启动流程与汇编自举

## TL;DR

- Go 程序启动始于底层汇编入口 `runtime.rt0_go`，负责初始化 `g0` 栈、线程本地存储（TLS）以及主线程 `m0`。
- `schedinit` 完成内存分配器、垃圾回收器、调度器及 `GOMAXPROCS` 逻辑处理器的初始化，并构建首个用户 Goroutine `runtime.main`。
- Go 运行时巧妙地将抢占信号伪装为“栈溢出”：通过改写 `stackguard0` 为特殊常量，让函数序言的栈检查触发并拦截执行流。
- `sysmon` 是脱离 P 独立运行的高优先级监控线程，负责抢占超时 Goroutine、剥离阻塞在系统调用的 P，并驱动网络轮询器与定时器。

## 启动入口与汇编自举

操作系统内核在加载 Go 二进制文件后，控制权由 `_start` 跳转至各架构专属的汇编代码文件 `runtime/asm_<isa>.s` 中的 `runtime.rt0_go()`。

整个自举过程分为三个关键阶段：
1. **建立底层运行时结构**：设置线程系统栈、TLS（Thread Local Storage）、绑定 `g0` 与主线程 `m0`。
2. **初始化核心运行时子系统**：在无 Cgo 状态下依次调用 `runtime.check`、`runtime.osinit`（信号与定时器初始化）与 `runtime.schedinit`（调度器与内存分配器核心初始化）。
3. **点火调度器**：调用 `runtime.newproc` 创建第一个 Goroutine（执行 `runtime.main`），随后调用 `runtime.mstart` 驱动主线程 `m0` 正式进入调度循环。

### RISC-V 汇编实现剖析

在实际的 CPU 物理执行中，Go 编译器和汇编器必须在操作系统内核移交 CPU 控制权时，迅速搭建起满足 Go 语言执行环境的必要上下文。这包括栈基地址初始化、TLS 寄存器绑定、参数复制以及系统检查。

以 `runtime/asm_riscv64.s` 为例，汇编入口 `runtime.rt0_go` 的主要步骤如下：
1. **栈指针调整与传参保护**：调整硬件栈指针寄存器 `X2`（即 `SP`），为命令行参数 `argc`（寄存器 `A0`）和 `argv`（寄存器 `A1`）分配临时保存空间。
2. **初始化系统 Goroutine g0**：加载静态符号 `$runtime.g0(SB)` 至专属伪寄存器 `g`，并在操作系统栈上开辟 64KB 临时栈空间，同时设置高低地址界限 `g0.stack.hi` 与 `g0.stack.lo`。
3. **建立线程双向绑定**：将主线程变量 `$runtime.m0(SB)` 加载到临时寄存器，设置 `m0.g0 = g0` 与 `g0.m = m0`，确立 Go 运行时调度器的初始锚点。
4. **触发运行时子系统自检**：在准备好的系统栈环境下，依次调用基础类型大小检查、信号初始化 `osinit` 以及调度器初始化 `schedinit`。
5. **创建首个主 Goroutine 并启动调度器**：通过 `runtime.newproc` 包装 `runtime.mainPC` 入口函数并加入就绪队列，最后由 `runtime.mstart` 启动物理线程的调度轮询。

以下为对应的完整汇编实现：

```asm
// 声明汇编函数 rt0_go（NOSPLIT 禁用栈分裂，TOPFRAME 标明调用栈顶）
TEXT runtime·rt0_go(SB),NOSPLIT|TOPFRAME,$0
    // 保存命令行参数 argc, argv 到当前系统栈
    SUB $24, X2
    MOV A0, 8(X2)   // argc
    MOV A1, 16(X2)  // argv

    // 绑定 g0 到当前物理线程的 TLS/系统栈空间
    MOV $runtime·g0(SB), g
    MOV $(-64*1024), T0         // 分配 64KB 临时工作栈
    ADD T0, X2, T1
    MOV T1, g_stackguard0(g)    // 设置栈保护边界下界
    MOV T1, g_stackguard1(g)    // 保存真实栈边界以支持抢占恢复
    MOV T1, (g_stack+stack_lo)(g)
    MOV X2, (g_stack+stack_hi)(g)

    // 绑定 m0 与 g0：m0.g0 = g0, g0.m = m0
    MOV $runtime·m0(SB), T0
    MOV g, m_g0(T0)
    MOV T0, g_m(g)

    // 运行时架构校验与命令行参数解析
    CALL runtime·check(SB)
    CALL runtime·args(SB)
    CALL runtime·osinit(SB)
    CALL runtime·schedinit(SB)

    // 创建主 Goroutine：包装 runtime.mainPC 入口
    MOV $runtime·mainPC(SB), T0
    SUB $16, X2
    MOV T0, 8(X2)
    MOV ZERO, 0(X2)
    CALL runtime·newproc(SB)
    ADD $16, X2

    // 启动当前线程 M 的调度循环，永不返回
    CALL runtime·mstart(SB)
    WORD $0 // 异常防护：若 mstart 返回则直接崩溃
    RET
```

::: definition SB（Static Base Register）
在 Go 汇编语法中，`SB` 并非硬件 CPU 上的物理寄存器，而是链接器（Linker）约定的一种虚拟基址符号。`foo(SB)` 表示全局变量或函数 `foo` 的内存地址；`$foo(SB)` 表示获取该符号的立即数地址。
:::

## 线程启动与 mstart 调度流水线

`mstart()` 是所有新线程（M）在汇编层的统一入口，调用 `mstart0()` 完成初始化后进入 `mstart1()`：

1. **信号栈与屏蔽字设置**：
   - `minitSignalStack()`：为当前线程分配专用的备用信号栈。当发生致命异常（如栈溢出或 SIGSEGV）时，操作系统可在独立的信号栈上执行信号处理函数，避免因普通栈空间耗尽而无法报告错误。
   - `minitSignalMask()`：屏蔽非必要信号，仅放行运行时关注的信号（如 Linux 下的 `SIGSEGV`、`SIGBUS`、`SIGURG` 等）。
2. **绑定逻辑处理器 P**：通过 `acquirep(pp *p)` 将物理线程 M 与逻辑处理器 P 关联，并刷新当前 P 的本地内存缓存 `pp.mcache`。
3. **调度循环 `schedule()`**：线程进入无限调度循环，通过 `findRunnable()` 查找可运行的 Goroutine 并切换执行上下文。

### 核心调度轮询机制：findRunnable

`findRunnable()` 是调度器的任务分配枢纽，按如下优先级顺序寻找可执行的 G：
1. 当前 P 的本地队列（`runnext` 与 `runq`）。
2. 全局运行队列（`sched.runq`）。
3. 网络轮询器（`netpoll`）唤醒的 I/O 就绪 Goroutine。
4. 运行就绪的定时器任务（Timers）。
5. 从其他 P 的本地队列中进行工作窃取（Work-Stealing）。

## 协作抢占的栈溢出伪装机制

在 Go 1.14 引入信号抢占之前，Go 依赖协作式抢占。其底层机制精妙地复用了编译器自动插入的“栈扩容检查”逻辑：

```text
高地址（栈顶）        ← 栈向低地址增长
|-------------------| ← g.stack.hi
|  函数的局部变量   |
|-------------------| ← 当前 SP
|  剩余可用栈空间   |
|-------------------| ← g.stackguard0 = g.stack.lo + _StackGuard
|  栈保护“危险区”   |
|-------------------| ← g.stack.lo（栈底）
```

编译器在每个非叶子函数的序言（Prologue）阶段自动生成栈边界检查汇编：

```asm
CMP SP, g.stackguard0
JLS runtime.morestack // 若 SP < stackguard0，说明可用栈不足，跳转扩容
```

::: insight
**抢占伪装设计**：当调度器希望抢占一个长时间运行的 Goroutine 时，直接将其 `g.stackguard0` 改写为预设的特殊标记常量 `StackPreempt`（`0xfffffade`）。
由于无符号比较下当前物理 `SP` 必然大于该值（在地址空间高位），下次该 Goroutine 只要执行任何函数调用，就会误以为栈空间不足而跳入 `runtime.morestack`。
在 `morestack` 内部，运行时检查发现触发扩容的原因是 `StackPreempt`，于是顺理成章地将当前 G 挂起移入就绪队列，实现抢占！原来的真实栈边界早已提前保存在 `g.stackguard1` 中，恢复执行时再重新换回。
:::

## 核心系统后台守护进程

### 系统监控线程：sysmon

`sysmon`（System Monitor）是 Go 运行时中地位极为特殊的常驻系统线程：
- **无 P 运行**：`sysmon` 独立运行于操作系统线程上，不绑定任何逻辑处理器 P。因此，`sysmon` 的执行**严禁使用任何写屏障**。
- **动态生命周期调节**：由 `runtime.main` 通过 `systemstack` 调用 `newm(sysmon, nil, -1)` 显式拉起。

`sysmon` 在主循环中执行如下核心职责：
1. **抢占长时间运行的 G**：检测连续运行超过 10ms 的 Goroutine，下发抢占标记（协作标记或 `SIGURG` 信号）。
2. **系统调用解绑（handoffp）**：发现某个 P 在系统调用中被阻塞超过 10ms，强制将该 P 与当前 M 解绑，转交给空闲 M 继续消费队列任务。
3. **网络轮询注入**：周期性轮询 `netpoll`，将就绪的 Goroutine 唤醒并投入全局队列。
4. **内存回收巡检**：超过 2 分钟未发生垃圾回收时，强制唤醒 GC Worker 执行兜底垃圾回收；同时唤醒 Scavenger 归还物理内存。

### 定时器（Timers）与终结器（Finalizers）

- **Timer 驱动机制**：现代 Go 将定时器四叉堆与 P 紧密结合，每个 P 维护私有的定时器堆，大幅减少了早期集中全局锁引起的激烈争用。
- **Finalizer 协同 Goroutine**：当用户为对象挂载 `runtime.SetFinalizer` 时，垃圾回收阶段扫描出的孤立可析构对象会被加入终结器链表，由系统专职的 `finalizer` Goroutine 负责消费并安全执行回调。
