---
title: 6.1220 算法的设计与分析
type: course
course: 6.1220 算法的设计与分析
course_id: '6.1220'
tags: [algorithms, divide-and-conquer, dynamic-programming, network-flow, linear-programming, randomized-algorithms, cryptography]
status: complete
source: https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/
---

# 6.1220 算法的设计与分析

## TL;DR

- **课程定位**：MIT 高级本科算法经典课程（原 6.046J），系统讲授非平凡算法的设计范式、数学严密性证明与计算下界分析。
- **核心范式**：涵盖分治法、高级动态规划、贪心选择、均摊势能分析、网络流增量改进、线性规划对偶与随机化跳表/哈希。
- **前沿拓展**：深入分布式对称破缺、现代密码学协议、缓存无关外部存储模型与 NP 完全性归约证明。

---

## 课程概述

6.1220（原 6.046J）是 MIT 计算机科学与工程系的核心理论进阶课程。相比于初阶算法（6.1210 / 6.006）聚焦于基础数据结构与经典图搜索，本课程重点建立对**复杂问题的高效算法设计范式、渐近数学证明、随机化与下界分析**的深度理解。

### 先行条件

- **6.1210 / 6.006 算法导论**：熟练掌握基本图遍历（BFS/DFS）、最短路径（Dijkstra/Bellman-Ford）、平衡搜索树与渐近表示法（$O, \Omega, \Theta$）。
- **6.1200 / 6.042 计算机数学**：离散数学、组合计数、条件概率与期望、递归方程求解与图论基础。

### 推荐教材

- Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein. *Introduction to Algorithms* (CLRS), 4th Edition, MIT Press.
- Jon Kleinberg, Éva Tardos. *Algorithm Design*, Pearson.

---

## 课程知识架构

本门课程围绕三大主线展开：**基础与高级范式**、**图与连续优化**、**现代与前沿计算模型**。每一个专题不仅要求掌握算法的具体步骤，更强调通过不变量与数学推导证明算法的正确性与复杂度界限。

- **基础与高级范式**：从分治法的递推式主定理展开，过渡到中位数查找的确定性线性时间选择；通过势能函数精确量化动态数组与并查集的均摊成本；探索区间与二叉树上的高级动态规划结构。
- **图与连续优化**：通过割性质与环性质建立最小生成树的统一贪心视角；基于残余网络与增广路径剖析最大流最小割定理；将离散图问题抽象为线性规划，通过对偶性与单纯形几何视角连接至博弈论极小极大定理。
- **现代计算模型与密码学**：跳脱传统确定性比较模型，利用随机化打破输入假设（跳表与两级完美哈希）；在分布式系统中探讨对称破缺与共识；分析密码学单向陷门与零知识证明；结合现代多级存储层次构建缓存无关算法。

---

## 讲义笔记导航

| 讲次 | 核心主题与算法 | 讲义链接 | 核心思想 / 机制 |
| :--- | :--- | :--- | :--- |
| **Lec 01** | 课程概览与区间调度 | [lec1.md](./lec1.md) | 最早完成时间贪心证明、带权区间调度 DP |
| **Lec 02** | 分治法：中位数查找与凸包 | [lec2.md](./lec2.md) | BFPRT 五分中位数线性选择、凸包分治合并 |
| **Lec 04** | 分治法：van Emde Boas 树 | [lec4.md](./lec4.md) | 递归全集分解、$O(\log \log u)$ 优先队列 |
| **Lec 05** | 均摊分析：势能法与并查集 | [lec5.md](./lec5.md) | 聚合分析、记账法、势能法、并查集反阿克曼复杂度 |
| **Lec 07** | 随机化：跳表 | [lec7.md](./lec7.md) | 几何分布索引、向后分析法、$O(\log n)$ 高概率界 |
| **Lec 08** | 随机化：通用哈希与完美哈希 | [lec8.md](./lec8.md) | 通用哈希族、两级完美哈希、最坏 $O(1)$ 查找 |
| **Lec 10** | 动态规划：高级 DP | [lec10.md](./lec10.md) | 最长回文子序列、最优二叉搜索树、交替硬币博弈 |
| **Lec 12** | 贪心算法：最小生成树 | [lec12.md](./lec12.md) | 割性质与环性质、Kruskal 与 Prim 严密性证明 |
| **Lec 13** | 增量改进：最大流与最小割 | [lec13.md](./lec13.md) | 残余网络、增广路径、最大流最小割定理、Ford-Fulkerson |
| **Lec 15** | 线性规划：建模、对偶与博弈 | [lec15.md](./lec15.md) | LP 标准型、半平面可行域、强对偶定理与零和博弈 |
| **Lec 16** | 计算复杂性：P、NP 与 NP 完全性 | [lec16.md](./lec16.md) | 多项式时间验证、Karp 归约、3-SAT 与顶点覆盖 |
| **Lec 19** | 同步分布式算法：对称破缺 | [lec19.md](./lec19.md) | 环网络领导者选举、LCR/HS 算法、确定性与随机化 |
| **Lec 21** | 密码学：哈希函数 | [lec21.md](./lec21.md) | 抗原像/碰撞性、随机预言机、Merkle-Damgård |
| **Lec 22** | 密码学：加密体系与 RSA | [lec22.md](./lec22.md) | 对称/公钥体制、Diffie-Hellman、RSA、零知识证明 |
| **Lec 23** | 缓存无关算法：中位数与矩阵 | [lec23.md](./lec23.md) | 理想缓存模型、分块扫描、分治矩阵乘法缓存缺页分析 |

---

## 课程作业与习题（Problem Sets）

| 习题编号 | 题目 PDF (OCW) | 官方参考解答 (PDF) |
| :--- | :--- | :--- |
| **Problem Set 1** | [Problem Set 1](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_pset1/) | [Solutions 1](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_pset1sols/) |
| **Problem Set 2** | [Problem Set 2](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_pset2/) | [Solutions 2](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_pset2sols/) |
| **Problem Set 3** | [Problem Set 3](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_pset3/) | [Solutions 3](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_pset3sols/) |
| **Problem Set 4** | [Problem Set 4](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_pset4/) | [Solutions 4](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_pset4sols/) |
| **Problem Set 5** | [Problem Set 5](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_pset5/) | [Solutions 5](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_pset5sols/) |
| **Problem Set 6** | [Problem Set 6](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_pset6/) | [Solutions 6](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_pset6sols/) |
| **Problem Set 7** | [Problem Set 7](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_pset7/) | [Solutions 7](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_pset7sols/) |
| **Problem Set 8** | [Problem Set 8](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_pset8/) | [Solutions 8](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_pset8sols/) |
| **Problem Set 9** | [Problem Set 9](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_pset9/) | [Solutions 9](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_pset9sols/) |
| **Problem Set 10** | [Problem Set 10](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_pset10/) | [Solutions 10](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_pset10sols/) |

---

## 考试测试（Exams）

| 考试阶段 | 考题 PDF (OCW) | 参考解答 (PDF) |
| :--- | :--- | :--- |
| **期中测试 1 (Quiz 1)** | [Quiz 1 考卷](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_quiz1/) | [Quiz 1 官方解答](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_quiz1sols/) |
| **期中测试 2 (Quiz 2)** | [Quiz 2 考卷](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_quiz2/) | [Quiz 2 官方解答](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_quiz2sols/) |
| **期末考试 (Final Exam)** | [Final Exam 考卷](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_final/) | [Final Exam 官方解答](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/mit6_046js15_finalsols/) |
