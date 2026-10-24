---
title: '连续型随机变量 II：指数分布无记忆性与高斯积分 (Continuous Random Variables II)'
type: lecture
lecture: 11
tags: [exponential-distribution, memoryless-property, hazard-rate, gaussian-integral]
status: complete
---

# Lec 11 连续型随机变量 II：指数分布无记忆性与高斯积分 (Continuous Random Variables II)

> MIT 15.085J / 6.436J 概率论基础 · 讲义 11 · 授课教师：Prof. John Tsitsiklis / Devavrat Shah

## TL;DR

- 指数分布（Exponential Distribution）是实数正半轴上唯一具备无记忆性的连续分布。
- 危险率函数（Hazard Rate）$\lambda(t) = f(t) / (1 - F(t))$ 严格度量了系统的瞬时失效率。
- 高斯极坐标变换解构了正态分布归一化常数 $\sqrt{2\pi}$ 的微积分终极本源。

## 1. 唯一的时间对称性：指数分布与无记忆性（Memoryless Property）

在排队论、可靠性工程、放射性核衰变与电信网络交换中，**指数分布（Exponential Distribution）**占据着无可争议的核心统领地位。

设随机变量 $X \sim \operatorname{Exp}(\lambda)$（参数 $\lambda > 0$ 为速率率 Rate）：
$$f_X(x) = \lambda e^{-\lambda x} \mathbb{I}_{x \ge 0}, \qquad F_X(x) = 1 - e^{-\lambda x}, \quad x \ge 0$$
其期望为 $\mathbb{E}[X] = 1/\lambda$，方差为 $\operatorname{Var}(X) = 1/\lambda^2$。

指数分布之所以在随机建模中无处不在，是因为它拥有一个近乎神迹的数学特性——**无记忆性（Memoryless Property）**：

::: theorem 无记忆性充要定理 (Memoryless Property)
设非负连续随机变量 $X$ 拥有支撑集 $[0, \infty)$。
$X$ 服从指数分布，**当且仅当对于任意的时间点 $s, t \ge 0$，均满足：**
$$\mathbb{P}(X > s + t \mid X > s) = \mathbb{P}(X > t)$$
:::

通俗解释：如果你正在等待一辆到达间隔服从指数分布的公交车，假设你已经苦苦等待了 $s = 30$ 分钟车还没来；在这一刻，你还需要“额外再等至少 $t$ 分钟”的概率，**与一个刚刚走进候车站的新乘客等待至少 $t$ 分钟的概率完全没有任何区别！** 系统对过去的等待历史展现出绝对的“健忘”。

证明仅需一行代数计算：
$$\mathbb{P}(X > s + t \mid X > s) = \frac{\mathbb{P}(X > s + t)}{\mathbb{P}(X > s)} = \frac{e^{-\lambda(s + t)}}{e^{-\lambda s}} = e^{-\lambda t} = \mathbb{P}(X > t)$$

```mermaid
flowchart LR
    A[已运行时间 s 幸存: X > s] -->|条件概率测度重标定| B[过去运行历史瞬间归零!]
    B --> C[剩余寿命分布与全新设备完全等价: P(X > s+t | X > s) = P(X > t)]
```

在数学分析上，满足柯西泛函方程 $g(s+t) = g(s)g(t)$ 的连续非负降函数，只能是唯一的指数函数 $g(t) = e^{-\lambda t}$！

## 2. 可靠性工程的核心指标：危险率函数（Hazard Rate）

在设备寿命寿命预测中，并非所有机械都像指数分布那样永不老化。
定义随机变量 $X$ 的**生存函数（Survival Function）**为 $S(t) = \mathbb{P}(X > t) = 1 - F(t)$。

::: definition 危险率函数 (Hazard Rate / Failure Rate)
设连续寿命变量 $X$ 的密度为 $f(t)$。定义其在时刻 $t$ 的**瞬时危险率函数**为：
$$\lambda(t) = \lim_{\Delta t \to 0^+} \frac{\mathbb{P}(t < X \le t + \Delta t \mid X > t)}{\Delta t} = \frac{f(t)}{1 - F(t)} = -\frac{S'(t)}{S(t)} = -\frac{d}{dt} \ln S(t)$$
:::

对其积分，立即解出全局生存概率公式：
$$S(t) = \exp\left( -\int_0^t \lambda(u) \, du \right)$$

观察危险率函数的斜率走势：
- **$\lambda(t) = \lambda$（恒定常数）**：系统完全无老化，正是唯一的指数分布！
- **$\lambda'(t) > 0$（递增危险率 IFR）**：设备发生磨损老化（如汽车轴承、人体器官）；
- **$\lambda'(t) < 0$（递减危险率 DFR）**：初期故障率高、存活越久越强壮（如新上线软件 Bug 排除）。

## 3. 高斯概率积分的极坐标解构

如果说指数分布是离散与记忆的极限，那么**标准正态分布（Standard Normal Distribution / Gaussian）**则是连续概率大厦的定海神针：
$$f(x) = \frac{1}{\sqrt{2\pi}} e^{-x^2 / 2}, \quad x \in \mathbb{R}$$

初学者常震撼于分母上的常数 $\sqrt{2\pi}$：一个纯粹的概率衰减函数，为什么会精准地蹦出一个圆周率 $\pi$ 的平方根？
利用第 9 讲学到的 **Fubini-Tonelli 定理**与二维极坐标变换，高斯给出了震撼人类数学史的经典推导：

令 $I = \int_{-\infty}^\infty e^{-x^2 / 2} dx$。
将其自乘构造二维平面上的重积分：
$$I^2 = \left( \int_{-\infty}^\infty e^{-x^2 / 2} dx \right) \left( \int_{-\infty}^\infty e^{-y^2 / 2} dy \right) = \int_{-\infty}^\infty \int_{-\infty}^\infty e^{-(x^2 + y^2)/2} \, dx dy$$

在笛卡尔直角坐标系中，被积函数是一个旋转对称的钟形高维抛物曲面。
做**二维极坐标代换**：$x = r \cos \theta, y = r \sin \theta$（雅可比行列式微元 $dx dy = r \, dr d\theta$）：
$$I^2 = \int_0^{2\pi} d\theta \int_0^\infty r e^{-r^2 / 2} \, dr$$
外层角度积分直接输出 $2\pi$！
内层径向积分由于微元中恰好出现了 $r$，令 $u = r^2 / 2$（$du = r dr$）：
$$\int_0^\infty e^{-u} \, du = \left[ -e^{-u} \right]_0^\infty = 1$$
于是：
$$I^2 = 2\pi \cdot 1 = 2\pi \implies I = \sqrt{2\pi}$$

::: insight 无记忆性与旋转对称性的深层物理同一性
指数分布与高斯分布看似形态迥异，但在数学物理学深处，它们是同一种最高对称性的两种投影：
指数分布是**一维时间平移不变性**的唯一极限（无记忆性）；
高斯分布是**多维欧氏空间旋转不变性**的唯一极限（在二维中，独立性要求 $f(x)f(y) = g(x^2+y^2)$，解出来的唯一形式正是高斯！）。
大自然的概率规律从不凭空创造形式，它所有的美丽，都源于底层物理时空对对称性守恒律的最高遵循。
:::
