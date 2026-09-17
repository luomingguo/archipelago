---
title: 6.1210 算法导论
type: course
course: 6.1210 算法导论
course_id: '6.1210'
tags: [algorithms, data-structures, graph-algorithms, dynamic-programming, computational-complexity]
status: complete
source: https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
---
# 6.006 算法导论

> 课程：MIT 6.006 Introduction to Algorithms，Spring 2020

## TL;DR

- 课程以“正确、高效、可清楚表达”为主线，训练从计算问题、操作接口和计算模型出发设计算法。
- 内容依次覆盖序列与集合数据结构、排序、哈希、平衡树、堆、图遍历、最短路径、动态规划和复杂性。
- 笔记以视频 transcript 保留讲师的动机、例子和推理顺序，再用 lecture notes 校准定义、伪代码、正确性和复杂度。

## 课程定位与学习成果

完成课程后，应能够：

- 把实际任务抽象为输入、输出和可验证的正确性条件；
- 为序列、集合、优先队列和图选择合适表示，说明操作成本与权衡；
- 证明算法正确性，并在 Word-RAM 模型中给出渐近时间和空间界；
- 识别分治、贪心、松弛与动态规划的适用条件，而不是只记住算法名称；
- 区分多项式、伪多项式和指数时间，并用多项式时间规约比较问题难度。

## 前置知识

建议先学完 [6.1200J 计算机科学的数学](../maths_for_cs/)，或至少熟悉命题逻辑、数学归纳法、渐近记号、递推、图的基本概念与离散概率。编程不是课程主题，但需要能读懂 Python 伪代码和基本数据结构实现。

## 讲义目录

### 单元一：数据结构与排序

1. [算法与计算](./lec1.md)
2. [数据结构与动态数组](./lec2.md)
3. [排序与递归](./lec3.md)
4. [哈希](./lec4.md)
5. [线性时间排序](./lec5.md)
6. [二叉树与二叉搜索树](./lec6.md)
7. [AVL 树](./lec7.md)
8. [优先队列与二叉堆](./lec8.md)

### 单元二：图遍历与最短路径

9. [广度优先搜索](./lec9.md)
10. [深度优先搜索](./lec10.md)
11. [加权最短路径](./lec11.md)
12. [Bellman–Ford 算法](./lec12.md)
13. [Dijkstra 算法](./lec13.md)
14. [全源最短路径与 Johnson 算法](./lec14.md)

### 单元三：动态规划与复杂性

15. [动态规划 I：SRTBOT 与 DAG](./lec15.md)
16. [动态规划 II：LCS、LIS 与硬币游戏](./lec16.md)
17. [动态规划 III：APSP、括号与钢琴指法](./lec17.md)
18. [动态规划 IV：杆切割、子集和与伪多项式时间](./lec18.md)
19. [计算复杂性](./lec19.md)

## 官方资源

- [课程主页](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/)
- [课程视频与 transcripts](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/video_galleries/lecture-videos/)
- [Lecture notes](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/pages/lecture-notes/)
- [Assignments](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/pages/assignments/)
- [Practice problems](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/pages/practice-problems/)
- [Quizzes](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/pages/quizzes/)

## 阅读建议

首读时先理解每讲的 TL;DR 和核心不变量，再尝试不看正文写出操作接口、正确性论证与运行时间。仅能复述伪代码不等于掌握算法；能够说明前提失效时算法为何失效，才表明理解了边界。
