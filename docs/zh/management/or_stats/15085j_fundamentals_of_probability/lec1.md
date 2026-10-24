---
title: '概率模型公理体系、sigma-代数与测度空间 (Probabilistic Models & Measures)'
type: lecture
lecture: 1
tags: [probability-measures, sigma-algebra, kolmogorov-axioms, caratheodory-extension]
status: complete
---

# Lec 1 概率模型公理体系、sigma-代数与测度空间 (Probabilistic Models & Measures)

> MIT 15.085J / 6.436J 概率论基础 · 讲义 1 · 授课教师：Prof. John Tsitsiklis / Devavrat Shah

## TL;DR

- 柯尔莫哥洛夫公理体系以概率空间三元组 $(\Omega, \mathcal{F}, \mathbb{P})$ 奠定现代概率论基石。
- $\sigma$-代数（$\sigma$-field）在可数交并补运算下封闭，杜绝了非可测集带来的代数悖论。
- 卡拉西奥多里扩张定理（Carathéodory Extension）保证了从代数环到完整测度空间的唯一延拓。

## 1. 经典概率的危机与柯尔莫哥洛夫测度公理

在 20 世纪以前，概率论主要依赖拉普拉斯的古典“等可能度量”或几何概率模型（例如蒲丰投针、贝特朗奇论）。然而，随着连续不可数样本空间的引入，古典概率爆发了深刻的自相矛盾——即著名的**贝特朗悖论（Bertrand's Paradox）**：在同一个圆内随机绘制一条弦，其长度大于内接等边三角形边长的概率，由于“随机选取”的不同几何定义，可以分别算成 $1/2$、$1/3$ 甚至 $1/4$！

为了彻底消除这种主观歧义，前苏联数学大师安德雷·柯尔莫哥洛夫（Andrei Kolmogorov）于 1933 年出版了划时代的《概率论的基础概念》，**将概率论完全公理化为实分析与测度论的一个分支**。

现代概率论建立在**概率空间三元组（Probability Space）**之上：
$$(\Omega, \mathcal{F}, \mathbb{P})$$
1. **样本空间 $\Omega$（Sample Space）**：包含随机试验所有可能基本结果 $\omega$ 的全集；
2. **事件域 $\mathcal{F}$（Event Space / $\sigma$-Algebra）**：由 $\Omega$ 的子集构成的集合族；
3. **概率测度 $\mathbb{P}$（Probability Measure）**：定义在 $\mathcal{F}$ 上的实值集合函数。

```mermaid
flowchart LR
    subgraph ProbabilitySpace [概率空间三元组 (Omega, F, P)]
        Omega[样本空间 Omega: 所有随机结果 omega 的全集]
        F[事件域 F: 可数代数运算封闭的 sigma-代数]
        P[概率测度 P: 满足非负性、规范性与可数可加性]
    end
    Omega --> F
    F --> P
    P --> Event[为任意合法事件 A in F 赋予确定概率 P(A) in [0, 1]]
```

## 2. 为什么需要 $\sigma$-代数？非可测集的幽灵

初学者常问：为什么不能把样本空间 $\Omega$ 的所有子集构成的幂集 $2^\Omega$ 直接作为事件域？
答案是：**在不可数连续空间中，选择公理（Axiom of Choice）证明必然存在无法被赋予任何长度或体积的“病态怪兽”——非可测集（Non-measurable Sets）**（如 Vitali 集、Banach-Tarski 悖论）！
如果执意使用幂集，概率论必须丢弃其最核心的生命线——可数可加性。因此，数学家退而求其次，只在结构优良的子集族上定义概率：

::: definition $\sigma$-代数 ($\sigma$-Algebra)
样本空间 $\Omega$ 的子集集合族 $\mathcal{F} \subset 2^\Omega$ 称为一个 **$\sigma$-代数**，若满足以下三条公理：
1. **包含全集**：$\Omega \in \mathcal{F}$（由此必然包含空集 $\emptyset \in \mathcal{F}$）；
2. **对补集运算封闭**：若 $A \in \mathcal{F}$，则余集 $A^c = \Omega \setminus A \in \mathcal{F}$；
3. **对可数并集运算封闭**：若序列 $A_1, A_2, A_3, \dots \in \mathcal{F}$，则其可数并集依然属于该集合族：
$$\bigcup_{i=1}^\infty A_i \in \mathcal{F}$$
根据德摩根定律，$\mathcal{F}$ 对可数交集 $\bigcap_{i=1}^\infty A_i$ 同样自动封闭。
:::

在实数轴 $\mathbb{R}$ 上，由所有开区间 $(a, b)$ 生成的最小 $\sigma$-代数被称为**博雷尔 $\sigma$-代数（Borel $\sigma$-Algebra）**，记为 $\mathcal{B}(\mathbb{R})$。它包含了所有我们能够用微积分描述的区间、单点与离散集合。

## 3. 概率测度与卡拉西奥多里扩张定理

::: definition 柯尔莫哥洛夫概率公理
集合函数 $\mathbb{P}: \mathcal{F} \to [0, 1]$ 称为概率测度，若满足：
1. **非负性（Non-negativity）**：对任意 $A \in \mathcal{F}$，均有 $\mathbb{P}(A) \ge 0$；
2. **规范性（Normalization）**：全集概率为 1，$\mathbb{P}(\Omega) = 1$；
3. **可数可加性（Countable Additivity）**：若可数个事件 $A_1, A_2, \dots \in \mathcal{F}$ 两两互斥（$A_i \cap A_j = \emptyset, \forall i \ne j$），则：
$$\mathbb{P}\left( \bigcup_{i=1}^\infty A_i \right) = \sum_{i=1}^\infty \mathbb{P}(A_i)$$
:::

::: theorem 测度的连续性 (Continuity of Measure)
可数可加性等价于测度沿单调极限的连续性：
1. **下连续（Continuity from below）**：若 $A_1 \subset A_2 \subset A_3 \subset \dots$ 且 $\lim A_n = \bigcup A_n = A$，则 $\lim_{n \to \infty} \mathbb{P}(A_n) = \mathbb{P}(A)$；
2. **上连续（Continuity from above）**：若 $A_1 \supset A_2 \supset A_3 \supset \dots$ 且 $\lim A_n = \bigcap A_n = A$，则 $\lim_{n \to \infty} \mathbb{P}(A_n) = \mathbb{P}(A)$。
:::

::: theorem 卡拉西奥多里扩张定理 (Carathéodory's Extension Theorem)
设 $\mathcal{F}_0$ 是集合代数（仅对有限交并封闭），$\mathbb{P}_0$ 是定义在 $\mathcal{F}_0$ 上的非负规范可加测度。
则 $\mathbb{P}_0$ 能够**唯一确定地延拓（Unique Extension）**到由 $\mathcal{F}_0$ 生成的整个 $\sigma$-代数 $\sigma(\mathcal{F}_0)$ 上，并保持完全可数可加性！
:::

这一宏伟定理彻底解决了现代概率论的建造合法性：我们只需为最简单基础的有限区间定义概率（如区间长度 $b - a$），卡拉西奥多里机器就会自动为实数轴上几乎一切复杂的几何集合赋予绝对唯一的严谨概率值！

::: insight 测度论赋予概率论纯粹的公理尊严
很多初学者以为概率论只是“高级的高中排列组合加上几条正态分布公式”。
但 15.085J 开门见山地宣示：概率论不是统计经验的集合，而是实数分析中最高级的测度理论在总测度归一化为 1 时的特殊投影。
引入 $\sigma$-代数不是为了故弄玄虚，而是为了在无穷可数维度的风暴中，为人类的代数逻辑构筑一道永远不被悖论击穿的防波堤。只有站在测度论的坚实岩石上，大数定律与随机分析的高楼大厦才能稳立于世。
:::
