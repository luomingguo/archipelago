---
title: '广义规划与次梯度优化算法 (Generalized Programming & Subgradient Optimization)'
type: lecture
lecture: 22
tags: [generalized-programming, subgradient-method, step-size-rules, dantzig-wolfe-connection]
status: complete
---

# Lec 22 广义规划与次梯度优化算法 (Generalized Programming & Subgradient Optimization)

> MIT 15.084J / 6.252J 非线性规划 · 讲义 22 · 授课教师：Prof. Robert Freund

## TL;DR

- 次梯度法（Subgradient Method）以纯粹的向量迭代解决大规模不可微凸对偶优化。
- 与梯度下降不同，负次梯度不一定是局部下降方向，必须依靠凸投影几何证明收敛。
- 丹齐格广义规划（Generalized Programming）是列生成在非线性凸集上的连续推广。

## 1. 不可微凸优化与次梯度法（The Subgradient Method）

在第 18 讲到第 20 讲中，我们看到拉格朗日对偶函数 $q(\mu) = \inf_x L(x, \mu)$ 永远是一个凹函数。为了求解对偶最优乘子，我们必须求解凸优化问题：
$$\min_{\mu \ge 0} \quad \psi(\mu) = -q(\mu)$$

然而，由于 $q(\mu)$ 是无数个仿射函数的下确界，它在很多点处是**不可微的（Non-differentiable）**！
传统赖以生存的梯度法、牛顿法在此彻底失效。

为了攻克这一难题，前苏联数学家瑙姆·绍尔（Naum Z. Shor）在 20 世纪 60 年代开创了**次梯度法（Subgradient Method）**。

次梯度法的迭代格式看似与梯度下降毫无二致：
$$\mu_{k+1} = \Pi_{\mathbb{R}_+^m}\left( \mu_k - \alpha_k g_k \right)$$
其中 $g_k \in \partial \psi(\mu_k)$ 是当前点处提取的一个次梯度，$\Pi$ 为非负投影算子，$\alpha_k > 0$ 为步长。

```mermaid
flowchart TD
    subgraph SubgradientDynamics [次梯度法非单调但距离收缩机制]
        Current[当前点 mu_k: 计算次梯度 g_k] --> Move[沿负次梯度迈出步长 -alpha_k * g_k]
        Move --> NonDescent{目标函数是否一定下降?}
        NonDescent -- 否! 目标可能暂时反弹上升! --> Geometry[凸分离超平面几何]
        Geometry --> Shrink[到最优解集距离严格单调缩减: ||mu_k+1 - mu*||^2 < ||mu_k - mu*||^2]
        Shrink --> Converge[经过遍历平均后最终收敛至全局最优解]
    end
```

## 2. 负次梯度不是下降方向的残酷事实

初学者最容易陷入的一个致命认知误区是：误以为“负次梯度就像负梯度一样，能够保证目标函数下降”。
**这是绝对错误的！负次梯度方向完全可能是一个上升方向！**

反例：考察单变量绝对值函数 $f(x_1, x_2) = |x_1| + 2 |x_2|$。在点 $(1, 0)$ 处，次微分集合包含向量 $(1, 2)^T$。沿着负方向 $(-1, -2)^T$ 行进，函数值瞬间从 1 暴涨！

既然目标函数不能保证单调下降，次梯度法凭什么收敛？
答案在于**到最优解集的欧氏距离在单调缩减**！

考察当前点到任意最优解 $\mu^*$ 的平方距离：
$$\begin{aligned}
\|\mu_{k+1} - \mu^*\|_2^2 &= \|\Pi(\mu_k - \alpha_k g_k) - \Pi(\mu^*)\|_2^2 \\
&\le \|\mu_k - \alpha_k g_k - \mu^*\|_2^2 \\
&= \|\mu_k - \mu^*\|_2^2 - 2 \alpha_k g_k^T (\mu_k - \mu^*) + \alpha_k^2 \|g_k\|_2^2
\end{aligned}$$

根据第 17 讲次梯度的定义式：$g_k^T (\mu^* - \mu_k) \le \psi(\mu^*) - \psi(\mu_k) \le 0$，即：
$$g_k^T (\mu_k - \mu^*) \ge \psi(\mu_k) - \psi^* > 0$$
代入上式得到核心不等式：
$$\|\mu_{k+1} - \mu^*\|_2^2 \le \|\mu_k - \mu^*\|_2^2 - 2 \alpha_k (\psi(\mu_k) - \psi^*) + \alpha_k^2 \|g_k\|_2^2$$

只要步长 $\alpha_k$ 足够小，使得 $\alpha_k \|g_k\|^2 < 2 (\psi(\mu_k) - \psi^*)$，**当前点到最优解的欧氏距离就绝对在严格缩短！** 算法可能在目标函数上剧烈颠簸，但它在空间中像一颗被引力拉扯的卫星，坚定不移地向最优解核心收缩！

::: theorem 次梯度法步长收敛准则
设次梯度有界：$\|g_k\|_2 \le G$。
若步长序列满足经典的**平方可和但不可和准则（Square Summable but not Summable）**：
$$\sum_{k=1}^\infty \alpha_k^2 < \infty \quad \text{且} \quad \sum_{k=1}^\infty \alpha_k = \infty \quad \left(\text{例如 } \alpha_k = \frac{1}{k}\right)$$
则次梯度法输出的最优历史函数值必然**严格渐近收敛至全局最优解**：$\lim_{k \to \infty} \min_{i=1,\dots,k} \psi(\mu_i) = \psi^*$！
其收敛速率为 $\mathcal{O}(1/\sqrt{k})$。
:::

## 3. 丹齐格广义规划（Generalized Programming）

如果不想忍受次梯度法 $\mathcal{O}(1/\sqrt{k})$ 的缓慢收敛，我们能否利用线性规划的单纯形机械结构来精确优化非线性凸集？
乔治·丹齐格在 1960 年提出了**广义规划（Generalized Linear Programming）**。

考虑在凸集 $C$ 上优化：
$$\min \quad c^T x \quad \text{s.t.} \quad A x = b, \quad x \in C$$
根据第 16 讲学到的魏尔-闵可夫斯基定理，有界闭凸集 $C$ 等于其全部极点原子的凸包包络：$x = \sum \lambda_k x^k, \sum \lambda_k = 1, \lambda_k \ge 0$。

广义规划每一步维护一个仅包含有限个极点的受限主规划（RMP）：
1. 解当前 RMP 获得对偶乘子向量 $p$；
2. 求解子问题：$\min_{x \in C} (c - A^T p)^T x$；
3. 将解得的最优极点 $x^*$ 作为全新的一列**追加到主规划中**，直至子问题的目标不低于乘子。

广义规划直接将大规模凸对偶优化降维成了经典列生成（Column Generation）！

::: insight 粗犷迭代与精巧切割的两极
次梯度法与广义规划代表了处理不可微凸问题的两种极致哲学：
次梯度法极其粗犷：它不要任何矩阵求逆，不建任何辅助模型，抓起一个次梯度就往前迈步，在超大规模分布式网络与深度学习中拥有不可替代的鲁棒性；
广义规划极度精巧：它用单纯形表作为总指挥，步步为营地在凸曲面上切出多面体外包络。
在计算优化的宏伟工具箱里，既有瑞士军刀般的精巧列生成，也有重锤般的次梯度投影。懂得在不同的系统瓶颈前调兵遣将，是顶尖工程师成熟的标志。
:::
