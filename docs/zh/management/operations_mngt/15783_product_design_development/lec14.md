---
title: 产品开发经济学
type: lecture
lecture: 14
tags: [product-economics, net-present-value, sensitivity-analysis]
status: complete
source: 'https://studylib.net/doc/28287998/syllabuspdd-spring-2026--1-'
---

# Lec 14 产品开发经济学（Product Development Economics）

> 对应Spring 2026 Class 16。原始链接：[课程大纲](https://studylib.net/doc/28287998/syllabuspdd-spring-2026--1-)；核心阅读：[PDD第8版](https://www.mheducation.com/highered/product/Product-Design-and-Development-Ulrich.html)第18章。

## TL;DR

- 产品开发经济学把开发费、资本支出、运营成本、营销支出、价格、销量与上市时间放入同一现金流模型，用现值比较决策。
- 净现值是对一组假设的压缩表达，不是确定答案；销量、价格、单位成本和延误等关键变量必须进行情景与敏感度分析。
- Sprint 5要求团队选择适合产品的组织情景，记录所有财务假设，并找出哪些不确定性最可能改变继续投入的判断。

## 现金流与净现值

把第$t$期净现金流记为$CF_t$，与周期一致的折现率为$r$，则：

$$
NPV=\sum_{t=0}^{T}\frac{CF_t}{(1+r)^t}
$$

模型至少应区分开发支出、设备与工装、单位生产及履约成本、营销支出、销售收入和终值。不同组织情景的成本结构不同，创业公司、成熟制造商与非营利组织不能共用未经说明的假设。

## 敏感度与情景

先建立可审查的基准情景，再逐项改变销量、价格、成本、开发周期和开发费用，观察决策是否翻转。若变量之间存在联动，例如提前上市会提高加急费用和初期报废率，应建立组合情景而非单变量乐观估算。

::: pitfall [把销量当普通输入]
新产品销量通常是模型中最不确定的变量。只给一个精确销量会让NPV的小数位显得比市场证据更可靠。至少应给出低、基准和高情景及其触发条件。
:::

::: insight [模型的价值在于找到临界点]
与其争论哪组预测“正确”，不如求出销量、价格或上市时间达到什么阈值时项目才值得继续，再判断团队能否以用户和运营证据跨过该阈值。
:::

## 课前准备

- 阅读教材第18章“产品开发经济学”。
