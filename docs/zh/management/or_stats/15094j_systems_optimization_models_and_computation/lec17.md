---
title: '结构力学拓扑优化：桁架设计与凸规划模型 (Structural Optimization: Truss Design)'
type: lecture
lecture: 17
tags: [structural-optimization, truss-design, compliance-minimization, convex-programming]
status: complete
---

# Lec 17 结构力学拓扑优化：桁架设计与凸规划模型 (Structural Optimization: Truss Design)

> MIT 15.094J 鲁棒系统优化建模与计算 (Systems Optimization: Models and Computation) · 授课教师：Prof. Dimitris Bertsimas / Robert Freund

## TL;DR

- 结构拓扑优化将桥梁与建筑桁架杆件截面积分布抽象为刚度矩阵与外力平衡系统。
- 柔度极小化（Compliance Minimization）在弹性力学中等价于互补能量原理与凸二次规划。
- 通过将应力与位移约束转化为二阶锥（SOCP）或半正定规划（SDP）实现全局高效求解。

## 建筑力学与数学优化的世纪联姻

在土木工程、航空航天机翼骨架与现代高层建筑设计中，**结构拓扑优化（Structural Topology Optimization）**是决定结构物安全性与材料轻量化的核心学科。

工程师面临着经典的极值挑战：
给定一组空间节点（Nodes）以及作用在结构上的外部机械载荷（如风荷载、重力载荷、地震动载荷），在成百上千根备选的连接杆件（Truss Bars）中：
**如何为每一根杆件分配最优的横截面积（Cross-Sectional Area），使得在消耗最少钢材总自重的前提下，整座结构的物理刚度达到最大（变形柔度最小），且处处满足弹性胡克定律与屈服应力上限？**

麻省理工学院 15.094J 将力学物理学的虚功原理，无缝转化为优雅的凸二次规划与锥优化范式。

## 弹性桁架力学的物理控制方程

设空间桁架结构包含 $m$ 根杆件，$n$ 个自由度节点。
- **决策变量**：$a_i \ge 0$ 表示杆件 $i$ 的横截面积（$i = 1, \dots, m$），杆件长度为 $L_i$，弹性杨氏模量为 $E_i$。结构总材料体积预算为 $V_0$：
$$
\sum_{i=1}^m L_i a_i \le V_0
$$
- **几何相容性矩阵（Compatibility Matrix）**：$B \in \mathbb{R}^{m \times n}$ 将节点微小位移向量 $u \in \mathbb{R}^n$ 映射为各杆件的轴向伸长应变：
$$
\Delta L = B u
$$
- **刚度与内力本构关系**：根据胡克定律，杆件内部轴向拉伸/压缩轴力向量 $q \in \mathbb{R}^m$ 满足：
$$
q_i = \left(\frac{E_i a_i}{L_i}\right) (B u)_i
$$
- **节点静态力平衡方程**：外部载荷向量 $f \in \mathbb{R}^n$ 必须与各杆件内力严格平衡：
$$
B^T q = f \iff K(a) u = f
$$
其中系统的**全局刚度矩阵（Global Stiffness Matrix）**是关于杆件截面积 $a$ 的线性对称半正定张量：
$$
K(a) = \sum_{i=1}^m a_i \left(\frac{E_i}{L_i} b_i b_i^T\right) = B^T \text{diag}\left(\frac{E_i a_i}{L_i}\right) B \succeq 0
$$

```mermaid
flowchart LR
    A["杆件截面积向量 a ≥ 0 (总材料体积 ∑ L_i a_i ≤ V_0)"] --> B["组装全局对称半正定刚度矩阵 K(a) = ∑ a_i K_i"]
    B --> C["静力平衡方程: K(a) u = f"]
    C --> D["定义结构柔度 (Compliance): C(a) = f^T u = f^T K(a)^{-1} f"]
    D --> E["应用外力势能对偶转换"]
    E --> F["转化为标准凸二次规划 / 线性规划对偶全局秒解！"]
```

## 结构柔度极小化与凸规划等价性 (Compliance Minimization)

结构的整体弹性刚度通常由**柔度（Compliance, 弹性应变能的两倍）**来度量：
$$
C(a) = f^T u = f^T K(a)^{-1} f
$$
柔度越小，说明在相同外力 $f$ 作用下结构的弹性位移越小、抗变形能力越强。
优化问题表述为：
$$
\min_{a \ge 0} \quad f^T K(a)^{-1} f \quad \text{s.t.} \quad \sum_{i=1}^m L_i a_i \le V_0
$$
注意：虽然刚度矩阵求逆项 $K(a)^{-1}$ 看起来高度非线性，但根据矩阵分块 Schur 补引理与力学**余能原理（Principle of Complementary Energy）**：
该问题在内力空间 $q$ 中竟然等价于一个纯粹的**凸二次规划甚至线性规划**！

::: theorem [桁架设计的对偶凸等价定理]
引入每个杆件内部的轴力标量 $q_i$。原极小化柔度问题严格等价于以下凸规划：
$$
\begin{aligned}
\min_{a \ge 0, q} \quad & \sum_{i=1}^m \frac{L_i}{E_i a_i} q_i^2 \\
\text{s.t.} \quad & B^T q = f \quad (\text{静力平衡约束}) \\
& \sum_{i=1}^m L_i a_i \le V_0
\end{aligned}
$$
若进一步利用柯西-施瓦茨不等式对截面积 $a$ 进行解析最小化消元，问题奇迹般地退化为一个**纯绝对值线性规划**：
$$
\min_{q} \quad \frac{1}{V_0} \left(\sum_{i=1}^m \frac{L_i}{\sqrt{E_i}} |q_i|\right)^2 \quad \text{s.t.} \quad B^T q = f
$$
:::

### 结论的震撼工程意义
这意味着：**求解一座拥有数万根杆件的大型复杂桁架的最优拓扑，根本不需要繁琐的有限元试错，只需直接调用标准线性规划单纯形法，在秒级时间内即可求出严格无误差的全局物理最优解！**
解中截面积 $a_i^* = 0$ 的杆件可以直接从设计图纸中拔除，自然生成宛如大自然骨骼般优美的极简镂空仿生拓扑！

::: pitfall 忽视压杆失稳欧拉临界载荷（Euler Buckling）
上述线性规划仅考虑了材料屈服强度。在受压杆件中，当长细比过大时，杆件会在达到屈服极限前发生灾难性的**侧向欧拉屈曲失稳（Buckling）**：$q_{\text{crit}} \propto \frac{E I}{L^2} \propto a^2$。若将欧拉屈曲纳入约束，模型将升级为非凸二次约束，必须结合半正定松弛（SDP Relaxation）。
:::

::: insight 物理力学极值与运筹数学在宇宙底层的同构
为什么最小势能原理、虚功原理在数学形式上与拉格朗日对偶和 KKT 条件如此惊人地一致？
因为物理世界本身就是一个巨大的最优化求解器：**大自然在决定一根受力骨骼的纤维走向、一片树叶的叶脉分布时，无时无刻不在求解着使全系统应变自由能最小的凸优化问题**。掌握这套数学语言的工程师，本质上是在用上帝创造物理世界的法则来进行人类的工程设计。
:::
