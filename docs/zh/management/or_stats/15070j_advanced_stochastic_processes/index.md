---
title: '15.070J 高级随机过程与离散概率 (Advanced Stochastic Processes)'
type: course
course: '15.070J 高级随机过程与离散概率 (Advanced Stochastic Processes)'
course_id: '15.070J'
tags: [stochastic-processes, brownian-motion, martingales, ito-calculus, large-deviations]
status: complete
source: 'https://ocw.mit.edu/courses/15-070j-advanced-stochastic-processes-fall-2013/'
---

# 15.070J 高级随机过程与离散概率 (Advanced Stochastic Processes)

> MIT Sloan School of Management & Operations Research Center · 课号 15.070J / 6.265J · 授课教师：Prof. David Gamarnik

## TL;DR

- 麻省理工学院运筹学中心（ORC）与 EECS 旗舰博士级测度随机过程与随机分析理论奠基课程。
- 奠定现代测度拓扑与大偏差理论（LDP）基石：Cramér 定理、指数倾斜测度变换与 Gärtner-Ellis 相依过程极限。
- 深入布朗运动公理化体系：Kolmogorov 连续性定理、处处不可微性、几何反射原理与极值分布。
- 贯通鞅论核心大厦：Doob 可选抽样定理、Wald 恒等式、Doob 上跨引理与几乎必然收敛定理、Doob $L^p$ 极大不等式。
- 掌握高维概率几何集中与现代随机微积分：Azuma-Hoeffding、McDiarmid 有界差分、Talagrand 凸距离不等式、伊藤积分与伊藤引理、Black-Scholes 偏微分方程、Girsanov 测度变换、Donsker 泛函中心极限定理与 Skorokhod 反射布朗运动（RBM）。

## 课程全景与教学大纲

MIT 15.070J（跨院系代码 6.265J）由世界著名概率论与运筹学学者 David Gamarnik 教授主讲。课程系统构建起现代测度概率论、大偏差原理、鞅论、集中不等式与伊藤随机微积分的严谨公理化大厦，并无缝对接至通信网络、重负荷排队系统与金融工程前沿。

全课 22 讲讲义编排如下：

| 讲次 | 讲义主题 (Lecture Topic) | 核心理论、定理与算法突破 | 状态 |
| :--- | :--- | :--- | :---: |
| [Lec 1](lec1.md) | [度量空间拓扑、完备性与可分性 (Metric Spaces and Topology)](lec1.md) | 开球拓扑、柯西序列完备性、稠密子集与波兰空间（Polish Spaces）、博雷尔 $\sigma$-代数 | Complete |
| [Lec 2](lec2.md) | [大偏差理论基础与 i.i.d. 指数衰减律 (Large Deviations for i.i.d. RVs)](lec2.md) | 对数矩母函数、Legendre-Fenchel 对偶凸变换、良率函数、相对熵与 Kullback-Leibler 散度 | Complete |
| [Lec 3](lec3.md) | [Cramér 定理与大偏差原理渐近拓扑 (Cramér's Theorem)](lec3.md) | 开集下界与闭集上界、测度指数倾斜（Esscher 变换）、重要性采样最优对偶参数 | Complete |
| [Lec 4](lec4.md) | [大偏差技术的工程应用：排队、通信与破产风险 (Applications of LD)](lec4.md) | Cramér-Lundberg 保险破产模型、调节系数方程、Lindley 排队缓冲区溢出、有效带宽理论 | Complete |
| [Lec 5](lec5.md) | [高维大偏差与相依过程：Gärtner-Ellis 定理 (Gärtner-Ellis Theorem)](lec5.md) | 极限累积量母函数、本质平滑性、马尔可夫链 Perron-Frobenius 谱半径对偶展开 | Complete |
| [Lec 6](lec6.md) | [布朗运动公理化构建与轨道性质 (Introduction to Brownian Motion)](lec6.md) | 独立平稳正态增量、协方差核、Kolmogorov-Chentsov 连续性定理、处处不可导与 1/2-Hölder 连续 | Complete |
| [Lec 7](lec7.md) | [强马氏性、反射原理与极值分布 (The Reflection Principle)](lec7.md) | 自然滤过流与停时、强马尔可夫性、André 几何反射原理、运行极大值 $M_t$ 与 Lévy 首达时分布 | Complete |
| [Lec 8](lec8.md) | [布朗运动的二次变差与全变差发散性 (Quadratic Variation)](lec8.md) | 经典黎曼-斯蒂尔杰斯积分失效、均方收敛 $[B, B]_t = t$、全变差无穷发散、$(dB_t)^2 = dt$ 微元铁律 | Complete |
| [Lec 9](lec9.md) | [条件期望的 L2 投影、信息流与鞅结构 (Conditional Expectations & Martingales)](lec9.md) | 抽象 Radon-Nikodym 条件期望、$L^2$ 空间正交投影、滤过流 $\{\mathcal{F}_t\}$、鞅/下鞅/上鞅判定 | Complete |
| [Lec 10](lec10.md) | [鞅与停时理论 I：Doob 可选抽样定理 (Doob's Optional Sampling)](lec10.md) | 赌徒策略与停时可积性、Doob 抽样定理充分条件、双边吸收壁触碰概率与 Wald 恒等式 | Complete |
| [Lec 11](lec11.md) | [鞅与停时理论 II：收敛定理与 Doob 极大值不等式 (Convergence & Doob Inequalities)](lec11.md) | 上跨计数器与 Doob 上跨引理、几乎必然收敛定理、Doob 弱极大不等式与 $L^p$ 极大不等式 | Complete |
| [Lec 12](lec12.md) | [鞅集中不等式与 Azuma-Hoeffding 极限界 (Martingale Concentration)](lec12.md) | 鞅差序列、条件 Hoeffding 引理、Doob 鞅展开构造、McDiarmid 有界差分定理与随机图色数集中 | Complete |
| [Lec 13](lec13.md) | [Talagrand 凸距离不等式与高维几何集中 (Talagrand's Inequality)](lec13.md) | 加权凸包距离 $d_T(x, A)$、高维乘积测度等周性质、自证明证书函数、最长递增子序列 $\mathcal{O}(n^{1/4})$ 界 | Complete |
| [Lec 14](lec14.md) | [伊藤微积分启航：非预知过程与随机微分基础 (Introduction to Ito Calculus)](lec14.md) | 采样点位置决定的命运分叉、非预知性与因果律、左端点采样的不可替代性、伊藤等距定理 | Complete |
| [Lec 15](lec15.md) | [初等过程的伊藤积分构造与 L2 完备化 (Ito Integral for Simple Processes)](lec15.md) | 阶梯初等过程代数和、交叉项正交清零证明、初等过程稠密性与 Hilbert 空间柯西完备化延拓 | Complete |
| [Lec 16](lec16.md) | [通用伊藤积分的轨道连续性与局部鞅延拓 (Properties of Ito Integral)](lec16.md) | Doob 极大不等式保证处处连续轨道、停时截断局部化技术、局部平方可积 $\mathcal{L}^2$、连续局部鞅类 $\mathcal{M}_{\text{loc}}$ | Complete |
| [Lec 17](lec17.md) | [伊藤引理与随机微积分链式法则 (Ito Process and Ito's Formula)](lec17.md) | 连续半鞅微元法则、一维与多维伊藤引理、二阶曲率漂移修正项、几何布朗运动解析求解 | Complete |
| [Lec 18](lec18.md) | [连续半鞅积分与 Kunita-Watanabe 不等式 (Integration w.r.t. Martingales)](lec18.md) | 尖括号二次协变差 $\langle M, N \rangle_t$、Kunita-Watanabe 柯西不等式、Burkholder-Davis-Gundy (BDG) 范数双向等价 | Complete |
| [Lec 19](lec19.md) | [金融经济学应用：Black-Scholes 偏微分方程与 Girsanov 变换 (Financial Economics)](lec19.md) | 动态 Delta 对冲组合消灭随机性、BSM 偏微分方程、Girsanov 测度变换定理、风险中性等价鞅定价 | Complete |
| [Lec 20](lec20.md) | [弱收敛拓扑、波兰空间概率测度与 Prokhorov 紧致性 (Theory of Weak Convergence)](lec20.md) | 有界连续函数测试积分、Portmanteau 五重等价定理、相对紧致与几何胎紧（Tightness）、Prokhorov 充要定理 | Complete |
| [Lec 21](lec21.md) | [泛函中心极限定理与维纳测度的连续性构建 (Donsker's Invariance Principle)](lec21.md) | 分段线性随机折线、有限维分布与 Arzelà-Ascoli 连续模胎紧性、Donsker 不变性原理与连续映射定理 | Complete |
| [Lec 22](lec22.md) | [Skorokhod 映射定理、反射布朗运动与重负荷排队极限 (Skorokhod Mapping & RBM)](lec22.md) | 刚性边界互补松弛条件、局部时单调补偿力、稳态指数分布、重负荷排队网络扩散逼近 | Complete |

## 核心方法论与思想沉淀

::: insight 测度变换与正交投影是穿越随机迷雾的双子灯塔
概率论在初学者的印象中往往充斥着硬币、骰子与求和公式。然而，当步入现代高级随机过程的高原，我们赫然发现：
1. **条件期望是 Hilbert 空间中的正交投影**：在不完备信息的迷雾中，数学为你锁定了方差最小、最为理性的无偏基准；
2. **鞅是绝对公平的宇宙法则是守恒律**：任何精妙的停时策略都无法击穿可选抽样定理的庄严审判；
3. **测度变换是跨越认知维度的时空折跃门**：从大偏差理论中的 Cramér 测度指数倾斜，到金融经济学中消除漂移的 Girsanov 风险中性测度变换，人类通过主动改变概率测度的权重，将极端罕见的灾难事件与不可预测的市场主观情绪，巧妙化解为平易近人的标准高斯微积分。
这种深邃的数学力量，不仅塑造了 20 世纪下半叶物理学与金融学的黄金时代，更为现代复杂系统的决策优化提供了永不磨灭的思想罗盘。
:::
