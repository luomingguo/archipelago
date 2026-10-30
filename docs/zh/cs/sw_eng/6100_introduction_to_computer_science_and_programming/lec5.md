---
title: 随机漫步与高阶函数参数化
type: lecture
lecture: 5
tags: [random-walk, simulation, higher-order-functions, brownian-motion, modularity]
status: complete
source: https://introcomp.mit.edu/fall26
---

# Lec 5 随机漫步与高阶函数参数化（Random Walks & Functions as Arguments）

> MIT 6.100 · 计算机科学与 Python 编程导论 · Fall 2026 · 教材参考：Guttag 16, 4.4

## TL;DR

- **随机漫步与布朗运动建模**：通过定义位置坐标、方向选择与移动步长，建立离散二维随机漫步模型，模拟花粉扩散、布朗运动与金融资产价格随机波动。
- **高阶函数泛型抽象**：函数作为一等公民（First-Class Citizen）可作为参数传入模拟骨架，实现“仿真框架代码”与“具体物理漫步策略”的彻底解耦。
- **平方根扩散定律验证**：模拟实验直观印证统计物理经典结论——经过 $N$ 步无偏随机漫步后，漫步者与起点的期望欧氏距离正比于 $\sqrt{N}$。

## 1. 物理扩散现象与随机漫步模型

随机漫步（Random Walk）是统计物理与随机过程中的基石模型。1827 年英国植物学家罗伯特·布朗在显微镜下观察到水中的花粉颗粒呈现无规则剧烈运动（即布朗运动），后来爱因斯坦在其 1905 年的奇迹年论文中从微观流体分子碰撞热运动角度，首次用随机漫步理论给出了定量的数学物理推导。

在计算程序中，一个基础的二维离散随机漫步包含三个核心要素：
1. **当前空间位置（Location）**：由平面二维连续笛卡尔坐标 $(x, y)$ 完整描述漫步者在某一离散时刻的绝对时空点。
2. **行动规则（Drunk/Walker）**：刻画漫步者在每一次时钟滴答中，基于自身生理或物理环境约束，向周围各个可能方向迁移的概率分布机制。
3. **活动场域（Field）**：漫步者所在的外部边界空间，定义了无障碍平原、周期性环形边界（Torus）或吸收/反射阻挡墙。

---

## 2. 仿真代码的高阶函数解耦

在构建复杂科学模拟程序时，最优雅的软件设计原则是**关注点分离（Separation of Concerns）**。

初学者往往容易犯下一个典型的设计缺陷：为“经典等概率四方向漫步”、“带向北漂移倾向的风向漫步”和“对角线漫步”各自复制粘贴一套包含循环与距离累计的完整模拟代码。这种散落的代码复制会导致后期修改主循环逻辑时出现维护灾难。

在现代高阶编程中，得益于 Python 中**函数作为一等公民（First-Class Citizen）**的天然特性，函数可以像普通整数或字符串一样被赋值给变量、存入集合，或者作为参数传入另一个函数中。我们完全可以把具体的“单步步进逻辑”提炼为纯函数策略接口，并将其作为形式参数动态注入到通用的漫步仿真引擎之中：

```python
import random
import math
from typing import Callable, Tuple

Coordinate = Tuple[float, float]
StepStrategy = Callable[[], Coordinate]

# 策略 1：标准四方向等概率漫步
def standard_step() -> Coordinate:
    return random.choice([(0.0, 1.0), (0.0, -1.0), (1.0, 0.0), (-1.0, 0.0)])

# 策略 2：带有向北偏置（Drift）的非对称漫步
def biased_step() -> Coordinate:
    # 40% 概率向北，各 20% 概率向其他三方向
    r = random.random()
    if r < 0.4:
        return (0.0, 1.1)
    elif r < 0.6:
        return (0.0, -0.9)
    elif r < 0.8:
        return (1.0, 0.0)
    else:
        return (-1.0, 0.0)

# 通用仿真骨架：接收任意步进函数作为参数
def simulate_walk(num_steps: int, step_fn: StepStrategy) -> float:
    """
    执行一次特定策略的随机漫步，返回终点到起点的欧氏直线距离
    """
    x, y = 0.0, 0.0
    for _ in range(num_steps):
        dx, dy = step_fn()
        x += dx
        y += dy
    return math.sqrt(x ** 2 + y ** 2)
```

通过这一高阶抽象屏障，`simulate_walk` 框架对漫步者的内部行为完全保持无知。无论未来新增何种怪异的运动规则（例如速度服从高斯分布或步长随时间衰减），都不需要修改主模拟循环的一行代码。

::: definition 高阶函数（Higher-Order Function）
接收一个或多个函数作为形式参数，或者将一个函数作为执行结果返回的函数。高阶函数构成了函数式编程范式的核心，赋予代码根据外部逻辑灵活特化内部行为的强大参数化能力。
:::

---

## 3. 统计汇总与平方根扩散规律

单次随机漫步的结果具有偶然性，为了观察宏观规律，必须在框架外层封装蒙特卡洛统计循环，多次执行采样求取平均期望距离：

```python
def walk_sim(num_steps: int, num_trials: int, step_fn: StepStrategy) -> float:
    """
    多轮试验汇总求平均最终位移
    """
    distances = [simulate_walk(num_steps, step_fn) for _ in range(num_trials)]
    return sum(distances) / len(distances)

# 观测在不同步数下的平均位移
trials = 500
for steps in [100, 400, 1600, 6400]:
    mean_dist = walk_sim(steps, trials, standard_step)
    ratio = mean_dist / math.sqrt(steps)
    print(f"步数: {steps:4d} | 平均位移: {mean_dist:6.2f} | 距离与 sqrt(N) 比例: {ratio:.3f}")
```

运行上述代码，控制台将输出高度稳定的比值（通常在 $0.88$ 附近）。这在数值上直接证实了理论物理中的经典结论：
$$\mathbb{E}[D_N] \propto \sqrt{N}$$

当步数增加至 4 倍时，漫步者探索的空间直线位移仅翻倍。如果需要移动 10 倍距离，漫步者必须付出 100 倍的时间开销，这深刻解释了为什么分子扩散在宏观尺度上是一种极端低效的物质传输方式。

::: pitfall 忽视步长分布带来的统计失真
在自定义 `step_fn` 时，如果误将 $(dx, dy)$ 分别独立在 $[-1.0, 1.0]$ 区间内均匀采样，漫步者的方向选择在正方形对角线处会被隐式加权（对角线最大距离为 $\sqrt{2}$），破坏原本设想的各向同性（Isotropic）扩散假定。必须通过极坐标转换或者正规化处理维持步长的物理对称性。
:::

## 我的理解

::: insight 组合优于复制的软件工程典范
本讲展示了科学计算中最清爽的工程范式：通用仿真骨架对具体的物理规则保持无知（Agnostic），物理模型仅作为纯函数参数插拔注入。高阶函数消除了面向对象在极简脚本场景下的冗余样板代码，让程序员的精力能够完全聚焦于物理规律与统计假设的对比分析。
:::
