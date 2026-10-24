---
title: '需求预测 I：时间序列平滑与自回归'
type: lecture
status: complete
tags: [demand-forecasting, time-series, exponential-smoothing]
---
# Lec 3 需求预测 I：时间序列平滑与自回归（Demand Forecasting I: Time Series Analysis）

## TL;DR

- 所有物流与库存决策的前提基石：理解需求信号的水平、趋势与季节性分解分解原理。
- 单指数平滑法（SES）到 Holt-Winters 双参数与三参数动态状态更新递推方程推导。
- 预测误差度量标尺：MAD、MSE、MAPE 与跟踪信号（Tracking Signal）系统性偏差诊断。

## 一、时间序列分解的核心数学架构

在物流系统运营中，未来的需求预测永远存在误差，但这绝不意味着预测毫无价值。科学的时间序列分析旨在将混杂在随机白噪声中的系统性规律过滤提取出来。

一个经典的时间序列需求观察值 $y_t$ 可以分解为四个核心成分的乘积或加法模型：
$$y_t = [L_t + T_t \cdot t] \cdot S_t + \epsilon_t$$
其中：
- $L_t$ 为基准水平（Level），代表当前时期的基础需求规模；
- $T_t$ 为线性趋势（Trend），代表每个周期固定增加或减少的需求斜率；
- $S_t$ 为季节性因子（Seasonal Factor），反映以年、季或周为周期的循环波动特征；
- $\epsilon_t$ 为均值为 0、方差为 $\sigma^2$ 的独立同分布随机误差（Random Noise）。

## 二、指数平滑方法族演进

### 1. 简单指数平滑法（Simple Exponential Smoothing, SES）
当数据不存在显著趋势和季节性，仅围绕基准水平上下波动时，采用单参数平滑：
$$\hat{y}_{t+1} = \alpha y_t + (1 - \alpha) \hat{y}_t = \hat{y}_t + \alpha (y_t - \hat{y}_t)$$
平滑系数 $\alpha \in (0, 1)$ 决定了历史记忆的衰减速度：$\alpha$ 越大，模型对最新一期的真实变动越敏感；$\alpha$ 越小，模型对随机噪音的滤波平滑能力越强。

### 2. Holt 双参数线性趋势平滑法
当需求存在持续上升或下降趋势时，单指数平滑会出现严重的系统性滞后。Holt 模型引入两个更新方程，分别追踪水平 $L_t$ 与趋势斜率 $T_t$：
$$L_t = \alpha y_t + (1 - \alpha)(L_{t-1} + T_{t-1})$$
$$T_t = \beta (L_t - L_{t-1}) + (1 - \beta) T_{t-1}$$
未来向前 $k$ 期预测值为：
$$\hat{y}_{t+k} = L_t + k \cdot T_t$$

### 3. Holt-Winters 三参数季节性平滑法（乘法模型）
当需求同时具备趋势和周期性季节波动（周期长度为 $p$）时，增加第三个季节因子平滑系数 $\gamma$：
$$L_t = \alpha \left( \frac{y_t}{S_{t-p}} \right) + (1 - \alpha)(L_{t-1} + T_{t-1})$$
$$T_t = \beta (L_t - L_{t-1}) + (1 - \beta) T_{t-1}$$
$$S_t = \gamma \left( \frac{y_t}{L_t} \right) + (1 - \gamma) S_{t-p}$$
未来 $k$ 期预测计算式为：
$$\hat{y}_{t+k} = (L_t + k \cdot T_t) \cdot S_{t - p + (k \bmod p)}$$

## 三、预测精度度量与跟踪信号（Tracking Signal）

评价预测模型优劣不能单看某一次的绝对偏差，必须构建严格的统计误差指标体系：

::: definition [常见预测误差指标定义]
设第 $t$ 期真实需求为 $y_t$，预测值为 $\hat{y}_t$，当期预测误差 $e_t = y_t - \hat{y}_t$：
1. **平均绝对偏差（Mean Absolute Deviation, MAD）**：
   $$MAD = \frac{1}{n} \sum_{t=1}^n |e_t|$$
2. **均方误差（Mean Squared Error, MSE）**：
   $$MSE = \frac{1}{n} \sum_{t=1}^n e_t^2$$
3. **平均绝对百分比误差（Mean Absolute Percentage Error, MAPE）**：
   $$MAPE = \frac{1}{n} \sum_{t=1}^n \left| \frac{e_t}{y_t} \right| \times 100\%$$
:::

在正态分布误差假定下，标准差与 MAD 之间存在换算常数：$\sigma \approx 1.25 \cdot MAD$。

::: pitfall [跟踪信号（Tracking Signal, TS）越界警报]
累积预测误差之和与 MAD 的比值定义为跟踪信号：
$$TS_t = \frac{\sum_{i=1}^t e_i}{MAD_t}$$
正常的无偏预测模型中，正负误差应该相互抵消，$TS_t$ 应当在 0 附近平稳震荡。一旦 $|TS_t| > 4$，表明预测模型已经出现了严重的**单向系统性系统偏置（Bias）**（持续低估或持续高估），必须立即介入重新校准参数或引入外部因果变量！
:::

## 我的理解

很多企业在做预测时陷入两个极端：要么盲目迷信深层复杂黑盒 AI 算法，要么完全依靠业务老销售的拍脑袋直觉。MIT 15.770J 展现了运筹统计学的从容与力量：Holt-Winters 这套经典的递推方程，逻辑透明、计算量轻微，能够完美拆解现实需求中的基准、增量与周期规律。更关键的是跟踪信号机制，它像一具警醒的仪表盘，在系统失偏的第一时间拉响警报，避免物流网络因为盲目乐观或悲观陷入全网瘫痪。
