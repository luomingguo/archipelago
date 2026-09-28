---
title: 静态不完全信息博弈与海萨尼转换
type: lecture
lecture: 16
tags: [bayesian-games, incomplete-information, harsanyi-transformation, type-space]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 16 静态不完全信息博弈与海萨尼转换（Bayesian Games）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 不完全信息博弈（Incomplete Information）：玩家不完全知晓对手的收益函数或行动能力。
- 海萨尼转换（Harsanyi Transformation）：引入虚拟玩家“自然”（Nature）选择类型，转化为不完美信息博弈。
- 形式化定义贝叶斯博弈与贝叶斯纳什均衡（Bayesian Nash Equilibrium, BNE）。

## 核心概念与数学形式化

### 贝叶斯博弈的形式化定义

一个静态贝叶斯博弈定义为一个元组：
$$\mathcal{G} = \langle I, (A_i)_{i \in I}, (\Theta_i)_{i \in I}, p, (u_i)_{i \in I} \rangle$$
1. 局中人集合：$I = \{1, 2, \dots, n\}$。
2. 行动空间：$A_i$ 表示玩家 $i$ 的纯行动集合。联合行动空间为 $A = \prod_i A_i$。
3. 类型空间：$\Theta_i$ 表示玩家 $i$ 的私人类型集合。联合类型空间为 $\Theta = \prod_i \Theta_i$。在博弈开始时，玩家 $i$ 确切知道自己的真实类型 $\theta_i \in \Theta_i$。
4. 共同先验分布（Common Prior）：$p \in \Delta(\Theta)$，所有玩家关于自然抽取各类型组合的初始概率信念。
5. 条件后验信念：给定自身类型 $\theta_i$，玩家 $i$ 利用贝叶斯法则计算对手类型的条件概率：
   $$p(\theta_{-i} \mid \theta_i) = \frac{p(\theta_i, \theta_{-i})}{\sum_{\theta_{-i}'} p(\theta_i, \theta_{-i}')}$$
6. 收益函数：$u_i(a_1, \dots, a_n; \theta_1, \dots, \theta_n)$。

### 纯策略与贝叶斯纳什均衡（BNE）
- 玩家 $i$ 的纯策略是一个映射：$s_i: \Theta_i \to A_i$。
- 策略剖面 $s^* = (s_1^*, \dots, s_n^*)$ 构成一个**贝叶斯纳什均衡**，当且仅当对每个玩家 $i$ 的每一个可能被抽中的类型 $\theta_i \in \Theta_i$，其选择的行动 $s_i^*(\theta_i)$ 均最大化其条件期望收益：
  $$s_i^*(\theta_i) \in \arg\max_{a_i \in A_i} \sum_{\theta_{-i} \in \Theta_{-i}} p(\theta_{-i} \mid \theta_i) u_i(a_i, s_{-i}^*(\theta_{-i}); \theta_i, \theta_{-i})$$

## 经济应用与机制分析

政府采购招标中，政府对投标企业的真实生产成本存在严重的信息不对称。贝叶斯博弈表明，若忽视企业的私人信息租金，设计出的固定总价合同必然引发效率低下或逆向选择危机。

## 边界条件与易错点

忘记策略必须针对每一个可能的类型 $\theta_i$ 都指派行动（哪怕某个类型概率极低）；混淆先验概率与观察到自身类型后的后验条件概率。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=-6A59LiKUss)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
海萨尼转换是博弈论史上最惊艳的天才神来之笔：面对“你不知道我知道什么、我不知道你知道我不知道什么”的不可知论无限认知深渊，海萨尼引入“自然”作为博弈第一步，将所有私人隐秘信息统一编码为外生随机给定的“类型”（Type），一举将哲学迷宫驯服为可以用概率测度严格求解的标准数学模型。
:::
