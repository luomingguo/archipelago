---
title: '离散随机变量、指示函数与期望的级数定义 (Discrete Random Variables & Expectations)'
type: lecture
lecture: 5
tags: [discrete-random-variables, expectation, indicator-functions, change-of-variables]
status: complete
---

# Lec 5 离散随机变量、指示函数与期望的级数定义 (Discrete Random Variables & Expectations)

> MIT 15.085J / 6.436J 概率论基础 · 讲义 5 · 授课教师：Prof. John Tsitsiklis / Devavrat Shah

## TL;DR

- 离散随机变量的值域为可数点集，其诱导测度可被概率质量函数（PMF）完全描述。
- 指示函数（Indicator Function）分解将抽象期望无缝转化为线性代数投影。
- 期望必须要求绝对收敛（$\mathbb{E}[|X|] < \infty$），防止级数重排导致无穷抵消的代数陷阱。

## 1. 离散随机变量与概率质量函数（PMF）

在第 4 讲建立的广义可测映射框架下，最直观的一类随机变量是**离散随机变量（Discrete Random Variable）**：
其值域 $\operatorname{Range}(X) = X(\Omega) = \{x_1, x_2, x_3, \dots\} \subset \mathbb{R}$ 是一个**至多可数集合（At most countable）**。

定义其**概率质量函数（Probability Mass Function, PMF）**：
$$p_X(x_k) = \mathbb{P}(X = x_k) = \mathbb{P}\left( \{\omega \in \Omega \mid X(\omega) = x_k\} \right)$$
满足规范化：$p_X(x_k) \ge 0$ 且 $\sum_{k} p_X(x_k) = 1$。

离散随机变量使得抽象测度空间中的积分运算，完全降解为了人类最熟悉的离散加法与数列级数求和。

```mermaid
flowchart LR
    A[样本空间分割: A_k = {omega | X(omega) = x_k}] --> B[指示函数分解: X = sum x_k * I_A_k]
    B --> C[期望线性算子: E[X] = sum x_k * E[I_A_k]]
    C --> D[离散质量求和: E[X] = sum x_k * p_X(x_k)]
```

## 2. 积木块原子：指示函数（Indicator Function）的力量

在分析学与高等概率论中，最强大、最基础的微观原子工具是**事件的指示函数（Indicator Function）**：

::: definition 指示函数 (Indicator Function)
对于任意事件 $A \in \mathcal{F}$，定义指示函数 $\mathbb{I}_A: \Omega \to \{0, 1\}$：
$$\mathbb{I}_A(\omega) = \begin{cases} 1, & \text{若 } \omega \in A \\ 0, & \text{若 } \omega \notin A \end{cases}$$
:::

指示函数展现出一系列极其神奇的代数与微积分全纯特性：
1. **乘法即交集**：$\mathbb{I}_{A \cap B} = \mathbb{I}_A \cdot \mathbb{I}_B$；
2. **反向即补集**：$\mathbb{I}_{A^c} = 1 - \mathbb{I}_A$；
3. **互斥即加法**：若 $A \cap B = \emptyset$，则 $\mathbb{I}_{A \cup B} = \mathbb{I}_A + \mathbb{I}_B$；
4. **期望即概率**：$\mathbb{E}[\mathbb{I}_A] = 1 \cdot \mathbb{P}(A) + 0 \cdot \mathbb{P}(A^c) = \mathbb{P}(A)$！

任何离散随机变量都可以被唯一地表示为指示函数的线性组合（简单函数分解）：
$$X(\omega) = \sum_{k=1}^\infty x_k \mathbb{I}_{A_k}(\omega), \quad \text{其中 } A_k = \{\omega \mid X(\omega) = x_k\}$$

## 3. 期望的严格定义与绝对收敛陷阱

::: definition 离散随机变量的数学期望 (Expectation)
设 $X$ 为离散随机变量。若无穷级数**绝对收敛**：
$$\sum_{k=1}^\infty |x_k| p_X(x_k) < \infty$$
则定义 $X$ 的**数学期望（Expectation / Expected Value）**为：
$$\mathbb{E}[X] = \sum_{k=1}^\infty x_k p_X(x_k)$$
若正部级数收敛而负部发散，则 $\mathbb{E}[X] = -\infty$；反之亦然。若正负部级数同时发散到无穷，则**期望不存在（Undefined）**！
:::

::: pitfall 为什么必须要求绝对收敛？柯西反例
初学者极易忽视“绝对收敛”这四个字。
考察著名的**圣彼得堡悖论**或**柯西分布（Cauchy Distribution）**的离散对等物：
设离散变量 $X$ 取偶数 $x_k = (-1)^k \frac{2^k}{k}$，或考虑 $p_X(k) = \frac{C}{k^2}$，取值 $x_k = (-1)^k k$。
此时条件级数 $\sum (-1)^k \frac{1}{k}$ 虽然按交错级数审敛法是收敛的（等于 $-\ln 2$）；
但根据黎曼级数重排定理（Riemann Series Theorem）：**任意非绝对收敛的条件级数，只要任意调换求和次序，可以让求和结果变成任意指定的实数、或者直接发散到正负无穷！**
由于样本空间中的事件根本没有先天的“自然排列顺序”（我们完全可以先数正数、再数负数），如果允许条件收敛进入期望定义，同同一个随机变量的期望值会随着计算机遍历循环的顺序改变而任意漂移！绝对收敛是保证期望值物理客观性的唯一底线。
:::

::: theorem 无意识统计学家法则 (Law of the Unconscious Statistician, LOTUS)
设 $Y = g(X)$ 为随机变量的变换。计算 $\mathbb{E}[Y]$ **无需先大费周折求出 $Y$ 自身的复杂分布**，只需通过原变量分布直接积分：
$$\mathbb{E}[g(X)] = \sum_{k=1}^\infty g(x_k) p_X(x_k)$$
:::

::: insight 期望作为无限维度的质心投影
数学期望是概率论向物理学质心概念的最高致敬。
指示函数把样本空间的每一个子块变成了单位质量的质元；而期望将不可数抽象空间中无数随机路径的复杂摇摆，投影成实数轴上唯一的引力中心。
坚持绝对收敛的刚性，就是在面对无限的诱惑时，恪守理性大厦的稳固。这是应用数学家从大一高等数学走向研究生高级测度论的成年礼。
:::
