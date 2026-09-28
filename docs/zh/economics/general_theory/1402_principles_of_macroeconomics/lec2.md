---
title: 国民收入核算与基本宏观概念
type: lecture
lecture: 2
tags: [national-accounts, gdp-measurement, inflation-rate, unemployment-rate]
status: complete
source: 'https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/'
---

# Lec 2 国民收入核算与基本宏观概念（Basic Macroeconomic Concepts）

> MIT 14.02 · Principles of Macroeconomics · 主讲 Ricardo J. Caballero

## TL;DR

- 国内生产总值（GDP）从生产法（增加值）、收入法与支出法三个等价维度进行核算。
- 严谨区分名义 GDP 与实际 GDP，通过 GDP 平减指数与消费者物价指数（CPI）度量通胀率。
- 阐明失业率与劳动参与率的定义边界，解析奥肯定律所揭示的产出增长与失业变动的经验关系。

## 核心模型与推导

### GDP 的三种核算方法

国内生产总值（GDP）是一个国家（或地区）在一定时期内生产的所有最终商品和服务的市场价值：

1. **支出法（Expenditure Approach）**：
   $$Y = C + I + G + NX$$
   - $C$：居民最终消费支出。
   - $I$：企业固定资本形成总额及存货投资。
   - $G$：政府购买商品与服务（不含转移支付）。
   - $NX = X - IM$：净出口（出口减进口）。

2. **生产法（增加值法, Value Added Approach）**：
   $$Y = \sum (\text{各行业总产出} - \text{中间投入})$$

3. **收入法（Income Approach）**：
   $$Y = \text{劳动报酬} + \text{营业盈余} + \text{固定资产折旧} + \text{生产税净额}$$

### 名义 GDP 与实际 GDP
- **名义 GDP（$Y_t$）**：用当期价格核算的产出，$Y_t = \sum P_{i,t} Q_{i,t}$。
- **实际 GDP（$Y_t^R$）**：用基期价格核算的产出，$Y_t^R = \sum P_{i,0} Q_{i,t}$。
- **GDP 平减指数**：$P_t = \frac{Y_t}{Y_t^R}$，通胀率为 $\pi_t = \frac{P_t - P_{t-1}}{P_{t-1}}$。

## 经济机制与政策分析

失业率指标需结合劳动参与率综合解读：经济极度萧条时，大量长期失业者退出劳动力市场成为“沮丧劳工”，可能导致名义失业率被动下降，掩盖了劳动力资源的实际闲置状况。

## 适用边界与易错点

混淆 GDP 与 GNP（国民生产总值）；误将政府转移支付（如社保救济）直接计入政府购买 $G$。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=kmUPK9AIE64)
- [MIT 14.02 官方课程主页](https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/)
- [MIT 14.02 官方资源下载页](https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/download/)

::: insight
GDP 核算的核心是“增加值”而非总交易额，避免了中间品重复计算。名义变量与实际变量的剥离是宏观思维的基石：福利改善只能来自商品与服务实际产量的提升，而非单纯由货币超发推动的价格通胀。
:::
