---
title: '近似算法 III：半正定规划松弛与 Goemans-Williamson 算法 (Approximation III: SDP)'
type: lecture
lecture: 23
tags: [sdp-relaxation, max-cut, goemans-williamson, unique-games-conjecture, hyperplane-rounding]
status: complete
---

# Lec 23 近似算法 III：半正定规划松弛与 Goemans-Williamson 算法 (Approximation III: SDP)

> MIT 15.083 / 6.859J 整数规划与组合优化 · 讲义 23 · 授课教师：Prof. Dimitris Bertsimas

## TL;DR

- 半正定规划松弛（SDP Relaxation）将离散二值标量提升为高维欧氏球面单位向量。
- GW 算法利用均匀随机超平面切割，以 0.878567 近似比攻克 NP-hard 最大割难题。
- 唯一博弈猜想（UGC）确立了 0.878 是多项式时间逼近最大割的终极理论数学极限。

## 1. 突破线性的天花板：半正定松弛（SDP Relaxation）

在第 21-22 讲中，所有的近似算法都建立在线性规划（LP）松弛之上。然而，许多极其本质的图论与组合优化问题（如最大割 Max-Cut、图最大割二分划分、布尔 2-SAT），其核心驱动力是两两节点之间的**二次非凸交互项（Quadratic Interaction $x_i x_j$）**。

如果强行用线性不等式去包络这些二次项，松弛多面体将极其虚弱。
1995 年，米歇尔·戈曼斯（Michel Goemans）与大卫·威廉姆森（David Williamson）在 ACM STOC 会议上发表了被誉为 20 世纪理论计算机科学最高皇冠的论文，开创了**半正定规划松弛（SDP Relaxation）**时代。

考虑经典的 NP-hard **图最大割问题（Max-Cut Problem）**：
给定无向图 $G = (V, E)$，边权 $w_{ij} \ge 0$。寻找一个割集，使得被割开的边权重之和最大：
$$\max \quad \frac{1}{2} \sum_{(i, j) \in E} w_{ij} (1 - y_i y_j) \quad \text{s.t.} \quad y_i \in \{-1, +1\}, \quad \forall i \in V$$

```mermaid
flowchart TD
    subgraph GW_Architecture [Goemans-Williamson 算法三部曲]
        Discrete[1. 离散二次规划: y_i in {-1, +1} NP-hard] --> Lifting[向量升维松弛: y_i 升为球面单位向量 v_i in S^n-1]
        Lifting --> SolveSDP[2. 求解半正定规划 SDP: 内点法在多项式时间内求得 Gram 矩阵 X*]
        SolveSDP --> Hyperplane[3. 几何随机超平面切割: 生成各向同性高斯向量 r ~ N(0, I)]
        Hyperplane --> Output[输出离散割: sign(r^T v_i) 保证 0.878567 近似比!]
    end
```

## 2. 向量升维与随机超平面舍入（Random Hyperplane Rounding）

GW 算法的核心魔术分为两步：

### 第一步：从一维标量到高维单位向量
将一维离散变量 $y_i \in \{-1, +1\}$，松弛为 $n$ 维欧氏空间中的**单位球面向量（Unit Vectors $v_i \in \mathbb{R}^n$, $\|v_i\|_2 = 1$）**！
原问题松弛为：
$$\max \quad \frac{1}{2} \sum_{(i, j) \in E} w_{ij} (1 - v_i^T v_j) \quad \text{s.t.} \quad \|v_i\|_2^2 = 1, \quad \forall i \in V$$
令格拉姆矩阵 $X_{ij} = v_i^T v_j$。由于矩阵正半定性与向量内积的完全等价性，这等价于一个**标准的半正定规划（SDP）**：
$$\max_{X \succeq 0} \quad \frac{1}{2} \sum_{(i, j) \in E} w_{ij} (1 - X_{ij}) \quad \text{s.t.} \quad X_{ii} = 1, \quad \forall i \in V$$
利用我们在 15.084J 第 14-15 讲学到的内点法，这个 SDP 可以在多项式时间内解出高精度的最优向量解集合 $\{v_1^*, \dots, v_n^*\}$！

### 第二步：各向同性随机超平面切割
如何将这组漂浮在 $n$ 维球面上的向量，重新拍扁还原为 $\{-1, +1\}$ 的离散标签？
从多元正态分布 $\mathcal{N}(0, I_n)$ 中独立采样一个随机向量 $r \in \mathbb{R}^n$。
向量 $r$ 定义了一个通过原点的**随机超平面**，其法向量正是 $r$。
依据向量落在超平面的哪一侧，决定节点的离散归属：
$$y_i = \operatorname{sign}(r^T v_i^*) = \begin{cases} +1, & \text{若 } r^T v_i^* \ge 0 \\ -1, & \text{若 } r^T v_i^* < 0 \end{cases}$$

## 3. 0.878567 近似比的数学奇迹与 UGC 极限

两个单位向量 $v_i^*$ 和 $v_j^*$ 被随机超平面切开（即 $y_i$ 与 $y_j$ 异号）的几何概率是多少？
在由这两根向量张成的二维平面上，超平面法向量 $r$ 的投影是均匀对称的。两向量被切开的概率，**严格等于它们之间的夹角 $\theta_{ij} = \arccos(v_i^{*T} v_j^*)$ 占整个平角 $\pi$ 的比例**：
$$\Pr[y_i \ne y_j] = \frac{\theta_{ij}}{\pi} = \frac{\arccos(v_i^{*T} v_j^*)}{\pi}$$

计算输出割的数学期望权重：
$$\mathbb{E}[\text{Cost}(\text{GW})] = \sum_{(i, j) \in E} w_{ij} \Pr[y_i \ne y_j] = \sum_{(i, j) \in E} w_{ij} \frac{\arccos(v_i^{*T} v_j^*)}{\pi}$$

将其与连续 SDP 松弛上界中对应项 $\frac{1}{2} w_{ij} (1 - v_i^{*T} v_j^*) = \frac{1}{2} w_{ij} (1 - \cos \theta_{ij})$ 进行单项逐一比值放缩：

::: theorem Goemans-Williamson 近似比定理 (1995)
对于任意夹角 $\theta \in [0, \pi]$，比值函数的绝对下界为一个严格常数：
$$\alpha_{\text{GW}} = \min_{0 \le \theta \le \pi} \frac{\frac{\theta}{\pi}}{\frac{1 - \cos \theta}{2}} = \frac{2}{\pi} \min_{0 \le \theta \le \pi} \frac{\theta}{1 - \cos \theta} \approx 0.878567$$
因此，GW 算法输出的离散割权重期望，**严格保证至少达到理论最优解的 $87.8567\%$**：
$$\mathbb{E}[\text{Cost}(\text{GW})] \ge 0.878567 \cdot \text{OPT}$$
:::

更令人肃然起敬的是：苏巴什·科特（Subhash Khot）等人在 2007 年证明，在著名的**唯一博弈猜想（Unique Games Conjecture, UGC）**成立的前提下：
**$0.878567$ 是全人类在多项式时间内逼近最大割问题的绝对极限！没有任何经典算法或未来算法能够达到 $0.878568$！**

::: insight 几何直觉对离散计算的终极加冕
Goemans-Williamson 算法是整个人类应用数学历史上最美的诗篇。
当线性的割平面在复杂的二次互斥前失去光芒时，半正定规划以不可思议的魄力，将一维离散变量拔地而起，化作高维球面上自由呼吸的流线。
一道纯粹随机的几何超平面，像一道闪电划破高维夜空，将球冠的连续几何概率无损兑现为离散世界的帕累托高地。这是数学之美、算法之美与物理几何直觉的最高结合。
:::
