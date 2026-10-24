---
title: '随机 K-SAT 相变与二阶矩方法 (Random K-SAT Phase Transitions and the Second Moment Method)'
type: lecture
lecture: 1
tags: [phase-transitions, random-graphs, statistical-physics]
status: complete
---

# Lec 1 随机 K-SAT 相变与二阶矩方法 (Random K-SAT Phase Transitions and the Second Moment Method)

> MIT 15.098 应用概率与随机过程前沿研讨 · 讲义 1

## TL;DR

- 随机 K-SAT 问题展现出急剧的满足性相变现象，相变阈值比 $\alpha = m/n$ 决定了公式几乎必然可满足或不可满足。
- 一阶矩方法通过马尔可夫不等式给出了满足性阈值的高概率不可满足上界 $\alpha \le 2^k \ln 2$。
- 二阶矩方法结合切比雪夫不等式与解空间聚类对称性，克服重叠方差发散以证明下界。
## 组合相变与布尔满足性问题

在理论计算机科学与统计物理交叉领域中，**布尔可满足性问题（Boolean Satisfiability, SAT）**处于计算复杂性理论的核心位置。
根据 Cook-Levin 定理，3-SAT 是首个被证明的 NP-完全问题。然而，在最坏情况复杂度之外，计算机科学家与统计物理学家更关注**典型实例（Average-Case）**的求解难度与结构演化。

设 $n$ 为布尔变量 $x_1, \dots, x_n \in \{0, 1\}$ 的总数。一个随机 $k$-SAT 实例由 $m$ 个独立随机抽取的子句（Clause）以逻辑与（AND）连接而成，记为合取范式（CNF）公式：
$$
\Phi = C_1 \land C_2 \land \dots \land C_m
$$
其中每个子句 $C_j$ 包含 $k$ 个从 $2n$ 个可能文字（Literal, 即 $x_i$ 或 $\neg x_i$）中无放回均匀随机抽取的文字，并以逻辑或（OR）相连。我们定义子句-变量比（Clause-to-Variable Ratio）为：
$$
\alpha = \frac{m}{n}
$$
当 $n \to \infty$ 且保持 $\alpha$ 固定时，公式 $\Phi$ 可满足的概率 $\mathbb{P}(\Phi \text{ is SAT})$ 表现出极其剧烈的尖锐相变（Sharp Phase Transition）。

```mermaid
flowchart LR
    A["稀疏区域: α < α_c"] --> B["满足态 (SAT Phase): 解空间巨大且连通, 多项式局部搜索易求得"]
    B --> C["临界区域: α ≈ α_c"]
    C --> D["相变阈值点: 解空间发生对称性破缺与碎片化 (Clustering)"]
    D --> E["过约束区域: α > α_c"]
    E --> F["不可满足态 (UNSAT Phase): 几乎必然存在矛盾链条, 复杂度呈指数级爆炸"]
```

在统计物理学中，这一现象对应于自旋玻璃（Spin Glass）模型的冻结与副本对称破缺（Replica Symmetry Breaking）。而在应用概率中，核心课题则是利用概率极限定理与矩方法给出临界阈值 $\alpha_c(k)$ 的严格渐近界。

## 一阶矩方法与不可满足上界

一阶矩方法（First Moment Method）是概率图论中最经典的上界推导工具。其数学基础是马尔可夫不等式（Markov Inequality）。

设 $Z = \sum_{\sigma \in \{0, 1\}^n} \mathbb{I}_{\{\sigma \models \Phi\}}$ 为满足公式 $\Phi$ 的合法真值赋值（Valid Assignments）的总数。
对于任意一个固定的真值赋值 $\sigma$，由于 $C_j$ 中每个文字被违背的概率独立为 $1/2$，因此该子句未被满足的概率为 $(1/2)^k$。
子句被满足的概率即为 $1 - 2^{-k}$。由于 $m$ 个子句独立抽取：
$$
\mathbb{P}(\sigma \models \Phi) = \left(1 - 2^{-k}\right)^m
$$
由期望的线性性质，合法真值赋值总数的数学期望为：
$$
\mathbb{E}[Z] = \sum_{\sigma} \mathbb{P}(\sigma \models \Phi) = 2^n \left(1 - 2^{-k}\right)^m = \left(2 \left(1 - 2^{-k}\right)^\alpha\right)^n
$$

::: theorem [随机 K-SAT 一阶矩不可满足上界]
当子句密度 $\alpha > \frac{\ln 2}{-\ln(1 - 2^{-k})}$ 时：
$$
\lim_{n \to \infty} \mathbb{P}(\Phi \text{ is SAT}) = 0
$$
利用泰勒展开 $-\ln(1 - 2^{-k}) \approx 2^{-k}$，可得渐近上界：
$$
\alpha_c(k) \le 2^k \ln 2
$$
:::

证明极为简洁：由马尔可夫不等式，$\mathbb{P}(Z > 0) = \mathbb{P}(Z \ge 1) \le \mathbb{E}[Z]$。当 $2(1 - 2^{-k})^\alpha < 1$ 时，$\mathbb{E}[Z]$ 随 $n$ 呈指数衰减收敛于 0。

## 二阶矩方法与方差控制

为了证明当 $\alpha$ 较小时公式几乎必然可满足，必须证明 $\mathbb{P}(Z > 0) \to 1$。
单纯利用一阶矩无法做到这一点，因为 $\mathbb{E}[Z] \to \infty$ 并不意味着 $Z > 0$ 几乎必然发生（可能极少数小概率样本中 $Z$ 巨大，而绝大多数样本中 $Z = 0$）。
为此必须引入**二阶矩方法（Second Moment Method）**，其本质源于柯西-施瓦茨不等式或帕利-辛格不等式（Paley-Zygmund Inequality）：
$$
\mathbb{P}(Z > 0) \ge \frac{(\mathbb{E}[Z])^2}{\mathbb{E}[Z^2]}
$$
因此，只要能证明在某个密度区域内存在常数 $C < \infty$ 使得 $\mathbb{E}[Z^2] \le C (\mathbb{E}[Z])^2$，即可直接推导出满足概率有正下界，再结合自同构对称性与尖锐阈值定理（Friedgut Theorem）即可将概率提升至 1。

::: definition [重叠度与成对赋值满足概率]
设 $\sigma, \tau \in \{0, 1\}^n$ 为两个赋值，其重叠度（Overlap）定义为相同比特位的比例：
$$
s(\sigma, \tau) = \frac{1}{n} \sum_{i=1}^n \mathbb{I}_{\{\sigma_i = \tau_i\}} \in [0, 1]
$$
二阶矩可展开为对所有可能重叠度的积分：
$$
\mathbb{E}[Z^2] = \sum_{\sigma, \tau} \mathbb{P}(\sigma \models \Phi \land \tau \models \Phi) = 2^n \sum_{d=0}^n \binom{n}{d} P(s)^m
$$
其中 $s = d/n$ 为重叠比例，$P(s)$ 为单个子句同时被 $\sigma$ 和 $\tau$ 满足的联合概率。
:::

经组合计数推导，两个重叠度为 $s$ 的赋值同时违背一个随机子句的概率为 $2^{-k} + 2^{-k} - (1 - s)^k 2^{-k}$（即两者各自违背但共享变量赋值一致的交集）。因此联合满足概率为：
$$
P(s) = 1 - 2 \cdot 2^{-k} + 2^{-k} s^k
$$
分析目标转化为研究函数 $g(s) = \frac{1}{n} \ln \left( \binom{n}{sn} P(s)^m \right)$ 在 $s \in [0, 1]$ 上的鞍点与极值。

::: pitfall [标准二阶矩在均匀解空间中的灾难性发散]
对于朴素的变量集，$g(s)$ 在 $s = 1/2$（完全正交无关）处取得局部极大值，但在接近 $s = 1$ 时，由于解之间的局部微扰聚集效应，$g(s)$ 往往会在端点处爆发式上翘，导致 $\mathbb{E}[Z^2] / (\mathbb{E}[Z])^2 \sim e^{\Omega(n)} \to \infty$。
这种发散并不是因为公式不可满足，而是因为“解并不均匀分布于超立方体中”，而是聚类成互不连通的离散簇（Clusters）。因此直接对所有解应用二阶矩会在临界点之前很早就彻底失效。
:::

::: insight [加权修剪与非重叠子集二阶矩]
现代应用概率（如 Achlioptas, Peres, Moore 等人）通过对解施加**加权过滤（Weighted Second Moment Method）**，强制剔除包含过量临界重叠变量的解，或者仅对无孤立自由度的“刚性解”（Rigid Solutions）计算二阶矩。
这一数学技术成功将可证明的 SAT 下界推进至 $\alpha \ge 2^k \ln 2 - \frac{k}{2} \ln 2 - O(1)$，与一阶矩上界在渐近主项上精确对齐！
:::
