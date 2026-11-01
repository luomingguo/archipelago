---
title: '安全介绍与身份认证'
type: lecture
lecture: 21
tags: [authentication, password-hashing, rainbow-tables, challenge-response]
status: complete
---

# Lec 21 安全介绍与身份认证

> 课程：MIT 6.1800 Computer System Engineering  
> 参考材料：Saltzer & Kaashoek 教材第 11 章（§11.2）及官方授课大纲

**开场白**

在前面的 20 讲中，我们建立了一套极其完备的工程武器库：

- 我们抵御了物理磁盘损坏（RAID）；
- 我们抵御了机器断电死机（WAL & 崩溃恢复）；
- 我们抵御了网络链路丢包与拥塞（TCP & RED）；
- 我们甚至抵御了网络分区与服务器硬件起火（Raft 共识）。

但是，请大家注意前面所有容错假设的一个共同潜台词：我们此前面对的敌人，始终是“无意识的大自然物理规律”。然而，从今天开始，真实世界中最狡黠、最富有智慧、最有耐心的人类恶意攻击者（Adversaries / Hackers）正式登场。

## 系统安全的三大支柱

任何一个安全系统，都在捍卫这三项神圣属性：

- **机密性（Confidentiality）**：只有授权主体能够读取数据，抵御窃听与信息泄露；
- **完整性（Integrity）**：只有被合法授权的实体才能修改数据；任何未经授权的篡改都会被瞬间精准察觉（防篡改、防伪造）；
- **可用性（Availability）**：合法的用户随时能够正常访问和使用系统资源（防死锁、防拒绝服务攻击）

简称**CIA三元祖（CIA Triad）**


## 威胁模型

在评估任何系统安全之前，**第一句必须问的话永远是：你的威胁模型是什么？**

- 谁是攻击者？（是隔壁宿舍好奇的同学？是一个有组织的跨国网络犯罪集团？还是拥有数十亿美元算力与超级计算机的国家级情报机构？）
- 攻击者的物理能力是什么？（他能不能窃听公共 Wi-Fi 信号？他能不能伪造任意 IP 数据包？他能不能物理拆开服务器芯片量测电压？）


1883 年，密码学家奥古斯特·柯克霍夫提出了密码学最伟大的原则：

*“一套安全系统的保密性，绝对不能依赖于算法或设计架构本身的隐蔽保密；算法细节完全可以公之于众，系统的终极安全必须仅仅维系在密钥（Key）的机密性之上！”*

在工程上，试图通过“不公开源码”、“自己发明一套神秘的私有加密逻辑”来求得安全的做法，被称为**隐蔽式安全（Security through Obscurity）**，在黑客面前是纯粹的掩耳盗铃，不出三个月就会被逆向工程彻底攻破！


---

## 认证的基本概念

**认证（Authentication）** 旨在可靠识别请求的主体。身份认证通常涉及两个阶段：

1. **会面阶段（Rendezvous）**：个人访问权威机构，建立身份标识符，并商定认证方法。
2. **身份验证阶段（Verification of Identity）**：主体提交身份凭证，系统验证其真实性。

身份认证凭据通常基于三类要素：
- **记忆信息**（Something you know）：密码、PIN 码、加密私钥；
- **持有物品**（Something you have）：磁条卡、智能硬件令牌、手机短信/TOTP；
- **生物特征**（Something you are）：指纹、面容、声纹。

---

## 逐步改进的密码存储方案

### 版本 1——明文存储

![明文密码存储架构图](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66827d0628b11.png)

验证用户身份接口：

```python
# 第一个版本，明文存储到服务器上
def check_password(username, inputted_password):
    stored_password = account_table[username]
    return stored_password == inputted_password
```

::: pitfall 明文存储的灾难
一旦数据库发生 SQL 注入泄露或遭遇物理失窃（拖库），全网所有复用该密码的用户账户将瞬间遭到毁灭性打击。
:::

---

### 版本 2——哈希存储

为了解决密码直接存储带来的弱点，可以采用密码的加密哈希值而非明文存储密码。

**加密哈希函数**将任意长的字节数组 $M$ 映射到固定长度的值 $V$（例如 SHA-256），具有如下**性质**：

- **确定性（Deterministic）**：对于给定的输入 $M$，很容易计算出 $V \leftarrow H(M)$；
- **单向性（Pre-image Resistance）**：已知 $V$，在计算上无法反推出明文 $M$；
- **次原像抗性（Second Pre-image Resistance）**：给定 $M$，难以找到另一输入 $M' \neq M$ 使得 $H(M) = H(M')$；
- **抗碰撞性（Collision Resistance）**：难以在全域找到任意两个不同的输入 $M_1 \neq M_2$ 使得 $H(M_1) = H(M_2)$。

验证用户身份接口：

```python
# 第 2 版本：单向哈希
def check_password(username, inputted_password):
    stored_hash = accounts_table[username]
    inputted_hash = hash(inputted_password)
    return stored_hash == inputted_hash
```

> **思考**：攻击者在只获得哈希值的情况下，是否能推断出用户的实际密码？  
> 理论上无法直接反推，但攻击者可以使用**彩虹表（Rainbow Table）**发起空间换时间的离线攻击。

![彩虹表哈希映射预计算攻击](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66827bd757025.png)

因为人类倾向于设置常见弱密码（如 `123456`、`password`），攻击者可预先将全球最常见数千万个密码的哈希值全部计算并落盘。一旦拖库成功，仅需常数级查表即可瞬间还原大量弱密码。

---

### 版本 3——慢哈希函数（Key Derivation Functions）

标准哈希函数（如 SHA-256）在硬件中设计为**追求极速**（单核每秒计算数百万次），这使得 GPU 与 ASIC 矿机能每秒穷举数十亿个候选密码。

**慢哈希函数**引入可调节工作量因子（Work Factor），故意让单次哈希计算耗费数十至数百毫秒计算资源：

- **确定性**：输入一致则输出一致；
- **计算阻滞**：引入大量循环迭代（如 PBKDF2 的数万次迭代）；
- **内存硬度（Memory-Hardness）**：如 Argon2 与 scrypt，强行要求占用数兆至数十兆 RAM，封杀专用芯片并行穷举。

```python
# 第 3 版本：慢哈希函数
def check_password(username, inputted_password):
    stored_hash = accounts_table[username]
    inputted_hash = slow_hash(inputted_password)
    return stored_hash == inputted_hash
```

> **评估**：慢哈希函数限制了彩虹表构建的速度，但对于最常见的数百个极弱密码，攻击者依然可以耗费算力预计算。

---

### 版本 4——加盐哈希（Salted Hashing）

为了彻底摧毁彩虹表的复用价值，系统对每个用户分配一个密码学安全的随机值——**盐（Salt）**。盐以明文形式公开存储在账户表中，它不是秘密。

![加盐哈希架构图](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6682914d7f4cd.png)

验证用户身份接口：

```python
# 第 4 版本：加盐慢哈希
def check_password(username, inputted_password):
    stored_hash = accounts_table[username].hash
    salt = accounts_table[username].salt
    inputted_hash = slow_hash(inputted_password + salt)
    return stored_hash == inputted_hash
```

::: theorem 加盐防御彩虹表的数学机制
若盐的长度为 64 位（约 $1.8 \times 10^{19}$ 种可能），攻击者要使用彩虹表，就必须为全网每一个独立盐单独构建一张覆盖常见词汇的哈希表。全域彩虹表的空间复杂度由 $O(P)$ 骤升至 $O(P \times 2^{64})$，这在物理存储上是不可能的，黑客被迫退化为针对单人的高成本在线暴力试错。
:::

---

## Cookie 机制与会话凭证保护

为了减少密码的网络暴露频次，HTTP 使用 Cookie 维持认证会话状态，避免重复提交密码。

![Cookie 会话管理流水线](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66829aa64db65.png)

服务器利用仅自己知晓的机密密钥 `server_key` 为用户生成带有有效期的防伪会话凭证：

```text
cookie = {user, expiration, HMAC(server_key, user || expiration)}
```

::: definition 现代 Web Cookie 三大防御属性
1. **`Secure`**：强制浏览器仅在底层为 HTTPS 的加密通道中传输该 Cookie，免疫明文 Wi-Fi 抓包窃听；
2. **`HttpOnly`**：禁止客户端 JavaScript 脚本读取该 Cookie（`document.cookie` 不可见），阻断 XSS 漏洞盗取会话；
3. **`SameSite`（Strict / Lax）**：限制第三方站点跨站携带本站 Cookie，从源头粉碎跨站请求伪造（CSRF）。
:::

---

## 质询-应答协议（Challenge-Response Protocols）

在不安全的公开信道中，如何向对端证明“我知道密码 $K$”，却**绝不在信道上发送任何明文密码**？

质询-应答协议通过引入一次性随机数（Nonce）实现证明：

![质询应答协议基本交互流程](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6682999544fc4.png)

1. 客户端发起登录：“我是 Alice”；
2. 服务端生成单次随机数 $R$（Challenge）发送给客户端；
3. 客户端利用共享秘密 $K$ 计算：$\text{Response} = H(K \parallel R)$ 发回；
4. 服务端在本地独立计算对比，一致则认证成功。

![钓鱼服务器与恶意假冒威胁模型](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66829a9d36276.png)

::: insight 作者见解与机制辨析
质询-应答协议的核心价值在于**将密码知识的证明转化为基于 Nonce 的临时不可逆签名**。网络窃听者截获了 $R$ 和 $H(K \parallel R)$，不仅无法反解 $K$，而且无法在下一轮认证中重放（Replay Attack），因为服务端的下一轮 Challenge 必为全新的不可预测随机数。
:::

---

## 设计安全认证协议的核心原则

1. **双向认证**：不仅用户需要认证服务器，客户端也必须校验服务端合法性，防范钓鱼中继；
2. **零密码网络明文暴露**：优先采用质询-应答或基于公钥的挑战签名机制；
3. **凭据生命周期受限**：会话 Token 设置严格过期时限并引入滑动失效；
4. **强完整性校验**：所有敏感会话凭据均需结合加密哈希（HMAC）防范篡改。

## TL;DR

- **威胁模型先行**：安全系统设计必须首先确立攻击者能力与信任边界，严格遵循柯克霍夫原则（Kerckhoffs's Principle），绝不依赖算法隐蔽。
- **密码加盐粉碎彩虹表**：明文随机盐（Salt）强制使每个用户的预计算映射独立，消除了跨用户的空间换时间字典攻击；配合慢哈希函数（bcrypt/Argon2）抵御硬件暴力破解。
- **最小暴露与凭证隔离**：HTTP Cookie 需配置 `Secure`、`HttpOnly` 与 `SameSite` 防止网络嗅探与 XSS 窃取；质询-应答（Challenge-Response）协议实现零密码网络暴露认证。
