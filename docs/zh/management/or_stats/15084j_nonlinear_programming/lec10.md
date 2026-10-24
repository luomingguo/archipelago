---
title: '外罚函数法与二次惩罚项渐近性态 (Penalty Methods)'
type: lecture
lecture: 10
tags: [penalty-methods, quadratic-penalty, ill-conditioning, asymptotic-convergence]
status: complete
---

# Lec 10 外罚函数法与二次惩罚项渐近性态 (Penalty Methods)

> MIT 15.084J / 6.252J 非线性规划 · 讲义 10 · 授课教师：Prof. Robert Freund

## TL;DR

- 外罚函数法（Exterior Penalty Method）通过惩罚项将有约束优化松弛为无约束序列。
- 二次罚项 $\frac{\rho}{2} \|h(x)\|^2$ 保障可微性，极值点序列在 $\rho \to \infty$ 时必收敛至 KKT 点。
- 罚参数趋向无穷直接诱发海森矩阵条件数发散，是数值优化的阿喀琉斯之踵。

## 1. 约束软化与外罚函数（Exterior Penalty Function）

在非线性规划中，处理约束曲面最粗暴、也最直观的方法是**罚函数法（Penalty Methods）**，由著名应用数学家理查德·柯朗（Richard Courant）于 1943 年提出。

考虑通用的约束优化问题：
$$\min_{x \in \mathbb{R}^n} \quad f(x) \quad \text{s.t.} \quad h_j(x) = 0, \; j=1,\dots,l, \quad g_i(x) \le 0, \; i=1,\dots,m$$

罚函数法的基本哲学是：**打破可行域的铁幕，允许算法自由漫游在整个欧氏空间 $\mathbb{R}^n$ 中；但一旦算法试探点越界违法，系统立即施加一笔极其沉重的代数罚金（Penalty Cost）**。

构造无约束增广目标函数：
$$Q(x; \rho) = f(x) + \rho \cdot P(x)$$
其中 $\rho > 0$ 称为**罚参数（Penalty Parameter）**，$P(x) \ge 0$ 为**违规惩罚函数**，满足：
1. 若 $x$ 完全可行（即 $h(x) = 0, g(x) \le 0$），则 $P(x) = 0$；
2. 若 $x$ 不可行，则 $P(x) > 0$。

```mermaid
flowchart TD
    subgraph PenaltyLoop [外罚函数法序列优化]
        In[初始罚参数 rho_1 > 0] --> Sub[无约束极小化: x_k = argmin Q(x, rho_k)]
        Sub --> Check{违规量 P(x_k) < tolerance 吗?}
        Check -- 是 --> Done[收敛至原约束最优解 x*]
        Check -- 否 --> Update[提高罚参数: rho_k+1 = gamma * rho_k (gamma > 1)]
        Update --> Sub
    end
```

## 2. 二次惩罚函数（Quadratic Penalty）及其微分性质

为了让无约束子问题能够直接应用牛顿法或拟牛顿法，惩罚函数必须处处连续可微。工业上最常用的标准是**二次罚函数（Quadratic Penalty Function）**：

$$P(x) = \frac{1}{2} \sum_{j=1}^l h_j(x)^2 + \frac{1}{2} \sum_{i=1}^m \left[ \max(0, g_i(x)) \right]^2$$

二次罚函数不仅处处连续可微，其一阶梯度公式极其平滑紧凑：
$$\nabla_x Q(x; \rho) = \nabla f(x) + \rho \sum_{j=1}^l h_j(x) \nabla h_j(x) + \rho \sum_{i=1}^m \max(0, g_i(x)) \nabla g_i(x)$$

::: theorem 外罚函数序列收敛性定理
设可行域非空且有界，$f, g_i, h_j$ 连续。
设罚参数序列满足单调递增发散：$\rho_k \to +\infty$。
设 $x_k$ 为无约束子问题 $\min_x Q(x; \rho_k)$ 的全局极小点。
则点列 $\{x_k\}$ 的任意极限点 $x^*$ **必然是原约束优化问题的全局最优解**！
并且，各约束的代数罚金乘以参数，渐近给出了真实的对偶乘子估计：
$$\lambda_j^* = \lim_{k \to \infty} \rho_k h_j(x_k), \qquad \mu_i^* = \lim_{k \to \infty} \rho_k \max(0, g_i(x_k))$$
:::

## 3. 数值灾难：海森矩阵条件数爆炸

尽管外罚函数法理论上完美收敛，但在实际工程计算中，纯外罚函数法几乎无法独立用于高精度工业求解！

问题出在哪里？
考察二次罚函数的二阶海森矩阵：
$$\nabla_{xx}^2 Q(x; \rho) \approx \nabla^2 f(x) + \rho \sum_{j=1}^l \nabla h_j(x) \nabla h_j(x)^T + \rho \sum_{i \in A(x)} \nabla g_i(x) \nabla g_i(x)^T$$

注意看后面两项：
它们是活动约束梯度外积张成的秩亏矩阵（秩至多为 $l + |A(x)| < n$）。
- 在约束梯度的跨度子空间（Range Space）内，由于被超大参数 $\rho$ 放大，特征值尺度高达 $\mathcal{O}(\rho)$；
- 在切空间零子空间（Null Space）内，特征值尺度仅仅由 $\nabla^2 f$ 决定，尺度为 $\mathcal{O}(1)$！

当算法为了逼近高精度解而将罚参数推高至 $\rho = 10^8$ 时，无约束子问题的**海森矩阵谱条件数将灾难性地恶化到 $10^8$ 甚至更高**！
计算机浮点数的舍入误差在解方程时瞬间击穿有效精度，牛顿法直接遭遇数值奇异。

::: insight 粗暴惩罚与渐进折中的宿命
外罚函数法向我们展现了人类直觉在面对刚性约束时的天然弱点：
想要杜绝越界，就用无限大的大棒（$\rho \to \infty$）猛击；但无限大的大棒在消灭物理违规的同时，也粉碎了数值曲面的平滑微积分结构。
这种“为消除约束而制造病态条件数”的死结，迫使运筹学家必须寻找一种更精妙的机制——在罚参数保持有限常数的优雅状态下，依然能够彻底消除约束偏差。这就是下一讲增广拉格朗日乘子法的伟大救赎。
:::
