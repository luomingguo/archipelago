---
title: LOCAL 模型与有根树着色
type: lecture
lecture: 1
tags: [distributed-algorithms, local-model, graph-coloring, symmetry-breaking]
status: complete
---
# Lec 1 LOCAL 模型与有根树着色

> 对应 DGA 第 1.1 节与第 1.2.1 节 · 延伸阅读：Cole–Vishkin (1986)、GPS87、Naor–Stockmeyer (STOC 1993)

## TL;DR

- LOCAL 模型不限制消息大小与本地算力，用同步轮数精确刻画图算法输出对局部邻域拓扑的依赖半径。
- 有向路径 2-着色需要 $\Omega(n)$ 轮全局信息，但有根树 3-着色仅需 $\Theta(\log^* n)$ 轮局部通信即可完成。
- 利用 Sperner 家族或确定性掷币（Cole-Vishkin）可在单轮内将颜色数指数级压缩，经 $\log^* n$ 轮收敛至常数色后再降至 3 色。

## 1. 本讲要回答的核心问题

分布式图算法关心：**每个节点只能看到自己周围一小圈邻域，它能不能仅凭这点局部信息算出一个全局上合法的解？**

以图着色为例：直觉上“相邻不同色”是个全局约束，但我们将看到——对很多问题，每个节点的输出只依赖于它 $t$ 跳邻域内的拓扑，而 $t$ 可以小到 $\log^* n$。这种“局部即可”的现象正是本课程的主线。

本讲先给出计算模型（*LOCAL model*），再用**有根树 3-着色**这个看似简单、实则有深度的问题，展示局部算法的第一个非平凡结论。

## 2. LOCAL 模型

::: definition LOCAL 模型
给定任意 $n$ 节点图 $G=(V,E)$，$V=\{1,2,\dots,n\}$，它抽象了通信网络（默认简单、无向、无权）。每个节点 $v\in V$ 上运行一个进程。算法开始时，进程**不知道** $G$ 的结构，只知道 $n$（或一个上界 $N\in[n,n^c]$）以及自己在 $\{1,\dots,n\}$ 中的唯一标识符（*identifier*）。算法按**同步轮（synchronous rounds）**进行：每一轮，节点先基于已知信息做本地计算，然后向**所有邻居**发送一条消息，再接收邻居发来的消息。最终每个节点需算出自己的那部分输出（例如自己的颜色）。
:::

**关键约定：** LOCAL 模型**不限制消息长度，也不限制本地算力**。带宽受限的版本是后续的（*CONGEST model*）。

## 3. 局部性的数学刻画

LOCAL 模型最重要的性质是把“轮数”翻译成“看多远”：

> **观察.** 任何 $t$ 轮 LOCAL 算法，都等价于一个把每个节点的 $t$ 跳邻域拓扑映射到其输出的函数；反之亦然。

*为什么？* 因为消息无限长，一个节点在 $t$ 轮里能完整收集到距离 $t$ 以内所有节点的全部信息（第 1 轮收到 1 跳邻居、第 2 轮间接收到 2 跳……）。于是它的输出只能是这份信息的函数。反向：若存在这样一个函数，每个节点先用 $t$ 轮把 $t$ 跳邻域收齐，再本地套用该函数即可。

因此 LOCAL 模型在数学意义上**精确刻画了图问题的“局部性”**：解一个问题所需的最小轮数 = 输出对邻域的最小依赖半径。

::: theorem 平凡上界（Observation 1.2）
任意 $n$ 节点图上的任意图问题都可在 $O(n)$ 轮内解决；更精确地，用 $D$ 表示图的直径，则任意问题可在 $O(D)$ 轮内解决。
:::

*理由：* $O(D)$ 轮后，每个节点都已知道整张图，可本地暴力求全局最优解。所以课程真正有趣之处在于：哪些问题能比 $O(D)$ **快得多**地解决。

## 4. 有根树着色：问题设定

考虑有根树 $T=(V,E)$，$V=\{1,\dots,n\}$，每个节点 $v$ 知道自己的父亲 $p(v)$。目标是求一个**合法着色（proper coloring）** $\varphi:V\to\{1,\dots,q\}$，使得不存在节点 $v$ 满足 $\varphi(v)=\varphi(p(v))$。我们希望颜色数 $q$ 尽量小、轮数尽量少。

树显然可 2-着色，但在 LOCAL 模型里 2-着色非常贵：

> **观察 1.3.** 任何对 $n$ 节点有向路径做 2-着色的 LOCAL 算法都至少需要 $\Omega(n)$ 轮。
>
> *直觉：* 2-着色在路径上唯一（交替黑白），要确定自己该取哪一色，必须知道自己到端点的奇偶距离，这是全局信息。

而 **3-着色**没有这种障碍——它的轮复杂度紧确为 $\tfrac12\log^* n \pm O(1)$。本讲给出上界（算法），下界留到 Lec 4。

## 5. $\log^*$ 函数

::: definition 迭代对数 $\log^*$
$$\log^*(x)=\begin{cases}0 & x\le 1\\ 1+\log^*(\log x) & x>1\end{cases}$$
即“对 $x$ 反复取对数，把它降到 $\le 1$ 所需的次数”。它增长极慢：对一切实际的 $n$，$\log^* n \le 5$。
:::

## 6. 主结果

> **定理 1.4.** 任意 $n$ 节点有根树都可用 3 种颜色在 $\log^* n + O(1)$ 轮内着色。

> 注：上界可精化到 $\tfrac12\log^* n + O(1)$（SV93）甚至恰好 $\tfrac12\log^* n$（RS14），本讲不涉及。已知的 $O(\log^* n)$ 算法有四种思路（CV86, SV93, NS93, FHK16），主体相似。这里用的版本基于 NS95 的想法加上 GPS87 的若干步骤。

证明分三步：(a) 单轮把颜色数近指数地砍小（Sperner 家族）；(b) 迭代 $\log^* n$ 次降到常数色；(c) 再花常数轮降到 3 色。

## 7. 第一步：单轮颜色缩减（Sperner 家族）

> **引理 1.5.** 给定有根树的一个 $k$-着色 $\varphi_{\text{old}}$（$k$ 大于某常数 $C_0$），可在**单轮**内算出 $k'$-着色 $\varphi_{\text{new}}$，其中 $k' = \log k + \tfrac{\log\log k}{2}+1$。

**证明.** 每个节点 $u$ 把自己颜色 $\varphi_{\text{old}}(u)$ 发给孩子。下面让每个节点 $v$ 仅凭 $\varphi_{\text{old}}(v)$ 与其父亲 $u$ 的 $\varphi_{\text{old}}(u)$ 重新算色，无需再通信。

固定一个单射 $M:\{1,\dots,k\}\to \mathcal{F}_{k'}$，其中 $\mathcal{F}_{k'}$ 是 $\{1,\dots,k'\}$ 的所有大小为 $k'/2$ 的子集构成的族。这样的单射存在，因为
$$|\mathcal{F}_{k'}|=\binom{k'}{k'/2}\ge \frac{2^{k'}}{\sqrt{2k'}}\ge k.$$
对节点 $v$（父亲为 $u$）：由于 $M(\varphi_{\text{old}}(v))$ 与 $M(\varphi_{\text{old}}(u))$ 都是大小 $k'/2$ 的子集，且 $\varphi_{\text{old}}(v)\ne\varphi_{\text{old}}(u)$、$M$ 为单射，故
$$M(\varphi_{\text{old}}(v))\setminus M(\varphi_{\text{old}}(u))\ne\varnothing.$$
取 $\varphi_{\text{new}}(v)$ 为该差集中任一颜色，则它不在父亲的色集 $M(\varphi_{\text{old}}(u))$ 中，因而 $\varphi_{\text{new}}(v)\ne\varphi_{\text{new}}(u)$。$\square$

::: definition Sperner 家族（Sperner Family）
一族集合，其中没有任何一个集合是另一个集合的子集，称为 Sperner 家族。上证的关键正是：$\{1,\dots,k'\}$ 的所有 $k'/2$ 元子集互不包含。一般地，$k'$ 元集的全部 $\ell$ 元子集（$k'>\ell$）构成大小 $\binom{k'}{\ell}$ 的 Sperner 家族，取 $\ell=\lfloor k'/2\rfloor$ 时最大。Sperner 定理（Sperner 1928）表明这是固定基集下的最优界。
:::

**等价的二进制方法（更易实现）。** 把 $\varphi_{\text{old}}(v)$、$\varphi_{\text{old}}(u)$ 写成 $\lceil\log k\rceil$ 位二进制。设 $i_v$ 为二者首次不同的最低位下标，$b_v$ 为 $\varphi_{\text{old}}(v)$ 在该位的取值，令 $\varphi_{\text{new}}(v)=(i_v,b_v)$。这给出一个 $2\lceil\log k\rceil$-着色——这正是经典的（*Cole–Vishkin*）技巧“确定性掷币（deterministic coin tossing）”。

## 8. 第二步：迭代降到常数色

反复套用引理 1.5：
- 1 轮后：$n \to \log n + \tfrac{\log\log n}{2}+1$ 色；
- 再 1 轮：$\to \log\log n + O(\log\log\log n)$ 色；
- ……
- 共 $\log^* n + O(1)$ 轮后：降到不超过某常数 $C_0$ 色。

此时再用引理 1.5 已无收益。

## 9. 第三步：从常数色降到 3 色

> **引理 1.6.** 给定有根树的 $k$-着色（$k>4$），可在**两轮**内算出 $(k-1)$-着色。

**证明.** 第一轮每个节点 $u$ 把色发给孩子；令每个节点 $v$ 取临时色 $\varphi'_{\text{old}}(v)=\varphi_{\text{old}}(p(v))$（根节点取 $\{1,2,3\}\setminus\{\varphi_{\text{old}}(r)\}$ 中任一色）。这仍是合法着色，且有好性质：**同一父亲的所有孩子临时色相同**。

第二轮每个节点把 $\varphi'_{\text{old}}$ 发给孩子。然后定义：若 $\varphi'_{\text{old}}(v)\ne k$，保持不变；若 $\varphi'_{\text{old}}(v)=k$，则改取 $\{1,2,3\}\setminus\{\varphi'_{\text{old}}(p(v)),\,\varphi_{\text{old}}(v)\}$ 中一色。只有颜色为 $k$ 的节点改色，它们互不相邻，且新色与父、子都不同，故结果合法。$\square$

**定理 1.4 的证明.** 先用引理 1.5 迭代 $\log^* n + O(1)$ 次降到 $C_0=O(1)$ 色，再用引理 1.6 迭代 $C_0-3=O(1)$ 次降到 3 色。总轮数 $\log^* n + O(1)$。$\square$

## 10. 推广到一般图

可把定理 1.4 推广到**最大度为 $\Delta$ 的任意图**，在 $O(\log^* n)$ 轮内用 $\Delta^{O(\Delta)}$ 色着色：把每个节点的至多 $\Delta$ 个邻居各当作一个“父亲”，对每个邻居各做一次引理 1.5 式的比较，得到一个 $\Delta$ 元组作为新色。一轮把色数从 $k$ 降到 $(O(\log k))^\Delta$，迭代 $O(\log^* n)$ 次得 $\Delta^{O(\Delta)}$ 色。再花 $\Delta^{O(\Delta)}$ 额外轮可降到 $\Delta+1$ 色（每轮让“颜色严格大于全部邻居”的节点改取一个未被邻居占用的色）。Lec 3 将给出对 $\Delta$ 依赖好得多的 $\Delta+1$ 着色。

## 11. 本讲小结与延伸阅读

| 结果 | 颜色数 | 轮数 |
|---|---|---|
| 有向路径 2-着色 | 2 | $\Omega(n)$（下界） |
| 有根树 3-着色 | 3 | $\Theta(\log^* n)$ |
| 一般图推广 | $\Delta^{O(\Delta)}$ → $\Delta+1$ | $O(\log^* n)$ + $\Delta^{O(\Delta)}$ |

核心工具：**单轮颜色缩减**（Sperner 家族 / 二进制位比较），把颜色数近指数压缩。

- **Cole & Vishkin (1986)** — Deterministic Coin Tossing，$\log^*$ 着色的源头之一。
- **GPS87** — Parallel symmetry-breaking in sparse graphs，本讲算法借用其步骤。
- **Naor & Stockmeyer (STOC 1993)** — What can be computed locally？引入 LCL（局部可检验标号）框架，把“局部性”形式化。
