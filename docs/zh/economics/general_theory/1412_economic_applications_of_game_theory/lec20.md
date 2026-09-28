---
title: 互联网广告拍卖：广义二阶拍卖与关键词竞价
type: lecture
lecture: 20
tags: [ad-auctions, gsp, vcg-mechanism, search-advertising]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 20 互联网广告拍卖：广义二阶拍卖与关键词竞价（Ad Auctions）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 梳理搜索引擎关键词广告的商业模式与点击率（CTR）排序加权。
- 剖析广义二阶拍卖（Generalized Second Price, GSP）机制及其非真实报价的博弈结构。
- 对比 Vickrey-Clarke-Groves（VCG）机制，推导 GSP 的无嫉妒稳定均衡（Envy-Free Equilibrium）。

## 核心概念与数学形式化

### 广告位竞价模型设定

$K$ 个广告槽位，点击率严格递减：$\alpha_1 > \alpha_2 > \dots > \alpha_K$。
$N$ 位广告主，每次点击真实价值为 $v_1, v_2, \dots, v_N$。
广告主提交出价 $b_1 \ge b_2 \ge \dots \ge b_N$。

### 1. 广义二阶拍卖（GSP）规则
- 广告位 $k$ 分配给出价第 $k$ 高的竞标者；
- 每点击扣费（Cost Per Click, CPC）等于排在下一位者的出价：
  $$p_k = b_{k+1}$$
- 竞标者 $k$ 获得的净收益为：
  $$u_k = \alpha_k (v_k - b_{k+1})$$
- **关键性质**：在 GSP 中，真实出价 $b_k = v_k$ **不再是**占优策略！广告主有动机通过微调出价故意输给上一个人，以换取低槽位更便宜的每点击成本。

### 2. GSP 对称无嫉妒均衡（Envy-Free / Locally-Bilinear Equilibrium）
一个出价剖面构成无嫉妒均衡，如果任何广告主都不羡慕别人所获得的槽位和支付组合：
$$\alpha_k(v_k - p_k) \ge \alpha_j(v_k - p_j) \quad \forall j$$
- **Edelman, Ostrovsky, and Schwarz (2007) 定理**：
  在所有对称无嫉妒均衡中，存在一个唯一的稳定均衡，其配置结果与产生的平台总收益严格等价于主导理论 VCG 机制的收益！

## 经济应用与机制分析

现代平台算法治理在设计机制时，必须严密测算广告主自发算法调价的博弈收敛性。如果竞价规则诱发周期性出价跳跃震荡（Cycling Bids），不仅损耗广告主服务器算力，更会导致平台变现流水的剧烈不确定性。

## 边界条件与易错点

误以为 GSP 拥有单一二阶拍卖的弱占优性；混淆出价 $b_k$ 与实际扣费 $p_k$。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=Myfs7LdkV98)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
支撑当今全球万亿美元数字经济帝国的核心引擎，正是 Google 和百度背后的 GSP 广告竞价算法。虽然 GSP 表面上是二阶拍卖的自然多槽位推广，但它却丢失了弱占优真实报价的优良性质；然而令人称奇的是，市场各方通过自发演化出的“无嫉妒均衡”，在现实中达成了与经典 VCG 机制分毫不差的高效稳定分配。
:::
