---
title: 6.5610 应用密码学与安全（Spring 2026）
type: course
course: 6.5610 应用密码学与安全（Spring 2026）
course_id: '6.5610'
tags: [applied-cryptography, provable-security, privacy-enhancing-technologies, zero-knowledge]
status: draft
source: 'https://65610.csail.mit.edu/2026/'
---
# 6.5610 应用密码学与安全（Spring 2026）

> 课程主页：[MIT 6.5610 Applied Cryptography and Security](https://65610.csail.mit.edu/2026/)

## TL;DR

- 课程从安全定义与对称原语出发，推进到格密码、PIR、FHE、MPC、可验证计算和 ORAM。
- 本目录整合了官网提供 lecture notes 的 18 个核心主题；本地文件名为保持既有 URL 未因客座课插入而重排。
- 2026 Panopto 录像需要 MIT 登录，本次无法取得 transcript，因此没有把未核验的口头内容写进笔记。

## 先修与阅读方法

建议先掌握概率、线性代数、有限域和基础密码学；没有系统安全背景时，可先读 [6.1600](../foundation_of_security/)。阅读每讲时先看安全目标和攻击者能力，再看构造与归约，最后检查“工程视角”中的假设是否能在真实部署中成立。

## 课程地图

### 一、对称密码学基础

| 讲次 | 笔记 | 核心连接 |
| --- | --- | --- |
| L1 | [密码学哈希](./lec1.md) | 单向性、抗碰撞性、随机预言机 |
| L2 | [从 PRF 构造对称加密](./lec2.md) | 安全游戏、随机化加密、IND-CPA |
| L3 | [PRF、计数器模式与 ChaCha20](./lec3.md) | 具体安全、nonce、流密码 |
| L4 | [PRP、Feistel 与 AES](./lec4.md) | 分组密码、模式与实现侧信道 |

### 二、公钥与格密码

| 讲次 | 笔记 | 核心连接 |
| --- | --- | --- |
| L5 | [Diffie–Hellman 与公钥加密](./lec5.md) | 密钥交换、混合加密、身份绑定 |
| L6 | [Rabin、RSA 与后量子动机](./lec6.md) | 陷门函数、填充、Shor 算法 |
| L7 | [从 LWE 构造公钥加密](./lec7.md) | Regev 加密、格困难性、噪声预算 |

### 三、私密检索与密文计算

| 讲次 | 笔记 | 核心连接 |
| --- | --- | --- |
| L8 | [私有信息检索](./lec8.md) | 查询隐私、多服务器与计算 PIR |
| L9 | [全同态加密 I](./lec9.md) | 密文运算、噪声增长、GSW |
| L10 | [全同态加密 II](./lec10.md) | 自举、模数切换、密钥切换 |

### 四、零知识与多方计算

| 讲次 | 笔记 | 核心连接 |
| --- | --- | --- |
| L11 | [交互式证明与零知识](./lec11.md) | 模拟、知识提取、Fiat–Shamir |
| L12 | [秘密共享](./lec12.md) | Shamir、多项式插值、阈值信任 |
| L13 | [安全多方计算](./lec13.md) | 理想/现实范式、Yao、BGW |
| L14 | [MPC 应用](./lec14.md) | PSI、阈值密码、SPDZ |

### 五、简洁证明与访问模式隐私

| 官网讲次 | 本地笔记 | 核心连接 |
| --- | --- | --- |
| L15 | [Sumcheck 协议](./lec15.md) | 多项式求和、随机挑战、Schwartz–Zippel |
| L18 | [GKR 协议](./lec16.md) | 分层电路、逐层归约、可验证计算 |
| L19 | [zk-SNARKs](./lec17.md) | 算术化、承诺、简洁验证 |
| L20 | [Oblivious RAM](./lec18.md) | 访问模式、重洗、Path ORAM |

> L16（Jim Bidzos）、L17（Ron Rivest）是客座讲座，L21 是 TA 研究展示；官网未提供与其他讲次同形态的 lecture notes，本目录没有用推测内容补位。由于这三讲也没有可用 transcript，课程状态标为 `draft`。

## 文件编号说明

本目录原有 `lec16.md`、`lec17.md`、`lec18.md` 分别对应官网 L18、L19、L20。为避免破坏既有链接，文件名保持不变；文件 frontmatter 的 `lecture` 与标题则采用官网实际讲次。

## 延伸阅读

- [A Graduate Course in Applied Cryptography](https://toc.cryptobook.us/book.pdf)
- [6.1600 课程讲义仓库](https://github.com/mit-pdos/6.1600-notes)
- [Ron Rivest 的密码学与安全参考资料](https://courses.csail.mit.edu/6.857/2022/references)

::: insight
高级密码学的共同方法，是把复杂安全主张转化为清晰游戏，再把攻击逐步归约到更小的概率事件或已知困难问题；构造只是这条证明链中的一个环节。
:::
