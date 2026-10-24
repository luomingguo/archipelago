---
title: '15.083 整数规划与组合优化 (Integer Programming and Combinatorial Optimization)'
type: course
course: '15.083 整数规划与组合优化 (Integer Programming and Combinatorial Optimization)'
course_id: '15.083'
tags: [integer-programming, combinatorial-optimization, cutting-planes, branch-and-bound, polyhedral-combinatorics]
status: complete
source: 'https://ocw.mit.edu/courses/15-083j-integer-programming-and-combinatorial-optimization-fall-2009/'
---

# 15.083 整数规划与组合优化 (Integer Programming and Combinatorial Optimization)

> MIT Sloan School of Management & Operations Research Center · 课号 15.083 / 6.859 · 授课教师：Prof. Dimitris Bertsimas

## TL;DR

- 麻省理工学院运筹学中心（ORC）高阶离散优化博士核心课，全面涵盖整数规划与组合优化的理论、几何、代数与算法。
- 奠定凸包理想表述理论基石：完全单模矩阵（TUM）、全对偶整性（TDI）与 Edmonds 匹配多面体。
- 深入次可加对偶理论、拉格朗日松弛（Held-Karp TSP 算法）、次梯度与束方法、及离散鲁棒优化。
- 贯穿格论（Lattices, LLL 算法与 Lenstra 固定维度多项式算法）、代数几何（Gröbner 基与 Barvinok 计数）前沿。
- 掌握现代 MIP 求解器核心引擎：Chvátal-Gomory 割、MIR 割、裂项割、分支定界、启发式（Feasibility Pump / RINS）、近似算法与分支割平面列定价（Branch-Cut-and-Price）。

## 课程全景与教学大纲

MIT 15.083J 由国际著名运筹学家 Dimitris Bertsimas 教授主讲，系统梳理了从多面体组合学、代数与几何、对偶与松弛，到前沿大规模离散算法（Benders 分解、列生成、分支割平面）的完整理论大厦。

全课 25 讲讲义编排如下：

| 讲次 | 讲义主题 (Lecture Topic) | 核心理论、定理与算法突破 | 状态 |
| :--- | :--- | :--- | :---: |
| [Lec 1](lec1.md) | [离散优化建模艺术与大 M 法则陷阱 (Formulations)](lec1.md) | 0-1 决策变量逻辑转换、劣质大 M 陷阱、紧致凸包多面体表述 | Complete |
| [Lec 2](lec2.md) | [计算复杂性理论与多项式时间归约 (Complexity)](lec2.md) | P/NP/NP-Complete 分级、Cook-Levin 定理、SAT 与离散规划图灵规约 | Complete |
| [Lec 3](lec3.md) | [多面体表述增强方法 I：覆盖割与背包多面体 (Enhance Formulations I)](lec3.md) | 背包多面体（Knapsack Polyhedron）、极小覆盖不等式（Minimal Cover Cuts）、序列提升（Sequential Lifting） | Complete |
| [Lec 4](lec4.md) | [多面体表述增强方法 II：析取规划与多面体投影 (Enhance Formulations II)](lec4.md) | 析取规划（Disjunctive Programming）、巴拉斯定理（Balas Theorem）、傅里叶-莫茨金变量投影消除 | Complete |
| [Lec 5](lec5.md) | [理想表述理论 I：完全单模矩阵与 Hoffman-Kruskal 定理 (Ideal Formulations I)](lec5.md) | 完全单模矩阵（TUM）、全幺模充要条件、二分图匹配与网络流的天然纯整数性 | Complete |
| [Lec 6](lec6.md) | [理想表述理论 II：全对偶整性 (TDI) 与最小割最大流 (Ideal Formulations II)](lec6.md) | 全对偶整性（Totally Dual Integral, TDI）、Edmonds-Giles 框架、对偶多面体极点整数性 | Complete |
| [Lec 7](lec7.md) | [理想表述理论 III：一般图 Edmonds 匹配多面体与开花算法 (Ideal Formulations III)](lec7.md) | 奇圈约束剖析、埃德蒙兹开花（Blossom）多面体、多项式判定强分离神谕 | Complete |
| [Lec 8](lec8.md) | [整数规划对偶理论与次可加对偶 (Superadditive Duality)](lec8.md) | 强对偶失效与对偶间距、次可加值函数（Superadditive Functions）、值函数极小化对偶全景 | Complete |
| [Lec 9](lec9.md) | [拉格朗日松弛理论与 Held-Karp TSP 算法 (Lagrangian Relaxation)](lec9.md) | 复杂约束罚分、拉格朗日对偶函数凹性、Held-Karp 1-Tree 最小生成树紧致下界 | Complete |
| [Lec 10](lec10.md) | [松弛求解算法：次梯度优化与束方法 (Subgradient Optimization and Bundle Methods)](lec10.md) | 非光滑对偶优化、Polyak 次梯度步长准则、近端项稳定化束方法（Bundle Methods） | Complete |
| [Lec 11](lec11.md) | [鲁棒离散优化：Bertsimas-Sim 预算不确定模型 (Robust Discrete Optimization)](lec11.md) | 离散参数扰动脆弱性、预算不确定集 $\Gamma$、非线性鲁棒对偶转化保留 MIP 结构 | Complete |
| [Lec 12](lec12.md) | [格理论基础 I：格点、基底、行列式与格基规约 LLL 算法 (Lattices I)](lec12.md) | 格几何（Lattices）、Gram-Schmidt 正交化、Lenstra-Lenstra-Lovász (LLL) 多项式规约 | Complete |
| [Lec 13](lec13.md) | [格理论基础 II：Lenstra 固定维度整数规划多项式算法 (Lattices II)](lec13.md) | 椭球拉伸变换、极窄宽度方向搜索、固定维度 $n$ 下 $\mathcal{O}(2^{\mathcal{O}(n^3)})$ 多项式定理 | Complete |
| [Lec 14](lec14.md) | [代数几何应用 I：希尔伯特基与多项式环 Gröbner 基 (Algebraic Geometry I)](lec14.md) | 希尔伯特有限基底定理、单项式偏序（Lex/G-Lex）、Buchberger Gröbner 基规约测试 | Complete |
| [Lec 15](lec15.md) | [代数几何应用 II：有理生成函数与 Barvinok 格点计数 (Algebraic Geometry II)](lec15.md) | 多面体锥多项式编码、单形圆锥锥化分解、Barvinok 多项式时间纯整数格点精准计数 | Complete |
| [Lec 16](lec16.md) | [多面体割平面几何：Chvátal-Gomory 闭包与有限性 (Chvátal-Gomory Closure)](lec16.md) | 严格支撑超平面取整、一阶 CG 闭包、Schrijver 纯有理多面体有限 CG 秩收敛定理 | Complete |
| [Lec 17](lec17.md) | [割平面法 I：Gomory 分数割与纯整数割平面算法 (Cutting Planes I)](lec17.md) | 最优单纯形表行生成、分数部分四舍五入、对偶单纯形法有限步终止收敛证明 | Complete |
| [Lec 18](lec18.md) | [割平面法 II：混合整数舍入 (MIR) 割与裂项割 (Cutting Planes II)](lec18.md) | 混合变量离散断点、MIR 基础函数性质、Split Disjunction 等价性与一般分离技术 | Complete |
| [Lec 19](lec19.md) | [枚举法与分支定界树：搜索策略、分支策略与剪枝 (Enumerative Methods)](lec19.md) | 树形分支搜索、强分支（Strong Branching）伪费用评估、双边上下界主动剪枝 | Complete |
| [Lec 20](lec20.md) | [原问题启发式算法：可行性泵 (Feasibility Pump) 与局部搜索 (Heuristics)](lec20.md) | LP 投影与取整交替迭代、近邻启发式搜索（RINS）、大邻域搜索（LNS）优质解速成 | Complete |
| [Lec 21](lec21.md) | [近似算法 I：贪心算法、拟阵与背包多项式近似模式 FPTAS (Approximation I)](lec21.md) | 近似比 $\alpha$ 定义、独立集拟阵贪心最优性、DP 状态空间放缩 $1+\epsilon$ 近似 | Complete |
| [Lec 22](lec22.md) | [近似算法 II：顶点覆盖与无约束设施选址原对偶算法 (Approximation II)](lec22.md) | LP 松弛取整分析、原对偶增广路径驱动松弛互补条件、2-近似极限因果分析 | Complete |
| [Lec 23](lec23.md) | [近似算法 III：旅行商问题 (TSP) Christofides 3/2 近似与割平面法 (Approximation III)](lec23.md) | 度量空间三角不等式、MST + 奇度数点最小权完美匹配、欧拉回路与短路跳跃比值严格保证 | Complete |
| [Lec 24](lec24.md) | [混合整数规划大规模分解：逻辑 Benders 分解 (Mixed Integer Optimization I)](lec24.md) | 离散主问题与连续子问题、极点最优性割与极射线可行性割、割平面热启动协同 | Complete |
| [Lec 25](lec25.md) | [混合整数规划统一框架：分支割平面与列生成算法 (Mixed Integer Optimization II)](lec25.md) | 树节点动态加入有效不等式、受限主规划定价子问题延时生成、Branch-Cut-and-Price 全景架构 | Complete |

## 核心方法论与思想沉淀

::: insight 凸包是整数世界的终极几何投影
整数规划的困难，源于离散格点构成的可行域打破了微积分与凸分析的连续平滑性。人类求解离散问题的所有理论突破，本质上都在做同一件事：**在不丢失离散整数点的前提下，通过寻找最紧致的半空间约束，将离散可行域逼近为其凸包（Convex Hull）**。从 Edmonds 奇圈开花、Chvátal-Gomory 割到 MIR 割，每一个精妙的有效不等式，都是切去连续松弛虚假空间、直抵整数本质的手术刀。
:::
