---
title: '比例与计数数据推断'
type: lecture
lecture: 8
tags: [proportions, chi-square-test, contingency-table, goodness-of-fit, multinomial-distribution]
status: complete
source: 'https://ocw.mit.edu/courses/15-075j-statistical-thinking-and-data-analysis-fall-2011/resources/mit15_075jf11_chpt09a/'
---

# Lec 8 比例与计数数据推断（Inferences for Proportions and Counts）

> MIT 15.075J / ESD.07J · Statistical Thinking and Data Analysis · Fall 2011
> 授课教师：Prof. Cynthia Rudin
> 资料来源：[MIT OpenCourseWare Chapter 9 Notes](https://ocw.mit.edu/courses/15-075j-statistical-thinking-and-data-analysis-fall-2011/resources/mit15_075jf11_chpt09a/)

## TL;DR

- 单二项比例估计量 $\hat{p} = \frac{Y}{n}$ 在大样本条件（$n\hat{p} \ge 10, n(1-\hat{p}) \ge 10$）下，由 CLT 保证渐近服从正态分布 $\mathcal{N}\left(p, \frac{p(1-p)}{n}\right)$。
- 单向分类计数数据的**皮尔逊拟合优度检验（Goodness-of-Fit Test）**度量观测频数与理论期望频数之间的相对偏离度平方和：$\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}$，渐近服从自由度为 $c - 1$ 的卡方分布。
- 二维列联表（Two-Way Contingency Table）检验行变量与列变量的统计独立性；其期望频数基于乘法定理构建为 $E_{ij} = \frac{R_i C_j}{n}$，自由度严格等于 $(r - 1)(c - 1)$。

## 一、单样本二项比例的大样本推断

在市场份额调研、大选民调支持率预测或软件缺陷率统计中，观测数据通常为二元伯努利结果 $X_i \in \{0, 1\}$，发生成功事件的总数为 $Y = \sum_{i=1}^n X_i \sim \operatorname{Bin}(n, p)$。

样本比例估计量定义为：
$$\hat{p} = \frac{Y}{n} = \frac{1}{n}\sum_{i=1}^n X_i$$

### 1. 均值、方差与正态近似条件

- **数学期望：** $E[\hat{p}] = \frac{E[Y]}{n} = \frac{np}{n} = p$（无偏估计）；
- **抽样方差：** $\operatorname{Var}(\hat{p}) = \frac{\operatorname{Var}(Y)}{n^2} = \frac{np(1-p)}{n^2} = \frac{p(1-p)}{n}$。

::: theorem [二项正态近似经验法则]
当满足 $n\hat{p} \ge 10$ 且 $n(1-\hat{p}) \ge 10$ 时，二项分布的偏度被充分抑制，样本比例估计量 $\hat{p}$ 可稳健地近似为高斯正态分布：
$$\hat{p} \sim \mathcal{N}\left(p, \frac{p(1-p)}{n}\right)$$
:::

### 2. 置信区间与 Wald vs 准确区间

在大样本正态近似下，最常用的 **Wald 置信区间**为：
$$\hat{p} \pm z_{\alpha/2} \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$$

::: pitfall [极小概率下的 Wald 区间失效陷阱]
当真实比例 $p$ 接近 0 或 1（例如高精尖制造缺陷率 $p < 0.01$）时，Wald 置信区间可能产生下界小于 0 或覆盖率严重低于名义置信度的荒谬结果。此时必须采用带有连续性修正的 Wilson 得分区间（Score Interval）或 Clopper-Pearson 精确置信区间。
:::

---

## 二、单向分类计数：多项分布与卡方拟合优度检验

当分类变量具有多个互斥类别（例如消费者对 $c$ 种不同口味冰淇淋或不同品牌洗衣粉的市场份额偏好）时，单次试验由伯努利推广至多项分布。

设有 $c$ 个类别，每个类别的真实发生概率为 $p_1, p_2, \dots, p_c$（满足 $\sum p_i = 1$）。抽样 $n$ 个样本，各类别实际观测计数记为 $n_1, n_2, \dots, n_c$（满足 $\sum n_i = n$）。

我们要检验总体各类别发生概率是否符合某个特定的理论基准分布 $\mathbf{p}_0 = (p_{10}, p_{20}, \dots, p_{c0})$：
$$
\begin{cases}
H_0: p_1 = p_{10}, \; p_2 = p_{20}, \; \dots, \; p_c = p_{c0} \\
H_1: \text{至少存在一个 } i \text{ 使得 } p_i \ne p_{i0}
\end{cases}
$$

### 1. 皮尔逊卡方检验统计量的构造

在零假设 $H_0$ 为真的前提下，第 $i$ 类别的**理论期望频数**为：
$$e_i = n p_{i0}$$

皮尔逊（Karl Pearson）构造的卡方拟合优度统计量为：
$$\chi^2 = \sum_{i=1}^c \frac{(n_i - e_i)^2}{e_i} = \sum_{i=1}^c \frac{(\text{Observed}_i - \text{Expected}_i)^2}{\text{Expected}_i}$$

::: theorem [拟合优度卡方分布定理]
当样本量足够大（要求所有单元格期望频数 $e_i \ge 5$）时，统计量 $\chi^2$ 渐近服从自由度为 $\nu = c - 1$ 的卡方分布：
$$\chi^2 \sim \chi^2_{c-1}$$
:::

**自由度为什么是 $c - 1$？**
由于总样本量是预先固定的常数 $\sum_{i=1}^c n_i = n$，前 $c - 1$ 个格子的计数一旦确定，最后一个格子的计数即被完全锁定，因此自由调节的独立维度只有 $c - 1$ 个。

---

## 三、二维列联表：属性关联性与独立性检验

在很多社会科学与商业分析中，我们关心两个属性分类变量之间是否存在某种统计依赖（例如“收入高低”与“员工工作满意度”是否相关）。

数据汇总呈现为一个 $r \times c$ 的**二维列联表（Contingency Table）**：

| 收入水平 \ 满意度 | 非常不满意 | 不满意 | 满意 | 非常满意 | 行边缘合计 $R_i$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **低收入（$<\$6\text{K}$）** | $n_{11}$ | $n_{12}$ | $n_{13}$ | $n_{14}$ | $R_1$ |
| **中低收入（$\$6\text{K}-15\text{K}$）** | $n_{21}$ | $n_{22}$ | $n_{23}$ | $n_{24}$ | $R_2$ |
| **中高收入（$\$15\text{K}-25\text{K}$）** | $n_{31}$ | $n_{32}$ | $n_{33}$ | $n_{34}$ | $R_3$ |
| **高收入（$>\$25\text{K}$）** | $n_{41}$ | $n_{42}$ | $n_{43}$ | $n_{44}$ | $R_4$ |
| **列边缘合计 $C_j$** | $C_1$ | $C_2$ | $C_3$ | $C_4$ | **总样本量 $n$** |

### 1. 独立性零假设下的期望频数推导

检验假设设定为：
$$
\begin{cases}
H_0: \text{行变量与列变量相互独立} \quad (P(A_i \cap B_j) = P(A_i)P(B_j)) \\
H_1: \text{两变量存在某种统计关联}
\end{cases}
$$

在零假设下，事件 $A_i$（属于第 $i$ 行）的边缘概率估计为 $\hat{P}(A_i) = \frac{R_i}{n}$，事件 $B_j$（属于第 $j$ 列）的边缘概率估计为 $\hat{P}(B_j) = \frac{C_j}{n}$。

由独立性乘法法则，落在单元格 $(i, j)$ 的期望概率为：
$$P_{ij} = \hat{P}(A_i)\hat{P}(B_j) = \left(\frac{R_i}{n}\right)\left(\frac{C_j}{n}\right)$$

因此，该单元格的**理论期望频数 $E_{ij}$** 为：
$$E_{ij} = n \cdot P_{ij} = n \cdot \frac{R_i}{n} \cdot \frac{C_j}{n} = \frac{R_i C_j}{n} = \frac{\text{第 } i \text{ 行合计} \times \text{第 } j \text{ 列合计}}{\text{总样本量 } n}$$

### 2. 独立性卡方统计量与自由度推导

双向列联表的检验统计量定义为所有 $r \times c$ 个单元格相对偏差的累加和：
$$\chi^2 = \sum_{i=1}^r \sum_{j=1}^c \frac{(O_{ij} - E_{ij})^2}{E_{ij}}$$

::: theorem [二维列联表自由度定理]
二维列联表独立性卡方统计量渐近服从自由度为 $(r - 1)(c - 1)$ 的卡方分布：
$$\chi^2 \sim \chi^2_{(r-1)(c-1)}$$
:::

**自由度的代数证明：**
整个矩阵共有 $r \times c$ 个独立单元格。但受到行边缘固定与列边缘固定的线性约束：
1. 每行的和必须等于 $R_i$（消耗 $r$ 个约束）；
2. 每列的和必须等于 $C_j$（消耗 $c$ 个约束）；
3. 由于行和之和等于列和之和（$\sum R_i = \sum C_j = n$），两套约束中存在 1 个冗余约束。
因此总约束数量为 $r + c - 1$。有效自由度为：
$$\nu = rc - (r + c - 1) = rc - r - c + 1 = (r - 1)(c - 1)$$

::: insight [卡方检验的宏观辨识力]
列联表卡方检验是一种强有力的无分布假定（Distribution-Free）非参数探索工具。无论定性分类标签是名义型（如职业分类）还是序数型（如满意度等级），它都能敏锐地探测到两个维度之间是否存在打破完全随机均质分配的内在组织结构。
:::
