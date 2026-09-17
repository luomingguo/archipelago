---
title: 简洁数据结构：Rank、Select 与 LOUDS 树表示
type: lecture
lecture: 17
tags: [succinct-data-structures, rank-select, louds, bit-vector, information-theory]
status: complete
---
# Lec 17 简洁数据结构：Rank、Select 与 LOUDS 树表示（Succinct Data Structures: Rank, Select, and LOUDS Tree Representation）

> 对应 MIT 6.851 Lecture 17 · 讲师：Erik Demaine · 核心文献：Jacobson (FOCS 1989), Clark (1996), Munro & Raman (SICOMP 2001)

## TL;DR

- 简洁数据结构（Succinct Data Structures）致力于在接近信息论最优下界 $\text{OPT} + o(\text{OPT})$ 比特空间内，支持快速查询操作（与耗费 $O(n w)$ 比特的普通指针结构形成鲜明对比）。
- 奠基石为位向量上的 $\text{Rank}$ 与 $\text{Select}$ 原语：Jacobson 提出利用大块（Superblock）、小块（Subblock）与四俄国人（Four Russians）常数查表，实现仅需额外 $o(n)$ 比特开销并在 $O(1)$ 时间内完成 $\text{Rank}$ 查询。
- 基于层序一元度数序列（LOUDS），静态二叉树可仅用 $2n + o(n)$ 比特紧凑编码，并借助 $\text{Rank}/\text{Select}$ 在 $O(1)$ 时间内完成父节点、左右孩子寻址及子树大小计算。

## 一、空间效率层次：从隐式、简洁到紧凑

在传统算法设计中，我们通常假设“线性空间”$O(n)$ 是可接受的。然而在现代海量数据（如基因组学、搜索引擎倒排索引、全网图谱）场景下，$O(n)$ 个机器字（Word）意味着 $O(n w)$ 个比特。对于 $w=64$，指针开销比真实信息量大了一到两个数量级。

设存储对象集合的信息论最优下界为 $\text{OPT} = \lceil \log_2 (\text{状态总数}) \rceil$ 比特。空间效率的追求可分为以下三类层次：

::: definition 空间敏感数据结构层次
1. **隐式数据结构（Implicit Data Structures）**：
   - 占用空间 $= \text{OPT} + O(1)$ 比特。
   - 几乎不能额外存储任何指针或辅助信息，只能利用数据元素的物理排列顺序来隐含结构。典型代表：二叉堆（Heap）、有序数组。
   - Franceschini 和 Grossi（2003）证明了存在隐式动态搜索树，在最坏情况下以 $O(\log n)$ 时间支持插入、删除和搜索。
2. **简洁数据结构（Succinct Data Structures）**：
   - 占用空间 $= \text{OPT} + o(\text{OPT})$ 比特。
   - 首项系数严格为 1，仅允许次线性阶的额外开销（$o(\text{OPT})$）。这是空间高效数据结构研究中最核心、最实用的范式。
3. **紧凑数据结构（Compact Data Structures）**：
   - 占用空间 $= O(\text{OPT})$ 比特。
   - 允许常数因子膨胀，但相较于传统指针结构仍节省了 $O(w)$ 的字长因子。
:::

## 二、位向量核心原语：Rank 与 Select

构建复杂简洁结构的基础是静态位向量（Bit Vector）。给定长度为 $n$ 的二进制数组 $B[0 \dots n-1]$，我们需要在 $O(1)$ 时间内支持两类核心操作：

::: definition Rank 与 Select 原语
- $\text{rank}_q(B, i)$：计算前缀子串 $B[0 \dots i]$ 中比特值 $q \in \{0, 1\}$ 出现的次数。
- $\text{select}_q(B, j)$：返回位向量 $B$ 中第 $j$ 次出现比特值 $q \in \{0, 1\}$ 的下标位置（1-indexed）。
:::

例如对于位向量：
$$
B = [0, 1, 1, 0, 1, 0, 0, 1]
$$
- $\text{rank}_1(B, 4) = 3$（前 5 个位置包含 3 个 1）。
- $\text{select}_1(B, 3) = 4$（第 3 个 1 位于下标 4）。
- 注意：由于 $\text{rank}_0(B, i) = (i + 1) - \text{rank}_1(B, i)$，因此只需实现 $\text{rank}_1$ 即可自动获得 $\text{rank}_0$。

## 三、Jacobson 的 Rank 结构：$O(1)$ 时间与 $n + o(n)$ 比特

Guy Jacobson 在 1989 年给出了支持 $O(1)$ 时间 $\text{Rank}$ 查询的优雅层次分解方案，其核心在于**大块、小块与四俄国人预计算查表**。

### 3.1 两级分块与计数存储

我们将长度为 $n$ 的位向量 $B$ 进行两级划分：

1. **第一级：大块（Superblocks）**
   - 将位向量切分为若干大小为 $S = \lfloor \frac{1}{2} \log^2 n \rfloor$ 的大块。
   - 大块数量为 $N_S = \lceil n / S \rceil = O(n / \log^2 n)$。
   - 对每个大块，存储从数组起始位置到该大块起点的 1 的累积总数。
   - 每个前缀和数值最大为 $n$，需要 $\lceil \log_2 n \rceil$ 比特存储。
   - 大块辅助表总空间：
   $$
   \frac{n}{\frac{1}{2} \log^2 n} \cdot \log n = O\left(\frac{n}{\log n}\right) = o(n) \text{ 比特}
   $$

2. **第二级：小块（Subblocks）**
   - 将每个大块进一步细分为若干大小为 $b = \lfloor \frac{1}{2} \log n \rfloor$ 的小块。
   - 小块数量为 $N_b = \lceil n / b \rceil = O(n / \log n)$。
   - 对每个小块，**仅存储该小块在其所属大块内部**的 1 的相对累积数。
   - 由于一个大块内最多有 $S = \frac{1}{2} \log^2 n$ 个元素，相对累积数的最大值为 $\frac{1}{2} \log^2 n$。
   - 因此每个小块计数只需 $\lceil \log_2 S \rceil = O(\log\log n)$ 比特！
   - 小块辅助表总空间：
   $$
   \frac{n}{\frac{1}{2} \log n} \cdot O(\log\log n) = O\left(n \frac{\log\log n}{\log n}\right) = o(n) \text{ 比特}
   $$

```text
 位向量 B:  [ 0 1 1 0 1 0 ... | 1 0 0 1 1 1 ... | ... ]
            ├─────────────────┤
            │  Superblock S   │ -> 绝对前缀和: O(log n) bits
            ├───┬───┬───┬─────┤
            │ b │ b │ b │  b  │ -> 块内相对和: O(log log n) bits
            └───┴───┴───┴─────┘
```

### 3.2 第三级：四俄国人全局查表（Four Russians Trick）

经过两级分块后，落在某个具体小块内的查询偏移量最多只有 $b = \frac{1}{2} \log n$ 位。我们无需再分配动态存储，而是使用一个**全局只读共享查找表（Lookup Table）**：
- 查找表的输入包含：长度为 $b$ 的任意可能二进制串，以及一个查询偏移下标 $k \in [0, b-1]$。
- 查找表输出：该长为 $b$ 的字串中前 $k$ 位的 1 的数量。
- 可能的二进制字串共有 $2^b = 2^{\frac{1}{2}\log n} = \sqrt{n}$ 种。
- 偏移下标有 $b = \frac{1}{2} \log n$ 种取值。
- 表项结果最大为 $b$，需 $\log b = O(\log\log n)$ 比特存储。
- 全局查找表总空间：
$$
2^b \cdot b \cdot \log b = \sqrt{n} \cdot \left(\frac{1}{2} \log n\right) \cdot O(\log\log n) = O(\sqrt{n} \log n \log\log n) = o(n) \text{ 比特}
$$

### 3.3 常数时间查询拼接

对于任意给定下标 $i$：
1. 定位其所在的大块索引 $I_S = \lfloor i / S \rfloor$ 和小块索引 $I_b = \lfloor i / b \rfloor$。
2. 计算小块内部的剩余偏移量 $r = i \bmod b$。
3. 从大块表中直接读出前缀和 $A[I_S]$（耗时 $O(1)$）。
4. 从小块表中直接读出相对和 $B_{\text{rel}}[I_b]$（耗时 $O(1)$）。
5. 从原位向量中切出对应的 $b$ 位小串，直接查表得到局部和 $Table[\text{bits}, r]$（耗时 $O(1)$）。
6. 最终结果：
$$
\text{rank}_1(i) = A[I_S] + B_{\text{rel}}[I_b] + Table\Big(B\big[I_b \cdot b \dots I_b \cdot b + b - 1\big], r\Big)
$$
三部分相加仅需 $O(1)$ 时间，且额外附加空间严格为 $o(n)$ 比特！

## 四、Clark 的 Select 算法

$\text{Select}$ 操作比 $\text{Rank}$ 更加复杂，因为 1 的分布可能极度不均匀（既可能紧密扎堆，也可能极其稀疏）。

Clark 于 1996 年提出了常数时间 $\text{Select}$ 方案：
1. 不按固定位置长度分块，而是**按 1 的出现次数分块**。每 $\log n \log\log n$ 个 1 划分为一个大块。
2. 根据大块在物理位向量中所跨越的长度 $L$ 进行分类：
   - 若 $L \ge (\log n \log\log n)^2$，说明 1 分布极度稀疏，但由于这样的大块总数极少，可以直接为每个 1 显式存储其实际绝对位置，总空间依然满足 $o(n)$。
   - 若 $L < (\log n \log\log n)^2$，说明 1 分布稠密，进一步使用更小阶数的二级分块与递归查表。
3. 同样达成 $O(1)$ 时间与 $n + o(n)$ 比特空间。

## 五、简洁二叉树表示：LOUDS 编码与常数时间导航

### 5.1 理论下界：卡特兰数

大小为 $n$ 个节点的有根有序二叉树数量由第 $n$ 个卡特兰数（Catalan Number）给出：
$$
C_n = \frac{1}{n+1} \binom{2n}{n} \approx \frac{4^n}{\sqrt{\pi} n^{1.5}}
$$
其信息论最优下界为：
$$
\log_2 C_n = 2n - \Theta(\log n) \text{ 比特}
$$
普通的指针表示法：每个节点需左右孩子指针及可能的数据指针，在 64 位系统下至少需要 $2 \times 64n = 128n$ 比特。而简洁数据结构的目标是以接近 **$2n$ 比特** 的空间存储整棵树，并支持全部树上导航操作。

### 5.2 LOUDS 树编码（Level-Order Unary Degree Sequence）

LOUDS 采用广度优先搜索（BFS，层序遍历）对树进行位编码：
- 为统一处理，在树根上方添加一个虚拟超级根节点（Super Root）。
- 按层序遍历每个节点。对于度数（孩子数量）为 $d$ 的节点，用一元编码（Unary Code）输出 $d$ 个 `1` 并以单个 `0` 结尾（即 $1^d 0$）。
- 对于一般的二叉字典树（Binary Trie），每个节点可有左孩子与右孩子：若左孩子存在输出 `1`，不存在输出 `0`；右孩子同理。

对于包含 $n$ 个节点的树，总共输出的 `1` 的数量等于总边数 $n-1$，输出的 `0` 的数量等于节点数 $n$。因此整棵树被编码为一个长度为 $2n + 1$ 比特的单一二进制位向量 $B$！

```text
        Node 1 (根)
        /        \
    Node 2      Node 3
      \
     Node 4

层序度数编码：
- SuperRoot: 10 (1个孩子)
- Node 1:   110 (2个孩子: Node 2, 3)
- Node 2:   010 (右孩子存在: Node 4)
- Node 3:   000 (无孩子)
- Node 4:   000 (无孩子)
拼接为纯位向量 B，配合 Rank / Select 索引
```

### 5.3 基于 Rank 与 Select 的常数时间树导航

在 LOUDS 编码向量 $B$ 中，每个节点由其在位向量中对应的第 $i$ 个 `1` 或 `0` 唯一定位。利用位向量上的 $\text{Rank}$ 与 $\text{Select}$ 原语，树的各种拓扑关系可以直接计算：

::: theorem LOUDS 导航公式
对于位于下标位置 $v$ 的节点：
- $\text{LeftChild}(v) = \text{select}_0(B, \text{rank}_1(B, v)) + 1$
- $\text{RightChild}(v) = \text{LeftChild}(v) + 1$
- $\text{Parent}(v) = \text{select}_1(B, \text{rank}_0(B, v))$
- $\text{IsLeaf}(v) = (B[\text{LeftChild}(v)] == 0)$
:::

所有上述运算均只包含常数次加减法与常数次 $\text{Rank}/\text{Select}$ 调用。因此：
- 节点父子导航时间严格为 $O(1)$；
- 存储总空间严格为 $2n + o(n)$ 比特！

## 六、我的理解

::: insight 简洁数据结构的本质是信息的去冗余与代数索引化
传统数据结构的“指针”本质上是一种粗暴的空间浪费：指针不仅存储了拓扑关系，还附带了物理内存随机分配的无关地址信息。
简洁数据结构揭示了一个深刻真理：**数据结构本身的拓扑形态是可以被算术化的**。
1. LOUDS 抛弃了指针，将二维树形结构展平成一维二进制流，直接逼近卡特兰数的信息论极限 $2n$ 比特。
2. 失去指针带来的寻址困难，被更底层的代数原语（$\text{Rank}/\text{Select}$）彻底化解。
3. Jacobson 的分块机制则展示了典型的“分治查表”哲学：大块吸收全局和、小块限制局部字长、微块查表消化末端常数。这种三层递进的思维模型，是理论计算机科学中兼顾极致空间与极致时间复杂度的最高典范。
:::
