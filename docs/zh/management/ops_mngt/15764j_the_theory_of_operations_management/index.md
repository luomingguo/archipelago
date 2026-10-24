---
title: '15.764J 运营管理理论'
type: course
course: '15.764J 运营管理理论'
course_id: '15.764J'
tags: [operations-theory, inventory-theory, stochastic-control, queueing-models]
status: complete
source: 'https://ocw.mit.edu/courses/15-764-the-theory-of-operations-management-spring-2004/'
---
# 15.764J 运营管理理论（The Theory of Operations Management）

> MIT Sloan School of Management · Spring 2004 · 授课教师：Prof. Jérémie Gallien, Stephen Graves

## TL;DR

- 聚焦顾客导向运营（Customer-Driven Operations）的高阶运筹学与应用随机过程理论体系。
- 涵盖多级分销库存、按订单装配（ATO）、预测演进鞅模型（MMFE）与短生命周期扩散控制。
- 深入离散选择收益管理（Choice-Based RM）、大服务系统 QED 随机流体排班与分层把关人机制。

::: definition [顾客导向运营理论（Customer-Driven Operations Theory）]
指将终端顾客的微观选择行为（交期敏感度、动态产品替代、等待焦虑折旧、异质效用）内生化，运用随机动态规划、弱收敛与布朗控制问题（EBCP），求解大规模服务与制造网络稳态最优控制律的数学理论体系。
:::

## 课程体系与理论分析全景

本博士研讨课立足于麻省理工学院经典运筹理论，系统剖析 24 篇开创性学术成果，分为六大核心理论板块：

1. **第一板块：多级分销系统（Lec 1–4）**：研讨顾客导向范式、Eppen-Schrage 集中订货与风险共担、Graves 负二项分布可维修件多级 METRIC 模型，以及 Roundy 98% 整数比例批量策略。
2. **第二板块：按订单装配系统（Lec 5–9）**：剖析 Rosling 树状装配向串联系统的同构降维、Gallien-Wein 随机装配组件采购启发式、Lu-Song 整单损失（Order-Based）凸优化、Wang-Glasserman 大偏差交期库存权衡，以及 Plambeck-Ward 高吞吐重交通布朗控制。
3. **第三板块：需求预测演进模型（Lec 10–12）**：推导 Heath-Jackson MMFE 鞅模型协方差分解、Graves-Kletter 状态空间动态 MRP 线性平滑，以及 Toktay-Wein 有限产能排队与自回归需求耦合动力学。
4. **第四板块：短生命周期产品管理（Lec 13–16）**：掌握 Fisher-Raman 两阶段精准响应（Accurate Response）、Kurawarwala-Matsuo 时变 Bass 扩散基准库存、Ho-Savin-Terwiesch 供应受限扩散动力学，以及 Fisher-Rajaram 代表性门店聚类与 MINLP 选品。
5. **第五板块：顾客选择与收益管理（Lec 17–19）**：推导 Mahajan-van Ryzin 动态替代样本路径梯度、Bitran 客户终身价值（CLV）与服务质量控制，以及 Talluri-van Ryzin 离散选择收益管理（CDLP）与有效前沿凸包筛选。
6. **第六板块：大规模服务与客户联络中心（Lec 20–24）**：研讨 Whitt 延迟通知排队论、Harrison-Zeevi 随机流体 QED 平方根排班、Pinker-Shumsky 多技能员工效率质量权衡、Armony-Maglaras 双通道虚拟回电控制，以及 Shumsky-Pinker 两级把关人转诊博弈。

## 讲义全景大纲 / Lecture Notes

### 第一板块：多级分销系统
- [Lec 1 研讨导引与顾客导向运营理论范式](./lec1.md)
  - 博士研讨定位、微观选择内生化、六大理论板块全景、维数灾难与渐近最优哲学。
- [Lec 2 多仓库集中式订货策略与风险共担模型](./lec2.md)
  - Eppen-Schrage 两级系统、分配平衡假设（Balanced Allocation）、风险共担效应平方根推导。
- [Lec 3 可维修备件的多级库存系统与 (S-1, S) 策略](./lec3.md)
  - Graves 备件理论、Palm 定理（$M/G/\infty$）、Depot 积压传递方差膨胀、负二项分布（NBD）双参数拟合。
- [Lec 4 单仓库多零售商系统的 98% 整数比例批量策略](./lec4.md)
  - Roundy 批量模型、2 的幂次方策略（Power-of-Two）、凸松弛与 98% 最坏情况界限证明。

### 第二板块：按订单装配系统
- [Lec 5 随机需求下装配系统的最优库存控制](./lec5.md)
  - 树状装配拓扑与短板效应、Rosling 状态空间降维同构映射、梯队基准库存策略最优性。
- [Lec 6 随机装配系统中的组件采购启发式策略](./lec6.md)
  - 通用多对多 ATO、受控广义排队网络、二次规划凸松弛、Gallien-Wein 线性分离采购策略。
- [Lec 7 按订单装配系统的基于订单成本优化](./lec7.md)
  - 整单交付（Order-Based）与极值非线性算子、Lu-Song 拟凸性与多维单调性证明、拉格朗日影子价格分解。
- [Lec 8 按订单装配系统中的交期与库存权衡](./lec8.md)
  - 承诺交期（Quoted Lead-time）竞争、大偏差理论（LDP）与渐近指数衰减率、延迟制造（Postponement）证明。
- [Lec 9 大规模按订单装配系统的高吞吐重交通随机控制](./lec9.md)
  - Plambeck-Ward 高吞吐重交通缩放、多维反射布朗运动（RBM）、等效布朗控制问题（EBCP）与前馈-反馈闭环。

### 第三板块：需求预测演进模型
- [Lec 10 需求预测演进模型（MMFE）与安全库存分析](./lec10.md)
  - Heath-Jackson 鞅模型（MMFE）、条件期望投影与鞅差序列正交分解、提前期内动态安全库存配置。
- [Lec 11 动态物料需求计划与供应链滚动优化](./lec11.md)
  - MRP 系统神经质、Graves-Kletter 状态空间 LQG 控制、离散代数黎卡提方程与线性平滑低通滤波器。
- [Lec 12 平稳需求下的预测-生产-库存耦合系统动力学](./lec12.md)
  - Toktay-Wein 耦合动力学、AR(1) 自回归需求过程、前瞻调整工作量指标与中度利用率信息价值峰值。

### 第四板块：短生命周期产品管理
- [Lec 13 早期销售快速响应与需求不确定性缩减](./lec13.md)
  - Sport Obermeyer 困境、Accurate Response 两阶段随机混合整数规划、专家意见分歧方差启发式规则。
- [Lec 14 短生命周期产品的预测与时变库存控制](./lec14.md)
  - 非平稳钟形曲线、Bass 创新-模仿扩散微分方程、Kurawarwala-Matsuo 时变基准库存相位提前量定理。
- [Lec 15 供应受限下新产品扩散与销售动力学控制](./lec15.md)
  - 缺货等待与负面口碑反噬、Ho-Savin-Terwiesch 四维流体非线性系统、临界产能爬坡与动态撇脂定价。
- [Lec 16 时尚商品的精准零售测试与量产组合优化](./lec16.md)
  - 门店特征聚类（$k$-means）、代表性测试门店 ANCOVA 外推、包含起订量与视觉陈列深度约束的 MINLP 选品。

### 第五板块：顾客选择与收益管理
- [Lec 17 动态顾客替代行为下的零售品类库存配置](./lec17.md)
  - 驱动型替代（Stockout Substitution）、多项式 Logit（MNL）效用微观机理、Mahajan-van Ryzin 样本路径随机梯度。
- [Lec 18 基于价格与服务质量的顾客关系与流失管理](./lec18.md)
  - 关系型运营范式、客户终身价值（CLV）马尔可夫决策过程、满意度溢价法则与危机干预服务杠杆。
- [Lec 19 离散选择模型下的收益管理与网络客座控制](./lec19.md)
  - 买低蚕食（Buy-down）、Talluri-van Ryzin 售票子集选择模型、有效前沿凸包筛选与 Choice-Based LP（CDLP）。

### 第六板块：大规模服务与客户联络中心
- [Lec 20 延迟通知对顾客等待心理与排队系统的优化](./lec20.md)
  - 未知等待的心理焦虑、Whitt 状态依赖延迟预估器、虚假报低的反噬与分级粗粒度通知最优性。
- [Lec 21 基于随机流体模型的大型呼叫中心人员排班](./lec21.md)
  - 多技能呼叫中心运筹困境、QED 范式平方根人员定额法则（$s = R + \beta \sqrt{R}$）、两阶段随机线性流体规划。
- [Lec 22 跨职能多技能员工的效率与质量权衡分析](./lec22.md)
  - 认知负荷与技能稀释、赖特学习曲线（Wright's Curve）、Pinker-Shumsky 核心专才-外围通才混合结构定理。
- [Lec 23 带有回电选项的客户联络中心路由与系统设计](./lec23.md)
  - 虚拟排队（Virtual Queueing）、实时在线与异步外呼双通道排队网络、Armony-Maglaras 门槛值动态调度律。
- [Lec 24 服务系统中的把关人与转诊机制优化](./lec24.md)
  - 分层把关人（Gatekeeper）架构、过度转诊 vs. 不当截留两类失误、Shumsky-Pinker 最优契约与激励对齐。

---

本资料整理自 [MIT OpenCourseWare](https://ocw.mit.edu/courses/15-764-the-theory-of-operations-management-spring-2004/)，遵循 Creative Commons BY-NC-SA 4.0 许可协议，仅供个人学习使用。
