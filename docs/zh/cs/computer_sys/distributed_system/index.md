---
title: 6.5840 分布式系统（Spring 2026）
type: course
course: 分布式系统（Spring 2026）
course_id: '6.5840'
tags: [distributed-systems, consensus, fault-tolerance, consistency, replication]
status: complete
source: https://pdos.csail.mit.edu/6.5840/schedule.html
---
# 6.5840 分布式系统（Spring 26）

## TL;DR

- 课程系统研究大规模分布式系统的核心理论与工程实践：涵盖状态机复制、强弱一致性模型、分布式事务与拜占庭容错。
- 学习路径依序推进：「计算与主备基础（RPC/MapReduce/GFS）」→「共识与复制（Paxos/Raft/ZooKeeper）」→「事务与云存储（Spanner/FaRM/DynamoDB）」→「新型范式与去中心化（Ray/SUNDR/Bitcoin/PBFT）」。
- 核心权衡聚焦于容错、一致性与性能（延迟/吞吐）的三方内在张力，培养基于真实网络延迟、时钟漂移与机器故障设计可验证工业级系统的架构能力。

## 课程定位与核心议题

分布式系统是现代云计算、大规模数据基础设施与去中心化网络的基石。MIT 6.5840 是一门高强度的核心研究生课程，包含理论讲授、经典论文研读与 5 个高难度工程实验（基于 Go 语言）。课程的核心目标不是简单罗列工业工具，而是从根本上理解分布式环境下的通信、协调、容错与状态一致性。

### 为什么分布式系统具有挑战？

单机计算拥有共享内存、统一物理时钟和全或无的故障模型（Crash-Stop）；而在分布式环境中，系统必须在以下固有物理限制下提供确定性服务：

1. **并发与异步网络**：消息可能延迟、乱序、丢失或重传，网络随时可能发生任意拓扑分区（Network Partition）。
2. **局部独立故障**：集群中部分机器可能在任意时刻崩溃、重启或假死，系统必须在部分节点失效时持续对外提供可用服务。
3. **物理时钟漂移**：不同节点的本地时钟存在相对漂移与不同步，无法依赖绝对物理墙上时间确定事件因果序。

### 三大核心指标与系统权衡

所有分布式系统的架构决策均是在以下三维空间内权衡取舍：

| 核心指标 | 设计目标 | 主要机制与代价 |
|---|---|---|
| **容错（Fault Tolerance）** | 节点发生崩溃时保持高可用与数据不丢失 | 主备复制（Primary-Backup）、多数派共识（Paxos/Raft）、状态机快照与日志重放；代价是冗余资源与网络交互开销 |
| **一致性（Consistency）** | 对外提供直观且正确的状态读写规约 | 强一致（线性一致性/可串行化）、弱一致（因果一致性/最终一致性）；强一致需要跨节点协调通信，牺牲响应延迟 |
| **可扩展性（Scalability）** | 增加 $N$ 台机器换取近似 $N$ 倍的吞吐提升 | 分片（Sharding）、分布式哈希与负载均衡；代价是跨分片协调、分布式事务与重平衡复杂度 |

::: insight 核心系统洞见：分布式权衡的不可避免性
容错需要复制与网络同步，一致性要求全局状态协调，而网络与通信本身是吞吐和延迟的最大瓶颈。优秀架构师的工作从来不是寻找“完美架构”，而是在给定的业务一致性需求、网络延迟容忍度与硬件成本约束下，精准定位最优折中点。
:::

## 前置知识与能力准备

本课程注重理论证明与生产级系统实现的双向结合，学习前应具备：

- 操作系统工程（MIT 6.1810）
- 计算机系统工程（MIT 6.1800）

## 实验体系与实践路线

6.5840 的实验体系以严苛著称，代码直接运行在自动化并发测试与网络故障注入（延迟、丢包、乱序、分区）环境中：

```text
Lab 1: MapReduce  ──>  Lab 2: Key/Value  ──>  Lab 3: Raft  ──>  Lab 4: KV-Raft  ──>  Lab 5: Sharded KV
  (分布式批处理)        (RPC与幂等去重)         (共识状态机)        (容错KV服务)         (动态分片集群)
```

| 实验代号 | 实验名称 | 核心挑战与考察点 |
|---|---|---|
| **Lab 1** | [MapReduce](https://pdos.csail.mit.edu/6.824/labs/lab-mr.html) | 实现分布式 Master/Worker 调度架构、任务切分、Map 中间结果落盘、Reduce 聚合、Worker 超时重派与宕机容错 |
| **Lab 2** | Key/Value Server | 构建单机 RPC KV 存储服务，实现基于唯一客户端 ID 与递增序列号的 RPC 幂等去重、并发安全锁控制与内存表操作 |
| **Lab 3** | Raft Consensus | 从零实现完整的 Raft 共识引擎：<br>• **3A**：心跳驱动与随机选举超时（Leader 选举）<br>• **3B**：日志复制、AppendEntries 一致性检查与提交点推进<br>• **3C**：非易失元数据持久化与崩溃重启恢复<br>• **3D**：InstallSnapshot RPC 与状态机日志截断压缩 |
| **Lab 4** | KV-Raft | 将 Raft 引擎与上层应用解耦对接：通过 `applyCh` 驱动确定性状态机、线性一致性读取保证、快照生成与日志安全恢复 |
| **Lab 5** | Sharded Key/Value | 实现工业级分片集群：基于分片控制器（Shard Controller）完成配置更新、多 Raft 组协同、跨组分片数据原子拉取与无损平滑迁移 |

## 课程模块与讲义导引

课程共 21 讲，按由浅入深划分为四大认知进阶模块：

### 模块一：分布式计算基础与共识开端（Lec 1 ~ Lec 5）

建立分布式基础模型，从无状态批处理、单机并发进阶至经典共识算法：

- [Lec 1 介绍 & MapReduce](./lec1.md)
  - 分布式核心挑战、可扩展性瓶颈、MapReduce 编程抽象、Master 容错与 Straggler 慢任务重跑机制。
- [Lec 2 RPC 与线程并发](./lec2.md)
  - Go 并发原语选型、条件变量 vs 通道、RPC 语义（At-Least-Once vs At-Most-Once）、网络爬虫与并发 KV 实例。
- [Lec 3 GFS：谷歌分布式文件系统](./lec3.md)
  - 大文件工作负载设计哲学、单 Master 架构与元数据内存化、Chunkserver 读写链路、记录追加（Record Append）与弱一致性折中。
- [Lec 4 Paxos：经典共识算法](./lec4.md)
  - 多数派（Quorum）数学性质、两阶段协议（Prepare/Accept）、防脑裂机制、Multi-Paxos 工业落地挑战。
- [Lec 5 Golang 并发设计模式](./lec5.md)
  - 核心设计者 Russ Cox 特邀讲座：Go 类型系统思维、避免深层继承、Goroutine 状态机流式处理与 RPC 协议复用。
- [附录 Spark：弹性分布式数据集 RDD](./spark.md)
  - 内存计算范式、Lineage 细粒度容错、宽依赖/窄依赖切分与 Shuffle 优化。

### 模块二：复制状态机与一致性理论（Lec 6 ~ Lec 10）

深入分布式系统理论皇冠——在不可靠网络中对操作全序达成一致与规约判定：

- [Lec 6 容错复制：Raft（一）选主与日志对齐](./lec6.md)
  - 强 Leader 原则、随机化选举超时（打破对称防 Split Vote）、日志一致性检查与 AppendEntries nextIndex 回退优化。
- [Lec 7 容错复制：Raft（二）持久化、快照与只读租约](./lec7.md)
  - 状态持久化边界与崩溃恢复、状态机快照与 InstallSnapshot RPC、Copy-on-Write 机制、线性化只读操作与租约（Lease）优化。
- [Lec 8 一致性模型与线性一致性](./lec8.md)
  - 线性一致性（Linearizability）严格规约、线性化点判定、真实时间偏序约束、顺序一致性对比与 6 大经典时序判定例题。
- [Lec 9 ZooKeeper：分布式协调原语](./lec9.md)
  - 弱事务下的协调哲学、树形层次命名空间、Watch 机制、有序临时节点（Ephemeral-Sequential）实现分布式锁与选主、ZAB 协议。
- [Lec 10 Lab 实验答疑：Raft 调试与并发陷阱](./lec10.md)
  - 梳理 Raft 状态机死锁排查、定时器重置竞争、活锁与脑裂调试策略、测试用例深层逻辑剖析。

### 模块三：分布式事务与大规模存储系统（Lec 11 ~ Lec 17）

跨越单状态机边界，解决分片架构下的原子提交、主备变体与极致性能追求：

- [Lec 11 分布式事务：2PL 与 2PC](./lec11.md)
  - ACID 语义拆解、两阶段锁（2PL）保证隔离性与死锁解除、两阶段提交（2PC）保证跨分片原子提交、协调者崩溃无限阻塞破解。
- [Lec 12 Spanner：全球级分布式数据库](./lec12.md)
  - 跨地域多 Paxos 组事务、TrueTime API（GPS + 原子钟界定 $\epsilon$ 误差界）、Commit Wait 规则严格实现外部一致性（External Consistency）。
- [Lec 13 链式复制（Chain Replication）](./lec13.md)
  - 强一致主备模式、读写分离拓扑（头节点写、尾节点读）、故障恢复与租约机制；附 VMware FT 容错虚拟机实录。
- [Lec 14 FaRM：基于 RDMA 与 NVRAM 的乐观并发控制](./lec14.md)
  - 单数据中心极致性能压榨、单边 RDMA 绕过 CPU/内核、NVRAM 消灭磁盘写瓶颈、OCC 提交协议四阶段（Lock/Validate/Commit）。
- [Lec 15 DynamoDB：可预测性能的云原生 NoSQL](./lec15.md)
  - 从 Dynamo 的无中心 Gossip 到 DynamoDB 的完全托管架构、存储计算分离、请求路由准入与多租户突发流量削峰。
- [Lec 16 缓存一致性：Facebook Memcached 架构](./lec16.md)
  - 读密集型社交图挑战、跨 Region 复制一致性、Lease 机制防御击穿与陈旧写入、Gutter 降级服务器池；附 [论文精读](./lec16paper.md)。
- [Lec 17 AWS Lambda：按需容器加载](./lec17.md)
  - Serverless 冷启动 50ms 挑战、块级按需加载（Block-level loading）、无信任去重与收敛加密、分层缓存与纠删码防尾延迟。

### 模块四：异步计算范式、不可信存储与拜占庭共识（Lec 18 ~ Lec 21）

突破局域网与可信集群假设，探讨大规模动态图计算与拜占庭敌手模型：

- [Lec 18 Ray：分布式 Future 与 Ownership 架构](./lec18.md)
  - 强化学习与动态任务图需求、Future 与 Actor 混合编程模型、Ownership 分布式调度树、Plasma 共享内存对象存储与 Lineage 容错。
- [Lec 19 SUNDR：不可信服务器上的 Fork 一致性](./lec19.md)
  - 防御恶意的存储提供商、加密哈希树与数字签名、Fork 一致性安全界限（分叉即永久隔离不可隐蔽）。
- [Lec 20 比特币：去中心化账本与工作量证明](./lec20.md)
  - 开放网络无许可准入、UTXO 交易链模型、工作量证明（PoW）算力抽签选主、最长链原则与防双花博弈论激励。
- [Lec 21 实用拜占庭容错（PBFT）](./lec21.md)
  - 恶意参与者模型、容错极限界定（$n \ge 3f+1$ 严谨推导）、三阶段投票（Pre-Prepare/Prepare/Commit）、视图切换（View Change）与检查点。

## 经典研读文献清单

本课程绝大多数知识沉淀于以下计算机系统史上的里程碑论文：

1. **MapReduce (2004)**: Jeffrey Dean, Sanjay Ghemawat. *MapReduce: Simplified Data Processing on Large Clusters*. OSDI.
2. **GFS (2003)**: Sanjay Ghemawat, Howard Gobioff, Shun-Tak Leung. *The Google File System*. SOSP.
3. **Paxos Made Simple (2001)**: Leslie Lamport. *Paxos Made Simple*. ACM SIGACT News.
4. **Raft (2014)**: Diego Ongaro, John Ousterhout. *In Search of an Understandable Consensus Algorithm*. USENIX ATC.
5. **Linearizability (1990)**: Maurice P. Herlihy, Jeannette M. Wing. *Linearizability: A Correctness Condition for Concurrent Objects*. TOPLAS.
6. **ZooKeeper (2010)**: Patrick Hunt, Mahadev Konar, Flavio P. Junqueira, Benjamin Reed. *ZooKeeper: Wait-free Coordination for Internet-scale Systems*. USENIX ATC.
7. **Spanner (2012)**: James C. Corbett et al. *Spanner: Google’s Globally-Distributed Database*. OSDI.
8. **FaRM (2015)**: Aleksandar Dragojević et al. *No compromises: distributed transactions with consistency, availability, and performance*. SOSP.
9. **DynamoDB (2022)**: Mostafa Elhemali et al. *Amazon DynamoDB: A Scalable, Predictably Performant, and Fully Managed NoSQL Database Service*. USENIX ATC.
10. **Memcached at Facebook (2013)**: Rajesh Nishtala et al. *Scaling Memcache at Facebook*. NSDI.
11. **AWS Lambda (2023)**: Marc Brooker et al. *On-demand Container Loading in AWS Lambda*. USENIX ATC.
12. **Ray (2018)**: Philipp Moritz et al. *Ray: A Distributed Framework for Emerging AI Applications*. OSDI.
13. **SUNDR (2004)**: Jinyuan Li et al. *Secure Untrusted Data Repository (SUNDR)*. OSDI.
14. **Bitcoin (2008)**: Satoshi Nakamoto. *Bitcoin: A Peer-to-Peer Electronic Cash System*.
15. **PBFT (1999)**: Miguel Castro, Barbara Liskov. *Practical Byzantine Fault Tolerance*. OSDI.
