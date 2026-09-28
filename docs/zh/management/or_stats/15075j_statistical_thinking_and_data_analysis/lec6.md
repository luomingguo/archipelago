---
title: 单样本推断与功效分析
type: lecture
lecture: 6
tags: [confidence-interval, hypothesis-testing, t-test, statistical-power, sample-size-determination]
status: complete
source: 'https://ocw.mit.edu/courses/15-075j-statistical-thinking-and-data-analysis-fall-2011/resources/mit15_075jf11_chpt07/'
---

# Lec 6 单样本推断与功效分析（Inference for Single Samples）

> MIT 15.075J / ESD.07J · Statistical Thinking and Data Analysis · Fall 2011
> 授课教师：Prof. Cynthia Rudin
> 资料来源：[MIT OpenCourseWare Chapter 7 Notes](https://ocw.mit.edu/courses/15-075j-statistical-thinking-and-data-analysis-fall-2011/resources/mit15_075jf11_chpt07/)

## TL;DR

- 单样本参数推断包含等价的三重决策工具：**检验统计量（z / t）**、**$p$ 值比较**与**双侧置信区间**（若零假设基准 $\mu_0$ 落在 $100(1-\alpha)\%$ 置信区间之外，则在 $\alpha$ 水平下必拒绝 $H_0$）。
- 样本量确定公式 $n = \left(\frac{z_{\alpha/2}\sigma}{E}\right)^2$ 将推断精度（区间半宽 $E$）、置信水平（$z_{\alpha/2}$）与工程成本直接挂钩，明确呈现精度每提升一倍需四倍样本量的平方反比规律。
- 统计功效函数 $\pi(\mu_1) = \Phi\left(-z_\alpha + \frac{\mu_1 - \mu_0}{\sigma/\sqrt{n}}\right)$ 量化了当真实效应量为 $\mu_1$ 时成功探测到差异的概率，是科学设计实验、避免“假阴性”惨剧的前置必做计算。

## 一、双侧置信区间（Confidence Intervals）的严格代数推导

相比单一的点估计量，区间估计（Interval Estimation）为总体未知参数 $\theta$ 提供了一个具有受控可信度的数值范围 $[L, U]$，使得：
$$P(L \le \theta \le U) = 1 - \alpha$$
称 $[L, U]$ 为 $\theta$ 的 $100(1-\alpha)\%$ 双侧置信区间。

### 1. 总体方差 $\sigma^2$ 已知情形（z 区间）

设样本 $X_1, X_2, \dots, X_n \overset{\text{i.i.d.}}{\sim} \mathcal{N}(\mu, \sigma^2)$，已知总体方差 $\sigma^2$。构建枢轴量（Pivotal Quantity）：
$$Z = \frac{\bar{X} - \mu}{\sigma / \sqrt{n}} \sim \mathcal{N}(0, 1)$$

在标准正态分布的双尾各分配 $\alpha/2$ 的概率质量，定义上侧分位点 $z_{\alpha/2}$ 使得 $P(Z \ge z_{\alpha/2}) = \alpha/2$。由于对称性，双侧截断概率为：
$$P\left(-z_{\alpha/2} \le \frac{\bar{X} - \mu}{\sigma / \sqrt{n}} \le z_{\alpha/2}\right) = 1 - \alpha$$

对不等式链进行代数重排求解未知参数 $\mu$：
1. 各项乘以标准误 $\sigma/\sqrt{n}$：
   $$-z_{\alpha/2} \frac{\sigma}{\sqrt{n}} \le \bar{X} - \mu \le z_{\alpha/2} \frac{\sigma}{\sqrt{n}}$$
2. 同减样本均值 $\bar{X}$ 并同乘负号（反转不等号）：
   $$\bar{X} - z_{\alpha/2} \frac{\sigma}{\sqrt{n}} \le \mu \le \bar{X} + z_{\alpha/2} \frac{\sigma}{\sqrt{n}}$$

由此推导出均值 $\mu$ 的经典 $100(1-\alpha)\%$ 置信区间公式：
$$\left[\bar{X} - z_{\alpha/2}\frac{\sigma}{\sqrt{n}}, \quad \bar{X} + z_{\alpha/2}\frac{\sigma}{\sqrt{n}}\right]$$

### 2. 总体方差 $\sigma^2$ 未知情形（t 区间）

在绝大多数真实工业场景中，总体真实方差 $\sigma^2$ 不可能预先获知。使用样本标准差 $S = \sqrt{\frac{1}{n-1}\sum (X_i - \bar{X})^2}$ 替代 $\sigma$：
$$T = \frac{\bar{X} - \mu}{S / \sqrt{n}} \sim t_{n-1}$$

根据学生氏 t 分布临界值 $t_{n-1, \alpha/2}$，推导出小样本正态总体的 t 置信区间：
$$\left[\bar{X} - t_{n-1, \alpha/2}\frac{S}{\sqrt{n}}, \quad \bar{X} + t_{n-1, \alpha/2}\frac{S}{\sqrt{n}}\right]$$

::: pitfall [置信区间的经典认知谬误]
绝不能说“总体真实均值 $\mu$ 落在区间 $[L, U]$ 内的概率为 $95\%$”。
- **频率学派真谛：** 未知参数 $\mu$ 是一个客观存在的固定常数，没有任何随机性；真正随机的是由随机抽样所计算出的**区间端点 $[L, U]$ 本身**。
- **准确诠释：** 若我们按照相同流程独立重复进行 100 次抽样并计算出 100 个不同的置信区间，其中大约有 95 个区间会成功覆盖真实的总体参数 $\mu$。
:::

---

## 二、样本容量确定：精度与成本的工程博弈

在发起一项大规模临床试验、社会调查或工业质检前，产品经理或工程师面临的首要决策就是：“我们究竟需要采集多少个样本（$n$）？”

设实验设计要求置信区间的最大误差容限（区间半宽，Margin of Error）不超过 $E$：
$$E = z_{\alpha/2} \frac{\sigma}{\sqrt{n}}$$

两边平方并解出样本量 $n$：
$$n = \left(\frac{z_{\alpha/2} \sigma}{E}\right)^2$$

::: example [智能穿戴设备心率测量采样规划]
某硬件团队正在校准一款新手环的心率传感器。已知该场景下心率标准差大约为 $\sigma = 12 \text{ bpm}$。若管理层要求在 $95\%$ 置信度下（$\alpha = 0.05 \implies z_{0.025} = 1.96$），平均心率测量的误差半宽不得超过 $E = 2 \text{ bpm}$：
$$n = \left(\frac{1.96 \times 12}{2}\right)^2 = (1.96 \times 6)^2 = 11.76^2 \approx 138.3$$
取向上整，实验至少需要招募 $n = 139$ 名受试者。若想将误差进一步减半至 $E = 1 \text{ bpm}$，所需样本量将暴增至 $139 \times 4 \approx 553$。
:::

---

## 三、统计功效分析（Power Calculations）与功效函数

假设检验不仅要控制犯第一类错误的假阳性概率 $\alpha$，还必须确保当真实世界存在明确业务改善时，实验具有足够的能力将其检测出来。

### 1. 单侧检验功效函数的精确推导

考察右单侧均值假设检验：
$$\begin{cases}
H_0: \mu \le \mu_0 \\
H_1: \mu > \mu_0 \quad (\text{具体考察某个真实备择值 } \mu = \mu_1 > \mu_0)
\end{cases}$$

检验的决策准则是：当标准化统计量 $Z = \frac{\bar{X} - \mu_0}{\sigma/\sqrt{n}} \ge z_\alpha$ 时拒绝 $H_0$。将其还原为样本均值临界值形式：
$$\text{拒绝域：} \quad \bar{X} \ge \mu_0 + z_\alpha \frac{\sigma}{\sqrt{n}}$$

根据定义，**统计功效（Statistical Power）** 是在真实均值确实为 $\mu_1$ 时成功拒绝 $H_0$ 的概率，记作功效函数 $\pi(\mu_1)$：
$$\pi(\mu_1) = P\left(\bar{X} \ge \mu_0 + z_\alpha \frac{\sigma}{\sqrt{n}} \;\middle|\; \mu = \mu_1\right)$$

在条件 $\mu = \mu_1$ 下，样本均值服从 $\bar{X} \sim \mathcal{N}\left(\mu_1, \frac{\sigma^2}{n}\right)$。对其进行真均值标准化：
$$Z_{\text{true}} = \frac{\bar{X} - \mu_1}{\sigma / \sqrt{n}} \sim \mathcal{N}(0, 1)$$

不等式两边同减去 $\mu_1$ 并除以 $\sigma/\sqrt{n}$：
$$\begin{aligned}
\pi(\mu_1) &= P\left(\frac{\bar{X} - \mu_1}{\sigma/\sqrt{n}} \ge \frac{\mu_0 - \mu_1 + z_\alpha \frac{\sigma}{\sqrt{n}}}{\sigma/\sqrt{n}}\right) \\
&= P\left(Z_{\text{true}} \ge z_\alpha - \frac{\mu_1 - \mu_0}{\sigma/\sqrt{n}}\right) \\
&= 1 - \Phi\left(z_\alpha - \frac{\mu_1 - \mu_0}{\sigma/\sqrt{n}}\right) = \Phi\left(-z_\alpha + \frac{\mu_1 - \mu_0}{\sigma/\sqrt{n}}\right)
\end{aligned}$$

::: theorem [功效敏感性四要素]
由功效公式 $\pi(\mu_1) = \Phi\left(-z_\alpha + \frac{\mu_1 - \mu_0}{\sigma/\sqrt{n}}\right)$ 可得：
1. **效应量（Effect Size $\mu_1 - \mu_0$）越大：** 真实偏离零假设越大，功效越接近 100%；
2. **样本容量 $n$ 越大：** 标准误 $\sigma/\sqrt{n}$ 越小，第二项显著增大，功效迅速提升；
3. **总体方差 $\sigma$ 越小：** 噪声抑制越强，检测力越高；
4. **显著性水平 $\alpha$ 越宽松：** 临界值 $z_\alpha$ 越小，功效越高（但以牺牲第一类错误为代价）。
:::

::: insight [功效计算如何拯救被浪费的实验预算]
许多初创企业在做 A/B 测试或临床试验时，常常草草抽取 20–30 个样本就匆忙下结论“两组无显著差异（p > 0.05）”。而实际事后计算功效发现，该实验的统计功效可能只有 $15\%$！这意味着即使新方案有重大突破，实验也有高达 $85\%$ 的概率因噪声太大而彻底漏检。没有进行前置功效规划的假设检验，本质上是在掷骰子碰运气。
:::
