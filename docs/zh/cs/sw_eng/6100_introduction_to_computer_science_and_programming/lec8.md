---
title: 浮点精度、二分搜索与连续优化
type: lecture
lecture: 8
tags: [bisection-search, floating-point, continuous-optimization, numerical-methods, linear-regression]
status: complete
source: https://introcomp.mit.edu/fall26
---

# Lec 8 浮点精度、二分搜索与连续优化（Bisection Search & Optimization）

> MIT 6.100 · 计算机科学与 Python 编程导论 · Fall 2026 · 教材参考：Guttag 3.2–3.4

## TL;DR

- **二进制浮点舍入极限**：实数在计算机内部受限于 64 位 IEEE 754 标准，二进制分数无法有限表示多数十进制小数（如 0.1），数值算法中必须使用容差 $\epsilon$ 代替精确判等。
- **对数级二分搜索（Bisection Search）**：利用连续单调函数的零点介值定理，每次将搜索区间对半剪枝，时间复杂度为 $O(\log_2((\text{high}-\text{low})/\epsilon))$，实现极速指数级收敛。
- **连续最优化与回归雏形**：定义目标损失函数（Loss Function），通过数值逼近或梯度下界寻找极值，为线性回归与机器学习参数拟合奠定算法基础。

## 1. 计算机实数表示：IEEE 754 与精度截断

计算机由离散的高低电平逻辑门构成，而连续实数轴是不可数无穷的。在 64 位双精度浮点数标准下，一个实数被编码为：
$$x = (-1)^s \times (1 + \text{mantissa}) \times 2^{\text{exponent} - 1023}$$

其中 1 位符号位、11 位指数位、52 位尾数位。因为分母必须是 2 的幂次，类似 $\frac{1}{10} = \frac{1}{2^4} + \frac{1}{2^5} + \dots$ 演变为无限循环二进制小数，必须发生截断舍入。

在连续数学计算中，绝对相等的判断是不成立的。我们必须定义一个允许的绝对误差容限 $\epsilon$（Epsilon）：
$$|f(x) - y| \le \epsilon$$

---

## 2. 二分搜索法（Bisection Search）：指数级加速

在求解非线性方程（如求任意实数 $x > 0$ 的平方根 $\sqrt{x}$）时，如果采用 Lec 2 中的穷举步进枚举法（每次递增 0.0001），随着精度要求的提升，运算轮数呈线性爆炸。

二分搜索算法利用了函数的连续性与单调性：若连续函数 $f(x)$ 在区间 $[a, b]$ 两端异号（即 $f(a) \cdot f(b) < 0$），则根据介值定理，区间内必然存在至少一个零点。算法每次检查中点 $m = \frac{a + b}{2}$，并将搜索区间缩减一半：

```python
def square_root_bisection(x: float, epsilon: float = 1e-7) -> float:
    """
    利用二分搜索计算正实数 x 的平方根，精度达到 epsilon
    """
    if x < 0:
        raise ValueError("负数不存在实数平方根")
    
    # 明确搜索边界：处理 x < 1 的边界情形 (如 x = 0.25, 根为 0.5 > 0.25)
    low = 0.0
    high = max(1.0, x)
    num_guesses = 0
    
    ans = (low + high) / 2.0
    while abs(ans ** 2 - x) >= epsilon:
        if ans ** 2 < x:
            low = ans
        else:
            high = ans
        ans = (low + high) / 2.0
        num_guesses += 1
        
        # 防御性上限，防止由于 epsilon 设定过小导致浮点死循环
        if num_guesses > 100:
            break
            
    print(f"二分搜索在 {num_guesses} 次猜测内收敛到结果")
    return ans

# 计算 54321 的平方根
root = square_root_bisection(54321.0)
print(f"计算结果: {root:.7f} | 检验误差: {abs(root ** 2 - 54321.0):.2e}")
```

### 复杂度飞跃：从 $O(N)$ 到 $O(\log N)$

若初始区间长度为 $L$，每次迭代后区间长度减半。经过 $k$ 步后区间长度收缩为 $\frac{L}{2^k}$。为了达到精度 $\epsilon$，所需步数满足：
$$\frac{L}{2^k} \le \epsilon \implies k \ge \log_2\left(\frac{L}{\epsilon}\right)$$

即使将搜索区间设为一百万（$L = 10^6$），并将误差收敛到十亿分之一（$\epsilon = 10^{-9}$），$L / \epsilon = 10^{15} \approx 2^{50}$，二分搜索仅需大约 50 次循环即可得出精确到小数点后 9 位的结果！

---

## 3. 连续最优化与简单线性回归

二分搜索最初被用于解决单调连续函数的求根问题。然而在更广泛的工程决策与数据建模任务中，我们所面临的核心挑战往往不是求解某个等式，而是：**在连续的多维参数空间中，寻找使得系统整体损失达到全局极小的最优设计点**。这一思想正是整个现代统计机器学习、深度学习反向传播与运筹优化的底层灵魂。

为了将工程问题形式化表述，我们必须定义两个核心概念：
1. **模型假设（Model Hypothesis）**：例如在一元线性模型中，假设输出与输入满足线性关系 $y = m \cdot x$。
2. **目标损失函数（Loss Function / Objective Function）**：用于量化当前候选参数 $m$ 的预测值与真实观测值之间的偏离程度。最经典也是数学性质最优雅的选择是**残差平方和（Residual Sum of Squares, RSS）**：
   $$\mathcal{L}(m) = \sum_{i=1}^N (y_i - m \cdot x_i)^2$$

由于平方和损失函数在实数域上是一个关于参数 $m$ 的严格单峰二次凸函数（Convex Function），其图像呈现一个碗状抛物线。根据微积分极值定理，该函数的全局最小值点必然出现在其一阶导数（梯度）等于零的驻点处。

此时，我们对损失函数求关于参数 $m$ 的一阶偏导数：
$$\frac{d\mathcal{L}(m)}{dm} = \sum_{i=1}^N 2(y_i - m \cdot x_i) \cdot (-x_i) = -2 \sum_{i=1}^N x_i (y_i - m \cdot x_i)$$

注意观察这个导数表达式：当 $m$ 较小时，导数为负值，代表损失函数正随着 $m$ 的增大而下降；当 $m$ 越过最优解后，导数变为正值。这意味着**导数函数关于参数 $m$ 具有严格的单调递增性**！于是，原本极其抽象的“最优化寻优问题”，在数学上被极其优美地降维转化为针对导数函数的“二分单调求根问题”：

```python
from typing import List, Tuple

Point = Tuple[float, float]

def linear_regression_bisection(points: List[Point], epsilon: float = 1e-5) -> float:
    """
    通过对导数进行二分求根，寻找最小二乘法最佳斜率 m
    损失函数对 m 的导数: dL/dm = -2 * sum(x_i * (y_i - m * x_i))
    """
    def derivative(m_val: float) -> float:
        return -2.0 * sum(x * (y - m_val * x) for x, y in points)
    
    # 假设斜率搜索区间在 [-100.0, 100.0]
    low, high = -100.0, 100.0
    while high - low > epsilon:
        mid = (low + high) / 2.0
        if derivative(mid) < 0:
            # 导数为负，说明损失函数还在下降，最优解在右侧
            low = mid
        else:
            high = mid
    return (low + high) / 2.0

sample_data = [(1.0, 2.1), (2.0, 3.9), (3.0, 6.1), (4.0, 8.0)]
best_m = linear_regression_bisection(sample_data)
print(f"最优拟合斜率 m: {best_m:.4f} (真实关系约为 2.0)")
```

::: pitfall 边界盲区与非单调函数失效
二分搜索具有极高的收敛速度，但其成立具有严苛的前提假定：目标函数必须在搜索区间内具备严格单调性（或其导数单调）。如果目标函数存在多个局部极小值（Non-convex Multi-modal），二分搜索可能会完全丢失全局最优解，必须结合随机重启（Random Restarts）或模拟退火等全局探索算法。
:::

## 我的理解

::: insight 算法加速的核心是利用信息消除不确定性
二分搜索是信息论在算法设计中的教科书级体现。每一次条件判定并不是简单地淘汰一个候选值，而是通过一次比较消除整整一半的未知空间（获得 1 比特的信息增益）。从穷举的线性爬行，到二分的对数级飞跃，软件架构师必须深刻理解：高效率来自对问题数学结构（单调性、连续性）的敏锐洞察与充分利用。
:::
