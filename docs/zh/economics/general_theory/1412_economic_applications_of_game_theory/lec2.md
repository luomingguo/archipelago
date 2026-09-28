---
title: 博弈的表述形式：标准式与扩展式
type: lecture
lecture: 2
tags: [game-representation, normal-form, extensive-form, information-sets]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 2 博弈的表述形式：标准式与扩展式（Representation of Games）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 标准式（战略式）博弈由玩家集、策略集与收益函数三要素严格定义：$G = (I, \{S_i\}, \{u_i\})$。
- 扩展式（博弈树）博弈细致刻画决策行动顺序、历史路径与信息集划分。
- 战略是完整的行动预案：必须为玩家每一个可能到达（甚至不可能到达）的信息集指定行动。

## 核心概念与数学形式化

### 标准式博弈（Normal Form Game）

一个标准式博弈定义为一个三元组 $G = \langle I, (S_i)_{i \in I}, (u_i)_{i \in I} \rangle$：
1. 局中人集合：$I = \{1, 2, \dots, n\}$。
2. 策略空间：对每一玩家 $i \in I$，$S_i$ 表示其所有可行策略的集合。所有玩家联合策略空间为 $S = S_1 \times S_2 \times \dots \times S_n$。
3. 收益函数：$u_i: S \to \mathbb{R}$，将联合策略剖面 $s = (s_1, \dots, s_n)$ 映射为玩家 $i$ 的实数效用回报。

### 扩展式博弈（Extensive Form Game）
扩展式博弈通过博弈树形式化呈现：
- 节点集合与偏序关系：包含根节点 $x_0$、决策节点 $X$ 和终端节点 $Z$。
- 玩家指派函数：$p: X \to I \cup \{c\}$，其中 $c$ 表示“自然”（Nature）行动节点。
- 信息集（Information Sets）划分 $h \in H_i$：若玩家在节点 $x$ 无法区分自己处于 $x$ 还是同集内的 $x'$，则 $x, x' \in h$。
- **纯策略定义**：玩家 $i$ 的纯策略 $s_i$ 是一个映射，为属于玩家 $i$ 的每一个信息集 $h \in H_i$ 指派一个可行行动 $a \in A(h)$。

## 经济应用与机制分析

制度设计实质上是构建博弈规则的博弈树结构。信息集的设计（如司法审判中的证据封闭、行政审批中的信息隔离）从根本上限定了各方利益主体的策略空间与寻租成本。

## 边界条件与易错点

在扩展式博弈中制定策略时，漏写非均衡路径节点的行动；混淆静态博弈与完美信息动态博弈的策略维度。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=JAib42oAiKE)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
许多初学者最容易犯的错误是混淆“行动”（Action）与“策略”（Strategy）。行动只是在某一特定时刻做出的瞬间举措，而策略是一份穷尽所有可能局面的完备军事作战预案。哪怕一个信息集在均衡路径上永远不会被触发，策略也必须严谨声明如果意外到达该如何行动。
:::
