---
title: '概率论核心回顾'
type: lecture
lecture: 1
tags: [probability-space, conditional-probability, bayes-theorem, weak-law-of-large-numbers, random-variables]
status: complete
source: 'https://ocw.mit.edu/courses/15-075j-statistical-thinking-and-data-analysis-fall-2011/resources/mit15_075jf11_chpt02/'
---

# Lec 1 概率论核心回顾（Review of Probability）

> MIT 15.075J / ESD.07J · Statistical Thinking and Data Analysis · Fall 2011
> 授课教师：Prof. Cynthia Rudin
> 资料来源：[MIT OpenCourseWare Chapter 2 Notes](https://ocw.mit.edu/courses/15-075j-statistical-thinking-and-data-analysis-fall-2011/resources/mit15_075jf11_chpt02/)

## TL;DR

- 现代概率论建立在柯尔莫哥洛夫公理体系之上：样本空间 $S$、事件代数与满足非负性、规范性及可加性的概率测度 $P$。
- 条件概率 $P(A|B) = \frac{P(A \cap B)}{P(B)}$ 是统计推断的逻辑核心；严禁混淆“独立性”（$P(A \cap B) = P(A)P(B)$）与“互斥/不相交”（$P(A \cap B) = 0$）。
- 全概率定理与贝叶斯法则构成由果溯因的逆概率计算范式，是先验信念向后验证据更新的数学保证。
- 弱大数定律（WLLN）借由切比雪夫不等式严格确立：无论随机变量服从何种具体分布，随着样本量 $n \to \infty$，样本均值以概率收敛于总体真实期望 $\mu$。

## 一、概率空间与柯尔莫哥洛夫公理体系

现代数学与统计学对不确定性的建模完全统一于安德雷·柯尔莫哥洛夫（Andrey Kolmogorov）于 1933 年确立的测度论公理体系。一个规范的概率空间由三元组 $(\Omega, \mathcal{F}, P)$ 或 $(S, \mathcal{E}, P)$ 构成：

::: definition [概率空间（Probability Space）]
一个概率空间由三个核心要素构成：
1. **样本空间（Sample Space, $S$ 或 $\Omega$）：** 随机试验所有可能结果的完备集合。
   - 掷单枚骰子：$S = \{1, 2, 3, 4, 5, 6\}$；
   - 掷两枚骰子：$S = \{(i, j) \mid i, j \in \{1, \dots, 6\}\}$，包含 36 种基本结果；
   - 周一的气温测量：$S = [-50, 50] \subset \mathbb{R}$。
2. **事件集合（Event Algebra, $\mathcal{E}$）：** 样本空间 $S$ 的子集簇。每个事件 $A \in \mathcal{E}$ 是若干试验结果的集合。事件的并集、交集与补集仍构成事件。
3. **概率测度（Probability Measure, $P$）：** 定义在事件代数上的实值集合函数 $P: \mathcal{E} \to [0, 1]$，为每个事件赋予度量其发生可能性的数值。
:::

柯尔莫哥洛夫三大公理确立了概率测度必须满足的边界：
1. **非负性公理：** 对任意事件 $A$，均有 $P(A) \ge 0$。
2. **规范性公理：** 必然事件的概率为 1，即 $P(S) = 1$。
3. **可加性公理（Additivity）：** 若事件 $A$ 与 $B$ 互斥（即 $A \cap B = \emptyset$），则：
   $$P(A \cup B) = P(A) + P(B)$$
   对于可数无穷个互不相交的事件序列 $A_1, A_2, \dots$，满足可数可加性 $P\left(\bigcup_{i=1}^\infty A_i\right) = \sum_{i=1}^\infty P(A_i)$。

直观上，我们可以将概率测度 $P$ 视为定义在维恩图（Venn Diagram）上的“测度”或“面积”。

---

## 二、条件概率、独立性与贝叶斯定理

统计学与纯数学的一大分水岭在于对“信息注入”的处理。当部分信息（事件 $B$ 发生）已知时，样本空间发生动态收缩。

### 1. 条件概率的定义与乘法法则

::: definition [条件概率（Conditional Probability）]
给定事件 $B$ 发生（$P(B) > 0$），事件 $A$ 发生的条件概率定义为：
$$P(A \mid B) := \frac{P(A \cap B)}{P(B)}$$
:::

直观上，在已知 $B$ 发生的前提下，$B$ 成为新的有效样本空间，而事件 $A$ 仅能通过与 $B$ 相交的部分 $A \cap B$ 实现。乘法法则随之确立：
$$P(A \cap B) = P(A \mid B) P(B) = P(B \mid A) P(A)$$

### 2. 统计独立性 vs 互斥性

::: definition [统计独立性（Independence）]
事件 $A$ 与事件 $B$ 统计独立，当且仅当得知 $B$ 发生与否完全不改变 $A$ 发生的信念概率：
$$P(A \mid B) = P(A) \iff P(A \cap B) = P(A) P(B)$$
:::

::: pitfall [混淆“独立性”与“互斥性（Disjointness）”]
初学者常将“互斥”误认为“独立”。事实恰恰相反：
- **互斥（Disjoint / Mutually Exclusive）：** 指 $A \cap B = \emptyset$，两事件在物理上绝不可能同时发生，因此 $P(A \cap B) = 0$。若 $P(A) > 0, P(B) > 0$，则互斥事件**必然高度相关**——只要 $B$ 发生，立刻断定 $A$ 绝不可能发生（$P(A|B) = 0 \ne P(A)$）。
- **独立（Independent）：** 指两事件各行其道，联合发生的概率恰好等于各自边际概率之积 $P(A \cap B) = P(A)P(B) > 0$。
:::

### 3. 全概率公式与贝叶斯法则

设样本空间 $S$ 存在一个完备分割（Partition）$B_1, B_2, \dots, B_n$，满足两两互斥（$\forall i \ne j, B_i \cap B_j = \emptyset$）且其并集覆盖全集（$\bigcup_{i=1}^n B_i = S$）。

对于任意事件 $A$，可将其拆分为 $A = \bigcup_{i=1}^n (A \cap B_i)$。由可加性与乘法法则，导出**全概率公式**：
$$P(A) = \sum_{i=1}^n P(A \cap B_i) = \sum_{i=1}^n P(A \mid B_i) P(B_i)$$

结合条件概率定义，推导出经典的**贝叶斯定理（Bayes' Rule）**：
$$P(B_k \mid A) = \frac{P(A \mid B_k) P(B_k)}{P(A)} = \frac{P(A \mid B_k) P(B_k)}{\sum_{i=1}^n P(A \mid B_i) P(B_i)}$$

::: example [罕见病筛查假阳性悖论]
某罕见病在人群中的先验患病率为 $P(D) = 0.001$。现有临床检测手段：
- 敏感度（真阳性率）：$P(+ \mid D) = 0.99$；
- 特异度（真阴性率）：$P(- \mid D^c) = 0.95$（即假阳性率 $P(+ \mid D^c) = 0.05$）。

若一名随机体检者的检测结果为阳性（$+$），其真实患病的概率 $P(D \mid +)$ 是多少？
利用贝叶斯法则展开：
$$P(+) = P(+ \mid D)P(D) + P(+ \mid D^c)P(D^c) = 0.99 \times 0.001 + 0.05 \times 0.999 = 0.00099 + 0.04995 = 0.05094$$
$$P(D \mid +) = \frac{0.00099}{0.05094} \approx 0.0194 \quad (1.94\%)$$
尽管测试工具号称“99% 准确”，但阳性结果中绝大多数仍是健康人的假阳性。这证明了在极小先验发生率下，假阳性噪声将压倒微弱的真实信号。
:::

---

## 三、随机变量、矩与联合分布特性

### 1. 期望、方差与分位数

- **期望（Expectation）：** 离散型 $E[X] = \sum_x x f(x)$，连续型 $E[X] = \int_{-\infty}^\infty x f(x) dx$。
- **方差（Variance）：** 衡量数值围绕均值的离散程度：
  $$\operatorname{Var}(X) := \sigma^2 = E[(X - \mu)^2] = E[X^2] - (E[X])^2$$
- **分位数（Quantile）：** 对连续累积分布函数 $F(x) = P(X \le x)$，其第 $p$ 分位数 $\theta_p$ 满足 $F(\theta_p) = p$。第 0.5 分位数即为中位数（Median）。

### 2. 协方差与相关系数

对于联合分布随机变量 $(X, Y)$，定义**协方差（Covariance）**：
$$\operatorname{Cov}(X, Y) := \sigma_{XY} = E[(X - \mu_X)(Y - \mu_Y)] = E[XY] - \mu_X \mu_Y$$

若 $X$ 与 $Y$ 统计独立，则 $E[XY] = E[X]E[Y]$，必有 $\operatorname{Cov}(X, Y) = 0$（反之不成立，不相关不代表独立）。

常用协方差运算法则：
1. $\operatorname{Cov}(X, X) = \operatorname{Var}(X)$
2. $\operatorname{Cov}(aX + c, bY + d) = ab \operatorname{Cov}(X, Y)$
3. $\operatorname{Var}(X \pm Y) = \operatorname{Var}(X) + \operatorname{Var}(Y) \pm 2\operatorname{Cov}(X, Y)$

为消除量纲影响，将协方差标准化得到**皮尔逊相关系数（Correlation Coefficient）**：
$$\rho_{XY} := \operatorname{Corr}(X, Y) = \frac{\operatorname{Cov}(X, Y)}{\sqrt{\operatorname{Var}(X)\operatorname{Var}(Y)}} = \frac{\sigma_{XY}}{\sigma_X \sigma_Y}, \quad \rho_{XY} \in [-1, 1]$$

---

## 四、极限定理：切比雪夫不等式与弱大数定律

### 1. 切比雪夫不等式（Chebyshev's Inequality）

::: theorem [切比雪夫不等式]
设随机变量 $X$ 具有有限期望 $\mu$ 与有限方差 $\sigma^2$。对任意常数 $c > 0$：
$$P(|X - \mu| \ge c) \le \frac{\sigma^2}{c^2}$$
若设 $c = k\sigma$，则 $P(|X - \mu| \ge k\sigma) \le \frac{1}{k^2}$。
:::

切比雪夫不等式是非参数性质的保守上界：无论随机变量服从何种具体分布（哪怕严重偏斜），距离均值超过 2 个标准差的概率绝对不超过 $1/4 = 25\%$；距离均值超过 3 个标准差的概率绝对不超过 $1/9 \approx 11.1\%$。

### 2. 弱大数定律（Weak Law of Large Numbers, WLLN）

假设披萨店老板想要评估每天平均售出的披萨份数。设第 $i$ 天的销量为随机变量 $X_i$，观测 $n$ 天后的样本平均销量为：
$$\bar{X}_n = \frac{1}{n} \sum_{i=1}^n X_i$$

::: theorem [弱大数定律（WLLN）]
设 $X_1, X_2, \dots, X_n$ 为独立同分布（i.i.d.）的随机变量序列，共同期望为 $\mu$，有限方差为 $\sigma^2$。则对任意常数 $\epsilon > 0$：
$$\lim_{n \to \infty} P(|\bar{X}_n - \mu| \ge \epsilon) = 0$$
:::

**数学证明（基于切比雪夫不等式）：**
1. 样本均值的期望为：
   $$E[\bar{X}_n] = \frac{1}{n}\sum_{i=1}^n E[X_i] = \mu$$
2. 由于独立性，样本均值的方差为：
   $$\operatorname{Var}(\bar{X}_n) = \operatorname{Var}\left(\frac{1}{n}\sum_{i=1}^n X_i\right) = \frac{1}{n^2}\sum_{i=1}^n \operatorname{Var}(X_i) = \frac{n\sigma^2}{n^2} = \frac{\sigma^2}{n}$$
3. 将 $\bar{X}_n$ 代入切比雪夫不等式：
   $$P(|\bar{X}_n - \mu| \ge \epsilon) \le \frac{\operatorname{Var}(\bar{X}_n)}{\epsilon^2} = \frac{\sigma^2}{n\epsilon^2}$$
4. 当 $n \to \infty$ 时，右侧界限 $\frac{\sigma^2}{n\epsilon^2} \to 0$。证毕。

::: insight [大数定律消除微观不确定性的力量]
日常业务中单个样本可能波动极大（例如某天只有 1-2 位顾客，某天因举行峰会激增至 50 人），但大数定律向我们保证：只要统计时间跨度 $n$ 足够长，局部的奇异波动在宏观上必然被平均化稀释，样本均值一定会依概率稳定收敛至真实的期望中枢 $\mu$。
:::

---

## 五、精选概率分布族速查

### 1. 离散型分布

| 分布族 | 符号表述 | 概率质量函数 $P(X=x)$ | 期望 $E[X]$ | 方差 $\operatorname{Var}(X)$ | 物理与业务模型背景 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **伯努利分布** | $\operatorname{Bernoulli}(p)$ | $p^x (1-p)^{1-x}, x \in \{0, 1\}$ | $p$ | $p(1-p)$ | 单次投掷硬币、转化/未转化二元事件 |
| **二项分布** | $\operatorname{Bin}(n, p)$ | $\binom{n}{x} p^x (1-p)^{n-x}$ | $np$ | $np(1-p)$ | $n$ 次独立有放回抽样中成功发生 $x$ 次的概率 |
| **超几何分布** | $\operatorname{HyGE}(N, M, n)$ | $\frac{\binom{M}{x}\binom{N-M}{n-x}}{\binom{N}{n}}$ | $n\frac{M}{N}$ | $n\frac{M}{N}\frac{N-M}{N}\frac{N-n}{N-1}$ | **无放回**抽样；有限总体质量抽检合格品计数 |
| **多项分布** | $\operatorname{Multinomial}(n, \mathbf{p})$ | $\frac{n!}{\prod x_i!} \prod p_i^{x_i}$ | $np_i$ | $np_i(1-p_i)$ | 二项分布的多元推广（如顾客偏好 $k$ 种商品） |
| **泊松分布** | $\operatorname{Pois}(\lambda)$ | $\frac{\lambda^x e^{-\lambda}}{x!}, x \in \mathbb{N}$ | $\lambda$ | $\lambda$ | 稀有事件发生次数（二项分布 $n \to \infty, np \to \lambda$ 的极限） |

### 2. 连续型分布与正态分布性质

- **均匀分布 $U[a, b]$：** 密度函数 $f(x) = \frac{1}{b-a}$，$E[X] = \frac{a+b}{2}$。
- **指数分布 $\operatorname{Exp}(\lambda)$：** $f(x) = \lambda e^{-\lambda x} (x \ge 0)$，具有无记忆性，常用于建模排队论中连续泊松事件的到达间隔等待时间。
- **伽马分布 $\operatorname{Gamma}(\lambda, r)$：** $r$ 个独立指数分布随机变量之和。
- **高斯正态分布 $\mathcal{N}(\mu, \sigma^2)$：**
  $$f(x) = \frac{1}{\sqrt{2\pi}\sigma} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$
  通过标准化变换 $Z = \frac{X - \mu}{\sigma} \sim \mathcal{N}(0, 1)$，其累积概率记为 $\Phi(z)$。

::: theorem [正态随机变量线性组合性质]
若 $X_1, X_2, \dots, X_n \overset{\text{i.i.d.}}{\sim} \mathcal{N}(\mu, \sigma^2)$，则其样本均值 $\bar{X} = \frac{1}{n}\sum_{i=1}^n X_i$ 严格服从正态分布：
$$\bar{X} \sim \mathcal{N}\left(\mu, \frac{\sigma^2}{n}\right)$$
:::
此性质为后续构造单样本与双样本参数检验的置信区间提供了最直接的精确分布基础。
