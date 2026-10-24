---
title: '凸函数的充要特征与凸无约束最优性 (Convex Unconstrained Optimization)'
type: lecture
lecture: 2
tags: [convex-functions, convex-optimization, global-optimality, epigraph]
status: complete
---

# Lec 2 凸函数的充要特征与凸无约束最优性 (Convex Unconstrained Optimization)

> MIT 15.084J / 6.252J 非线性规划 · 讲义 2 · 授课教师：Prof. Robert Freund

## TL;DR

- 凸集与凸函数的公理化定义排除了任何多峰性与欺骗性局部鞍点陷阱。
- 一阶特征（支撑超平面）与二阶特征（海森半正定）确立了判定凸性的代数准则。
- 凸优化最高公理：在凸集上极小化凸函数，任意局部极小点必然是全局极小点！

## 1. 凸分析基石：凸集、凸函数与上图（Epigraph）

在第 1 讲中我们看到，对于通用非线性函数，局部极值无法向全局延展。为了打破这种局部盲人摸象的困境，现代优化理论建立在**凸分析（Convex Analysis）**的坚实基座之上。

::: definition 凸集与凸函数
1. **凸集（Convex Set）**：集合 $C \subset \mathbb{R}^n$ 称为凸集，若对任意两点 $x, y \in C$ 以及标量 $\lambda \in [0, 1]$，线段连线仍在集合内：$\lambda x + (1 - \lambda) y \in C$；
2. **凸函数（Convex Function）**：设定义域 $\operatorname{dom}(f) \subset \mathbb{R}^n$ 为凸集。函数 $f: \operatorname{dom}(f) \to \mathbb{R}$ 称为凸函数，若对任意 $x, y \in \operatorname{dom}(f)$ 及 $\lambda \in [0, 1]$，割线永远不低于函数值：
$$f(\lambda x + (1 - \lambda) y) \le \lambda f(x) + (1 - \lambda) f(y)$$
若当 $x \ne y$ 且 $\lambda \in (0, 1)$ 时严格不等式成立，则称 $f$ 为**严格凸函数（Strictly Convex）**。
:::

几何上，凸函数有一个极其优美且深刻的几何等价：函数 $f$ 的**上图（Epigraph）** $\operatorname{epi}(f) = \{(x, t) \in \mathbb{R}^{n+1} \mid t \ge f(x)\}$ 是高维空间中的一个凸集！这一几何对应使得分析函数的凸性完全转化为分析其几何几何体的凸性。

```mermaid
flowchart TD
    subgraph Convexity_Geometry [凸函数几何与代数三大等价]
        Def[割线几何: f(lambda x + (1-lambda)y) <= lambda f(x) + (1-lambda)f(y)]
        Grad[一阶切线支撑: f(y) >= f(x) + nabla f(x)^T (y - x)]
        Hess[二阶曲率全正: nabla^2 f(x) >= 0 对所有 x 恒半正定]
    end
    Def <--> Grad
    Grad <--> Hess
```

## 2. 凸函数的一阶与二阶微分充要判据

微积分赋予了我们极佳的代数工具，避免使用点对定义逐一验证凸性：

::: theorem 凸函数一阶充要条件 (First-Order Convexity Characterization)
设开凸集 $C \subset \mathbb{R}^n$ 上函数 $f$ 可微。则 $f$ 是凸函数当且仅当对任意 $x, y \in C$：
$$f(y) \ge f(x) + \nabla f(x)^T (y - x)$$
几何意义：**凸函数曲面在任意点处的切平面（仿射近似），恒位于整个函数曲面的下方！切平面是凸函数的全局支撑下界（Global Underestimator）！**
:::

::: theorem 凸函数二阶充要条件 (Second-Order Convexity Characterization)
设开凸集 $C \subset \mathbb{R}^n$ 上函数 $f \in C^2$。则：
1. $f$ 是凸函数，当且仅当其海森矩阵在定义域内处处半正定：
$$\nabla^2 f(x) \succeq 0, \quad \forall x \in C$$
2. 若海森矩阵在定义域内处处严格正定（$\nabla^2 f(x) \succ 0$），则 $f$ 必然是严格凸函数。
:::

## 3. 凸优化的核心定理：局部即全局

利用凸函数的一阶支撑性质，我们可以立即证明运筹学史上最伟大的基础定理：

::: theorem 凸优化全局最优定理
设 $f: \mathbb{R}^n \to \mathbb{R}$ 为凸函数。
1. 若 $x^*$ 是 $f$ 的局部极小点，则 $x^*$ **必然是 $f$ 的全局极小点**！
2. 驻点即全局最优：$x^*$ 是全局极小点，**当且仅当** $\nabla f(x^*) = 0$！
3. 若 $f$ 是严格凸函数，则全局最优解若存在，**必然唯一**！
:::

**证明极其优美**：
假设 $x^*$ 是驻点，即 $\nabla f(x^*) = 0$。根据一阶充要条件，对任意 $y \in \mathbb{R}^n$：
$$f(y) \ge f(x^*) + \nabla f(x^*)^T (y - x^*) = f(x^*) + 0^T (y - x^*) = f(x^*)$$
不等式 $f(y) \ge f(x^*)$ 对全空间每一个点都无条件成立，因此 $x^*$ 无懈可击地是全局最优解！

::: insight 凸性作为确定性计算的诺亚方舟
在非凸世界中，深度学习调参人员被数以亿计的局部极小值和马鞍面折磨得焦头烂额，模型性能全凭随机种子与运气；
而在凸优化的世界里，**局部信息直接拥有了洞穿全宇宙的穿透力**。你在当前点脚下测量出的零梯度，就是一个具有全局法律效力的证书，绝对证明整个定义域内没有任何地方能够超越当前解。这就是为什么应用数学家会不惜一切代价，通过变量代换、对偶变换或松弛，把一切工业模型向凸世界靠拢。
:::
