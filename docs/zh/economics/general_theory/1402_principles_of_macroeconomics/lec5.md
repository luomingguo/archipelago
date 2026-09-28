---
title: IS-LM 联合均衡模型
type: lecture
lecture: 5
tags: [is-lm, macroeconomic-equilibrium, crowding-out, policy-mix]
status: complete
source: 'https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/'
---

# Lec 5 IS-LM 联合均衡模型（IS-LM Model）

> MIT 14.02 · Principles of Macroeconomics · 主讲 Ricardo J. Caballero

## TL;DR

- IS 曲线刻画商品市场均衡（产出与利率呈负相关关系）。
- LM 曲线刻画金融市场均衡（现代央行将政策利率设为目标值 $i = \bar{i}$）。
- 求解两市场联合均衡 $(Y^*, i^*)$，系统评估财政扩张引起的产出增长与潜在投资挤出。

## 核心模型与推导

### IS 曲线推导（商品市场均衡）
引入内生投资函数 $I = I(Y, i)$，其中 $\frac{\partial I}{\partial Y} > 0$（加速数效应），$\frac{\partial I}{\partial i} < 0$（资金成本效应）：
$$Y = C(Y - T) + I(Y, i) + G$$
当利率 $i$ 上升时，投资下降导致总需求下降，通过乘数效应使得均衡产出 $Y$ 降低。因此 IS 曲线在 $(Y, i)$ 空间向下倾斜。

### LM 曲线设定（金融市场均衡）
在现代央行通胀目标与利率走廊操作下，央行通过调整货币供给将利率稳定在目标水平：
$$i = \bar{i}$$
因此现代 LM 曲线表现为一条位于政策利率 $\bar{i}$ 处的水平线。

### 政策组合效应
1. **财政扩张（$\Delta G > 0$ 或 $\Delta T < 0$）**：
   IS 曲线向右移动，在政策利率维持 $\bar{i}$ 不变时，产出从 $Y_0$ 扩张至 $Y_1$，无利率挤出。
2. **货币宽松（$\bar{i}$ 下调）**：
   LM 曲线向下平移，沿 IS 曲线滑动，刺激投资与总产出扩张。

## 经济机制与政策分析

财政政策与货币政策的协同搭配（Policy Mix）是宏观调控的艺术。例如在应对经济滑坡时，扩张性财政与降息配合能实现产出最大化提升；而在赤字削减期，宽松货币政策可有效对冲财政紧缩对总需求的负面冲击。

## 适用边界与易错点

混淆曲线移动（由外生政策变量 $G, T, ar{i}$ 引致）与沿曲线移动（由内生变量 $Y, i$ 联动引致）。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=qg_HT3CjFI4)
- [MIT 14.02 官方课程主页](https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/)
- [MIT 14.02 官方资源下载页](https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/download/)

::: insight
IS-LM 模型的伟大之处在于把实体经济（商品市场）与金融虚拟经济（货币市场）通过利率 $i$ 和产出 $Y$ 编织进一个可解析的二维联立方程组。任何宏观冲击都不能孤立看待，必须在两个市场的交互反馈中寻找最终均衡。
:::
