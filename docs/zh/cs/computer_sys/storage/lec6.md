---
title: 文件系统缓存与一致性
type: lecture
lecture: 6
tags: [crash-consistency, fsck, soft-updates, metadata-integrity, file-system-cache]
status: complete
---
# Lec 6 文件系统缓存与一致性

## TL;DR

- **崩溃一致性难题（Crash Consistency Problem）**：一次逻辑文件修改（如文件创建或追加）涉及数据块、Inode 元数据与空闲位图等多块更新；若在落盘中途遭遇断电崩溃，系统将产生悬空指针、空间泄漏或文件交叉破坏等严重不一致状态。
- **事后扫描修复与 FSCK 局限**：传统文件系统检查器（FSCK）在系统重启后挂起并进行全局五阶段遍历修复；但其时间开销与物理磁盘容量成正比（$O(\text{Disk Size})$），在大规模现代存储设备上耗时达数小时甚至数天，破坏了系统可用性。
- **内存依赖编排与运行时验证**：CMU 提出的 Soft Updates 通过在内存中维护元数据更新依赖有向图与动态回滚，消除同步写的同时保证盘上结构永不破损；现代系统（如 Recon）进一步引入运行时事务不变量校验，在脏块触盘前主动阻断内核软件 Bug 带来的静默损坏。

## 阅读资料

- Ganger, Gregory R. and McKusick, Marshall Kirk and Soules, Craig A. N. and Patt, Yale N.
  [*Soft Updates: A Solution to the Metadata Update Problem in File Systems*](https://course.ece.cmu.edu/~ece746/papers//papers/Ganger_2000-Gregory_R._Ganger_and_Marshall_Kirk_McKusick_and_Craig_A._N._Soules_and_Yale_N._Patt-Soft_Updates:_A_Solution_to_the_Metadata_Update_Problem_in_File_Systems.pdf), In *ACM Transactions on Computer Systems (TOCS)*, May 2000, pages 127--153
- Giampaolo, Dominic
  [*Practical File System Design with the Be File System, Chapter 7*](https://course.ece.cmu.edu/~ece746/papers//textbook_chapters/Giampaolo-Practical_File_System_Design_with_the_Be_File_System_Chapter_7.pdf)
- Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau
  [*Operating Systems: Three Easy Pieces, Chapter 42: Crash Consistency: FSCK and Journaling*](http://pages.cs.wisc.edu/~remzi/OSTEP/file-journaling.pdf)
- Fryer, Daniel and Sun, Kuei and Mahmood, Rahat and Cheng, TingHao and Benjamin, Shaun and Goel, Ashvin and Brown, Angela Demke
  [*Recon: Verifying File System Consistency at Runtime*](https://course.ece.cmu.edu/~ece746/papers//papers/Fryer.pdf), In *Proceedings of the 10th USENIX Conference on File and Storage Technologies (FAST)*, 2012, pages 7--7

## 本讲定位

为了平摊极其昂贵的物理 I/O 延迟，现代操作系统内核无一例外地将文件系统读写置于内存页缓存（Page Cache）中异步执行。写系统调用执行后，脏页会在内存中滞留数秒乃至数十秒。

然而，这为系统引入了存储领域最棘手的核心挑战之一：**如果在脏页部分刷入磁盘的过程中机器突然断电或内核崩溃，磁盘上的文件系统结构将处于何种状态？系统能否安全恢复？** 本讲聚焦崩溃一致性难题，深入对比离线修复工具 FSCK、精巧的 Soft Updates 依赖机制以及现代运行时一致性守护框架 Recon。

## 崩溃一致性难题（The Crash Consistency Problem）

考虑向现有文件中追加一个 4KB 数据块的最简单场景。在磁盘底层，文件系统必须原子更新三个完全不连续的磁盘块：
1. **数据块 $D_b$**：存放新追加的用户真实数据；
2. **Inode 节点 $I_b$**：更新文件长度 `st_size`，并增加指向新数据块的指针；
3. **数据位图 $B_b$**：将对应物理数据块的分配标志位置为 1。

由于硬件控制器单次唯一保证原子的只有单个物理扇区的写操作，更新这三个跨越不同物理区域的块必然存在先后次序。若在写入间隙发生突然断电，系统将面临灾难性状态：
- **仅 $D_b$ 写入**：元数据全未更新，数据相当于从未写过。虽无数据错乱，但新写入的数据彻底丢失；
- **仅 $I_b$ 写入**：Inode 指向了一个未写入的新块（垃圾数据），更严重的是位图显示该块仍是空闲的！若后续其他进程创建新文件，系统会将该块分配给另一个 Inode，导致**两个完全不相干的文件指向同一块磁盘物理区域，产生致命的数据交叉覆盖**；
- **仅 $B_b$ 写入**：位图标记块已占用，但没有任何 Inode 引用它，造成永久性的**空间泄漏（Space Leak）**。

## 经典事后修复：FSCK 机制与可用性瓶颈

在日志技术普及之前，传统 UNIX 系统（如早期的 FFS）采用简单直接的策略：前台异步写，崩溃重启后依赖 **FSCK（File System Checker）** 进行离线遍历体检。

FSCK 在系统重启时挂起所有前台业务，执行严谨的五阶段全盘扫描：
1. **块与大小检查**：遍历所有 Inode，校验分配块数与文件大小是否一致，检查是否存在重复块引用；
2. **路径名检查**：扫描根目录开始的所有目录项，验证目录格式与 Inode 有效性；
3. **连接性检查**：检测孤立目录，将失去父节点的目录挂载至 `/lost+found`；
4. **引用计数检查**：重新统计全盘每个 Inode 的实际目录链接数，修复 Inode 中错误的 `i_nlink` 计数值；
5. **空闲图扫描**：根据前述扫描中实际被引用的所有块和 Inode，重新生成位图并覆盖磁盘上的脏位图。

### FSCK 的致命瓶颈

FSCK 能够有效修复大部分简单的结构断裂，但其时间复杂度与物理磁盘总容量成正比：

$$
T_{\text{fsck}} = O(\text{Total Disk Size})
$$

当磁盘从数十 MB 暴增至数 TB、数 PB 时，一次完整的 FSCK 扫描需要读取数以亿计的元数据扇区，耗时长达数小时乃至数天。在现代数据中心与企业级服务中，长达数小时的宕机停服是绝对不可接受的。存储系统迫切需要一种**与盘容量无关、在崩溃后毫秒级恢复一致性**的架构方案。

## 内存依赖图与有序更新：Soft Updates

为了彻底消除对耗时 FSCK 的依赖，同时避免传统同步写（Synchronous Write，即每次修改元数据都强制堵塞等待磁盘返回）带来的吞吐暴跌，Ganger、McKusick 与 Patt 等人提出了享誉学术界的 **Soft Updates（TOCS'00）**。

### 核心安全准则（Safety Invariants）

Soft Updates 发现，只要严格遵守以下三条基本定序准则，盘上的元数据在任何崩溃瞬间都不会损坏：
1. **永不指向未分配的资源**：必须先将新分配的数据块或 Inode 写入磁盘，然后才能写入指向该资源的指针；
2. **永不复用未擦除旧指针的资源**：必须先在磁盘上清除对旧资源的引用，然后才能将该资源重新分配给新文件；
3. **在资源复用前必须持久化新指针**：确保所有依赖关系单向有序推进。

### 依赖有向图与依赖回滚（Dependency Rollbacks）

然而，在操作系统页缓存中，一个 4KB 的物理块往往聚合了数十个文件的 Inode 或上千个目录项。这会导致**循环依赖（Cyclic Dependencies）**：
- 文件 A 的 Inode 依赖于目录块 D（必须先写 Inode 再写目录项）；
- 而目录块 D 中又恰好包含文件 B 的目录项，文件 B 的分配又反向依赖于目录块 D。

如果直接刷盘，系统将陷入死锁。Soft Updates 在内核内存中显式构建了一张精细的**有向依赖图（Dependency Graph）**：
1. 当一个脏块准备刷盘时，Soft Updates 检查该块内是否存在尚未完成前置依赖的未决修改（Pending Updates）；
2. **动态回滚（Rollback）**：Soft Updates 临时将内存中未就绪的字段修改回滚为旧的安全值，将处于合法一致状态的块安全刷入磁盘；
3. **前滚恢复（Rollforward）**：磁盘 I/O 确认完成后，Soft Updates 立即在内存中重新应用刚刚回滚的修改，等待其前置依赖就绪后进入下一次刷盘。

Soft Updates 允许系统以纯异步的速度写入磁盘，同时在数学上严格保证：无论何时拔掉电源，磁盘上的状态永远不会出现悬空指针或非法交叉，恢复时无需扫描全盘，仅需轻量回收极少数泄漏的孤儿块。然而，其代价是内核内部依赖图追踪极其复杂，逻辑边界繁重，后来逐步被更为通用、代码更易维护的**预写式日志（Journaling）**技术所取代。

## 运行时完整性守护：Recon 框架

无论是 FSCK 还是 Soft Updates，其模型都基于一个隐含假设：文件系统软件本身的内存操作是绝对正确的，损坏仅来源于“写入顺序被断电打断”。

然而，多伦多大学 Fryer 等人（FAST'12）的生产调研表明，**现代文件系统内核逻辑的软件 Bug、野指针与内存静默翻转，构成了实际运行中元数据崩溃损坏的首要来源**。

为此，**Recon（FAST'12）** 提出了基于事务一致性不变量的运行时验证体系：
1. **元数据变更为逻辑事务**：Recon 将所有文件系统修改操作包装为微型事务；
2. **磁盘提交屏障拦截**：在任何元数据脏块被驱动器发送给底层磁盘介质之前，Recon 拦截该 I/O 请求；
3. **不变量布尔求值**：利用专用校验核心快速验证形式化一致性不变量（如“每个被 Inode 引用的数据块在位图中必须且仅能被置位一次”、“目录树不存在孤立闭环”）；
4. **主动阻断写穿**：一旦检测到不变量违背，Recon 立即拦截该恶意写入并报警，阻止软件 Bug 污染不可逆的持久化磁盘介质，将单机崩溃防护从“事后被动修复”推进到了“事前主动阻断”。

## 我的理解

::: insight
**崩溃一致性是分布式事务与单机存储在微观世界的首次交汇**：
初看之下，崩溃一致性似乎只是单机文件系统在管理几块磁盘扇区时的工程细节；但深入其本质，它与分布式系统中的两阶段提交（2PC）和共识算法面对着完全相同的数学困难——**如何在不可靠、无原子多点写入保证的物理世界中，构建具备 ACID 语义的状态机**。
FSCK 相当于事后全量补偿回滚，Soft Updates 相当于用拓扑排序与悲观锁消解死锁，而后续将深入研读的 Journaling 则直接将数据库的 WAL 事务理念移植到了操作系统内核。理解了单机文件系统在这一问题上的惨烈探索，才能真正洞察现代大规模分布式存储系统在处理故障与状态恢复时的底色与灵感来源。
:::
