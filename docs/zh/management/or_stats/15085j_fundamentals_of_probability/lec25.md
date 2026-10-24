---
title: '鞅论 I：条件期望作为正交投影、滤波与停时理论 (Martingales I: Filtration)'
type: lecture
lecture: 25
tags: [martingales, conditional-expectation, filtration, stopping-times, hilbert-space]
status: complete
---

# Lec 25 鞅论 I：条件期望作为正交投影、滤波与停时理论 (Martingales I: Filtration)

> MIT 15.085J / 6.436J 概率论基础 · 讲义 25 · 授课教师：Prof. John Tsitsiklis / Devavrat Shah

## TL;DR

- 条件期望 $\mathbb{E}[X \mid \mathcal{G}]$ 是希尔伯特空间 $L^2$ 中将随机变量向子空间做正交投影的唯一几何算子。
- 信息流滤波（Filtration $\mathcal{F}_t$）数学形式化了时间的单向流逝与信息积累。
- 鞅（Martingale）刻画了绝对公平博弈：未来在已知当前历史下的期望严格等于现状。

## 1. 现代概率论的最高山巅：鞅论（Martingales）

在随机数学的浩瀚宇宙中，如果说大数定律是地基，那么**鞅论（Martingale Theory）**就是高耸入云的巴别塔。由法国数学家保罗·列维与美国数学大师约瑟夫·杜布（Joseph L. Doob）奠基的鞅论，彻底统治了现代随机微积分、金融资产定价（无套利定价理论与 Black-Scholes 偏微分方程）、统计序贯分析与算法复杂度证明。

鞅的核心直觉源自博彩业中最古老的渴望——**绝对公平的博弈（Fair Game）**：
**无论你过去是赢是输、无论你采用多么精巧复杂的历史策略，在当前这一瞬间，你在下一轮博弈后所拥有的财富期望值，精确等于你当前手中已经持有的本金！**

为了严密形式化这一命题，必须首先彻底革新条件期望的数学定义。

```mermaid
flowchart TD
    subgraph HilbertProjection [希尔伯特空间 L^2 中的条件期望投影]
        Space[全空间 L^2(Omega, F, P): 包含一切随机变量 X]
        Subspace[闭子空间 L^2(Omega, G, P): 仅由子 sigma-代数 G 可测的变量张成]
        Space -->|最小均方误差正交投影 Operator| Subspace
        Subspace --> Projection[投影点唯一确定: Y = E[X | G]]
        Projection --> Orthogonal[正交残差性质: <X - E[X|G], Z> = 0 对所有 Z in L^2(G) 恒成立!]
    end
```

## 2. 条件期望的公理化革命：测度论与希尔伯特投影

在第 6 讲中我们接触了离散变量的条件期望。但在不可数连续空间中，“给定事件 $Y = y$”的概率为零，分母为零导致传统微积分公式彻底死锁！
柯尔莫哥洛夫给出了震撼世界的**公理化条件期望定义**：

::: definition 广义测度论条件期望
设 $(\Omega, \mathcal{F}, \mathbb{P})$ 为概率空间，$X \in L^1$ 为可积随机变量，$\mathcal{G} \subset \mathcal{F}$ 为子 $\sigma$-代数。
随机变量 $Y$ 称为 $X$ 关于 $\mathcal{G}$ 的**条件期望**，记作 $Y = \mathbb{E}[X \mid \mathcal{G}]$，若满足两大刚性条件：
1. **可测性（信息约束）**：$Y$ 是 $\mathcal{G}$-可测的；
2. **积分等价性（测度守恒）**：对于子代数中的**任意事件 $A \in \mathcal{G}$**，集合积分完全相等：
$$\int_A Y \, d\mathbb{P} = \int_A X \, d\mathbb{P}$$
由拉东-尼科迪姆定理，满足上述条件的随机变量 $Y$ **在几乎处处意义下存在且唯一**！
:::

在希尔伯特空间 $L^2(\Omega, \mathcal{F}, \mathbb{P})$（配备内积 $\langle X, Z \rangle = \mathbb{E}[X Z]$）中，条件期望正是**将任意随机变量 $X$ 正交投影到闭子空间 $L^2(\Omega, \mathcal{G}, \mathbb{P})$ 上的唯一投影算子**！
残差向量 $X - \mathbb{E}[X \mid \mathcal{G}]$ 与子空间内所有可测变量严格正交：
$$\mathbb{E}\left[ \left( X - \mathbb{E}[X \mid \mathcal{G}] \right) Z \right] = 0, \quad \forall Z \in L^2(\mathcal{G})$$

## 3. 信息流滤波、鞅与停时（Stopping Times）

时间在流逝，人类掌握的真实信息量随时间单调递增。这一客观物理规律在数学上被抽象为**滤波（Filtration）**：

::: definition 滤波与适应过程 (Filtration & Adapted)
1. **滤波（Filtration）**：子 $\sigma$-代数构成的单调递增族系 $\mathbb{F} = \{\mathcal{F}_n\}_{n \ge 0}$：
$$\mathcal{F}_0 \subset \mathcal{F}_1 \subset \mathcal{F}_2 \subset \dots \subset \mathcal{F}$$
$\mathcal{F}_n$ 包含了直到时刻 $n$ 为止系统全部可以观测到的历史信息；
2. **适应过程（Adapted Process）**：若对每个 $n$，$X_n$ 是 $\mathcal{F}_n$-可测的。
:::

::: definition 鞅、下鞅与上鞅 (Martingale)
适应过程 $\{X_n, \mathcal{F}_n\}_{n \ge 0}$ 称为：
1. **鞅（Martingale）**：若 $\mathbb{E}[|X_n|] < \infty$，且对所有 $n$ 恒满足：
$$\mathbb{E}[X_{n+1} \mid \mathcal{F}_n] = X_n$$
（未来期望严格等于现在：公平博弈）；
2. **下鞅（Submartingale）**：若 $\mathbb{E}[X_{n+1} \mid \mathcal{F}_n] \ge X_n$（未来期望上升：有利博弈）；
3. **上鞅（Supermartingale）**：若 $\mathbb{E}[X_{n+1} \mid \mathcal{F}_n] \le X_n$（未来期望下降：不利博弈/赌场现实）。
:::

在现实世界中，我们常常需要根据当前已经发生的信息决定何时离场（例如股票止损线、达到目标收益出场）。这种基于历史决定的随机时间被称为**停时（Stopping Time）**：

::: definition 停时 (Stopping Time)
随机变量 $\tau: \Omega \to \{0, 1, 2, \dots\} \cup \{+\infty\}$ 称为关于滤波 $\mathbb{F}$ 的**停时**，若对于每一个确定的时间点 $n \ge 0$，事件“在时刻 $n$ 或之前停止”仅由截止到时刻 $n$ 为止的信息就能做出判定：
$$\{\tau = n\} \in \mathcal{F}_n \quad (\text{或 } \{\tau \le n\} \in \mathcal{F}_n)$$
:::

停时严酷禁止“预知未来”：你可以决定“只要今天股价跌破 10 元我就抛售”（这是合法的停时），但你绝对无法决定“在明天股价达到最高峰的前一天抛售”（这不是停时，因为它依赖未来的信息）。

::: insight 投影视角将不确定性化为确定性几何
鞅论是数学分析中最震撼人心的对称性架构。
它把纷乱无章的随机演化，变成了希尔伯特空间中一系列单调嵌套子空间的正交投影序列。
在鞅的世界里，未来虽然充满未知，但它对现在的条件期望像磐石一样恒定。这种将动态随机演化，投影为静态函数空间内积几何的卓越智慧，构筑了现代量化金融无套利定价的全部数学灵魂。
:::
