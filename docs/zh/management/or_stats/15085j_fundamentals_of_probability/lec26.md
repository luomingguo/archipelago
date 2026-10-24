---
title: '鞅论 II：Doob 可选停时定理与鞅收敛全景 (Martingales II: Optional Stopping)'
type: lecture
lecture: 26
tags: [optional-stopping-theorem, martingale-convergence, doob-inequality, polya-urn]
status: complete
---

# Lec 26 鞅论 II：Doob 可选停时定理与鞅收敛全景 (Martingales II: Optional Stopping)

> MIT 15.085J / 6.436J 概率论基础 · 讲义 26 · 授课教师：Prof. John Tsitsiklis / Devavrat Shah

## TL;DR

- 杜布可选停时定理（Doob's Optional Stopping）证明了任何合法的离场策略绝无法战胜公平博弈。
- 杜布最大值不等式（Doob's Maximal Inequality）以终点时刻能量牢牢锁死整条样本轨道的极值。
- 几乎处处鞅收敛定理（Martingale Convergence Theorem）为非同分布系统提供了最强大的极限收敛铁律。

## 1. 赌徒谬误的终极数学死刑：杜布可选停时定理

自概率论诞生之日起，全世界无数赌徒发明了成千上万种自以为聪明的离场策略（例如著名的加倍下注翻倍法 Martingale Betting System）：只要输了就下注翻倍，只要赢一次立即收手离场。赌徒们狂热地坚信：通过设计一套精巧的停时策略 $\tau$，一定能把一个公平博弈（期望收益为 0）扭转成一个必胜系统！

约瑟夫·杜布在 1953 年以无情的严密公理宣判了一切离场策略的死刑——**杜布可选停时定理（Doob's Optional Stopping Theorem, OST）**：

::: theorem 杜布可选停时定理 (Doob's Optional Stopping Theorem)
设 $\{X_n, \mathcal{F}_n\}$ 为鞅，$\tau$ 为停时。
若满足以下三大约束条件之一：
1. 停时有界：存在确定常数 $M < \infty$，使得 $\mathbb{P}(\tau \le M) = 1$；
2. 停时几乎处处有限（$\mathbb{P}(\tau < \infty) = 1$），且在停止时刻前鞅过程一致有界：$|X_{n \wedge \tau}| \le c < \infty$；
3. 停时期望有限（$\mathbb{E}[\tau] < \infty$），且单步增量有界：$\mathbb{E}[|X_{n+1} - X_n| \mid \mathcal{F}_n] \le c$。
则：**停止时刻的随机变量 $X_\tau$ 的数学期望，严格等于初始时刻的起始期望值！**
$$\mathbb{E}[X_\tau] = \mathbb{E}[X_0]$$
:::

可选停时定理在数学上给出了绝对确定性的冷酷宣判：
**在公平的博弈中，没有任何人类能够通过选择何时离场来改变命运的期望！不论你的停时算法多么复杂，你的最终期望收益永远严格等于零！**

```mermaid
flowchart TD
    subgraph MartingaleCrownJewels [杜布鞅论三大皇冠定理]
        OST[1. 杜布可选停时定理 OST: 任何离场策略 E[X_tau] = E[X_0] 绝无法攻破公平博弈]
        MaxIneq[2. 杜布最大值不等式: 轨道峰值概率被终点能量严格压制 P(max X_k >= lambda) <= E[X_n]/lambda]
        MCT[3. 几乎处处鞅收敛定理: 只要在 L^1 有界 sup E[|X_n|] < 无穷, 样本轨道必以概率 1 收敛至 X_infty!]
    end
```

## 2. 轨迹极值的绝对统治：杜布最大值不等式（Doob's Maximal Inequality）

在工程控制与高频金融中，我们不仅关心系统在终端时刻的值，更关心系统在整个运行周期中的**历史最大回撤与峰值破坏（Path Supremum）**：
$$X_n^* = \max_{0 \le k \le n} X_k$$

杜布证明了马尔可夫不等式在随机过程轨道层面的惊人升级：

::: theorem 杜布最大值不等式 (Doob's Maximal Inequality)
设 $\{X_k\}_{k=0}^n$ 为非负下鞅（例如 $X_k = |M_k|$，其中 $M$ 为任意鞅）。
则对于任意阈值 $\lambda > 0$：
$$\mathbb{P}\left( \max_{0 \le k \le n} X_k \ge \lambda \right) \le \frac{\mathbb{E}[X_n]}{\lambda}$$
进一步，在 $L^p$ 范数下（$p > 1$），历史最大值的整体能量被终端时刻严格夹逼（杜布 $L^p$ 不等式）：
$$\mathbb{E}\left[ \left( \max_{0 \le k \le n} X_k \right)^p \right] \le \left( \frac{p}{p - 1} \right)^p \mathbb{E}[X_n^p]$$
:::

这真是一个神迹般的定理：**要控制一整条随机曲线在过去成千上万步中的最高峰值，你根本不需要去监控整条轨迹，你只需要去看它在终点时刻的单点能量 $\mathbb{E}[X_n]$！**

## 3. 终局收敛：几乎处处鞅收敛定理（Martingale Convergence Theorem）

作为 15.085J 的终章高潮，我们将见证概率论最强悍的极限收敛机器——**几乎处处鞅收敛定理**。

传统的强大数定律要求变量必须严格独立同分布（i.i.d.）；
而鞅收敛定理**彻底粉碎了一切独立性要求！** 它允许变量之间存在极其强烈的非线性历史耦合！

::: theorem 杜布几乎处处鞅收敛定理 (Doob's Forward Convergence Theorem)
设 $\{X_n, \mathcal{F}_n\}$ 为下鞅或鞅。
只要满足**在 $L^1$ 范数下一致有界（不需要一致可积，仅需有界）**：
$$\sup_{n \ge 0} \mathbb{E}[|X_n|] < \infty$$
则：**随机变量序列 $X_n$ 必然以概率 1（几乎处处）收敛到一个有限的极限随机变量 $X_\infty$！**
$$X_n \xrightarrow{a.s.} X_\infty < \infty$$
:::

证明的核心基于极其优美的**穿越不等式（Upcrossing Inequality）**：杜布证明了在任意闭区间 $[a, b]$ 内，样本轨道向上穿越区间的次数期望被能量上限牢牢锁死为有限实数。既然无法无限次上下震荡，轨道只能收敛！

::: example 波利亚罐模型（Pólya's Urn）的极限分布
罐中有红球和黑球各 1 个。每次随机摸出 1 球，看清颜色后放回，并额外放入 1 个同色球（正反馈滚雪球效应，完全破坏独立性！）。
设第 $n$ 次摸球后红球的比例为 $X_n$。
极易验证：$\{X_n\}$ 是一个严格处于 $[0, 1]$ 之间的有界鞅！
根据鞅收敛定理，$X_n$ **必然以概率 1 严格收敛于某个极限变量 $X_\infty$**！
更精妙的计算表明，$X_\infty$ 在 $(0, 1)$ 上服从标准均匀分布！每一个平行宇宙中的观察者，都会看到系统红球比例最终稳定为一个确定的百分比，但不同宇宙的稳态数值在 0 到 1 之间完全随机展开。
:::

::: insight 测度论概率的终曲与星辰大海
回顾整个 15.085J 的壮丽航程：
我们从非可测集的深渊起步，以 $\sigma$-代数筑起理性的堤坝；我们见证了勒贝格积分对病态函数的降维包容，用控制收敛与特征函数穿透了中心极限定理的高斯涌现；最终，我们在希尔伯特空间的投影引力下构筑起鞅论的大厦，以可选停时与鞅收敛定格了动态随机系统的终极命运。
概率论绝不是与不确定性妥协的权宜之计，它是人类用极致严密的纯数学逻辑，在无限混沌的迷雾中，为大自然的守恒律谱写的最庄严的赞歌。
:::
