---
title: '松弛求解算法：次梯度优化、束方法与乘子调整 (Algorithms for Relaxations)'
type: lecture
lecture: 10
tags: [subgradient-optimization, bundle-methods, dual-multipliers, cutting-planes]
status: complete
---

# Lec 10 松弛求解算法：次梯度优化、束方法与乘子调整 (Algorithms for Relaxations)

> MIT 15.083 / 6.859J 整数规划与组合优化 · 讲义 10 · 授课教师：Prof. Dimitris Bertsimas

## TL;DR

- 拉格朗日对偶函数是分段线性凹函数，在拐点处处不可微，传统微积分彻底失效。
- 经典 Polyak 次梯度步长规则以几何级数逼近对偶最优值，收敛受制于之字震荡。
- 束方法（Bundle Methods）利用历史次梯度切平面构建局部二次近端模型，实现稳定高阶收敛。

## 1. 对偶函数的非光滑地貌与次梯度提取

在第 9 讲中，我们构建了拉格朗日对偶函数：
$$L(\lambda) = \min_{x \in X} \left\{ c^T x + \lambda^T (b - A x) \right\}$$
为了获得最紧致的下界，我们必须最大化 $L(\lambda)$（$\max_{\lambda \ge 0} L(\lambda)$）。

然而，由于集合 $X$ 是离散点集，其极点数量有限，设为 $\{x^1, \dots, x^K\}$。
对偶函数 $L(\lambda)$ 本质上是有限个关于 $\lambda$ 的仿射函数的逐点极小值：
$$L(\lambda) = \min_{k=1,\dots,K} \left\{ c^T x^k + \lambda^T (b - A x^k) \right\}$$
它是一个**典型的分段线性凹函数（Piecewise Linear Concave Function）**！在多面体面与面的交界脊线上，函数导数发生突变，存在尖锐的折角与不可微断裂。

幸运的是，提取次梯度极其廉价：
设在当前乘子 $\lambda_k$ 下，子问题求得的最优整数解为 $x^*(\lambda_k) \in X$。
则根据次梯度公理，向量：
$$g_k = b - A x^*(\lambda_k)$$
**百分之百精确构成了函数 $L(\cdot)$ 在点 $\lambda_k$ 处的一个合法次梯度（Subgradient）！**
物理含义直截了当：$g_k$ 正是当前解对耦合硬约束的**资源违反残差量（Constraint Violation）**！

```mermaid
flowchart TD
    subgraph SubgradientLoop [次梯度对偶乘子更新循环]
        Lambda[当前乘子 lambda_k] --> SolveSub[求解离散子问题: x*(lambda_k) in X]
        SolveSub --> Residual[计算约束违规残差: g_k = b - A x*]
        Residual --> PolyakStep[Polyak 步长法则: s_k = gamma_k * (z_UB - L(lambda_k)) / ||g_k||^2]
        PolyakStep --> Update[投影更新: lambda_k+1 = max(0, lambda_k + s_k * g_k)]
        Update --> Check{步长或对偶间距收敛?}
        Check -- 否 --> Lambda
        Check -- 是 --> Done[输出高精度拉格朗日最优下界]
    end
```

## 2. Polyak 次梯度步长规则（Polyak's Step-Size Rule）

在第 15.084J 第 22 讲中，我们看到标准次梯度法通常采用递减步长 $\alpha_k = 1/k$，收敛速度极慢。
鲍里斯·波利亚克（Boris Polyak）利用目标函数已知的上界估计，提出了现代运筹学通用的**Polyak 步长法则**：

设 $z_{\text{UB}}$ 为当前通过任意启发式算法已知的全局最优目标函数**上界（Incumbent Upper Bound）**。
定义第 $k$ 步的迭代步长为：
$$s_k = \gamma_k \frac{z_{\text{UB}} - L(\lambda_k)}{\|g_k\|_2^2}, \quad \text{其中 } \gamma_k \in (0, 2)$$
乘子更新方程为非负投影：
$$\lambda_{k+1} = \max\left( 0, \; \lambda_k + s_k g_k \right)$$

参数 $\gamma_k$ 遵循阻尼递减策略：从 $\gamma = 2$ 开始；若在连续 $N$ 轮（如 $N=10$）迭代中对偶目标 $L(\lambda)$ 未能取得实质性改善，则将参数减半：$\gamma \leftarrow \gamma / 2$。
Polyak 步长直接将收敛速度从龟速的次线性推升至极其实用的**拟几何收敛（Geometric Convergence）**！

## 3. 彻底克服之字震荡：束方法（Bundle Methods）

尽管 Polyak 次梯度法非常直观，但它有一个顽固的工程缺陷：每一步迭代只保留**当前的单一瞬时次梯度 $g_k$**，完全丢失了历史信息。在狭窄尖锐的折叠山脊处，乘子向量会在山脊两侧以接近 180 度的反向做剧烈的“之字形横跳”，导致迭代步长急剧萎缩。

为了终结这一病态，数学家克劳德·勒马雷夏尔（Claude Lemaréchal）在 20 世纪 70 年代提出了高级的**束方法（Bundle Methods）**。

其核心机制是：**在内存中维护一个“次梯度束（Bundle）”，汇聚过去走过的所有历史切平面：**
$$\mathcal{B}_k = \left\{ (x^j, g_j, L(\lambda_j)) \;\middle|\; j \in J_k \right\}$$
利用这个束，在当前最佳中心点 $\hat{\lambda}$ 附近构建由这些切平面交织而成的局部模型：
$$\check{L}_k(\lambda) = \min_{j \in J_k} \left\{ L(\lambda_j) + g_j^T (\lambda - \lambda_j) \right\}$$

在每一步迭代中，束方法求解一个带近端二次正则项（Proximal Term）的平滑凸二次规划（QP）：
$$\lambda_{k+1} = \arg\max_{\lambda \ge 0} \left\{ \check{L}_k(\lambda) - \frac{\rho_k}{2} \|\lambda - \hat{\lambda}\|_2^2 \right\}$$

二次正则项强制算法绝不盲目跳跃，切平面包络让算法在多个方向之间做平滑加权。束方法彻底消除了次梯度的震荡灾难，成为了高精度非光滑对偶优化的工业黄金标杆。

::: insight 历史信息的积累是对抗非光滑性的唯一武器
非光滑函数的本质是信息的突然断裂。
单步次梯度法像一个健忘的探险者，在悬崖两边反复碰壁；而束方法把每一次碰壁的历史切平面全部完整记忆在“束（Bundle）”中，并在内存中逐渐拼装出周围地形的局部全景凸模型。
用二次近端项限制冲动，用历史割平面导航未来，这正是高级运筹算法在混沌非光滑曲面上行稳致远的最高智慧。
:::
