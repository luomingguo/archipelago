---
title: 资产定价：股票估值、红利折现与理性泡沫
type: lecture
lecture: 23
tags: [asset-pricing, stock-valuation, fundamental-value, rational-bubbles]
status: complete
source: 'https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/'
---

# Lec 23 资产定价：股票估值、红利折现与理性泡沫（Asset Pricing）

> MIT 14.02 · Principles of Macroeconomics · 主讲 Ricardo J. Caballero

## TL;DR

- 运用戈登股利折现模型（Gordon Growth Model）求解股票的基本面均衡价值。
- 区分基本面价格与资产价格泡沫（Asset Price Bubbles）：投机者寄希望于未来以更高价格转手的自洽信念。
- 探讨资产负债表渠道与资产价格繁荣-萧条周期对实体宏观经济的系统性外溢。

## 核心模型与推导

### 股票基本面现值模型

设股票每期支付股利 $D_t$，实际折现率为 $r$：
根据无套利条件，当期股价等于预期下一期股利与下一期售价的现值：
$$Q_t = \frac{D_{t+1}^e + Q_{t+1}^e}{1 + r}$$
通过向前递归迭代展开，得到**基本面价值（Fundamental Value）**：
$$Q_t^* = \sum_{k=1}^\infty \frac{D_{t+k}^e}{(1 + r)^k}$$

若假定股利以恒定增长率 $g$ 持续增长（戈登增长模型）：
$$Q_t^* = \frac{D_1}{r - g} \quad (r > g)$$

### 理性泡沫的数学形成
通解形式允许存在泡沫成分 $B_t$：
$$Q_t = Q_t^* + B_t$$
将通解代入无套利条件：
$$Q_t^* + B_t = \frac{D_{t+1}^e + Q_{t+1}^e}{1 + r} + \frac{B_{t+1}^e}{1 + r}$$
由于基本面部分自身满足方程，泡沫部分必须满足：
$$B_{t+1}^e = (1 + r) B_t$$
只要预期泡沫以不低于实际贴现率 $(1+r)$ 的速率几何级数膨胀，资产价格便可长期系统性偏离内在基本面，直到不可维持的临界点到来破裂。

## 经济机制与政策分析

面对资产价格泡沫，央行是否应当“迎风航行”（Leaning Against the Wind）进行先发制人加息？主流共识倾向于警惕：单纯用利率工具刺破泡沫代价过高（往往会误杀实体经济）；更为精准的武器是基于逆周期资本缓冲与贷款价值比（LTV）限制的宏观审慎政策（Macroprudential Policy）。

## 适用边界与易错点

混淆短期投机情绪驱动的股价噪音与未来长期贴现率改变引起的结构性估值重塑。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=dCJEeSD7hKk)
- [MIT 14.02 官方课程主页](https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/)
- [MIT 14.02 官方资源下载页](https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/download/)

::: insight
股票等风险资产的价格永远是对未来的折现。然而资产价格波动之烈，往往远超基础红利与宏观基本面的变化幅度。只要投资者预期明天能以更高价格转手，理性泡沫就能在数学上完全自洽地持续膨胀，直至信念崩塌的瞬间将整个银行体系拖入深渊。
:::
