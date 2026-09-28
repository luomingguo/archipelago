---
title: 拍卖机制设计：四种经典拍卖与投标策略
type: lecture
lecture: 18
tags: [auction-theory, first-price-auction, second-price-auction, vickrey-auction]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 18 拍卖机制设计：四种经典拍卖与投标策略（Auctions）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 建立独立私有价值（IPV）基准拍卖环境：买方估值 $v_i \sim F[0, 1]$ 独立同分布。
- 证明二阶密封价格拍卖（SPA / Vickrey 拍卖）中，真实报价 $b_i = v_i$ 是弱占优策略。
- 求解一阶密封价格拍卖（FPA）的对称贝叶斯纳什均衡，揭示“压价竞标”（Bid Shading）的数学规律。

## 核心概念与数学形式化

### 独立私有价值模型（IPV）
$n$ 位竞标者。买家 $i$ 的真实估值为 $v_i \in [0, 1]$，独立同分布服从 $F(v)$，密度函数为 $f(v)$。

### 1. 二阶密封拍卖（SPA）弱占优定理
在 SPA 中，最高出价者赢得物品，但只需支付第二高出价：
$$u_i(b_i, b_{-i}) = \begin{cases} v_i - \max_{j \ne i} b_j & \text{若 } b_i > \max_{j \ne i} b_j \\ 0 & \text{若 } b_i < \max_{j \ne i} b_j \end{cases}$$
- **定理**：真实出价 $b_i^*(v_i) = v_i$ 是每个竞标者的**弱占优策略（Weakly Dominant Strategy）**！
  - 若尝试向上虚报 $b_i > v_i$，只有在第二高价落在 $(v_i, b_i)$ 之间时会改变结果，但此时净收益 $v_i - \max b_j < 0$ 蒙受亏损；
  - 若尝试向下压价 $b_i < v_i$，只有在第二高价落在 $(b_i, v_i)$ 之间时会错失本可盈利的交易。

### 2. 一阶密封拍卖（FPA）对称 BNE 求解
最高出价者赢得物品并按自身出价付款。存在压价动机：
设对称单调递增出价函数 $b(v)$。买家期望收益：
$$\max_b (v_i - b) \Pr(\text{赢得物品}) = (v_i - b) F(b^{-1}(b))^{n-1}$$
一阶条件求导，积分得出唯一对称微分方程解：
$$b^*(v_i) = \mathbb{E}\left[\max_{j \ne i} v_j \Bigm| \max_{j \ne i} v_j \le v_i\right] = v_i - \frac{\int_0^{v_i} F(x)^{n-1} dx}{F(v_i)^{n-1}}$$
- 特别地，若 $v_i \sim U[0, 1]$，则 $b^*(v_i) = \frac{n-1}{n} v_i$。参与人数越多，压价空间越窄，出价越逼近真实估值。

## 经济应用与机制分析

国有资产转让与频谱牌照拍卖中，规则细节决定了财政收入成败。采用英式公开拍卖或二阶拍卖能极大降低中小型民营企业的估值调研与策略计算门槛，激活更多竞争者入场。

## 边界条件与易错点

混淆私有价值模型与共同价值模型（在共同价值中盲目真实报价会遭遇严重的“胜者的诅咒 Winner's Curse”）。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=7dTlS_PLo6I)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
维克里二阶拍卖是博弈机制设计中最迷人、最精巧的发明。通过让赢家支付“全场第二高报价”，机制巧妙斩断了竞标者隐藏底牌的企图：多报一分钱只能增加被宰的风险，少报一分钱只会白白痛失盈利的宝物。诚实汇报成为了抵御任何复杂心机博弈的最优铠甲。
:::
