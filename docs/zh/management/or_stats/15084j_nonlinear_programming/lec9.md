---
title: '等式约束流形搜索：投影梯度法与仿射投影 (Projection Methods)'
type: lecture
lecture: 9
tags: [projection-methods, projected-gradient, equality-constraints, null-space]
status: complete
---

# Lec 9 等式约束流形搜索：投影梯度法与仿射投影 (Projection Methods)

> MIT 15.084J / 6.252J 非线性规划 · 讲义 9 · 授课教师：Prof. Robert Freund

## TL;DR

- 线性等式约束将可行域锁定在欧氏空间的低维仿射子空间（Affine Subspace）。
- 投影矩阵 $P = I - A^T (A A^T)^{-1} A$ 将自由梯度精确投射到切空间中。
- 零空间法（Null-Space Method）彻底消除等式约束，实现降维自由无约束优化。

## 1. 仿射子空间与投影几何

在约束优化算法的发展史中，最先攻克的堡垒是**线性等式约束问题**：

$$\min_{x \in \mathbb{R}^n} \quad f(x) \quad \text{s.t.} \quad A x = b$$

其中 $A \in \mathbb{R}^{m \times n}$ 假设行满秩（$\operatorname{rank}(A) = m < n$）。
可行域 $\Omega = \{x \in \mathbb{R}^n \mid A x = b\}$ 是一个仿射流形（Affine Manifold），其几何维数精确为 $n - m$。

如果我们在当前可行点 $x_k$ 处直接沿着负梯度方向 $-\nabla f(x_k)$ 移动，只要该梯度不属于 $A$ 的零空间，新的点 $x_k - \alpha \nabla f(x_k)$ 就会立即脱离可行平面（$A(x_k - \alpha \nabla f) = b - \alpha A \nabla f \ne b$），瞬间违规不可行！
为了既能降低目标函数，又绝对不脱离约束流形，我们必须将负梯度向量**正交投影（Orthogonal Projection）到约束的切空间上**。

```mermaid
flowchart LR
    Grad[自由负梯度 -nabla f(x)] --> Projector[正交投影算子 P = I - A^T(A A^T)^-1 A]
    Projector --> ProjGrad[流形内切方向 d = -P nabla f(x)]
    ProjGrad --> FeasibleStep[新点 x+ = x + alpha * d 严格保持 Ax = b]
```

## 2. 投影梯度算子（Projected Gradient Operator）

切空间的代数定义是矩阵 $A$ 的零空间（Null Space）：
$$\operatorname{Null}(A) = \{d \in \mathbb{R}^n \mid A d = 0\}$$

根据基本线性代数定理，欧氏空间 $\mathbb{R}^n$ 可以正交分解为行空间与零空间之和：
$$\mathbb{R}^n = \operatorname{Range}(A^T) \oplus \operatorname{Null}(A)$$

对于任意给定的向量 $v \in \mathbb{R}^n$，我们要寻找它在 $\operatorname{Null}(A)$ 上的唯一正交投影 $d$：
$$d = \arg\min_{z} \quad \frac{1}{2} \|z - v\|_2^2 \quad \text{s.t.} \quad A z = 0$$

为该二次规划应用我们在第 7 讲学到的 KKT 条件：
$$z - v + A^T \lambda = 0 \implies z = v - A^T \lambda$$
两边左乘 $A$ 并代入 $A z = 0$：
$$A v - (A A^T) \lambda = 0 \implies \lambda = (A A^T)^{-1} A v$$
回代得到正交投影算子：
$$d = \left( I - A^T (A A^T)^{-1} A \right) v = P v$$

::: definition 正交投影矩阵与投影梯度法
定义**投影矩阵（Projection Matrix）**：
$$P = I - A^T (A A^T)^{-1} A$$
$P$ 具有两大代数刚性：对称性（$P^T = P$）与幂等性（$P^2 = P$）。
**投影梯度法（Projected Gradient Method）**的单步迭代公式为：
$$x_{k+1} = x_k - \alpha_k P \nabla f(x_k)$$
由于 $A (P \nabla f) = A \nabla f - A A^T (A A^T)^{-1} A \nabla f = 0$，只要初始点 $x_0$ 满足 $A x_0 = b$，后续所有的迭代点**绝对保真地永久驻留在流形内部**！
:::

## 3. 降维的艺术：零空间法（Null-Space Approach）

虽然投影矩阵 $P$ 形式极其优美，但在大规模计算中，每次乘法都要解 $(A A^T)^{-1}$ 依然存在矩阵开销。
更工业级的方案是**零空间基表示法（Null-Space Method / Reduced Gradient Method）**。

构造矩阵 $Z \in \mathbb{R}^{n \times (n-m)}$，使得其列向量张成 $A$ 的零空间正交基：
$$A Z = 0, \quad \operatorname{rank}(Z) = n - m$$
设 $x_0$ 为满足 $A x_0 = b$ 的任意特解。则可行域内任意点都可以唯一参数化为：
$$x(y) = x_0 + Z y, \quad y \in \mathbb{R}^{n-m}$$

将原约束问题代入该参数化表达，约束 $A x = b$ 被**彻底消灭**！
原问题等价降维为一个完全无约束的优化大题：
$$\min_{y \in \mathbb{R}^{n-m}} \quad \psi(y) = f(x_0 + Z y)$$

对降维目标函数应用链式法则：
$$\nabla_y \psi(y) = Z^T \nabla f(x) = g_z(x) \quad &&\text{(约化梯度 Reduced Gradient)}$$
$$\nabla_{yy}^2 \psi(y) = Z^T \nabla^2 f(x) Z = H_z(x) \quad &&\text{(约化海森矩阵 Reduced Hessian)}$$

在此子空间中，我们可以不受任何拘束地运行纯牛顿法、拟牛顿法（BFGS）或共轭梯度法，每一步只需在 $n-m$ 维空间中求解线性方程：
$$H_z(x_k) \Delta y = -g_z(x_k) \implies x_{k+1} = x_k + Z \Delta y$$

::: insight 维度压缩与流形自由行进
零空间法体现了运筹优化最崇高的工程智慧：**消灭约束的最好方式，是把约束本身变成坐标系**。
与其在全空间带着镣铐跳舞、每走一步就战战兢兢做一次流形投影，不如直接重构内在维度（Intrinsic Dimensions）。在航空飞行器轨迹优化和机器人动力学逆解中，零空间方法将上千条刚体铰链动力学等式压缩为几十个关节广义坐标，让复杂的流形动力学退化为自由空间的牛顿冲刺。
:::
