---
title: 零和博弈与极大极小定理
type: lecture
lecture: 7
tags: [zero-sum-games, minimax-theorem, security-strategies, linear-programming]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 7 零和博弈与极大极小定理（Zero-Sum Games）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 零和博弈（Zero-Sum Games）中各方利益严格对立，联合收益之和恒为常数：$u_1 + u_2 = 0$。
- 定义保守安全策略与极大极小值（Maximin Value）：假定对手全力压制自己时所能保证的最差收益。
- 阐释冯·诺依曼极大极小定理：在有限零和博弈的混合策略空间中，极大极小值等于极小极大值。

## 核心概念与数学形式化

### 零和博弈与安全策略

设二人零和博弈中 $u_1(s_1, s_2) = -u_2(s_1, s_2) = u(s_1, s_2)$。
- 玩家 1 的**下安全值（Maximin Value）**：
  $$\underline{v} = \max_{\sigma_1 \in \Delta(S_1)} \min_{\sigma_2 \in \Delta(S_2)} u(\sigma_1, \sigma_2)$$
- 玩家 1 的**上安全值（Minimax Value）**：
  $$\bar{v} = \min_{\sigma_2 \in \Delta(S_2)} \max_{\sigma_1 \in \Delta(S_1)} u(\sigma_1, \sigma_2)$$

恒有弱不等式成立：$\underline{v} \le \bar{v}$。

### 冯·诺依曼极大极小定理（von Neumann, 1928）
在任何有限二人零和博弈中，混合策略极大极小值与极小极大值严格相等：
$$\underline{v} = \bar{v} \equiv v^*$$
常数 $v^*$ 称为该**博弈的价值（Value of the Game）**。
- 此时使极大极小值成立的策略剖面 $(\sigma_1^*, \sigma_2^*)$ 恰好构成该博弈的纳什均衡（鞍点 Saddle Point）。
- 求解零和博弈混合策略等价于求解一对互为对偶的线性规划（Linear Programming）问题。

## 经济应用与机制分析

在网络防御与关键基础设施防护中，安全架构师必须将攻击者假定为最具敌意的零和破坏者。基于极大极小防御准则设计冗余容灾，能够确保在遭遇未知的零日漏洞突袭时依然维持底线系统存活。

## 边界条件与易错点

误将非零和博弈（如双赢或囚徒困境）生搬硬套极大极小定理；忽视纯策略零和博弈可能不存在鞍点。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=CBCf8iWKFZY)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
零和博弈是人类冲突最严酷的缩影。在零和世界中，不存在任何合作互利的可能，你的所得就是我的切肤之痛。极大极小定理的数学之美在于揭示了防守与进攻的终极对称：竭尽全力保障自己的底线安全，在数学上恰好完全锁定了剥夺对手超额收益的进攻上限。
:::
