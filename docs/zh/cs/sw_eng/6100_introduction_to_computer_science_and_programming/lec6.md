---
title: 概率分布、方差与中心极限定理
type: lecture
lecture: 6
tags: [probability-distributions, variance, clt, normal-distribution, statistics]
status: complete
source: https://introcomp.mit.edu/fall26
---

# Lec 6 概率分布、方差与中心极限定理（Probability, Distributions & CLT）

> MIT 6.100 · 计算机科学与 Python 编程导论 · Fall 2026 · 教材参考：Guttag 17.2–17.4

## TL;DR

- **概率测度与随机变量**：随机变量是样本空间到实数集的映射，概率分布（离散概率质量函数 PMF 与连续概率密度函数 PDF）完整刻画了各可能结果的发生概率。
- **均值与方差度量**：期望（均值 $\mu$）衡量分布的集中趋势，方差（$\sigma^2$）与标准差（$\sigma$）衡量数据围绕均值的离散程度与不确定性风险。
- **中心极限定理（CLT）**：无论总体分布形态如何，只要具有有限均值与方差，大量独立同分布样本均值的抽样分布在样本量增大时必然渐近趋向于正态高斯分布。

## 1. 统计描述两要素：期望与离散度量

在对仿真实验产生的大量数据进行分析时，单凭肉眼观察原始输出毫无意义。我们需要能够精确凝练数据集特征的统计指标，将成千上万的散乱数据降维为具备解释力的参数。

对于包含 $N$ 个观测值的数据集 $X = \{x_1, x_2, \dots, x_N\}$，统计学定义了三项基础度量：
1. **样本均值（Sample Mean）**：
   $$\mu = \frac{1}{N} \sum_{i=1}^N x_i$$
2. **样本方差（Sample Variance）**：
   $$\sigma^2 = \frac{1}{N} \sum_{i=1}^N (x_i - \mu)^2$$
3. **标准差（Standard Deviation）**：
   $$\sigma = \sqrt{\sigma^2}$$

标准差具备与原始数据相同的物理量纲，直观表达了数据点与均值之间的平均偏离幅度。

```python
import math
from typing import List

def calculate_stats(data: List[float]) -> dict:
    """
    计算数据集的均值、方差与标准差
    """
    n = len(data)
    if n == 0:
        raise ValueError("数据集不能为空")
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    std_dev = math.sqrt(variance)
    return {"mean": mean, "variance": variance, "std_dev": std_dev}
```

---

## 2. 常见分布形态与正态分布

自然界与计算机模拟中最常见的三类基础概率分布包括：

- **均匀分布（Uniform Distribution）**：在区间 $[a, b]$ 内任意一点发生的概率密度完全恒定，如随机数发生器 `random.random()`。
- **指数分布（Exponential Distribution）**：常用于建模无记忆性的排队到达等待时间（如网络数据包间隔）。
- **正态分布（Normal / Gaussian Distribution）**：呈现经典的钟形曲线（Bell Curve），由均值 $\mu$ 和标准差 $\sigma$ 唯一决定。

::: definition 正态分布经验法则（68-95-99.7 法则）
对于服从正态分布的连续随机变量：
- 约 $68.27\%$ 的数据点落在 $[\mu - \sigma, \mu + \sigma]$ 区间内；
- 约 $95.45\%$ 的数据点落在 $[\mu - 2\sigma, \mu + 2\sigma]$ 区间内；
- 约 $99.73\%$ 的数据点落在 $[\mu - 3\sigma, \mu + 3\sigma]$ 区间内。
:::

---

## 3. 中心极限定理（CLT）及其计算实验验证

中心极限定理（Central Limit Theorem, CLT）被称为概率论中最具魔力的皇冠定理。它庄严宣告：**无论母体本身多么扭曲非对称，海量独立随机变量的求和与平均，终将汇入对称优美的正态分布**。

这一结论在计算机仿真与实际工程推断中至关重要。这意味着即使我们无法探明单个输入要素所遵循的具体几何度量，只要系统受到大量微小独立因子的共同加和作用，其整体宏观指标就必然呈现高斯正态特征。

### 实验设计与 Python 数值验证

为了彻底摆脱公式推导的空洞感，我们设计一个计算机实验：直接从 $[0.0, 1.0)$ 的连续均匀分布母体中进行密集采样。在直觉上，均匀分布的概率密度函数是一条绝对平坦的水平横线，其两端在 0 和 1 处戛然而止，完全不具备任何类似于正态分布的中间隆起或平滑拖尾特征。

我们编写两层抽样循环：内层负责单次抽样并计算样本均值，外层重复上万次以观测这些均值本身的宏观分布态势：

```python
import random

def sample_means_experiment(population_fn, sample_size: int, num_samples: int) -> List[float]:
    """
    CLT 实验引擎：每次抽取 sample_size 个独立样本求均值，重复 num_samples 次
    """
    means = []
    for _ in range(num_samples):
        sample = [population_fn() for _ in range(sample_size)]
        means.append(sum(sample) / sample_size)
    return means

# 母体生成函数：极其平坦的均匀分布，理论均值 0.5，理论标准差 1/sqrt(12) 约 0.2887
uniform_pop = lambda: random.random()

# 实验：每次抽取 50 个样本求均值，重复 10000 次
sample_means = sample_means_experiment(uniform_pop, sample_size=50, num_samples=10000)
stats = calculate_stats(sample_means)

print(f"抽样均值均值: {stats['mean']:.4f} (期望 0.5000)")
print(f"抽样均值标准差: {stats['std_dev']:.4f} (理论标准误 SE: {0.2887 / math.sqrt(50):.4f})")
```

当我们运行这段代码时，控制台输出的抽样统计指标高度印证了两条深刻的数学定理：
1. **抽样均值的无偏估计性**：成千上万次独立抽样所得均值的平均数（约 $0.5001$），与母体理论真值 $\mu = 0.5$ 达到了小数点后三位以上的精密吻合。
2. **标准误（Standard Error, SE）随样本量开方反比衰减**：抽样分布的标准差不再等于母体本身的离散度，而是收缩为：
   $$\text{SE} = \frac{\sigma_{\text{pop}}}{\sqrt{n}}$$
   在单次样本量 $n = 50$ 的条件下，抽样分布的标准差迅速压缩至约 $0.0408$。如果将每次采样的数量扩大到 $n = 200$，其不确定性离散带将进一步减半至 $0.0204$。

::: pitfall 将中心极限定理混淆于大数定律
- **大数定律（LLN）**：断言当样本量趋于无穷时，样本均值在概率意义上收敛到母体均值（描述的是点估计的极限位置）。
- **中心极限定理（CLT）**：描述的是样本均值围绕母体均值波动的**分布形状与误差散布速度**（渐近正态且方差按 $1/n$ 衰减）。
:::

## 我的理解

::: insight 从混沌中涌现秩序的数学必然
中心极限定理是现代大数据统计推断与蒙特卡洛采样的坚实立足点。它赋予了工程师极大的底气：即使我们对现实复杂系统的底层具体物理机制一无所知，只要能够通过计算机独立进行重复测量，所获取的聚合统计指标就天然进入了正态分布的已知掌控域，从而可以量化任何测量结论的不确定度。
:::
