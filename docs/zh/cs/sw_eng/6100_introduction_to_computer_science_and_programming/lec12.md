---
title: 递归求解思维与深度优先搜索引入
type: lecture
lecture: 12
tags: [recursion, divide-and-conquer, dfs, depth-first-search, call-stack]
status: complete
source: https://introcomp.mit.edu/fall26
---

# Lec 12 递归求解思维与深度优先搜索引入（Recursion & Introduction to DFS）

> MIT 6.100 · 计算机科学与 Python 编程导论 · Fall 2026 · 教材参考：Guttag 17.5, 5.6, 14.2

## TL;DR

- **递归两要素**：递归算法将大问题规约为同构的更小子问题，必须具备无需递归的基准情形（Base Case）与逐步向基准情形收敛的递推步骤（Recursive Step）。
- **递归调用栈推演**：每一次递归调用均会在系统栈上压入一个全新的局部栈帧；若缺失基准情形或无法收敛，将导致栈空间耗尽引发递归深度超限错误。
- **深度优先搜索（DFS）思想**：沿着一条可能路径“不撞南墙不回头”地一探到底，遭遇死胡同后利用函数调用栈自动回溯（Backtracking）探索备选分支。

## 1. 递归思维：从数学归纳法到分治求解

初学编程者习惯于用循环来思考问题（“先做第一步，再做第二步，持续循环直到完成”），这种思维被称为命令式迭代。而**递归（Recursion）**代表了一种截然不同且更为强大的声明式计算心智模型。

递归的本质思想直接脱胎于数学归纳法（Mathematical Induction）：
- **基础步（Base Case）**：证明命题在最简单的情形（如 $n = 0$ 或 $n = 1$）下成立。
- **归纳步（Inductive Step）**：假定命题对规模为 $n-1$ 的子问题已经成立，在此基础上推导出规模为 $n$ 的解。

```python
def factorial(n: int) -> int:
    """
    计算非负整数 n 的阶乘 n!
    """
    # 基准情形：0! = 1
    if n == 0:
        return 1
    # 递推步骤：n! = n * (n - 1)!
    return n * factorial(n - 1)
```

::: definition 递归的两大不可妥协契约
1. **明确且完备的基准情形（Base Case）**：必须存在至少一个直接返回已知结果、不再发起任何递归调用的终止分支。
2. **严格单调收敛的递推步（Recursive Step）**：每一次递归调用传入的参数规模必须严格小于当前问题规模，保证状态单调逼近基准情形。
:::

---

## 2. 汉诺塔（Towers of Hanoi）与调用栈帧展开

汉诺塔问题是展示递归威力最经典的范例：三根柱子 $A, B, C$，初始时 $A$ 柱上自下而上套有 $n$ 个由大到小的圆盘，要求在每次仅移动一个圆盘且大盘永远不能压在小盘之上的前提下，将所有圆盘完整移至 $C$ 柱。

若试图用迭代循环追踪每个盘子的具体位移，其逻辑将极其晦涩；但若站在递归的高度思考，整个移动过程被不可思议地简化为三步：
1. 将前 $n-1$ 个小盘借助目标柱 $C$，从源柱 $A$ 移动到辅助柱 $B$；
2. 将第 $n$ 个底盘直接从源柱 $A$ 移动到目标柱 $C$；
3. 将暂存在辅助柱 $B$ 上的 $n-1$ 个小盘借助源柱 $A$，从 $B$ 移至目标柱 $C$。

```python
def solve_hanoi(n: int, source: str, target: str, spare: str) -> None:
    """
    将 n 个圆盘从 source 移动到 target，以 spare 作为辅助柱
    """
    if n == 1:
        print(f"将 1 号圆盘从 {source} 移动至 {target}")
        return
    
    # 步骤 1：先将 n - 1 个盘子移到辅助柱
    solve_hanoi(n - 1, source, spare, target)
    
    # 步骤 2：移动当前最大的底盘
    print(f"将 {n} 号圆盘从 {source} 移动至 {target}")
    
    # 步骤 3：将辅助柱上的 n - 1 个盘子移到目标柱
    solve_hanoi(n - 1, spare, target, source)

solve_hanoi(3, "A", "C", "B")
```

在系统底层，每一次调用 `solve_hanoi` 都会将局部变量与返回地址作为一个栈帧压入调用栈（Call Stack），当最深层的基准情形 `n == 1` 执行完毕后，栈帧自顶向下逐一弹出，自动恢复上一层调用时的执行环境。

---

## 3. 深度优先搜索（DFS）初探与回溯机制

对比上一讲 BFS 的波浪式同心圆层级推进，**深度优先搜索（Depth-First Search, DFS）**采取了完全不同的策略：**一旦选定一个方向，就执着地沿着该分支不断向前深入，直到撞见死胡同（无法前行）或找到目标为止**。当一条路径被证明不可行时，算法沿着调用栈向后撤退一步，重新探索该节点上的其他备选分支，这种试错机制被称为**回溯（Backtracking）**。

利用递归的天然调用栈，我们可以写出极其精简的图连通性 DFS 搜索：

```python
from typing import Dict, List, Optional

def dfs_find_path(graph: Dict[str, List[str]], current: str, target: str, visited: Optional[List[str]] = None) -> Optional[List[str]]:
    """
    使用递归 DFS 寻找从 current 到 target 的一条可行路径
    """
    if visited is None:
        visited = []
        
    visited = visited + [current]
    
    # 基准情形：抵达目标
    if current == target:
        return visited
        
    # 递推步骤：递归深入探索邻接节点
    for neighbor in graph.get(current, []):
        if neighbor not in visited:
            # 递归深入，返回非空路径即代表寻路成功
            path = dfs_find_path(graph, neighbor, target, visited)
            if path is not None:
                return path
                
    return None  # 所有分支均已穷尽且失败，触发回溯
```

与 BFS 相比，DFS 的优势在于其极低的空间占用：如果搜索树的深度为 $h$，DFS 在任意时刻只需维护当前路径上的 $O(h)$ 个栈帧，而在极深的大规模图搜索中，BFS 往往会因为队列中堆积海量同层节点而耗尽内存。

::: pitfall Python 默认递归深度限制
Python 为了防止 C 级别栈溢出崩溃，默认设置了递归调用深度上限（通常为 1000）。当递归层数过深时会抛出 `RecursionError: maximum recursion depth exceeded`。在处理超长链表或超大图时，应将递归改写为显式维护栈结构的迭代版本，或通过 `sys.setrecursionlimit()` 提高上限。
:::

## 我的理解

::: insight 递归是自相似世界的自然镜像
许多复杂的数据结构（树、AST 语法树、DOM 树、分形几何、嵌套字典）本身就是通过递归规则定义的：一棵树就是根节点加上若干棵子树。处理自相似结构的最自然语言必然是递归。当我们学会相信递归假设（“假定子树已经求解完成”），原本错综复杂的算法推演瞬间化为几行优雅的数学映射。
:::
