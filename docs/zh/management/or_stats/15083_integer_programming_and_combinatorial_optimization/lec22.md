---
title: '近似算法 II：线性松弛舍入法与随机超平面舍入 (Approximation II: LP Rounding)'
type: lecture
lecture: 22
tags: [lp-rounding, randomized-rounding, derandomization, vertex-cover]
status: complete
---

# Lec 22 近似算法 II：线性松弛舍入法与随机超平面舍入 (Approximation II: LP Rounding)

> MIT 15.083 / 6.859J 整数规划与组合优化 · 讲义 22 · 授课教师：Prof. Dimitris Bertsimas

## TL;DR

- 线性规划松弛（LP Relaxation）为复杂组合极值提供了极佳的连续分数基准坐标。
- 确定性舍入（Deterministic Threshold Rounding）为顶点覆盖等问题锁定优雅的 2-近似比。
- 瓦兹拉尼随机舍入（Randomized Rounding）利用概率解释分数解，配合去随机化实现稳健收敛。

## 1. 连续基准的力量：LP 松弛作为近似跳板

在第 21 讲中，我们主要利用纯组合图论与动态规划构造近似算法。然而，现代近似算法最强悍、最通用的主干设计范式，是**线性规划松弛舍入法（LP Rounding Paradigm）**。

其设计哲学分为两步：
1. **连续松弛求基准**：丢弃整数约束，求解连续多面体松弛 LP，得到分数极点解 $x^* \in [0, 1]^n$。
   由于可行域被扩大，松弛最优值 $z_{\text{LP}} = c^T x^*$ 天然构成了真实未知整数极值 $z_{\text{IP}}$ 的绝对保底基准（对于极小化问题：$z_{\text{LP}} \le z_{\text{IP}}$）；
2. **精巧舍入回整数**：通过某种确定的阈值或随机概率机制，将分数解向量 $x^*$ 舍入（Rounding）为一个纯整数可行解 $\hat{x} \in \{0, 1\}^n$，并证明舍入后的成本 $\operatorname{Cost}(\hat{x})$ 绝不超过 $z_{\text{LP}}$ 的 $\alpha$ 倍！

```mermaid
flowchart LR
    DiscreteIP[原 NP-hard 离散规划: min c^T x s.t. x in {0, 1}^n] --> Relax[1. 求解连续松弛 LP: 耗费多项式时间]
    Relax --> FractSol[得到分数极点解 x* in [0, 1]^n]
    FractSol --> Rounding[2. 舍入机制: 阈值截断或随机伯努利采样]
    Rounding --> IntSol[输出合法整数解 x_hat in {0, 1}^n]
    IntSol --> Guarantee[理论证明: Cost(x_hat) <= alpha * Cost(x*) <= alpha * OPT!]
```

## 2. 确定性阈值舍入：加权最小顶点覆盖（Vertex Cover）

考虑经典的 NP-hard **加权最小顶点覆盖问题（Minimum Weight Vertex Cover）**：
给定图 $G = (V, E)$，每个节点有非负权重 $w_v \ge 0$。要挑选一组顶点集合，使得图中的每一条边至少有一个端点被选中：

$$\min_{x} \quad \sum_{v \in V} w_v x_v \quad \text{s.t.} \quad x_u + x_v \ge 1, \quad \forall (u, v) \in E, \quad x_v \in \{0, 1\}$$

设计极简的 **LP 舍入算法**：
1. 求解其连续线性松弛（令 $0 \le x_v \le 1$），得到分数最优解 $x^*$；
2. **确定性阈值截断规则**：
   $$\hat{x}_v = \begin{cases} 1, & \text{若 } x_v^* \ge \frac{1}{2} \\ 0, & \text{若 } x_v^* < \frac{1}{2} \end{cases}$$

分析该算法的合法性与近似比：
- **可行性检验**：对于任意边 $(u, v) \in E$，松弛约束要求 $x_u^* + x_v^* \ge 1$。
  两数之和大于等于 1，**两者之中至少有一个数必须大于等于 $1/2$！**
  因此，$\hat{x}_u$ 与 $\hat{x}_v$ 中至少有一个被舍入为 1！边 $(u, v)$ 必然被合法覆盖！
- **近似比证明**：注意观察舍入乘数：因为 $\hat{x}_v = 1$ 时必有 $x_v^* \ge 1/2$，即 $\hat{x}_v \le 2 x_v^*$。代入总成本：
$$\sum_{v \in V} w_v \hat{x}_v \le \sum_{v \in V} w_v (2 x_v^*) = 2 \sum_{v \in V} w_v x_v^* = 2 \cdot z_{\text{LP}} \le 2 \cdot z_{\text{IP}}$$
仅需三行推导，无懈可击地证明了这是一个**绝对保证不超过 2 倍最优解的 2-近似算法**！

## 3. 拉加万-赫夫曼随机舍入（Randomized Rounding）与去随机化

确定性截断有时难以处理复杂不等式。普拉巴卡尔·拉加万（Prabhakar Raghavan）与克里斯托斯·帕帕迪米特里乌（Christos Papadimitriou）在 1987 年发明了**随机舍入法（Randomized Rounding）**：

**将分数解 $x_j^* \in [0, 1]$，直接解释为独立伯努利随机试验的发生概率！**
独力独立生成离散变量：
$$\hat{X}_j = \begin{cases} 1, & \text{以概率 } x_j^* \\ 0, & \text{以概率 } 1 - x_j^* \end{cases}$$

根据我们在 15.085J 学到的期望线性性：
$$\mathbb{E}[\hat{X}_j] = 1 \cdot x_j^* + 0 \cdot (1 - x_j^*) = x_j^*$$
输出解的数学期望成本为：
$$\mathbb{E}[\operatorname{Cost}(\hat{X})] = \sum c_j \mathbb{E}[\hat{X}_j] = \sum c_j x_j^* = z_{\text{LP}}$$
**随机舍入输出解的数学期望，精确等于最完美的连续松弛下界！**

随后，利用第 15.085J 第 13 讲学到的**切尔诺夫指数界（Chernoff Bound）**，证明所有约束被违反的概率随维度呈指数级衰减，配合条件期望法（Method of Conditional Expectations）实现确定性的去随机化（Derandomization）。

::: insight 连续松弛是指引离散搜索的北极星
LP 舍入法体现了运筹优化最深邃的几何映射哲学：
离散整数解空间像夜空中散落的孤立星辰；直接在离散星辰中盲目跳跃，极易迷失方向；
而连续松弛 LP 搭建了一片平滑通透的力学势场。求解器在多项式时间内迅速滑动到势场的最低极值点，为我们指示了离散星团最密集的核心方位。舍入算法顺水推舟，轻轻一跃，就稳稳降落在高质量整数解的怀抱之中。
:::
