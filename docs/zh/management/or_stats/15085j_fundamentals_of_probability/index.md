---
title: '15.085J 概率论基础 (Fundamentals of Probability)'
type: course
course: '15.085J 概率论基础 (Fundamentals of Probability)'
course_id: '15.085J'
tags: [probability-theory, measure-theory, convergence-concepts, central-limit-theorem, markov-chains, martingales]
status: complete
source: 'https://ocw.mit.edu/courses/6-436j-fundamentals-of-probability-fall-2018/'
---

# 15.085J 概率论基础 (Fundamentals of Probability)

> MIT Sloan School of Management & EECS · Operations Research Center · 课号 15.085J / 6.436J · 授课教师：Prof. John Tsitsiklis / Devavrat Shah

## TL;DR

- 麻省理工学院研究生阶段严格基于测度论（Measure-Theoretic）公理体系构建的概率论理论基石。
- 确立概率空间三元组 $(\\Omega, \\mathcal{F}, \\mathbb{P})$、$\\sigma$-代数封闭性与勒贝格积分三大极限收敛定理（MCT, Fatou, DCT）。
- 严密建立四大收敛性拓扑谱系（$a.s., P, L^p, d$）、弱大数定理、强大数定理（SLLN）与中心极限定理（CLT）。
- 系统覆盖离散/连续时间马尔可夫链（遍历定理、细致平衡）与现代鞅论（Doob 可选停时定理与鞅收敛）。

## 课程全景与教学大纲

MIT 15.085J（跨院系代码 6.436J）是由世界著名学者 John Tsitsiklis 与 Devavrat Shah 教授共同讲授的经典研究生硬核课程。课程彻底摒弃了初等统计学的试凑直觉，以实分析与测度论为手术刀，为随机变量、期望、极限与动态随机过程建立起纯粹无瑕的公理化数学底座。

全课 26 讲系统化讲义编排如下：

| 讲次 | 讲义主题 (Lecture Topic) | 核心理论、定理与数学突破 | 状态 |
| :--- | :--- | :--- | :---: |
| [Lec 1](lec1.md) | [概率模型公理体系、sigma-代数与测度空间 (Probabilistic Models)](lec1.md) | 柯尔莫哥洛夫三公理、$\\sigma$-代数运算封闭性、下连续与卡拉西奥多里（Carathéodory）扩张 | Complete |
| [Lec 2](lec2.md) | [两大基石概率模型与非可测集构造 (Two Models & Vitali Sets)](lec2.md) | 无限伯努利序列与勒贝格测度同构、选择公理、维塔利（Vitali）不可测集严谨悖论证明 | Complete |
| [Lec 3](lec3.md) | [条件概率、全概率公式与独立性事件系统 (Conditioning & Independence)](lec3.md) | 证据驱动样本空间坍缩、全概率公式、贝叶斯定理、柯尔莫哥洛夫零一律（Zero-One Law） | Complete |
| [Lec 4](lec4.md) | [随机变量的测度论定义与生成代数 (Random Variables)](lec4.md) | 确定性可测映射本质、博雷尔原像审查、前推测度（CDF）与杜布-丁金引理（Doob-Dynkin） | Complete |
| [Lec 5](lec5.md) | [离散随机变量、指示函数与期望的级数定义 (Discrete Expectations)](lec5.md) | 概率质量函数（PMF）、指示函数简单积木分解、黎曼重排陷阱与绝对收敛刚性 | Complete |
| [Lec 6](lec6.md) | [方差、协方差与条件期望的离散投影 (Discrete Variance & Conditioning)](lec6.md) | 二阶中心矩波动、协方差矩阵半正定性、条件期望作为随机变量、全方差分解公式（Eve's Law） | Complete |
| [Lec 7](lec7.md) | [抽象勒贝格积分 I：非负简单函数与单调收敛定理 (Abstract Integration I)](lec7.md) | 黎曼横切崩溃批判、勒贝格因变量纵向切分公理阶梯、单调收敛定理（MCT）自由交换极限 | Complete |
| [Lec 8](lec8.md) | [抽象勒贝格积分 II：Fatou 引理与控制收敛定理 (Abstract Integration II)](lec8.md) | 法图引理（Fatou）下半连续基底、控制收敛定理（DCT）终极杀手锏、移动逃逸质量反例 | Complete |
| [Lec 9](lec9.md) | [积测度空间与 Fubini-Tonelli 积分次序交换定理 (Product Measures & Fubini)](lec9.md) | 笛卡尔积测度唯一延拓、托内利定理（Tonelli）非负无条件交换、富比尼（Fubini）绝对可积守护 | Complete |
| [Lec 10](lec10.md) | [连续型随机变量 I：绝对连续性与 Radon-Nikodym 导数 (Continuous Random Variables I)](lec10.md) | 单点概率为零哲学、测度绝对连续性（$\\mathbb{P} \\ll \\lambda$）、拉东-尼科迪姆导数与概率密度函数（PDF） | Complete |
| [Lec 11](lec11.md) | [连续型随机变量 II：指数分布无记忆性与高斯积分 (Continuous Random Variables II)](lec11.md) | 指数分布无记忆性充要证明、危险率函数（Hazard Rate）、高斯积分二维极坐标变换解构 | Complete |
| [Lec 12](lec12.md) | [导出分布与变量代换：雅可比行列式与卷积微积分 (Derived Distributions)](lec12.md) | 体积微元缩放守恒律、多维非线性双射雅可比行列式、独立随机变量之和连续卷积积分 | Complete |
| [Lec 13](lec13.md) | [矩母函数、拉普拉斯变换与 Chernoff 指数界 (Moment Generating Functions)](lec13.md) | 指数期望全阶动差生成、独立和卷积消灭点乘化、分布唯一性、切尔诺夫（Chernoff）指数界 | Complete |
| [Lec 14](lec14.md) | [多元高斯向量：协方差正定性、正交投影与条件正态性 (Multivariate Normal)](lec14.md) | 线性组合正态公理、马氏距离等密度椭球、不相关即独立特例、条件高斯分布与舒尔补解耦 | Complete |
| [Lec 15](lec15.md) | [特征函数、逆转公式与 Lévy 连续性定理 (Characteristic Functions)](lec15.md) | 复傅里叶全域良定义、模长有界性、列维逆转公式（Inversion）、Lévy 连续性定理弱收敛引擎 | Complete |
| [Lec 16](lec16.md) | [随机变量收敛性四大层级：几乎处处、依概率、Lp 与依分布 (Convergence Modes)](lec16.md) | 四大收敛模式严格定义、单向蕴含拓扑谱系、打字机序列经典反例、Riesz 子序列救赎定理 | Complete |
| [Lec 17](lec17.md) | [弱大数定律：契比雪夫不等式与样本均值弱收敛 (Laws of Large Numbers I: WLLN)](lec17.md) | 马尔可夫与契比雪夫不等式、方差除以 $n$ 稀释律、辛钦（Khinchin）一阶矩充要弱大数定律 | Complete |
| [Lec 18](lec18.md) | [强大数定律：柯尔莫哥洛夫三级数定理与几乎处处收敛 (Laws of Large Numbers II: SLLN)](lec18.md) | 弱与强的本质鸿沟、波莱尔-坎泰利引理（Borel-Cantelli）、柯尔莫哥洛夫强大数定律充要证明 | Complete |
| [Lec 19](lec19.md) | [一致可积性、Vitali 收敛定理与级数几乎处处收敛 (Uniform Integrability)](lec19.md) | 尾部质量逃逸防线、维塔利收敛定理（Vitali）、柯尔莫哥洛夫三级数几乎处处收敛判据 | Complete |
| [Lec 20](lec20.md) | [中心极限定理、Lindeberg-Feller 条件与随机过程样本轨道 (CLT & Processes)](lec20.md) | 微观混沌的宏观高斯涌现、Lindeberg-Feller 非同分布边界、随机过程截面与样本轨道对偶 | Complete |
| [Lec 21](lec21.md) | [离散时间马尔可夫链 I：无记忆转移与 Chapman-Kolmogorov 方程 (Markov Chains I)](lec21.md) | 一阶历史独立性、随机转移矩阵 $P$、查普曼-科尔莫哥洛夫方程与矩阵幂动力学 $P^n$ | Complete |
| [Lec 22](lec22.md) | [离散时间马尔可夫链 II：常返、暂态与不可约分解 (Markov Chains II)](lec22.md) | 互通等价类划分、不可约闭类、首达概率 $f_{ii}$ 与常返/暂态二分法、有限状态不可约常返定理 | Complete |
| [Lec 23](lec23.md) | [离散时间马尔可夫链 III：平稳分布与大数遍历定理 (Markov Chains III: Ergodicity)](lec23.md) | 矩阵不动点 $\\pi = \\pi P$、细致平衡条件（Detailed Balance）与时间可逆性、强遍历定理时空交换 | Complete |
| [Lec 24](lec24.md) | [可数无穷状态链与连续时间马尔可夫跳跃过程 (Infinite Chains & Continuous Time)](lec24.md) | 零常返（Null Recurrent）怪兽、Polya 随机游走三维逃逸定理、无穷小生成元 $Q$ 矩阵与微分方程 | Complete |
| [Lec 25](lec25.md) | [鞅论 I：条件期望作为正交投影、滤波与停时理论 (Martingales I: Filtration)](lec25.md) | 希尔伯特空间 $L^2$ 投影算子、递增滤波 $\\mathbb{F}$、公平博弈鞅定义、合规停时（Stopping Time）公理 | Complete |
| [Lec 26](lec26.md) | [鞅论 II：Doob 可选停时定理与鞅收敛全景 (Martingales II: Optional Stopping)](lec26.md) | 赌徒策略死刑宣告（Doob OST）、杜布最大值不等式整轨控制、几乎处处鞅收敛定理与波利亚罐 | Complete |

## 核心方法论与思想沉淀

::: insight 测度论是抵御无穷悖论的绝对理性之盾
在不可数无限与无穷维度的世界里，人类基于有限经验形成的“直觉”极其容易沦为逻辑谬误的温床。
从贝特朗悖论到维塔利不可测集，分析学历史一再证明：缺少测度论的严谨约束，概率论就会在条件级数重排与选择公理的撕扯下分崩离析。
$\\sigma$-代数的封闭性并非数学家的吹毛求疵，而是**在浩瀚混乱的无穷集合宇宙中，精确划定人类认知与物理可观测性的法律边界**。正是这一套由柯尔莫哥洛夫立下的公理铁律，捍卫了整个现代随机科学的确定性尊严。
:::

::: insight 投影与对称是随机大厦的隐秘双螺旋
通读全课，会发现两座反复耸立的宏伟思想灯塔：
其一是**投影（Projection）**：从条件期望在希尔伯特空间的正交投影，到马尔可夫链在平稳分布上的遍历投影，再到多元高斯条件分布在舒尔补上的线性投影；
其二是**对称（Symmetry）**：从指数分布的无记忆时间对称，到高斯分布的欧氏旋转对称，再到鞅论中未来对过去期望的完美中和。
当面对复杂的随机现象时，只要牢牢抓住系统的守恒投影与内生对称性，混沌的随机波浪就会自发展现出严密而壮丽的几何律动。
:::

---

本资料整理自 [MIT OpenCourseWare 6.436J / 15.085J Fundamentals of Probability](https://ocw.mit.edu/courses/6-436j-fundamentals-of-probability-fall-2018/)，遵循 Creative Commons BY-NC-SA 4.0 许可协议，仅供个人技术沉淀与知识库研读使用。
