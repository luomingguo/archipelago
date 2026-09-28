---
title: 开放经济导论：商品与金融市场开放及汇率
type: lecture
lecture: 17
tags: [open-economy, exchange-rates, uncovered-interest-parity, balance-of-payments]
status: complete
source: 'https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/'
---

# Lec 17 开放经济导论：商品与金融市场开放及汇率（Introduction to Open Economy）

> MIT 14.02 · Principles of Macroeconomics · 主讲 Ricardo J. Caballero

## TL;DR

- 区分名义汇率 $E$ 与衡量国际商品相对价格的实际汇率 $\varepsilon = \frac{EP}{P^*}$。
- 建立经常账户与资本金融账户的国际收支恒等平衡关系。
- 推导未抵补利率平价（UIP），确立金融开放环境下国内名义利率与预期汇率变动的套利联系。

## 核心模型与推导

### 汇率定义与实际汇率

- **名义汇率（$E$）**：单位本币可兑换的外币数额（标价法定义：$E \uparrow$ 表示本币升值）。
- **实际汇率（$\varepsilon$）**：用本国商品篮子衡量外国商品篮子的相对价格：
  $$\varepsilon = \frac{E \cdot P}{P^*}$$
  - $P$ 为本国物价水平，$P^*$ 为外国物价水平。
  - $\varepsilon \uparrow$ 表示本国商品相对于外国商品变得昂贵，本国实际汇率升值（实际竞争力下降）。

### 国际金融市场与未抵补利率平价（UIP）
投资者在国内债券（收益率 $i_t$）与外国债券（收益率 $i_t^*$）之间权衡无套利均衡：
$$1 + i_t = (1 + i_t^*) \frac{E_t}{E_{t+1}^e}$$
取对数近似：
$$i_t \approx i_t^* - \frac{E_{t+1}^e - E_t}{E_t}$$
- **UIP 经济学含义**：国内名义利率必须等于外国名义利率加上预期本币贬值率。若国内利率高于外国，市场必须预期本币在未来发生贬值，以抹平无风险套利空间。

## 经济机制与政策分析

开放经济下的“不可能三角”（Mundellian Trilemma）宣告：一国无法同时实现资本自由流动、独立自主的货币政策以及固定汇率制。必须在三者中放弃其一，任何政策妄图兼得的尝试都会被投机资本冲垮。

## 适用边界与易错点

混淆直接标价法与间接标价法；误以为名义汇率升值必然等同于实际竞争力的全面恶化。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=5uygC4oJvCI)
- [MIT 14.02 官方课程主页](https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/)
- [MIT 14.02 官方资源下载页](https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/download/)

::: insight
开放经济引入了一记全新的自由度——汇率。实际汇率不仅决定了一国商品在国际市场上的竞争力，未抵补利率平价更将全球金融市场融为一体：一国央行如果试图独立决定国内利率，就必须随时准备承受汇率的剧烈反向补偿调整。
:::
