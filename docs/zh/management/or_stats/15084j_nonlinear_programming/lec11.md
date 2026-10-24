---
title: '增广拉格朗日乘子法与条件数解耦 (Augmented Lagrangian Methods)'
type: lecture
lecture: 11
tags: [augmented-lagrangian, al-method, multipliers-method, hestenes-powell]
status: complete
---

# Lec 11 增广拉格朗日乘子法与条件数解耦 (Augmented Lagrangian Methods)

> MIT 15.084J / 6.252J 非线性规划 · 讲义 11 · 授课教师：Prof. Robert Freund

## TL;DR

- 增广拉格朗日法（Augmented Lagrangian / Method of Multipliers）融合拉格朗日与二次罚项。
- 引入对偶乘子迭代更新，使罚参数 $\rho$ 维持在温和有限常数下即可实现零可行性违规。
- 彻底消解了纯外罚函数法海森矩阵条件数无限发散的恶疾，奠定了非线性求解器的底座。

## 1. 赫斯滕斯与鲍威尔的破局：乘子法（Method of Multipliers）

在第 10 讲中，我们目睹了外罚函数法的绝境：要想让可行性偏差 $h(x) \to 0$，罚参数 $\rho$ 必须被逼向不可容忍的 $+\infty$，导致海森矩阵条件数彻底崩塌。

1969 年，马格努斯·赫斯滕斯（Magnus Hestenes）与迈克尔·鲍威尔（Michael J. D. Powell）独立提出了一项颠覆性的天才发明——**增广拉格朗日乘子法（Augmented Lagrangian Method, ALM / Method of Multipliers）**。

赫斯滕斯与鲍威尔的洞见极其深刻：
外罚函数法之所以必须依赖 $\rho \to \infty$，是因为它的目标函数 $f(x) + \frac{\rho}{2} \|h(x)\|^2$ 的极小值点永远只能停留在可行域外部的一侧（它必须保留一点微小的违规残差 $h(x) \ne 0$，才能产生拉力抵抗目标函数梯度 $\nabla f$）。
如果我们在目标函数中**主动加入拉格朗日乘子项 $\lambda^T h(x)$**，用乘子直接抵消真实的一阶驻点漂移：

$$\mathcal{L}_A(x, \lambda; \rho) = f(x) + \sum_{j=1}^l \lambda_j h_j(x) + \frac{\rho}{2} \sum_{j=1}^l h_j(x)^2$$

仔细观察这个神奇的增广拉格朗日函数：
**一旦我们猜中了真实的对偶最优乘子 $\lambda^*$，即使罚参数 $\rho$ 仅仅是一个非常温和、有限的小正数（如 $\rho = 10$），真实约束最优解 $x^*$ 也将严格、毫无偏差地成为该无约束增广函数的无约束极小点！**

```mermaid
flowchart TD
    subgraph ALMCycle [增广拉格朗日迭代闭环]
        direction TB
        X_sub[1. 原问题步: 在固定 lambda_k 下极小化 x_k+1 = argmin L_A(x, lambda_k; rho)]
        Check{可行性违规 ||h(x_k+1)|| 是否充分下降?}
        Check -- 是 --> DualUpdate[2. 对偶更新: lambda_k+1 = lambda_k + rho * h(x_k+1)]
        Check -- 否 --> RhoUpdate[提高惩罚参数: rho = 10 * rho]
        DualUpdate --> Next[进入下一轮无约束子问题]
        RhoUpdate --> Next
    end
```

## 2. 对偶乘子一阶梯度上升更新法则

在每一步迭代中，固定当前乘子估计 $\lambda_k$，通过普通牛顿法或拟牛顿法求解无约束极小化：
$$x_{k+1} = \arg\min_{x \in \mathbb{R}^n} \mathcal{L}_A(x, \lambda_k; \rho)$$

由一阶最优性条件，当前解满足零梯度：
$$\nabla_x \mathcal{L}_A(x_{k+1}, \lambda_k; \rho) = \nabla f(x_{k+1}) + \sum_{j=1}^l \left( \lambda_k^{(j)} + \rho h_j(x_{k+1}) \right) \nabla h_j(x_{k+1}) = 0$$

将此式与原问题的真实 KKT 驻点方程 $\nabla f(x^*) + \sum \lambda_j^* \nabla h_j(x^*) = 0$ 进行对比，赫斯滕斯导出了一条堪称神来之笔的**对偶乘子更新公式**：

::: definition 增广拉格朗日对偶乘子更新公式
$$\lambda_{k+1}^{(j)} = \lambda_k^{(j)} + \rho \cdot h_j(x_{k+1}), \quad \forall j = 1, \dots, l$$
:::

这不仅是一个代数凑配，它的数学本质是：**在拉格朗日对偶问题上执行精确的对偶梯度上升步长（Dual Gradient Ascent），且步长恰好精确等于 $\rho$！**

## 3. 推广至不等式约束与有界罚参数收敛性

对于包含不等式约束 $g_i(x) \le 0$ 的系统，我们引入非负松弛变量 $s_i \ge 0$ 使得 $g_i(x) + s_i = 0$。在增广拉格朗日函数中显式对 $s_i \ge 0$ 执行极小化并解析消元，得到针对不等式的无松弛紧凑表达：

$$\mathcal{L}_A(x, \lambda, \mu; \rho) = f(x) + \sum_{j=1}^l \left[ \lambda_j h_j(x) + \frac{\rho}{2} h_j(x)^2 \right] + \frac{1}{2\rho} \sum_{i=1}^m \left[ \left( \max(0, \mu_i + \rho g_i(x)) \right)^2 - \mu_i^2 \right]$$

不等式乘子对应更新为：
$$\mu_{k+1}^{(i)} = \max\left( 0, \; \mu_k^{(i)} + \rho g_i(x_{k+1}) \right)$$

::: theorem 增广拉格朗日有限罚参数超线性收敛定理
设二阶充分条件与 LICQ 成立。
存在有限阈值 $\bar{\rho} < \infty$，只要固定 $\rho > \bar{\rho}$（无需让 $\rho \to +\infty$），增广拉格朗日乘子法生成的序列 $(x_k, \lambda_k, \mu_k)$ **必然局部收敛至真实的 KKT 最优解**！
并且，其收敛速度通常呈现**超线性（Superlinear Convergence）**甚至几何级数加速，而子问题的海森矩阵条件数在全过程中始终被牢牢禁锢在一个极其健康的常数范围内！
:::

::: insight 软硬兼施与对称博弈的胜利
增广拉格朗日法是非线性优化最经典的辩证法教科书。
纯对偶法太软，在非凸问题中缺乏局部下凸性保障；纯罚函数法太硬，无限暴力的罚金直接诱发数值海啸。
增广拉格朗日法用 $\frac{\rho}{2} \|h(x)\|^2$ 为原本可能凹陷或平坦的鞍点曲面垫上了一层稳固的局部正曲率，同时用对偶乘子 $\lambda$ 动态代偿残余偏差。软硬兼施之间，约束优化被化解为一系列温和、优雅的无约束凸二次冲刺。现代大工业求解器（如 LANCELOT, IPOPT, ADMM）无一不流淌着 ALM 的高贵血液。
:::
