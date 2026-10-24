---
title: '内点法 II：仿射尺度法与原对偶路径跟踪算法 (Interior Point II: Primal-Dual Path)'
type: lecture
lecture: 21
tags: [path-following, primal-dual-interior-point, affine-scaling, newton-step]
status: complete
---

# Lec 21 内点法 II：仿射尺度法与原对偶路径跟踪算法 (Interior Point II: Primal-Dual Path)

> MIT 15.081J / 6.251J 数学规划导论 · 讲义 21 · 授课教师：Prof. Dimitris Bertsimas / John Tsitsiklis

## TL;DR

- 仿射尺度法通过对角缩放椭球椭球变换将当前点归一化到空间中心。
- 原对偶内点法（Primal-Dual IPM）联合对原变量 $x$、松弛 $s$ 与对偶 $p$ 同步执行牛顿更新。
- 预测-校正（Predictor-Corrector）两步架构大幅拓宽了单步下降步长，成为工业标准。

## 1. 坐标归一化与仿射尺度法（Affine Scaling）

如何让计算机高效沿着中心路径行进？最早的探索始于 1986 年由戴克（I. I. Dikin）提出并由万德贝（R. Vanderbei）等人复兴的**仿射尺度法（Affine Scaling Algorithm）**。

在标准型 LP $\min c^T x$ s.t. $Ax = b, x \ge 0$ 中，当前处于内部可行点 $x^k > 0$。如果直接沿着负目标方向 $-c$ 行进，很可能会非常突兀地撞到某个靠近原点的坐标轴边界（例如 $x_1 = 0$）而被迫停下极小的步长。
仿射尺度法的绝妙之处在于：定义对角标度矩阵 $X_k = \operatorname{diag}(x_1^k, \dots, x_n^k)$，做变量代换：
$$y = X_k^{-1} x \iff x = X_k y$$
在这个变换下，旧的当前点 $x^k$ 被极其完美地映射到了新坐标系的正中心单位向量：$y^k = \mathbf{1} = (1, 1, \dots, 1)^T$！
此时当前点距离所有的非负边界 $y_j = 0$ 拥有完全相等的安全裕度（距离均为 1）。在新空间中计算投影梯度方向，再通过 $X_k$ 逆映射回原空间，算法就能迈出巨大的下降步伐。

```mermaid
flowchart TD
    subgraph PrimalDualSystem [原对偶非线性系统 F(x, p, s) = 0]
        direction TB
        E1[原约束: A x - b = 0]
        E2[对偶约束: A^T p + s - c = 0]
        E3[双曲互补: X S 1 - sigma * mu * 1 = 0]
    end
    PrimalDualSystem -->|多元微积分一阶泰勒展开| Newton[牛顿雅可比线性系统 J * Delta = -F]
    Newton -->|求解稀疏对称正定增广阵| Steps[求得方向 Delta x, Delta p, Delta s]
    Steps -->|阻尼步长保持严格正值| Update[同步更新: x+ = x + alpha * Delta x]
```

## 2. 工业王牌：原对偶路径跟踪算法（Primal-Dual Path-Following）

尽管纯原仿射尺度法非常直观，但现代商业级内点求解器（如 Mosek, Gurobi, CPLEX）无一例外全部采用性能断层领先的**原对偶内点算法（Primal-Dual Interior-Point Method）**。

其核心思想是：**不再分别求解原问题或对偶问题，而是将原变量 $x \in \mathbb{R}^n$、松弛变量 $s \in \mathbb{R}^n$ 与对偶变量 $p \in \mathbb{R}^m$ 视为一个平等的复合大系统！**

中心路径方程定义了一个非线性方程组系统 $F(x, p, s) = 0$：
$$F(x, p, s) = \begin{bmatrix}
A x - b \\
A^T p + s - c \\
X S \mathbf{1} - \sigma \mu \mathbf{1}
\end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}, \quad (x > 0, s > 0)$$
其中 $X = \operatorname{diag}(x_1, \dots, x_n)$，$S = \operatorname{diag}(s_1, \dots, s_n)$，$\mu = \frac{x^T s}{n}$ 为平均对偶间隙，$\sigma \in [0, 1]$ 为居中向心参数（Centering Parameter）。

对这个非线性系统应用多元微积分的**牛顿-拉夫逊方法（Newton-Raphson Method）**，在当前点 $(x, p, s)$ 处展开一阶雅可比线性方程组：

$$\begin{bmatrix}
A & 0 & 0 \\
0 & A^T & I \\
S & 0 & X
\end{bmatrix} \begin{bmatrix}
\Delta x \\
\Delta p \\
\Delta s
\end{bmatrix} = -\begin{bmatrix}
A x - b \\
A^T p + s - c \\
X S \mathbf{1} - \sigma \mu \mathbf{1}
\end{bmatrix}$$

通过高斯块消元，第三行给出：$\Delta s = -X^{-1} S \Delta x - s + \sigma \mu X^{-1} \mathbf{1}$。
代入第二行并左乘 $A$ 矩阵，最终整个巨型系统被紧凑归结为一个对称正定的**正规方程组（Normal Equations）**：

$$\left( A D^2 A^T \right) \Delta p = r_p$$
其中 $D = S^{-1/2} X^{1/2}$ 为对角权重矩阵！
解出 $\Delta p$ 后，回代即可顺次求得 $\Delta s$ 与 $\Delta x$。

## 3. 梅罗特拉预测-校正器（Mehrotra's Predictor-Corrector）

1992 年，桑杰·梅罗特拉（Sanjay Mehrotra）提出了堪称内点法工业落地的圣经架构——**预测-校正算法（Predictor-Corrector）**：
1. **预测步（Affine Step, 令 $\sigma = 0$）**：纯粹探寻最优降落方向，计算如果不考虑中心化，单纯形步长最多能走多远；根据预测步衰减的剧烈程度，动态自适应判定当前最理想的向心因子 $\sigma = (\mu_{\text{affine}} / \mu)^3$；
2. **校正步（Corrector Step）**：利用二阶微积分交叉项 $\Delta X_{\text{aff}} \Delta S_{\text{aff}} \mathbf{1}$ 补偿泰勒展开遗留的高阶曲率误差，使得牛顿方向紧紧依附在中心路径的高速车道上，大幅避免触碰非负边界。

梅罗特拉算法的引入，使内点法在任意规模的工业规划中，通常**无论维度是 1 万还是 1000 万，都能以惊人恒定的 20 到 40 次牛顿迭代直接精准击穿最优解！**

::: insight 对称矩阵分解作为算力发动机
观察正规方程 $(A D^2 A^T) \Delta p = r$：
在内点法的几十次循环中，瓶颈只有一项——对对称正定矩阵 $M = A D^2 A^T$ 执行稀疏乔列斯基分解（Sparse Cholesky Factorization $M = L L^T$）。
更精妙的是：矩阵 $M$ 的非零元稀疏拓扑在所有迭代中完全不变，只有对角数值 $D$ 在变化！求解器只需在初始化阶段执行一次极高耗时的符号分解（Symbolic Factorization），随后每次迭代只需跑纯数值流水线。算法理论与底层芯片向量流水线在此达成了最高契合。
:::
