---
title: 贝叶斯纳什均衡的经济应用
type: lecture
lecture: 17
tags: [bayesian-nash-equilibrium, asymmetric-information, cournot-bayesian, public-goods]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 17 贝叶斯纳什均衡的经济应用（Bayesian Nash Equilibrium: Applications）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 求解成本非对称信息下的双寡头古诺竞争模型，解析私人成本对竞争对手产出的战略性影响。
- 分析阿克洛夫柠檬市场博弈中的逆向选择与市场崩溃机制。
- 探讨具有私人偏好的公共品自愿提供博弈，刻画搭便车倾向与信息租金的权衡。

## 核心概念与数学形式化

### 非对称信息古诺模型（Cournot with Incomplete Information）

企业 1 成本已知为 $c$。企业 2 成本为私人信息：
- 可能是低成本 $c_L$，概率为 $\theta$；
- 可能是高成本 $c_H$，概率为 $1 - \theta$。
反需求函数为 $P = A - (q_1 + q_2)$。

**求解步骤**：
1. **企业 2 的决策**：
   企业 2 确切知道自身类型 $c_k \in \{c_L, c_H\}$，求解：
   $$\max_{q_2(c_k)} [A - q_1 - q_2(c_k) - c_k] q_2(c_k) \implies q_2^*(c_k) = \frac{A - q_1 - c_k}{2}$$
2. **企业 1 的决策**：
   企业 1 面对企业 2 的策略，其期望对手产量为 $\mathbb{E}[q_2] = \theta q_2^*(c_L) + (1-\theta)q_2^*(c_H)$：
   $$\max_{q_1} [A - q_1 - \mathbb{E}[q_2] - c] q_1 \implies q_1^* = \frac{A - \mathbb{E}[q_2] - c}{2}$$
3. **联立求解**：
   将 $q_2^*(c_L)$ 与 $q_2^*(c_H)$ 代入 $\mathbb{E}[q_2]$，解出显式解析均衡，得到企业 1 的产量与企业 2 两种类型的最佳产量剖面。

## 经济应用与机制分析

非对称信息是市场失灵的重要根源。在二手车、二手房交易以及个人信贷领域，建立权威第三方的独立质量认证或征信公示机制，是打消买方柠檬疑虑、促成有效市场出清的制度前提。

## 边界条件与易错点

在写出企业 1 的期望收益时，误把期望符号放在产量二次项的外侧导致错误平方；忽略企业 2 真实成本类型的分离决策。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=9_jcdMsPomQ)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
在私人信息的世界里，“我知道什么”直接决定了“我猜你会怎么猜我”。在非对称古诺竞争中，即使低成本企业生产能力很强，它的最优产量也必须克制：因为它知道对手无法确切辨别自己的底细，对手的高产量猜测会反过来压缩自己的市场生存空间。
:::
