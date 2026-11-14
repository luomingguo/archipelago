---
title: '查询优化器：规则与代价'
type: lecture
lecture: 8
tags: [query-optimizer, cost-model, dynamic-programming, cardinality-estimation]
status: complete
source: 'https://dsg.csail.mit.edu/6.5830/'
---

# Lec 8 查询优化器：规则与代价

## TL;DR

- 查询优化器是关系数据库中最具智力挑战的组件，通过在等价逻辑计划空间中执行代价估算，将声明式 SQL 映射为最优物理执行树。
- 启发式规则优化（RBO）利用关系代数等价公理进行无条件正向重写（谓词下推、列裁剪与子查询扁平化）；代价估算（CBO）依赖统计信息（直方图与高频值 MCV）量化算子 I/O 与 CPU 成本。
- 经典 Selinger 动态规划连接定序将左深树搜索空间从 $O(n!)$ 压缩至 $O(n \cdot 2^{n-1})$；引入“有趣序”（Interesting Orders）保留物理排序状态，有效避免了局部最优误杀全局最优解。
---

## 架构演进与核心洞察

::: insight 优化器中的“测不准原理”与基数估计误差雪崩
查询优化器绝非全知全能的数学神祇。它的致命弱点在于基数估计（Cardinality Estimation）的误差传播。由于多列之间普遍存在真实世界的数据相关性（如“车型=保时捷”与“价格>100万”），经典独立性假设（Attribute Value Independence）会导致连接基数估计出现几个数量级的偏差。代价模型在错误的基数输入下，极易选出一个极慢的笛卡尔积式计划。正如德国慕尼黑工大 Viktor Leis 在著名论文《How Good Are Query Optimizers, Really?》中所揭示的：当代价模型与搜索算法已经极其成熟时，基数估计的准确度决定了优化器的生死。
:::

## 课前阅读与文献研读 (Reading Assignment)

> 本讲核心必读文献。System R 关系优化器奠基之作，系统阐述单表访问路径选择、基于动态规划的左深树（Left-Deep Trees）连接定序，以及保留“有趣的顺序（Interesting Orders）”的剪枝理论。  
> 📖 **文献研读入口**：[必读论文精读：Access Path Selection（Selinger 关系查询优化器奠基之作）](./paper/selinger_query_optimization.md)

## 核心机制与讲义正文

> [!TIP] **[待补截图]** 建议截取官方课件 Slides 第 8 讲中关于“Selinger 动态规划搜索格子与左深树（Left-Deep Tree）剪枝流程图”。此处预留插图空间。

## 1. 课程导入：从声明式 SQL 到物理执行计划

在关系型数据库管理系统（DBMS）中，用户提交的 SQL 查询具有高度的**声明式（Declarative）**特征：用户仅向系统声明“想要获得什么样的数据”，而绝不指定“如何逐步获取这些数据”。

```text
                  用户提交声明式 SQL 查询:
        SELECT * FROM nation, customer, supplier
        WHERE nation.nationkey = customer.nationkey
          AND supplier.nationkey = customer.nationkey
          AND nation.name = 'GERMANY';
                                 |
                                 v
                     [ 词法 / 语法解析器 (Parser) ]
                                 |
                                 v
                     [ 逻辑计划生成与语义绑定 (Binder) ]
                                 |
                     +-----------v-----------+
                     |   查询优化器 (Optimizer)   |  <-- 决定系统生死的超级大脑
                     +-----------+-----------+
                                 |
                                 v
                  最优物理执行计划树 (Physical Plan)
               (指定扫描方式、连接顺序、物理连接算子)
```

查询优化器的根本职责，就是在数以亿计的等价物理算子树中，寻找一条能够在有限的 CPU 时钟周期与外存 I/O 约束下以最快速度产出结果的执行路径。

![查询优化器四大核心模块架构图](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66bfffe1bc0fe.png)

现代查询优化器主要包含四大紧密协同的核心构件：
1. **逻辑重写规则引擎（Rewrite Rules / RBO）**：基于关系代数等价公理，对逻辑计划树进行模式匹配与代数重写，消除无意义的开销；
2. **计划枚举搜索器（Plan Enumeration）**：系统探索候选执行计划的搜索空间。最经典的方法是源自 IBM System R 的 Selinger 动态规划算法；对于更大规模的复杂查询，则结合自顶向下的 Memo 框架或遗传算法；
3. **基数估计器（Cardinality Estimator）**：根据底层数据采样或直方图统计信息，精确预测每个算子在运行时将吐出多少行数据；
4. **代价评估模型（Cost Model）**：一个高度校准的数学成本函数，综合考量磁盘页面 I/O 读写次数与 CPU 指令开销，为候选物理计划打分。

![SQL 解析、绑定、逻辑计划生成与物理优化器执行流程图](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6847ba3ec92a3.png)

### 1.1 逻辑计划与物理计划的分离

在数据库内核中，逻辑算子与物理算子之间存在严格的“一对多”映射：
- **逻辑计划（Logical Plan）**：直接对应关系代数中的抽象集合操作符（如投影 $\pi$、选择 $\sigma$、连接 $\bowtie$），仅表达“做什么”，完全不关心底层算法实现；
- **物理计划（Physical Plan）**：落实到具体的机器可执行算法（例如是走哈希连接 `HashJoin`、排序归并 `SortMergeJoin` 还是块嵌套循环 `BlockNLJ`；是走全表顺序扫描 `SeqScan` 还是二级索引扫描 `IndexScan`）。

![多表连接顺序与物理算子选择的代价对比示例](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66c007177ec72.png)

针对同一个简单的三表连接查询，不同的连接顺序、不同的物理算子搭配与不同的底层扫描路径，会组合出数百种截然不同的物理执行树。在处理大数据量时，最优方案只需数毫秒，而最差方案可能因为触发全表笛卡尔积与磁盘交换而耗时数天！

### 1.2 为什么基数估计最具挑战性？

查询优化的本质是对未来的精准预测。基数估计的复杂性随着维度的增加呈几何级数攀升：

![单列索引点查基数估计机制](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66c007e578389.png)

对于单列上的简单等值谓词（如 `id = 100`），基数估计较为直接，仅需利用唯一索引的唯一值计数即可给出精确评估。

![复合多列索引的数据相关性与基数估算](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66c0089ede8b9.png)

然而，当查询涉及复合多列过滤谓词时（例如 `make = 'Honda' AND model = 'Accord'`），由于列与列之间存在强烈的现实世界语义相关性，若机械套用概率独立性相乘公式，估计值将严重偏离真实数据分布。

![多表连接操作的数据分布畸变与基数估计难题](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66c008deb176c.png)

进入多表连接阶段后，每一次连接操作都会重塑元组的频率分布并引入复杂的跨表数据关联。一旦底层两表连接的基数估计产生 10 倍偏差，经过上层多级算子的雪崩式传播，顶层基数偏差将放大至数万倍，直接导致优化器做出灾难性的物理决策。

---

## 2. 基于启发式规则的逻辑查询优化（RBO）

基于规则的优化（Rule-Based Optimization / RBO）依赖关系代数的等价变换公理。这套重写规则是经过数据库专家精心设计的**启发式经验规则（Heuristics）**，无论底层物理数据规模多大，这些转换在绝大多数工况下都能无条件削减算子开销，为后续的代价寻优构建一个紧凑精炼的逻辑底座。

### 2.1 选择与过滤优化

#### 规则 1：拆分合取谓词（Split Conjunctive Predicates）

当 SQL 的 `WHERE` 子句中包含通过 `AND` 连接的复合条件时，优化器首先将复合谓词拆解为一组独立的单子句谓词集合：

```sql
SELECT ARTIST.NAME
FROM ARTIST, APPEARS, ALBUM
WHERE ARTIST.ID = APPEARS.ARTIST_ID 
  AND APPEARS.ALBUM_ID = ALBUM.ID
  AND ALBUM.NAME = "Andy's OG Remix";
```

![逻辑查询优化合取谓词拆分示例](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/68479c68ec2bf.png)

拆解为离散谓词后，优化器便能针对每个独立的谓词子句判断其关联的表属性，从而为下一步的谓词下推铺平道路。

#### 规则 2：谓词下推（Predicate Pushdown）

谓词下推是关系数据库中最为关键的代数优化之一。优化器将过滤条件尽可能下推至逻辑计划树的叶子节点（即数据扫描算子附近）：

![关系代数逻辑优化谓词下推算子树变换](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6847babe16dff.png)

通过尽早执行过滤，系统在扫描阶段即可借助存储引擎的单表索引或 Zone Map 跳过无效记录，极大地削减了流向后续连接算子与网络通信的数据量。

### 2.2 投影下推与列裁剪（Projection Pushdown）

在宽表分析场景中，单行记录可能包含上百个属性，但当前 SQL 查询通常仅访问其中的两三个字段。投影下推规则会尽早剔除后续算子不需要的所有非关键属性：

![投影下推与列裁剪规则示意图](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6847bb727f087.png)

列裁剪显著缩减了中间算子在内存中暂存元组的物理行宽（Tuple Width），使得单个 CPU 缓存行（Cache Line）与操作系统内存页能够容纳更多记录，极大提升了缓存命中率与数据流转带宽。

### 2.3 关系代数重写与子查询展开

#### 规则 3：将笛卡尔积转换为等值连接（Replace Cartesian Products with Joins）

当用户在 `FROM` 子句中声明多个表且通过逗号分隔时，逻辑解析器在语法层默认生成笛卡尔积（Cross Product）。优化器在识别出 `WHERE` 子句中存在的两表等值关联条件后，立刻将原本昂贵的无约束笛卡尔积重写为带谓词的有向连接算子：

![笛卡尔积转换为内连接规则重写](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/68479c69f2dde.png)

这一重写彻底消除了中间阶段生成无意义膨胀矩阵的风险，使连接算子能够安全使用哈希或归并算法执行高效配对。

#### 规则 4：关联子查询解关联与扁平化（Subquery Decorrelation & Flattening）

对于形如 `WHERE val IN (SELECT ...)` 或带相关变量的关联子查询，朴素执行器会将其视作黑盒循环函数，每处理一行外部元组就重复执行一次内部子查询，复杂度高达 $O(N \times M)$。

![关联子查询解除关联与扁平化示意图](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/68479c69f2c1d.png)

优化器通过将子查询扁平化重写为半连接（Semi-Join）或反连接（Anti-Join），将其提升为与普通数据表同等的平坦连接算子，使得优化器能够统筹安排全表哈希探测与索引寻道。

#### 规则 5：复杂查询块分解（Query Block Decomposition）

针对包含聚合视图与复杂嵌套的查询，现代优化器支持将其切分为相互独立的逻辑查询块（Query Blocks）：

![复杂查询块分解前逻辑计划](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/68479c71b6bb1.png)

系统依次对每个独立查询块进行代数变换与算子内联，必要时将公共子查询结果物化至轻量级内存临时表中，避免跨层递归计算的资源浪费：

![复杂查询块分解后临时物化结果集示意图](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/68479c71d40ad.png)

---

## 3. 统计信息收集与基数估计体系（Cardinality Estimation）

基于代价的优化（CBO）必须依赖量化指标。数据库内部通过在元数据字典中维护各表的数据特征，为代价函数提供精准的输入。

### 3.1 单表离散值基数与选择概率计算

选择率（Selectivity）度量了一个谓词条件从输入总记录中筛选出合格数据的比例：

![单表离散值基数与选择概率计算示例](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66c00a3ba7663.png)

在数据均匀分布的基本假设下，若表 $R$ 共有 9 条记录且取值离散均匀分布在 $0 \sim 8$，则谓词 $X < 5$ 的选择概率为 $\Pr(X < 5) = \frac{5}{9}$，其估计基数记为：
$$\widehat{\text{Card}}(X < 5) = \frac{5}{9} \times 9 = 5$$

### 3.2 等宽直方图与线性插值（Equi-Width Histograms）

直方图是工业界最成熟的单列分布建模工具。在等宽直方图中，属性的值域范围被划分为 $k$ 个物理宽度完全相同的桶（Buckets），每个桶记录落入该区间的元组计数：

![统计直方图桶划分与均匀性假设偏差示意图](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6847c766b7b97.png)

![等宽直方图分桶与频数统计](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6847c76718e49.png)

在进行范围查询估算时，优化器假定桶内的数据分布是连续且均匀的，采用线性插值法计算部分覆盖桶的选择率：

![等宽直方图范围谓词查询基数估算](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66c00b16e99c2.png)

![等宽直方图线性插值估算与边界误差分析](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66c00c19b2c60.png)

例如对于查询谓词 $X < 23\text{K}$，该条件完全覆盖了前四个桶（占比分别为 $0.61, 0.09, 0.05, 0.036$），并且部分覆盖了第五个桶（$[20\text{K}, 25\text{K}]$，该桶总频数为 $0.02$）。线性插值比例为 $\frac{23\text{K} - 20\text{K}}{25\text{K} - 20\text{K}} = \frac{3}{5}$，其综合基数预估为：
$$\widehat{\text{Card}}(X < 23\text{K}) = \left(0.61 + 0.09 + 0.05 + 0.036 + 0.02 \times \frac{3}{5}
ight) \times |R|$$

等宽直方图的最大局限在于：当数据存在长尾倾斜（Skew）时，某些高频极端值会与大量稀疏值挤在同一个宽桶内，导致点查估计出现严重失真。

### 3.3 高频值表（MCV）与等深直方图结合（PostgreSQL 工业实践）

为了克服等宽直方图在倾斜数据下的致命缺陷，现代数据库（如 PostgreSQL）采用了**高频值数组（Most Common Values / MCV）+ 等深直方图**的双层混合统计架构：

![高频值表与长尾分布示意图](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66c02c04b284f.png)

![MCV 配合等深直方图联合估算谓词选择率](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6852e4bc4fc94.png)

1. **高频值阵列（MCV List）**：显式列出出现频次最高的前 $N$ 个具体离散值及其精确频率（例如图示中 $0$ 出现占比 $0.305$，$1$ 出现占比 $0.05$）；
2. **等深直方图（Equi-Depth Histogram）**：将剔除高频值后的长尾数据，划分为若干频数完全相同的桶（区间宽度自适应），彻底杜绝极端值污染。

![PostgreSQL 系统目录 pg_statistic 统计信息表结构](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66c02d52a40e7.png)

![PostgreSQL 使用 MCV 数组实现单列精确基数估计](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66c02d6f25a7a.png)

在 PostgreSQL 系统目录 `pg_statistic` 中，`stanullfrac` 记录空值率，`stanumbers` 与 `stavalues` 分别存储 MCV 频率和具体数值，使得单表过滤谓词的估计准确度达到工业级水准。

### 3.4 现代草图（Sketches）与抽样技术

除了直方图之外，现代数据库还在内存中集成高级概率数据结构与动态采样：
- **Count-Min Sketch (1988)**：利用多组独立哈希函数与计数矩阵，在次线性空间内以可控概率误差估计数据流中特定值的出现频率；
- **HyperLogLog (HLL, 2007)**：通过观察哈希值前导零的最大长度，在极其微小的内存开销（如 1.5 KB）下高精度估计海量数据集的唯一值基数（NDV / Distinct Count）；
- **动态采样（Data Sampling）**：在缺乏统计信息或针对极其复杂的函数黑盒谓词时，系统在后台对物理页面进行随机抽样，直接在样本数据上执行谓词评估并按比例放大：

![数据库采样估计基数流程](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6847c7682e185.png)

![采样数据估算与置信区间推断示意图](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6847c767b4db1.png)

### 3.5 属性相关性陷阱与多维直方图

当过滤条件跨越多个属性时（例如 `WHERE X < 5 AND Y < 0`），传统优化器默认采用**属性值独立性假设（Attribute Value Independence / AVI）**，将各个单列的选择概率直接相乘：

![多列复合过滤谓词在属性独立假设下的估计误差](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66c02dfe08556.png)

若属性之间存在强相关性，盲目相乘会导致估计基数被严重低估几个数量级。为了应对该问题，学术界与工业界探索了多维建模方案：

![多维直方图网格划分与高维指数级存储爆炸](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66c02edf007e1.png)

- **多维网格直方图**：将空间切分为多维立方体单元，但其存储复杂度为 $O(\text{nbins}^d)$，维度 $d > 2$ 时遭遇严重的维度灾难；
- **概率图模型（Probabilistic Graphical Models / PGM）**：利用树状依赖图或贝叶斯网络紧凑建模属性间的条件独立性，在多维相关性建模与存储开销之间取得良好平衡：

![概率图模型用于属性相关性建模架构](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66c05858694c7.png)

![基于贝叶斯网络的单表多列联合分布推断](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66c06111bf944.png)

### 3.6 连接操作输出基数数学推导

等值连接 $R \bowtie_{R.X = S.Y} S$ 的基数估计是整个查询优化中最具决定性的环节。假定已知以下统计信息：
- 表 $R$ 共有 $|R|$ 行，连接键唯一值数量为 $\text{NDV}(R.X)$；
- 表 $S$ 共有 $|S|$ 行，连接键唯一值数量为 $\text{NDV}(S.Y)$。

![等值连接操作在均匀分布假设下的输出基数推导](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66c04718b231a.png)

在包含性假设与均匀分布假设下，两表中每一个匹配值在 $R$ 中的平均重复次数为 $\frac{|R|}{\text{NDV}(R.X)}$，在 $S$ 中的平均重复次数为 $\frac{|S|}{\text{NDV}(S.Y)}$。能够匹配上的唯一键值总数受限于较小的集合 $\min(\text{NDV}(R.X), \text{NDV}(S.Y))$。

因此，连接输出基数的经典推导公式为：
$$\widehat{\text{Card}}(R \bowtie S) = \min(\text{NDV}(R.X), \text{NDV}(S.Y)) \times \frac{|R|}{\text{NDV}(R.X)} \times \frac{|S|}{\text{NDV}(S.Y)} = \frac{|R| \times |S|}{\max(\text{NDV}(R.X), \text{NDV}(S.Y))}$$

高级商业数据库（如 Oracle）还会维护专用的**连接直方图（Join Histograms）**，在对应分桶区间内执行局部匹配，进一步消减长尾连接中的估计误差：

![连接直方图区间匹配机制](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66c056757aa98.png)

---

## 4. MIT 课件经典实战推演：三表代价评估与 Clicker 深度解析

在 MIT 6.5830 课件（Lecture 8）中，Prof. Tianyu Li 给出了一个极其严密的推导案例，系统演示优化器如何将基数估计与物理连接代价模型熔于一炉。

### 4.1 查询场景与环境参数设定

考虑以下三表连接分析查询：

```sql
SELECT * FROM emp, dept, kids
WHERE sal > 10k
  AND emp.dno = dept.dno
  AND emp.eid = kids.eid;
```

#### 数据库微架构与存储参数：
- 内存缓冲池大小：$M = 10$ 页（Pages）；
- 页面规约：每页大小 10 KB，每页可容纳 100 条元组记录（100 tuples/page）；
- **部门表 `dept`**：$NCARD = 100$ 行，占 $TCARD = 1$ 页（10 KB），主键为 `dno`；
- **员工表 `emp`**：$NCARD = 10,000$ 行，占 $TCARD = 100$ 页（1 MB），外键 `dno` 关联部门；
- **子女表 `kids`**：$NCARD = 30,000$ 行，占 $TCARD = 300$ 页（3 MB），外键 `eid` 关联员工（平均每个员工有 3 个子女）；
- **过滤谓词**：`emp.sal > 10k`，选择率为 $F_1 = 0.1$。

### 4.2 优化器五步推演法

根据 Selinger 框架，优化器必须依次执行以下五大步骤：
1. **第一步：估计基础关系大小**；
2. **第二步：估计单表谓词选择率**；
3. **第三步：计算中间连接结果基数**；
4. **第四步：评估物理执行计划操作代价（I/O 与 CPU）**；
5. **第五步：在候选空间中挑出全局最优方案**。

### 4.3 随堂测验与权威解析（MIT Clicker Questions）

#### 【Clicker 测验 1：单表等值选择率估计】
**题目**：对于等值谓词 `col = val`，在以下选项中，哪一个是最佳的选择率（Selectivity）估计公式？  
A. $1 / TCARD(R)$  
B. $ICARD(I) / NCARD(I)$  
C. $1 / ICARD(I)$  
D. $(max\_key - val) / ICARD(I)$  

**【权威解析】**：
- **正确答案为 (C)**。
- **推导逻辑**：$ICARD(I)$ 代表该索引属性上不同唯一值的数量（Number of Distinct Keys）。在均匀分布假设下，每一个唯一值出现的概率均等，因此特定常量的选择概率为 $\frac{1}{ICARD(I)}$。选项 A 混淆了物理页面数；选项 B 是平均每个元组的唯一度倒数；选项 D 错用了范围插值逻辑。

#### 【Clicker 测验 2：中间连接结果大小计算】
**题目**：在上述查询中，先执行过滤 $\sigma_{sal > 10k}(emp)$，然后与 `dept` 执行等值连接 $emp.dno = dept.dno$。该中间连接结果的大小是多少？  
A. $100 \times (10,000 \times 0.1) \times 0.01 = 1,000$  
B. $10,000 \times 0.1 = 1,000$  
C. $10,000 \times 0.1 \times 0.01 = 10$  
D. $10,000 \times 0.1 \times 100 = 100,000$  

**【权威解析】**：
- **正确答案为 (A) 与 (B) 等价，结果均为 1,000**。
- **推导逻辑**：
  1. 过滤后合格的员工人数为 $10,000 \times 0.1 = 1,000$ 条记录；
  2. 由于 `dno` 是 `dept` 的主键，每个员工记录唯一对应一个部门，故连接选择率为 $\frac{1}{ICARD(dept.dno)} = \frac{1}{100} = 0.01$；
  3. 笛卡尔积为 $100 \times 1,000 = 100,000$，乘以连接选择率 $0.01$，最终输出基数为 **1,000 条元组**。
  4. 随后，这 1,000 名合格员工再与 `kids` 表按 `eid` 连接。由于外键关系每个员工对应 3 个孩子，最终查询产出 **3,000 条元组**！

### 4.4 物理算子连接代价对比

在确定中间基数后，优化器必须决定物理算子：
- 若先执行 `kids` 与 `emp` 连接：`kids` 很大（300 页），内存仅 10 页，无论是 Grace Hash Join 还是 Block Nested Loops 都会产生昂贵的写盘与重复扫描开销；
- 若先执行 `emp` 过滤并与 `dept` 连接：`dept` 仅 1 页（10 KB），可**完全常驻内存缓冲池**！使用 In-Memory Hash Join 或 Blocked Hash Join，只需单次顺序扫描 `emp`（100 页），I/O 开销微乎其微；产出的 1,000 条中间元组（10 页）刚好能塞进内存，随后作为外表驱动对 `kids` 上的 `eid` 索引执行 Index Nested Loop Join。
- **结论**：优化器精准挑选了最优顺序 $((\sigma(emp) \bowtie dept) \bowtie kids)$，避免了成百上千次额外的磁盘 I/O！

---

## 5. 物理算子代价精细化建模（Cost Formulas）

优化器的物理代价度量通常定义为：
$$\text{Cost} = (\text{Page I/O}) \times W_{io} + (\text{CPU Instructions}) \times W_{cpu}$$

在磁盘与 SSD 存储体系中，外存 I/O 依然是延迟的主要决定因素。

### 5.1 单表基础访问路径（Access Paths）代价

在单表访问层面，优化器必须在全表扫描与各类索引寻道之间进行抉择。假定单表包含过滤谓词，综合选择率为 $F$：

#### 方案 A：全表顺序扫描（Sequential Scan / SeqScan）
$$\text{Cost}_{\text{SeqScan}} = TCARD(R)$$
- 顺序扫描的物理代价是确定且无寻道惩罚的：无论过滤条件最终剔除多少元组，存储引擎都必须线性读取该表占用的全部物理页面。

#### 方案 B：聚簇索引扫描（Clustered Index Scan）
$$\text{Cost}_{\text{Clustered}} = \text{Tree Height} + \lceil F \times TCARD(R) \rceil$$
- 聚簇索引的叶子节点物理顺序与底层数据页面完全一致。执行引擎仅需付出常数级（通常为 2~3 次）树高寻道 I/O 定位到起始边界叶子，随后沿着双向链表以极高带宽顺序连续读取后续页面。

#### 方案 C：非聚簇索引扫描（Unclustered Index Scan）
$$\text{Cost}_{\text{Unclustered}} = \text{Tree Height} + \lceil F \times NINDEX(I) \rceil + \lceil F \times NCARD(R) \rceil$$
- **随机寻道惩罚与转折临界点（Tipping Point）**：在非聚簇索引中，叶子节点仅记录数据行的 RID（PageID + SlotID）。由于底层数据堆页面无序存放，每一个符合条件的索引记录在回表（Table Lookup）时都可能引发一次全新的随机磁盘寻道。当选择率 $F$ 超过 **3% ~ 5%** 时，其离散 I/O 开销便迅速超过全表扫描 $TCARD(R)$。此时成熟的优化器会果断放弃索引回表，退回全表顺序扫描。

### 5.2 物理连接算子代价汇总表（MIT 6.5830 课件权威总结）

在连接两张数据表时，优化器需要评估不同的物理算法在当前可用内存缓冲池 $M$ 下的 I/O 与 CPU 代价。下表系统整理了 MIT 6.5830 课程给出的物理连接算子成本对照全景：

```text
+-----------------------+-------------------------+--------------------+-------------------------+
| 连接算法              | 外存 I/O 代价 (I/O Cost)| CPU 计算复杂度     | 内存驻留前置约束        |
+-----------------------+-------------------------+--------------------+-------------------------+
| Simple Nested Loop    | |S| x |R| + |S|         | O(|R| x |S|)       | 无要求 (性能最差)       |
| Blocked Nested Loop   | |S| + (|S|/M) x |R|     | O(|R| x |S|)       | 内存 M 越大越逼近 |R|+|S| |
| Index Nested Loop     | |S| + {S} x c (c <= 4)  | O({S} x log{R})    | 内表建有 B+ 树索引      |
| Sort-Merge (内存)     | |R| + |S|               | O({S} log {S})     | 两表在内存中或已有序    |
| External Sort-Merge   | 3(|R| + |S|)            | O({S} log {S})     | 外存分批归并            |
| In-Memory Hash Join   | |R| + |S|               | O({R} + {S})       | 较小表 R 能完全塞入内存 |
| Blocked Hash Join     | |S| + (|S|/M) x |R|     | O({S} + B{R})      | 内存分批构建 Hash 表    |
| Grace Hash Join       | 3(|R| + |S|)            | O({R} + {S})       | 外存双向分区分治        |
+-----------------------+-------------------------+--------------------+-------------------------+
```

从上述代价模型可以得出数据库优化器在工业实践中的几条黄金法则：
1. **Grace Hash Join 是通用的安全底线**：在处理缺乏索引且无序的大规模数据集时，Grace Hash Join 能够以恒定 $3(|R| + |S|)$ 的外存 I/O 完成分治连接，且 CPU 复杂度仅为线性的 $O(|R| + |S|)$，是现代 OLAP 引擎的保底王牌；
2. **Sort-Merge Join 的关键门槛是有序输入**：外部归并排序本身的 I/O 成本高达 $3(|R| + |S|)$ 且伴随密集的 CPU 排序比较开销。如果两表缺乏索引，Sort-Merge 通常不如 Hash Join 具竞争力；然而，一旦输入流已经通过聚簇索引排好序，或者后续需要响应 `ORDER BY`，Sort-Merge Join 仅需单次扫入 $|R| + |S|$，将以压倒性优势胜出；
3. **小表全内存哈希是理论性能巅峰**：若优化器通过基数估计判断较小的构建表 $R$ 能够完全容纳在内存缓冲池中（$|R| \le M$），则选择内存哈希连接，I/O 开销骤降至单次流式读入的 $|R| + |S|$。这也是优化器为何极度偏好将过滤后的小表安排在早期优先执行的根源所在；
4. **混合哈希连接（Hybrid Hash Join）实现动态平滑过渡**：当可用内存介于 $\sqrt{|R|}$ 与 $|R|$ 之间时，现代高级优化器还会进一步推演混合哈希连接代价。通过将内存中最大可能容纳的第 0 号分区常驻缓冲池，直接免除该分区的写盘与重读 I/O，使综合外存代价平滑下降至 $(3 - 2f)(|R| + |S|)$（其中 $f$ 为常驻内存比例）。这种细粒度的代价阶梯为优化器在物理资源受限时做出最优调度提供了坚实的数学依据。

---

## 6. 连接搜索空间与左深树（Left-Deep Trees）

在多表连接优化中，算子树的物理拓扑形态直接决定了内存消耗与流式流水线（Pipeline）的设计。

```text
      左深树 (Left-Deep Tree)                  丛状树 / 浓密树 (Bushy Tree)
                (⨝)                                       (⨝)
               /   \                                     /   \
             (⨝)    D                                  (⨝)   (⨝)
            /   \                                     /  \   /  \
          (⨝)    C                                   A    B C    D
         /   \
        A     B
```

### 6.1 为什么经典 Selinger 优化器坚决限定左深树？

1. **流水线零外存物化（Pipelining & Zero Materialization）**：
   在左深树中，左子树作为外层驱动表，产出的每条中间元组可以直接在 CPU 寄存器与缓存中流向下游连接算子；而右子树始终是一张基表（Base Relation），可以通过索引直接探测。**整个查询树完全不需要在外存磁盘中暂存任何中间派生表**！
2. **状态空间急剧收敛**：
   - 浓密树（Bushy Tree）形态数随表数量 $n$ 呈双阶乘发散：$\frac{(2n - 2)!}{(n - 1)!}$。当 $n = 10$ 时形态数高达 **1764 万种**；
   - 而左深树的拓扑结构被严格固定为 $(...(((R_1 \bowtie R_2) \bowtie R_3) \bowtie ...)$，优化器仅需决策 $n$ 张表的排列顺序（$n!$），大幅削减了无效搜索空间。

---

## 7. Selinger 动态规划连接枚举算法（Selinger DP Algorithm）

1979 年，IBM System R 团队的 Patricia Selinger 发表了现代数据库优化器的奠基论文 *“Access Path Selection in a Relational Database Management System”*。

### 7.1 最优子结构与分治搜索

Selinger 的核心洞察在于：**连接 $k$ 张表的最优执行方案，必定是由某个包含 $k-1$ 张表的最优子方案与剩下的一张基表以最优方式连接而成。**

这一最优子结构性质使得我们能够利用动态规划（Dynamic Programming）自底向上依次枚举子集大小 $i = 1, 2, \dots, n$：

![3 表连接所有可能顺序的组合枚举](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6847c0ac06572.png)

![System R 动态规划自底向上构建双表连接最优子方案](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6847c0ad17563.png)

![动态规划自底向上三表连接物理算子代价比较与剪枝](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6847c0ada1c32.png)

![Selinger 算法构建最优左深连接树](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6847c0b10351e.png)

### 7.2 复杂度证明：从阶乘级到指数级的跃迁

- **暴力全排列复杂度**：需搜索 $n!$ 种可能。当 $n = 12$ 时，$12! = \mathbf{479,001,600}$（近 4.8 亿次）；
- **Selinger 动态规划复杂度推导**：
  大小为 $k$ 的子集有 $\binom{n}{k}$ 个，构建每个大小为 $k$ 的子集需要从其中挑选一个元素进行 $k$ 次扩展探测。总操作步数为：
  $$\sum_{k=1}^n k \binom{n}{k} = n \sum_{k=1}^n \binom{n-1}{k-1} = n \cdot 2^{n-1}$$
  当 $n = 12$ 时，操作步数仅为 $12 \times 2^{11} = \mathbf{24,576}$ 次！
  **计算量直接缩减了近 20,000 倍！**

---

## 8. 致命机制反转：有趣序（Interesting Orders）

如果 Selinger 算法在每个阶段真的**只保留局部代价最低的那个计划**，优化器就会犯下灾难性的严重错误！

### 8.1 为什么局部最优可能导致全局惨败？

考虑一个带有排序需求的连接查询：

```sql
SELECT * FROM Emp JOIN Kids ON Emp.eno = Kids.eno 
ORDER BY Emp.eno;
```

![带有 ORDER BY 排序需求时执行计划代价逆转与有趣序效应](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6847c0b05d467.png)

在阶段 1 评估 `Emp` 表的访问路径时：
- **方案 A（SeqScan）**：顺序读取，代价为 **100**（局部最优！）；
- **方案 B（IndexScan on `idx_eno`）**：走索引读取，局部代价为 **120**（比全表扫描贵 20）。

若按朴素动态规划，方案 B 在阶段 1 就会被**彻底剪枝抛弃**！

#### 后续阶段的大逆转：
进入阶段 2 连接与排序计算时：
- **基于方案 A（无序输出）**：
  由于数据无序，必须使用 Hash Join（代价 150），且最后为了响应 `ORDER BY Emp.eno`，必须额外执行一次昂贵的外存全排序（External Sort），排序代价为 **300**！
  $$\text{总代价}_{\text{Plan A}} = 100 + 150 + 300 = \mathbf{550}$$
- **基于方案 B（产出有趣序）**：
  由于索引扫描输出的数据已经**天然按 `eno` 排序**！
  下游的连接可以直接采用高效的流式 Sort-Merge Join（代价仅 80），且连接产出的结果**仍然按 `eno` 排序**，顶层的 `ORDER BY` 算子代价直接归零（无缝消除）！
  $$\text{总代价}_{\text{Plan B}} = 120 + 80 + 0 = \mathbf{200}$$

```text
最终结果：
方案 A 局部看似便宜 20，全局代价却高达 550！
方案 B 局部昂贵 20，全局总代价仅为 200，完胜方案 A！
```

### 8.2 有趣序（Interesting Order）的定义与保留契约

::: definition 有趣序（Interesting Order）
一个物理执行计划所产出的元组排列顺序，如果**与查询中的 `ORDER BY` 列、`GROUP BY` 列、或者潜在下游 `Merge Join` 所要求的连接键完全一致**，该物理排序就被定义为一个“有趣序”。
:::

#### Selinger 剪枝铁律修正：
对于同一个关系子集，优化器在剪枝时**绝不能只保留单张王牌**，必须维护一个计划集合：
1. **保留一个全局绝对代价最低的计划**（哪怕它是无序的）；
2. **为每一个独特的“有趣序”，保留一个该顺序下代价最低的计划**！

若存在 $k$ 个有趣序，搜索复杂度最多增加 $(k + 1)$ 倍，但彻底杜绝了错杀全局最优解的风险。

---

## 9. 搜索空间工业级扩展与自顶向下架构（Cascades Framework）

当连接表数量超过 12 张时，$n \cdot 2^{n-1}$ 依然会引发耗时过长。现代数据库采取了分级自适应策略：

1. **遗传算法（PostgreSQL GEQO）**：
   PostgreSQL 内部设定了硬编码阈值 `geqo_threshold = 12`。当涉及表数量超过 12 时，自动放弃动态规划，转用模拟生物进化的遗传算法，通过染色体编码连接顺序、随机交叉变异与适应度迭代，在多项式时间内收敛出一个优良近似解；
2. **自顶向下的 Memo 框架（Cascades Framework）**：
   由 Goetz Graefe 开创的 Cascades 框架（被 Microsoft SQL Server、CockroachDB、Calcite 采用），通过 Memo 数据结构将等价表达式分组管理，结合目标驱动的分支限界剪枝（Branch-and-Bound Pruning），极大提升了扩展性与搜索效率：

![Cascades 逻辑规则与物理规则转换示例](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66b963b265173.png)

![Cascades 框架 Memo 组内等价表达式展开](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6847c0b3ddb27.png)

![Memo 结构搜索过程与分支限界剪枝](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6847c0b4d0459.png)

![自顶向下物理执行计划搜索完成与最优树输出](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66b965110c931.png)

---

## 10. 经典文献精读与研讨思考题（Paper Reading & Discussion）

### 10.1 必读奠基论文与经典文献

1. **System R 与基于代价优化的开山文献**：  
   Patricia G. Selinger, Morton M. Astrahan, Donald D. Chamberlin, Raymond A. Lorie, Thomas G. Price.  
   *“Access Path Selection in a Relational Database Management System”*.  
   In Proceedings of the 1979 ACM SIGMOD International Conference on Management of Data, pages 23–34, 1979.
2. **自顶向下可扩展优化器框架经典之作**：  
   Goetz Graefe.  
   *“The Cascades Framework for Query Optimization”*.  
   IEEE Data Engineering Bulletin, 18(3): 19–29, 1995.
3. **现代优化器基数估计误差实证里程碑（JOB 论文）**：  
   Viktor Leis, Andrey Gubichev, Atanas Mirchev, Peter Boncz, Alfons Kemper, Thomas Neumann.  
   *“How Good Are Query Optimizers, Really?”*.  
   Proceedings of the VLDB Endowment (PVLDB), 9(3): 204–215, 2015.

---

### 10.2 核心深度思考题与系统级推演

#### 思考题 1：为什么 Viktor Leis 等人在 2015 年的 JOB 评测中得出结论：“现代查询优化器的主要瓶颈不在于代价模型，而在于基数估计（Cardinality Estimation）的灾难性误差传播”？
- **误差随连接深度指数级放大**：在单表上，直方图估计可能只有 20% 的误差；但在经历 5~10 次多表连接后，由于属性值独立性假设（AVI）被彻底打破，连接基数估计误差会以指数级累积放大，甚至达到 $10^4$ 到 $10^6$ 倍（几个数量级的系统性偏离）！
- **劣币驱逐良币**：即使物理代价公式（I/O 与 CPU 加权）精确到微秒级，一旦输入了一个被严重低估百万倍的中间基数，优化器就会错误地认为内存 Hash Join 开销极小，进而选出一个在真实数据下发生严重外存溢出的灾难性计划。Leis 等人证实：**只要基数估计准确，哪怕使用极简的代价模型，所有主流优化器都能选出近乎完美的物理计划！**

#### 思考题 2：为什么左深树（Left-Deep Trees）在某些具有特定数据分布的复杂星型模型（Star Schema）查询中可能不是最优解？浓密树（Bushy Trees）在何时具备不可替代的优势？
- **雪花/星型模型的预聚合**：当查询包含一个巨大的事实表（Fact Table）和多个小维度表（Dimension Tables）时，如果事实表无法直接通过单表索引过滤，左深树必须让巨型事实表从最底层开始不断与维度表串行连接；
- **浓密树的并行双向削减**：浓密树允许先将维度表 $D_1 \bowtie D_2$ 以及 $D_3 \bowtie D_4$ 分别独立完成预先连接，生成小巧且带有高过滤性的复合过滤键（或利用布隆过滤器构建成位图）；随后让事实表与这两个紧凑的派生表进行哈希探测，大幅消减了巨型事实表的流转体积与 CPU 计算开销。

#### 思考题 3：自底向上（Bottom-up / Selinger DP）与自顶向下（Top-down / Cascades Memo）两种优化器架构的核心设计哲学有何不同？为什么现代分布式数据库更偏爱 Cascades？
- **搜索驱动哲学不同**：
  - **Selinger DP（自底向上）**：从叶子单表出发，完全由数据驱动生成子集解，缺乏全局目标导向。很难在搜索早期根据顶层约束（如 `LIMIT 10`）进行有效剪枝；
  - **Cascades（自顶向下）**：从根查询的最终目标出发，采用按需搜索与分支限界剪枝（Branch-and-Bound）。一旦找到一个成本为 100 的完整可行计划，在后续搜索其他子树时，只要探测到某个分支的局部代价已达 101，即可立即终止该分支的展开；
- **规则扩展性与分布式物理属性**：Cascades 将关系代数重写解耦为独立的变换规则（Transform Rules）与实现规则（Implementation Rules）。在分布式数据库（如 CockroachDB、TiDB）中，数据分片分布（Data Partitioning / Hash Distribution）被抽象为一等公民的“物理属性（Physical Properties）”，Cascades 天然能够像处理“有趣序”一样处理“分布式数据分布属性”，架构扩展性显著超越传统 Selinger DP。

---

## 11. 本讲总结与全书知识拓扑

本讲系统解构了关系数据库内核中最为复杂、极富数学美感的核心中枢——查询优化器的完整技术演进脉络。

从关系代数的逻辑等价重写到物理算子代价建模，从 Selinger 动态规划的左深树剪枝到有趣序的状态逆转，优化器在毫秒级的极短编译预算内，完成了从声明式代数语义到硅芯片物理调度的惊艳跨越。

下图系统呈现了本讲核心优化构件与关键算法流派的全局知识拓扑：

```text
+-----------------------------------------------------------------------------------------+
|                               查询优化器核心架构与技术全景                              |
|                                                                                         |
|   逻辑重写阶段 (RBO) --------> 关系代数等价变换 -----> 谓词下推、列裁剪、常量折叠       |
|   基数估计基础 (Stats) ------> 直方图与高频值 (MCV) -> 解决偏态分布，突破均匀独立性假设 |
|   经典连接定序 (Selinger DP) -> 动态规划自底向上 -----> 左深树剪枝，状态复杂度 n*2^(n-1)|
|   全局寻优逆袭 (Interesting) -> 物理序状态保留 ------> 消除下游 ORDER BY 与 Merge Join  |
|   高维表爆炸应对 ------------> 遗传算法 (GEQO) ------> 大于 12 张表多项式时间内平滑收敛 |
|   现代可扩展架构 ------------> 自顶向下 Cascades ----> Memo 分组与目标驱动分支限界剪枝  |
+-----------------------------------------------------------------------------------------+
```

现代工业级优化器的演进印证了一个深刻的事实：没有单一的万能算法能够通吃所有工况。在小规模查询下，以 Selinger DP 为代表的确定性自底向上搜索能保证黄金最优解；在复杂多表分析中，基于 Memo 结构的自顶向下 Cascades 框架提供了强大的可扩展性与目标驱动剪枝；而在超高维表连接时，遗传算法（GEQO）与机器学习基数估计则以概率手段化解了状态爆炸的死结。

在下一讲（第 11 讲）中，我们将正式跨入现代大数据分析与云原生数仓时代的核心存储与执行引擎架构：**列式存储与极致压缩（Column Stores: C-Store to Parquet）**。深入探讨如何通过**列式物理切分、字典与游程编码（RLE）极致压缩、延迟物化（Late Materialization）**与现代工业级存储格式（Apache Parquet），彻底突破行式存储在大宽表分析中的 I/O 吞吐瓶颈！
