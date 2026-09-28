---
title: 动态博弈与逆向归纳法
type: lecture
lecture: 8
tags: [extensive-form-games, backward-induction, zermelo-theorem, centipede-game]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 8 动态博弈与逆向归纳法（Backward Induction）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 完美信息有限博弈中，博弈树的每个决策节点均清楚知晓前序所有历史路径。
- 逆向归纳法（Backward Induction）从树的终端节点逐步向前推导每一阶段的最佳行动。
- 证明策梅洛定理（Zermelo's Theorem），探讨蜈蚣博弈（Centipede Game）中理论解与实验现象的悖论。

## 核心概念与数学形式化

### 完美信息有限博弈与策梅洛定理

一个动态博弈具有**完美信息（Perfect Information）**，如果博弈树上的每一个信息集都只包含唯一的决策节点（即不存在同时发生的隐蔽行动）。

- **策梅洛定理（Zermelo's Theorem, 1913）**：
  在任何有限步、无机会节点（无自然随机行动）的二人完备信息零和博弈中（如下棋），要么先行者必有必胜策略，要么后行者必有必胜策略，要么双方均有确保平局的策略。

### 逆向归纳法算法
1. 找到所有仅引出终端节点的前置决策节点（倒数第一阶段）。
2. 在该节点上，行动玩家必定选择使自身最终收益最大化的单步行动 $a^*$。
3. 将该节点的收益替换为选定行动 $a^*$ 所带来的收益向量。
4. 重复此向前折叠过程，直至抵达博弈树根节点。

### 蜈蚣博弈（Centipede Game）悖论
两名玩家交替选择继续（$C$）或结束（$E$）。继续使得总奖池翻倍，但对方先结束可拿走大头。
- **逆向归纳预测**：在第 $T$ 步，最后的玩家必定背叛拿走大头；前一位玩家预见到此在第 $T-1$ 步必定先下手背叛……倒推至第 1 步，第一名玩家在第一秒立刻选择结束，各自拿走微薄收入 $\$1$。
- **实验实证反差**：真实人类实验中，被试普遍能默契维持合作长达数十轮，大幅提升彼此收益。

## 经济应用与机制分析

在养老储蓄与代际财政契约制定中，如果每一代选民都按照逆向归纳法预期下一代会削减福利，代际互助体系就会瓦解。制度设计必须通过宪法级法律约束与长期声誉沉淀，打破逆向归纳诱发的合作瓦解链条。

## 边界条件与易错点

在存在不完美信息（信息集包含多个节点）的动态博弈中盲目套用逆向归纳法；忽视实验中人们对微小利他倾向的贝叶斯推断。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=VHex0a2JFWI)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
逆向归纳法的核心逻辑是“从未来倒推现在”：要想知道今天第一步该怎么走，必须先算清在博弈最后一刻理性人会怎么选。然而蜈蚣博弈揭示了完全理性的冰冷困境：如果双方对彼此理性具有无限阶确信，合作会在第一步就被掐死，完全错失了持续协作带来的百倍回报。
:::
