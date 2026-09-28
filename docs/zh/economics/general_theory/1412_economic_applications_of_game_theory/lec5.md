---
title: 纳什均衡及其混合策略扩展
type: lecture
lecture: 5
tags: [nash-equilibrium, mixed-strategies, fixed-point-theorem, coordination-games]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 5 纳什均衡及其混合策略扩展（Nash Equilibrium）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 纳什均衡（Nash Equilibrium）定义：没有任何局中人拥有单方面偏离其策略的单调动机。
- 引入混合策略（Mixed Strategy）：玩家在纯策略空间上赋予独立概率分布进行随机化博弈。
- 阐明纳什定理：任何有限博弈必至少存在一个混合策略纳什均衡（基于 Kakutani 不动点定理）。

## 核心概念与数学形式化

### 纯策略纳什均衡定义

策略剖面 $s^* = (s_1^*, s_2^*, \dots, s_n^*) \in S$ 构成一个**纳什均衡**，如果对任意玩家 $i \in I$ 和任意可行备选策略 $s_i \in S_i$，均满足：
$$u_i(s_i^*, s_{-i}^*) \ge u_i(s_i, s_{-i}^*) \quad \forall s_i \in S_i$$
即每个玩家的均衡策略都是对其他玩家均衡策略的最佳反应：$s_i^* \in BR_i(s_{-i}^*)$。

### 混合策略纳什均衡（Mixed Strategy Nash Equilibrium, MSNE）
设玩家 $i$ 的混合策略为 $\sigma_i \in \Delta(S_i)$，收益为期望效用 $u_i(\sigma_i, \sigma_{-i})$。
$(\sigma_1^*, \dots, \sigma_n^*)$ 构成纳什均衡，当且仅当：
$$u_i(\sigma_i^*, \sigma_{-i}^*) \ge u_i(s_i, \sigma_{-i}^*) \quad \forall s_i \in S_i, \forall i \in I$$

- **无差异原则（Indifference Principle）**：
  若玩家 $i$ 在混合策略中以严格正概率选择两个纯策略 $s_{i1}$ 和 $s_{i2}$，则对手的混合策略必须使得 $i$ 从这两个纯策略中获得的期望收益**严格相等**：
  $$u_i(s_{i1}, \sigma_{-i}^*) = u_i(s_{i2}, \sigma_{-i}^*)$$

### 纳什存在性定理
任何有限博弈（有限玩家、有限纯策略集合）都至少存在一个（纯策略或混合策略）纳什均衡。证明利用了最佳反应对应在紧凸集上的 Kakutani 不动点定理。

## 经济应用与机制分析

在反恐安检、逃税稽查与环保巡查中，执法部门的最优检查策略必然是混合策略：保持不可预测的随机性，并将抽查概率精准设定在恰好消除违法者期望超额净收益的无差异线上。

## 边界条件与易错点

在计算混合策略纳什均衡时，误用自己的收益去求解自己的概率，忽视了自身概率必须通过让对手无差异来反向求解。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=ftCXguW2k4o)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
纳什均衡的划时代意义在于把“预期的一致性”与“行动的最优性”闭环锁合。混合策略的本质不是为了欺骗对手而扔骰子，而是将自己的行为调整到让对手在多个备选策略之间感到“完全无差异”的微妙临界状态，从而维持系统性的稳态平衡。
:::
