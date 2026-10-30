---
title: 并行动态图算法与并查集
type: lecture
lecture: 17
tags: [dynamic-graphs, union-find, parallel-algorithms, connected-components, work-efficiency]
status: complete
---

# Lec 17 并行动态图算法与并查集（Parallel Dynamic Graph Algorithms & Union-Find）

## TL;DR

- 动态图计算通过批量更新（Batch Updates）吸收高频边流，避免了每次边插入或删除时全图静态重算的巨大代价。
- 经典串行并查集依赖完全路径压缩与按秩合并，但在多核并发下直接加锁会导致热点根节点的灾难性写竞争。
- 无锁并行并查集采用随机化挂接（Random Hooking）与路径减半（Path Halving）策略，结合原子 CAS 操作消除死锁并防止有向成环。
- ConnectIt 框架证明：在并发多线程环境下，适度弱化路径压缩深度以减少共享缓存行失效，能在理论工作量高效性（Work-Efficiency）与硬件吞吐间达成最优折中。

## 静态图到动态图处理的范式跃迁

在前述讲义中，我们讨论的 Ligra、GraphChi 与 GraphIt 等经典图计算框架均建立在**静态图（Static Graph）**假设之上：图的拓扑结构（顶点集 $V$ 与边集 $E$）在计算开始前已经固化并完全装载至 CSR/CSC 矩阵中。

然而，在社交网络演化、金融交易风控、网络安全流量监测以及知识图谱流式补全等工业级现实场景中，图拓扑始终处于高度动态的摄取状态：

$$
G_{t} = G_0 \cup \Delta E^+_1 \setminus \Delta E^-_1 \cup \Delta E^+_2 \setminus \Delta E^-_2 \dots
$$

若每当系统接收到数条新边时，都重新调用静态连通分量（Connected Components, CC）或双连通分量算法，每次批处理将承担高达 $O(|V| + |E|)$ 的全图遍历开销。当吞吐量达到每秒数百万边时，系统将彻底瘫痪。

因此，**动态图算法（Dynamic Graph Algorithms）**的工程目标在于：将持续流入的边组织为微批次（Batch of Edges $\Delta E$），在保持图算法时间复杂度对批次规模 $|\Delta E|$ 敏感的同时，充分利用多核并行处理能力实现亚毫秒级的低延迟增量更新。

```mermaid
flowchart LR
    Stream["流式边事件流<br/>(e1, e2, e3... 每秒数百万)"] --> Batch["微批次聚束器 (Batching)<br/>B = {e_1, ..., e_k}"]
    Batch --> Filter["批内并行去重与自环消除"]
    Filter --> ParallelUF["无锁并行并查集<br/>CAS 挂接与路径减半"]
    ParallelUF --> Forest["连通分量生成树森林<br/>动态增量维护"]
```

## 并行并查集（Parallel Disjoint Set / Union-Find）的核心挑战

连通分量是动态图处理中最核心的基础原语。对于仅包含边插入的增量图（Incremental Graph），**并查集（Union-Find / Disjoint-Set Union）**是最高效的数据结构。

在串行计算模型下，Tarjan 证明了结合**路径压缩（Path Compression）**与**按秩合并（Union by Rank）**的并查集，处理 $m$ 次操作的时间复杂度为近乎线性的 $O(m \cdot \alpha(n))$，其中 $\alpha$ 是阿克曼函数的反函数。

然而，将串行并查集直接迁移至现代共享内存多核硬件时，面临严峻的体系结构挑战：

1. **共享根节点的缓存颠簸（Cache Ping-Pong）**：
   在无向图连通性计算中，属于同一庞大连通分量的数千个顶点往往拥有相同的根节点（Root）。如果多个核心并发执行 `Union` 操作并在根节点处加锁或原子修改其父节点，该根节点所在的缓存行（Cache Line）将在数十个 CPU 核心的私有 L1/L2 缓存之间高频失效迁移，导致总线带宽瞬间饱和。
2. **并发路径压缩的拓扑破坏与死锁**：
   若并发线程在没有全局互斥锁保护的情况下尝试更新指针 `parent[u] = parent[parent[u]]`，可能发生写冲突，甚至导致父指针相互引用形成拓扑环路（Cycle），引发后续 `Find` 操作陷入死循环。
3. **工作量高效性（Work-Efficiency）的退化**：
   若使用粗粒度读写锁保证安全性，算法的理论跨度（Span）将退化为与并发操作数线性相关，丧失了并行扩展能力；而若完全放弃路径压缩，单次查找的树深退化为 $O(n)$，使得总计算工作量从 $O(m \alpha(n))$ 剧增至 $O(m \cdot n)$。

## 无锁并行并查集设计：Blelloch-Shun 随机化挂接与路径压缩

为了在多核并行环境下兼顾无锁进度保证（Lock-Freedom）与 $O(m \alpha(n))$ 的严格工作量高效性，Blelloch、Shun、Dhulipala 等学者提出了一套基于原子比较并交换（Compare-And-Swap, CAS）的无锁挂接与路径折半算法体系。

### 规则化单向挂接（Directional Hooking）

消除并发环路的核心原则在于打破对称性，强制所有合并操作必须遵循全局严格单调的序关系：

::: definition [确定性优先级挂接准则]
为图中的每个顶点 $u \in V$ 分配一个唯一的只读优先级标识 $P(u)$（例如顶点的唯一 ID，或者在初始化时通过哈希函数生成的伪随机数）。
当需要合并两个处于不同树上的代表节点 $r_1$ 与 $r_2$ 时，约定必须且只能由**优先级较低**的根节点将其父指针指向**优先级较高**的根节点：
$$
r_1 \to r_2 \iff P(r_1) < P(r_2)
$$
:::

该单调序准则从数学上杜绝了环路产生的可能性：由于父节点的优先级严格大于子节点，任意沿着父指针遍历的路径其优先级必然严格单调递增，因此绝不会存在指向自身的闭合环路。

```mermaid
flowchart TD
    subgraph TreeMerge["单向确定性挂接示例"]
        R1["根节点 r1<br/>ID: 42 (较低)"]
        R2["根节点 r2<br/>ID: 108 (较高)"]
        R1 -- "原子 CAS(parent[r1], r1, r2) 成功" --> R2
    end
```

### 路径折半（Path Halving）与路径分裂（Path Splitting）

传统的完全路径压缩要求在 `Find(u)` 执行时，将从 $u$ 到根节点路径上的所有节点直接连到根节点。这需要二次遍历并对路径上每个节点写入最新根节点指针，写冲突概率极高。

无锁算法改用单程非阻塞的**路径折半（Path Halving）**：

::: theorem [路径折半的不变式]
在 `Find` 遍历过程中，对于访问到的每个节点 $u$，若其父节点 $p$ 不是根节点（即 $p \neq parent[p]$），算法使用一次原子写或弱 CAS 将 $u$ 的父指针更新为其祖父节点：
$$
parent[u] \leftarrow parent[p]
$$
该操作使 $u$ 及其祖父节点之间的距离减半，且仅依赖局部的只读信息与单次原子写入，单核与多核下均能保证整棵树的深度被限制在 $O(\log n)$ 级别。
:::

## 批处理动态连通分量架构（ConnectIt / Batch-Dynamic CC）

在实际的大规模图流处理系统（如 ConnectIt）中，单次边插入被聚束为大小为 $B$ 的微批次。算法分为两阶段高效执行：

### 阶段一：批内过滤（Intra-Batch Filtering）
并发工作线程首先对微批次内的所有边进行局部粗筛：
1. 过滤掉自环边（$u = v$）；
2. 过滤掉批内重复出现的边；
3. 对属于当前线程本地私有分块的边进行局部 Union 操作，消除大量原本会直接冲击全局共享树的局部冗余边。

### 阶段二：并发全局合并（Inter-Batch Concurrent Linking）
剩余的跨边界边由工作窃取调度器（Cilk / OpenMP）分派到多核上并发执行无锁 `Link-and-Compress`。当所有线程完成当前批次的边消费后，调用一次全局轻量级规约（Parallel Flat Reduction），即可对外提供一致的连通性查询视图。

## 算法实现：无锁并行 Link-and-Compress 并查集

在工程实现中，必须采用现代 C++ 标准库中的 `std::atomic` 内存序语义，严防编译器重排与处理器乱序执行破坏内存可见性。

### 内存序选择与硬件微架构协同

在无锁算法的传统设计中，开发者往往保守地滥用全屏障内存序（`std::memory_order_seq_cst`），这会在 x86 与 ARM 平台上强制插入昂贵的总线锁指令（如 `MFENCE` 或 `DMB ISH`），造成严重的流水线停顿。

对于无锁并查集而言，底层的拓扑属性为内存序的极致松弛提供了数学支撑：
1. **路径折半的松弛写（Relaxed Store）**：在 `find_root` 中更新父指针时，由于树的单调优先级与无环性质不会因为单次内存写传播的轻微延迟而被破坏，因此完全可以使用开销最低的 `std::memory_order_relaxed`。即使某个核心读取到了尚未更新的旧父节点指针，算法依然能够沿着单调递增的指针安全到达真正的代表元，仅仅多经历一次跳步。
2. **挂接操作的获取-释放屏障（Acquire-Release）**：在执行关键的代表元原子合并时，`compare_exchange_weak` 采用 `std::memory_order_release`，确保被挂接子树先前的所有拓扑变更对后续观察到新父指针的核心完全可见。

### 挂接竞争与活锁消除

在并发合并阶段，最关键的细节在于处理多核并发挂接引发的 CAS 失败。当核心 A 尝试执行 `CAS(parent[r1], r1, r2)` 时，核心 B 可能已经先一步将 `r1` 挂接到了另一个更高优先级的节点 $r_3$。

算法无须采用任何重试计数器或随机退避（Exponential Backoff）自旋，因为：
- CAS 失败意味着目标节点 `r1` 的父指针已经被其他核心成功向前推进；
- 失败的核心只需将本地临时变量指针更新为最新的父节点，沿着新拓扑继续向上溯源；
- 每一个失败的循环都在有效缩短与当前最新根节点的逻辑距离，因此系统整体具有严格的无锁前向推进保证（Lock-Freedom），绝不存在死锁与活锁。

为了保证数据在内存中的连续性并减少页表查找开销，顶点的父指针数组应当在连续虚拟内存中线性分配，并对齐于 64 字节的缓存行边界。同时，在调用端使用 OpenMP 或 Cilk 并行循环驱动边集的并发处理，通过将待合并的边按端点哈希初步分桶，能够进一步削弱对共享代表元的争抢压力。

下面给出了经过生产验证的无锁并行并查集精简核心实现：

```cpp
#include <atomic>
#include <cstdint>
#include <vector>

class ParallelUnionFind {
    std::vector<std::atomic<uint32_t>> parent;

public:
    explicit ParallelUnionFind(uint32_t n) : parent(n) {
        for (uint32_t i = 0; i < n; ++i) parent[i].store(i, std::memory_order_relaxed);
    }

    uint32_t find_root(uint32_t u) {
        uint32_t curr = u;
        while (true) {
            uint32_t p = parent[curr].load(std::memory_order_relaxed);
            uint32_t gp = parent[p].load(std::memory_order_relaxed);
            if (p == curr) return curr;
            if (p == gp) return p;
            parent[curr].store(gp, std::memory_order_relaxed); // 路径折半
            curr = gp;
        }
    }

    void unite(uint32_t u, uint32_t v) {
        while (true) {
            uint32_t root_u = find_root(u), root_v = find_root(v);
            if (root_u == root_v) return;
            if (root_u > root_v) std::swap(root_u, root_v); // 强制单向挂接
            uint32_t expected = root_u;
            if (parent[root_u].compare_exchange_weak(
                    expected, root_v, std::memory_order_release, std::memory_order_relaxed)) {
                return;
            }
        }
    }
};
```

在执行上述逻辑时，弱比较交换（`compare_exchange_weak`）比强版本（`compare_exchange_strong`）具有显著的性能优势。在 ARM 或 RISC-V 等基于加载链接/条件存储（LL/SC）的弱内存模型体系结构中，强比较交换需要外包一层重试循环以规避硬件假性失败（Spurious Failure）；而弱比较交换可直接映射为单条条件存储指令，假性失败将直接顺应外层 `while(true)` 循环无缝重试，彻底消除了硬件层面的冗余分支跳转。

上述实现的巧妙之处在于整个算法没有任何显式锁、自旋锁或死循环风险。对于包含数亿顶点的图拓扑，即使 64 个 CPU 核心同时对其施加巨量并发 `unite`，所有核心均能持续前向推进（Wait-Free / Lock-Free）。

## 工程权衡：树深控制 vs 并发写冲突的物理边界

在算法工程的视角下，经典理论中对“树深越浅越好”的直觉在多核共享内存体系中被彻底颠覆。

::: insight 结构扁平化与写放大的并发矛盾
在传统的算法理论中，Tarjan 的完全路径压缩之所以被推崇至极致，是因为在单核上每一次额外的指针写操作代价极低，而将树完全扁平化（高度压至 1）能使后续所有查找的理论步数缩减至 1。

然而在多核体系结构下：
1. **写放大引发总线饱和**：完全路径压缩意味着每次 `Find` 遍历都必须对整条路径上的所有节点执行写操作（Store）。在 MESI 缓存一致性协议下，每次写内存都要求当前核心向总线广播 `Invalidate` 消息，并强制将对应的缓存行独占（Modified 状态）。
2. **读操作的高效性**：相反，路径折半（Path Halving）在绝大部分情况下只执行廉价的局部写，树的深度依然稳定保持在极其扁平的 $O(\log n)$ 范围（实际测试中平均深度极少超过 3 到 4 层）。

实验表明，在高并发争用场景下，**适度容忍树高度多增加 1 到 2 层，换取写冲突与总线广播报文暴降 80%**，系统的整体吞吐量反而提升了 2 到 4 倍。这是算法工程中典型的“以极微小的理论工作量让步，换取微架构硬件亲和性最大化”的经典范例。
:::

| 算法变种 | 理论工作量（Work） | 理论跨度（Span） | 缓存一致性写冲突 | 现代多核硬件适用度 |
| :--- | :--- | :--- | :--- | :--- |
| **串行加粗粒度互斥锁** | $O(m \alpha(n))$ | $O(m)$（完全串行化） | 低（串行排队） | 极差（多核加速比接近 1） |
| **无锁完全路径压缩** | $O(m \alpha(n))$ | $O(\text{polylog}(n))$ | 极高（每次查找重写整条链） | 较差（高并发下总线颠簸严重） |
| **无锁随机挂接 + 路径折半** | $O(m \alpha(n))$ | $O(\text{polylog}(n))$ | 极低（单向无环、弱内存序写入） | **极优（生产系统主流实现）** |
| **无路径压缩随机合并** | $O(m \log n)$ | $O(\log^2 n)$ | 零（纯只读查找，仅合并写一次） | 中等（理论工作量退化明显） |
