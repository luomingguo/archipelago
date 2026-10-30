---
title: 深度优先回溯与 Dijkstra 最短路径算法
type: lecture
lecture: 13
tags: [dijkstra, dfs-backtracking, weighted-graphs, priority-queue, shortest-path]
status: complete
source: https://introcomp.mit.edu/fall26
---

# Lec 13 深度优先回溯与 Dijkstra 最短路径算法（DFS Backtracking & Dijkstra）

> MIT 6.100 · 计算机科学与 Python 编程导论 · Fall 2026 · 教材参考：Guttag 14.2, 6.1–6.2

## TL;DR

- **DFS 全路径回溯与带权剪枝**：DFS 可遍历两点间的所有可能简单路径，结合全局最优距离剪枝，能在搜索途中提前放弃劣于当前已知解的无用分支。
- **带权图最短路与 BFS 的失效**：当图中的边带有非均匀正权重（如真实路网里程或耗时）时，跳数最少的路径不再是最优路径，无权 BFS 无法保证解的正确性。
- **Dijkstra 贪心算法核心**：利用优先队列（Priority Queue）每次挑选当前距离起点累积代价最小的未确定节点进行松弛（Relaxation），在正权图上以 $O((|V| + |E|)\log |V|)$ 确定性求得单源最短路径。

## 1. DFS 最短路径搜索与分支剪枝

在上一讲中，基础版本的深度优先搜索（DFS）仅用于寻找一条任意可行的通路：一旦遇到目标节点便立即沿调用栈向外返回。然而在现实工程中，我们通常需要寻找包含实际权重（如道路通行时长、油耗或机票价格）的全局最优最短路径。

若要利用 DFS 解决这一最优化问题，算法不能在找到第一条路径后就草草收场，而必须遍历两点之间所有可能的无环简单路径，并在所有可行候选解中比较选出总权重最小的那一条。但在包含大量交叉路口的复杂网络中，简单路径的总数量随着节点数的增加呈现爆炸性的指数级增长。

为了有效遏制这种组合爆炸风险，算法工程中引入了**分支限界剪枝（Branch and Bound Pruning）**机制。其核心逻辑非常直观：在全图遍历的递归推进过程中，算法在全局维护一个用于记录“当前已知全局最短距离”的变量 `best_dist`。每当 DFS 沿着某一特定分支向前探索时，如果发现当前累积走过的路程 `current_dist` 已经超过或等于已知的 `best_dist`，算法就可以做出绝对确定的数学断言：无论该分支后续如何演进，其最终成本都绝不可能打破现有记录。此时程序果断放弃继续深入，立刻终止当前分支并执行回溯：

```python
from typing import Dict, List, Tuple, Optional

# 带权邻接字典：节点 -> [(邻居节点, 边权重)]
WeightedGraph = Dict[str, List[Tuple[str, float]]]

def dfs_shortest_weighted_path(
    graph: WeightedGraph,
    current: str,
    target: str,
    visited: List[str],
    current_dist: float,
    best_dist: float,
    best_path: Optional[List[str]]
) -> Tuple[float, Optional[List[str]]]:
    """
    带剪枝的 DFS 全局最短路径搜索
    """
    visited = visited + [current]
    
    if current == target:
        return current_dist, visited
        
    for neighbor, weight in graph.get(current, []):
        if neighbor not in visited:
            new_dist = current_dist + weight
            # 关键剪枝：若当前分支距离已超已知全局最优，直接放弃探索
            if new_dist < best_dist:
                dist_found, path_found = dfs_shortest_weighted_path(
                    graph, neighbor, target, visited, new_dist, best_dist, best_path
                )
                if path_found is not None and dist_found < best_dist:
                    best_dist = dist_found
                    best_path = path_found
                    
    return best_dist, best_path
```

通过这一剪枝技巧，DFS 在实际运行中能够大面积斩断指数级搜索树上的枯枝败叶。在算法实现细节中，有三个核心机制尤为值得深入剖析：
1. **路径拷贝传递（`visited + [current]`）**：这里没有使用原地修改的 `visited.append(current)`，而是采用了创建全新子列表的连接语法。这确保了在当前分支递归回溯时，父帧中的 `visited` 历史状态不会被错误污染，自然维护了不同平行分支之间的路径隔离性。
2. **界限动态收缩（Dynamic Bound Shrinking）**：初始时可以将 `best_dist` 设为正无穷大。一旦首次成功抵达目标节点，`best_dist` 就会瞬间被更新为一个有限实数。随着后续更优解的不断发现，搜索界限会越来越严格，导致后续无效分支被拦截得越来越早。
3. **最坏情况瓶颈**：尽管分支限界能够大幅削减实际搜索开销，但它的剪枝效率高度依赖于“是否能尽早碰巧找到一条较短的可行解”。如果在搜索初期连续踩入极深且昂贵的糟糕分支，算法依然难逃指数级的时间爆炸。这促使我们转向具备严格多项式时间保证的最优搜索算法。

---

## 2. 为什么无权 BFS 无法求解带权图

在 Lec 11 中，我们证明了 BFS 能够以 $O(|V| + |E|)$ 的极高效率找到无权图的最短路径。然而，一旦边上被赋予了实际的物理度量（例如距离、票价或网络延迟），BFS 的最短路径性质将彻底崩溃。

考虑如下经典反例：
- 节点 $A$ 直接连通至 $B$，边权重为 $100$（直达但极慢）；
- 节点 $A$ 经由中继 $C$ 连接到 $B$，其中边 $A \to C$ 权重为 $1$，$C \to B$ 权重为 $2$。

如果运行 BFS，算法在第一层搜索时就会发现直达路径 $A \to B$（仅消耗 1 跳），并将其判定为最短路径输出（总成本 100）；而真正的全局最优路径 $A \to C \to B$（消耗 2 跳，但总成本仅为 3）却会被 BFS 视作冗余而弃用！

为了在带权网络中高效求解单源最短路径，计算机科学界迎来了荷裔计算机科学家艾兹格·迪杰斯特拉（Edsger W. Dijkstra）的传世之作。

---

## 3. Dijkstra 贪心算法原理解析与实现

Dijkstra 算法的绝妙之处在于将贪心选择性质与动态状态松弛完美融合：

::: definition Dijkstra 算法执行流程
1. **距离数组初始化**：将起点的最短估计距离设为 0，其余所有顶点设为正无穷大（$\infty$）。
2. **贪心选择**：从未被永久确定的顶点集合中，挑选出当前估计距离最小的节点 $u$。由于图中的所有边权均为非负数，此时到达 $u$ 的距离已经不可能被其他更远的分支后续反超，故 $u$ 的最短距离正式被永久固化。
3. **边松弛（Relaxation）**：遍历 $u$ 的所有出边 $(u, v)$，若发现通过 $u$ 中转抵达 $v$ 的新成本小于此前记录的估计值（即 $\text{dist}[u] + w(u, v) < \text{dist}[v]$），则向下更新 $\text{dist}[v]$ 的值。
4. **重复迭代**：重复步骤 2 与 3，直至所有可达节点均被确定。
:::

在 Python 中，为了快速完成“挑选当前距离最小节点”这一操作，我们必须借助于标准库 `heapq` 提供的最小堆优先队列（Min-Heap Priority Queue）：

```python
import heapq
from typing import Dict, List, Tuple

def dijkstra_algorithm(graph: WeightedGraph, start_node: str) -> Dict[str, float]:
    """
    计算从 start_node 到图中所有可达节点的最短距离字典
    """
    # 记录各节点的最短距离表，初始为无穷大
    distances: Dict[str, float] = {node: float('inf') for node in graph}
    distances[start_node] = 0.0
    
    # 优先队列中存放元组：(当前累积距离, 当前节点标识)
    priority_queue: List[Tuple[float, str]] = [(0.0, start_node)]
    
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        # 懒惰删除处理：若当前出堆的距离已大于已知最优记录，直接跳过
        if current_distance > distances[current_vertex]:
            continue
            
        for neighbor, edge_cost in graph.get(current_vertex, []):
            distance_via_current = current_distance + edge_cost
            
            # 松弛操作：找到更短路径
            if distance_via_current < distances[neighbor]:
                distances[neighbor] = distance_via_current
                heapq.heappush(priority_queue, (distance_via_current, neighbor))
                
    return distances

# 测试用例：验证带权反例
network = {
    "A": [("B", 100.0), ("C", 1.0)],
    "B": [],
    "C": [("B", 2.0)]
}

shortest_distances = dijkstra_algorithm(network, "A")
print(f"从 A 到 B 的最小代价为：{shortest_distances['B']}")  # 正确输出 3.0
```

### 复杂度对比

- **时间复杂度**：利用二叉最小堆优化后，每次堆操作耗时 $O(\log |V|)$，总时间复杂度为 $O((|V| + |E|)\log |V|)$，远优于 DFS 的最坏阶乘级指数穷举。
- **限制边界**：Dijkstra 算法**严禁出现负权边**。若存在负边，贪心选择的单调不可逆性被打破，可能导致算法产出错误结论，此时必须改用 Bellman-Ford 算法。

::: pitfall 贪心算法在负权边场景下的失效
Dijkstra 算法成立的理论基石在于：从优先队列取出的节点其距离已经不可能被其他分支进一步缩小。如果图中存在一条权值为负数的边，某条原本看起来更长的路径在叠加负权后可能会变得极小，从而颠覆贪心选择的前序断言。
:::

## 我的理解

::: insight 局部贪心迈向全局最优的数学约束
Dijkstra 算法展示了贪心选择性质的强大与脆弱。贪心算法往往最轻快优雅，但它成立的背后必须有严格的物理边界作为庇护（在非负距离世界里，走得越远成本必然越高）。在软件架构设计中，当我们试图使用局部贪心策略优化业务性能时，必须反复审视系统是否存在“负权”反例打破了全局单调性。
:::
