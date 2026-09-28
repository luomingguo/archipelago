---
title: 扩展 IS-LM 模型：名义与实际利率、风险溢价与金融中介
type: lecture
lecture: 7
tags: [real-interest-rate, fisher-equation, risk-premium, financial-crises]
status: complete
source: 'https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/'
---

# Lec 7 扩展 IS-LM 模型：名义与实际利率、风险溢价与金融中介（An Extended IS-LM Model）

> MIT 14.02 · Principles of Macroeconomics · 主讲 Ricardo J. Caballero

## TL;DR

- 运用费雪方程式区分名义利率 $i$ 与实际借贷利率 $r = i - \pi^e$。
- 引入风险溢价 $x$，构建企业与居民面临的真实借贷利率 $r + x$。
- 解释金融中介资本金受损如何推高风险溢价 $x$，导致 IS 曲线剧烈左移引致金融危机。

## 核心模型与推导

### 费雪方程式与借贷利率
企业与家庭决策基于预期实际利率（Real Interest Rate）：
$$r \approx i - \pi^e$$
其中 $\pi^e$ 为预期通胀率。

实体部门进行投资借贷时，金融市场要求额外的风险溢价（Risk Premium）$x$：
$$\text{实际借贷成本} = r + x = i - \pi^e + x$$
- $x$ 取决于借款人违约风险、抵押品价值以及银行部门的杠杆率与资本充足率。

### 扩展 IS-LM 方程组
- **IS 关系**：
  $$Y = C(Y - T) + I(Y, i - \pi^e + x) + G$$
- **LM 关系**：
  $$i = \bar{i}$$

当金融机构爆发信用危机或坏账激增时，$x \uparrow$，即使央行维持政策利率 $\bar{i}$ 不变，实体借贷成本仍然飙升，导致投资断崖式下滑，IS 曲线向左剧烈收缩。

## 经济机制与政策分析

防范金融危机的政策核心在于救助系统重要性金融中介。央行充当最后贷款人提供紧急流动性、财政直接注资修复银行资本充足率，是压低风险溢价 $x$、阻止实体经济滑向深度衰退的关键操作。

## 适用边界与易错点

混淆央行政策利率 $i$ 与实体经济实际承担的综合借贷成本 $r+x$；忽视通缩预期（$\pi^e < 0$）会自动推高实际利率。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=fkiWQZPOHXk)
- [MIT 14.02 官方课程主页](https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/)
- [MIT 14.02 官方资源下载页](https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/download/)

::: insight
2008 年次贷危机的核心教训在于：央行政策利率哪怕降到了零，实体经济面对的实际借贷利率却可能因风险溢价的暴涨而急剧上升。金融中介是宏观经济的血液循环系统，资本金匮乏与流动性挤兑会直接摧毁投资需求。
:::
