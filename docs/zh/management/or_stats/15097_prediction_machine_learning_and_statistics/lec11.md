---
title: '机器学习中的凸优化技术：梯度下降与近端算子 (Convex Optimization for Machine Learning)'
type: lecture
lecture: 11
tags: [convex-optimization, gradient-descent, sgd, proximal-gradient]
status: complete
---

# Lec 11 机器学习中的凸优化技术：梯度下降与近端算子 (Convex Optimization for Machine Learning)

> MIT 15.097 统计与机器学习前沿研讨 (Prediction: Machine Learning and Statistics) · 授课教师：Prof. Roy Welsch

## TL;DR

- 凸优化构成了几乎所有现代监督学习模型（SVM、逻辑回归、稀疏正则化）的底层求解引擎。
- 随机梯度下降（SGD）以单样本无偏梯度估计打破海量大数据的内存与算力天花板。
- 近端梯度法（Proximal Gradient Method）通过近端算子（Proximal Operator）完美攻克非光滑 $L_1$ 正则化稀疏求解。

## 优化算法：机器学习的幕后引擎

在机器学习的教科书与论文中，研究者常常热衷于讨论目标函数、概率图与网络拓扑。
然而，一位清醒的工业算法工程师必须深刻认识到：
**任何一个机器学习模型被设计出来之后，只要它还没有被求解出来，它就只是一堆写在纸上的废纸！**
从逻辑回归的交叉熵、支持向量机的二次规划、到深度神经网络的反向传播，连接数学模型与最终预测能力的唯一桥梁，正是**数值凸优化算法（Convex Optimization Algorithms）**。

麻省理工学院 15.097 第十一讲，系统梳理从**一阶梯度下降**、**随机梯度下降（SGD）**到现代**非光滑近端算子（Proximal Operators）**的技术全貌。

## 批量梯度下降与收敛性分析 (Batch Gradient Descent)

考虑无约束凸极小化问题：
$$
\min_{w \in \mathbb{R}^d} \quad f(w) = \frac{1}{n}\sum_{i=1}^n f_i(w)
$$
标准**批量梯度下降（Batch Gradient Descent, BGD）**的迭代格式为：
$$
w_{k+1} = w_k - \eta_k \nabla f(w_k) = w_k - \frac{\eta_k}{n}\sum_{i=1}^n \nabla f_i(w_k)
$$
其中 $\eta_k > 0$ 为步长（学习率 Learning Rate）。

::: theorem [Lipschitz 光滑条件下的收敛率定理]
若目标函数 $f(w)$ 是凸函数，且梯度满足 $L$-Lipschitz 连续性（即 $\|\nabla f(x) - \nabla f(y)\| \le L \|x - y\|$，意味着曲率有界）：
当固定学习率取值 $\eta \le \frac{1}{L}$ 时，梯度下降法保证目标函数单调递减，且经过 $k$ 步迭代后满足次线性收敛率：
$$
f(w_k) - f(w^*) \le \frac{L \|w_0 - w^*\|_2^2}{2 k} \sim \mathcal{O}\left(\frac{1}{k}\right)
$$
若 $f(w)$ 进一步满足**强凸性（Strongly Convex）**（参数为 $\mu > 0$，即下方被二次抛物线托住），则收敛速度暴增为**几何级线性收敛（Linear Convergence）**：
$$
\|w_k - w^*\|_2^2 \le \left(1 - \frac{\mu}{L}\right)^k \|w_0 - w^*\|_2^2 \sim \mathcal{O}(e^{-c k})
$$
:::

## 随机梯度下降 (Stochastic Gradient Descent, SGD)

批量梯度下降在小数据集上运行良好。然而，当样本量达到数千万（$n = 10^7$）时：
**每向前走微不足道的一小步，计算机必须强行遍历全量 1000 万个样本来计算平均梯度！**
算力开销极其恐怖，且单步迭代耗时过长。

赫伯特·罗宾斯（Herbert Robbins）与萨顿·门罗（Sutton Monro）在 1951 年创立了现代人工智能的生命线——**随机梯度下降（SGD）**：
在每一步迭代中，算法**完全不再扫描全量数据集，而是均匀随机抽取单个样本 $i \in \{1, \dots, n\}$（或极小批次 Mini-batch）**，直接以该单样本的梯度作为全局梯度的无偏估计：
$$
w_{k+1} = w_k - \eta_k \nabla f_i(w_k)
$$

```mermaid
flowchart LR
    A["单样本随机抽取 i_k ~ Uniform(1, ..., n)"] --> B["计算瞬时单样本梯度: g_k = ∇ f_{i_k}(w_k)"]
    B --> C["验证数学无偏性: E[g_k | w_k] = ∇ f(w_k)"]
    C --> D["单步纳秒级快速参数更新: w_{k+1} = w_k - η_k g_k"]
    D --> E["参数轨迹剧烈高频震荡但宏观逼近极值谷底！"]
```

由于 $\mathbb{E}_{i}[\nabla f_i(w)] = \nabla f(w)$，单样本梯度的数学期望严格等于真实全局梯度。
尽管单步更新带有巨大的随机方差扰动（轨迹呈现剧烈锯齿漫步），但只要学习率满足经典的 **Robbins-Monro 条件**：
$$
\sum_{k=1}^\infty \eta_k = \infty \quad \text{且} \quad \sum_{k=1}^\infty \eta_k^2 < \infty \quad (\text{如取 } \eta_k = \mathcal{O}(1/k))
$$
**随机梯度下降几乎必然（a.s.）收敛至全局真实最优解！**
单步计算复杂度从 $\mathcal{O}(n d)$ 彻底降维至常数 $\mathcal{O}(d)$，使得算法能够在大数据洪流中秒级吞吐流式数据。

## 非光滑复合优化与近端梯度法 (Proximal Gradient Method)

在现代高维特征选择与稀疏学习中，我们经常使用 **Lasso 正则化（$L_1$ 范数惩罚）**：
$$
\min_{w} \quad F(w) = g(w) + h(w) = \frac{1}{2n}\|X w - y\|_2^2 + \lambda \|w\|_1
$$
此时遇到了巨大的数学障碍：
前项 $g(w)$ 是光滑可微的，但正则项 $h(w) = \lambda \sum |w_i|$ 在坐标轴零点处**存在尖锐的折角，处处不可导！**
传统的梯度下降在此处彻底瘫痪。如果直接忽略折角强行用次梯度法，其收敛速度会从 $\mathcal{O}(1/k)$ 暴跌至极其缓慢的 $\mathcal{O}(1/\sqrt{k})$，且几乎永远无法产生真正的纯稀疏零系数。

近端梯度法（Proximal Gradient Method / ISTA / FISTA）给出了极其优美的破局方案。

::: definition [近端算子 (Proximal Operator)]
对于闭凸非光滑函数 $h(x)$ 与标量 $\gamma > 0$，定义其**近端算子**为：
$$
\text{prox}_{\gamma h}(v) = \arg\min_{x \in \mathbb{R}^d} \left\{h(x) + \frac{1}{2\gamma}\|x - v\|_2^2\right\}
$$
几何意义：在非光滑惩罚项 $h(x)$ 与锚点 $v$ 的邻近距离之间做最佳折中。
:::

::: theorem [软阈值算子与 L1 近端解 (Soft-Thresholding)]
当非光滑项为 $L_1$ 范数 $h(x) = \lambda \|x\|_1$ 时，其近端算子具有完全解耦的**闭式解析软阈值收缩公式**：
$$
\left(\text{prox}_{\gamma \lambda \|\cdot\|_1}(v)\right)_i = \mathcal{S}_{\gamma \lambda}(v_i) = \text{sign}(v_i) \max\left(0, |v_i| - \gamma \lambda\right)
$$
:::

### 近端梯度法两步迭代全景
1. **第一步（光滑前向梯度步）**：沿着可微项 $g(w)$ 的负梯度走一步：$v_k = w_k - \eta \nabla g(w_k)$；
2. **第二步（非光滑近端后向映射）**：通过软阈值算子将 $v_k$ 向零点收缩截断：
$$
w_{k+1} = \text{prox}_{\eta h}(v_k) = \mathcal{S}_{\eta \lambda}\left(w_k - \eta \nabla g(w_k)\right)
$$
凡是绝对值低于阈值 $\eta \lambda$ 的微小系数，在这一步被**硬生生干净利落地直接置零（Exact Sparsity）**！
通过结合 Nesterov 加速动量（FISTA 算法），非光滑凸优化的收敛速度被奇迹般地重新拉回至理论最高极限 $\mathcal{O}(1/k^2)$！

::: pitfall 随意设置固定的过大步长导致算法发散
在复合优化中，步长 $\eta$ 必须严格小于光滑部分 Lipschitz 常数的倒数 $1/L$。若 $L$ 难以解析预先计算，必须采用回溯线搜索（Backtracking Line Search），否则目标函数值会在后期发生灾难性的发散爆炸。
:::

::: insight 近端算子是化解不可导折角的太极云手
面对不可导的折角，强行求导如同用蛮力撞墙；
而近端算子展现了现代凸分析的深厚内功：**它通过在局部引入一个微小的二次距离弹簧，将尖锐的非光滑断崖，转化为一个无限温和光滑的近端点折中**。在这张一弛之间，算法既享受了梯度的飞速前进，又获得了最纯粹的稀疏模型结构。
:::
