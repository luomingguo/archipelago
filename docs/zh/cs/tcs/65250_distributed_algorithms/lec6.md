---
title: 网络分解：定义与随机化构造
type: lecture
lecture: 6
tags: [distributed-algorithms, network-decomposition, randomized-algorithms, ball-carving]
status: complete
---
# Lec 6 网络分解：定义与随机化构造

> 对应 DGA 第 1.5.1 节（定义与应用）与第 1.5.2 节（随机化构造） · 延伸阅读：ALGP89、Linial–Saks (SODA 1992)、Miller–Peng–Xu (SPAA 2013)、Elkin–Neiman (PODC 2016)

## TL;DR

- 网络分解将图节点划分为 $C$ 个颜色块，每个块由两两不相邻、内部直径 $\le D$ 的簇构成，是统一求解着色与 MIS 等局部问题的通用归约器。
- 给定 $(C,D)$ 网络分解，可在 $O(CD)$ 轮内完成 $(\Delta+1)$-着色或 MIS 求解。
- 基于几何分布随机半径的球生长（Ball Carving）算法利用无记忆性使边界丢弃概率恒为 $\varepsilon$，在 $O(\log^2 n)$ 轮内高概率构造出 $C=D=O(\log n)$ 的弱直径分解。

## 1. 本讲要回答的核心问题

前几讲围绕“着色”展开。本讲引入一个**更通用**的工具——**网络分解（network decomposition）**，它能统一求解一大类局部问题（着色、MIS、最大匹配等）。

核心想法：把图的节点分成 $C$ 个“块（block）”，每块由一些**低直径、互不相邻**的簇（cluster）组成。然后逐块处理：同块内各簇互不相邻可并行；每簇直径小，可由簇内领袖在 $O(D)$ 轮内聚合局部信息并本地求解。于是只要 $C$、$D$ 都小，整个问题就快。

## 2. 定义

::: definition 弱直径网络分解（Weak-Diameter Network Decomposition）
$(C,D)$ 弱直径网络分解把 $G$ 划分为顶点不交的子图 $G_1,\dots,G_C$，使每个 $G_i$ 由若干**顶点不交且两两不相邻**的簇 $X_1,X_2,\dots$ 组成，每簇内任两点 $v,u$ 在**原图 $G$** 中距离 $\le D$（簇的数量不限）。每个 $G_i$ 称为一个块。
:::

::: definition 强直径网络分解（Strong-Diameter Network Decomposition）
$(C,D)$ 强直径网络分解：划分为 $G_1,\dots,G_C$，每个 $G_i$ 的**每个连通分量**直径 $\le D$。
:::

二者区别在于“距离按谁算”：弱直径允许簇在自身诱导子图里断开，只要在原图 $G$ 里靠得近；强直径要求簇在自身子图里就连通且低直径。**强直径分解一定是弱直径分解。**

## 3. 应用：用网络分解做 $(\Delta+1)$-着色

> **定理 1.31.** 给定 $G$ 的 $(C,D)$ 弱直径网络分解，可在 $O(CD)$ 轮内算出 $(\Delta+1)$-着色。

**证明.** 逐块着色 $G_1,\dots,G_C$，处理 $G_{i+1}$ 时考虑前面已着的色。对 $G_{i+1}$ 的每个簇 $X_j$：取簇内 ID 最大者 $v_j$ 为领袖（$O(D)$ 轮可选出）。$v_j$ 聚合 $X_j$ 的诱导拓扑及 $X_j$ 在前面块中相邻节点的颜色（相关信息都在 $v_j$ 的 $D+1$ 距离内，$O(D)$ 轮可达），本地贪心地给 $X_j$ 各点选 $(\Delta+1)$ 中合法色，再回传。由于同块各簇互不相邻，全部簇并行无冲突。每块 $O(D)$ 轮，共 $O(CD)$。$\square$

> 同理可在 $O(CD)$ 轮内求 MIS。网络分解因此是“通用归约器”：好的分解直接带来一大类问题的快速分布式算法。

## 4. 随机化构造（球生长 / Ball Carving）

> **定理 1.32.** 存在随机 LOCAL 算法，在 $O(\log^2 n)$ 轮内高概率算出任意 $n$ 节点图的 $(C,D)$ 弱直径网络分解，$C=O(\log n)$，$D=O(\log n)$。

> 轮数可改进到 $O(\log n)$；而 $C,D$ 已近最优，不能同时显著改进。

**算法（逐块生成，第 $i+1$ 块）.** 在 $G\setminus(\bigcup_{j\le i}G_j)$ 上：
1. 每个节点 $u$ 独立抽取随机半径 $r_u\sim\mathrm{Geom}(\varepsilon)$，即 $\Pr[r_u=y]=\varepsilon(1-\varepsilon)^{y-1}$（$\varepsilon\in(0,1)$ 为自由参数）。把 $u$ 距离 $\le r_u$ 内的点视为 $u$ 的“球”。
2. 对每个 $v$，令 $\mathrm{Center}(v)$ = 满足 $\mathrm{dist}_G(u,v)\le r_u$ 的节点中 ID 最小者。
3. **同中心的节点构成一个簇**；丢弃恰好落在球边界（$\mathrm{dist}_G(v,u)=r_u$，$u=\mathrm{Center}(v)$）的节点，留作下一块处理。

要证两件事：簇直径低、$C$ 轮后所有节点都被聚类。

### 4.1 簇直径

> **引理 1.33.** 高概率下最大簇直径 $\le O(\log n/\varepsilon)$，故该聚类可在 $O(\log n/\varepsilon)$ 轮算出。
> （几何分布的指数尾界使得半径以高概率不超过 $O(\log n/\varepsilon)$。）

### 4.2 每个节点被丢弃的概率小

> **引理 1.34.** 对每个节点 $v$，它未被聚类（落在自己簇边界而被丢弃）的概率 $\le\varepsilon$。

**证明.** 对固定中心 $u$，定义事件：
- $E_1=\{r_u=\mathrm{dist}_G(v,u)\}$（恰在边界）；
- $E_2=\{r_u\ge\mathrm{dist}_G(v,u)\}$（球含 $v$）；
- $E_3=\{\forall u'\in\mathrm{before}(u),\ r_{u'}<\mathrm{dist}_G(v,u')\}$（ID 更小者都够不到 $v$）。

则
$$\Pr[v\text{ 未聚类}\mid\mathrm{Center}(v)=u]=\Pr[E_1\cap E_3\mid E_2\cap E_3]=\frac{\Pr[E_1]}{\Pr[E_2]}=\varepsilon,$$
其中用到 $E_3$ 与 $E_1,E_2$ 独立，以及几何分布的**无记忆性**：$\Pr[r_u=t\mid r_u\ge t]=\varepsilon$。于是
$$\Pr[v\text{ 未聚类}]=\sum_u\Pr[v\text{ 未聚类}\mid\mathrm{Center}(v)=u]\Pr[\mathrm{Center}(v)=u]=\varepsilon.\qquad\square$$

> **直觉：** 几何半径的无记忆性让“恰好停在边界”相对于“球已盖住 $v$”的条件概率恒为 $\varepsilon$，与具体中心无关——这是整个分析能干净收尾的关键。

### 4.3 块数

::: theorem 推论 1.35（网络分解块数上界）
经 $C=O(\log_{1/\varepsilon} n)$ 次迭代后，所有节点高概率被聚类。

*理由：* 每次迭代每个节点以概率 $\ge1-\varepsilon$ 被聚类（引理 1.34），故 $O(\log_{1/\varepsilon}n)$ 轮后剩余未聚类节点高概率为零。取 $\varepsilon$ 为常数即得 $C=O(\log n)$、$D=O(\log n)$。
:::

## 5. 历史脉络

- **ALGP89**（Awerbuch–Luby–Goldberg–Plotkin）首次提出网络分解概念，给出确定性 $2^{O(\sqrt{\log n\log\log n})}$ 构造。
- **LS91**（Linial–Saks）称之为低直径图分解，给出 SODA 1992 的随机构造。
- **MPX13**（Miller–Peng–Xu）用**随机移位 / 指数随机半径**（本讲球生长的并行版本前身）给出干净的并行构造。
- **PODC 2016**（Elkin–Neiman）给出分布式强直径网络分解。
- 长期开放问题：确定性 $\mathrm{poly}(\log n)$ 构造——直到 RG20 解决（Lec 7）。

## 6. 本讲小结与网络分解性质

| 内容 | 结论 |
|---|---|
| 弱 / 强直径分解 | 强 ⇒ 弱 |
| 应用 | $(C,D)$ 分解 $\Rightarrow$ $O(CD)$ 轮 $(\Delta+1)$-着色 / MIS |
| 随机构造 | $C=D=O(\log n)$，$O(\log^2 n)$（可优化到 $O(\log n)$）轮 |
| 关键技巧 | 几何随机半径 + 无记忆性，使丢弃概率恒为 $\varepsilon$ |

网络分解把“如何调度局部计算以避免冲突”抽象成一个独立的图划分问题，是连接随机化与确定性、连接着色与一般局部问题的枢纽。
