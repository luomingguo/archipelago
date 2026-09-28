---
title: 寡头垄断
type: lecture
lecture: 13
tags: [oligopoly, game-theory, nash-equilibrium, prisoners-dilemma, dominant-strategy]
status: complete
source: 'https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/resources/mit14_01_f23_lec13/'
---

# Lec 13 寡头垄断

> MIT 14.01 Principles of Microeconomics · Lecture 13 · Jonathan Gruber

## TL;DR

- 寡头市场由少数几家大企业主导，企业决策具备强烈的策略互动性与依存性，无法单方面独立定价。
- 博弈论模型以参与人、策略集与收益矩阵为基础，纳什均衡定义为在对手策略给定下的单边最优反应。
- 囚徒困境揭示个体理性追求优势策略可能导致集体次优结果，合谋往往因欺诈冲动而天然不稳定。

> MIT 14.01 · Principles of Microeconomics · 主讲 Jonathan Gruber

## 6.1.1 寡头垄断概览（Oligopoly Overview）

- 寡头垄断（oligopoly）是指市场中只有少数几家企业，且存在其他企业进入市场的实质性壁垒（substantial barriers to entry）。
- 在寡头垄断市场中，企业可以合作行动，也可以不合作行动。如果合作，它们可以组成卡特尔（cartel）；如果不合作，结果会趋向竞争性市场结果，利润更低。
- 只有两家企业的市场被称为双寡头（duopoly）。

## 6.1.2 博弈论（Game Theory）

- 博弈论有两个关键点：
  - 每家企业都会制定一个策略，该策略取决于它认为其他企业会如何行动，所有企业的策略组合在一起，共同决定了市场结果；
  - 当市场达到均衡时，博弈结束。
- 纳什均衡（Nash Equilibrium）：在给定其他企业行为的情况下，没有一家企业想要改变自己的策略。
- 囚徒困境（prisoner's dilemma）：博弈论的一个简单例子，我们用支付矩阵（payoff matrix）来说明这个问题。
- 占优策略（dominant strategy）：无论对方做什么，己方的最优选择都是同一个策略。

## 6.1.3 古诺非合作均衡模型（Cournot Model of Noncooperative Equilibrium）

- 古诺均衡（Cournot equilibrium）：一组各企业的产量，满足在其他所有企业产量保持不变的情况下，没有一家企业能通过改变自己的产量获得更高的利润。
- 反应曲线（reaction curve）：企业利润最大化产量与它预期竞争对手将生产的产量之间的关系。古诺均衡就是各条反应曲线的交点。
- 计算古诺均衡的数学步骤：
  - 计算某一企业的剩余需求（residual demand），即从市场需求中扣除其他企业产量决策后，留给该企业产品的需求；
  - 建立总收益（total revenue）函数；
  - 由总收益函数推导边际收益（marginal revenue）；
  - 求解该企业的利润最大化问题（$MR = MC$），得到该企业对其他企业产量决策的最优反应函数（best response function）；
  - 解是一组产量（每家企业各一个），它们联立求解上述反应函数所构成的方程组。

::: insight 互动阴影下的理性悲剧
从完全竞争与纯粹垄断走向寡头，我们跨越了从“单人最优化”向“多人交互博弈”的范式鸿沟。囚徒困境是人类社会最沉重的隐喻：两家寡头企业如果秘密合谋维持高价，本可共享垄断暴利；但在缺乏可信外部惩戒的情境下，每一个单方背叛偷降价格的冲动都无法遏制。个体理性的自私计算，最终无情地碾碎了集体合谋的美梦。
:::

## 复习要点

**概念理解（Conceptual Understanding）**

- 能解释"囚徒困境"。
- 理解为什么合作可以在无限重复博弈（infinitely repeated game）中维持，而在有限期博弈（finite periods）中无法维持。
- 能解释为什么卡特尔是不稳定的。

**图形与数学理解（Graphical and Math Understanding）**

- 给定支付矩阵，能找出博弈的纳什均衡。
- 能求解两家企业在古诺均衡下的产量与价格。
- 能求解 $n$ 家企业组成卡特尔时的均衡。


## 参考资料与延伸阅读

- [MIT OCW 14.01 官方课程资源主页](https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/)
- Gruber, Jonathan. *Public Finance and Public Policy*. Worth Publishers.
- Varian, Hal R. *Intermediate Microeconomics: A Modern Approach*. W. W. Norton & Company.
