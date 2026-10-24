---
title: '对偶理论 II：凸规划 Slater 条件与拉格朗日强对偶定理 (Duality Theory II: Strong Duality)'
type: lecture
lecture: 19
tags: [strong-duality, slater-condition, lagrange-duality, hyperplane-separation]
status: complete
---

# Lec 19 对偶理论 II：凸规划 Slater 条件与拉格朗日强对偶定理 (Duality Theory II: Strong Duality)

> MIT 15.084J / 6.252J 非线性规划 · 讲义 19 · 授课教师：Prof. Robert Freund

## TL;DR

- 强对偶性（$d^* = p^*$）抹平了对偶间隙，是凸优化最优解在对偶维度的镜像投射。
- 斯莱特条件（Slater's Condition）通过严格内点假设，排除了边界相切奇异性。
- 分离超平面定理在值函数上图中的应用，给出了强对偶定理的终极公理化证明。

## 1. 强对偶性的几何意义：零对偶间距

在前一讲中我们确立了弱对偶性 $d^* \le p^*$。然而，优化理论最渴望达到的境界是**强对偶性（Strong Duality）**：
$$d^* = p^*$$

当强对偶性成立时，求解原问题与求解对偶问题在数学上完全等价！我们可以将一个包含大量复杂非线性约束的原规划，转化为一个关于乘子的凹无约束（或仅带非负约束）平滑对偶规划，往往能够大幅降低求解复杂度。

那么，究竟在什么条件下，非线性优化的强对偶性能够百分之百严格成立？

```mermaid
flowchart TD
    subgraph ConvexProgram [标准凸规划体系]
        C1[目标函数 f(x) 为凸函数]
        C2[不等式约束 g_i(x) 均为凸函数]
        C3[等式约束 h_j(x) 为仿射线性函数 Ax = b]
    end
    ConvexProgram --> Slater{Slater 条件审查: 存在严格内点 x_bar 使得 g_i(x_bar) < 0 吗?}
    Slater -- 是 --> StrongDuality[强对偶定理成立: d* = p* 且对偶最优解存在!]
    Slater -- 否且边界相切 --> Anomaly[可能出现非零对偶间距或乘子无界退化]
```

## 2. 斯莱特约束规格（Slater's Condition）

对于一般的非凸问题，强对偶性通常不成立。但在凸优化世界中，著名数学家莫顿·斯莱特（Morton L. Slater）于 1950 年提出了优化历史上最简明、也最具威力的约束规格：

::: definition 斯莱特条件 (Slater's Condition)
考虑凸规划：
$$p^* = \min_{x \in C} \quad f(x) \quad \text{s.t.} \quad g_i(x) \le 0, \; i=1,\dots,m, \quad A x = b$$
其中 $C \subset \mathbb{R}^n$ 为凸集，$f, g_i$ 为凸函数。
若存在一个点 $\bar{x} \in \operatorname{relint}(C)$（相对内部），使得：
1. 等式约束严格满足：$A \bar{x} = b$；
2. **所有非线性不等式约束严格小于零**：
$$g_i(\bar{x}) < 0, \quad \forall i = 1, \dots, m$$
则称该凸规划满足**斯莱特条件（Slater's Condition）**。点 $\bar{x}$ 称为该系统的**严格可行内点（Strictly Feasible Point）**。
:::

如果一部分不等式约束本身就是纯仿射线性的（即 $g_k(x) = c_k^T x - d_k$），斯莱特条件甚至允许对这些线性约束取等号，仅要求非线性凸约束严格为负即可（弱化斯莱特条件）。

## 3. 拉格朗日强对偶定理的严格证明

现在，我们利用第 16 讲学到的凸集严格分离定理，给出这一不朽定理的几何证明！

::: theorem 拉格朗日强对偶定理 (Strong Duality Theorem for Convex Programs)
设凸规划满足斯莱特条件，且原问题最优值有限（$p^* > -\infty$）。
则**强对偶性严格成立**：
$$d^* = p^*$$
并且，**对偶问题的最优解 $(\mu^*, \lambda^*)$ 必然存在且有限**！
:::

**宏伟的几何证明概要**：
构造欧氏空间 $\mathbb{R}^{m + l + 1}$ 中的集合 $\mathcal{A}$：
$$\mathcal{A} = \left\{ (u, w, t) \in \mathbb{R}^m \times \mathbb{R}^l \times \mathbb{R} \;\middle|\; \exists x \in C, \; g_i(x) \le u_i, \; A x - b = w, \; f(x) \le t \right\}$$
由于 $f, g_i$ 均为凸函数且约束线性，易证集合 $\mathcal{A}$ 是一个**凸集**！

再构造一个仅含一根垂直射线的集合 $\mathcal{B}$：
$$\mathcal{B} = \left\{ (0, 0, t) \in \mathbb{R}^m \times \mathbb{R}^l \times \mathbb{R} \;\middle|\; t < p^* \right\}$$
由原问题最优值 $p^*$ 的定义，任何原可行点（$u \le 0, w = 0$）的目标值绝不可能严格小于 $p^*$！
因此，凸集 $\mathcal{A}$ 与集合 $\mathcal{B}$ **互不相交**！

根据凸集分离超平面定理，必然存在非零法向量 $(\mu, \lambda, \alpha) \ne 0$ 和标量 $\beta$，将 $\mathcal{A}$ 与 $\mathcal{B}$ 完整分离：
$$\alpha t_A + \mu^T u + \lambda^T w \ge \beta \ge \alpha t_B, \quad \forall (u, w, t_A) \in \mathcal{A}, \; (0, 0, t_B) \in \mathcal{B}$$

分析各分量符号：
1. 易推导出 $\alpha \ge 0$ 且 $\mu \ge 0$；
2. 利用斯莱特内点 $\bar{x}$（$g_i(\bar{x}) < 0$），可以严格证明**垂直乘子 $\alpha$ 绝不可能为零（$\alpha > 0$）**！
将其归一化（令 $\alpha = 1$），分离不等式直接给出：
$$f(x) + \mu^T g(x) + \lambda^T (A x - b) \ge p^*, \quad \forall x \in C$$
对左边关于 $x \in C$ 取下确界，立即得到对偶函数取值：
$$q(\mu, \lambda) \ge p^*$$
结合弱对偶性 $q(\mu, \lambda) \le p^*$，只能是等号成立：$q(\mu, \lambda) = p^*$！
强对偶性 $d^* = p^*$ 与对偶最优解存在性获证！

::: insight 严格内点对奇异切线的免疫
为什么斯莱特条件如此不可或缺？
观察证明的最后一步：如果可行域只是一个与其他曲面发生“相切”的扁平奇点，分离超平面很可能会变成一堵完全垂直的墙（$\alpha = 0$），使得目标函数项被彻底过滤抹杀。
斯莱特条件要求系统必须存在一个丰满的、拥有非零体积的“内部膨胀核心”。这个核心像一颗撑开气球的充气泵，强制将分离超平面推倒成一个倾斜的、具有正向上法向量的支撑切面。这正是凸几何对代数稳定性的最高恩赐。
:::
