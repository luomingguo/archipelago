---
title: '人工神经网络基础：感知机与误差反向传播算法 (Neural Networks & Backpropagation)'
type: lecture
lecture: 6
tags: [neural-networks, deep-learning, backpropagation, perceptron]
status: complete
---

# Lec 6 人工神经网络基础：感知机与误差反向传播算法 (Neural Networks & Backpropagation)

> MIT 15.062J 数据挖掘 · 讲义 6 · 授课教师：Prof. Roy Welsch / Nitin Patel

## TL;DR

- 人工神经网络（ANN）受生物大脑神经元突触网络启发，是现代深度学习的奠基石。
- 单层感知机（Perceptron）仅能表达线性超平面，被明斯基（Minsky）异或（XOR）难题判定死刑。
- 多层前馈网络（MLP）引入非线性激活函数，奠定了泛函万能逼近定理（Universal Approximation）。
- 误差反向传播算法（Backpropagation）利用多元微积分链式法则，实现了对数百万权重梯度的端到端高效求解。

## 1. 生物神经元抽象与感知机（Perceptron）的兴衰

1943 年，神经生理学家沃伦·麦卡洛克（Warren McCulloch）与数学家沃尔特·皮茨（Walter Pitts）提出了人类历史上第一个神经元数学模型（M-P 神经元）。1958 年，弗兰克·罗森布拉特（Frank Rosenblatt）在康奈尔航空实验室制造出了世界上第一台硬件神经网络机器——**感知机（Perceptron）**。

### 1.1 感知机的数学结构

单层感知机模拟生物树突接收电信号并经过轴突放电的生物过程：
输入为特征向量 $x = (x_1, x_2, \dots, x_p)$，每个输入通道配备可学习的连接突触权重 $w_j$：
$$z = \sum_{j=1}^p w_j x_j + b = w^T x + b$$
通过阶跃激活函数（Step Activation Function）输出二元判定：
$$\hat{y} = f(z) = \begin{cases} +1, & z \ge 0 \\ -1, & z < 0 \end{cases}$$

### 1.2 第一次 AI 寒冬：异或（XOR）危机

感知机诞生之初引发了媒体的疯狂狂欢，被盛赞为“会思考的电子大脑原型”。然而在 1969 年，麻省理工学院人工智能实验室联合创始人马文·明斯基（Marvin Minsky）与西摩尔·帕珀特（Seymour Papert）出版了严密的数学专著《感知机》（Perceptrons）。

明斯基从数学上严密证明：**单层感知机本质上是一个严格的线性分类器，其决策边界必须是空间中的一条超平面。因此，它甚至连人类逻辑学中最简单的“异或逻辑（XOR）”都绝对无法解决**！
- 异或逻辑真值表：$(0, 0) \to 0, \ (1, 1) \to 0, \ (1, 0) \to 1, \ (0, 1) \to 1$；
- 在二维平面上，四个点呈现交叉对角分布，没有任何一条直线能够将它们两两完全分开！
明斯基的这一纸严谨死刑判决，导致全球政府与学术界瞬间撤回了对神经网络的全部科研资助，直接引爆了长达十余年的第一次人工智能严冬。

```mermaid
flowchart LR
    Input[输入层神经元 x_1, x_2, ... x_p] --> Weights[突触权重线性加权求和: z = w^T x + b]
    Weights --> Activation[非线性激活函数: Sigmoid / Tanh / ReLU]
    Activation --> Hidden[隐藏层神经元表示: 提取高维抽象特征]
    Hidden --> OutputLayer[输出层: 输出最终分类概率与预测值]
    OutputLayer --> Loss[损失函数计算: 预测误差 Loss]
    Loss --> Backprop[反向传播引擎: 链式法则自顶向下传递梯度更新权重]
    Backprop --> Weights
```

## 2. 多层前馈网络（MLP）与激活函数

走出绝境的唯一钥匙是**引入隐藏层（Hidden Layers）与非线性激活函数**。

若网络仅由多层纯线性变换堆叠：$W_2(W_1 x) = (W_2 W_1) x = W_{\text{new}} x$，多层矩阵相乘依然等价于单一线性层。只有在每个神经元输出端嵌入**非线性激活函数（Nonlinear Activation Function）**，网络才能扭曲空间，折叠出任意复杂的决策边界：

1. **Sigmoid 函数**：
   $$\sigma(z) = \frac{1}{1 + e^{-z}}, \quad \sigma'(z) = \sigma(z)(1 - \sigma(z))$$
   导数在两端趋于零，深层网络中极易引发**梯度消失（Vanishing Gradient）**；
2. **双曲正切函数（Tanh）**：
   $$\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}, \quad \text{零均值对称输出}$$
3. **线性整流函数（ReLU）**：
   $$\text{ReLU}(z) = \max(0, z)$$
   正区间导数恒为 1，极大加速了深度网络的梯度回传收敛速度。

::: theorem [万能逼近定理 (Universal Approximation Theorem, Hornik 1989)]
设 $\sigma(\cdot)$ 为任意非恒常、有界的连续非线性激活函数。对于任意紧致子集 $K \subset \mathbb{R}^n$ 上的任意连续真实函数 $f(x)$，以及任意给定的误差精度 $\epsilon > 0$：
**只需包含一个隐藏层、且包含足够多神经元的前馈神经网络，就能够以任意精度 $\epsilon$ 逼近目标函数 $f(x)$**！
该定理奠定了多层神经网络作为全人类数学史上“通用函数拟合器”的崇高地位。
:::

## 3. 误差反向传播算法（Backpropagation）的核心数学推导

尽管万能逼近定理在理论上证明了网络的存在性，但包含成千上万个参数权重的庞大网络，究竟该如何通过计算高效调整每个神经元连接处的微观权重？

1986 年，戴维·鲁梅尔哈特（David Rumelhart）、杰弗里·辛顿（Geoffrey Hinton）与罗纳德·威廉姆斯（Ronald Williams）在《自然》（Nature）发表经典论文，正式确立了**误差反向传播算法（Backpropagation / BP 算法）**。

### 3.1 链式求导法则（The Chain Rule）

设网络输出层预测值为 $\hat{y}$，真实标签为 $y$。定义平方和损失函数（Loss Function）：
$$E = \frac{1}{2} (y - \hat{y})^2$$

考虑某隐藏层神经元 $j$ 与其上游输入神经元 $i$ 之间的权重 $w_{ij}$。目标是计算损失函数关于该权重的梯度偏导数 $\frac{\partial E}{\partial w_{ij}}$，以便执行**梯度下降更新（Gradient Descent）**：
$$w_{ij} \leftarrow w_{ij} - \eta \frac{\partial E}{\partial w_{ij}}$$
其中 $\eta > 0$ 为学习率（Learning Rate）。

依据微积分复合函数求导链式法则，将偏导数严谨拆解为三项连续乘积：
$$\frac{\partial E}{\partial w_{ij}} = \frac{\partial E}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z_j} \cdot \frac{\partial z_j}{\partial w_{ij}}$$
- **第一项（误差传播）**：$\frac{\partial E}{\partial \hat{y}} = - (y - \hat{y})$；
- **第二项（激活函数局域梯度）**：$\frac{\partial \hat{y}}{\partial z_j} = f'(z_j)$；
- **第三项（输入信号强度）**：由于 $z_j = \sum w_{ik} a_i + b$，故 $\frac{\partial z_j}{\partial w_{ij}} = a_i$（来自上游节点的激活输出）。

定义局部误差敏感度 $\delta_j = \frac{\partial E}{\partial z_j}$。对于隐藏层神经元，其误差敏感度 $\delta_j$ 可以通过其所有下游下游连接节点的误差 $\delta_k$ **由后向前反向递推（Backward Recursion）**计算：
$$\delta_j = f'(z_j) \sum_{k \in \text{Downstream}} \delta_k w_{jk}$$

这意味着：**正向传播（Forward Pass）自左向右逐层计算每个神经元的激活值；反向传播（Backward Pass）自右向左逐层传递误差梯度！**算法以惊人的计算效率同时求解出全网数百万个权重的更新方向。

::: example [手织布与消费信贷中的非线性风险曲面拟合]
在处理信用卡欺诈检测时，欺诈行为往往呈现环形包裹或高度扭曲的非凸分布（例如正常用户的交易金额集中在中间区间，极小额试探刷卡与极大额异地套现均属于盗刷高危区）。
逻辑回归由于线性超平面限制必须依赖人工费力构建复杂的交叉多项式特征；而包含两个隐藏层的 MLP 神经网络，通过神经元权重的自发迭代组合，自动在多维特征空间中弯曲出一个封闭的包络曲面，将两端的欺诈异常精准圈选。
:::

::: pitfall [过拟合、鞍点与局部极小值黑洞]
神经网络的损失函数曲面是一个极其复杂的非凸高维流形，充斥着大量的**局部极小点（Local Minima）与平坦鞍点（Saddle Points）**。此外，网络强大的参数拟合能力使其极其容易把训练集的背景噪声当成规律死记硬背。现代实战中必须引入权重衰减正则化（Weight Decay / L2 Regularization）、随机失活（Dropout）与早停机制（Early Stopping）对其施加缰绳。
:::

::: insight [我的理解：神经网络是用算力堆叠出的自适应感知机器]
在传统编程世界中，人类工程师必须事无巨细地写下每一条 `if-else` 业务规则；而神经网络彻底颠覆了软件工程的底层范式。我们不再为计算机编写规则，我们只是搭建起一座连接着数万个微观参数的网状突触脚手架，随后把海量数据像电流一样倾泻而入。在一次次前向计算与反向误差修正的冲刷下，参数自己找到了秩序，网络自己学会了看清世界的纹理。这就是机器自我学习的破晓时刻。
:::
