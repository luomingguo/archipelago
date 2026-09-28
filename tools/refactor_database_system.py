#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deep refactoring and consolidation of 6.5830 Database System.
- Resolves all 37 required findings and 17 recommendation findings.
- Imports external lectures (lec2, lec4, lec16, lec21, b-tree, 17MPP).
- Decouples GoDB lab (700 lines) from index.md into project/godb_lab_guide.md.
- Generates compliant concept/b_tree_storage_engine.md.
- Injects standard frontmatter, unique ## TL;DR, and ::: insight semantic containers.
"""

import os
import re

EXT_DIR = '/Users/mac/Documents/MIT/6_ComputerScience/Computer Systems/6.5830 Database System'
REPO_DIR = '/Users/mac/Documents/MIT/archipelago/docs/zh/cs/computer_sys/database_system'

SPECS = {
    1: {
        'title': '关系模型与 SQL 基础',
        'en_title': 'Relational Model and SQL',
        'tags': ['relational-model', 'relational-algebra', 'sql-basics', 'declarative-query'],
        'tldr': [
            '关系模型建立在一阶谓词逻辑之上，通过二维关系（表）和元组（行）实现物理存储与逻辑数据的完全解耦。',
            '关系代数（选择、投影、笛卡尔积、集合差、重命名）构成了声明式查询优化的理论数学基石。',
            'SQL 作为声明式语言只描述“想要什么”而非“怎么去取”，由数据库内核负责计划生成与物理执行。',
        ],
        'insight': """::: insight 声明式语言的数据独立性价值
Codd 提出关系模型的最伟大贡献不仅在于表格，而在于确立了“物理数据独立性（Physical Data Independence）”。在关系模型诞生之前，网状模型（CODASYL）和层次模型（IMS）迫使程序员在代码里硬编码指针遍历逻辑。一旦磁盘物理布局变动，所有上层业务代码全部报废。SQL 的声明式本质把性能优化的沉重包袱从应用开发者肩上卸下，交给了内核查询优化器。
:::"""
    },
    2: {
        'title': '现代 SQL 与数据库系统运维',
        'en_title': 'Modern SQL and Database Administration',
        'tags': ['advanced-sql', 'window-functions', 'role-based-access', 'table-maintenance'],
        'tldr': [
            '现代 SQL-92/99 规范大幅超越基础 CRUD，引入通用表表达式（CTE）、递归查询与强大的窗口函数（Window Functions）。',
            '数据定义（DDL）、数据控制（DCL）与数据操作（DML）协同保障企业级多租户安全与模式完整性约束。',
            '系统运维通过基于角色的访问控制（RBAC）、资源组配额隔离及统计信息分析（ANALYZE）维持稳定吞吐。',
        ],
        'insight': """::: insight 窗口函数对传统分组的颠覆
初学者常将 `GROUP BY` 与窗口函数（`OVER (PARTITION BY ...)`）混淆。`GROUP BY` 是破坏性的——它将多行聚合坍缩为单行，导致行级明细丢失；而窗口函数在保留原有每一行明细数据的同时，沿窗口轴线计算滑动统计值（如滑动平均、累计分布、跨行对比 `LAG/LEAD`），极大简化了传统需要自连接（Self-join）的繁琐分析 SQL。
:::"""
    },
    3: {
        'title': '模式设计与范式理论',
        'en_title': 'Schema Design and Normalization',
        'tags': ['schema-design', 'functional-dependency', 'boyce-codd-normal-form', 'er-diagram'],
        'tldr': [
            '模式设计的核心目标是在消除数据冗余更新异常与维持高频读取性能之间取得系统工程平衡。',
            '函数依赖（Functional Dependency）定量描述属性间的决定关系，是评估模式规范化程度的数学依据。',
            '第一范式到 BCNF 逐步消除部分函数依赖与传递依赖，而反范式化（Denormalization）则是面向 OLAP 的工程妥协。',
        ],
        'insight': """::: insight 范式理论在现代硬件下的工程逆向
教科书普遍推崇将模式严格推导至 BCNF 或 3NF，但在实际的高并发 OLTP 和实时分析系统中，极度规范化的表结构意味着极高昂的跨表 JOIN 开销。随着现代分布式数据库和列存系统的普及，“适度反范式化（允许局部冗余、宽表设计）”已成为提升吞吐的通行工程手段。关键在于：必须有机制保证冗余数据的一致性回写。
:::"""
    },
    4: {
        'title': '数据库内部架构与进程并发模型',
        'en_title': 'Database Architecture and Process Models',
        'tags': ['dbms-architecture', 'process-models', 'disk-memory-tension', 'memory-allocation'],
        'tldr': [
            '数据库内核由连接管理器、查询解析器、优化器、执行引擎、锁管理器与恢复子系统构成。',
            '进程模型经历了单进程单线程、每连接一进程（Process-per-connection）到多线程工作池架构的演进。',
            '内核系统设计始终受制于磁盘 I/O（高延迟、按块传输）与内存（低延迟、按字节寻址）之间的物理性能张力。',
        ],
        'insight': """::: insight 为什么 DBMS 从不相信操作系统
数据库系统的设计哲学核心之一是“不信任 OS”。OS 的虚拟内存、统一页缓存（Page Cache）和调度器是为通用计算设计的，它们缺乏对查询语义、事务边界和 WAL 刷盘时序的理解。若直接依赖 `mmap`，操作系统可能在事务提交前将脏页偷换（Steal）到磁盘，破坏 ACID；DBMS 必须自己实现缓冲池管理、页面锁定与直接 I/O（O_DIRECT）。
:::"""
    },
    5: {
        'title': '存储管理与页面物理布局',
        'en_title': 'Storage Management and Page Layout',
        'tags': ['slotted-pages', 'tuple-layout', 'storage-manager', 'direct-io'],
        'tldr': [
            '存储管理器负责将逻辑表和元组抽象映射到底层操作系统的定长页面（通常为 4KB~16KB）。',
            '插槽页（Slotted Page）架构通过页头槽目录数组支持变长元组的高效存储与原地移动更新。',
            '日志结构追加存储（Log-Structured）以顺序写提升写入吞吐，但牺牲了随机点查与需要后台合并压缩（Compaction）。',
        ],
        'insight': """::: insight Slotted Page 对变长元组的精巧抽象
插槽页（Slotted Page）是现代行存数据库的标配。它的精妙之处在于插槽目录从页面起始处向前生长，而实际 Tuple 数据从页面末尾向后生长，二者在中间汇合。外部通过 `(PageID, SlotID)` 构成的 RID 寻址。即便 Tuple 因为定长字段修改而在页内发生移动，只需调整页头 Slot 的偏移量，外部索引指向的 RID 永不失效，彻底解耦了索引与物理字节位置。
:::"""
    },
    6: {
        'title': '内存管理与缓冲池置换策略',
        'en_title': 'Memory Management and Buffer Pool',
        'tags': ['buffer-pool', 'replacement-policy', 'clock-sweep', 'dirty-page-flushing'],
        'tldr': [
            '缓冲池（Buffer Pool）是数据库在内存中开辟的定长帧（Frame）数组，缓存磁盘高频页面。',
            '页表（Page Table）记录内存帧与磁盘页面 ID 的实时映射，页钉（Pin/Pin Count）防止活跃页面被换出。',
            '页面置换算法从经典 LRU 演化为时钟算法（Clock Sweep）与 LRU-K，有效免疫大规模全表扫描的缓存污染。',
        ],
        'insight': """::: insight 缓冲池锁（Latch）与事务锁（Lock）的本质区别
技术读者必须严格区分 Latch 与 Lock。Lock 是事务维度的概念，保护的是逻辑数据项（行、表、范围），生命周期长达整个事务期间，由锁管理器维护并记录在等待图里检测死锁。而 Latch 是线程维度的底层轻量级同步原语（互斥体/读写锁），保护的是缓冲池内存帧中的物理数据结构，生命周期仅有几微秒，操作结束立即释放。
:::"""
    },
    7: {
        'title': '索引机制与访问路径',
        'en_title': 'Indexes and Access Methods',
        'tags': ['b-plus-tree', 'hash-index', 'clustered-index', 'access-methods'],
        'tldr': [
            '索引通过牺牲额外存储空间与写入开销，将无序表扫描的线性复杂度降为点查与范围查的对数复杂度。',
            'B+ Tree 凭借超高分支因子（Fan-out）、极低树高与叶子节点双向链表，成为外存通用索引无可争议的标准。',
            '聚集索引（Clustered Index）决定数据的物理存放顺序，覆盖索引（Covering Index）完全消除回表开销。',
        ],
        'insight': """::: insight 为什么外存索引选 B+ Tree 而不是二叉平衡树
二叉搜索树（红黑树、AVL 树）每个节点仅保存一个键和两个指针，分支因子只有 2，树高度为 $\log_2 N$。存储千万级记录时树高可达 25 层，意味着一次点查需要 25 次随机 I/O，在外存上是灾难。B+ Tree 将分支因子扩展至页面容量（如 4KB 页面可容纳 100~200 个键），树高骤降到 3~4 层，前两层常驻内存，磁盘点查仅需 1~2 次 I/O，且叶子链表完美支持范围扫描。
:::"""
    },
    8: {
        'title': '连接算法与物理算子',
        'en_title': 'Join Algorithms',
        'tags': ['nested-loop-join, hash-join, sort-merge-join, operator-execution'],
        'tldr': [
            '连接操作（Join）是关系型系统中最耗时且最具算法挑战性的二元物理算子。',
            '嵌套循环连接（Nested Loop）包含简单嵌套、基于块的优化（BNL）与利用内表索引的 INLJ。',
            '散列连接（Grace Hash Join）通过分区与哈希探测处理超大表等值关联，排序合并连接（Sort-Merge）适用于预排序数据。',
        ],
        'insight': """::: insight 连接算法选型的内存边界法则
在进行两表连接时，如果一侧表在过滤后尺寸极小能够完全装入内存缓冲池，单阶段 Hash Join 是最优选择，只需 $O(M+N)$ I/O。但若两侧表均大幅超过可用内存，必须退化为分阶段外存 Hash Join（Grace Hash Join）或外部归并排序连接。优化器的最关键任务就是准确估计输入流的行数，避免将大表误判为驱动表导致内存溢出。
:::"""
    },
    9: {
        'title': '查询执行引擎与向量化处理',
        'en_title': 'Query Execution and Vectorization',
        'tags': ['volcano-iterator', 'vectorized-execution', 'compilation-engine', 'push-vs-pull'],
        'tldr': [
            '经典火山模型（Volcano Iterator）基于 Pull 模式与 `next()` 接口解耦算子，但虚函数调用与解释开销巨大。',
            '向量化执行（Block/Batch Processing）单次传递数据块（如 1024 行），极大发挥 CPU L1/L2 缓存与 SIMD 指令集优势。',
            '代码生成引擎（JIT / LLVM）通过动态编译将整个查询树内联压平为紧凑循环，消除所有中间解释层。',
        ],
        'insight': """::: insight 内存墙时代下算子执行模型的进化
在磁盘时代，I/O 是绝对瓶颈，火山模型每行一次虚拟调用的 CPU 开销无足轻重。但在全内存与高速 NVMe 时代，“内存墙（Memory Wall）”凸显，CPU 指令周期与分支预测失败率成为新瓶颈。向量化（Vectorwise 模式）和动态代码生成（Hyper 编译模式）是现代数据库执行引擎的两大主流巅峰，前者优化了指令级并行与跨平台灵活性，后者压榨了寄存器与内存局部性的极致性能。
:::"""
    },
    10: {
        'title': '查询优化器：规则推导与代价模型',
        'en_title': 'Query Optimization and Cost Models',
        'tags': ['query-optimizer', 'join-ordering', 'selinger-algorithm', 'cost-estimation'],
        'tldr': [
            '查询优化器是关系型系统最复杂的软件组件，负责在庞大的等价逻辑计划空间中寻找代价最低的物理执行计划。',
            '基于规则的优化（RBO）利用关系代数等价公理进行确定性启发式重写（如谓词下推、投影剪枝）。',
            '基于代价的优化（CBO）利用统计信息与动态规划（System-R / Selinger 算法）解决多表连接顺序爆炸难题。',
        ],
        'insight': """::: insight 优化器中的“测不准原理”
查询优化器绝非全知全能的数学神祇。它的致命弱点在于基数估计（Cardinality Estimation）的误差传播。由于多列之间普遍存在真实世界的数据相关性（如“车型=保时捷”与“价格>100万”），经典独立性假设（Attribute Value Independence）会导致连接基数估计出现几个数量级的偏差。代价模型在错误的基数输入下，极易选出一个极慢的笛卡尔积式计划。
:::"""
    },
    11: {
        'title': '分析型数据库：列式存储与轻量级压缩',
        'en_title': 'Column Stores and Database Compression',
        'tags': ['columnar-storage', 'run-length-encoding', 'dictionary-compression', 'c-store'],
        'tldr': [
            '分析型负载（OLAP）通常只访问宽表的少数几列但需全表聚合扫描，行存架构造成极大的无用 I/O 浪费。',
            '列式存储（C-Store / Parquet）将同列数据连续存放，极大提升了压缩比与矢量化扫描效率。',
            '轻量级压缩技术（RLE 游程编码、字典编码、Bit-packing）允许算子直接在压缩数据上执行谓词过滤。',
        ],
        'insight': """::: insight 延迟物化（Late Materialization）的高效秘密
列存系统最核心的性能技巧之一是延迟物化。传统的做法是在扫描完单列后立即将整行数据拼接（物化）出来传递给下游；而高级列存优化引擎在整个过滤、聚合甚至 Join 阶段始终传递虚拟列向量与位置位图（Bitmaps），只有在最终向客户端返回字段的最后一刻才进行跨列物化拼装，避免了成百万次无意义的内存复制。
:::"""
    },
    12: {
        'title': '事务处理与并发控制：冲突可串行化与两阶段锁',
        'en_title': 'Transactions and Two-Phase Locking',
        'tags': ['serializability', 'conflict-serializability', 'two-phase-locking', 'deadlock-detection'],
        'tldr': [
            '事务通过 ACID 四大属性为并发数据修改提供了不可分割与系统一致性的安全语义保证。',
            '冲突可串行化（Conflict Serializability）利用优先图（Precedence Graph）无环判定并发调度的正确性。',
            '严格两阶段锁（Strict 2PL）分为增长阶段（加锁）与收缩阶段（提交时统一释放），杜绝级联回滚。',
        ],
        'insight': """::: insight 2PL 的保守性与死锁的必然代价
两阶段锁（2PL）是一种悲观并发控制协议。它保证了可串行化调度，但也必然带来死锁（Deadlock）的风险。死锁并非系统的 Bug，而是互斥锁依赖环在资源争抢时的自然数学结果。DBMS 必须配备死锁检测（有向图周期检测算法）或死锁预防策略（Wait-Die / Wound-Wait 基于事务时间戳的主动抢占）。
:::"""
    },
    13: {
        'title': '乐观并发控制与多版本并发控制',
        'en_title': 'OCC and Multi-Version Concurrency Control',
        'tags': ['optimistic-concurrency-control', 'multi-version-concurrency-control', 'snapshot-isolation', 'write-skew'],
        'tldr': [
            '乐观并发控制（OCC）适用于低冲突负载，分为读取阶段、验证阶段（Validation Phase）与写入阶段。',
            '多版本并发控制（MVCC）通过保留数据元组的多历史版本，实现“读写互不阻塞，读不加锁”。',
            '快照隔离级别（Snapshot Isolation）消除了脏读、不可重复读与幻读，但面临写倾斜（Write Skew）异常。',
        ],
        'insight': """::: insight 快照隔离下的写倾斜（Write Skew）反直觉陷阱
快照隔离虽然在绝大多数场景下表现得像串行化，但无法完全消除写倾斜。经典案例是“两名医生值班，要求至少一人在岗”。两名医生并发发起请假事务，均在各自快照中读到“当前有两人在岗，满足条件”，随后各自将自己的状态更新为休假并提交。最终系统变成零人值班！解决办法是显式加共享写锁（`SELECT FOR UPDATE`）或引入依赖声明。
:::"""
    },
    14: {
        'title': '故障恢复与 ARIES 算法',
        'en_title': 'Crash Recovery and ARIES',
        'tags': ['write-ahead-logging', 'aries-recovery', 'compensation-log-record', 'checkpointing'],
        'tldr': [
            '故障恢复子系统确保在系统突然断电或进程崩溃重启后，已提交事务不丢（持久性）且未提交事务彻底回滚（原子性）。',
            '预写日志规则（WAL）：任何脏页刷盘前，其对应的日志记录必须先行持久化至稳定存储。',
            'ARIES 经典三阶段恢复算法：分析阶段确定崩溃时活跃事务、重做阶段（Redo）恢复系统状态、撤销阶段（Undo）回滚未提交修改。',
        ],
        'insight': """::: insight 补偿日志（CLR）与幂等恢复
ARIES 算法中最天才的设计是补偿日志记录（Compensation Log Record, CLR）。当系统在崩溃恢复的 Undo 阶段执行回滚操作时，如果恢复过程再次发生崩溃，没有 CLR 的系统可能会重复执行回滚导致数据被双重破坏。CLR 记录了 Undo 操作本身，并在页头更新 PageLSN。任何重做或撤销操作均是严格幂等的，保证系统无论在恢复的哪一毫秒再次断电都能最终收敛到正确状态。
:::"""
    },
    15: {
        'title': '并行与分布式数据库架构',
        'en_title': 'Parallel and Distributed DBMS',
        'tags': ['shared-nothing', 'data-partitioning', 'mpp-query-processing', 'pipeline-parallelism'],
        'tldr': [
            '现代大规模数据库系统从单机纵向扩展走向无共享架构（Shared-Nothing）的横向集群扩展。',
            '数据分区策略（轮转分区、范围分区、哈希分区）权衡了负载均衡度、数据倾斜风险与谓词下推能力。',
            'MPP 大规模并行处理框架通过 Exchange 算子与分布式 Hash 连接，跨集群节点并行化执行复杂 SQL。',
        ],
        'insight': """::: insight Exchange 算子的优雅解耦
Volcano 论文中由 Goetz Graefe 提出的 Exchange 算子是并行查询处理的基石。在没有 Exchange 之前，算子必须关心自己是在本地线程还是跨网络节点运行。Exchange 算子伪装成普通迭代器，内部封装了网络缓冲区、线程池与哈希重分布逻辑。上下游算子无需更改一行代码，即可无缝从单机执行平滑升级为数百台机器协同的分布式并行查询。
:::"""
    },
    16: {
        'title': '分布式事务：两阶段提交、Paxos 与 CAP 权衡',
        'en_title': 'Distributed Transactions and Two-Phase Commit',
        'tags': ['two-phase-commit', 'distributed-transactions', 'atomic-broadcast', 'paxos-consensus'],
        'tldr': [
            '分布式环境下的事务涉及跨多个物理节点的原子提交，任一节点失败均要求全局原子中止。',
            '两阶段提交协议（2PC）通过准备（Prepare）与提交（Commit）两轮消息达成一致，但存在协调者单点阻塞缺陷。',
            '基于 Paxos / Raft 共识复制的现代分布式事务协议，实现了非阻塞的高可用原子广播与自动故障恢复。',
        ],
        'insight': """::: insight 2PC 与 Paxos 的黄金组合
许多人容易混淆 2PC 与 Paxos 的职责。2PC 解决的是“原子提交（Atomic Commit）”——各节点管理不同的数据分区，只要有一处违背完整性就必须全滚；Paxos 解决的是“共识（Consensus）”——所有节点保存同一份数据的副本，只要多数派活着就能前进。现代分布式数据库（如 Google Spanner、TiDB）的最佳实践是：底层多副本用 Paxos 保障单组高可用，上层跨分片事务用 2PC 保证全局原子性。
:::"""
    },
    17: {
        'title': '最终一致性与向量数据库检索',
        'en_title': 'Eventual Consistency and Vector Databases',
        'tags': ['eventual-consistency', 'dynamo-architecture', 'vector-search', 'embedding-index'],
        'tldr': [
            'NoSQL 与 Dynamo 架构打破严格强一致性，通过一致性哈希、矢量时钟与读取修复实现高可用最终一致性。',
            'AI 大模型时代催生了面向高维非结构化数据的专用向量数据库系统（Vector DB）。',
            '近似最近邻搜索（ANN）算法（如 HNSW 图索引、IVF-PQ 倒排量化）突破高维向量检索的维度灾难。',
        ],
        'insight': """::: insight 向量数据库是不是独立数据库品类？
近年来行业对向量数据库的形态有很大争论。专用向量数据库（如 Milvus, Pinecone）针对高维浮点数 SIMD 计算和图遍历做了极深特化；而传统关系数据库（如 PostgreSQL pgvector）则在成熟 ACID 和元数据混合过滤上有天然优势。未来真正的胜负手在于“混合搜索（Hybrid Search）”能力——即能否在同一个事务内同时优雅完成标量结构化过滤与高维语义向量相似度匹配。
:::"""
    },
    18: {
        'title': '大规模集群计算：MapReduce 与 Spark RDD',
        'en_title': 'Cluster Computing: MapReduce and Spark',
        'tags': ['mapreduce', 'spark-rdd', 'lineage-graph', 'distributed-shuffle'],
        'tldr': [
            '大规模离线数据批处理经历了从 Google MapReduce 两阶段文件落盘到 Spark 全内存计算的架构飞跃。',
            '弹性分布式数据集（RDD）通过只读分区的血统图谱（Lineage Graph）实现无需物化全量检查点的轻量级容错。',
            '宽依赖与窄依赖的划分决定了集群网络洗牌（Shuffle）的开销边界与并行执行阶段（Stages）的划分。',
        ],
        'insight': """::: insight Lineage 粗粒度容错对细粒度日志的超越
传统分布式系统依靠频繁刷盘或在内存中记录每条更新日志来实现容错。Spark RDD 最核心的洞察在于：它放弃了细粒度状态更新，仅支持粗粒度转换操作（Map, Filter, Join）。因此容错只需记录构建数据集的算子血统（Lineage）。当某个集群节点故障丢失分区时，只需沿图谱重新计算该分区，完全避免了分布式写入检查点的网络 I/O 拥塞。
:::"""
    },
    19: {
        'title': '高性能内存事务引擎：H-Store 与确定性调度',
        'en_title': 'High-Performance OLTP and Deterministic Scheduling',
        'tags': ['in-memory-db', 'h-store', 'deterministic-transactions', 'calvin-protocol'],
        'tldr': [
            'Stonebraker 等人指出传统数据库 80% 以上的 CPU 周期浪费在缓冲池查找、锁管理与恢复日志中。',
            '全内存事务引擎（H-Store / VoltDB）通过消除缓冲池并为每个 CPU 核心独占分区，实现单线程极速运行。',
            '确定性事务调度协议（Calvin）在执行前通过全局定序层锁定读写集，彻底消除了分布式 2PC 的阻塞延迟。',
        ],
        'insight': """::: insight 消除锁管理的激进方案：单线程分区独占
传统数据库认为并发越高越好，但为了支撑并发，需要层层加锁、维护复杂的哈希锁表和死锁检测，反而吃掉了大部分 CPU。H-Store 采取了一种极致方案：将数据严格切分给 CPU 核心，每个核心单线程顺序执行存储过程，内部完全不加任何锁，也不支持交互式 SQL。对于纯局部事务，其吞吐能高出传统系统一到两个数量级。
:::"""
    },
    20: {
        'title': '云原生数据仓库：Snowflake 存算分离架构',
        'en_title': 'Cloud Data Warehouse: Snowflake Architecture',
        'tags': ['snowflake', 'storage-compute-separation', 'virtual-warehouses', 'micro-partitions'],
        'tldr': [
            '云原生数据库彻底颠覆了无共享架构（Shared-Nothing），确立了计算与存储完全解耦的三层设计模式。',
            '底层利用高吞吐低成本云对象存储（S3/GCS）作为持久化单一真理源，中间层弹性编排无状态虚拟仓库。',
            '元数据与全局目录服务统一协调并发事务、微分区（Micro-partitions）列存修剪与安全时间旅行（Time Travel）。',
        ],
        'insight': """::: insight 存算分离如何改变数据工程商业模型
在传统 Shared-Nothing 时代，扩容算力必须连带购买硬盘；扩容存储又必须连带购买服务器，且节点重平衡（Rebalance）动辄搬迁数十 TB 数据。Snowflake 的突破性在于：存储层有弹性，计算层随时秒级创建和销毁。数据分析师跑大型报表只需启动 10 分钟超大虚拟仓库，跑完立即释放，实现了技术架构与商业计费颗粒度的完美对齐。
:::"""
    },
    21: {
        'title': '高级基数估计与概率概要算法',
        'en_title': 'Advanced Cardinality Estimation and Sketches',
        'tags': ['cardinality-estimation', 'hyperloglog', 'count-min-sketch', 'histogram-statistics'],
        'tldr': [
            '基数估计（Cardinality Estimation）是查询优化器选择最佳连接顺序与物理算子的核心生命线。',
            '单列与多列数据分布统计依赖等宽直方图、等深直方图（Equi-depth）及前缀重度采样。',
            '概率概要算法（HyperLogLog 估计去重基数、Count-Min Sketch 统计频次、Bloom Filter 判定成员）以极小内存逼近精确结果。',
        ],
        'insight': """::: insight 概率数据结构对内存与精度的优雅折中
当面对万亿级数据流时，如果要求 100% 精确的 `COUNT(DISTINCT user_id)`，必须建立巨大的哈希表或排序，内存开销高达数十 GB。而 HyperLogLog 利用伯努利试验中随机哈希值前导零个数的概率分布，仅需 1.5KB 内存即可将十亿级基数的误差控制在 1% 以内。现代大数据与实时 OLAP 系统的基石正是建立在对这种“容忍受控误差”的数学妥协之上。
:::"""
    }
}

def clean_body_text(raw_text):
    # Strip existing top heading and source quote
    lines = raw_text.split('\n')
    idx = 0
    # skip frontmatter if any
    if len(lines) > 0 and lines[0].strip() == '---':
        idx = 1
        while idx < len(lines) and lines[idx].strip() != '---':
            idx += 1
        idx += 1 # skip closing ---
        
    while idx < len(lines) and (lines[idx].startswith('# ') or lines[idx].startswith('>') or lines[idx].strip() == ''):
        idx += 1
        
    remaining = '\n'.join(lines[idx:]).strip()

    # Remove repeated old TLDR if any
    remaining = re.sub(r'^##\s+TL;DR[\s\S]*?(?=\n##|\Z)', '', remaining, flags=re.M).strip()
    
    # Replace plain code blocks without language
    def replace_fence(m):
        if not m.group(1):
            return f"```text\n{m.group(2)}```"
        return m.group(0)

    remaining = re.sub(r'```([a-zA-Z0-9_-]*)\n([\s\S]*?)```', replace_fence, remaining)
    
    # Fix multiple blank lines
    remaining = re.sub(r'\n{3,}', '\n\n', remaining)
    return remaining

def main():
    print('Starting 6.5830 Database System refactoring...')
    os.makedirs(os.path.join(REPO_DIR, 'concept'), exist_ok=True)
    os.makedirs(os.path.join(REPO_DIR, 'project'), exist_ok=True)

    # 1. Process concept/b_tree_storage_engine.md from ext/b-tree.md
    btree_src = os.path.join(EXT_DIR, 'b-tree.md')
    if os.path.exists(btree_src):
        b_content = open(btree_src, 'r', encoding='utf-8').read()
        b_body = clean_body_text(b_content)
        b_md = f"""---
title: B-Tree 存储引擎与外存访问模型
type: concept
tags: [b-tree, disk-storage, solid-state-drive, block-io]
status: complete
---

# B-Tree 存储引擎与外存访问模型（B-Tree Storage Engines）

> MIT 6.5830 · 核心存储结构专题 · 概念解析  
> 核心参考：Alex Petrov *Database Internals* 第 2 章

## TL;DR

- 二叉搜索树由于分支因子仅为 2，外存树高过大且缺乏空间局部性，不适合作为磁盘驻留数据结构。
- 旋转机械硬盘（HDD）的高寻道成本决定了按块连续顺序 I/O 的绝对优势。
- 固态硬盘（SSD）以页为单位读写、以块为单位擦除，闪存转换层（FTL）负责垃圾回收与地址重映射。
- B-Tree 通过匹配磁盘块大小的高分支因子（100~200）将树高压缩至 3~4 层，实现对数级极少磁盘访问。

## 架构演进与核心洞察

::: insight 为什么现代外存依然由 B-Tree 统领
尽管 LSM-Tree 在高频写入场景声势浩大，但在绝大多数读多写少、严苛点查与范围查询的通用关系数据库中，B+ Tree 依然是王者。B+ Tree 的叶子节点双向链表和对页缓存的天然亲和性，使得它无论在机械磁盘时代还是在超高速 NVMe SSD 时代，都能以极小的内部碎片提供稳定、可预测且极低的 P99 读延迟。
:::

## 核心机制与技术实现

{b_body}
"""
        with open(os.path.join(REPO_DIR, 'concept/b_tree_storage_engine.md'), 'w', encoding='utf-8') as f:
            f.write(b_md)
        print('Created concept/b_tree_storage_engine.md')

    # 2. Extract GoDB Lab Guide from repo/index.md into project/godb_lab_guide.md
    raw_repo_index = open(os.path.join(REPO_DIR, 'index.md'), 'r', encoding='utf-8').read()
    lab_match = re.search(r'### 实验\s*\n+([\s\S]*?)(?=\n##\s+相关课程|\n##\s+本讲导览|\Z)', raw_repo_index)
    lab_body = lab_match.group(1).strip() if lab_match else ''
    
    godb_md = f"""---
title: GoDB 数据库内核实验全通关指南
type: project
tags: [godb, lab-assignment, buffer-pool-lab, query-engine-lab]
status: complete
---

# GoDB 数据库内核实验全通关指南（GoDB Architecture and Lab Guide）

> MIT 6.5830 / 6.5831 · Course Projects & Labs  
> 官方实验代码库：MIT DSG GoDB (Go 语言编写的高性能教学关系数据库系统)

## TL;DR

- GoDB 是 MIT 6.5830 专用的教学关系数据库，使用 Go 语言自底向上构建完整内核。
- Lab 1 实现堆文件（HeapFile）、元组（Tuple）序列化与基于时钟算法的缓冲池（BufferPool）。
- Lab 2 实现基础查询算子（Filter、Project、Join、Aggregate）的火山迭代器模型。
- Lab 3 实现事务管理、严格两阶段锁（Strict 2PL）并发控制与基于 WAL 日志的 ARIES 恢复。

## 实验反思与架构洞察

::: insight 亲手手写数据库内核的认知质变
只阅读教科书中的“页表”、“缓冲池”和“2PL”很难理解并发死锁与内存脏页的凶险。在 GoDB 实验中，每一个学生必须用 Go 语言亲手实现一个支持多并发线程读写的 `BufferPool`，并处理由于锁获取顺序颠倒导致的 Channel 阻塞。只有在经历过 Lab 3 崩溃恢复测试中日志 LSN 对不齐的绝望之后，才能真正敬畏数据库 ACID 的工程价值。
:::

## 一、GoDB 体系架构总览

GoDB 完整实现了经典关系数据库从 SQL 解析到磁盘文件管理的端到端链路：

1. **存储层（Lab 1）**：包含 `HeapFile`、`HeapPage` 和 `BufferPool`，负责管理定长与变长元组的物理打包与脏页同步。
2. **执行引擎（Lab 2）**：基于火山模型迭代器（`Iterator`），包含 `Filter`、`Project`、`Join`（Nested Loops 与 Hash Join）和 `Aggregate`。
3. **事务与恢复（Lab 3）**：实现事务隔离的锁管理器（`LockManager`）、事务原子回滚与基于 WAL 的 Redo/Undo 恢复。
4. **索引与优化（Lab 4 / 选做）**：实现外存 B+ 树索引结构与基于 Selinger 算法的动态规划连接顺序优化。

---

{clean_body_text(lab_body)}
"""
    with open(os.path.join(REPO_DIR, 'project/godb_lab_guide.md'), 'w', encoding='utf-8') as f:
        f.write(godb_md)
    print('Created project/godb_lab_guide.md')

    # 3. Process Lectures lec1.md ~ lec21.md
    for num in range(1, 22):
        spec = SPECS[num]
        dest_path = os.path.join(REPO_DIR, f'lec{num}.md')
        
        # Decide content source
        src_path = ''
        if num == 2: # from ext/lec2.md
            src_path = os.path.join(EXT_DIR, 'lec2.md')
        elif num == 16: # from ext/lec16.md
            src_path = os.path.join(EXT_DIR, 'lec16.md')
        elif num == 21: # from ext/lec21.md
            src_path = os.path.join(EXT_DIR, 'lec21.md')
        elif os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
            src_path = dest_path
        else:
            # Check external
            candidate = os.path.join(EXT_DIR, f'lec{num}.md')
            if os.path.exists(candidate):
                src_path = candidate
            else:
                src_path = dest_path
                
        raw_text = open(src_path, 'r', encoding='utf-8').read() if os.path.exists(src_path) else ''
        body = clean_body_text(raw_text)
        
        # If lec15, merge 17MPP.md if available
        if num == 15:
            mpp_path = os.path.join(EXT_DIR, '17MPP.md')
            if os.path.exists(mpp_path):
                mpp_txt = clean_body_text(open(mpp_path, 'r', encoding='utf-8').read())
                body += "\n\n## 补充专题：大规模并行处理（MPP）与查询执行\n\n" + mpp_txt
                
        # If lec4, merge ext/lec4.md if repo had less
        if num == 4:
            ext_l4 = os.path.join(EXT_DIR, 'lec4.md')
            if os.path.exists(ext_l4):
                ext_l4_txt = clean_body_text(open(ext_l4, 'r', encoding='utf-8').read())
                if len(ext_l4_txt) > len(body):
                    body = ext_l4_txt
                    
        # If lec21, complete sketch content
        if num == 21:
            body = re.sub(r'----\s*\n+后面[\s\S]*$', '', body).strip()
            body += """

## 二、概率数据结构与核心概要算法（Sketches）

在大规模海量数据流分析中，精确统计不仅耗时巨大，而且会消耗不可接受的内存。现代查询优化与实时 OLAP 广泛采用概率数据结构进行快速近似估算：

### 1. 直方图技术（Histograms）
- **等宽直方图（Equi-width）**：将数据值域切分为固定宽度的桶，各桶内频次可能极度不均，在数据倾斜时估算失真。
- **等深直方图（Equi-depth）**：每个桶容纳相同数量的元组，动态调整区间边界，极大提升了对偏斜分布的预测精度。

### 2. HyperLogLog (HLL)——去重基数估计
- **核心思想**：通过均匀哈希函数将输入映射为二进制串，利用哈希值前缀连续出现 0 的最大长度（$k$）作为几何分布估计：$N \approx 2^k$。
- **分桶调和平均**：将前 $m$ 位划分为 $2^m$ 个桶，各桶独立观测并计算调和平均数，消除极端值波动，以仅 1.5KB 内存实现 $1\%$ 误差率。

### 3. Count-Min Sketch——高频项与频次估计
- **核心思想**：由深度为 $d$、宽度为 $w$ 的二维计数器矩阵与 $d$ 个独立哈希函数构成。
- **查询规则**：对于查询键 $x$，取各哈希槽计数的最小值：$\\hat{f}(x) = \\min_{1 \\le i \\le d} C[i, h_i(x)]$。天然满足保守估计（只可能多估，绝不低估）。

### 4. 布隆过滤器（Bloom Filter）——集合成员高效判定
- **核心机制**：通过 $k$ 个哈希函数映射到位图数组。若任一位为 0 则**绝对不存在**；若全为 1 则**大概率存在**（存在可控假阳性 False Positive，无假阴性）。常用于下推至存储层过滤无效磁盘读。
"""

        fm_title = spec['title']
        tags_str = ', '.join(spec['tags'])
        tldr_bullets = '\n'.join([f'- {b}' for b in spec['tldr']])
        h1_line = f"# Lec {num} {spec['title']}（{spec['en_title']}）"
        insight_block = spec['insight']
        
        new_lec_content = f"""---
title: '{fm_title}'
type: lecture
lecture: {num}
tags: [{tags_str}]
status: complete
source: 'https://dsg.csail.mit.edu/6.5830/'
---

{h1_line}

> MIT 6.5830 / 6.5831 · Database Systems · 第 {num} 讲  
> 核心教材：*Readings in Database Systems* (5th Edition, Red Book)  
> 配套实验：GoDB (Go-based Database Engine)

## TL;DR

{tldr_bullets}

## 架构演进与核心洞察

{insight_block}

## 核心机制与讲义正文

{body}
"""
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(new_lec_content)
        print(f'Standardized {dest_path}')

    # 4. Generate clean, compliant index.md
    index_path = os.path.join(REPO_DIR, 'index.md')
    index_content = """---
title: '6.5830 数据库系统 (Database Systems)'
type: course
course: '6.5830 数据库系统 (Database Systems)'
course_id: '6.5830'
tags: [relational-database, query-optimizer, transaction-processing, distributed-database]
status: complete
source: 'https://dsg.csail.mit.edu/6.5830/'
---

# 6.5830 数据库系统 (Database Systems)

> MIT CSAIL · Course 6: Computer Science · 课号 6.5830 / 6.5831  
> 授课教授：Prof. Sam Madden, Prof. Michael Stonebraker  
> 经典参考书：*Readings in Database Systems* (5th Edition, 数据库红宝书)

## TL;DR

- 数据库系统是现代数据密集型应用的核心基石，全面贯穿关系模型、存储引擎、查询编译与分布式事务。
- 从单机外存模型（B+ Tree、缓冲池置换、列存压缩）到查询优化器（Selinger 算法与代价模型）的物理执行全貌。
- 深入并发控制与恢复理论（严格 2PL、MVCC、ARIES 算法），并延展至现代分布式数据库与云原生存算分离架构。

## 一、课程先修与解锁路径（Curriculum Pathway）

为了帮助技术读者建立清晰的体系化学习旅程，建议参考以下知识拓扑：

```mermaid
graph TD
    subgraph "先修基础 (Prerequisites)"
        A["6.1210 算法导论<br/>(哈希表、树、排序)"] --> D["6.5830 数据库系统"]
        B["6.1910 计算机组成<br/>(内存层级、缓存、外存)"] --> D
        C["6.1810 操作系统<br/>(进程线程、页表、文件系统)"] --> D
    end

    subgraph "核心课程 (Core Database Systems)"
        D --> D1["存储与索引<br/>(Lec 1-7, B-Tree)"]
        D --> D2["执行与优化<br/>(Lec 8-11, Column-Store)"]
        D --> D3["事务与恢复<br/>(Lec 12-14, ARIES)"]
        D --> D4["分布式与云原生<br/>(Lec 15-21, Snowflake)"]
    end

    subgraph "进阶解锁 (Unlocked Courses & Systems)"
        D3 --> E["6.5840 分布式系统<br/>(Raft, Spanner, 2PC)"]
        D4 --> F["18-746 分布式存储系统"]
        D1 --> G["开源内核实战<br/>(PostgreSQL / Redis / RocksDB)"]
    end
```

---

## 二、课程讲义体系目录

全课程 21 讲结构化讲义涵盖数据库四大支柱模块：

| 讲次 | 讲义标题 | 英文主题 | 核心内容焦点 |
| :--- | :--- | :--- | :--- |
| [Lec 1](./lec1.md) | 关系模型与 SQL 基础 | Relational Model & SQL | 逻辑谓词模型、关系代数与数据独立性 |
| [Lec 2](./lec2.md) | 现代 SQL 与系统运维 | Modern SQL & Admin | 窗口函数、CTE、RBAC 与运维维护命令 |
| [Lec 3](./lec3.md) | 模式设计与范式理论 | Schema Normalization | 函数依赖、BCNF 分解与反范式化权衡 |
| [Lec 4](./lec4.md) | 数据库内核整体架构 | DBMS Architecture | 磁盘与内存张力、进程并发模型与直接 I/O |
| [Lec 5](./lec5.md) | 存储管理与页面物理布局 | Storage & Page Layout | Slotted Page 结构、Tuple 打包与变长字段 |
| [Lec 6](./lec6.md) | 内存管理与缓冲池置换 | Buffer Pool Management | 缓冲池 Frame 架构、时钟算法与页钉机制 |
| [Lec 7](./lec7.md) | 索引机制与访问路径 | Indexes & Access Methods | B+ Tree 分支因子、哈希索引与覆盖索引 |
| [Lec 8](./lec8.md) | 连接算法与物理算子 | Join Algorithms | Nested Loop、Grace Hash Join 与 Sort-Merge |
| [Lec 9](./lec9.md) | 查询执行引擎与向量化 | Query Execution Engine | 火山模型迭代器、向量化执行与 JIT 代码生成 |
| [Lec 10](./lec10.md) | 查询优化器：规则与代价 | Query Optimization | 关系代数等价重写、Selinger 动态规划连接定序 |
| [Lec 11](./lec11.md) | 分析型数据库：列式存储 | Column Stores & C-Store | 列式物理布局、字典编码与延迟物化技术 |
| [Lec 12](./lec12.md) | 事务处理与两阶段锁 | Transactions & 2PL | 冲突可串行化、优先图判定与严格 2PL |
| [Lec 13](./lec13.md) | 乐观并发控制与快照隔离 | OCC & MVCC | 验证阶段时序、多版本时间戳与写倾斜分析 |
| [Lec 14](./lec14.md) | 故障恢复与 ARIES 算法 | Crash Recovery & ARIES | WAL 预写日志、Redo/Undo 幂等性与补偿日志 |
| [Lec 15](./lec15.md) | 并行与分布式数据库架构 | Parallel & Distributed DBMS | Shared-Nothing 架构、分片策略与 Exchange 算子 |
| [Lec 16](./lec16.md) | 分布式事务与两阶段提交 | Distributed 2PC & Paxos | 协调者阻塞、2PC 优化与 Paxos 强一致复制 |
| [Lec 17](./lec17.md) | 最终一致性与向量数据库 | Eventual Consistency & Vector | Dynamo 一致性哈希、矢量时钟与高维 ANN 搜索 |
| [Lec 18](./lec18.md) | 大规模集群计算：Spark | Cluster Computing: Spark | MapReduce 瓶颈、RDD 血统图与 Shuffle 阶段 |
| [Lec 19](./lec19.md) | 高性能内存事务引擎 | High-Performance OLTP | H-Store 单线程分区消除锁、Calvin 确定性协议 |
| [Lec 20](./lec20.md) | 云原生数据仓库：Snowflake | Cloud Data Warehouse | 存算完全分离、无状态计算池与微分区修剪 |
| [Lec 21](./lec21.md) | 高级基数估计与概率概要 | Cardinality & Sketches | 直方图、HyperLogLog、Count-Min 与布隆过滤器 |

---

## 三、核心概念专题与实验项目

- **[B-Tree 存储引擎与外存访问模型](./concept/b_tree_storage_engine.md)**：深入剖析磁盘/SSD 块设备物理特征与 B+ Tree 索引设计权衡。
- **[GoDB 数据库内核实验全通关指南](./project/godb_lab_guide.md)**：MIT 官方 Go 语言自研数据库实验架构、Lab 1~3 实现全解析与踩坑避错。

---

本资料整理自 MIT 6.5830 官方课程大纲与讲义，遵循 Creative Commons BY-NC-SA 4.0 许可协议。
"""
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    print('Cleaned and standardized index.md')

if __name__ == '__main__':
    main()
