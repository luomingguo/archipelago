---
title: 曲线拟合、过拟合与交叉验证
type: lecture
lecture: 9
tags: [curve-fitting, least-squares, overfitting, cross-validation, r-squared]
status: complete
source: https://introcomp.mit.edu/fall26
---

# Lec 9 曲线拟合、过拟合与交叉验证（Curve-Fitting & Validation）

> MIT 6.100 · 计算机科学与 Python 编程导论 · Fall 2026 · 教材参考：Guttag 20

## TL;DR

- **多项式最小二乘拟合**：利用多项式函数 $y = \sum_{k=0}^d c_k x^k$ 逼近连续实验数据，求解使得总残差平方和达到极小的最优多项式系数向量。
- **决定系数（$R^2$ 评分）**：以基准均值模型的总方差为分母，$R^2 = 1 - \frac{\text{RSS}}{\text{TSS}}$ 衡量模型对观测数据方差变异的解释比例，取值在 $[0, 1]$ 之间。
- **过拟合与交叉验证（Cross-Validation）**：盲目提高模型复杂度（如过高的多项式阶数）会导致模型死记噪声（高方差低泛化）；必须将数据划分为训练集与验证集，以未见样本的泛化误差评估模型。

## 1. 实验观测与最小二乘曲线拟合

在科学研究与工程测量中，物理定律往往隐藏在伴随测量噪声的实验散点背后（例如弹簧伸长量与拉力、RC 电路充放电曲线）。曲线拟合（Curve Fitting）的目标是：**寻找一条最具代表性的连续数学曲线，穿透随机误差，恢复潜在的物理本质**。

设有一组 $N$ 个观测点 $(x_1, y_1), \dots, (x_N, y_N)$。我们希望选择一个 $d$ 阶多项式模型：
$$\hat{y}(x) = c_d x^d + c_{d-1} x^{d-1} + \dots + c_1 x + c_0$$

最小二乘准则要求极小化残差平方和：
$$\text{RSS} = \sum_{i=1}^N (y_i - \hat{y}(x_i))^2$$

在 Python 中，`numpy.polyfit(x, y, deg)` 通过求解正规方程组（Normal Equations），能够以极高数值稳定性直接返回最佳系数数组 $[c_d, c_{d-1}, \dots, c_0]$。

---

## 2. 拟合优度度量：决定系数 $R^2$

如何量化评估一条拟合曲线究竟是“优秀”还是“糟糕”？如果单纯比较残差绝对值，由于原始数据量纲不同（如纳秒 vs 光年），不同问题之间完全无法横向对比。

统计学引入了无量纲的**决定系数（Coefficient of Determination, $R^2$）**：

::: definition 决定系数（$R^2$ 统计量）
$$R^2 = 1 - \frac{\sum_{i=1}^N (y_i - \hat{y}_i)^2}{\sum_{i=1}^N (y_i - \bar{y})^2} = 1 - \frac{\text{RSS}}{\text{TSS}}$$
其中 $\text{TSS}$ 是总平方和（仅用均值 $\bar{y}$ 预测时的基准误差），$\text{RSS}$ 是当前模型的残差平方和。
- $R^2 = 1.0$：模型完美穿过所有数据点，预测误差为 0；
- $R^2 = 0.0$：模型的预测能力等同于盲目猜测均值；
- $R^2 < 0.0$：模型拟合极差，表现甚至劣于直接输出常数均值。
:::

```python
import numpy as np

def compute_r_squared(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    计算拟合预测结果的决定系数 R^2
    """
    mean_y = np.mean(y_true)
    total_sum_squares = np.sum((y_true - mean_y) ** 2)
    residual_sum_squares = np.sum((y_true - y_pred) ** 2)
    
    if total_sum_squares == 0:
        return 1.0 if residual_sum_squares == 0 else 0.0
    return 1.0 - (residual_sum_squares / total_sum_squares)
```

---

## 3. 过拟合陷阱与训练-测试集交叉验证

初学者极容易陷入一个致命思维误区：**“多项式阶数越高，曲线在图表上贴合得越紧密，$R^2$ 越接近 1.0，模型就越好”**。

在实际场景中，数据必然混杂有不可避免的高频随机测量噪声。如果给模型赋予了过量的自由参数（例如用 16 阶多项式拟合 20 个散点），多项式会剧烈扭曲振荡以强行穿过每一个噪声点。这种现象被称为**过拟合（Overfitting）**：模型在训练集上拥有极高的拟合度，但在面对任何未知的新数据时，预测误差将发生灾难性的指数级发散！

### 训练-测试分离与泛化评估

为了识别并防范过拟合，机器学习与统计建模建立了金科玉律：**绝对不能在用于训练的同一批数据上评估模型的预测能力**。如果在已知数据上评分，模型只需要死记硬背每个点的坐标即可获得满分，但这在面向未来的真实预测中毫无意义。

标准的验证流程是将有限的数据集严格划分为两个互斥的子空间：
1. **训练集（Training Set）**：通常占原始样本的 70%~80%，这部分数据被全量提供给优化求解算法，用于计算和拟合最佳的多项式参数系数。
2. **测试/验证集（Validation Set）**：占剩余的 20%~30%，在参数拟合阶段必须被完全隔离并对算法严格保密，仅在系数解算完毕之后，输入 $x_{\text{test}}$ 计算预测输出，并以此客观量化模型面对全新未知输入时的真实泛化误差。

下面我们通过合成带有高斯测量白噪声的二次曲线实验，展示不同多项式阶数在训练集与测试集上的表现分野：

```python
import numpy as np

def cross_validate_polynomials(x: np.ndarray, y: np.ndarray, degrees: list) -> None:
    """
    对不同多项式阶数执行训练集拟合与测试集泛化验证
    """
    # 随机打乱并按 7:3 划分
    indices = np.arange(len(x))
    np.random.seed(42)
    np.random.shuffle(indices)
    
    split_point = int(len(x) * 0.7)
    train_idx, test_idx = indices[:split_point], indices[split_point:]
    
    x_train, y_train = x[train_idx], y[train_idx]
    x_test, y_test = x[test_idx], y[test_idx]
    
    for deg in degrees:
        coeffs = np.polyfit(x_train, y_train, deg)
        pred_train = np.polyval(coeffs, x_train)
        pred_test = np.polyval(coeffs, x_test)
        
        r2_train = compute_r_squared(y_train, pred_train)
        r2_test = compute_r_squared(y_test, pred_test)
        print(f"阶数 {deg:2d} | 训练集 R^2: {r2_train:.3f} | 测试集 R^2: {r2_test:.3f}")

# 构造底层二次关系 y = 2*x^2 + 3 并叠加高斯白噪声
x_raw = np.linspace(-3, 3, 40)
y_raw = 2.0 * (x_raw ** 2) + 3.0 + np.random.normal(0, 1.5, size=len(x_raw))

cross_validate_polynomials(x_raw, y_raw, degrees=[1, 2, 8, 15])
```

在执行上述代码时，我们可以观察到极其典型的数据科学特征现象：
- 当阶数为 1 时：欠拟合（Underfitting），直线无法表达二次曲线的弯曲趋势，训练集和测试集的 $R^2$ 均偏低。
- 当阶数为 2 时：完美捕获底层物理法则，训练集与测试集均保持在 $0.95$ 以上的优异高分，模型展现出绝佳的泛化预测能力。
- 当阶数上升至 8 和 15 时：训练集 $R^2$ 持续攀升并逼近 $0.999$，然而测试集 $R^2$ 急剧暴跌为严重的负值，彻底暴露了高阶模型的过拟合脆弱性。

::: pitfall 奥卡姆剃刀与模型复杂性惩罚
“若无必要，勿增实体”。在两个对测试数据具有相近预测能力的模型之间，永远优先选择结构更简单、参数更少的那一个。简单模型不仅计算开销小，更具备抵御现实世界分布漂移（Distribution Shift）的稳健鲁棒性。
:::

## 我的理解

::: insight 拟合是记忆，泛化是智慧
从曲线拟合到深度学习，数据科学的核心矛盾始终是“记忆历史数据”与“泛化预测未来”之间的拉锯战。计算机在记忆特定样本细节上具有无限的优势，但真正的工程智能恰恰体现在懂得克制参数的自由度，主动过滤高频随机噪声，提炼出跨越时空不变的稳定客观规律。
:::
