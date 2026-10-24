---
title: '纯自适应搜索与 Hit-and-Run 全局优化 (Pure Adaptive Search in Global Optimization and Hit-and-Run Sampling)'
type: lecture
lecture: 6
tags: [hit-and-run, global-optimization, markov-chain]
status: complete
---

# Lec 6 纯自适应搜索与 Hit-and-Run 全局优化 (Pure Adaptive Search in Global Optimization and Hit-and-Run Sampling)

> MIT 15.099 优化理论文献前沿研讨 · 讲义 6

## TL;DR

- 纯自适应搜索（Pure Adaptive Search, PAS）是全局优化算法的黄金理论基准。
- 证明了 PAS 在凸与非凸目标下的期望迭代步数关于维度 $d$ 呈严格线性 $O(d)$。
- Hit-and-Run 算法提供了在任意紧凸域上实现多项式时间均匀采样的实用马尔可夫链。
## 理想全局优化基准：纯自适应搜索 (PAS)

在评估各种启发式全局优化算法时，研究者长期缺乏一个像信息论中香农极限或排序算法中 $O(n \ln n)$ 那样的“理论最优性能天花板”。
1992 年 Zelda Zabinsky 与 Robert L. Smith 提出了著名的**纯自适应搜索（Pure Adaptive Search, PAS）**理论模型。

PAS 定义了一个理想化的随机算法过程：
设在有界紧致集合 $S \subset \mathbb{R}^d$ 上极小化可测目标函数 $f(x)$。
从初始点 $X_0$ 出发，在第 $k$ 步，PAS 算法从当前**严格改善水平集（Improving Level Set）**中**均匀随机**抽取下一个状态点：
$$
S_k = \left\{ x \in S : f(x) < f(X_{k-1}) \right\}
$$
$$
X_k \sim \text{Uniform}(S_k)
$$
如此递归，直至目标函数值落入全局极小值的 $\epsilon$-邻域内。

```mermaid
flowchart LR
    A["初始紧凸域 S_0, 目标 min f(x)"] --> B["从当前改善区域均匀采样: X_k ~ Uniform(S_k)"]
    B --> C["水平集体积收缩: E[Vol(S_k) / Vol(S_{k-1})] = 1/2"]
    C --> D["线性步数定理: 期望迭代步数 E[N] = O(d ln(1/ε))"]
    D --> E["实现困境: 在通用复杂非凸集合上直接均匀采样属于 NP-hard"]
    E --> F["实用解法: Hit-and-Run 马尔可夫链采样逼近 PAS"]
```

## PAS 线性复杂度定理

直觉上，随着搜索深入，改善区域 $S_k$ 的体积呈几何衰减，在极高维度下其体积在全空间占比会呈指数级缩小（如 $10^{-d}$）。
人们普遍猜测任何算法为了在如此狭小的空间内采样，所需迭代步数必定随维度 $d$ 指数爆炸。
然而 Zabinsky 和 Smith 给出了颠覆直觉的严格证明：

::: theorem [Zabinsky-Smith PAS 线性复杂度定理]
对于任意在有界凸集上满足 Lipschitz 条件的连续凸函数优化，PAS 算法达到相对误差 $\epsilon$ 所需的**期望迭代步数 $N$ 严格随空间维度 $d$ 呈线性增长**：
$$
\mathbb{E}[N] \le c \cdot d \cdot \ln\left( \frac{1}{\epsilon} \right)
$$
其中常数 $c$ 仅取决于多面体的几何偏心率。
:::

证明基于标量随机变量的概率积分变换：由于每次采样均在更小测度的子集内均匀选取，改善集体积的比值序列在对数刻度下服从泊松到达过程（Poisson Process）。无论空间维度多高，每次均匀采样在对数体积期望上都能稳健地将剩余候选空间砍掉一半！

## 实用采样器：Hit-and-Run 马尔可夫链

PAS 虽然拥有极为耀眼的线性收敛步数，但它包含一个致命假设：“如何在形状极其复杂不可知的改善集 $S_k$ 内进行均匀抽样？”
直接拒绝采样在维度 $d > 10$ 时命中率即跌至机器精度以下。
为了物理实现 PAS，Smith 创立了**Hit-and-Run 算法（碰撞运行采样）**：

::: definition [Hit-and-Run 算法几何步骤]
设当前位于改善多面体内的点 $x \in S$：
1. **方向选择**：在 $d$ 维单位球面上均匀随机抽取一个方向向量 $\theta \sim \text{Uniform}(S^{d-1})$；
2. **线段求交**：计算过点 $x$ 沿方向 $\theta$ 的直线与边界 $\partial S$ 的交集，确定一维线段：
$$
\Lambda = \{ \lambda \in \mathbb{R} : x + \lambda \theta \in S \} = [\lambda_{\min}, \lambda_{\max}]
$$
3. **一维移动**：在线段 $[\lambda_{\min}, \lambda_{\max}]$ 上均匀抽取一个标量 $\lambda^* \sim \text{Uniform}(\lambda_{\min}, \lambda_{\max})$；
4. **状态转移**：更新位置 $x' = x + \lambda^* \theta$。
:::

László Lovász 等人后续在随机游走理论中证明了：Hit-and-Run 是一类**快速混合马尔可夫链（Rapidly Mixing Markov Chain）**。
其全变差距离收敛至均匀分布的混合时间（Mixing Time）仅关于维度呈多项式增长 $O^*(d^3)$，从而将 PAS 的纯理论设想变为了可运行的工程现实。

::: insight [高维连续空间的“维度降维打击”]
Hit-and-Run 算法展示了一种处理高维复杂几何体的极高智慧：**将极其复杂的高维空间相交难题，降维投影为极其平凡的一维线段求交与一维均匀采样**。
在高维球坐标变换下，一维沿线的均匀抽样通过方向的各向同性积分，在稳态下严密导出了全空间严格的均匀遍历测度，成为现代运筹学与统计物理计算的一座丰碑。
:::
