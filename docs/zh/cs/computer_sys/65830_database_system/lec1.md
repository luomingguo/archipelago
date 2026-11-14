---
title: '关系模型与 SQL 基础'
type: lecture
lecture: 1
tags: [relational-model, relational-algebra, sql-basics, declarative-query]
status: complete
source: 'https://dsg.csail.mit.edu/6.5830/'
---

# Lec 1 关系模型与 SQL 基础

## TL;DR

- 数据库管理系统（DBMS）的核心价值在于确立物理与逻辑数据独立性，将应用开发者从底层存储组织与手工指针导航中彻底解放。
- 层次模型（IMS）与网状模型（CODASYL）因强制暴露物理指针遍历、缺乏数据独立性并导致海量数据冗余而走向黄昏。
- Edgar F. Codd 提出的关系模型基于数学集合论与一阶谓词逻辑，将数据抽象为二维关系表与元组无序集合。
- 声明式 SQL 配合关系代数等价重写（谓词下推、投影修剪）与成本优化器（CBO），使得内核能够在毫秒级内搜索并生成最优物理执行计划。
---

## 架构演进与核心洞察

::: insight 为什么关系模型最终一统天下？
在关系模型诞生之前，计算机厂商普遍认为“由数学公式描述的无序表格不可能达到手写指针遍历的极致性能”。Codd 的天才构想在于：**将性能优化的沉重包袱从应用开发者身上卸下，交给底层的通用查询优化器**。程序员只需关注“我要什么（What）”，而底层的优化器能根据全局统计信息，动态挑选出远超普通程序员想象的最优执行路径！
:::

## 课前阅读与文献研读 (Reading Assignment)

> 本讲奠定数据库管理系统的核心基石。课前推荐研读 Stonebraker 与 Hellerstein 梳理半个世纪数据模型兴衰演进的经典之作，理解物理数据独立性与声明式查询对计算机科学的深远影响。  
> 📖 **文献研读入口**：[推荐文献研读：What Goes Around Comes Around（数据模型半个世纪的技术轮回）](./paper/what_goes_around_comes_around.md)

## 核心机制与讲义正文

> [!TIP] **[待补截图]** 建议截取官方课件 Slides 第 1 讲中的“数据独立性（物理数据独立性 vs 逻辑数据独立性）分层架构示意图”。此处预留插图空间。

## 课程开场与技术演进全景

在计算机科学领域，各种应用框架和前端技术层出不穷，但数据库内核所沉淀的核心技术——**数据建模、声明式查询、成本优化、ACID 事务与大规模分布式一致性**，历经半个世纪的风雨洗礼依然历久弥新。

```text
+---------------------------------------------------------------------------------+
|                       数据管理系统半个世纪的演进技术图谱                        |
|                                                                                 |
|   1960s         1970s-80s          2000s            2015-2025         2025+     |
|   [大型机]     [早起服务器]      [商用集群]         [公有云]        [AI/GPU集群] |
|                                                                                 |
|   IBM IMS     System R / Ingres   NoSQL 系统      云原生数据仓库     AI/向量引擎 |
|   层次网状     关系模型/SQL/ACID   KV/文档存储     存算分离/Snowflake 语义算子/RAG|
|                                                                                 |
|   【底层恒定不变的技术基石】：                                                  |
|   数据独立性 -> 关系代数推导 -> 代价模型优化 -> 并发与故障恢复 (WAL/ARIES)      |
+---------------------------------------------------------------------------------+
```

## 什么是数据库系统？

数据库（*Database*）是有组织、有结构的数据记录与实体关系的集合。而**数据库管理系统（*DBMS: Database Management System*）**则是负责管理、持久化、索引并提供高效声明式检索的底层软件系统。

在实际工业级系统中，如果只依赖普通文件系统（如将数据写成 CSV 或 JSON 文件存在磁盘上）：

1. **多用户并发冲突**：多个写进程同时追加文件，极易破坏文件元数据导致数据损坏；
2. **读写性能低下**：为了找到特定用户的一笔订单，必须对百 GB 的文件进行全量线性扫描；
3. **系统崩溃时的一致性毁灭**：若写入到一半时服务器发生断电宕机，文件处于半写入状态，毫无原子性回滚机制。

DBMS 就是为了从根本上解决这些系统级难题而诞生的基石软件。

![数据库产品大览](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66954d3007cb8.png)

## 层次模型与网状模型

在关系数据库统治世界之前，业界先后经历了**层次模型（*Hierarchical Model*）**与**网状模型（*Network Model*）**。理解它们的致命痛点，是深刻领悟关系模型伟大之处的前提。

### 层次模型

层次模型将数据组织为树状分层结构（Segment Tree）。以动物园管理系统（Zoo）为例：包含饲养员（Keepers）、笼子（Cages）和动物（Animals）。

```text
+--------------------------------------------------------------+
|               层次模型 (IMS) 的树状数据组织与数据冗余        |
|                                                              |
|                     [ 饲养员: Jane ]                         |
|                       /          \                           |
|           [ 动物: Mike, 驼鹿 ]     [ 动物: Tianyu, 长颈鹿 ]  |
|                 |                          |                 |
|           [ 笼子: 1 号笼 ]           [ 笼子: 2 号笼 ]        |
|                                                              |
|   【致命缺陷】：                                             |
|   若一只动物由多个饲养员照料，或多个动物共享同一个笼子：     |
|   -> 笼子数据必须在树的多个分支下重复存储（数据冗余）！      |
|   -> 一旦笼子清洁时间变动，必须遍历整棵树修改，极易导致不一致|
+--------------------------------------------------------------+
```

#### IMS 的低级物理编程接口（DL/1）

程序员必须编写复杂的低阶过程代码，沿着物理指针在树中“攀爬”：

```text
// 查询饲养员 Jane 所负责的所有笼子
GetUnique(Keepers, name = "Jane")
Until done:
    cageid = GetNextParent(cages).no
    print cageid
```

层次模型的致命缺陷
1. **非层次关系的无法表达与数据冗余**：真实世界充斥着多对多（N:M）关系，强制用树表达必然造成海量冗余拷贝；
2. **极其脆弱的物理数据独立性（Physical Data Independence）**：如果 DBA 将根节点的物理存储从有序数组改为哈希索引，原先依赖 `GetNext` 顺序扫描的所有上层应用程序当场崩溃；
3. **缺乏逻辑数据独立性（Logical Data Independence）**：如果业务调整让饲养员直接管理笼子而非动物，树的上下层结构颠倒，原有的遍历代码必须全量报废重写！

### 网状模型（CODASYL，1970年代）

为了解决层次模型无法表达多对多关系的缺陷，CODASYL 联盟提出了网状图模型。数据记录之间通过物理指针连成复杂的网状结构。

```text
+--------------------------------------------------------------+
|                 CODASYL 网状模型的“导航式编程”               |
|                                                              |
|      [饲养员: Joe] ----caredforby----> [动物: Mike]          |
|            |                                |                |
|         livesin                          livesin             |
|            v                                v                |
|      [ 1 号笼子 ] <-------------------- [ 2 号笼子 ]         |
|                                                              |
|   【开发体验】：                                             |
|   程序员如同在迷宫中穿行，必须在内存中维护当前位置指针（Cursor)|
|   一步步跟踪指针跳跃，被称为“导航式编程（Navigational）”     |
+--------------------------------------------------------------+
```

在网状模型中，写代码就像在物理图结构中走迷宫。程序与底层的物理指针、哈希表实现严重耦合，系统的维护成本高得令人绝望。

---

## 3. Codd 关系模型的革命：数据独立性与数学抽象

1970 年，IBM 圣何塞实验室的数学家 **Edgar F. Codd** 发表了改变计算机历史的开创性论文《*A Relational Model of Data for Large Shared Data Banks*》，图灵奖传奇就此启幕。

```text
+--------------------------------------------------------------+
|                      关系模型的核心抽象                      |
|                                                              |
|   1. 统一表格抽象：所有数据均表示为二维表 (Relation / Table) |
|   2. 无序元组集合：表是元组（Tuples / Rows）的无序数学集合   |
|   3. 标量原子属性：每个字段（Field / Attribute）必须是原子标量|
|   4. 物理细节隐藏：完全隐藏索引类型、物理排序与指针跳转细节！|
+--------------------------------------------------------------+
```

```text
Animals 关系表 (Relation):
+----+--------+-----+---------+--------+
| id | name   | age | species | cageno |
+----+--------+-----+---------+--------+
| 1  | Mike   | 3   | Moose   | 1      |
| 2  | Tianyu | 12  | Giraffe | 1      |
| 3  | Sally  | 1   | Student | 2      |
+----+--------+-----+---------+--------+
```

::: definition 物理数据独立性 vs 逻辑数据独立性

- **物理数据独立性（Physical Data Independence）**：逻辑数据模型与底层物理存储（B+ 树、哈希表、页大小、行存/列存）完全隔离。无论 DBA 在后台如何创建索引或重组文件，上层查询逻辑与应用程序代码均无需做任何改动。
- **逻辑数据独立性（Logical Data Independence）**：应用程序与全局逻辑模式（Schema）解耦。通过视图（View）与模式重构，即便数据库增加了新字段或对表进行了范式拆分，上层业务程序依然能够透明运行。
  :::

::: insight 为什么关系模型最终一统天下？
在关系模型诞生之前，计算机厂商普遍认为“由数学公式描述的无序表格不可能达到手写指针遍历的极致性能”。Codd 的天才构想在于：**将性能优化的沉重包袱从应用开发者身上卸下，交给底层的通用查询优化器**。程序员只需关注“我要什么（What）”，而底层的优化器能根据全局统计信息，动态挑选出远超普通程序员想象的最优执行路径！
:::

## 4. 关系代数：查询优化的数学理论基石

关系代数（Relational Algebra）是一门由元组集合操作构成的过程化形式语言。它的核心特性是**封闭性（Closure Property）**：**每一个关系代数表达式的输入是关系，输出也必然是一个全新的关系！**

### 4.1 六大核心基本算子

```text
+-----------------------------------------------------------------------------+
|                            关系代数六大基本算子                             |
|                                                                             |
|   算子名称          数学记号                 代数语义                       |
|  +---------------+------------------------+-------------------------------+ |
|  | 选择 (Select) | $\sigma_{pred}(R)$     | 筛选出满足谓词 $pred$ 的元组子集|
|  | 投影 (Project)| $\pi_{A_1,..,A_k}(R)$  | 提取指定列属性，剔除其余字段并去重|
|  | 笛卡尔积       | $R \times S$           | 两表所有元组的两两组合全积     |
|  | 集合并 (Union) | $R \cup S$             | 两张同构关系的并集            |
|  | 集合差 (Diff)  | $R - S$                | 属于 $R$ 但不属于 $S$ 的元组   |
|  | 重命名 (Rename)| $\rho_{S}(R)$          | 赋予关系或属性全新的别名       |
|  +---------------+------------------------+-------------------------------+ |
+-----------------------------------------------------------------------------+
```

### 4.2 导出算子：自然连接与条件连接

在日常查询中最关键的**连接算子（Join: $\bowtie$）**，本质上是笛卡尔积与选择算子的复合推导：

$$\ R \bowtie_{R.cageno = S.cageid} S = \sigma_{R.cageno = S.cageid}(R \times S) \$$

```text
Animals (A)                        Cages (C)
+--------+--------+                +--------+----------+
| name   | cageno |                | cageid | bldg     |
+--------+--------+                +--------+----------+
| Mike   | 1      |                | 1      | 32       |
| Sally  | 2      |                | 2      | 34       |
+--------+--------+                +--------+----------+

笛卡尔积 (A x C):
[Mike, 1, 1, 32] -> 符合条件!
[Mike, 1, 2, 34] -> 不符合，丢弃
[Sally, 2, 1, 32]-> 不符合，丢弃
[Sally, 2, 2, 34]-> 符合条件!

最终 Join 结果:
+-------+--------+--------+------+
| name  | cageno | cageid | bldg |
+-------+--------+--------+------+
| Mike  | 1      | 1      | 32   |
| Sally | 2      | 2      | 34   |
+-------+--------+--------+------+
```

---

## 5. 声明式查询语言：从过程化遍历到 SQL 表达式

### 5.1 过程化命令 vs 声明式表达

对比以下两种寻找“32 号建筑中所有动物名称”的编写方式：

#### 过程化伪代码（Imperative / Procedural）：

```python
# 程序员必须显式指定双重嵌套循环与遍历顺序
results = []
for a in animals:
    for c in cages:
        if a.cageno == c.no and c.bldg == 32:
            results.append(a.name)
return results
```

**致命隐患**：如果 `animals` 有 1000 万行，而 `cages` 只有 10 行，上面的外层循环会极其低下！程序员一旦写错循环顺序，整个系统就会发生数十倍的性能劣化。

#### 声明式 SQL（Declarative）：

```sql
SELECT a.name 
FROM animals AS a, cages AS c
WHERE a.cageno = c.no AND c.bldg == 32;
```

**声明式魅力**：开发者只声明需要什么数据，绝不指定任何循环、排序或索引使用方式！

---

## 6. 查询编译流水线：从 SQL 到优化执行计划

当数据库内核接收到一条 SQL 语句时，它究竟是如何将文本转化为高效的底层执行机器指令的？

```text
+--------------------------------------------------------------+
|                    DBMS 内核查询执行全流水线                 |
|                                                              |
|   声明式 SQL 查询文本                                        |
|        |                                                     |
|        v                                                     |
|   [词法/语法解析器 (Parser)]                                 |
|        |                                                     |
|        v                                                     |
|   抽象语法树 (AST) & 逻辑算子树 (Logical Plan)               |
|        |                                                     |
|        v                                                     |
|   [关系代数重写与等价变换 (Optimizer: 规则优化 RBO)]          |
|   - 谓词下推 (Predicate Pushdown)                            |
|   - 投影尽早修剪 (Projection Pruning)                        |
|        |                                                     |
|        v                                                     |
|   [基于代价的连接定序 (Cost-based Optimizer: CBO)]           |
|   - 评估索引扫描 vs 全表扫描                                 |
|   - 选择物理连接算法 (Hash Join / Merge Join / Index Scan)   |
|        |                                                     |
|        v                                                     |
|   物理执行计划 (Physical Plan / Compiled Operators)          |
|        |                                                     |
|        v                                                     |
|   [火山模型执行引擎 (Volcano Iterator / Vectorized Engine)]  |
+--------------------------------------------------------------+
```

### 6.1 经典优化实战：谓词下推（Predicate Pushdown）

考虑前述查询的两种等价关系代数树：

```text
      [未经优化的初始计划]                       [谓词下推后的优化计划]
             Project (name)                             Project (name)
                  |                                          |
             Filter (bldg=32)                           Join (cageno=no)
                  |                                         /         \
            Join (cageno=no)                         Animals      Filter (bldg=32)
               /        \                                              |
           Animals     Cages                                         Cages

【未优化代价】：                              【优化后代价】：
两表先做全量笛卡尔积，产生 1000万 x 1000 =    先在 Cages 表上执行 Filter (bldg=32)，
100 亿条临时数据，再做过滤！内存爆仓崩溃！    数据量从 1000 瞬间压缩至 2 条！
                                              随后仅需对这 2 条记录做极速索引点查！
```

通过简单的关系代数等价代换：

$$\ \sigma_{c.bldg=32}(A \bowtie C) \equiv A \bowtie (\sigma_{c.bldg=32}(C)) \$$

数据库优化器在毫秒内将运算规模压缩了数千倍，这就是声明式查询与优化器的强大威力！

## SQL 必要练习 + 论文阅读

1、 [完成 SQL 的练习]([1. SQL — A Practical Introduction to Databases (runestone.academy)](https://runestone.academy/ns/books/published/practical_db/PART1_SQL/index.html))

2、 [完成关系模型（3.1 节）的练习]([3. RELATIONAL DATABASE THEORY — A Practical Introduction to Databases (runestone.academy)](https://runestone.academy/ns/books/published/practical_db/PART3_RELATIONAL_DATABASE_THEORY/index.html))

3、 阅读参考书上的 Michael Stonebraker 和 Joseph Hellerstein 的文章《What Goes Around Comes Around》中的第 1 至 4 节

4、（可选）关系模型的开山鼻祖论文； E.F. Codd. A relational model of data for large shared data banks. Communications of the ACM, 1970.[[PDF](http://portal.acm.org/ft_gateway.cfm?id=362685&type=pdf&coll=GUIDE&dl=GUIDE&CFID=1781172&CFTOKEN=98614393)].

回答以下问题：

- 哪些类型的程序在 SQL 中编写起来容易？哪些类型的程序较难？
- 您觉得声明式编程比命令式编程更容易还是更难？
- 什么是数据独立性的概念？为什么它很重要？
- 关系模型背后的关键思想是什么？它们为何优于之前的模型？关系模型在哪些方面具有限制性？
- “分层”模型（如 IMS 系统）与 Codd 提出的关系模型之间最重要的区别是什么？

---

## 详细机制推导与原版课堂图解

> MIT 6.5830 / 6.5831 · Database Systems · 第 1 讲  
> 核心教材：*Readings in Database Systems* (5th Edition, Red Book)  
> 配套实验：GoDB (Go-based Database Engine)

## 基本概念

### 什么是数据库？

- 结构化数据的集合
  - 一般被组织成“记录”,  一般在磁盘上，数据量非常大
  - 以及记录之间的关系

- 这门课里面提到的数据库是指： DBMS。
  - 用来存储和查询数据库的软件系统。

### 数据库分类

![截屏 2024-02-06 04.38.50](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66954d3007cb8.png)

**数据模型（data model） & 布局（layout）**

- 在数据库中构造和表示数据的系统方法
- 对数据一致性、共享数据、以及高效访问持久化数据非常重要
- 数据模型举例
  - 关系型 （大部分 DBMS 采用）
  - 非关系型
    - K/V
    - 文档/XML/对象
    - Wide-Column/Column-Family

  - Array/Matrix/Vectors (机器学习)
  - 过时
    - 分层
    - 网络
    - 多值

**Schema**

是指给定一个数据模型，对该数据集合（实体）的一种描述

**声明式查询**

- 数据库查询过程（query processing）
- 访问和操纵数据的算法

**一致性/事务（"ACID"）**

**关系模型术语与日常生活术语对比**

![截屏 2024-02-21 11.52.43](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/65d573948db93.png)

## 案例：动物园网站

### 特性

- 管理员接口
  - 编辑
  - 添加动物
- 公共设施
  - 图片 & 地图
- 动物饲养员
  - 喂养时间
- 1K 个动物，5K 个 URL， 10 个管理员，200 个动物饲养员

### 动物园数据模型

#### 实体关系图

![截屏 2024-02-06 04.49.39](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/669573f45e804.png)

- 动物实体： 1 名字、1 年龄、1 品种
- 饲养员实体： 1 名字
- 笼子实体： 1 清理时间、1 建筑标号
- 一个笼子实体**包含**多个动物实体
- 一个动物饲养员看管多个笼子，一个笼子被多个饲养员看管

> 有其他比表集合更好的方式表示动物园数据吗？
>
>  不同的表示方法之间的权衡点在哪里？

#### 分层表示法

cage 1
	Tim
		giraffe
		13 yrs
	Sally
		student
		1 yr

cage 2
	Sam
		salamander
		3 yrs

#### 图表示法

```mermaid
graph TD
    A[animals] --> B[Tim]
    A[animals] --> C[Sally]
    A[animals] --> D[Sam]
    B[Tim] --> E[cage1]
    C[Sally] --> E[cage1]
    D[Sam] --> F[cage2]
    

```

####  扁平表示法

| name  | age  | species    | cageno | feedtime | bldg |
| ----- | ---- | ---------- | ------ | -------- | ---- |
| Tim   | 13   | giraffe    | 1      | 1:30     | 1    |
| Sam   | 3    | salamander | 2      | 2:30     | 2    |
| Sally | 1    | student    | 1      | 1:30     | 1    |

> 这是一个好的表示方法吗？ 为什么？

扁平化表示方法没有”规范化“（normalized)——数据重复了

### SQL

SQL，Structured Query Language，结构化查询语言

**查询长颈鹿的名称**

- 命令式

  ```python
  for each row r in animals:
    if r.species = 'giraffe':
      print(r.name)
  ```

- 声明式

  ```sql
  SELECT r.name FROM animals WHERE r.species = 'giraffe';
  ```

**查询 32 号建筑的笼子**

- 命令式

  ```python
  for each row a in animals:
    for each row c in cages:
      if a.cageno == c.no and c.bldg = 32:
      	print(a)
  ```

- 声明式

  ```sql
  SELECT a.name FROM animals AS a, cages AS c WHERE a.cageno = c.no AND c.bldg = 32
  ```

可以看出命令式用了嵌套循环，而声明式是用连接的方式。

**复杂的查询**

![截屏 2024-07-16 03.35.51](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66957a1e2b6de.png)

从上述例子中，我们得出结论，声明式查询**关注做什么，而不是怎么做**

- 对于给定的 SQL，有很多可能的程序计划
- 除了遍历所有记录，我们还能做些什么？
  - 按照动物类型进行排序
    - 这种排序方法对于特定类型（例如 "bears"）的查询非常有效，可以快速定位目标数据
    - 即插入操作会变慢，因为每次插入新记录时都需要保持排序顺序
  - 将动物表存储到哈希表中，或者树结构(“索引”）

#### SQL 执行过程

```mermaid
graph TD;
    SQL["SQL"] --> ProceduralPlan["Procedural Plan程序计划"];
    ProceduralPlan --> OptimizedPlan["Optimized Plan优化计划"];
    OptimizedPlan --> CompiledProgram["Compiled Program编译程序"];
```

逻辑独立

- 如果我们想要更改 schem 而不更改代码呢？
- 如果我们只是添加一列或者一个表
- 视图允许我们将一个旧的 schema 映射到新的

视图

- 视图是一个将一个表表示其他表的逻辑定义
- 例子: 一个计算每个笼子的动物视图

```sql
CREATE VIEW cage_count as (SELECT cageno, count(*) FROM animal JOIN cages ON cageno=no GROUP by cageno)
```

- 例子： 如果我想添加多个喂养时间。
  - Rename existing animals table to animals2
  - Create feedtimes table
  - Copy feedtime data from animals
  - Remove feedtime column from animals
  - Create a view called animals that is a query over animals and feedtimes

```sql
CREATE VIEW animals as(
SELECT name, age, species,cageno,
	(SELECT feedtime FROM feedtimes WHERE animalid = id LIMIT 1) FROM animals
)
```

## 数据模型发展历史

### 不同的数据模型

- 分层数据模型（IMS/DL1)， 20 世纪 60 年代
- 网络数据模型（CODASYL)， 20 世纪 70 年代
- 关系数据模型， 20 世纪 70 年代

### 主要观点

- 数据冗余（如何避免）
- 物理和逻辑数据独立
- 关系代数和公理

**案例： 动物园网站**

![截屏 2024-07-16 04.04.25](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/669580cf1abef.png)

schema： 属性名称和属性类型

行，也称记录，或者元祖

----

对动物数据模型进行小更改

- 每个动物都在一个笼子里，多个动物可能共享一个笼子
- 每个动物被 1 个饲养员照顾，饲养员需要照看多个动物

### IMS（分层模型）

- 数据被组织称段 segment

  - 段是记录的集合，每个段都有相同的段类型。段类型定义了记录的结构

  - IMS 中的数据按段类型排列成树状结构，例如

    ```text
    Keepers
    	Animals
    		Cages
    
    or
    
    Keepers
    	Cages
    		Animals
    ```

- 段有不同的物理表示方式，决定了它们在存储和访问上的组织方式，比如

  - 无序
  - 可通过索引进行组织
    - 按某个关键字排序
    - 通过哈希函数组织

**分层表示的例子**

假如有两个饲养员，3 个动物，2 个笼子

![截屏 2024-07-16 09.38.31](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6695cf1c64dea.png)

这个例子中的物理表示方法为

```text
Keeper1段
A1段   A2段  A3段   // A表animal
C1段   C2段  C3段   // C表cage
```

#### 段的结构

- 每个段都有一个特殊的物理表示方式
  - 由数据库管理员选择
- 段的结构选择影响到他们所支持的操作。

#### IMS、DL/1 的操作

- GetUnique(segtype, pred)

  - 从指定段类型中获取满足特定条件（pred）的第一个记录
  - 只有被组织成 hash/有序段才能被支持

- GetNext(segtype, pred)

  - 获取层次结构中符合条件的第一个或下一个记录

  - 第一次调用 `GetNext("Animals", "type = 'salamander'")`：在 `Animals` 段中查找第一个类型为 "salamander" 的记录。

    后续调用 `GetNext("Animals", "type = 'salamander'")`：获取下一个类型为 "salamander" 的记录。

- GetNextParent(segtype, pred)

  - 类似 `GetNext`，但不会向上移动到层次结构中的下一个父段
  - 限制在当前父段内搜索。

- Delete， Insert

**例子**

![截屏 2024-07-16 09.54.38](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6695d2e329fca.png)

**1、 找到饲养员 Jane 看管的所有笼子**

```text
GetUnique(Keepers, name="Jane") // 将当前位置隐式地导航到 Jane 的记录。此时，系统在 Keepers 段内，指向 Jane 的记录

Until done:
  cageid = GetNextParent(cages).no  // 操作获取下一个笼子的记录
  print cageid
```

`GetNextParent` 操作会在当前父记录（即 Jane）的范围内查找 `cages` 段的记录，并获取该记录的 ID

**2、找到看管 6 号笼子的管理员**

```text
keep = GetUnique(keepers)
Until done:
  cage = GetNextParent(cages, id=6)
  if (cage is not null):
  	print keep
 	keep = GetNext(keepers)
```

#### 缺点

- 数据重复，因为每个层次的节点都必须包含相关的子节点信息。
  - 在层次数据库中，完全避免数据冗余是很困难的，因为层次结构本身会导致某些数据项的重复出现。不同的层次结构设计可以在一定程度上减少冗余，但总会有某些部分的数据会重复存储。
- 低级编程接口的痛点，需要编写详细的搜索算法来遍历层次结构中的数据
- 物理数据独立性的限制
  - 如果根段的存储方式从索引改变为哈希，那么那些使用 `GetNext` 操作的程序可能会失败，因为哈希段不支持 `GetNext` 操作
  - 根段的类型改变，也会如此
  - 如果根段是顺序存储的，那么无法在中间插入新的记录
- 逻辑数据独立性的限制
  - 如果 schema 改变了，程序也要跟着改

#### 逻辑数据独立性

假设动物园管理层决定改变饲养员的工作方式：

- **旧制度**：一个饲养员负责多个笼子和笼子中的所有动物。
- **新制度**：一个饲养员只负责一个笼子及该笼子中的所有动物

这样一来，使用 `GN` 或 `GNP` 操作访问数据的程序必须更新，否则程序的行为可能不再符合预期

```text
// 旧结构
Keepers
  cages
  	Animal
// 新结构
cages
  keepers
    Animal  
```

### CODASYL 数据模型

用来解决 IMS/PL1 的局限性，基于图或网络数据模型

![截屏 2024-07-16 10.20.57](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6695d91249142.png)

记录能够根据一些 key 被 hash 或者排序。

**找到 Joe 看管的所有笼子**

![截屏 2024-07-16 10.24.31](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6695d9e7981ef.png)

```text
Find keepers(name = 'Joe')
	Until done:
		Find next animal in caredforby
			Find cage in livesin
```

这种编程方法就像是在一个复杂的地图上找到一个起点，然后沿着路径进行导航

- 每一行代码都隐含在这个结构中的某个位置
- 需要记住你所在的位置

#### 缺点

- 非常复杂——导航式编程
- 程序缺乏物理或逻辑数据独立性:
  - 如果要修改数据库结构，就得改程序；
  - 也不能随便改物理表示，因为不同的索引类型支持的操作可能不一样。

**关系模型**就是为了解决这个问题的。

### 关系型数据模型

#### 原则

- 简单的表示方式

- 面向集合的编程模型，不需要"导航"

- 不需要物理数据模型的描述（!）
  - 例如，不需要指定排序顺序、哈希等

#### 基本特征

- **数据表示方式**：所有数据都以记录（元组）的形式存在于表格中。
- **表格属性**：表格是无序的集合，其中不包含重复的记录。
- **数据库结构**：数据库由一个或多个这样的表格组成。
- **模式描述**：每个表格（关系）都有一个模式，描述了表格中每个列或字段的类型。
- **字段类型**：每个字段都是基本数据类型，而不是集合或其他关系。
- **物理表示不指定**：关系模型不关注数据的物理存储方式，例如索引类型、嵌套结构等。

**例子说明**

![截屏 2024-07-16 10.33.50](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6695dc1551b07.png)

## 关系代数

5 个基本操作

- 投影 Projection (π(T, c1, ... cn))
  - 选择部分列组成的子集
- 选择 Selection(𝞂(T, pred))
  - 选择满足条件的行组成的子集
- 笛卡尔积（叉积，Cross Product） (T1 x T2)
  - 连接两个表
- 联接（⨝(T1, T2, pred）) = 𝞂(T1 x T2, pred)
  - 用一个判定条件联接两个表
- 集合的操作（并、差等）
- ”代数“——对其自身的操作具有封闭性。 大白话就是说， 无论对数据库中的哪个关系（表）进行什么样的操作，都会得到一个新的关系（表）

![截屏 2024-02-21 16.23.14](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/65d5b2fd62c4e.png)

**用笛卡尔积实现连接**

![截屏 2024-07-16 10.45.49](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6695dee3754fb.png)

**例子： 找到笼子号 32 的动物们**

```text
𝞂(
	⨝ (
		animals,
		cages,
		animals.cageno = cages.no
	),
	bldg = 32
)
```

> 你觉得数据库就是这样实现代码？

```text
⨝(
	animals,
	𝞂 (
		cages,
		bldg = 32
	),
	animals.cageno = cages.no
)
```

### 关系代数的等价规则

- 连接重排序（目的得到的 Join 记录最少，一般有贪心算法和动态规划算法）
  - A ⨝ B = B ⨝ A
  - (A ⨝ B) join C = A ⨝ (B ⨝ C)
- 选择重排序
  - 𝞂1(𝞂2(A)) = 𝞂2(𝞂1(A))
- 选择下推
  - 𝞂(A ⨝_pred B) = 𝞂(A) ⨝\_pred 𝞂(B)
  - 𝞂可能仅用于一个表
- 投影下推
  - π(𝞂(A)) = 𝞂(π(A))
  - 可以在应用投影操作之前或之后应用筛选操作，结果应该是一样的。前提是投影操作不会移除筛选条件中使用的字段
  - 同样能应用在连接

## 物理独立性

物理独立性是指可以更改数据的表示方式而无需修改代码的能力。

例子

```sql
SELECT a.name FROM animals AS a, cages AS c
WHERE a.cageno = c.no AND c.bldg = 32
```

在上述查询中，并没有明确指定动物和笼子表格的数据表示方式。它们可以是排序的、存储在哈希表或树中等。如果改变了数据的物理表示方式，SQL 查询本身不会改变。

## 逻辑独立性

逻辑数据独立性是指可以在不需要修改代码的情况下更改数据库 schema。

- 如果只是添加一个列或者表格，这并不会造成问题。
- 视图（Views）允许我们将旧的模式映射到新的模式，使得旧的程序仍然可以正常工作。
- 即使是在修改现有字段的情况下，通过良好的视图设计，也可以确保旧程序与新模式的兼容性。

### 视图（View）简介

**视图**是一个基于其他表的逻辑定义表的方式。

例如， 一个视图可以计算每个笼子中的动物数量

```sql
CREATE VIEW cage_count AS
(SELECT cageno, count(*)
FROM animals JOIN cages ON animals.cageno = cages.no
GROUP BY cageno
)
```

这个视图可以像其他表一样在查询中使用。

**视图的例子**

>假设我想要添加多个喂食时间？
>
>如何支持旧程序？

- 将现有的 `animals` 表重命名为 `animals2`。
- 创建一个 `feedtimes` 表格。
- 从 `animals2` 中复制喂食时间数据。
- 从 `animals2` 中移除 `feedtime` 列。
- 创建一个名为 `animals` 的视图，该视图是对 `animals2` 和 `feedtimes` 表的查询

```sql
-- 创建一个名为 animals 的视图，查询 animals2 和 feedtimes 表
CREATE VIEW animals AS
SELECT a.name, a.age, a.species, a.cageno,
       (SELECT feedtime FROM feedtimes WHERE animalid = a.id LIMIT 1) AS feedtime
FROM animals2 a
);
```

## 总结： IMS vs. CODASYL vs. 关系型

![截屏 2024-07-16 11.04.29](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6695e3445f009.png)

## SQL

### Join（联接）

#### 引入

![截屏 2024-07-16 11.36.49](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6695ead864fcb.png)

加入饲养员和笼子的关系如上所示

Schema:

- Animals: (aid, name, age, species, acageno)
- Cages(no, feedtime, bldg)
- Keepers(id, name)
- keeps(kid, cageno)

**找到 32 号建筑物中的所有笼子**

- 命令式

  ```text
  for each row a in animals:
  	for each row c in cages:
  		if a.acageno = c.no and c.bldg = 32
  			output a
  ```

- 声明式

  ```sql
  SELECT name
  FROM animals, cages
  WHERE acageno = no AND bldg = 32;
  ```

- 另外一种声明式语法

  ```sql
  SELECT name
  FROM animals JOIN cages on acageno = no
  WHERE bldg = 32;
  ```

### 别名与歧义

![截屏 2024-02-18 21.30.26](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6695f062a140d.png)

**例子： 喂养熊的所有饲养员**

```sql
SELECT name FROM keepers JOIN keeps ON id = kid
JOIN cages on cageno = no
JOIN animals on cageno = no
Where species = 'bear'
```

> 这个 sql 语句并不能使用，为什么？

因为 SELECT name 时候这个 name 的指代不明确，没有指明是哪个实体。改成 animals.name 即可

### 聚合

**例子： 找到每个笼子由多少个饲养员管理**

```sql
SELECT no, count(*)
FROM cages JOIN keeps ON on=cageno
GROUP BY no
```

> 那没有饲养员管理的笼子呢？

可以使用右联或者外联

> [!IMPORTANT]
>
> count(*)， 所有行都被统计（包括 NULL）
>
> count(col) ，只统计非空的值的行

### Join（联接）

#### 左联

```sql
T1 LEFT JOIN T2 ON pred
```

- 所有满足 `pred` 条件的 `T1 x T2` 行。

- 以及 `T1` 中没有与 `T2` 中任何行匹配的所有行（这些行的 `T2` 列值将为空）。

#### 右联

与左联类似，但是方向相反

```sql
T1 LEFT JOIN T2 ON pred
```

- 所有满足 `pred` 条件的 `T1 x T2` 行。

- 以及 `T2` 中没有与 `T1` 中任何行匹配的所有行（这些行的 `T1` 列值将为空）。

#### 外联/全联

即把左联结果表+右联结果表组合在一起，然后过滤掉重复的

```sql
T1 OUTER JOIN T2 ON pred
```

#### 内联（默认）

```sql
T1 INNER JOIN T2 ON pred
# 或者直接
T1 JOIN T2 ON pred
```

- 所有满足 `pred` 条件的 `T1 x T2` 行
- 如果某行在其中一个表中没有匹配的行，那么这行将不会出现在结果集中

#### 自联

**例子，查找照顾熊和长颈鹿的所有管理员**

```sql
SELECT keepers.name
FROM keepers JOIN keeps ON id = kid
JOIN cages ON cageno = no
JOIN animals ON acageno =cageno
WHERE species = 'Bear' AND = species = 'Giraffe'
```

> 这个 SQL 并没有效果，为什么？

需要构建两个表，Bear keepers 和 Giraffe keepers，然后取交集

**先构建 Bear keepers 表**

![image-20240716175623140](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/669643ca5ca5f.png)

![image-20240716175718377](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66964401c8d10.png)

**再构建 Giraffe keepers 表**

![截屏 2024-07-16 17.59.04](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6696447286c80.png)

**最后联接**

![截屏 2024-07-16 17.59.46](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6696449ba2f3d.png)

## SQL 必要练习 + 论文阅读

1、 [完成 SQL 的练习]([1. SQL — A Practical Introduction to Databases (runestone.academy)](https://runestone.academy/ns/books/published/practical_db/PART1_SQL/index.html))

2、 [完成关系模型（3.1 节）的练习]([3. RELATIONAL DATABASE THEORY — A Practical Introduction to Databases (runestone.academy)](https://runestone.academy/ns/books/published/practical_db/PART3_RELATIONAL_DATABASE_THEORY/index.html))

3、 阅读参考书上的 Michael Stonebraker 和 Joseph Hellerstein 的文章《What Goes Around Comes Around》中的第 1 至 4 节

4、（可选）关系模型的开山鼻祖论文； E.F. Codd. A relational model of data for large shared data banks. Communications of the ACM, 1970.[[PDF](http://portal.acm.org/ft_gateway.cfm?id=362685&type=pdf&coll=GUIDE&dl=GUIDE&CFID=1781172&CFTOKEN=98614393)].

回答以下问题：

- 哪些类型的程序在 SQL 中编写起来容易？哪些类型的程序较难？
- 您觉得声明式编程比命令式编程更容易还是更难？
- 什么是数据独立性的概念？为什么它很重要？
- 关系模型背后的关键思想是什么？它们为何优于之前的模型？关系模型在哪些方面具有限制性？
- “分层”模型（如 IMS 系统）与 Codd 提出的关系模型之间最重要的区别是什么？
