---
title: 统计量的抽样分布与三大推导分布
type: lecture
lecture: 4
tags: [sampling-distribution, central-limit-theorem, chi-square-distribution, student-t-distribution, f-distribution]
status: complete
source: 'https://ocw.mit.edu/courses/15-075j-statistical-thinking-and-data-analysis-fall-2011/resources/mit15_075jf11_chpt05/'
---

# Lec 4 统计量的抽样分布与三大推导分布（Sampling Distributions）

> MIT 15.075J / ESD.07J · Statistical Thinking and Data Analysis · Fall 2011
> 授课教师：Prof. Cynthia Rudin
> 资料来源：[MIT OpenCourseWare Chapter 5 Notes](https://ocw.mit.edu/courses/15-075j-statistical-thinking-and-data-analysis-fall-2011/resources/mit15_075jf11_chpt05/)

## TL;DR

- 中心极限定理（CLT）确立了现代参数统计的普适地基：无论总体服从何种具体分布，独立同分布样本均值的标准化统计量在样本量 $n \to \infty$ 时均依分布收敛于标准正态分布 $\mathcal{N}(0, 1)$。
- 样本方差没有通用的非参数 CLT 结论；但在正态总体假定下，标准化样本方差服从自由度为 $n-1$ 的**卡方分布（$\chi^2_{n-1}$）**，由于使用样本均值估算总体均值而损失了 1 个自由度。
- 当总体方差 $\sigma^2$ 未知且样本量较小时，以样本标准差 $S$ 替代总体 $\sigma$ 得到的统计量脱离正态分布，服从**学生氏 t 分布（Student's t-distribution）**，其厚尾性补偿了小样本方差估计的不确定性。
- **Snedecor's F 分布**源于两个独立卡方变量除以各自自由度后的比值，是方差齐性检验、ANOVA 方差分析与线性回归总体显著性检验的核心数学工具。

## 一、中心极限定理（Central Limit Theorem, CLT）

如果说大数定律（LLN）回答了“样本均值收敛到何处”，那么中心极限定理（CLT）则进一步精确刻画了“样本均值围绕其真值波动的极限概率形态”。

::: theorem [林德伯格-列维中心极限定理（Lindeberg-Lévy CLT）]
设 $X_1, X_2, \dots, X_n$ 是来自任意分布的独立同分布（i.i.d.）随机样本序列，其具有有限总体均值 $\mu$ 与有限总体方差 $\sigma^2 > 0$。

当样本量 $n \to \infty$ 时，样本均值 $\bar{X} = \frac{1}{n}\sum_{i=1}^n X_i$ 的标准化统计量依分布收敛（Convergence in Distribution）至标准正态分布：
$$Z_n = \frac{\bar{X} - \mu}{\sigma / \sqrt{n}} \xrightarrow{d} \mathcal{N}(0, 1)$$
即对任意实数 $z$：
$$\lim_{n \to \infty} P\left(\frac{\bar{X} - \mu}{\sigma / \sqrt{n}} \le z\right) = \Phi(z)$$
其中 $\Phi(z) = \int_{-\infty}^z \frac{1}{\sqrt{2\pi}} e^{-y^2/2} dy$ 为标准正态累积分布函数。
:::

### 1. 结构分解：为什么分母是 $\sigma/\sqrt{n}$？

1. 样本均值的期望严格等于总体均值：$E[\bar{X}] = \mu$；
2. 样本均值的离散方差由于各样本独立随机扰动的抵消，被缩减为原方差的 $1/n$：
   $$\operatorname{Var}(\bar{X}) = \frac{\sigma^2}{n} \implies \operatorname{SD}(\bar{X}) = \frac{\sigma}{\sqrt{n}}$$
3. 因此，$Z_n = \frac{\bar{X} - E[\bar{X}]}{\operatorname{SD}(\bar{X})}$ 本质上就是对随机变量 $\bar{X}$ 执行的标准化变换（z-score）。

::: insight [CLT 的工程魔力与采样模拟]
CLT 的强大之处在于它对**总体原始分布形态完全解耦**。哪怕总体是严重偏斜的指数分布、双峰分布甚至是高度离散的硬币投掷，只要单次抽样独立且样本量足够（工程经验通常要求 $n \ge 30$），成千上万次重复抽样所得的样本均值直方图必然演化为标准的钟形曲线。
:::

---

## 二、样本方差的抽样分布：卡方分布（$\chi^2$ Distribution）

中心极限定理完美解决了大样本均值的分布问题，但对于样本方差 $S^2 = \frac{1}{n-1}\sum_{i=1}^n (X_i - \bar{X})^2$，不存在普适于任意总体的 CLT 类似定理。然而，在**正态总体假设**下，其分布与卡方分布严格挂钩。

### 1. 卡方分布的定义与性质

::: definition [卡方分布（Chi-Square Distribution）]
设 $Z_1, Z_2, \dots, Z_\nu \overset{\text{i.i.d.}}{\sim} \mathcal{N}(0, 1)$ 为 $\nu$ 个相互独立且服从标准正态分布的随机变量。定义其平方和为：
$$X = \sum_{i=1}^\nu Z_i^2 \sim \chi^2_\nu$$
称 $X$ 服从自由度为 $\nu$ 的卡方分布。其概率密度函数为：
$$f(x) = \frac{1}{2^{\nu/2}\Gamma(\nu/2)} x^{\nu/2 - 1} e^{-x/2}, \quad x \ge 0$$
:::

卡方分布是伽马分布在 $\lambda = 1/2, r = \nu/2$ 时的特例，其期望与方差为：
$$E[\chi^2_\nu] = \nu, \quad \operatorname{Var}(\chi^2_\nu) = 2\nu$$

### 2. 样本方差的卡方抽样定理

::: theorem [样本方差抽样分布定理]
若 $X_1, X_2, \dots, X_n \overset{\text{i.i.d.}}{\sim} \mathcal{N}(\mu, \sigma^2)$，则：
$$\frac{(n-1)S^2}{\sigma^2} = \frac{\sum_{i=1}^n (X_i - \bar{X})^2}{\sigma^2} \sim \chi^2_{n-1}$$
并且，样本均值 $\bar{X}$ 与样本方差 $S^2$ 相互统计独立。
:::

**推导 $S^2$ 的矩特征：**
1. 期望：
   $$E[S^2] = E\left[\frac{\sigma^2}{n-1}\chi^2_{n-1}\right] = \frac{\sigma^2}{n-1}E[\chi^2_{n-1}] = \frac{\sigma^2}{n-1}(n-1) = \sigma^2$$
2. 方差：
   $$\operatorname{Var}(S^2) = \operatorname{Var}\left(\frac{\sigma^2}{n-1}\chi^2_{n-1}\right) = \frac{\sigma^4}{(n-1)^2}\operatorname{Var}(\chi^2_{n-1}) = \frac{\sigma^4}{(n-1)^2} \cdot 2(n-1) = \frac{2\sigma^4}{n-1}$$

当 $n \to \infty$ 时，$\operatorname{Var}(S^2) \to 0$，$S^2$ 均方收敛于 $\sigma^2$。

::: pitfall [卡方分布必须依赖已知 $\sigma$]
请注意，$\frac{(n-1)S^2}{\sigma^2}$ 作为一个可查询概率临界表的已知分布，必须依赖于已知的总体方差 $\sigma^2$。如果总体方差 $\sigma^2$ 本身未知，我们无法单纯依靠卡方分布完成对未知均值的单样本推断。
:::

---

## 三、小样本下的真实救星：学生氏 t 分布（Student's t-Distribution）

在 20 世纪初吉尼斯酿酒厂（Guinness Brewery）的质量控制实践中，威廉·戈塞（William Sealy Gosset，笔名“Student”）面临的真实困境是：样本量极小（$n < 10$），且总体真实方差 $\sigma^2$ 完全未知。

若仍直接把未知的 $\sigma$ 简单粗暴替换为样本估计量 $S$：
$$T = \frac{\bar{X} - \mu}{S / \sqrt{n}}$$
此时分母本身是一个具有显著随机波动的随机变量，因此 $T$ 不再服从高斯分布。

### 1. t 分布的数学构造与几何意义

将 $T$ 统计量在分子分母同除以 $\sigma/\sqrt{n}$：
$$T = \frac{\frac{\bar{X} - \mu}{\sigma / \sqrt{n}}}{\sqrt{\frac{S^2}{\sigma^2}}} = \frac{Z}{\sqrt{\frac{\chi^2_{n-1}}{n-1}}}$$
其中分子 $Z \sim \mathcal{N}(0, 1)$，分母为独立卡方随机变量除以其自由度的平方根。由此推导出的分布即为自由度 $\nu = n-1$ 的 **Student's t 分布**。

其概率密度函数为：
$$f(t) = \frac{\Gamma\left(\frac{\nu+1}{2}\right)}{\sqrt{\pi\nu}\,\Gamma\left(\frac{\nu}{2}\right)} \left(1 + \frac{t^2}{\nu}\right)^{-\frac{\nu+1}{2}}, \quad -\infty < t < \infty$$

### 2. t 分布的核心特征与渐近性质

1. **对称性：** 与标准正态分布一样，围绕 $t = 0$ 严格左右对称。
2. **厚尾性（Heavy Tails）：** 相比高斯分布，t 分布曲线在峰值处更平缓，而在尾部概率更厚。这是因为分母 $S$ 的随机波动放大了极端偏差的出现几率，提供了更保守的置信边界。
3. **渐近收敛性：** 当样本量 $n \to \infty$（自由度 $\nu \to \infty$）时，由大数定律 $S^2/\sigma^2 \to 1$，分母几乎变为常数 1，此时：
   $$t_\nu \xrightarrow{d} \mathcal{N}(0, 1)$$

---

## 四、双样本方差比率：Snedecor's F 分布

在许多工业对比试验中（例如比较两种不同生产工艺的稳定性，或比较新旧两款算法预测误差的离散程度），核心问题是检验两组独立的总体方差是否相等：$\sigma_1^2 = \sigma_2^2$。

### 1. F 分布的定义与构建

::: definition [F 分布（F-Distribution）]
设 $U \sim \chi^2_{\nu_1}$ 与 $V \sim \chi^2_{\nu_2}$ 为两个相互独立的卡方随机变量。定义其各自除以对应自由度之后的比值为：
$$W = \frac{U / \nu_1}{V / \nu_2} \sim \mathcal{F}_{\nu_1, \nu_2}$$
称 $W$ 服从第一自由度（分子自由度）为 $\nu_1$、第二自由度（分母自由度）为 $\nu_2$ 的 F 分布。
:::

### 2. 在样本方差比中的应用

对于来自两独立正态总体的样本，其样本方差满足：
$$\frac{(n_1 - 1)S_1^2}{\sigma_1^2} \sim \chi^2_{n_1-1}, \quad \frac{(n_2 - 1)S_2^2}{\sigma_2^2} \sim \chi^2_{n_2-1}$$
将其构造成 F 统计量：
$$F = \frac{\frac{(n_1-1)S_1^2 / \sigma_1^2}{n_1-1}}{\frac{(n_2-1)S_2^2 / \sigma_2^2}{n_2-1}} = \frac{S_1^2 / \sigma_1^2}{S_2^2 / \sigma_2^2} \sim \mathcal{F}_{n_1-1, n_2-1}$$

在原假设 $\sigma_1^2 = \sigma_2^2$ 成立的零假定下，两总体方差对消，统计量简化为纯样本方差之比：
$$F = \frac{S_1^2}{S_2^2} \sim \mathcal{F}_{n_1-1, n_2-1}$$

### 3. F 分布的倒数倒置性质

由于 F 统计量由比率构成，若颠倒分子分母次序，其分布自由度随之互换：
$$F_{\nu_1, \nu_2} = \frac{1}{F_{\nu_2, \nu_1}}$$
由此导出临界值反转定理，极大简化了查表与计算：
$$f_{\nu_1, \nu_2, 1-\alpha} = \frac{1}{f_{\nu_2, \nu_1, \alpha}}$$

---

## 五、四大抽样分布关系总览图

正态总体下的四大基础抽样分布构成了一个紧密嵌套的数学网络：

```text
               正态总体 X_i ~ N(μ, σ²)
                        │
         ┌──────────────┴──────────────┐
         ▼                             ▼
   样本均值 X̄                   标准化平方和
   X̄ ~ N(μ, σ²/n)              (n-1)S²/σ² ~ χ²_{n-1}
         │                             │
         │           ┌─────────────────┤
         ▼           ▼                 ▼
   Z = (X̄-μ)/(σ/√n)  分母抽样         双独立样本方差比
   Z ~ N(0, 1)       T = Z/√(χ²/ν)    F = (S₁²/σ₁²) / (S₂²/σ₂²)
         │           T ~ t_{n-1}      F ~ F_{n₁-1, n₂-1}
         │               │
         └─ (n → ∞) ─────┘
```

这一拓扑网络展示了参数统计学中四大核心抽样分布之间的深厚血缘关联：

1. **高斯母体（Normal Distribution）：** 作为一切古典参数推断的理论源头，生成了具有尺度缩放特征的样本均值统计量 $Z$。当样本容量增大时，由中心极限定理（CLT）担保，非正态总体的样本均值亦迅速向正态分布收敛。
2. **平方和测度（Chi-Square Distribution）：** 捕捉了正态样本方差围绕总体真实方差离散波动的平方和行为。自由度 $n-1$ 恰如其分地反映了样本均值锚定所消耗的自由约束。
3. **复合小样本利器（Student's t Distribution）：** 通过将标准正态随机变量与卡方变量的平方根进行商运算，彻底化解了现实工程中总体方差未知时的均值估计困境；其特有的重尾特性为小样本决策提供了更为稳健保守的安全边界，且在 $n \to \infty$ 时平滑回退至高斯分布。
4. **方差比率判别（Fisher-Snedecor F Distribution）：** 则将两个独立卡方变量除以各自自由度的比值统一为尺度分析利器，构成了后续双样本方差齐性检验、ANOVA 单因素/多因素方差分析以及线性回归全模型显著性检验的通用判定基石。

掌握这四大分布的衍生脉络与假设边界，便掌握了统计推断从单参数点估计向多元假设检验跨越的关键钥匙。
