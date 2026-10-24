---
title: '对偶理论 I：拉格朗日对偶函数与弱对偶性 (Duality Theory I: Lagrange Dual)'
type: lecture
lecture: 18
tags: [lagrange-dual, weak-duality, duality-gap, lower-bounding]
status: complete
---

# Lec 18 对偶理论 I：拉格朗日对偶函数与弱对偶性 (Duality Theory I: Lagrange Dual)

> MIT 15.084J / 6.252J 非线性规划 · 讲义 18 · 授课教师：Prof. Robert Freund

## TL;DR

- 拉格朗日对偶函数 $q(\mu, \lambda) = \inf_x L(x, \mu, \lambda)$ 是凹函数，天然提供原问题理论下界。
- 弱对偶定理证明了对偶问题的最大值恒不大于原问题最小值：$d^* \le p^*$。
- 非凸系统中的对偶间距（Duality Gap）度量了非凸可行域凸包松弛后的真实几何损失。

## 1. 原问题与拉格朗日松弛（Lagrangian Relaxation）

在非线性规划中，处理复杂不等式与等式约束最通用、最深刻的理论工具是**拉格朗日对偶理论（Lagrange Duality Theory）**。

考虑通用的非线性规划问题（称为原问题 Primal Problem, $P$）：

$$\begin{aligned}
p^* = \min_{x \in X} \quad & f(x) \\
\text{s.t.} \quad & g_i(x) \le 0, \quad i = 1, \dots, m \\
& h_j(x) = 0, \quad j = 1, \dots, l
\end{aligned}$$

其中集合 $X \subset \mathbb{R}^n$ 可以包含简单的盒状上下界或甚至离散整数约束。
如果我们将复杂的技术约束 $g_i(x) \le 0$ 与 $h_j(x) = 0$ 拿掉，将其以带权惩罚的形式直接搬进目标函数中，就构成了经典的**拉格朗日函数（Lagrangian Function）**：

$$L(x, \mu, \lambda) = f(x) + \sum_{i=1}^m \mu_i g_i(x) + \sum_{j=1}^l \lambda_j h_j(x)$$

其中 $\mu_i \ge 0$ 为不等式乘子，$\lambda_j \in \mathbb{R}$ 为等式乘子。

```mermaid
flowchart TD
    subgraph Primal_Space [原问题空间]
        P[原规划 min f(x) s.t. g(x) <= 0, h(x) = 0]
        X[在复杂约束下艰难寻找可行极小点 p*]
    end
    subgraph Dual_Space [拉格朗日对偶空间]
        L[拉格朗日下确界: q(mu, lambda) = inf_x L(x, mu, lambda)]
        D[对偶规划 max q(mu, lambda) s.t. mu >= 0]
    end
    P --> L
    L --> D
    D -->|弱对偶定理: d* <= p* 恒成立!| X
```

## 2. 拉格朗日对偶函数（The Lagrange Dual Function）

::: definition 拉格朗日对偶函数
定义对偶函数 $q: \mathbb{R}_+^m \times \mathbb{R}^l \to \mathbb{R} \cup \{-\infty\}$ 为拉格朗日函数在集合 $X$ 上的下确界（Infimum）：
$$q(\mu, \lambda) = \inf_{x \in X} L(x, \mu, \lambda) = \inf_{x \in X} \left\{ f(x) + \sum_{i=1}^m \mu_i g_i(x) + \sum_{j=1}^l \lambda_j h_j(x) \right\}$$
:::

注意观察这个函数的结构：
对于固定的 $x$，函数 $L(x, \mu, \lambda)$ 是关于乘子 $(\mu, \lambda)$ 的**纯仿射线性函数**！
而一族仿射函数的逐点下确界（Pointwise Infimum），根据第 2 讲学到的凸凹性公理，**天然永远是一个严格凹函数（Concave Function）**！
这意味着：**不论原始原问题 $f$ 和 $g$ 多么非凸、多么畸形，其拉格朗日对偶函数 $q(\mu, \lambda)$ 永远是一个拥有良好性质的凹函数！**

::: theorem 弱对偶定理 (Weak Duality Theorem)
设 $x$ 是原问题的任意可行解（满足 $x \in X, g(x) \le 0, h(x) = 0$），$(\mu, \lambda)$ 是任意满足 $\mu \ge 0$ 的乘子对。则恒有：
$$q(\mu, \lambda) \le f(x)$$
特别地，对偶问题的最大值 $d^*$ 永远不超过原问题的最小值 $p^*$：
$$d^* = \max_{\mu \ge 0, \lambda} q(\mu, \lambda) \le \min_{x \text{ 可行}} f(x) = p^*$$
:::

证明极其优美：
$$q(\mu, \lambda) = \inf_{z \in X} L(z, \mu, \lambda) \le L(x, \mu, \lambda) = f(x) + \sum_{i=1}^m \mu_i g_i(x) + \sum_{j=1}^l \lambda_j h_j(x)$$
由于 $x$ 可行，$g_i(x) \le 0, h_j(x) = 0$；又因为 $\mu_i \ge 0$，故 $\mu_i g_i(x) \le 0$。
因此 $L(x, \mu, \lambda) \le f(x) + 0 + 0 = f(x)$，弱对偶性得证！

## 3. 对偶间距（Duality Gap）与几何扰动函数

定义原问题最优值与对偶问题最优值之间的差值为**对偶间距（Duality Gap）**：
$$\text{Gap} = p^* - d^* \ge 0$$

- 若 $\text{Gap} = 0$，称**强对偶性（Strong Duality）**成立；
- 若 $\text{Gap} > 0$，说明存在正的对偶间隙。

为了从几何直觉上理解对偶间距，定义原问题的**扰动值函数（Perturbation / Value Function）**：
$$v(u, w) = \min_{x \in X} \{f(x) \mid g_i(x) \le u_i, \; h_j(x) = w_j\}$$
显然 $p^* = v(0, 0)$。
可以严格证明：**对偶问题本质上是在寻找扰动值函数 $v(u, w)$ 在原点 $(0, 0)$ 处的非降支撑超平面！**
- 若值函数 $v(u, w)$ 是下凸的（凸规划成立），则根据支撑超平面定理，原点处存在完美的支撑平面，该切平面的法向量就是最优对偶乘子 $(\mu^*, \lambda^*)$，且强对偶严格成立（$\text{Gap} = 0$）；
- 若原问题是非凸的，值函数 $v(u, w)$ 呈现凹陷褶皱，支撑平面无法贴紧原点切口，遗留下来的悬空高度恰好就是对偶间距！

::: insight 寻找下界作为优化认知的终极武器
在计算机科学与运筹学中，证明一个解存在往往比证明它“最优”容易得多。
通过代入一个可行解，我们只拿到了真实价值的一个上界（Upper Bound）；而拉格朗日对偶函数为我们提供了人类探寻理论绝对下界（Lower Bound）的火眼金睛。
即使面对无法精确求解的非凸 NP-hard 工业大题，对偶问题作为凹规划可以在多项式时间内轻松求出极大值。手握对偶下界，决策者就能在黑暗中精确丈量出当前启发式算法距离物理极限的绝对距离。
:::
