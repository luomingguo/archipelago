---
title: 索洛增长模型：储蓄、资本积累与产出
type: lecture
lecture: 14
tags: [solow-model, capital-accumulation, steady-state, golden-rule]
status: complete
source: 'https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/'
---

# Lec 14 索洛增长模型：储蓄、资本积累与产出（Saving, Capital Accumulation, and Output）

> MIT 14.02 · Principles of Macroeconomics · 主讲 Ricardo J. Caballero

## TL;DR

- 建立不考虑技术进步的索洛模型基准框架：$Y = F(K, L)$ 具有规模报酬不变。
- 求解人均资本动态方程 $\dot{k} = s f(k) - \delta k$，确定经济长期稳态 $k^*$。
- 推导资本积累的黄金分割律水平（Golden Rule Level of Capital），平衡储蓄与人均消费。

## 核心模型与推导

### 索洛模型数学推导（无技术进步版）

设规模报酬不变生产函数 $Y = F(K, L)$，改写为人均形式：
$$y = \frac{Y}{L} = F\left(\frac{K}{L}, 1\right) \equiv f(k) \quad (f'(k) > 0, f''(k) < 0)$$
其中 $k \equiv \frac{K}{L}$ 为人均资本。

假定储蓄率 $s \in (0, 1)$，资本折旧率为 $\delta$：
- 人均投资：$i = s y = s f(k)$
- 人均折旧：$\delta k$
- 人均资本积累动态微分方程：
  $$\dot{k} = s f(k) - \delta k$$

### 稳态分析（Steady State, $\dot{k} = 0$）
$$s f(k^*) = \delta k^* \implies \frac{f(k^*)}{k^*} = \frac{\delta}{s}$$
稳态下，人均资本 $k^*$ 和人均产出 $y^* = f(k^*)$ 保持不变，总产出 $Y$ 增长率为 0。

### 黄金分割律（Golden Rule）
稳态人均消费为：
$$c^* = y^* - i^* = f(k^*) - \delta k^*$$
对 $k^*$ 求极值 $\frac{d c^*}{d k^*} = 0$：
$$f'(k_{\text{gold}}^*) = \delta$$
资本边际产出等于折旧率时的资本水平可使全社会长期人均消费最大化。若 $k^* > k_{\text{gold}}^*$，经济处于动态无效率状态（Dynamic Inefficiency）。

## 经济机制与政策分析

政策制定者切忌盲目追求高储蓄率。过度储蓄压榨了当代人的消费福祉，所积累的资本由于极端低效的边际产出甚至无法补偿高昂的折旧负担，反而导致后代人的稳态消费受损。

## 适用边界与易错点

混淆“产出水平效应”（储蓄率提高永久提升稳态收入）与“产出增长效应”（储蓄率提高仅短暂提升过渡期增长率）。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=VE4whF07w08)
- [MIT 14.02 官方课程主页](https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/)
- [MIT 14.02 官方资源下载页](https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/download/)

::: insight
索洛模型最震撼人心的结论是：提高储蓄率虽然能在过渡期推高增长率并永久提高稳态产出水平，但**资本积累本身绝不可能维持永久的长期增长**！由于资本边际报酬递减，新增投资最终只能刚好补偿旧资本折旧，增长率最终必定归零。
:::
