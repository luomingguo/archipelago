---
title: "最短路径算法 II：路由表构造与稀疏生成子图"
type: lecture
lecture: 16
tags: [distributed-algorithms, routing-tables, spanners, congest-model]
status: complete
---
# Lec 16 最短路径算法 II：路由表构造与稀疏生成子图

> 主要文献：Lenzen–Patt-Shamir《Fast Routing Table Construction Using Small Messages》(STOC 2013) · Baswana–Sen《A Simple and Linear Time Randomized Algorithm for Computing Sparse Spanners in Weighted Graphs》(RSA 2006)

## TL;DR

- Lenzen 与 Patt-Shamir 提出了首个在 CONGEST 模型下用小消息于 $\tilde O(n^{1/2+\varepsilon} + HD)$ 轮内构造加权紧凑路由表的分布式算法。
- Baswana-Sen 随机算法通过逐层聚类生长在 $O(k)$ 轮内构造出 $(2k-1)$ 拉伸且仅含 $\tilde O(n^{1+1/k})$ 条边的稀疏生成子图（Spanner）。
- 将骨架图采样与生成子图压缩结合，使原本稠密的骨架拓扑能够被全网广播，达成了全源距离估计与路由判定的理论极限。

## 1. 本讲要回答的核心问题

Lec 15 算“到源点的距离”。本讲更进一步：**用小消息快速构造近似距离与路由表（routing tables）**——让每个节点不仅知道距离，还知道“下一跳往哪走”。

> **主结果（Lenzen–Patt-Shamir 2013）.** 给定 $0<\varepsilon\le1/2$，存在随机算法在 $\tilde O(n^{1/2+\varepsilon}+HD)$ 轮内（$HD$ 为无权跳数直径）算出近似距离与路由，**拉伸（stretch）**为 $O(\varepsilon^{-1}\log\varepsilon^{-1})$，高概率成立。

这是首个用 $O(\log n)$ 位小消息、在 $\tilde o(n)$ 轮内（当 $HD\in\tilde o(n)$）近似加权最短路的分布式算法，近匹配下界 $\tilde\Omega(\sqrt n+HD)$。

两大支柱：**骨架图（skeleton graph）** 与 **稀疏生成子图（spanner）**。

## 2. 骨架图（Skeleton Graph）

::: definition 骨架节点与骨架图
每个节点独立以概率约 $1/\sqrt n$ 被选为**骨架节点**，得 $\tilde O(\sqrt n)$ 个。骨架图 $G_{\mathrm{sk}}$ 以骨架节点为顶点，两骨架点间的边权 = 它们在原图中“**至多 $\tilde O(\sqrt n)$ 跳**”的最短距离。
:::

**关键性质（高概率）.** 任一对节点间的最短路若用 $\ge\tilde O(\sqrt n)$ 跳，则被骨架节点“切分”成每段 $\le\tilde O(\sqrt n)$ 跳的子路径——于是长程距离可在骨架图上“接力”算出，而骨架图只有 $\tilde O(\sqrt n)$ 个顶点。

**计算骨架边权.** 用限跳 Bellman–Ford（Lec 15）跑 $\tilde O(\sqrt n)$ 轮，让每个骨架点得到到附近骨架点的距离。骨架图边数可能达 $\Theta(n)$——直接广播太贵，于是引入**生成子图压缩**。

## 3. 稀疏生成子图（Spanner）：Baswana–Sen

::: definition $\alpha$-生成子图（Spanner）
图 $G$ 的子图 $H$ 称为 $\alpha$-生成子图（拉伸 $\alpha$），若对任意 $u,v$：$d_H(u,v)\le\alpha\cdot d_G(u,v)$。即 $H$ 用更少的边把距离近似保持到 $\alpha$ 倍以内。
:::

> **定理（Baswana–Sen 2006）.** 对任意整数 $k\ge1$，可（高概率）构造一个 **$(2k-1)$-生成子图**，期望边数 $\tilde O(n^{1+1/k})$，在 CONGEST 中用 $O(k)$ 轮（$k-1$ 次迭代）算出；集中式为线性时间。

**算法（基于聚类的逐层生长）.** 维护一个簇划分，初始每个节点自成一簇。第 $i$ 次迭代（共 $k-1$ 次）：

1. 上一层的每个簇独立以概率 $n^{-1/k}$ **存活**进入本层；
2. 对每个**未被任何相邻存活簇覆盖**的节点 $v$：把 $v$ 到**每个相邻簇**的最轻边各加入生成子图，然后 $v$ 退出（成为已定型）；
3. 对**相邻有存活簇**的节点 $v$：加入 $v$ 到某个相邻存活簇的最轻边，$v$ 加入该簇（采纳其簇标签）。

最后一步把所有剩余节点连到它们相邻的全部簇。

::: theorem 最优权衡推论
$(2k-1)$ 拉伸配 $O(n^{1+1/k})$ 边，是生成子图的已知最优权衡（与 Erdős 围长猜想一致）。
:::

## 4. 拼装：路由表构造

把上述两件拼起来：

1. **骨架采样：** 选 $\tilde O(\sqrt n)$ 骨架节点。
2. **骨架边权：** $\tilde O(\sqrt n)$-跳限跳 Bellman–Ford 算骨架点间距离，得骨架图 $G_{\mathrm{sk}}$。
3. **骨架生成子图：** 对 $G_{\mathrm{sk}}$（$\tilde O(\sqrt n)$ 个点）跑 Baswana–Sen，得 $\tilde O(n^{(k+1)/(2k)})$ 条边的**骨架生成子图**——足够稀疏，可在 $\tilde O(n^{1/2+\varepsilon}+HD)$ 轮内**广播给所有节点**（每个节点据此本地重建近似骨架距离）。
4. **本地短程：** 每个节点用 $\tilde O(\sqrt n)$-跳限跳 Bellman–Ford 知道到附近骨架点的距离与路由。
5. **合并 + 标签：** 近似距离 = 短程 + 骨架生成子图上的距离；路由的“下一跳”由短程方向 + 骨架接力给出。节点被赋予 $O(\log\varepsilon^{-1}\log n)$ 位标签以支持紧凑路由。

## 5. 与下界和 Lec 15 的关系

- **近最优：** $\tilde O(n^{1/2+\varepsilon}+HD)$ 近匹配 $\tilde\Omega(\sqrt n+HD)$（Lec 14）。
- **与 Nanongkai (Lec 15) 对比：** 两者都用 $\sqrt n$ **骨架**切分长程最短路。区别：Nanongkai 追求 $(1+o(1))$ 高精度的 SSSP；Lenzen–Patt-Shamir 追求**全源距离 + 路由表**，以稍大的常数级拉伸换取近 $\sqrt n$ 的全源构造。Baswana–Sen 生成子图是把稠密距离信息压到可广播规模的关键。

## 6. 本讲小结与全局问题收束

| 组件 | 结论 |
|---|---|
| 骨架图 | $\tilde O(\sqrt n)$ 采样点，限跳 BF 算边权，切分长程最短路 |
| Baswana–Sen 生成子图 | $(2k-1)$ 拉伸、$\tilde O(n^{1+1/k})$ 边、$O(k)$ 轮，聚类逐层生长 |
| 路由表（LPS 2013） | $\tilde O(n^{1/2+\varepsilon}+HD)$ 轮、拉伸 $O(\varepsilon^{-1}\log\varepsilon^{-1})$ |
| 最优性 | 近匹配 $\tilde\Omega(\sqrt n+HD)$ |

主线：**骨架采样把长程问题降到 $\tilde O(\sqrt n)$ 个关键点，生成子图把这些点的稠密距离信息压稀到可全网广播**——两者结合，使加权最短路与路由表在小消息模型里逼近理论极限。这也收束了 Lec 12–16 的全局问题主线：$\tilde\Theta(D+\sqrt n)$ 既是 MST、Min-Cut、最短路的上界，也是它们共同的下界。
