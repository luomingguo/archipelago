---
title: 现代并行算法与计算模型
type: lecture
lecture: 2
tags: [parallel-algorithms, work-span-model, prefix-sum, greedy-scheduling, brents-theorem]
status: complete
---

# Lec 2 现代并行算法与计算模型（Parallel Algorithms: Work-Span Model & Prefix Sums）

## TL;DR

- **Work-Span 计算模型**：将多线程计算抽象为计算 DAG，定义总工作量 $T_1$（单核串行总操作数）与关键路径跨度 $T_\infty$（无限核下的最长因果依赖路径）。
- **布伦特贪心调度定理（Brent's Theorem）**：任意贪心调度器在 $P$ 个处理器上的执行时间严格满足 $T_P \le T_1/P + T_\infty$，揭示了并行算法可扩展性的两大致命边界。
- **并行高效性（Work-Efficiency）与前缀和（Scan）**：设计并行算法的首要原则是保证 $T_1 = O(T_{\text{seq}})$；基于平衡树上行（Reduce）与下行（Down-sweep）构造的前缀和算法以 $O(n)$ 工作量与 $O(\log n)$ 跨度成为并行图与数据处理的核心积木。

## 计算 DAG 与 Work-Span 模型

在设计多核并行算法时，传统的 PRAM（Parallel Random Access Machine）模型因假设处理器之间具备无成本的步调一致锁步（Lock-step）同步而脱离了真实机器现实。现代并行算法理论采用更为通用且真实的**动态多线程 DAG 模型（Dynamic Multithreading DAG Model）**。

在动态多线程模型中，算法执行过程被形式化为一个有向无环图 $G = (V, E)$：
- 节点 $v \in V$ 代表一段无需内部同步的连续串行计算指令序列（通常称为一个 Strand）。
- 有向边 $(u, v) \in E$ 代表指令之间的控制因果依赖关系，例如线程衍生（Spawn）、返回（Join）或普通的串行后继。

```text
               ( u )  Strand u 生成并行任务
              /     \
    ( spawn )/       \( sequential )
            v         v
          ( v1 )     ( v2 )
            \         /
             \( join )/
              v     v
               ( w )  Strand w 必须等待两者同步结束
```

::: definition Work-Span 核心指标
- **总工作量（Work, $T_1$）**：算法在单核处理器上执行全部计算节点所耗费的绝对总指令数或时间，等于 DAG 中所有节点的计算时间之和。
- **跨度（Span / Critical Path Length, $T_\infty$）**：算法在假设拥有无限多个物理处理器的理想机器上执行所需的时间，等于 DAG 中从起点到终点权重最大路径的长度。
- **理论并行度（Parallelism）**：比值 $\mathcal{P} = T_1 / T_\infty$，代表该算法在不发生算力闲置的前提下能够有效利用的最大理论处理器数量。
:::

## 贪心调度与布伦特定理

一个优秀的并行算法必须能够在拥有任意 $P$ 个物理核心的机器上高效运行。调度器负责在运行时动态将就绪的 Strand 映射到空闲物理核心上。

::: theorem 布伦特定理 / 贪心调度定理（Brent's Theorem）
设任意贪心调度器（Greedy Scheduler，即只要存在就绪任务且存在空闲处理器，处理器就绝不摸鱼）在 $P$ 个处理器上调度一个总工作量为 $T_1$、跨度为 $T_\infty$ 的计算 DAG，则其总执行时间 $T_P$ 严格满足：
$$
T_P \le \frac{T_1 - T_\infty}{P} + T_\infty < \frac{T_1}{P} + T_\infty
$$
:::

**定理证明思路**：
我们将调度器的执行过程按时钟步进行切分。在每一步中，系统分为两类状态：
1. **完全步骤（Complete Step）**：系统中就绪的 Strand 数量 $\ge P$。此时所有 $P$ 个处理器均满载运行，消耗了 $P$ 个单位的工作量。这类步骤的总数至多为 $\lfloor(T_1 - T_\infty)/P\rfloor$。
2. **不完全步骤（Incomplete Step）**：系统中就绪的 Strand 数量 $< P$。由于调度器是贪心的，所有就绪的 Strand 均被调度执行。这意味着关键路径上的至少一个前驱依赖节点被消耗，导致 DAG 剩余的最大跨度严格减少 1。因此，不完全步骤的总数严格受限于 $T_\infty$。

将两类步骤的时间累加，即得到 $T_P \le (T_1 - T_\infty)/P + T_\infty$。

布伦特定理揭示了多核算法扩展的两大刚性规律：
- 当 $P \ll T_1 / T_\infty$ 时，$T_1/P$ 项占主导，算法表现出近乎完美的**线性加速比（Linear Speedup）**：$T_P \approx T_1/P$。
- 当 $P \gg T_1 / T_\infty$ 时，$T_\infty$ 项成为无法逾越的下限，增加更多核心对减少运行时间毫无助益。

## 并行高效性（Work-Efficiency）

::: definition 并行高效性（Work-Efficiency）
如果一个并行算法的总工作量 $T_1(n)$ 在渐近意义上与该问题已知的最优串行算法 $T_{\text{seq}}(n)$ 完全相同，即 $T_1(n) = O(T_{\text{seq}}(n))$，则称该算法是**并行高效的（Work-Efficient）**。
:::

::: pitfall 忽视 Work-Efficiency 的设计陷阱
设计并行算法时，初学者往往为了极度压缩跨度 $T_\infty$ 而设计出工作量剧增的算法。例如，使用 $O(n^2)$ 个处理器在 $O(1)$ 跨度内通过全两两比较寻找数组最大值。尽管跨度极小，但其总工作量由串行的 $O(n)$ 暴增为 $O(n^2)$。在核心数 $P$ 有限的现实机器上，由于 $T_P \ge T_1/P$，当 $P$ 固定时，该算法的实际运行时间反而比普通的串行扫描慢数百倍！**并行设计的第一铁律是必须首先保持 Work-Efficient**。
:::

## 并行前缀和（Parallel Prefix Sum / Scan）

前缀和是并行计算中最为基础且强大的原语。给定输入数组 $A = [a_0, a_1, \dots, a_{n-1}]$ 与结合律二元算子 $\oplus$，输出数组 $Y$ 满足 $y_i = a_0 \oplus a_1 \oplus \dots \oplus a_i$。

串行计算前缀和只需简单循环累加，工作量为 $O(n)$，但其数据依赖导致跨度为 $\Theta(n)$。Blelloch 提出了著名的基于平衡二叉树的两阶段并行前缀和算法，同时达成 $O(n)$ 工作量与 $O(\log n)$ 跨度。

### 阶段一：上行规约树（Up-Sweep / Reduce）

在第一阶段中，算法模拟一颗完全平衡的自底向上规约树。输入数组的全部 $n$ 个叶子节点按两两一组配对，父节点通过并行调用加法算子记录两个子节点的和。该过程递归推进，直到计算出覆盖全数组的总和并保存在根节点中。其树形结构如下图所示：

```text
Level 3:                    [ 36 ] (root)
                          /        \
Level 2:          [ 10 ]              [ 26 ]
                 /      \            /      \
Level 1:      [ 3 ]    [ 7 ]      [ 11 ]   [ 15 ]
             /    \   /    \     /     \  /     \
Level 0:    1      2 3      4   5       6 7      8
```

每向上一层，活跃的并行任务数量减半，树的高度严格等于 $\lceil\log_2 n\rceil$。由于每一层的规约加法可以在各个节点之间完全无竞争地并行触发，整个上行阶段的关键路径跨度仅为树高 $O(\log n)$。与此同时，全部内部节点执行的加法操作总数为：
$$
\frac{n}{2} + \frac{n}{4} + \dots + 1 = n - 1 = O(n)
$$
这保证了上行阶段消耗的总算力与单核串行累加在同一渐近阶数内。

### 阶段二：下行传播树（Down-Sweep）

根节点初始化为单位元 $0$。从根节点自顶向下将当前节点的前驱累加值传递给左子节点，同时将左子节点的原始和累加给右子节点：

```python
def down_sweep(node, value_from_left):
    if node.is_leaf():
        node.output = value_from_left + node.val
        return
    # 左子树继承来自父节点左侧的累加值
    down_sweep(node.left, value_from_left)
    # 右子树继承（来自父节点左侧的累加值 + 左子树的总和）
    down_sweep(node.right, value_from_left + node.left.sum)
```

两阶段均包含 $O(n)$ 次操作与 $O(\log n)$ 层树深遍历，因此整个并行 Scan 算法达成了严格的 Work-Efficient：$T_1(n) = O(n)$，跨度 $T_\infty(n) = O(\log n)$。

::: insight 并行算法的本质是对抗因果链的代数重排
在单机串行思维中，计算是沿着时间单向流动的一维因果链（从 $i$ 流向 $i+1$）；而在并行计算的世界里，所有计算都被升维为多维空间中的树形或图状拓扑。Work-Span 模型告诉我们，算法工程师的核心任务不是盲目增加线程数量，而是利用算子的代数性质（如结合律、结合律与分配律）**主动打破时间轴上的刚性因果链**。以并行 Scan 为代表的树状折叠技术，正是通过在空间上构建对称的平衡树，将原本长度为 $n$ 的因果链压缩至对数深度 $\log n$，从而在物理多核芯片上释放出巨大的吞吐潜能。
:::
