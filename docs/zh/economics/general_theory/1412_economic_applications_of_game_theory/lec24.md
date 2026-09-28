---
title: 廉价磋商（Cheap Talk）与战略信息传递
type: lecture
lecture: 24
tags: [cheap-talk, crawford-sobel, strategic-communication, credibility]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 24 廉价磋商（Cheap Talk）与战略信息传递（Cheap Talk）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 廉价磋商（Cheap Talk）：信息发送没有任何直接造假成本，言语本身不直接进入收益函数。
- 奠基之作 Crawford-Sobel（1982）模型：利益冲突程度从根本上约束了信息传递的颗粒度。
- 证明纯言语博弈无法实现完全真实披露，只能达成粗糙的区间分区均衡（Partition Equilibrium）。

## 核心概念与数学形式化

### 克劳福德-索贝尔模型（Crawford and Sobel, 1982）

1. **博弈流程**：
   - 发送方（Sender, $S$）观察到真实状态 $\theta \sim U[0, 1]$。
   - $S$ 向接收方（Receiver, $R$）发送一条无成本语言消息 $m \in M$。
   - $R$ 听到消息后采取行动 $y \in \mathbb{R}$。

2. **收益函数与利益偏差（Bias, $b > 0$）**：
   - 接收方偏好：$u_R(y, \theta) = -(y - \theta)^2$（$R$ 的最理想行动是 $y = \theta$）。
   - 发送方偏好：$u_S(y, \theta, b) = -(y - (\theta + b))^2$（$S$ 总是希望 $R$ 的行动比真实状态高出 $b$）。

### 区间分区均衡（Partition Equilibrium）
- **定理**：所有 PBE 必然是**区间分区形态**！即存在分界点序列 $0 = a_0 < a_1 < \dots < a_K = 1$。
  只要状态 $\theta \in (a_{k-1}, a_k)$，发送方发送相同的模糊消息 $m_k$。
- **接收方的最优反应**：在区间中点采取行动：
  $$y_k^* = \frac{a_{k-1} + a_k}{2}$$
- **发送方在边界点的无差异套索条件**：
  $$a_{k+1} - a_k = a_k - a_{k-1} + 4b$$
- **核心推论**：
  均衡中所能支持的最大分区数 $K(b)$ 满足：
  $$K(b) = \left\lfloor -\frac{1}{2} + \frac{1}{2}\sqrt{1 + \frac{2}{b}} \right\rfloor$$
  - 当 $b \to 0$ 时，$K \to \infty$，趋向完全信息披露；
  - 当 $b \ge 1/4$ 时，$K = 1$，唯一均衡是**无信息的闲聊胡扯（Babbling Equilibrium）**，任何沟通完全失效！

## 经济应用与机制分析

在企业年报的前瞻性业绩指引与央行的货币政策措辞中，普遍采用“稳健”、“合理充裕”等模糊用语。这种刻意的模糊性并非水平低下，而是由于官方与金融市场存在潜在利益偏差时，博弈论所证明的唯一能够维持信息可信度的最优理性沟通形态。

## 边界条件与易错点

混淆廉价磋商（言语无直接成本）与可验证信息披露（Disclosure Games, 语言无法造假但可选择性保留）；忽视闲聊均衡（Babbling）作为平庸均衡永远存在。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=SsdSpzJ-d7s)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
“空口无凭”（Talk is Cheap）并不意味着语言毫无力量。在利益完全一致时，廉价磋商能够实现无缝完美的沟通协作；但只要各方存在哪怕微小的利益偏差，言辞就必然被战略性地模糊化。战略沟通的最高境界不是撒弥天大谎，而是通过恰到好处的语焉不详，在守住自身私利的同时向对方传达恰足成事的粗粒度真相。
:::
