---
title: '15.081J 数学规划导论 (Introduction to Mathematical Programming)'
type: course
course: '15.081J 数学规划导论 (Introduction to Mathematical Programming)'
course_id: '15.081J'
tags: [mathematical-programming, linear-programming, duality-theory, interior-point-methods, polyhedral-geometry]
status: complete
source: 'https://ocw.mit.edu/courses/6-251j-introduction-to-mathematical-programming-fall-2009/'
---

# 15.081J 数学规划导论 (Introduction to Mathematical Programming)

> MIT Sloan School of Management & EECS · Operations Research Center · 课号 15.081J / 6.251J · 授课教师：Prof. Dimitris Bertsimas / John Tsitsiklis

## TL;DR

- 麻省理工学院运筹学中心（ORC）与 EECS 旗舰级研究生数学规划理论奠基之作。
- 贯通多面体几何学（魏尔-闵可夫斯基定理、极点与极射线）与代数基本可行解（BFS）。
- 严谨证明强对偶性定理、法卡斯引理（Farkas' Lemma）与互补松弛性（Complementary Slackness）。
- 囊括大规模分布式分解（DW 列生成、Benders 割平面）、椭球法、内点法与 Goemans-Williamson 半正定规划。

## 课程全景与教学大纲

MIT 15.081J（跨院系代码 6.251J）是由世界顶级运筹学家 Dimitris Bertsimas 与 John Tsitsiklis 教授共同打造的经典神作，也是全球顶级优化教科书《Introduction to Linear Optimization》的源头活水。课程以公理化数学证明、几何直觉与现代大规模计算算力为三位一体，系统构建起整个优化科学的理论底座。

全课 25 讲系统化讲义编排如下：

| 讲次 | 讲义主题 (Lecture Topic) | 核心理论、定理与算法突破 | 状态 |
| :--- | :--- | :--- | :---: |
| [Lec 1](lec1.md) | [线性规划建模、分段线性目标与绝对值转化 (Formulations)](lec1.md) | 标准型映射、分段线性凸函数、切比雪夫与 $L_1$ 范数线性化 | Complete |
| [Lec 2](lec2.md) | [多面体几何学基础：超平面、半空间与凸集 (Geometry I)](lec2.md) | 闭半空间有限交集、多面体与多胞形、极点与顶点的几何充要等价 | Complete |
| [Lec 3](lec3.md) | [代数与几何的统一：基本可行解与活动约束 (Geometry II)](lec3.md) | 活动约束子矩阵满秩条件、基本解与基本可行解（BFS）、退化性几何金字塔 | Complete |
| [Lec 4](lec4.md) | [多面体表示定理与极射线分解 (Geometry III: Representation)](lec4.md) | 衰退锥与极方向、魏尔-闵可夫斯基表示定理（Minkowski-Weyl）、线性规划基本定理 | Complete |
| [Lec 5](lec5.md) | [单纯形法 I：邻接极点搜索与检验数向量 (The Simplex Method I)](lec5.md) | 单纯形行进方向、检验数（Reduced Costs）$\\bar{c}_j$、最小比值测试与影子价格 | Complete |
| [Lec 6](lec6.md) | [单纯形法 II：单纯形表更新与两阶段法 (Simplex II: Tableau)](lec6.md) | 高斯-若尔当主元变换、人工变量、两阶段单纯形法（Phase I / Phase II）冷启动 | Complete |
| [Lec 7](lec7.md) | [单纯形法 III：退化性、死循环与 Bland 最小下标防循环法则 (Simplex III)](lec7.md) | 零步长迭代机制、霍夫曼死循环反例、Bland 偏序防循环规则严格有限步收敛证明 | Complete |
| [Lec 8](lec8.md) | [修正单纯形法与大规模稀疏矩阵求逆更新 (Simplex IV: Revised Simplex)](lec8.md) | 惰性计算机制、初等 Eta 矩阵秩一基逆更新、Markowitz LU 三角分解 | Complete |
| [Lec 9](lec9.md) | [对偶理论 I：对偶问题构建、弱对偶性与经济影子价格 (Duality I)](lec9.md) | 对偶下界推导、弱对偶定理（Weak Duality）、对偶间距（Duality Gap）与 SOP 转换 | Complete |
| [Lec 10](lec10.md) | [对偶理论 II：Farkas 引理、分离超平面定理与强对偶性证明 (Duality II)](lec10.md) | 闭凸集严格分离超平面定理、法卡斯引理备选公理、强对偶定理终极证明与四种终局态 | Complete |
| [Lec 11](lec11.md) | [对偶理论 III：互补松弛定理与对偶单纯形法 (Complementary Slackness)](lec11.md) | 互补松弛正交性、Lemke 对偶单纯形法、整数割平面加入后的秒级热启动（Warm Start） | Complete |
| [Lec 12](lec12.md) | [灵敏度分析与参数规划：右端项与目标系数扰动 (Sensitivity Analysis)](lec12.md) | 最优基容许变动范围（Allowable Range）、影子价格有效区间、分段线性参数规划 | Complete |
| [Lec 13](lec13.md) | [鲁棒线性优化：多面体与椭球不确定集对偶等价 (Robust Optimization)](lec13.md) | 传统脆弱性批判、Bertsimas 鲁棒预算模型（Budget of Uncertainty）、二阶锥（SOCP）等价 | Complete |
| [Lec 14](lec14.md) | [大规模优化 I：Dantzig-Wolfe 分解原理与延迟列生成 (Dantzig-Wolfe)](lec14.md) | 块角形结构解耦、完全主规划与受限主规划（RMP）、定价子问题与卷材下料（Cutting-Stock） | Complete |
| [Lec 15](lec15.md) | [大规模优化 II：Benders 分解原理与延迟割平面生成 (Benders Decomposition)](lec15.md) | 变量投影、二阶段混合规划、对偶极点最优性割（Optimality Cut）与极射线可行性割 | Complete |
| [Lec 16](lec16.md) | [网络流规划 I：最小费用流模型与最大流残量网络 (Network Flows I)](lec16.md) | 节点-弧关联矩阵、最大流最小割定理（Max-Flow Min-Cut）、残量网络与增广路径 | Complete |
| [Lec 17](lec17.md) | [网络流规划 II：网络单纯形法与完全单模矩阵 (Network Flows II)](lec17.md) | 完全单模矩阵（TUM）与 Hoffman-Kruskal 纯整数性、支撑树基、环路推流纳秒迭代 | Complete |
| [Lec 18](lec18.md) | [椭球法与多项式时间线性规划复杂度理论 (The Ellipsoid Method)](lec18.md) | Klee-Minty 扭曲超立方体指数反例、哈奇扬椭球法（Khachiyan's Algorithm）多项式收敛 | Complete |
| [Lec 19](lec19.md) | [指数级约束规划与分离神谕等价性 (Problems with Exponentially Many Constraints)](lec19.md) | 分离神谕（Separation Oracle）、GLS 优化与分离多项式等价定理、TSP 子回路最小割判定 | Complete |
| [Lec 20](lec20.md) | [内点法 I：障碍函数法与中心路径几何 (Interior Point Methods I: Central Path)](lec20.md) | 穿透多面体腹地、弗里施对数障碍函数（Log-Barrier）、中心路径（Central Path）解析轨迹 | Complete |
| [Lec 21](lec21.md) | [内点法 II：仿射尺度法与原对偶路径跟踪算法 (Interior Point II: Primal-Dual)](lec21.md) | 坐标归一化、原对偶非线性系统牛顿-拉夫逊更新、梅罗特拉（Mehrotra）预测-校正器 | Complete |
| [Lec 22](lec22.md) | [内点法 III：多项式时间收敛性证明与超线性加速 (Interior Point III)](lec22.md) | 短步路径跟踪法 $\\mathcal{O}(\\sqrt{n} L)$ 证明、涅米洛夫斯基自协调函数（Self-Concordance） | Complete |
| [Lec 23](lec23.md) | [半正定规划与半正定锥松弛：Goemans-Williamson 算法 (Semidefinite Optimization)](lec23.md) | 半正定锥（PSD Cone）与 LMI、GW 算法高维单位向量松弛、0.878 近似比极限随机超平面舍入 | Complete |
| [Lec 24](lec24.md) | [离散优化 I：整数规划建模技巧、大 M 隐患与紧致多面体表述 (IP Formulations)](lec24.md) | 0-1 指示变量逻辑表达、劣质大 M 对松弛下界的致命破坏、理想表述凸包等价 | Complete |
| [Lec 25](lec25.md) | [离散优化 II：分支定界树、割平面法与分支割平面全景 (Branch and Cut)](lec25.md) | 分治与 LP 边界剪枝、Gomory 分数割平面无损切除、分支割平面（Branch and Cut）求解器全景 | Complete |

## 核心方法论与思想沉淀

::: insight 对偶理论是连接物理现实与经济价值的彩虹桥
线性规划不是单纯的求极值代码。原问题（Primal）站在工程师和生产调度者的视角，在设备产能、物料守恒和工人排班的硬物理约束下寻找成本最低方案；而对偶问题（Dual）则站在市场出清者和资本配置者的视角，为每一种稀缺要素寻找最公允的市场影子价格（Shadow Price）。
强对偶定理证明了：**工程师追求极度精益的物理优化，与自由市场对全要素资源的最高理性估值，在数学的终点毫无偏差地完全重合**。这种震撼人心的对称性，是整个现代微观经济学与资源配置科学的灵魂。
:::

::: insight 几何直觉与矩阵稀疏性决定算法命脉
许多学习者往往迷失在单纯形表复杂的初等消元公式中。然而，从多面体的极点、棱线，到支撑树网络流的环路推流，再到内点法在对数引力场中的中心路径滑行，**优化的本质始终是高维流形上的几何探索**。
在现代工业界，掌控了稀疏乔列斯基分解（Sparse Cholesky）、秩一基逆更新与树遍历指针优化的工程师，能够让数百万维的大规模系统在眨眼之间完成出清。这种理论几何高度与底层硬件算力的极致结合，正是 MIT 运筹学享誉全球的底色。
:::

---

本资料整理自 [MIT OpenCourseWare 6.251J / 15.081J Introduction to Mathematical Programming](https://ocw.mit.edu/courses/6-251j-introduction-to-mathematical-programming-fall-2009/)，遵循 Creative Commons BY-NC-SA 4.0 许可协议，仅供个人技术沉淀与知识库研读使用。
