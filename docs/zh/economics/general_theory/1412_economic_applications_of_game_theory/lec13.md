---
title: 无限重复博弈与触发策略
type: lecture
lecture: 13
tags: [repeated-games, infinitely-repeated, grim-trigger, tit-for-tat]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 13 无限重复博弈与触发策略（Infinitely Repeated Games）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 无限重复博弈消除确定的终点，引入跨期贴现因子 $\delta \in (0, 1)$。
- 冷酷触发策略（Grim Trigger）：以永久背叛惩罚换取合作，推导维系合作的临界贴现阈值 $\delta^*$。
- 以牙还牙（Tit-for-Tat）与有限期宽恕策略：分析抗噪容错性与抵生报复机制。

## 核心概念与数学形式化

### 囚徒困境的冷酷触发策略分析

设阶段博弈收益矩阵：
| | 合作 $C$ | 背叛 $D$ |
| :---: | :---: | :---: |
| **合作 $C$** | $(1, 1)$ | $(-1, 2)$ |
| **背叛 $D$** | $(2, -1)$ | $(0, 0)$ |

**冷酷触发策略（Grim Trigger）定义**：
- 第一期选择 $C$。
- 在第 $t$ 期，若所有过去历史 $(a_1, \dots, a_{t-1})$ 全为 $(C, C)$，则继续选择 $C$；
- 只要有任何一名玩家在任何历史中选择过 $D$，永久转入 $D$（永远不予宽恕）。

### 临界贴现阈值 $\delta^*$ 求解
利用单阶段偏离原则：
1. **坚守合作的贴现总收益现值**：
   $$V(C) = 1 + \delta \cdot 1 + \delta^2 \cdot 1 + \dots = \frac{1}{1 - \delta}$$
2. **当期背叛的最高贴现现值**：
   当期拿到最高偷袭收益 $2$，随后对手永久转入 $D$，未来每期只能拿 $0$：
   $$V(D) = 2 + \delta \cdot 0 + \delta^2 \cdot 0 + \dots = 2$$
3. **维系 SPNE 的充要条件**：
   $$V(C) \ge V(D) \implies \frac{1}{1 - \delta} \ge 2 \implies 1 \ge 2 - 2\delta \implies \delta \ge \frac{1}{2}$$
只要贴现因子 $\delta \ge 0.5$（即对明天的重视程度不低于今天的一半），自发合作即可作为子博弈精炼纳什均衡永久维持！

## 经济应用与机制分析

在建立行业自律同业公会或国际碳减排机制时，政策的核心不是派驻警察物理盯防，而是建立透明的信息通报网络与可信的违约抵制同盟，确保任何违规行为都会在未来遭遇确定性的共同抵制。

## 边界条件与易错点

误以为只要贴现因子够大合作就自动发生（忽视了博弈永远存在“全员背叛”这一平庸纳什均衡，合作依赖于各方的协调聚焦）。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=HRZeLYNhOUw)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
“未来的阴影”（Shadow of the Future）是文明自发秩序生长的最深沃土。在无限重复博弈中，当人们对未来的重视程度超越了当期背叛的短期暴利时，互利合作就从高尚的道德倡议蜕变为铁一般的自利最优选择。冷酷触发策略展示了威慑的威严：合作越诱人，背叛后的报复就必须越不可挽回。
:::
