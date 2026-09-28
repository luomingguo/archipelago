---
title: 共同知识与博弈论认识论前沿
type: lecture
lecture: 25
tags: [common-knowledge, aumann-structure, agreeing-to-disagree, epistemic-foundations]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 25 共同知识与博弈论认识论前沿（Common Knowledge）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 区分“互相知道”（Mutual Knowledge）与无穷层级的“共同知识”（Common Knowledge）。
- 运用奥曼（Aumann）信息分割结构严密定义共同知识，阐明经典的红眼睛/蓝眼睛悖论。
- 证明奥曼共识定理（Agreeing to Disagree）：具有共同先验的贝叶斯理性人，其后验共识绝不可能互相产生分歧。

## 核心概念与数学形式化

### 奥曼信息结构与共同知识定义（Aumann, 1976）

设可能世界状态空间为 $\Omega$。玩家 $i$ 的信息结构表现为 $\Omega$ 的一个分割（Partition）$\mathcal{P}_i$。
当真实状态为 $\omega$ 时，玩家 $i$ 仅知道真实状态落在集合 $P_i(\omega) \in \mathcal{P}_i$ 中。

- **知道算子（Knowledge Operator）**：
  事件 $E \subset \Omega$。玩家 $i$ 知道事件 $E$ 发生，记为 $K_i(E) = \{\omega \in \Omega \mid P_i(\omega) \subseteq E\}$。
- **相互知识（Mutual Knowledge）**：
  所有人都知道事件 $E$：$K(E) = \bigcap_{i \in I} K_i(E)$。
- **共同知识（Common Knowledge）**：
  所有人知道、且所有人知道所有人都知道……以此类推至无穷阶：
  $$CK(E) = K(E) \cap K(K(E)) \cap K^3(E) \cap \dots = \bigcap_{m=1}^\infty K^m(E)$$
  - **几何刻画**：事件 $E$ 是共同知识，当且仅当包含当前状态的 $\mathcal{P}_1, \dots, \mathcal{P}_n$ 的**最小共同粗分割（Meet）**完全包含于 $E$。

### 奥曼共识定理（Agreeing to Disagree）
设玩家 1 与 2 拥有共同先验概率分布 $p \in \Delta(\Omega)$。
若两名玩家对某一事件 $A$ 的后验概率估计值分别为 $q_1 = p(A \mid P_1(\omega))$ 与 $q_2 = p(A \mid P_2(\omega))$，且这一对后验估计值在状态 $\omega$ 处是**共同知识**，则：
$$q_1 = q_2$$
贝叶斯理性人绝不可能“在理性共识上互相承认彼此存在观点分歧”！金融市场中纯粹基于投机信息的疯狂交易之所以不可能成立（无交易定理 No-Trade Theorem），根源亦在于此。

## 经济应用与机制分析

金融市场监管中的突发降息或官方声明，其核心价值不仅是传递事实，更是向全市场确立“共同知识”。只有当所有市场主体确信其他所有交易对手都确信政策转向时，流动性预期的正反馈飞轮才能被瞬间激活。

## 边界条件与易错点

混淆高阶相互知识与真正的无限阶共同知识（Rubinstein 电子邮件博弈证明，哪怕达到 99 阶相互知识，行为也与 1 阶知识时完全无异，无法实现任何协调合作）。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=YHAY9UY9MgE)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
博弈论最深邃的哲学归宿是认知认识论。我们日常以为的“大家都知道”，往往只是脆弱的第一层相互知道。红眼睛悖论惊人地证明：哪怕村长宣布了一句全场每一个人亲眼看见、早已心知肚明的显而易见大实话，只要这句话被当众公开喊出，它就把信息从有限层级轰击跃迁为无限阶的“共同知识”，瞬间引爆震撼世界的连锁反应。
:::
