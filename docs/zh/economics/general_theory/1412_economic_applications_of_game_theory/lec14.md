---
title: 民间定理（Folk Theorem）与长期合作秩序
type: lecture
lecture: 14
tags: [folk-theorem, repeated-games, minimax-punishment, social-order]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 14 民间定理（Folk Theorem）与长期合作秩序（Folk Theorem）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 定义可行收益集（Feasible Payoffs）与个体理性收益集（Individually Rational Payoffs）。
- 极小极大惩罚收益（Minimax Payoffs）：任何理性玩家绝不可能被长期压制在安全底线之下。
- 阐明弗里德曼与福登伯格-马斯金民间定理：只要贴现因子充分接近 1，任何严格个体理性的可行收益均可被 SPNE 实现。

## 核心概念与数学形式化

### 基础定义

设阶段博弈 $G$ 中纯策略联合收益的凸包为**可行收益集（Feasible Set, $V$）**：
$$V = \text{co}\{u(s) \mid s \in S\}$$

- 玩家 $i$ 的**极小极大收益（Minimax Value）**：
  $$\underline{v}_i = \min_{\alpha_{-i} \in \prod_{j \ne i}\Delta(S_j)} \max_{a_i \in A_i} u_i(a_i, \alpha_{-i})$$
  任何理性玩家在长期内绝不接受低于 $\underline{v}_i$ 的平均回报。

- **严格个体理性收益集（Strictly Individually Rational Payoffs, $V^*$）**：
  $$V^* = \{v \in V \mid v_i > \underline{v}_i, \forall i \in I\}$$

### 民间定理（Fudenberg and Maskin, 1986）
假定可行收益集 $V$ 的维度等于玩家人数 $n$（完全维度条件 Full-Dimensionality Condition）：
对于严格个体理性集合 $V^*$ 中的**任意**收益向量 $v = (v_1, \dots, v_n) \in V^*$，存在一个贴现因子阈值 $\underline{\delta} < 1$，使得对于所有 $\delta \in (\underline{\delta}, 1)$：
存在该无限重复博弈的一个子博弈精炼纳什均衡（SPNE），其平均折现收益严格等于 $v$！

## 经济应用与机制分析

民间定理为习惯法、商人自治公会以及开源软件社区的代码审查文化提供了坚实的数理辩护。在缺乏自上而下的中央强制执法力时，重复博弈的极小极大威胁是人类文明演化出自发协作秩序的终极基石。

## 边界条件与易错点

忘记民间定理的前提是贴现因子 $\delta \to 1$ 且收益必须在个体理性底线 $\underline{v}_i$ 之上；忽视其带来的极端多重均衡难以挑选的问题。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=3ws34WgJKzk)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
民间定理是博弈论中最具哲学震撼力的里程碑：它证明了在足够有耐心的重复交往中，自利理性人可以自发涌现出几乎任何形式的社会秩序——从绝对平等的共产协作，到高度严苛的阶层分工。但这把双刃剑也带来“多重均衡的诅咒”：它没有告诉我们哪一种秩序会最终胜出。
:::
