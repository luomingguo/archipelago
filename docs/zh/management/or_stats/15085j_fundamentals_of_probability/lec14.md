---
title: '多元高斯向量：协方差正定性、正交投影与条件正态性 (Multivariate Normal Distributions)'
type: lecture
lecture: 14
tags: [multivariate-normal, gaussian-vectors, orthogonal-projection, conditional-gaussian]
status: complete
---

# Lec 14 多元高斯向量：协方差正定性、正交投影与条件正态性 (Multivariate Normal Distributions)

> MIT 15.085J / 6.436J 概率论基础 · 讲义 14 · 授课教师：Prof. John Tsitsiklis / Devavrat Shah

## TL;DR

- 多元高斯向量（Multivariate Gaussian）由其均值向量 $\mu$ 与对称半正定协方差阵 $\Sigma$ 唯一表征。
- 任意分量的线性组合依然严格服从高斯分布，仿射变换保持正态封闭性。
- 条件分布依然严格为高斯分布，条件期望精确等于线性最小均方误差正交投影。

## 1. 多元正态分布的公理化定义与特征向量

在多维随机向量的庞大家族中，**多元正态分布（Multivariate Normal / Gaussian Vector）**享有至高无上的尊荣地位。无论是在卡尔曼滤波（Kalman Filter）、计量经济学联立方程、还是机器学习高斯过程（Gaussian Processes）中，它都是无可替代的唯一物理假说。

设随机向量 $X = (X_1, \dots, X_n)^T \in \mathbb{R}^n$。
初学者常以为“每个分量 $X_i$ 是正态的，整个向量就是多元正态的”。
**这是大错特错的伪命题！**（存在两个边际分布为标准正态的变量，其联合支撑集集中在两条交叉直线上，联合分布根本非正态！）。

测度论给出的无瑕疵定义必须基于**全方向线性投影的一维正态性**：

::: definition 多元高斯随机向量
随机向量 $X \in \mathbb{R}^n$ 称为**多元高斯随机向量**，若对于**任意常数向量 $a \in \mathbb{R}^n$**，其标量线性组合 $a^T X = \sum_{i=1}^n a_i X_i$ 均服从一维标量正态分布（允许方差为 0 的退化正态分布）。
:::

定义其均值向量为 $\mu = \mathbb{E}[X] \in \mathbb{R}^n$，协方差矩阵为 $\Sigma = \mathbb{E}[(X - \mu)(X - \mu)^T] \in \mathbb{R}^{n \times n}$（$\Sigma \succeq 0$）。
记作：
$$X \sim \mathcal{N}(\mu, \Sigma)$$

```mermaid
flowchart TD
    subgraph GaussianProperties [多元高斯向量的核心代数刚性]
        Def[公理定义: 任意线性组合 a^T X 必为一维正态] --> Affine[仿射封闭性: Y = A X + b 严格服从 N(A mu + b, A Sigma A^T)]
        Affine --> Uncorr[不相关即独立: 若 Cov(Xi, Xj) = 0 则 Xi 与 Xj 严格统计独立!]
        Uncorr --> Cond[条件分布封闭: X1 | X2 依然严格为多元正态分布!]
    end
```

若协方差矩阵严格正定（$\Sigma \succ 0$，即 $\det(\Sigma) > 0$），多元高斯向量拥有平滑的联合概率密度函数：
$$f_X(x) = \frac{1}{(2\pi)^{n/2} \sqrt{\det(\Sigma)}} \exp\left( -\frac{1}{2} (x - \mu)^T \Sigma^{-1} (x - \mu) \right)$$

二次型 $(x - \mu)^T \Sigma^{-1} (x - \mu)$ 正是我们在非线性规划第 4 讲学到的**马氏距离（Mahalanobis Distance）**！等密度面在 $n$ 维欧氏空间中构成了一族轴向由 $\Sigma$ 特征向量锁定的同心超椭球面。

## 2. 划时代的特质：不相关即独立（Uncorrelated implies Independent）

在通用概率世界中，“协方差为零（不相关）”仅仅排除了线性相关，两者之间完全可能存在复杂的非线性依赖关系（如 $X \sim \mathcal{N}(0, 1), Y = X^2$）；
然而，在**联合高斯宇宙中，这是唯一的特例！**

::: theorem 高斯正交即独立定理
设 $X = (X_1, X_2)^T$ 联合服从多元高斯分布。
则随机向量 $X_1$ 与 $X_2$ **相互独立，当且仅当它们的协方差矩阵为零矩阵**：
$$\operatorname{Cov}(X_1, X_2) = 0$$
:::

证明仅需端详联合密度或矩母函数：当 $\Sigma_{12} = 0$ 时，协方差矩阵对角化为分块对角阵，马氏距离二次型在指数上完全解耦为独立加和：
$$\exp\left( -\frac{1}{2} x^T \Sigma^{-1} x \right) = \exp\left( -\frac{1}{2} x_1^T \Sigma_{11}^{-1} x_1 \right) \cdot \exp\left( -\frac{1}{2} x_2^T \Sigma_{22}^{-1} x_2 \right)$$
密度函数严格因式分解，独立性瞬间获证！

## 3. 条件高斯分布与舒尔补线性更新（Conditional Gaussians）

将多元高斯向量分块划分：
$$X = \begin{bmatrix} X_1 \\ X_2 \end{bmatrix} \sim \mathcal{N}\left( \begin{bmatrix} \mu_1 \\ \mu_2 \end{bmatrix}, \; \begin{bmatrix} \Sigma_{11} & \Sigma_{12} \\ \Sigma_{21} & \Sigma_{22} \end{bmatrix} \right)$$

当我们观测到分量 $X_2 = x_2$ 后，未观测分量 $X_1$ 的后验条件概率分布是什么？

::: theorem 高斯条件分布定理
条件分布 $X_1 \mid X_2 = x_2$ **依然严格是一个多元高斯分布**！
$$X_1 \mid X_2 = x_2 \sim \mathcal{N}\left( \mu_{1|2}, \; \Sigma_{1|2} \right)$$
其条件均值与条件协方差矩阵由如下公式解析给出：
1. **条件均值（后验最优估计）**：
$$\mu_{1|2} = \mathbb{E}[X_1 \mid X_2 = x_2] = \mu_1 + \Sigma_{12} \Sigma_{22}^{-1} (x_2 - \mu_2)$$
2. **条件协方差矩阵（后验不确定性）**：
$$\Sigma_{1|2} = \operatorname{Cov}(X_1 \mid X_2 = x_2) = \Sigma_{11} - \Sigma_{12} \Sigma_{22}^{-1} \Sigma_{21}$$
:::

注意观察条件协方差 $\Sigma_{1|2}$：
这正是我们在非线性规划第 23 讲学到的**舒尔补（Schur Complement）**！
更震撼的是：**条件协方差矩阵 $\Sigma_{1|2}$ 完全是一个确定性常数矩阵，它与观测到的具体数值 $x_2$ 毫无半点关系！**
不论你观测到的信号是 0 还是 100 万，系统的不确定性衰减幅度是完全恒定预知的！这就是卡尔曼滤波器（Kalman Filter）能够脱机离线预先计算 Riccati 方差更新方程的数学根源。

::: insight 希尔伯特空间投影的现实化身
多元高斯条件均值公式：$\mathbb{E}[X_1 \mid X_2] = \mu_1 + \Sigma_{12} \Sigma_{22}^{-1} (X_2 - \mu_2)$。
在广义随机变量中，最优均方估计（MMSE）通常是非线性极其复杂的抽象算子；
唯有在高斯世界里，**最优非线性估计，退化为了一个纯粹的、刚性的、可以用普通矩阵求逆计算的线性回归！**
非线性概率论的深奥难题，被高斯测度的完美旋转对称性，温顺地驯服为了本科生都可以轻松手算的线性代数。
:::
