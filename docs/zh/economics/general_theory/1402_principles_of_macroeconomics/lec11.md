---
title: IS-LM-PC 综合模型与中期宏观动态
type: lecture
lecture: 11
tags: [is-lm-pc, output-gap, medium-run-equilibrium, monetary-policy-rule]
status: complete
source: 'https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/'
---

# Lec 11 IS-LM-PC 综合模型与中期宏观动态（The IS-LM-PC Model）

> MIT 14.02 · Principles of Macroeconomics · 主讲 Ricardo J. Caballero

## TL;DR

- 将短期 IS-LM 模型与菲利普斯曲线 PC 结合，构建完整的现代 IS-LM-PC 模型。
- 引入产出缺口概念 $(Y - Y_n)$，将通胀变动形式化为产出缺口的直接函数。
- 刻画经济从短期均衡向中期潜在产出调整的动态收敛路径及央行自然利率选择。

## 核心模型与推导

### IS-LM-PC 体系构建

1. **产出与失业率关系（产出缺口）**：
   记潜在产出为 $Y_n$。若当期就业量 $N = Y$（标准化人均产量为 1），劳动力总量为 $L$：
   $$u = 1 - \frac{Y}{L} \implies u - u_n = -\frac{Y - Y_n}{L}$$
   定义产出缺口（Output Gap）为 $(Y - Y_n)$。

2. **菲利普斯曲线（PC 关系）**：
   假定预期锚定在央行通胀目标 $\bar{\pi}$：
   $$\pi - \bar{\pi} = \frac{\alpha}{L}(Y - Y_n)$$
   - 若 $Y > Y_n$（正产出缺口，经济过热），通胀率将高于目标水平（$\pi > \bar{\pi}$）。
   - 若 $Y < Y_n$（负产出缺口，经济衰退），通胀率将低于目标水平（$\pi < \bar{\pi}$）。

3. **IS 关系与自然利率 $r_n$**：
   $$Y = C(Y - T) + I(Y, r + x) + G$$
   - 对应潜在产出 $Y_n$ 的实际借贷利率称为**自然利率（Wicksellian Natural Rate of Interest, $r_n$）**。

### 中期自动调整机制
若当期短期均衡产出 $Y > Y_n$，经济过热引致通胀攀升。央行为了捍卫通胀目标，必然在中期提高政策利率 $r$ 直至 $r = r_n$，产出随之回落至 $Y_n$，通胀平复至 $\bar{\pi}$。

## 经济机制与政策分析

央行进行逆周期调节的本质是寻找并对准不可直接观测的“自然实际利率” $r_n$。如果政策利率长期滞后于自然利率的变动，经济就会在过热恶性通胀或萧条通缩之间剧烈摇摆。

## 适用边界与易错点

混淆实际政策利率 $r$ 与自然利率 $r_n$；误认为中期调整会自动发生而无需央行改变政策姿态。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=QMtbUSfRWBY)
- [MIT 14.02 官方课程主页](https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/)
- [MIT 14.02 官方资源下载页](https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/download/)

::: insight
IS-LM-PC 模型是现代主流宏观教学皇冠上的明珠。它打破了凯恩斯学派与古典学派的人为对立：短期需求决定了产出可以偏离潜在产出；但偏离产生的通胀缺口会倒逼央行调整实际利率，最终在中期引导经济收敛至古典生产函数决定的潜在产出。
:::
