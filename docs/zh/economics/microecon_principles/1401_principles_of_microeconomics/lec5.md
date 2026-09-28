---
title: 生产理论
type: lecture
lecture: 5
tags: [production-function, marginal-product, diminishing-returns, returns-to-scale, isoquant]
status: complete
source: 'https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/resources/mit14_01_f23_lec5/'
---

# Lec 5 生产理论

> MIT 14.01 Principles of Microeconomics · Lecture 5 · Jonathan Gruber

## TL;DR

- 生产函数将资本与劳动等投入要素转换为产出，等产量线刻画要素之间的边际技术替代率（MRTS）。
- 短期内固定资本投入导致边际报酬递减规律必然出现，边际产出（MP）最终低于平均产出（AP）。
- 长期所有要素均可调整，规模报酬（规模递增、递减或不变）决定企业长期扩张的物理边界。

> MIT 14.01 · Principles of Microeconomics · 主讲 Jonathan Gruber

## 3.1.1 生产函数（Production Function）

- 企业的目标是在既定的技术约束下，通过最小化成本来实现利润最大化。
- 生产函数（production functions）描述了企业在技术上可行的生产能力。企业通过生产过程把投入（或称生产要素，factors of production）转化为产出。这里产出（outputs）是企业生产的商品和服务，投入（inputs）是资本（capital）和劳动（labor）。

$$q = f(L, K)$$

其中 $q$ 为产出，$L$ 为劳动，$K$ 为资本。

- 短期（short run）内，至少有一种投入是固定的。长期（long run）内，所有投入都是可变的。

## 3.1.2 短期生产（Short Run Production）

- 回忆短期内至少有一种投入是固定的。假设资本固定、劳动可变。劳动的边际产量（marginal product of labor, $MP_L$）是在其他投入不变的情况下，多使用一单位劳动所带来的总产出的变化。

$$MP_L = \frac{\delta q}{\delta L}$$

一般假设边际产量递减（diminishing marginal products）：并非下一个工人带来的产出增量总是大于前一个工人（原文强调该假设的方向：随着劳动增加，新增工人带来的产出增量递减）。

- 资本的边际产量（marginal product of capital, $MP_K$）是在其他投入不变的情况下，多使用一单位资本所带来的额外产出。

$$MP_K = \frac{\delta q}{\delta K}$$

## 3.1.3 长期生产（Long Run Production）

- 等产量线（isoquants）是显示所有能产出相同数量的 $(L, K)$ 组合的曲线。等产量线的形状由投入之间的可替代程度（degree of substitutability）决定。
- 等产量线的有符号斜率为负；**边际技术替代率**（marginal rate of technical substitution, MRTS）是其绝对值。随着劳动增加，MRTS 通常递减。

$$MRTS = -\left.\frac{dK}{dL}\right|_{q\text{不变}} = \frac{MP_L}{MP_K}$$

## 3.1.4 规模报酬（Returns to Scale）

当按同一比例增加所有投入时，存在三种情形：

- 规模报酬不变（constant returns to scale）：投入按比例增加，产出也按比例增加。例如 $f(2L, 2K) = 2f(L, K)$。
- 规模报酬递增（increasing returns to scale）：投入按比例增加，产出增加的比例超过投入增加的比例。例如 $f(2L, 2K) > 2f(L, K)$。
- 规模报酬递减（decreasing returns to scale）：投入按比例增加，产出增加的比例低于投入增加的比例。例如 $f(2L, 2K) < 2f(L, K)$。

## 视频补充：技术改变生产函数

在[第 5 讲字幕 35:30 附近](subtitles/lec05.srt)，Gruber 用汽车生产解释技术进步：装配线、可互换零件和分工让相同投入在单位时间内生产更多汽车。分析生产函数时，需区分**沿既有生产函数增加投入**与**技术改进使整个生产函数改变**；后者不是单纯的边际产量或规模报酬变化。

::: insight 物理规律对经济产出的引力约束
边际报酬递减规律是经济世界不可逾越的物理重力法则。如果不发生递减，我们就能在花盆里种出养活全人类的粮食。生产函数向我们表明：技术革新虽然能外移等产量线，但如果缺乏资本与组织形态的协同匹配，单纯堆砌单一要素最终必然被沉重的边际报酬递减拖入泥淖。
:::

## 复习要点

**概念理解（Conceptual Understanding）**

- 理解生产函数的投入与产出。
- 分辨短期生产与长期生产的差异。
- 识别规模报酬不变、递增、递减三种不同情形。

**图形与数学理解（Graphical and Math Understanding）**

- 会计算劳动的边际产量、资本的边际产量。
- 会绘制等产量线，理解其斜率即为边际技术替代率；给定生产函数时会计算 MRTS。


## 参考资料与延伸阅读

- [MIT OCW 14.01 官方课程资源主页](https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/)
- Gruber, Jonathan. *Public Finance and Public Policy*. Worth Publishers.
- Varian, Hal R. *Intermediate Microeconomics: A Modern Approach*. W. W. Norton & Company.
