---
title: '局部弱收敛方法与随机组合优化 (The Method of Local Weak Convergence in Random Matchings and Spanning Trees)'
type: lecture
lecture: 5
tags: [local-weak-convergence, random-graphs, combinatorial-optimization]
status: complete
---

# Lec 5 局部弱收敛方法与随机组合优化 (The Method of Local Weak Convergence in Random Matchings and Spanning Trees)

> MIT 15.098 应用概率与随机过程前沿研讨 · 讲义 5

## TL;DR

- 局部弱收敛（Local Weak Convergence / Benjamini-Schramm 收敛）刻画稀疏大图的微观根邻域极限。
- 阿尔道斯（Aldous）利用泊松加权无限树（PWIT）给出了全域随机分配问题的严格极限解 $\zeta(2) = \pi^2/6$。
- 随机最小生成树与匹配问题可在无限极限对象上转化为测度收敛的逐点极值马尔可夫决策。
## 稀疏图极限与 Benjamini-Schramm 收敛

在分析大规模网络（如 $n \to \infty$ 的互联网拓扑或社交网络）以及随机组合优化（如随机旅行商问题、最小生成树、加权匹配）时，经典基于全局图拉普拉斯矩阵的极限理论往往无法捕捉局部的异构微观特征。
为了严谨刻画稀疏图序列的极限形态，Itai Benjamini 与 Oded Schramm（以及 David Aldous）提出了**局部弱收敛（Local Weak Convergence / Objective Method）**。

设 $\mathcal{G}_*$ 为所有局部有限连通根图（Rooted Graphs $(G, o)$）在同构意义下的紧化度量空间。
度量定义为：两个根图若在以根节点为中心、半径为 $k$ 的邻域内图结构严格同构，则其距离小于 $2^{-k}$。

```mermaid
flowchart LR
    subgraph Finite["有限大随机图序列 G_n"]
        A["随机选取根节点 o_n ~ Uniform(V_n)"] --> B["提取 r-跳邻域球 B_r(G_n, o_n)"]
    end
    subgraph Convergence["弱收敛极限测度"]
        B -- "n -> ∞ (Benjamini-Schramm)" --> C["极限随机无限根图 (T, o)"]
        C --> D["极限对象: 泊松加权无限树 (PWIT)"]
    end
    subgraph Solving["优化问题求解"]
        D --> E["在无限树上求解递归分布式腔方程"]
        E --> F["直接提取原问题全局平均最优成本极限常数"]
    end
```

::: definition [局部弱收敛]
设 $G_n = (V_n, E_n)$ 为有限图序列。从 $V_n$ 中独立均匀抽取根节点 $o_n$。
若对任意固定半径 $r$ 以及任意给定的有限根图球 $H$，均有：
$$
\lim_{n \to \infty} \mathbb{P}(B_r(G_n, o_n) \cong H) = \mu(B_r(T, o) \cong H)
$$
则称图序列 $G_n$ 局部弱收敛至极限随机根图 $(T, o)$。
:::

这一收敛概念的威力在于：对于许多**局部可分解的组合优化问题**（即最优解在节点 $v$ 处的决策主要由其 $r$-邻域决定的问题），有限图上的平均成本极限可直接转化为在极限无穷根图上的单点期望！

## 阿尔道斯 $\zeta(2)$ 极限分配猜想与证明

在经典的巴黎-梅扎德（Mézard-Parisi）完全二分图随机匹配问题中，设左右各有 $n$ 个节点，每对顶点之间的边权 $w_{ij}$ 为独立同分布的均匀分布 $U(0, 1)$ 或单位指数分布 $\text{Exp}(1)$。
设 $C_n$ 为最小权重完美匹配（Minimum Weight Perfect Matching）的总成本。
统计物理学家通过非严谨的副本方法预测，当 $n \to \infty$ 时：
$$
\lim_{n \to \infty} \mathbb{E}[C_n] = \zeta(2) = \sum_{k=1}^\infty \frac{1}{k^2} = \frac{\pi^2}{6} \approx 1.64493
$$

David Aldous 在 1992-2001 年间通过局部弱收敛方法给出了震惊学界的严格数学证明。
他证明了完全加权二分图在任一顶点局部的局部弱极限正是**泊松加权无限树（Poisson Weighted Infinite Tree, PWIT）**。

::: definition [泊松加权无限树 (PWIT)]
PWIT 是一棵以 $o$ 为根的无限多叉树。每个节点的子节点到达过程由强度为 1 的一维泊松点过程（Poisson Point Process）给出：
子边权重序列 $0 < \xi_1 < \xi_2 < \dots < \xi_k < \dots$ 为泊松点；
每个子节点独立递归生成同分布的后代子树。
:::

## 极限匹配与递归分配方程式

在有限图上的最优分配问题中，每个节点需要选择一条入射边，使得全局权值和最小且互斥。
在极限树 PWIT 上，令 $W$ 为根节点 $o$ 传递给其父节点的“边际出价/保留成本”（Marginal Cost）。
根据贝尔曼最优性原理，根节点在其所有子节点中进行权衡：
$$
W = \min_{i \ge 1} (\xi_i - W_i)^+
$$
其中 $W_i$ 为各子树独立生成的同分布边际保留成本。

通过解该连续随机变量的稳态积分方程（Recursive Distributional Equation, RDE）：
$$
F(t) = \mathbb{P}(W \le t) = \exp\left( -\int_t^\infty (1 - F(s)) \, ds \right)
$$
代入微分方程求解可得严格解析解 $F(t) = \frac{1}{1 + e^{-t}}$，即逻辑斯蒂分布（Logistic Distribution）！
进而积分算得根节点贡献的极限平均匹配权重正好为 $\frac{1}{2} \int_{-\infty}^\infty t f(t) \, dt + \dots = \zeta(2) / n$。

::: insight [局部弱收敛的认识论革命]
局部弱收敛彻底改变了离散概率论的研究范式。
传统方法试图直接在规模为 $n$ 的复杂组合拓扑中硬抗排列组合的几何约束；
而局部弱收敛告诉你：**大图的本质在局部就是一棵树**。由于有限图的环路长度在局部以极高概率趋向无穷（无局部短环），因此可以通过将空间拓扑平滑延拓为测度空间中的无限树，利用树上的动态规划与马尔可夫递归精确求解，最终完美解释了物理学副本对称的内在数学严谨性。
:::
