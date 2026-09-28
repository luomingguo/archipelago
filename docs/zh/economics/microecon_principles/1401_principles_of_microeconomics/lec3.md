---
title: 预算约束与约束选择
type: lecture
lecture: 3
tags: [budget-constraint, constrained-optimization, consumer-optimum, corner-solution]
status: complete
source: 'https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/resources/mit14_01_f23_lec3/'
---

# Lec 3 预算约束与约束选择

> MIT 14.01 Principles of Microeconomics · Lecture 3 · Jonathan Gruber

## TL;DR

- 预算线 $P_x X + P_y Y \le I$ 界定了消费者在既定收入与市场价格下的客观可行选择集。
- 内点最优消费组合发生在无差异曲线与预算线的相切点，满足主观边际替代率等于客观价格比。
- 对于完全互补品或完全替代品，最优解常位于预算约束边界的角点，相切条件可能不再适用。

> MIT 14.01 · Principles of Microeconomics · 主讲 Jonathan Gruber

## 预算约束

- 消费者的资源是有限的，这被称为**预算约束（budget constraint）**。一个简化假设是：预算等于收入（income, $I$）。
- 对两种商品 $X$ 和 $Y$，预算约束定义为：

$$
I = p_X X + p_Y Y
$$

- 预算线的**有符号斜率**为：

$$
\frac{dY}{dX} = -\frac{p_X}{p_Y}
$$

  直观理解：在预算固定的情况下，多选择购买一种商品，就必然意味着减少了可以花在其他商品上的钱。

- 价格和收入的变动会改变预算约束的**位置**和**斜率**。
  - 例如，如果横轴商品 $X$ 的价格上升，预算线绕纵轴截距向内旋转，变得更陡。
  - 如果收入下降，预算约束会向内平移（shift inwards）。

## 约束优化

- 约束选择（constrained choice）的目标是在预算约束下最大化效用（utility）。消费者的偏好由无差异曲线（indifference curve）表示。
- 消费者能够选择的最优消费组合，出现在无差异曲线与预算约束相切（tangent）的那一点：

$$
MRS = \frac{MU_X}{MU_Y} = \frac{\partial U/\partial X}{\partial U/\partial Y} = \frac{p_X}{p_Y}
$$

  在这一点上，两条曲线的有符号斜率同为 $-p_X/p_Y$。如果最优选择在边界，需比较角点，不能直接套用相切条件。

- 上述等式给出的是**内点解（interior solution）**（消费者对两种商品都有正的消费量）；如果无差异曲线比较平坦（flat），也可能出现**角点解（corner solution）**，即消费者只消费其中一种商品。

::: insight 主观欲望与客观现实的完美切点
$MRS = P_x / P_y$ 是整个微观经济学最富哲学韵味的方程：等式左边是纯粹主观的内心渴望（你愿意放弃多少 Y 来换取一单位 X），等式右边则是冷酷无情的市场现实（市场强制要求你放弃多少 Y 才能买到一单位 X）。当主观偏好的切线与客观预算的坚壁在此相吻，个体的福祉便在约束之下达成了极限。
:::

## 复习要点

- 会根据价格和收入写出预算约束。
- 能用图形方法展示如何在预算约束下找到使消费者效用最大化的消费组合。
- 给定效用函数、两种商品的价格和收入，能用代数方法求解最优消费组合，并注意检查是否存在角点解。


## 参考资料与延伸阅读

- [MIT OCW 14.01 官方课程资源主页](https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/)
- Gruber, Jonathan. *Public Finance and Public Policy*. Worth Publishers.
- Varian, Hal R. *Intermediate Microeconomics: A Modern Approach*. W. W. Norton & Company.
