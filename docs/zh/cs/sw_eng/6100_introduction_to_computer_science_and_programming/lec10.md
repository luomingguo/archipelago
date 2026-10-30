---
title: 映射字典、不可变元组与图表示
type: lecture
lecture: 10
tags: [dictionaries, tuples, graph-representation, adjacency-list, key-value]
status: complete
source: https://introcomp.mit.edu/fall26
---

# Lec 10 映射字典、不可变元组与图表示（Dictionaries, Tuples & Graphs）

> MIT 6.100 · 计算机科学与 Python 编程导论 · Fall 2026 · 官方讲义核心内容

## TL;DR

- **不可变序列元组（Tuples）**：元组是用小括号表示的定长不可变序列，由于其哈希值固定不可变，天然适于作为复合数据的键（如多维坐标）。
- **键值映射字典（Dictionaries）**：字典是基于散列表实现的可变关联容器，支持以接近 $O(1)$ 的时间复杂度实现键到值的增删改查映射。
- **图结构的邻接字典建模**：图由节点（Nodes/Vertices）与边（Edges）构成，在 Python 中最自然高效的计算机表示是邻接表字典（Adjacency Dictionary）。

## 1. 元组（Tuple）：不可变多元组与安全复合键

元组（Tuple）是 Python 中最紧凑高效的只读序列。与列表不同，元组一旦创建便严禁执行任何原地修改操作：

```python
coords = (42.3601, -71.0942)  # MIT 经纬度坐标
# coords[0] = 40.0  # 报错：TypeError: 'tuple' object does not support item assignment
```

元组具有两项无可替代的核心用途：
1. **轻量多值打包与解包（Unpacking）**：函数返回多个数值时，Python 会隐式打包为元组返回，调用方可一行优雅解包：
   ```python
   def get_min_max(values: list) -> tuple:
       return min(values), max(values)
   
   low, high = get_min_max([12, 5, 87, 1])
   ```
2. **哈希散列与字典键**：字典要求键必须是不可变对象。元组（只要其包含的子元素均为不可变类型）具备固定哈希值，是表示网格坐标 `(row, col)` 键的最优选择。

---

## 2. 映射字典：底层原理与语法接口

列表通过连续的整数下标索引数据（$0, 1, 2, \dots$），而字典（Dictionary）允许使用任意不可变自定义对象作为键（Key），建立到值（Value）的定向映射。

在 Python 3.7+ 中，字典不仅保证键的唯一性，还保证插入顺序的确定性保持：

```python
# 词频统计器
text = "to be or not to be that is the question"
word_counts = {}

for word in text.split():
    # 常用惯用写法：利用 get 提供默认回退值
    word_counts[word] = word_counts.get(word, 0) + 1

print(word_counts["to"])  # 2
```

::: definition 字典常用时间复杂度
- **键查找 / 插入 / 删除**：平均为 $O(1)$ 常数时间，最坏情况（严重哈希冲突）退化为 $O(N)$。
- **键遍历**：`dict.keys()`、`dict.values()`、`dict.items()` 均为 $O(N)$ 线性时间视图。
:::

---

## 3. 图（Graphs）的抽象定义与邻接字典建模

图是计算机科学中表达复杂关联关系的最通用抽象数据模型。社交网络好友关注、交通路网导航、互联网网页超链接以及任务依赖拓扑，本质上都是图结构。

::: definition 图的数学定义
图 $G = (V, E)$ 由非空顶点集合 $V$（Vertices）和连接顶点的边集合 $E$（Edges）组成。若边具备方向性，则称为有向图（Digraph）；若边带有权重（如距离或费用），则称为带权图（Weighted Graph）。
:::

在 Python 中，建模图结构无需过早引入复杂的第三方库。最符合 Pythonic 哲学的轻量高效表达方式是**邻接表字典（Adjacency Dictionary）**：
- 字典的**键（Key）**：表示图中的每一个源节点。
- 字典的**值（Value）**：表示该节点可以直接抵达的邻接后继节点列表（或集合）。

```python
from typing import Dict, List

# 校园建筑道路网络邻接表
campus_map: Dict[str, List[str]] = {
    "Building 10": ["Building 4", "Building 13", "Great Dome"],
    "Building 4":  ["Building 10", "Building 8"],
    "Building 8":  ["Building 4", "Student Center"],
    "Building 13": ["Building 10"],
    "Great Dome":  ["Building 10"],
    "Student Center": ["Building 8"]
}

def print_graph_connections(graph: Dict[str, List[str]]) -> None:
    """
    遍历并打印图中所有连通通道
    """
    for node, neighbors in graph.items():
        destinations = ", ".join(neighbors)
        print(f"[{node}] 能够直接抵达 -> {destinations}")

print_graph_connections(campus_map)
```

这种表示法不仅内存占用极低（仅存储实际存在的边，空间复杂度为 $O(|V| + |E|)$），而且能够在 $O(1)$ 时间内瞬间取出任意特定节点的所有出边邻居，为下一讲的图搜索算法提供了极其高效的遍历访问接口。

::: pitfall 使用可变列表作为字典键导致崩溃
尝试使用列表作为字典键会引发致命运行时错误：
```python
d = {}
d[[1, 2]] = "invalid"  # 报错：TypeError: unhashable type: 'list'
```
这是因为可变列表的内容随时可能被就地修改，如果允许其作为键，哈希槽位将失去寻址稳定性。遇到多维联合索引时，必须统一转换为不可变元组 `d[(1, 2)] = "valid"`。
:::

## 我的理解

::: insight 关系比实体更重要
面向对象初学者往往执着于为“建筑”、“网页”建立繁琐的实体类，而图论思想告诉我们：现实世界复杂性的根源在于实体之间的连接拓扑。字典将孤立的节点编织为相互引用的关系网，掌握了邻接字典的构建，就打通了从离散数据处理通往图搜索与网络优化的关键通道。
:::
