---
title: Recitation 4 MongoDB 容器化与数据持久化
type: lecture
tags: [mongodb, database, docker, containerization]
status: complete
source: 'https://61040.github.io/fa26/recitations/recitation-4.pdf'
---
# Recitation 4 MongoDB 容器化与数据持久化（MongoDB & Data Modeling）

官方课件：[Recitation 4](https://61040.github.io/fa26/recitations/recitation-4.pdf) · 配套练习：[Prep 4: MongoDB](https://61040.github.io/fa26/preps/mongodb/)。本实验指导学生使用 Podman / Docker Compose 一键启动本地容器化 MongoDB，并演示概念级数据状态的隔离存储与基本 CRUD 读写。

## TL;DR

- 借助容器化（Podman / Docker Compose），开发者无需在宿主机污染环境即可获得轻量、可重现的本地 MongoDB 实例。
- 概念设计倡导状态独立性：每个 Concept 自主管理所属的集合，禁止跨概念共用杂乱的“全局上帝表”。
- 掌握 MongoDB 文档型存储的核心操作：`insertOne`, `find`, `updateOne` 与 `deleteOne`。
- 建立索引（Indexes）约束唯一性（`unique: true`），在数据库物理层兜底概念规格的不变量约束。

## 实验核心技能

### 1. 本地容器配置（compose.yaml）

在现代软件工程中，本地搭建数据库的首选方案是容器化。容器技术能够将数据库服务及其所需依赖完全打包隔绝，避免在不同操作系统之间产生复杂的路径与环境冲突。通过撰写一份清晰的声明式 Compose 文件，项目团队的任何新成员只需执行一行指令，即可在本地瞬间拉起与生产环境高度一致的数据库服务。

```yaml
services:
  mongo:
    image: docker.io/library/mongo:7.0
    restart: unless-stopped
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db

volumes:
  mongo-data:
```

通过 `bun run storage` 一键启动数据库，数据卷持久化在本地。

### 2. 概念内部数据读写示范

概念设计要求每个概念拥有独立自洽的状态空间，禁止跨概念共用表结构。以点赞（Upvoting）概念为例，该概念只需要关心“谁给什么条目投了票”，而完全不需要关心被投票的对象是一篇文章、一辆车还是一条评论。在底层持久化时，我们为该概念建立专属的集合与联合唯一索引，从物理层杜绝同一用户重复投票的不一致隐患。

每个概念独立持有一个 `Collection`，例如 `Upvoting` 概念仅读写 `upvoting_votes` 集合：

```ts
import { MongoClient } from "mongodb";

const client = new MongoClient("mongodb://localhost:27017");
await client.connect();
const db = client.db("conceptbox");
const votes = db.collection("upvoting_votes");

// 增加投票（保证唯一性）
await votes.createIndex({ voter: 1, item: 1 }, { unique: true });
await votes.insertOne({ voter: "alice", item: "post_101", timestamp: new Date() });
```

::: insight
文档数据库的自由 Schema 是一把双刃剑。如果没有概念设计的状态规格约束，数据库很容易退化成任意字段混杂的垃圾堆。概念的 Simple State Form 为底层无模式文档提供了逻辑上的强模式保障。
:::
