---
title: '抽象勒贝格积分 I：非负简单函数与单调收敛定理 (Abstract Integration I)'
type: lecture
lecture: 7
tags: [lebesgue-integral, abstract-integration, monotone-convergence, simple-functions]
status: complete
---

# Lec 7 抽象勒贝格积分 I：非负简单函数与单调收敛定理 (Abstract Integration I)

> MIT 15.085J / 6.436J 概率论基础 · 讲义 7 · 授课教师：Prof. John Tsitsiklis / Devavrat Shah

## TL;DR

- 黎曼积分横向划分定义域，勒贝格积分（Lebesgue Integral）纵向切分值域测度。
- 从非负简单函数极限起步，公理化构筑无惧病态函数的广义积分大厦。
- 单调收敛定理（MCT）突破了数学校验极限与积分交换顺序的核心物理铁幕。

## 1. 黎曼积分的崩溃与勒贝格纵向切分革命

在本科高等数学中，我们学习的积分全部是**黎曼积分（Riemann Integral）**：将横坐标自变量区间 $[a, b]$ 细分成无数微小区间 $\Delta x_i$，取矩形面积累加并求极限：$\sum f(\xi_i) \Delta x_i$。

然而，在面对高度离散与随机交织的函数时，黎曼积分表现出灾难性的无能为力！
考察著名的**狄利克雷函数（Dirichlet Function）**：
$$f(x) = \begin{cases} 1, & \text{若 } x \in \mathbb{Q} \cap [0, 1] \\ 0, & \text{若 } x \notin \mathbb{Q} \cap [0, 1] \end{cases}$$
在任意微小的区间内，总有无穷多个有理数和无理数。黎曼上和恒为 1，黎曼下和恒为 0，两者永远无法相等！黎曼积分宣布狄利克雷函数“不可积”。
然而在物理上，有理数集只是可数点集，其长度测度严格为 0；在抛硬币中，掷中有理数的概率绝对是 0，这个函数的积分理应毫无悬念地等于 0！

为了拯救现代分析学，法国数学巨匠亨利·勒贝格（Henri Lebesgue）在 1902 年提出了惊世骇俗的**勒贝格积分（Lebesgue Integral）**：
**不要横向切分自变量定义域！去纵向切分因变量值域（Range）！**

```mermaid
flowchart TD
    subgraph RiemannVsLebesgue [黎曼横切 vs 勒贝格纵切]
        Riemann[黎曼积分: 细分自变量 x 轴 -> 要求函数高度光滑连续 -> 狄利克雷不可积]
        Lebesgue[勒贝格积分: 细分因变量 y 轴 -> 汇聚相同高度的原像集合 E_i = f^-1([y_i, y_i+1)) -> 调动测度 P(E_i)]
    end
    Lebesgue --> Robust[完美积分几乎一切可测函数: 狄利克雷积分严格为 0!]
```

勒贝格形象地比喻道：“黎曼积分像一个笨拙的收银员，顾客拿出一大堆硬币，他必须按从口袋里掏出来的先后顺序一枚枚累加；而勒贝格积分像一个精明的点钞员，先把所有的 1 分钱堆在一起，把所有的 5 分钱堆在一起，分别乘以枚数再相加！”

## 2. 勒贝格积分的公理化三步阶梯构筑

现代概率论将抽象期望 $\mathbb{E}[X]$ 严格定义为随机变量 $X$ 关于概率测度 $\mathbb{P}$ 的勒贝格积分：
$$\mathbb{E}[X] = \int_\Omega X(\omega) \, d\mathbb{P}(\omega)$$

其数学构建分为极其刚性的严密三步：

### 第一步：非负简单函数积分
设可测非负函数 $s(\omega)$ 仅取有限个离散值 $a_1, \dots, a_k \ge 0$：
$$s(\omega) = \sum_{i=1}^k a_i \mathbb{I}_{A_i}(\omega), \quad A_i \in \mathcal{F}$$
定义其勒贝格积分为纯代数求和：
$$\int_\Omega s \, d\mathbb{P} = \sum_{i=1}^k a_i \mathbb{P}(A_i)$$

### 第二步：非负可测函数的极限逼近
对于任意一般的非负随机变量 $X \ge 0$（不论其连续、离散还是混合型），定义其积分为**所有被它从下方支撑住的简单函数积分的上确界（Supremum）**：
$$\int_\Omega X \, d\mathbb{P} = \sup \left\{ \int_\Omega s \, d\mathbb{P} \;\middle|\; 0 \le s \le X, \; s \text{ 为简单函数} \right\}$$

### 第三步：通用实随机变量的正负部拆分
将任意随机变量拆解为正部 $X^+ = \max(X, 0) \ge 0$ 与负部 $X^- = \max(-X, 0) \ge 0$（显然 $X = X^+ - X^-$）。
若 $\int X^+ d\mathbb{P}$ 与 $\int X^- d\mathbb{P}$ 中至少有一个有限，定义：
$$\int_\Omega X \, d\mathbb{P} = \int_\Omega X^+ \, d\mathbb{P} - \int_\Omega X^- \, d\mathbb{P}$$
若两者均有限（等价于 $\mathbb{E}[|X|] < \infty$），称 $X$ **勒贝格可积（Integrable, 记为 $X \in L^1$）**！

## 3. 分析学的皇冠明珠：单调收敛定理（MCT）

在经典微积分中，极限与积分何时能够交换次序（$\lim \int f_n = \int \lim f_n$）是一个极其凶险的问题，通常必须依赖苛刻的“一致收敛（Uniform Convergence）”。
而在勒贝格积分的壮丽大厦中，这一问题获得了彻底的解放！

::: theorem 单调收敛定理 (Monotone Convergence Theorem, MCT)
设非负随机变量序列 $\{X_n\}$ 逐点单调递增：
$$0 \le X_1(\omega) \le X_2(\omega) \le X_3(\omega) \le \dots, \quad \forall \omega \in \Omega$$
且其逐点极限为 $X(\omega) = \lim_{n \to \infty} X_n(\omega)$。
则**极限与期望算子可以完全无条件自由交换次序**：
$$\lim_{n \to \infty} \mathbb{E}[X_n] = \mathbb{E}\left[ \lim_{n \to \infty} X_n \right] = \mathbb{E}[X]$$
:::

::: insight 测度连续性向代数微积分的直接兑现
单调收敛定理之所以能够成立，其最深层的引擎正是第 1 讲学到的**测度上连续性**！
因为值域的纵向切分把自变量复杂的波动变成了事件集合序列的可数递增；简单函数的积分随着台阶上升，严丝合缝地填满了函数曲面下方的全部测度体积。
勒贝格积分彻底消除了黎曼积分对拓扑连续性的病态执念，让概率论能够从容应对物理世界中一切跳跃、截断与分形过程。
:::
