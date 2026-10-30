---
title: 随机程序设计与仿真模拟基础
type: lecture
lecture: 4
tags: [simulation, stochastic-programs, pseudo-random, monte-carlo, probability]
status: complete
source: https://introcomp.mit.edu/fall26
---

# Lec 4 随机程序设计与仿真模拟基础（Simulation & Stochastic Programs）

> MIT 6.100 · 计算机科学与 Python 编程导论 · Fall 2026 · 教材参考：Guttag 18, 17.1

## TL;DR

- **确定性与随机性程序**：确定性程序对相同输入产生严格一致的输出，而随机程序（Stochastic Programs）的内部状态演进依赖概率分布，用于模拟现实世界的非确定性现象。
- **伪随机数生成机理**：计算机无法产生真随机数，通过确定性递推公式与种子（Seed）生成在统计学上无法与真随机区分的伪随机序列（Pseudo-random Sequence）。
- **蒙特卡洛模拟范式**：通过大量重复独立的随机抽样试验，利用样本统计频率逼近理论解或高维积分，以算力换取复杂数学问题的直接数值解。

## 1. 从确定性世界到随机性建模

在传统的算法范式中，程序具有绝对的确定性：给定特定的输入，无论在何时何地执行多少次，其执行轨迹与最终输出都完全固定。然而现实物理世界中的许多系统（如天气演进、金融资产波动、排队等待网络以及分子扩散）本质上受到随机扰动的影响。

为了研究这些无法通过简单闭式解析公式求解的复杂系统，计算机科学引入了**随机程序（Stochastic Programs）**。通过在代码中引入概率分布机制，我们建立数字沙盒以模拟真实事件的动态演化。

---

## 2. 伪随机数生成器与确定性可复现性

计算机本身是严格按时钟周期和布尔门工作的确定性机器。Python 标准库的 `random` 模块底层采用梅森旋转算法（Mersenne Twister），其周期长达 $2^{19937}-1$。

这种发生器根据一个初始数值——**随机种子（Seed）**，通过确定性的数学递推函数生成后续的数字流：

```python
import random

# 设置确定性随机种子以保证实验可复现
random.seed(42)

for _ in range(5):
    print(random.random())  # 生成 [0.0, 1.0) 区间内的伪随机浮点数
```

::: definition 伪随机数发生器（PRNG）
一种使用确定性算法产生在统计检验上满足均匀性与独立性假定、外观上不可预测的数字序列的计算装置。其整个序列完全由初始种子决定，保证了科学实验的高保真可复现性。
:::

### 常用随机采样原语

- `random.random()`：产生 $[0.0, 1.0)$ 上的均匀分布实数。
- `random.randint(a, b)`：闭区间 $[a, b]$ 内等概率随机整数。
- `random.choice(seq)`：从非空序列中等概率随机抽取单一元素。
- `random.sample(seq, k)`：不放回随机抽取 $k$ 个独立元素。

---

## 3. 蒙特卡洛模拟：以生日悖论为例

蒙特卡洛方法（Monte Carlo Simulation）的核心哲学是：**用巨量的计算机采样试验代替高难度的理论积分与组合推演**。

经典的“生日悖论”（Birthday Paradox）探讨：在一个包含 $K$ 个人的房间中，至少有两人生日相同的概率何时超过 $50\%$？

理论推导表明：
$$P(\text{至少两人同生日}) = 1 - \prod_{i=0}^{K-1} \left(1 - \frac{i}{365}\right)$$

通过蒙特卡洛模拟，我们可以直接编写直观的试验循环进行数值验证，而完全不需要手动展开复杂的阶乘计算：

```python
import random

def has_duplicate_birthdays(num_people: int) -> bool:
    """
    单次模拟：随机生成 num_people 个生日，判定是否存在重复
    """
    birthdays = [random.randint(1, 365) for _ in range(num_people)]
    return len(set(birthdays)) < num_people

def estimate_birthday_probability(num_people: int, num_trials: int = 10000) -> float:
    """
    蒙特卡洛外层循环：重复 num_trials 次独立模拟，统计频率
    """
    duplicates_count = 0
    for _ in range(num_trials):
        if has_duplicate_birthdays(num_people):
            duplicates_count += 1
    return duplicates_count / num_trials

# 运行模拟：测试 23 个人时的概率
prob = estimate_birthday_probability(23, num_trials=20000)
print(f"23 个人中至少两人生日相同的模拟概率约为：{prob:.4f}")  # 约 0.507
```

随着试验轮数 `num_trials` 从 100 增加至 20000，样本频率会稳步收敛到理论真实值 $0.5073$ 附近。这种将数学概率映射为代码中布尔命中统计的方法，构成了现代计算金融学与物理仿真的核心基石。

::: pitfall 蒙特卡洛模拟中的样本量偏差
蒙特卡洛方法的估计误差通常与试验次数的平方根成反比（$O(1/\sqrt{N})$）。这意味着如果希望将模拟结果的精度提高 10 倍，需要将计算量扩大 100 倍。盲目使用极小的采样量（例如仅执行 10 次模拟）无法得出具有统计显著性的科学结论。
:::

## 我的理解

::: insight 计算机作为实验科学实验室
在解析数学遇到维度灾难与非线性阻碍的地方，计算模拟开辟了第三种科学研究范式（理论推导、物理实验之外的“计算实验”）。蒙特卡洛算法教会我们：面对未知混乱的概率问题，无需先陷入繁复公式的恐慌，先构造一个贴合现实规则的仿真微型世界，让计算机快速投掷数万次骰子，答案便会自然浮出水面。
:::
