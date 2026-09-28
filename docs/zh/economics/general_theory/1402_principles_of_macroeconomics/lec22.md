---
title: 金融市场与预期：收益率曲线与期限结构
type: lecture
lecture: 22
tags: [expectations, yield-curve, term-structure, pure-expectations-hypothesis]
status: complete
source: 'https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/'
---

# Lec 22 金融市场与预期：收益率曲线与期限结构（Financial Markets and Expectations）

> MIT 14.02 · Principles of Macroeconomics · 主讲 Ricardo J. Caballero

## TL;DR

- 引入现值折现理论与理性预期框架：资产价格是未来预期现金流的贴现和。
- 基于纯预期假说（Pure Expectations Hypothesis）推导长期债券收益率与预期未来短期利率的关系。
- 剖析收益率曲线倒挂（Inverted Yield Curve）作为经济衰退先行指标的宏观机制。

## 核心模型与推导

### 债券价格与收益率

考虑一张面值为 $\$100$ 的 2 年期零息国债：
- 其当期价格为 $P_{2t}$。
- 2 年期年化到期收益率 $i_{2t}$ 定义为：
  $$P_{2t} = \frac{100}{(1 + i_{2t})^2}$$

### 纯预期理论（Expectations Hypothesis）
投资者在以下两种策略之间无套利套换：
1. 持有一张 2 年期债券至到期，年化期望收益率 $1 + i_{2t}$。
2. 先持有 1 年期债券（收益率 $i_{1t}$），到期后再将本息滚入下一年 1 年期债券（预期收益率 $i_{1,t+1}^e$）。

无套利条件：
$$(1 + i_{2t})^2 = (1 + i_{1t})(1 + i_{1,t+1}^e)$$
取对数近似：
$$i_{2t} \approx \frac{1}{2}\left( i_{1t} + i_{1,t+1}^e \right)$$
推广至 $n$ 期债券：
$$i_{nt} \approx \frac{1}{n} \sum_{k=0}^{n-1} i_{1,t+k}^e + \text{期限溢价 } \theta_n$$

### 收益率曲线倒挂
通常情况下，期限溢价 $\theta_n > 0$ 且经济平稳增长，曲线向上倾斜（$i_{2t} > i_{1t}$）。
当市场强烈预期央行在未来因严重衰退而不得不激进降息（即 $i_{1,t+1}^e \ll i_{1t}$）时，短端利率高于长端利率，导致曲线倒挂（$i_{1t} > i_{2t}$），成为经典的宏观衰退先兆信号。

## 经济机制与政策分析

中央银行的前瞻性指引（Forward Guidance）正是通过直接管理市场对未来短期利率的预期序列 $i_{1,t+k}^e$，从而在短期名义利率已触及 ZLB 的窘境下，依然能够成功压低长期借贷收益率，维系金融宽松环境。

## 适用边界与易错点

将债券价格上涨与债券收益率上升相混淆；忽视期限溢价对预期推断的干扰。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=csWwk_MOLww)
- [MIT 14.02 官方课程主页](https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/)
- [MIT 14.02 官方资源下载页](https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/download/)

::: insight
收益率曲线是金融市场对未来宏观经济走势最深邃的水晶球。长端利率不是短期利率的简单搬运，而是内嵌了市场全行业对未来数年央行降息预期与经济衰退概率的集体共识。收益率倒挂之所以屡屡准确预言危机，正是市场对即将来临的经济硬着陆投下的恐慌选票。
:::
