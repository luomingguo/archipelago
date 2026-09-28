---
title: 不确定性与风险偏好
type: lecture
lecture: 20
tags: [expected-utility-theory, risk-aversion, certainty-equivalent, risk-premium, jensens-inequality]
status: complete
source: 'https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/resources/mit14_01_f23_lec20/'
---

# Lec 20 不确定性与风险偏好

> MIT 14.01 Principles of Microeconomics · Lecture 20 · Jonathan Gruber

## TL;DR

- 冯·诺依曼-摩根斯坦期望效用理论表明，不确定性下的选择取决于各可能状态效用的概率加权平均。
- 效用函数的二阶导数决定风险偏好：严格凹函数刻画风险厌恶，凹性程度决定了风险溢价的大小。
- 根据琴生不等式（Jensen's Inequality），风险厌恶者的期望财富效用严格高于随机财富的期望效用。

## 核心结论

风险选择应比较各结果带来的**期望效用**，而不只比较金额的期望值。若结果 $x_i$ 的概率为 $p_i$，则 $E[X]=\sum_i p_i x_i$，而 $EU=\sum_i p_i u(x_i)$。一般有 $u(E[X])\neq E[u(X)]$。

## 效用曲线与风险态度

- **风险厌恶**：效用函数凹，收入的边际效用递减；同一期望值下偏好确定金额。
- **风险中性**：效用函数线性，只关心期望金额。
- **风险偏好**：效用函数凸，可能偏好具有波动的赌局。

风险厌恶者愿意付保费，把不确定损失转换为确定成本。使其恰好无差异的最高保费与按概率计算的预期损失之间的差额，是风险溢价。损失规模、收入与效用曲线的形状会改变它。

::: insight 财富凹性与人类对安宁的溢价
为什么人们愿意花钱买保险？因为金钱在人类心灵中具有递减的边际价值。丢掉一万元导致的饥寒交迫痛苦，远比捡到一万元带来的锦上添花狂喜更为剧烈。正是效用函数向下弯曲的几何凹性，催生了现代保险与金融对冲帝国。风险溢价不是浪费，它是人类理性为了换取确定性与心灵安宁而自愿向不确定的宇宙支付的门票。
:::

## 复习要点

算出每个结果的效用再乘概率；不要先求平均金额再代入效用函数。

## 视频中的例子

视频开头以“天气预报有下雨概率，要不要带伞”说明不确定性决策：比较的是各状态发生概率、带伞或不带伞的结果，以及个人对结果的效用。只算天气的平均状态没有意义；保险分析也需要把**概率与各状态的效用**结合，而不是只比较平均金钱收入。见[字幕约 01:05 起](subtitles/lec20.srt)。


## 参考资料与延伸阅读

- [MIT OCW 14.01 官方课程资源主页](https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/)
- Gruber, Jonathan. *Public Finance and Public Policy*. Worth Publishers.
- Varian, Hal R. *Intermediate Microeconomics: A Modern Approach*. W. W. Norton & Company.
