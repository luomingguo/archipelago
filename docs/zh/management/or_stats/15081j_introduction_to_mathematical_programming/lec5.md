---
title: '单纯形法 I：邻接极点搜索与检验数向量 (The Simplex Method I)'
type: lecture
lecture: 5
tags: [simplex-method, reduced-costs, basis-exchange, optimality-conditions]
status: complete
---

# Lec 5 单纯形法 I：邻接极点搜索与检验数向量 (The Simplex Method I)

> MIT 15.081J / 6.251J 数学规划导论 · 讲义 5 · 授课教师：Prof. Dimitris Bertsimas / John Tsitsiklis

## TL;DR

- 单纯形法的核心机制是沿多面体棱线在相邻基本可行解（BFS）之间做贪心迭代。
- 检验数（Reduced Cost）$\bar{c}_j$ 严格度量了引入非基变量 $x_j$ 对目标函数的边际改善率。
- 进基变量选择负检验数，出基变量遵循最小比值测试（Minimum Ratio Test）保障可行性。

## 1. 相邻基本可行解与单纯形行进方向

单纯形法（Simplex Algorithm）由乔治·丹齐格（George Dantzig）于 1947 年提出，被誉为 20 世纪对人类工商业文明影响最深远的十大算法之一。其核心几何直觉极其优美：**从多面体的一个顶点出发，若当前顶点不是最优解，则沿着一条目标函数下降最快的棱线行进到相邻的顶点；重复该过程，直至无法继续下降为止**。

设当前基本可行解由基指标集 $B = (B(1), \dots, B(m))$ 确定，当前解为：
$$x_B = B^{-1} b \ge 0, \quad x_N = 0$$

现在我们希望让某个非基变量 $x_j$（$j \in N$）从 0 增加到一个正数 $\theta > 0$（**进基 Entering**），同时保持所有其他非基变量为 0：$x_k = 0$（$\forall k \ne j, k \in N$）。

为了始终满足等式约束 $A x = b$，基变量必须同步联动：
$$A_B x_B + A_j x_j = b \implies x_B = B^{-1} b - B^{-1} A_j \theta = x_B^* - d_B \theta$$
其中 $d_B = B^{-1} A_j$ 称为**第 $j$ 个单纯形方向在基分量上的投影**。

```mermaid
flowchart LR
    A[当前顶点 x_B = B^-1 b] -->|选择负检验数 cbar_j < 0| B[确定单纯形搜索方向 d = -B^-1 Aj]
    B -->|最小比值测试 theta* = min x_Bi / di| C[保持非负约束 x >= 0]
    C -->|出基变量 x_l 降至 0| D[到达更优相邻顶点 x_new]
    D -->|所有检验数 cbar >= 0| E[收敛至全局最优解]
```

## 2. 检验数（Reduced Cost）与最优性条件

当非基变量 $x_j$ 增加 $\theta$ 时，全局目标函数 $z = c^T x = c_B^T x_B + c_j x_j$ 会发生怎样的变化？

$$\begin{aligned}
z(\theta) &= c_B^T (x_B^* - \theta B^{-1} A_j) + c_j \theta \\
&= c_B^T x_B^* + \theta \left( c_j - c_B^T B^{-1} A_j \right) \\
&= z^* + \theta \cdot \bar{c}_j
\end{aligned}$$

::: definition 检验数（Reduced Cost）
对于任意变量 $j \in \{1,\dots,n\}$，其检验数 $\bar{c}_j$ 定义为：
$$\bar{c}_j = c_j - c_B^T B^{-1} A_j = c_j - p^T A_j$$
其中 $p^T = c_B^T B^{-1}$ 被称为单纯形乘子向量（Simplex Multipliers），也是后续对偶理论中的对偶变量。
对于所有基变量 $j \in B$，易见 $B^{-1} A_B = I$，故其检验数恒等于 0：$\bar{c}_B = 0$。
:::

::: theorem 单纯形最优性充分条件
设 $x^*$ 为对应基矩阵 $B$ 的基本可行解。若对于所有非基变量 $j \in N$，检验数均非负：
$$\bar{c}_j \ge 0, \quad \forall j \in N$$
则 $x^*$ 是该线性规划的**全局最优解**。
:::

如果某个 $\bar{c}_j < 0$，说明增加 $x_j$（即 $\theta > 0$）将严格使目标函数下降！这就是算法继续前进的指令。

## 3. 步长确定与最小比值测试（Minimum Ratio Test）

既然选择了一个 $\bar{c}_j < 0$ 的变量进基，我们能让 $\theta$ 无限增加吗？
不行！因为基变量必须满足非负性约束：
$$x_{B(i)}(\theta) = x_{B(i)}^* - \theta (B^{-1} A_j)_i \ge 0, \quad \forall i = 1, \dots, m$$

定义向量 $u = B^{-1} A_j$：
1. 若对所有 $i$，均有 $u_i \le 0$，则不论 $\theta$ 增加多大，$x_B(\theta)$ 都只会增加或不变，永远非负！此时目标函数可以趋向 $-\infty$，**算法终止，判定问题无界（Unbounded）**。
2. 若存在某些分量 $u_i > 0$，则当 $\theta$ 增大时，对应的基变量在递减。为了保证非负，步长上限由第一个触碰到零边界的变量严格锁定：

::: definition 最小比值测试（Minimum Ratio Rule）
最优进基步长 $\theta^*$ 为：
$$\theta^* = \min_{\{i \mid u_i > 0\}} \frac{x_{B(i)}^*}{u_i}$$
设取得最小值的索引为 $l$（即 $\theta^* = x_{B(l)}^* / u_l$），则对应的变量 $x_{B(l)}$ 降为 0，该变量被移出基矩阵（**出基 Leaving**），非基变量 $x_j$ 进入基矩阵接替其位置。
:::

::: insight 检验数即对偶影子价格过滤网
很多工程人员机械地背诵 $\bar{c}_j = c_j - c_B^T B^{-1} A_j$，却不明白其深刻的经济学本质。
$A_j$ 是生产一单位产品 $j$ 所需消耗的 $m$ 种资源配额向量；$p^T = c_B^T B^{-1}$ 是这 $m$ 种资源在当前生产计划下的边际影子价值（Shadow Prices）。
因此，$p^T A_j$ 是把资源挪去生产产品 $j$ 所放弃的机会成本（Opportunity Cost）！
$\bar{c}_j = c_j - p^T A_j$ 正是“名义成本”减去“机会成本”。只有当消耗资源的机会成本比生产该产品本身的收益更有吸引力（净收益大于 0，即极小化下 $\bar{c}_j < 0$）时，重配生产线才是理性的。单纯形法每一步都在模拟最纯粹的市场边际均衡！
:::
