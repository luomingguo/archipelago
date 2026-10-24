---
title: '近似算法 I：贪心覆盖、拟阵次模与动态规划 FPTAS (Approximation Algorithms I)'
type: lecture
lecture: 21
tags: [approximation-algorithms, fptas, greedy-approximation, submodular-maximization]
status: complete
---

# Lec 21 近似算法 I：贪心覆盖、拟阵次模与动态规划 FPTAS (Approximation Algorithms I)

> MIT 15.083 / 6.859J 整数规划与组合优化 · 讲义 21 · 授课教师：Prof. Dimitris Bertsimas

## TL;DR

- 近似算法（Approximation Algorithms）以可证明的多项式时间最坏情况近似比攻克 NP 难关。
- 贪心集合覆盖算法证明了最坏保证比恰好等于调和级数：$\alpha = H_n = \ln n + \mathcal{O}(1)$。
- 动态规划值域翻转加截断缩放铸就了 0-1 背包问题的完全多项式时间近似方案（FPTAS）。

## 1. 战胜 NP-hard 的第二条道路：近似算法

在第 2 讲中，计算复杂度理论确立了：除非 $\mathcal{P} = \mathcal{NP}$，否则任何算法都不可能在多项式时间内精确求解 NP-hard 优化大题。
面对这一铁律，运筹科学家开辟了一条全新的康庄大道——**近似算法（Approximation Algorithms）**：

**我们放弃对“绝对精确最优解”的执念，但绝对不放弃对“算法效率与理论质量”的最高追求！**
我们要求算法必须满足双重铁律：
1. **运算时间必须是严格的多项式时间（Polynomial-time）**；
2. **输出的近似解，其目标函数值与不可达的理论宇宙最优解之比，必须拥有绝对数学证明的最坏情况近似比（Approximation Ratio）！**

::: definition 近似比与 $\alpha$-近似算法
对于极小化问题（假设目标值非负），多项式算法 $\mathcal{A}$ 输出的解为 $x$，理论最优解为 $x^*$。若对所有可能的输入实例，均严格满足：
$$\frac{\operatorname{Cost}(x)}{\operatorname{Cost}(x^*)} \le \alpha \quad (\alpha \ge 1)$$
则称算法 $\mathcal{A}$ 是一个 **$\alpha$-近似算法（$\alpha$-Approximation Algorithm）**。对于极大化问题，比值定义为 $\frac{\operatorname{Cost}(x)}{\operatorname{Cost}(x^*)} \ge \alpha$（$\alpha \in (0, 1]$）。
:::

```mermaid
flowchart TD
    subgraph ApproxSpectrum [近似算法理论阶层光谱]
        FPTAS[FPTAS: 完全多项式时间近似方案 (1 + epsilon) 最强王冠] --> PTAS[PTAS: 多项式时间近似方案 O(n^f(1/epsilon))]
        PTAS --> ConstApprox[常数级近似比 Constant: 例如 2-近似, 0.878-近似]
        ConstApprox --> LogApprox[对数级近似比: 例如集合覆盖 ln n]
        LogApprox --> Inapprox[不可近似性定理 Inapproximability: 强行证明超越该界即 P=NP]
    end
```

## 2. 经典分析范例：贪心集合覆盖算法的对数保证

考虑经典的 NP-hard **加权集合覆盖问题（Set Covering Problem）**：
全集为 $U = \{1, \dots, m\}$，候选子集族 $\mathcal{S} = \{S_1, \dots, S_k\}$，每个子集成本为 $c(S)$。
贪心策略极其直观：**在每一步，挑选那个“单位新覆盖元素的边际成本（Cost per newly covered element）”最低的子集！**
$$S^* = \arg\min_{S \in \mathcal{S}} \frac{c(S)}{|S \setminus U_{\text{covered}}|}$$

乔瓦茨（Václav Chvátal）与洛瓦兹（László Lovász）在 1970 年代给出了严谨的代数分析证明：

::: theorem 贪心集合覆盖近似比定理 (Chvátal, 1979)
设全集中最大子集的元素个数为 $d = \max |S_j|$。
贪心集合覆盖算法的近似比**严格保证为调和级数（Harmonic Number）**：
$$\frac{\text{Cost}(\text{Greedy})}{\text{Cost}(\text{OPT})} \le H(d) = \sum_{i=1}^d \frac{1}{i} \le \ln(d) + 1$$
:::

证明利用了巧妙的“费用分摊（Cost-sharing）”思想：将选取的子集成本均摊到每一个新覆盖的元素头上，构造出对偶可行解，借助弱对偶性立即完成了调和级数积分夹逼！
后续理论证明：在 $\mathcal{P} \ne \mathcal{NP}$ 假说下，**$(1 - o(1)) \ln n$ 是任何多项式算法逼近集合覆盖的数学绝对极限！** 贪心算法在几十年前就已经站在了理论的极点之上。

## 3. 近似算法的最高圣杯：FPTAS 与背包问题

如果一个算法不仅能逼近最优解，而且允许用户**任意指定误差容忍度 $\varepsilon > 0$**，算法保证在多项式时间内输出 $(1 + \varepsilon)$ 倍理论最优解，这被称为**完全多项式时间近似方案（FPTAS）**！

::: definition 完全多项式时间近似方案 (FPTAS)
算法族 $\{\mathcal{A}_\varepsilon\}$ 称为 FPTAS，若对于任意给定的相对误差 $\varepsilon > 0$，算法输出的解满足误差在 $\varepsilon$ 以内，且其运行时间关于**输入规模 $n$ 和误差倒数 $1/\varepsilon$ 同时呈现多项式依赖**：
$$\text{Time} = \mathcal{O}\left( \operatorname{poly}(n, \; 1/\varepsilon) \right)$$
:::

经典 0-1 背包问题：$\max \sum v_j x_j$ s.t. $\sum w_j x_j \le W$。
传统基于重量的动态规划时间为 $\mathcal{O}(n W)$（伪多项式时间，当 $W$ 很大时爆炸）。
卡普（Karp）与伊巴拉（Ibarra）在 1975 年设计了经典的 FPTAS：
1. **值域翻转动态规划**：定义 $DP(i, v)$ 为前 $i$ 个物品达到总价值 $v$ 所需的最小重量。时间复杂度为 $\mathcal{O}(n \cdot V_{\max})$（其中 $V_{\max} = \sum v_j$）；
2. **价值缩放与舍入截断（Scaling & Rounding）**：设定缩放因子 $K = \frac{\varepsilon v_{\max}}{n}$。
   定义压缩后的离散整数价值：
   $$\tilde{v}_j = \left\lfloor \frac{v_j}{K} \right\rfloor$$
3. 在压缩价值系统上运行值域动态规划：由于最大压缩价值仅为 $\tilde{V}_{\max} = n^2 / \varepsilon$，**动态规划的运行时间被严格强制压缩为多项式阶 $\mathcal{O}(n^3 / \varepsilon)$！**

由于每个物品向下取整造成的价值损失绝不超过 $K$，总损失不超过 $n K = \varepsilon v_{\max} \le \varepsilon \cdot \text{OPT}$！
算法完美交出 $(1 - \varepsilon) \cdot \text{OPT}$ 的答案！

::: insight 近似算法是实用主义理性的胜利
近似算法向我们展示了理论科学家在面对不可逾越的理论深渊时，所展现出的无与伦比的优雅。
我们没有在 NP 难度的铁墙上撞得粉身碎骨，也没有退化为碰运气的经验启发式。
我们用严格的数学证明，在有限多项式算力与可控的误差区间之间签下了一份白纸黑字的契约。这是人类在有限宇宙中调和理想与现实的最高智慧。
:::
