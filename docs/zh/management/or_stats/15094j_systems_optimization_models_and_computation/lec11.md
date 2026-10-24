---
title: '大型货运网络加载与双挂车匹配优化 (Network Loading and Pup Matching)'
type: lecture
lecture: 11
tags: [network-design, freight-logistics, pup-matching, combinatorial-optimization]
status: complete
---

# Lec 11 大型货运网络加载与双挂车匹配优化 (Network Loading and Pup Matching)

> MIT 15.094J 鲁棒系统优化建模与计算 (Systems Optimization: Models and Computation) · 授课教师：Prof. Dimitris Bertsimas / Robert Freund

## TL;DR

- 公路货运网络加载（Network Loading）将连续货物吨位离散映射为整车卡车（Trailers）调度。
- 双挂短车匹配（Pup Matching）通过将两辆短挂车组合为单一长挂车节省干线牵引车头成本。
- 大规模网络设计中的阶梯固定费用与动态中转集并展示了极具挑战的整数网络流结构。

## 北美干线公路货运的工业现实

在零担公路货运（Less-Than-Truckload, LTL，如 FedEx Freight、Old Dominion、UPS）与大型电商物流网络中，每天有数十万吨货物在横跨大陆的公路网中流动。

在实际公路货运运营中，存在一个极其独特的物理装备特征——**双挂短车联运（Pup Trailers & Pup Matching）**：
- 标准的全尺寸长挂车（Standard Van）长度为 53 英尺；
- 而零担物流公司大量采购长度仅为 28 英尺的小型短挂车（称为 **Pup Trailer**）；
- **核心运营灵活性**：在市内狭窄街道取派件时，单台牵引车头拉动 1 个 Pup，机动灵活；而进入城际高速公路干线时，**允许用一台重型牵引车头，通过中间连接架（Dolly Converter），同时拖挂两辆 Pup 短车（构成所谓的 Tandem / Double Pup）！**

在干线上，拖挂两辆 Pup 所消耗的柴油与司机工资，仅仅比拖挂单辆 Pup 增加不到 15%，却**将单次干线运输运力硬生生翻了一倍**！
如何在大规模货运网络中决定各条弧上的挂车加载数量，并让流向相同方向的 Pup 短车在沿途枢纽完美两两“配对合体（Pup Matching）”，构成了极其复杂的运筹大题。

## 网络加载问题 (The Network Loading Problem)

设货运网络为有向图 $G = (V, E)$。
多种不同起讫点（OD 对）的货物需求在网络中流动。商品 $k$ 在弧 $e$ 上的流量为连续变量 $f_e^k \ge 0$。
穿过弧 $e$ 的总物理货物吨位为：
$$
F_e = \sum_{k} f_e^k
$$
然而，公路干线上不能直接“运送散装吨位”，必须通过离散的整车容器（Containers / Trailers）进行封装！
设单辆标准卡车或挂车的最大载重容量为 $C$。
必须为弧 $e$ 采购或指派的**整数整车车次**为离散变量 $y_e \in \mathbb{Z}_{\ge 0}$：
$$
F_e \le C \cdot y_e \iff \sum_k f_e^k \le C \cdot y_e
$$
每开行一趟卡车，需支付高昂的司机工资、高速公路通行费与燃油固定费用 $K_e$。

```mermaid
flowchart LR
    A["起源地分拨中心 A"] -->|"发货: 单个短挂车 Pup 1"| H["干线中转集散枢纽 H"]
    B["起源地分拨中心 B"] -->|"发货: 单个短挂车 Pup 2"| H
    H -->|"算法配对成功! 合体为双挂车 (Double Pup)"| D["由单一重型车头牵引, 节省 45% 运力成本!"]
    D -->|"长途城际干线高速行驶"| M["目的地拆卸枢纽 M"]
    M -->|"拆分为两辆单挂车"| C1["终端配送点 1"]
    M -->|"解绑各自送达"| C2["终端配送点 2"]
```

## 双挂车匹配优化的数学模型 (Pup Matching Formulation)

设在某个干线中转枢纽节点 $h$：
当天有 $N_{\text{arr}}$ 辆单挂短车 Pup 进港到达，同时各本地货运站生成了一批新 Pup。这些挂车拥有各自不同的最终目的地。
我们需要决定：**哪两辆 Pup 应该在枢纽 $h$ 被配对锁定为一个双挂车组，一起沿着某条共同的下游干线路径前进？**

定义匹配决策：
设集合 $\mathcal{P}$ 为待流转的 Pup 短车集合。
若两辆短车 $p_1, p_2 \in \mathcal{P}$ 的下游路由存在一段共同的重叠干线区间（从节点 $u$ 到节点 $v$），则它们构成了**潜在可匹配对 $(p_1, p_2) \in \mathcal{M}$**。
- 若单独开行两辆单车：干线成本为 $2 \times \text{Cost}(u, v)$；
- 若将其配对为双挂车：总成本仅为 $(1 + \delta) \times \text{Cost}(u, v)$（$\delta \approx 0.15$ 为附加燃料阻力系数）；
- **净套利节约金额**为：
$$
S(p_1, p_2) = (1 - \delta) \text{Cost}(u, v) > 0
$$

整个枢纽匹配子问题可以严密抽象为**一般图上的最大权匹配问题（Maximum Weight Matching）**：
设 0-1 决策变量 $x_{ij} = 1$ 表示短车 $i$ 与短车 $j$ 进行配对：
$$
\begin{aligned}
\max \quad & \sum_{(i, j) \in \mathcal{M}} S(i, j) x_{ij} \\
\text{s.t.} \quad & \sum_{j: (i, j) \in \mathcal{M}} x_{ij} \le 1, \quad \forall i \in \mathcal{P} \quad (\text{每辆短车至多只能与另一辆短车配对一次}) \\
& x_{ij} \in \{0, 1\}
\end{aligned}
$$

## 奇圈约束与 Edmonds 开花算法 (Blossom Algorithm)

一般图的最大权匹配虽然看似简单，但若直接进行连续 LP 松弛，其极点解会出现大量的 $\frac{1}{2}$ 分数解（例如三个互为匹配的短车构成三角形奇圈，各取 $x_{12} = x_{23} = x_{13} = 0.5$）。
为了消灭奇圈分数解，必须引入多面体组合学著名的 **Edmonds 奇圈开花不等式（Blossom Inequalities）**：
对于任意包含奇数个顶点的子集 $U \subset \mathcal{P}$（$|U| = 2k + 1$）：
$$
\sum_{e \in E(U)} x_e \le \frac{|U| - 1}{2} = k
$$
利用杰克·埃德蒙兹（Jack Edmonds）开花算法，最大权匹配可以在 $\mathcal{O}(|V|^3)$ 多项式时间内求出严格纯整数全局最优解！

::: pitfall 忽视枢纽组装解绑耗时导致的交付晚点
在枢纽将两辆 Pup 短车用连接架机械锁死装配（Coupling）、或者在后道拆卸分离（Decoupling），需要专门的地勤工人耗费 30-45 分钟。如果算法为了微小的运费节约，在网络沿途频繁地将挂车反复拆装匹配，导致的时间延误会引发严重的整网违约罚款。
:::

::: insight 物理构件的组合裂变是运筹学的用武之地
一辆 28 英尺的短挂车，单独看平平无奇；
但当运筹算法赋予其“在市区化整为零、在干线聚沙成塔”的动态网络匹配逻辑时，**原本笨重的物理运输网络瞬间进化为一套像乐高积木一样可以实时重组的柔性流体**。这种将机械物理设计与图论匹配完美融为一体的系统优化，是现代物流工程最杰出的代表作。
:::
