---
title: 记忆化与动态规划算法
type: lecture
lecture: 18
tags: [dynamic-programming, memoization, overlapping-subproblems, optimal-substructure, knapsack]
status: complete
source: https://introcomp.mit.edu/fall26
---

# Lec 18 记忆化与动态规划算法（Dynamic Programming）

> MIT 6.100 · 计算机科学与 Python 编程导论 · Fall 2026 · 教材参考：Guttag 14.1, 15

## TL;DR

- **动态规划两要素**：问题必须具备最优子结构（子问题的最优解能合成全局最优解）与重叠子问题（不同分支包含大量完全相同的子计算状态）。
- **记忆化递归（Memoization）**：在自顶向下的递归树中引入哈希查找表（Memo Table），每个状态仅在首次遭遇时计算一次并缓存，后续直接 $O(1)$ 读取，消除指数级冗余。
- **伪多项式复杂度（Pseudo-polynomial）**：动态规划将 0/1 背包的时间复杂度从 $O(2^N)$ 彻底压缩至 $O(N \cdot W)$，在实际工程算力承受范围内完美降维。

## 1. 动态规划的两大理论基石

动态规划（Dynamic Programming, DP）由理查德·贝尔曼（Richard Bellman）在 20 世纪 50 年代提出。初学者常常被这个富有神秘色彩的名字所迷惑，实际上它的核心哲学异常纯粹：**绝不重复计算相同的问题两次**。

一个最优化问题能够使用动态规划高效求解，必须严格满足两大结构特征：

::: definition 最优子结构（Optimal Substructure）
全局问题的全局最优解，必然是由其各个局部的子问题的最优解推导组合而成的。
:::

::: definition 重叠子问题（Overlapping Subproblems）
在求解大问题的过程中，递归搜索树的不同分支会反复重访完全相同的子状态参数空间。子状态的实际数量远远少于递归树的节点总数。
:::

以斐波那契数列为例：$F(n) = F(n-1) + F(n-2)$。在朴素递归树中，$F(n-2)$ 被计算了两次，$F(n-3)$ 被计算了三次，随着深度增加，冗余计算呈斐波那契数级几何爆炸！

---

## 2. 记忆化搜索（Memoization）：自顶向下的优雅升华

解决重叠子问题最自然直接的方法是**记忆化（Memoization）**。

在传统的自顶向下递归架构中，程序每遇到一个新的子问题，都会盲目地重新展开深层子树进行完整演算。而记忆化技术在进入实际递归递推之前，首先在堆内存中开辟一个全局持久的哈希字典 `memo` 作为计算快照缓存表。这个缓存表就像是一个答题记录本，字典的键（Key）是能够唯一精确标识当前子状态特征的不可变参数元组，字典的值（Value）则是该子状态计算出的最优解结构。

整个记忆化递归函数在执行时，严格遵循四步流水线操作：
1. **查表拦截（Cache Lookup）**：函数一旦被调用，第一条语句必须首先检查当前输入的参数元组是否已经存在于 `memo` 字典之中。如果是，说明在此前某一平行分支中已经彻底解决过这个一模一样的子问题，程序直接以 $O(1)$ 常数时间返回缓存结果，瞬间斩断整棵深达数十层的子调用树；
2. **基准情形验证（Base Cases）**：若未命中缓存，照常判定递归边界条件（如物品已耗尽或背包剩余容量归零）；
3. **状态转移计算（State Transition）**：执行标准的递归分解推演，分别获取包含与不包含当前物品的最佳子解，并做极值决策；
4. **存表沉淀（Cache Storage）**：在通过 `return` 语句将结果回传给上一层调用方之前，必须将本次刚刚耗费算力推导出的新鲜解结构，完整存入 `memo` 字典对应槽位中。

### 0/1 背包问题的记忆化实现

在 0/1 背包问题中，决定一个子问题未来命运的全部上下文，并不依赖于“我们此前具体挑选了哪些特定物品”，而仅仅由两个数值唯一决定：`(当前待考察物品索引 index, 当前背包剩余可用承重 avail_weight)`。

只要这两个数值相同，无论此前是经过何种曲折复杂的路径到达这一状态，其后续可能产生的最大新增价值都必然完全恒定。因此，我们将 `(index, avail_weight)` 作为哈希表复合键。在函数签名设计上，类型注解清晰标明了输入输出契约：参数接收物品清单、当前考察偏移量、当前可用承重以及记忆字典本身；返回值则是一个两元组，第一项为最大价值整数，第二项为具体选中的物品不可变元组。

在具体的工程实现中，我们必须特别注意递归基准条件与记忆字典生命周期的设计细节：
- **状态键的轻量性**：避免将大尺寸的可变对象（如整个子列表）作为键，仅使用两个轻量整型标量构造元组，确保哈希计算与查找在数纳秒内完成；
- **自顶向下展开与回溯保存**：当首次计算某一特定状态时，算法递归深入并等待子调用返回，一旦获取当前最优组合，立即向 `memo` 写入该结果，实现算力的永久沉淀：

```python
from typing import Dict, List, Tuple

class Item:
    def __init__(self, name: str, value: int, weight: int):
        self.name = name
        self.value = value
        self.weight = weight

MemoKey = Tuple[int, int]
MemoTable = Dict[MemoKey, Tuple[int, Tuple[Item, ...]]]

def fast_knapsack_memo(
    items: List[Item],
    index: int,
    avail_weight: int,
    memo: MemoTable
) -> Tuple[int, Tuple[Item, ...]]:
    """
    记忆化动态规划求解 0/1 背包问题
    """
    state_key = (index, avail_weight)
    
    # 步骤 1：查表检查缓存
    if state_key in memo:
        return memo[state_key]
        
    # 步骤 2：基准情形
    if index == len(items) or avail_weight == 0:
        return 0, ()
        
    next_item = items[index]
    
    # 步骤 3：可行性判断与递归状态转移
    if next_item.weight > avail_weight:
        result = fast_knapsack_memo(items, index + 1, avail_weight, memo)
    else:
        # 分支 A：选
        val_with, taken_with = fast_knapsack_memo(
            items, index + 1, avail_weight - next_item.weight, memo
        )
        val_with += next_item.value
        
        # 分支 B：不选
        val_without, taken_without = fast_knapsack_memo(
            items, index + 1, avail_weight, memo
        )
        
        if val_with > val_without:
            result = (val_with, taken_with + (next_item,))
        else:
            result = (val_without, taken_without)
            
    # 步骤 4：存表并返回
    memo[state_key] = result
    return result
```

让我们通过一个微型追踪演算来理解记忆化的神效：假设在探索物品 0 的“选择”分支后，背包剩余承重为 15，并继续深入考察了物品 1 至 3；而在物品 0 的“放弃”分支中，通过其他物品的某种组合消耗，背包剩余承重碰巧再次下降为 15，且恰好轮到考察物品 4。在朴素递归中，以 `(index=4, avail_weight=15)` 为根的整棵决策子树将被完整无误地重新算上一遍；而在记忆化版本中，该子问题在第一次被解决并存入 `memo` 后，第二次进入时在 `if state_key in memo:` 处直接毫秒级返回，完美避开了数以万计的下游子节点计算。

此外，在空间管理方面，记忆化字典的大小与调用栈深度的乘积依然维持在线性或伪多项式级别。调用栈的深度严格等于候选物品的总件数 $N$，因此即使面对上千件物品，栈空间开销也仅为数千层局部帧，绝不会产生由于搜索树过宽导致的内存溢出。

通过这一层轻量级的字典拦截，搜索树中数百万个原本重叠的冗余节点被整齐折叠，递归树直接收敛为一张有向无环状态转移网。这种自顶向下带备忘录的编程风格，保留了递归推导的直观数学美感，同时赋予了程序与自底向上循环表格完全同等的高性能保证。

---

## 3. 复杂度降维：从 $O(2^N)$ 到 $O(N \cdot W)$

让我们从状态空间的维度量化这一算法飞跃：
- 待考察物品索引 `index` 的可能取值有 $N + 1$ 种（$0, 1, \dots, N$）；
- 假设背包容量 $W$ 为整数，`avail_weight` 的可能取值有 $W + 1$ 种（$0, 1, \dots, W$）；
- 因此，整个宇宙中存在的**不同状态总数上限**仅有 $(N + 1) \times (W + 1)$ 种！

因为每一个可能的状态在执行过程中都仅被实际计算一次并写入哈希表，其余全部调用均以 $O(1)$ 常数时间命中返回。故记忆化动态规划的总时间复杂度严格受限于：
$$O(N \cdot W)$$

当 $N = 100, W = 1000$ 时，$2^{100} \approx 1.26 \times 10^{30}$（整个宇宙恒星总数级别的算力需求），而 $N \cdot W = 10^5$（个人笔记本电脑仅需几毫秒即可瞬间算完）！

::: pitfall 伪多项式时间（Pseudo-Polynomial Time）的理论边界
$O(N \cdot W)$ 在算法形式上看似是乘积多项式，但计算机科学将其严谨归类为**伪多项式时间**。因为参数 $W$ 的编码长度仅为 $\log_2(W)$ 比特。如果输入一个极大的数字 $W = 10^{18}$，输入比特长度仅增加 60 位，但计算步数却暴涨为不可承受之重。动态规划的高效性建立在“承重数值 $W$ 处于工程合理范围内”的实际假设之上。
:::

## 我的理解

::: insight 空间换时间的终极体现
动态规划深刻揭示了计算世界中的资源转化定律：算力不足时，可以通过消耗少量内存（哈希表缓存）来抵扣天量的重复推演。通过识别出系统的本质状态参数（`index` 与 `weight`），原本看似无穷蔓延的指数级未知丛林，被规整映射为一个紧凑有限的状态网格。这是每一个高级工程师必须刻入骨髓的核心思维。
:::
