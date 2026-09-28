---
title: 跨期选择与现值
type: lecture
lecture: 17
tags: [intertemporal-choice, present-value, discounting, euler-equation, net-present-value]
status: complete
source: 'https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/resources/mit14_01_f23_lec17/'
---

# Lec 17 跨期选择与现值

> MIT 14.01 Principles of Microeconomics · Lecture 17 · Jonathan Gruber

## TL;DR

- 跨期消费选择将今日消费与明日消费纳入预算约束，边际跨期替代率等于 $1+r$ 市场利率折现比。
- 净现值（NPV）法则是资本投资的黄金标尺：仅当未来现金流折现总和超越当期初始成本时投资可行。
- 利率既是借贷资金的客观价格，也是人类放弃即时享乐、推迟消费向未来延展的耐心补偿。

## 核心结论

不同日期的金额不能直接相加。今天的一元可立即消费或投资，因此未来同额现金的现值较低。选择投资或消费计划时，应把所有现金流折算到同一时点。

若利率为 $r$，一年后收到的 $F$ 的现值为 $PV=F/(1+r)$；第 $t$ 年的现金流则除以 $(1+r)^t$。项目的净现值为

$$NPV=-C_0+\sum_{t=1}^{T}\frac{F_t}{(1+r)^t}$$

在给定风险与机会成本的模型中，$NPV>0$ 说明项目的折现收益超过初始成本。

## 名义与实际利率

通胀降低未来货币的购买力。低通胀近似下，实际利率约为名义利率减通胀率；精确关系为 $(1+i)/(1+\pi)-1$。跨期选择关心的是购买力而非票面金额。

::: insight 时间维度的贴现微积分
利率是连接当下与未来的引力常数。没有时间维度的经济学是残缺的扁平画卷；一旦引入折现率，任何长周期的修桥、造路、求学与科研，都必须经受净现值（NPV）的严苛审判。贴现公式冷酷地提醒我们：遥远未来的繁华若折现到今天，往往轻如鸿毛；唯有超越平庸贴现率的伟大工程，才能抵御岁月复利的侵蚀。
:::

## 复习要点

先统一计价日期，再比较方案；折现率上升会降低给定未来收益的现值。

## 视频中的连接

第 17 讲从家庭储蓄流向银行、债券和股票，再由企业获得资金投资的链条，引出现值计算。把未来收入折成现值，才能与今天放弃的消费、投入资本的机会成本比较；不同日期的名义金额不能直接相减。见[字幕约 00:50–01:23](subtitles/lec17.srt)。


## 参考资料与延伸阅读

- [MIT OCW 14.01 官方课程资源主页](https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/)
- Gruber, Jonathan. *Public Finance and Public Policy*. Worth Publishers.
- Varian, Hal R. *Intermediate Microeconomics: A Modern Approach*. W. W. Norton & Company.
