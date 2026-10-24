---
title: '15.084J 非线性规划 (Nonlinear Programming)'
type: course
course: '15.084J 非线性规划 (Nonlinear Programming)'
course_id: '15.084J'
tags: [nonlinear-programming, convex-analysis, kkt-conditions, interior-point-methods, semidefinite-programming]
status: complete
source: 'https://ocw.mit.edu/courses/15-084j-nonlinear-programming-spring-2004/'
---

# 15.084J 非线性规划 (Nonlinear Programming)

> MIT Sloan School of Management & EECS · Operations Research Center · 课号 15.084J / 6.252J · 授课教师：Prof. Robert Freund

## TL;DR

- 麻省理工学院运筹中心（ORC）研究生核心课程，系统构筑连续非线性与凸优化理论大厦。
- 确立无约束与约束最优性公理：微积分驻点、切锥几何、约束规格（LICQ / Slater）与 KKT 条件。
- 涵盖最速下降、阻尼牛顿、增广拉格朗日（ALM）、无投影 Frank-Wolfe 与原对偶内点法。
- 深入拉格朗日弱/强对偶、冯·诺依曼鞍点博弈、次梯度优化与半正定规划（SDP）及 LMI 应用。

## 课程全景与教学大纲

MIT 15.084J（跨院系课号 6.252J）是由国际顶尖优化大师 Robert Freund 教授主讲的研究生高阶旗舰课程。课程跨越了传统非线性规划的狭窄微积分视界，将分析学、微分几何、凸对偶与现代半正定锥优化熔铸为统一的科学范式。

全课 26 讲系统化讲义编排如下：

| 讲次 | 讲义主题 (Lecture Topic) | 核心理论、定理与算法突破 | 状态 |
| :--- | :--- | :--- | :---: |
| [Lec 1](lec1.md) | [无约束优化的一阶与二阶最优性条件 (Unconstrained Optimality)](lec1.md) | 多元泰勒展开、驻点必要条件（FONC）、海森半正定/正定（SONC / SOSC）与鞍点判定 | Complete |
| [Lec 2](lec2.md) | [凸函数的充要特征与凸无约束最优性 (Convex Unconstrained)](lec2.md) | 凸集上图（Epigraph）、一阶支撑切线、二阶海森处处半正定与“局部极小即全局最优” | Complete |
| [Lec 3](lec3.md) | [牛顿法与阻尼步长：二次模型与局部二次收敛 (Newton's Method)](lec3.md) | 仿射不变性、二次收敛阶数（Quadratic Convergence）、Armijo 回溯线搜索与正定修正 | Complete |
| [Lec 4](lec4.md) | [二次型理论与 Rayleigh 商：特征值极值与曲率椭圆 (Quadratic Forms)](lec4.md) | 实对称矩阵谱分解、瑞利商定理（Rayleigh-Ritz）、谱条件数 $\\kappa$ 与长短半轴几何变形 | Complete |
| [Lec 5](lec5.md) | [最速下降梯度法与 Armijo 回溯线搜索 (Steepest Descent)](lec5.md) | 柯西负梯度推导、精确线搜索相邻步 90 度正交之字震荡、Kantorovich 不等式线性收敛界 | Complete |
| [Lec 6](lec6.md) | [约束优化最优性条件 I：切锥几何与 Fritz John 必要条件 (Constrained Optimality I)](lec6.md) | 流形边界切锥（Bouligand Cone）、活动集、Fritz John 定理与目标乘子 $\\mu_0 = 0$ 奇异退化 | Complete |
| [Lec 7](lec7.md) | [约束优化最优性条件 II：KKT 条件与约束规格（LICQ / Slater） (KKT Conditions)](lec7.md) | 线性无关约束规格（LICQ）、Slater 内点、KKT 四大支柱公理与凸规划充要性 | Complete |
| [Lec 8](lec8.md) | [约束优化最优性条件 III：二阶充分必要条件与临界锥曲率 (Constrained Optimality III)](lec8.md) | 临界锥（Critical Cone）子空间、拉格朗日海森正定性（SOSC）、边框海森矩阵测试 | Complete |
| [Lec 9](lec9.md) | [等式约束流形搜索：投影梯度法与仿射投影 (Projection Methods)](lec9.md) | 零空间正交投影矩阵 $P$、幂等性、零空间约化梯度法（Null-Space Approach）消去约束 | Complete |
| [Lec 10](lec10.md) | [外罚函数法与二次惩罚项渐近性态 (Penalty Methods)](lec10.md) | 二次罚项平滑松弛、罚参数 $\\rho \\to \\infty$ 序列收敛定理、海森矩阵条件数爆炸灾难 | Complete |
| [Lec 11](lec11.md) | [增广拉格朗日乘子法与条件数解耦 (Augmented Lagrangian Methods)](lec11.md) | Hestenes-Powell 乘子法、对偶梯度上升更新、有限罚参数超线性收敛与条件数彻底解耦 | Complete |
| [Lec 12](lec12.md) | [内点障碍函数法与 Frank-Wolfe 条件梯度算法 (Barrier Methods & Frank-Wolfe)](lec12.md) | 逆函数与对数势垒、Frank-Wolfe 无投影线性子规划、$\\mathcal{O}(1/k)$ 次线性与极点稀疏表示 | Complete |
| [Lec 13](lec13.md) | [非线性规划前半程核心理论与算法收敛全景对比 (Midterm Synthesis)](lec13.md) | 最优性微积分谱系大一统、一阶/拟牛顿/二阶算法竞技场、工业选型决策漏斗模型 | Complete |
| [Lec 14](lec14.md) | [线性优化内点法 I：仿射几何与解析中心势函数 (IPM for Linear I)](lec14.md) | 多面体解析中心（Analytic Center）、Karmarkar 对数势函数、每步势能常数衰减多项式界 | Complete |
| [Lec 15](lec15.md) | [线性优化内点法 II：原对偶中心路径跟踪与工业实现 (IPM for Linear II)](lec15.md) | 原对偶扰动 KKT 联立牛顿法、正规方程乔列斯基分解、梅罗特拉（Mehrotra）预测-校正器 | Complete |
| [Lec 16](lec16.md) | [凸集几何学：分离超平面、支撑超平面与凸锥极对偶 (Analysis of Convex Sets)](lec16.md) | 闭凸集欧氏投影变分不等式、严格分离定理、边界支撑超平面与凸锥双极定理 | Complete |
| [Lec 17](lec17.md) | [凸函数深度剖析：次梯度、共轭函数与 Fenchel 对偶 (Analysis of Convex Functions)](lec17.md) | 不可微次微分集合 $\\partial f$、极值充要条件 $0 \\in \\partial f$、Fenchel-Legendre 变换与双共轭 | Complete |
| [Lec 18](lec18.md) | [对偶理论 I：拉格朗日对偶函数与弱对偶性 (Duality Theory I: Lagrange Dual)](lec18.md) | 拉格朗日下确界凹函数特性、弱对偶定理（Weak Duality）、对偶间隙与扰动值函数支撑 | Complete |
| [Lec 19](lec19.md) | [对偶理论 II：凸规划 Slater 条件与拉格朗日强对偶定理 (Duality Theory II)](lec19.md) | 严格可行内点假设、分离超平面终极证明强对偶性 $p^* = d^*$ 与对偶最优乘子存在性 | Complete |
| [Lec 20](lec20.md) | [对偶理论 III：极大极小定理与拉格朗日鞍点理论 (Duality Theory III: Saddle Points)](lec20.md) | 双向夹逼鞍点等价性定理、冯·诺依曼极小极大定理（Minimax）、最优化与零和博弈纳什均衡 | Complete |
| [Lec 21](lec21.md) | [对偶理论 IV：广义锥对偶与二阶锥/半正定锥对偶映射 (Duality Theory IV: Conic Duality)](lec21.md) | 固锥广义偏序、对偶锥构建、二阶锥（SOCP）与半正定锥（SDP）自对偶性映射 | Complete |
| [Lec 22](lec22.md) | [广义规划与次梯度优化算法 (Generalized Programming & Subgradient)](lec22.md) | 负次梯度非下降性反例、欧氏距离单调收缩收敛证明、Dantzig 广义线性规划列生成等价 | Complete |
| [Lec 23](lec23.md) | [半正定规划 I：标准型、线性矩阵不等式（LMI）与凸锥几何 (Semidefinite Optimization I)](lec23.md) | 矩阵迹内积与正半定锥、谱面体（Spectrahedron）、舒尔补引理（Schur Complement）降维 | Complete |
| [Lec 24](lec24.md) | [半正定规划 II：SDP 强弱对偶性、隐式退化与非零对偶间距 (Semidefinite Optimization II)](lec24.md) | 迹正半定弱对偶、光滑曲面导致的非零对偶间距反常反例、严格正定 Slater 保护屏障 | Complete |
| [Lec 25](lec25.md) | [半正定规划 III：组合优化多项式松弛与控制理论应用 (Semidefinite Optimization III)](lec25.md) | 布尔二次规划矩阵提升松弛、李雅普诺夫（Lyapunov）系统动力学稳定性 LMI、Lasserre SOS 层级 | Complete |
| [Lec 26](lec26.md) | [非线性规划前沿扩展、流形优化与课程知识大贯通 (Extensions and Wrap-up)](lec26.md) | Stiefel 黎曼流形测地线优化、分布式交替方向乘子法（ADMM）、全课五大理论支柱总决战 | Complete |

## 核心方法论与思想沉淀

::: insight 约束曲率与拉格朗日乘子的力的哲学
在非线性约束优化的宏伟殿堂中，KKT 条件绝不仅仅是枯燥的一阶导数联立方程，而是**牛顿力学平衡原理在多维黎曼流形上的纯净再现**。
目标函数的负梯度 $-\\nabla f$ 犹如引力场的拉拽矢量，而各个活动约束的法向梯度 $\\nabla g_i$ 则是刚性壁面施加的支持反作用力。拉格朗日乘子 $\\mu_i$ 精确刻画了这堵墙为了抵挡质点冲撞所承受的内生压力。互补松弛性宣判了：未受冲撞的自由墙壁其压力恒等于零。掌握了这种几何受力的物理直觉，复杂的代数消元就化为了直观的受力分析。
:::

::: insight 升维转化是征服非线性的最高智慧
初等优化试图在低维空间死磕非凸与非线性，常常在无数局部极小值和马鞍面中折戟沉沙；
而现代凸优化大师展现了完全相反的哲学——**主动升维（Lifting）**。
通过舒尔补引理，我们将二次曲面升维为高维分块矩阵的半正定不等式（LMI）；通过外积提升，我们将 NP 难的图最大割松弛为半正定锥上的单位超球面。高维空间赋予了凸性前所未有的开阔原野，使得看似不可逾越的非线性障碍在凸锥的引力场下迎刃而解。
:::

---

本资料整理自 [MIT OpenCourseWare 15.084J / 6.252J Nonlinear Programming](https://ocw.mit.edu/courses/15-084j-nonlinear-programming-spring-2004/)，遵循 Creative Commons BY-NC-SA 4.0 许可协议，仅供个人技术沉淀与知识库研读使用。
