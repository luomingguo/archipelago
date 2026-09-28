---
title: 'SQL 进阶——条件、分组、排序与多表连接'
type: lecture
lecture: 4
tags: [sql-joins, aggregate-functions, group-by, query-filtering]
status: complete
source: 'https://mitxonline.mit.edu/courses/course-v1:MITxT+CTL.SC4x/'
---

# Lec 4 SQL 进阶——条件、分组、排序与多表连接（Database Conditional, Grouping, and Joins）

> 对应 MIT CTL.SC4x · Supply Chain Technology and Systems · 第 4 讲  
> 核心参考：*SC4x Key Concept Document* (Summer 2019) & MITx MicroMasters SCM 课程大纲

## TL;DR

- 进阶 SQL 通过 WHERE 条件表达式、ORDER BY 排序与 LIMIT 分页实现精准数据截取。
- 聚合函数（SUM、AVG、COUNT）结合 GROUP BY 与 HAVING 实现多维度指标汇总与后验过滤。
- 内连接（INNER JOIN）与左连接（LEFT JOIN）满足跨供应商、订单与物料表的复杂全景关联。

::: insight 统计缺货率时的连接语义陷阱
在分析供应商履约表现时，新手分析师往往直接使用 `INNER JOIN` 将订单表与发货表关联。但这样会直接过滤掉“从未发货”的完全违约订单，导致计算出的供应商准时交付率（OTIF）被严重虚高美化。正确的做法是始终以全量订单表为基准使用 `LEFT JOIN`，并通过 `WHERE shipment_id IS NULL` 精准捕获违约记录。
:::

## 1. 本讲的定位

Lec3 学会了最基础的 `SELECT ... FROM`。真正处理供应链规模的数据时，还需要：**精确筛选记录**、**按组做统计**、**排序与抽样**、以及**把多张表拼接起来**——这些都是"大数据"能被有效利用的关键操作。

## 2. 条件子句（Conditional Clauses）

条件子句是查询中用来"按条件筛选返回哪些行"的部分。除了基础的 `WHERE`，还有两个常用增强写法：

### 2.1 `WHERE ... IN`

用于筛选某属性取值**属于一组指定值**中任意一个的记录：

```sql
SELECT *
FROM Offices
WHERE State IN ('CO', 'UT', 'TX');
```

等价于：

```sql
SELECT *
FROM Offices
WHERE State = 'CO' OR State = 'UT' OR State = 'TX';
```

### 2.2 `BETWEEN`

用于筛选某属性取值落在两个数值**之间（含端点，闭区间）**的记录，同样适用于日期/时间型数据。

## 3. NULL 值

NULL 是一个特殊占位符，代表"未知"或"不适用"的值——当某值为空/缺失时，就以 NULL 存储。几个必须牢记的坑：

- **NULL 在任何比较运算中都不会评估为 TRUE**（既不是等于，也不是不等于，是"未知"）；
- 判断 NULL 要用 `IS NULL` / `IS NOT NULL`，**不能用 `= NULL`**；
- 当某个属性可能包含 NULL 或缺失值时，在写条件子句时需要**格外小心**，否则容易漏掉或误判记录。

## 4. 分组与统计函数（Grouping & Statistical Functions）

熟悉基础查询后，可以进一步使用 SQL 内置的统计函数，**对一组记录做聚合运算**。

- `GROUP BY`：把记录按某属性分组，**每组返回一个值**；
- `HAVING`：对 `GROUP BY` 之后的分组结果做进一步筛选（作用类似 `WHERE`，但作用对象是分组结果而非原始行）。

**常用聚合统计函数**：`COUNT`、`SUM`、`AVG`、`MIN`、`MAX` 等（教材 Table 1 汇总的常用 SQL 函数）。更进阶的统计量（如加权平均、z-score）可以通过组合这些基础函数自行搭建。

## 5. 排序与抽样（Sorting & Sampling）

| 子句/函数 | 作用 |
|---|---|
| `ORDER BY` | 指定查询结果按升序（`ASC`）或降序（`DESC`）返回 |
| `LIMIT` | 限制返回的记录数量，便于抽查或提升效率 |
| `RAND()` | 生成随机值，用于随机抽样或随机排序结果 |

**随机排序整表**：
```sql
SELECT * FROM table ORDER BY RAND();
```

**随机抽取一条记录**：
```sql
SELECT * FROM table ORDER BY RAND() LIMIT 1;
```

**在输出中生成一个随机数**：
```sql
SELECT id, RAND() FROM table;
```

## 6. 创建新表与别名

- **`AS`（别名）**：为查询返回的某个属性或函数结果创建一个别名；
- **`CREATE TABLE ... AS`**：用一条 `SELECT` 查询的结果，在数据库中创建一张新表——新表的列和数据类型会依据 SELECT 结果自动匹配：

```sql
CREATE TABLE new_table
AS (SELECT column_name(s)
    FROM old_table);
```

- **`SELECT ... INTO`**：如果目标表结构已经存在，可以把查询结果直接插入这张**已存在**的表（或外部数据库）：

```sql
SELECT column_name(s)
INTO newtable [IN externaldb]
FROM table1;
```

> 二者的区别：`CREATE TABLE AS` 是"新建表 + 填数据"一步完成；`SELECT INTO` 要求目标表已经存在，只是把数据插进去。

## 7. 多表连接（Joining Multiple Tables）

关系数据库模型的威力就在于：可以**连接多张表**，构建出原本没有预料到的新关系——比如把自己的表和外部数据源（如某邮编对应的人口统计信息、某承运商的运费分区结构）结合起来分析。

**JOIN 的基本要求**：
- 参与连接的列**不需要**一定是键，但**通常是键**（主键或外键）；
- 连接列的**数据类型必须兼容**；
- **NULL 永远无法与任何值连接匹配成功**。

### 7.1 JOIN 的类型

| JOIN 类型 | 行为 |
|---|---|
| `INNER JOIN` | 只返回两表中**键匹配**的记录（连接公共列取值相同的行） |
| `LEFT JOIN` | 返回**左表（第一张表）全部行**，无论是否在右表中找到匹配 |
| `RIGHT JOIN` | 返回**右表（第二张表）全部行**，无论是否在左表中找到匹配 |
| `OUTER JOIN` | 返回**两表所有行**，无论是否匹配（这是 Microsoft SQL 的写法，**MySQL 中没有**） |

> 在 MySQL 中，`JOIN` 与 `INNER JOIN` 是等价的。

三表连接（Join from 3 Tables）本质上只是"在已经连接好的两表结果"上，再与第三张表做一次额外的 JOIN。

### 7.2 视图（Views）

视图是**虚拟表**——它不会改变底层数据，但能简化复杂查询、便于生成报表。特点：
- 以"非规范化（denormalized）"的形式向用户呈现数据；
- **不会**创建数据的独立副本，而是**引用**底层表中的数据；
- 数据库只存储视图的**定义**，每次调用视图时数据都会重新取算。

**使用视图的三个好处**：
1. 面向用户的查询更简单（复杂逻辑封装在视图定义里）；
2. 提供一层**安全边界**，可以限制用户对视图中数据的访问范围；
3. 提供更好的**独立性**——底层表结构的小改动不会影响使用视图的用户或程序。

## 8. 本讲小结与学习目标回顾

- 学会用 `SELECT` 搭配条件子句做筛选；
- 认识 NULL 值的特殊角色和处理方式；
- 复习用 `GROUP BY` 对数据分组；
- 了解 SQL 中普遍存在统计函数，并学会应用聚合统计函数；
- 复习排序与抽样技巧：`ORDER BY`、`LIMIT`、`RAND`；
- 学会用 `AS` 关键字创建新表和别名；
- 熟悉多表连接（JOIN）的基本操作；
- 认识各类 JOIN（INNER / LEFT / RIGHT / OUTER）的区别；
- 认识何时以及如何使用视图（VIEW）。

**下一讲（Lec 5）**：SQL 用熟练之后，回到更宏观的数据库工程话题——**索引与性能、OLTP vs OLAP、NoSQL、云计算与数据清洗**。
