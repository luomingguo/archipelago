---
title: '导出分布与变量代换：雅可比行列式与卷积微积分 (Derived Distributions & Jacobians)'
type: lecture
lecture: 12
tags: [derived-distributions, jacobian-determinant, convolution, coordinate-transform]
status: complete
---

# Lec 12 导出分布与变量代换：雅可比行列式与卷积微积分 (Derived Distributions & Jacobians)

> MIT 15.085J / 6.436J 概率论基础 · 讲义 12 · 授课教师：Prof. John Tsitsiklis / Devavrat Shah

## TL;DR

- 随机变量代换 $Y = g(X)$ 的测度映射严格遵循体积微元缩放守恒律。
- 多维光滑双射通过雅可比矩阵行列式（Jacobian Determinant）实现联合密度的精确变换。
- 独立随机变量之和的分布由其边际密度的卷积积分（Convolution）解析给出。

## 1. 变量代换的微元守恒律

在实际数据科学与物理推导中，我们往往只能直接观测到原始随机变量 $X$，而系统真正的最终输出是其经过非线性物理系统过滤后的派生随机变量：
$$Y = g(X)$$
例如：已知电路输入电压 $V \sim \mathcal{N}(0, \sigma^2)$，求电热功率 $P = I V = V^2 / R$ 的概率分布。

很多初学者容易犯一个极其低级的错误：随手写出 $f_Y(y) = f_X(g^{-1}(y))$。
**这是彻底荒谬的！概率密度不是无量纲的数，它具有物理量纲（测度/体积）！**

在单变量严格单调可微函数变换下，根据概率守恒原理：
$$\mathbb{P}(y < Y \le y + dy) = \mathbb{P}(x < X \le x + dx) \implies f_Y(y) |dy| = f_X(x) |dx|$$
由于 $dy = g'(x) dx$，移项立即导出**一维变量代换定理**：

::: theorem 一维随机变量代换定理
设 $X$ 为连续随机变量，$g: \mathbb{R} \to \mathbb{R}$ 为严格单调可微函数。则 $Y = g(X)$ 的概率密度为：
$$f_Y(y) = f_X(g^{-1}(y)) \cdot \left| \frac{d}{dy} g^{-1}(y) \right| = \frac{f_X(x)}{|g'(x)|} \Bigg|_{x = g^{-1}(y)}$$
:::

分母上的导数绝对值 $|g'(x)|$ 具有极其优美的物理意义：它度量了映射 $g$ 对局部体积微元的**拉伸与压缩率**！如果函数在某处极度陡峭（$|g'| \gg 1$），原本集中的微元被剧烈拉伸变稀薄，对应的概率密度必然大幅稀释下降。

```mermaid
flowchart TD
    subgraph MultiVarTransform [多维变量变换微元映射]
        X_domain[原始输入空间 R^n: 随机向量 X, 密度 f_X(x)] --> Mapping[光滑双射变换: y = g(x)]
        Mapping --> Y_domain[输出空间 R^n: 随机向量 Y]
        Mapping --> Det[计算雅可比矩阵行列式: J_g(x) = det [dy_i / dx_j]]
        Det --> Density[输出联合密度: f_Y(y) = f_X(g^-1(y)) * |det J_g^-1(y)|]
    end
```

## 2. 多维随机向量代换与雅可比行列式（Jacobian Determinant）

将这一几何守恒规律推广至高维空间 $\mathbb{R}^n$：
设向量映射 $Y = g(X) = (g_1(X), \dots, g_n(X))^T$ 在开集上是一对一双射，且连续可微。

定义映射 $g$ 的**雅可比矩阵（Jacobian Matrix）**：
$$J_g(x) = \frac{\partial(g_1, \dots, g_n)}{\partial(x_1, \dots, x_n)} = \begin{bmatrix}
\frac{\partial g_1}{\partial x_1} & \dots & \frac{\partial g_1}{\partial x_n} \\
\vdots & \ddots & \vdots \\
\frac{\partial g_n}{\partial x_1} & \dots & \frac{\partial g_n}{\partial x_n}
\end{bmatrix}$$

在多元微积分与微分几何中，雅可比矩阵的行列式绝对值 $|\det J_g(x)|$ 精确度量了超立方体体积微元在高维非线性扭曲映射下的**局部高阶体积缩放比**！

::: theorem 多维随机向量代换定理
设随机向量 $X \in \mathbb{R}^n$ 的联合密度为 $f_X(x)$。若映射 $y = g(x)$ 为双射，则输出随机向量 $Y$ 的联合概率密度为：
$$f_Y(y) = f_X(g^{-1}(y)) \cdot \left| \det J_{g^{-1}}(y) \right| = \frac{f_X(x)}{|\det J_g(x)|} \Bigg|_{x = g^{-1}(y)}$$
:::

::: example Box-Muller 变换：从均匀分布生成高斯白噪声
计算机硬件通常只能生成区间 $(0, 1)$ 上的独立均匀随机数 $U_1, U_2 \sim \text{Uniform}(0, 1)$。
如何生成完全独立的标准正态分布随机数 $Z_1, Z_2 \sim \mathcal{N}(0, 1)$？
Box 与 Muller 在 1958 年设计了基于雅可比代换的经典算法：
$$Z_1 = \sqrt{-2 \ln U_1} \cos(2\pi U_2), \qquad Z_2 = \sqrt{-2 \ln U_1} \sin(2\pi U_2)$$
计算其逆映射的雅可比行列式，行列式的值恰好等于 $\frac{1}{2\pi} \exp\left( -\frac{z_1^2 + z_2^2}{2} \right)$！
原本极其生硬的均匀随机数，瞬间解耦为两个完全独立的标准高斯白噪声！
:::

## 3. 独立和的代数结构：卷积公式（Convolution）

当两个随机变量是加法关系时（$Z = X + Y$），其代数结构尤为重要。

设 $X$ 和 $Y$ **相互独立**，联合密度为 $f_{XY}(x, y) = f_X(x) f_Y(y)$。
构造线性可逆变换：
$$\begin{cases} Z = X + Y \\ W = X \end{cases} \iff \begin{cases} X = W \\ Y = Z - W \end{cases}$$
雅可比矩阵为 $\begin{bmatrix} 0 & 1 \\ 1 & -1 \end{bmatrix}$，行列式模长为 $|\det J| = |-1| = 1$。
求出联合密度 $f_{ZW}(z, w) = f_X(w) f_Y(z - w)$。
通过对辅助变量 $w$ 积分（边缘化），立即导出分析学中的**连续卷积公式（Convolution）**：

::: theorem 独立和卷积定理 (Convolution Formula)
两个独立连续随机变量之和 $Z = X + Y$ 的概率密度，是两个独立边缘密度的**连续卷积**：
$$f_Z(z) = (f_X * f_Y)(z) = \int_{-\infty}^\infty f_X(x) f_Y(z - x) \, dx = \int_{-\infty}^\infty f_Y(y) f_X(z - y) \, dy$$
:::

::: insight 几何测度在函数空间中的无损传递
变量代换与卷积公式是测度论在坐标系中的优雅舞蹈。
雅可比行列式是守门员，严守着每一块微元测度的质量不增不减。
无论是信号在通信信道中的失真放大，还是多个独立随机误差的连续叠加，拉东-尼科迪姆导数伴随雅可比拉伸在空间中平滑传导。这种强烈的几何保真性，构筑了现代统计物理与信息论的计算中枢。
:::
