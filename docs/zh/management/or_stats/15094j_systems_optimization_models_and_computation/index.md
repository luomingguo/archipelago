---
title: '15.094J 鲁棒系统优化建模与计算 (Systems Optimization: Models and Computation)'
type: course
course: '15.094J 鲁棒系统优化建模与计算 (Systems Optimization: Models and Computation)'
course_id: '15.094J'
tags: [robust-optimization, large-scale-optimization, semidefinite-programming, column-generation, benders-decomposition]
status: complete
source: 'https://ocw.mit.edu/courses/15-094j-systems-optimization-models-and-computation-sma-5223-spring-2004/'
---

# 15.094J 鲁棒系统优化建模与计算 (Systems Optimization: Models and Computation)

> MIT Sloan School of Management & Operations Research Center · 课号 15.094J / SMA 5223 · 授课教师：Prof. Dimitris Bertsimas / Robert Freund

## TL;DR

- 麻省理工学院运筹学中心（ORC）与新加坡-MIT 联盟（SMA）旗舰研究生大规模系统优化与前沿计算理论奠基课。
- 奠定大规模计算与前沿工业建模基石：放射治疗逆向剂量规划（IMRT）、修正单纯形稀疏 LU 分解、拉格朗日松弛与次梯度、电信 VPN 可靠拓扑嵌入。
- 深入分布式与结构化分解核心：Dantzig-Wolfe 列生成原理、随机运输-库存联合设计（LIRP）、混合整数有效不等式与 Benders 分解。
- 贯通机器学习与凸二次规划前沿：支持向量机（SVM）、软间隔与 Mercer 核方法、大规模二次规划（有效集法与 SMO 算法）、电商收益管理与自适应联合分析（ACA）。
- 掌握前沿高阶锥优化与鲁棒抗震大厦：桁架结构力学拓扑凸规划、空间分支定界（sBB / McCormick 包络）、多阶段随机规划（L-Shaped）、Bertsimas 预算不确定集鲁棒对等体、半正定规划（SDP / LMIs）、桁架防共振固有频率调节与 Wardrop 交通平衡拥塞收费。

## 课程全景与教学大纲

MIT 15.094J（跨国联合代码 SMA 5223）由世界顶级运筹优化泰斗 Dimitris Bertsimas 教授与 Robert Freund 教授联合主讲。课程横跨医疗物理、电信网络、智能制造、模式识别、结构力学与交通控制六大现实工业重镇，系统构筑起大规模数学规划与鲁棒计算的完整科学范式。

全课 24 讲讲义编排如下：

| 讲次 | 讲义主题 (Lecture Topic) | 核心理论、定理与系统计算突破 | 状态 |
| :--- | :--- | :--- | :---: |
| [Lec 1](lec1.md) | [放射治疗中的优化建模与计算前沿 (Radiation Therapy Optimization)](lec1.md) | 调强放疗（IMRT）逆向剂量投影规划、体素-微束元矩阵稀疏化、剂量容积直方图（DVH）凸二次转化 | Complete |
| [Lec 2](lec2.md) | [单纯形法的大规模计算加速与稀疏基逆更新 (Simplex Computational Updates)](lec2.md) | 修正单纯形法惰性计算、BTRAN/FTRAN 方程求解、乘积型基逆（PFI）与 Forrest-Tomlin 稀疏 LU 更新 | Complete |
| [Lec 3](lec3.md) | [应用拉格朗日对偶与约束松弛技术 (Applied Lagrange Duality & Relaxation)](lec3.md) | 复杂耦合约束价格惩罚、弱对偶定理万能下界保证、非光滑凹函数与 Polyak 步长次梯度优化 | Complete |
| [Lec 4](lec4.md) | [系统优化软件架构与计算实践例程 (Optimization Software Architecture)](lec4.md) | 现代代数建模系统（AML）解耦架构、CSC/CSR 稀疏矩阵布局、懒惰约束与启发式用户回调机制 | Complete |
| [Lec 5](lec5.md) | [电信网络拓扑设计：最低成本可靠 VPN 嵌入 (Minimum-Cost VPN Embeddings)](lec5.md) | 软管模型（Hose Model）多面体不确定流量集、树形路由拓扑设计、有向割集与多项式分离 | Complete |
| [Lec 6](lec6.md) | [大规模列生成算法基础与 Dantzig-Wolfe 分解原理 (Column Generation Foundations)](lec6.md) | 变量数超越宇宙粒子总数挑战、受限主规划（RMP）对偶定价子问题、Gilmore-Gomory 卷材下料 | Complete |
| [Lec 7](lec7.md) | [列生成进阶应用：随机运输-库存联合网络设计 (Stochastic Network Design)](lec7.md) | 选址-库存-路由联合（LIRP）、平方根安全库存非线性解耦、Shu-Shen-Teo 集合划分模式列生成 | Complete |
| [Lec 8](lec8.md) | [大规模整数规划与有效不等式生成 (Large-Scale IP & Valid Inequalities)](lec8.md) | 凸包面不等式、极小背包覆盖割与序列提升、MIR 割、GLS 优化与分离多项式时间等价定理 | Complete |
| [Lec 9](lec9.md) | [凸约束优化基础与几何分离超平面定理 (Convex Constrained Optimization)](lec9.md) | 局部最优即全局最优分水岭、Hilbert 闭凸集正交投影定理、严格分离超平面与次梯度支持平面 | Complete |
| [Lec 10](lec10.md) | [供应链分销系统规划与多级选址模型 (Facility Location & Systems)](lec10.md) | 强表述与弱表述多面体松弛下界对决、轴辐式网络（Hub-and-Spoke）设计与规模经济转运折让 | Complete |
| [Lec 11](lec11.md) | [大型货运网络加载与双挂车匹配优化 (Network Loading and Pup Matching)](lec11.md) | 公路货运整车阶梯加载、双挂短车（Pup Matching）中转合体套利、Edmonds 开花匹配算法 | Complete |
| [Lec 12](lec12.md) | [模式分类与线性可分支持向量机 (Linearly Separable SVMs)](lec12.md) | 最大几何间隔原理、凸二次规划标准型转化、KKT 互补松弛性与支持向量（Support Vectors）诞生 | Complete |
| [Lec 13](lec13.md) | [模式分类与二次规划：软间隔与对偶核映射 (Soft-Margin SVM & Kernels)](lec13.md) | 松弛变量容忍噪声、Wolfe 对偶盒式约束二次规划、Mercer 定理与无限维 RKHS 高斯核技巧 | Complete |
| [Lec 14](lec14.md) | [大规模二次优化求解算法：有效集与原对偶内点法 (Large-Scale QP Methods)](lec14.md) | 全稠密核矩阵内存瓶颈、有效集工作集切换、原对偶内点中心路径法、Platt 序列最小优化（SMO） | Complete |
| [Lec 15](lec15.md) | [电子商务中的动态定价与收益管理优化 (Dynamic Pricing & Revenue Management)](lec15.md) | HJB 动态规划值函数、库存边际机会成本、网络 DLP 影子价格准入控制、多项 Logit 选品组合 | Complete |
| [Lec 16](lec16.md) | [解析中心、牛顿法与自适应联合分析 (Analytic Center, Newton's Method & ACA)](lec16.md) | 对数障碍函数最大容积中心、Nesterov 自协调函数牛顿法二次收敛、基于 Web 的交互效用挖掘 | Complete |
| [Lec 17](lec17.md) | [结构力学拓扑优化：桁架设计与凸规划模型 (Structural Optimization: Truss)](lec17.md) | 弹性胡克定律与刚度矩阵、柔度极小化（Compliance）、对偶余能原理与纯线性规划等价性 | Complete |
| [Lec 18](lec18.md) | [非凸优化挑战与全局优化空间分支定界 (Non-Convex Optimization & Bounds)](lec18.md) | 双线性乘积项 McCormick 凸凹包络、空间分支定界（sBB）连续长方体剖分、OBBT 边界收紧技术 | Complete |
| [Lec 19](lec19.md) | [随机线性优化与多阶段情景树补偿模型 (Stochastic LP & Scenario Recourse)](lec19.md) | 多阶段情景树信息流拓扑、非预知性约束（Non-Anticipativity）、L-Shaped 并行子问题割平面 | Complete |
| [Lec 20](lec20.md) | [不确定性优化前沿：鲁棒对等体与不确定集合 (Robust Optimization)](lec20.md) | 概率分布拟合脆弱性、盒式/椭球不确定集、Bertsimas 预算不确定集 $\Gamma$ 纯线性对偶无损转化 | Complete |
| [Lec 21](lec21.md) | [Benders 分解算法在结构化大规模规划中的工程实践 (Benders Decomposition)](lec21.md) | 变量投影哲学、极点最优性割与极射线可行性割、Magnanti-Wong 帕累托最优割彻底消灭慢收敛 | Complete |
| [Lec 22](lec22.md) | [半正定规划与线性矩阵不等式前沿基础 (Introduction to SDP and LMIs)](lec22.md) | 对称矩阵正半定锥 $\mathbb{S}_+^n$、Schur 补引理与二次约束 LMI 凸转化、对数行列式障碍内点法 | Complete |
| [Lec 23](lec23.md) | [桁架结构动力学：基于 SDP 的固有频率优化 (Truss Natural Frequency via SDP)](lec23.md) | 避免共振破坏、Rayleigh 商广义特征值极小化、质量刚度比值充要转化为单一全局 LMI 约束 | Complete |
| [Lec 24](lec24.md) | [交通流平衡、Wardrop 原则与拥塞收费优化 (Traffic Equilibrium & Congestion)](lec24.md) | Wardrop 用户均衡（UE）纳什博弈、Beckmann 积分凸势函数规划、庇古边际拥塞收费消解布雷斯悖论 | Complete |

## 核心方法论与思想沉淀

::: insight 鲁棒系统优化是人类用数学理性对抗无常宇宙的终极盾牌
在工程、医学、商业与交通的交汇处，现实系统永远充满着惊涛骇浪：
参数在漂移、机器在损坏、患者在呼吸、司机在博弈、市场在波动。
15.094J 向世人展现了一套极其崇高的科学世界观：
- **从不确定性中提纯确定性**：无论是通过 McCormick 凸包络封印非凸深渊，还是通过 Bertsimas 预算不确定集抵御黑天鹅；
- **从离散裂痕中构筑连续凸包**：无论是 Edmonds 奇圈开花，还是半正定矩阵锥的光滑飞跃；
- **从微观自私中引导宏观崇高**：无论是拉格朗日内部影子价格，还是庇古交通边际拥塞收费。
**运筹学不是冷冰冰的数字代码，它是人类在复杂、随机与对抗的世界中，用最清醒的数学理性为现代文明构筑的最强护城河**。
:::
