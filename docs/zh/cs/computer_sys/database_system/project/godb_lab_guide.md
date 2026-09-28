---
title: GoDB 数据库内核实验全通关指南
type: project
tags: [godb, lab-assignment, buffer-pool-lab, query-engine-lab]
status: complete
---

# GoDB 数据库内核实验全通关指南（GoDB Architecture and Lab Guide）

> MIT 6.5830 / 6.5831 · Course Projects & Labs  
> 官方实验代码库：MIT DSG GoDB (Go 语言编写的高性能教学关系数据库系统)

## TL;DR

- GoDB 是 MIT 6.5830 专用的教学关系数据库，使用 Go 语言自底向上构建完整内核。
- Lab 1 实现堆文件（HeapFile）、元组（Tuple）序列化与基于时钟算法的缓冲池（BufferPool）。
- Lab 2 实现基础查询算子（Filter、Project、Join、Aggregate）的火山迭代器模型。
- Lab 3 实现事务管理、严格两阶段锁（Strict 2PL）并发控制与基于 WAL 日志的 ARIES 恢复。

## 实验反思与架构洞察

::: insight 亲手手写数据库内核的认知质变
只阅读教科书中的“页表”、“缓冲池”和“2PL”很难理解并发死锁与内存脏页的凶险。在 GoDB 实验中，每一个学生必须用 Go 语言亲手实现一个支持多并发线程读写的 `BufferPool`，并处理由于锁获取顺序颠倒导致的 Channel 阻塞。只有在经历过 Lab 3 崩溃恢复测试中日志 LSN 对不齐的绝望之后，才能真正敬畏数据库 ACID 的工程价值。
:::

## 一、GoDB 体系架构总览

GoDB 完整实现了经典关系数据库从 SQL 解析到磁盘文件管理的端到端链路：

1. **存储层（Lab 1）**：包含 `HeapFile`、`HeapPage` 和 `BufferPool`，负责管理定长与变长元组的物理打包与脏页同步。
2. **执行引擎（Lab 2）**：基于火山模型迭代器（`Iterator`），包含 `Filter`、`Project`、`Join`（Nested Loops 与 Hash Join）和 `Aggregate`。
3. **事务与恢复（Lab 3）**：实现事务隔离的锁管理器（`LockManager`）、事务原子回滚与基于 WAL 的 Redo/Undo 恢复。
4. **索引与优化（Lab 4 / 选做）**：实现外存 B+ 树索引结构与基于 Selinger 算法的动态规划连接顺序优化。

---
