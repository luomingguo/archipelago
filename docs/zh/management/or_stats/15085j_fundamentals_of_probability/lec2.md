---
title: '两大基石概率模型与非可测集构造 (Two Fundamental Models & Vitali Sets)'
type: lecture
lecture: 2
tags: [bernoulli-process, lebesgue-measure, vitali-sets, axiom-of-choice]
status: complete
---

# Lec 2 两大基石概率模型与非可测集构造 (Two Fundamental Models & Vitali Sets)

> MIT 15.085J / 6.436J 概率论基础 · 讲义 2 · 授课教师：Prof. John Tsitsiklis / Devavrat Shah

## TL;DR

- 无限次伯努利抛硬币试验与区间 $[0, 1)$ 上的勒贝格测度通过二进制小数展开完美同构。
- 维塔利（Vitali）集合利用选择公理与有理数平移等价类证明了不可测集的存在性。
- 测度论将不可测集永久隔离在可观测事件域之外，确立了概率论的物理观测边界。

## 1. 离散到连续的完美同构：无限伯努利序列与勒贝格测度

在概率论中，存在两个看似天差地别、实则互为镜像的基石模型：
1. **无限独立抛硬币模型（Infinite Coin Tosses）**：样本空间 $\Omega = \{0, 1\}^\mathbb{N}$，每个基本结果是一个无限长的二进制序列 $\omega = (\omega_1, \omega_2, \omega_3, \dots)$，其中 $\omega_i \in \{0, 1\}$；
2. **单位区间上的均匀分布（Uniform Distribution on $[0, 1)$）**：样本空间 $\Omega = [0, 1)$，概率测度即标准的一维勒贝格测度（长度测度 $\lambda([a, b)) = b - a$）。

这两个模型在代数与拓扑上可以通过**二进制实数小数展开（Binary Expansion）**实现几乎处处（Almost Everywhere）的一一映射：
$$X(\omega) = \sum_{i=1}^\infty \frac{\omega_i}{2^i} = 0.\omega_1 \omega_2 \omega_3 \dots$$

```mermaid
flowchart LR
    A[无限离散抛硬币序列 omega in {0, 1}^N] -->|映射 X = sum omega_i / 2^i| B[连续实数区间 [0, 1) 上的随机数]
    B -->|柱集 Cylinder Set: 前 n 位固定| C[对应区间长度 1 / 2^n 的二进区间]
```

对于任意给定的前 $n$ 次硬币结果（称为**柱集 Cylinder Set**），在抛硬币空间中的概率为 $(1/2)^n$；
而在实数轴上，该柱集恰好对应长度为 $1/2^n$ 的半开半闭二进区间 $[k/2^n, (k+1)/2^n)$！
根据第 1 讲的卡拉西奥多里扩张定理，由柱集生成的积空间 $\sigma$-代数，与实数区间上的博雷尔 $\sigma$-代数 $\mathcal{B}([0, 1))$ **完全保测度同构**！
离散与连续的鸿沟，在二进制级数展开下被瞬间消弭。

## 2. 撕裂直觉的幽灵：维塔利不可测集（Vitali Set）构造

现在，我们必须正面回答第 1 讲留下的终极拷问：**为什么我们不能为单位区间 $[0, 1)$ 的所有子集都定义概率？为什么全子集幂集 $2^{[0, 1)}$ 必须被废弃？**

意大利数学家朱塞佩·维塔利（Giuseppe Vitali）在 1905 年利用现代数学的**选择公理（Axiom of Choice）**，构造出了人类历史上第一个不可测集。

构造过程极其惊心动魄：
在区间 $[0, 1)$ 上定义一个等价关系 $\sim$：
$$x \sim y \iff x - y \in \mathbb{Q} \quad (\text{两数之差为有理数})$$
易证 $\sim$ 是一个严格的等价关系。该关系将整个区间 $[0, 1)$ 切割为不可数无限个彼此互不相交的等价类集合。

**动用选择公理**：从每一个互不相交的等价类中，**有且仅挑出一个代表元素**。
将所有挑出来的元素汇聚在一起，构成的集合记为 $V \subset [0, 1)$。这个集合 $V$ 就是著名的**维塔利集合（Vitali Set）**！

```mermaid
flowchart TD
    subgraph VitaliContradiction [维塔利集合的可加性自毁证明]
        AC[选择公理从每个有理数等价类抽出一员构成 V] --> Shifts[用 [-1, 1] 内所有可数有理数 q_k 做模 1 平移: V_k = V + q_k]
        Shifts --> Disjoint[平移集 V_k 两两严格互斥]
        Disjoint --> Cover[可数并集被严密夹在 [0, 1] 与 [-1, 2] 之间]
        Cover --> MeasureCheck{若 V 有测度 P(V): 计算可数测度总和}
        MeasureCheck -- 若 P(V) = 0 --> Zero[总和为 0 < 1: 矛盾!]
        MeasureCheck -- 若 P(V) > 0 --> Inf[总和为无穷大 > 3: 矛盾!]
    end
```

## 3. 为什么维塔利集不可测？

假设集合 $V$ 拥有合法的勒贝格测度 $\lambda(V) = p$。
列举区间 $[-1, 1]$ 内的所有有理数，由于有理数可数，记为有序序列 $q_1, q_2, q_3, \dots \in \mathbb{Q} \cap [-1, 1]$。
定义维塔利集合的平移集：
$$V_k = V + q_k = \{v + q_k \mid v \in V\}$$

分析这些平移集合的奇妙性质：
1. **两两不交**：若存在 $x \in V_i \cap V_j$（$i \ne j$），则存在 $v_i, v_j \in V$ 使得 $v_i + q_i = v_j + q_j \implies v_i - v_j = q_j - q_i \in \mathbb{Q}$。这意味着 $v_i$ 与 $v_j$ 属于同一个等价类！但根据选择公理，$V$ 从每个等价类中只挑选了一个代表，故必须 $v_i = v_j$，进而 $q_i = q_j$，发生平移编号矛盾！
2. **两重夹逼覆盖**：
   - 因为每一个 $x \in [0, 1)$ 必然与 $V$ 中某元素 $v$ 仅差一个有理数 $r \in [-1, 1]$，故 $[0, 1) \subset \bigcup_{k=1}^\infty V_k$；
   - 又因为 $V \subset [0, 1)$ 且 $q_k \in [-1, 1]$，故所有平移点绝不会逃逸出 $[-1, 2]$，即 $\bigcup_{k=1}^\infty V_k \subset [-1, 2]$。

对夹逼包含式应用概率可数可加性与平移不变性（$\lambda(V_k) = \lambda(V) = p$）：
$$\lambda([0, 1)) \le \lambda\left( \bigcup_{k=1}^\infty V_k \right) = \sum_{k=1}^\infty \lambda(V_k) \le \lambda([-1, 2])$$
代入数值：
$$1 \le \sum_{k=1}^\infty p \le 3$$

现在考察常数 $p$ 的取值：
- 若 $p = 0$：左边得 $1 \le 0$，**荒谬矛盾！**
- 若 $p > 0$：无穷个正数累加为 $+\infty$，右边得 $+\infty \le 3$，**彻底崩溃！**

结论无可置疑：**实数轴上不存在任何实数能够作为维塔利集 $V$ 的测度！维塔利集是一个彻头彻尾的非可测集！**

::: insight 哥德尔选择公理与概率论的边界
维塔利集是 20 世纪数理逻辑在测度论中掷下的一枚深水炸弹。
它迫使所有的数学家承认：人类的语言与选择公理，能够拼装出超出物理度量能力的超限奇异体。
概率论之所以必须以 $\sigma$-代数作为神圣过滤网，正是为了对维塔利集这类幽灵实行永久封杀。只要我们把可观测事件严格限制在博雷尔域内，概率论就能彻底免除可加性自毁的威胁，在严谨理性的轨道上安全驰骋。
:::
