---
title: "期望的应用与方差"
type: lecture
lecture: 23
tags: [expectation, variance, union-bound, independence]
status: complete
source: https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/resources/61200-sp24-lecture23-2024may09_mp4/
---
# Lec 23 期望的应用与方差

> 资料依据：[课程视频与 transcript](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/resources/61200-sp24-lecture23-2024may09_mp4/) · 官方未提供本讲 Lecture notes

## TL;DR

- 联合界用期望上界“至少一个事件发生”的概率；当事件互独立时，反向的指数下界说明期望较大时至少一个事件几乎必然发生。
- 独立随机变量满足乘积的期望等于期望的乘积，但期望不与除法交换；先取比值再平均可以得到误导性结论。
- 方差是与均值偏差平方的期望，度量分布的离散程度；独立变量之和的方差可相加，这解释了分散独立风险为何能降低波动。

## 用指示变量计数事件

设 $E_1,\ldots,E_n$ 是同一样本空间上的事件，$N$ 表示实际发生的事件数。对每个事件定义指示变量

$$
I_i=\begin{cases}
1,&E_i\text{ 发生},\\
0,&E_i\text{ 不发生}.
\end{cases}
$$

则 $N=\sum_{i=1}^n I_i$。由期望的线性，不论这些事件是否独立，都有

$$
\mathbb E[N]
=\sum_{i=1}^n\mathbb E[I_i]
=\sum_{i=1}^n\Pr[E_i].
$$

### 联合界

“至少一个事件发生”等价于 $N\ge 1$。因为在该事件上 $N\ge 1$，所以

$$
\Pr\!\left[\bigcup_{i=1}^n E_i\right]
=\Pr[N\ge 1]
\le \mathbb E[N]
=\sum_{i=1}^n\Pr[E_i].
$$

::: theorem 联合界（union bound）
任意事件 $E_1,\ldots,E_n$ 都满足

$$
\Pr\!\left[\bigcup_{i=1}^n E_i\right]
\le \sum_{i=1}^n\Pr[E_i].
$$

这个结论不需要独立性，但右边可能大于 1，因而有时很松。
:::

## 独立事件的反向界

若 $E_1,\ldots,E_n$ 互独立，则它们的补集也互独立：

$$
\Pr[N=0]
=\prod_{i=1}^n\bigl(1-\Pr[E_i]\bigr)
\le \prod_{i=1}^n e^{-\Pr[E_i]}
=e^{-\sum_i\Pr[E_i]}
=e^{-\mathbb E[N]}.
$$

因此

$$
\Pr[N\ge1]\ge 1-e^{-\mathbb E[N]}.
$$

讲师把这个结论称为“Murphy 定律”：当失败模式互独立且失败数的期望很大时，至少一次失败的概率非常接近 1。

::: pitfall
这个下界依赖互独立。在“懒苏珊转盘”手机例子中，所有人是否拿回手机完全相关：要么全对，要么全错。每个人拿对的概率虽是 $1/n$，却不能使用上述独立下界。
:::

## 期望与乘法

::: theorem 独立随机变量的乘积期望
若 $X$ 与 $Y$ 独立，则

$$
\mathbb E[XY]=\mathbb E[X]\mathbb E[Y].
$$
:::

证明思路是按 $X=x,Y=y$ 对期望求和，再用独立性把联合概率分解为两个边缘概率。例如两枚独立公平六面骰子 $D_1,D_2$ 满足

$$
\mathbb E[D_1D_2]
=\mathbb E[D_1]\mathbb E[D_2]
=3.5^2
=12.25.
$$

但 $D_1$ 并不与自身独立，因此

$$
\mathbb E[D_1^2]=\frac{1^2+2^2+\cdots+6^2}{6}=\frac{91}{6}\ne 12.25.
$$

### 不要交换期望与除法

一般而言，

$$
\mathbb E\!\left[\frac1X\right]\ne\frac1{\mathbb E[X]}.
$$

比较两个系统的相对性能时，“先对各工作负载求比值再取平均”可能在交换分子分母后仍宣称对方更好。如果问题是比较平均运行时间，应先分别计算期望，再比较两个期望。

## 方差与标准差

::: definition 方差
随机变量 $X$ 的方差为

$$
\operatorname{Var}(X)
=\mathbb E\!\left[(X-\mathbb E[X])^2\right].
$$

标准差为 $\sigma(X)=\sqrt{\operatorname{Var}(X)}$，它与 $X$ 使用相同量纲。
:::

方差通过平方避免正负偏差相互抵消，并给较大的偏离更高权重。它有一个常用等价公式：

$$
\operatorname{Var}(X)=\mathbb E[X^2]-\mathbb E[X]^2.
$$

基本性质包括：

- 平移不改变方差：$\operatorname{Var}(X+c)=\operatorname{Var}(X)$；
- 缩放会平方地缩放方差：$\operatorname{Var}(cX)=c^2\operatorname{Var}(X)$；
- 若 $X,Y$ 独立，则 $\operatorname{Var}(X+Y)=\operatorname{Var}(X)+\operatorname{Var}(Y)$。

对成功概率为 $p$ 的 Bernoulli 随机变量 $H$，因 $H^2=H$，

$$
\operatorname{Var}(H)=p-p^2=p(1-p).
$$

因此，$n$ 次独立抛硬币的正面数 $S=\sum_i H_i$ 满足

$$
\mathbb E[S]=np,
\qquad
\operatorname{Var}(S)=np(1-p).
$$

## 分散投资的数学前提

设总资金为 $M$，平均分到 $k$ 个互相独立、方差为 1 的投资 $S_1,\ldots,S_k$ 中。总收益的方差为

$$
\operatorname{Var}\!\left(\sum_{i=1}^k\frac{M}{k}S_i\right)
=\sum_{i=1}^k\frac{M^2}{k^2}\operatorname{Var}(S_i)
=\frac{M^2}{k}.
$$

标准差为 $M/\sqrt{k}$，随独立投资数增加而下降。

::: pitfall
降低风险的结论依赖独立性。当资产受同一市场因素驱动时，协方差不为零，方差不能简单相加，分散化的收益也会减弱。
:::

## 我的理解

::: insight
期望的线性不需独立，而乘积期望和方差可加性需要独立条件。记住这一分界比背公式更重要：加法中的交叉项可被期望线性直接处理，乘法和方差中的交叉项则必须靠独立性消去。
:::
