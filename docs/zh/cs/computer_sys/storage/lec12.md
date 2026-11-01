---
title: 极度可扩展的存储
type: lecture
lecture: 12
tags: [object-storage, ceph, crush-algorithm, consistent-hashing, scalable-storage]
status: complete
---
# Lec 12 极度可扩展的存储

## TL;DR

- **对象存储抽象范式**：为了跨越数万节点与百亿级文件的规模天花板，分布式对象存储（Object Storage）彻底抛弃了脆弱的 POSIX 层级目录树与细粒度锁协议，采用扁平化命名空间（Bucket + Key）与不可变数据对象模型。
- **算力换存储与无查表寻址（CRUSH）**：Ceph 开创性地提出了基于伪随机确定性函数的 CRUSH 算法，利用分层故障域拓扑图直接计算出对象所属的物理存储守护进程（OSD），消除了千亿级对象在传统中心化路由表上的元数据瓶颈。
- **控制面与数据面彻底解耦**：现代云原生对象存储（如 Ceph 与 Windows Azure Storage）将结构化元数据分区管理与底层流式持久化数据块（Extents）严格分离，实现近乎无限的水平横向扩展能力。

## 阅读资料

- Weil, Sage A. and Brandt, Scott A. and Miller, Ethan L. and Long, Darrell D. E. and Maltzahn, Carlos
  [*Ceph: A Scalable, High-Performance Distributed File System*](https://www.usenix.org/legacy/events/osdi06/tech/full_papers/weil/weil.pdf), In *Proceedings of the 7th USENIX Symposium on Operating Systems Design and Implementation (OSDI)*, 2006, pages 307--320
- Brad Calder, Ju Wang, Aaron Ogus, Niranjan Nilakantan, Arild Skjolsvold, Sam McKelvie, Yikang Xu, Shashwat Srivastav, Jiesheng Wu, Huseyin Simitci, Jaidev Haridas, Chakravarthy Uddaraju, Hemal Khatri, Andrew Edwards, Vaman Shenoy, Margie Kavalam, Hanan Liron, James Sprunt, Arpan Desai, Ashish Shenoy, Ramu Sonhavane, Neeta Radia, Vinod Radhakrishnan, Nayden Naydenov, Parveen Sengupta, Vikas Patidar, Saurabh Bansal, Arnab Roy, Ramanathan Saravanan, Jayashree Sakleshpur, Pradeep Nayak, Swaminathan Krishnan, Chanchal Singh, Ankit Borikar, Niranjan Ramankutty, Mayank Verma, Parikshit Rao
  [*Windows Azure Storage: A Highly Available Cloud Storage Service with Strong Consistency*](https://dl.acm.org/doi/10.1145/2043556.2043571), In *Proceedings of the 23rd ACM Symposium on Operating Systems Principles (SOSP)*, 2011, pages 143--157
- Garth A. Gibson et al.
  [*File Server Scaling with Network-Attached Secure Disks (NASD)*](https://www.pdl.cmu.edu/PDL-FTP/NASD/asplos98.pdf), ACM SIGMETRICS Performance Evaluation Review, 1997

## 本讲定位

第十一讲中，我们看到 GFS 虽然成功支撑了数千台节点的批处理计算，但其架构依然保留着单 Master 节点的脆弱约束，且 64MB 的 Chunk 粒度在面对数以百亿计的小图片、微视频与网盘文件时导致 Master 内存迅速耗尽。

本讲探讨面向全球级海量数据存储的终极解法——**分布式对象存储（Distributed Object Storage）**。我们重点研读两大代表性成果：CMU/UCSC 提出的开源对象存储基石 **Ceph** 及其突破性的 **CRUSH 寻址算法**，以及微软构建的商业级云原生存储架构 **Windows Azure Storage (WAS)**。

## 范式转移：从层级树到扁平对象模型

传统分布式文件系统（如 NFS、AFS 乃至 GFS）之所以在数万台节点并发时遭遇性能断崖，根本原因在于其背负的 **POSIX 文件系统语义遗产**：
1. **树形目录锁瓶颈**：当数万个客户端同时在同一个目录下创建或移动文件时，目录 Inode 的排他锁成为单点性能灾难；
2. **重命名（Rename）的原子性沉重开销**：在分布式网络中原子性地移动一个目录子树，需要跨多个服务器加锁协调；
3. **路径逐级解析（LOOKUP 放大）**：为了读取 `/a/b/c/d/file.txt`，客户端必须沿途跨网络发起多次目录解析。

### 对象存储的核心抽象

对象存储放弃了 POSIX 的层级结构，代之以极其极简的抽象模型：
- **扁平命名空间**：仅包含存储桶（Bucket）与唯一的对象键（Object Key，即任意字符串）；
- **对象实体（Object）**：由唯一的 ID、不可变的数据载荷（Payload / Blob）以及用户自定义的键值元数据（Metadata）构成；
- **极简 RESTful 接口**：仅提供 `PUT`（创建/覆盖）、`GET`（读取）、`DELETE`（删除）以及 `HEAD`（查询元数据）四项原子语义，杜绝复杂的就地随机小写与目录锁竞争。

## 算力代查表：Ceph 与 CRUSH 伪随机放置算法

在传统的分布式系统中，为了知道某个对象究竟存放在哪台机器上，系统必须维护一张庞大的“对象到物理节点”的**元数据路由表**。然而，当对象数量突破千亿、物理磁盘多达数十万块时，**维护和同步这张路由表本身所需的元数据开销，就足以耗尽整个分布式集群的全部内存与网络带宽**。

Sage Weil 等人在 OSDI'06 提出的 **Ceph** 给出了一项天才般的创新：**彻底消除集中式路由表，用数学计算代替数据库查表！**

### 放置组（Placement Group, PG）解耦

Ceph 并不直接追踪每一个独立的对象，而是引入了逻辑间接层——**放置组（Placement Group, PG）**：
1. 当客户端写入一个名为 `object_id` 的对象时，首先通过确定性哈希函数计算其 PG 编号：

$$
\text{PG\_ID} = \text{Hash}(\text{object\_id}) \pmod M
$$

其中 $M$ 是整个集群预先设定的全局固定 PG 总数（通常为数万到数十万）；
2. 即使全集群包含数千亿个具体对象，它们在逻辑上被收敛归集到了有限个（如 65536 个）固定 PG 中，元数据规模压缩了数个数量级。

### CRUSH 算法的数学机理

获得 `PG_ID` 后，Ceph 不去查询任何元数据服务器，而是由客户端本地调用 **CRUSH（Controlled Replication Under Scalable Hashing）算法**，以纯数学函数直接算出承载该 PG 的一组物理存储守护进程（OSD）：

$$
(\text{OSD}_1, \text{OSD}_2, \dots, \text{OSD}_R) = \text{CRUSH}(\text{ClusterMap}, \text{Rule}, \text{PG\_ID})
$$

CRUSH 的核心特性包括：
- **感知故障域层次结构（Hierarchical Cluster Map）**：集群管理员用树形结构定义物理拓扑（数据中心 $\rightarrow$ 机架 $\rightarrow$ 交换机 $\rightarrow$ 服务器 $\rightarrow$ 物理磁盘）。CRUSH 能够依据管理员策略，强制保证该 PG 的 3 个副本分别落在**不同的机架甚至不同变压器供电的机房**，提供极高物理容灾能力；
- **确定性与无中心化**：只要集群拓扑图（Cluster Map）版本一致，任何客户端在任意地点输入相同的 `PG_ID`，算出的物理 OSD 列表完全相同；客户端直接与对应的 Primary OSD 发起点对点网络通信，集群完全不存在任何全局寻址单点；
- **最小化数据迁移（Minimal Data Migration）**：当集群新增一块磁盘或某台服务器宕机导致拓扑图变更时，类似于一致性哈希，CRUSH 算法仅引发极其微小比例（$1/N$）的关联 PG 产生物理迁移，绝不会造成全集群数据的全局乱序洗牌。

## 一致性哈希与分布式哈希环

除了 Ceph 的 CRUSH 树形算法外，另一类极具代表性的无中心对象寻址范式是以 Amazon Dynamo、OpenStack Swift 为代表的**一致性哈希环（Consistent Hashing Ring）**：
1. **哈希环构造**：将哈希函数的输出空间（如 128 位 MD5 或 256 位 SHA-1）首尾相接，闭合形成一个从 0 到 $2^{128}-1$ 的环；
2. **虚拟节点（Virtual Nodes / Vnodes）**：为了防止物理机器性能异构或由于哈希值离散导致的数据倾斜，每台物理机被哈希映射为环上的数百个虚拟节点；
3. **数据寻址与顺时针路由**：计算对象键的哈希值后落入环上某一点，沿着环顺时针方向找到的第一个物理虚拟节点，即为该对象的负责存储主节点；
4. **弹性伸缩优势**：当有新节点加入或故障下线时，仅影响环上与其直接相邻的局部扇区，受影响的数据比例仅为整体容量的 $1/K$。

## 云原生双层架构：Windows Azure Storage (WAS)

微软在 SOSP'11 公开的 **Windows Azure Storage (WAS)** 展现了超大规模工业级商业云存储的典型分层架构设计。

WAS 将系统清晰切分为两层：
1. **流式持久化层（Stream Layer / Extent Replication）**：
   - 专职负责物理数据块的高吞吐高可靠持久化；
   - 底层文件被称为 Stream，由一组只追加（Append-Only）的连续 Extents 构成；
   - 在三个存储节点间通过 Paxos/Quorum 保证 Extent 的强一致多副本复制，完全不涉及上层复杂的命名空间、对象索引与事务逻辑；
2. **对象分区层（Partition Layer）**：
   - 构建于 Stream Layer 之上，面向用户提供丰富的多租户对象语义（Blobs、Tables、Queues）；
   - 维护对象全局元数据索引，并根据数据访问热度将键空间切分为多个动态分区（Partitions），在数百台 Partition Server 之间自适应负载均衡。

通过将“物理块多副本持久化”与“逻辑对象元数据管理”在物理进程上彻底拆开，WAS 既保证了底层硬件级别的超高读写吞吐，又为上层海量多租户提供了具备 ACID 强一致性的企业级对象与表格服务。

## 我的理解

::: insight
**极度可扩展性的秘诀，在于用“不可变数据”与“局部自治计算”消解全局锁**：
在单机操作系统中，我们习惯于共享内存与互斥锁；当系统规模扩大到数万台节点时，任何跨机器的全局互斥协调都会成为吞吐量的催命符。
对象存储的伟大蜕变，本质上是一场“去中心化”的认知革命：它把文件系统中最沉重的层级目录与就地更新彻底剥离，代之以不可变的键值载荷；随后利用 CRUSH 与一致性哈希这一极其强大的数学武器，将原本必须向中央服务器排队询问的元数据查询，下放给每一台客户端在本地用 CPU 算力瞬间求值。**算力是无限可扩展的，而中心化通信带宽永远有限**。这种以局部确定性计算取代全局集中式通信的思想，是现代云原生海量架构最核心的破局智慧。
:::
