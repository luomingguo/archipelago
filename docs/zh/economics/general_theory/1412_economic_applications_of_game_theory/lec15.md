---
title: 隐性卡特尔与反垄断规制
type: lecture
lecture: 15
tags: [implicit-cartels, antitrust, rotemberg-saloner, price-wars]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 15 隐性卡特尔与反垄断规制（Implicit Cartels）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 运用无限重复博弈建模寡头垄断企业之间的隐性价格同盟（Tacit Collusion）。
- 分析 Rotemberg-Saloner 需求波动模型：景气繁荣期偷袭诱惑激增，均衡价格战反周期爆发。
- 剖析反垄断宽恕政策（Leniency Program）如何利用首位自首免责制造囚徒困境瓦解卡特尔。

## 核心概念与数学形式化

### 1. 基准隐性卡特尔模型
两家企业进行无限期伯川德价格竞争。垄断利润为 $\Pi^M$。
- 若默契维持垄断高价，每期平分利润 $\frac{\Pi^M}{2}$。
- 若一方降价 $\epsilon$ 偷袭，当期独吞几乎全部利润 $\Pi^M$，此后永久陷入边际成本零利润价格战。
- 维持卡特尔的条件：
  $$\frac{\Pi^M / 2}{1 - \delta} \ge \Pi^M \implies \delta \ge \frac{1}{2}$$

### 2. Rotemberg-Saloner 需求波动与价格战
需求状态在每一期随机在繁荣（$D^H$）与萧条（$D^L$）之间独立同分布切换（$D^H > D^L$）。
- 在繁荣期，当期偏离收益为 $\Pi^M(D^H)$；
- 而未来被惩罚损失的仅仅是期望平均利润 $\frac{\mathbb{E}[\Pi]}{2}$。
- **反常结论**：当需求处于峰值 $D^H$ 时，由于偏离诱惑过大，全额垄断价格无法维持；卡特尔为了防止同盟被偷袭瓦解，**被迫在繁荣期自愿削减价格**开展阶段性价格战，以降低偷袭收益维系同盟稳定！

## 经济应用与机制分析

现代反垄断机构的“宽恕制度”（Leniency Policy）被公认为打击垄断最成功的机制创新：第一家主动提供书面证据自首的企业享受 100% 罚款豁免，第二家仅减免 50%，其余重罚。这彻底破坏了密谋者之间的重复博弈信任，引发竞相自首抢跑。

## 边界条件与易错点

直觉上误以为需求繁荣期价格必然更高，忽视了卡特尔维持自律在繁荣期面临更高的激励相容约束；混淆显性明文串通与纯默契隐性卡特尔。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=9MtmH12aag4)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
垄断企业最脆弱的时刻往往不是萧条期，而是需求爆发的大繁荣期。因为当市场需求巨大时，单方面打折偷袭抢占全场订单的暴利实在太诱人，以至于长期的未来惩罚都无法压制当期的背叛冲动。聪明的反垄断法规通过重赏“第一个自首者”，在密谋者内部植入信任危机，从内部引爆隐性卡特尔。
:::
