---
title: 6.1200J 计算机科学的数学
type: course
course: 6.1200J 计算机科学的数学
course_id: '6.1200J'
tags: [discrete-mathematics, proof, graph-theory, combinatorics, probability]
status: complete
source: https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/
---
# 6.1200J 计算机科学的数学

> 课程：MIT 6.1200J / 18.062J Mathematics for Computer Science，Spring 2024

## TL;DR

- 课程提供计算机科学所需的离散数学语言：从命题逻辑和证明出发，逐步进入渐近分析、数论、图论、计数和概率。
- 学习重点是把直觉转化为可检查的定义、命题和证明，并能识别每个结论依赖的前提。
- 笔记以官方视频 transcript 为讲授顺序，整合 lecture notes 的形式化内容；第 23 讲官方未提供 lecture notes，因此该篇明确以 transcript 为主。

## 课程定位与学习成果

这门课是算法、理论计算机、密码学和随机化方法的数学基础。完成后，应能够：

- 按命题逻辑形式选择直接证明、逆否、反证、分类或归纳；
- 使用渐近记号与递推分析算法增长率；
- 用整除性、模运算和数论定理论证基础密码方案；
- 用图、树、匹配、DAG 和关系为离散结构建模；
- 用组合计数、条件概率、期望、方差与集中不等式分析随机过程。

## 前置知识

课程从证明基础起步，不要求预先学过高级离散数学。需要熟悉中学代数，并愿意阅读和书写形式化推理。若将本课作为 [6.006 算法导论](../introduction_to_algorithms/) 的前置，建议至少完成第 1–7 讲与图论单元。

## 讲义目录

### 单元一：证明

1. [谓词、集合与证明](./lec1.md)
2. [反证法与数学归纳法](./lec2.md)
3. [分类讨论与强归纳法](./lec3.md)
4. [状态机、不变量与终止性](./lec4.md)

### 单元二：算法分析

5. [求和方法](./lec5.md)
6. [渐近分析](./lec6.md)
7. [递推关系](./lec7.md)

### 单元三：数论与密码学

8. [整除性与欧几里得算法](./lec8.md)
9. [模运算](./lec9.md)
10. [密码学](./lec10.md)

### 单元四：图论、匹配与关系

11. [图与图着色](./lec11.md)
12. [匹配与稳定匹配](./lec12.md)
13. [连通性与树](./lec13.md)
14. [有向图与 DAG](./lec14.md)
15. [关系与计数原理](./lec15.md)

### 单元五：计数

16. [计数技巧](./lec16.md)
17. [容斥、鸽巢与组合恒等式](./lec17.md)

### 单元六：概率

18. [概率论导论](./lec18.md)
19. [条件概率与 Bayes 定理](./lec19.md)
20. [独立性](./lec20.md)
21. [随机变量与概率分布](./lec21.md)
22. [期望与期望的线性](./lec22.md)
23. [期望的应用与方差](./lec23.md)（官方无 lecture notes，依 transcript 整理）
24. [大偏差界：Markov、Chebyshev 与 Chernoff 界](./lec24.md)

## 来源与整合规则

- [课程主页](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/)
- [课程视频与 transcripts](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/resources/lecture-videos/)
- [Lecture notes](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/resources/lecture-notes/)
- [官方指定阅读篇章](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/pages/readings/)
- [Mathematics for Computer Science 教材（PDF）](https://courses.csail.mit.edu/6.042/spring18/mcs.pdf)

视频 transcript 用于恢复讲师如何引入问题、解释直觉、处理学生疑问和连接例子；lecture notes 用于校准定义、公式、定理条件与书面证明。两者不一致时，正文应显式区分讲授直觉与形式陈述，不把口语化简写当作定理。
