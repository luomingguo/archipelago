---
title: '15.062J 数据挖掘：发现创造商业价值的模型与算法 (Data Mining)'
type: course
course: '15.062J 数据挖掘：发现创造商业价值的模型与算法 (Data Mining)'
course_id: '15.062J'
tags: [data-mining, predictive-analytics, machine-learning, classification-trees, clustering]
status: complete
source: 'https://ocw.mit.edu/courses/15-062-data-mining-spring-2003/'
---

# 15.062J 数据挖掘：发现创造商业价值的模型与算法 (Data Mining)

> MIT Sloan School of Management · Operations Research & Statistics · 课号 15.062J / ESD.72J · 授课教师：Prof. Roy Welsch / Nitin Patel

## TL;DR

- 融通统计学推断严谨性与计算机科学机器学习算力，专为应对高维、非平衡与海量工业数据。
- 涵盖有监督分类（k-NN, 朴素贝叶斯, CART, 判别分析, 逻辑回归, 神经网络, 正则化回归）与无监督洞察（PCA, 聚类, 关联规则, 协同过滤）。
- 强调非对称误分类代价（Cost-Sensitive Learning）、提升图（Lift Chart）与非平衡正例挖掘的商业决策闭环。
- 贯穿辉瑞制药 CRM 处方药精准营销、零售配货聚类、信用卡欺诈对抗等全链路工业实战案例。

## 课程全景与教学大纲

MIT 15.062J 是斯隆管理学院与运筹中心联合开设的经典数据挖掘旗舰课程。课程不仅深度讲授统计机器学习的核心数学原理与优化推导，更强调**“从商业痛点到算法建模，再到非对称成本评估与系统上线”**的完整工程链路。

全课 18 讲完整讲义知识库编排如下：

| 讲次 | 讲义主题 (Lecture Topic) | 核心算法与商业场景 | 状态 |
| :--- | :--- | :--- | :---: |
| [Lec 1](lec1.md) | [数据挖掘导论与 k-近邻分类预测 (Overview & k-NN)](lec1.md) | 割草机购买意向、欧氏距离归一化、维数灾难与 $k$ 值交叉验证 | Complete |
| [Lec 2](lec2.md) | [贝叶斯决策论与朴素贝叶斯分类 (Bayes Rule & Naïve Bayes)](lec2.md) | 极大后验概率 (MAP)、条件独立性假设、拉普拉斯平滑与垃圾邮件过滤 | Complete |
| [Lec 3](lec3.md) | [分类树与递归二分剪枝 (Classification Trees & CART)](lec3.md) | 波士顿房价高危分区、基尼不纯度、信息增益、CCP 复杂度剪枝 | Complete |
| [Lec 4](lec4.md) | [费希尔判别分析与多元统计分类 (Discriminant Analysis)](lec4.md) | Fisher 线性判别投影 (LDA/QDA)、鸢尾花分类、类内散度与类间散度 | Complete |
| [Lec 5](lec5.md) | [逻辑回归实战与织布机营销案例 (Logistic Regression Case: Handlooms)](lec5.md) | 对数几率几率比 (Odds Ratio)、极大似然估计、印度织布机投产营销 | Complete |
| [Lec 6](lec6.md) | [人工神经网络与反向传播算法 (Artificial Neural Networks)](lec6.md) | 多层感知机 (MLP)、Sigmoid 激活函数、链式法则反向传播、早停正则化 | Complete |
| [Lec 7](lec7.md) | [模型评估体系：提升图、增益曲线与 ROC (Model Evaluation)](lec7.md) | 累积收益曲线、十分位提升度 (Decile Lift)、非平衡样本非对称误分类矩阵 | Complete |
| [Lec 8](lec8.md) | [多元线性回归回顾与经典假设检验 (Multiple Regression Review)](lec8.md) | Gauss-Markov 定理、OLS 最小二乘投影、异方差与自相关残差诊断 | Complete |
| [Lec 9](lec9.md) | [现代数据挖掘中的多元回归与高维正则化 (MLR & Lasso)](lec9.md) | 共线性方差膨胀因子 (VIF)、AIC/BIC、Lasso $L_1$ 稀疏特征筛选与 Ridge $L_2$ | Complete |
| [Lec 10](lec10.md) | [回归树与主流挖掘算法横向对决 (Regression Trees & Comparison)](lec10.md) | 均方误差分割、IBM/GM 股票收益率波动预测、线面模型综合选型矩阵 | Complete |
| [Lec 11](lec11.md) | [无监督聚类算法：k-Means 与层次聚类 (Clustering Analysis)](lec11.md) | 轮廓系数 (Silhouette)、Ward 最小方差法、树状图截断与距离度量 | Complete |
| [Lec 12](lec12.md) | [零售商品企划与客户分群聚类案例 (Retail Merchandising Case)](lec12.md) | 百货零售门店形态聚类、库存配额优化、长尾商品与客户画像提炼 | Complete |
| [Lec 13](lec13.md) | [模型集成、装袋与提升算法 (Ensemble Methods: Bagging & Boosting)](lec13.md) | 偏差-方差分解、Bootstrap 聚合、随机森林 OOB 估计、AdaBoost 样本重加权 | Complete |
| [Lec 14](lec14.md) | [主成分分析与正交降维 (Principal Component Analysis)](lec14.md) | 协方差矩阵特征值分解、碎石图 (Scree Plot)、红酒理化指标投影压缩 | Complete |
| [Lec 15](lec15.md) | [辉瑞制药客户关系管理实战案例 (CRM at Pfizer)](lec15.md) | 医生处方药开药行为挖掘、学术拜访响应建模、法规伦理红线与 ROI 转化 | Complete |
| [Lec 16](lec16.md) | [购物篮分析与关联规则挖掘 (Association Rules & Apriori)](lec16.md) | 支持度 (Support)、置信度 (Confidence)、提升度 (Lift)、Apriori 频繁项集剪枝 | Complete |
| [Lec 17](lec17.md) | [工业推荐系统与协同过滤算法 (Collaborative Filtering)](lec17.md) | 基于用户与物品的协同过滤、余弦相似度、奇异值分解 (SVD) 隐语义空间 | Complete |
| [Lec 18](lec18.md) | [数据挖掘前沿工程实践、数据漂移与反欺诈演进 (The Practice of Data Mining)](lec18.md) | CRISP-DM 标准流程、概念漂移监测 (PSI)、动态对抗黑产图挖掘、工程伦理 | Complete |

## 核心方法论与思想沉淀

::: insight 商业价值创造是数据挖掘的唯一裁判
工业界的数据挖掘与纯粹的 Kaggle 竞赛有本质区别。Kaggle 追求在固定测试集上将准确率提升千分之几，为此不惜堆叠数百层的黑盒集成模型；而商业决策往往受到**推理延迟、可解释性审查（如信贷合规 Fair Lending Act）、管道运维成本与非对称误分类损失**的强力约束。
在医疗诊断与金融风控中，漏报一例恶性肿瘤或黑产团伙洗钱的代价是极其沉重的，而误报只是增加一次低成本复检或短信验证。掌握**提升图（Lift Chart）与基于非对称代价矩阵的截断阈值优化（Cost-Sensitive Threshold Tuning）**，远比盲目追求全样本 Accuracy 具备高出数量级的商业杀伤力。
:::

::: insight 降维与特征表示决定算法表现上限
在现代企业的高维数据中，直接拟合模型往往面临维数灾难与样本稀疏的困境。无论是通过 PCA 提取主成分正交子空间，通过 Lasso 进行稀疏特征选择，还是通过隐语义模型（SVD）将数百万用户的离散评分映射至低维潜在兴趣向量，**对高维空间几何结构的压缩与重构始终是数据挖掘最底层的核心功力**。
:::

---

本资料整理自 [MIT OpenCourseWare 15.062 Data Mining](https://ocw.mit.edu/courses/15-062-data-mining-spring-2003/)，遵循 Creative Commons BY-NC-SA 4.0 许可协议，仅供个人技术沉淀与知识库研读使用。
