---
title: 分布式 FS & NAS 接口
type: lecture
lecture: 10
tags: [distributed-file-system, nfs, afs, rpc-semantics, cache-consistency]
status: complete
---
# Lec 10 分布式 FS & NAS 接口

## TL;DR

- **分布式透明性与故障模型**：网络附加存储（NAS）通过远程过程调用（RPC）在不可靠物理信道上重建单机文件系统抽象，直面独立部分失效（Partial Failure）与网络丢包挑战。
- **NFS 无状态与幂等设计**：Sun NFSv2/v3 坚守“服务器无状态”法则，通过自包含文件句柄（File Handle）与幂等操作消除崩溃恢复状态机，但必须承受 Close-to-Open 弱一致性与高频属性轮询（GETATTR）带来的可扩展性限制。
- **AFS 有状态回调与扩展性飞跃**：CMU AFS 采用全文件本地磁盘缓存与状态化回调承诺（Callback Promises），写入仅在文件关闭时原子回传，服务器主动通知失效，将单服务器可支撑的客户端规模提升了一个数量级。

## 阅读资料

- The Design and Implementation of the 4.4BSD Operating System, CHAPTER 9
- [*Scale and Performance in a Distributed File System, 1988*](https://scispace.com/pdf/scale-and-performance-in-a-distributed-file-system-41h9xbvkhz.pdf)
- [*Operating Systems: Three Easy Pieces, CH48——Distributed System*](http://pages.cs.wisc.edu/~remzi/OSTEP/dist-intro.pdf)
- [*Operating Systems: Three Easy Pieces, CH49——NFS*](http://pages.cs.wisc.edu/~remzi/OSTEP/dist-nfs.pdf)
- [*Operating Systems: Three Easy Pieces, CH50——AFS*](http://pages.cs.wisc.edu/~remzi/OSTEP/dist-afs.pdf)
- [*RFC 1813 —— NFS Version 3 Protocol Specification*](http://www.faqs.org/rfcs/rfc1813.html)

## 本讲定位

前面的讲次都在讨论单机存储：一台机器的磁盘或固态硬盘上如何布局文件系统、如何管理页面缓存并保证崩溃完整性。本讲跳出单机边界，进入分布式文件系统——多台计算客户端通过网络并发访问中心化存储服务器。这是网络附加存储（*Network-Attached Storage, NAS*）的核心技术底座。

我们将重点对比存储史上的两座里程碑系统：Sun 推出的**网络文件系统（NFS）**与 CMU 研发的**安德鲁文件系统（AFS）**。两者在协议状态、缓存粒度与一致性语义上做出了截然相反的架构抉择，构成了分布式系统设计的经典教科书案例。

## 分布式系统基石：故障、通信与 RPC 语义

在单机系统中，硬件错误通常导致整机崩溃停机（Fail-stop）。而在分布式系统中，最严苛的挑战是**独立部分失效（Partial Failure）**：
- 服务器可能在任何时刻宕机重启；
- 路由器缓冲区拥塞会导致随机丢包；
- 网络分区（Network Partition）使得存活节点彼此无法感知状态。

系统不仅要容忍不可靠的物理网络，更要向上层应用提供稳定确定的执行语义。

### 传输抽象与不可靠通信层

网络底层（如 IP 层）仅提供不可靠的尽力而为（Best-effort）数据报传输。端到端论证（End-to-End Argument）指出：既然网络传输中的丢包与重排不可避免，且高层应用校验不可或缺，底层通信应当尽量保持精炼。

在构建 NAS 协议时，系统通常在 UDP 或 TCP 之上实现轻量级传输管理。对于无连接数据报通信，基础的消息收发接口依赖于套接字系统调用：

```c
// 基础 UDP 数据报收发原型
int sd = socket(AF_INET, SOCK_DGRAM, 0);
sendto(sd, request_buf, req_len, 0, (struct sockaddr *)&server_addr, addr_len);
recvfrom(sd, reply_buf, reply_len, 0, (struct sockaddr *)&from_addr, &from_len);
```

### 超时重传与幂等性保障

当客户端发送请求后未在预期窗口内收到响应时，系统面临经典困境：究竟是请求数据包丢失了，还是服务器已成功执行但响应确认（ACK）在返程中丢失？

![网络丢包与确认丢失导致的请求重试与重复接收问题示意图](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20260305180221673.png)

单纯依赖超时重传（Timeout/Retry）会导致同一个修改请求被服务器重复执行两次。为达成“至多一次（At-most-once）”或“精确一次（Exactly-once）”语义，系统必须引入两项关键机制：
1. **单调递增序列号与请求缓存（Sequence Counters / Duplicate Request Cache）**：服务器在内存中维护近期已处理请求的 ID 表。当收到重复请求时，直接重放保存的结果，而不重新执行底层业务逻辑；
2. **幂等性设计（Idempotency）**：如果一个操作执行一次与连续执行多次产生的系统最终状态完全一致，则称该操作是幂等的。读操作天然幂等，而将 `append_record()` 改造为带有绝对偏移量的 `write(offset, data)` 则是将非幂等操作转化为幂等操作的典型范式。

## NFS：无状态协议与开放标准

Sun 在 1980 年代设计的 NFS（Network File System）是工业界最成功的分布式文件系统之一。Sun 采取了极富远见的开放协议策略：发布标准 RFC 规范，精确定义网络数据表示（XDR）与 RPC 格式，使异构操作系统能够无缝互联。

![NFS 体系架构图：客户端 VFS/NFS 客户端、RPC/XDR 通信层与远程 NFS 服务器/本地文件系统层次](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20260305205904932.png)

### 设计核心：服务器彻底无状态（Stateless Server）

NFSv2 的首要设计目标是**简化服务器崩溃恢复**：
- 服务器**不维护任何客户端运行时状态**：它不记录哪个客户端打开了哪个文件、当前文件读写偏移量在哪里、哪些数据块被谁缓存在本地；
- 每一个发往服务器的 RPC 请求都必须是自包含的（Self-contained），携带完成该操作所需的全部上下文。

如果服务器发生断电宕机，客户端发出的 RPC 只会阻塞超时；一旦服务器重启完毕，下一个重传的 RPC 能够被服务器立即处理，**无需任何复杂的故障协商、日志握手或状态重建协议**。

### 文件句柄（File Handle）与核心协议接口

在单机 POSIX API 中，进程通过整型文件描述符（FD）访问文件，FD 指向内核易失内存中的打开文件表。由于 NFS 服务器无状态，它绝不返回此类易失句柄，而是使用**文件句柄（File Handle, 32 字节不透明二进制串）**：

$$
\text{File Handle} = \langle \text{Volume ID}, \text{Inode Number}, \text{Generation Number} \rangle
$$

- `Volume ID`：标识特定的物理文件系统分区；
- `Inode Number`：标识文件在该分区内的物理索引节点；
- `Generation Number`：**世代号**。当文件被删除而 Inode 编号被操作系统复用给全新文件时，世代号递增，防止持有旧句柄的失效客户端误操作新文件。

核心 RPC 接口全部依托文件句柄展开：
- `LOOKUP(dir_fh, name) -> (file_fh, attr)`：在指定目录下检索文件名，返回其文件句柄；
- `READ(file_fh, offset, count) -> (data, attr)`：携带绝对偏移量读取数据，天然幂等；
- `WRITE(file_fh, offset, count, data) -> (attr)`：携带绝对偏移量覆盖写入；
- `GETATTR(file_fh) -> (attr)`：获取文件元数据（尤其包含 `mtime` 修改时间）。

### 客户端缓存与 Close-to-Open 弱一致性

为了避免每次 read/write 都跨越网络，NFS 客户端会在本地内存页缓存中保留文件副本。但这立刻引入了分布式缓存一致性挑战。

NFS 采用被称为 **Close-to-Open 一致性** 的工程折衷：
1. **写回策略（Flush on Close）**：当进程在客户端调用 `close()` 关闭文件时，客户端会将所有未同步的脏页同步强制刷回（Flush）NFS 服务器；
2. **重检策略（Revalidate on Open）**：当进程调用 `open()` 打开文件时，客户端向服务器发起 `GETATTR` 获取服务器端最新 `mtime`。若服务器时间戳更新，客户端立即清空本地缓存，强制从服务器重新拉取；
3. **属性缓存计时器（Attribute Cache Timeout）**：为了避免每次读写都发起 `GETATTR` 拖垮服务器，客户端将文件属性在本地缓存一段时间（如文件属性缓存 3 秒，目录属性缓存 30–60 秒）。在属性有效期内，客户端读取本地缓存无需向服务器请示。

这一设计放弃了严苛的单机 UNIX 强一致性语义，允许多个客户端在秒级时间窗口内观察到暂时的不一致，换取了可接受的交互性能。

## AFS：全文件缓存与状态化回调承诺

在 CMU（卡内基梅隆大学）校园网规模下，数千台工作站并发挂载使得 NFS 服务器被频繁的 `LOOKUP` 和 `GETATTR` 属性轮询彻底击垮。为此，Satyanarayanan 等人设计了 **Andrew File System (AFS)**，旨在将系统可扩展性提升两个数量级。

### AFS-2 核心架构原则

1. **全文件磁盘缓存（Whole-file Local Disk Caching）**：
   - 客户端机器在本地硬盘划出专用缓存分区（Vice Cache）；
   - 当应用调用 `open()` 时，AFS 客户端守护进程（Venus）一次性将整个文件从中央服务器（Vice）下载到本地磁盘；
   - 后续所有的 `read()` 和 `write()` 完全在本地磁盘上运行，速度等同于单机本地 I/O，**产生零网络流量与零服务器负载**。
2. **关闭时原子刷写（Flush-on-Close）**：
   - 应用修改数据并在本地关闭文件时，Venus 将修改后的全量文件（或差异块）一次性传回服务器，实现以文件为单位的粗粒度原子提交。
3. **回调承诺（Callback Promises）**：
   - AFS 彻底放弃了无状态设计。服务器**记住哪些客户端正在缓存哪些文件**；
   - 当客户端成功缓存一个文件时，服务器给客户端发放一个带有租期的“回调承诺（Callback）”；
   - 只要客户端持有有效的 Callback，它就可以 100% 信任本地磁盘缓存的数据是绝对最新的，**完全无需向服务器轮询**；
   - 只有当某个客户端写回新版本文件时，服务器主动向所有持有该文件 Callback 的其他客户端发送“回调失效（Break Callback）”RPC。

### NFS 与 AFS 架构深度对比

| 评估维度 | Sun NFS (v2/v3) | CMU AFS (v2) |
| :--- | :--- | :--- |
| **服务器状态模型** | 严格无状态（Stateless） | 有状态（Stateful，跟踪客户端回调记录） |
| **缓存存储介质** | 客户端内存页缓存（Page Cache） | 客户端本地独立硬盘（Whole-file Cache） |
| **缓存一致性协议** | 客户端主动轮询（GETATTR 属性缓存 3s 超时） | 服务器主动通知（Server Break Callback） |
| **写入持久化策略** | 块级周期刷写 + Close-to-Open | 完整文件在 `close()` 时一次性网络写回 |
| **一致性保证语义** | 弱一致性（存在秒级陈旧读窗口） | 会话语义（Session Semantics / Last-writer-wins） |
| **服务器崩溃恢复** | 极简（客户端透明重试，服务器零恢复代码） | 较重（服务器需重建 Callback 状态表或广播作废） |
| **单服务器扩展规模** | 支撑数十台客户端即达饱和瓶颈 | 单服务器轻松支撑数百至上千台客户端并发 |

## 我的理解

::: insight
**NFS 与 AFS 的路线之争是分布式系统“无状态健壮性”与“状态化可扩展性”的终极对决**：
NFS 坚守无状态，换来了工业界梦寐以求的简单可靠性：服务器哪怕一天崩溃十次，客户端应用几乎毫无感知。但无状态的代价值得深思——既然服务器不记得谁持有什么，客户端就必须不断发送 `GETATTR` 验证有效性，网络最终被海量“询问是否有更新”的无效元数据流量淹没。
AFS 则展现了另一种系统美学：敢于在服务器维护状态（Callbacks），从而将海量读流量彻底截流在客户端本地。这深刻揭示了分布式系统的第一守则：**不存在免费的扩展性；想要削减 90% 的交互网络负载，就必须在服务器端承担维护一致性状态机与容错恢复的工程复杂度**。这一思想直接启迪了后来的分布式租约（Leases）与现代云存储缓存体系。
:::
