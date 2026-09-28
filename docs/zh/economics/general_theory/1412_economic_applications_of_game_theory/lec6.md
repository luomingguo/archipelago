---
title: 不完全竞争市场应用：古诺、伯川德与豪泰林模型
type: lecture
lecture: 6
tags: [cournot-competition, bertrand-paradox, hotelling-model, industrial-organization]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 6 不完全竞争市场应用：古诺、伯川德与豪泰林模型（Imperfect Competition）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 古诺（Cournot）模型：寡头企业同时选择产量，求解反应曲线交点确立市场价格与均衡产量。
- 伯川德（Bertrand）模型：同质产品价格竞争导致价格等于边际成本的“伯川德悖论”。
- 豪泰林（Hotelling）线性城市模型：引入产品空间差异化与消费者交通成本，成功化解价格战悖论。

## 核心概念与数学形式化

### 1. 古诺产量竞争模型（Cournot Oligopoly）
两家企业生产同质产品，边际成本均为 $c$。反需求函数为 $P(Q) = a - b(q_1 + q_2)$。
企业 1 利润函数：
$$\pi_1(q_1, q_2) = [a - b(q_1 + q_2) - c] q_1$$
一阶最优化条件：
$$\frac{\partial \pi_1}{\partial q_1} = a - c - 2b q_1 - b q_2 = 0 \implies q_1^*(q_2) = \frac{a - c - b q_2}{2b}$$
由于对称性，$q_1^* = q_2^* = \frac{a - c}{3b}$。总产出 $Q^* = \frac{2(a - c)}{3b}$，价格 $P^* = \frac{a + 2c}{3} > c$。

### 2. 伯川德价格竞争与悖论（Bertrand Paradox）
两家企业同时选择价格 $p_1, p_2$。需求完全流向价格更低者：
若同质产品且产能无限制，唯一纳什均衡为：
$$p_1^* = p_2^* = c, \quad \pi_1 = \pi_2 = 0$$
仅需两家企业即可完全复现完全竞争结果！

### 3. 豪泰林空间差异化模型（Hotelling Model）
消费者均匀分布在区间 $[0, 1]$，企业位于两端 $0$ 与 $1$。消费者购买产生交通成本 $t \cdot x^2$。
无差异临界消费者 $\hat{x}$ 满足：
$$p_1 + t \hat{x}^2 = p_2 + t(1 - \hat{x})^2$$
解出企业需求函数并求极值，得到均衡价格：
$$p_1^* = p_2^* = c + t$$
企业通过水平差异化获得了 $t$ 的正利润加成，成功逃脱伯川德残酷价格杀戮。

## 经济应用与机制分析

反垄断监管在评估企业并购时，必须区分行业竞争的本质属性：在产能受限的资本密集型重工业中更接近古诺模型，而在数字平台与标准化零售中极易陷入伯川德竞相降价或补贴大战。

## 边界条件与易错点

混淆产能调整周期（产量决策往往是中期、价格调整往往是短期）；忽视伯川德悖论对同质与无产能约束两个严苛假定的依赖。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=79Nqii6nQ5U)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
从古诺到伯川德，企业竞争变量的选取（产量 vs 价格）带来了天壤之别的结果。两家同质企业的价格战在瞬间就能摧毁所有超额利润；现代企业之所以能够维持高额毛利，核心就在于通过产品差异化和品牌区隔在认知空间中建立“豪泰林护城河”。
:::
