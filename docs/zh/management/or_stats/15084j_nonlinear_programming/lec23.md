---
title: '半正定规划 I：标准型、线性矩阵不等式（LMI）与凸锥几何 (Semidefinite Optimization I)'
type: lecture
lecture: 23
tags: [semidefinite-programming, lmi, psd-cone, schur-complement]
status: complete
---

# Lec 23 半正定规划 I：标准型、线性矩阵不等式（LMI）与凸锥几何 (Semidefinite Optimization I)

> MIT 15.084J / 6.252J 非线性规划 · 讲义 23 · 授课教师：Prof. Robert Freund

## TL;DR

- 半正定规划（SDP）在对称半正定矩阵锥 $\mathbb{S}_+^n$ 上极小化矩阵线性迹内积。
- 舒尔补引理（Schur Complement）将所有凸二次不等式与矩阵范数精确转化为线性矩阵不等式（LMI）。
- SDP 兼具线性规划的多项式易解性与非线性二次曲面的极其强悍的表达力。

## 1. 突破维度的界限：从向量到对称正半定矩阵

在非线性规划的前半程，我们的变量全都是欧氏空间中的一维列向量 $x \in \mathbb{R}^n$。
从本讲开始，我们正式进入 20 世纪 90 年代以来整个应用数学界最重大的突破——**半正定规划（Semidefinite Programming, SDP）**。

在 SDP 中，基础决策变量是一个实对称矩阵 $X \in \mathbb{S}^n$（$X = X^T$）。
定义矩阵内积为弗罗贝尼乌斯内积（Frobenius Inner Product）：
$$C \bullet X = \operatorname{tr}(C X) = \sum_{i=1}^n \sum_{j=1}^n C_{ij} X_{ij}$$

::: definition 半正定规划标准型 (Standard Primal SDP)
给定对称矩阵 $C, A_1, \dots, A_m \in \mathbb{S}^n$ 与资源向量 $b \in \mathbb{R}^m$。
标准型原半正定规划表述为：

$$\begin{aligned}
\min_{X \in \mathbb{S}^n} \quad & \operatorname{tr}(C X) \\
\text{s.t.} \quad & \operatorname{tr}(A_i X) = b_i, \quad i = 1, \dots, m \\
& X \succeq 0
\end{aligned}$$
:::

约束 $X \succeq 0$ 意味着对任意向量 $z \in \mathbb{R}^n$，二次型 $z^T X z \ge 0$。
看似简单的一条矩阵半正定约束，等价于**不可数无限条线性的标量不等式**！它赋予了模型难以想象的几何刚性。

```mermaid
flowchart TD
    subgraph LMI_Transformations [舒尔补引理统一多类凸约束]
        Quad[凸二次约束: x^T P x + q^T x + r <= 0] --> Schur[舒尔补引理 Schur Complement]
        MatrixNorm[矩阵诱导范数: ||A(x)||_2 <= t] --> Schur
        Eigenvalue[最大特征值极小化: lambda_max(A(x)) <= t] --> Schur
        Schur --> LMI[标准线性矩阵不等式 LMI: F(x) = F_0 + sum x_i F_i >= 0]
    end
```

## 2. 线性矩阵不等式（Linear Matrix Inequality, LMI）

半正定规划的对偶问题通常表现为一种极具工程实用价值的形式——**线性矩阵不等式（Linear Matrix Inequality, LMI）**：

::: definition 线性矩阵不等式 (LMI)
设对称矩阵 $F_0, F_1, \dots, F_p \in \mathbb{S}^n$。关于决策向量 $y \in \mathbb{R}^p$ 的**线性矩阵不等式（LMI）**定义为：
$$F(y) = F_0 + \sum_{k=1}^p y_k F_k \succeq 0$$
即矩阵 $F(y)$ 必须处于半正定矩阵锥内部。
:::

满足 LMI 的集合 $\mathcal{Y} = \{y \in \mathbb{R}^p \mid F(y) \succeq 0\}$ 称为一个**谱面体（Spectrahedron）**。
由于特征值函数是凹函数，谱面体必然是一个闭凸集！谱面体是传统多面体（Polyhedron）向非线性平滑曲面的终极推广。

## 3. 变换的魔法：舒尔补引理（Schur Complement Lemma）

如何将工程与控制理论中大量繁琐的非线性二次约束、矩阵逆与奇异值范数转化为优雅的 LMI？
核心钥匙就是无处不在的**舒尔补引理（Schur Complement Lemma）**：

::: theorem 舒尔补引理 (Schur Complement Lemma)
考虑对称分块矩阵：
$$M = \begin{bmatrix} A & B \\ B^T & C \end{bmatrix}$$
假设子块 $A \succ 0$ 严格正定。
则整个矩阵 $M$ 半正定（$M \succeq 0$），**当且仅当其关于 $A$ 的舒尔补矩阵半正定**：
$$S = C - B^T A^{-1} B \succeq 0$$
:::

::: example 凸二次约束向 LMI 的降维打击
考察任意凸二次约束：$x^T P x + q^T x + r \le 0$（其中 $P \succ 0$）。
将该不等式移项变形：
$$-(q^T x + r) - x^T P x \ge 0 \iff -(q^T x + r) - x^T (P^{1/2})^T I^{-1} (P^{1/2} x) \ge 0$$
根据舒尔补引理，这**百分之百充要等价于一个极其优美的仿射分块 LMI**：
$$\begin{bmatrix}
I & P^{1/2} x \\
(P^{1/2} x)^T & -(q^T x + r)
\end{bmatrix} \succeq 0$$
原本非线性的二次曲面，通过增加内部辅助维度，直接被“拉平”成了一个严格线性的矩阵不等式！
:::

类似地，矩阵谱范数不等式 $\|A(x)\|_2 \le t$ 等价于 $\begin{bmatrix} t I & A(x) \\ A(x)^T & t I \end{bmatrix} \succeq 0$。

::: insight 升维消灭非线性的现代数学哲学
为什么半正定规划被称为 20 世纪末优化理论的最伟大飞跃？
舒尔补引理为我们揭示了一个深刻的哲学原理：**在低维空间中看起来极其顽固、复杂的非线性曲率，只要我们敢于向更高维度的对称矩阵空间进行投影和升维，它就会退化为纯粹平面的线性矩阵不等式！**
SDP 既保留了线性规划能够使用内点法在多项式时间内精确求解的全部优良算法基因，又获得了吞纳几乎所有凸二次、二次型与矩阵特征值约束的无边法力。这是应用数学最纯粹的升维魔法。
:::
