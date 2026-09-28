---
title: '现代 SQL 与数据库系统运维'
type: lecture
lecture: 2
tags: [advanced-sql, window-functions, role-based-access, table-maintenance]
status: complete
source: 'https://dsg.csail.mit.edu/6.5830/'
---

# Lec 2 现代 SQL 与数据库系统运维（Modern SQL and Database Administration）

> MIT 6.5830 / 6.5831 · Database Systems · 第 2 讲  
> 核心教材：*Readings in Database Systems* (5th Edition, Red Book)  
> 配套实验：GoDB (Go-based Database Engine)

## TL;DR

- 现代 SQL-92/99 规范大幅超越基础 CRUD，引入通用表表达式（CTE）、递归查询与强大的窗口函数（Window Functions）。
- 数据定义（DDL）、数据控制（DCL）与数据操作（DML）协同保障企业级多租户安全与模式完整性约束。
- 系统运维通过基于角色的访问控制（RBAC）、资源组配额隔离及统计信息分析（ANALYZE）维持稳定吞吐。

## 架构演进与核心洞察

::: insight 窗口函数对传统分组的颠覆
初学者常将 `GROUP BY` 与窗口函数（`OVER (PARTITION BY ...)`）混淆。`GROUP BY` 是破坏性的——它将多行聚合坍缩为单行，导致行级明细丢失；而窗口函数在保留原有每一行明细数据的同时，沿窗口轴线计算滑动统计值（如滑动平均、累计分布、跨行对比 `LAG/LEAD`），极大简化了传统需要自连接（Self-join）的繁琐分析 SQL。
:::

## 核心机制与讲义正文

关系数据库的声明式查询语言， 每隔几年会更新。SQL-92 是 DBMS 必须支持的最低标准，才能声称其支持 SQL。每个供应商都在一定程度上遵循该标准，但也有许多专有扩展。

该语言由不同类型的命令组成： 

1. 数据操作语言 (DML)：SELECT、INSERT、UPDATE 和 DELETE 语句
2. 数据定义语言 (DDL)：表、索引、视图和其他对象的模式定义
3. 数据控制语言 (DCL)：安全性、访问控制
4. 它还包括视图定义、完整性和引用约束以及事务。

关系代数基于集合Set（无序，无重复）。SQL 基于包Bags（无序，允许重复）

## 2.1 数据定义

### 5.2 数据操纵

## 2.3 事务和锁

### XA事务

### 5.4 复制

### 5.5 预处理

### 5.6 组合语法

## 2.7 管理员

### 账户管理

```sql
ALTER USER 语句
CREATE ROLE 语句
CREATE USER 语句
DROP ROLE 语句
DROP USER 语句
GRANT 语句
RENAME 语句
SET DEFAULT ROLE 语句
SET PASSWORD 语句
SET ROLE 语句
```

```sql
-- 需求：创建一个 可以访问、新增，更新，但不可以删除 数据库 test的的开发者ROLE， 以及创建几个USER，授权为这种角色的ROLE

-- 1. 创建一个角色 'developer_role'，并赋予访问、新增和更新权限，但不允许删除
CREATE ROLE 'developer_role';

-- 2. 授予角色对 'test' 数据库的访问权限、插入权限和更新权限
GRANT SELECT, INSERT, UPDATE ON test.* TO 'developer_role';

-- 3. 创建一些用户
CREATE USER 'developer_user1'@'%' IDENTIFIED BY 'password1';
CREATE USER 'developer_user2'@'%' IDENTIFIED BY 'password2';

-- 4. 将 'developer_role' 角色授权给这些用户
GRANT 'developer_role' TO 'developer_user1'@'%';
GRANT 'developer_role' TO 'developer_user2'@'%';

-- 5. 刷新权限
FLUSH PRIVILEGES;
```

### 资源组管理

```sql
ALTER RESOURCE GROUP 语句
CREATE RESOURCE GROUP 语句
DROP RESOURCE GROUP 语句
SET RESOURCE GROUP 语句
```

### 表维护

如果表的数据发生了较大变化可以用

```sql
ANALYZE TABLE 语句 -- 分析表的统计信息，并更新索引的统计信息。
CHECK TABLE 语句
OPTIMIZE TABLE 语句 -- 优化表，重新组织表的存储以提高查询性能。
REPAIR TABLE 语句
```

### SHOW 语句

### 2.8 工具

**describe** 和 **explain** 语句是同义词，是获取有关表结构或查询执行计划的。实际运用上，前者作为查表结构，后者获取查询计划。
