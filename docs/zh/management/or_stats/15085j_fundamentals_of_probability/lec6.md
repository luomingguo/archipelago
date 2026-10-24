---
title: '方差、协方差与条件期望的离散投影 (Discrete Variance & Conditional Expectation)'
type: lecture
lecture: 6
tags: [variance, covariance, conditional-expectation, total-variance-formula]
status: complete
---

# Lec 6 方差、协方差与条件期望的离散投影 (Discrete Variance & Conditional Expectation)

> MIT 15.085J / 6.436J 概率论基础 · 讲义 6 · 授课教师：Prof. John Tsitsiklis / Devavrat Shah

## TL;DR

- 方差 $\operatorname{Var}(X)$ 刻画随机波动能量，协方差矩阵度量高维随机矢量的仿射耦合。
- 条件期望 $\mathbb{E}[X \mid Y]$ 自身是一个依赖于观测 $Y$ 的全新随机变量。
- 全期望公式（Tower Property）与全方差分解公式将系统总方差优雅拆解为组间与组内方差。

## 1. 波动度量：二阶中心矩与方差（Variance）

在第 5 讲中，一阶期望 $\mathbb{E}[X]$ 锁定了随机变量的重心位置。然而，两个期望完全相同的系统，其微观风险特征可能天差地别：例如年化收益率期望同为 $8\%$ 的两只基金，一只波动率仅有 $2\%$（稳健国债组合），另一只每日经历 $40\%$ 的惊涛骇浪（加密货币杠杆）。

为了量化随机变量围绕其重心的离散发散程度，必须引入二阶统计量：

::: definition 方差与标准差 (Variance & Standard Deviation)
设随机变量 $X$ 满足 $\mathbb{E}[X^2] < \infty$。定义其**方差**为二次偏差的期望：
$$\operatorname{Var}(X) = \mathbb{E}\left[ (X - \mathbb{E}[X])^2 \right] = \mathbb{E}[X^2] - (\mathbb{E}[X])^2$$
其非负平方根 $\sigma_X = \sqrt{\operatorname{Var}(X)}$ 称为**标准差（Standard Deviation）**，其物理量纲与原变量保持严格一致。
:::

方差满足仿射缩放性质：$\operatorname{Var}(a X + b) = a^2 \operatorname{Var}(X)$（常数平移对波动无任何贡献）。

```mermaid
flowchart TD
    subgraph VarianceDecomposition [总方差分解定理: Eve's Law]
        TotalVar[总方差 Var X: 全局无条件总不确定性] --> ExpOfVar[期望方差 E[Var(X|Y)]: 平均观测后的不可消减残余方差]
        TotalVar --> VarOfExp[方差期望 Var(E[X|Y]): 观测变量 Y 对解耦预测所解释的波动解释力]
    end
    ExpOfVar & VarOfExp --> Sum[严格正交直和分解: Var X = E[Var(X|Y)] + Var(E[X|Y])]
```

## 2. 随机向量的代数拓扑：协方差矩阵（Covariance Matrix）

当研究多个随机变量构成的随机向量 $X = (X_1, \dots, X_n)^T$ 时，单一变量的方差无法捕捉跨分量的协同联动。

::: definition 协方差与相关系数
两个随机变量 $X, Y$ 的**协方差**定义为：
$$\operatorname{Cov}(X, Y) = \mathbb{E}[(X - \mathbb{E}[X])(Y - \mathbb{E}[Y])] = \mathbb{E}[X Y] - \mathbb{E}[X]\mathbb{E}[Y]$$
归一化无量纲指标为 **Pearson 相关系数**：
$$\rho_{XY} = \frac{\operatorname{Cov}(X, Y)}{\sigma_X \sigma_Y} \in [-1, 1]$$
:::

对于随机向量 $X \in \mathbb{R}^n$，定义其**协方差矩阵（Covariance Matrix）**：
$$\Sigma = \mathbb{E}\left[ (X - \mu)(X - \mu)^T \right] \in \mathbb{R}^{n \times n}, \quad \text{其中 } \Sigma_{ij} = \operatorname{Cov}(X_i, X_j)$$

::: theorem 协方差矩阵的对称半正定性
对于任意随机向量 $X$，其协方差矩阵 $\Sigma$ 必然是**实对称半正定矩阵**（$\Sigma \succeq 0$）！
:::
证明仅需一行二次型展开：对任意确定性向量 $a \in \mathbb{R}^n$：
$$a^T \Sigma a = a^T \mathbb{E}[(X - \mu)(X - \mu)^T] a = \mathbb{E}\left[ a^T (X - \mu)(X - \mu)^T a \right] = \mathbb{E}\left[ \left( a^T (X - \mu) \right)^2 \right] \ge 0$$
这一性质直接与我们在非线性规划第 23 讲学到的半正定锥 $\mathbb{S}_+^n$ 建立了完美的深层链接！

## 3. 条件期望：从数值跃迁为随机变量

在初等微积分中，条件期望常被写成一个数字：$\mathbb{E}[X \mid Y = y] = \sum x \mathbb{P}(X=x \mid Y=y)$。
但在高等测度论概率中，必须完成一次至关重要的认知跃迁：
**条件期望 $\mathbb{E}[X \mid Y]$ 不是一个常数，而是一个随着观测变量 $Y$ 的随机变动而变动的全新随机变量！**

定义函数 $g(y) = \mathbb{E}[X \mid Y = y]$。
那么，复合随机变量 $g(Y)$ 被记为 $\mathbb{E}[X \mid Y]$！它完全由 $Y$ 生成的信息代数 $\sigma(Y)$ 所支配。

::: theorem 塔式法则与全期望公式 (Tower Property)
$$\mathbb{E}\left[ \mathbb{E}[X \mid Y] \right] = \mathbb{E}[X]$$
通俗解释：**对所有可能出现的观测条件 $Y$ 进行期望加权平均，必然严格复原原变量的宏观无条件期望！**
:::

::: theorem 全方差公式 (Law of Total Variance / Eve's Law)
$$\operatorname{Var}(X) = \mathbb{E}\left[ \operatorname{Var}(X \mid Y) \right] + \operatorname{Var}\left( \mathbb{E}[X \mid Y] \right)$$
:::

这一公式在金融工程与机器学习中被誉为“圣经法则”：
1. 第一项 $\mathbb{E}[\operatorname{Var}(X \mid Y)]$：在知晓了 $Y$ 之后，系统内部遗留的**平均未解释方差（Unexplained Variance）**；
2. 第二项 $\operatorname{Var}(\mathbb{E}[X \mid Y])$：预测模型输出因变量随输入波动产生的**解释方差（Explained Variance）**！
它直接证明了：**任何观测信息 $Y$ 的引入，必然严格使得预测偏差的期望方差下降！信息永远是有价值的！**

::: insight 几何正交投影的微观萌芽
条件期望 $\mathbb{E}[X \mid Y]$ 是应用数学史上最伟大的设计之一。
在线性代数中，我们要逼近一个高维向量，最优的方式是向子空间做正交投影；
而在概率论的希尔伯特空间 $L^2(\Omega, \mathcal{F}, \mathbb{P})$ 中，条件期望正是**将任意随机变量 $X$ 正交投影到由观测信息张成的子空间 $\sigma(Y)$ 上的唯一最佳均方逼近点（MMSE Estimator）**！
全方差分解正是勾股定理（毕达哥拉斯定理）在无穷维随机函数空间的优雅显现。
:::
