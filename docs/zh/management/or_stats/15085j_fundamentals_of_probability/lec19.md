---
title: '一致可积性、Vitali 收敛定理与级数几乎处处收敛 (Uniform Integrability)'
type: lecture
lecture: 19
tags: [uniform-integrability, vitali-convergence-theorem, l1-convergence, kolmogorov-three-series]
status: complete
---

# Lec 19 一致可积性、Vitali 收敛定理与级数几乎处处收敛 (Uniform Integrability)

> MIT 15.085J / 6.436J 概率论基础 · 讲义 19 · 授课教师：Prof. John Tsitsiklis / Devavrat Shah

## TL;DR

- 一致可积性（Uniform Integrability, UI）彻底消除了随机序列尾部质量逃逸的病态。
- 维塔利收敛定理（Vitali Convergence Theorem）确立了依概率收敛升级为 $L^1$ 范数收敛的充要条件。
- 柯尔莫哥洛夫三级数定理以三道代数防线严格判定独立随机级数的几乎处处收敛性。

## 1. 质量逃逸的终结：一致可积性（Uniform Integrability）

在第 8 讲中，我们学习了控制收敛定理（DCT）：只要存在一个可积控制变量 $|X_n| \le Y$（$\mathbb{E}[Y] < \infty$），期望与极限就能自由交换。
然而，在现代随机分析与鞅论中，很多时候我们**根本找不到这样一个在全时间轴上死死压制住所有序列的全局上界 $Y$**！
例如：序列虽然没有单一上界，但其高阶尾部的能量分布整体衰减得极其整齐。

为了在缺少绝对上界时依然能够安全兑现期望极限，分析学大师创立了**一致可积性（Uniform Integrability, UI）**：

::: definition 一致可积性 (Uniform Integrability)
随机变量集合 $\{X_i\}_{i \in I}$ 称为**一致可积的（Uniformly Integrable）**，若满足：
$$\lim_{M \to \infty} \sup_{i \in I} \mathbb{E}\left[ |X_i| \cdot \mathbb{I}_{|X_i| > M} \right] = 0$$
:::

直观几何物理诠释：不管你考察集合中的哪一个变量，只要你把截断阈值 $M$ 推得足够高，**所有变量落在遥远尾部 $[M, \infty)$ 内的残余能量，必须在一致意义下被彻底碾平归零！**
没有任何一个变量能够在遥远的无穷深渊里，偷渡非零的微积分质量！

```mermaid
flowchart TD
    subgraph UICriteria [判定一致可积性的三大充分判据]
        Lp[1. 存在 p > 1: sup_i E[|X_i|^p] < 无穷 (L^p 有界)] --> UI[集合具有一致可积性 Uniform Integrability]
        DCT[2. 控制支配: |X_i| <= Y 且 E[Y] < 无穷] --> UI
        Doob[3. 鞅条件期望族: X_i = E[Z | F_i] 且 E[|Z|] < 无穷] --> UI
    end
    UI --> Vitali[激活维塔利收敛定理: 依概率收敛 <=> L^1 强收敛!]
```

## 2. 维塔利收敛定理（Vitali's Convergence Theorem）

一致可积性究竟有什么神力？
意大利数学家朱塞佩·维塔利证明了分析学最锋利的充要极限定理：

::: theorem 维塔利收敛定理 (Vitali's Convergence Theorem)
设 $X_n \in L^1$ 为随机变量序列。则以下两条**严格充要等价**：
1. 序列在 $L^1$ 范数下强收敛：$X_n \xrightarrow{L^1} X$（即 $\lim_{n \to \infty} \mathbb{E}[|X_n - X|] = 0$，由此 $\lim \mathbb{E}[X_n] = \mathbb{E}[X]$）；
2. 序列**依概率收敛于 $X$（$X_n \xrightarrow{P} X$），并且集合 $\{X_n\}$ 具有一致可积性（UI）！**
:::

维塔利定理彻底揭开了勒贝格积分收敛的底层黑盒：
**依概率收敛（$P$）负责掌控有限区间内部的几何形状对齐，而一致可积性（UI）负责充当边防警察，严防尾部质量逃逸！**
两者双剑合璧，就 $100\%$ 获得了微积分期望收敛的最高通行证。

## 3. 柯尔莫哥洛夫三级数定理（Kolmogorov's Three-Series Theorem）

在随机级数求和 $\sum_{n=1}^\infty X_n$ 中，我们如何判定级数是否以概率 1 收敛？
柯尔莫哥洛夫在 1928 年给出了概率论中唯一一个包含充要条件的宏伟判据：

::: theorem 柯尔莫哥洛夫三级数定理
设 $X_1, X_2, \dots$ 为**相互独立**的随机变量序列。
选择任意固定常数 $c > 0$，定义截断随机变量：
$$Y_n = X_n \cdot \mathbb{I}_{|X_n| \le c} = \begin{cases} X_n, & \text{若 } |X_n| \le c \\ 0, & \text{若 } |X_n| > c \end{cases}$$
随机级数 $\sum_{n=1}^\infty X_n$ **几乎处处收敛（以概率 1 收敛）**，**当且仅当以下三个实数级数同时收敛**：
1. **大尾截断概率级数收敛**：
$$\sum_{n=1}^\infty \mathbb{P}(|X_n| > c) < \infty$$
2. **截断期望级数收敛**：
$$\sum_{n=1}^\infty \mathbb{E}[Y_n] \quad \text{收敛（有限实数）}$$
3. **截断方差级数收敛**：
$$\sum_{n=1}^\infty \operatorname{Var}(Y_n) < \infty$$
:::

三道防线层层锁死：
第一道防线借由波莱尔-坎泰利引理保证了在有限步之后，原变量 $X_n$ 与截断变量 $Y_n$ 完全无差；
第二道防线消除了漂移趋势；第三道防线利用鞅平方变差锁死了随机震荡。

::: insight 能量约束是微积分大厦的真正钢筋
一致可积性是现代纯数学最深邃的品味之一。
它不再执着于具体每一个函数的孤立形状，而是把整个序列的尾部能量作为一个整体的拓扑对象来审视。
有了 UI，我们才能在后续第 25 讲到第 26 讲中，毫无阻碍地证明鞅在无穷远处的几乎处处收敛定理。这种对无穷远处能量逸散的精确防堵，是现代高等概率论成熟的最鲜明标志。
:::
