---
title: 片上网络 I：基础
type: lecture
lecture: 15
tags: [network-on-chip, wormhole-switching, virtual-channels, credit-based-flow-control, router-pipeline]
status: complete
---
# Lec 15 片上网络 I：基础

## TL;DR

- 片上网络（NoC）采用分包路由与专用链路取代共享总线，奠定众核芯片高带宽可扩展互连基石。
- 数据包细分为头微片（Head Flit）、体微片（Body Flit）与尾微片（Tail Flit），适配流控单元。
- 虫孔流控（Wormhole Switching）以极小缓冲区实现流水传输，依托基于信用的背压（Credit-Based）实现无损通信。
- 虚通道（Virtual Channel）在物理链路上复用逻辑队列，既消除了队头阻塞（HOL Blocking），又打破了消息死锁环。

> MIT 6.1920 · Constructive Computer Architecture
> 讲师：Tushar Krishna · 日期：2024-04-07

## 1. NoC 的动机

::: definition
**定义 — 片上网络（*Network-on-Chip, NoC*）**

多核芯片中，各核心、缓存和内存控制器之间需要互连通信（尤其是缓存一致性消息）。NoC 是将网络交换机（*router*）和链路集成在芯片上的片上互连结构，解决传统总线（*bus*）带宽瓶颈和可扩展性问题。
:::

**NoC 的四个设计维度**：

| 维度 | 类比 | 功能 |
|------|------|------|
| 拓扑（*Topology*）| 道路网络 | 节点如何连接 |
| 路由（*Routing*）| 路段序列 | 消息走哪条路径 |
| 流控（*Flow Control*）| 红绿灯 | 消息何时前进/等待 |
| 路由器微架构（*Router Microarch*）| 交叉口设计 | 如何构建路由节点 |

---

## 2. 数据包结构

::: definition
**定义 — 数据包与微片（*Packet & Flit*）**

数据包（*packet*）包含完整的头部（源、目的地址）和有效载荷。为了高效流水线传输，数据包被分割为固定大小的*微片（flit, flow control unit）*：

- **头微片（head flit）**：含路由信息（目的地址）

- **体微片（body flit）**：数据有效载荷

- **尾微片（tail flit）**：标记数据包结束
:::

---

## 3. 流量控制（*Flow Control*）

当下游路由器缓冲区满时，上游必须等待。三种处理方式：

| 策略 | 行为 | 代价 |
|------|------|------|
| 丢包（*Drop*）| 丢弃 flit，发送方重传 | 丢包检测复杂 |
| 误路（*Misroute*）| 走非最短路径绕行 | 延迟增加 |
| 等待（*Wait/Credit-Based*）| 上游等待直到有空间 | 最常用，需信用计数 |

**基于信用（*Credit-Based*）的背压机制**：

- 每个下游缓冲区槽对应 1 个信用（*credit*）
- 上游路由器发送 flit 时消耗 1 信用
- 下游 flit 被消费后，发送 credit 返回上游
- 上游信用为 0 时停止发送（*stall*）

---

## 4. 虫孔流控（*Wormhole Flow Control*）

::: definition
**定义 — 虫孔流控（*Wormhole Flow Control*）**

数据包头微片一旦找到空闲链路就立即传输，后续体/尾微片紧随（像蠕虫钻入管道）。不需要在中间路由器存储整个数据包（降低缓冲区需求），但一个数据包可能同时占用多个路由器的链路，导致**队头阻塞（*Head-of-Line Blocking, HOL Blocking*）**：一个大包堵住链路，小包无法通过。
:::

---

## 5. 虚通道（*Virtual Channels, VC*）

::: definition
**定义 — 虚通道（*Virtual Channel*）**

在同一物理链路上划分多个独立的 flit 缓冲队列（虚通道），多个数据包可以共享同一物理链路但使用不同的 VC 缓冲区。VC 的关键用途：

（1）缓解 HOL Blocking：不同 VC 的队头互不阻塞

（2）死锁避免：通过限制 VC 转换方向打破依赖环路
:::

---

## 6. 路由器微架构流水线

::: definition 定义 — 5 级路由器流水线
- **BW（Buffer Write）**：flit 写入输入缓冲区

- **RC（Route Computation）**：根据目的地计算输出端口

- **VA（VC Allocation）**：为 flit 分配下游虚通道

- **SA（Switch Allocation）**：竞争使用交叉开关（*crossbar*）的输出端口

- **ST（Switch Traversal）+ LT（Link Traversal）**：flit 通过交叉开关并传输到下游链路
:::

**交叉开关类型**：
- **基于多路选择器（*Mux-Based*）**：面积小，但并行度有限
- **矩阵型（*Matrix Crossbar*）**：面积 $O(N^2)$，全无阻塞，延迟小

---

## 7. 性能指标

**零负载延迟（*Zero-Load Latency*）**：

$$T_N = H \times (t_r + t_l) + T_s + T_c$$

- $H$：跳数（<em>hop count</em>）
- $t_r$：路由器延迟，$t_l$：链路延迟（静态，取决于拓扑和路由）
- $T_s$：序列化延迟 = 数据包长度 / 链路带宽（静态）
- $T_c$：竞争延迟（动态，取决于流量）

::: example 例题 — 环形 NoC 的零负载延迟

:::

8 节点环形拓扑，路由器延迟 1 周期，链路延迟 1 周期，数据包 4 flit，带宽 1 flit/周期：

- 最坏跳数（直径）= $\lfloor 8/2 \rfloor = 4$
- 序列化延迟 $T_s = 4/1 = 4$ 周期
- 零负载延迟 $= 4 \times (1+1) + 4 = 12$ 周期

Sol：增加带宽（更宽链路）可减少 $T_s$；使用 2D Mesh 减少平均跳数可减少路由延迟。

## 核心机制小结与片上网络基础权衡

NoC 以路由器+链路替代总线，解决多核芯片的互连扩展性问题；数据包拆分为 flit 流水传输；基于信用的背压机制保证不丢包；虫孔流控降低缓冲需求但引入 HOL Blocking；虚通道缓解 HOL 并用于死锁避免；5 级路由器流水线平衡了延迟和吞吐量。

## 核心机制思考与底层洞察

::: insight 物理约束的倒置：广域网与硅片片上网络的微架构反差
片上网络（NoC）虽然借鉴了宏观计算机通信网络（如以太网、互联网）的报文分组交换理念，但在微观硅片尺度上，其设计前提经历了一场彻底的物理反转：

1. **宏观网络与片上介质的成本倒置**：在宏观因特网中，铺设长途光缆与物理链路是极其昂贵的硬件资产，而端节点的 DRAM 缓冲区相对廉价。因此宏观网络倾向于使用存储转发（Store-and-Forward）和大容量数据包队列，尽最大可能提升单根光纤的带宽利用率。然而在单块芯片上，金属布线层（Metal Layers）极为密集且边际成本低廉，相反，高速低延迟的片上 SRAM 缓冲区（Buffer）却极其昂贵，不仅吞噬了宝贵的计算核心硅片面积，更在待机时产生沉重的静态漏电功耗。
2. **极简缓存与虫孔流控的必然选择**：这种物理反转直接决定了 NoC 的微架构哲学：绝对避免大容量缓存。虫孔流控（Wormhole Switching）将数据包切分为微小的 flit，路由器仅需维护能容纳几拍数据的微型 FIFO 即可开始流水线穿透。
3. **确定性与无损通信的硬约束**：宏观互联网能够容忍偶发丢包并通过 TCP 滑动窗口超时重传；但片上多核通信绝大部分承载着缓存一致性协议和寄存器级消息，任何一个 flit 的丢失都会直接引发芯片逻辑死锁或系统崩溃。基于信用（Credit-Based）的背压流控机制正是为了保证绝对无损传输而生，它以严密的信用收发闭环在硬件底层提供了确定性的流量安全护栏。
:::
