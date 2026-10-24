---
title: '割平面法 I：Gomory 分数割与对偶单纯形热启动 (Cutting Planes I: Gomory Cuts)'
type: lecture
lecture: 17
tags: [cutting-planes, gomory-fractional-cuts, dual-simplex, warm-start]
status: complete
---

# Lec 17 割平面法 I：Gomory 分数割与对偶单纯形热启动 (Cutting Planes I: Gomory Cuts)

> MIT 15.083 / 6.859J 整数规划与组合优化 · 讲义 17 · 授课教师：Prof. Dimitris Bertsimas

## TL;DR

- Gomory 分数割从当前连续松弛最优单纯形表的非整基行中纯代数提炼。
- 割平面在严密保留原问题所有整数解的前提下，一刀切除当前松弛分数解。
- 结合对偶单纯形法（Dual Simplex），割平面加入后系统实现 1~2 步热启动（Warm Start）秒级恢复。

## 1. 割平面的代数提炼：从单纯形表到整值约束

在第 16 讲中，我们学习了 Chvátal-Gomory 闭包的宏观几何理论。然而，在实际运行工业求解器时，我们不可能盲目猜测乘子向量 $u$。
拉尔夫·戈莫里（Ralph Gomory）在 1958 年提出了举世闻名的**Gomory 分数割（Gomory Fractional Cut）**算法：
**直接从当前连续松弛的最优单纯形表（Optimal Simplex Tableau）中，就地取材提炼出杀伤力最强的割平面！**

设求解松弛 LP 终止，得到最优基矩阵 $B$。
若当前基本可行解存在非整数分量，任选一个非整数基变量行（设基变量为 $x_{B(i)}$）：
$$x_{B(i)} + \sum_{j \in N} \bar{a}_{ij} x_j = \bar{b}_i$$
其中 $\bar{b}_i \notin \mathbb{Z}$ 是一个非整数，$\bar{a}_{ij} = (B^{-1} A)_{ij}$ 是当前单纯形表中的技术系数。

将实数拆分为向下取整的整数部分与非负纯小数部分（记 $f_0 = \bar{b}_i - \lfloor \bar{b}_i \rfloor \in (0, 1)$，以及 $f_j = \bar{a}_{ij} - \lfloor \bar{a}_{ij} \rfloor \in [0, 1)$）：
$$x_{B(i)} + \sum_{j \in N} (\lfloor \bar{a}_{ij} \rfloor + f_j) x_j = \lfloor \bar{b}_i \rfloor + f_0$$
移项重新编排：
$$\sum_{j \in N} f_j x_j - f_0 = \lfloor \bar{b}_i \rfloor - x_{B(i)} - \sum_{j \in N} \lfloor \bar{a}_{ij} \rfloor x_j$$

```mermaid
flowchart TD
    subgraph GomoryDualityLoop [Gomory 割与对偶单纯形热启动闭环]
        direction TB
        LPOpt[当前连续松弛 LP 最优: 发现基变量 x_B(i) = 3.7 为非整数] --> Generate[提取代数小数部分: sum f_j * x_j >= f_0]
        Generate --> Inject[注入新约束: 引入松弛变量 s = -f_0 + sum f_j x_j >= 0]
        Inject --> WarmStart[当前解违规 s = -f_0 < 0: 对偶可行性依然完好保留!]
        WarmStart --> DualPivot[对偶单纯形法执行 1~2 步主元消元: 秒级热启动恢复新的更优下界]
    end
```

## 2. 整数刚性与当前解斩首定理

仔细审视上述等式两端在任意合法整数解 $x \in \mathbb{Z}^n$ 处的代数特性：
- **等式右边**：$\lfloor \bar{b}_i \rfloor$ 是整数，$x_{B(i)}$ 是整数，$\sum \lfloor \bar{a}_{ij} \rfloor x_j$ 全是整数乘加！因此：**等式右边必须是一个严格的纯整数**！
- **等式左边**：由于右边是整数，左边 $\sum_{j \in N} f_j x_j - f_0$ 也必须是整数。
  因为决策变量 $x_j \ge 0$ 且小数部分 $f_j \ge 0$，而 $f_0 \in (0, 1)$ 是一个严格小于 1 的正小数；
  如果左边想要等于一个整数，它绝对不能是负整数（因为若小于等于 $-1$，意味着 $\sum f_j x_j \le -1 + f_0 < 0$，与非负性直接矛盾！）。
  因此：左边必须大于等于 0！

由此，直接导出**Gomory 分数割平面**：
$$\sum_{j \in N} f_j x_j \ge f_0$$

::: theorem Gomory 割平面的绝对有效性与分离性
1. **绝不剔除任何合法整数解**：对于原问题中的任意可行整数解，该不等式严格恒成立；
2. **当场斩首当前连续松弛极点**：考察当前的连续松弛最优解，由于所有非基变量全为零（$x_N^* = 0$），代入割平面左边为：
$$\sum_{j \in N} f_j \cdot 0 = 0$$
而右端项 $f_0 > 0$ 是一个严格正数！不等式变为 $0 \ge f_0$，发生绝对代数矛盾！
**当前的分数最优解，被这一条割平面以不可辩驳的代数力量当场斩杀剔除！**
:::

## 3. 对偶单纯形法的秒级热启动（Warm Start）

引入非负松弛变量 $s \ge 0$，将割平面写入单纯形表底部：
$$-s + \sum_{j \in N} f_j x_j = f_0 \iff s - \sum_{j \in N} f_j x_j = -f_0$$

此时单纯形表的右端项出现了一个负数：$s = -f_0 < 0$！
如果使用原单纯形法，原可行性被破坏，必须重新从两阶段法从头开始算起；
但是，我们在第 15.081J 第 11 讲学到的**对偶单纯形法（Dual Simplex Method）在此展现出神威**：
添加这条割平面，目标函数行里的检验数向量 $\bar{c} \ge 0$ 完全没有受到任何影响！**对偶可行性完好无损！**

求解器只需将新加入的松弛变量行作为出基变量，执行对偶最小比值测试，通常**仅需 1 到 2 步对偶高斯消元，就能在几微秒内直接热启动恢复出新的、下界显著抬升的连续最优解！**

::: insight 割平面法是代码中的纯逻辑手术
Gomory 割平面的推导展现了应用数学最惊艳的逻辑美感。
它不需要你懂得图论，不需要你分析具体的业务背景。它就像一套纯粹的通用代数过滤器，只要你在单纯形表中看到了小数（$f_0 > 0$），这套代数机械臂就会自动将这个小数的余数转化为一道锋利的割刀。
现代工业级整数求解器在根节点往往一口气切出数千条 Gomory 割，在分支定界树尚未展开之前，就已经将连续松弛多面体削去了大半虚胖。
:::
