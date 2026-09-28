---
title: Bluespec / Minispec 硬件综合
type: lecture
lecture: 8
tags: [bluespec, logic-synthesis, fsm, gcd-datapath]
status: complete
---
# Lec 8 Bluespec / Minispec 硬件综合

## TL;DR

- **高级综合映射**：方法综合为纯组合逻辑输出通路，规则综合为下一状态组合计算与寄存器时钟沿更新网络。
- **多周期计算架构**：以 GCD 辗转相减算法为例，利用寄存器时序反馈打破纯组合位宽限制，实现时间换空间的变长迭代。
- **守卫契约消除误用**：通过 `Maybe` 类型与带有 Guard 条件的接口，将就绪信号下沉为硬件级互锁，彻底杜绝中间态被非法采样的协议漏洞。

---

## 硬件高级综合与时序控制范式

[Lec 7](lec7.md) 建立了模块抽象（submodule / method / rule / input）。本讲聚焦**综合**：这些高级描述如何变成实际硬件，并用 GCD（最大公约数）这个**多周期 FSM** 完整走一遍“模块化设计一个时序计算”的流程。

## 综合模型：方法 + 规则 → 组合逻辑 + 寄存器

回顾 [Lec 6](lec6.md) 的时序电路：寄存器存状态，组合逻辑算“下一状态”和“输出”。在模块里：

- **方法（method）** 综合成算输出的组合逻辑；
- **规则（rule）** 综合成算下一状态的组合逻辑，并在每个时钟沿把结果 `<=` 进寄存器；
- **规则每个周期都触发一次**——它读当前状态与 input，算出 `<=` 的新值。

> 因此“写 Minispec ≈ 画出方法/规则两块组合逻辑，再把寄存器接上”。所有 `if`/`?:` 在组合逻辑里都成为 **mux**（[Lec 3](lec3.md)）；循环在编译期展开（[Lec 5](lec5.md)）。

## 多周期计算：GCD（欧几里得算法）

GCD 用辗转相减：当 `x >= y` 就 `x = x - y`；否则交换 `x, y`；直到 `x == 0`，此时 `y` 即结果。每一步是一拍，需要**多个周期**，正好体现“[时间比空间更灵活](lec7.md)”。

### Minispec 实现（朴素接口）

在朴素实现中，我们通过分离的数据输入端、启动控制信号与状态输出端来构建多周期欧几里得辗转相减数据通路：
1. **状态寄存器与数据通路**：实例化两个 32 位寄存器 `x` 和 `y` 保存操作数。在每个时钟周期，数据通路通过 32 位比较器评估 `x >= y`，通过 32 位减法器计算差值，并通过并行多路选择器根据比较结果决定将差值回写或直接交换两寄存器。
2. **非阻塞赋值的硬件交换**：借助 `<=` 在时钟沿统一更新的语义，`x <= y; y <= x;` 在硬件上直接映射为两组交叉连线，无需在数据通路中插入额外的临时暂存触发器。
3. **朴素控制信号的散落性**：外部控制器必须在拉高 `start` 的同一周期稳定驱动操作数 `a` 与 `b`；后续周期中控制器需要不断轮询 `isDone` 组合信号，直至其拉高后再从 `result` 端口采样最终计算值。

```minispec
typedef Bit#(32) Word;
module GCD;
  Reg#(Word) x(1);
  Reg#(Word) y(0);
  input Bool start default = False;
  input Word a default = 0;
  input Word b default = 0;
  rule gcd;
    if (start) begin
      x <= a; y <= b;                 // 装载新输入
    end else if (x != 0) begin
      if (x >= y) x <= x - y;         // 相减
      else begin x <= y; y <= x; end  // 交换（靠 <= 同周期生效，无需临时变量）
    end
  endrule
  method Word result = y;             // 结果
  method Bool isDone = (x == 0);      // 是否算完
endmodule
```

设置 `start = True` 并传入 `a, b` 即开始计算；若干周期后 `isDone` 变真，此时 `result` 给出答案。注意整段是**纯组合的条件**（综合成几个 mux + 减法器 + 比较器），由 `rule` 每周期推进一步。

### 这个接口很糟糕——为什么

> **踩坑**：上面接口**极易误用**：
> - 可能设了 `a/b` 却忘了 `start`；
> - 可能忘了先查 `isDone` 就去读 `result`（拿到中间结果）；
> - 即使 `start = False`，每周期也得把所有 input 都驱动一遍，很啰嗦。

根因仍是 [Lec 7](lec7.md) 强调的：**相关的输入/输出应当聚合**。理想接口只需两件事：一次性“启动（给全部参数，或一个都不给）”，以及取“一个**可能有效**的结果”。这要用到 `Maybe` 类型。

### `Maybe` 类型与干净接口

`Maybe#(T)` 要么 `Invalid`（无值），要么 `Valid(v)`（带值）；用 `isValid` 判断、`fromMaybe(d, m)` 取值。用它改写 GCD 的接口（Bluespec 风格，便于用守卫做自我保护）：

```bluespec
interface GCD;
  method Action            start(Bit#(32) a, Bit#(32) b);  // 一次给全参数
  method ActionValue#(Bit#(32)) getResult;                 // 取结果（守卫保证已算完）
endinterface

module mkGCD(GCD);
  Reg#(Bit#(32)) x <- mkReg(0);
  Reg#(Bit#(32)) y <- mkReg(0);
  Reg#(Bool)     busy <- mkReg(False);

  rule gcd (busy);                       // 仅在 busy 时推进
    if (x >= y && y != 0) x <= x - y;
    else if (y != 0) begin x <= y; y <= x; end
    // y == 0 ⇒ 结束（busy 在 getResult 里清除）
  endrule

  method Action start(Bit#(32) a, Bit#(32) b) if (!busy);  // 忙时不可启动
    x <= a; y <= b; busy <= True;
  endmethod

  method ActionValue#(Bit#(32)) getResult if (busy && y == 0); // 算完才可取
    busy <= False;
    return x;
  endmethod
endmodule
```

![带守卫接口的 GCD 模块状态转移与 Ready/Enable 信号交互流程](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6810cdd224655.png)

- `start` 的守卫 `if (!busy)`：**忙时拒绝再次启动**，避免覆盖正在进行的计算；
- `getResult` 的守卫 `if (busy && y == 0)`：**只有算完才能取**，从结构上杜绝“读到中间结果”；
- 方法的硬件信号见 [Lec 7](lec7.md)：`start` 是 Action（输入 + enable + ready），`getResult` 是 ActionValue（enable + 输出 + ready）。

模块的输入输出端口正是由其**接口**决定的：`start(a,b)` 对应两个输入端口，`getResult()` 对应一个输出端口（外加各自的 ready/enable 握手线）。

![基于守卫方法综合生成的硬件数据通路与握手控制逻辑结构](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20250429230615513.png)

## 硬件综合与接口契约总结

- **综合**：method→输出组合逻辑，rule→下一状态组合逻辑 + 寄存器更新；rule 每周期触发。
- **多周期模块**让我们能做组合逻辑做不到的变长计算（GCD、串行加法器……）。
- **好接口 = 聚合相关 I/O + 用 `Maybe` 表达有效性 + 用守卫自我保护**，让误用在结构上不可能发生——这正是 [Lec 7](lec7.md) FIFO 故事的教训落地。

## 我的理解

::: insight
### Bluespec 原子规则调度与门级冲突仲裁的本质

在传统 RTL（如 Verilog/VHDL）中，多周期状态机的并发互斥逻辑全靠工程师手工编写有限状态机（FSM）的独热码或二进制跳转逻辑。一旦系统演化为多个并发运行的子任务，跨状态转换的竞争冒险极难排查。

Bluespec / Minispec 的底层综合编译器解决这一问题的核心在于**形式化的一步一规则（One-Rule-at-a-Time, ORAAT）语义**：
1. **读写集合冲突分析**：编译器为每条规则自动推导读取集（Read Set）与写入集（Write Set）。若两条规则 `R1` 与 `R2` 试图在同一时钟周期写入同一个寄存器，或者一条规则修改了另一条规则守卫所依赖的状态，编译器判定二者发生资源冲突或次序冲突。
2. **隐式优先级编码器合成**：面对冲突，编译器不会生成不确定的未定义网表，而是根据预设或推导的优先级策略，自动合成为带使能优先级的多路选择树（Priority Encoder）。若调度器发现 `R1` 激活，则 `R2` 的硬件 `enable` 信号被组合逻辑强制置低，使其推迟至下一可用周期执行。
3. **原子事务的形式化可证明性**：这种硬件综合模型从根本上将硬件并发执行等价为顺序执行的一个合法交错（Interleaving），使得系统级不变式（Invariants）在时序硬件中能够像数据库事务一样被精确证明与约束。
:::
