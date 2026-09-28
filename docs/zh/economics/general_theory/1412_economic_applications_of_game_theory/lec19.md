---
title: 收益等价定理与最优拍卖设计
type: lecture
lecture: 19
tags: [revenue-equivalence, optimal-auctions, myerson, reserve-price]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 19 收益等价定理与最优拍卖设计（Revenue Equivalence）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 阐明并证明维克里-迈耶森收益等价定理（Revenue Equivalence Theorem, RET）。
- 任何满足配置有效性且最低估值类型期望收益为零的标准拍卖，必产生严格相等的卖家期望总收益。
- 引入迈耶森虚拟价值（Virtual Valuation），推导使卖家收益最大化的最优保留底价（Reserve Price）。

## 核心概念与数学形式化

### 收益等价定理（Revenue Equivalence Theorem）

**定理假设**：
1. 每个买家的估值 $v_i$ 独立同分布于严格单调递增分布函数 $F(v)$；
2. 所有竞标者均风险中性（Risk Neutral）；
3. 拍卖规则在均衡时保证物品最终分配给估值最高的买家（配置有效性）；
4. 最低可能估值类型的买家获得零期望效用。

**定理结论**：
任何满足上述假设的拍卖机制，不仅赋予任何类型买家完全相同的期望支付额，且**给卖方带来的期望总收益严格相等**！
$$\mathbb{E}[\text{Revenue}]_{\text{FPA}} = \mathbb{E}[\text{Revenue}]_{\text{SPA}} = \mathbb{E}[\text{Revenue}]_{\text{English}} = \mathbb{E}[\text{Revenue}]_{\text{Dutch}}$$

### 迈耶森最优拍卖与虚拟价值（Myerson, 1981）
定义买家 $i$ 的**虚拟估值（Virtual Valuation）**：
$$\psi(v_i) = v_i - \frac{1 - F(v_i)}{f(v_i)}$$
- 卖家的期望收益等价于向虚拟估值最高者分配：
  $$\mathbb{E}[\text{Revenue}] = \mathbb{E}\left[ \max_{i} \psi(v_i) \right]$$
- **最优保留价（Reserve Price, $r^*$）**：
  卖家应将底价设定在虚拟价值恰好等于卖家自身估值 $v_0$（若 $v_0=0$ 则 $\psi(r^*) = 0$）：
  $$r^* - \frac{1 - F(r^*)}{f(r^*)} = 0$$
  最优保留底价**与竞标者总人数 $n$ 完全无关**！

## 经济应用与机制分析

收益等价定理证明：卖家想要多赚钱，花样翻新的拍卖形式并无实质帮助，真正起决定性作用的是两件事：第一，引入尽可能多的竞争买家（Bulow-Klemperer 定理：多招募一个买家胜过设计精巧的最优底价）；第二，坚持设立合理的保留底价 $r^*$。

## 边界条件与易错点

当买家具有风险厌恶时误套用收益等价定理（在风险厌恶下，FPA 收益严格高于 SPA）；忽视共同价值环境下相关性对等价定理的破坏。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=mu0X3GpDAy8)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
收益等价定理是现代经济学最令人惊叹的守恒定律之一。无论规则是一阶暗标、二阶暗标、英式升价还是荷兰式降价，只要买家风险中性且满足 IPV，规则的表层差异最终都会被理性的策略性出价调整彻底抚平，给卖家带来分毫不差的期望银两。打破等价的唯一关键，是卖家设立最优保留价。
:::
