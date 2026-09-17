---
title: 6.5250 分布式算法
type: course
course: 6.5250 分布式算法
course_id: '6.5250'
tags: [distributed-algorithms, local-model, congest-model, consensus, network-decomposition]
status: complete
source: https://people.csail.mit.edu/ghaffari/DA25/
---
# 6.5250 分布式算法

> 课程：MIT 6.5250 Distributed Algorithms · 讲师：Mohsen Ghaffari · 资料依据：官方讲义与经典文献

## TL;DR

- 课程深入研究分布式计算的基础理论与算法：覆盖 LOCAL 局部分布式模型、CONGEST 带宽受限模型及异步容错系统。
- 核心主题包括对称性破除（着色与 MIS）、网络分解与去随机化、同步/异步共识及其不可能界、以及全局图优化（MST、Min-Cut、最短路径）。
- 重点聚焦于用算法工具和组合技术证明严格的轮复杂度上界、下确界及不可能结果（如 Linial 着色下界、FLP 不可能性与 Peleg-Rubinovich 带宽下界）。

## 课程定位与学习成果

分布式算法是现代众多计算系统的核心，包括有线和无线网络、集群计算、多核系统、分布式数据库与通信系统。本课程为研究生层面的理论课程，目标在于帮助学习者掌握分布式环境下的通信、协调、局部性与容错原理，并具备分析轮复杂度与证明下界的能力。完成后，应能够：

- 区分 LOCAL 模型与 CONGEST 模型的能力边界，将通信轮数映射为局部邻域依赖拓扑；
- 运用确定性掷币（Cole-Vishkin）、覆盖无关族与缺陷着色解决对称性破除与图着色问题；
- 掌握 Luby 随机 MIS 算法及其边减半分析法，理解网络分解（Network Decomposition）作为去随机化引擎的工作机制；
- 分析容错同步共识协议（FloodSet、EIG），并用不可区分性论证证明 $n > 3f$ 与 $f+1$ 轮下界；
- 深入理解异步模型中的 FLP 不可能性定理（双值性论证），以及 Ben-Or 随机共识的破僵局机制；
- 掌握 CONGEST 模型下的分布式 MST、Min-Cut 与加权最短路径近似算法，并理解基于集合不交性的 $\tilde\Omega(D+\sqrt n)$ 全局下界框架。

## 前置知识

- **算法设计与分析**（MIT 6.1220 / 6.046）：掌握基础图算法、贪心策略、动态规划与渐近复杂度分析；
- **概率与随机算法**：熟悉期望、马尔可夫不等式、切诺夫界与并集界；
- **自动机与形式化模型**（MIT 6.045）：熟悉状态机、不可区分性论证与基础计算复杂性。

## 参考书目

- Nancy A. Lynch. *Distributed Algorithms*. Morgan Kaufmann, 1996.（经典教材，系统覆盖同步与异步共识、网络搜索与同步器）
- Hagit Attiya, Jennifer Welch. *Distributed Computing: Fundamentals, Simulations, and Advanced Topics*. 2nd Edition, Wiley, 2004.（强调时间同步与系统模拟，风格现代）
- Maurice Herlihy, Nir Shavit. *The Art of Multiprocessor Programming*. Morgan Kaufmann, 2008.（多核与共享内存并发算法基础）
- Rachid Guerraoui, Michal Kapalka. *Principles of Transactional Memory*. Morgan & Claypool, 2010.
- Shlomi Dolev. *Self-Stabilization*. MIT Press, 2000.
- Dilsun Kaynar, Nancy Lynch, Roberto Segala, Frits Vaandrager. *The Theory of Timed I/O Automata*. 2nd Edition, 2010.

## 讲义目录

### 模块一：同步与基础通信原语

1. [LOCAL 模型与有根树着色](./lec1.md)
   - 对应 DGA §1.1, §1.2.1 · 局部性数学刻画、$\log^*$ 函数、Sperner 家族与单轮指数颜色缩减
2. [泛洪、BFS 树、广播、收敛广播与 Bellman-Ford](./lec2.md)
   - CONGEST 模型基础原语、树上流水线广播、散发-聚合范式与分布式最短路径

### 模块二：局部分布式图算法（对称性破除）

3. [一般图的确定性着色](./lec3.md)
   - 对应 DGA §1.4 · Linial $O(\Delta^2)$ 着色、覆盖无关族显式构造、分桶并行缩减与 Kuhn 缺陷着色
4. [着色下界](./lec4.md)
   - 对应 DGA §1.2.2, §1.3.1 · 有向路径 3-着色 $\Omega(\log^* n)$ 下界、Ramsey 论证与高围长图不可区分性
5. [最大独立集 MIS](./lec5.md)
   - 对应 DGA §1.6 · MIS 到 $(\Delta+1)$-着色归约、Luby 随机算法与单手击杀期望边减半分析
6. [网络分解：定义与随机化构造](./lec6.md)
   - 对应 DGA §1.5.1, §1.5.2 · 弱/强直径分解、基于几何分布随机半径的球生长（Ball Carving）
7. [网络分解：确定性构造](./lec7.md)
   - 对应 DGA §1.5.4 · RG20 突破性成果、聚类引理、逐比特前缀消界机制与分布式去随机化

### 模块三：容错与异步分布式算法

8. [容错同步共识算法](./lec8.md)
   - 对应 Lynch 第 5.1, 6.1–6.3 节 · 协同进攻不可能性、FloodSet、OptFloodSet 与 EIGByz 递归多数表决
9. [容错同步共识下界](./lec9.md)
   - 对应 Lynch 第 6.4–6.7, 7.1 节 · 拜占庭 $n > 3f$ 六边形拼接证明、连通度 $\ge 2f+1$、任何共识 $f+1$ 轮下界与 k-agreement
10. [异步共识：FLP 不可能性与 Ben-Or](./lec10.md)
    - 异步消息传递模型、FLP 不可能性定理（双值性与临界步论证）、Ben-Or 随机共识与自由选择
11. [同步器](./lec11.md)
    - 对应 Lynch 第 16 章 · GlobSynch 规范、安全推进抽象、$\alpha/\beta/\gamma$ 三种同步器权衡与低直径簇分解

### 模块四：全局分布式图算法

12. [最小生成树 MST 算法](./lec12.md)
    - 对应 DGA §2.2 · 分布式 Borůvka、大小分量划分、低拥塞捷径（Low-Congestion Shortcuts）与 $\tilde O(D+\sqrt n)$ 上界
13. [最小割 Min-Cut 近似算法](./lec13.md)
    - 对应 DGA §2.3 · 连通度稀疏证书、基于加权 MST 的构造、$(2+\varepsilon)$-近似割与平面图 $\tilde O(D)$ 加速
14. [全局问题下界：MST、Min-Cut 与最短路](./lec14.md)
    - Peleg-Rubinovich 高速路下界、基于集合不交性的两方通信复杂度归约与 $\tilde\Omega(D+\sqrt n)$ 紧界
15. [最短路径算法 I：加权最短路的分布式近似](./lec15.md)
    - 限跳 Bellman-Ford、跳数直径与拓扑直径脱钩、$\sqrt n$ 骨架采样与 $(1+o(1))$-近似 SSSP
16. [最短路径算法 II：路由表构造与稀疏生成子图](./lec16.md)
    - 骨架图压缩、Baswana-Sen 稀疏生成子图、Lenzen-Patt-Shamir 紧凑路由表构造

### 模块五：进阶前沿专题（论文阅读）

- **专题 1：全连通网络中的路由**
  - Lenzen & Wattenhofer, STOC 2011 · [Routing in the Complete Network](https://dl.acm.org/doi/10.1145/1993636.1993639)
  - Lenzen, PODC 2013 · [Optimal Routing in the Complete Network](https://dl.acm.org/doi/10.1145/2484239.2501983)
- **专题 2：线性素描与动态图连通性**
  - Ahn, Guha, McGregor, SODA 2012 / PODS 2012 · [Dynamic Graph Streams via Linear Sketching](https://people.cs.umass.edu/~mcgregor/papers/12-dynamic.pdf)
  - Kapron, King, Mountjoy, SODA 2013 · [Dynamic Graph Connectivity in Polylogarithmic Worst Case Time](https://epubs.siam.org/doi/10.1137/1.9781611973105.81)
- **专题 3：局部计算算法 (LCAs)**
  - Nguyen & Onak, FOCS 2008 · [Constant-Time Approximation Algorithms for Maximum Matching and Other Problems](https://ieeexplore.ieee.org/abstract/document/4690966/)
  - Rubinfeld, Tamir, Vardi, Xie, ITCS 2011 · [Fast Local Computation Algorithms](https://arxiv.org/abs/1104.1377)
  - Ghaffari, FOCS 2022 · [Derandomizing Local Computation Algorithms](https://arxiv.org/abs/2210.01104)
- **专题 4：图粉碎与局部复杂度格局**
  - Barenboim, Elkin, Pettie, Schneider, FOCS 2012 · [The Locality of Distributed Symmetry Breaking](https://ieeexplore.ieee.org/abstract/document/6375310)
  - Ghaffari, SODA 2016 · [An Improved Distributed Algorithm for Maximal Independent Set](https://epubs.siam.org/doi/10.1137/1.9781611974331.ch20)
  - Chang, Kopelowitz, Pettie, FOCS 2016 · [An Exponential Separation between Randomized and Deterministic Complexity in the LOCAL Model](https://ieeexplore.ieee.org/document/7782976)
  - Chang & Pettie, FOCS 2017 · [A Hierarchy of Lower Bounds for Sublinear Additive Spanners](https://arxiv.org/abs/1704.06297)
- **专题 5：分布式 Lovász Local Lemma**
  - Moser & Tardos, JACM 2010 · [A Algorithmic Proof of the General Lovász Local Lemma](https://dl.acm.org/doi/abs/10.1145/1667053.1667060)
  - Chung, Pettie, Su, PODC 2014 · [Distributed Algorithms for the Lovász Local Lemma and Graph Coloring](https://dl.acm.org/doi/10.1145/2611462.2611465)
- **专题 6：拟团分解与局部舍入**
  - Halldorsson, Maus, Kuhn, Tonoyan, STOC 2021 · [Fast and Simple Distributed Coloring through Almost Clique Decomposition](https://dl.acm.org/doi/10.1145/3406325.3451089)
  - Ghaffari & Kuhn, FOCS 2021 · [Local Rounding](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9719807)
  - Faour, Ghaffari, Grunau, Kuhn, Rozhon, SODA 2023 · [Distributed Lovász Local Lemma and MIS](https://arxiv.org/abs/2209.11651)
