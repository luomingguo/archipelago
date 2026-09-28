---
title: 15.075J 统计思维与数据分析
type: course
course: 15.075J 统计思维与数据分析
course_id: '15.075J'
tags: [statistics, probability, data-analysis, statistical-inference, regression-analysis]
status: complete
source: 'https://ocw.mit.edu/courses/15-075j-statistical-thinking-and-data-analysis-fall-2011/'
---

# 15.075J 统计思维与数据分析（Statistical Thinking and Data Analysis）

> MIT Sloan (15.075J) · MIT Engineering Systems Division (ESD.07J) · Fall 2011
> 授课教师：Prof. Cynthia Rudin、Allison Chang、Dimitrios Bisias
> 资料来源：[MIT OpenCourseWare](https://ocw.mit.edu/courses/15-075j-statistical-thinking-and-data-analysis-fall-2011/)

## TL;DR

- 本课程是 MIT 针对管理学院与工学院本科生开设的应用统计学基石课程，建立从基础概率论、数据收集与抽样分布到统计推断与回归分析的完整方法链。
- 强调“统计思维”（Statistical Thinking）：统计不仅是公式套用，更是量化现实世界不确定性、识别数据收集偏差与进行因果严谨论证的科学工具。
- 课程内容由两大核心模块构成：前半程聚焦概率测度、随机变量、抽样方案与大数定律；后半程系统深入参数估计、假设检验、方差分析（ANOVA）、多元线性回归与非参数统计方法。

## 课程定位与知识体系

统计学是现代数据科学、运筹管理与商业决策的底层基石。15.075J / ESD.07J 旨在打通从数学概率空间到真实数据洞察的通路：

1. **从概率模型到经验现实：** 理解样本空间、随机变量与极限理论，把现实中不确定的随机现象严格抽象为概率测度与分布律。
2. **从观测偏差到科学抽样：** 辨析总体参数与样本统计量之间的不可逆界限，理解简单随机抽样、分层抽样与整群抽样的权衡，规避混杂因素与自选择偏差。
3. **从参数估计到决策推断：** 建立基于中心极限定理与抽样分布的置信区间与假设检验机制，掌握第一类/第二类错误的权衡策略。
4. **从相关关联到多元解释：** 运用普通最小二乘法（OLS）建立单变量与多变量回归模型，诊断残差分布与共线性风险，指导现实决策。

## 讲义知识索引

课程讲义紧密围绕统计分析全生命周期展开：

| 讲次 | 核心专题 | 重点概念与推导 | 状态 |
| :--- | :--- | :--- | :--- |
| **[Lec 1](./lec1.md)** | **概率论核心回顾（Review of Probability）** | 柯尔莫哥洛夫公理、条件概率、全概率定理与贝叶斯法则、协方差、弱大数定律、常见离散与连续分布 | 已收录 |
| **[Lec 2](./lec2.md)** | **数据收集与抽样策略（Collecting Data）** | 总体与样本、抽样框、简单随机抽样（SRS）、分层抽样、整群抽样、系统抽样、自选择偏差 | 已收录 |
| **[Lec 3](./lec3.md)** | **数据探索与特征汇总（Summarizing & Exploring Data）** | 均值、中位数、四分位距（IQR）、盒须图、偏度、辛普森悖论与时间序列平滑 | 已收录 |
| **[Lec 4](./lec4.md)** | **统计量的抽样分布（Sampling Distributions）** | 样本均值分布、卡方分布、学生氏 t 分布、Snedecor F 分布、中心极限定理（CLT） | 已收录 |
| **[Lec 5](./lec5.md)** | **统计推断基本概念（Basic Concepts of Inference）** | 点估计、MSE 正交分解、偏差-方差权衡、样本方差除以 n-1 的代数证明、假设检验认识论 | 已收录 |
| **[Lec 6](./lec6.md)** | **单样本推断与功效分析（Inference for Single Samples）** | z/t 置信区间代数推导、样本容量规划（$n \propto 1/E^2$）、检验功效函数 $\pi(\mu_1)$ 精确解析 | 已收录 |
| **[Lec 7](./lec7.md)** | **双样本比较与实验设计（Two Sample Inferences）** | 成对匹配设计消噪机理、独立双样本合并方差（Pooled Variance）、Welch 修正自由度 | 已收录 |
| **[Lec 8](./lec8.md)** | **比例与计数数据推断（Proportions & Counts）** | 二项大样本正态逼近、多项分布拟合优度卡方检验、二维列联表自由度 $(r-1)(c-1)$ 证明 | 已收录 |
| **[Lec 9](./lec9.md)** | **一元线性回归与相关性（Simple Linear Regression）** | 最小二乘正规方程解析推导、均值穿透性、ANOVA 变异分解 $\operatorname{SST} = \operatorname{SSR} + \operatorname{SSE}$、$R^2 = r^2$ | 已收录 |
| **[Lec 10](./lec10.md)** | **多元线性回归与模型诊断（Multiple Linear Regression）** | 矩阵闭式解 $\hat{\boldsymbol{\beta}} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{Y}$、调整 $R^2_{\text{adj}}$、全模型 F 检验、多重共线性 VIF 诊断 | 已收录 |
| **[Lec 11](./lec11.md)** | **非参数统计方法（Nonparametric Methods）** | 稳健性 vs 功效权衡、中位数符号检验（Sign Test）、Wilcoxon 秩和与符号秩检验、95.5% 渐近相对效率 | 已收录 |

## 先修基础与参考资料

- **先修数学基础：** 建议具备初等微积分（单变量积分与级数）以及基础线性代数知识。
- **配套教材：** Devore, Jay L. *Probability and Statistics for Engineering and the Sciences*. 8th ed. Boston, MA: Cengage Learning, 2011.
- **计算实践：** 课程作业与案例深度结合 MATLAB / R 语言进行计算实验与蒙特卡洛模拟。
