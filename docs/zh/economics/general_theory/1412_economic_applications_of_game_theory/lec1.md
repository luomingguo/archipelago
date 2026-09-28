---
title: 个人决策理论与策略环境基础
type: lecture
lecture: 1
tags: [game-theory, decision-theory, expected-utility, strategic-thinking]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 1 个人决策理论与策略环境基础（Introduction to Individual Decision-Making）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 决策理论从行动集、可能结果集与跨期或风险偏好关系出发刻画理性人行为。
- 在不确定性环境下，冯·诺依曼-摩根斯坦期望效用函数将主观概率与客观结果加权统一。
- 策略性博弈与单人决策的根本区别：自身收益不仅取决于自身行动，更取决于对手的理性选择。

## 核心概念与数学形式化

### 决策环境与期望效用理论

单人决策问题的标准三元组：
1. 可行行动集合 $A = \{a_1, a_2, \dots, a_n\}$。
2. 外部世界状态集合 $\Omega = \{\omega_1, \dots, \omega_m\}$，满足概率分布 $p \in \Delta(\Omega)$。
3. 结果集合 $X$，结果映射函数 $g: A \times \Omega \to X$。

冯·诺依曼-摩根斯坦（vNM）效用函数：
$$U(a) = \sum_{\omega \in \Omega} p(\omega) u(g(a, \omega))$$
理性主体求解优化问题：
$$\max_{a \in A} U(a)$$

### 策略性交互环境（博弈论的引入）
当外部环境的状态不仅由外生自然决定，而是由另一名（或多名）理性局中人 $j$ 的行动 $s_j \in S_j$ 决定时，决策问题转变为博弈（Game）。此时概率分布不再是纯粹的客观物理分布，而是局中人对其他局中人策略的**信念（Beliefs）**。

## 经济应用与机制分析

在微观经济政策与产业规划中，政府不能将市场主体视为被动接受价格的单人决策者。任何监管规则的出台，都会触发被规制企业自发的逆向策略博弈，产生意想不到的逃避或套利行为。

## 边界条件与易错点

混淆对客观自然状态的不确定性与对对手行动策略的不确定性；误以为期望效用要求局中人风险中性。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=WRibE2nt8wM)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
博弈论不是高高在上的象牙塔抽象，而是关于“多主体交互决策”的数学物理学。单人最优化面对的是无意识的自然法则，而博弈决策面对的是同样具有前瞻性、企图预测你下一步行动的活生生的人。策略思维的精髓是站在对手的立场推演其最佳反应。
:::
