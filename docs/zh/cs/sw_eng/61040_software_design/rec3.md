---
title: Recitation 3 HTTP 与 REST API 实践
type: lecture
tags: [http-protocol, rest-api, web-architecture, backend-basics]
status: complete
source: 'https://61040.github.io/fa26/preps/http-rest/'
---
# Recitation 3 HTTP 与 REST API 实践（HTTP & REST Practice）

配套练习：[Prep 3: HTTP & REST](https://61040.github.io/fa26/preps/http-rest/)。本实验深入现代 Web 客户端与服务端通信的基石：HTTP 协议请求/响应报文结构、RESTful 语义规范以及端点调试技巧。

## TL;DR

- HTTP 是无状态的应用层请求-响应协议，报文由起始行、首部头（Headers）与主体（Body）构成。
- RESTful 架构约定使用标准 HTTP 动词（GET, POST, PUT, DELETE）操作资源，遵循幂等性与安全性语义。
- 掌握常见 HTTP 状态码的精准语义：200 OK、201 Created、400 Bad Request、401/403 鉴权失败、404 Not Found、500 服务端错误。
- 熟练使用 curl、httpbin 与浏览器 Network 选项卡调试请求头、载荷（Payload）与跨域问题（CORS）。

## 实验核心技能

### 1. 请求方法语义与幂等性

| 动词 | 语义职责 | 安全性（Safe） | 幂等性（Idempotent） |
| --- | --- | --- | --- |
| `GET` | 读取资源 | 是 | 是 |
| `POST` | 触发动作或创建资源 | 否 | 否 |
| `PUT` | 全量替换或指定更新 | 否 | 是 |
| `DELETE` | 删除指定资源 | 否 | 是 |

### 2. 首部头与内容协商

- `Content-Type: application/json`：告知服务端请求体为 JSON 格式。
- `Accept: application/json`：期望服务端响应返回 JSON 数据。
- `Authorization: Bearer <token>`：在首部安全传递凭据，杜绝在 URL 查询参数中泄漏敏感令牌。

::: insight
在概念设计中，一个概念的动作（Action）在对外暴露时往往映射为具体的 HTTP 端点。保持端点语义纯粹、状态码表达精确，是将概念规格转变为可靠 Web API 的第一道关卡。
:::
