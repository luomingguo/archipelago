---
title: 严格劣势策略与优势策略剔除
type: lecture
lecture: 3
tags: [dominance, strictly-dominated, iesds, prisoners-dilemma]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 3 严格劣势策略与优势策略剔除（Dominance）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 严格劣势策略（Strictly Dominated Strategy）指无论对手选择何种策略，该策略的收益均严格劣于某备择策略。
- 理性人绝不会选择严格劣势策略，由此建立迭代剔除严格劣势策略（IESDS）算法。
- 证明 IESDS 的最终解与剔除顺序完全无关，阐明囚徒困境中个体理性与集体理性的深刻冲突。

## 核心概念与数学形式化

### 严格劣势策略的形式化定义

在标准式博弈 $G$ 中，称玩家 $i$ 的纯策略 $s_i \in S_i$ 被纯策略（或混合策略）$s_i' \in \Delta(S_i)$ **严格劣势（Strictly Dominated）**，如果对于对手的所有可能策略组合 $s_{-i} \in S_{-i}$，均有：
$$u_i(s_i', s_{-i}) > u_i(s_i, s_{-i}) \quad \forall s_{-i} \in S_{-i}$$

### 弱劣势策略定义
若上式中的严格大于改为弱大于且至少存在一个 $s_{-i}$ 严格成立：
$$u_i(s_i', s_{-i}) \ge u_i(s_i, s_{-i}) \quad \forall s_{-i}, \quad \exists s_{-i}^*: u_i(s_i', s_{-i}^*) > u_i(s_i, s_{-i}^*)$$
则称 $s_i$ 被弱劣势（Weakly Dominated）。

### 迭代剔除严格劣势策略（IESDS）
1. 设立初始策略集 $S_i^0 = S_i$。
2. 在第 $k$ 轮，剔除所有在对手受限策略集 $S_{-i}^{k-1}$ 下被严格劣势的策略，得到 $S_i^k$。
3. 重复直至没有可剔除策略，最终保留集合为 $S^\infty = \prod_i S_i^\infty$。
- **定理**：在有限博弈中，IESDS 的最终留存策略集与各轮具体的剔除顺序严格无关（Order Independence）。

## 经济应用与机制分析

公共政策（如公地治理与排污权交易）的立法宗旨，在于通过惩罚与税收重构个体的收益函数，使得“搭便车”和“过度排放”从优势策略退化为劣势策略，从而利用自利驱动达成社会最优。

## 边界条件与易错点

混淆严格劣势与弱劣势：弱劣势策略剔除的结果通常依赖于剔除顺序，可能意外删掉合法纳什均衡。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=b7BAHSV1EBo)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
严格劣势策略剔除是博弈论中最无可争议的预测基石。它甚至不需要假设对手如何精准行动，只需最弱的假定：没有理性人会主动去碰无论如何都更糟糕的选项。囚徒困境的悲剧在于，坦白是各自的严格优势策略，制度唯有改变收益矩阵才能挽救合作。
:::
