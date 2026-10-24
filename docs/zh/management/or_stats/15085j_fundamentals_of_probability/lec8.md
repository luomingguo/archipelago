---
title: '抽象勒贝格积分 II：Fatou 引理与控制收敛定理 (Abstract Integration II: DCT)'
type: lecture
lecture: 8
tags: [dominated-convergence, fatou-lemma, interchange-limit-expectation, l1-space]
status: complete
---

# Lec 8 抽象勒贝格积分 II：Fatou 引理与控制收敛定理 (Abstract Integration II: DCT)

> MIT 15.085J / 6.436J 概率论基础 · 讲义 8 · 授课教师：Prof. John Tsitsiklis / Devavrat Shah

## TL;DR

- 法图引理（Fatou's Lemma）建立了任意非负函数序列极限下确界积分的半连续不等式。
- 控制收敛定理（Dominated Convergence Theorem, DCT）是概率极限理论最强王牌。
- 只要存在可积上界门卫 $Y$（$\mathbb{E}[Y] < \infty$），几乎处处收敛即可无条件兑现期望收敛。

## 1. 非单调序列的底线护盾：法图引理（Fatou's Lemma）

在第 7 讲中，单调收敛定理（MCT）展现了神级威力。但它有一个极其刚性的前提条件：序列必须单调递增（$X_n \uparrow X$）。
如果随机变量序列在收敛过程中像弹簧一样上下剧烈震荡（例如 $X_n = n \mathbb{I}_{(0, 1/n)}$，剧烈冲高但几乎处处收敛于 0），积分与极限还能交换吗？

法国数学家皮埃尔·法图（Pierre Fatou）在 1906 年证明了任意非负可测序列必然恪守的**下半连续性基底**：

::: theorem 法图引理 (Fatou's Lemma)
设 $\{X_n\}$ 为任意非负随机变量序列（$X_n \ge 0$）。则恒成立如下不等式：
$$\mathbb{E}\left[ \liminf_{n \to \infty} X_n \right] \le \liminf_{n \to \infty} \mathbb{E}[X_n]$$
:::

证明仅需一行（借助单调收敛定理）：
定义单调非减序列 $Y_k = \inf_{n \ge k} X_n$。显然 $Y_k \uparrow \liminf X_n$。
根据 MCT，$\mathbb{E}[Y_k] \uparrow \mathbb{E}[\liminf X_n]$。
而由定义，$Y_k \le X_k$，故 $\mathbb{E}[Y_k] \le \mathbb{E}[X_k]$。对两边取下极限，不等式立即获证！

```mermaid
flowchart TD
    subgraph LimitConvergenceTrio [勒贝格积分三大极限收敛定理]
        MCT[单调收敛定理 MCT: 要求单调递增 X_n <= X_n+1] --> Fatou[法图引理 Fatou: 仅需非负性，给出期望下确界不等式]
        Fatou --> DCT[控制收敛定理 DCT: 只要存在可积上界 |X_n| <= Y, 完美交换极限!]
    end
```

## 2. 现代分析学的杀手锏：控制收敛定理（DCT）

法图引理给出了小于等于的不等式。在什么条件下，等号能够严格成立？
这就是应用数学与工程科学中引用频率最高、最为倚重的终极核武器——**勒贝格控制收敛定理（Dominated Convergence Theorem, DCT）**！

::: theorem 控制收敛定理 (Dominated Convergence Theorem, DCT)
设随机变量序列 $\{X_n\}$ 几乎处处收敛于 $X$（即 $\mathbb{P}(\lim_{n \to \infty} X_n = X) = 1$）。
若存在一个**非负可积随机变量 $Y$（Dominated Random Variable，满足 $\mathbb{E}[Y] < \infty$）**，使得对所有的 $n$，几乎处处恒有：
$$|X_n(\omega)| \le Y(\omega), \quad \forall n \ge 1$$
则：
1. 极限随机变量 $X$ 自身必然勒贝格可积（$X \in L^1$）；
2. **极限与期望算子严格完全可交换**：
$$\lim_{n \to \infty} \mathbb{E}[X_n] = \mathbb{E}\left[ \lim_{n \to \infty} X_n \right] = \mathbb{E}[X]$$
3. 序列在 $L^1$ 范数下强收敛：$\lim_{n \to \infty} \mathbb{E}[|X_n - X|] = 0$。
:::

**简练优雅的证明**：
因为 $|X_n| \le Y$，构造两组非负变量：$Y + X_n \ge 0$ 以及 $Y - X_n \ge 0$。
分别对其应用法图引理：
1. $\mathbb{E}[\liminf (Y + X_n)] \le \liminf \mathbb{E}[Y + X_n] \implies \mathbb{E}[Y] + \mathbb{E}[X] \le \mathbb{E}[Y] + \liminf \mathbb{E}[X_n] \implies \mathbb{E}[X] \le \liminf \mathbb{E}[X_n]$；
2. $\mathbb{E}[\liminf (Y - X_n)] \le \liminf \mathbb{E}[Y - X_n] \implies \mathbb{E}[Y] - \mathbb{E}[X] \le \mathbb{E}[Y] - \limsup \mathbb{E}[X_n] \implies \limsup \mathbb{E}[X_n] \le \mathbb{E}[X]$。
将上下极限夹逼：
$$\mathbb{E}[X] \le \liminf_{n \to \infty} \mathbb{E}[X_n] \le \limsup_{n \to \infty} \mathbb{E}[X_n] \le \mathbb{E}[X]$$
整个夹逼链条瞬间闭合！极限定理获证！

## 3. 经典反例：移动逃逸质量（Escape of Mass）

为了深刻铭记控制上界 $Y$ 的不可或缺，必须看一看失去控制时发生的经典灾难：

::: example 逃逸至无穷的质量脉冲
设样本空间为 $(0, 1)$ 配备均匀测度。
定义脉冲随机变量序列：$X_n(\omega) = n \cdot \mathbb{I}_{(0, 1/n)}(\omega)$。
1. **逐点收敛性**：对于任意固定的一点 $\omega \in (0, 1)$，只要 $n > 1/\omega$，$X_n(\omega)$ 就永远变成了 0！
   因此，几乎处处极限为 $X(\omega) = \lim X_n(\omega) = 0$！
   按照极限求期望：$\mathbb{E}[X] = \mathbb{E}[0] = 0$；
2. **然而直接求期望**：
   $\mathbb{E}[X_n] = n \cdot \mathbb{P}(0 < \omega < 1/n) = n \cdot \frac{1}{n} = 1$！
   其极限为 $\lim_{n \to \infty} \mathbb{E}[X_n] = 1 \ne 0$！
:::

为什么极限不能交换？
因为在这个反例中，函数序列在趋向无穷的过程中，把整整 1 个单位的质量浓缩在越来越狭窄的针尖上发射向了无穷大，其上界函数 $\sup_n X_n(\omega) = \frac{1}{\omega}$ 在原点附近的积分是 $\int_0^1 \frac{1}{\omega} d\omega = +\infty$，根本不存在任何可积的控制变量！
控制收敛定理如同一道坚实的防盗门，彻底杜绝了质量逃逸的把戏。

::: insight 泛函分析在概率极限中的绝对统治
控制收敛定理是分析学历史上最完美的定理之一。
在工科与物理学中，人们为了计算导数与积分的交换（参数求导 $\frac{d}{dt} \int f(x, t) dx = \int \frac{\partial f}{\partial t} dx$）、求和与积分的交换，常常提心吊胆；
而在测度论概率中，DCT 告诉我们：只要你能找到一个哪怕非常粗糙但整体积分为有限实数的保护伞 $Y$，你就可以在大自然的一切极限运算中大展拳脚。这是勒贝格积分带给人类理性思维最无价的自由。
:::
