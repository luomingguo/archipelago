---
title: '割平面法 II：混合整数舍入割（MIR）与 Split 割平面 (Cutting Planes II: MIR)'
type: lecture
lecture: 18
tags: [mixed-integer-rounding, mir-cuts, split-cuts, disjunctive-programming]
status: complete
---

# Lec 18 割平面法 II：混合整数舍入割（MIR）与 Split 割平面 (Cutting Planes II: MIR)

> MIT 15.083 / 6.859J 整数规划与组合优化 · 讲义 18 · 授课教师：Prof. Dimitris Bertsimas

## TL;DR

- 混合整数舍入割（Mixed Integer Rounding, MIR）将纯整数割推广至连续与整数交织的系统。
- 析取规划（Disjunctive Programming）将离散选择几何化为凸多面体的并集与凸包。
- Split 割平面体系包含了几乎所有工业求解器（Gurobi, CPLEX）的核心通用割平面池。

## 1. 混合变量的挑战：从纯整数到 MIP

在第 17 讲中，Gomory 分数割要求所有变量必须是纯整数。然而，现代工业应用中 $90\%$ 以上的模型是**混合整数规划（MIP）**：
既包含 0-1 离散开机决策 $y \in \{0, 1\}$，又包含连续的物理流量、电量与金额 $x \ge 0$。

当等式约束中同时纠缠着连续实数变量与整数变量时：
$$\sum_{j \in I} a_j y_j + \sum_{k \in C} g_k x_k = b$$
我们再也不能粗暴地对所有系数向下取整，因为连续变量 $x_k$ 可以取任意极小的小数，破坏了整加整为整的代数结构！

为了攻克混合系统，埃贡·巴拉斯（Egon Balas）与杰拉德·科努埃若尔（Gérard Cornuéjols）等大师创立了**混合整数舍入理论（Mixed Integer Rounding, MIR）**与**析取规划（Disjunctive Programming）**。

```mermaid
flowchart TD
    subgraph DisjunctiveSplit [析取切割与 Split 凸包]
        Poly[原始松弛多面体 P] --> Disjunction[空间正交析取: pi^T x <= pi_0 或 pi^T x >= pi_0 + 1]
        Disjunction --> SliceL[左半空间切片: P 交 {pi^T x <= pi_0}]
        Disjunction --> SliceR[右半空间切片: P 交 {pi^T x >= pi_0 + 1}]
        SliceL & SliceR --> ConvexHull[取两者并集的凸包: conv P_L U P_R]
        ConvexHull --> SplitCut[生成支撑割平面: Split Cut / MIR Cut!]
    end
```

## 2. 基础单约束系统：单变量混合整数舍入核心函数

考虑最极简的一维混合不等式原型系统：
$$y + s \ge b, \quad y \in \mathbb{Z}, \quad s \ge 0$$
其中 $y$ 是整数变量，$s$ 是非负连续松弛变量，$b \in \mathbb{R}$ 为任意实数。

记 $b$ 的小数部分为 $f = b - \lfloor b \rfloor \in (0, 1)$。
对整数变量 $y$ 的可能取值进行析取讨论：
1. 若 $y \ge \lfloor b \rfloor + 1$：因为 $s \ge 0$，此时已经满足要求；
2. 若 $y \le \lfloor b \rfloor$：为了满足 $y + s \ge b$，连续变量 $s$ 必须承担起全部的赤字补足工作：
$$s \ge b - y \ge b - \lfloor b \rfloor = f$$

将这两种离散情形合并，科努埃若尔推导出了著名的**基本 MIR 不等式**：

::: theorem 基本混合整数舍入不等式 (Base MIR Inequality)
对于集合 $S = \{(y, s) \in \mathbb{Z} \times \mathbb{R}_+ \mid y + s \ge b\}$，以下线性不等式对所有可行解严格成立：
$$y + \frac{s}{1 - f} \ge \lfloor b \rfloor + 1 \iff y + \frac{s}{1 - (b - \lfloor b \rfloor)} \ge \lceil b \rceil$$
:::

观察这个不等式的威力：连续变量 $s$ 被乘以了一个大于 1 的斜率放大因子 $\frac{1}{1-f}$，使得割平面紧紧贴合离散阶梯的每一个拐角，构成了该一维混合系统的完美理想凸包！

## 3. 析取切割（Disjunctive Cuts）与 Split 割平面系统

埃贡·巴拉斯在 1970 年代奠基的**析取规划（Disjunctive Programming）**，为所有工业割平面提供了统一的几何母体。

对于任意整数变量 $x_j \in \mathbb{Z}$，它在物理上必然满足二分析取：
$$x_j \le \pi_0 \quad \bigvee \quad x_j \ge \pi_0 + 1, \quad (\pi_0 \in \mathbb{Z})$$

多面体 $P$ 被这两个半空间切割为两半：
$$P_0 = P \cap \{x \mid x_j \le \pi_0\}, \qquad P_1 = P \cap \{x \mid x_j \ge \pi_0 + 1\}$$
任何合法的整数解，要么落在 $P_0$ 内部，要么落在 $P_1$ 内部。
因此，真实整数点集必然完全包含在它们的**凸包（Convex Hull）**之中：
$$\operatorname{conv}(P_0 \cup P_1)$$

::: definition Split 割平面 (Split Cuts)
任何能够将松弛多面体 $P$ 中的点切除、但对凸包 $\operatorname{conv}(P_0 \cup P_1)$ 保持全局有效的线性不等式，称为一个 **Split 割平面**。
:::

科努埃若尔等学者证明了组合多面体学最震撼的统一性定理：
**在任意混合整数规划中，以下四类看似来源完全不同的割平面系统，在数学上是百分之百严格等价的：**
1. **所有可能的 Split 割平面集合**；
2. **所有可能的混合整数舍入割（MIR Cuts）集合**；
3. **混合整数 Gomory 割（MIG Cuts）集合**；
4. **两阶段升维投影割平面**！

::: insight 工业求解器的割平面军火库
在现代商业求解器（如 Gurobi）的控制台日志中，我们常常看到如下一行行闪耀的数字：
`Gomory: 42, MIR: 128, Flow Cover: 65, Zero-half: 18, Lift-and-project: 12`。
所有这些名字花哨的割平面，其底层骨架全部统一在 MIR 与 Split 析取凸包的母体之下。
通过在单纯形表的行向量上巧妙线性组合，求解器在毫秒级时间内从千百个投影方向向可行域挥出手术刀。理解了 MIR，就掌握了现代工业求解器最核心的工业机密。
:::
