---
title: 完美贝叶斯均衡（PBE）与序贯理性
type: lecture
lecture: 21
tags: [perfect-bayesian-equilibrium, pbe, sequential-rationality, belief-updating]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 21 完美贝叶斯均衡（PBE）与序贯理性（Perfect Bayesian Equilibrium）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 动态不完全信息博弈中，SPNE 无法对包含多个节点的信息集进行有效筛选。
- 引入系统信念（System of Beliefs）与序贯理性（Sequential Rationality）。
- 严格形式化完美贝叶斯均衡（PBE）：在均衡路径上严格满足贝叶斯法则，在非均衡路径上保持信念自洽。

## 核心概念与数学形式化

### 完美贝叶斯均衡的四项核心要求

在动态扩展式不完全信息博弈中，一个评估剖面（Assessment）由策略剖面 $\sigma$ 与系统信念 $\mu$ 构成：$(\sigma, \mu)$。
$\mu(x \mid h)$ 表示局中人在抵达信息集 $h$ 时，确信自己处于特定节点 $x \in h$ 的后验条件概率。

1. **要求 1（信念完备性）**：
   在属于玩家 $i$ 的每一个信息集 $h \in H_i$ 上，玩家必须持有一个良定义的概率分布 $\mu(h) \in \Delta(h)$。
2. **要求 2（序贯理性, Sequential Rationality）**：
   在每一个信息集 $h$ 处，给定当前信念 $\mu(h)$ 以及对手后续推荐策略 $\sigma_{-i}$，行动玩家的策略选择必须使自身自该节点起的期望折现效用最大化：
   $$\sigma_i(h) \in \arg\max_{a_i \in A(h)} \mathbb{E}_{\mu(h), \sigma}[u_i \mid h, a_i]$$
3. **要求 3（均衡路径上的贝叶斯法则）**：
   如果信息集 $h$ 在均衡策略剖面 $\sigma^*$ 下具有严格正的发生概率（$\Pr(h \mid \sigma^*) > 0$），则其上的信念 $\mu^*(x \mid h)$ 必须严格通过贝叶斯定理基于先验概率与策略动作计算生成。
4. **要求 4（非均衡路径上的合理推断）**：
   在发生概率为零的离道（Off-the-equilibrium-path）信息集上，信念不受贝叶斯公式直接约束，但必须满足行动独立性与结构合理性。

## 经济应用与机制分析

法律条文与行政合规在处理企业未预见的罕见意外事件时，实际上是在确立非均衡路径上的“合理信义信念”。制度如果不明确非均衡路径的归责原则，投机者就会蓄意制造意外以利用信念漏洞勒索寻租。

## 边界条件与易错点

忽视非均衡路径上的信念可以存在自由度，导致遗漏可能存在的冷门 PBE；误在概率为零的除以零节点强行套用贝叶斯公式。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=yDNNcall_ho)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
进入不完全信息的动态深水区，我们不仅需要对“行动”求解均衡，更需要对每个玩家在每一个时刻脑海深处的“信念”（Belief）进行均衡定价。完美贝叶斯均衡（PBE）要求理性人在行动时永远保持“序贯理性”：无论你是如何意外漂流到这个残局节点的，此时此刻的下一步行动必须对你当下的后验信念最优化。
:::
