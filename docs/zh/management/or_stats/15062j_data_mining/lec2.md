---
title: '贝叶斯决策论与朴素贝叶斯分类器 (Classification, Bayes Rule & Naive Bayes)'
type: lecture
lecture: 2
tags: [naive-bayes, bayes-rule, text-classification, conditional-independence]
status: complete
---

# Lec 2 贝叶斯决策论与朴素贝叶斯分类器 (Classification, Bayes Rule & Naive Bayes)

> MIT 15.062J 数据挖掘 · 讲义 2 · 授课教师：Prof. Roy Welsch / Nitin Patel

## TL;DR

- 贝叶斯决策论确立了最小化后验错误率的理论最优分类分界线（贝叶斯最优分类器）。
- 朴素贝叶斯（Naïve Bayes）引入条件独立性假定，奇迹般攻克了高维联合似然概率的维度爆炸难题。
- 极大似然估计与拉普拉斯平滑（Laplace Smoothing）解决了零频词概率为零引发的“一票否决”系统崩溃。
- 在垃圾邮件过滤与高维文本分类中，朴素贝叶斯展现出惊人的极速计算效率与超强抗噪声能力。

## 1. 贝叶斯最优分类器理论

在统计分类理论中，假设自然界的数据生成过程遵循某种客观的真实概率分布。对于输入特征向量 $X = (x_1, x_2, \dots, x_p)$ 与类别标签 $Y \in \{C_1, C_2, \dots, C_K\}$，如果我们已知真实世界中两组核心概率分布：
1. **先验概率（Prior Probability, $P(C_k)$）**：在未观察到具体特征前，随机抽取一个样本属于类别 $C_k$ 的自然发生概率；
2. **类条件概率密度（Class-Conditional Density / 似然率, $P(X \mid C_k)$）**：在已知样本属于类别 $C_k$ 的前提下，观测到特征组合 $X$ 的概率。

依据**贝叶斯定理（Bayes' Rule）**，我们可以反向推导出在看到观测特征 $X$ 之后，样本属于类别 $C_k$ 的**后验概率（Posterior Probability）**：
$$P(C_k \mid X) = \frac{P(X \mid C_k) P(C_k)}{P(X)} = \frac{P(X \mid C_k) P(C_k)}{\sum_{l=1}^K P(X \mid C_l) P(C_l)}$$

::: theorem [贝叶斯最优决策准则 (Bayes Optimal Classifier)]
为了极小化分类的平均期望错误率（Misclassification Error Rate），最优的决策规则是选择使后验概率最大的那个类别（最大后验概率法则，MAP）：
$$\hat{Y} = \arg\max_{C_k} P(C_k \mid X) = \arg\max_{C_k} P(X \mid C_k) P(C_k)$$
分母 $P(X)$ 对所有候选类别均相同，因此在比较大小时可以完全忽略。
理论证明：**贝叶斯分类器的期望错误率（称为贝叶斯误差率 Bayes Error Rate）是全宇宙所有可能分类器在理论上能够达到的最低理论极限**。
:::

```mermaid
flowchart TD
    Obs[输入高维特征向量 X: 如邮件包含的一万个词项] --> Likelihood[计算类条件似然率: P X | 垃圾邮件 vs P X | 正常邮件]
    Likelihood --> CondIndep[核心假定: 特征之间在给定类别下严格条件独立]
    CondIndep --> Product["条件概率直接连乘: P x_1|C * P x_2|C * ... * P x_p|C"]
    Product --> Posterior["后验得分计算: 似然乘积 * 先验概率 P C"]
    Posterior --> MAP[MAP 判决: 选择后验得分最大类别]
```

## 2. “朴素”假设的魔力：条件独立性

如果贝叶斯公式如此完美，为什么在实际商业中不能直接使用？
因为现实中的**类条件联合概率分布 $P(x_1, x_2, \dots, x_p \mid C_k)$ 极其难以直接从数据中估计**！
设每个自变量仅仅只有 2 种离散取值（如 0 或 1），当特征维度 $p = 50$ 时，特征空间包含 $2^{50} \approx 10^{15}$ 种可能的组合。即使企业拥有 1 亿条用户记录，绝大多数特征组合在样本库中出现的频次也严格为零，根本无法统计出多维联合似然概率。

朴素贝叶斯算法在这里做出了一个极其大胆、近乎幼稚（Naïve）的假设——**类条件独立性假定（Conditional Independence Assumption）**：
**假设在给定类别 $C_k$ 的条件下，输入向量中的所有特征 $x_1, x_2, \dots, x_p$ 相互之间在统计上严格独立**！

根据独立随机变量的乘法定理，高维联合似然概率瞬间瓦解为 $p$ 个单变量边际似然概率的简单连乘积：
$$P(x_1, x_2, \dots, x_p \mid C_k) = \prod_{j=1}^p P(x_j \mid C_k) = P(x_1 \mid C_k) \times P(x_2 \mid C_k) \times \dots \times P(x_p \mid C_k)$$

### 2.1 朴素贝叶斯分类判决公式

$$\hat{Y}_{\text{NB}} = \arg\max_{C_k} \left[ P(C_k) \prod_{j=1}^p P(x_j \mid C_k) \right]$$
在计算机数值计算中，为了防止几十个小于 1 的概率连续相乘引发浮点数**下溢（Arithmetic Underflow）**，通常两边取自然对数，将乘法转化为平稳的加法运算：
$$\hat{Y}_{\text{NB}} = \arg\max_{C_k} \left[ \ln P(C_k) + \sum_{j=1}^p \ln P(x_j \mid C_k) \right]$$

## 3. 拉普拉斯平滑（Laplace Smoothing）与工程实操

在自然语言文本分类中，朴素贝叶斯最经典的战场当属**垃圾邮件过滤器（Spam Filtering）**。

假设语料库包含 20,000 个词汇。对于一封新的待测邮件，我们统计其中包含的单词。如果某个生僻词（例如 `"viagra"`）在训练集的“正常邮件”子库中从未出现过，那么依据最大似然估计：
$$P(\text{"viagra"} \mid \text{Normal}) = \frac{0}{N_{\text{normal}}} = 0$$
在概率连乘公式中，任何一个因子为零，将导致整个连乘积**瞬间坍塌为绝对的零（$0 \times \dots = 0$）**！
这意味着，即便这封邮件里的其余 500 个单词全部是极其正常的商务交流词汇，仅仅因为出现了一个从未在正常库中见过的生僻词，模型就会彻底一票否决正常类别，将其武断判定为垃圾邮件。

::: definition [拉普拉斯平滑 (Laplace / Add-1 Smoothing)]
为了解决零概率问题，我们在分子上伪加 1，在分母上加上可能取值的总基数 $V$（词汇表大小）：
$$\hat{P}(x_j = w \mid C_k) = \frac{\text{Count}(w, C_k) + 1}{\sum_{w' \in V} \text{Count}(w', C_k) + |V|}$$
这样确保了每一个特征在任何类别下的条件概率都严格大于零，同时对样本量庞大的高频词概率几乎不产生任何可察觉的扰动。
:::

::: example [垃圾邮件分类实战推导]
某分类器收到一封短信息，仅包含两个关键词：`"free"` 与 `"lottery"`。
训练集历史统计先验：
- 垃圾邮件先验 $P(\text{Spam}) = 0.30$，正常邮件先验 $P(\text{Ham}) = 0.70$；
- 词频似然率（经平滑后）：
  - $P(\text{"free"} \mid \text{Spam}) = 0.80, \quad P(\text{"lottery"} \mid \text{Spam}) = 0.40$
  - $P(\text{"free"} \mid \text{Ham}) = 0.05, \quad P(\text{"lottery"} \mid \text{Ham}) = 0.01$

计算后验得分（非归一化）：
1. 垃圾邮件后验得分：
   $$\text{Score}(\text{Spam}) = P(\text{Spam}) \times P(\text{"free"} \mid \text{Spam}) \times P(\text{"lottery"} \mid \text{Spam}) = 0.30 \times 0.80 \times 0.40 = \mathbf{0.096}$$
2. 正常邮件后验得分：
   $$\text{Score}(\text{Ham}) = P(\text{Ham}) \times P(\text{"free"} \mid \text{Ham}) \times P(\text{"lottery"} \mid \text{Ham}) = 0.70 \times 0.05 \times 0.01 = \mathbf{0.00035}$$

后验归一化真实概率：
$$P(\text{Spam} \mid \text{Text}) = \frac{0.096}{0.096 + 0.00035} = \frac{0.096}{0.09635} \approx \mathbf{99.64\%}$$
系统以近乎绝对的把握将其直接拦截并投入垃圾箱。
:::

::: pitfall [条件独立性假设在强相关特征下的概率极化]
在现实中，词语之间往往存在强关联（例如 `"Hong"` 后面极大概率跟随 `"Kong"`）。朴素贝叶斯重复计算这两个高度绑定的词汇，相当于对同一个语义证据进行了双重甚至三重重复计票，导致最终输出的后验概率极其容易极化在接近 $1.0$ 或接近 $0.0$ 的极端边缘。虽然这很少影响最终分类排序的准确性，但导致其概率绝对值无法直接作为可靠的校准置信度使用。
:::

::: insight [我的理解：为什么荒谬的假设能产出伟大的模型？]
朴素贝叶斯的“条件独立性”在常识上显然是错误的——语言中充斥着严密的语法制约与前后呼应，没有任何一个词是真正孤立的。但现代机器学习的一个深刻哲学正在于：**模型的有效性并不取决于其微观假设有多真实，而取决于其对目标任务的鲁棒性**。分类器只需判断哪边的概率更高，而无需精准计算其绝对真值。正是这种大刀阔斧的“朴素”裁剪，赋予了它在大规模文本洪流中秒级吞吐的无敌生命力。
:::
