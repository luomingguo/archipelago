---
title: '约束优化最优性条件 I：切锥几何与 Fritz John 必要条件 (Constrained Optimality I)'
type: lecture
lecture: 6
tags: [constrained-optimization, tangent-cone, fritz-john-conditions, polar-cone]
status: complete
---

# Lec 6 约束优化最优性条件 I：切锥几何与 Fritz John 必要条件 (Constrained Optimality I)

> MIT 15.084J / 6.252J 非线性规划 · 讲义 6 · 授课教师：Prof. Robert Freund

## TL;DR

- 可行方向锥与切锥（Tangent Cone）在微分几何层面刻画了可行域边界的无穷小结构。
- 约束优化最优解要求在可行流形上的任意切向量与负梯度方向的内积不得为正。
- 弗里茨·约翰（Fritz John）条件通过引入目标乘子 $\mu_0 \ge 0$ 绕开了约束规格退化。

## 1. 约束优化的几何边界：从开集到流形边界

在第 1 到 5 讲中，我们探索的无约束优化世界是平坦自由的欧氏空间 $\mathbb{R}^n$。在开集中，我们可以沿着任意 $360^\circ$ 的方向迈出无穷小步伐。

然而在现实世界中，一切决策都受制于物理与技术边界：
$$\begin{aligned}
\min_{x \in \mathbb{R}^n} \quad & f(x) \\
\text{s.t.} \quad & g_i(x) \le 0, \quad i = 1, \dots, m \quad &&\text{(不等式约束)} \\
& h_j(x) = 0, \quad j = 1, \dots, l \quad &&\text{(等式约束)}
\end{aligned}$$

当最优解 $x^*$ 落在可行域 $\Omega$ 的边界上时，负梯度方向 $-\nabla f(x^*)$ 往往指向可行域的外部！我们绝不能指望 $\nabla f(x^*) = 0$。
如何在任意非线性曲面约束边界上建立形式化的极值微分法则？这必须从**切锥（Tangent Cone）**几何建立起严格公理。

```mermaid
flowchart TD
    subgraph TangentGeometry [边界切锥与可行流形]
        Feasible[可行域 Omega: g_i(x) <= 0, h_j(x) = 0] --> Boundary[边界点 x* 处的活动约束集 A(x*)]
        Boundary --> Tangent[切锥 T_Omega(x*): 所有逼近序列方向的极限]
        Tangent --> DualCone[极锥 Polar Cone 与法锥 Normal Cone]
    end
    Tangent -->|最优性判据: 负梯度必须落在极锥内!| OptRule[-nabla f(x*) 属于 N_Omega(x*)]
```

## 2. 可行方向锥与切锥（Tangent Cone）

::: definition 可行方向与切锥
设 $\Omega \subset \mathbb{R}^n$ 为闭集合，$x^* \in \Omega$。
1. **可行方向（Feasible Direction）**：非零向量 $d \in \mathbb{R}^n$ 称为可行方向，若存在 $\bar{\alpha} > 0$，使得对任意步长 $\alpha \in [0, \bar{\alpha}]$，均有 $x^* + \alpha d \in \Omega$；
2. **切锥（Tangent Cone / Bouligand Cone）**：向量 $d \in \mathbb{R}^n$ 称为 $\Omega$ 在 $x^*$ 处的切向量，若存在可行域内的点序列 $\{x_k\} \subset \Omega$（$x_k \to x^*, x_k \ne x^*$）以及正实数标量序列 $\tau_k > 0$，使得：
$$d = \lim_{k \to \infty} \tau_k (x_k - x^*)$$
所有切向量构成的集合记为 $T_\Omega(x^*)$。切锥必然是一个闭锥（Closed Cone），但未必是凸的。
:::

::: theorem 一阶几何最优性必要条件
设 $x^*$ 是目标函数 $f$ 在可行域 $\Omega$ 上的局部极小点。则负梯度方向 $-\nabla f(x^*)$ 绝不可能与切锥内部形成锐角，即：
$$\nabla f(x^*)^T d \ge 0, \quad \forall d \in T_\Omega(x^*)$$
几何意义：**在最优解处，沿着任何允许在可行域内行进的切方向，目标函数的方向导数绝不能严格小于 0（否则目标还能继续下降）！**
:::

## 3. 弗里茨·约翰（Fritz John）定理

如何将上述抽象的几何切锥条件转化为可以通过约束函数的梯度 $\nabla g_i$ 与 $\nabla h_j$ 显式计算的代数方程？
数学家弗里茨·约翰（Fritz John）在 1948 年给出了无任何前提假设的普遍定理：

::: definition 活动约束集 (Active Set)
在可行点 $x^*$ 处，记所有等号成立的不等式约束下标集合为**活动约束集（Active Set）**：
$$A(x^*) = \{i \in \{1,\dots,m\} \mid g_i(x^*) = 0\}$$
:::

::: theorem 弗里茨·约翰必要条件 (Fritz John Theorem)
设 $f, g_i, h_j$ 在局部极小点 $x^*$ 处连续可微。
则存在**不全为零**的拉格朗日乘子向量 $\mu_0, \mu_1, \dots, \mu_m \ge 0$ 以及 $\lambda_1, \dots, \lambda_l \in \mathbb{R}$，使得：
1. **一阶驻点平衡方程**：
$$\mu_0 \nabla f(x^*) + \sum_{i=1}^m \mu_i \nabla g_i(x^*) + \sum_{j=1}^l \lambda_j \nabla h_j(x^*) = 0$$
2. **互补松弛性**：
$$\mu_i g_i(x^*) = 0, \quad \forall i = 1, \dots, m$$
3. **非平凡性**：
$$(\mu_0, \mu, \lambda) \ne 0, \quad \mu_0 \ge 0, \; \mu_i \ge 0$$
:::

::: pitfall 目标乘子 mu_0 = 0 的病态退化
注意观察 Fritz John 条件中最玄妙的乘子 $\mu_0$！
若 $\mu_0 > 0$，两边同除以 $\mu_0$，即可完全归一化为标准的 KKT 条件；
然而，如果由于约束曲面在边界处存在尖点、相切或自交，可能导致 $\mu_0 = 0$！
一旦 $\mu_0 = 0$，目标函数的梯度 $\nabla f(x^*)$ 被乘以 0 彻底抹杀！条件退化为仅与约束梯度相关的代数平衡 $\sum \mu_i \nabla g_i + \sum \lambda_j \nabla h_j = 0$。这意味着不论你的目标函数是什么（哪怕是一个完全荒谬的函数），只要约束在这个几何奇异点相切，Fritz John 条件都会机械地成立！
为了彻底斩断 $\mu_0 = 0$ 的退化阴影，优化理论必须引入**约束规格（Constraint Qualifications）**。
:::

::: insight 从几何切空间到代数梯度的桥梁
约束优化是微分几何与代数拓扑在工商业中的投射。
切锥是真实物理世界的流形轮廓，而梯度向量是坐标微积分给出的法向测度。Fritz John 定理以令人惊叹的极简形式，把复杂的空间包络压缩成了几个乘子线性组合为零。它警示我们：现实世界的约束边界可能充满几何奇异（Singularities），唯有深入其切空间微观构造，才能建立真正牢固的最优性定理。
:::
