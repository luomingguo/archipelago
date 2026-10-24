---
title: '整数对偶理论 I：超加性对偶与值函数理论 (Superadditive Duality)'
type: lecture
lecture: 8
tags: [integer-duality, superadditive-functions, value-function, subadditivity]
status: complete
---

# Lec 8 整数对偶理论 I：超加性对偶与值函数理论 (Superadditive Duality)

> MIT 15.083 / 6.859J 整数规划与组合优化 · 讲义 8 · 授课教师：Prof. Dimitris Bertsimas

## TL;DR

- 线性规划对偶乘子是线性标量内积，整数规划对偶算子必须升华为超加性非线性值函数。
- 超加性（Superadditivity）严格保持了离散网格上资源合并的规模经济递增特性。
- 整数强对偶性通过构造超加性非减极值函数，实现了零对偶间距的终极代数闭环。

## 1. 线性对偶的破产与整数值函数的非线性

在第 15.081J 第 9-11 讲中，线性规划的对偶理论极其纯粹：为每一条约束赋予一个常数影子价格 $p_i$，对偶目标就是线性组合 $p^T b$。
强对偶定理保证了 $c^T x^* = p^{*T} b$。

然而，在整数规划中：
$$z_{\text{IP}}(b) = \min \{c^T x \mid A x \ge b, \; x \ge 0, \; x \in \mathbb{Z}^n\}$$
如果我们依然试图用一个固定的线性向量 $p$ 去给资源定价，**线性对偶彻底破产了！**
因为整数可行域是离散破碎的点阵，其扰动值函数 $z_{\text{IP}}(b)$ **根本不是凸函数，而是一个充满台阶跳跃、锯齿断裂与局部阶跃的非凸下半连续函数！**

一个线性的平面无论怎么倾斜，都绝不可能严丝合缝地贴紧一个到处是台阶锯齿的离散曲面。
为了建立严格的整数规划对偶理论，我们必须将“对偶变量是一个实向量 $p$”的狭隘观念彻底抛弃，将对偶对象升华为**函数空间中的非线性泛函——超加性函数（Superadditive Functions）**！

```mermaid
flowchart TD
    subgraph DualityEvolution [对偶维度的范式飞跃]
        LP_Dual[线性对偶: 对偶解是一组常数标量乘子 p in R^m -> 线性泛函 p^T b]
        IP_Dual[整数对偶: 对偶解必须是一个非线性超加性函数 F: R^m -> R]
    end
    LP_Dual -->|离散锯齿导致线性失效| IP_Dual
    IP_Dual --> Closed[强对偶成立: max F(b) = min c^T x]
```

## 2. 超加性函数（Superadditive Functions）公理体系

::: definition 超加性函数 (Superadditive Function)
定义在欧氏空间上的函数 $F: \mathbb{R}^m \to \mathbb{R}$ 称为**超加性的（Superadditive）**，若满足：
1. $F(0) = 0$；
2. 对任意向量 $u, v \in \mathbb{R}^m$，均满足超加性不等式：
$$F(u + v) \ge F(u) + F(v)$$
若 $F$ 同时满足单调非减（若 $u \le v$ 则 $F(u) \le F(v)$），则称 $F$ 为**单调非减超加性函数**。
:::

超加性在经济学上具有极其深刻的直观解释：
**“整体大于部分之和（规模经济效益）！”**
当两个工厂将各自的原材料配额 $u$ 和 $v$ 合并在一起统一统筹排产时，由于离散整数调度与机器固定开机费用的规模效应，合并后的产出价值 $F(u + v)$ 必然不小于分散独立生产时的价值总和 $F(u) + F(v)$！

## 3. 整数超加性对偶问题与强对偶闭合

利用超加性函数，我们可以构筑起数学上无懈可击的**整数超加性对偶规划（Superadditive Dual Problem）**：

$$\begin{aligned}
w_{\text{Dual}} = \max_{F} \quad & F(b) \\
\text{s.t.} \quad & F(A_j) \le c_j, \quad \forall j = 1, \dots, n \\
& F: \mathbb{R}^m \to \mathbb{R} \text{ 为单调非减超加性函数}
\end{aligned}$$

注意约束 $F(A_j) \le c_j$：它要求对消耗资源配额向量 $A_j$ 所赋予的综合估值，绝不能超过制造该产品本身的名义成本 $c_j$（与线性对偶 $p^T A_j \le c_j$ 完全对应！）。

::: theorem 整数弱对偶定理 (Weak Integer Duality)
设 $x$ 为原整数规划的任意可行解（满足 $A x \ge b, x \ge 0, x \in \mathbb{Z}^n$），$F$ 为任意超加性对偶可行函数。
则恒成立：
$$F(b) \le c^T x$$
:::

证明仅需端详超加性的数学归纳递推：
$$F(b) \le F(A x) = F\left( \sum_{j=1}^n x_j A_j \right) \ge \sum_{j=1}^n x_j F(A_j) \le \sum_{j=1}^n x_j c_j = c^T x$$
弱对偶性获证！

::: theorem 整数强对偶定理 (Strong Integer Duality Theorem)
若原整数规划存在有限最优解，则其超加性对偶规划也必然存在最优超加性函数 $F^*$，使得：
$$F^*(b) = z_{\text{IP}}(b) = c^T x^*$$
**对偶间距严格为零！强对偶性在函数对偶空间中完满闭合！**
:::

更惊人的是：最优的对偶函数 $F^*$ 不是别人，**它正是原系统的真实扰动值函数自身（Value Function $z_{\text{IP}}(\cdot)$）！**

::: insight 从标量对偶到算子对偶的数学升华
超加性对偶是应用数学跨越非凸鸿沟的最高智慧。
当简单的标量影子价格在离散锯齿前折断时，数学家没有退缩，而是将“价格”本身升维成了一台非线性的评估算子。
每一个 Gomory 割平面的推导、每一个 Chvátal-Gomory 整值截断，本质上都是在用取整函数 $\lfloor \cdot \rfloor$ 拼接出一个具体的局部超加性函数。
这一理论不仅终结了“整数规划是否存在对偶”的百年争论，更直接催生了现代割平面法与值函数下界松弛技术的代数源泉。
:::
