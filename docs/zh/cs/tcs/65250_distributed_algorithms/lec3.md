---
title: 一般图的确定性着色
type: lecture
lecture: 3
tags: [distributed-algorithms, graph-coloring, local-model, linial-algorithm]
status: complete
---
# Lec 3 一般图的确定性着色

> 对应 DGA 第 1.4 节 · 延伸阅读：Linial (1992)、Kuhn–Wattenhofer (PODC 2006)、Kuhn (SPAA 2009)

## TL;DR

- 在最大度为 $\Delta$ 的图上，Linial 算法利用覆盖无关族在 $O(\log^* n)$ 轮内将着色数压缩至 $O(\Delta^2)$。
- Kuhn-Wattenhofer 引入分桶并行缩减技巧，在 $O(\Delta\log\Delta + \log^* n)$ 轮内将色数降低至 $(\Delta+1)$。
- Kuhn 缺陷着色通过允许受控的同色邻居度数，配合度数减半递归，进一步实现了 $O(\Delta + \log^* n)$ 轮的确定性 $(\Delta+1)$-着色。

## 1. 本讲要回答的核心问题

终极目标是 **$(\Delta+1)$-着色**：用颜色 $\{1,\dots,\Delta+1\}$ 给最大度 $\Delta$ 的图合法着色。集中式贪心（逐点取一个未被已着邻居占用的色）显然可行，但直接搬到 LOCAL 会退化为 $\Omega(n)$ 轮（着色顺序是全局的）。

本讲分三步逼近 $(\Delta+1)$-着色，轮数依次改进：

1. **Linial 算法**：$O(\Delta^2)$ 色，$O(\log^* n)$ 轮；
2. **Kuhn–Wattenhofer**：转成 $(\Delta+1)$ 色，$O(\Delta\log\Delta+\log^* n)$ 轮；
3. **Kuhn 缺陷着色**：进一步到 $O(\Delta+\log^* n)$ 轮。

## 2. Take 1：Linial 的 $O(\Delta^2)$ 着色

> **定理 1.17.** 存在确定性 LOCAL 算法，在 $O(\log^* n)$ 轮内把任意最大度 $\Delta$ 的 $n$ 节点图着成 $O(\Delta^2)$ 色。

核心是单轮颜色缩减（推广自 Lec 1 引理 1.5；区别在于现在要避开**所有邻居**而非仅父亲）：

> **引理 1.18.** 给定最大度 $\Delta$ 图的 $k$-着色，单轮内可算出 $k'$-着色，$k'=O(\Delta^2\log k)$；若 $k\le\Delta^3$，则可改进到 $k'=O(\Delta^2)$。

**定理 1.17 的证明.** 从初始 $n$-着色出发反复用引理 1.18：
$$n \to O(\Delta^2\log n)\to O(\Delta^2(\log\Delta+\log\log n))\to\cdots$$
$O(\log^* n)$ 次后到 $O(\Delta^2\log\Delta)$ 色，再用引理 1.18 第二部分一轮降到 $O(\Delta^2)$ 色。$\square$

## 3. 关键工具：覆盖无关族 (Cover-Free Families)

::: definition 覆盖无关族（Cover-Free Family）
给定基集 $\{1,\dots,k'\}$，集族 $S_1,\dots,S_k\subseteq\{1,\dots,k'\}$ 称为 **$\Delta$-覆盖无关族**，若对任意指标 $i_0,i_1,\dots,i_\Delta$ 都有
$$S_{i_0}\setminus\Big(\bigcup_{j=1}^{\Delta} S_{i_j}\Big)\ne\varnothing.$$
即：族中没有任何一个集合被另外 $\Delta$ 个集合的并所覆盖。
:::

> **用法（单轮颜色缩减）.** 旧色为 $q$ 的节点 $v$ 用集合 $S_q\subseteq\{1,\dots,k'\}$ 作为自己的“候选色集”。它取新色 $q'\in S_q$ 使得 $q'$ 不在任何邻居的候选色集中。覆盖无关性恰好保证：$v$ 至多 $\Delta$ 个邻居的色集之并不能盖住 $S_q$，故这样的 $q'$ 必存在。

覆盖无关族是 Sperner 家族（Lec 1）的推广：Sperner 家族 = 1-覆盖无关族。我们希望基集 $k'$ 尽量小。

### 3.1 存在性：概率方法（Lemma 1.20）

> **引理 1.20.** 对任意 $k,\Delta$，存在大小为 $k$、基集大小 $k'=O(\Delta^2\log k)$ 的 $\Delta$-覆盖无关族。

**证明.** 取 $k'=C\Delta^2\log k$（$C$ 充分大）。对每个 $i$，让 $S_i$ 独立地以概率 $p=1/\Delta$ 纳入每个元素。固定 $i_0,\dots,i_\Delta$，单个元素 $q$ 落入 $S_{i_0}\setminus\bigcup_j S_{i_j}$ 的概率为 $\tfrac1\Delta(1-\tfrac1\Delta)^\Delta\ge\tfrac{1}{4\Delta}$。故无任何此种 $q$ 的概率 $\le(1-\tfrac1{4\Delta})^{k'}\le e^{-C\Delta\log k/4}$。指标选法共 $k\binom{k-1}{\Delta}\le k(k-1)^\Delta$ 种，并集界给出失败概率
$$\le k(k-1)^\Delta e^{-C\Delta\log k/4}\le e^{-C\Delta\log k/8}\ll 1.$$
故存在。$\square$

### 3.2 显式构造：低次多项式（Lemma 1.21）

> **引理 1.21.** 对 $\Delta\ge k^{1/3}$，存在大小 $k$、基集 $k'=O(\Delta^2)$ 的 $\Delta$-覆盖无关族。

**证明.** 取素数 $q\in[3\Delta,6\Delta]$（由伯特兰-切比雪夫定理存在）。在有限域 $\mathbb F_q$ 上，给每个 $i$ 配一个不同的 2 次多项式 $g_i:\mathbb F_q\to\mathbb F_q$（共 $q^3>\Delta^3>k$ 个，足够）。令 $S_i=\{(a,g_i(a)):a\in\mathbb F_q\}\subseteq\mathbb F_q\times\mathbb F_q$，基集大小 $k'=q^2=O(\Delta^2)$。两条性质：
- (A) $|S_i|=q$；
- (B) $i\ne i'$ 时 $|S_i\cap S_{i'}|\le 2$（因 $g_i-g_{i'}$ 为 $\le 2$ 次多项式，至多 2 个零点）。

于是
$$\Big|S_{i_0}\setminus\bigcup_{j=1}^\Delta S_{i_j}\Big|\ge |S_{i_0}|-\sum_{j=1}^\Delta|S_{i_0}\cap S_{i_j}|\ge q-2\Delta>\Delta\ge 1.\qquad\square$$

> 去掉 $\Delta\ge k^{1/3}$ 假设：取 $q=\Theta(\Delta\log_\Delta k)$、$d=\Theta(\log_\Delta k)$，得 $k'=O(\Delta^2\log^2_\Delta k)$。

引理 1.20 与 1.21 即给出引理 1.18，从而完成定理 1.17。

## 4. Take 2：Kuhn–Wattenhofer，转成 $(\Delta+1)$ 着色

### 4.1 逐一缩减（Warm-up）

> **引理 1.22.** 给定最大度 $\Delta$ 图的 $k$-着色（$k\ge\Delta+2$），单轮内可算 $(k-1)$-着色。

**证明.** 颜色 $\ne k$ 的节点不变；颜色 $=k$ 的节点改取 $\{1,\dots,\Delta+1\}$ 中某个未被邻居占用的色（因度 $\le\Delta$，必存在）。$\square$

> **定理 1.23.** 存在确定性 LOCAL 算法在 $O(\Delta^2+\log^* n)$ 轮内给出 $(\Delta+1)$-着色。
>
> （先 Linial 得 $O(\Delta^2)$ 色，再逐一缩减 $O(\Delta^2)$ 轮。）

### 4.2 分桶并行缩减（KW06 的巧思）

> **引理 1.24.** 给定 $k$-着色（$k\ge\Delta+2$），在 $O(\Delta\log\tfrac{k}{\Delta+1})$ 轮内可算 $(\Delta+1)$-着色。

**证明.** 把颜色 $\{1,\dots,k\}$ 分成 $\lfloor\tfrac{k}{2\Delta+2}\rfloor$ 个桶，每桶 $2\Delta+2$ 色。**各桶可并行**做逐一缩减（不同桶色不交，互不干扰），$O(\Delta)$ 轮后每桶降到 $\Delta+1$ 色，总色数减半。重复 $\lceil\log\tfrac{k}{\Delta+1}\rceil$ 次即到 $\Delta+1$ 色。$\square$

> **定理 1.25.** 存在确定性 LOCAL 算法在 $O(\Delta\log\Delta+\log^* n)$ 轮内给出 $(\Delta+1)$-着色。
>
> （Linial 得 $O(\Delta^2)$ 色，再用引理 1.24，$k=O(\Delta^2)$ 时为 $O(\Delta\log\Delta)$ 额外轮。）

## 5. Take 3：Kuhn 缺陷着色，$O(\Delta+\log^* n)$ 轮

::: definition 缺陷着色（Defective Coloring）
$\varphi:V\to\{1,\dots,k\}$ 称为 **$d$-缺陷 $k$-着色**，若每种颜色 $q$ 诱导的子图最大度 $\le d$；即每个节点至多有 $d$ 个同色邻居。标准合法着色就是 $0$-缺陷着色。
:::

> **引理 1.28.** 给定 $d$-缺陷 $k$-着色，单轮内可算 $d'$-缺陷 $k'$-着色，$k'=O\big((\tfrac{\Delta-d}{d'-d+1})^2\log k\big)$。
> （即：大幅减色，仅微增缺陷。）

> **定理 1.26.** 存在确定性 LOCAL 算法在 $O(\Delta+\log^* n)$ 轮内给出 $(\Delta+1)$-着色。

**证明（递归分解度数）.** 先 Linial 得 $C\Delta^2$ 色。反复用引理 1.28：
$$C\Delta^2\text{-色}\to(\tfrac{\Delta}{\log\Delta})\text{-缺陷}\,O(\log^3\Delta)\text{-色}\to\cdots$$
$O(\log^*\Delta)$ 次后得 $(\tfrac\Delta2)$-缺陷 $O(1)$-色。每个色类诱导出最大度 $\le\Delta/2$ 的子图，即把 $G$ 分成 $O(1)$ 个度 $\le\Delta/2$ 的子图 $G_1,\dots,G_{O(1)}$，对各自递归用 $\Delta/2+1$ 色（并行），合并后是 $O(\Delta)$ 色，再逐一缩减 $O(\Delta)$ 轮到 $\Delta+1$。递归式
$$T(\Delta)=O(\log^*\Delta)+T(\Delta/2)+O(\Delta)\ \Rightarrow\ T(\Delta)=O(\Delta).$$
加上初始 $O(\log^* n)$ 即得。$\square$

## 6. 历史与现状

$O(\Delta+\log^* n)$ 长期被认为可能是确定性 $(\Delta+1)$-着色的极限，直到 2015：

- **Barenboim (2015):** $O(\Delta^{3/4}\log\Delta+\log^* n)$；
- **Fraigniaud–Heinrich–Kosowski (FHK16):** $O(\sqrt\Delta\log^{2.5}\Delta+\log^* n)$。

确定性 $(\Delta+1)$-着色的最优轮复杂度仍是重要开放问题。随机算法是另一条线（Lec 5：$O(\log n)$ 随机 $(\Delta+1)$-着色）。

## 7. 本讲小结与算法对比

| 算法 | 颜色数 | 轮数 | 关键工具 |
|---|---|---|---|
| Linial (Take 1) | $O(\Delta^2)$ | $O(\log^* n)$ | 覆盖无关族 |
| Kuhn–Wattenhofer (Take 2) | $\Delta+1$ | $O(\Delta\log\Delta+\log^* n)$ | 分桶并行缩减 |
| Kuhn 缺陷着色 (Take 3) | $\Delta+1$ | $O(\Delta+\log^* n)$ | 缺陷着色 + 度数减半递归 |

主线：“先快速降到 $\mathrm{poly}(\Delta)$ 色（覆盖无关族，$O(\log^* n)$ 轮），再把对 $\Delta$ 的依赖一步步压低（分桶 / 缺陷着色）”。
