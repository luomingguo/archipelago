---
title: Flash SSD 操作 II
type: lecture
lecture: 2
tags: [flash-memory, ssd-unwritten-contract, nvm, flash-cache, sustainable-storage]
status: complete
---
# Lec 2 Flash SSD 操作 II

## TL;DR

- **固态硬盘不成文契约（Unwritten Contract）**：SSD 虽然向上层暴露通用 LBA 块设备接口，但其内部 FTL 架构存在五项关键的不成文契约——请求规模匹配通道并发、地址边界对齐、按预期死亡时间分组（冷热分离）、均匀写磨损与时间空间局部性利用。
- **混合主存中的非易失性内存（NVM）**：相变内存（PCM）等新型 NVM 兼具字节寻址与持久化特性，但其写延迟、写功耗及有限寿命显著劣于 DRAM；操作系统必须通过脏页写回策略与冷热页面迁移协同调度。
- **可持续闪存缓存与新型接口**：传统块接口隐藏擦除操作导致高额写入放大，FairyWREN 等前沿缓存系统通过新型写-读-擦（WRE）接口与准入控制，大幅降低闪存写入量并延长介质物理寿命。

## 阅读资料

- He, Jun and Kannan, Sudarsun and Arpaci-Dusseau, Andrea C. and Arpaci-Dusseau, Remzi H.
  [*The Unwritten Contract of Solid State Drives*](http://dl.acm.org/citation.cfm?id=3064187), In *Proceedings of the Twelfth European Conference on Computer Systems (EuroSys)*, 2017, pages 127--144
- Mogul, Jeffrey C. and Argollo, Eduardo and Shah, Mehul and Faraboschi, Paolo
  [*Operating System Support for NVM+DRAM Hybrid Main Memory*](http://www.usenix.org/event/hotos09/tech/full_papers/mogul/mogul.pdf), In *Proceedings of the 12th Conference on Hot Topics in Operating Systems (HotOS)*, 2009, pages 14--14
- Sara McAllister, Yucong Sherry Wang, Benjamin Berg, Daniel S. Berger, George Amvrosiadis, Nathan Beckmann, Gregory R. Ganger
  [*FairyWREN: A Sustainable Cache for Emerging Write-Read-Erase Flash Interfaces*](https://www.usenix.org/system/files/osdi24-mcallister.pdf), In *Proceedings of the 18th USENIX Symposium on Operating Systems Design and Implementation (OSDI)*, 2024

## 本讲定位

第一讲中，我们建立了 NAND 闪存最基础的物理模型与 FTL 映射机制。然而，现代数据中心中的高性能 SSD 内部包含了极其复杂的多通道多芯片并发架构与专有优化固件。

本讲深入剖析上层系统软件与 SSD 交互时的“潜规则”——SSD 的**不成文契约（Unwritten Contract）**；随后探索将非易失性存储介质（NVM）引入主存层次的操作系统支持；最后通过 OSDI'24 最新成果探讨新型闪存接口与可持续存储缓存设计。

## 固态硬盘的不成文契约（The Unwritten Contract）

在机械磁盘时代，Schlosser 和 Ganger 曾提炼出 HDD 的不成文契约：“按顺序访问邻近扇区速度最快”。随着硬件切换为固态硬盘，业界一度认为“SSD 无论怎么随机访问性能都一样”。

威斯康星大学 He 等人（EuroSys'17）对大量主流商用 SSD 进行了系统化实证测试，推翻了上述盲目乐观假设，形式化总结了现代 SSD 的**五大不成文契约**：

### 1. 请求规模契约（Request Scale）

- **现象**：虽然闪存物理读写以页（如 4KB/8KB）为单位，但单个独立 4KB 随机请求无法跑满设备标称性能。
- **机制**：现代 SSD 控制器拥有 8 到 32 个独立的硬件通道（Channels），每个通道上挂载多个 Die。要榨干总线吞吐，软件必须发起足够大的批量请求（如 128KB 以上）或者通过异步 I/O（如 io_uring）保持足够深的队列深度（Queue Depth $\ge 32$），从而同时激活所有内部闪存通道的芯片交错并发。

### 2. 物理对齐契约（Alignment）

- **现象**：即使请求大小恰好是 4KB，如果该请求跨越了两个 4KB 物理闪存页的边界（例如从字节偏移 2048 开始写入 4KB），性能会断崖式下跌 50% 以上。
- **机制**：未对齐的请求会迫使 FTL 将单一逻辑请求拆解为针对两个独立物理页的读-修改-写（Read-Modify-Write, RMW），直接导致 I/O 放大。上层文件系统和数据库必须严格按照物理闪存页大小对齐写入。

### 3. 按预期生命周期分组（Grouping by Death Time）

- **现象**：将长期不变的静态数据（如操作系统内核二进制、归档文件）与高频更新的动态数据（如事务 WAL 日志、临时索引）混合写入同一个文件或临近 LBA 时，SSD 的写入放大（WAF）急剧恶化。
- **机制**：垃圾回收器（GC）在选择擦除块时，若一个块内既有死数据又有存活的冷数据，系统必须将存活冷数据反复搬移复制。若上层软件能将生命周期相近的数据聚集在连续地址空间写入，整个块将在相近时间内同时失效，垃圾回收效率可趋近于 100%（有效页搬移量归零）。

### 4. 均匀写磨损（Uniformity of Wear）

- **现象**：上层软件不应自行在小范围 LBA 内执行高频循环覆盖。
- **机制**：尽管现代 FTL 支持磨损均衡，但若局部 LBA 写入速率过度偏离全局均值，会迫使 FTL 频繁发起昂贵的静态磨损均衡迁移，将其他块的冷数据强行对调，造成前台 I/O 剧烈抖动与延迟长尾。

### 5. 局部性契约（Locality in FTL Cache）

- **现象**：现代大容量 SSD 无法将全部 LBA 到物理页的映射表常驻在控制器的微小片上 SRAM 中，通常在板载 DRAM 中维护分页映射缓存（Demand-based Page-level FTL, DFTL）。
- **机制**：具有强时间局部性与空间局部性的访问能持续命中 FTL 内部的映射缓存；反之，若发起完全随机的离散读写，每次 I/O 都会遭遇 FTL 映射页缺失（Translation Page Miss），导致一次请求触发两次物理闪存读取。

## 混合主存中的非易失性内存（NVM + DRAM）

随着相变存储器（PCM）、阻变存储器（ReRAM）等非易失性内存（NVM）技术的出现，存储系统迎来了介于 DRAM 与 NAND 闪存之间的全新存储层级：
- **核心优势**：支持像 DRAM 一样通过 CPU 内存总线进行字节级寻址（Load/Store 指令），同时断电后数据不丢失，读延迟仅为数十纳秒（接近 DRAM）。
- **物理非对称性缺陷**：
  - **写延迟高**：NVM 写入延迟比 DRAM 慢 3 到 10 倍；
  - **写能耗大**：改变相变材料物理结晶状态需要施加高电流，单次写能耗是 DRAM 的数倍；
  - **寿命有限**：PCM 单元擦写寿命约为 $10^7 \sim 10^8$ 次，远低于 DRAM 的无限擦写。

Mogul 等人（HotOS'09）指出了操作系统管理 NVM+DRAM 混合主存的核心职责：
1. **页面智能放置（Page Placement）**：操作系统内存管理单元（MMU）必须跟踪页面的读写频率。对于高频写入的脏页优先保留在 DRAM 中，而只读代码段与访问稀疏的冷数据页则下沉至 NVM；
2. **写回感知（Write-back Awareness）**：传统的内核页面置换算法（如 Clock 或 LRU）只考虑访问时间戳，在混合主存中，算法必须结合“写入惩罚”权衡——淘汰一个 NVM 页面比淘汰 DRAM 页面昂贵得多。

## 可持续闪存缓存与新兴 WRE 接口：FairyWREN

在大规模数据中心中，闪存通常被用作大规模分布式键值存储与对象存储的前置缓存（Flash Cache）。然而，传统 SSD 面向缓存工作负载时暴露了深刻矛盾：
- 缓存数据的生命周期极短，写入频率极高；
- 块设备接口隐藏了擦除操作，FTL 后台 GC 产生极其严重的写入放大，导致数据中心 SSD 在 1–2 年内即被迅速写死穿孔；
- 频繁更换 SSD 带来了巨大的隐含碳足迹（Embodied Carbon）。

McAllister 等人在 OSDI'24 提出的 **FairyWREN** 探索了软硬件协同的可持续缓存架构：
1. **显式写-读-擦（Write-Read-Erase, WRE）接口**：打破传统块设备封装，将闪存底层的擦除控制直接暴露给上层缓存软件（类似于开放通道 Open-Channel / ZNS 规范）；
2. **智能准入控制（Cache Admission Policy）**：拒绝将仅被访问一次的“穿透型对象”写入闪存，仅对高频重用对象发放闪存写入许可；
3. **消除 FTL 垃圾回收**：FairyWREN 按闪存物理擦除块的大小组织缓存段（Cache Segments），当缓存淘汰发生时，直接以整块为单位发起硬件擦除，**将 FTL 层的写入放大系数从 3~5 彻底压制至 1.0**，使得普通低成本 QLC 闪存能够在数据中心高压缓存场景下平稳运行数年。

## 我的理解

::: insight
**“抽象屏障”的利弊权衡是存储系统演进的永恒主线**：
将 SSD 伪装成一个兼容传统磁盘的 LBA 线性数组，是计算机工业史上最成功的商业兼容性设计，它使得操作系统无需改动一行代码便能享受到固态硬盘的巨大速度红利。
但当硬件性能逼近物理极限时，这种刻意构建的“黑盒假象”便反噬了系统效率——操作系统费尽心力做内存缓存，SSD 在底层偷偷做 FTL 映射缓存；上层应用想要擦除一段数据，底层却因为不知晓语义而反复搬移冷数据。
从“不成文契约”的逆向工程，到 ZNS 与 FairyWREN 对 WRE 接口的显式重构，存储体系结构正在完成一次螺旋式上升：**当硬件介质足够复杂时，最高效的系统永远不是彻底遮蔽底层的黑盒，而是软硬件共同遵守契约、向彼此透明开放关键物理语义的协同体**。
:::
