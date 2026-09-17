---
title: 线性规划：建模、对偶与博弈
type: lecture
lecture: 15
tags: [linear-programming, duality, simplex, game-theory, minimax-theorem]
status: complete
---

# Lec 15 线性规划：建模、对偶与博弈（Linear Programming: Formulations, Duality & Games）

## TL;DR

- **线性规划形式化**：在线性等式或不等式约束集合下优化线性目标函数，给出了将大量离散图算法（最短路、最大流、二分匹配）统一建模为连续优化的通用范式。
- **几何多面体与单纯形法**：线性约束的交集构成凸多胞体（Convex Polyhedron），极值点必然落在多胞体的顶点（Extreme Points）上，单纯形法沿多面体棱线贪心爬升寻优。
- **对偶理论（Duality Theory）**：原问题（Primal）的线性组合诱导出对偶问题（Dual），弱对偶定理提供下界保障，强对偶定理保证原问题最优值与对偶问题最优值严格相等。
- **零和博弈与 Minimax 定理**：通过线性规划对偶性严格推导冯·诺依曼极小化极大定理，证明两人零和博弈中混合策略均衡的存在性与价值确定性。

---

## 线性规划（LP）形式化与标准型

线性规划（Linear Programming, LP）是一类在满足由线性等式与不等式构成的约束条件下，最大化或最小化某个线性目标函数的连续优化方法。

::: definition
**线性规划标准型（Standard Form）**
给定目标函数系数向量 $\mathbf{c} \in \mathbb{R}^n$，约束矩阵 $\mathbf{A} \in \mathbb{R}^{m \times n}$，以及约束边界向量 $\mathbf{b} \in \mathbb{R}^m$：
$$
\begin{aligned}
\text{Maximize } \quad & \mathbf{c}^\top \mathbf{x} = \sum_{j=1}^n c_j x_j \\
\text{Subject to } \quad & \mathbf{A} \mathbf{x} \le \mathbf{b} \\
& \mathbf{x} \ge \mathbf{0}
\end{aligned}
$$
其中决策变量向量为 $\mathbf{x} = (x_1, x_2, \dots, x_n)^\top$。
:::

任意线性规划均可通过标准代数变形转化为标准型：
- 最小化目标转换为最大化相反数：$\min \mathbf{c}^\top \mathbf{x} \iff \max (-\mathbf{c})^\top \mathbf{x}$；
- 无符号限制变量拆分为两个非负变量之差：$x_j = x_j^+ - x_j^-$（$x_j^+, x_j^- \ge 0$）；
- 等式约束拆分为一对反向不等式：$a^\top x = b \iff a^\top x \le b \land -a^\top x \le -b$。

### 建模范例：政治选举竞选广告投放

假设我们参与竞选，需通过在 4 个议题（修路、枪支管控、农业补贴、汽油税）上投放广告来赢得 3 个群体（城市、郊区、农村）的选票：
- 人口基数：城市 100,000 人，郊区 200,000 人，农村 50,000 人；目标是使每个群体的净支持率均超过 50%；
- 设每投放 1000 美元广告在各议题上对各群体支持率的边际增量由矩阵给出；
- 决策变量 $x_1, x_2, x_3, x_4 \ge 0$ 分别代表在 4 个议题上的资金投入，目标函数为最小化总开销 $\sum x_j$。
这一实际决策问题可直接表述为一个标准的线性规划。

---

## 几何视角：凸多面体与极值顶点

考虑包含两个变量的简单二维线性规划：
$$
\begin{aligned}
\text{Maximize } \quad & x_1 + 2x_2 \\
\text{Subject to } \quad & -3x_1 + 2x_2 \le 10 \\
& x_1 + x_2 \le 15 \\
& x_1 \ge 0, \quad x_2 \ge 0
\end{aligned}
$$

![线性规划二维凸多面体可行域与目标函数平移示意图](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20260517153618515.png)

### 凸性与可行域（Feasible Region）

1. **半平面交集**：每个线性不等式 $\mathbf{a}_i^\top \mathbf{x} \le b_i$ 在几何上定义了一个闭半空间（Half-space）。所有约束半空间的交集构成了**可行域（Feasible Region）**；
2. **凸集性质**：半空间是凸集，而任意多个凸集的交集依然是凸集。因此，**线性规划的可行域必然是凸多面体（Convex Polyhedron）**；
3. **三种可行性状态**：
   - **最优可行（Optimal）**：可行域非空且目标函数有上界，存在最优解；
   - **不可行（Infeasible）**：约束条件互相冲突，可行域为空集；
   - **无界（Unbounded）**：可行域向某个方向无限延伸，目标函数可趋向无穷大 $\mathbf{c}^\top \mathbf{x} \to +\infty$。

### 极值定理与单纯形法（Simplex Method）

目标函数 $\mathbf{c}^\top \mathbf{x} = t$ 对应一组平行的超平面。随着数值 $t$ 逐步增大，超平面沿法向量 $\mathbf{c}$ 方向向外平行平移，直到即将脱离可行域的最后一个接触点，该点即为最优解 $\mathbf{x}^*$。

::: theorem
**线性规划基本定理**
若线性规划存在有限最优解，则至少存在一个最优解位于可行域多面体的**顶点（Vertex / Extreme Point）**上。
:::

George Dantzig 于 1947 年提出的**单纯形法（Simplex Algorithm）**，其几何直觉正是：从可行域的某个初始顶点出发，沿着目标函数值递增的棱边（Edge）连续跳转到相邻顶点，直到当前顶点的所有相邻顶点的目标值均不大于自身为止。

---

## 线性规划对偶理论：弱对偶与强对偶定理

对偶理论是线性规划中最深刻的核心理论。它解答了一个根本问题：**如何快速证明给定的某个解确实是全局最优的，而不是仅仅找到了局部极大值？**

### 原问题与对偶问题对应关系

考虑标准型原问题（Primal）：
$$
(P): \quad \max \quad \mathbf{c}^\top \mathbf{x} \quad \text{s.t.} \quad \mathbf{A}\mathbf{x} \le \mathbf{b}, \quad \mathbf{x} \ge \mathbf{0}
$$
我们希望给目标函数 $\mathbf{c}^\top \mathbf{x}$ 寻找一个最小的可能上界。通过对原问题的 $m$ 条约束分别乘以非负乘子 $y_1, y_2, \dots, y_m \ge 0$ 并求和：
$$
\mathbf{y}^\top \mathbf{A} \mathbf{x} \le \mathbf{y}^\top \mathbf{b}
$$
只要我们挑选的乘子满足 $\mathbf{y}^\top \mathbf{A} \ge \mathbf{c}^\top$（即 $\mathbf{A}^\top \mathbf{y} \ge \mathbf{c}$），那么由于 $\mathbf{x} \ge \mathbf{0}$，恒有：
$$
\mathbf{c}^\top \mathbf{x} \le (\mathbf{A}^\top \mathbf{y})^\top \mathbf{x} = \mathbf{y}^\top \mathbf{A} \mathbf{x} \le \mathbf{y}^\top \mathbf{b} = \mathbf{b}^\top \mathbf{y}
$$
为了寻找最紧凑的上界，我们应最小化 $\mathbf{b}^\top \mathbf{y}$，从而引出**对偶问题（Dual）**：
$$
(D): \quad \min \quad \mathbf{b}^\top \mathbf{y} \quad \text{s.t.} \quad \mathbf{A}^\top \mathbf{y} \ge \mathbf{c}, \quad \mathbf{y} \ge \mathbf{0}
$$

### 弱对偶定理（Weak Duality）

::: theorem
**弱对偶定理**
设 $\mathbf{x}$ 为原问题 $(P)$ 的任意可行解，$\mathbf{y}$ 为对偶问题 $(D)$ 的任意可行解，则：
$$
\mathbf{c}^\top \mathbf{x} \le \mathbf{b}^\top \mathbf{y}
$$
:::

### 强对偶定理（Strong Duality）

::: theorem
**强对偶定理（John von Neumann）**
若原问题 $(P)$ 拥有有限最优解 $\mathbf{x}^*$，则对偶问题 $(D)$ 亦必然拥有有限最优解 $\mathbf{y}^*$，且两者的最优目标函数值**严格相等**：
$$
\mathbf{c}^\top \mathbf{x}^* = \mathbf{b}^\top \mathbf{y}^*
$$
对偶间隙（Duality Gap）完全闭合为 0。
:::

最大流最小割定理正是强对偶定理在全幺模矩阵（Totally Unimodular Matrix）上的直接具象。

---

## 博弈论：零和博弈与冯·诺依曼极小化极大定理

博弈论研究多个理性决策主体在相互影响的环境下的策略互动。

### 懦夫博弈（Chicken Game）模型引入

两名司机从相反方向驶向一座单车道单行桥。谁先转向避让，谁就认输；若两人均不避让直行，将发生致命碰撞。

| 收益矩阵 | 玩家 2：避让 | 玩家 2：直行 |
| :--- | :--- | :--- |
| **玩家 1：避让** | $(0, 0)$ | $(-1, 1)$ |
| **玩家 1：直行** | $(1, -1)$ | $(-1000, -1000)$ |

- 基本假设：非合作、同时行动（Simultaneous Move）、单次博弈、完全信息（收益矩阵双方公开）、超级理性（Hyper-rational）；
- 纯策略（Pure Strategy）下不存在对称的纳什均衡；必须引入**混合策略（Mixed Strategy）**，即玩家以特定的概率分布独立随机选择动作。

### 两人零和博弈（Zero-Sum Games）

::: definition
**两人有限零和博弈**
玩家 1（行玩家，Row Player）有 $m$ 种策略，玩家 2（列玩家，Column Player）有 $n$ 种策略。
双方的利益完全对立，可以用一个 $m \times n$ 的收益矩阵 $\mathbf{A} \in \mathbb{R}^{m \times n}$ 表示：当行玩家选策略 $i$ 且列玩家选策略 $j$ 时，行玩家获得收益 $A_{ij}$，列玩家支付代价 $A_{ij}$（收益为 $-A_{ij}$）。
:::

行玩家的目标是最大化收益，列玩家的目标是最小化行玩家的收益。
- 行玩家的混合策略：概率向量 $\mathbf{x} \in \Delta_m = \{ \mathbf{x} \in \mathbb{R}^m \mid \sum x_i = 1, x_i \ge 0 \}$；
- 列玩家的混合策略：概率向量 $\mathbf{y} \in \Delta_n = \{ \mathbf{y} \in \mathbb{R}^n \mid \sum y_j = 1, y_j \ge 0 \}$；
- 双方博弈的期望收益为：
  $$
  \mathbb{E}[\text{Payoff}] = \mathbf{x}^\top \mathbf{A} \mathbf{y} = \sum_{i=1}^m \sum_{j=1}^n x_i A_{ij} y_j
  $$

### 极小化极大定理（Minimax Theorem）

若行玩家先公开自己的混合策略 $\mathbf{x}$，理性的列玩家必然选择使期望收益最小的对策，行玩家可确保的最保守收益为：
$$
\max_{\mathbf{x}} \min_{\mathbf{y}} \mathbf{x}^\top \mathbf{A} \mathbf{y}
$$
反之，若列玩家先公开策略 $\mathbf{y}$，行玩家可获得的最大收益为 $\min_{\mathbf{y}} \max_{\mathbf{x}} \mathbf{x}^\top \mathbf{A} \mathbf{y}$。显然先手暴露策略总是不利的：
$$
\max_{\mathbf{x}} \min_{\mathbf{y}} \mathbf{x}^\top \mathbf{A} \mathbf{y} \le \min_{\mathbf{y}} \max_{\mathbf{x}} \mathbf{x}^\top \mathbf{A} \mathbf{y}
$$

::: theorem
**冯·诺依曼极小化极大定理（von Neumann, 1928）**
在任意有限两人零和博弈中，行动顺序的劣势完全消失，恒有：
$$
\max_{\mathbf{x} \in \Delta_m} \min_{\mathbf{y} \in \Delta_n} \mathbf{x}^\top \mathbf{A} \mathbf{y} = \min_{\mathbf{y} \in \Delta_n} \max_{\mathbf{x} \in \Delta_m} \mathbf{x}^\top \mathbf{A} \mathbf{y} = V^*
$$
该实数 $V^*$ 称为该博弈的**博弈值（Value of the Game）**。
:::

### 基于 LP 对偶性的严谨推导

行玩家寻求最优策略 $\mathbf{x}$，等价于求解：
$$
\begin{aligned}
\text{Maximize } \quad & v \\
\text{Subject to } \quad & \sum_{i=1}^m x_i A_{ij} \ge v \quad (\forall j = 1, \dots, n) \\
& \sum_{i=1}^m x_i = 1 \\
& x_i \ge 0
\end{aligned}
$$
这是一个标准的线性规划！将其写成矩阵形式并根据对偶变换规则推导其对偶问题，得到的正好是列玩家寻求最优防守策略 $\mathbf{y}$ 的线性规划！
由线性规划强对偶定理，原问题最优解与对偶问题最优解必存在且目标值完全相等。因此，**极小化极大定理在数学上完全等价于线性规划强对偶定理**。

---

## 我的理解

::: insight
线性规划与对偶理论是连续数学赋予离散计算机科学的一把万能钥匙：
1. **统一视角的数学降维**：最短路、最大流、最小割、二分图最大匹配、生成树基环系统，表面上是各不相同的组合图论算法，但在代数底层，它们全部是线性规划在全幺模约束矩阵下的特例。掌握了对偶理论，就掌握了整个组合优化的元方法。
2. **对偶证明的极速核验**：要证明一个原问题解的最优性，若仅在原空间枚举往往需要指数时间。但对偶理论告诉我们：只要出示一个对偶可行解且两者数值匹配，最优性便立刻不可辩驳地得以确立。这种“寻找对偶证书”的哲学，正是整个计算复杂性理论中 NP 凭据验证与交互证明系统的基石。
3. **从单向优化到博弈平衡**：强对偶性在零和博弈中的映射展现了数学的深刻统一——最强进攻者的最大化努力，与最严防守者的最小化压制，在理性混合策略的连续概率空间中必然达成一个完美的势能平衡点 $V^*$。计算机科学正是通过线性规划，为社会学与经济学奠定了坚不可摧的数学公理根基。
:::
