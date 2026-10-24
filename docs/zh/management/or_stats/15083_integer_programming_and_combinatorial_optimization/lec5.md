---
title: '理想表述 I：完全单模矩阵 TUM 与二分图多面体 (Ideal Formulations I: TUM)'
type: lecture
lecture: 5
tags: [totally-unimodular, tum, bipartite-matching, hoffman-kruskal]
status: complete
---

# Lec 5 理想表述 I：完全单模矩阵 TUM 与二分图多面体 (Ideal Formulations I: TUM)

> MIT 15.083 / 6.859J 整数规划与组合优化 · 讲义 5 · 授课教师：Prof. Dimitris Bertsimas

## TL;DR

- 理想表述（Ideal Formulation）要求连续松弛多面体精确等于整数点凸包 $\operatorname{conv}(S)$。
- 完全单模矩阵（TUM）保证了对于任意整数右端项，线性规划松弛解天生纯整数。
- 二分图匹配多面体、网络流与区间图矩阵展示了组合结构退化为连续优化的理论巅峰。

## 1. 整数规划的至高境界：理想表述（Ideal Formulations）

在离散优化中，算法的最高梦想是：**完全不需要运行任何耗费算力的分支定界搜索，直接把整数规划当作连续线性规划（LP）扔进求解器，解出来的极点解天然、百分之百就是一个纯整数解！**

这可能实现吗？
答案是：完全可能！只要这个模型的表述达到了**理想表述（Ideal Formulation）**：

::: definition 理想表述 (Ideal Formulation)
设离散可行解集合为 $S = \{x \in \mathbb{Z}^n \mid A x \ge b\}$。
若一个连续松弛多面体 $P = \{x \in \mathbb{R}^n \mid \tilde{A} x \ge \tilde{b}\}$ 恰好**严格等于离散点集的凸包（Convex Hull）**：
$$P = \operatorname{conv}(S)$$
则称多面体 $P$ 为离散集合 $S$ 的一个**理想表述**。
:::

根据我们在 15.081J 中学到的表示定理：凸包 $\operatorname{conv}(S)$ 的**每一个几何极点（Extreme Point），其坐标分量必然严格属于集合 $S$（全为纯整数）！**
因此，在理想表述上极小化任意线性目标函数，单纯形法或内点法求得的最优解直接就是整数最优解！

```mermaid
flowchart LR
    Discrete[离散整数可行点集 S in Z^n] --> Hull[取凸包运算: conv S]
    Hull --> Polytope[理想多面体 P = conv S]
    Polytope --> LP[直接运行连续线性规划 LP]
    LP --> IntegerOpt[无需分支定界，直接秒解整数极值!]
```

## 2. 霍夫曼-克鲁斯卡尔定理与完全单模矩阵（TUM）

什么样的代数矩阵能够天然生成理想表述？
艾伦·霍夫曼（Alan Hoffman）与约瑟夫·克鲁斯卡尔（Joseph Kruskal）在 1956 年给出了经典的充要理论：

::: definition 完全单模矩阵 (Totally Unimodular Matrix, TUM)
一个整数矩阵 $A \in \mathbb{Z}^{m \times n}$ 称为完全单模矩阵（TUM），若其**任意阶（$1 \times 1, 2 \times 2, \dots, k \times k$）方子矩阵的行列式取值只能是 $0, +1$ 或 $-1$**：
$$\det(B) \in \{-1, 0, 1\}, \quad \forall \text{ 方子矩阵 } B$$
:::

::: theorem 霍夫曼-克鲁斯卡尔定理 (Hoffman-Kruskal Theorem)
设 $A$ 为整数矩阵。多面体 $P(b) = \{x \ge 0 \mid A x \le b\}$ 对于**所有可能的整数向量 $b \in \mathbb{Z}^m$**，其全部几何极点均为纯整数向量，**当且仅当矩阵 $A$ 是完全单模矩阵（TUM）**！
:::

证明直击克莱姆法则（Cramer's Rule）：任意基本可行解（BFS）的基变量满足 $x_B = B^{-1} b = \frac{\operatorname{adj}(B) b}{\det(B)}$。
当 $A$ 是 TUM 时，基矩阵行列式 $\det(B) = \pm 1$。分母永远是 $\pm 1$，伴随矩阵与 $b$ 全为整数，分子分母相除必然毫无误差地得到纯整数！

## 3. 二分图匹配多面体（Bipartite Matching Polytope）

TUM 最具代表性的几何化身，是图论中的**二分图（Bipartite Graph）**。

设无向图 $G = (V, E)$，其节点集可划分为两个互斥集合 $V = L \cup R$（所有边仅连接 $L$ 与 $R$）。
匹配问题要求挑选一组互不相交的边，最大化边权之和：

$$\begin{aligned}
\max_{x} \quad & \sum_{e \in E} w_e x_e \\
\text{s.t.} \quad & \sum_{e \in \delta(v)} x_e \le 1, \quad \forall v \in V \\
& x_e \in \{0, 1\}
\end{aligned}$$

考察该系统的约束矩阵——无向图的**节点-边关联矩阵（Node-Edge Incidence Matrix）** $M$：
其每一列对应一条边 $e = (u, v)$（其中 $u \in L, v \in R$），该列在行 $u$ 处为 1，在行 $v$ 处为 1，其余全为 0。

::: theorem 二分图关联矩阵 TUM 判定定理 (Poincaré-Ghouila-Houri)
一个无向图 $G$ 是二分图，**当且仅当其节点-边关联矩阵 $M$ 是完全单模矩阵（TUM）**！
:::

**震撼推论**：
二分图最大匹配问题的连续线性松弛多面体：
$$P = \left\{ x \in \mathbb{R}^{|E|} \;\middle|\; \sum_{e \in \delta(v)} x_e \le 1, \; \forall v \in V, \quad x_e \ge 0 \right\}$$
**百分之百精确等于二分匹配的凸包 $\operatorname{conv}(S)$！它是一个纯粹的理想表述！**
因此，二分图匹配问题完全不需要整数规划求解，直接运行连续单纯形法即可秒级出清！

::: pitfall 一般图匹配的奇环非整崩塌
注意：如果图不是二分图，比如包含奇数环（例如 3 个节点的三角形完全图 $K_3$）：
每个节点度数为 2，约束为 $x_{12} + x_{13} \le 1, x_{12} + x_{23} \le 1, x_{13} + x_{23} \le 1$。
此时连续松弛会求出一个恶心至极的非整极点：$x_{12} = x_{23} = x_{13} = 1/2$！目标和为 $1.5$；
然而真实整数最大匹配显然只能选 1 条边（最大值为 1）！
完全单模性在奇环面前彻底崩塌，必须引入下一讲学到的全对偶整数性（TDI）与埃德蒙兹奇割花朵算法！
:::

::: insight 离散与连续的最高境界是无缝融合
理想表述理论向运筹学者展示了数学最高形式的和谐：
离散整数变量的阶梯跳跃，在完全单模的镜面反射下，平滑退化为了多面体的连续极点。
当我们识别出一个问题具备完全单模性时，NP 难度的阴霾瞬间烟消云散，留下的只有多项式时间算法的无限畅通。寻找理想表述，是每一个离散数学家终生追求的圣杯。
:::
