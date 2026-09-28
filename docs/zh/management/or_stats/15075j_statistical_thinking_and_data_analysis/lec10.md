---
title: 多元线性回归与模型诊断
type: lecture
lecture: 10
tags: [multiple-regression, multicollinearity, variance-inflation-factor, f-test, residual-diagnostics]
status: complete
source: 'https://ocw.mit.edu/courses/15-075j-statistical-thinking-and-data-analysis-fall-2011/resources/mit15_075jf11_chpt11/'
---

# Lec 10 多元线性回归与模型诊断（Multiple Linear Regression）

> MIT 15.075J / ESD.07J · Statistical Thinking and Data Analysis · Fall 2011
> 授课教师：Prof. Cynthia Rudin
> 资料来源：[MIT OpenCourseWare Chapter 11 Notes](https://ocw.mit.edu/courses/15-075j-statistical-thinking-and-data-analysis-fall-2011/resources/mit15_075jf11_chpt11/)

## TL;DR

- 多元线性回归将响应变量建模为 $k$ 个预测特征的线性组合：$Y_i = \beta_0 + \sum_{j=1}^k \beta_j x_{ij} + \epsilon_i$；回归系数 $\beta_j$ 的物理含义是**在控制其他所有特征固定不变的前提下，第 $j$ 个变量变动一个单位对响应变量的偏边际增量**。
- **总体显著性 F 检验**考察全模型是否存在任何有效信号（$H_0: \beta_1 = \dots = \beta_k = 0$），统计量为 $F = \frac{\operatorname{SSR}/k}{\operatorname{SSE}/(n-k-1)} \sim \mathcal{F}_{k, n-k-1}$。
- **多重共线性（Multicollinearity）**是回归建模的最大隐形杀手：当预测变量间存在高度线性自相关时，矩阵接近奇异，导致单个变量的系数估计方差急剧膨胀、符号反常且 t 检验失真；必须通过**方差膨胀因子（VIF）**进行诊断与剔除。

## 一、多元线性回归模型与矩阵表达

在管理科学与运筹决策中，现实经济现象（如某零售网点饮料销量、商品用户生命周期价值 LTV、员工离职倾向）极少能由单一指标解释。多元线性回归（Multiple Linear Regression, MLR）拓展了模型维度：

$$Y_i = \beta_0 + \beta_1 x_{i1} + \beta_2 x_{i2} + \dots + \beta_k x_{ik} + \epsilon_i, \quad i = 1, \dots, n$$

其中 $k$ 为自变量特征数，$n$ 为样本观测数（要求 $n > k + 1$）。误差项假设为 $\epsilon_i \overset{\text{i.i.d.}}{\sim} \mathcal{N}(0, \sigma^2)$。

### 1. 矩阵形式统一表述

将所有观测与参数矢量化：
$$\mathbf{Y} = \begin{bmatrix} Y_1 \\ Y_2 \\ \vdots \\ Y_n \end{bmatrix}, \quad
\mathbf{X} = \begin{bmatrix}
1 & x_{11} & x_{12} & \cdots & x_{1k} \\
1 & x_{21} & x_{22} & \cdots & x_{2k} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
1 & x_{n1} & x_{n2} & \cdots & x_{nk}
\end{bmatrix}, \quad
\boldsymbol{\beta} = \begin{bmatrix} \beta_0 \\ \beta_1 \\ \vdots \\ \beta_k \end{bmatrix}, \quad
\boldsymbol{\epsilon} = \begin{bmatrix} \epsilon_1 \\ \epsilon_2 \\ \vdots \\ \epsilon_n \end{bmatrix}$$

紧凑模型形式为：
$$\mathbf{Y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\epsilon}$$

### 2. 最小二乘正规方程与矩阵解

残差平方和目标函数写为向量内积：
$$Q(\boldsymbol{\beta}) = (\mathbf{Y} - \mathbf{X}\boldsymbol{\beta})^T (\mathbf{Y} - \mathbf{X}\boldsymbol{\beta}) = \mathbf{Y}^T\mathbf{Y} - 2\boldsymbol{\beta}^T\mathbf{X}^T\mathbf{Y} + \boldsymbol{\beta}^T\mathbf{X}^T\mathbf{X}\boldsymbol{\beta}$$

对矢量 $\boldsymbol{\beta}$ 求梯度并令其为零向量：
$$\nabla_{\boldsymbol{\beta}} Q = -2\mathbf{X}^T\mathbf{Y} + 2\mathbf{X}^T\mathbf{X}\hat{\boldsymbol{\beta}} = \mathbf{0} \implies \mathbf{X}^T\mathbf{X}\hat{\boldsymbol{\beta}} = \mathbf{X}^T\mathbf{Y}$$

当设计矩阵 $\mathbf{X}$ 满足列满秩（各特征线性无关）时，矩阵 $\mathbf{X}^T\mathbf{X}$ 可逆，导出**多元最小二乘估计量的唯一闭式解**：
$$\hat{\boldsymbol{\beta}} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{Y}$$

其协方差矩阵为：
$$\operatorname{Cov}(\hat{\boldsymbol{\beta}}) = \sigma^2 (\mathbf{X}^T\mathbf{X})^{-1}$$

---

## 二、模型适配度与总体显著性 F 检验

在多元回归中，单个系数的显著性 t 检验与全模型的综合解释力可能产生脱节，必须多层级协同评估。

### 1. 复判定系数（$R^2$）与调整判定系数（$R^2_{\text{adj}}$）

复判定系数依然定义为：
$$R^2 = \frac{\operatorname{SSR}}{\operatorname{SST}} = 1 - \frac{\operatorname{SSE}}{\operatorname{SST}}$$

::: pitfall [盲目增加特征导致伪 $R^2$ 虚高]
在多元线性回归中，哪怕强行往模型中塞入毫无逻辑关系的随机纯噪声特征，$R^2$ 的数值在数学上也**绝对不可能下降，只会单调递增**！这是因为二次投影在更大子空间上的残差平方和只会减小或不变。
:::

为了惩罚无意义的特征膨胀，必须引入考虑自由度的**调整后判定系数（Adjusted $R^2$）**：
$$R^2_{\text{adj}} := 1 - \frac{\operatorname{SSE}/(n - k - 1)}{\operatorname{SST}/(n - 1)} = 1 - (1 - R^2)\frac{n - 1}{n - k - 1}$$
仅当新引入的变量所带来的残差平方和降幅能够抵消自由度损失带来的惩罚时，$R^2_{\text{adj}}$ 才会上升。

### 2. 全模型总体显著性 F 检验

在解读具体特征之前，必须首先验证整个特征集合在宏观上是否蕴含任何真实预测能力：
$$\begin{cases}
H_0: \beta_1 = \beta_2 = \dots = \beta_k = 0 \quad (\text{所有特征均无解释力，仅截距起作用}) \\
H_1: \text{至少存在一个 } j \in \{1, \dots, k\} \text{ 使得 } \beta_j \ne 0
\end{cases}$$

构造基于方差分析的检验统计量：
$$F = \frac{\operatorname{SSR} / k}{\operatorname{SSE} / (n - k - 1)} = \frac{R^2 / k}{(1 - R^2) / (n - k - 1)} \sim \mathcal{F}_{k, n - k - 1}$$

若该 $F$ 检验的 $p$ 值大于 $\alpha$（未能拒绝 $H_0$），则整个回归模型全盘崩溃，底层没有任何具有统计显著性的真实信号。

---

## 三、多重共线性（Multicollinearity）深度诊断与应对

### 1. 共线性引发的数值灾难机制

当某两个或多个自变量之间存在极高的线性相关性时（例如在分析员工表现时，同时将“工作工龄（月数）”和“入职天数”作为并列自变量输入）：
1. 设计矩阵的 Gram 矩阵 $\mathbf{X}^T\mathbf{X}$ 接近奇异（条件数 Condition Number 极大）；
2. 逆矩阵 $(\mathbf{X}^T\mathbf{X})^{-1}$ 的对角线元素剧烈膨胀；
3. **严重恶果：** 估计量 $\hat{\beta}_j$ 的标准误 $\operatorname{SE}(\hat{\beta}_j) = \sqrt{\sigma^2 [(\mathbf{X}^T\mathbf{X})^{-1}]_{jj}}$ 极端巨大，导致各变量的 t 检验统计量极度微弱（全部显示 $p > 0.05$ 不显著），尽管全模型的 F 检验表现出极强的总体显著性（$p < 0.001$）。同时，系数估计值可能出现荒谬反常的正负符号颠倒。

### 2. 方差膨胀因子（Variance Inflation Factor, VIF）

::: definition [方差膨胀因子（VIF）]
针对第 $j$ 个预测变量 $X_j$，将其作为因变量、对其余所有 $k-1$ 个预测变量进行辅助线性回归，得到辅助拟合优度 $R_j^2$。定义：
$$\operatorname{VIF}_j := \frac{1}{1 - R_j^2}$$
:::

- **判定准则：**
  - $\operatorname{VIF}_j = 1$：该变量与其他变量完全正交独立；
  - $1 < \operatorname{VIF}_j < 5$：轻度多重共线性，通常无需处理；
  - $\operatorname{VIF}_j \ge 10$：存在严重且不可接受的多重共线性。
- **治理策略：**
  1. 人工剔除理论含义高度重叠的冗余变量；
  2. 采用主成分分析（PCA）降维重构正交潜因子；
  3. 引入收缩正则化方法（如岭回归 Ridge 或 ElasticNet）对矩阵施加 $L_2$ 惩罚。

---

## 四、经典残差诊断与高阶扩展

回归拟合完成后，必须通过**残差图（Residual Plots）**对底层的高斯-马尔可夫四项基本假定执行“体检”：

1. **残差 vs 拟合值散点图（$e_i \text{ vs } \hat{y}_i$）：**
   - 理想状态：残差随机散落在一个以 0 为中心的水平对称带内；
   - 若呈现明显的抛物线弯曲弯月形态：表明自变量与因变量之间存在非线性关系，需引入二次多项式项或对数变换 $\ln(Y)$；
   - 若呈现“漏斗状”喇叭口扩散形态：表明存在**异方差性（Heteroscedasticity）**，需采用加权最小二乘法（WLS）或稳健标准误（Huber-White Sandwich Estimator）。
3. **杠杆率（Leverage）与库克距离（Cook's Distance）：** 识别在自变量空间极其孤立且对回归斜率具有颠覆性主导权的强影响点（Influential Points）。

::: insight [偏回归系数的控制性释义与遗漏变量偏差]
多元回归系数 $\beta_j$ 的核心价值在于其“全控制性”（Ceteris Paribus）。然而，现实中未包含进模型的**遗漏变量（Omitted Variables）**若同时与自变量 $X_j$ 和因变量 $Y$ 相关，残差项 $\epsilon$ 将不再满足与 $X$ 正交的零协方差假定，从而导致回归系数估计量产生严重偏倚（Omitted Variable Bias）。因此，在将多元回归解释为因果杠杆前，必须通过因果识别框架（如工具变量法、双重差分法 DID 或断点回归 RDD）弥补观测数据的内生性缺陷。
:::
