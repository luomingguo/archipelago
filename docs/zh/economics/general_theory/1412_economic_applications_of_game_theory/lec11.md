---
title: 单阶段偏离原则与动态博弈检验
type: lecture
lecture: 11
tags: [one-shot-deviation-principle, dynamic-programming, spne-verification, infinite-horizon]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 11 单阶段偏离原则与动态博弈检验（One-Shot Deviation Principle and Bargaining）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 在无限期或长程动态博弈中，全策略路径的穷举检验面临维数灾难。
- 单阶段偏离原则（One-Shot Deviation Principle, OSDP）：检验整体最优性等价于检验任何单期偏离不带来增益。
- 阐明具有“无限期连续贴现”（Continuity at Infinity）性质的博弈中 OSDP 的充要性证明。

## 核心概念与数学形式化

### 单阶段偏离的形式化定义

考虑多阶段动态博弈。策略剖面 $s = (s_1, \dots, s_n)$。
- 玩家 $i$ 的一个备选策略 $s_i'$ 是 $s_i$ 在历史 $h$ 处的**单阶段偏离（One-Shot Deviation）**，如果：
  1. 在历史 $h$ 处，$s_i'(h) \ne s_i(h)$；
  2. 在所有其他历史 $h' \ne h$ 处，$s_i'(h') = s_i(h')$。

### 单阶段偏离原则（OSDP）
- **条件**：博弈满足在无穷远处连续（Continuity at Infinity，即遥远未来的收益受贴现因子压制，对当期总现值影响趋于零）。
- **定理**：策略剖面 $s^*$ 是一个子博弈精炼纳什均衡（SPNE），**当且仅当**不存在任何玩家 $i$ 和任何历史 $h$，使得玩家 $i$ 能够通过在历史 $h$ 实施单阶段偏离而严格提高其在该子博弈中的期望折现收益。

### 检验算法步骤
1. 找出玩家在所有典型状态或历史下的策略推荐行动。
2. 假定玩家偏离一期选择备选行动 $a_i \ne s_i^*(h)$，但假定此后所有未来阶段均重新严格服从原推荐策略 $s_i^*$。
3. 比较当期单阶段偏离净现值与原均衡净现值，若 $\forall h, \Delta V \le 0$，则均衡严格获证。

## 经济应用与机制分析

金融监管合规审计的抽查验证逻辑完全契合 OSDP：只要金融机构在每一个日终结算时间节点的单日违规套利期望利润为负，就能以最低的稽查监管成本保证金融体系全生命周期的合规稳定性。

## 边界条件与易错点

将 OSDP 盲目推广到不满足无穷远处连续性的博弈（如无贴现且无限持续累积收益的病态博弈）。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=iL3XRRI5rQs)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
单阶段偏离原则是博弈论与动态规划（贝尔曼方程）相遇的奇迹定理。面对无限期无穷无尽的策略分支，我们无需疲于奔命去推演未来成百上千步的复杂偏离；只要证明在每一个可能历史下，任何一次性的单步试探性出轨都无法赚取超额回报，整个庞大系统就坚如磐石。
:::
