---
title: 从生产到成本
type: lecture
lecture: 6
tags: [cost-minimization, marginal-cost, average-total-cost, economies-of-scale, expansion-path]
status: complete
source: 'https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/resources/mit14_01_f23_lec6/'
---

# Lec 6 从生产到成本

> MIT 14.01 Principles of Microeconomics · Lecture 6 · Jonathan Gruber

## TL;DR

- 成本最小化要求等成本线与等产量线相切，满足边际技术替代率等于要素价格比 $w/r$。
- 边际成本（MC）曲线穿越平均可变成本（AVC）与平均总成本（ATC）的最低点，主导供给弹性。
- 长期平均成本曲线是所有短期平均成本包络线，其平坦或 U 形态决定了产业内的最优企业规模。

> MIT 14.01 · Principles of Microeconomics · 主讲 Jonathan Gruber

## 短期成本

- **固定成本（fixed costs）**是短期内无法调整数量的投入的成本。本课程通常把资本（capital）归为固定成本。
- **可变成本（variable costs）**是短期内可以调整数量的投入的成本。本课程通常把劳动（labor）归为可变成本。
- **总成本（total costs）**是固定成本与可变成本之和：

$$
C = FC + VC
$$

- **边际成本（marginal cost）**是多生产一单位产出带来的成本变化：

$$
MC = \frac{\Delta C}{\Delta q}
$$

  在短期，固定成本不随产量变化，所以 $MC=\Delta VC/\Delta q$；它是**每单位产出**的可变成本增量，并非总可变成本的绝对变化量。

- **平均成本（average costs）**是平均到每单位产出上的生产成本：

$$
AC = \frac{C}{q}, \qquad AVC = \frac{VC}{q}, \qquad AFC = \frac{FC}{q}
$$

- 在常见的 U 形成本图中，平均固定成本（AFC）持续下降；平均可变成本（AVC）与平均总成本（AC）可先下降后上升。MC 曲线穿过 AVC 和 AC 各自的最低点。MC 是否为直线、AVC 如何变化，仍由具体生产技术决定。
- **沉没成本（sunk costs）**是无论怎样调整生产方式都无法收回的成本。沉没成本已经无法挽回，因此不应该影响未来的生产决策。

## 长期成本

- 回忆一下，在长期，所有投入的成本都是可变的。因此企业面临的选择变成了投入组合（input mix）的选择，目标是最大化生产效率，即最小化成本。
- **等成本线（isocost line）**是能带来同一总成本水平的资本与劳动的所有组合。总成本为：

$$
C = rK + wL
$$

- 企业会为给定的产出水平选择经济上有效率（economically efficient）的投入组合。
- 当等产量线（isoquant）$f(L, K)$ 与等成本线 $C = wL + rK$ 相切时，实现了成本最小化：

$$
\frac{MP_L}{MP_K} = \frac{w}{r} \;\Rightarrow\; \frac{MP_L}{w} = \frac{MP_K}{r}
$$

  经济上有效率的点，是花在劳动上的最后一美元与花在资本上的最后一美元，对产出的边际贡献相等的点。
- **扩展路径（expansion path）**描绘的是在所有产出水平下，成本最小化的 $(K, L)$ 组合所构成的轨迹。

## 会计利润与经济利润

- **会计利润（accounting profits）**只衡量以现金形式实际发生的收入流入和成本流出。
- **经济利润（economic profit）**除了会计利润所涵盖的部分外，还要计入那些未必以现金支付的机会成本（opportunity costs）。

::: insight 对偶原理下的成本透视
生产最大化与成本最小化是完全对称的拉格朗日对偶命题。成本曲线不是凭空画出来的会计数字，它是生产技术等产量线在要素市场价格加权下的精确数学投影。MC 曲线之所以在谷底穿过 ATC，是因为只要新增一单位的边际成本低于均值，平均成本就必然被拉低——这是算术平均值在微积分中的永恒真理。
:::

## 复习要点

- 能识别固定成本、可变成本和沉没成本的定义。
- 理解短期与长期生产的区别：短期内至少有一种投入（资本）是固定的；长期内所有投入都是可变的。
- 能解释为什么平均成本曲线的最低点恰好与边际成本曲线相交。
- 理解企业会选择能以最低成本生产给定产出的投入组合。
- 能推导不同的成本函数：总成本、固定成本、可变成本、边际成本、平均成本。
- 掌握 AFC、AVC、MC 三条曲线在图形上的形状特征。
- 能在等产量线—等成本线图中，用图形方法展示如何得到成本最小化的 $(L, K)$ 组合。


## 参考资料与延伸阅读

- [MIT OCW 14.01 官方课程资源主页](https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/)
- Gruber, Jonathan. *Public Finance and Public Policy*. Worth Publishers.
- Varian, Hal R. *Intermediate Microeconomics: A Modern Approach*. W. W. Norton & Company.
