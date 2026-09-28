---
title: '高级基数估计与概率概要算法'
type: lecture
lecture: 21
tags: [cardinality-estimation, hyperloglog, count-min-sketch, histogram-statistics]
status: complete
source: 'https://dsg.csail.mit.edu/6.5830/'
---

# Lec 21 高级基数估计与概率概要算法（Advanced Cardinality Estimation and Sketches）

> MIT 6.5830 / 6.5831 · Database Systems · 第 21 讲  
> 核心教材：*Readings in Database Systems* (5th Edition, Red Book)  
> 配套实验：GoDB (Go-based Database Engine)

## TL;DR

- 基数估计（Cardinality Estimation）是查询优化器选择最佳连接顺序与物理算子的核心生命线。
- 单列与多列数据分布统计依赖等宽直方图、等深直方图（Equi-depth）及前缀重度采样。
- 概率概要算法（HyperLogLog 估计去重基数、Count-Min Sketch 统计频次、Bloom Filter 判定成员）以极小内存逼近精确结果。

## 架构演进与核心洞察

::: insight 概率数据结构对内存与精度的优雅折中
当面对万亿级数据流时，如果要求 100% 精确的 `COUNT(DISTINCT user_id)`，必须建立巨大的哈希表或排序，内存开销高达数十 GB。而 HyperLogLog 利用伯努利试验中随机哈希值前导零个数的概率分布，仅需 1.5KB 内存即可将十亿级基数的误差控制在 1% 以内。现代大数据与实时 OLAP 系统的基石正是建立在对这种“容忍受控误差”的数学妥协之上。
:::

## 核心机制与讲义正文

## 一、回顾查询优化中的位置

回顾查询优化器的整体结构：包括

- 重写规则（*Rewrite Rules*）、
- 计划枚举（*Plan Enumeration*）、
- 基数估计器（*Cardinality Estimator*），其中
  - 基数估计对连接顺序（*Join Ordering*）
  - 算子选择（*Operator Selection*）至关重要——可以说是其中最具挑战性的问题
- 成本模型（*Cost Model*）。

![image-20260613174603423](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20260613174603423.png)

### 为什么基数估计如此重要？

下面给出一个三表连接查询的例子：

```sql
SELECT * FROM nation n, customer c, supplier s
WHERE n.nationkey = c.nationkey
AND s.nationkey = c.nationkey
AND n.name = 'GERMANY'
```

不同的连接顺序会带来截然不同的中间结果规模。

如左图所示， 先把 `nation`（经过 `name='GERMANY'` 过滤后只剩很少的记录）与 `customer` 连接，再与 `supplier` 连接，中间结果可能很小

![image-20260613175249043](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20260613175249043.png)

但如果由右图所示，先把 `customer` 与 `supplier` 连接（两者都是大表），中间结果可能会膨胀到上千万级别，再与 `nation` 连接。

要回答"哪种连接顺序更优？"、"应该选择哪种连接算法？"、"应该选择索引扫描还是顺序扫描？"这些问题，都离不开准确的基数估计与成本信息。

### 为什么基数估计如此有挑战性？

- **单列过滤**：非常容易——只需要知道该列的取值分布
- **多列过滤**：更难，因为不同列之间可能存在相关性（*Correlation*）
- **多表连接**：难度大幅增加——因为数据的分布和列之间的相关性，在连接之后会发生改变

![image-20260613175705538](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20260613175705538.png)

## 二、概率数据结构与核心概要算法（Sketches）

在大规模海量数据流分析中，精确统计不仅耗时巨大，而且会消耗不可接受的内存。现代查询优化与实时 OLAP 广泛采用概率数据结构进行快速近似估算：

### 1. 直方图技术（Histograms）
- **等宽直方图（Equi-width）**：将数据值域切分为固定宽度的桶，各桶内频次可能极度不均，在数据倾斜时估算失真。
- **等深直方图（Equi-depth）**：每个桶容纳相同数量的元组，动态调整区间边界，极大提升了对偏斜分布的预测精度。

### 2. HyperLogLog (HLL)——去重基数估计
- **核心思想**：通过均匀哈希函数将输入映射为二进制串，利用哈希值前缀连续出现 0 的最大长度（$k$）作为几何分布估计：$N pprox 2^k$。
- **分桶调和平均**：将前 $m$ 位划分为 $2^m$ 个桶，各桶独立观测并计算调和平均数，消除极端值波动，以仅 1.5KB 内存实现 $1\%$ 误差率。

### 3. Count-Min Sketch——高频项与频次估计
- **核心思想**：由深度为 $d$、宽度为 $w$ 的二维计数器矩阵与 $d$ 个独立哈希函数构成。
- **查询规则**：对于查询键 $x$，取各哈希槽计数的最小值：$\hat{f}(x) = \min_{1 \le i \le d} C[i, h_i(x)]$。天然满足保守估计（只可能多估，绝不低估）。

### 4. 布隆过滤器（Bloom Filter）——集合成员高效判定
- **核心机制**：通过 $k$ 个哈希函数映射到位图数组。若任一位为 0 则**绝对不存在**；若全为 1 则**大概率存在**（存在可控假阳性 False Positive，无假阴性）。常用于下推至存储层过滤无效磁盘读。
