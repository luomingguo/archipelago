---
title: 数据探索与特征汇总
type: lecture
lecture: 3
tags: [summary-statistics, robust-statistics, simpsons-paradox, pearson-correlation, time-series-smoothing]
status: complete
source: 'https://ocw.mit.edu/courses/15-075j-statistical-thinking-and-data-analysis-fall-2011/resources/mit15_075jf11_chpt04/'
---

# Lec 3 数据探索与特征汇总（Summarizing Numerical Data）

> MIT 15.075J / ESD.07J · Statistical Thinking and Data Analysis · Fall 2011
> 授课教师：Prof. Cynthia Rudin
> 资料来源：[MIT OpenCourseWare Chapter 4 Notes](https://ocw.mit.edu/courses/15-075j-statistical-thinking-and-data-analysis-fall-2011/resources/mit15_075jf11_chpt04/)

## TL;DR

- 描述性统计量分为两类：对异常值敏感的代数统计量（均值 $\bar{x}$、样本方差 $s^2$）与具有抗噪鲁棒性的顺序统计量（中位数、四分位距 IQR）。
- 样本方差计算中必须除以自由度 $n-1$（贝塞尔修正），以修正由于使用样本均值 $\bar{x}$ 代替总体均值 $\mu$ 所导致的系统性低估。
- 辛普森悖论（Simpson's Paradox）揭示了宏观聚合数据可能彻底颠覆微观分层结论的机制，根源在于未受控的潜伏混杂变量及非均衡样本规模。
- 皮尔逊相关系数 $r \in [-1, 1]$ 仅度量双变量间的**线性关联系数**，绝不蕴含因果机制，且易受双峰聚类或离群点严重扭曲；分析前必须进行散点图可视化检验。

## 一、位置与分散度：敏感度 vs 稳健性

在拿到原始样本数据集后，第一步是通过一组精炼的数值特征刻画其位置中枢（Location）与离散程度（Dispersion）。

### 1. 均值与中位数的鲁棒性对比

::: definition [样本均值与中位数]
给定一组观测样本 $x_1, x_2, \dots, x_n$：
- **样本均值（Sample Mean）：**
  $$\bar{x} := \frac{1}{n}\sum_{i=1}^n x_i$$
- **样本中位数（Sample Median）：** 将数据按升序重排为次序统计量 $x_{(1)} \le x_{(2)} \le \dots \le x_{(n)}$：
  $$\tilde{x} := \begin{cases}
  x_{\left(\frac{n+1}{2}\right)}, & n \text{ 为奇数} \\
  \frac{1}{2}\left[x_{\left(\frac{n}{2}\right)} + x_{\left(\frac{n}{2} + 1\right)}\right], & n \text{ 为偶数}
  \end{cases}$$
:::

::: example [异常点对统计量的击穿效应]
考虑序列 $A = \{1, 2, 3, 4, 5\}$ 与序列 $B = \{1, 2, 3, 4, 500\}$：
- 序列 $A$：$\bar{x} = 3$，$\tilde{x} = 3$；
- 序列 $B$：仅仅将最后一个数替换为 500，均值暴增至 $\bar{x} = 102$（失真），而中位数依然稳健保持为 $\tilde{x} = 3$。
中位数具有 $50\%$ 的最高击穿点（Breakdown Point），在收入分布、房价统计和高噪声业务日志中比均值更具现实参考价值。
:::

### 2. 五数概括与四分位距（IQR）

为了全面展现数据的分位数结构，统计学采用**五数概括（Five-Number Summary）**：
$$\{x_{\min}, Q_1, Q_2, Q_3, x_{\max}\}$$
其中 $Q_1$ 为下四分位数（第 25 百分位数 $\theta_{0.25}$），$Q_2$ 为中位数（第 50 百分位数 $\theta_{0.5}$），$Q_3$ 为上四分位数（第 75 百分位数 $\theta_{0.75}$）。

- **全距（Range）：** $x_{\max} - x_{\min}$，极易受极值扰动。
- **四分位距（Interquartile Range, IQR）：**
  $$\operatorname{IQR} := Q_3 - Q_1$$
  IQR 测量了中间 $50\%$ 核心数据的跨度，具有高度抗噪性，常用于绘制盒须图（Boxplot）及定义离群点（通常定义落在 $[Q_1 - 1.5\operatorname{IQR}, Q_3 + 1.5\operatorname{IQR}]$ 之外的样本为离群值）。

### 3. 样本方差与自由度修正（Bessel's Correction）

::: definition [样本方差与样本标准差]
样本方差 $s^2$ 与样本标准差 $s$ 定义为：
$$s^2 := \frac{1}{n-1}\sum_{i=1}^n (x_i - \bar{x})^2, \quad s = \sqrt{s^2}$$
:::

::: theorem [自由度损失原理]
在计算平方离差和时，由于样本均值满足硬性约束 $\sum_{i=1}^n (x_i - \bar{x}) \equiv 0$，任意 $n-1$ 个离差项一旦确定，最后一个离差项即被完全锁定，因此自由调节的独立信息量（自由度）只有 $n-1$。若除以 $n$，则估计量会系统性低估总体方差 $\sigma^2$；除以 $n-1$ 保证了期望 $E[s^2] = \sigma^2$（即无偏估计）。
:::

- **变异系数（Coefficient of Variation, CV）：** $\operatorname{CV} = \frac{s}{\bar{x}}$，消除量纲影响，用于对比不同均值规模数据集的相对波动率。
- **标准分（z-score）：** $z_i = \frac{x_i - \bar{x}}{s}$，度量单点距离均值的标准差倍数。

---

## 二、双变量关联：相关性与辛普森悖论

### 1. 皮尔逊样本相关系数

::: definition [样本皮尔逊相关系数（Pearson Correlation）]
衡量两组连续变量 $X$ 与 $Y$ 间线性协同变化趋势的标准化指标：
$$r := \frac{S_{xy}}{S_x S_y} = \frac{\frac{1}{n-1}\sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\frac{1}{n-1}\sum_{i=1}^n (x_i - \bar{x})^2} \sqrt{\frac{1}{n-1}\sum_{i=1}^n (y_i - \bar{y})^2}} = \frac{1}{n-1}\sum_{i=1}^n \left(\frac{x_i - \bar{x}}{S_x}\right)\left(\frac{y_i - \bar{y}}{S_y}\right)$$
:::

数学性质：
1. $r \in [-1, 1]$，当且仅当所有数据点严格落在一条非水平直线上时达到 $\pm 1$。
2. 符号表示斜率方向（正相关 vs 负相关）。
3. $r$ 具有尺度不变性：对变量进行线性缩放（$aX+b, cY+d$，$ac>0$），相关系数数值保持不变。

::: pitfall [相关性陷阱：非线性、离群值与因果谬误]
1. **零相关不等于无关系：** 若 $Y = X^2$ 且 $X$ 对称分布在 $[-1, 1]$，二者存在完全确定的非线性函数关系，但计算所得 $r = 0$。
2. **相关性不蕴含因果性（Correlation does not imply Causation）：** 例如统计数据显示“财富增长与健康指标衰退存在显著相关”，实际背后存在共同驱动的潜伏变量——“年龄增长”。
:::

### 2. 辛普森悖论（Simpson's Paradox）深度剖析

::: definition [辛普森悖论]
在两个变量之间的关联模式，在各个独立子群中呈现同一方向（例如均为正），但将所有子群的数据合并后，该关联模式发生反转（变为负）的统计反常现象。
:::

::: example [经典临床案例：肾结石手术疗法疗效反转]
某医院针对两类结石患者（小结石与大结石）对比疗法 A（开腹手术）与疗法 B（微创介入）的治愈率：

| 病情细分 | 疗法 A 治愈率 | 疗法 B 治愈率 | 比较结论 |
| :--- | :--- | :--- | :--- |
| **小结石（轻症）** | **93%** ($81/87$) | 87% ($234/270$) | **疗法 A 更优** |
| **大结石（重症）** | **73%** ($192/263$) | 69% ($55/80$) | **疗法 A 更优** |
| **合并汇总（不分子群）**| 78% ($273/350$) | **83%** ($289/350$) | **反转！疗法 B 表现更优** |

**机制成因：**
1. 存在严重的混杂变量（结石大小）。大结石本身治愈难度极高（基准治愈率低），且医生倾向于将重症大结石患者安排做疗法 A（$263$ 例 vs 疗法 B 仅 $80$ 例）。
2. 疗法 B 分配的大多是极容易治愈的小结石轻症患者（$270$ 例）。
3. 简单合并汇总时，非均衡的样本权重导致疗法 A 的平均成功率被重症拖垮，造成宏观上的虚假优势。
:::

::: insight [规避辛普森悖论的方法论原则]
任何涉及决策对比的数据分析，必须先进行因果图梳理，检验是否存在影响干预分配的混杂变量。一旦存在关键分层特征，决策必须基于各细分层内的同质条件概率，严禁使用粗暴加权的大池汇总结论指导业务。
:::

---

## 三、时间序列特征与平滑预测

对于按时间先后顺序采集的序列数据 $x_1, x_2, \dots, x_T$，数据点之间通常存在时间自相关性。

### 1. 移动平均（Moving Averages, MA）

使用长度为 $w$ 的滑动时间窗口均值平滑高频随机噪声：
$$\operatorname{MA}_t := \frac{1}{w}\sum_{j=0}^{w-1} x_{t-j}$$
若以 $\hat{x}_t = \operatorname{MA}_{t-1}$ 作为未来预测值，单期预测误差定义为 $e_t = x_t - \hat{x}_t$。

**平均绝对百分比误差（Mean Absolute Percent Error, MAPE）：**
$$\operatorname{MAPE} := \frac{1}{T-1}\sum_{t=2}^T \left|\frac{e_t}{x_t}\right| \times 100\%$$
MAPE 消除了指标自身量纲与增长趋势的影响，度量相对预测误差精度（要求 $x_t \ne 0$）。

### 2. 指数加权移动平均（EWMA）

传统滑动窗口在移出窗口时会将历史数据彻底丢弃，而 EWMA 通过递推机制赋予历史更平滑的衰减权重：
$$\operatorname{EWMA}_t := \omega x_t + (1 - \omega)\operatorname{EWMA}_{t-1}$$
其中 $\omega \in (0, 1)$ 为平滑因子。将其递归展开：
$$\operatorname{EWMA}_t = \omega x_t + \omega(1-\omega)x_{t-1} + \omega(1-\omega)^2 x_{t-2} + \dots + (1-\omega)^t x_0$$
离当前越近的数据赋予越高的几何衰减权重，$\omega$ 越大表示对最新观测值越敏感。

### 3. 自相关系数（Autocorrelation Coefficient）

度量时间序列与其自身滞后 $k$ 期变量之间的线性依赖强度：
$$r_k := \frac{\sum_{t=k+1}^T (x_{t-k} - \bar{x})(x_t - \bar{x})}{\sum_{t=1}^T (x_t - \bar{x})^2}$$
自相关图（ACF）是识别时间序列季节性周期、趋势性以及检验残差白噪声特性的基础工具。
