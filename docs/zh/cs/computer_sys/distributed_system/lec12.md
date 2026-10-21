---
title: Spanner
type: lecture
lecture: 12
tags: [spanner, truetime, external-consistency, distributed-transactions, snapshot-isolation]
status: complete
---
# Lec 12 Spanner

## TL;DR
- Spanner 通过**多 Paxos 组分片复制 + 跨组 2PC** 实现全球分布式事务，每个分片一个 Paxos 组，TC 自身也被 Paxos 复制，解决 2PC 的阻塞问题。
- **TrueTime API** 暴露时钟不确定区间 `[earliest, latest]`；Start 规则要求提交时间戳 ≥ TT.now().latest，Commit Wait 规则要求等到 TT.after(s) 为真才返回客户端，以此保证**外部一致性**（等价于线性化）。
- 读写事务：使用 2PL 加锁 + 2PC 提交，跨美国约 100ms；只读事务：无锁、从本地足够新的副本读、无需 2PC，延迟低 10 倍。
- **快照隔离**：每条记录存多版本时间戳，只读事务按其开始时间戳读取对应版本，保证串行化同时不阻塞写事务。
- 99.9% 的事务是只读的（F1 负载），设计大量优化为只读路径提速是 Spanner 的核心取舍。

## 一、动机与背景

### 1.1 Google F1 的痛点

Spanner 的第一个客户是 Google F1——广告后台数据库。F1 此前将数据分片存储在多个 MySQL 和 BigTable 实例中，痛点明确：

| 需求 | 旧方案的问题 |
|------|------------|
| **跨分片事务** | MySQL 分片之间无原子提交 |
| **同步复制** | 副本之间一致性难以保证 |
| **强一致性** | BigTable 只提供单行事务，无外部一致性 |
| **低延迟读取** | 跨数据中心读取延迟高 |

工作负载特征（论文 Table 6）：**99.9% 的事务是只读事务**。这意味着只读事务的性能极为关键。

### 1.2 设计目标

::: definition Spanner 的三大目标
1. **全球分布**：数据跨数据中心复制，支持数百个数据中心、数百万台机器、数万亿行记录

2. **强一致性**：外部一致性（External Consistency）的读写事务 + 全局一致性快照读

3. **高性能只读**：只读事务无锁、从本地副本读取，延迟比读写事务低 10 倍
:::

---

## 二、系统架构

### 2.1 层次结构

```text
Universe（一次 Spanner 部署，全球只有少数几个）
  └── Zone（区域，管理部署的基本单位，类似一次 Bigtable 部署）
        ├── Zonemaster（负责将数据分配给 Spanserver）
        ├── Location Proxy（客户端用来定位数据所在的 Spanserver）
        └── Spanserver × 100~数千（实际服务数据）
              └── Tablet × 100~1000（数据存储单元）
                    └── Paxos 状态机（用于复制）
                          ├── Lock Table（Leader 上，管理 2PL 锁）
                          └── Transaction Manager（Leader 上，管理分布式事务）
```

- **Universe Master**：控制台，显示所有 Zone 状态，用于调试
- **Placement Driver**：后台任务，分钟级别跨 Zone 自动迁移数据

### 2.2 Spanserver 软件栈

每个 Spanserver 管理 100~1000 个 **Tablet**，每个 Tablet 实现的映射：

$$(\text{key: string}, \text{timestamp: int64}) \rightarrow \text{string}$$

与 Bigtable 的关键区别：Spanner 的 Tablet 存储**多版本数据**，每个版本对应一个时间戳。Tablet 的状态存储在 Colossus（GFS 继任者）上的 B-tree 文件 + 预写日志中。

每个 Tablet 上运行一个 **Paxos 状态机**：
- Paxos 使用**基于时间的 Leader 租约**（默认 10 秒），支持长期稳定的 Leader
- Leader 上有**锁表（Lock Table）**：管理 2PL 状态，将 key range 映射到锁状态
- Leader 上有**事务管理器（Transaction Manager）**：管理分布式事务（2PC 的 Participant Leader）

### 2.3 为什么选择这种架构？

::: insight 架构设计的权衡
• **分片**：并行化实现巨大总吞吐量

• **跨数据中心副本**：容忍整个站点故障

• **本地副本读取**：低延迟，驱动了 TrueTime 设计

• **Paxos 只需多数派**：容忍慢速/远程副本，不阻塞
:::

### 2.4 目录（Directory）抽象

::: definition 目录（Directory）
一组具有**相同键前缀**的连续键的集合，是 Spanner 数据移动的**基本单位**。同一目录中的所有数据共享相同的复制配置（副本数、地理位置等）。
:::

- 数据在 Paxos 组之间移动时，以**目录**为单位（而非整个 Tablet）
- 目录可被**共置（colocate）**到同一 Tablet，加速跨目录的联合访问
- **Movedir**：后台任务，在 Paxos 组之间移动目录；先后台迁移大部分数据，最后用一个小事务原子性完成剩余迁移，不阻塞正常读写
- 若目录过大，Spanner 将其拆分成多个 **Fragment**，由不同 Paxos 组服务

---

## 三、TrueTime API

这是 Spanner 最核心、最创新的设计。

### 3.1 问题：时钟不同步

分布式系统中，不同机器的时钟存在**漂移（skew）**，无法精确知道"现在的真实时间"。传统方案：
- NTP 同步：误差可达几十毫秒
- 逻辑时钟（Lamport Clock）：无法映射到真实时间

Spanner 的方案：**直接暴露时钟不确定性**，提供带误差区间的时间 API。

### 3.2 TrueTime API 定义

::: definition TrueTime API
| 方法 | 返回值 | 含义 |
|------|--------|------|
| `TT.now()` | `TTinterval [earliest, latest]` | 真实时间必定落在此区间内 |
| `TT.after(t)` | bool | 真实时间是否已经过了 t（即 t < earliest） |
| `TT.before(t)` | bool | 真实时间是否还未到 t（即 t > latest） |

保证：$t_{abs}(\text{now}) \in [TT.now().earliest, TT.now().latest]$
:::

### 3.3 TrueTime 的实现

- 每个数据中心部署**时间主服务器（Time Master）**，装备 **GPS 接收器**或**原子钟（铷钟/铯钟）**
- GPS 提供绝对时间参考，原子钟提供精确的频率基准（两者互为备份）
- 各 Spanserver 上的守护进程（timeslave daemon）每隔一段时间与多个 Time Master 同步
- 不确定性（$\epsilon$）通常 **< 10ms**，平均约 1~7ms

```text
典型的 TTinterval: [now - ε, now + ε]
其中 ε ≈ 1~7ms（实测），最差 < 10ms
```

::: insight TrueTime 的关键保证
真实时间**必定**落在返回的区间内。换言之，Spanner 不假装时钟是精确的，而是诚实地告知"时间不确定性的上界"，并在协议中利用这个上界做出正确决策。
:::

---

## 四、事务类型与并发控制

### 4.1 三种操作类型

| 类型 | 描述 | 需要锁 | 需要 2PC |
|------|------|--------|---------|
| **读写事务** | 读+写，使用 2PL + 2PC | 是 | 是（跨分片时） |
| **只读事务** | 预声明无写操作，快照读 | 否 | 否 |
| **快照读** | 指定过去某时间戳的只读操作 | 否 | 否 |

### 4.2 读写事务

**完整流程：**

1. 客户端选择唯一的事务 ID（TID）
2. 客户端将每个读取请求发送给相关分片的 **Paxos Leader**
   - Leader 的锁表中对相关记录加**读锁**（可能需等待）
   - 读锁**不通过 Paxos 复制**（Leader 失效 → 事务中止）
3. 客户端准备提交时，选择一个 Paxos 组作为 **2PC 协调者（TC）**
4. 客户端向各分片 Leader 发送写入请求
5. 每个写入分片 Leader（Participant Leader）：
   - 对写入记录加**写锁**
   - 通过 Paxos 将"prepare 记录"（包含锁状态和新值）复制到副本组
   - 通知 TC "已 prepared"
6. TC（Coordinator Leader）：
   - 若所有参与者都 prepared → 通过 Paxos 记录 COMMIT 决定
   - 通知所有参与者 Leader 和客户端
7. 每个参与者 Leader：
   - 通过 Paxos 将 TC 的决定复制到副本组
   - 执行写入，释放锁

::: insight 关键设计：2PC over Paxos
TC 和参与者都是 Paxos 副本组，内部有多个副本。TC Leader 崩溃时，Paxos 选出新 Leader 继续推进 2PC，**解决了传统 2PC 的阻塞问题**。代价是读写事务延迟较高（跨数据中心多次网络往返，约 100ms 跨美国）。
:::

### 4.3 只读事务

只读事务占 99.9% 的工作负载，是 Spanner 优化的重点。

**三个优化：**
1. **从本地副本读取**：避免跨数据中心消息（但本地副本可能不是最新的！）
2. **无锁**：不阻塞读写事务，读写事务也不阻塞它
3. **无 2PC**：不需要事务管理器协调

**代价**：需要解决正确性问题——如何在无锁、读过时副本的情况下保证可串行化和外部一致性？

#### 4.3.1 为什么不能直接读最新值？

考虑并发场景：

```text
T1: Wx Wy C           # 转账事务 1
T2:    Wx Wy C        # 转账事务 2
T3:       Rx    Ry    # 只读事务（读 x 时 T2 已提交，读 y 时 T2 还没提交？）
```

T3 若直接读最新值，可能读到 T2 写入的 x，但读到 T1 写入的 y——结果不符合任何串行顺序。

#### 4.3.2 快照隔离（Snapshot Isolation）

::: definition 快照隔离（SI）
给每个事务分配一个时间戳，只读事务读取该时间戳之前最新提交版本的数据。每个副本为每条记录存储多个带时间戳的版本。

• 读写事务时间戳 = 提交时间

• 只读事务时间戳 = 开始时间

• 执行结果等价于按时间戳顺序的串行执行
:::

**示意：**
```text
x 的版本历史：
  x@t=10: 100   ← T1 写入
  x@t=20: 101   ← T2 写入

只读事务 T3 时间戳 = 15：
  读 x → 得到 x@t=10 = 100  （只看 ≤ 15 的最新版本）
```

---

## 五、外部一致性与 Commit Wait

### 5.1 外部一致性定义

::: definition 外部一致性（External Consistency）
如果事务 $T_1$ 在事务 $T_2$ **开始之前**已经提交，那么 $T_2$ 的提交时间戳必须大于 $T_1$ 的提交时间戳。

形式化：
$$t_{abs}(e_1^{commit}) < t_{abs}(e_2^{start}) \Rightarrow s_1 < s_2$$

等价于线性化（Linearizability）在事务粒度上的保证。
:::

外部一致性比可串行化更强：它额外要求事务的串行顺序与**真实时间顺序**一致。若用户在浏览器 A 提交了转账，刷新浏览器 B 应该能看到——这就是外部一致性。

### 5.2 时间戳分配规则

为保证外部一致性，Spanner 使用两条规则：

**Start 规则**：TC 在收到提交请求（事件 $e_i^{server}$）后，为事务 $T_i$ 分配提交时间戳 $s_i$，要求：

$$s_i \ge TT.now().latest$$

即时间戳必须不早于当前 TrueTime 的**上界**，确保 $s_i$ 不会被当成"过去的时间"。

**Commit Wait 规则**：TC 必须等待，直到真实时间已经过了 $s_i$：

$$\text{等待直到 } TT.after(s_i) = \text{true}$$

即等待直到 $TT.now().earliest > s_i$，此时可以确信 $s_i < t_{abs}(\text{now})$。

### 5.3 外部一致性的证明

$$
\begin{align*}
(1)\quad & s_1 < t_{abs}(e_1^{commit}) & \text{（Commit Wait 规则）} \\
(2)\quad & t_{abs}(e_1^{commit}) < t_{abs}(e_2^{start}) & \text{（假设 T2 在 T1 提交后开始）} \\
(3)\quad & t_{abs}(e_2^{start}) \le t_{abs}(e_2^{server}) & \text{（因果性）} \\
(4)\quad & t_{abs}(e_2^{server}) \le s_2 & \text{（Start 规则）} \\
\hline
& \therefore\quad s_1 < s_2 & \text{（传递性）}
\end{align*}
$$

::: insight Commit Wait 的代价与收益
代价：读写事务必须等待约 $2\epsilon$（两倍时间不确定性，约 2~14ms）才能释放结果给客户端。

收益：保证了全局时间戳的单调性，使后续事务的时间戳必然更大，外部一致性得以保证。

TrueTime 的不确定性越小（$\epsilon$ 越小），Commit Wait 等待越短，性能越高。
:::

### 5.4 Paxos Leader 租约与单调性

**单调性不变式**：每个 Paxos 组内，所有 Paxos 写入的时间戳必须单调递增（即使换了新 Leader）。

保证方式：利用**租约区间不重叠（Disjointness Invariant）**——任意两个 Leader 的租约时间区间不重叠，因此每个 Leader 只在自己的租约区间内分配时间戳，自然单调。

Leader 退位时，必须等待 $TT.after(s_{max}) = \text{true}$（$s_{max}$ 为该 Leader 使用过的最大时间戳），确保新 Leader 分配的时间戳不会小于旧 Leader 的最大值。

---

## 六、只读事务的时间戳选择

### 6.1 目标

只读事务需要选择一个时间戳 $t_{read}$，使得：
- 读取到的是 $t_{read}$ 时刻前最新提交的版本（可串行化）
- 如果 T1 在 T3 开始前提交，T3 必须看到 T1 的写入（外部一致性）

### 6.2 时间戳选择策略

**简单策略**：$t_{read} = TT.now().latest$

- 保证读取到所有已提交事务（因为任何已提交事务的 $s_i \le t_{read}$）
- 但可能需要等待：副本上的数据可能还没应用到该时间戳

**safe time 机制**：每个副本维护一个 $t_{safe}$，表示该副本已经应用到的最大时间戳。只读事务在某副本上的读取条件：

$$t_{read} \le t_{safe}$$

若 $t_{read} > t_{safe}$，需等待副本追上（或换一个更新的副本）。

### 6.3 从本地副本读取的正确性

本地副本可能不是 Paxos 多数派成员，数据可能比 Leader 滞后。但只要 $t_{read} \le t_{safe}$，该副本上该时间戳之前的所有写入都已应用，读取结果是正确的——这正是多版本存储的价值所在。

::: insight 只读事务为什么不需要锁？

A：只读事务读取的是历史快照（某个时间戳之前的版本），历史数据是不可变的，不会被读写事务修改。因此读写事务和只读事务之间不存在数据竞争，无需加锁。
:::

---

## 七、性能数据（论文 Table 3 & 6）

| 事务类型 | 跨城市延迟 | 跨大洲延迟 |
|----------|-----------|-----------|
| **读写事务** | ~14ms | ~100ms |
| **只读事务** | ~1.4ms | ~10ms |

只读事务比读写事务快约 **10 倍**，这对于 99.9% 只读的工作负载意义重大。

---

## 八、Spanner 设计权衡总结

::: insight Spanner 牺牲了什么来换取外部一致性？

1. **Commit Wait 延迟**：读写事务必须等待 $2\epsilon$，约 2~14ms

2. **专用硬件**：需要 GPS 接收器和原子钟才能将 $\epsilon$ 控制在 10ms 以内

3. **系统复杂性**：TrueTime API、commit wait 逻辑、多版本存储都增加了实现复杂度

换取的收益：全球范围内的强一致性，同时只读事务几乎无额外开销。
:::

::: insight 若 TrueTime 时钟不准确，会发生什么？

若某服务器的时钟偏快（$\epsilon$ 被低估），可能分配出大于真实时间的时间戳，导致另一个真实上后发生的事务得到更小的时间戳——外部一致性被破坏。Spanner 通过维护多个独立的时间源（GPS + 原子钟互为备份）来检测并隔离错误的时间服务器。
:::

::: insight Spanner 中 2PC 的阻塞问题是如何解决的？

传统 2PC 的 TC 是单点，TC 崩溃导致参与者无限期阻塞。Spanner 将 TC（Coordinator Leader）和参与者都实现为 Paxos 副本组：

• TC Leader 崩溃 → Paxos 在租约到期后选出新 Leader，新 Leader 从 Paxos 日志中恢复 2PC 状态，继续推进

• 不会无限期阻塞，只会短暂延迟（租约超时时间，约 10s）
:::

---

## 本讲小结

::: insight 核心要点

1. **Spanner 的核心创新**：TrueTime（暴露时钟不确定性）+ Commit Wait（等待时间戳成为确定过去）→ 实现全球外部一致性

2. **架构**：Universe > Zone > Spanserver > Tablet > Paxos 状态机；每个分片一个 Paxos 组

3. **读写事务**：2PL（锁） + 2PC（原子提交） + Paxos（每个参与者内部复制）；慢但强一致

4. **只读事务**：无锁 + 本地副本 + 快照隔离；快（10x）但需要正确选择时间戳

5. **外部一致性**：Start Rule（$s_i \ge TT.now().latest$）+ Commit Wait（等待 $TT.after(s_i)$）共同保证 $s_1 < s_2$ 当 T1 先完成

6. **影响**：Spanner 证明了全球范围强一致性分布式事务是可行的，影响了 CockroachDB、YugabyteDB 等后续系统
:::

## 论文阅读：全球分布式数据库 Spanner

[Spanner: Google’s Globally-Distributed Database, OSDI 2012](https://pdos.csail.mit.edu/6.824/papers/spanner.pdf)

## 本讲导览

Spanner 是谷歌可扩展，多版本，全球分布式并支持同步复制的数据库。它是第一个在全球范围内分布数据并支持外部一致性（externally-consistent）的分布式事务的系统。本文描述了 Spanner 的架构、功能特性、各项设计决策背后的基本原理/动机，以及一个暴露时钟不确定性的新颖时间 API。该 API 及其实现对实现外部一致性以及一系列强大特性至关重要： **在过去时间点进行非阻塞读取，无锁的只读事务以及跨 Spanner 示例的原子性的 schema 变更。**

## 1. 引言

Spanner 是一个由 Google 设计，构建和部署的可扩展的全球分布式数据库。从最高层的抽象来看，**它是一个将数据分片存储在全球数据中心的多组 Paxos 状态机的数据库**。复制技术用于实现全球可用性（availability） 和地理位置局部性（geographic locality）；客户端可以在副本之间自动故障转移（failover）。随着数据量或服务器数量的变化，Spanner 会自动在机器之间重新分片数据，并且会自动在机器之间（甚至跨数据中心）迁移数据以实现负载均衡和响应故障。Spanner 的**设计目标**是扩展到**数百个数据中心的数百万台机器，支持数万亿行数据库记录**。

Spanner 的首个客户是 F1，这是 Google 广告后台的重写版本。F1 使用了分布在美国境内的五个副本。大多数其他应用则可能会选择在一个地理区域内的 3 到 5 个数据中心之间复制数据，这些数据中心具有相对独立的故障模式。换句话说，大多数应用会在更低延迟与更高可用性之间选择前者，只要能在 1 至 2 个数据中心故障的情况下继续运行。

**Spanner 的主要关注点是管理跨数据中心复制的数据**。尽管许多项目都乐于使用 Bigtable [9]，但我们也经常收到用户的抱怨，说 Bigtable 对某些类型的应用程序来说可能难以使用。 具体来说，具有复杂、和不断演进的 schema 的，或是在大范围复制情况下**需要强一致性的应用程序**。Google 的许多应用程序还是选择使用了 Megastore [5] ， 虽然它写入吞吐量相对较差，但由于其半关系型数据模型和对同步复制的支持。因此，Spanner 已经从类似 Bigtable 的版本化键值存储演变成了一个时态多版本数据库。数据存储在模式化的半关系型表中；数据是版本化的，每个版本都会自动用其提交时间打上时间戳；旧版本的数据受可配置的垃圾回收策略管理；应用程序可以读取旧时间戳的数据。**Spanner 支持通用事务，并提供基于 SQL 的查询语言**。

作为一个全球分布式数据库，Spanner 提供了几个有趣的特性。首先，应用程序可以在细粒度层面上动态控制数据的复制配置。应用程序可以指定约束条件来控制哪些数据中心包含哪些数据、数据距离用户有多远（以控制读取延迟）、副本之间的距离有多远（以控制写入延迟），以及维护多少个副本（以控制持久性、可用性和读取性能）。系统还可以动态且透明地在数据中心之间移动数据以平衡数据中心之间的资源使用。

其次，Spanner 具有两个在分布式数据库中难以实现的特性：**它提供外部一致性 [16] 的读写操作**，以及在**某个时间戳上对整个数据库进行全局一致性读取的能力**。这些特性之所以能够实现，是因为尽管事务可能是分布式的，但 Spanner 为事务分配了具有全局意义的提交时间戳。这些时间戳反映了序列化顺序。此外，序列化顺序满足外部一致性（或等效地，线性化 [20]）：如果事务 T1 在另一个事务 T2 开始之前提交，那么 T1 的提交时间戳小于 T2 的时间戳。Spanner 是第一个在全球范围内提供此类保证的系统。

**这些特性的关键是新的 TrueTime API 及其实现**。该 API 直接暴露时钟不确定性，Spanner 时间戳的保证取决于实现提供的界限。如果不确定性较大，Spanner 会放慢速度以等待不确定性消失。Google 的集群管理软件提供了 TrueTime API 的实现。通过使用多个现代时钟参考（GPS 和原子钟），该实现将不确定性保持在较小的范围内（通常小于 10ms）。

各部分内容安排如下：

- **第 2 节**：介绍 Spanner 的实现结构、功能特性和设计决策；
- **第 3 节**：描述新的 TrueTime API 及其实现概览；
- **第 4 节**：讲述 Spanner 如何利用 TrueTime 实现外部一致性事务、无锁只读事务和原子模式更新；
- **第 5 节**：展示 Spanner 的性能基准测试与 TrueTime 的行为表现，并分享 F1 项目的使用经验；
- **第 6、7、8 节**：探讨相关工作、未来方向，并总结全文。

## 2. 实现

本节描述了 Spanner 的实现的结构及其背后的基本原理。然后描述了**目录（directory）**抽象，它用于管理复制和局部性，并且是数据移动的基本单位。最后，描述了我们的数据模型、解释了为什么 Spanner 看起来像是关系型数据库而不是键值存储，以及应用程序如何控制数据局部性。

Spanner 的一次部署被称为一个**"宇宙"（universe）**。鉴于 Spanner 在全球范围内管理数据，运行中的 universe 数量将会很少。我们目前运行着一个测试/试验宇宙、一个开发/生产宇宙和一个仅用于生产的宇宙。

Spanner 被组织为一组**区域（zone）**，其中每个区域大致类似于 Bigtable 服务器 [9] 的一次部署。区域是管理部署的基本单位。区域集合同时也是数据可以在其间进行复制的位置集合。当新的数据中心投入使用或旧的数据中心关闭时，可以向运行中的系统添加或移除区域。区域也是物理隔离的单位：例如，在同一个数据中心中可能有一个或多个区域，这种情况出现在不同应用程序的数据必须在同一数据中心的不同服务器集合之间进行分区时。

![image-20241117101714092](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6739522ca3a3d.png)

图一展示了 Spanner universe 中的服务器的组织结构。一个区域有一个区域主控（zonemaster），和 100 到几千个 spannerver。前者负责将数据分配给 spanserver; 后者负责将客户端提供数据服务。每个区域的**位置代理（location proxy）**被客户端用来定位被分配来服务其数据的 spanserver。

**宇宙主控服务器（universe master）**和**位置驱动器（placement driver）**目前是单例的。universe master 主要是一个控制台，用于显示所有区域的状态信息以进行交互式调试。位置驱动器处理跨区域的自动数据移动，这种移动的时间尺度是分钟级的。位置驱动器会定期与 spanserver 通信，以找出需要移动的数据，这种移动可能是为了满足更新后的复制约束或者是为了平衡负载。

由于篇幅原因，我们将只详细描述 spanserver。

### 2.1 Spanserver 软件栈

![image-20241117173534542](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6739b8e8d8e0f.png)

本节重点介绍 spanserver 的实现，以说明如何将复制和分布式事务层叠在我们基于 Bigtable 的实现上。软件栈如图 2，在最底层，每个 spanserver 负责管理 100 到 1000 个称为**tablet**的数据结构实现。类似于 Bigtable 的 tablet 抽象，它实现了以下映射的集合：
$$
(key: string, timestamp: int64) \rightarrow string
$$
与 Bigtable 不同的是，Spanner 为数据分配时间戳，这是 Spanner 更像多版本数据库而不是键值存储的一个重要特征。**tablet 的状态存储在一组 B-tree-like 的文件和预写日志中，这些文件都位于名为 Colossus 的分布式文件系统上**（这是 GFS 的继任者）

为了支持复制，每个 spanserver 在每个 tablet 之上实现了一个 Paxos 状态机。（Spanner 的早期版本在每个 tablet 上支持多个 Paxos 状态机，这允许更灵活的复制配置。但该设计的复杂性让我们放弃了。）每个状态机将其元数据和日志存储在其对应的 tablet 中。我们的**Paxos 实现支持基于时间的长期 Leader 租约，每个租约为 10 秒**。当前的 Spanner 实现对每个 Paxos 写入两次日志记录：一次在 tablet 日志中，一次在 Paxos 日志中。这个选择处于权宜之计，我们可能最终会改进。我们的 Paxos 实现是流水线式的，以便在广域网延迟的情况下提高 Spanner 的吞吐量：但是写入是通过 Paxos 按顺序生效的（这是我们在第 4 节中将依赖的一个事实）。

Paxos 状态机用于实现一个一致复制的映射集合。每个副本的键值映射状态存储在其对应的 tablet 中。写操作必须在 leader 发起 Paxos 协议；读操作则可以直接从任意一个**足够新**的副本底层 tablet 读取状态。这些副本的集合共同构成一个 **Paxos 组（Paxos group）**。

在每个作为 Leader 的副本上，每个 spanserver 都实现了一个**锁表（lock table）**来实现并发控制。锁表中保存着两阶段锁（two-phase locking）的状态信息：它将键区间（ranges of keys）映射到锁状态（lock states）。（注意，让 Paxos leader 长时间存活对于高效管理锁表是至关重要的）。在 Bigtable 和 Spanner 中，我们都需要支持**长事务（long-lived transactions）**（例如生成报表的操作，可能持续几分钟），而这种事务在存在冲突时，如果采用乐观并发控制（OCC）会表现很差。因此，那些需要同步的操作（例如事务性读操作）会在锁表中获取锁； 而其他不需要同步的操作则会绕过锁表。

在每一个作为 leader 的副本 上，每个 spanserver 还实现了一个 事务管理器（transaction manager），用于支持分布式事务。事务管理器用于实现一个 参与者 leader（participant leader）； 而该组中的其他副本则称为 参与者从节点（participant slaves）。如果一个事务只涉及单个 Paxos 组（大多数事务属于这种情况）， 它可以绕过事务管理器，因为锁表和 Paxos 一起就能保证事务性。但如果一个事务涉及多个 Paxos 组，这些组的 leader 之间就需要协调， 执行 两阶段提交（2PC）。在这些参与者组中，会选出一个组作为 协调者（coordinator）： 该组的 leader 被称为 协调者 leader（coordinator leader）， 而该组的从节点称为 协调者从节点（coordinator slaves）。每个事务管理器的状态都会存储在其底层的 Paxos 组中， 因此，这些状态信息同样是被复制的（replicated）。

###  2.2 目录与数据放置

在 KV 集合之上，Spanner 提供了一种称为目录（Directory）的分桶抽象（bucketing abstraction），一个目录是一组具有相同前缀的连续键；支持目录机制的好处是：应用可以通过精心选择键来控制数据的局部性。

一个目录中的所有数据具有相同的复制配置（replication configuration）。当数据在 Paxos 组之间移动时，Spanner 是以目录为基本单位移动的。图 3 所示。Spanner 可能出于以下原因移动某个目录：

- 从一个 Paxos 组中转移部分负载；
- 将经常一起被访问的目录放到同一个组里；
- 或者将目录移动到**更靠近访问者**的组中。

目录的移动不会中断客户端操作 一个 50MB 大小的目录通常可以在几秒内完成迁移。

![image-20251010110918623](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20251010110918623.png)

由于一个 Paxos 组中可能包含多个目录，这意味着： Spanner 的 tablet 不同于 Bigtable 的 tablet。Bigtable 的 tablet 通常是按字典序连续的一个键空间分区，而 Spanner 的 tablet 是一个容器（container），它可以封装多个行空间分区（partitions of the row space）。我们做出这种设计，是为了能够将多个经常一起被访问的目录共置（colocate）到同一 tablet 中。

**Movedir** 是 Spanner 的后台任务，用于在 Paxos 组之间移动目录。 它还用于增加或删除 Paxos 组的副本， 因为目前 Spanner 还不支持 Paxos 内部的动态配置更改。Movedir 不是一个单独的事务，以避免在大规模数据移动时阻塞正在进行的读写操作。相反，Movedir 首先注册一个“即将移动”状态，然后在后台逐步移动数据。当绝大部分数据已经迁移完毕，只剩下少量数据时，它会使用一个事务原子性地完成剩余数据的移动， 并更新两个 Paxos 组的元数据。

一个目录也是应用可以单独指定**地理复制属性（geographic-replication properties）**的最小单位， 简称为目录的 **放置（placement）**。

Spanner 的放置规格语言（placement-specification language）将复制配置的管理职责划分为两部分：

**系统管理员（administrators）**控制以下两个维度：

- 副本的数量与类型；
- 副本的地理放置位置。 他们会定义这些维度下的命名选项（例如：
   “North America, replicated 5 ways with 1 witness”——北美地区，5 个副本，1 个见证节点）。

**应用程序（applications）**通过给数据库或单个目录打标签，
 使用这些选项的组合，来控制数据如何被复制。

例如，一个应用可以将每个用户的数据放在单独的目录中：这样用户 A 的数据可以有三个副本位于欧洲，而用户 B 的数据可以有五个副本位于北美。为了便于说明，上述描述进行了简化。 实际上，如果一个目录增长过大，Spanner 会将其分片（shard）成多个片段（fragments）。 这些片段可以由不同的 Paxos 组（也就是不同的服务器）提供服务。 因此，Movedir 实际上移动的单位是目录片段（fragments），而不是整个目录。

## 4. 并发控制

我们介绍 TrueTime 如何确保正确性，且如何实现外部一致性、无锁只读事务和非阻塞历史读。这些特性可以在时间戳 t 进行全库审计读取（audit read）：将精确反映出截止时间 t 已经提交的所有事务的效果。

接下来，需要区分两种写操作。Paxos 写入，是指 Paxos 协议层执行的写操作。Spanner 客户端写入，是指用户或应用层发起的写操作。

### 4.1 时间戳管理

![image-20251010153936815](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20251010153936815.png)

表 2 列出了 Spanner 支持的操作类型。Spanner 支持读写事务、只读事务（预声明的快照隔离事务）、和快照读——对过去时间点的只读操作。前两者系统自动重试，客户端你无需编写重试逻辑。

**只读事务（Read-Only Transactions）**是一种享有快照隔离性能优势的事务，必须预先声明该事务不会有写操作。制度实物中的所有读操作在系统选定的某个时间戳下执行，无需加锁，因此不会阻塞正在执行的写入操作。这种事务可以在任意一个**足够新**的副本上执行

**快照读（Snapshot Reads）**是指过去的某个时间点的只读操作，也不需要加锁。客户端可以直接指定时间戳，或者指定最大允许的时间滞后，由 Spanner 自行选择时间戳。无论那种，都需要在足够新的副本上执行。

对于只读事务和快照读来说，一旦时间戳被确定，提交是不可避免的。除非该时间戳对应的数据已被垃圾回收（GC）。因此客户端可以避免在重试循环中缓冲结果。当服务器发生故障时， 客户端只需在另一个服务器上使用相同的时间戳和当前读取位置继续查询即可。

#### 4.1.1 Paxos Leader 租约

Spanner 的 Paxos 实现使用定时租约来确保 leader 能长时间存活（默认 10 秒）。潜在的 leader 会发送请求以获取租约投票；当它获得了法定多数（quorum）的租约投票后，就知道自己拥有租约。副本在每次写入时会隐式延长它的租约投票，而当租约快到期时，leader 会请求延长租约投票。 leader 的租约间隔从获得多数投票开始到失去多数投票结束。Spanner 依赖以下 **不相交不变式（disjointness invariant）**：即任意两个 leader 的租约区间是互不重叠的。（附录 A 有描述如何保证不变式）

Spanner 允许 Paxos leader **主动退位（abdicate）**， 方法是让其从节点释放对它的租约投票，但是 Spanner 限制了退位的时机。我们定义$s_{max}$为 leader 已使用的最大时间戳，在退位之前，leader 必须等待直到：$TT.after(s_{max})$为 True

#### 4.1.2 为读写事务分配时间戳

事务性的读写操作使用 2PL，因此，在一个事务中，系统可以在所有锁都已获得、但尚未释放时分配时间戳。 因此，在一个事务中，系统可以在所有锁都已经获得、但未释放时分配时间戳。对于某个事务，Spanner 会将其提交时间戳设置为 Paxos 写入的时间戳。

Spanner 依赖以下单调性不变式： 在每个 Paxos 组内，所有 Paxos 写入的时间戳必须单调递增，即使换了新的 Leader，也要保持递增。对于单一 Leader 节点，这个要求是显然成立的；而在多个 leader 之间（即 leader 更换的场景下）这个不变式利用租约区间不重叠得以保证。每个 Leader 只能在其租约时间区间内分配时间戳。此外，每当一个新时间戳 `s` 被分配时， 系统会将 $s_{max}$ 更新为 `s`，以维持区间不重叠的保证。

Spanner 还需要保持以下外部一致性不变式： 如果事务 T2 的开始时间在事务$T_1$提交时间之后，那么$T_2$的时间戳必须大于$T_1$的提交时间戳。形式化表达如下：假设事务$T_i$的开始时间为$e^{start}_i$，提交时间为$e^{commit}_i$，提交时间戳为$s_i$，则有
$$
t_{abs}(e^{commit}_1) < t_{abs}(e^{start}_2) ⇒ s_1 < s_2
$$
为保证上述不变式，Spanner 的事务执行与时间戳分配遵循以下两条规则。设事务$T_i$的提交请求到达协调者 leader 的事件为$e^{server}_i$。

**Start 规则** 协调者 Leader 在收到提交请求（即$e^{server}_i$事件）后，会为事务$T_i$分配一个提交时间戳$s_i$， 要求
$$
s_i \ge TT.now().latest
$$
也就是说，事务的提交请求时间戳必须不早于当前的 TrueTime 上确界。

**Commit Wait 规则** 协调者 Leader 必须确保，客户端在 TrueTime 确认已经过了提交时间戳$s_i$之前，不能看到事务$T_i$的提交结果。换言之，必须等待直到：$TT.after(s_i)$ == true，这确保 $s_i$ 小于事务的实际提交时间：$s_i \lt t_{abs}(e^{commit}_i)$

证明：
$$
\begin{align*}
(1)\ & s_1 < \mathrm{t_abs}(e^{commit}_1) && \text{(由 Commit Wait 规则)} \\
(2)\ & \mathrm{t_abs}(e^{commit}_1) < \mathrm{t_abs}(e^{start}_2) && \text{(假设)} \\
(3)\ & \mathrm{t_abs}(e^{start}_2) \le \mathrm{t_abs}(e^{server}_2) && \text{(因果性)} \\
(4)\ & \mathrm{t_abs}(e^{server}_2) \le s_2 && \text{(由 Start 规则)} \\
\hline
& \therefore\ s_1 < s_2 && \text{(传递性)}
\end{align*}
$$

#### 4.1.3 在给定时间戳上提供读服务

前一节提到的单调性不变式使 Spanner 能够判断一个副本是否足够新，从而是否可以在某个时间戳 `t` 上提供一致的读取。
