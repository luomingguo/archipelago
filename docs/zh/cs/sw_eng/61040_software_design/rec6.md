---
title: Recitation 6 Cookies、Sessions 与认证状态保持
type: lecture
tags: [session-management, cookies, authentication, web-security]
status: complete
source: 'https://61040.github.io/fa26/preps/cookies/'
---
# Recitation 6 Cookies、Sessions 与认证状态保持（Cookies, Sessions & Auth）

配套练习：[Prep 6: Cookies and sessions](https://61040.github.io/fa26/preps/cookies/)。HTTP 协议本身是无状态的，本实验探讨现代 Web 如何借助安全 Cookie、服务端 Session 与签名令牌（JWT）在不可信网络上建立持久、受控的身份会话。

## TL;DR

- Cookie 是服务端在 HTTP 响应中通过 `Set-Cookie` 头指令写入浏览器并在后续请求自动附带的小型键值对。
- 关键安全标志位：`HttpOnly`（防御 XSS 窃取）、`SameSite=Lax/Strict`（防御 CSRF 攻击）、`Secure`（仅限 HTTPS 传输）。
- Session 机制在服务端存储用户会话数据，客户端仅持有随机不透明的 `session_id`。
- JWT 令牌将声明信息经私钥签名后完全存放在客户端，具备无状态横向扩展能力，但撤销与吊销相对复杂。

## 实验核心技能

### 1. 安全 Cookie 属性对照

```http
Set-Cookie: session_id=s%3A8f9a2b...; Path=/; HttpOnly; Secure; SameSite=Lax
```

- **`HttpOnly`**：禁止页面内的 JavaScript 脚本（如 `document.cookie`）读取该 Cookie，即使网站存在 XSS 漏洞，攻击者也无法直接盗走会话凭证。
- **`SameSite=Lax`**：阻止第三方网站发起的跨站请求自动携带 Cookie，有效遏制大部分 CSRF 跨站伪造请求。
- **`Secure`**：强制浏览器仅在加密的 HTTPS 连接下才发送此 Cookie，杜绝明文中间人嗅探。

### 2. 概念设计视角下的认证边界

在概念设计中，`Session` 或 `Authentication` 本身就是一个独立概念，其 State 为 `a set of Sessions with unique token and user`。业务概念（如 `Posting`）绝不直接操作密码或 Cookie，而是通过同步规则在请求到达时完成身份解析。

::: insight
身份认证不是一个简单的字段，而是一套跨越物理边界的信任握手协议。永远不要轻信客户端提交的明文身份声明；任何越过网络边界的请求，必须通过受密码学保护的凭据在服务端安全解析。
:::
