---
title: "动态规划 II：LCS、LIS 与硬币游戏"
type: lecture
lecture: 16
tags: [dynamic-programming, longest-common-subsequence, longest-increasing-subsequence, game-theory]
status: complete
source: https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-16-dynamic-programming-part-2-lcs-lis-coins/
---
# Lec 16 动态规划 II：LCS、LIS 与硬币游戏

> 资料依据：[课程视频与 transcript](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-16-dynamic-programming-part-2-lcs-lis-coins/) · [Lecture notes](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/mit6_006s20_lec16/)

## TL;DR

- 最长公共子序列用两个后缀索引描述状态；当首元素相等时同时前进，否则在丢弃任一序列首元素之间取最优。
- 最长递增子序列需要把“必须选当前元素”编入子问题，否则状态不足以判断下一个元素能否接入。
- 交替硬币游戏可显式加入当前玩家状态，也可利用零和性把对手收益改写为总和减去己方收益。

## 本讲导览

- 最长公共子串（LCS，Longest Common Subsequence）
- 最长增长子串（LIS，Longest Increasing Subsequence ）
- 交替硬币游戏（Alternating coin game）

## 最长公共子串（LCS）

给定两个系列 A & B，找到最大的公共子串（无需要连续）

Ex： Hieroglyphology 和 Michelangelo，其 LCS 为 hello 或者是 heglo 或 iello 或者 ieglo，长度都是 5

- **S**ubproblem

  - $L(i, j) = LCS(A[i:], B[j:]) \text{ for }0 <= i <= | A |, 0 <= j <= |B|$

- **R**elate:

  - 首字母要么匹配，要么不匹配

  - 如果首字母匹配，则某个 LCS 会使用它们

  - 如果某个 LCS 使用了 A[i] 的第一个字符，而没有使用 B[j] 的第一个字符，匹配 B[j] 也是最优的

  - 如果它们不匹配，它们不能同时出现在最长公共子序列中

    **猜测**A[i]和 B[j]其中有一个不在 LCS 中
    $$
    L(i, j) = 
    \begin{cases}
    L(i+1, j+1) + 1 \text{  if A[i] = B[j]} \\
    \max \left\{L(i+1, j), L(i, j+1)\right\}  \text{  其他}
    \end{cases}
    $$

- **T**opo

  - 逐步减小 ``i+j``
  - 可以通过 bottom-up 方法： 先减小``i``，再减小``j``

- **B**ase

  - $L(|A|, j) = 0 = L( i, |B| )$ （其中有一个字符串为空）

- **O**riginal

  - 最长公共子序列为 L(0, 0)
  - 保存父指针用于重构序列
  - 如果父指针同时增加索引值，则将该字符添加到 LCS 中

- **T**ime

  - 子问题数目： (|A| + 1) · (|B| + 1)
  - 每个子问题的工作量：O(1)
  - 总共的运行时间 $O(|A|·|B|)$

**LCS 子问题 DAG**

![动态规划 II：LCS、LIS 与硬币游戏图示 1](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/666d5b886cbe8.png)

（边缘的是 Base case， 每个节点都是一个子问题，对应于什么是最长公共子序列，比如（3，2）这个点而言， 子问题就是 EIR 和 ABIT 的 LCS 是什么？箭头是父指针）

```python
def lcs(A, B):
  a, b = len(A), len(B)
  x = [[0] * (b+1) for _ in range (a+1)]
  for i in reversed(range(a)):
    for j in reversed(range(b)):
      if A[i] == B[j]:
        x[i][j] = x[i+1][j+1] + 1
      else:
        x[i][j] = max(x[i+1][j], x[i][j+1])
  return x[0][0]
```

## 最长增长子序列（LIS）

问题描述： 给定长度为 n 的序列 A，找到一条最长（可不连续）字母严格递增的子序列，即 LIS(A)

Ex: CARBOHYDRATE ==> ABORT

尝试的解决方案：

- 子问题自然是 A 的前缀或者后缀，以后缀为例 A[i:]
- 一个很自然的的问题是 A[i]是否在 LIS 中？（需要进行分支）
- 但是，如何在 A[i+1:]上递归并保证是递增子序列呢？
- 修正：给子问题添加**约束**，提供足够的结构来实现递增性

SRTBOT 分析：

- **S**ubprobs
  - 令 L(i) = 后缀$A[i:]$最大递增子序列的长度，即$LIS(A[i:])$，其中 $0\le i \le |A|$
  - 约束: 以 A[i]为开始（也就是说 A[i]在最大递增子序列里面）
- **R**elate
  - 已知第一个元素是 A[i]，那么第二个元素是哪个呢？
    - 可以是任何$A[j]\text{，其中} j  > i \text{ 且 } A[j] > A[i]$ ，
    - 也可能 A[i]是 LIS 最后一个元素
  - $L(i) = 1 + \max \left\{L(j) | i < j < n, A[i] < A[j]\right\} ∪ \left\{0\right\}$
  - 错误的思路： 我们思考 i 是不是在 LIS 当中，在和不在分别讨论。第一反应是 L(i) =  max{L(i+1), 1+L(i+1)}， 因为这是子问题约束的关系
- **T**opo order
  - for  i = |A|, ..., 0
- **B**ase:
  - 无需，因为我们考虑的就是 A[i]就是最后一个 LIS 元素
- **O**riginal:
  - 那个是 LIS 的第一个元素呢？ **靠猜**
  - 我们 LIS(A)的长度为$\max \left\{L(i) | 0\le i\le|A|\right\}$
  - 需要存储子问题父指针来重构序列
- **T**ime:
  - 子问题个数： θ(|A|)
  - 每个子问题的工作量： O(|A|)
  - 总的时间复杂度：$O(|A|^2)$

> 练习题：  加速到$O(|A|\log{|A|})$完成，通过将每个子问题的工作量减到$O(\log{|A|})$ ，提示 AVL 增强树

我们用了两次暴力解法， 一个是求以 i 为开头的的 LIS，第二个是，我们选择了 j 暴力尝试所有可能。

**LIS 子问题的 DAG 图**

![动态规划 II：LCS、LIS 与硬币游戏图示 2](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/666e9fbdbde9f.png)

```python
def lis(A):
  a = len(A)
  l = [1] * a
  for i in reversed(range(a)):
    for j in range(i, a):
      if A[j] > A[i]:
        x[i] = max(x[i], 1+x[j])
  return max(x)
```

## 交替硬币游戏

给定一系列 n 个硬币，其价值为 $v_0, ... v_{n-1}$，两个玩家轮流拿硬币，每轮可以从剩下的硬币中取第一个或者最后一个硬币，我的目标最大化我拿到的硬币总价值，我先开始。

### 方案一： 子问题扩展

子问题扩展， subproblem expansion 的 SRTBOT 分析：

- **S**ubprobs:   $X(i, j, p)$ = 我能在 $v_i, .... , v_j$拿到的最高值硬币, p 代表是你还是我
- **R**elate:  
  - 玩家 p 必须选择 第$i$ 个或者 $j$ 个硬币（需要猜！）
  - 如果 p=me， 那么我将得到那个值，否则什么都没得到
  - 然后轮到另外一个玩家
  - $X(i, j, me) = \max \left\{X(i+1, j, u) + v_i, X(i, j-1, u) + v_j\right\}$
  - $X(i, j , u) = \min \left\{X(i+1, j, me), X(i, j-1, me)\right\}$
- **T**opo:  增大  ``j-i``
- **B**ase:
  - $X(i, i, me) = v_i$
  - $X(i, i, u) = 0$
- Original problems:
  -  $X(0, n-1, me)$
  -  保存父指针来重构策略
- **T**ime analysis:
  - 子问题个数： $\Theta(n^2)$
  - 每个子问题的工作量: $\Theta(1)$
  - 总共时间复杂度: $\Theta(n^2)$

**子问题 DAG**

![动态规划 II：LCS、LIS 与硬币游戏图示 3](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/666ea842acaff.png)

以上，叫**子问题扩展**

### 方案二： 零和博弈

零和博弈：我拿走所有你不拿的硬币，没有合作关系

- **S**ubproblems:
  - $x(i, j) =$ 我能拿到的最大分数，在基于硬币 $v_i, ...,v_j$的情况下
  - 其中 $0\le i \le j \lt n$
- **R**elate
  - 我必须选择要么是第 i 个 要么是第 j 个
  - 因此，你能够获得 $x(i+1, j)$或者$x(i, j-1)$，分别对应于我选择硬币 i 或 j
  - 为了计算我能获得的价值，从总硬币值中减去这一部分
  - $x(i, j) = \max \left\{v_i + \sum^j_{k=i+1} v_k - x(i+1, j), v_j+\sum_{k=i}^{j-1}v_k-x(x, j-1)\right\}$
- **T**opo order
  - 逐步增大 ``j-i``
- **B**ase
  - $x(i, i) = v_i$
- **O**riginal
  - $x(0, n-1)$
  - 存储父指针
- **T**ime Analysis
  - 子问题数目 $\Theta(n^2)$
  - 每个子问题的工作量 $\Theta(n)$，计算总和
  - 运行时间为 $\Theta(n^3)$

**子问题 DAG**

![动态规划 II：LCS、LIS 与硬币游戏图示 4](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/666ea862d10b2.png)

> 练习题： 将复杂度提升到$\Theta(n^2)$，通过以$\Theta(n^2)$时间内预处理所有和$\sum^j_{k=i}v_k$

## 我的理解

::: insight
LIS 的状态设计展示了一个通用技巧：当“可行的未来”取决于历史中某个边界值时，把该边界值或其索引放进状态，就能恢复无后效性。
:::
