---
title: '电子商务中的动态定价与收益管理优化 (E-commerce Dynamic Pricing and Revenue Management)'
type: lecture
lecture: 15
tags: [revenue-management, dynamic-pricing, e-commerce, assortment-optimization]
status: complete
---

# Lec 15 电子商务中的动态定价与收益管理优化 (E-commerce Dynamic Pricing and Revenue Management)

> MIT 15.094J 鲁棒系统优化建模与计算 (Systems Optimization: Models and Computation) · 授课教师：Prof. Dimitris Bertsimas / Robert Freund

## TL;DR

- 现代电子商务收益管理通过需求价格弹性与有限库存时效性最大化期望总收入。
- 单资源与多网络资源定价展示了贝尔曼动态规划向确定性线性规划（DLP）的渐近转化。
- MNL 离散选择模型刻画了多品类之间的同类蚕食（Cannibalization）与产品组合推荐。

## 数字化零售的纳秒级价格博弈

在传统的实体零售业中，商品价格通常印在纸质标签上，调整一次全店商品价格需要人工耗费数天；
而在现代电子商务巨头（如亚马逊、京东、美团、Uber 与各大航司官网）的数字世界中，**价格变成了一个实时跳动的纳秒级连续控制变量**：
- 面对距离航班起飞只剩最后 48 小时的 15 张头等舱机票，系统应如何动态定价以在防止座位空置起飞与榨取高价值商旅客户之间做最佳平衡？
- 当某种爆款电子产品库存仅剩 50 件且补货周期漫长时，算法该如何随时间和需求流速调整加价阶梯？
- 当平台上展示多款相互替代的手机机型时，如何设计选品展示组合（Assortment），以防低价机型严重蚕食（Cannibalize）高毛利旗舰机型的利润？

**动态定价（Dynamic Pricing）与收益管理（Revenue Management）**构成了现代平台经济最核心的算法印钞机。

## 经典有限库存动态定价控制模型

设企业在销售季初（时刻 $t = 0$）拥有某种易腐或有限时效商品（Perishable Assets，如机票、酒店客房、时装）的物理初始库存 $C$。
销售周期长度为固定时间窗口 $[0, T]$，到期后未售出库存残值归零。
在时刻 $t$，企业展示的即时销售价格为决策变量 $p(t) \in [\underline{p}, \bar{p}]$。
市场客户的到达服从**受价格控制的非齐次泊松过程**，其瞬时购买强度（到达率）为价格的单调递减函数 $\lambda(p)$（$\lambda'(p) < 0$）。
瞬时预期收入生成速率为：
$$
r(p) = p \cdot \lambda(p)
$$

```mermaid
flowchart LR
    A["当前剩余销售时间 τ = T - t 与当前剩余库存 x"] --> B["构建 Hamilton-Jacobi-Bellman (HJB) 动态规划方程"]
    B --> C["∂V/∂t + max_p {r(p) - λ(p) ΔV(x, t)} = 0"]
    C --> D["计算边际机会成本 (Opportunity Cost): ΔV = V(x, t) - V(x-1, t)"]
    D --> E["最优定价准则: 边际收益等于边际销售成本加库存边际影子机会成本！"]
    E --> F["输出纳秒级动态价格标签 p*(x, t)"]
```

## 贝尔曼动态规划与最优边际影子成本

设 $V(x, t)$ 为在时刻 $t$ 剩余库存量为 $x$ 时的未来期望最大总收入值函数（Value Function）。
边界条件：$V(0, t) = 0$（售罄），$V(x, T) = 0$（期末归零）。

根据连续时间动态规划**HJB 方程（Hamilton-Jacobi-Bellman Equation）**：
$$
\frac{\partial V}{\partial t}(x, t) + \max_{p} \left\{p \lambda(p) - \lambda(p) \left[V(x, t) - V(x - 1, t)\right]\right\} = 0
$$

::: definition [边际库存机会成本 (Opportunity Cost / Shadow Value)]
定义消耗 1 单位库存的未来边际机会成本为：
$$
\Delta V(x, t) = V(x, t) - V(x - 1, t) \ge 0
$$
最优定价一阶充要条件为：
$$
p^*(x, t) = \arg\max_{p} \left\{\lambda(p) \left(p - \Delta V(x, t)\right)\right\}
$$
:::

### 价格动态演化的两大经济学铁律
1. **库存稀缺性溢价（Scarcity Effect）**：
在固定时间 $t$ 下，值函数关于库存是严格凹的，这意味着边际价值 $\Delta V(x, t)$ 随库存 $x$ 的减少而严格单调上升！
**当库存告急（$x$ 极小）时，机会成本暴增，算法自动触发“激进加价（Surge Pricing）”，将有限的库存保留给最不差钱的高净值客户**！
2. **时间衰减恐慌（Time-Decay Effect）**：
在固定库存 $x$ 下，随着时间逼近截止期 $T$（$t \to T$），边际机会成本 $\Delta V(x, t) \downarrow 0$ 急剧归零。
**当时间所剩无几时，算法自动触发“清仓跳水降价”，不惜一切代价将沉没资产变现出清**！

## 多资源网络收益管理与确定性线性规划 (Network DLP)

在复杂航线网络中（如乘客订购“北京 $\to$ 芝加哥 $\to$ 纽约”的联程机票），一张机票同时占用了两段航班航段的物理机上座位。
面对由 $m$ 个物理资源与 $n$ 条产品航线构成的网络，求解多维状态的动态规划遭遇了严重的维数灾难。

工业界普遍采用**确定性线性规划（Deterministic Linear Program, DLP）**与对偶控制：
设产品 $j$ 的全航程票价为 $p_j$，全销售季度的期望总需求为 $D_j$。资源消耗关联矩阵为 $A$。
$$
\begin{aligned}
\max_{x} \quad & \sum_{j=1}^n p_j x_j \\
\text{s.t.} \quad & \sum_{j=1}^n A_{ij} x_j \le C_i, \quad \forall i = 1, \dots, m \quad (\text{物理资源容量约束, 对偶影子价格 } \pi_i) \\
& 0 \le x_j \le D_j, \quad \forall j = 1, \dots, n
\end{aligned}
$$
根据对偶理论，产品 $j$ 的总机会成本严格等于其沿途消耗的所有航段影子价格之和：
$$
\text{Opportunity Cost}_j = \sum_{i=1}^m A_{ij} \pi_i^*
$$
**在线准入决策规则（Bid-Price Control）**：只要新进客户愿付票价超过其消耗的影子价格总和（$p_j \ge \sum A_{ij} \pi_i^*$），立即批准出票，否则坚决拒票！

## 多项 Logit 选品组合优化 (MNL Assortment Optimization)

在电商货架展示中，客户不是孤立看待某一款商品，而是在平台推荐的商品组合 $S \subset \{1, \dots, N\}$ 中进行对比挑选。
根据随机效用理论著名的**多项 Logit 模型（Multinomial Logit, MNL）**：
客户选择购买商品 $j \in S$ 的概率为：
$$
P_j(S) = \frac{v_j}{v_0 + \sum_{k \in S} v_k}
$$
其中 $v_j = \exp(u_j)$ 为商品 $j$ 的基准吸引力偏好，不买离开的外部选项吸引力为 $v_0$。

电商平台的收入极大化选品问题：
$$
\max_{S \subset \{1, \dots, N\}} \quad R(S) = \sum_{j \in S} r_j P_j(S) = \frac{\sum_{j \in S} r_j v_j}{v_0 + \sum_{k \in S} v_k}
$$
Talluri 和 van Ryzin 严格证明了：
**最优推荐产品组合，必然属于“按收益率排序的收入前缀集合（Revenue-Ordered Assortments）”！**
只需将所有商品按利润单价 $r_1 \ge r_2 \ge \dots \ge r_N$ 倒序排列，最优组合必然是形如 $\{1, 2, \dots, k\}$ 的前 $k$ 个高毛利商品的嵌套组合，求解仅需 $\mathcal{O}(N \log N)$ 排序时间！

::: pitfall 忽视动态价格歧视引发的消费者反弹与规避行为
若电商算法根据用户设备型号（如 iPhone 识别）实施激进的大数据杀熟加价，一旦被消费者察觉，不仅会引发公关海啸，更会导致理性消费者学会使用小号、比价插件进行算法规避。定价模型必须纳入长期声誉损失与公平性约束。
:::

::: insight 定价算法是用微积分探测人类欲望弹性的触角
在古典经济学中，亚当·斯密的“看不见的手”是一种宏观哲学抽象；
而在现代电子商务的服务器机房里，**收益管理算法变成了那只清晰可见、由对偶影子价格与泊松跳跃方程严密编织的数字之手**。它每秒钟在数亿次买卖撮合中，用最精准的边际微积分，动态调节着全人类物质资产供需平衡的最高效率。
:::
