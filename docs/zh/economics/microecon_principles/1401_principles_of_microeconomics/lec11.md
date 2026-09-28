---
title: 垄断（一）
type: lecture
lecture: 11
tags: [monopoly, marginal-revenue, lerner-index, market-power, monopoly-pricing]
status: complete
source: 'https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/resources/mit14_01_f23_lec11/'
---

# Lec 11 垄断（一）

> MIT 14.01 Principles of Microeconomics · Lecture 11 · Jonathan Gruber

## TL;DR

- 垄断者面临整条向下倾斜的市场需求曲线，降低价格增加销量的同时会稀释原有销量边际收益。
- 垄断利润最大化严格遵循边际收益等于边际成本（$MR = MC$），产量受限导致价格高于边际成本。
- 勒纳指数 $L = (P - MC)/P = 1/|\epsilon|$ 确立了市场势力加价率与需求价格弹性绝对值的反比关系。

> MIT 14.01 · Principles of Microeconomics · 主讲 Jonathan Gruber

## 5.1.1 垄断利润最大化（Monopoly Profit Maximization）

- 垄断（monopoly）是指市场上只有一家企业的情形。这样的企业是价格制定者（price makers），而不是价格接受者（price takers）。
- 总收益（total revenue）为

$$TR = P(Q) \cdot Q$$

- 平均收益（average revenue）由需求曲线给出

$$AR = P(Q)$$

- 边际收益（marginal revenue, MR）是多卖一单位带来的额外收益

$$MR = \frac{\partial TR}{\partial Q}$$

- 垄断企业面对向下倾斜的需求曲线，因此

$$MR = \frac{\partial TR}{\partial Q} = \frac{\partial P(Q) \cdot Q}{\partial Q} = P(Q) + Q\frac{\partial P}{\partial Q}$$

又因为

$$MR = P(Q) + Q\frac{\partial P}{\partial Q} < P(Q)$$

垄断企业为了多卖出一单位产品，必须降低其所销售的全部单位的价格。这与完全竞争企业不同——完全竞争企业无法影响自己出售商品的价格。因此，垄断企业的 MR 曲线位于 AR 曲线（即需求曲线）之下。

- 垄断企业绝不会在需求曲线的缺乏弹性（inelastic）部分生产：

$$MR = P(Q) + Q\frac{\partial P}{\partial Q} = P\left(1 + \frac{1}{\epsilon_D}\right)$$

当 $|\epsilon_D| < 1$ 时，$MR < 0$。

- 为实现利润最大化，垄断企业在 $MR = MC$ 处生产。

$$MR = P\left(1 + \frac{1}{\epsilon_D}\right) = MC$$

$$\frac{P - MC}{P} = -\frac{1}{\epsilon_D}$$

这就是加成（markup），即衡量垄断力量的指标，其大小取决于需求弹性。加成越高，说明需求越缺乏弹性。

## 5.1.2 垄断的福利效应（Welfare Effects of Monopoly）

- 垄断企业的产量低于完全竞争条件下的产量，这会减少总剩余（total surplus），并产生无谓损失（deadweight loss）。
- 在完全价格歧视（perfect price discrimination）下，社会福利可以达到最大化。

::: insight 稀释效应与市场势力的贪婪边界
垄断者为什么不能随心所欲定出天价？勒纳指数给出了冷冰冰的答案：垄断者受到需求弹性的无情约束。由于垄断者卖出额外一单位必须降低所有单位的价格，边际收益必然比价格跌落得更快。越是缺乏弹性的商品，垄断者搜刮的油水越丰厚；但只要存在哪怕一丝替代可能，消费者转投他处的脚步就会成为悬在垄断者头顶的达摩克利斯之剑。
:::

## 复习要点

**概念理解（Conceptual Understanding）**

- 解释为什么对垄断企业而言边际收益低于平均收益，而对完全竞争企业则不然。
- 理解为什么垄断企业和完全竞争企业都希望在 $MR = MC$ 处生产。
- 解释为什么垄断企业的市场力量取决于需求弹性。
- 解释为什么当垄断企业无法进行价格歧视时会产生无谓损失（DWL）。
- 解释为什么当垄断企业可以进行价格歧视时不会产生无谓损失（DWL）。

**图形与数学理解（Graphical and Math Understanding）**

- 给定成本函数和需求曲线，能求解垄断市场中的价格与产量；并注意检查垄断企业是否会选择停产。
- 会推导垄断加成与需求弹性之间的关系式。
- 能在图形上识别统一定价（uniform price）情形下垄断的生产者剩余、消费者剩余和无谓损失（DWL）。


## 参考资料与延伸阅读

- [MIT OCW 14.01 官方课程资源主页](https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/)
- Gruber, Jonathan. *Public Finance and Public Policy*. Worth Publishers.
- Varian, Hal R. *Intermediate Microeconomics: A Modern Approach*. W. W. Norton & Company.
