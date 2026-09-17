---
title: 最小生成树 MST 算法
type: lecture
lecture: 12
tags: [distributed-algorithms, mst, congest-model, ghs-algorithm]
status: complete
---
# Lec 12 最小生成树 MST 算法

> 对应 DGA 第 2.2 节 · 延伸阅读：Garay–Kutten–Peleg (FOCS 1993)、Kutten–Peleg (PODC 1995)

## TL;DR

- 在考虑有限带宽的 CONGEST 模型下，分布式最小生成树（MST）构成了所有全局图优化算法的基准母题。
- 基于分布式 Borůvka 算法骨架，通过区分小分量（本地收敛广播）与大分量（全图 BFS 流水线），将单阶段 MWOE 查找优化至 $O(D+\sqrt n)$ 轮。
- 引入低拥塞捷径（Low-Congestion Shortcuts）统一抽象，不仅解释了一般图的 $\tilde O(D+\sqrt n)$ 界，还在平面图与排除 minor 图族上实现了 $\tilde O(D)$ 轮的近直径级加速。

## 1. 本讲要回答的核心问题

从本讲起进入**全局问题（global problems）**：解依赖远处信息，最好情形也要 $\Theta(D)$ 跳（$D$ 为网络直径）。模型换成考虑带宽的（*CONGEST model*）——每轮每条边只能传一条 $O(\log n)$ 位消息。

**最小生成树（MST）**在分布式网络优化中地位极为中心：其上下界技术被反复用于其他全局问题。本讲给出一个近最优的 $\tilde O(D+\sqrt n)$-轮 MST 算法（基于 Kutten–Peleg），并引入统一框架**低拥塞捷径（low-congestion shortcuts）**。

## 2. 算法骨架：分布式 Borůvka

沿用 Borůvka 思路，共 $O(\log n)$ 个 phase，逐步把森林合并成生成树。初始每个节点自成一个分量。

每个 phase：每个分量 $S_i$ 有领袖 $s_i$（且知分量大小），沿其**最小权出边（minimum-weight outgoing edge, MWOE）**建议一次合并。

::: theorem MWOE 属于 MST
假设边权互异（把边端点 ID 追加到权值上即可使其唯一，且新权下的 MST 是原权下某个 MST），则每个分量的 MWOE 必属于 MST。
:::

设当前有 $N$ 个分量。每条建议边至多被两端各提一次，故至少 $N/2$ 条不同建议边；加入这些边即合并分量，分量数降到 $\le N/2$。$\log n$ 个 phase 后归一，得生成树。

剩下两件事：**如何算 MWOE**、**如何执行合并**，都要在 $O(D+\sqrt n)$ 轮内完成。

## 3. 计算最小权出边

每个节点 $v$ 先把 $c(v)$ 设为自己关联的最小权出边。目标：每个 $v\in S_i$ 得知整个分量 $S_i$ 的 MWOE。按分量大小分两类处理：

- **小分量（$<\sqrt n$ 顶点）：** 在分量自己的 BFS 树上做一次 $\min$-**收敛广播**（Lec 2），叶到根取最小，根得 MWOE，再广播回全分量。耗时 $O(\sqrt n)$。
- **大分量（$\ge\sqrt n$ 顶点）：** 这类分量至多 $n/\sqrt n=\sqrt n$ 个。因数量少，可让它们的通信都走**全图的 BFS 树**并用**流水线（pipelining）**并行处理，$O(D+\sqrt n)$ 轮算出全部大分量的 MWOE。

> 两类合起来给出每 phase $O(D+\sqrt n)$ 轮，共 $\tilde O(D+\sqrt n)$ 轮的 MST。

## 4. 统一框架：低拥塞捷径

小/大分量的划分本质是一个图论对象：

::: definition 低拥塞捷径（Low-Congestion Shortcuts）
给定图 $G$ 及把 $V$ 划分为各自连通的子集 $S_1,\dots,S_N$。一组子图 $H_1,\dots,H_N\subseteq G$ 称为**拥塞 $\alpha$、扩张 $\beta$ 的捷径**，若：
1. 每个 $G[S_i]+H_i$ 的直径 $\le\beta$；
2. 每条边 $e$ 至多出现在 $\alpha$ 个 $G[S_i]+H_i$ 中。
:::

> **定理 2.3.** 若图族 $\mathcal G$ 中每个图的任意连通划分都存在 $\max\{\alpha,\beta\}\le K$ 的捷径，且可在 $\tilde O(T)$ 轮找到，则存在随机 MST 算法在 $\tilde O(T)+O(\alpha\log n+\beta\log^2 n)=\tilde O(T+K)$ 轮内算出 MST。

直觉：$\beta$ 控制“分量内信息聚合要走多远”，$\alpha$ 控制“多少分量挤在同一条边上”。三类典型图族：
- **一般图：** 小/大划分给出 $\max\{\alpha,\beta\}\le D+\sqrt n$，故 $\tilde O(D+\sqrt n)$。
- **平面图及其推广**（有界亏格、有界树宽、排除稠密 minor）：存在 $\max\{\alpha,\beta\}\le\tilde O(D)$ 的捷径且 $\tilde O(D)$ 轮可找到 ⇒ $\tilde O(D)$-轮 MST。
- **Erdős–Rényi 随机图 $G_{n,p}$**：存在 $\max\{\alpha,\beta\}\le\mathrm{poly}\log n$ 的捷径 ⇒ $2^{O(\sqrt{\log n})}$-轮 MST。

## 5. 执行合并

为控制合并深度，把合并限制成**星形（star-shaped）**：每个分量领袖掷一枚随机硬币，只允许“正面”分量作中心、接收“反面”邻接分量的合并边；中心领袖成为新领袖。这种概率化星形合并仍在 $O(\log n)$ 个 phase 后高概率成树。

每次合并，每个节点需获知三样额外信息，均可在 $O(D+\sqrt n)$ 轮内传播：
1. 自己分量领袖掷的硬币；
2. 新分量领袖 ID（=中心分量领袖）；
3. 新分量大小。

## 6. 历史与现状

- **Garay–Kutten–Peleg (FOCS 1993)：** 首个 MST 的**亚线性时间**分布式算法，开启 $\tilde O(D+\sqrt n)$ 这条线。
- **Kutten–Peleg (PODC 1995)：** $O(D+\sqrt n\log^* n)$，即本讲算法的来源；同文给出 $k$-支配集的快速构造。
- 该 $\tilde O(D+\sqrt n)$ 在最坏情形近最优（下界见 Lec 14）。

## 7. 本讲小结与算法框架

| 内容 | 结论 |
|---|---|
| 骨架 | 分布式 Borůvka，$O(\log n)$ phase，每 phase 沿 MWOE 星形合并 |
| MWOE 计算 | 小分量本地收敛广播 / 大分量全局 BFS + 流水线 ⇒ $O(D+\sqrt n)$ |
| 统一框架 | 低拥塞捷径（拥塞 $\alpha$、扩张 $\beta$），$\tilde O(T+K)$ MST |
| 一般图 / 平面 / 随机图 | $\tilde O(D+\sqrt n)$ / $\tilde O(D)$ / $2^{O(\sqrt{\log n})}$ |

MST 是全局问题的“母题”：分量–MWOE–合并的三段式、以及小/大分量（低拥塞捷径）的调度思想，将在 Min-Cut（Lec 13）与最短路（Lec 15–16）中反复出现。
