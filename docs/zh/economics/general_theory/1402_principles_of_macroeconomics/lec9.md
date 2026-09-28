---
title: 菲利普斯曲线与通货膨胀预期演变
type: lecture
lecture: 9
tags: [phillips-curve, inflation-expectations, adaptive-expectations, stagflation]
status: complete
source: 'https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/'
---

# Lec 9 菲利普斯曲线与通货膨胀预期演变（The Phillips Curve and Inflation）

> MIT 14.02 · Principles of Macroeconomics · 主讲 Ricardo J. Caballero

## TL;DR

- 结合 WS 和 PS 曲线推导连接通胀率、预期通胀与失业率的菲利普斯曲线。
- 回顾 1960 年代原始菲利普斯曲线（通胀与失业的稳定反向替代关系）的破灭。
- 引入适应性预期模型 $\pi_t^e = \theta \pi_{t-1}$，解释 1970 年代滞胀与加速通胀菲利普斯曲线的形成。

## 核心模型与推导

### 菲利普斯曲线的推导

将工资设定 $W = P^e (1 - \alpha u + z)$ 代入价格设定 $P = (1 + m)W$：
$$P = P^e (1 + m)(1 - \alpha u + z)$$
两边取自然对数并利用近似公式 $\ln(1+x) \approx x$，得到现代菲利普斯曲线：
$$\pi_t = \pi_t^e + (m + z) - \alpha u_t$$

当失业率处于自然失业率 $u_n$ 时，$\pi_t = \pi_t^e$，故 $0 = (m + z) - \alpha u_n \implies u_n = \frac{m + z}{\alpha}$。
代入重写为：
$$\pi_t - \pi_t^e = -\alpha (u_t - u_n)$$

### 预期形成机制的变迁
1. **1960 年代以前（原始菲利普斯曲线）**：
   通胀低且无持久性，公众假定 $\pi_t^e = 0$，得到失业与通胀水平的直接负向替代：
   $$\pi_t = -\alpha (u_t - u_n)$$
2. **1970 年代滞胀期（加速通胀菲利普斯曲线）**：
   通胀高企，公众形成自适应预期 $\pi_t^e = \pi_{t-1}$：
   $$\pi_t - \pi_{t-1} = -\alpha (u_t - u_n)$$
   政府若试图将失业率维持在 $u_n$ 之下，代价不是一次性高通胀，而是通胀率的无休止加速上升！

## 经济机制与政策分析

央行信誉与通胀预期的锚定至关重要。实施通胀目标制（Inflation Targeting）的根本目的就是建立可靠的制度承诺，使公众预期 $\pi_t^e$ 稳定在 2% 的目标锚点，从而隔绝供给冲击对工资-物价螺旋的传导。

## 适用边界与易错点

混淆通胀水平上升与通胀变动率（加速）之间的数学区别；忽视预期形成方式的内生性改变。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=mhqsslG9tyw)
- [MIT 14.02 官方课程主页](https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/)
- [MIT 14.02 官方资源下载页](https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/download/)

::: insight
菲利普斯曲线的历史是宏观经济学关于“预期”的最生动洗礼。当通胀维持低位时，公众预期锚定在零，政策制定者享受了低失业与微弱通胀的蜜月；但一旦政府试图长期利用这一替代关系，公众通胀预期迅速脱锚，最终在 1970 年代酿成了失业与通胀齐飞的滞胀灾难。
:::
