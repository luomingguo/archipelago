---
title: 哈希映射、集合与广度优先搜索
type: lecture
lecture: 11
tags: [hashing, sets, bfs, breadth-first-search, shortest-path]
status: complete
source: https://introcomp.mit.edu/fall26
---

# Lec 11 哈希映射、集合与广度优先搜索（Hashing, Sets & BFS）

> MIT 6.100 · 计算机科学与 Python 编程导论 · Fall 2026 · 教材参考：Guttag 5.7, 5.1, 5.5, 14.2.1

## TL;DR

- **哈希函数与常数级寻址**：哈希函数将任意对象映射为定长整数，通过数组槽位直接寻址结合冲突解决机制，实现集合与字典 $O(1)$ 平均时间复杂度的超高速成员检测。
- **集合（Set）的数学运算**：集合是唯一无序元素的集合体，提供交集（`&`）、并集（`|`）与差集（`-`）等高效去重与集合代数运算。
- **广度优先搜索（BFS）**：基于先进先出（FIFO）队列逐层向外波浪式扩展，天然保证在无权图（或等权图）中首次访问目标节点时所经历的路径必然是最短路径。

## 1. 哈希原理与集合（Set）数据结构

为什么在包含 1000 万个元素的 Python 列表中查找某个值需要几秒钟（$O(N)$ 线性扫描），而在同样大小的集合（`set`）或字典（`dict`）中查找却能在几微秒内瞬间完成？

这背后的核心加速机制就是**哈希（Hashing）**：
1. **哈希函数（Hash Function）**：输入任意不可变对象，计算出一个确定性的整数散列值（通过内置函数 `hash(obj)`）。
2. **桶数组直接索引**：将哈希值对底层数组长度取模 `slot = hash(key) % array_size`，直接跳转到对应内存地址读取。
3. **哈希冲突（Collision）处理**：当两个不同对象映射到同一个桶槽位时，Python 采用开放寻址法（Open Addressing）进行二次探测。

```python
# 集合的成员检测具有 O(1) 性能优势
forbidden_passwords = {"123456", "password", "qwerty", "admin"}

def is_secure(pwd: str) -> bool:
    # 瞬间在 O(1) 内完成判定
    return pwd not in forbidden_passwords
```

集合还原生支持数学集合代数运算：
- 并集：`A | B`
- 交集：`A & B`
- 差集：`A - B`
- 对称差集：`A ^ B`

---

## 2. 广度优先搜索（BFS）算法与队列模型

广度优先搜索（Breadth-First Search, BFS）是图算法中最基础且威力巨大的搜索范式。

它的搜索策略如同向平静的水面投入一枚石子：**波纹从起点开始，以同心圆的方式一圈一圈向外层层扩散**。先访问所有距离起点为 1 步的邻居，再访问距离为 2 步的邻居，以此类推。在图遍历过程中，这种特性直接带来了一个无比关键的数学性质：如果边的权重全部相等（例如每次移动均为 1 步），那么当我们第一次在搜索树中看到终点节点时，这条从根节点到该节点的路径就绝对不可能是绕远的，它必然就是全局最短路径！

::: definition BFS 最短路径性质
在边权均为正等值（或无权）的图结构中，广度优先搜索首次触达目标节点时所经过的路径，必然包含最少的边数（即全局最短路径）。
:::

为了在代码中严格维护“先探索近处节点、后探索远处节点”的时序关系，我们不能使用任意容器，而必须借助于**先进先出（FIFO, First-In-First-Out）的队列（Queue）**。队列保证了先被发现的浅层节点其后继路径必然先于深层节点被取出并展开。同时，为了防止在包含环路的复杂图（如环形道路网）中陷入无限死循环，算法必须搭配一个基于哈希的**已访问集合（Visited Set）**，一旦某个节点已经被扩展或入队，后续再次遭遇该节点时立即予以跳过：

```python
from collections import deque
from typing import Dict, List, Optional

def bfs_shortest_path(graph: Dict[str, List[str]], start: str, target: str) -> Optional[List[str]]:
    """
    使用 BFS 寻找从 start 到 target 的最短节点跳数路径
    """
    if start not in graph or target not in graph:
        return None
    if start == target:
        return [start]
    
    # 队列中存放的是完整的探索路径列表，初始化放入起点路径 [start]
    queue = deque([[start]])
    # 记录已访问过的节点，规避环路无限死循环
    visited = {start}
    
    while queue:
        # 取出队列头部的最早路径
        current_path = queue.popleft()
        current_node = current_path[-1]
        
        # 扩展当前节点的所有邻居
        for neighbor in graph.get(current_node, []):
            if neighbor == target:
                # 首次抵达目标，当前路径拼接上 neighbor 即为最短解
                return current_path + [neighbor]
            
            if neighbor not in visited:
                visited.add(neighbor)
                # 构造延伸路径并压入队列尾部
                queue.append(current_path + [neighbor])
                
    return None  # 队列已空仍未找到，两点不连通
```

我们利用上一讲建立的 MIT 校园地图进行寻路测试。在这段测试代码中，程序首先加载了包含 6 个建筑节点的拓扑字典。当调用 `bfs_shortest_path` 函数时，队列首先将起点 `["Great Dome"]` 压入，随后在其邻居中顺次探索至 `Building 10`。在下一轮循环中，`Building 10` 又将其相连的 `Building 4` 与 `Building 13` 分别打包为全新路径推进队列。整个执行过程严密保持了由近及远的层级推进：

```python
campus_network = {
    "Building 10": ["Building 4", "Building 13", "Great Dome"],
    "Building 4":  ["Building 10", "Building 8"],
    "Building 8":  ["Building 4", "Student Center"],
    "Building 13": ["Building 10"],
    "Great Dome":  ["Building 10"],
    "Student Center": ["Building 8"]
}

path = bfs_shortest_path(campus_network, "Great Dome", "Student Center")
print("从 Great Dome 到 Student Center 的最短导航路径：")
print(" -> ".join(path))  # Great Dome -> Building 10 -> Building 4 -> Building 8 -> Student Center
```

从打印输出的路径可以看出，算法并未被分支更多的无关节点所干扰，而是以最简洁的四步直达 Student Center，完美展现了 BFS 在拓扑遍历中的高确定性。

### 复杂度分析

设图的顶点数为 $|V|$，边数为 $|E|$：
- **时间复杂度**：每个节点至多入队出队一次，每条边至多被扫描检查常数次，总时间为 $O(|V| + |E|)$。
- **空间复杂度**：最坏情况下队列与 `visited` 集合需要容纳所有节点，空间为 $O(|V|)$。

::: pitfall 误用标准列表作为 BFS 队列
在 Python 中，如果使用标准 `list` 并通过 `list.pop(0)` 实现出队，该操作的时间复杂度为 $O(N)$（因为删除首元素会导致后续所有元素在内存中向前平移 1 个单位）。如果搜索规模达到万级节点，算法整体将灾难性退化为 $O(|V|^2)$！在实现 BFS 时，必须严格使用 `collections.deque` 实现双端 $O(1)$ 出队。
:::

## 我的理解

::: insight 状态空间的同心圆波浪
BFS 的思想远超几何地图寻路。在博弈论（如魔方复原、八数码拼图、象棋推演）中，任何问题都可以被建模为“状态图”：每一个可能的游戏局面是一个节点，每一个合法的操作规则是一条边。BFS 确保了我们能以最少的移动步数，找到解开迷题的全局最优策略。
:::
