---
title: '理想表述 II：全对偶整数性 TDI 与拟阵贪心算法 (Ideal Formulations II: TDI)'
type: lecture
lecture: 6
tags: [total-dual-integrality, tdi, matroids, greedy-algorithm, edmonds-characterization]
status: complete
---

# Lec 6 理想表述 II：全对偶整数性 TDI 与拟阵贪心算法 (Ideal Formulations II: TDI)

> MIT 15.083 / 6.859J 整数规划与组合优化 · 讲义 6 · 授课教师：Prof. Dimitris Bertsimas

## TL;DR

- 全对偶整数性（Total Dual Integrality, TDI）要求任意整数目标下的对偶线性规划必有整数最优解。
- 埃德蒙兹-吉尔斯定理证明：若系统满足 TDI 且右端项为整数，原多面体必为纯整数凸包。
- 拟阵（Matroids）理论确立了局部贪心算法能够绝对命中全局离散最优解的充要代数结构。

## 1. 对偶空间的整数奇迹：全对偶整数性（TDI）

在第 5 讲中，完全单模矩阵（TUM）要求矩阵本身的子行列式全部为 $\pm 1, 0$。这是一个极其严苛的代数条件。现实中很多重要的组合多面体（如一般图最大匹配、树形图二叉树），其约束矩阵**根本不是 TUM**，但其极点依然奇迹般地全是纯整数！

如何超越 TUM 的狭窄框架？
杰克·埃德蒙兹（Jack Edmonds）与罗伯特·吉尔斯（Robert Giles）在 1977 年提出了颠覆性的**全对偶整数性（Total Dual Integrality, TDI）**理论：
**不要只盯住原问题！转向对偶问题的整数性！**

::: definition 全对偶整数性 (Total Dual Integrality, TDI)
考虑线性系统 $A x \le b$（$A, b$ 为有理数）。
若对于**任意使得对偶问题目标有限的整数向量 $c \in \mathbb{Z}^n$**，其对偶线性规划：
$$\min_{y} \quad y^T b \quad \text{s.t.} \quad y^T A = c^T, \quad y \ge 0$$
**都必然存在一个纯整数最优解 $y^* \in \mathbb{Z}^m$**，则称线性不等式系统 $A x \le b$ 是**全对偶整数的（Totally Dual Integral, TDI）**！
:::

```mermaid
flowchart TD
    subgraph TDIMechanism [埃德蒙兹-吉尔斯 TDI 整数闭包]
        Dual[对偶线性规划: min y^T b s.t. y^T A = c, y >= 0] --> Check{对任意整数目标向量 c in Z^n: 对偶最优解 y* 是否必为纯整数?}
        Check -- 是 --> TDI[系统满足全对偶整数性 TDI]
        TDI --> B_int{右端项 b 是否为整数向量?}
        B_int -- 是 --> PrimalInt[定理保证: 原多面体 P = {x | Ax <= b} 的所有极点必然全为纯整数!]
    end
```

::: theorem 埃德蒙兹-吉尔斯定理 (Edmonds-Giles Theorem)
设线性系统 $A x \le b$ 满足全对偶整数性（TDI），且**右端项向量 $b$ 是纯整数向量（$b \in \mathbb{Z}^m$）**。
则多面体 $P = \{x \in \mathbb{R}^n \mid A x \le b\}$ 的**全部极点必为纯整数点**！即 $P = \operatorname{conv}(P \cap \mathbb{Z}^n)$ 是一个完美的理想表述！
:::

这一证明极其震撼：由于强对偶定理，支持超平面在整数斜率 $c$ 下的最优值 $c^T x^* = y^{*T} b$ 是两个整数向量的内积，因此最优值必然是一个整数！根据凸分析极点分离，如果一个多面体在所有整数方向上的投影极值全为整数，它的极点就绝对逃不掉，只能是整数！

## 2. 贪心算法的代数圣杯：拟阵（Matroids）

在计算机科学中，最朴素的算法莫过于**贪心算法（Greedy Algorithm）**：每一步挑选当前看起来最好的边或元素。对于一般问题，贪心算法往往短视崩溃；但在**拟阵（Matroid）**上，贪心算法是百发百中的神枪手！

拟阵由哈斯勒·惠特尼（Hassler Whitney）于 1935 年提出，旨在公理化抽象线性代数中的“线性无关”与图论中的“无环生成树”：

::: definition 拟阵 (Matroid)
拟阵是一个序对 $M = (E, \mathcal{I})$，其中 $E$ 为有限基础集，$\mathcal{I} \subset 2^E$ 为独立子集族（Independent Sets），满足三大公理：
1. **非空性**：$\emptyset \in \mathcal{I}$；
2. **遗传性（Hereditary）**：若 $I \in \mathcal{I}$ 且 $J \subset I$，则 $J \in \mathcal{I}$；
3. **扩张交换公理（Augmentation Property）**：若 $I_1, I_2 \in \mathcal{I}$ 且 $|I_1| < |I_2|$，则**必然存在元素 $e \in I_2 \setminus I_1$**，使得：
$$I_1 \cup \{e\} \in \mathcal{I}$$
:::

拟阵中的极大独立集称为**基（Bases）**，由扩张公理保证：**拟阵的所有基必然拥有严格相等的基数大小（即拟阵的秩 Rank）**！

::: theorem 埃德蒙兹拟阵贪心定理 (Edmonds' Greedy Theorem)
在独立子集系统 $(E, \mathcal{I})$ 上极大众化线性权重 $\sum_{e \in I} w_e$。
对于**任意非负权重向量 $w \ge 0$**，经典贪心算法（从大到小排序依次加入）**绝对保证输出全局最优解，当且仅当系统 $(E, \mathcal{I})$ 是一个拟阵！**
:::

## 3. 拟阵多面体（Matroid Polytope）与双拟阵交（Matroid Intersection）

定义拟阵的秩函数 $r: 2^E \to \mathbb{Z}_+$：$r(S) = \max \{|I| \mid I \in \mathcal{I}, I \subset S\}$。
秩函数满足次模性（Submodularity）：$r(A \cap B) + r(A \cup B) \le r(A) + r(B)$。

埃德蒙兹推导出了**拟阵独立集多胞形**的解析表述：
$$P_M = \left\{ x \in \mathbb{R}^{|E|} \;\middle|\; x(S) = \sum_{e \in S} x_e \le r(S), \; \forall S \subset E, \quad x \ge 0 \right\}$$
由于次模性的神奇刚性，该系统不仅是理想表述，更是**严格满足全对偶整数性（TDI）**！

::: theorem 拟阵交定理 (Matroid Intersection Theorem)
设有两个定义在同一基础集 $E$ 上的拟阵 $M_1 = (E, \mathcal{I}_1)$ 与 $M_2 = (E, \mathcal{I}_2)$。
则其共同独立子集（$\mathcal{I}_1 \cap \mathcal{I}_2$）的凸包，**精确等于两个独立多胞形的交集**：
$$\operatorname{conv}(\mathcal{I}_1 \cap \mathcal{I}_2) = P_{M_1} \cap P_{M_2}$$
并且该相交系统依然是 **TDI 的，必然可以在多项式时间内精确求解！**
:::

有向图最小树形图（Arborescence）、二分图最大匹配、彩色生成树等上百个经典难题，本质上全都是两个拟阵的交集！

::: insight 次模性是离散世界的凸性
全对偶整数性（TDI）与拟阵理论揭示了离散优化深处最迷人的代数对称性：
在连续世界中，凸性是易解性的基石；而在离散世界中，**次模性（Submodularity）就是离散维度的凸性！**
当一个组合系统被拟阵与 TDI 捕获时，局部的贪心选择自发升华为全局的全局最优。数学家通过这种对偶整数性的雕琢，为离散网络拉起了一张可以自由运行连续微积分的平滑天幕。
:::
