---
title: '整数优化几何学：Chvátal-Gomory 闭包与割平面等级 (Geometry of Integer Optimization)'
type: lecture
lecture: 16
tags: [chvatal-gomory, polyhedral-combinatorics, cg-closure, cutting-plane-rank]
status: complete
---

# Lec 16 整数优化几何学：Chvátal-Gomory 闭包与割平面等级 (Geometry of Integer Optimization)

> MIT 15.083 / 6.859J 整数规划与组合优化 · 讲义 16 · 授课教师：Prof. Dimitris Bertsimas

## TL;DR

- Chvátal-Gomory 割（CG 割）通过对有效不等式左端线性组合与右端向下取整系统生成。
- 一阶 CG 闭包 $P^{(1)}$ 严格收缩连续松弛多面体，保留原多胞形内所有整数点。
- Chvátal 基础定理证明：有限次重复 CG 闭包运算必然能在有限阶数下完全重构整数凸包！

## 1. 割平面的公理化诞生：Chvátal-Gomory 运算

在第 3 讲中我们学习了针对背包问题的覆盖割。然而，对于通用的任意整数规划多面体 $P = \{x \in \mathbb{R}^n \mid A x \le b\}$，我们能否发明一种通用的、机械化的数学流水线，源源不断地生成能够切除非整数解的绝对强割平面？

瓦茨拉夫·赫瓦塔尔（Václav Chvátal）在 1973 年系统总结了拉尔夫·戈莫里（Ralph Gomory）的代数思想，建立了组合优化中最核心的几何概念——**Chvátal-Gomory 割（简称 CG 割）**。

其推导过程极其简洁，仅基于两条不容置疑的公理：
设 $x \in P \cap \mathbb{Z}^n$ 为任意合法整数解。
1. **线性组合有效性**：挑选任意非负乘子向量 $u \ge 0$。只要 $A x \le b$ 成立，显然有：
$$(u^T A) x \le u^T b$$
2. **向下取整单调性**：假设我们在选取 $u$ 时，使得左端项的系数**恰好全部变成了纯整数**：即 $u^T A \in \mathbb{Z}^n$。
   此时，由于决策变量也是纯整数（$x \in \mathbb{Z}^n$），不等式左边的内积 $(u^T A) x$ **必然是一个纯整数！**
   一个必须是纯整数的数值，如果小于等于实数 $u^T b$，那么它必然**无条件小于等于该实数的向下取整（Floor Function）**！

由此，直接诞生了统治运筹界半个世纪的**Chvátal-Gomory 割平面公理**：

::: definition Chvátal-Gomory 割 (CG Cut)
设 $A x \le b$ 为多面体的有效不等式系统。对于任意满足 $u^T A \in \mathbb{Z}^n$ 的非负乘子向量 $u \ge 0$，线性不等式：
$$(u^T A) x \le \lfloor u^T b \rfloor$$
对于该多面体内的**所有整数解 $x \in P \cap \mathbb{Z}^n$ 严格恒成立**！称该不等式为一个 **CG 割平面**。
:::

```mermaid
flowchart TD
    subgraph CG_Hierarchy [Chvátal-Gomory 闭包逐级逼近凸包]
        P0[原始连续松弛多面体 P = P^(0)] -->|提取所有可能 CG 割求交集| P1[一阶闭包 P^(1): 严格切去外围非整极点]
        P1 -->|在 P^(1) 上再次提取 CG 割| P2[二阶闭包 P^(2)]
        P2 --> Pk[第 k 阶闭包 P^(k)]
        Pk -->|有限次迭代 Chvátal 定理| ConvexHull[完美收敛: P^(r) = conv(P交Z^n) 纯整数凸包!]
    end
```

## 2. 一阶 CG 闭包与多面体收缩（The CG Closure）

如果我们把一个多面体能够生成出来的**所有不可数无穷多个 CG 割平面**全部收集起来，取它们的共同交集，会得到一个什么样的全新几何体？

::: definition 一阶 Chvátal 闭包 (First CG Closure)
多面体 $P$ 的**一阶 Chvátal-Gomory 闭包**定义为满足所有可能合法 CG 割平面的点集交集：
$$P^{(1)} = \left\{ x \in \mathbb{R}^n \;\middle|\; (u^T A) x \le \lfloor u^T b \rfloor, \; \forall u \ge 0 \text{ 使得 } u^T A \in \mathbb{Z}^n \right\}$$
:::

仔细观察这个闭包：
- 任何原整数可行点绝不会被误杀：$P \cap \mathbb{Z}^n \subset P^{(1)} \subset P$；
- 多面体中凡是距离整数网格较远的分数尖角，被密集的整取整割平面全方位平滑削平！

威廉·库克（William Cook）等人证明了关于该闭包的深层拓扑性质：
**尽管合法的乘子 $u$ 有不可数无限多个，但生成出来的闭包 $P^{(1)}$ 必然依然是一个拥有有限个刻画面的有理凸多面体（Rational Polyhedron）！**

## 3. 终极定理：Chvátal 阶数有限性（Chvátal Rank）

如果一阶闭包 $P^{(1)}$ 依然存在分数极点，我们可以将 $P^{(1)}$ 作为新的起点，继续对其生成 CG 割，得到二阶闭包 $P^{(2)} = (P^{(1)})^{(1)}$，并依次递推定义第 $k$ 阶闭包 $P^{(k)}$。

这个切削过程会不会陷入无穷无尽的死循环？
瓦茨拉夫·赫瓦塔尔给出了奠定整个现代组合优化几何学的**有限性终极定理**：

::: theorem 赫瓦塔尔有限阶收敛定理 (Chvátal's Theorem, 1973)
设 $P$ 为任意有理多胞形（有界多面体）。
则必然存在一个**有限的非负整数 $r < \infty$**，使得第 $r$ 阶 Chvátal 闭包**精确等于该离散点集的真实纯整数凸包**：
$$P^{(r)} = \operatorname{conv}\left( P \cap \mathbb{Z}^n \right)$$
最小的满足此条件的整数 $r$ 被称为多面体 $P$ 的 **Chvátal 阶数（Chvátal Rank）**。
:::

若多面体原本就不包含任何整数点（$P \cap \mathbb{Z}^n = \emptyset$），定理保证在有限步内必然产生空集：$P^{(r)} = \emptyset$（此时出现矛盾不等式 $0 \le -1$）。

::: insight 割平面作为离散世界的微积分微分
Chvátal-Gomory 闭包理论是运筹学历史上最纯粹的几何诗篇。
它向全人类证明了：**任何复杂到极致的 NP 难离散整数凸包，本质上都可以通过最简单的“加权内积加向下取整”这两步初等算术，在有限步内被完全雕刻出来！**
Chvátal 阶数度量了一个离散问题在几何深处的“非整数复杂度”。当今所有商业求解器中的 Gomory 割、MIR 割、零半割（Zero-Half Cuts），全都是这台伟大理论机器在工业现实中的具象化体现。
:::
