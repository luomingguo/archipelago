---
title: 技术进步与长期平衡增长路径
type: lecture
lecture: 15
tags: [technological-progress, balanced-growth-path, effective-labor, endogenous-growth]
status: complete
source: 'https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/'
---

# Lec 15 技术进步与长期平衡增长路径（Technological Progress and Growth）

> MIT 14.02 · Principles of Macroeconomics · 主讲 Ricardo J. Caballero

## TL;DR

- 引入劳动增进型技术进步（Harrod-Neutral），构建有效劳动模型 $Y = F(K, A N)$。
- 求解平衡增长路径（Balanced Growth Path），证明长期人均产出增长率严格等于技术进步率 $g_A$。
- 探讨研发激励、知识非排他性与内生增长理论的核心机制。

## 核心模型与推导

### 包含技术与人口增长的索洛模型

生产函数为：
$$Y = F(K, AN)$$
其中 $A$ 为技术状态，有效劳动为 $AN$。技术增长率 $\frac{\dot{A}}{A} = g_A$，人口增长率 $\frac{\dot{N}}{N} = g_N$。

定义单位有效劳动的资本与产出：
$$\tilde{k} \equiv \frac{K}{AN}, \quad \tilde{y} \equiv \frac{Y}{AN} = f(\tilde{k})$$

有效劳动的人均资本动态演化方程：
$$\dot{\tilde{k}} = s f(\tilde{k}) - (\delta + g_A + g_N)\tilde{k}$$

### 稳态平衡增长路径（$\dot{\tilde{k}} = 0$）
$$s f(\tilde{k}^*) = (\delta + g_A + g_N)\tilde{k}^*$$

在平衡增长路径上各宏观变量的增长率：
- 单位有效劳动资本 $\tilde{k}^*$ 与产出 $\tilde{y}^*$：增长率 $= 0$。
- 人均资本 $\frac{K}{N} = \tilde{k} A$ 与人均产出 $\frac{Y}{N} = \tilde{y} A$：增长率 $= g_A$。
- 总资本 $K$ 与总产出 $Y$：增长率 $= g_A + g_N$。

## 经济机制与政策分析

要想在长期维持生活水平的阶梯式跃升，公共政策的重心必须转向基础研究资助、专利知识产权保护以及竞争性创新生态的培育。任何无法转化为技术生产率红利的增长尝试，最终都会被折旧消耗殆尽。

## 适用边界与易错点

混淆单位劳动产出 $Y/N$ 与单位有效劳动产出 $Y/(AN)$；误认为人口增长能提高人均收入水平。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=nNqnivVl8WI)
- [MIT 14.02 官方课程主页](https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/)
- [MIT 14.02 官方资源下载页](https://ocw.mit.edu/courses/14-02-principles-of-macroeconomics-spring-2023/download/)

::: insight
只有技术进步，才能战胜资本边际报酬递减的物理铁律。在平衡增长路径上，资本存量与总产出以相同的速率奔腾向前，使得资本-产出比保持常数。经济增长的本质是新点子、新算法与新工艺对有限物质要素的不断重新编排。
:::
