---
title: 6.5210 高级算法
course: 6.5210 高级算法
course_id: '6.5210'
type: course
tags: [advanced-algorithms, algorithms, data-structures, graph-algorithms, mit]
status: complete
---

# 6.5210 / 6.854 高级算法（Advanced Algorithms）

## TL;DR

- **算法边界的系统性突破**：超越经典比较模型与最坏情况分析，探索利用字级并行、势能均摊、随机化与几何对偶性突破经典复杂度下界。
- **核心数据结构模块**：系统涵盖全域与完美哈希、Fibonacci 堆、持久化数据结构、伸展树（Splay Tree）、单调优先队列与 van Emde Boas 树。
- **理论深度与研究导向**：直面计算机科学理论经典论文，聚焦势能分析法（Potential Method）、路径复制与节点复制机制，以及动态最优性等未解问题。

## 课程简介与设计哲学

高效算法的需求几乎出现在计算机科学的每一个分支领域中。然而，不同领域需要解决的问题类型、“高效”的数学定义乃至底层的计算模型都有根本性的不同。

MIT 6.5210（原 6.854 / 18.415J）由著名算法理论学者 David Karger 等人开设，定位为算法方向的高级综合性研究生课程。课程的核心目标是帮助学生跨越基础本科算法（如 6.046）的门槛，达到能够直接阅读、理解并推进算法顶级理论会议与期刊（STOC, FOCS, SODA, JACM）研究论文的水平。

课程的四大核心支柱：
1. **打破传统计算模型**：超越比较模型（$\Omega(n \log n)$ 下界），利用 RAM 字级并行性与整数键域特性设计亚对数级数据结构。
2. **均摊分析与自适应性**：借助势能函数量化连续操作代价，使数据结构无需显式平衡即可达到最优均摊界。
3. **随机化与哈希技术**：通过 2-全域哈希族与两级哈希表以 $O(1)$ 期望或最坏情况时间消除碰撞。
4. **几何与持久化范式**：利用时空转换与节点复制技术实现多版本数据结构的时间旅行与高效点定位。

## 先修要求

学习本课程需要扎实的算法与离散数学基础：
- **MIT 6.1220 / 6.046**：算法设计与分析（渐近符号、分治、动态规划、贪心、基础图算法）
- **MIT 6.041 / 18.600**：概率统计与随机过程（条件概率、期望线性性、Markov 不等式、Chernoff 界）
- **MIT 6.1200 / 6.042**：计算机科学离散数学（图论、组合数学、模运算与数论基础）

## 讲义模块索引

本课程高级数据结构专题讲义完整涵盖了经典理论算法体系：

| 讲义 | 核心主题 | 关键技术点 | 核心理论收益 |
| :--- | :--- | :--- | :--- |
| [Lec 1 全域哈希与完美哈希](./lec1.md) | Universal & Perfect Hashing | 2-universal 哈希族、二次探测、FKS 两级完美哈希 | 期望 $O(1)$ 查找与最坏 $O(1)$ 查找 |
| [Lec 2 Fibonacci 堆与均摊分析](./lec2.md) | Fibonacci Heaps & Amortization | 惰性合并、级联剪切（Cascading Cut）、势能法 | Insert/Decrease-Key 均摊 $O(1)$，加速 Dijkstra |
| [Lec 3 持久化数据结构与平面点定位](./lec3.md) | Persistent Data Structures | 路径复制、胖节点（Fat Nodes）、节点复制法 | $O(\log n)$ 历史点定位，$O(1)$ 均摊更新空间 |
| [Lec 4 伸展树与自调整二叉树](./lec4.md) | Splay Trees & Self-Adjusting Trees | 双旋转（zig-zig, zig-zag）、访问引理、静态最优性 | 无平衡因子，均摊 $O(\log n)$，自适应热点访问 |
| [Lec 5 单调优先队列与多级桶](./lec5.md) | Monotone Priority Queues & Dial's Algo | 单调性、Dial 算法、两级桶、Denardo-Fox 惰性字典树 | 小整数边权下 Dijkstra 降至 $O(m + n\log C / \log\log C)$ |
| [Lec 6 整数优先队列与基数堆](./lec6.md) | Integer Priority Queues & Radix Heaps | 全域分治、vEB 树递归缩减、基数堆（Radix Heaps） | 整数全域下 $O(\log\log U)$ 检索与 $O(m + n\log C)$ 最短路 |

## 作业与参考资料

### 配套作业（Problem Sets）

课程归档了经典课后作业题（PDF 格式）：
- [Problem Set 1 (Pset1.pdf)](./Pset1.pdf)
- [Problem Set 2 (Pset2.pdf)](./Pset2.pdf)
- [Problem Set 3 (Pset3.pdf)](./Pset3.pdf)
- [Problem Set 4 (Pset4.pdf)](./Pset4.pdf)
- [Problem Set 5 (Pset5.pdf)](./Pset5.pdf)

### 经典文献与经典教材

- **经典论文**：
  - Carter, J. L., & Wegman, M. N. (1979). *Universal classes of hash functions*. JCSS.
  - Fredman, M. L., Komlós, J., & Szemerédi, E. (1984). *Storing a sparse table with $O(1)$ worst case access time*. JACM (FKS Hashing).
  - Fredman, M. L., & Tarjan, R. E. (1987). *Fibonacci heaps and their uses in improved network optimization algorithms*. JACM.
  - Sleator, D. D., & Tarjan, R. E. (1985). *Self-adjusting binary search trees*. JACM (Splay Trees).
  - Driscoll, J. R., Sarnak, N., Sleator, D. D., & Tarjan, R. E. (1989). *Making data structures persistent*. JCSS.
  - van Emde Boas, P. (1977). *Preserving order in a forest in less than logarithmic time and linear space*. Information Processing Letters.
- **推荐参考教材**：
  - Cormen, Leiserson, Rivest, and Stein. *Introduction to Algorithms* (CLRS). MIT Press.
  - Robert E. Tarjan. *Data Structures and Network Algorithms*. SIAM, 1983.
  - Ahuja, Magnanti, and Orlin. *Network Flows: Theory, Algorithms, and Applications*. Prentice Hall, 1993.
  - Motwani and Raghavan. *Randomized Algorithms*. Cambridge University Press, 1995.
