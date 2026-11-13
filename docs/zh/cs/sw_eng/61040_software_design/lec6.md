---
title: 设计概念状态 · 软件设计
type: lecture
lecture: 6
tags: [state-modeling, concept-specification, data-modeling, invariants]
status: complete
source: 'https://61040.github.io/fa26/lectures/designing-state.pdf'
---
# Lec 6 设计概念状态（Designing Concept State）

官方课件：[Designing State](https://61040.github.io/fa26/lectures/designing-state.pdf)。本讲探讨概念设计中最核心的抽象基础：如何使用**简明状态形式**（*Simple State Form, SSF*）精准声明概念内部状态，建立清晰的集合、映射与不变量约束。

## TL;DR

- 概念的内部状态是其兑现承诺所必须记住的最小事实集合，禁止为了迎合 UI 控件或特定数据库结构随意膨胀。
- Simple State Form (SSF) 将状态严格定义为“实体集合（*Sets of Individuals*）”与“关系映射（*Relations*）”，具备一阶逻辑清晰度与跨存储引擎可迁移性。
- 实体值仅由其身份（*Identity*）决定而非复合对象；可选字段通过空集合表达，非空与唯一性通过修饰符及组合约束强制约束。
- 良好的状态声明天然内嵌不变量（*Invariants*），能在规格层杜绝数据孤岛、状态冗余与未声明的副作用。

## 为什么需要对状态形式化建模？

在传统软件工程中，工程师常常混淆了“**业务行为所需的事实**”与“**数据库表的物理结构**”。把所有字段揉杂在单一对象中，或者直接按照前端界面控件存储状态，会导致概念边界模糊、数据不一致以及隐式依赖。

::: definition 简明状态形式（Simple State Form, SSF）
SSF 是一种面向概念规格的数据建模语法，既能被人直观理解，又能无歧义地转换为 MongoDB Schema、SQL 关系表、Alloy 形式化规约或 TypeScript 类声明。
:::

SSF 具有以下核心语义特征：
1. **实体集合（Sets of Individuals）**：声明概念所管理的基本实体类型（如 `User`、`Post`、`Session`）。
2. **关系映射（Relations）**：声明实体映射到其他实体或基本标量类型（`String`、`Number`、`Date`、`Flag`）的二元关系。
3. **子集分类（Subsets）**：在不破坏主集的前提下声明实体的状态子集（如 `PendingOrders` 是 `Orders` 的子集）。
4. **组合约束（Unique Constraints）**：声明跨字段联合唯一性，例如 `unique item and voter` 防止重复投票。

## SSF 核心语法规范

```ssf
concept Upvoting [Item]
state
  a set of Voters with
    unique voterId String
  a set of Votes with
    a voter Voter
    an item Item
    unique voter and item
```

### 标量与集合字段的修饰规则

- **必选标量**：默认每个映射必须存在且唯一（例如 `a voter Voter`）。
- **可选标量**：使用 `optional` 修饰，表示可映射为空（例如 `an optional nickname String`）。
- **多值映射**：使用 `set of` 或 `seq of`（有序序列）。集合映射**禁止**使用 `optional`，无对应项时统一表示为空集 $\emptyset$。
- **唯一性约束**：使用 `unique` 修饰字段或声明 `unique field1 and field2` 复合约束。

## 状态建模的常见陷阱

1. **混入 UI 临时状态**：如将 `isHovered`、`currentPage` 声明进概念状态。概念只记录业务事实，视图状态由前端组件独立持有。
2. **状态冗余与双向记录**：同时记录 `user.posts` 和 `post.author`，导致同步困难。SSF 建议仅声明单向基础映射，反向通过查询（query）推导。
3. **暴露内部复合对象**：将复杂的 JSON 嵌套对象作为字段类型，破坏了表示独立性。对象应平铺拆解为具名实体与关系。

::: insight
状态建模的关键不是“如何存储”，而是“系统为了向用户兑现承诺，在时空跨度上必须记住的最少事实是什么”。若某字段可由已有状态通过纯函数推导得出，它就不应进入概念的状态空间；状态空间越精炼，不变量的验证成本就越低，因果同步就越可靠。
:::
