---
title: '增强表述方法 II：扩展表述与 Benders 投影 (Extended Formulations & Projection)'
type: lecture
lecture: 4
tags: [extended-formulations, projection, farkas-projection, compact-representations]
status: complete
---

# Lec 4 增强表述方法 II：扩展表述与 Benders 投影 (Extended Formulations & Projection)

> MIT 15.083 / 6.859J 整数规划与组合优化 · 讲义 4 · 授课教师：Prof. Dimitris Bertsimas

## TL;DR

- 扩展表述（Extended Formulations）通过引入辅助变量实现约束指数级降维。
- 雅纳卡基斯定理（Yannakakis）确立了多胞形线性扩展复杂度的理论下界。
- 傅里叶-莫茨金消元与法卡斯投影建立了高维扩展空间向低维物理空间的映射通道。

## 1. 升维的奇迹：扩展表述（Extended Formulations）

在第 1 讲与第 3 讲中，我们总是在原始决策变量空间 $\mathbb{R}^n$ 中努力添加有效不等式。然而，组合数学中最令人绝望的事实是：**许多极其基础的经典离散多面体，如果只在原始变量空间中描述，其刻画面（Facets）数量随维度呈指数级（$2^n$ 或 $n!$）天文爆炸！**
例如第 15.081J 第 19 讲中见过的旅行商 TSP 子回路多面体、偶置换多面体。

1988 年，理论计算机大师米哈里斯·雅纳卡基斯（Mihalis Yannakakis）系统揭示了一项震撼应用数学的秘密：
**如果我们敢于向更高维度的空间引入少量的辅助变量（Auxiliary Variables），原本需要指数级条约束才能围成的复杂低维多面体，在高维空间中可以被惊人地压缩为一个仅含多项式阶约束的紧凑多面体！**

::: definition 扩展表述与多胞形投影
设多面体 $P \subset \mathbb{R}^n$。若存在高维空间 $\mathbb{R}^{n+p}$ 中的多面体 $Q = \{(x, y) \in \mathbb{R}^n \times \mathbb{R}^p \mid A x + B y \ge b\}$，使得 $P$ 恰好是 $Q$ 在前 $n$ 维坐标空间上的**正交正规投影（Orthogonal Projection）**：
$$P = \pi_x(Q) = \{x \in \mathbb{R}^n \mid \exists y \in \mathbb{R}^p \text{ 使得 } (x, y) \in Q\}$$
则称多面体 $Q$ 是 $P$ 的一个**扩展表述（Extended Formulation）**。$Q$ 的约束行数称为该表述的尺寸（Size）。
:::

```mermaid
flowchart TD
    subgraph DimensionLifting [高维紧凑表述向低维复杂多面体的投影]
        HighDim[高维扩展多面体 Q in R^n+p: 仅含 O(n^2) 条紧凑线性约束]
        Projector[正交坐标投影算子 pi_x: 消除辅助变量 y]
        LowDim[原始物理空间多面体 P in R^n: 暴露出 2^n 条天文数字级刻画面!]
    end
    HighDim --> Projector
    Projector --> LowDim
```

## 2. 经典范例：生成树与跨越连通图

考虑在连通图 $G = (V, E)$ 上寻找最小支撑树（Spanning Tree）的可行多面体。
在原始边变量空间 $x_e \in [0, 1]$（$|E| = m$）中，埃德蒙兹（Jack Edmonds）证明：为了保证连通且无环，必须包含所有子集的连通约束：
$$\sum_{e \in E(S)} x_e \le |S| - 1, \quad \forall S \subset V$$
约束数量高达 $2^{|V|}$ 条！

现在，引入高维辅助变量——**虚拟商品网络流（Multi-commodity Network Flows）**：
选定节点 1 为根节点。假设根节点需要向其余每个节点 $k \in V \setminus \{1\}$ 分别运送 1 单位的专属商品。
设 $f_{ij}^k \ge 0$ 为弧 $(i, j)$ 上运送给节点 $k$ 的商品流量。
构建**高维扩展规划系统**：
1. 每一类商品的网络流守恒约束（节点平衡）；
2. 边容量耦合约束：$f_{ij}^k + f_{ji}^k \le x_e$（若边 $e=(i, j)$ 未被选中，则绝对禁止走流！）；
3. 总边数约束：$\sum_{e \in E} x_e = |V| - 1$。

仔细端详这个扩展系统：
- 辅助变量数量为 $\mathcal{O}(|V| \cdot |E|)$；
- **总约束数量仅有 $\mathcal{O}(|V|^2)$ 条**！原本 $2^{|V|}$ 的指数级约束网络，在高维网络流投影下被**彻底降维打击为多项式阶平方量级**！

## 3. 投影与法卡斯引理消除（Farkas Elimination）

我们如何从数学上精确证明一个高维扩展表述 $Q = \{(x, y) \mid A x + B y \ge b\}$ 投影下来究竟对应哪些低维约束？
这必须搬出第 15.081J 第 10 讲学到的**法卡斯引理（Farkas' Lemma）与对偶极射线**：

点 $x \in \pi_x(Q)$，当且仅当下述关于 $y$ 的线性系统**存在可行解**：
$$B y \ge b - A x$$

由法卡斯引理，该系统有解当且仅当对于其对偶锥中的所有**极方向（Extreme Rays）** $u \in \operatorname{extray}\{u \ge 0 \mid u^T B = 0\}$，均满足：
$$u^T (b - A x) \le 0 \iff (u^T A) x \ge u^T b$$

这揭示了一个惊人的对称哲学：
**低维空间中那 $2^n$ 条让人绝望的刻画面，其法向量 $(u^T A)$ 恰恰对应了高维子系统矩阵 $B$ 的对偶多面锥的所有极方向！**

::: theorem 雅纳卡基斯非负矩阵秩定理 (Yannakakis' Theorem, 1991)
一个多胞形 $P$ 能够被尺寸为 $r$ 的线性扩展表述紧凑表达，**当且仅当其松弛矩阵（Slack Matrix $S_{ij} = b_i - a_i^T v_j$）的非负秩（Nonnegative Rank）满足 $\operatorname{rank}_+(S) \le r$**！
:::

在 2012 年，Fiorini 等学者利用该定理震惊世界地证明了：**对于著名的旅行商 TSP 多面体与割多面体，绝对不存在任何多项式规模的对称线性扩展表述！**（其非负秩必为 $2^{\Omega(n)}$）。这从几何深处为多面体方法划定了不可逾越的物理极限。

::: insight 维度升华的无上玄妙
扩展表述是凸多面体几何最优雅的诗篇。
在低维欧氏空间中，我们被无数条交叉重叠的几何切面遮蔽了双眼，举步维艰；
而只要我们敢于升起辅助变量的维度，复杂的几何多胞形瞬间舒展开来，化作一组优雅通透的高维仿射流动。
即使理论证明了 TSP 无法被无限降维，但扩展表述为绝大多数工业规划（设施选址、多品种流、生产批量规划 Lot-Sizing）提供了化繁为简的多项式捷径。
:::
