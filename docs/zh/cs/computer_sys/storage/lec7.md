---
title: 崩溃恢复与日志机制
type: lecture
lecture: 7
tags: [journaling, write-ahead-logging, crash-recovery, metadata-journaling, checkpointing]
status: complete
---
# Lec 7 崩溃恢复与日志机制

## TL;DR

- **预写式日志核心思想**：日志文件系统（Journaling File System）将数据库中的预写式日志（Write-Ahead Logging, WAL）引入内核，在修改原地物理结构前，先将更新操作按事务序列顺序追加写入专有日志区，将崩溃恢复时间从全盘扫描的 $O(\text{Disk Size})$ 剧降至仅与未决日志量相关的 $O(\text{Log Size})$。
- **三类日志模式权衡**：完整数据日志（Data Journaling）提供最高一致性但承受双倍写入带宽惩罚；元数据日志（Writeback）速度最快但面临旧数据泄露隐患；有序日志（Ordered Journaling，ext3/ext4 默认）通过强制“数据先写原位、元数据后写日志并提交”的定序屏障，以极低开销兼顾性能与安全。
- **两阶段提交与检查点流转**：事务持久化严格依赖写入屏障（Write Barrier），确保事务数据落盘后再写入提交标记（TxEnd）；后台检查点（Checkpointing）异步将提交内容搬移回原位（In-place）并推进循环日志指针，完成生命周期闭环。

## 阅读资料

- Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau
  [*Operating Systems: Three Easy Pieces, Chapter 42: Crash Consistency: FSCK and Journaling*](http://pages.cs.wisc.edu/~remzi/OSTEP/file-journaling.pdf)
- Giampaolo, Dominic
  [*Practical File System Design with the Be File System, Chapter 7: Logging*](https://course.ece.cmu.edu/~ece746/papers//textbook_chapters/Giampaolo-Practical_File_System_Design_with_the_Be_File_System_Chapter_7.pdf)
- Jim Gray and Andreas Reuter
  [*Transaction Processing: Concepts and Techniques*](https://www.sciencedirect.com/book/9781558601901/transaction-processing), Morgan Kaufmann, 1992

## 本讲定位

第六讲揭示了崩溃一致性问题的本质与传统 FSCK 的可用性缺陷，并剖析了 Soft Updates 依赖图的优雅与繁杂。

在工业界演进中，真正成为统治性主流方案的，是将经典数据库事务理论移植入操作系统内核的**预写式日志（Write-Ahead Logging, WAL / Journaling）**技术（如 Linux ext3/ext4、XFS、Windows NTFS、BeFS）。本讲深入拆解日志文件系统的事务抽象、三种数据日志模式、检查点机制以及崩溃恢复协议。

## 预写式日志（WAL）与事务模型

日志文件系统的基本思路极具启发性：**在向磁盘原本的复杂物理数据结构（Inode、位图、目录项）执行就地修改之前，先用一段专用的连续磁盘空间（日志区，Journal）按顺序记下即将执行的操作细节**。

### 事务（Transaction）解构

一次文件修改在日志中被组织为一个逻辑事务，包含以下结构：
1. **事务开始块（TxBegin）**：记录事务的唯一递增 ID（TID）及包含的块描述符；
2. **描述符与更新内容块**：包含即将修改的目标 Inode、数据位图或目录项在最终盘上的目标逻辑块地址（LBA）以及最新的更新字节副本；
3. **事务提交块（TxEnd / Commit Block）**：仅包含一个固定的提交标记与校验和。

### 恢复时间的质变

如果在系统运行中途发生崩溃断电：
- 系统重启挂载时，内核无需遍历整块物理磁盘，**只需要线性扫描几兆字节到几百兆字节的日志区**；
- 若某个事务已经写入了完整的 `TxEnd`，内核确信该更新已逻辑提交，只需将其记录的内容顺序重放到实际物理位置；
- 若某个事务在写入途中断电，缺少 `TxEnd`，内核直接丢弃该不完整片段。

恢复时间从依赖物理介质总容量的 $O(\text{Disk Size})$ 缩减为与当前未决日志量成正比的 $O(\text{Log Size})$，通常仅需数十毫秒至数秒即可完成。

## 日志的三种工作模式与性能权衡

在日志中究竟应该记录哪些内容？操作系统在吞吐量与一致性之间发展出了三种经典的模式：

### 1. 数据日志（Data Journaling / Full Journaling）

- **工作机制**：用户写入的真实数据块与所有元数据块一样，必须首先完整写入日志区并提交，随后再异步写回常规文件数据区。
- **代价与权衡**：所有用户数据都被强制写入了磁盘两次（一次进日志，一次进原位），**产生 2.0 倍的写入放大与吞吐量折半**。尽管它提供了极高的一致性保证（即使崩溃也不会丢失刚刚写入的数据），但在实际生产环境中由于过重的 I/O 惩罚极少被默认启用。

### 2. 元数据日志（Metadata Journaling / Writeback）

- **工作机制**：仅将 Inode、位图等元数据写入日志区；用户真实数据直接异步写入原位数据区，两者落盘完全解耦无序。
- **安全隐患**：若系统先将元数据（更新了文件大小与指针）写入日志并提交，而用户真实数据尚未真正落盘就发生了断电，重启恢复后，文件的元数据指向了一块**包含旧文件残留内容的脏数据块**。这不仅导致数据损坏，还可能在多租户服务器上引发严重的安全数据泄露。

### 3. 有序日志（Ordered Journaling，Linux ext3/ext4 默认模式）

为了既避免数据日志的 2 倍带宽惩罚，又杜绝元数据日志的陈旧脏读隐患，有序日志提出了精巧的定序屏障协议：

```text
步骤 1: 将用户数据块直接写入原位数据区 (In-place Data Write)
步骤 2: 等待用户数据写入彻底完成 (I/O Barrier / Flush)
步骤 3: 将元数据变更作为事务写入日志区 (Metadata Journal Write)
步骤 4: 写入事务提交块 TxEnd 并确认落盘 (Commit Barrier)
步骤 5: 稍后在后台异步将元数据写回原位 (Checkpointing)
```

通过在“用户数据落盘”与“元数据事务提交”之间强行插入硬件定序屏障，有序日志保证了：**任何被提交元数据所指向的数据块，在物理上必然已经包含了最新的真实数据**。该模式在维持单倍数据写流量的同时，完全消除了安全脏读隐患，成为当今主流操作系统的默认黄金标准。

## 提交协议、写屏障与检查点（Checkpointing）

在实现日志协议时，必须防止现代磁盘硬件控制器的乱序写回（Out-of-order Write Caching）。

### 为什么必须有写屏障（Write Barrier）？

假设系统向日志区写入了 5 个元数据块和 1 个 `TxEnd` 提交块。如果直接异步并发下发，磁盘控制器为了优化磁头寻道，可能会优先把物理位置靠后的 `TxEnd` 刷入持久介质，而前 5 个元数据块还在控制器易失 DRAM 缓存中。

此时若突然断电，重启后日志区存在一个孤立的 `TxEnd`，恢复程序会误认为该事务已完整提交并重放垃圾数据，导致文件系统毁灭性损坏。

因此，内核必须使用显式硬件指令：
1. 先下发所有内容更新块；
2. 发出强制刷新指令（`fsync` / `REQ_PREFLUSH` / `REQ_FUA`）；
3. 收到驱动器确认后，再单独下发 `TxEnd` 块，最后再次刷新。

### 检查点（Checkpointing）与循环日志管理

日志区通常是一个固定大小（如 128MB）的循环缓冲区（Circular Buffer）：
- **检查点推进**：当事务成功提交后，后台工作线程异步将日志中的最新元数据写入最终的 Inode 表与位图物理原位，这一过程称为**检查点（Checkpointing）**；
- 一旦检查点完成，该事务所占用的日志空间便可安全标记为空闲并循环复用，日志的头指针向前推进。

## 崩溃恢复协议（Recovery Protocol）

当带有日志的文件系统在崩溃后重新挂载时，执行确定的三步恢复协议：

1. **扫描日志确定边界**：从最近一次已知的检查点检查点指针出发，前向线性扫描日志，记录所有具有合法校验和与 `TxEnd` 的事务列表；
2. **重做重放（Redo Replay）**：按照事务递增序列号（TID），依序将所有已提交事务的元数据块覆盖写入到对应的最终磁盘物理扇区，确保所有提交的修改全部持久化生效；
3. **丢弃未决事务**：对于扫描到日志末尾发现缺少 `TxEnd` 的半截事务，直接丢弃忽略；未提交事务涉及的原位元数据从未被修改，文件系统自然保持在崩溃前的上一致状态。

## 我的理解

::: insight
**日志机制的核心是用“时间维度上的版本记录”化解“空间维度上的原位撕裂”**：
在传统覆盖写文件系统中，崩溃破坏之所以致命，是因为我们在同一个物理扇区上既要读取旧状态、又要就地写入新状态，物理世界一旦在微秒间隙断电，旧状态已碎，新状态未立。
日志机制的哲学飞跃在于：**把修改行为本身变成一阶公民（First-class Entity）**。系统不再急于原地销毁旧状态，而是在连续时序日志中先行建立确定性的不可变凭据。即使原地物理世界千疮百孔，只要时序日志完整，系统就拥有随时回滚与重构现实的神圣权力。这种将可变状态转化为追加事件日志（Event Sourcing / WAL）的思想，构成了后世从分布式共识 Raft 到微服务事件驱动架构的基石。
:::
