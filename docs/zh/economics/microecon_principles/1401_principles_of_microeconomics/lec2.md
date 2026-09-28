---
title: 偏好与效用函数
type: lecture
lecture: 2
tags: [consumer-preferences, utility-function, indifference-curves, marginal-rate-of-substitution]
status: complete
source: 'https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/resources/mit14_01_f23_lec2/'
---

# Lec 2 偏好与效用函数

> MIT 14.01 Principles of Microeconomics · Lecture 2 · Jonathan Gruber

## TL;DR

- 偏好关系遵循完备性、传递性与非饱和性三大公理，保证消费者能够对任意消费束理性排序。
- 无差异曲线描绘带来相同效用的商品组合，其凸向原点的几何特征反映边际替代率（MRS）递减。
- 效用函数是序数性质的数学工具，其具体数值大小无绝对物理意义，仅反映偏好排名的相对高低。

> MIT 14.01 · Principles of Microeconomics · 主讲 Jonathan Gruber

## 消费者偏好

- 消费者的选择由**偏好（preferences）**和**预算约束（budget constraints）**共同决定。
- 为了对消费者偏好建模，需要三条假设：
  - **完备性（Completeness）**：比较任意两个商品组合（bundle）时，消费者要么偏好其中一个，要么偏好另一个，要么感到无差异（indifferent）。
  - **传递性（Transitivity）**：如果消费者偏好组合 $x$ 甚于组合 $y$，且偏好组合 $y$ 甚于组合 $z$，那么必然偏好组合 $x$ 甚于组合 $z$。
  - **非饱和性（Non-Satiation）**：一种商品越多总是越好，消费者永远不会被"喂饱"（满足）。

## 无差异曲线

- **无差异曲线（indifference curve）**是消费者理论的基本图形工具，它连接所有能给消费者带来相同效用水平的商品组合。无差异曲线有四条重要性质：
  - 消费者偏好更高（更靠外）的无差异曲线。
  - 无差异曲线是向下倾斜（downward-sloping）的。
  - 无差异曲线永远不会相交。
  - 每一个可能的消费组合都恰好对应一条无差异曲线。

## 效用

- **效用（utility）**是对偏好进行映射的一种方式。我们用效用得到的是**序数排序（ordinal ranking）**，而不是**基数排序（cardinal ranking）**——也就是说，效用数值本身的大小没有意义，重要的只是不同组合之间效用高低的相对顺序。
- **效用函数（utility function）**把消费者从不同消费组合中获得的效用转化为可以互相比较的单位（数值）。
- **边际效用（marginal utility）**是效用对某种商品求导数，衡量消费者多消费一单位该商品时效用如何变化。在常见模型中会假设边际效用递减；具体效用函数仍需单独检查。
- **边际替代率（marginal rate of substitution, MRS）**是无差异曲线斜率的绝对值：
  - 边际替代率（MRS）= 消费者愿意用纵轴（$Y$）商品交换横轴（$X$）商品的比率。
  - 其数学表达为：

$$
MRS = -\left.\frac{dY}{dX}\right|_{U\text{不变}} = \frac{MU_x}{MU_y} = \frac{\partial U/\partial x}{\partial U/\partial y}
$$

  - 无差异曲线的有符号斜率为 $-MRS$；MRS 本身是正的替换比率。
  - 沿着无差异曲线移动时，MRS 是递减的（即边际替代率递减）。

::: insight 序数效用的主观性升华
经济学放弃“基数效用”而转向“序数效用”，是现代社会科学最伟大的方法论革命之一。我们永远无法用仪器精确测量一个人吃冰淇淋产生的“快乐毫伏数”，但通过观察他在无差异曲线上的边际取舍（MRS），就能精确预测他在面对价格变动时的全部宏观行为。
:::

## 复习要点

- 会用图形证明无差异曲线永不相交。
- 会用图形证明无差异曲线向下倾斜。
- 能画出对应"完全互补品"（perfect complements）和"完全替代品"（perfect substitutes）情形的无差异曲线。
- 给定对消费者偏好的文字描述，能据此画出对应的无差异曲线草图。
- 给定效用函数，能计算边际效用。
- 给定效用函数，能计算边际替代率（MRS）。


## 参考资料与延伸阅读

- [MIT OCW 14.01 官方课程资源主页](https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/)
- Gruber, Jonathan. *Public Finance and Public Policy*. Worth Publishers.
- Varian, Hal R. *Intermediate Microeconomics: A Modern Approach*. W. W. Norton & Company.
