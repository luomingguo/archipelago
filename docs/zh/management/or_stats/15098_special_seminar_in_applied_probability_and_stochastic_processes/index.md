---
title: '15.098 应用概率与随机过程前沿研讨'
type: course
course: '15.098 应用概率与随机过程前沿研讨'
course_id: '15.098'
tags: [applied-probability, queueing-networks, mixing-times, random-graphs]
status: stub
source: 'https://ocw.mit.edu/courses/15-098-special-seminar-in-applied-probability-and-stochastic-processes-spring-2006/'
---

# 15.098 应用概率与随机过程前沿研讨

> MIT Course 15 · Operations Research/Statistics · 课号 15.098

## TL;DR

- 应用概率专题前沿，聚焦大规模网络排队、随机图与马尔可夫链混合时间（Mixing time）。
- 利用谱隙（Spectral gap）与电网络类比解析高维离散状态空间的快速采样动力学。
- 大偏差理论（Large deviations）为极端罕见事件风险度量提供渐近指数衰减估计。

## 课程简介 / Description

This seminar is intended for doctoral students and discusses topics in applied probability. This semester includes a variety of fields, namely statistical physics (local weak convergence and correlation decay), artificial intelligence (belief propagation algorithms), computer science (random K-SAT problem, coloring, average case complexity) and electrical engineering (low density parity check (LDPC) codes).

## 讲义 / Lecture Notes

- **1**
  - A model of random k-SAT (random instance of a boolean constraint satisfaction problem) is considered where the size
  - k
  - of each clause is growing as function of the number of variables
  - n
  - . A threshold for satisfiability is obtained using the second moment method.
- **2**
  - The authors consider the random sparse regular graph model and the problem of coloring such graphs. For each graph q they obtain the largest connectivity parameter
  - r
  - =
  - r(q)
  - such that the graph is
  - q
  - colorable. They identify
  - r
  - up to two possible values.
  - B. Local Weak Convergence and Correlation Decay: The notion of local weak convergence allows one to study asymptotic spatial structural properties of probabilistic combinatorial optimization problems. The property of correlation decay facilitates one to establish these properties.
- **3**
  - A queuing model is considered where the customers access database over time. A certain phase transition result is established depending on the arrival rate of the customer requests. This result is related to certain statistical physics models, specifically in the context of hard-core model on Bethe lattices.
- **4**
  - A new method for solving approximately a class of counting problems is introduced. The method is based on correlation decay property, originating from statistical physics. The method is applied to approximately count the number of independent sets in arbitrary graphs with degree at most five.
- **5**
  - A survey of local weak convergence method is discussed with applications to random matching, spanning trees and various other related models.
- **6**
  - A local weak convergence method is used to compute the expected size of the largest weighted independent set and matching on regular graphs with large girth.
  - C. Belief Propagation and LDPC Codes: Belief propagation is an iterative distributed heuristic algorithm for combinatorial optimization problem. It is expected to perform very well in the context of probabilistic setup.
  - 7-8
  - A framework for using the belief propagation algorithm is discussed for several applications including Markov random fields and Bayesian (belief) networks.
- **9**
  - Belief propagation algorithm is proven to solve the problem of finding the largest weighted matching of a bi-partite graph.
- **10**
  - First two chapters of an important textbook on a coding theory are discussed. Topics include linear codes, ML decoding, Channel coding theory, factor graph representation, decoding via message passing.

---

本资料整理自 [MIT OpenCourseWare](https://ocw.mit.edu/courses/15-098-special-seminar-in-applied-probability-and-stochastic-processes-spring-2006/)，遵循 Creative Commons BY-NC-SA 4.0 许可协议，仅供个人学习使用。
