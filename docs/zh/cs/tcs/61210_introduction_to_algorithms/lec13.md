---
title: "Dijkstra 算法"
type: lecture
lecture: 13
tags: [dijkstra, shortest-path, greedy-algorithm]
status: complete
source: https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-13-dijkstra/
---
# Lec 13 Dijkstra 算法

> 资料依据：[课程视频与 transcript](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-13-dijkstra/) · [Lecture notes](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/mit6_006s20_lec13/)

## TL;DR

- Dijkstra 算法适用于边权非负的图，每次从未定型顶点中选择当前距离估计最小者。
- 非负性保证：最小估计顶点不可能再通过其他未定型顶点获得更短路径，因此贪心选择可以安全定型。
- 用二叉堆实现优先队列时，算法运行时间为 $O((|V|+|E|)\log |V|)$，稀疏图中可写作 $O(|E|\log |V|)$。

## 非负权重边

- 思路： 将 BFS 的方法推广到加权图
  - 以源点 s 为中心扩展球面
  - 反复搜索更近的顶点，然后再搜索更远的顶点
  - 但如果事先不知道距离，如何搜索更近的点？
- 观察 1： 如果权重非负，则沿着最短路径的距离单调增加
  - 即，如果顶点 u 出现在 s 到 v 的最短路径上，则$\delta(s, u) \le \delta(s, v)$
  - 设 $V_x \subset V$ 是从 s 出发可到达的距离 $\le x$ 的顶点子集（分层子集）
  - 如果$v \in V_x$，则从 s 到 v 的任何最短路径经过的顶点都在$V_x$内
  - 或许可以一次扩展一个顶点来增长$V_x$（ 但是如果权重很大，为每个 x 扩展会很慢）
- 观察 2： 如果给定从 s 出发按距离递增顺序排列的顶点，可以快速解决 SSSP 问题
  - 移除违反此顺序的边（因为有些边不能参与最短路径）
  - 如果存在零权重边，可能仍然会有环： 反复合并成单个顶点
  - 使用 DAG 松弛法在 O(|V| + |E|)时间内计算出每个$v\in V$的$\delta(s, v)$

## Dijkstra’s 算法

- 思路： 从源点 s 出发到各顶点的距离递增顺序松弛边

- 如何做到按距离递增？ 用一种数据结构能有序地找到下一个顶点，比如 **可变优先队列**Q，其数据项带有键和唯一 ID，支持的操作有

  | 操作                    | 描述                                     |
  | ----------------------- | ---------------------------------------- |
  | `Q.build(X)`            | 用迭代器 `X` 中的项初始化 `Q`            |
  | `Q.delete_min()`        | 删除键最小的项                           |
  | `Q.decrease_key(id, k)` | 找到具有ID `id` 的存储项并将键更改为 `k` |

- 通过交叉链接（cross-linking）优先队列 Q'和一个字典 D 将 ID 映射到 Q‘中

- 假设顶点是 ID 从 0 到 |V| -1 的证书，因此可以使用直接访问数组来实现字典 D

- 为了简洁起见，假设数据项 x 是一个元祖（x.id, x.key）

## 我的理解

::: insight
Dijkstra 不是“更快的 Bellman–Ford”，而是以非负边权为交换条件，获得了一个更强的贪心不变量。一条负边就可使“定型后永不更改”的论证失效。
:::
