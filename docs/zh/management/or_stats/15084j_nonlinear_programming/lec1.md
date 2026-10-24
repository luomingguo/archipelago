---
title: '无约束优化的一阶与二阶最优性条件 (Unconstrained Optimization Optimality Conditions)'
type: lecture
lecture: 1
tags: [unconstrained-optimization, optimality-conditions, hessian-matrix, taylor-expansion]
status: complete
---

# Lec 1 无约束优化的一阶与二阶最优性条件 (Unconstrained Optimization Optimality Conditions)

> MIT 15.084J / 6.252J 非线性规划 · 讲义 1 · 授课教师：Prof. Robert Freund

## TL;DR

- 无约束极小值的一阶必要条件（Fermat 定理）要求梯度向量为零（驻点）。
- 二阶必要条件要求海森矩阵半正定（$\nabla^2 f \succeq 0$），正定则是严格局部极小值的充分条件。
- 多元泰勒展开将非线性曲面局部近似为二次型，奠定了所有局部下降搜索的理论基石。

## 1. 无约束非线性优化的数学抽象与局部极值

在连续优化领域，**无约束优化问题（Unconstrained Optimization）**是最基础、也最纯粹的形式化表述：

$$\min_{x \in \mathbb{R}^n} \quad f(x)$$

其中目标函数 $f: \mathbb{R}^n \to \mathbb{R}$ 通常假定为二次连续可微函数（$f \in C^2$）。在机器学习模型训练（如深度神经网络损失极小化、逻辑回归极大似然估计）、物理学能量极小化以及工程系统参数辨识中，无约束优化无处不在。

与线性规划可行域有界、极值必在边界极点取得不同，非线性函数的曲面可能存在极其复杂的起伏，呈现多峰性（Multimodality）、鞍点（Saddle Points）与退化山脊。

::: definition 局部极小值与全局极小值
1. **全局极小值点（Global Minimizer）**：若对于所有 $x \in \mathbb{R}^n$，均有 $f(x^*) \le f(x)$，则称 $x^*$ 为全局极小点；
2. **局部极小值点（Local Minimizer）**：若存在 $\varepsilon > 0$，使得对于所有满足 $\|x - x^*\| < \varepsilon$ 的邻域点，均有 $f(x^*) \le f(x)$，则称 $x^*$ 为局部极小点；若不等式为严格不等式（$x \ne x^*$ 时 $f(x^*) < f(x)$），则称其为**严格局部极小点**。
:::

```mermaid
flowchart LR
    subgraph FunctionProperties [微积分泰勒级数展开]
        Grad[一阶导数: 梯度向量 nabla f(x)]
        Hess[二阶导数: 海森矩阵 nabla^2 f(x)]
    end
    Grad -->|nabla f(x*) = 0| Stationary[一阶驻点 Stationary Point]
    Stationary --> Hess
    Hess -->|Hessian 正定 > 0| LocalMin[严格局部极小点]
    Hess -->|Hessian 负定 < 0| LocalMax[局部极大点]
    Hess -->|特征值有正有负| Saddle[非极值鞍点 Saddle Point]
```

## 2. 一阶与二阶最优性条件

利用多变量微积分的泰勒定理（Taylor's Theorem），在试探点 $x^*$ 附近沿任意方向 $d \in \mathbb{R}^n$ 展开：
$$f(x^* + d) = f(x^*) + \nabla f(x^*)^T d + \frac{1}{2} d^T \nabla^2 f(x^*) d + o(\|d\|^2)$$

根据该展开式，可系统导出分析学中最核心的极值判定准则：

::: theorem 一阶必要条件 (First-Order Necessary Condition, FONC)
设 $f: \mathbb{R}^n \to \mathbb{R}$ 在包含 $x^*$ 的开集上一阶连续可微。若 $x^*$ 是局部极小点，则梯度向量必然为零：
$$\nabla f(x^*) = 0$$
满足梯度的点称为**驻点（Stationary Point）**。
:::

::: theorem 二阶必要条件 (Second-Order Necessary Condition, SONC)
设 $f \in C^2$。若 $x^*$ 是局部极小点，则除梯度为零外，其海森矩阵（Hessian Matrix）必然是**半正定矩阵**：
$$\nabla f(x^*) = 0 \quad \text{且} \quad \nabla^2 f(x^*) \succeq 0$$
即对任意非零方向 $d \in \mathbb{R}^n$，均有 $d^T \nabla^2 f(x^*) d \ge 0$。
:::

::: theorem 二阶充分条件 (Second-Order Sufficient Condition, SOSC)
设 $f \in C^2$。若点 $x^*$ 满足梯度为零，且其海森矩阵为**严格正定矩阵**：
$$\nabla f(x^*) = 0 \quad \text{且} \quad \nabla^2 f(x^*) \succ 0$$
（即所有特征值严格大于零：$\lambda_{\min}(\nabla^2 f(x^*)) > 0$），则 $x^*$ 必然是 $f$ 的一个**严格局部极小点**！
:::

::: pitfall 半正定不能作为充分条件
初学者最常犯的逻辑错误，是把二阶必要条件当成充分条件。
反例：考察一维单变量函数 $f(x) = x^3$ 或 $f(x) = -x^4$。
在原点 $x = 0$ 处，$f'(0) = 0$ 且 $f''(0) = 0$（半正定成立）；
然而 $x = 0$ 在 $x^3$ 中是拐点，在 $-x^4$ 中更是局部的全局极大点！因此，当海森矩阵出现零特征值（奇异退化）时，必须考察更高阶导数或使用全局凸分析。
:::

::: insight 局部信息的局限性与算法宿命
微积分的二阶最优性条件本质上是在用一块二次抛物面贴合局部曲面。
在非凸优化中，计算机算法所能凭借的几乎只有局部的梯度与海森矩阵。这意味着算法在找到一个驻点时，哪怕验证了海森矩阵严格正定，也只能宣告“这是一个在微观邻域内无法继续改善的局部最优”，而无法回答十公里外是否存在深不见底的全局马里亚纳海沟。理解局部最优的这种本体论边界，是通往全局优化与凸分析的第一步。
:::
