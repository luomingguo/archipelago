---
title: '时序电路与模块设计（Sequential Circuits & Module Design）'
type: lecture
lecture: 2
tags: [sequential-circuits, bsv-rules, atomic-transactions, fifo-design, multiplier-tradeoffs]
status: complete
---
# Lec 02 时序电路与模块设计（*Sequential Circuits & Module Design*）

## TL;DR

- 时序电路将状态寄存器与组合逻辑相结合，在时钟上升沿同步更新内部状态。
- BSV 的规则（Rule）具备原子性（One-Rule-at-a-Time 语义），由守护条件（Guard）保护执行时机。
- 弹性流水线依赖 Guarded Interface 与双元素 FIFO，解决单元素 FIFO 入队与出队的调度冲突（Conflict Free）。
- 比较组合、折叠与流水线乘法器，展示了在时钟频率、计算延迟、吞吐量和硅片面积之间的经典体系结构权衡。

> MIT 6.1920 · Constructive Computer Architecture
> 讲师：Arvind · 日期：2024-02-08

## 1. 时序电路的本质

::: definition
**定义 — 时序电路（*Sequential Circuit*）**

时序电路是组合逻辑 + 状态寄存器的组合。每个时钟周期，寄存器先读取旧值，经组合逻辑计算后，在时钟上升沿（*rising edge*）写入新值。
:::

寄存器的 BSV 声明：

```bsv
Reg#(Bit#(32)) x <- mkReg(0);    // 初始值为 0
Reg#(Bit#(32)) y <- mkRegU;      // 初始值不确定
```

读取是组合操作（`x` 即当前值）；写入 `x <= expr` 在时钟沿执行。

---

## 2. GCD 算法的 BSV 实现

最大公约数（*Greatest Common Divisor, GCD*）利用辗转相减法：

$$\gcd(a, b) = \begin{cases} a & \text{if } a = b \\ \gcd(a-b, b) & \text{if } a > b \\ \gcd(a, b-a) & \text{if } a < b \end{cases}$$

BSV 规则实现：

```bsv
rule swap (a > b);
    a <= b;
    b <= a - b;
endrule

rule sub (a <= b && a != 0);
    b <= b - a;
endrule
```

::: definition
**定义 — 规则（*Rule*）**

规则是 BSV 的基本执行单元，包含条件（*guard*）和动作体（*body*）。规则在条件为真时可以触发；每个时钟周期，调度器（*scheduler*）选择一个或多个兼容规则执行。
:::

### 2.1 带接口的 GCD 模块

```bsv
interface GCD;
    method Action start(Bit#(32) a, Bit#(32) b);
    method ActionValue#(Bit#(32)) getResult;
endinterface
```

::: theorem
**推论 — 保护接口（*Guarded Interface*）**　BSV 方法可以携带隐式条件（guard）。`start` 方法只在模块空闲时可调用（例如 `a == 0`）；`getResult` 只在结果就绪时可调用。调用者无需显式检查——guard 自动组合在上层规则的条件中。
:::

---

## 3. FIFO 设计

### 3.1 一元素 FIFO（*1-Element FIFO*）

```text
状态：Reg#(Maybe#(t)) data  ← tagged Invalid（空）
enq(x)：data <= tagged Valid x；条件：!isValid(data)
deq   ：data <= Invalid；条件：isValid(data)
first ：return fromMaybe(?, data)；条件：isValid(data)
```

**限制**：enq 和 deq 不能在同一周期并发执行（SC 冲突）。

### 3.2 两元素 FIFO（*2-Element FIFO*）

增加第二个寄存器，使入队和出队可以在同一周期进行：

```text
状态：d0, d1（两个 Maybe 寄存器）
enq：写入空槽
deq：移动 d1 → d0，清空 d1
```

::: theorem 推论 — 流水线吞吐量
两元素 FIFO 允许 enq CF deq（无冲突并发），使得上下游规则可同一周期同时触发，实现吞吐量为 1 的弹性流水线（*elastic pipeline*）。
:::

---

## 4. 时序乘法器设计

### 4.1 折叠乘法器（*Folded Multiplier*）

通过重复使用 **1 个** `add32` 电路，迭代 31 次完成 32 位乘法：

```bsv
Reg#(Bit#(32)) partial_product <- mkReg(0);
Reg#(Bit#(32)) x <- mkReg(0);
Reg#(Bit#(6))  i <- mkReg(32);  // 初始为 32 表示空闲

rule mul_step (i < 31);
    if (x[0] == 1) partial_product <= partial_product + (b << i);
    x <= x >> 1;
    i <= i + 1;
endrule
```

### 4.2 三种乘法器比较

::: example 例题 — 乘法器设计权衡

:::

| 类型 | 延迟（周期） | 吞吐量 | 硬件面积 |
|------|------------|--------|---------|
| 组合（*Combinational*） | 1 | 1 | 大（32 个 add32）|
| 折叠（*Folded Sequential*） | 31 | 1/31 | 小（1 个 add32）|
| 流水线（*Pipelined*） | 31 | 1 | 大（31 个 add32）|

Sol：折叠乘法器面积最小但吞吐量最低；流水线乘法器吞吐量恢复为 1，面积与延迟各取折中。

---

## 5. 模块化与抽象

::: definition
**定义 — 接口（*Interface*）**

BSV 中 `interface` 定义模块的外部可见 API（方法集合），与模块实现解耦。任何满足同一接口的模块都可以替换，实现硬件多态性（*polymorphism*）。
:::

**`if` 条件 vs. `guard` 条件的区别**：
- `if` 在规则体内：条件为假时规则仍可触发，但不执行该分支
- `guard` 在接口方法上：条件为假时整个调用该方法的规则**不能触发**

---

## 核心机制小结与设计权衡

时序电路通过寄存器保持状态，BSV 的规则语义保证每个规则原子执行；GCD、FIFO 和迭代乘法器是时序电路的典型案例，三种乘法器设计揭示了面积—延迟—吞吐量之间的经典权衡。

## 核心机制思考与底层洞察

::: insight 规则原子语义（ORAAT）与硬件并行的张力调和
BSV 规则最迷人的特质在于其 **One-Rule-at-a-Time (ORAAT)** 形式化语义与物理硬件高并发之间的对立统一：

1. **认知抽象层：串行原子事务**：在设计者的概念世界中，每个 Rule 都是不可分割的原子事务。你只需要证明：当系统处于一致性状态 $S$ 时，任一激活的规则 $R_i$ 单独触发后，产生的新状态 $S'$ 仍然合法。这从根本上消除了经典 Verilog 中多进程竞争冒险、时钟跨域和隐式时序冒险等令人头疼的心智负担。
2. **硬件综合层：自动并行调度**：真实芯片不可能每个周期只执行一个规则。BSV 编译器充当了硬件事务调度器：它对所有规则的读写集合进行精细的形式化依赖分析（Read/Write Sets）。如果两条规则 $R_1$ 与 $R_2$ 互不干扰（Conflict-Free），硬件调度逻辑会在同一周期内同时发射执行它们；如果存在前向读写关系，编译器自动生成穿透旁路或定序逻辑（$R_1 < R_2$）；只有存在双向写冲突时才强制互斥仲裁。这种将复杂的并发正确性证明交给编译器算法的能力，正是建构式硬件设计能驾驭乱序多核芯片的核心基石。
:::
