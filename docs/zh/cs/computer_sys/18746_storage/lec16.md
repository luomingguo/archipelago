---
title: LSM 树及其应用
type: lecture
lecture: 16
tags: [lsm-tree, sstable, compaction, bloom-filter, write-amplification]
status: complete
---
# Lec 16 LSM 树及其应用

## TL;DR

- **写入密集型存储范式转移**：针对传统 B 树在海量写场景下的随机寻道与页分裂瓶颈，LSM-Tree（日志结构合并树）将随机更新拦截在内存中完成有序化，转化为磁盘上的大批量顺序追加合并，实现吞吐量数量级提升。
- **分层解耦与滚动归并**：经典两组件架构通过内存组件 $C_0$ 缓冲写入，并利用后台滚动归并（Rolling Merge）连续下刷至磁盘驻留组件 $C_1$；现代系统演化为 Leveled/Tiered 多级 SSTable 结构，并配合布隆过滤器（Bloom Filter）将点查 I/O 压制至常数级。
- **前沿元数据系统落地**：CMU TableFS 将本地文件系统目录与 Inode 打包存入嵌入式 LSM 树，消除海量小文件随机读写；DeltaFS 则将 LSM 范式推广至百亿亿次（Exascale）超算分布式瞬态元数据管理。

## 阅读资料

- Patrick O'Neil, Edward O'Neil, Gerhard Weikum
  [*The Log-Structured Merge-Tree (LSM-Tree)*](https://www.cs.umb.edu/~poneil/lsmtree.pdf), Acta Informatica 33, 351–385 (1996)
- Kai Ren, Garth Gibson (CMU PDL)
  [*TABLEFS: Enhancing Metadata Efficiency in the Local File System*](https://course.ece.cmu.edu/~ece746/papers//papers/tablefs.pdf), USENIX ATC 2013
- Qing Zheng et al. (CMU PDL)
  [*DeltaFS: Exascale File Systems for Transient Datasets*](https://www.pdl.cmu.edu/PDL-FTP/Storage/ACMToS-0920.pdf), ACM Transactions on Storage, 2020

## 引入：B 树在写入密集型负载下的困局

在高性能联机事务处理（OLTP）和日志监控场景中，系统往往面临持续不断的高频写入。例如在标准的银行 TPC-A 基准测试中，每笔交易除了向账户表扣款外，还必须向历史审计表（History Table）追加一条流水记录，并为该流水建立复合索引（如基于 `Account-ID` 和时间戳 `Timestamp`）。

如果采用传统的 **B 树 / B+ 树** 组织磁盘索引，每一次新纪录插入都会遭遇严峻挑战：
1. **随机 I/O 惩罚**：由于新插入记录的索引键分布离散，系统必须将离散的叶子节点磁盘页从外存读入内存缓冲区；
2. **写放大与页分裂**：一旦目标叶子页存满，将触发级联节点分裂（Page Split），导致多次离散的脏页回写；
3. **“五分钟法则（Five Minute Rule）”失灵**：Gray 和 Putzolu 提出的经济学平衡点指出，如果一个磁盘页在一定周期（历史上约为 5 分钟，现代约为 60 秒）内无法被再次访问，将其长期驻留在昂贵的 DRAM 中是不经济的。对于拥有数亿条历史记录的大型索引，绝大多数叶子节点在内存缓冲区中的命中率无限趋近于零，导致几乎每次写操作都会转化为真实的物理磁盘寻道。

以 1000 TPS 的系统为例，维护一个 5.76 亿条记录的历史 B 树索引，每天将产生数千次物理磁盘 I/O，需要耗费数十乃至上百个机械磁盘臂（Disk Arms）才能满足吞吐需求。B 树在本质上是**读优化**的数据结构，它将就地更新（In-place Update）的昂贵代价完全推给了写入路径。

## 两组件 LSM-Tree 架构与滚动归并

针对这一物理矛盾，Patrick O'Neil 等人于 1996 年提出了 **Log-Structured Merge-Tree (LSM-Tree)**。其核心洞察是：**将对磁盘的细碎随机写入，推迟并在内存中缓冲排序，随后利用归并排序的思想，转化为对磁盘大块连续区域的顺序流式追加**。

### $C_0$ 与 $C_1$ 双组件模型

在最经典的二组件模型中，LSM 树由两个结构清晰的组件构成：
- **内存组件 $C_0$**：完全常驻于 DRAM 内存中的有序动态数据结构（通常采用红黑树、AVL 树或跳表 SkipList）。所有新到来的插入、更新和删除（写入墓碑标记）首先追加写入磁盘上的预写式日志（WAL）以保证故障持久性，随后直接在内存中的 $C_0$ 完成插入与排序，延迟仅为纳秒级；
- **磁盘驻留组件 $C_1$**：持久化保存在物理外存上的高效有序索引树（结构类似于连续排布的 100% 满填充 B 树）。$C_1$ 的节点大小通常设置为多页物理块（如 64KB 到数 MB），以充分榨取磁盘顺序流式传输的最高带宽。

### 滚动归并（Rolling Merge）过程

当内存中的 $C_0$ 组件达到预设的容量阈值时，系统触发后台清理流程，通过**滚动归并（Rolling Merge）**将数据迁移到磁盘驻留的 $C_1$ 组件：
1. **并发游标驱动**：滚动归并进程维护两个逻辑游标，分别指向 $C_0$ 树的最小节点和 $C_1$ 树的当前外存叶子节点；
2. **多路流式归并**：类似于经典外排归并排序，游标按升序遍历 $C_0$ 和 $C_1$。遇到相同的键时，用 $C_0$ 中的最新版本覆盖旧记录（若为墓碑则彻底清除）；
3. **批量顺序写出**：归并产生的新排序数据被连续组装并写入新分配的连续外存块，形成全新的 $C_1$ 节点，同时原子释放旧的 $C_1$ 节点空间。

通过这种设计，磁头在归并期间仅进行长距离的大块顺序读写，原本分散在全盘各处的数万次微小随机寻道被压缩为一次高效的批量流式 I/O。

## 现代多层 LSM 树扩展与读优化

随着数据规模暴增至 TB/PB 级别，单一的 $C_1$ 组件会导致归并周期过长。现代 LSM 树存储引擎（如 Google LevelDB、RocksDB、Cassandra）将其推广为**多层级结构（Multi-component / Leveled Hierarchy）**：

1. **MemTable 与 Immutable MemTable**：
   - 活跃写入进入内存 MemTable；
   - 饱和后冻结为只读的 Immutable MemTable，同时开辟新的 MemTable 接收写入，后台线程异步将 Immutable MemTable 顺序刷盘生成 Level 0 的不可变文件（Sorted String Table, SSTable）。
2. **SSTable 与两类 Compaction 策略**：
   - **Size-Tiered Compaction**：每一层包含多个大小相近的 SSTable。当某一层的文件数达到阈值，触发归并合并为一个更大的 SSTable 放入下一层。该策略写入放大（WAF）极低，适合写密集型高吞吐场景；
   - **Leveled Compaction**：除 Level 0 外，每一层内部的所有 SSTable 键范围严格互不重叠。当第 $L$ 层总容量超出上限时，选取一个 SSTable 与第 $L+1$ 层中有重叠键范围的所有 SSTable 归并。该策略空间放大极低，且能极好地限制点查延迟。
3. **读路径与布隆过滤器（Bloom Filter）**：
   - 读取操作必须自顶向下遍历：MemTable $\rightarrow$ Immutable MemTable $\rightarrow$ Level 0 $\rightarrow$ Level 1 $\dots$；
   - 为了避免在各层未命中 SSTable 上浪费随机 I/O，LSM 树为每个 SSTable 在内存中维护紧凑的**布隆过滤器（Bloom Filter）**。若布隆过滤器判定目标键不存在，则 100% 确认无需读取该磁盘块，从而将单次点查的物理 I/O 次数严格压制在常数级别（通常 $\le 1$ 次）。

## 真实系统应用案例：TableFS 与 DeltaFS

LSM 树的高吞吐追加特性不仅革新了数据库存储引擎，更深刻重塑了现代文件系统的元数据架构。

### TableFS：化解本地文件系统小文件元数据风暴

在海量微小文件（如小图片、源文件）场景下，传统本地文件系统（ext4、XFS）因频繁的 Inode 寻道和目录项锁竞争出现吞吐断崖。CMU Parallel Data Lab 提出的 **TableFS（USENIX ATC'13）** 给出了激进解法：
- 将传统文件系统底层的目录项数组和 Inode 树完全抛弃，转而在上层嵌入一个经过定制的 LevelDB 引擎；
- 目录结构被扁平化编码为键值对：Key 为 `(parent_inode_id, filename)`，Value 为紧凑序列化的 Inode 属性元数据；
- 小于阈值（如 4KB）的小文件数据直接作为 Value 与元数据一起内联存入 LSM 树，大文件数据则以对象形式存储在底层简单对象库中；
- 借助 LSM 树对小键值的极致写入合并，TableFS 在保持完整 POSIX 目录语义的同时，将文件创建与目录遍历速度提升了 2 到 10 倍。

### DeltaFS：超算万亿级瞬态数据的极速吸收

在百亿亿次（Exascale）高性能计算（HPC）模拟中，数万个计算节点可能在几毫秒内同时向文件系统倾倒海量中间检查点文件。传统集中式元数据服务器会瞬间崩溃。CMU 与 LANL 合作研发的 **DeltaFS（ACM ToS'20）** 将 LSM 树去中心化分布至所有计算节点：
- 在每个计算节点的本地节点存储中嵌入瞬态 LSM 树；
- 计算节点向本地 LSM 树无锁极速写入元数据与检查点小文件，彻底消除中心化网络锁与目录协调；
- 模拟结束后，各节点后台流式归并（Merge）并将全局元数据有序推向并行底层持久存储，支撑起了万亿级文件的瞬时高通量产生。

## 我的理解

::: insight
**LSM 树展示了存储系统设计中“用时间换空间、用批量换吞吐”的最优工程解**：
计算机系统的物理定律决定了：在任何介质上，顺序写入的带宽始终远超随机写入。B 树为了维护完美的读局部性与原地检索树形结构，在写入时付出了极其惨重的随机 I/O 代价。
LSM 树的伟大之处在于它彻底放弃了“原地维护完美结构”的执念。它承认写入瞬间的结构不完美，允许数据在内存中先沉淀，通过后置异步的归并排序逐步清理熵增。这种“Append-Only + 后台 Compaction”的架构范式，不仅完美契合了机械硬盘减少磁臂移动的物理天性，更与现代 NAND 闪存“写前必擦、顺序写入寿命最高”的底层契约产生了跨时代的深刻共鸣。
:::
