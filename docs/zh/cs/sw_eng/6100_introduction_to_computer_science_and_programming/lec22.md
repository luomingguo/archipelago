---
title: 基于面向对象的物理仿真：理想气体定律
type: lecture
lecture: 22
tags: [physical-simulation, oop-design, particle-collision, ideal-gas-law, modeling]
status: complete
source: https://introcomp.mit.edu/fall26
---

# Lec 22 基于面向对象的物理仿真：理想气体定律（Physical Simulation & Ideal Gas Law）

> MIT 6.100 · 计算机科学与 Python 编程导论 · Fall 2026 · 官方讲义核心内容

## TL;DR

- **面向对象微观仿真范式**：将微观物理实体建模为自主封装的实例对象（如 `Molecule` 与 `Container`），通过离散时间步步进（Time-stepping）驱动位置更新与弹性碰撞检测。
- **动量守恒与压强涌现机制**：气体压强本质上是海量微观气体分子碰撞容器壁时发生的动量交换累积效应；通过追踪每秒单位面积上的总冲量，从微观粒子力学自然推导宏观热力学状态。
- **理想气体状态方程（$PV = Nk_BT$）验证**：通过调节容器体积 $V$、分子数量 $N$ 与平均动能（温度 $T$），计算机仿真数据严密重现玻尔兹曼理想气体定律。

---

## 1. 物理仿真的面向对象抽象架构

在传统科学计算与经典力学教学中，物理系统的演化往往依赖于微积分连续方程的闭式解析解（Analytical Solutions）。然而，当封闭容器中存在成百上千个具有独立质量、空间位置与随机初速度的微观粒子时，粒子与粒子之间的散射以及粒子与多边形边界之间的碰撞反射，构成了极其繁复的分段非线性边界条件。连续微积分方程在此类多体问题面前通常难以直接求解。

计算思维为我们提供了另一种极其强大而优雅的求解范式——基于离散时间步进的数值动力学仿真（Numerical Time-stepping Simulation）。面向对象程序设计（OOP）天然契合这种自底向上的建模视角：
- **微观实体自主性**：现实世界中的每个物理实体都拥有自身独立的几何属性、动力学状态与物理法则。我们将单个微观分子建模为高内聚的 `Molecule` 对象，使其具备自省和自主移动能力；
- **环境边界解耦**：容器 `GasContainer` 充当刚体外场，专门负责施加空间几何约束与边界反弹计算，与分子的具体运动逻辑形成清晰的正交分工；
- **全局调度与宏观统计**：控制器 `GasSimulation` 统一管理全局时钟流逝 $\Delta t$，驱动所有活动分子的状态迁移，并在时间轴上积分收集微观碰撞事件，最终在宏观统计层面涌现出压强与温度等热力学参量。

```text
       ┌────────────────── Box: 容器 (W, H) ──────────────────┐
       │                                                      │
       │    o Molecule 1 (v_x, v_y)                           │
       │     \                                                │
       │      \                                               │
       │       v                                              │
       │      --- (弹性碰撞墙壁: v_x -> -v_x, 累计冲量 dp)     │
       │                                                      │
       │            o Molecule 2                              │
       └──────────────────────────────────────────────────────┘
```

这种架构使原本高深复杂的统计物理学推导，转化为计算机内存中若干自治对象之间的状态流转与局部交互。

---

## 2. 核心类体系设计与动力学演化

在弹性碰撞模型中，当分子与左右垂直边界碰撞时，垂直速度 $v_y$ 保持不变，水平速度反转：$v_x \leftarrow -v_x$。此过程中容器壁受到的动量冲量为：
$$\Delta p_x = 2 m |v_x|$$

同理，上下边界碰撞反转 $v_y$，产生的冲量为 $\Delta p_y = 2 m |v_y|$。宏观压强 $P$ 定义为在观测时长 $T_{\text{total}}$ 内，所有碰撞产生的总冲量除以容器壁周长（二维情形）与观测时长的乘积：
$$P = \frac{\sum \Delta p}{\text{Perimeter} \times T_{\text{total}}}$$

### 2.1 微观粒子与容器碰撞模型（Molecule 与 GasContainer）

在微观粒子建模中，`Molecule` 承担着记录质点物理状态的责任。根据经典力学假设，理想气体分子被视作无体积的质点，分子间不考虑范德华力或长程相互作用势能，仅在与刚体容器壁接触时发生瞬间完全弹性碰撞。

类的设计要素包含：
1. **单一职责原则与实体解耦**：为什么不让 `Molecule` 自身负责边界检测？因为分子作为微观质点，不应该感知容器的存在形式（容器可以是长方形、圆形或三维立方体）。`Molecule` 仅专注于自身运动状态的演进，而 `GasContainer` 专门负责几何拓扑判定。这种职责划分是高内聚、低耦合架构设计的典范；
2. **状态向量维护与牛顿运动学**：实例属性 `self.x` 与 `self.y` 记录分子在二维平面笛卡尔坐标系中的绝对位置，而 `self.vx` 与 `self.vy` 则分别表示水平与垂直速度分量。在每一个离散时间步 $\Delta t$ 内，位置的更新遵循经典牛顿一阶积分：$x \leftarrow x + v_x \Delta t$ 与 $y \leftarrow y + v_y \Delta t$；
3. **动能自省计算**：方法 `kinetic_energy` 基于标准物理公式 $E_k = \frac{1}{2} m (v_x^2 + v_y^2)$ 返回分子的即时平动动能。在统计物理中，所有分子的平均动能直接正比于系统的绝对温度；
4. **刚体容器边界判定与冲量传递**：`GasContainer` 对象管理一个尺寸为 $W \times H$ 的固定矩形空间。方法 `resolve_collisions` 执行关键的碰撞检测。当粒子越过左壁（$x \le 0$）或右壁（$x \ge W$）时，法向速度反向（$v_x \leftarrow -v_x$），同时反作用于容器壁的动量冲量绝对值为 $\Delta p = |(-m v_x) - (m v_x)| = 2 m |v_x|$。由于连续的动量冲击，容器壁累积了宏观推力。

```python
import random
import math
from typing import List


class Molecule:
    """微观气体分子：封装质量、空间坐标与运动速度"""
    def __init__(self, x: float, y: float, vx: float, vy: float, mass: float = 1.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        
    def move(self, dt: float) -> None:
        """按当前速度沿匀速直线运动推进时间步 dt"""
        self.x += self.vx * dt
        self.y += self.vy * dt
        
    def kinetic_energy(self) -> float:
        """计算单分子的平动动能 E_k = 0.5 * m * v^2"""
        return 0.5 * self.mass * (self.vx ** 2 + self.vy ** 2)


class GasContainer:
    """刚体密封容器：负责限制分子边界并记录反冲冲量"""
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
        self.total_momentum_transferred = 0.0
        
    def resolve_collisions(self, p: Molecule) -> None:
        """检测分子与四面刚性容器壁的弹性碰撞，并转移冲量"""
        if p.x <= 0.0:
            p.x = -p.x
            p.vx = -p.vx
            self.total_momentum_transferred += 2.0 * p.mass * abs(p.vx)
        elif p.x >= self.width:
            p.x = 2.0 * self.width - p.x
            p.vx = -p.vx
            self.total_momentum_transferred += 2.0 * p.mass * abs(p.vx)
            
        if p.y <= 0.0:
            p.y = -p.y
            p.vy = -p.vy
            self.total_momentum_transferred += 2.0 * p.mass * abs(p.vy)
        elif p.y >= self.height:
            p.y = 2.0 * self.height - p.y
            p.vy = -p.vy
            self.total_momentum_transferred += 2.0 * p.mass * abs(p.vy)
```

在碰撞边界的镜面修正逻辑中，不仅反转了垂直于壁面的法向速度分量，还将超出边界的微小位移通过关于边界对称翻折折回（例如 $x \leftarrow 2W - x$），以抵消离散时间步进带来的轻微穿透误差。这种几何镜像处理保证了微观层面的相空间体积守恒。

### 2.2 仿真主循环与宏观压强统计（GasSimulation）

微观粒子与静态容器搭建就绪后，系统需要一个调度器驱动整套动力学演化。`GasSimulation` 作为顶层外观与控制器，整合了随机采样、状态步进与宏观观测三大职责：

1. **初态热平衡随机生成**：分子初始坐标在容器内部 $[0.1W, 0.9W]$ 范围内均匀随机分布，避免分子一开始就紧贴墙壁产生边界初态伪影。速度分量 $v_x, v_y$ 采样自零均值高斯分布 $\mathcal{N}(0, \sigma^2)$，这在统计力学中精确对应于麦克斯韦-玻尔兹曼速率分布的二维形式，方差 $\sigma^2$ 直接代表气体的初试温度标尺；
2. **离散时间演化引擎**：在每次时间步进循环中，调度器遍历全部粒子调用 `m.move(dt)` 更新坐标，紧接着调用容器的 `resolve_collisions(m)` 完成即时反弹判定。如果容器内包含 $N$ 个粒子，仿真持续 $S$ 个步长，单次仿真的总时间复杂度为严谨的 $O(N \cdot S)$；
3. **微观到宏观物理量的换算积分**：根据压强的物理定义，压强是单位面积（二维情况下为单位周长）在单位时间内所承受的总冲量：
   $$P = \frac{\Delta p_{\text{total}}}{\text{Perimeter} \cdot T_{\text{total}}}$$
   与此同时，系统求取全体分子的动能均值作为温度代用指标，并将实际测得的 $P \cdot V / (N \cdot T)$ 比值作为理想气体状态常数的无量纲验证指标；
4. **能量守恒不变量断言**：在完全弹性碰撞模型中，整个封闭系统的总机械能必须保持严格守恒。控制器可以在每个宏观采样周期检查 $\sum E_k$ 的波动，如果能量变化超出浮点舍入误差（$\epsilon > 10^{-7}$），则表明时间步长可能过大或者碰撞算法存在数值阻尼缺陷；
5. **热力学观测指标封装**：返回字典对实验关键维度进行了集中映射。`volume` 对应容器二维占地面积 $W \times H$，`temperature_proxy` 对应微观平均动能，而无量纲比值 `pv_ratio` 直接度量宏观压力容积乘积与粒子内能的比率。在理想气体模型中，该比值在统计误差范围内恒定收敛，提供了极佳的自动化单元测试断言标靶。

```python
class GasSimulation:
    """仿真调度控制器：统筹分子集合在容器内的离散时间演进"""
    def __init__(self, num_molecules: int, width: float, height: float, temp_factor: float):
        self.container = GasContainer(width, height)
        self.molecules: List[Molecule] = []
        
        # 初始化均匀随机分布在容器内的分子
        for _ in range(num_molecules):
            x = random.uniform(0.1 * width, 0.9 * width)
            y = random.uniform(0.1 * height, 0.9 * height)
            # 速度分量服从高斯分布，标准差与温度平方根成正比
            vx = random.gauss(0, temp_factor)
            vy = random.gauss(0, temp_factor)
            self.molecules.append(Molecule(x, y, vx, vy))
            
    def run(self, total_time: float, dt: float = 0.01) -> dict:
        """推进动力学仿真并输出宏观热力学参数"""
        steps = int(total_time / dt)
        for _ in range(steps):
            for m in self.molecules:
                m.move(dt)
                self.container.resolve_collisions(m)
                
        # 统计宏观量
        wall_length = 2.0 * (self.container.width + self.container.height)
        pressure = self.container.total_momentum_transferred / (wall_length * total_time)
        avg_kinetic_energy = sum(m.kinetic_energy() for m in self.molecules) / len(self.molecules)
        area = self.container.width * self.container.height
        
        return {
            "pressure": pressure,
            "volume": area,
            "temperature_proxy": avg_kinetic_energy,
            "pv_ratio": (pressure * area) / (len(self.molecules) * avg_kinetic_energy)
        }
```

通过这一主循环，微观离散时间步上的几何碰撞冲量被平滑积分并换算为连续压强读数，完成了微观力学向宏观状态变量的跨尺度跃迁。这种利用简单微观行为推导宏观统计属性的计算实验，是现代计算物理与分子动力学模拟（Molecular Dynamics）的核心基础。

---

## 3. 宏观物理定律的涌现（Emergence）

当我们运行上述模拟程序时，一件极其震撼的事情发生了：程序中没有写下任何一条宏观热力学公式，每一个粒子仅仅遵循最基础的牛顿运动定律与几何反弹规则。

然而，通过观察仿真返回的统计结果：
```python
sim = GasSimulation(num_molecules=200, width=50.0, height=50.0, temp_factor=10.0)
results = sim.run(total_time=20.0)
print(f"模拟计算压强 P: {results['pressure']:.3f}")
print(f"状态比值 (P * V) / (N * T): {results['pv_ratio']:.3f}")
```

在多次运行中，比值 $\frac{P \cdot V}{N \cdot T}$ 始终高度稳定在一个恒定常数附近！
- 当我们将容器宽度 `width` 缩减一半（体积 $V$ 减半）时，分子碰撞边界的频率自然翻倍，测得的压强 $P$ 准确翻倍（波义耳定律：$P \propto 1/V$）；
- 当我们将初始速度标准差翻倍（温度 $T$ 提高 4 倍）时，压强随之线性上升 4 倍（查理定律：$P \propto T$）。

这充分展现了复杂自适应系统（Complex Adaptive Systems）中的**涌现（Emergence）**魅力：简单的微观局部交互规则，在面向对象封装的大规模并发协作下，自发组织出高度有序的宏观统计物理规律。

::: pitfall [时间步长 $\Delta t$ 过大导致穿墙越狱]
在离散时间步进仿真中，若 $\Delta t$ 设定过大，某个高速运动的粒子在一个时钟周期内的位移可能直接跃过容器边界甚至穿透外壁，导致碰撞检测逻辑失效。在计算物理中，必须保证 $\Delta t \ll \text{边界尺寸} / v_{\max}$（Courant-Friedrichs-Lewy 条件）。
:::

---

## 我的理解

::: insight [面向对象让计算机成为虚拟现实沙盒]
本讲是将前面二十讲所有知识体系融会贯通的巅峰实战：它结合了列表推导式、高斯随机采样、类与封装、物理守恒断言以及统计宏观估计。面向对象编程的最高价值，在于赋予了程序员创造虚拟数字宇宙的能力。通过对简单法则的代码建模，计算机打破了真实物理实验室的时空限制，成为洞悉物质深层演化机制的数字显微镜。
:::
