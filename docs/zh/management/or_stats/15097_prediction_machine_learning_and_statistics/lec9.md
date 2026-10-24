---
title: '逻辑回归与广义线性模型：从几率比到指数族 (Logistic Regression and GLMs)'
type: lecture
lecture: 9
tags: [logistic-regression, generalized-linear-models, maximum-likelihood, irls]
status: complete
---

# Lec 9 逻辑回归与广义线性模型：从几率比到指数族 (Logistic Regression and GLMs)

> MIT 15.097 统计与机器学习前沿研讨 (Prediction: Machine Learning and Statistics) · 授课教师：Prof. Roy Welsch

## TL;DR

- 逻辑回归（Logistic Regression）通过 Sigmoid 对数几率映射将线性预测值约束在概率开区间 $(0, 1)$。
- 极大似然估计（MLE）推导出全局严格凸的交叉熵对数似然损失函数。
- 迭代加权最小二乘法（IRLS）与广义线性模型（GLM）统一了二项、泊松与高斯响应族。

## 突破普通线性回归的概率边界

在处理连续数值预测时，普通最小二乘法（OLS）是首选工具。然而，当我们面对**二分类决策问题**（例如患者是否患病 $y \in \{0, 1\}$、信用卡客户是否违约）时，若直接强行套用线性回归模型 $y = w^T x + b$：
1. **概率预测溢出（Out-of-Bounds）**：线性函数值域在 $(-\infty, +\infty)$，它会荒谬地预测出某位病人的患病概率为 $145\%$，或者预测另一位病人的概率为 $-32\%$；
2. **残差方差齐性破坏（Heteroscedasticity）**：二项分布的方差 $\text{Var}(Y \mid X) = p(X)(1 - p(X))$ 高度依赖于均值本身，使得 OLS 高斯马尔可夫定理彻底失效。

为了在保持线性特征组合解释性的同时，为概率预测建立坚固的数学物理边界，现代统计学诞生了最广泛使用的经典分类算法——**逻辑回归（Logistic Regression）**。

## Sigmoid 变换与对数几率比 (Odds Ratio)

我们引入几率（Odds）的概念：事件发生概率与不发生概率的比值：
$$
\text{Odds} = \frac{p}{1 - p} \in (0, +\infty)
$$
对几率取自然对数，即得出著名的**Logit 变换（对数几率）**：
$$
\text{logit}(p) = \ln\left(\frac{p}{1 - p}\right) \in (-\infty, +\infty)
$$
我们令对数几率严格等于特征的线性组合：
$$
\ln\left(\frac{p(x)}{1 - p(x)}\right) = w^T x + b
$$
两边求反解，瞬间导出整个深度学习与现代统计学的核心激活函数——**Sigmoid / Logistic 函数** $\sigma(z)$：
$$
p(x) = \mathbb{P}(Y = 1 \mid X = x) = \sigma(w^T x + b) = \frac{1}{1 + e^{-(w^T x + b)}}
$$

```mermaid
flowchart LR
    A["输入特征加权和: z = w^T x + b ∈ (-∞, +∞)"] --> B["Sigmoid 非线性激活映射: σ(z) = 1 / (1 + e^{-z})"]
    B --> C["输出严格良态后验概率: P(Y=1|X) ∈ (0, 1)"]
    C --> D["构建伯努利对数似然函数: ln L(w) = ∑ [y_i ln p_i + (1-y_i) ln(1-p_i)]"]
    D --> E["利用 Hessian 矩阵执行牛顿迭代 (IRLS) 极速秒级求出全局唯一最优参数 w*！"]
```

## 极大似然估计与对数交叉熵损失 (Cross-Entropy Loss)

设训练集为 $\mathcal{D} = \{(x_i, y_i)\}_{i=1}^n$，$y_i \in \{0, 1\}$。每个样本服从参数为 $p_i = \sigma(w^T x_i)$ 的独立伯努利分布。
全样本联合似然函数为：
$$
L(w) = \prod_{i=1}^n p_i^{y_i} (1 - p_i)^{1 - y_i}
$$
两边取自然对数，导出**对数似然函数（Log-Likelihood）**：
$$
\ell(w) = \ln L(w) = \sum_{i=1}^n \left[y_i \ln(p_i) + (1 - y_i) \ln(1 - p_i)\right]
$$
为了与最优化算法中的“求极小值”习惯统一，我们定义目标函数为**负对数似然损失（Negative Log-Likelihood / 二元交叉熵损失）**：
$$
J(w) = -\frac{1}{n}\ell(w) = -\frac{1}{n}\sum_{i=1}^n \left[y_i \ln(\sigma(w^T x_i)) + (1 - y_i) \ln(1 - \sigma(w^T x_i))\right]
$$

### 梯度的惊人优美性
由于 Sigmoid 函数具有神圣的导数性质 $\sigma'(z) = \sigma(z)(1 - \sigma(z))$，计算损失函数关于权重向量 $w$ 的一阶梯度：
$$
\nabla_w J(w) = \frac{1}{n}\sum_{i=1}^n \left(\sigma(w^T x_i) - y_i\right) x_i = \frac{1}{n} X^T (\mathbf{p} - \mathbf{y})
$$
计算其二阶 Hessian 矩阵：
$$
\mathbf{H}(w) = \nabla_w^2 J(w) = \frac{1}{n}\sum_{i=1}^n p_i (1 - p_i) x_i x_i^T = \frac{1}{n} X^T \mathbf{W} X
$$
其中权重对角矩阵 $\mathbf{W} = \text{diag}(p_1(1-p_1), \dots, p_n(1-p_n))$。
由于对所有样本恒有 $p_i \in (0, 1) \implies p_i(1-p_i) > 0$，只要设计矩阵 $X$ 列满秩，**Hessian 矩阵 $\mathbf{H}$ 在全实数空间中处处严格正定！**
这意味着负对数似然损失是一个**处处严格凸（Strictly Convex）的函数**，绝无任何虚假的局部极小值，全局最优解唯一存在！

## 迭代加权最小二乘算法 (IRLS)

求解该严格凸规划最强大的算法是**牛顿-拉夫逊法（Newton-Raphson）**：
$$
w^{(k+1)} = w^{(k)} - \mathbf{H}(w^{(k)})^{-1} \nabla J(w^{(k)}) = \left(X^T \mathbf{W}_k X\right)^{-1} X^T \mathbf{W}_k \mathbf{z}_k
$$
其中工作变量为调整后的工作响应 $\mathbf{z}_k = X w^{(k)} + \mathbf{W}_k^{-1} (\mathbf{y} - \mathbf{p}_k)$。
注意上式的右端形式：**它完全等价于一个加权最小二乘法（Weighted Least Squares, WLS）！**
因此该算法被称为**迭代加权最小二乘法（Iteratively Reweighted Least Squares, IRLS）**，通常在 4 到 6 步牛顿迭代之内即能达到机器双精度极值。

## 广义线性模型大一统架构 (GLM Framework)

1972 年约翰·内尔德（John Nelder）与罗伯特·韦德伯恩（Robert Wedderburn）提出了统计学历史上最著名的整合框架——**广义线性模型（Generalized Linear Models, GLM）**。
GLM 指出，只要响应变量 $Y$ 的条件概率分布属于**一维指数族分布（Exponential Family）**：
$$
f(y; \theta, \phi) = \exp\left(\frac{y \theta - b(\theta)}{a(\phi)} + c(y, \phi)\right)
$$
- 若分布为高斯分布：对应恒等连接（Identity Link $\theta = \mu$），即经典 OLS 回归；
- 若分布为伯努利二项分布：对应 Logit 连接（$\theta = \ln(\mu / (1-\mu))$），即逻辑回归；
- 若分布为泊松计数分布：对应对数连接（$\theta = \ln \mu$），即处理交通事故频次与网站点击量的 **Poisson 回归**；
- 若分布为 Gamma 分布：对应倒数连接（$\theta = -1/\mu$），即处理设备寿命与等待时间的 **Gamma 回归**。
全人类统计学百年来纷繁复杂的回归流派，在 GLM 的指数族框架下完成了壮美的大一统！

::: pitfall 完美分离（Complete Separation）导致的参数发散灾难
当某个特征能够将正负类 100% 毫无重叠地切开时（完美可分数据），极大似然估计会彻底崩溃：为了让预测概率无限逼近 1，权重向量模长会发散至无穷大（$\|w\| \to \infty$），导致求逆数值溢出。工业界必须无条件为逻辑回归施加 $L_2$（Ridge）或 $L_1$（Lasso）正则化惩罚！
:::

::: insight 几率比是将非线性概率关进线性笼子的驯兽缰绳
现实的概率只能在 $[0, 1]$ 之间脆弱地呼吸，稍有不慎就会越界崩溃；
而 Logit 变换展现了非凡的代数优雅：**通过对几率取对数，它把原本狭窄的概率区间，平滑拉伸至无穷无尽的负无穷到正无穷实数轴。在这个开阔的实数平原上，人类可以用最熟悉的线性微积分尽情纵横驰骋，并在终点通过一道 Sigmoid 闸门，将结果稳稳收敛回现实的概率世界**。
:::
