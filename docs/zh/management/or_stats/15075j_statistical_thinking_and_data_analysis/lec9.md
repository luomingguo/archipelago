---
title: '一元线性回归与相关性'
type: lecture
lecture: 9
tags: [linear-regression, ordinary-least-squares, r-squared, gauss-markov-assumptions, coefficient-inference]
status: complete
source: 'https://ocw.mit.edu/courses/15-075j-statistical-thinking-and-data-analysis-fall-2011/resources/mit15_075jf11_chpt10/'
---

# Lec 9 一元线性回归与相关性（Simple Linear Regression and Correlation）

> MIT 15.075J / ESD.07J · Statistical Thinking and Data Analysis · Fall 2011
> 授课教师：Prof. Cynthia Rudin
> 资料来源：[MIT OpenCourseWare Chapter 10 Notes](https://ocw.mit.edu/courses/15-075j-statistical-thinking-and-data-analysis-fall-2011/resources/mit15_075jf11_chpt10/)

## TL;DR

- 一元线性回归模型 $Y_i = \beta_0 + \beta_1 x_i + \epsilon_i$ 将观测响应变量分解为**确定性线性信号**与**均值为零、方差恒定的独立高斯白噪声**。
- 普通最小二乘法（OLS）通过极小化残差平方和 $Q = \sum (y_i - \hat{y}_i)^2$，导出斜率参数解析解 $\hat{\beta}_1 = \frac{S_{xy}}{S_{xx}} = r \frac{S_y}{S_x}$，数学上直接体现为皮尔逊相关系数经尺度缩放后的投影。
- 方差分析（ANOVA）恒等式 $\operatorname{SST} = \operatorname{SSR} + \operatorname{SSE}$ 严密分解了总体变异度；判定系数 $R^2 = \frac{\operatorname{SSR}}{\operatorname{SST}} = r^2$ 量化了响应变量总变异中可被自变量线性解释的比例。

## 一、经典一元线性回归模型与高斯-马尔可夫假定

回归分析（Regression Analysis）旨在量化一个连续响应变量（因变量 $Y$）如何伴随一个或多个预测变量（自变量 $X$）的变动而发生系统性条件期望迁移。

设研究者给定了一组自变量的固定水平设置 $x_1, x_2, \dots, x_n$（在经典回归中视为确定性常量，非随机变量），并观测到对应的随机响应变量 $Y_1, Y_2, \dots, Y_n$：
$$Y_i = \beta_0 + \beta_1 x_i + \epsilon_i, \quad i = 1, \dots, n$$

::: definition [经典正态回归假定（Classical Normal Regression Assumptions）]
误差项 $\epsilon_1, \epsilon_2, \dots, \epsilon_n$ 满足以下四个核心假设：
1. **零均值假定：** $E[\epsilon_i] = 0$，保证条件期望满足线性形式 $E[Y_i \mid x_i] = \beta_0 + \beta_1 x_i$；
2. **同方差假定（Homoscedasticity）：** 对所有 $i$，误差方差恒定 $\operatorname{Var}(\epsilon_i) = \sigma^2$；
3. **无自相关假定（Uncorrelated）：** 当 $i \ne j$ 时，$\operatorname{Cov}(\epsilon_i, \epsilon_j) = 0$；
4. **正态性假定：** $\epsilon_i \overset{\text{i.i.d.}}{\sim} \mathcal{N}(0, \sigma^2) \implies Y_i \sim \mathcal{N}(\beta_0 + \beta_1 x_i, \sigma^2)$。
:::

---

## 二、普通最小二乘估计（OLS）的严密代数推导

为了在二维平面上寻找一条“拟合最优”的直线，高斯与勒让德提出了普通最小二乘准则（Ordinary Least Squares, OLS）：**寻找参数估计值 $(\hat{\beta}_0, \hat{\beta}_1)$，使得样本实际观测值 $y_i$ 与模型拟合线 $\hat{y}_i = \hat{\beta}_0 + \hat{\beta}_1 x_i$ 之间的垂直残差平方和达到全局最小**。

目标函数定义为二次损失函数：
$$Q(\beta_0, \beta_1) = \sum_{i=1}^n e_i^2 = \sum_{i=1}^n \big(y_i - (\beta_0 + \beta_1 x_i)\big)^2$$

### 1. 一阶极值条件（Normal Equations）

对目标函数分别关于 $\beta_0$ 和 $\beta_1$ 求偏导数，并令其等于 0：
$$\begin{aligned}
\frac{\partial Q}{\partial \beta_0} &= -2\sum_{i=1}^n \big(y_i - (\hat{\beta}_0 + \hat{\beta}_1 x_i)\big) = 0 \quad \implies \quad \sum_{i=1}^n y_i = n\hat{\beta}_0 + \hat{\beta}_1\sum_{i=1}^n x_i \\
\frac{\partial Q}{\partial \beta_1} &= -2\sum_{i=1}^n x_i \big(y_i - (\hat{\beta}_0 + \hat{\beta}_1 x_i)\big) = 0 \quad \implies \quad \sum_{i=1}^n x_i y_i = \hat{\beta}_0\sum_{i=1}^n x_i + \hat{\beta}_1\sum_{i=1}^n x_i^2
\end{aligned}$$

### 2. 闭式解的推导与均值穿透性

由第一个正规方程两边除以 $n$：
$$\bar{y} = \hat{\beta}_0 + \hat{\beta}_1 \bar{x} \implies \hat{\beta}_0 = \bar{y} - \hat{\beta}_1 \bar{x}$$

::: theorem [OLS 回归线均值穿透定理]
最小二乘回归直线必然无条件穿过样本质心点 $(\bar{x}, \bar{y})$。
:::

将 $\hat{\beta}_0$ 代入第二个正规方程消元整理：
$$\begin{aligned}
\sum_{i=1}^n x_i y_i &= (\bar{y} - \hat{\beta}_1 \bar{x})\sum_{i=1}^n x_i + \hat{\beta}_1\sum_{i=1}^n x_i^2 = n\bar{x}\bar{y} - \hat{\beta}_1 n\bar{x}^2 + \hat{\beta}_1\sum_{i=1}^n x_i^2 \\
\sum_{i=1}^n x_i y_i - n\bar{x}\bar{y} &= \hat{\beta}_1 \left(\sum_{i=1}^n x_i^2 - n\bar{x}^2\right)
\end{aligned}$$

引入经典离差平方和记号：
$$S_{xx} := \sum_{i=1}^n (x_i - \bar{x})^2 = \sum_{i=1}^n x_i^2 - n\bar{x}^2$$
$$S_{xy} := \sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y}) = \sum_{i=1}^n x_i y_i - n\bar{x}\bar{y}$$

由此推导出**斜率参数的经典解析解**：
$$\hat{\beta}_1 = \frac{S_{xy}}{S_{xx}} = \frac{\sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^n (x_i - \bar{x})^2} = r \frac{S_y}{S_x}$$
其中 $r = \frac{S_{xy}}{\sqrt{S_{xx}S_{yy}}}$ 是皮尔逊样本相关系数，$S_x, S_y$ 分别为各自的样本标准差。

将斜率代入回归方程，可写成高度对称的**标准化 z 形式**：
$$\frac{\hat{y} - \bar{y}}{S_y} = r \frac{x - \bar{x}}{S_x}$$

---

## 三、变异度分解定理与判定系数 $R^2$

为了量化模型对现实数据的解释能力，统计学将因变量的整体变异进行正交分解。

::: theorem [ANOVA 平方和正交分解恒等式]
$$\sum_{i=1}^n (y_i - \bar{y})^2 = \sum_{i=1}^n (\hat{y}_i - \bar{y})^2 + \sum_{i=1}^n (y_i - \hat{y}_i)^2$$
即：
$$\operatorname{SST} = \operatorname{SSR} + \operatorname{SSE}$$
:::

1. **总平方和（Total Sum of Squares, $\operatorname{SST}$）：** 衡量因变量 $y_i$ 脱离其样本均值的总波动，自由度为 $n - 1$；
2. **回归平方和（Regression Sum of Squares, $\operatorname{SSR}$）：** 衡量模型预测值 $\hat{y}_i$ 脱离均值的变异，即自变量 $X$ 成功解释的部分，自由度为 $1$；
3. **残差平方和（Error Sum of Squares, $\operatorname{SSE}$）：** 衡量真实值与预测线之间的垂直误差距离，即模型无法解释的随机噪声，自由度为 $n - 2$。

### 判定系数（Coefficient of Determination, $R^2$）

::: definition [判定系数 $R^2$]
$$R^2 := \frac{\operatorname{SSR}}{\operatorname{SST}} = 1 - \frac{\operatorname{SSE}}{\operatorname{SST}}$$
在一元线性回归中，判定系数严格等于样本皮尔逊相关系数的平方：$R^2 = r^2$。
:::

$R^2 \in [0, 1]$ 表达了响应变量 $Y$ 的总方差变异中，被自变量 $X$ 的线性回归模型所捕获并消除的百分比。

---

## 四、回归系数的统计推断与 t 检验

由于样本数据受到随机噪声 $\epsilon_i$ 的污染，计算出的估计量 $\hat{\beta}_1$ 本身也是一个随机变量。

### 1. 斜率估计量的抽样分布

将 $\hat{\beta}_1 = \sum w_i Y_i$（其中常数权重 $w_i = \frac{x_i - \bar{x}}{S_{xx}}$）展开：
1. **期望：** $E[\hat{\beta}_1] = \beta_1$（无偏估计）；
2. **方差：**
   $$\operatorname{Var}(\hat{\beta}_1) = \sum_{i=1}^n w_i^2 \operatorname{Var}(Y_i) = \sigma^2 \sum_{i=1}^n \left(\frac{x_i - \bar{x}}{S_{xx}}\right)^2 = \frac{\sigma^2}{S_{xx}}$$
3. 未知误差方差 $\sigma^2$ 的无偏估计量为**均方误差（Mean Squared Error）**：
   $$s^2 = \frac{\operatorname{SSE}}{n - 2} = \frac{1}{n-2}\sum_{i=1}^n (y_i - \hat{y}_i)^2$$

### 2. 斜率显著性 t 检验

检验预测变量 $X$ 与因变量 $Y$ 之间是否存在统计显著的线性关系：
$$\begin{cases}
H_0: \beta_1 = 0 \quad (\text{线性不相关}) \\
H_1: \beta_1 \ne 0
\end{cases}$$

构建检验统计量：
若计算出的 $|t| \ge t_{n-2, \alpha/2}$（或对应 $p \le \alpha$），则在 $\alpha$ 水平下拒绝 $H_0$，断定变量间存在显著的线性依存关系。

::: insight [高尔顿“均值回归”的统计本质]
弗朗西斯·高尔顿（Francis Galton）最早研究遗传数据时发现：高个子父母的子女往往比父母矮一点，而矮个子父母的子女往往比父母高一点，他将这一现象命名为“向均值回归”（Regression towards Mediocrity）。
从标准化的回归方程 $\frac{\hat{y} - \bar{y}}{S_y} = r \frac{x - \bar{x}}{S_x}$ 可以清晰看出：只要相关系数 $|r| < 1$（现实世界中几乎必然如此），自变量偏离其均值 1 个标准差时，因变量的条件期望仅仅偏离 $r$ 个标准差（$|r| < 1$ 产生了收缩效应）。这绝非神秘的生物遗传调控，而是数据受到不相关随机噪声扰动时的纯粹统计几何必然性。
:::
