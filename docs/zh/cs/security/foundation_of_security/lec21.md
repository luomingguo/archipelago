---
title: 差分隐私
type: lecture
lecture: 21
tags: [differential-privacy, laplace-mechanism, privacy-budget, composition-theorems]
status: complete
source: 'https://61600.csail.mit.edu/2026/'
---

# Lec 21 差分隐私
> MIT 6.1600 · Introduction to Computer Security

## TL;DR

- 传统静态脱敏与 K-匿名性无法抵御辅助信息链接与重构攻击，必须采用有严格数学保证的差分隐私（DP）。
- 差分隐私定义要求算法在仅相差单个个体的相邻数据集上，输出概率分布的比值受 $\exp(\epsilon)$ 严格约束。
- 介绍全局敏感度与拉普拉斯机制、高斯机制，阐释隐私预算 $\epsilon$ 的序列组合与高级组合性质。

## 1. 传统隐私保护手段的破灭

在现代数据分析与统计发布中，朴素的隐私保护方案普遍被证明是极其脆弱的：

- **去除直接标识符（De-identification）**：如抹去姓名与身份证号。Sweeney（2000）经典实验证明，仅凭“邮编 + 性别 + 出生日期”三元组，即可在全美人口普查数据中唯一确定 87% 的人口身份，进而与选民登记册链接破解了马萨诸塞州州长的就医记录。
- **K-匿名性（K-Anonymity）**：要求每个准标识符等价类中至少包含 $K$ 个个体。但 K-匿名无法抵御同质性攻击（Homogeneity Attack，若该类中所有人均患有同种疾病）与背景知识攻击。
- **重构攻击（Dinur-Nissim 定理, 2003）**：对数据库进行包含噪声的子集加和查询，只要查询次数达到数据规模的线性阶，对手就能以高概率利用线性规划重构出数据库中 99% 以上的全部原始记录！

结论：**任何允许对私有数据进行多次聚合统计查询的系统，若不注入经过严格数学校准的随机噪声，就必然会泄露个体隐私。**

## 2. 差分隐私的形式化定义

差分隐私（Differential Privacy, Dwork et al., 2006）不再关注“攻击者能否猜出数据”，而是从因果干预的角度提出承诺：**无论你是否参与该数据库，对外发布的统计结果的概率分布几乎完全一致**。因此，参与数据收集不会给任何个体带来额外的被识别风险。

### 2.1 相邻数据集与 $\epsilon$-差分隐私

::: definition 相邻数据集（Neighboring Databases）
两个数据集 $D, D' \in \mathcal{D}$ 互为相邻数据集（记作 $D \sim D'$），如果它们仅相差一条记录（即对称差 $|D \oplus D'| = 1$）。
:::

::: definition 纯差分隐私（$\epsilon$-Differential Privacy）
一个随机化算法 $\mathcal{M}: \mathcal{D} 	o \mathcal{S}$ 满足 $\epsilon$-差分隐私（$\epsilon$-DP），如果对于任意相邻数据集 $D \sim D'$ 以及输出空间上的任意子集 $S \subseteq \mathcal{S}$，均有：

$$\Pr[\mathcal{M}(D) \in S] \le e^\epsilon \Pr[\mathcal{M}(D') \in S]$$
:::

- $\epsilon$ 称为**隐私预算（Privacy Budget）**。
- 当 $\epsilon 	o 0$ 时，输出分布完全不受任何个体存在与否的影响，隐私保护最强，但数据效用归零。
- 现实中通常设定 $\epsilon \in (0.1, 2.0)$。

### 2.2 松弛版本：$(\epsilon, \delta)$-差分隐私

允许以极小概率 $\delta$ 发生极端隐私失效（例如偶然输出明文密钥）：

$$\Pr[\mathcal{M}(D) \in S] \le e^\epsilon \Pr[\mathcal{M}(D') \in S] + \delta$$

通常要求 $\delta \ll rac{1}{|D|}$（如 $\delta = 10^{-6}$），确保在密码学意义上几乎不可能发生灾难性泄露。

## 3. 核心机制：拉普拉斯与高斯机制

为了对确定性查询函数 $f: \mathcal{D} 	o \mathbb{R}^k$ 实现差分隐私，必须根据该函数的最坏情况波动注入噪声。

### 3.1 全局敏感度（Global Sensitivity）

::: definition $\ell_1$ 全局敏感度
查询函数 $f$ 的 $\ell_1$ 敏感度定义为任意两个相邻数据集所引致的函数输出最大变动量：

$$\Delta f = \max_{D \sim D'} \|f(D) - f(D')\|_1$$
:::

- **计数查询（Counting Query）**：“有多少人患有某种疾病？” $\implies \Delta f = 1$。
- **均值查询（Average Query）**：若数据值取自 $[0, B]$，样本量为 $N \implies \Delta f = rac{B}{N}$。

### 3.2 拉普拉斯机制（Laplace Mechanism）

拉普拉斯分布 $\mathrm{Lap}(b)$ 的概率密度函数为 $p(x) = rac{1}{2b} \exp(-rac{|x|}{b})$，其方差为 $2b^2$。

::: theorem 拉普拉斯机制定理
对于任意函数 $f: \mathcal{D} 	o \mathbb{R}^k$，算法：

$$\mathcal{M}_{	ext{Lap}}(D) = f(D) + (Y_1, \dots, Y_k)$$

其中 $Y_i \sim \mathrm{Lap}\left(rac{\Delta f}{\epsilon}ight)$ 独立同分布，则 $\mathcal{M}_{	ext{Lap}}$ 严格满足 $\epsilon$-差分隐私。
:::

### 3.3 高斯机制（Gaussian Mechanism）

当维度 $k$ 很高时，使用 $\ell_2$ 敏感度 $\Delta_2 f$ 并注入高斯噪声 $\mathcal{N}(0, \sigma^2 I_k)$ 可以获得更紧凑的误差边界。满足 $(\epsilon, \delta)$-DP 的高斯方差尺度为：

$$\sigma \ge rac{\Delta_2 f \sqrt{2\ln(1.25/\delta)}}{\epsilon}$$

## 4. 差分隐私的代数性质与组合定理

差分隐私之所以成为工业界隐私保护的标准基石，是因为它拥有两个极为强大的数学特性：

### 4.1 后处理抗性（Post-Processing Immunity）
若算法 $\mathcal{M}$ 满足 $\epsilon$-DP，则对任意（确定性或随机化的）外部函数 $g$，复合算法 $g \circ \mathcal{M}$ 依然严格满足 $\epsilon$-DP。
- 含义：攻击者拿到满足 DP 的输出后，无论采用多么先进的超级计算机、神经网络或外部背景知识数据库进行后处理挖掘，**都绝对无法放大已经由 DP 锁定的隐私泄露上限**！

### 4.2 组合性质（Composition Theorems）
- **序列组合（Sequential Composition）**：
  若算法 $\mathcal{M}_1$ 满足 $\epsilon_1$-DP，$\mathcal{M}_2$ 满足 $\epsilon_2$-DP，则将它们在同一数据集上先后运行并联合发布的整体算法满足 $(\epsilon_1 + \epsilon_2)$-DP。
- **高级组合定理（Advanced Composition）**：
  对同一数据连续执行 $k$ 次 $(\epsilon, \delta)$-DP 机制，累积隐私消耗仅按 $	ilde{O}(\epsilon \sqrt{k})$ 增长，而非朴素的 $k\epsilon$。

## 5. 中心化 DP vs 本地 DP

- **中心化差分隐私（Centralized DP）**：
  数据收集者（如美国人口普查局）是完全可信的，原始明文汇总在中心服务器，仅在对外发布查询统计结果时加噪。优点是噪声只需添加一次，统计精度极高。
- **本地差分隐私（Local DP, LDP）**：
  数据收集者不可信（如 Apple iOS 遥测、Google Chrome 词频统计）。每个用户的设备在将数据上传前自行注入本地噪声（基于随机化应答 Randomized Response）。由于每个样本都带噪，中心汇总时需要极其庞大的样本量（数千万用户）才能抹平噪声获得可用均值。

::: insight
差分隐私的本质不是建立一道防止入侵的“城墙”，而是把信息披露量度量为一种不可再生的“放射性同位素消耗预算”。每一个统计回答都在衰减系统剩余的隐私预算 $\epsilon$；当预算耗尽时，系统必须彻底停止回答任何新问题，否则隐私的数学保证便不复存在。
:::
