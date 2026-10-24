---
title: '特征函数、逆转公式与 Lévy 连续性定理 (Characteristic Functions)'
type: lecture
lecture: 15
tags: [characteristic-functions, fourier-transform, inversion-formula, levy-continuity-theorem]
status: complete
---

# Lec 15 特征函数、逆转公式与 Lévy 连续性定理 (Characteristic Functions)

> MIT 15.085J / 6.436J 概率论基础 · 讲义 15 · 授课教师：Prof. John Tsitsiklis / Devavrat Shah

## TL;DR

- 特征函数 $\varphi_X(t) = \mathbb{E}[e^{itX}]$ 作为复傅里叶变换，对全宇宙所有随机变量永远良定义。
- 逆转公式（Inversion Formula）证明特征函数与累积分布函数之间存在双射一一对应。
- 列维连续性定理（Lévy's Continuity Theorem）将弱收敛完全等价转化为复分析逐点收敛。

## 1. 突破实数轴发散的禁锢：复特征函数（Characteristic Function）

在第 13 讲中，矩母函数（MGF）展现了极强的代数威力。然而，MGF 有一个致命的阿喀琉斯之踵：
由于实指数函数 $e^{s X}$ 在无穷远处爆炸性增长，许多极其重要的随机变量（例如重尾分布、柯西分布 $\frac{1}{\pi(1+x^2)}$、对数正态分布）的期望在 $s \ne 0$ 时恒为 $+\infty$！对于这些变量，MGF 根本不存在。

为了给**所有随机变量建立无差别的统一度量衡**，数学家将指数参数推向了**复平面（Complex Plane）**，引入了**特征函数（Characteristic Function）**：

::: definition 特征函数 (Characteristic Function)
设 $X$ 为随机变量。其特征函数 $\varphi_X: \mathbb{R} \to \mathbb{C}$ 定义为复指数变换的期望：
$$\varphi_X(t) = \mathbb{E}\left[ e^{i t X} \right] = \mathbb{E}[\cos(t X)] + i \mathbb{E}[\sin(t X)], \quad t \in \mathbb{R}$$
其中 $i = \sqrt{-1}$ 为虚数单位。
:::

特征函数具有至高无上的数学合法性：
因为对任意实数 $t$ 和 $X$，复指数的模长恒等于 1：
$$|e^{i t X}| = \sqrt{\cos^2(t X) + \sin^2(t X)} = 1$$
被积函数永远被常数 1 严格控制！根据勒贝格控制收敛定理（DCT）：
**对于全宇宙中任意一个概率分布、任意一个随机变量，其特征函数 $\varphi_X(t)$ 在全实数轴 $\mathbb{R}$ 上永远存在、处处有界（$|\varphi_X(t)| \le 1$）、且处处一致连续！**

```mermaid
flowchart LR
    A[概率测度空间 (R, B(R), P_X)] -->|傅里叶-斯蒂尔切斯变换 E[e^itX]| B[复平面上特征函数 phi_X(t)]
    B -->|列维逆转公式 Inversion Formula| A
    B -->|逐点收敛 phi_n(t) -> phi(t)| C[依分布弱收敛 X_n => X]
```

## 2. 信息的无损复原：列维逆转公式（Lévy Inversion Formula）

特征函数是概率测度的**傅里叶-斯蒂尔切斯变换（Fourier-Stieltjes Transform）**。
我们在复平面上做了一通微积分运算后，能否毫无差错地逆向恢复出原随机变量的累积分布函数？

保罗·列维（Paul Lévy）在 1925 年给出了堪称分析学奇迹的**逆转公式（Inversion Theorem）**：

::: theorem 列维逆转公式 (Lévy's Inversion Formula)
设 $X$ 的特征函数为 $\varphi_X(t)$，分布函数为 $F_X(x)$。
对于 $F_X$ 的任意两个连续点 $a < b$：
$$F_X(b) - F_X(a) = \mathbb{P}(a < X \le b) = \lim_{T \to \infty} \frac{1}{2\pi} \int_{-T}^T \frac{e^{-i t a} - e^{-i t b}}{i t} \varphi_X(t) \, dt$$
若特征函数绝对可积（$\int_{-\infty}^\infty |\varphi_X(t)| dt < \infty$），则 $X$ 必然拥有连续平滑的概率密度函数，且密度可通过标准复傅里叶逆变换直接求出：
$$f_X(x) = \frac{1}{2\pi} \int_{-\infty}^\infty e^{-i t x} \varphi_X(t) \, dt$$
:::

该定理确立了：**特征函数与概率分布之间存在绝对的一一双射对应关系！** 掌握了特征函数，就完完全全掌握了概率测度在实数轴上的全部微观信息。

## 3. 终极极限定理的发动机：Lévy 连续性定理

特征函数在概率论中最伟大的功勋，是它把极其抽象、难以计算的测度弱收敛，完全等价转化为了**普通的初等微积分逐点极限**！

::: theorem 列维连续性定理 (Lévy's Continuity Theorem)
设 $\{X_n\}$ 为随机变量序列，其对应的特征函数序列为 $\{\varphi_n(t)\}$。
1. **若弱收敛则特征函数逐点收敛**：若 $X_n$ 依分布弱收敛于 $X$（记为 $X_n \xrightarrow{d} X$），则对所有 $t \in \mathbb{R}$，必有 $\lim_{n \to \infty} \varphi_n(t) = \varphi_X(t)$；
2. **反向判定定理（终极武器）**：若对每个实数 $t$，极限 $\varphi(t) = \lim_{n \to \infty} \varphi_n(t)$ 逐点存在，且极限函数 $\varphi(t)$ **在原点 $t = 0$ 处连续**！
   则：**函数 $\varphi(t)$ 必然是某个合法随机变量 $X$ 的特征函数，并且序列 $X_n$ 严格依分布弱收敛于 $X$！**
:::

正是凭借列维连续性定理，我们在后续证明**中心极限定理（CLT）**时，根本不需要处理几十个卷积积分的微积分极限，只需在一维复平面上展开泰勒级数：
$$\varphi_{\frac{S_n}{\sqrt{n}}}(t) = \left( 1 - \frac{t^2}{2n} + o(t^2/n) \right)^n \xrightarrow{n \to \infty} e^{-t^2 / 2}$$
根据 Lévy 定理，看到 $e^{-t^2/2}$ 的瞬间，全人类就可以 $100\%$ 确定：**和的极限分布必然绝对是标准正态分布！**

::: insight 旋转复向量对抗无限发散
特征函数是人类数学智慧最惊艳的华彩。
面对不可积的病态分布，实数变换束手无策；而欧拉公式 $e^{itx} = \cos tx + i \sin tx$ 将发散的实数轴轻盈地缠绕在复平面的单位圆环之上。
所有的质量逃逸与无穷发散，在单位圆的旋转周期中被完美消化中和。分析学最精妙的傅里叶核，在此化为了贯通离散与连续、有限与无限的黄金大道。
:::
