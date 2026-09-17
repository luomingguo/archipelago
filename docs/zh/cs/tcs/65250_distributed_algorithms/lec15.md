---
title: "最短路径算法 I：加权最短路的分布式近似"
type: lecture
lecture: 15
tags: [distributed-algorithms, shortest-paths, congest-model, approximation-algorithms]
status: complete
---
# Lec 15 最短路径算法 I：加权最短路的分布式近似

> 主要文献：Danupon Nanongkai《Distributed Approximation Algorithms for Weighted Shortest Paths》(STOC 2014)

## TL;DR

- 带权图中的跳数直径（Shortest-Path Diameter, SPD）可能与拓扑直径 $D$ 发生严重脱钩，导致精确 Bellman-Ford 退化至 $\Theta(n)$ 轮。
- Nanongkai 证明通过引入近似可以打破跳数壁垒，在 $\tilde O(\sqrt n\,D^{1/4} + D)$ 轮内求出加权 SSSP 的 $(1+o(1))$-近似解。
- 算法核心在于限跳 Bellman-Ford、$\sqrt n$ 个骨架节点的随机采样与多尺度边权随机缩放，在低直径图上近匹配了 $\tilde\Omega(\sqrt n+D)$ 下界。

## 1. 本讲要回答的核心问题

CONGEST 模型下的**加权单源最短路（SSSP）**：源点 $s$，每个节点要算出到 $s$ 的（近似）距离。无权图用 BFS 即 $O(D)$；**带权**则需 Bellman–Ford，最坏 $O(n)$ 轮。

一个自 2004 年（Elkin）就被提出的问题：**近似能否换取加速？** Nanongkai 给出肯定回答：

> **主结果.** 存在随机算法，在 $\tilde O(\sqrt n\,D^{1/4}+D)$ 轮内算出加权 SSSP 的 $(1+o(1))$-近似。
> 当 $D$ 较小时其轮数匹配 Das Sarma 等的下界 $\tilde\Omega(\sqrt n+D)$（Lec 14），相差仅 $\mathrm{poly}\log n$。

## 2. 难点：跳数直径 (Shortest-Path Diameter)

带权 Bellman–Ford 经 $h$ 轮算出的是“**至多 $h$ 跳**的最短路”。要算真实最短路，需 $h\ge$ **跳数直径（shortest-path diameter, SPD）**：最短路所用的最大边数。

::: example 权值使跳数脱钩（为何 $D$ 小却仍慢）
一个直径 $D=2$ 的图，其加权最短路却可能要绕经 $\Theta(n)$ 条边（轻边构成的长链 + 重的捷径边）。此时 $\mathrm{SPD}=\Theta(n)$，朴素 Bellman–Ford 要 $\Theta(n)$ 轮——**带权使“跳数”与“直径”脱钩**。
:::

因此算法的核心是**降低有效跳数**：用近似换取“用很少的跳就能逼近真实距离”。

## 3. 核心思想

### 3.1 限跳 Bellman–Ford（$h$-hop 距离）

::: definition $h$-跳距离（$h$-Hop Distance）
$d^{(h)}(u,v)$ 为从 $u$ 到 $v$、**至多 $h$ 条边**的最短路长度。它可由 Bellman–Ford 在 $h$ 轮内对所有 $v$ 同时算出（每轮做一次松弛 $d(v)\leftarrow\min_u d(u)+w(u,v)$）。
:::

若能让每对相关点间存在一条“近似最短、且只用 $\tilde O(h)$ 跳”的路径，则 $h$ 轮限跳 Bellman–Ford 即给出近似距离。

### 3.2 骨架 / 地标采样（Skeleton / Landmarks）

随机采样 $\Theta(\sqrt n)$ 个**骨架节点（skeleton nodes）**。关键性质（高概率）：**任意一条用 $\ge\sqrt n$ 跳的最短路上，必经过某个骨架节点**（因为长路径上每段长度 $\sqrt n$ 的窗口都大概率含一个采样点）。于是“长程”最短路被分解成“骨架点之间的跳”，而骨架点只有 $\tilde O(\sqrt n)$ 个。

### 3.3 拼装步骤

1. **短程：** 用 $\tilde O(\sqrt n)$ 轮的限跳 Bellman–Ford，算出每个节点到附近（$\le\sqrt n$ 跳）节点的近似距离，特别是到最近骨架节点的距离。
2. **骨架图：** 在 $\tilde O(\sqrt n)$ 个骨架节点上构造一张**骨架图（skeleton graph）**，边权为骨架点间的（限跳）近似距离；在其上求骨架点到 $s$ 的距离。骨架图很小，其信息可被高效汇总/广播。
3. **合并：** 每个节点的近似距离 $=$ 它到最近骨架点的短程距离 $+$ 骨架点到 $s$ 的距离，取最小。

### 3.4 随机缩放 / 扰动（控制近似与跳数）

为得到 $1+o(1)$ 而非常数近似，需对边权做**随机缩放/取整（scaling/rounding）**：把权值离散到 $\mathrm{poly}\log$ 个尺度，使限跳路径在每个尺度上都近似最优，再叠加。这把“少跳”与“高精度”同时兼顾。

## 4. 与上下界的关系

- **下界（Lec 14）：** Das Sarma 等给出 $\tilde\Omega(\sqrt n+D)$，对任意多项式近似比、即便 $D=\Theta(\log n)$ 都成立。故当 $D$ 小时本算法的 $\sqrt n$ 项是最优的。
- **APSP：** Nanongkai 进一步给出了加权全源最短路的亚线性近似算法。
- **精确最短路：** 是另一条更难的理论方向（Huang–Nanongkai–Saranurak FOCS 2017 等）。

## 5. 本讲小结与近似最短路框架

| 内容 | 结论 |
|---|---|
| 主结果 | $(1+o(1))$-近似 SSSP，$\tilde O(\sqrt n\,D^{1/4}+D)$ 轮 |
| 难点 | 跳数直径 $\mathrm{SPD}$ 可达 $\Theta(n)$，与 $D$ 脱钩 |
| 工具 | 限跳 Bellman–Ford + $\sqrt n$ 骨架采样 + 随机缩放 |
| 最优性 | $D$ 小时匹配下界 $\tilde\Omega(\sqrt n+D)$（Lec 14） |

主线：**近似确实能换取加速**——把“必须走满 $\mathrm{SPD}$ 跳”的硬约束，用骨架采样切成 $\tilde O(\sqrt n)$ 跳的短程问题加一个小骨架图。
