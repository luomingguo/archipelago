---
title: 子博弈精炼纳什均衡（SPNE）与可信承诺
type: lecture
lecture: 10
tags: [subgame-perfection, spne, credible-threats, commitment-value]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 10 子博弈精炼纳什均衡（SPNE）与可信承诺（Subgame-Perfect Nash Equilibrium）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 普通纳什均衡容许包含非均衡路径上的不可信虚张声势威胁（Incredible Threats）。
- 引入泽尔滕（Selten）子博弈精炼纳什均衡（SPNE）：在博弈的每一个子博弈中都诱导一个纳什均衡。
- 分析进入阻碍博弈，阐明切断自身退路的承诺机制（Commitment）如何将劣势转化为决定性胜势。

## 核心概念与数学形式化

### 子博弈与精炼定义

- **子博弈（Subgame）** 的构成必须满足：
  1. 始于一个单节点信息集 $x$。
  2. 包含 $x$ 的所有后继节点。
  3. 不破坏博弈树中任何其他信息集（即若某信息集的一个节点在子博弈内，其所有节点必须都在子博弈内）。

- **子博弈精炼纳什均衡（Subgame-Perfect Nash Equilibrium, SPNE）**：
  策略剖面 $s^*$ 是一个 SPNE，如果它在原博弈的**每一个子博弈**中，都诱导出一个该子博弈的纳什均衡。

### 进入阻碍博弈（Entry Deterrence）
潜在挑战者 $E$ 决定是否进入（In / Out）。若进入，在位霸主 $I$ 决定迎头反击（Fight）还是容忍分享（Accommodate）：
- 收益矩阵：Out 对应 $(0, 2)$；进入后 Fight 对应 $(-1, -1)$，Accommodate 对应 $(1, 1)$。
- **纯策略纳什均衡有两个**：$(In, Accommodate)$ 与 $(Out, Fight)$。
- **SPNE 筛选**：在位者威胁“只要你敢进入我就打到底（Fight）”在进入后的子博弈中并不是纳什均衡（因为面对既成事实，选择 Accommodate 得 1 优于 Fight 的 -1）。因此 Fight 是不可信威胁，唯一 SPNE 是在位者妥协、挑战者进入 $(In, Accommodate)$！

## 经济应用与机制分析

中央银行的通胀目标制以及政府的“绝不与恐怖分子妥协”政策，核心逻辑均是建立制度性硬承诺。通过立法剥夺当政者的临时相机抉择裁量权，彻底消除市场对救市与妥协的预期，从而在根源上预防危机的发生。

## 边界条件与易错点

误以为只要博弈树没有子博弈就天然满足 SPNE（此时 SPNE 退化为普通 NE）；混淆嘴上宣传的意图与物理不可逆的承诺行动。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=byS0I3U3YoQ)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
“背水一战”与“破釜沉舟”不是盲目狂热，而是博弈论最高深的可信承诺实践。如果对手知道你在遭遇冲突时还有后撤的退路，你的反击威胁就是不可信的废纸；唯有通过可观察且不可撤销的自我捆绑（切断退路），才能逼迫对手在逆向归纳中主动选择退让。
:::
