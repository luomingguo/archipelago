---
title: 缓存与存储缓冲区
type: lecture
lecture: 7
tags: [cache, memory-hierarchy, locality]
status: complete
---
# Lec 07 缓存与存储缓冲区
> MIT 6.1920 · Constructive Computer Architecture
> 讲师：Arvind / Thomas Bourgeat · 日期：2024-03-07

## TL;DR

- 缓存利用时间局部性和空间局部性，用较小的 SRAM 层隐藏 DRAM 的高访问延迟。
- 阻塞缓存通过缺失状态机完成写回与填充；存储缓冲区让 Store 不必同步等待缓存处理。
- 直接映射缓存实现简单但易发生冲突缺失，组相联以更多标签比较和置换逻辑换取更低的冲突率。

## 1. 存储器层次结构

::: definition
**定义 — 存储器层次（*Memory Hierarchy*）**

$$\text{容量}：\text{RegFile} \ll \text{SRAM（Cache）} \ll \text{DRAM}$$
$$\text{延迟}：\text{RegFile} \ll \text{SRAM} \ll \text{DRAM}$$
处理器通过利用**时间局部性**（*temporal locality*）和**空间局部性**（*spatial locality*）将热数据保留在快速 SRAM（缓存）中。
:::

**缓存命中（*hit*）**：数据在缓存中，低延迟返回。  
**缓存缺失（*miss*）**：数据不在缓存，需访问 DRAM，高延迟。

---

## 2. 直接映射缓存（*Direct-Mapped Cache*）

地址字段划分（字节地址，行大小为 $2^L$ 字）：

$$\underbrace{[31 \quad \cdots \quad L+\log_2 N+2]}_{\text{Tag}} \underbrace{[L+\log_2 N+1 \quad \cdots \quad L+2]}_{\text{Index}} \underbrace{[L+1 \quad \cdots \quad 2]}_{\text{Offset}} \underbrace{[1 \quad 0]}_{\text{字节}}$$

```bsv
function CacheIndex getIndex(Addr addr) = truncate(addr >> (2 + valueOf(logLineSz)));
function CacheTag   getTag(Addr addr)   = truncateLSB(addr);
```

**缺陷**：步长 = 缓存大小的访问模式会产生大量冲突缺失（*conflict miss*）。

---

## 3. 阻塞缓存 BSV 实现

阻塞缓存将复杂的存储器缺失处理过程显式建模为离散状态机的迁移序列：当检测到缓存缺失时，缓存暂停接受来自 CPU 核心的新请求，按序将旧的脏行写回主存，接着向 DRAM 发送新行填充请求，并在数据返回后完成行装填，最终返回 `Ready` 稳态恢复服务。

### 3.1 状态元素

阻塞缓存内部的硬件存储与控制寄存器配置如下：

```bsv
BRAM2Port#(...)     dataArray;    // 数据
BRAM1Port#(...)     tagArray;     // 标签
RegFile#(...)       dirtyArray;   // 脏位（写回策略）
FIFO#(Data)         hitQ    <- mkBypassFIFO;
Reg#(MemReq)        missReq <- mkRegU;
Reg#(ReqStatus)     mshr    <- mkReg(Ready);
FIFO#(MemReq)       memReqQ <- mkFIFO;
FIFO#(Line)         memRespQ <- mkFIFO;
```

**状态原语架构职责**：
- **`dataArray` 与 `tagArray`**：分别例化片上 BRAM 存储实际数据行与匹配标签。双端口 BRAM 允许 CPU 访问与缺失填充之间的流水化交错。
- **`dirtyArray`**：采用通用寄存器堆维护每行的修改状态。只有当某行被写指令修改过（Dirty），在被置换淘汰时才需要执行主存写回。
- **`hitQ`**：使用具有 $enq < deq$ 优先级的 `mkBypassFIFO`。当读请求命中时，数据能在同一周期内无延迟旁路穿透给流水线执行阶段。
- **`mshr` 与 `missReq`**：缺失状态保持寄存器（MSHR）记录状态机当前阶段（`Ready`、`StartMiss`、`SendFillReq`、`WaitFillResp`），`missReq` 锁存触发本次缺失的原始 CPU 请求。

### 3.2 缺失状态机

阻塞缓存的缺失处理状态流转遵循严格的单向拓扑环：

$$\text{Ready} \to \text{StartMiss} \to \text{SendFillReq} \to \text{WaitFillResp} \to \text{Ready}$$

在 BSV 中，状态转移通过互斥保护的规则集群精确表达：

```bsv
rule startMiss (mshr == StartMiss);
    // 若该槽有脏数据，先写回 DRAM
    if (tag valid && line dirty) memReqQ.enq(storeReq);
    mshr <= SendFillReq;
endrule

rule sendFillReq (mshr == SendFillReq);
    memReqQ.enq(missReq);   mshr <= WaitFillResp;
endrule

rule waitFillResp (mshr == WaitFillResp);
    let data = memRespQ.first; memRespQ.deq;
    // 更新 tagArray, dataArray, dirtyArray
    if (missReq.op == Ld) hitQ.enq(extractWord(data, missReq.addr));
    mshr <= Ready;
endrule
```

**各迁移步骤的微架构行为拆解**：
- **`startMiss`（旧行驱逐与脏行回写）**：检查待替换 Cache Line 的有效位与脏位。若该行包含未同步的修改数据，则将该行封装为写请求送入 `memReqQ` 队列排队写入主存；若为干净数据则直接跳过写回。
- **`sendFillReq`（新行请求发射）**：向主存总线发送缺失行地址的读取请求（Line Fill Request），并将控制器状态迁移到等待响应态 `WaitFillResp`。
- **`waitFillResp`（数据行填充与核心唤醒）**：当 DRAM 响应数据抵达 `memRespQ` 时，规则触发读取完整行数据，同步写入 `dataArray` 并更新 `tagArray`；若触发缺失的是 Load 指令，直接截取对应偏移字压入 `hitQ` 返回核心，并将 MSHR 恢复为 `Ready` 稳态。

::: theorem 推论 — 阻塞 vs. 非阻塞缓存
阻塞缓存（*blocking cache*）一次只处理一个缺失；非阻塞缓存（*non-blocking cache*）可在等待缺失响应时继续处理命中，显著提升内存并发度，但 BSV 实现更复杂（需 MSHR 队列）。
:::

---

## 4. 写策略

::: definition
**定义 — 写回 vs. 写穿（*Write-Back vs. Write-Through*）**

- **写回（*Write-Back*）**：写操作只更新缓存，标记为"脏"；置换时才写回 DRAM。节省带宽，需要脏位数组。

- **写穿（*Write-Through*）**：每次写操作同时写缓存和 DRAM。实现简单，无需脏位，但带宽消耗大。
:::

写缺失策略：
- **写缺失分配（*Write-Miss Allocate*）**：缺失时先把行取入缓存，再写。（配合写回使用）
- **写缺失不分配（*Write-Miss No-Allocate*）**：缺失时直接写 DRAM，不取行入缓存。（配合写穿使用）

---

## 5. 存储缓冲区（*Store Buffer, STB*）

::: definition
**定义 — 存储缓冲区（*Store Buffer*）**

存储缓冲区是处理器与 L1 之间的队列，Store 指令先进入 STB，处理器继续执行；STB 在后台将最旧的 Store 写入 L1 或 DRAM。Load 指令先搜索 STB（取最近匹配），再查 L1。
:::

**STB 加速原理**：Store 不直接等待 L1 缺失处理，延迟被隐藏。

```bsv
// Req 方法中
if (r.op == Ld) begin
    let x = stb.search(r.addr);
    if (isValid(x)) hitQ.enq(x);  // STB 命中
    else // 查 L1 ...
end else   // Store
    stb.enq(r.addr, r.data);      // 进入 STB
```

---

## 6. 组相联缓存（*Set-Associative Cache*）

::: definition
**定义 — N 路组相联（*N-Way Set-Associative*）**

N 路组相联 = N 个直接映射缓存并联。一个地址映射到唯一的"组"（*set*），但可以存放在组内 N 个"路"（*way*）的任意一个。通过并行比较 N 个标签来减少冲突缺失，置换策略常用 LRU（*Least Recently Used*）。
:::

比较：

| 类型 | 冲突缺失 | 标签比较 | 面积 |
|------|---------|---------|------|
| 直接映射 | 多 | 1 路 | 小 |
| N 路组相联 | 少 | N 路并行 | 中 |
| 全相联 | 极少 | 全部并行 | 大 |

::: example 例题 — 缓存参数计算

:::

32KB 直接映射缓存，行大小 16 字节（4 字），32 位地址：
- 行数 = 32K/16 = 2048 = $2^{11}$，Index 位数 = 11
- Offset 位数 = $\log_2 16 = 4$
- Tag 位数 = 32 - 11 - 4 = 17

Sol：每个缓存行需额外存储 17 位 Tag + 1 位 Valid + 1 位 Dirty。

---

## 我的理解

::: insight
缓存设计的核心不是单纯追求“更快的 SRAM”，而是把不同来源的等待分开处理：局部性减少慢层访问，MSHR 表达尚未完成的缺失，存储缓冲区则把 Store 从前台执行路径移到后台。组相联进一步用硬件比较成本换取更少的冲突。理解这些等待由谁记录、何时解除，比只记住缓存结构更容易迁移到乱序执行和一致性协议。
:::

## 本讲小结：缓存命中、缺失并发与冲突权衡

缓存通过时间/空间局部性加速访存；阻塞缓存用四状态 MSHR 状态机处理缺失；写回策略节省带宽但需脏位；存储缓冲区将 Store 延迟隐藏在后台；组相联通过多路并行查找消除冲突缺失，是现代处理器的标准配置。
