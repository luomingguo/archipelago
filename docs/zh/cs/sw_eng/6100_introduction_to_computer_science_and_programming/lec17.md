---
title: 状态空间剪枝与经典背包问题
type: lecture
lecture: 17
tags: [knapsack, pruning, branch-and-bound, state-space-search, recursion]
status: complete
source: https://introcomp.mit.edu/fall26
---

# Lec 17 状态空间剪枝与经典背包问题（Pruning & Knapsack Problem）

> MIT 6.100 · 计算机科学与 Python 编程导论 · Fall 2026 · 官方讲义核心内容

## TL;DR

- **递归 0/1 决策树实现**：将背包决策映射为递归函数：若当前物品重量超过剩余容量，强制进入“不选”分支；否则分别求解“选”与“不选”两个子问题并取价值较大者。
- **状态空间剪枝（Pruning）**：可行性剪枝（超重提前终止）与最优性剪枝（剩余物品理论最大价值上界不足以超越已知最优时提前回溯），大幅压缩实际搜索节点数。
- **指数复杂度的深层根源**：即使引入激进剪枝，在最坏输入情形下，算法依然需要遍历近乎满二叉树的组合规模，时间复杂度维持在 $O(2^N)$。

## 1. 递归求解 0/1 背包基线模型

在 Lec 16 建立的决策树模型指导下，我们可以将背包最优化问题直观翻译为递归算法。

递归算法的优美之处在于它把宏观上看似极其复杂的组合优化全局难题，层层剥离分解为每一个微观节点的二元决策。对于物品列表中的第 $i$ 件物品（索引从 0 开始），设当前背包剩余可用容量为 $w$。算法的执行推演严格遵循三项逻辑分支：

1. **基准情形（Base Cases）**：
   - 若候选物品已经全部考察完毕（`len(to_consider) == 0`），意味着决策树已达最深叶子节点，后续无法再产出任何收益；
   - 若剩余容量耗尽（`avail_weight == 0`），意味着背包物理空间已饱和，无法再装入任何正重量物品。在这两种情形下，能获得的新增价值必然为 0。
2. **容量超限分支**：
   - 若当前待考量的物品自身重量大于背包剩余可用承重（`next_item.weight > avail_weight`），该物品根本无法装入。算法在此处别无选择，只能直接递归进入“放弃该物品”的右子树分支，剩余承重保持不变。
3. **最优性抉择分支**：
   - 若当前物品自身重量未超限，算法面临双向探索抉择：
     - **方案 A（选）**：获得当前物品价值，剩余容量扣减其重量，递归求解剩余物品；
     - **方案 B（不选）**：当前物品弃之不用，容量不变，递归求解剩余物品；
     - 最终解通过比较取二者价值的较大者：$\max(\text{Val}_A + v_i, \; \text{Val}_B)$。

```python
class Item:
    def __init__(self, name: str, value: int, weight: int):
        self.name = name
        self.value = value
        self.weight = weight

def knapsack_recursive(to_consider: list, avail_weight: int) -> tuple:
    """
    基础递归 0/1 背包求解器，返回 (最大总价值, 选中的物品元组)
    """
    # 基准情形：无剩余物品或无剩余重量
    if len(to_consider) == 0 or avail_weight == 0:
        return 0, ()
        
    next_item = to_consider[0]
    
    # 可行性剪枝：若当前物品超重，强制不选
    if next_item.weight > avail_weight:
        return knapsack_recursive(to_consider[1:], avail_weight)
        
    # 分支 1：探索包含当前物品的左子树
    val_with, taken_with = knapsack_recursive(
        to_consider[1:], avail_weight - next_item.weight
    )
    val_with += next_item.value
    
    # 分支 2：探索不包含当前物品的右子树
    val_without, taken_without = knapsack_recursive(
        to_consider[1:], avail_weight
    )
    
    # 择优选取
    if val_with > val_without:
        return val_with, taken_with + (next_item,)
    else:
        return val_without, taken_without
```

这段基线实现完全保真地再现了 0/1 决策树的数学定义。尽管其逻辑无懈可击且绝对保证能命中全局最优解，但其在无剪枝干预时的运行时间严格取决于树的叶子数量，随着物品数量 $N$ 的增长而急剧呈现 $O(2^N)$ 的指数级膨胀。

---

## 2. 状态空间树的剪枝策略（Pruning）

朴素递归的时间复杂度是严格的 $O(2^N)$。为了在不牺牲解的精确性的前提下提升运行效率，必须在搜索树展开的过程中执行**状态空间剪枝（Pruning）**。

### 1. 可行性剪枝（Feasibility Pruning）
一旦某次决策导致累积重量超过背包容量限制（$avail\_weight < 0$），该节点之下的整棵子树直接被判定为非法解域，无需进一步展开。上述代码中的 `if next_item.weight > avail_weight` 便属于典型的可行性剪枝。

### 2. 上界最优性剪枝（Bounding Pruning）
在探索右子树（放弃当前物品）之前，我们可以先计算一个**乐观估计上界（Optimistic Upper Bound）**：假设后续剩余的所有物品不仅全部装入，甚至允许按分数背包方式贪心切碎填满剩余空间。

若该乐观估计能达到的理论极限总价值，依然小于我们在左子树或其他分支中已经实实在在找到的某个完整可行解的真实价值，那么探索该分支就是毫无价值的徒劳之举。此时算法可安全将整个子树切除回溯。

```text
                     决策节点 i
                   /            \
        [探索分支 A]            [分支 B 乐观上界评估]
     已获最佳价值: 280          理论剩余最大可能: 240
                                240 < 280 -> 触发剪枝! 直接回溯
```

---

## 3. 为什么剪枝依然无法攻克指数级难关

尽管激进的分支限界剪枝能够大幅提升算法在平均场景下的解题速度，但在最坏输入配置下（例如所有物品重量均极小且价值相近），剪枝条件可能一次都不会被触发，算法依旧退化为遍历整棵庞大的 $2^N$ 决策树。

在计算复杂性理论中，0/1 背包问题属于著名的 **NP-完全（NP-Complete）** 问题体系。这意味着在目前的计算机科学认知中，不存在能在多项式时间 $O(N^k)$ 内求解任意 0/1 背包实例的算法。

然而仔细审视递归决策树的节点，我们会发现一个惊人的秘密：**在不同的递归调用路径中，大量具有完全相同“剩余物品序列”与“剩余背包容量”的子问题，被反复重复求解了成千上万次！**

这种子问题重叠的结构缺陷，正是下一讲动态规划将要彻底攻克的突破口。

::: pitfall 列表切片 `to_consider[1:]` 带来的隐性拷贝开销
在递归函数中使用 `to_consider[1:]` 会在每一层调用中产生新的列表浅拷贝，引入 $O(N)$ 的额外时间和内存分配开销。在高性能工程实现中，应当改用不可变整型下标 `index` 追踪当前物品指针 `knapsack_fast(items, index, avail_weight)`。
:::

## 我的理解

::: insight 剪枝是排除法的高阶艺术
搜索算法的优劣，不仅取决于它“找到了什么”，更取决于它“聪明地忽略了什么”。剪枝的本质是利用数学不等式在搜索空间中建立防火墙。它告诉我们：面对庞大未知的搜索领域，只要能够严密证明某个方向绝无可能诞生更优解，不看就是最大的智慧与效率。
:::
