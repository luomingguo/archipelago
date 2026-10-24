---
title: '内点法 III：多项式时间收敛性证明与超线性加速 (Interior Point III: Convergence)'
type: lecture
lecture: 22
tags: [polynomial-complexity, short-step-path, self-concordance, superlinear-convergence]
status: complete
---

# Lec 22 内点法 III：多项式时间收敛性证明与超线性加速 (Interior Point III: Convergence)

> MIT 15.081J / 6.251J 数学规划导论 · 讲义 22 · 授课教师：Prof. Dimitris Bertsimas / John Tsitsiklis

## TL;DR

- 短步路径跟踪法（Short-Step IPM）严格证明了 $\mathcal{O}(\sqrt{n} L)$ 轮牛顿迭代的多项式上界。
- 涅米洛夫斯基自协调函数（Self-Concordant Functions）将内点法理论推广至任意凸锥空间。
- 在最优解邻域内，局部牛顿阻尼衰减为零，算法呈现二次甚至超线性超强收敛。

## 1. 短步路径跟踪法（Short-Step）的严格多项式收敛

在前两讲中，我们惊叹于原对偶内点法的工业神速。现在，我们必须给出严格的数学证明：**原对偶内点法为什么必然能在多项式时间内收敛？**

为了给出无懈可击的形式化证明，理论界设计了**短步路径跟踪算法（Short-Step Path-Following Method）**。
该算法定义了一个围绕中心路径的狭窄欧氏邻域：

::: definition 欧氏度量中心路径邻域 $\mathcal{N}_2(\theta)$
对于常数 $\theta \in (0, 1)$，定义原对偶点集的三元组邻域：
$$\mathcal{N}_2(\theta) = \left\{ (x, p, s) \in \mathcal{F}^\circ \;\middle|\; \|X S \mathbf{1} - \mu \mathbf{1}\|_2 \le \theta \mu \right\}$$
其中 $\mu = x^T s / n$。邻域严格限制了每个分量乘积 $x_i s_i$ 偏离全局平均间距 $\mu$ 的相对波动。
:::

算法执行规则极其严密：
1. 从严格处于邻域内的初始内点 $(x^0, p^0, s^0) \in \mathcal{N}_2(\theta)$ 出发；
2. 设定参数更新比例：$\mu_{k+1} = \left(1 - \frac{\beta}{\sqrt{n}}\right) \mu_k$（其中 $\beta = \mathcal{O}(1)$ 为极小常数）；
3. 仅执行一次牛顿迭代更新：$(x^{k+1}, p^{k+1}, s^{k+1}) = (x^k, p^k, s^k) + (\Delta x, \Delta p, \Delta s)$。

```mermaid
flowchart TD
    subgraph NeighborhoodProof [短步法单步归纳封闭]
        In[当前点处于 N_2 邻域内部] --> Reduce[缩减对偶间隙: mu+ = 1 - beta / sqrt n * mu]
        Reduce --> NewtonStep[执行单步牛顿校正]
        NewtonStep --> Out[新点依然严格闭合保留在 N_2 邻域内!]
        Out -->|对偶间隙以 1 - beta / sqrt n 几何递减| Iteration[迭代循环]
    end
```

::: theorem 短步内点法复杂度定理
设初始对偶间隙为 $\mu_0$。短步路径跟踪内点法在至多：
$$K = \mathcal{O}\left( \sqrt{n} \ln\left( \frac{n \mu_0}{\varepsilon} \right) \right)$$
次牛顿迭代内，保证对偶间隙收敛至 $\varepsilon$ 以内：$x^T s \le \varepsilon$。
由于单次牛顿方程求解为矩阵乘法与分解的多项式开销，该算法完整证明了线性规划的最优时间复杂度界！
:::

证明的核心在于二次收缩性：当位移限制在 $\mathcal{O}(1/\sqrt{n})$ 尺度内时，二阶残差项的范数满足 $\|\Delta X \Delta S \mathbf{1}\| \le \frac{\theta^2 + \beta^2}{2(1 - \theta)} \mu$，使得新点永远不会逃逸出 $\mathcal{N}_2$ 保护伞，实现了代数归纳法上的完美闭合。

## 2. 涅米洛夫斯基与涅斯捷罗夫的自协调理论（Self-Concordance）

短步法证明虽然漂亮，但过度依赖对数函数 $\ln(x)$ 的具体代数形式。内点法能否推广到任意非线性的凸优化问题？

1994 年，阿尔卡迪·涅米洛夫斯基（Arkadi Nemirovski）与尤里·涅斯捷罗夫（Yurii Nesterov）发表了凸优化理论的旷世神作《多项式方法在凸规划中的应用》，提出了**自协调函数理论（Self-Concordant Functions）**。

::: definition 自协调势函数
一个凸函数 $f: \mathbb{R} \to \mathbb{R}$ 称为自协调的，若其三阶导数被二阶导数以如下方式绝对控制：
$$|f'''(x)| \le 2 \left( f''(x) \right)^{3/2}$$
对于高维多元函数，要求沿任意方向限制的一元截面函数均满足该不等式。
:::

自协调性质在几何上的终极威力在于：**它彻底消除了牛顿法对空间坐标度量单位的依赖（Affine Invariance）！**
在自协调凸曲面上，牛顿减量 $\lambda(x) = \sqrt{\nabla f(x)^T [\nabla^2 f(x)]^{-1} \nabla f(x)}$ 是一个绝对的物理不变量。只要 $\lambda(x) < 1/4$，牛顿法就不可阻挡地进入了二次收敛区域（Quadratic Convergence Zone）。这一理论直接将线性规划、二阶锥规划（SOCP）与半正定规划（SDP）在凸分析层面全部大一统！

::: insight 优雅理论与工业暴力的共谋
短步法给出了最保守的 $\mathcal{O}(\sqrt{n})$ 理论证明；而梅罗特拉长步法在工业实测中展现出了近乎常数级的卓越表现。
这不仅没有削弱理论的尊严，反而展示了理论科学与工程实践最美妙的交响：理论筑牢了最深不可测的底线，确保算法在任何病态退化情形下都拥有多项式安全的逃生通道；而工程智慧则在宽阔的安全区内尽情纵马驰骋。正是这种双重保障，让现代优化求解器成为了工业界最坚不可摧的底层重器。
:::
