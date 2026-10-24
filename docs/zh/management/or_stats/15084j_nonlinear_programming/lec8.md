---
title: '约束优化最优性条件 III：二阶充分必要条件与临界锥曲率 (Constrained Optimality III)'
type: lecture
lecture: 8
tags: [second-order-conditions, critical-cone, border-hessian, strict-complementarity]
status: complete
---

# Lec 8 约束优化最优性条件 III：二阶充分必要条件与临界锥曲率 (Constrained Optimality III)

> MIT 15.084J / 6.252J 非线性规划 · 讲义 8 · 授课教师：Prof. Robert Freund

## TL;DR

- 一阶 KKT 仅能保证切平面合力为零，无法识别高阶鞍点与翻转极大值。
- 临界锥（Critical Cone）精确限制了所有一阶导数边际改善为零的敏感子空间。
- 拉格朗日函数海森矩阵在临界锥上的正定性构成了二阶充分条件的终极基准。

## 1. 一阶 KKT 的盲区：为什么必须引入二阶条件？

在无约束优化中，我们看到梯度为零（$\nabla f = 0$）只能保证驻点，必须凭借海森矩阵正定（$\nabla^2 f \succ 0$）才能百分之百断定为极小值。
在约束优化中，这一规律完全相同：**KKT 条件只是一阶线性近似的产物**。

想象一个球体放置在鞍形马鞍面上，曲面与一个约束平面相切：在切点处，KKT 力的平衡可能完美满足，但物体稍微沿着某一弯曲方向滑动，势能就会不可逆地倾泻崩溃！
为了判定一个 KKT 点究竟是真正的牢固极小点、还是危险的鞍点或局部极大点，必须考察**拉格朗日函数的二阶曲率（Curvature）在可行流形上的投影**。

```mermaid
flowchart TD
    subgraph SecondOrderLogic [二阶曲率判定链路]
        KKT[满足一阶 KKT 条件 (x*, mu*, lambda*)] --> Critical[构建临界锥 C(x*, mu*)]
        Critical --> Hessian[计算拉格朗日海森阵 nabla_xx^2 L]
        Hessian --> Check{对任意非零方向 d in C, d^T nabla_xx^2 L d 是否严格大于 0?}
        Check -- 是 --> Min[严格局部极小值充分条件 (SOSC) 成立!]
        Check -- 否且存在负值 --> NotMin[非极小值 (局部鞍点或极大点)]
    end
```

## 2. 临界锥（The Critical Cone）的几何定义

在二阶展开中，我们并不需要要求拉格朗日海森矩阵在全欧氏空间 $\mathbb{R}^n$ 上处处正定（这要求过强，往往直接退化为凸函数）。我们只需要关心那些**沿着它们行进既不会违背可行性、也不会引起一阶目标函数明显增大的方向**！

这些处于最优性剃刀边缘的方向构成了**临界锥（Critical Cone）**：

::: definition 临界锥 (Critical Cone)
设 $(x^*, \mu^*, \lambda^*)$ 满足 KKT 条件。临界锥 $C(x^*, \mu^*)$ 定义为满足以下条件的切向量集合：
$$C(x^*, \mu^*) = \left\{ d \in \mathbb{R}^n \;\middle|\; \begin{aligned}
\nabla h_j(x^*)^T d &= 0, \quad \forall j = 1, \dots, l \\
\nabla g_i(x^*)^T d &= 0, \quad \forall i \in A(x^*) \text{ 且 } \mu_i^* > 0 \\
\nabla g_i(x^*)^T d &\le 0, \quad \forall i \in A(x^*) \text{ 且 } \mu_i^* = 0
\end{aligned} \right\}$$
:::

注意观察不等式约束的精妙划分：
- 对于**强活动约束（$\mu_i^* > 0$）**：若方向 $d$ 使得 $\nabla g_i^T d < 0$，由于互补松弛性，一阶内积直接会导致目标函数增加；只有当 $\nabla g_i^T d = 0$ 时，该方向才不会立即脱离边界，必须在此方向上审查二阶导数；
- 对于**弱活动退化约束（$\mu_i^* = 0$）**：允许向可行域内部偏离（$\nabla g_i^T d \le 0$）。

在**严格互补性（Strict Complementarity）**成立的良态情形下（即所有活动约束乘子全部严格大于零 $\mu_i^* > 0$），临界锥退化为一个纯粹的**线性子空间（Linear Subspace）**！

## 3. 二阶必要条件与充分条件（SONC & SOSC）

记拉格朗日函数关于决策变量 $x$ 的海森矩阵为：
$$\nabla_{xx}^2 L(x^*, \mu^*, \lambda^*) = \nabla^2 f(x^*) + \sum_{i=1}^m \mu_i^* \nabla^2 g_i(x^*) + \sum_{j=1}^l \lambda_j^* \nabla^2 h_j(x^*)$$

::: theorem 二阶必要条件 (Second-Order Necessary Condition, SONC)
设 $x^*$ 为局部极小点，且满足 LICQ 约束规格。
设 $(x^*, \mu^*, \lambda^*)$ 满足 KKT 条件。则拉格朗日函数海森矩阵在整个临界锥上必然是**半正定的**：
$$d^T \nabla_{xx}^2 L(x^*, \mu^*, \lambda^*) d \ge 0, \quad \forall d \in C(x^*, \mu^*)$$
:::

::: theorem 二阶充分条件 (Second-Order Sufficient Condition, SOSC)
设 $(x^*, \mu^*, \lambda^*)$ 满足 KKT 条件。若拉格朗日函数海森矩阵在整个非零临界锥上是**严格正定的**：
$$d^T \nabla_{xx}^2 L(x^*, \mu^*, \lambda^*) d > 0, \quad \forall d \in C(x^*, \mu^*) \setminus \{0\}$$
则点 $x^*$ 必然是原约束优化问题的一个**严格局部极小点（Strict Local Minimizer）**！
并且，该局部极小点满足二阶强孤立性（Quadratic Growth Property）：存在常数 $\alpha > 0$，在其局部邻域内恒有 $f(x) \ge f(x^*) + \alpha \|x - x^*\|^2$。
:::

::: example 边框海森矩阵（Bordered Hessian）测试
对于仅含等式约束的系统（$\min f(x)$ s.t. $h(x) = 0$），将切空间约束与拉格朗日二阶项拼接在一起，构造经典的**边框海森矩阵（Bordered Hessian Matrix）**：
$$B = \begin{bmatrix} 0 & \nabla h(x^*)^T \\ \nabla h(x^*) & \nabla_{xx}^2 L(x^*, \lambda^*) \end{bmatrix}$$
通过考察边框海森矩阵的主子式符号交替规律，无需显式求解高维切空间，即可纯代数完成二阶充分条件的机械验证。
:::

::: insight 约束曲率对目标曲率的救赎与反噬
观察拉格朗日海森矩阵的构成：$\nabla^2 f + \sum \lambda_j \nabla^2 h_j$。
这里蕴含着非线性几何极度迷人的一幕：
即使原始目标函数在全空间是一个向下拉扯的凹函数（$\nabla^2 f \prec 0$），如果约束曲面是一个向外凸起的球壳（$\nabla^2 h \succ 0$），两者的叠加在切空间投影中完全可能变为严格正定！
约束曲面自身的几何弯曲，赋予了原本不稳定系统全新的结构刚性。反之，若约束曲面弯曲方向与目标相反，则会摧毁最优性。二阶条件正是这种“目标曲率与边界曲率相互对抗与补偿”的完美裁决书。
:::
