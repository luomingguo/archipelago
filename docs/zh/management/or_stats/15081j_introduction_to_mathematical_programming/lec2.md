---
title: '多面体几何学基础：超平面、半空间与凸集 (Geometry of Polyhedra I)'
type: lecture
lecture: 2
tags: [polyhedral-geometry, convex-sets, halfspaces, extreme-points]
status: complete
---

# Lec 2 多面体几何学基础：超平面、半空间与凸集 (Geometry of Polyhedra I)

> MIT 15.081J / 6.251J 数学规划导论 · 讲义 2 · 授课教师：Prof. Dimitris Bertsimas / John Tsitsiklis

## TL;DR

- 多面体（Polyhedron）是有限个闭半空间的交集，是线性规划可行域的几何本质。
- 凸集、仿射集、凸包与锥包建立了高维欧氏空间集合生成的代数代数系统。
- 极点（Extreme Point）在多面体几何中具有不可被内部线段非平凡表出的刚性特征。

## 1. 仿射集、超平面与半空间

线性规划的全部代数计算，本质上都是高维凸多面体几何上的投影与行进。为了深刻理解单纯形法与对偶定理，必须从欧氏空间 $\mathbb{R}^n$ 中的基本几何对象建立严格公理。

::: definition 超平面与半空间
对于非零向量 $a \in \mathbb{R}^n \setminus \{0\}$ 和标量 $b \in \mathbb{R}$：
1. **超平面（Hyperplane）** 是集合 $H = \{x \in \mathbb{R}^n \mid a^T x = b\}$。超平面是仿射维数为 $n-1$ 的仿射子空间，其法向量为 $a$。
2. **闭半空间（Closed Halfspace）** 是集合 $H_{\le} = \{x \in \mathbb{R}^n \mid a^T x \le b\}$ 或 $H_{\ge} = \{x \in \mathbb{R}^n \mid a^T x \ge b\}$。半空间显然是凸集。
:::

由有限个半空间相交所围成的几何体，构成了运筹学中最核心的研究实体：多面体。

::: definition 多面体与多胞形
1. **多面体（Polyhedron）**：有限个闭半空间的交集，即 $P = \{x \in \mathbb{R}^n \mid A x \ge b\}$，其中 $A \in \mathbb{R}^{m \times n}$，$b \in \mathbb{R}^m$。
2. **多胞形（Polytope）**：有界的多面体被称为多胞形。即存在有限实数 $M < \infty$，使得 $\forall x \in P$ 均有 $\|x\|_2 \le M$。
:::

```mermaid
flowchart TD
    subgraph Space [欧氏空间 R^n]
        A[半空间 1: a1^T x >= b1]
        B[半空间 2: a2^T x >= b2]
        C[半空间 3: a3^T x >= b3]
        D[半空间 m: am^T x >= bm]
    end
    A & B & C & D -->|有限交集 Intersection| P[凸多面体 Polyhedron P = {x | Ax >= b}]
    P -->|若有界 Bounded| PT[多胞形 Polytope]
    P -->|若无界 Unbounded| PR[包含极射线与极方向 Extreme Rays]
```

在多面体内部，任意两点的连线依然完整保留在集合内部，这种严格的凸性保证了局部最优解必然是全局最优解。

## 2. 极点、顶点与面：几何直觉的严格化

在直观视觉中，二维多边形或三维多面体的“尖角”显然是目标函数最可能取得极值的位置。在数学分析中，这种“尖角”存在三种看似不同但本质等价的形式化定义：

::: definition 极点（Extreme Point）
设 $P$ 为凸集。点 $x \in P$ 称为 $P$ 的**极点**，若不存在两个不同的点 $y, z \in P$（$y \ne z$）以及标量 $\lambda \in (0, 1)$，使得：
$$x = \lambda y + (1 - \lambda) z$$
即极点不能表示为多面体中任意两点的严格凸组合，极点无法位于集合内任何开线段的内部。
:::

::: definition 顶点（Vertex）
点 $x \in P$ 称为 $P$ 的**顶点**，若存在非零向量 $c \in \mathbb{R}^n$，使得 $x$ 是线性目标 $c^T y$ 在 $P$ 上的**唯一最优解**：
$$c^T x < c^T y, \quad \forall y \in P, \; y \ne x$$
:::

::: theorem 极点与顶点的几何等价性
设 $P = \{x \in \mathbb{R}^n \mid A x \ge b\}$ 为多面体，则点 $x \in P$ 是 $P$ 的极点，当且仅当 $x$ 是 $P$ 的顶点。
:::

::: pitfall 紧凸集与多面体的极点差异
注意，这一等价性在多面体（有限个半空间交集）中严格成立。但在一般的紧凸集（如欧氏球 $B = \{x \in \mathbb{R}^n \mid \|x\|_2 \le 1\}$）中，球面上每一个边界点都是极点，也是其法向量支撑超平面的顶点；然而，欧氏球拥有不可数无限个极点，而多面体由于约束矩阵 $A$ 的行数有限，其极点数量必然是**有限的**（至多 $\binom{m}{n}$ 个）。这正是线性规划能够实现有限步终止算法的根本前提！
:::

::: insight 几何直觉与计算复杂度的联结
为什么多面体理论能够支撑起现代工业规模的求解器？
因为有限性。有限个约束决定了极点个数的组合上限。单纯形法之所以能在几何上被形象地描述为“沿着多面体的棱线从一个顶点爬向相邻更优顶点”，正是因为多面体的面（Facets）、棱（Edges）与顶点（Vertices）构成了一个高度刚性的组合网格拓扑。理解多面体的几何结构，是洞穿线性规划内生机理的唯一钥匙。
:::
