---
title: '积测度空间与 Fubini-Tonelli 积分次序交换定理 (Product Measures & Fubini Theorem)'
type: lecture
lecture: 9
tags: [product-measure, fubini-theorem, tonelli-theorem, joint-distributions]
status: complete
---

# Lec 9 积测度空间与 Fubini-Tonelli 积分次序交换定理 (Product Measures & Fubini Theorem)

> MIT 15.085J / 6.436J 概率论基础 · 讲义 9 · 授课教师：Prof. John Tsitsiklis / Devavrat Shah

## TL;DR

- 积测度空间 $(\Omega_1 \times \Omega_2, \mathcal{F}_1 \otimes \mathcal{F}_2, \mathbb{P}_1 \times \mathbb{P}_2)$ 严谨形式化了多维联合概率。
- 托内利定理（Tonelli）保证了非负可测函数的重积分与累次积分可无条件交换次序。
- 富比尼定理（Fubini）将交换合法性推广至绝对可积函数，奠定联合密度与边缘分布的测度桥梁。

## 1. 积测度空间与联合概率分布的代数构建

在处理多维随机变量 $(X, Y)$ 时，我们面对的是两个试验系统的联合发生。如何严格定义二维乘积空间上的概率？

设有两个独立的概率空间 $(\Omega_1, \mathcal{F}_1, \mathbb{P}_1)$ 与 $(\Omega_2, \mathcal{F}_2, \mathbb{P}_2)$。
定义样本空间的笛卡尔积（Cartesian Product）：
$$\Omega = \Omega_1 \times \Omega_2 = \{(\omega_1, \omega_2) \mid \omega_1 \in \Omega_1, \; \omega_2 \in \Omega_2\}$$

在积空间上，最基础的几何砖块是**可测矩形（Measurable Rectangle）**：$A \times B$，其中 $A \in \mathcal{F}_1, B \in \mathcal{F}_2$。
由所有可测矩形生成的最小 $\sigma$-代数，称为**乘积 $\sigma$-代数（Product $\sigma$-Algebra）**，记为：
$$\mathcal{F} = \mathcal{F}_1 \otimes \mathcal{F}_2 = \sigma\left( \{A \times B \mid A \in \mathcal{F}_1, \; B \in \mathcal{F}_2\} \right)$$

由卡拉西奥多里扩张定理，存在唯一确定的**积测度（Product Measure）** $\mathbb{P} = \mathbb{P}_1 \times \mathbb{P}_2$，使得在任意可测矩形上的测度完全等于边缘测度的标量乘积：
$$\mathbb{P}(A \times B) = \mathbb{P}_1(A) \cdot \mathbb{P}_2(B)$$

```mermaid
flowchart LR
    subgraph ProductConstruction [积测度空间构建流程]
        R1[空间 1: (Omega_1, F_1, P_1)]
        R2[空间 2: (Omega_2, F_2, P_2)]
    end
    R1 & R2 --> Rect[可测矩形: A x B, 测度赋权 P1(A) * P2(B)]
    Rect --> Gen[生成乘积代数: F_1 (x) F_2]
    Gen --> Extension[卡拉西奥多里唯一延拓: 积测度空间 (Omega_1 x Omega_2, F_1 (x) F_2, P_1 x P_2)]
```

## 2. 托内利定理（Tonelli's Theorem）：非负函数的无条件交换

在微积分中，计算重积分最常见的手段是化为累次积分（Iterated Integrals）：先对 $x$ 积分再对 $y$ 积分，或者颠倒过来。
意大利数学家莱昂尼达·托内利（Leonida Tonelli）证明了一个令人极度安心的定理：

::: theorem 托内利定理 (Tonelli's Theorem)
设 $f(\omega_1, \omega_2)$ 是积测度空间上的**非负可测函数（$f \ge 0$）**。
则：
1. 截面函数可测：对于几平所有的 $\omega_1$，切片函数 $f(\omega_1, \cdot)$ 在 $\Omega_2$ 上可测；
2. **累次积分与重积分完全等价，且求积分次序可以无条件自由交换**：
$$\int_{\Omega_1 \times \Omega_2} f \, d(\mathbb{P}_1 \times \mathbb{P}_2) = \int_{\Omega_1} \left( \int_{\Omega_2} f(\omega_1, \omega_2) \, d\mathbb{P}_2 \right) d\mathbb{P}_1 = \int_{\Omega_2} \left( \int_{\Omega_1} f(\omega_1, \omega_2) \, d\mathbb{P}_1 \right) d\mathbb{P}_2$$
（即使积分结果为 $+\infty$，两侧也同时为 $+\infty$ 相等！）。
:::

托内利定理的无上价值在于：**它不需要函数可积！只要函数非负，你闭着眼睛交换次序永远是对的！**

## 3. 富比尼定理（Fubini's Theorem）：有符号函数的严格守门员

如果函数有正有负，托内利定理不再成立。意大利数学大师圭多·富比尼（Guido Fubini）给出了终极充要保障：

::: theorem 富比尼定理 (Fubini's Theorem)
设 $f(\omega_1, \omega_2)$ 在积测度空间上是**绝对可积函数**，即满足绝对值重积分为有限实数：
$$\int_{\Omega_1 \times \Omega_2} |f(\omega_1, \omega_2)| \, d(\mathbb{P}_1 \times \mathbb{P}_2) < \infty$$
则**重积分严格等于任意次序的累次积分**：
$$\int_{\Omega_1 \times \Omega_2} f \, d\mathbb{P} = \int_{\Omega_1} \left( \int_{\Omega_2} f \, d\mathbb{P}_2 \right) d\mathbb{P}_1 = \int_{\Omega_2} \left( \int_{\Omega_1} f \, d\mathbb{P}_1 \right) d\mathbb{P}_2$$
:::

::: example 工业标准工作流：Fubini-Tonelli 组合拳
在实际科学研究与论文推导中，面对一个包含正负号的复杂双重积分 $\iint f(x, y) dx dy$：
1. **第一步（先调用 Tonelli）**：给被积函数套上绝对值 $|f(x, y)| \ge 0$。利用托内利定理，随便挑一个最好算的次序计算累次积分，验证其是否有限（$< \infty$）；
2. **第二步（再调用 Fubini）**：一旦绝对可积被第一步确立，立即合法激活富比尼定理，放心大胆地交换原函数的求和与积分次序！
:::

::: pitfall 违反绝对可积性的次序交换灾难
若忽视绝对可积性，微积分将直接爆出伪谬：
考察单位正方形上的函数 $f(x, y) = \frac{x^2 - y^2}{(x^2 + y^2)^2}$。
- 先对 $x$ 后对 $y$ 积分：$\int_0^1 [ \int_0^1 f(x, y) dx ] dy = -\frac{\pi}{4}$；
- 先对 $y$ 后对 $x$ 积分：$\int_0^1 [ \int_0^1 f(x, y) dy ] dx = +\frac{\pi}{4}$！
同一个数学对象在不同的运算顺序下算出了完全相反的物理量！根源正在于 $|f(x, y)|$ 在原点附近的重积分为 $+\infty$，它击穿了富比尼定理的安全红线。
:::

::: insight 独立性与卷积的纯净代数母体
Fubini-Tonelli 定理是整个多维概率论与统计物理的发动机。
两个独立连续随机变量之和的分布，之所以能够被优雅地写成卷积积分（Convolution $f_{X+Y}(z) = \int f_X(x) f_Y(z - x) dx$），其微观底层全部依赖积测度的代数分解与 Fubini 积分次序交换。
从可测矩形到无穷维乘积空间（Kolmogorov 延拓定理），数学家为我们铺平了一条从单粒子微观测度向多体复杂随机系统迈进的康庄大道。
:::
