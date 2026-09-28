---
title: 短期商品市场与凯恩斯乘数
type: lecture
lecture: 3
tags: [goods-market, aggregate-demand, consumption-function, multiplier-effect]
status: complete
source: 'https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/'
---

# Lec 3 短期商品市场与凯恩斯乘数（The Goods Market）

> MIT 14.02 · Principles of Macroeconomics · 主讲 Ricardo J. Caballero

## TL;DR

- 短期内企业在固定物价水平下根据总需求组织生产，实现商品市场供求均衡 $Y = Z$。
- 消费函数采用线性设定 $C = c_0 + c_1(Y - T)$，边际消费倾向 $c_1 \in (0, 1)$。
- 推导自主支出乘数 $\frac{1}{1 - c_1}$，揭示外生投资或政府支出变动对总产出的放大效应。

## 核心模型与推导

### 商品市场总需求与均衡产出

总需求 $Z$ 由消费、投资和政府购买构成：
$$Z = C + I + G$$

假定短期内投资 $I$ 与政府支出 $G$、税收 $T$ 为外生给定：
$$C = c_0 + c_1(Y - T)$$
其中 $c_0 > 0$ 为自主消费，$c_1 \in (0, 1)$ 为边际消费倾向（Marginal Propensity to Consume, MPC）。

商品市场出清条件为产出等于总需求：
$$Y = Z = c_0 + c_1(Y - T) + I + G$$

整理求解均衡产出 $Y^*$：
$$(1 - c_1)Y = c_0 - c_1 T + I + G$$
$$Y^* = \frac{1}{1 - c_1} \left[ c_0 - c_1 T + I + G \right]$$

### 乘数分析
- **自主支出（Autonomous Spending）**：$[c_0 - c_1 T + I + G]$。
- **乘数（Multiplier）**：$\alpha = \frac{1}{1 - c_1} > 1$。
- 若政府购买增加 $\Delta G$，则产出增加 $\Delta Y = \frac{1}{1 - c_1} \Delta G$。

## 经济机制与政策分析

乘数效应意味着扩张性财政政策能有效撬动私人部门收入增长；但在现实中，税收比例化、进口漏损以及利率上升引致的投资挤出，都会使实际乘数远小于简单理论模型计算值。

## 适用边界与易错点

忘记消费取决于可支配收入 $(Y - T)$ 而非总收入 $Y$；误认为乘数效应在供给受限的中长期依然成立。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=fxrwTj2i_S4)
- [MIT 14.02 官方课程主页](https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/)
- [MIT 14.02 官方资源下载页](https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/download/)

::: insight
凯恩斯乘数效应本质上反映了经济系统内部收入与支出的正反馈循环。只要边际消费倾向小于 1，这个无限几何级数就必定收敛，保证了宏观经济体系在遭受局部外生冲击时不至于无底线发散，从而具有内在均衡点。
:::
