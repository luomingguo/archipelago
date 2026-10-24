---
title: '15.066J 制造与运营系统优化分析 (System Optimization and Analysis for Manufacturing)'
type: course
course: '15.066J 制造与运营系统优化分析 (System Optimization and Analysis for Manufacturing)'
course_id: '15.066J'
tags: [manufacturing-systems, operations-research, supply-chain, discrete-event-simulation, queueing-theory]
status: complete
source: 'https://ocw.mit.edu/courses/15-066j-system-optimization-and-analysis-for-manufacturing-summer-2003/'
---

# 15.066J 制造与运营系统优化分析 (System Optimization and Analysis for Manufacturing)

> MIT Sloan School of Management & Leaders for Global Operations (LGO) · 课号 15.066J / 2.890J · 授课教师：Prof. Stephen Graves

## TL;DR

- 麻省理工学院斯隆管理学院与工学院 LGO 全球运营领袖旗舰硕士课，融汇确定性数学规划、随机动态优化与离散事件仿真三位一体。
- 奠定现代生产运营与供应链骨架：线性规划产品组合、多周期综合生产计划、网络流与多商品流运输协同。
- 深入离散组合与排程前沿：装配线平衡、车间作业调度（Job Shop）、分支割平面与元启发式邻域搜索（LNS）。
- 攻克真实系统不确定性：牛鞭效应与多级安全库存（Base-Stock）、二阶段随机补偿规划（EVPI & VSS）、英特尔芯片良率与分选降级（Down-Binning）。
- 掌握先进数字孪生与仿真分析：离散事件时间推进（DES / SIMUL8）、约束理论（TOC / DBR）、正交实验设计（DOE / ANOVA）、高斯过程代理模型（Kriging）与非线性规划（NLP / KKT）。

## 课程全景与教学大纲

MIT 15.066J（跨院系机械工程代码 2.890J）由麻省理工学院运筹学与制造系统权威 Stephen Graves 教授倾力打造。课程将严谨的运筹学公理体系与福特汽车、英特尔、波音等世界顶尖工业巨头的实战案例紧密咬合，为现代智能制造系统奠定坚固的量化基石。

全课 24 讲系统化讲义编排如下：

| 讲次 | 讲义主题 (Lecture Topic) | 核心理论、定理与工业实践突破 | 状态 |
| :--- | :--- | :--- | :---: |
| [Lec 1](lec1.md) | [制造与运营系统优化概论与决策架构 (Manufacturing Systems Overview)](lec1.md) | 层级化决策金字塔、利特尔法则（WIP = TH × CT）、运筹规划与仿真决策矩阵 | Complete |
| [Lec 2](lec2.md) | [线性规划在运营决策中的建模艺术与几何基础 (LP Formulations & Geometry)](lec2.md) | 制造资源分配标准型、松弛变量物理含义、多面体极点与基可行解基本定理 | Complete |
| [Lec 3](lec3.md) | [线性规划应用与案例研究：复杂运营约束转化 (LP Applications & Cases)](lec3.md) | 多周期动态综合生产计划、物料流平衡方程、流程混料分式不等式线性化 | Complete |
| [Lec 4](lec4.md) | [物流网络流模型与多商品流架构 (Network Flow Models in Logistics)](lec4.md) | 最小费用流模型、节点-弧关联矩阵完全单模性（TUM）、多商品流共享运力耦合 | Complete |
| [Lec 5](lec5.md) | [生产物流协同与多工厂运输优化 (Multi-Commodity Flows & Transportation)](lec5.md) | 经典 Monge-Kantorovich 运输问题、互补松弛与影子价格、Benders 分解主子问题协同 | Complete |
| [Lec 6](lec6.md) | [工业实践案例：汽车总装与复杂生产规划 (Industrial LP: Ford Assembly)](lec6.md) | 福特汽车混流流水线、工位节拍（Takt Time）防漂移越界约束、选装率平准化配置 | Complete |
| [Lec 7](lec7.md) | [LP 求解方法、对偶影子价格与灵敏度分析 (LP Methods & Sensitivity)](lec7.md) | 对偶理论经济学内涵、容许变动范围、全要素内部转移公允定价、100% 规则 | Complete |
| [Lec 8](lec8.md) | [整数规划在设施选址与生产平衡中的建模技术 (Integer Programming & Location)](lec8.md) | 0-1 离散变量逻辑表达、劣质大 M 陷阱与紧致多面体表述、装配线平衡与对称性破缺 | Complete |
| [Lec 9](lec9.md) | [整数规划核心求解算法：分支定界与割平面全景 (IP Algorithms & Branch-and-Cut)](lec9.md) | 分支定界树三类剪枝法则、Gomory 分数割平面推导、分支割平面（Branch-and-Cut）引擎 | Complete |
| [Lec 10](lec10.md) | [组合启发式算法与车间作业调度优化 (Combinatorial Heuristics & Scheduling)](lec10.md) | Job Shop 复杂度深渊、SPT/EDD/CR 优先派遣规则、析取图模型与禁忌/大邻域搜索 | Complete |
| [Lec 11](lec11.md) | [多级供应链库存模拟与基本库存策略 (Inventory Simulation & Base-Stock)](lec11.md) | 啤酒游戏与牛鞭效应系统动力学、基本库存目标公式、Eppen-Martin 提前期方差放大 | Complete |
| [Lec 12](lec12.md) | [随机线性规划与二阶段补偿模型 (Stochastic LP & Recourse Models)](lec12.md) | 詹森不等式与平均值缺陷定律、情景树与确定性等价规划（DEP）、EVPI 与 VSS 价值度量 | Complete |
| [Lec 13](lec13.md) | [英特尔芯片制造案例：良率波动与产能分配 (Intel Semiconductor Capacity)](lec13.md) | 12周漫长投片周期、晶圆测积分选（Speed Binning）、降级柔性套利（Down-Binning） | Complete |
| [Lec 14](lec14.md) | [随机建模与仿真过程基础架构 (Simulation Foundations & Stochastic Modeling)](lec14.md) | 线性同余随机数生成、逆变换采样定理公理证明、离散事件时间推进、置信区间评估 | Complete |
| [Lec 15](lec15.md) | [蒙特卡洛仿真与风险量化分析实战 (Monte Carlo Simulation & Risk)](lec15.md) | Crystal Ball / @RISK 实战、敏感度龙卷风分析、风险价值（VaR）与条件风险价值（CVaR） | Complete |
| [Lec 16](lec16.md) | [供应链分销战略与门户枢纽案例分析 (Ontario Gateway Case Discussion)](lec16.md) | 安大略门户战略、越库配送（Cross-Docking）零库存运转、月台门位指派二次规划 | Complete |
| [Lec 17](lec17.md) | [离散事件仿真框架与 SIMUL8 动态建模 (Discrete-Event Simulation & SIMUL8)](lec17.md) | 实体-资源-队列三元组、下一事件时间推进动力学、有限缓冲级联阻塞与饥饿雪崩 | Complete |
| [Lec 18](lec18.md) | [约束理论 (TOC)、瓶颈调度与 DBR 控制机制 (Theory of Constraints & DBR)](lec18.md) | 五大聚焦步骤、鼓-缓冲-绳（DBR）物料拉动机制、有效产出会计破除虚假费用分摊 | Complete |
| [Lec 19](lec19.md) | [离散制造产线平衡与排队网络案例研讨 (Line Balancing & Queuing Case)](lec19.md) | 线平衡率与平滑系数、Jackson 开环排队网络乘积解定理、返工回路与漂移瓶颈治理 | Complete |
| [Lec 20](lec20.md) | [仿真输出统计分析与实验设计 (DOE and Simulation Output Analysis)](lec20.md) | 初始瞬态偏差与 Welch 预热期平滑截断、2^k 全因子正交实验设计、方差分析（ANOVA） | Complete |
| [Lec 21](lec21.md) | [基于仿真的优化方法与响应曲面代理模型 (Simulation-Based Optimization)](lec21.md) | 黑箱优化困境、响应曲面法（RSM）最速上升法、高斯过程克里金（Kriging）代理模型 | Complete |
| [Lec 22](lec22.md) | [流程工程中的非线性规划建模：能效与产率优化 (NLP Formulations)](lec22.md) | 换热器网络综合（HEN）、对数平均温差（LMTD）、双线性乘积项与非凸多局部极值陷阱 | Complete |
| [Lec 23](lec23.md) | [非线性规划算法、KKT 最优性条件与对偶理论 (NLP Algorithms & KKT Conditions)](lec23.md) | KKT 一阶平稳性与互补松弛充要条件、序列二次规划（SQP）、原对偶内点中心路径法 | Complete |
| [Lec 24](lec24.md) | [制造系统综合集成与工程实践总结 (Integrated Manufacturing Systems Capstone)](lec24.md) | 闭环三层中枢架构、跨越模型与现实的四大工程鸿沟、工业 4.0 数字孪生全景落地 | Complete |

## 核心方法论与思想沉淀

::: insight 制造系统工程是运筹学在物质世界中最雄浑的交响曲
运筹学诞生于二战的雷达雷区部署，而在和平时代的现代制造业中找到了最壮丽的安身之所。
制造不是孤立的机械加工，而是一条动态流淌的物理与信息价值长河。
- **线性规划为我们锚定了资源最优配置的极点航道**；
- **随机规划与库存理论为我们打造了穿越需求不确定风暴的稳固护甲**；
- **离散事件仿真为我们提供了在计算机硅基空间试错演练三十年的全息沙盘**；
- **约束理论与非线性算法让我们洞悉了系统复杂因果律中最具杠杆效应的命门**。
掌握这套方法论的工程师，不再仅仅是车间生产线旁的技术工人，而是驾驭全球实体经济千亿资产流转的卓越工业系统架构师。
:::
