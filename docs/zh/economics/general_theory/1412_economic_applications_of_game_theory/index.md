---
title: 14.12 博弈论经济应用
type: course
course: 14.12 Economic Applications of Game Theory
course_id: '14.12'
tags: [game-theory, nash-equilibrium, subgame-perfection, bayesian-games, mechanism-design]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# 14.12 博弈论经济应用

> 课程：MIT 14.12 Economic Applications of Game Theory, Fall 2025 · Ian Ball 授课。

## TL;DR

- 课程系统构建从静态博弈到动态博弈、从完全信息到不完全信息的现代非合作博弈论大厦。
- 梳理严格优势劣势剔除、理性化、纳什均衡、子博弈精炼均衡（SPNE）与完美贝叶斯均衡（PBE）。
- 重点探讨在寡头垄断、重复博弈隐性卡特尔、拍卖机制设计、劳动力信号传递与廉价磋商中的经济应用。

## 学习路线与讲次索引

### 一、基本解概念与市场竞争

- [第 01 讲：个人决策理论与策略环境基础](lec1.md)
- [第 02 讲：博弈的表述形式：标准式与扩展式](lec2.md)
- [第 03 讲：严格劣势策略与优势策略剔除](lec3.md)
- [第 04 讲：理性化与信念驱动的选择](lec4.md)
- [第 05 讲：纳什均衡及其混合策略扩展](lec5.md)
- [第 06 讲：不完全竞争市场应用：古诺、伯川德与豪泰林模型](lec6.md)
- [第 07 讲：零和博弈与极大极小定理](lec7.md)

### 二、动态博弈与重复互动

- [第 08 讲：动态博弈与逆向归纳法](lec8.md)
- [第 09 讲：讨价还价理论：纳什与鲁宾斯坦模型](lec9.md)
- [第 10 讲：子博弈精炼纳什均衡（SPNE）与可信承诺](lec10.md)
- [第 11 讲：单阶段偏离原则与动态博弈检验](lec11.md)
- [第 12 讲：有限重复博弈与合作的崩溃](lec12.md)
- [第 13 讲：无限重复博弈与触发策略](lec13.md)
- [第 14 讲：民间定理（Folk Theorem）与长期合作秩序](lec14.md)
- [第 15 讲：隐性卡特尔与反垄断规制](lec15.md)

### 三、贝叶斯博弈与拍卖机制设计

- [第 16 讲：静态不完全信息博弈与海萨尼转换](lec16.md)
- [第 17 讲：贝叶斯纳什均衡的经济应用](lec17.md)
- [第 18 讲：拍卖机制设计：四种经典拍卖与投标策略](lec18.md)
- [第 19 讲：收益等价定理与最优拍卖设计](lec19.md)
- [第 20 讲：互联网广告拍卖：广义二阶拍卖与关键词竞价](lec20.md)

### 四、动态私人信息与认知前沿

- [第 21 讲：完美贝叶斯均衡（PBE）与序贯理性](lec21.md)
- [第 22 讲：信号传递博弈与斯宾塞教育模型](lec22.md)
- [第 23 讲：不完全信息下的动态讨价还价与科斯猜想](lec23.md)
- [第 24 讲：廉价磋商（Cheap Talk）与战略信息传递](lec24.md)
- [第 25 讲：共同知识与博弈论认识论前沿](lec25.md)

## 核心解概念对照表

| 核心解概念 | 最本质的审查检验 | 适用环境与关键讲次 |
| :--- | :--- | :--- |
| **严格支配 / 理性化** | 是否在对手所有策略下均劣；能否成为某种先验信念下的最佳反应 | 静态完全信息（Lec 3–4） |
| **纳什均衡（NE）** | 每一位玩家对其他人的策略同时构成最佳反应 | 静态完全信息（Lec 5–7） |
| **子博弈精炼均衡（SPNE）** | 每一个子博弈中都诱导纳什均衡，消除不可信虚张声势威胁 | 动态完全信息与重复博弈（Lec 8–15） |
| **贝叶斯纳什均衡（BNE）** | 每一类私人类型基于后验概率对对手策略类型最佳反应 | 静态不完全信息与拍卖（Lec 16–20） |
| **完美贝叶斯均衡（PBE）** | 每个信息集处序贯理性，均衡路径上按贝叶斯法则更新信念 | 动态不完全信息与信号传递（Lec 21–24） |
| **共同知识（CK）** | 无限层级的“所有人知道所有人知道”，最小共同粗分割测度 | 认知博弈论与博弈论哲学根基（Lec 25） |

## 外部官方资源

- [MIT OCW 14.12 课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT OCW 14.12 视频清单（Lecture Videos）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/resources/lecture-videos/)
- [MIT OCW 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
博弈论是现代经济学乃至整个人类理性分析工具库中最强悍的通用语言。掌握博弈论绝非为了在零和倾轧中算计对手，而是为了深刻洞悉制度、契约与法律的内在逻辑：唯有设计出符合各方激励相容约束的精巧机制，才能将个人逐利的盲目冲动，驯化引导为维系人类长治久安的高效合作秩序。
:::
