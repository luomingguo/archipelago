---
title: 双样本比较与实验设计
type: lecture
lecture: 7
tags: [two-sample-inference, matched-pairs, independent-samples, pooled-variance, welch-t-test]
status: complete
source: 'https://ocw.mit.edu/courses/15-075j-statistical-thinking-and-data-analysis-fall-2011/resources/mit15_075jf11_chpt08/'
---

# Lec 7 双样本比较与实验设计（Inferences for Two Samples）

> MIT 15.075J / ESD.07J · Statistical Thinking and Data Analysis · Fall 2011
> 授课教师：Prof. Cynthia Rudin
> 资料来源：[MIT OpenCourseWare Chapter 8 Notes](https://ocw.mit.edu/courses/15-075j-statistical-thinking-and-data-analysis-fall-2011/resources/mit15_075jf11_chpt08/)

## TL;DR

- 双样本比较是 A/B 测试、药物临床试验与工程改进实验的统计支柱；实验设计分为**独立样本设计（Independent Samples）**与**成对匹配设计（Matched Pairs）**。
- 成对设计通过在配对个体内部直接做差（$D_i = X_i - Y_i$），消除了大量未观察到的个体间固有异质性（Blocking Factor），将双样本问题转化为方差更小、检测力更高的单样本问题。
- 独立小样本比较存在分水岭：若总体方差齐性（$\sigma_1^2 = \sigma_2^2$），采用**合并样本方差（Pooled Variance $S_p^2$）**构造自由度为 $n_1 + n_2 - 2$ 的标准两样本 t 检验；若方差非齐（$\sigma_1^2 \ne \sigma_2^2$），则必须采用 **Welch-Satterthwaite 近似 t 检验**。

## 一、两大经典实验设计架构：独立样本 vs 成对匹配

在比较两种处理（例如新算法 vs 旧基线、新药治疗组 vs 安慰剂对照组）的效果差异时，数据的采集架构决定了后续统计模型的有效性。

```text
                  双样本实验数据收集范式
                            │
         ┌──────────────────┴──────────────────┐
         ▼                                     ▼
   【独立双样本设计】                     【成对匹配设计】
  (Independent Samples)                  (Matched Pairs)
         │                                     │
   两个群体完全独立                      同一受试者前后自身对照
   n₁ 与 n₂ 可以不相等                   或基于强相似特征严格配对
   存在群体固有异质噪声                  求单点差值 D_i = X_i - Y_i
   自由度 n₁ + n₂ - 2                    自由度 n - 1 (消除个体间方差)
```

### 1. 独立样本设计（Independent Samples Design）

- **样本结构：** 样本 1：$x_1, \dots, x_{n_1}$（对照组）；样本 2：$y_1, \dots, y_{n_2}$（处理组）。
- **核心假定：** 所有 $x_i$ 与 $y_j$ 相互独立；样本量 $n_1$ 与 $n_2$ 可以不相等。
- **局限性：** 若受试者本身存在巨大的个体差异（如基础心率、初始业务水平），这些未被控制的背景噪声会全部进入分母的误差方差中，大幅削弱统计功效。

### 2. 成对匹配设计（Matched Pairs Design）

- **样本结构：** 观测数据天然成对出现：$(x_1, y_1), (x_2, y_2), \dots, (x_n, y_n)$。
- **典型场景：**
  - **自身前后对照：** 同一组员工在参加专业培训前（$x_i$）与培训后（$y_i$）的业务考核得分；
  - **区组匹配（Blocking）：** 医学研究中将年龄、性别、体重指数严格相近的两人配成一对，一人服药一人服安慰剂。
- **降维机制：** 对每对观测直接计算差值：
  $$D_i = X_i - Y_i, \quad i = 1, \dots, n$$
  直接将复杂的双变量联合分布**降维转化为单变量差值序列 $D_1, \dots, D_n$**。此时只需对 $\mu_D = \mu_1 - \mu_2$ 进行单样本 t 检验：
  $$T = \frac{\bar{D} - \delta_0}{S_D / \sqrt{n}} \sim t_{n-1}$$

::: insight [成对匹配消除背景噪声的威力]
成对设计的核心精髓在于：当两变量正相关时（$\operatorname{Cov}(X, Y) > 0$，例如同一个人的基础素质决定了他前后的绝对得分均偏高），差值的方差为：
$$\operatorname{Var}(X - Y) = \operatorname{Var}(X) + \operatorname{Var}(Y) - 2\operatorname{Cov}(X, Y) < \operatorname{Var}(X) + \operatorname{Var}(Y)$$
协方差项 $-2\operatorname{Cov}(X, Y)$ 从分母中抵消了大量的个体间变异，使得微弱的干预改善效应能够极其敏锐地被识别出来。
:::

---

## 二、独立大样本均值比较（$n_1, n_2 > 30$）

当两组样本量均足够大时，由中心极限定理（CLT），样本均值差 $\bar{X} - \bar{Y}$ 渐近服从正态分布：
$$E[\bar{X} - \bar{Y}] = \mu_1 - \mu_2$$
$$\operatorname{Var}(\bar{X} - \bar{Y}) = \operatorname{Var}(\bar{X}) + \operatorname{Var}(\bar{Y}) = \frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}$$

在大样本下，可用样本方差 $s_1^2, s_2^2$ 替代未知总体方差，构建双样本大样本 z 统计量：
$$Z = \frac{(\bar{X} - \bar{Y}) - \delta_0}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}} \xrightarrow{d} \mathcal{N}(0, 1)$$

双侧置信区间相应为：
$$(\bar{X} - \bar{Y}) \pm z_{\alpha/2}\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}$$

---

## 三、独立小样本均值比较：齐方差 vs 异方差

当样本量较小（$n_1, n_2 \le 30$）且总体服从正态分布时，推断方法取决于两总体方差是否具有同质性。

### 1. 方差齐性情形（$\sigma_1^2 = \sigma_2^2 = \sigma^2$）：合并样本方差

当两总体波动幅度一致时，单独使用 $s_1^2$ 或 $s_2^2$ 都会浪费另一组的信息。我们将两组的平方和加权汇总，得到**合并样本方差（Pooled Sample Variance）**：

::: definition [合并样本方差（$S_p^2$）]
$$S_p^2 := \frac{\sum_{i=1}^{n_1} (X_i - \bar{X})^2 + \sum_{j=1}^{n_2} (Y_j - \bar{Y})^2}{(n_1 - 1) + (n_2 - 1)} = \frac{(n_1 - 1)S_1^2 + (n_2 - 1)S_2^2}{n_1 + n_2 - 2}$$
:::

由此构建的**两样本合并 t 统计量**严格服从自由度为 $n_1 + n_2 - 2$ 的 t 分布：
$$T = \frac{(\bar{X} - \bar{Y}) - \delta_0}{S_p \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}} \sim t_{n_1 + n_2 - 2}$$

对应的 $100(1-\alpha)\%$ 置信区间为：
$$(\bar{X} - \bar{Y}) \pm t_{n_1 + n_2 - 2, \alpha/2} \cdot S_p \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}$$

### 2. 方差非齐情形（$\sigma_1^2 \ne \sigma_2^2$）：Welch-Satterthwaite t 检验

现实中两组方差往往存在天然差异（例如新治疗方案在带来均值改善的同时，大幅放大了病人的个体异质性波动）。此时统计量：
$$T' = \frac{(\bar{X} - \bar{Y}) - \delta_0}{\sqrt{\frac{S_1^2}{n_1} + \frac{S_2^2}{n_2}}}$$
并不服从精确的 t 分布（著名的 Behrens-Fisher 难题）。统计学采用 **Welch 修正自由度 $\nu$** 进行稳健逼近：

::: theorem [Welch-Satterthwaite 有效自由度公式]
$$\nu \approx \frac{\left(\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}\right)^2}{\frac{(s_1^2 / n_1)^2}{n_1 - 1} + \frac{(s_2^2 / n_2)^2}{n_2 - 1}}$$
计算所得的 $\nu$ 通常非整数，实际查表或计算 p 值时通常向下取整。
:::

---

## 四、方差齐性 F 检验（F-test for Equality of Variances）

在决定使用合并方差还是 Welch 检验之前，可通过双样本方差比率检验两总体方差是否相等：
$$\begin{cases}
H_0: \sigma_1^2 = \sigma_2^2 \\
H_1: \sigma_1^2 \ne \sigma_2^2
\end{cases}$$

构建检验统计量：
$$F = \frac{S_1^2}{S_2^2} \sim \mathcal{F}_{n_1 - 1, n_2 - 1}$$

::: pitfall [F 检验对正态性假定的极端敏感脆弱性]
虽然 t 检验在非正态总体下具有一定的抗噪稳健性，但方差齐性 F 检验对总体正态性假设**极度脆弱敏感**（非正态母体的峰度偏差会剧烈破坏 F 检验的第一类错误率）。现代统计实践中，若样本具有重尾或偏态特征，优先推荐使用非参数的 Levene 检验或 Bartlett 检验，或者直接默认采用无需方差齐性假定的 Welch t 检验。
:::
