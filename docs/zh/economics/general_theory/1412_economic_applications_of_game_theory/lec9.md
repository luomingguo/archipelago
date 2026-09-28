---
title: 讨价还价理论：纳什与鲁宾斯坦模型
type: lecture
lecture: 9
tags: [bargaining-theory, nash-bargaining, rubinstein-bargaining, patience-advantage]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 9 讨价还价理论：纳什与鲁宾斯坦模型（Negotiation）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 公理化纳什讨价还价解（Nash Bargaining Solution）：最大化双方超越违约断点收益的纳什积。
- 鲁宾斯坦（Rubinstein）轮流出价动态模型：无限期贴现环境下，耐受力较强者获得更大剩余。
- 证明当出价摩擦周期趋近于零时，非合作动态讨价还价的唯一均衡严格收敛于公理化纳什解。

## 核心概念与数学形式化

### 1. 公理化纳什讨价还价解（Axiomatic Nash Bargaining）
可行效用集 $X \subset \mathbb{R}^2$ 为紧凸集，分歧断点（Disagreement Point）为 $d = (d_1, d_2) \in X$。
纳什四公理（帕累托最优、仿射变换不变性、无关备选方案独立性 IIA、对称性）唯一定理化解：
$$x^* = \arg\max_{(x_1, x_2) \in X, x \ge d} (x_1 - d_1)(x_2 - d_2)$$

### 2. 鲁宾斯坦轮流出价模型（Rubinstein, 1982）
两名玩家瓜分大小为 1 的馅饼。玩家 1 与 2 的每期贴现因子分别为 $\delta_1, \delta_2 \in (0, 1)$。
- 奇数期 $t=1, 3, \dots$ 玩家 1 出价方案 $(x, 1-x)$，玩家 2 决定接受（博弈结束）或拒绝（进入下期）。
- 偶数期 $t=2, 4, \dots$ 玩家 2 出价方案 $(1-y, y)$，玩家 1 决定接受或拒绝。

利用平稳子博弈精炼均衡求解：
$$x^* = 1 - \delta_2 y^*, \quad y^* = 1 - \delta_1 x^*$$
联立解得玩家 1 在第一轮提出的唯一均衡份额：
$$x^* = \frac{1 - \delta_2}{1 - \delta_1 \delta_2}, \quad 1 - x^* = \frac{\delta_2(1 - \delta_1)}{1 - \delta_1 \delta_2}$$
- **推论**：博弈在第 1 轮被立即达成（无延迟帕累托有效）。若 $\delta_1 = \delta_2 = \delta$，则 $x^* = \frac{1}{1 + \delta} > \frac{1}{2}$（先动先得优势）；当出价间隔时间间隔 $\Delta \to 0$ 时，$\delta \to 1$，$x^* \to 1/2$。

## 经济应用与机制分析

劳资谈判或跨国贸易争端中，弱势方之所以屡屡妥协，根源在于资金链或供应链承受不起旷日持久的消耗停工（$\delta$ 极低）。设立谈判紧急救助缓冲基金，是均等化谈判力量、避免掠夺性协议的关键公共手段。

## 边界条件与易错点

混淆威胁破裂的内部断点收益（Disagreement payoff）与随时可带走走人的外部退出收益（Outside option）。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=_09ziyzbinY)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
谈判桌上的权力来自哪里？鲁宾斯坦模型给出了振聋发聩的答案：谈判筹码本质上是对“时间的耐心”。谁对拖延惩罚更具韧性（贴现因子 $\delta$ 更大）、谁的外部备选退出方案（Outside Option）更优越，谁就能在无情的动态较量中斩获压倒性份额。
:::
