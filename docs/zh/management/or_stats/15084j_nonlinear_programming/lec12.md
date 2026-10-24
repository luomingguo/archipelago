---
title: '内点障碍函数法与 Frank-Wolfe 条件梯度算法 (Barrier Methods & Frank-Wolfe)'
type: lecture
lecture: 12
tags: [barrier-methods, frank-wolfe, conditional-gradient, projection-free]
status: complete
---

# Lec 12 内点障碍函数法与 Frank-Wolfe 条件梯度算法 (Barrier Methods & Frank-Wolfe)

> MIT 15.084J / 6.252J 非线性规划 · 讲义 12 · 授课教师：Prof. Robert Freund

## TL;DR

- 内点障碍法（Barrier Method）通过逆函数或对数势垒在可行域内侧强制阻断触界。
- Frank-Wolfe 条件梯度算法利用紧致凸集上的线性子规划实现完全无需投影的稀疏迭代。
- $\mathcal{O}(1/k)$ 的次线性收敛换取了单步计算的极致轻量，在大规模矩阵完备与网络均衡中大放异彩。

## 1. 内点障碍函数法（Interior Barrier Methods）

与第 10 讲从可行域外部施加惩罚的“外罚法”不同，**内点障碍法（Barrier Methods）**采取了完全相反的防御姿态：
**算法初始点必须严格处于可行域内部深处；在每一次迭代中，障碍函数在可行域边界筑起一道无穷大能量势垒，确保算法永远在可行域内部滑行，绝不越雷池一步！**

考虑不等式约束优化：
$$\min_{x \in \mathbb{R}^n} \quad f(x) \quad \text{s.t.} \quad g_i(x) \le 0, \quad i = 1, \dots, m$$
定义严格内部：$\Omega^\circ = \{x \in \mathbb{R}^n \mid g_i(x) < 0, \; \forall i = 1, \dots, m\}$。

构造障碍目标函数：
$$B(x; \mu) = f(x) + \mu \cdot \phi(x)$$
其中 $\mu > 0$ 为障碍参数，经典障碍项有两种形式：
1. **逆障碍函数（Inverse / Caratheodory Barrier）**：$\phi(x) = -\sum_{i=1}^m \frac{1}{g_i(x)}$；
2. **对数障碍函数（Logarithmic Barrier）**：$\phi(x) = -\sum_{i=1}^m \ln(-g_i(x))$。

当试探点向边界靠近（$g_i(x) \to 0^-$）时，障碍项以爆发式的几何级数冲向 $+\infty$。
随着算法迭代，令 $\mu_k \to 0^+$，障碍势垒的有效影响范围被逐步压缩至边界附近极狭窄的微米级边缘，内部最优解序列 $\{x(\mu_k)\}$ 严格平滑逼近真实的边界最优极值！

```mermaid
flowchart LR
    subgraph FrankWolfeStep [Frank-Wolfe 单步迭代无投影循环]
        Grad[计算当前负梯度方向 -nabla f(x_k)] --> LP[求解线性目标子规划: s_k = argmin s in Omega nabla f(x_k)^T s]
        LP --> Direction[确定 FW 行进方向: d_k = s_k - x_k]
        Direction --> Step[线搜索确定步长 gamma_k = 2 / k+2]
        Step --> Update[凸组合更新: x_k+1 = 1 - gamma_k x_k + gamma_k s_k]
    end
```

## 2. 无投影优化的奇迹：Frank-Wolfe 条件梯度算法

在第 9 讲中，我们学习了投影梯度法。但如果可行域 $\Omega$ 是一个极其复杂的高维凸集（例如核范数单位球、大规模交通网络流分配多胞形），向该集合做欧氏正交投影（$\min_{z \in \Omega} \|z - v\|^2$）本身就是一个极耗算力的非线性二次规划！

玛格丽特·弗兰克（Marguerite Frank）与菲利普·沃尔夫（Philip Wolfe）在 1956 年提出了著名的**条件梯度法（Conditional Gradient / Frank-Wolfe Algorithm）**。
该算法最神奇的特质在于：**完全不需要任何流形投影，仅需在凸集上求解最简单的线性规划！**

::: definition Frank-Wolfe 算法流程
设 $\Omega$ 为紧致凸集。从任意可行点 $x_0 \in \Omega$ 开始，迭代执行：
1. **线性化子问题（Linear Subproblem）**：
   在当前点 $x_k$ 处，将非线性目标函数用一阶泰勒展开线性化，寻找可行域内使得线性内积最小的极值点：
   $$s_k = \arg\min_{s \in \Omega} \quad \nabla f(x_k)^T s$$
   由于目标是纯线性的，若 $\Omega$ 是多面体，这个子问题仅是一个极快的标准 LP，最优解 $s_k$ 必然落在 $\Omega$ 的某个极点（Extreme Point）上！
2. **确定下降方向**：定义更新向量为当前点指向极点的连线向量：
   $$d_k = s_k - x_k$$
3. **凸组合更新（Convex Combination Update）**：
   采用通用阻尼步长 $\gamma_k = \frac{2}{k + 2} \in (0, 1)$（或通过线搜索）：
   $$x_{k+1} = (1 - \gamma_k) x_k + \gamma_k s_k$$
:::

因为 $x_k \in \Omega$ 且 $s_k \in \Omega$，根据凸集的公理定义，它们的凸组合 $x_{k+1}$ **天然、百分之百自动驻留在可行域内部**！没有任何一点需要被截断或投影！

## 3. 弗兰克-沃尔夫对偶间隙（FW Duality Gap）与稀疏性

除了无投影特性，Frank-Wolfe 算法还免费产出一个极高价值的理论副产品——**Frank-Wolfe 对偶间隙（FW Gap）**：

$$g(x_k) = \max_{s \in \Omega} \nabla f(x_k)^T (x_k - s) = \nabla f(x_k)^T (x_k - s_k)$$

根据凸函数的一阶充要性质：$f(x^*) \ge f(x_k) + \nabla f(x_k)^T (x^* - x_k) \ge f(x_k) - g(x_k)$。
这意味着：**在任意迭代步，量 $g(x_k)$ 严格给出了当前点目标值与全局理论最优值之间的绝对误差上界！** 求解器无需知道真实的 $f(x^*)$，即可实时获取精确的终止收敛证明。

::: theorem Frank-Wolfe 收敛性与稀疏原子表示定理
设 $f$ 在紧凸集 $\Omega$ 上具有 $L$-Lipschitz 连续梯度。Frank-Wolfe 算法生成的序列满足 $\mathcal{O}(1/k)$ 的次线性收敛：
$$f(x_k) - f(x^*) \le \frac{2 L \operatorname{diam}(\Omega)^2}{k + 2}$$
更非凡的是，在第 $k$ 步迭代，解向量 $x_k$ **至多表示为 $k+1$ 个极点原子的凸组合**！
:::

在推荐系统矩阵完备（Matrix Completion）中，极点是秩一奇异向量外积。运行 $k$ 步 Frank-Wolfe 算法，输出的巨大矩阵其秩（Rank）绝对保证不超过 $k$！这种天然的极端稀疏低秩诱导能力，使其在大数据时代重获新生。

::: insight 速度与结构的哲学取舍
在优化算法的万神殿中，牛顿法是追求极致二次速度的狂飙跑车，但代价是极其沉重的二阶海森矩阵求逆；
Frank-Wolfe 则像一位朴素的苦行僧：它甘愿忍受 $\mathcal{O}(1/k)$ 的缓慢线性衰减，换取了彻底不需要求解任何逆矩阵、不需要做任何流形正交投影的极致轻盈。
更重要的是，它每一步都在用最纯粹的极点原子搭建解的骨架，把高维连续空间的优化转化为了离散原子的线性叠加。这种对几何本质结构的保留，在海量维度的现代机器学习中展现出了不可替代的优雅。
:::
