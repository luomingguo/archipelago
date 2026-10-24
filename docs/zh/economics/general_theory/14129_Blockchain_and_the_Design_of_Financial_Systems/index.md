---
title: MIT 14.129 区块链与金融系统设计
type: course
course: MIT 14.129 Blockchain and the Design of Financial Systems
course_id: '14.129'
tags: [blockchain, financial-systems, mechanism-design, monetary-theory]
status: complete
source: 'https://ocw.mit.edu/courses/14-129-blockchain-and-the-design-of-financial-systems-spring-2025/'
instructor: Robert M. Townsend
---
# MIT 14.129 区块链与金融系统设计（Blockchain and the Design of Financial Systems）

> **授课教授**：Robert M. Townsend（Elizabeth & James Killian Professor of Economics, MIT）  
> **学期与学分**：Spring 2025，MIT 经济学系博士 / 高年级本科生课程（亦对应高级契约理论专题）  
> **官方资源**：[MIT OpenCourseWare (14.129 Spring 2025)](https://ocw.mit.edu/courses/14-129-blockchain-and-the-design-of-financial-systems-spring-2025/)

## TL;DR

- 课程将计算机科学底层的区块链、智能合约与加密学，与经济学契约理论、机制设计与一般均衡理论深度统一。
- 核心研究范式是从理想的资源配置基准出发，探究信息不对称、激励冲突与结算摩擦下各类去中心化架构的实现可能。
- 课程拆解技术神话，证明分布式账本本质上是通过信息共享克服双边交易非效率，而非所有场景必须绑定代币与共识。
- 11 讲涵盖从基础数据库、跨期债务协调、代币化资产与交易失败，到多边信用抵销、随机金融网络、加密拍卖与算法博弈论。

## 课程定位与跨学科综合架构

MIT 14.129 并不是一门讨论加密货币二级市场投机或代码编写技巧的入门课程，而是一门在微观经济学前沿与理论计算机科学交汇点上展开的“金融系统机制设计”课程。

在传统金融学与计算机科学之间，长期存在着显著的话语脱节：

```mermaid
flowchart LR
    subgraph CS["计算机科学工具箱 (CS)"]
        direction TB
        CS1["分布式账本 (DLT / Blockchain)"]
        CS2["智能合约与虚拟机 (EVM / Solidity)"]
        CS3["现代加密原语 (ZKP / MPC / FHE)"]
        CS4["共识协议 (PoW / PoS / PBFT)"]
        CS5["算法博弈论 (Algorithmic Game Theory)"]
    end

    subgraph ECON["经济学理论基准 (Economics)"]
        direction TB
        EC1["阿罗-德布鲁一般均衡与福利经济学第一/第二定理"]
        EC2["机制设计与启示原理 (Revelation Principle)"]
        EC3["昂贵状态验证与最优债务契约 (Townsend CSV)"]
        EC4["全局博弈与协调失灵 (Morris-Shin / Diamond-Dybvig)"]
        EC5["网络清算与系统性风险 (Eisenberg-Noe)"]
    end

    CS <-->|"MIT 14.129 统一分析框架"| ECON
```

Townsend 教授提出了贯穿全课的四层分析框架：
1. **经济目标层（Economic Objectives）**：系统追求的福利目标是什么？（帕累托最优、风险完全分担、流动性最大化）；
2. **摩擦与约束层（Frictions & Obstacles）**：阻碍市场自发达成有效率结果的物理与信息摩擦是什么？（空间分割、缺乏双向承诺、私有信息、状态不可观察、计算不可行）；
3. **机制设计与技术选项层（Mechanisms & Architecture）**：如何组合共享账本、状态机代码、抵押托管（Escrow）或加密原语？与传统受信任第三方（Central Planner / Central Counterparty）相比有何取舍？
4. **均衡结果与制度影响（Equilibrium & Policy）**：各方在纳什均衡或相关均衡下的真实行为是什么？是否存在多重均衡恐慌？如何设计监管与公共基础设施？

## 课程全景地图与讲义导航

全课分为四大模块共 11 讲：

| 模块 | 讲次 | 主题与核心问题 | 对应讲义 |
|---|---|---|---|
| **第一模块：账本、货币与信息** | 第 1 讲 | 课程导论与经济学-计算机科学联合分析框架 | [lec1.md](./lec1.md) |
| | 第 2 讲 | 区块链作为数据库与货币的本质 | [lec2.md](./lec2.md) |
| | 第 3 讲 | 分布式账本作为信息问题的解决方案（Ostroy-Starr 不可能性定理） | [lec3.md](./lec3.md) |
| **第二模块：跨期协调、代币化与结算网络** | 第 4 讲 | 智能合约作为协调问题的解决方案（跨市场高流速私人债务） | [lec4.md](./lec4.md) |
| | 第 5 讲 | 代币化与可编程资产（原子结算、交易失败与敲竹杠摩擦） | [lec5.md](./lec5.md) |
| | 第 6 讲 | 多边贸易信用抵销网络（MTCS 与最小费用最大流算法） | [lec6.md](./lec6.md) |
| | 第 7 讲 | 随机金融网络与流动性注入（金融中心度 vs 系统性传染） | [lec7.md](./lec7.md) |
| **第三模块：机制设计、协议与现代加密学** | 第 8 讲 | 机制设计与激励 vs 协议与信任（经济学理性 vs 拜占庭容错） | [lec8.md](./lec8.md) |
| | 第 9 讲 | 现代加密学核心概念（公私钥、哈希、ZKP、MPC、同态加密） | [lec9.md](./lec9.md) |
| | 第 10 讲 | 利用加密原语设计金融基础设施（隐私拍卖、暗池与保险） | [lec10.md](./lec10.md) |
| **第四模块：前沿计算与算法博弈论** | 第 11 讲 | 算法博弈论与市场机制实现（Dubey 机制、粗相关均衡与 SPEEDEX） | [lec11.md](./lec11.md) |

## 前置知识与学习建议

本课程假定读者具备扎实的高级微观经济学与契约理论基础，并对离散数学与计算机网络有基本了解：

- **微观经济学基础**：熟练掌握消费者与生产者理论、阿罗-德布鲁完全市场一般均衡、埃奇沃斯盒状图分析，以及福利经济学第一、第二定理。
- **信息经济学与博弈论**：理解逆向选择（Akerlof）、道德风险（Holmström）、不完全契约、静态与动态博弈、纳什均衡、贝叶斯纳什均衡与启示原理（Revelation Principle）。
- **计算机与算法基础**：了解有向图模型、网络流问题（最大流/最小费用最大流）、时间复杂度概念（P vs NP vs PPAD），以及现代密码学基础概念（对称/非对称加密、哈希函数单向性）。
- **学习路线**：
  1. 建议先精读各讲的 `## TL;DR`，建立该讲的核心经济学权衡与机制直觉；
  2. 深入推导正文中的数学规划模型（规划者最优化、激励相容约束、网络流平衡条件）；
  3. 细读每讲的 `::: insight` 与 `::: pitfall`，理解理论机制落地时的真实工程陷阱与制度取舍。
