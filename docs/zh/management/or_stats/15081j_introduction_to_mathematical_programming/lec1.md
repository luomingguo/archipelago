---
title: '线性规划建模、分段线性目标与绝对值转化 (Formulations & Piecewise Linear)'
type: lecture
lecture: 1
tags: [linear-programming, piecewise-linear, chebyshev-approximation, lp-modeling]
status: complete
---

# Lec 1 线性规划建模、分段线性目标与绝对值转化 (Formulations & Piecewise Linear)

> MIT 15.081J / 6.251J 数学规划导论 · 讲义 1 · 授课教师：Prof. Dimitris Bertsimas / John Tsitsiklis

## TL;DR

- 线性规划（LP）以线性等式与不等式刻画凸多面体可行域，追求线性目标函数的极值。
- 凸分段线性凸函数与 $L_1$、$L_\infty$（切比雪夫）范数可通过引入辅助变量精确转化为标准 LP。
- 建模的艺术在于识别隐藏的线性凸结构，严格防范非凸极大化与严格不等式陷阱。

## 1. 线性规划的数学抽象与标准形式

线性规划（Linear Programming, LP）是现代应用数学与运筹学最核心的理论基石之一。在实际工业决策与运筹优化中，无论是跨国航空公司的机组排班、全球供应链的物流中继调度，还是高频量化交易中的资产组合再平衡，都可以抽象为一个在多维仿射约束下优化线性目标函数的数学问题。

线性规划的标准形式（Standard Form）通常表述为：

$$\begin{aligned}
\min_{x} \quad & c^T x \\
\text{s.t.} \quad & A x = b \\
& x \ge 0
\end{aligned}$$

其中 $c \in \mathbb{R}^n$ 为成本向量，$A \in \mathbb{R}^{m \times n}$ 为约束矩阵（通常假设 $\operatorname{rank}(A) = m < n$），$b \in \mathbb{R}^m$ 为资源限制向量。任何包含不等式约束 $\le$ 或自由变量（Unrestricted in Sign, Free Variables）的线性规划，都可以通过引入非负松弛变量（Slack Variables）$s \ge 0$ 或变量拆分 $x = x^+ - x^-$（$x^+, x^- \ge 0$）等价映射为标准型。

```mermaid
flowchart LR
    A[通用线性规划 General LP] -->|引入松弛/剩余变量| B[等式约束 Ax = b]
    A -->|拆分无约束自由变量| C[非负约束 x >= 0]
    B & C --> D[标准型 Standard Form LP]
    D -->|代数与几何等价| E[基本可行解 BFS 对应多面体极点]
```

线性规划标准形式的代数简洁性，不仅为单纯形法的单纯形表（Tableau）更新提供了统一的矩阵运算格式，更为后续对偶理论的对称推导奠定了公理化底座。在实际工程建模中，将现实业务逻辑精确映射到标准形式，是运筹工程师必须具备的首要基本功。

## 2. 非线性目标的线性化技巧：分段凸函数与范数优化

在大量实际运筹场景中，目标函数并非严格线性的常数乘积，而是呈现边际成本递增的凸分段线性结构（Piecewise Linear Convex Functions），或是需要最小化拟合残差的范数。

::: definition 分段线性凸函数
设连续函数 $f: \mathbb{R}^n \to \mathbb{R}$ 由有限个仿射函数的外包络定义，即 $f(x) = \max_{k=1,\dots,K} \{c_k^T x + d_k\}$。由于有限个凸函数的上确界仍为凸函数，故 $f(x)$ 必然为凸函数。
:::

考虑最小化分段线性凸函数问题：

$$\min_{x} \quad \max_{k=1,\dots,K} \{c_k^T x + d_k\} \quad \text{s.t.} \quad A x \ge b$$

我们引入标量辅助变量 $z \in \mathbb{R}$（Epigraph Variable），将原问题精确转化为包含 $K$ 个线性不等式的等价标准 LP：

$$\begin{aligned}
\min_{x, z} \quad & z \\
\text{s.t.} \quad & z \ge c_k^T x + d_k, \quad \forall k = 1, \dots, K \\
& A x \ge b
\end{aligned}$$

::: example 切比雪夫近似与 L1 回归的等价线性规划
在超定方程组 $A x \approx b$ 的鲁棒拟合中，最小化最大绝对残差（Chebyshev / $L_\infty$ 范数）：
$$\min_{x} \|A x - b\|_\infty = \min_{x} \max_{i=1,\dots,m} |a_i^T x - b_i|$$
通过引入标量 $t$，可等价转化为：
$$\min_{x, t} \quad t \quad \text{s.t.} \quad -t \le a_i^T x - b_i \le t, \quad \forall i = 1, \dots, m$$
类似地，最小化残差绝对值之和（$L_1$ 范数 $\min_x \|A x - b\|_1$）可通过为每个样本引入独立的非负残差上界 $u_i \ge 0$，转化为 $\min_{x, u} \sum_{i=1}^m u_i$ 且 $-u_i \le a_i^T x - b_i \le u_i$。
:::

::: pitfall 凹函数的极小化与凸函数的极大化陷阱
很多初学者容易犯一个严重错误：试图将 $\min_x \min_{k} \{c_k^T x + d_k\}$ 也通过类似手法转化为单目标 LP。注意，有限个线性函数的极小值 $g(x) = \min_{k} \{c_k^T x + d_k\}$ 是凹函数（Concave Function）。在凸多面体上极小化凹函数是一个 NP-hard 的非凸优化问题，极值可能出现在边界局部极小点，绝对不能用简单的线性约束转化！只有凸目标的最小化（或凹目标的最大化）才能保持线性规划的凸性。
:::

::: insight 凸性是易解性（Tractability）的真正边界
运筹学界有一句著名的格言：在优化领域，区分容易与困难的界线并不是“线性与非线性”，而是“凸与非凸”（R. T. Rockafellar）。
分段线性函数之所以能无缝降解为 LP，本质是因为其上图（Epigraph）是多个半空间的交集，因而是凸多面体。运筹建模人员的核心洞察力，在于从错综复杂的商业需求中抽离出隐性凸结构，并利用松弛与辅助变量将其投射到高维线性空间中。
:::
