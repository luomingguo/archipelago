---
title: '现代启发式算法：可行性泵（Feasibility Pump）与大邻域搜索 (Heuristic Methods)'
type: lecture
lecture: 20
tags: [primal-heuristics, feasibility-pump, rins, large-neighborhood-search, incumbent]
status: complete
---

# Lec 20 现代启发式算法：可行性泵（Feasibility Pump）与大邻域搜索 (Heuristic Methods)

> MIT 15.083 / 6.859J 整数规划与组合优化 · 讲义 20 · 授课教师：Prof. Dimitris Bertsimas

## TL;DR

- 原生启发式（Primal Heuristics）在分支定界早期快速抢占高质量整数解（Incumbent）。
- 可行性泵（Feasibility Pump）在连续线性可行域与纯整数格点之间通过投影交替抽吸。
- 松弛诱导邻域搜索（RINS）锁定共同决策，以受限小 MIP 极速挖掘局部更优解。

## 1. 速度的渴望：为什么分支树必须依赖原生启发式？

在严谨的分支定界树中，如果没有一个极高质量的全局整数可行解（现任解 Incumbent $\text{UB}^*$），界限剪枝（Pruning by Bound）就完全无法启动！整棵搜索树将不得不膨胀到数千万个节点。

如果在求解器刚刚运行的前 1 秒钟内，算法就能“施展魔法”快速摸到一个距离最优解仅差 $1\%$ 的极高质量整数可行解：
1. 全局上界 $\text{UB}^*$ 瞬间暴跌被牢牢锚定；
2. 后续搜索树中 $95\%$ 的次优子分支可以在一瞬间被界限剪枝批量消灭！

为了在最短时间内抢占高质量可行解，现代整数规划诞生了**原生启发式算法（Primal Heuristics）**。

```mermaid
flowchart LR
    subgraph FeasibilityPumpLoop [可行性泵 FP 交替投影循环]
        direction LR
        LP_point[线性可行点 x* in P: 满足连续约束但有小数] -->|最近邻舍入 Rounding| Int_point[整数点 z* in Z^n: 纯整数但违规不可行]
        Int_point -->|求解 L1 投影 LP: min ||x - z*||_1| LP_point
    end
    LP_point -. 距离 ||x* - z*|| = 0! .-> Found[成功捕获合法整数可行解!]
```

## 2. 几何双投影奇迹：可行性泵（Feasibility Pump）

由 Matteo Fischetti、Fred Glover 与 Andrea Lodi 于 2005 年提出的**可行性泵（Feasibility Pump, FP）**，被公认为近二十年来整数规划领域最伟大的原生启发式发明。

可行性泵的核心目标是：**完全不理会目标函数 $c^T x$！全力以赴在最短时间内抓出一个满足所有约束的整数解！**

两个世界被清晰解耦：
1. **连续线性可行域多面体**：$P = \{x \in \mathbb{R}^n \mid A x \ge b, \; 0 \le x \le u\}$（容易满足，但点有小数）；
2. **纯整数点阵空间**：$\mathbb{Z}^n$（容易满足，但往往违背线性约束）。

可行性泵像一台往复抽吸的活塞泵，在这两个集合之间高速交替投影：
1. **初始化**：求解连续松弛 LP，得到实数点 $x^* \in P$；
2. **向整数网格投影（Rounding）**：将当前点直接四舍五入取整，得到纯整数点 $z^* = \lfloor x^* + 0.5 \rfloor \in \mathbb{Z}^n$；
   - 检查：若 $z^* \in P$，大功告成！直接输出合法整数解退出！
3. **向多面体投影（LP 投影）**：纯整数点 $z^*$ 通常不在多面体内部。
   求解一个极其简单的线性规划，在多面体 $P$ 内部寻找距离 $z^*$ 最近的点（使用 $L_1$ 范数距离）：
   $$x^* = \arg\min_{x \in P} \quad \|x - z^*\|_1 = \arg\min_{x \in P} \sum_{j \in I} |x_j - z_j^*|$$
   （$L_1$ 范数展开为标准 LP，可用单纯形法秒解！）；
4. **循环与扰动重启**：若 $x^*$ 与 $z^*$ 之间的距离为 0，宣告捕获整数解！若陷入循环停滞，执行随机翻转扰动（Perturbation）打破死锁。

实验表明：可行性泵通常**只需 5 到 15 轮极快的 LP 抽吸，就能以超过 $98\%$ 的恐怖成功率在几百毫秒内直接抓出超复杂大题的初始整数可行解！**

## 3. 站在巨人肩膀上：松弛诱导邻域搜索（RINS）

一旦可行性泵或贪心法为我们抓到了第一个合法的现任整数解 $x^{\text{inc}}$，我们如何在此基础上进一步提升质量、快速降维？
埃米尔·杜迪奇（Emil Danna）等人提出了**松弛诱导邻域搜索（Relaxation Induced Neighborhood Search, RINS）**：

在分支定界树搜索的某个节点，设当前松弛 LP 解为 $x^{\text{LP}}$，现任整数最优解为 $x^{\text{inc}}$。
RINS 比较这两个向量的取值：
**如果某变量在连续松弛解与现任整数解中取值完全相同（$x_j^{\text{LP}} = x_j^{\text{inc}}$），这强烈暗示该变量有极大概率在全局真实最优解中就应该取这个值！**

RINS 的操作极其精妙：
1. **变量固定冻结**：将所有 $x_j^{\text{LP}} = x_j^{\text{inc}}$ 的变量全部固定锁定为常数；
2. **构建极小局部子 MIP**：只对剩下极少数有分歧的变量放开自由度；
3. **设置极短时间限制调用子求解器**：在这个规模极小、高度降维的子 MIP 上运行 100 个节点的分支定界。

RINS 在原最优解周围极具前瞻性的局部邻域内精准深潜，往往能够以闪电般的速度持续刷新全局最佳上界。

::: insight 严谨证明与直觉灵动的终极融合
运筹学的发展绝不是教条主义。
如果说切平面与分支定界是重甲步兵，步步为营推进理论下界；那么可行性泵与 RINS 就是身轻如燕的特种侦察兵，在错综复杂的离散森林中凭借几何直觉穿插突击。
正是在这种“确定性下界严密防守”与“启发式上界突击攻坚”的完美双向夹击下，现代 MIP 求解器才能在看似不可逾越的 NP-hard 铁幕中，屡屡创造出出清百万变量超级工业大题的计算奇迹。
:::
