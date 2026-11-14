---
title: 文件系统存储布局
type: lecture
lecture: 4
tags: [file-system-layout, inode, ffs, btrfs, f2fs, tablefs]
status: complete
---
# Lec 4 文件系统存储布局

## TL;DR

- **盘上数据结构核心命题**：文件系统将线性扇区划分为超级块（Superblock）、位图分配器、Inode 表与数据区，通过将层级路径转换为 Inode 编号索引，建立抽象文件到物理存储介质的映射网格。
- **小文件优化与 Extent 演进**：针对“绝大多数文件体积微小”的实证分布，传统 Inode 采用不对称多级间接指针；现代文件系统全面转向 Extent（连续物理块区间）表达，显著压缩元数据并保障顺序吞吐。
- **新介质与新架构范式**：Btrfs 基于 B 树森林与写时复制（COW）实现无损快照；F2FS 针对 NAND 闪存引入分段多头日志（Multi-head Logging）与 NAT 表化解游走树难题；TableFS 将元数据打包嵌入 LSM-Tree，消除小文件创建与目录遍历的高昂随机 I/O。

## 阅读资料

- [*The Design and Implementation of the 4.4BSD Operating System*](https://course.ece.cmu.edu/~ece746/papers//textbook_chapters/McKusick-The_Design_and_Implementation_of_the_4.4BSD_Operating_System_Chapter_8.pdf)
- [*Operating Systems: Three Easy Pieces*](http://pages.cs.wisc.edu/~remzi/OSTEP/file-implementation.pdf)
- [*BTRFS: The Linux B-Tree Filesystem, 13*](http://vtucs.com/wp-content/uploads/2015/02/btree-report.pdf)
- [*F2FS: A New File System for Flash Storage, 15*](https://www.usenix.org/system/files/conference/fast15/fast15-paper-lee.pdf)
  - 专门为闪存设计的日志结构文件系统
- [*TABLEFS: Enhancing Metadata Efficiency in the Local File System, 13*](https://www.pdl.cmu.edu/PDL-FTP/FS/CMU-PDL-13-102.pdf)
  - 将文件系统元数据打包存入键值存储（LSM-Tree）的突破性架构

## 本讲定位

前三讲已经建立了两类底层介质的完整物理模型：闪存固态硬盘（纯电子、随机与顺序差距小、写前必擦、存在擦写磨损）和机械磁盘（有机械寻道与旋转、随机比顺序慢两到三个数量级）。文件系统正是架设在这些裸介质之上的关键抽象层，它把“一堆扁平的逻辑扇区或闪存页”变成应用程序熟悉的层级化文件与目录树。

本讲的核心问题是：**文件系统在盘上应该如何排布其元数据与数据结构，才能在底层介质的物理约束下兼顾高速与崩溃可靠？** 我们先通过 OSTEP 的“极简文件系统”（vsfs）建立心智模型，随后分析传统 UNIX FFS 布局、Btrfs 的写时复制 B 树、面向闪存的 F2FS，以及将元数据引入 LSM-Tree 的 TableFS，全面掌握四种截然不同的布局哲学。

## 极简文件系统：VSFS 磁盘布局模型

为了理解文件系统的物理组织，我们构建一个划分为 64 个连续 4KB 数据块的简单文件系统（VSFS）：

1. **数据区（Data Region）**：存放用户写入的真实文件数据内容，占据绝大部分空间（如最后的 56 个块）；
2. **Inode 表（Inode Table）**：存放所有文件的索引节点元数据，保留连续的一组块（如 5 个块）；
3. **分配位图（Allocation Bitmaps）**：包含 Inode 位图与数据块位图，分别用 1 个比特标记某个 Inode 或数据块是否已被占用；
4. **超级块（Superblock）**：位于固定物理位置（如第 0 块），记录文件系统全局元信息（Inode 总数、数据块总数、Inode 表起始偏移、文件系统魔数与版本）。

![vsfs 磁盘块布局整体结构图（超级块、Inode/数据位图、Inode 表与数据区划分）](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20260305140404801.png)

当操作系统挂载（mount）一个文件系统时，第一步总是读取其超级块，校验魔数并初始化全局挂载结构。随后内核便可根据统一的算术公式精确计算出任意 Inode 编号对应的磁盘绝对扇区。

## 文件组织：Inode 与多级索引

Inode（Index Node）是持久化存储元数据的第一核心实体。一个典型的 Inode 大小通常为 128 或 256 字节，包含：
- 文件类型（常规文件、目录、符号链接、设备等）；
- 文件字节长度（Length）；
- 所有权与访问权限（UID/GID, Mode）；
- 时间戳信息（创建时间、修改时间 mtime、元数据修改时间 ctime、访问时间 atime）；
- 物理数据块指针数组。

![Inode 在磁盘地址空间中的偏移计算与扇区定位示意图](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20260305145241673.png)

### 不对称多级间接指针（Multi-level Index）

为了寻址不同大小的文件，传统 UNIX FFS Inode 采用非平衡树结构：
- **12 个直接指针（Direct Pointers）**：直接指向 12 个数据块（支持 $12 \times 4\text{KB} = 48\text{KB}$ 以内的小文件，无需二级查找）；
- **1 个间接指针（Indirect Pointer）**：指向一个包含 1024 个块指针的指针块（额外支持 4MB）；
- **1 个双重间接指针（Double-indirect Pointer）**：指向包含 1024 个间接块指针的块（额外支持 4GB）；
- **1 个三重间接指针（Triple-indirect Pointer）**：支持 TB 级超大文件。

这一设计深刻反映了存储领域的经验经验分布：**工业界真实统计表明，文件系统中 80% 以上的文件都是小于几 KB 的极小文件，而少数超大文件占据了绝大部分磁盘空间**。直接指针确保了绝大多数小文件访问零额外指针块 I/O。

### Extent 区间分配演进

当文件达到数 GB 时，多级指针会导致 Inode 与间接块产生巨大的元数据膨胀，且离散指针难以保证磁盘物理连续性。现代文件系统（如 Linux ext4、XFS）转向 **Extent（连续区间）** 机制：
- 一个 Extent 由三元组表达：`[逻辑文件偏移, 物理起始块号, 连续块长度]`；
- 一个 1GB 的完全连续写入文件仅需单一 Extent 即可描述，极大地压缩了元数据开销，并天然保障了底层的顺序高带宽传输。

## 目录组织与路径解析

在类 UNIX 系统中，“一切皆文件”，目录本质上也是一个特殊的常规文件：
- 其 Inode 元数据中的类型字段标记为目录；
- 其对应的数据块中存放的是一系列目录项条目列表：`[(文件名, Inode 编号), ...]`。

当应用发起系统调用 `open("/foo/bar", O_RDONLY)` 时，内核必须进行逐级递归解析：
1. 从固定的根目录 Inode（通常为 Inode 2）读取其数据块；
2. 扫描数据块寻找匹配名为 `"foo"` 的目录项，获得其 Inode 编号；
3. 读取 `"foo"` 的 Inode 并载入其数据块；
4. 扫描数据块匹配名为 `"bar"` 的项，获得目标文件的 Inode 编号；
5. 读取 `"bar"` 的 Inode 检查权限，在内核打开文件表中创建打开句柄。

## 现代写时复制文件系统：Btrfs

Btrfs（B-Tree File System）是现代 Linux 平台主流的写时复制（Copy-on-Write, COW）文件系统：
1. **B 树森林架构**：Btrfs 内部由多棵专门的 B 树组成（Subvolume 树、Extent 分配树、Chunk 映射树等），所有文件元数据、目录项甚至小文件内联数据均作为 B 树键值对存储；
2. **写时复制（COW）机制**：更新现有数据块时绝不原地覆盖，而是分配新的磁盘 Extent 写入新数据，随后层层向上更新父节点直至树根，最后原子更新超级块中的根指针；
3. **一等公民快照（Snapshots）**：创建快照仅仅是复制当前子卷 B 树的根节点并增加子树引用计数，耗时为毫秒级的 $O(1)$ 常数时间；
4. **端到端完整性校验**：所有元数据和数据块都配备 CRC32C/BLAKE2b 校验和，可在读取时静默检测“静默数据损坏”（Bit Rot）。

## 闪存感知文件系统：F2FS

由于传统文件系统是为机械磁盘设计的，直接运行在 SSD 上会与内部 FTL 产生严重冲突，加剧随机写入放大。三星主导研发的 **F2FS（Flash-Friendly File System, FAST'15）** 专为 NAND 闪存而生：
- **匹配闪存物理层次**：将整盘划分为 Segment（2MB，匹配闪存擦除块大小）、Section（多个 Segment 组成）与 Zone（多个 Section 组成，分配给特定类型日志）；
- **多头追加写入（Multi-head Logging）**：F2FS 同时维护 6 个活动日志头，将写入物理隔离为冷/温/热数据与冷/温/热节点（Inode/索引块），大幅降低垃圾回收时的无效搬移；
- **节点地址表（Node Address Table, NAT）**：传统日志结构文件系统（LFS）在追加写入时存在“游走树（Wandering Tree）”问题——叶子块更新会导致整条向上的父指针链全部需要重写。F2FS 引入定长的 NAT 表将节点 ID 间接映射到物理块，使得 Inode 更新时无需连带修改父目录，彻底切断游走链。

## 元数据 KV 存储化：TableFS

在海量小文件场景（如数亿张小图片的社交网络或机器学习训练集），传统文件系统的层级目录遍历与 Inode 分配会引发严重的随机 I/O 风暴。CMU PDL 提出的 **TableFS（USENIX ATC'13）** 探索了革命性的元数据布局：
- **元数据完全键值化**：TableFS 将目录树扁平化编码为一个嵌入式 LSM-Tree 存储引擎（LevelDB）。其键为 `(parent_inode_id, filename)`，值为序列化后的 Inode 属性；
- **小文件内联聚合**：对于小于数 KB 的极小文件，其文件内容直接作为 Value 与 Inode 元数据内联打包存入 LSM-Tree；对于大文件，仅记录外部大型数据对象的对象 ID；
- **性能飞跃**：借由 LSM-Tree 的批量连续写特性，TableFS 将密集创建/删除小文件与目录检索的吞吐量提升了 2 到 10 倍，证明了用工业级 KV 引擎替代传统 Inode 树的巨大架构优势。

## 我的理解

::: insight
**存储布局的演进史，就是对“局部性”与“间接层”权衡艺术的持续重构**：
从 FFS 依赖磁盘几何的柱面组局部化，到 Ext4 的 Extent 区间连续分配，再到 Btrfs 的写时复制与 TableFS 的元数据键值化，文件系统设计展现出惊人的规律：
每次底层硬件特征发生突变（从机械磁盘的磁臂寻道，到 SSD 的写前必擦，再到海量微小元数据风暴），系统软件就会引入一层新的间接映射（Indirect Pointers $\rightarrow$ Extents $\rightarrow$ NAT $\rightarrow$ LSM-Tree）。间接层消除了底层物理冲突，但也带来了内存与碎片化的新开销。卓越的文件系统从来不是最复杂的系统，而是在给定的硬件约束与工作负载特征之间，找到了平衡局部性与间接代价的最优折衷点。
:::
