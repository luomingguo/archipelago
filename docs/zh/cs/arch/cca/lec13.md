---
title: 缓存一致性
type: lecture
lecture: 13
tags: [cache-coherence, msi-protocol, directory-coherence, coherence-invariants, multicore-architecture]
status: complete
---
# Lec 13 缓存一致性

## TL;DR

- 缓存一致性旨在确保多核私有 L1 缓存中副本的一致视图，保证“单写多读（SWMR）”不变量。
- MSI 状态机定义了修改（M）、共享（S）与无效（I）状态，基于目录的协议以点对点消息消除全系统总线广播。
- BSV 实现利用上行（c2m）与下行（m2c）消息队列隔离客户端请求与父节点降级作废命令。
- 客户端与目录控制器拆解为解耦状态机规则，通过自愿降级（PutS/PutM）与被动转发（Fwd-GetS/Inv）协同推进。

> MIT 6.1920 · Constructive Computer Architecture
> 讲师：Arvind · 日期：2024-04-02

## 1. 缓存一致性问题

::: definition
**定义 — 缓存一致性问题（*Cache Coherence Problem*）**

多处理器系统中，每个核心有私有 L1 缓存。当核心 A 修改了变量 x，核心 B 的缓存中仍可能持有 x 的旧值。若不加处理，两个核心对同一内存地址将看到不同的值，违反一致性。
:::

**一致性需求**：同一地址的任意两次写操作，所有处理器看到的顺序相同；读操作返回最近一次写操作的值。

---

## 2. MSI 协议

::: definition
**定义 — MSI 状态机（*Modified-Shared-Invalid*）**

每个缓存行有三种状态：

- **M（*Modified*）**：本缓存独占该行，且数据已修改（与内存不同）。可读写，无需通知其他核。

- **S（*Shared*）**：本缓存有该行的只读副本，可能有其他核也持有 S 副本。可读，写时必须升级。

- **I（*Invalid*）**：本缓存没有该行的有效副本。任何访问都是缺失。
:::

**状态转换（核心视角）**：

| 当前状态 | 事件 | 动作 | 新状态 |
|--------|------|------|--------|
| I | 处理器 Load | 发送 GetS，等待数据 | S |
| I | 处理器 Store | 发送 GetM，等待数据 | M |
| S | 处理器 Store | 发送 UpgradeM，作废其他 S | M |
| M | 收到 Inv（目录要求降级）| 写回数据 | I 或 S |

---

## 3. 基于目录的缓存一致性（*Directory-Based Coherence*）

::: definition
**定义 — 目录（*Directory*）**

目录是一个集中式数据结构，为每个内存行记录：哪些缓存持有该行的副本（*sharers*），以及当前的状态（M/S/I）。目录位于内存控制器附近，负责协调所有一致性消息，避免总线广播（可扩展到多核）。
:::

**目录消息类型**：
- 核 → 目录：`GetS`（读请求）、`GetM`（写请求）、`PutS`（自愿降级）、`PutM`（写回 M 行）
- 目录 → 核：`Fwd-GetS`（转发读请求）、`Inv`（作废）、`Data`（数据响应）
- 核 → 核：`Data`（点对点数据转发）

---

## 4. BSV 缓存一致性实现

在 BSV 中实现目录式缓存一致性协议，核心在于通过独立的硬件通道与严格的规则解耦，规避多核系统中极易发生的协议级死锁。

### 4.1 两个方向的消息队列

为了防止请求与响应在同一物理队列中产生环路等待死锁，微架构显式划分双向通信信道：

```bsv
// 上行（核 → 目录）
FIFO#(CacheMsg)  c2m <- mkFIFO;   // cache to memory

// 下行（目录 → 核）
FIFO#(CacheMsg)  m2c <- mkFIFO;   // memory to cache
```

**信道解耦与死锁规避**：
- **上行请求信道（`c2m`）**：仅承载由本地处理器触发的一致性请求（如 `GetS`, `GetM`, `PutS`, `PutM`）。
- **下行响应与转发信道（`m2c`）**：承载来自目录控制器的一致性应答（数据填充 `Data`）以及来自其他核的被动转发介入（如作废通知 `Inv`、读转发 `Fwd-GetS`）。双通道在硬件上使用独立的物理 FIFO 或片上网络虚通道（Virtual Channel），从拓扑上打破循环等待条件。

### 4.2 关键规则（客户端 / 核心侧）

客户端缓存控制器被建模为响应外部事件与本地流水线请求的分布式状态机：

```bsv
rule startMiss (mshr == Ready && cacheMiss);
    c2m.enq(CacheMsg{type: GetS/GetM, addr: missAddr});
    mshr <= SendFillReq;
endrule

rule sendFillReq (mshr == SendFillReq);
    mshr <= WaitFillResp;
endrule

rule waitFillResp (mshr == WaitFillResp);
    let msg = m2c.first; m2c.deq;
    // 填充缓存行，更新 MSI 状态
    mshr <= Ready;
endrule

rule parentResp;  // 处理目录发来的 Fwd/Inv
    let msg = m2c.first; m2c.deq;
    // 修改本地 MSI 状态，可能需要发送 Data 给另一核
endrule
```

**客户端各状态规则的硬件行为**：
- **`startMiss`（缺失发起）**：当发生本地未命中时，MSHR 锁定当前地址，构造 `GetS`（读缺失）或 `GetM`（写缺失）协议包压入 `c2m`，核心暂时挂起。
- **`waitFillResp`（响应接收）**：当代管目录完成冲突协调并将 `Data` 消息压入 `m2c` 时，该规则触发，读取新行并更新本地 Tag 与 MSI 状态位，最后将 MSHR 释放回 `Ready`。
- **`parentResp`（父节点干预处理）**：这是一个并发运行的被动规则。当其他核心请求写该行时，目录会向本核心下发 `Inv`（作废）；若本核心持有 M 行，目录会下发 `Fwd-GetS`。该规则在后台原子降级本地状态，并将最新脏数据转发给请求核，保证跨核访问的强一致性。

### 4.3 关键规则（目录 / 父节点侧）

目录控制器位于片上互联网络的中心节点，维护全局一致性状态矩阵：

```bsv
rule dwn;     // 目录降级请求（downgrade）
    // 向持有 M 行的核发送 Fwd 或 Inv
endrule

rule dwnRsp;  // 收到核的降级响应
    // 更新目录状态，转发数据
endrule

rule dng;     // 自愿降级（voluntary downgrade）
    // 核主动发 PutS/PutM，目录更新 sharer 列表
endrule
```

**目录规则的仲裁逻辑**：
目录通过位图（Sharer Bitmask）记录每个缓存行的持有者。当收到 `GetM` 时，目录遍历位图，向所有持有只读 S 副本的核心并发下发 `Inv` 消息；只有在收集完所有核心的作废确认后，才将独占写权限（M 状态）授予请求核心。

---

## 5. 8 种一致性场景

::: example 例题 — GetS 命中 M 状态行

:::

场景：核 A 持有 M 状态（独占写），核 B 发送 GetS 读请求。

1. 核 B 发 `GetS` → 目录
2. 目录发 `Fwd-GetS` → 核 A（"把数据转给 B"）
3. 核 A 将缓存行状态降为 S，发 `Data` → 核 B，发 `PutM-Ack` → 目录
4. 目录更新：sharer = {A, B}，状态 = S
5. 核 B 收到 `Data`，状态置为 S

Sol：目录协议避免了广播，仅涉及 A、B、目录三方的点对点消息。

---

## 6. 协议不变量

::: theorem 推论 — MSI 不变量
任意时刻，对于同一地址：（1）至多一个缓存处于 M 状态；（2）若有缓存处于 M 状态，则所有其他缓存必须处于 I 状态；（3）处于 S 状态的缓存中的数据必须与内存（或 M 行）一致。BSV 实现中可以通过断言（*assertion*）在仿真中验证这些不变量。
:::

---

## 核心机制小结与一致性协议权衡

MSI 三状态协议通过 M→S→I 的状态转换维持缓存一致性；基于目录的实现用点对点消息替代总线广播，可扩展到众核；BSV 用独立规则实现目录的每个动作（startMiss、sendFillReq、parentResp、dwn 等），自然对应协议状态机；实际处理器（Intel/AMD）使用 MESI 或 MOESI 协议，添加了 Exclusive 和 Owned 状态以减少无效写缺失。

## 核心机制思考与底层洞察

::: insight 单写多读（SWMR）不变量与基于目录的可扩展性哲学
缓存一致性协议是计算机架构中状态机复杂度与形式化验证要求最高的领域，其演进体现了对物理互联特性的深刻洞察：

1. **总线监听（Snooping）的可扩展性死胡同**：在小型多核系统（如 4–8 核）中，监听总线（Snooping Bus）依赖物理连线的全核广播。然而总线是一种严格共享且电容负载巨大的物理介质，每次读写缺失都强迫全芯片所有核心比对本地缓存标签（Tag）。当核心数攀升至 16、64 乃至更多时，总线带宽迅速饱和，广播流量直接压垮系统。
2. **目录协议将空间广播收敛为定点点对点通信**：基于目录（Directory）的体系结构将一致性控制权下沉为一套精确的跟踪元数据。目录记录了每一个缓存行当前全局的拥有者和只读共享者集合（Sharers List）。发生缺失时，消息仅在请求核、目录与受影响的核心之间点对点定向路由，使得片上网络流量与系统核心总数解耦，为成百上千核的大规模数据中心处理器奠定了通信基础。
3. **BSV 规则对复杂协议状态机的数学固化**：在传统 HDL 中，一致性协议最致命的隐患是并发瞬态（Transient States）下的死锁与竞争冒险（例如发起请求的同时收到远端作废命令）。BSV 的守卫规则模型（Guarded Rules）将每个状态迁移封装为独立的原子事务，编译器自动完成输入队列保护与状态合法性校验，使得设计者能够用离散数学的方式验证“单写多读（Single-Writer, Multiple-Readers, SWMR）”不变量，从根源上杜绝了隐蔽的时序协议死锁。
:::
