---
title: '凸函数深度剖析：次梯度、共轭函数与 Fenchel 对偶 (Analysis of Convex Functions)'
type: lecture
lecture: 17
tags: [subgradient, subdifferential, conjugate-functions, fenchel-duality, non-smooth]
status: complete
---

# Lec 17 凸函数深度剖析：次梯度、共轭函数与 Fenchel 对偶 (Analysis of Convex Functions)

> MIT 15.084J / 6.252J 非线性规划 · 讲义 17 · 授课教师：Prof. Robert Freund

## TL;DR

- 次梯度（Subgradient）将微分导数概念推广至不可微凸曲面的折角与尖点。
- 次微分集合 $\partial f(x)$ 是紧致非空凸集，驻点条件推广为 $0 \in \partial f(x^*)$。
- 勒让德-芬切尔变换（Fenchel Conjugate）将原函数映射至斜率对偶空间，揭示非线性对偶终极奥义。

## 1. 突破平滑性的束缚：次梯度与次微分（Subgradients）

在现实优化问题中，大量极具实用价值的目标函数并非处处平滑可微：
- 机器学习中的稀疏正则项：$L_1$ 范数 $f(x) = \|x\|_1 = \sum |x_i|$ 在坐标轴上存在锋利的尖角；
- 鲁棒控制中的分段最大值：$f(x) = \max_{i} (a_i^T x + b_i)$ 在交汇脊线上导数断裂；
- 支持向量机（SVM）中的铰链损失（Hinge Loss）：$f(x) = \max(0, 1 - y x)$。

在这些不可微的尖点处，传统的连续梯度 $\nabla f(x)$ 瞬间不复存在。我们如何在这类非光滑曲面上寻找极小值？
凸分析大师让·雅克·莫罗（Jean Jacques Moreau）与拉尔夫·洛卡费勒（R. Tyrrell Rockafellar）创立了**次微分微积分（Subdifferential Calculus）**。

在第 2 讲中，凸函数的一阶充要特征是：切线永远在函数曲面下方。
次梯度的核心思想就是：**即使函数在尖点处没有唯一的切线，我们只要找到任意一条位于函数曲面下方的支撑超平面，该平面的法向斜率就是一个合法的“导数替代品”！**

::: definition 次梯度与次微分 (Subgradient & Subdifferential)
设 $f: \mathbb{R}^n \to \mathbb{R}$ 为凸函数。
1. **次梯度（Subgradient）**：向量 $g \in \mathbb{R}^n$ 称为 $f$ 在点 $x$ 处的一个次梯度，若对定义域内所有点 $y \in \mathbb{R}^n$，恒有全局支撑不等式：
$$f(y) \ge f(x) + g^T (y - x)$$
2. **次微分集合（Subdifferential）**：$f$ 在点 $x$ 处的**所有次梯度构成的集合**称为其在 $x$ 处的次微分，记为 $\partial f(x)$。
:::

```mermaid
flowchart TD
    subgraph NonSmoothGeometry [非光滑尖角处的切线束]
        Point[不可微尖点 x*] --> Tan1[支撑切线 1: 斜率 g_1]
        Point --> Tan2[支撑切线 2: 斜率 g_2]
        Point --> Tan3[支撑切线 3: 斜率 g_3]
    end
    Tan1 & Tan2 & Tan3 --> Subdiff[次微分集合 partial f(x*): 闭有界凸多胞形]
    Subdiff -->|极值判据: 零向量是否属于次微分?| OptRule[0 in partial f(x*)]
```

::: theorem 次微分的核心性质与最优性极值定理
1. **可微即退化**：若 $f$ 在点 $x$ 处可微，则其余次梯度全部消失，次微分集合退化为仅含单个梯度的单点集：$\partial f(x) = \{\nabla f(x)\}$；
2. **紧凸性**：对于定义域内部的点，次微分 $\partial f(x)$ 必然是一个**非空、闭且有界的凸集**；
3. **非光滑最优性充要公理**：点 $x^*$ 是凸函数 $f$ 的全局极小点，**当且仅当零向量包含在其定义域处的次微分集合之中**：
$$0 \in \partial f(x^*)$$
:::

证明仅需半行：将 $g = 0$ 代入定义式，$f(y) \ge f(x^*) + 0^T (y - x^*) = f(x^*)$，全局极小值获证！

## 2. 勒让德-芬切尔共轭函数（Fenchel Conjugate Function）

如果说傅里叶变换将时域信号映射至频域，那么在凸优化中，将空间位置坐标 $x$ 映射至其法向斜率空间的最高数学算子，就是**芬切尔共轭函数（Fenchel Conjugate / Legendre-Fenchel Transform）**。

::: definition 芬切尔共轭函数 (Convex Conjugate)
设 $f: \mathbb{R}^n \to \mathbb{R}$ 为任意函数（甚至不必是凸函数）。其共轭函数 $f^*: \mathbb{R}^n \to \mathbb{R} \cup \{+\infty\}$ 定义为线性内积与函数值的最大差值：
$$f^*(y) = \sup_{x \in \operatorname{dom}(f)} \left\{ y^T x - f(x) \right\}$$
:::

几何上，$f^*(y)$ 是斜率为 $y$ 的仿射超平面向上平移至恰好支撑函数曲面时，其在垂直纵截轴上的**截距的相反数**！
更神奇的是：由于 $f^*(y)$ 是一族关于变量 $y$ 的仿射线性函数 $y^T x - f(x)$ 的逐点上确界，**不论原始函数 $f(x)$ 多么非凸、多么畸形，其共轭函数 $f^*(y)$ 天然、无条件永远是一个凸函数！**

::: theorem 芬切尔-杨氏不等式 (Fenchel-Young Inequality)
对于任意 $x \in \operatorname{dom}(f)$ 与 $y \in \operatorname{dom}(f^*)$，恒成立：
$$f(x) + f^*(y) \ge x^T y$$
并且等号成立当且仅当斜率向量 $y$ 恰好是 $f$ 在 $x$ 处的次梯度：$y \in \partial f(x)$！
:::

更震撼的是，若 $f$ 是闭下半连续凸函数，做两次共轭将百分之百精确复原原函数：**双共轭定理（Biconjugate Theorem）**：
$$f^{**}(x) = (f^*)^*(x) = f(x)$$

## 3. 芬切尔对偶定理（Fenchel Duality）

利用共轭函数的强大威力，芬切尔（Werner Fenchel）建立起了无需任何拉格朗日乘子的非对称纯几何对偶定理：

考虑优化问题：
$$\min_{x \in \mathbb{R}^n} \quad f(x) + g(A x)$$
其芬切尔对偶问题形式极其纯粹：
$$\max_{y \in \mathbb{R}^m} \quad -f^*(-A^T y) - g^*(y)$$

::: theorem 芬切尔对偶定理 (Fenchel Duality Theorem)
若存在 $x_0 \in \operatorname{relint}(\operatorname{dom}(f))$ 使得 $A x_0 \in \operatorname{relint}(\operatorname{dom}(g))$，则原对偶最优值完全相等，且强对偶性成立，对偶最优解存在！
:::

::: insight 斜率空间是对物理空间的升维镜像
次梯度与芬切尔共轭是现代应用数学最辉煌的抽象。
在物理空间中，我们看到的是山川起伏的坐标高度 $f(x)$；而在对偶空间中，共轭函数 $f^*(y)$ 用每一块切面的法向倾斜角重新给整个曲面编目。
当原问题在尖锐复杂的约束边界上撞得头破血流时，变换到芬切尔对偶空间后，原本不可微的折叠尖角往往化作了极其平滑宽阔的开阔原野。这种在“坐标位移”与“斜率张力”之间的自如切换，是顶级应用数学大师终极的武器库。
:::
