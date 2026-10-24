---
title: '整数规划建模艺术：离散决策、集合覆盖与设施选址 (Formulations & Modeling)'
type: lecture
lecture: 1
tags: [integer-programming, formulations, set-covering, facility-location]
status: complete
---

# Lec 1 整数规划建模艺术：离散决策、集合覆盖与设施选址 (Formulations & Modeling)

> MIT 15.083 / 6.859J 整数规划与组合优化 · 讲义 1 · 授课教师：Prof. Dimitris Bertsimas

## TL;DR

- 0-1 离散变量赋予了运筹学表达非连续逻辑跳跃与组合状态的完整代数能力。
- 集合覆盖（Set Covering）、集合划分与旅行商问题展示了经典组合优化的几何表述。
- 紧致表述与松弛强度决定了底层求解器的搜索树规模，模型表述优于算法百倍。

## 1. 离散优化的现实动机与数学表述

在连续线性规划与非线性规划中，决策变量在多维实数欧氏空间 $\mathbb{R}^n$ 中连续流动。然而，人类社会最重大的战略决策，绝大多数具有不可分割的离散离散特性：
- 航空航天：一架波音 787 客机要么执飞波士顿到苏黎世的航线，要么停场，不能执飞 0.73 次；
- 供应链网络：一座投资数十亿的晶圆制造厂要么在德州破土动工，要么放弃，不能建立 0.5 座；
- 电信网络：数据包在路由器之间的路由交换要么走光缆链路 A，要么走链路 B。

**整数线性规划（Integer Linear Programming, ILP）**的形式化定义为：

$$\begin{aligned}
z_{\text{IP}} = \min_{x} \quad & c^T x \\
\text{s.t.} \quad & A x \ge b \\
& x \in \mathbb{Z}^n \quad (\text{或 } x \in \{0, 1\}^n)
\end{aligned}$$

若部分变量为整数、部分变量为连续实数，则称为**混合整数规划（Mixed-Integer Programming, MIP）**。

```mermaid
flowchart LR
    A[现实业务离散决策] --> B[0-1 指示变量 y in {0, 1}]
    B --> C[逻辑蕴含与固定费用转化]
    C --> D[连续松弛 LP Relaxation: 0 <= y <= 1]
    D --> E[分支割平面求解器出清]
```

看似只是简单地在末尾加上了一条“$x \in \mathbb{Z}^n$”的约束，整个问题的数学本质与计算复杂度发生了天翻地覆的质变：线性规划的多项式易解性瞬间坍塌，问题跃迁为理论计算机科学中的 **NP-hard 难题**！

## 2. 经典组合优化原语（Combinatorial Primitives）

运筹学界数十年的沉淀提炼出了若干统治级的经典组合优化模型原型：

### 2.1 集合覆盖与集合划分（Set Covering & Partitioning）
设全集为 $U = \{1, \dots, m\}$，候选子集族为 $S_1, \dots, S_n \subset U$，每个子集拥有选取成本 $c_j$。
要从这 $n$ 个子集中挑选一组子集，使得全集中的每一个元素都至少被覆盖一次（或恰好覆盖一次）：
$$\min_{x \in \{0, 1\}^n} \quad \sum_{j=1}^n c_j x_j \quad \text{s.t.} \quad \sum_{j: i \in S_j} x_j \ge 1, \quad \forall i \in U$$
这是全球所有大型航空公司机组排班（Crew Pairing）的通用数学母体。

### 2.2 无容量限制设施选址（UFL, Uncapacitated Facility Location）
有 $m$ 个潜在建厂选址，建立工厂 $i$ 的固定投资成本为 $f_i$；有 $n$ 个客户，工厂 $i$ 向客户 $j$ 供货的单位运输成本为 $c_{ij}$。
引入 0-1 建厂变量 $y_i \in \{0, 1\}$ 和供货决策变量 $x_{ij} \in [0, 1]$：
$$\min_{x, y} \quad \sum_{i=1}^m f_i y_i + \sum_{i=1}^m \sum_{j=1}^n c_{ij} x_{ij} \quad \text{s.t.} \quad \sum_{i=1}^m x_{ij} = 1, \quad x_{ij} \le y_i, \quad y_i \in \{0, 1\}$$

## 3. 表述强度（Formulation Strength）是第一生产力

在整数规划中，同一个物理问题可以写出成百上千种完全等价的数学模型。
设离散可行解集合为 $S = \{x \in \mathbb{Z}^n \mid A x \ge b\}$。
包含 $S$ 的不同连续线性松弛多面体 $P_1, P_2$ 满足：
$$S \subset P_2 \subset P_1$$
我们称表述 $P_2$ **严格强于（Stronger than）**表述 $P_1$！

::: definition 强表述与弱表述
在极小化问题中，松弛多面体越小，$P_2$ 算出的连续松弛下界 $z_{\text{LP}}(P_2)$ 必然严格高于 $z_{\text{LP}}(P_1)$，更加逼近真实的整数最优值 $z_{\text{IP}}$：
$$z_{\text{LP}}(P_1) \le z_{\text{LP}}(P_2) \le z_{\text{IP}}$$
下界越高，分支定界树（Branch and Bound Tree）在早期被剪枝的节点就呈指数级爆发！
:::

::: insight 建模质量决定算力生死
Dimitris Bertsimas 教授在 15.083 第一课中反复强调一句名言：“永远不要指望靠升级服务器 CPU 来拯救一个糟糕的模型”。
一个包含劣质大 M 的松弛多面体，其连续下界虚脱漂移，即使动用全球顶级超算也会在庞大的组合树形迷宫中陷入百年停滞；
而一个深刻理解了凸包几何、引入了紧致分歧割平面的强表述，在普通个人电脑上几毫秒内即可秒杀收敛。整数规划的胜负，在建模者敲下最后一行代码时，就已经注定了结局。
:::
