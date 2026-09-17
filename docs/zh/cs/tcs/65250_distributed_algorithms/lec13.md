---
title: 最小割 Min-Cut 近似算法
type: lecture
lecture: 13
tags: [distributed-algorithms, min-cut, approximation-algorithms, congest-model]
status: complete
---
# Lec 13 最小割 Min-Cut 近似算法

> 对应 DGA 第 2.3 节 · 延伸阅读：Ghaffari–Kuhn (DISC 2013)、Ghaffari–Haeupler (SODA 2016)

## TL;DR

- 在 CONGEST 模型中，最小割问题可通过构造连通度为 $k'$ 的稀疏证书将网络边数压缩至 $O(nk')$。
- 利用人工权重迭代调用分布式 MST 子程序，有效规避了在残差图上直接求森林导致直径失控的难题。
- 结合稀疏证书与边收缩两情形递归，在 $O(k(D+\sqrt n)\log^3 n)$ 轮内给出了 $(2+\varepsilon)$-近似最小割，并在平面图上借助低拥塞捷径进一步加速至 $\tilde O(D)$。

## 1. 本讲要回答的核心问题

**最小割（minimum cut）** $k$ 是使图断开所需删除的最少边数。本讲在 CONGEST 模型给出一个 $(2+\varepsilon)$-近似算法：输出非空顶点子集 $S$，使 $S$ 到 $V\setminus S$ 的边数 $\le(2+\varepsilon)k$。

> **主结果.** 对任意常数 $\varepsilon>0$，可在 $O\!\big(k(D+\sqrt n)\log^3 n\big)$ 轮内算出 $(2+\varepsilon)$-近似最小割（$k$ 为最小割大小）。

核心工具是**连通性的稀疏证书（sparse certificate）**，它复用了 Lec 12 的 MST 子程序。

## 2. 连通性的稀疏证书

直觉：在不改变最小割大小的前提下，把边数压到接近下限 $nk/2$ 的子图。

::: definition 连通度 $k'$ 的稀疏证书
生成子图 $H=(V,E_H)$ 称为 $G$ 关于连通度 $k'$ 的稀疏证书，若：
1. 对每个非空 $S\subset V$，$\mathrm{cut}_H(S,V\setminus S)\ge\min\{k',\,\mathrm{cut}_G(S,V\setminus S)\}$；
2. $H$ 至多 $nk'$ 条边。
:::

::: example 生成树作为稀疏证书
连通图 $G$ 的任意生成树 $T$ 满足条件 2（$n-1$ 条边）与条件 1（$\mathrm{cut}_T(S)\ge1$）。更一般地，不连通时任意极大生成森林都是 $k'=1$ 的稀疏证书。
:::

**构造（集中式轮廓）.** 迭代 $k'$ 次：第 $i$ 次计算当前图的极大生成森林 $F_i$，再令 $G\leftarrow G\setminus F_i$。最终 $H=\bigcup_{i=1}^{k'}F_i$ 即所求证书。

> **引理 2.5.** $H=\bigcup_i F_i$ 是连通度 $k'$ 的稀疏证书。

**分布式实现（避免在残图上反复算森林，因残图直径可能很大）.** 用人工边权：初始全设权 $1$；第 $i$ 次算**最小权生成树 $T_i$**，取其中**权为 $1$ 的边**作 $F_i$，然后把这些边权改成 $\infty$（实际取 $n^2$）。

> **引理 2.6.** 在“$G\setminus(\cup_{j<i}F_j)$ 权为 $1$、其余权为 $n^2$”的加权图上，$T_i$ 中权为 $1$ 的边恰构成 $G\setminus(\cup_{j<i}F_j)$ 的极大生成森林。

每个 $T_i$ 用 Lec 12 的 MST 算法在 $O((D+\sqrt n)\log n)$ 轮算出，$k'$ 次共 $O(k'(D+\sqrt n)\log n)$ 轮。

## 3. $(2+\varepsilon)$-近似算法

先假设最小割大小 $k$ 已知。算法每“层”如下：

1. 计算连通度 $k'=(1+\varepsilon/10)k$ 的稀疏证书 $H$（$O(k(D+\sqrt n)\log n)$ 轮）。
2. 考虑**收缩 $G\setminus H$ 的所有边**所得辅助图 $H'$。两条性质：(A) $H'$ 的边恰为 $H$ 的边，故 $H'$ 至多 $nk'=(1+\varepsilon/10)nk$ 条边；(B) $H'$ 的最小割 $=G$ 的最小割 $k$。

按 $H'$ 节点数分两情形：

::: theorem 情形 1（度数界与近似割）
若 $H'$ 有 $\ge n/(1+\varepsilon/5)$ 个节点，则平均度
$$\le\frac{2(1+\varepsilon/10)nk}{n/(1+\varepsilon/5)}\le 2k(1+\varepsilon/10)(1+\varepsilon/5)\le(2+\varepsilon)k,$$
故存在一个度 $\le(2+\varepsilon)k$ 的节点。它是 $G$ 中某些被收缩到一起的顶点子集 $S$，于是 $\mathrm{cut}_G(S)\le(2+\varepsilon)k$——这就是要找的近似割。
:::

**情形 2（$H'$ 有 $<n/(1+\varepsilon/5)$ 个节点）：** 难以直接找到小割，但节点数已缩小了 $(1+\varepsilon/5)$ 倍而最小割不变。令 $G\leftarrow H'$ **递归**。$O(\log_{1+\varepsilon/5} n)$ 层后节点数降到 $\le2$，必能找到割。

**去掉“已知 $k$”的假设：** 对 $1$ 到 $n^2$ 之间所有形如 $(1+\varepsilon/10)^i$ 的估计值各跑一遍，输出所有结果中**最小的割**。

## 4. 几点说明与拓展

- **去掉 $k$ 因子：** 用 Karger 式**采样**把最小割降到 $O(\log n)$，可把轮复杂度里的 $k$ 换成 $O(\log n)$，得 $\tilde O(D+\sqrt n)$。
- **加权图：** 把权 $w$ 边视为 $w$ 条平行边即可推广。
- **近最优性：** $\tilde O(D+\sqrt n)$ 已近最优——任何非平凡最小割近似都需 $\tilde\Omega(D+\sqrt n)$ 轮（下界见 Lec 14）。

## 5. 平面图：低拥塞捷径下的 $\tilde O(D)$

Ghaffari–Haeupler (SODA 2016) 把 Lec 12 的**低拥塞捷径**框架系统化，证明平面图（及有界亏格、排除稠密 minor 等）总存在 $\max\{\alpha,\beta\}\le\tilde O(D)$ 的捷径且 $\tilde O(D)$ 轮可构造。由此在平面网络上同时得到 $\tilde O(D)$-轮的 **MST** 与 **Min-Cut**——突破了一般图 $\tilde\Omega(\sqrt n)$ 的壁垒。

## 6. 本讲小结与近似割体系

| 内容 | 结论 |
|---|---|
| 稀疏证书 | 保最小割、边数 $\le nk'$；生成树为 $k'{=}1$ 证书 |
| 分布式构造 | 加权 MST 技巧，$O(k'(D+\sqrt n)\log n)$ 轮 |
| $(2+\varepsilon)$-近似 | 证书 + 收缩 + 两情形递归，$O(k(D+\sqrt n)\log^3 n)$ |
| 去 $k$ / 改进 | 采样 ⇒ $\tilde O(D+\sqrt n)$ |
| 平面图 | 低拥塞捷径 ⇒ $\tilde O(D)$ MST 与 Min-Cut |

Min-Cut 与 MST 共享同一套机制（MST 子程序、稀疏证书、低拥塞捷径），并同样止步于 $\tilde O(D+\sqrt n)$——下一讲证明这是全局问题的硬下界。
