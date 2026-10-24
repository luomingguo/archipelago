---
title: '弱大数定律：契比雪夫不等式与样本均值弱收敛 (Laws of Large Numbers I: WLLN)'
type: lecture
lecture: 17
tags: [weak-law-of-large-numbers, wlln, chebyshev-inequality, sample-mean]
status: complete
---

# Lec 17 弱大数定律：契比雪夫不等式与样本均值弱收敛 (Laws of Large Numbers I: WLLN)

> MIT 15.085J / 6.436J 概率论基础 · 讲义 17 · 授课教师：Prof. John Tsitsiklis / Devavrat Shah

## TL;DR

- 契比雪夫不等式（Chebyshev's Inequality）利用二阶矩给出了与分布无关的方差界。
- 弱大数定律（WLLN）证明独立同分布序列的样本均值依概率收敛于数学期望（$\bar{X}_n \xrightarrow{P} \mu$）。
- 辛钦（Khinchin）弱大数定律彻底剥离了有限方差假设，仅需一阶可积即可确立收敛。

## 1. 经验频率通向真理之路：大数定律的物理动机

从 18 世纪雅各布·伯努利（Jacob Bernoulli）在《猜度术》中苦苦思索 20 年起，人类就直觉地坚信一条经验铁律：
**如果一次试验被独立重复成千上万次，那么事件发生的经验频率必然会无限逼近其真实的理论概率；样本的算术平均值必然会无限逼近其理论期望！**

设 $X_1, X_2, X_3, \dots$ 为**独立同分布（Independent and Identically Distributed, i.i.d.）**的随机变量序列，期望为 $\mathbb{E}[X_i] = \mu$。
定义前 $n$ 次观测的**样本均值（Sample Mean）**：
$$\bar{X}_n = \frac{1}{n} \sum_{i=1}^n X_i$$

这一命题在数学分析上究竟意味着哪一种收敛？
本讲我们将见证大数定律的第一座丰碑——**弱大数定律（Weak Law of Large Numbers, WLLN）**。

```mermaid
flowchart LR
    subgraph WLLN_Mechanism [弱大数定律收敛机制]
        iid[独立同分布 i.i.d. 序列: 期望 mu, 方差 sigma^2] --> Mean[样本均值: X_bar_n = 1/n sum X_i]
        Mean --> VarCalc[方差以 1/n 几何衰减: Var(X_bar_n) = sigma^2 / n]
        VarCalc --> Chebyshev[代入契比雪夫不等式: P(|X_bar_n - mu| > epsilon) <= sigma^2 / (n * epsilon^2)]
        Chebyshev --> Limit[令 n -> 无穷: 误差概率绝对归零! X_bar_n 依概率收敛于 mu]
    end
```

## 2. 契比雪夫不等式与有限方差下的 WLLN 极速证明

为了度量样本均值偏离期望的概率，俄国数学家帕夫努蒂·契比雪夫（Pafnuty Chebyshev）在 1867 年给出了无懈可击的纯代数界：

::: theorem 马尔可夫与契比雪夫不等式
1. **马尔可夫不等式（Markov's Inequality）**：若非负随机变量 $Y \ge 0$，对任意常数 $a > 0$：
$$\mathbb{P}(Y \ge a) \le \frac{\mathbb{E}[Y]}{a}$$
2. **契比雪夫不等式（Chebyshev's Inequality）**：设随机变量 $Z$ 满足有限方差 $\operatorname{Var}(Z) < \infty$。令 $Y = (Z - \mathbb{E}[Z])^2, a = \varepsilon^2$，代入马尔可夫不等式立即得出：
$$\mathbb{P}\left( |Z - \mathbb{E}[Z]| \ge \varepsilon \right) \le \frac{\operatorname{Var}(Z)}{\varepsilon^2}$$
:::

现在，将契比雪夫不等式直接应用于样本均值 $\bar{X}_n$！
由于变量相互独立：
1. 期望不变：$\mathbb{E}[\bar{X}_n] = \frac{1}{n} \sum_{i=1}^n \mathbb{E}[X_i] = \frac{n \mu}{n} = \mu$；
2. **方差被样本容量 $n$ 强力稀释**：
$$\operatorname{Var}(\bar{X}_n) = \operatorname{Var}\left( \frac{1}{n} \sum_{i=1}^n X_i \right) = \frac{1}{n^2} \sum_{i=1}^n \operatorname{Var}(X_i) = \frac{n \sigma^2}{n^2} = \frac{\sigma^2}{n}$$

将方差代入契比雪夫不等式：
$$\mathbb{P}\left( |\bar{X}_n - \mu| \ge \varepsilon \right) \le \frac{\operatorname{Var}(\bar{X}_n)}{\varepsilon^2} = \frac{\sigma^2}{n \varepsilon^2}$$

考察当样本容量趋向无穷大时的极限：
对于任意给定的正实数 $\varepsilon > 0$，只要让 $n \to \infty$：
$$\lim_{n \to \infty} \mathbb{P}\left( |\bar{X}_n - \mu| \ge \varepsilon \right) \le \lim_{n \to \infty} \frac{\sigma^2}{n \varepsilon^2} = 0$$

根据第 16 讲对收敛模式的严格定义，这无懈可击地证明了：**样本均值 $\bar{X}_n$ 严格依概率收敛于理论真值 $\mu$！**

## 3. 辛钦弱大数定律（Khinchin's WLLN）：彻底剥离方差假设

上述证明依赖二阶矩存在（$\sigma^2 < \infty$）。如果随机变量只有一阶期望有限、而方差无穷大（如某些重尾 Pareto 分布），弱大数定律是否依然坚挺？

前苏联数学家亚历山大·辛钦（Aleksandr Khinchin）利用第 15 讲的**特征函数**，给出了彻底免除方差假设的终极定理：

::: theorem 辛钦弱大数定律 (Khinchin's Weak Law)
设 $X_1, X_2, \dots$ 为独立同分布随机变量序列，**仅需满足一阶期望有限**（$\mathbb{E}[|X_i|] < \infty$，记 $\mathbb{E}[X_i] = \mu$），无需任何方差有限性假设！
则样本均值必然**依概率收敛于 $\mu$**：
$$\bar{X}_n = \frac{1}{n} \sum_{i=1}^n X_i \xrightarrow{P} \mu \quad (n \to \infty)$$
:::

**两行震撼证明**：
单个变量的特征函数在原点一阶泰勒展开为：$\varphi_X(t) = 1 + i \mu t + o(t)$。
样本均值的特征函数为：
$$\varphi_{\bar{X}_n}(t) = \mathbb{E}\left[ e^{i t \frac{\sum X_k}{n}} \right] = \left[ \varphi_X(t/n) \right]^n = \left( 1 + i \mu \frac{t}{n} + o(t/n) \right)^n \xrightarrow{n \to \infty} e^{i \mu t}$$
极限特征函数 $e^{i \mu t}$ 对应确定性常数 $\mu$ 的特征函数！
根据列维连续性定理，$\bar{X}_n \xrightarrow{d} \mu$；又因为收敛到常数时弱收敛等价于依概率收敛，辛钦弱大数定律彻底获证！

::: insight 独立性带来的方差除以 n 奇迹
弱大数定律是统计学全部合法性的终极基石。
它的灵魂全部寄托在方差公式分母上的那个 $n$ 里：$\operatorname{Var}(\bar{X}_n) = \sigma^2 / n$。
每一个独立的样本数据，都在为抵抗微观混沌贡献一份确定性的重力。
从民意民调抽样、保费精算平衡、到蒙特卡洛积分仿真，人类之所以能够用有限的数据洞穿隐藏在自然深处的客观常数，正是因为弱大数定律在时间轴上持续稀释着一切孤立的随机扰动。
:::
