---
title: '条件概率、全概率公式与独立性事件系统 (Conditioning & Independence)'
type: lecture
lecture: 3
tags: [conditional-probability, independence, bayes-theorem, zero-one-law]
status: complete
---

# Lec 3 条件概率、全概率公式与独立性事件系统 (Conditioning & Independence)

> MIT 15.085J / 6.436J 概率论基础 · 讲义 3 · 授课教师：Prof. John Tsitsiklis / Devavrat Shah

## TL;DR

- 条件概率 $\mathbb{P}(A \mid B)$ 将先验样本空间收缩至证据子空间 $B$ 上进行重新归一化。
- 独立性并非互斥，而是代数乘积测度分解：$\mathbb{P}(A \cap B) = \mathbb{P}(A) \mathbb{P}(B)$。
- 柯尔莫哥洛夫零一律（Zero-One Law）证明尾事件的发生概率只能非黑即白：必为 0 或 1。

## 1. 证据驱动的测度重标定：条件概率公理

在真实世界中，决策者几乎永远不可能在纯粹无信息的先验世界中行动。每当观测到一个新的事实、信号或传感器读数（记为事件 $B$，且 $\mathbb{P}(B) > 0$），整个随机系统的样本空间就发生了结构性坍缩。

::: definition 条件概率 (Conditional Probability)
设 $(\Omega, \mathcal{F}, \mathbb{P})$ 为概率空间。对于给定条件事件 $B \in \mathcal{F}$（满足 $\mathbb{P}(B) > 0$），任意事件 $A \in \mathcal{F}$ 在 $B$ 发生之下的**条件概率**定义为：
$$\mathbb{P}(A \mid B) = \frac{\mathbb{P}(A \cap B)}{\mathbb{P}(B)}$$
:::

仔细考察这个定义式在测度论中的几何实质：
函数 $\mathbb{Q}(A) = \mathbb{P}(A \mid B)$ **自身就是一个完整合法、严格满足柯尔莫哥洛夫三大公理的全新概率测度**！
它把原本全集 $\Omega$ 上的概率测度，通过除以 $\mathbb{P}(B)$ 正规化，完全“投影剪裁”并浓缩到了子集 $B$ 的微观宇宙之中。

```mermaid
flowchart TD
    subgraph ConditioningMechanism [条件概率的样本空间坍缩]
        Omega[先验样本空间 Omega: 总测度为 1] --> Obs[观察到事件 B 发生: B 成为新的有效全集]
        Obs --> Trace[裁剪非 B 区域: 所有 B 补集测度归零]
        Trace --> Renorm[除以 P(B) 重新归一化: P(B | B) = 1]
    end
```

## 2. 全概率法则与贝叶斯定理（Bayes' Theorem）

::: definition 样本空间的可测划分 (Partition)
序列 $B_1, B_2, \dots \in \mathcal{F}$ 称为样本空间 $\Omega$ 的一个可测划分，若满足：
1. 两两互斥：$B_i \cap B_j = \emptyset, \; \forall i \ne j$；
2. 完整覆盖：$\bigcup_{i=1}^\infty B_i = \Omega$；
3. 每个子块非平凡：$\mathbb{P}(B_i) > 0$。
:::

::: theorem 全概率公式与贝叶斯逆推公式
设 $\{B_i\}$ 为样本空间划分。对于任意目标事件 $A$：
1. **全概率公式（Law of Total Probability）**：
$$\mathbb{P}(A) = \sum_{i=1}^\infty \mathbb{P}(A \cap B_i) = \sum_{i=1}^\infty \mathbb{P}(B_i) \mathbb{P}(A \mid B_i)$$
2. **贝叶斯定理（Bayes' Rule）**：
$$\mathbb{P}(B_k \mid A) = \frac{\mathbb{P}(B_k) \mathbb{P}(A \mid B_k)}{\sum_{i=1}^\infty \mathbb{P}(B_i) \mathbb{P}(A \mid B_i)}$$
:::

贝叶斯公式揭示了人类由果推因的认知本质：$\mathbb{P}(B_k)$ 是先验信念（Prior），$\mathbb{P}(A \mid B_k)$ 是物理证据似然（Likelihood），而分母是边缘全概率配分函数，乘积归一化后输出更新后的后验概率（Posterior）。

## 3. 统计独立性与柯尔莫哥洛夫零一律（Zero-One Law）

很多初学者容易将“事件独立”与“事件互斥”混为一谈。
互斥（$A \cap B = \emptyset$）是最强烈的**负相关**（一旦 $A$ 发生，$B$ 发生的概率直接归零！）；
而独立意味着“信息零增益”：即便得知 $B$ 发生，对 $A$ 的概率评估完全不产生任何扰动（$\mathbb{P}(A \mid B) = \mathbb{P}(A)$）。

::: definition 事件独立性与集合族独立性
1. **两事件独立**：若 $\mathbb{P}(A \cap B) = \mathbb{P}(A) \mathbb{P}(B)$；
2. **事件族相互独立**：事件集合族 $\{A_i\}_{i \in I}$ 称为相互独立，若对于该集合族的**任意有限子集** $\{i_1, \dots, i_k\}$，联合概率均满足代数连乘积分解：
$$\mathbb{P}\left( \bigcap_{j=1}^k A_{i_j} \right) = \prod_{j=1}^k \mathbb{P}(A_{i_j})$$
:::

当事件族延伸至无穷序列时，引出了概率论中最不可思议的深刻定理——**柯尔莫哥洛夫零一律（Kolmogorov's Zero-One Law）**：

::: definition 尾 $\sigma$-代数 (Tail $\sigma$-Algebra)
设 $A_1, A_2, A_3, \dots$ 为独立事件序列。定义第 $n$ 步之后的剩余信息 $\sigma$-代数：
$$\mathcal{T}_n = \sigma(A_n, A_{n+1}, A_{n+2}, \dots)$$
定义整个序列的**尾 $\sigma$-代数（Tail $\sigma$-Algebra）**为所有这些未来信息的交集：
$$\mathcal{T} = \bigcap_{n=1}^\infty \mathcal{T}_n$$
尾事件是那些“不受任何有限步历史事件影响”的渐近宏观事件（例如：无穷次抛硬币中正面朝上的频率极限是否存在、随机游走是否无穷次返回原点、无穷级数是否收敛）。
:::

::: theorem 柯尔莫哥洛夫零一律 (Kolmogorov's 0-1 Law)
设 $A_1, A_2, \dots$ 为相互独立事件序列，$\mathcal{T}$ 为其尾 $\sigma$-代数。
则对于**任意尾事件 $E \in \mathcal{T}$**，其发生概率**只能是 0 或者 1**！绝无任何中间值：
$$\mathbb{P}(E) \in \{0, 1\}$$
:::

**证明的绝妙构思**：
因为 $E \in \mathcal{T} \subset \mathcal{T}_{n+1}$，所以事件 $E$ 与有限历史 $\sigma(A_1, \dots, A_n)$ 严格独立！
既然对任意 $n$ 都独立，根据测度延拓，事件 $E$ 必然与整个序列生成的全空间 $\sigma(A_1, A_2, \dots)$ 独立！
然而，事件 $E$ 自身就属于该 $\sigma$-代数！
因此：**事件 $E$ 必须与自己独立**！
$$\mathbb{P}(E \cap E) = \mathbb{P}(E) \cdot \mathbb{P}(E) \iff \mathbb{P}(E) = \mathbb{P}(E)^2 \implies \mathbb{P}(E) = 0 \text{ 或 } 1$$

::: insight 宏观确定性脱胎于微观随机性
柯尔莫哥洛夫零一律具有超越数学本身的哲学震撼力。
在微观层面，每一次抛硬币充满混沌、不可预测；
然而，只要这些试验保持统计独立，任何描述长期命运的终极宏观问题（级数是否收敛、物理系统是否逃逸到无穷），在宇宙诞生之初就已经被数学公理注定：它要么以 $100\%$ 的概率必然发生，要么以 $0\%$ 的概率绝无可能发生。混沌在无穷的尽头凝结为了绝对的确定性。
:::
