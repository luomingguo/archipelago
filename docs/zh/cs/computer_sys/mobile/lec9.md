---
title: 惯性传感与航位推算
type: lecture
lecture: 9
tags: [inertial-sensing, imu, dead-reckoning, kalman-filter, sensor-fusion]
status: complete
---

# Lec 9 惯性传感与航位推算（Inertial Sensing & Dead Reckoning）

> MIT 6.1820 / MAS.453 · Mobile and Sensor Computing  
> 核心主题：MEMS 惯性测量单元、航位推算动力学与多传感器融合

## TL;DR

- 9-DOF IMU 整合微机电弹簧-电容加速度计、科里奥利陀螺仪与三轴地磁磁力计。
- 航位推算从姿态更新、坐标变换、重力剥离到加速度二次积分，无须外部参考独立解算轨迹。
- 传感器静态零偏经二次积分后导致位置误差随时间平方激增（$\propto \frac{1}{2}bt^2$），纯惯导无法长期独立运行。
- 卡尔曼滤波或互补滤波利用高频低噪的 IMU 结合低频无漂移的 GPS/视觉实现互补融合。

## 1. 惯性测量单元（IMU）硬件微观机理

与依赖空间外发射源的无线定位系统不同，**惯性测量单元（IMU, Inertial Measurement Unit）**是完全自洽、不受电磁屏蔽与多径干扰的内生型自主传感器。

::: definition 9 自由度（9-DOF）IMU 传感器组成
现代商用微机电（MEMS）IMU 在单颗硅芯片上集成了三类正交三轴微型物理传感器：
1. **三轴加速度计（Accelerometer）**：测量载体坐标系下的比力（Specific Force，包含载体线运动加速度与重力矢量合成），输出 $[a_x, a_y, a_z]$；
2. **三轴陀螺仪（Gyroscope）**：测量载体绕各轴旋转的角速度，输出 $[\Omega_x, \Omega_y, \Omega_z]$；
3. **三轴磁力计（Magnetometer）**：感应地球天然弱磁场向量，为偏航角（Yaw）提供无漂移的绝对地磁北极参考。
:::

### 1.1 MEMS 加速度计：梳齿微电容与牛顿第二定律

MEMS 加速度计内部蚀刻出微米尺度的微型机械悬臂梁、悬挂质量块（Proof Mass, $m$）与阻尼弹簧（弹性系数 $k$）：

```text
固定极板   ┌──┐    ┌──┐    ┌──┐ (固定梳齿电容)
           │  │    │  │    │  │
可动质量块 ├──┴────┴──┴────┴──┤ ===> 外力/加速度产生相对位移 x
           │  │    │  │    │  │
固定极板   └──┘    └──┘    └──┘
```

当外界产生加速度 $a$ 时，质量块因惯性产生反向位移 $x$：

$$F = m \cdot a = k \cdot x \implies x = \frac{m}{k} \cdot a$$

质量块两侧延伸出数十组交错的微型梳齿状差分电容。极板间距的微小位移改变了电容值：

$$\Delta C = C_1 - C_2 \approx 2 C_0 \cdot \frac{x}{d_0}$$

电荷放大器将电容微动转化为毫伏级模拟电压，经模数转换器输出离散加速度数值。

::: theorem 重力常在性与静止倾角估计
根据爱因斯坦等效原理，加速度计无法区分引力场与真实加速度。当设备静止在地面时，加速度计测得的合加速度严格等于相反方向的地表支持力，即合矢量大小为 $1.0\text{ g} \approx 9.8\text{ m/s}^2$ 垂直向上。利用静止状态下各轴的重力分量投影，系统可直接以代数方式高精度求解设备的绝对俯仰角（Pitch, $\theta$）与滚转角（Roll, $\phi$）：

$$\theta = \arctan\left(\frac{a_x}{\sqrt{a_y^2 + a_z^2}}\right),\quad \phi = \arctan\left(\frac{a_y}{a_z}\right)$$
:::

### 1.2 MEMS 陀螺仪：科里奥利效应（Coriolis Effect）

在旋转坐标系中，运动质点会受到垂直于运动方向的假想力——**科里奥利力**：

$$\vec{F}_c = -2m \left(\vec{\Omega} \times \vec{v}\right)$$

MEMS 陀螺仪内部通过静电激励使微型质量块以已知线速度 $\vec{v}$ 高频往复振荡。当芯片发生旋转角速度 $\vec{\Omega}$ 时，科氏力迫使质量块向侧向偏移，侧向差分电容捕捉该振动幅度，进而解调出旋转角速度。

---

## 2. 惯性航位推算（Dead Reckoning）动力学流水线

从 IMU 的原始物理输出推导出空间绝对运动轨迹，必须经过严格的四步动力学递推：

```text
原始数据 [ω, a_body]
   │
   ▼ 步骤 1: 四元数 / 旋转矩阵积分更新
当前姿态矩阵 R(t) ──> 姿态角 [Yaw, Pitch, Roll]
   │
   ▼ 步骤 2: 载体坐标系转换至世界导航坐标系
空间总加速度 a_world = R(t) * a_body
   │
   ▼ 步骤 3: 扣除地球重力矢量
纯净运动线加速度 a_linear = a_world - [0, 0, g]^T
   │
   ▼ 步骤 4: 数值二次积分
一次积分得速度 v(t) ──> 二次积分得位置坐标 p(t)
```

### 2.1 坐标变换与重力剥离

载体自身坐标系（Body Frame）随着手机的翻转剧烈变动。必须通过当前姿态旋转矩阵 $R(t)$ 将测量加速度投射至固定不动的世界大地坐标系（World Frame, 如东北天 ENU）：

$$\mathbf{a}_\text{world}(t) = R(t) \cdot \mathbf{a}_\text{body}(t)$$

从世界系加速度中精准扣除重力分量，获得纯净的运动加速度：

$$\mathbf{a}_\text{linear}(t) = \mathbf{a}_\text{world}(t) - \begin{bmatrix} 0 \\ 0 \\ g \end{bmatrix}$$

### 2.2 积分发散困境：二次积分对误差的暴风骤雨

::: example 传感器微小零偏引起的灾难性漂移估算
商用手机级 MEMS 加速度计出厂时即便经过标定，仍存在微小的未补偿直流零偏（Bias, $b$）。设 $b = 0.01\text{ m/s}^2$（仅相当于重力加速度的千分之一，人体感官完全无觉察）：

对恒定零偏 $b$ 进行一次时间积分，速度误差呈线性增长：

$$\Delta v(t) = \int_0^t b\, d\tau = b \cdot t$$

对速度误差再次积分，位置坐标误差随时间呈**二次方（平方）发散**：

$$\Delta p(t) = \iint_0^t b\, d\tau^2 = \frac{1}{2} b \cdot t^2$$

- 运行 $t = 10\text{ 秒}$：$\Delta p = \frac{1}{2} \times 0.01 \times 100 = 0.5\text{ 米}$（尚可接受）；
- 运行 $t = 60\text{ 秒}$（仅 1 分钟）：$\Delta p = \frac{1}{2} \times 0.01 \times 3600 = 18\text{ 米}$（完全脱轨）；
- 运行 $t = 10\text{ 分钟}$（600 秒）：$\Delta p = \frac{1}{2} \times 0.01 \times 360000 = 1800\text{ 米}$（误差近 2 公里）！
:::

::: theorem 纯惯导的漂移发散不可逆性
陀螺仪的角度漂移 $\Delta\theta \propto \epsilon \cdot t$ 还会导致姿态矩阵 $R(t)$ 发生倾斜，从而将部分重力矢量 $g$ 错误投影为水平加速度，导致水平位置误差以**时间三次方（$\propto \frac{1}{6} g \epsilon t^3$）**急剧崩溃。因此，消费级纯惯性导航绝不可能在无外部修正的前提下长时间独立工作。
:::

---

## 3. 传感器融合滤波：互补滤波与扩展卡尔曼滤波

针对单一传感器的致命短板，系统工程采用信息融合消除发散：

| 传感器类型 | 高频特性（毫秒级突变） | 低频与长期特性（分钟至小时级） | 核心致命缺陷 |
|:---|:---|:---|:---|
| **陀螺仪 / 加速度计** | **极佳**（响应快、无延时、高采样率） | **极差**（静态积分二次漂移发散） | 零偏积累 |
| **GPS / 无线基站** | **差**（更新率低 1 Hz，多径跳变跳点）| **极佳**（长期绝对坐标无误差积累） | 室内丢失、瞬态延迟 |
| **地磁磁力计** | 易受车体、钢筋瞬态电磁尖峰干扰 | 静态指向稳定指示地磁北极 | 室内局部磁场畸变 |

### 3.1 互补滤波直觉（Complementary Filter）

在频域中将互补频段信号加权拼接：

$$\hat{\theta}(t) = \alpha \cdot \underbrace{\left(\hat{\theta}(t-1) + \Omega(t) \cdot \Delta t\right)}_{\text{高通：积分陀螺仪追踪快速旋转}} + (1 - \alpha) \cdot \underbrace{\theta_\text{accel}(t)}_{\text{低通：重力加速度锚定水平基准}}$$

典型参数 $\alpha = 0.98$：在毫秒级瞬态完全信任陀螺仪积分，在数秒级稳态依靠重力倾角缓慢修正陀螺仪零偏，计算极其轻量，广泛运行于低算力 MCU。

### 3.2 卡尔曼滤波（Kalman Filter）状态观测

在更高精度的导航系统中，**卡尔曼滤波（KF / EKF）**基于高斯马尔可夫模型，以最小均方误差为目标在“模型预测”与“传感器观测”之间动态平衡：

$$\text{状态预测：}\quad \hat{\mathbf{x}}_{k|k-1} = \mathbf{F} \hat{\mathbf{x}}_{k-1|k-1} + \mathbf{B} \mathbf{u}_k$$

$$\text{协方差预测：}\quad \mathbf{P}_{k|k-1} = \mathbf{F} \mathbf{P}_{k-1|k-1} \mathbf{F}^T + \mathbf{Q}$$

$$\text{卡尔曼增益：}\quad \mathbf{K}_k = \mathbf{P}_{k|k-1} \mathbf{H}^T \left(\mathbf{H} \mathbf{P}_{k|k-1} \mathbf{H}^T + \mathbf{R}\right)^{-1}$$

$$\text{状态更新：}\quad \hat{\mathbf{x}}_{k|k} = \hat{\mathbf{x}}_{k|k-1} + \mathbf{K}_k \left(\mathbf{z}_k - \mathbf{H} \hat{\mathbf{x}}_{k|k-1}\right)$$

当 GPS 信号良好时，观测噪声协方差 $\mathbf{R}$ 极小，增益 $\mathbf{K}_k$ 增大，滤波器强力纠偏 IMU 零偏；当车辆驶入隧道 GPS 丢失时，系统自动切入纯预测模式，依赖 IMU 平滑过渡。

---

## 4. 惯性漂移控制与传感器融合本质

::: insight
惯性导航是系统控制理论中最具启发性的领域之一：
1. **微分与积分的认知悖论**：在数字世界中，采样率越高通常意味着信息越完整；但在惯性导航中，积分过程把传感器的高频白噪声转化为一阶随机游走（Random Walk），更把常数零偏放大为二次发散。这提醒我们：没有绝对外部物理基准的数学积分，本质上是在自闭环内自我放大混乱度。
2. **行人步态先验对积分的拯救（PDR 与 ZUPT）**：如果直接积分不可行，手机计步器与行人导航（PDR）是如何实现的？答案是引入了生物力学物理先验——人类行走不是火箭发射，而是周期的离散步态。当脚掌接触地面的瞬间，足部对地速度在物理上严格为零！利用这一先验引入**零速更新（ZUPT, Zero Velocity Update）**，在每次脚着地瞬间强行将积分速度归零并反向估计加速度零偏，成功将误差从 $t^2$ 压缩为与步数成线性关系。将物理世界的不变性（Invariance）融入数学估计算法，往往是打破工程发散死局的关键法宝。
:::
