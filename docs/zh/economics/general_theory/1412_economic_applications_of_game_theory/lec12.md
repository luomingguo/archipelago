---
title: 有限重复博弈与合作的崩溃
type: lecture
lecture: 12
tags: [repeated-games, finitely-repeated, backward-induction, chain-store-paradox]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 12 有限重复博弈与合作的崩溃（Finitely Repeated Games）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 重复博弈（Repeated Games）：相同基础阶段博弈在相同时期内被各方重复进行多次。
- 阶段博弈具有唯一纳什均衡时，有限次重复博弈的唯一 SPNE 是每一轮都机械重复静态均衡。
- 探讨多重阶段均衡（如惩罚均衡的存在）如何为有限期博弈创造内生合作空间。

## 核心概念与数学形式化

### 有限重复博弈的逆向归纳分解

设阶段博弈为 $G = \langle I, (A_i), (u_i) \rangle$。博弈重复 $T < \infty$ 期，总收益为累积贴现和：
$$U_i = \sum_{t=1}^T \delta^{t-1} u_i(a_t)$$

- **定理 1（唯一阶段均衡）**：
  若阶段博弈 $G$ 存在**唯一的纳什均衡** $a^*$，则对于任意有限期重复博弈 $G(T)$，存在**唯一的子博弈精炼纳什均衡**，即在每一期 $t = 1, \dots, T$、在任何历史路径下，所有玩家均无条件执行静态均衡行动 $a^*$。

- **定理 2（多重阶段均衡解锁合作）**：
  若阶段博弈 $G$ 存在多个纳什均衡，记较优纳什均衡为 $a^H$，较差（惩罚性）纳什均衡为 $a^L$（$u_i(a^H) > u_i(a^L)$）。
  则当 $T \ge 2$ 且贴现因子足够大时，可以通过以下触发策略在前期维持帕累托更优但非静态均衡的合作行动 $a^C$：
  - 前期执行 $a^C$；若历史无背叛，最后阶段给予 $a^H$ 奖励；
  - 一旦有人偏离 $a^C$，最后阶段全部转入 $a^L$ 严厉惩罚。

## 经济应用与机制分析

项目外包与政企采购中，“一次性一结”的短期合同极易招致偷工减料与违约扯皮；政府必须建立长期的企业信誉档案与准入名录，用未来持续中标的丰厚预期（长期互动）约束当期的工程质量。

## 边界条件与易错点

混淆“有限次重复但终点固定已知”与“有限次但每轮以概率 $p$ 随机终止”（后者数学上严格等价于带有有效贴现因子 $\delta(1-p)$ 的无限期博弈）。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=_XM0CRvaWq0)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
有限重复博弈呈现出经济学中最无情的冷酷宿命。哪怕博弈要重复一万次，只要终点是确切已知的，理性人就会在第一万次背叛，这导致第九千九百九十九次失去惩罚约束……合作的链条应声寸断。摆脱这一宿命的唯一生路，是让终点保持不确定的未知，或者在阶段博弈中拥有多重均衡作为惩罚武器。
:::
