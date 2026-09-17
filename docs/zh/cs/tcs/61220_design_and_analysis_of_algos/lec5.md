---
title: 均摊分析：势能法与并查集
type: lecture
lecture: 5
tags: [amortized-analysis, potential-method, union-find, dynamic-tables]
status: complete
---

# Lec 5 均摊分析：势能法与并查集（Amortized Analysis: Potential Method & Union-Find）

## TL;DR

- **均摊分析三大方法**：聚合分析求总体平均，记账法通过虚拟信用实现削峰填谷，势能法将数据结构内部状态映射为实数势能 $\Phi(D)$，为最坏单步沉重代价提供精细数学上界。
- **势能有效性准则**：均摊代价定义为 $\hat{c}_i = c_i + \Phi(D_i) - \Phi(D_{i-1})$，只要势能满足全局非负（$\Phi(D_n) \ge \Phi(D_0)$），均摊代价之和即为真实总代价的严格上界。
- **动态扩容与计数器**：通过为动态数组定义 $\Phi = 2 \cdot \mathrm{size} - \mathrm{capacity}$，以均摊代价 3 完美平摊指数扩容的 $O(n)$ 内存搬迁峰值。
- **并查集与反阿克曼复杂度**：联合应用按秩合并与路径压缩两大启发式优化，单次查找在扁平化森林中不断释放势能，使 $m$ 次操作的总体时间锁定在 $O(m \alpha(n))$，均摊单次几乎恒为常数。

---

## 均摊分析三大方法：聚合、记账与势能

在很多高效数据结构中，某些单步操作可能极为昂贵（例如动态数组翻倍扩容、并查集长链路径压缩），但昂贵操作的发生必然伴随着大量极其廉价的基础操作。**均摊分析（Amortized Analysis）** 的核心目的，是在一系列操作的总体序列上评估平均性能，保证任何长度为 $m$ 的操作序列的最坏总时间受控。

均摊分析与概率分析有根本不同：**均摊分析不依赖任何关于输入的概率假设，它是确定性的最坏情况保证**。

### 1. 聚合分析（Aggregate Analysis）

直接计算由 $n$ 个操作构成的任意操作序列的总时间 $T(n)$，然后求平均：
$$
\text{每个操作的均摊代价 } = \frac{T(n)}{n}
$$
例如：栈支持 `PUSH`、`POP` 以及一次弹出 $k$ 个元素的 `MULTIPOP`。虽然单次 `MULTIPOP` 最坏耗时 $O(n)$，但由于每个元素至多被入栈一次，因此在包含 $n$ 次操作的序列中，所有 `POP` 与 `MULTIPOP` 弹出的元素总数不超过 $n$。总耗时为 $O(n)$，均摊单次代价为 $O(1)$。

### 2. 记账法（Accounting Method）

为每种操作指定一个虚拟的**均摊代价（Amortized Cost）** $\hat{c}_i$：
- 若实际代价 $c_i < \hat{c}_i$，将多余的差额 $\hat{c}_i - c_i$ 作为**信用（Credit）**存入数据结构中的特定对象；
- 若实际代价 $c_i > \hat{c}_i$，则消耗先前积攒的信用补足真实开销。

::: definition
**记账法的有效性充要条件**
在任何时刻 $t$，系统内累积的信用总额必须非负：
$$
\sum_{i=1}^t \hat{c}_i - \sum_{i=1}^t c_i \ge 0 \quad (\forall t \ge 1)
$$
只要信用永不透支，均摊代价的总和 $\sum \hat{c}_i$ 必然构成真实代价总和 $\sum c_i$ 的严格上界。
:::

### 3. 势能法（Potential Method）

势能法是记账法的连续数学形式化。将数据结构在第 $i$ 次操作后的状态记为 $D_i$，初始状态为 $D_0$。定义一个**势函数（Potential Function）** $\Phi: D \to \mathbb{R}$，将数据结构状态映射为一个实数势能。

::: definition
**势能法的均摊代价**
第 $i$ 次操作的均摊代价 $\hat{c}_i$ 定义为实际代价加上势能变化量：
$$
\hat{c}_i = c_i + \Phi(D_i) - \Phi(D_{i-1})
$$
:::

对 $n$ 个操作求和：
$$
\sum_{i=1}^n \hat{c}_i = \sum_{i=1}^n \big( c_i + \Phi(D_i) - \Phi(D_{i-1}) \big) = \sum_{i=1}^n c_i + \Phi(D_n) - \Phi(D_0)
$$
整理得到真实总代价：
$$
\sum_{i=1}^n c_i = \sum_{i=1}^n \hat{c}_i + \Phi(D_0) - \Phi(D_n)
$$
只要我们设计的势函数满足对所有可能的终止状态都有 $\Phi(D_n) \ge \Phi(D_0)$（通常设定 $\Phi(D_0) = 0$ 且 $\Phi(D_i) \ge 0$），那么：
$$
\sum_{i=1}^n c_i \le \sum_{i=1}^n \hat{c}_i
$$
均摊代价的总和就是真实总代价的有效上界。设计势函数的核心目标是：**在数据结构走向昂贵操作的过程中不断蓄积势能（$\Delta \Phi > 0$），在昂贵操作发生时瞬间释放势能（$\Delta \Phi \ll 0$）以抵消巨大的实际代价 $c_i$**。

---

## 经典范例：动态表与二进制计数器

### 动态数组（Dynamic Table）翻倍扩容

动态数组在容量不足时触发重新分配，将容量翻倍并将旧元素全量拷贝。
- 设插入前数组已有 $size$ 个元素，总容量为 $capacity$；
- 若 $size < capacity$：直接插入，实际代价 $c_i = 1$；
- 若 $size = capacity$：分配 $2 \cdot capacity$ 空间，拷贝 $size$ 个元素并插入新元素，实际代价 $c_i = size + 1$。

#### 势函数构造

定义势函数：
$$
\Phi(T) = 2 \cdot size - capacity
$$
- 初始状态：$size = 0, capacity = 0 \implies \Phi(D_0) = 0$；
- 扩容刚完成时刻：$size = m, capacity = 2m \implies \Phi = 2m - 2m = 0$；
- 表即将被填满时刻：$size = m, capacity = m \implies \Phi = 2m - m = m$（积攒了恰好等于元素数量的势能！）；
- 由于表使用率始终 $\ge 1/2$，故 $\Phi(D_i) \ge 0 = \Phi(D_0)$ 恒成立。

#### 均摊代价计算

1. **未触发扩容时**（$size_i = size_{i-1} + 1, capacity_i = capacity_{i-1}$）：
   $$
   \hat{c}_i = 1 + \big( (2(size+1) - capacity) - (2size - capacity) \big) = 1 + 2 = 3
   $$
2. **触发扩容时**（$size_{i-1} = capacity_{i-1} = m, size_i = m+1, capacity_i = 2m$）：
   $$
   c_i = m + 1
   $$
   $$
   \Delta \Phi = \Phi(D_i) - \Phi(D_{i-1}) = \big( 2(m+1) - 2m \big) - \big( 2m - m \big) = 2 - m
   $$
   $$
   \hat{c}_i = c_i + \Delta \Phi = (m + 1) + (2 - m) = 3
   $$
无论是否触发扩容，每次插入操作的均摊代价恒为常数 3。因此 $n$ 次插入的实际总耗时严格处于 $O(n)$ 范围之内。

---

## 并查集（Disjoint Set Union）及其均摊复杂度分析

并查集维护由互不相交的动态集合构成的族，支持以下基本操作：
- `Make-Set(x)`：创建包含单个元素 $x$ 的独立集合；
- `Find-Set(x)`：返回包含 $x$ 的集合的代表元（根节点）；
- `Union(x, y)`：将包含 $x$ 与 $y$ 的两个集合合并为一个集合。

### 核心启发式优化

1. **按秩合并（Union by Rank）**：
   每个节点维护一个“秩”（Rank），近似表示子树高度。在合并两棵树时，始终将秩较小的根节点挂载到秩较大的根节点下方。若两根秩相同，任选其一作为新根并将新根的秩加 1。
   ::: theorem
   包含 $k$ 个节点的树其根节点的秩至多为 $\lfloor \log_2 k \rfloor$。因此任意节点的秩不超过 $\lfloor \log_2 n \rfloor$。
   :::
2. **路径压缩（Path Compression）**：
   在执行 `Find-Set(x)` 时，沿着从 $x$ 到根节点的查找路径遍历，将沿途访问到的所有节点直接重定向指向树根。

```python
def find_set(x):
    if x != x.parent:
        x.parent = find_set(x.parent)  # 递归扁平化
    return x.parent

def union(x, y):
    root_x, root_y = find_set(x), find_set(y)
    if root_x == root_y:
        return
    if root_x.rank < root_y.rank:
        root_x.parent = root_y
    elif root_x.rank > root_y.rank:
        root_y.parent = root_x
    else:
        root_y.parent = root_x
        root_x.rank += 1
```

### 阿克曼函数与反阿克曼函数

为了刻画并查集的极致复杂度，定义急剧爆炸式增长的阿克曼函数（Ackermann Function）：
$$
A_0(x) = x + 1, \quad A_{k}(0) = A_{k-1}(1), \quad A_k(x) = A_{k-1}(A_k(x-1))
$$
其中 $A_1(x) = 2x + 3$，$A_2(x) \approx 2^x$，$A_3(x) \approx 2^{2^{\cdots 2}}$（高度为 $x$ 的幂塔），$A_4(1) = A_3(2) = 2^{2^{65536}}$（远超已知宇宙原子总数）。

::: definition
**反阿克曼函数 $\alpha(n)$**
$$
\alpha(n) = \min \{ k \mid A_k(1) \ge n \}
$$
对于现实宇宙中能够表示的任何输入规模（直至 $n = 10^{80}$ 甚至宇宙原子级别），$\alpha(n) \le 4$。
:::

### 均摊界定理与势能刻画

::: theorem
**Tarjan 并查集均摊复杂度定理**
在一个包含 $n$ 个元素的并查集上执行 $m$ 次操作（其中包含 $n$ 次 `Make-Set`，且 $m \ge n$），采用按秩合并与路径压缩时，序列总运行时间为：
$$
T(m, n) = O(m \cdot \alpha(n))
$$
单次操作的均摊时间复杂度为 $O(\alpha(n))$。
:::

**证明机制直觉**：
我们为每个节点依据其秩 $rank(x)$ 与其父节点的秩 $rank(parent(x))$ 在阿克曼函数分层区间中的位置赋予势能。
- 每次 `Find-Set` 沿树向上攀爬时，如果某个节点的父节点秩跨越了层级，该步实际开销由单次操作支付（至多 $\alpha(n)$ 步跨层）；
- 如果父节点与子节点在同一层级内，路径压缩操作会使子节点的父指针跳过更长距离，直接提升父节点的秩，从而使该节点在当前层级内的相对势能严格下降；
- 释放出来的势能恰好抵消了该节点重定向指针的单步实际代价。因此，即使一次 `Find-Set` 穿越了极深的长链，其高昂的遍历代价也被先前未压缩状态积累的势能完全平摊。

---

## 我的理解

::: insight
均摊分析彻底颠覆了“单步最坏情况即系统瓶颈”的机械思维：
1. **时间守恒与势能蓄水池**：势能法揭示了计算过程中的某种守恒律。那些令人胆颤的“单步深重操作”，从来不是凭空掉下来的灾难，而是一批廉价操作长期偷懒累积的必然结果。势函数就是为数据结构设立的“债务与信用账本”，通过在日常低谷期强制储蓄，保证任何时候面对巨峰都能从容化解。
2. **两大约束的协同放大**：并查集的奇迹来自于“按秩合并”与“路径压缩”的绝妙共振。单靠按秩合并只能保证深度为对数阶；单靠路径压缩无法防范构造极度倾斜的退化树。按秩合并为树的节点秩建立了坚固的分层天花板，路径压缩则如同重力坍缩，在每一次查找中不可逆地将树的高度打平。
3. **渐近理论的物理尽头**：反阿克曼函数 $\alpha(n)$ 是理论计算机科学中最接近常数但又并非严格常数的优雅奇观。它向我们展示：在绝对严谨的数学形式下，只要系统允许历史操作对结构状态进行自适应重塑，计算效率可以逼近物理世界的逻辑极限。
:::
