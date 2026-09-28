---
title: 理性化与信念驱动的选择
type: lecture
lecture: 4
tags: [rationalizability, best-response, common-knowledge-of-rationality, epistemic-game-theory]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 4 理性化与信念驱动的选择（Rationalizability）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 最佳反应（Best Response）映射定义：给定对对手策略的特定概率信念，使自身期望收益最大化的策略集合。
- 理性化（Rationalizability）要求不仅每个主体理性，且“所有主体皆理性”构成无穷阶共同知识。
- 证明在二人博弈中，理性化策略集合与 IESDS 剔除后保留的策略集合严格等价。

## 核心概念与数学形式化

### 最佳反应映射（Best Response）

设玩家 $i$ 对对手策略组合 $s_{-i}$ 持有主观概率信念 $\mu_i \in \Delta(S_{-i})$。
玩家 $i$ 的**最佳反应集合**定义为：
$$BR_i(\mu_i) = \arg\max_{s_i \in S_i} \sum_{s_{-i} \in S_{-i}} \mu_i(s_{-i}) u_i(s_i, s_{-i})$$

一个策略 $s_i$ 称为**从不为最佳反应（Never a Best Response）**，如果不存在任何合法的信念 $\mu_i \in \Delta(S_{-i})$，使得 $s_i \in BR_i(\mu_i)$。

### 理性化与共同知识定理
- **共同知识理性（Common Knowledge of Rationality, CKR）**：
  1. 玩家 $i$ 是理性的（选择对其某信念的最佳反应）；
  2. 玩家 $i$ 确信对手也是理性的；
  3. 玩家 $i$ 确信对手确信所有人都是理性的……以此类推至无限阶。
- **Pearce (1984) / Bernheim (1984) 定理**：
  在二人正规有限博弈中，一个策略是理性化的，当且仅当它能够在 IESDS 的无休止剔除中幸存下来：
  $$\text{Rationalizable}_i = S_i^\infty$$

## 经济应用与机制分析

在国际地缘政治或金融恐慌中，极端悲观的信念哪怕脱离基本面，只要在无限高阶信念中自洽，就能诱发破坏性的理性化挤兑行为。预期管理政策必须针对群体的共同信念结构进行强力干预。

## 边界条件与易错点

误以为一个策略如果对对手的任何单点纯策略都不是最佳反应，就必定从不为最佳反应（忽视了对手混合策略所张成的凸包信念空间）。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=ZdwIokL0P_U)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
理性化是认知博弈论（Epistemic Game Theory）的精髓：它不强求所有人预先形成完全一致的客观预期，只追问“如果我知道你理性，你知道我知道你理性……直到无限层，我究竟能理性地做出哪些选择？”这为非均衡状态下的策略思考提供了坚实的认识论防线。
:::
