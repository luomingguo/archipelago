---
title: 产品开发的通用流程与课程框架
type: lecture
lecture: 1
tags: [product-development-process, stage-gate, phase-review, rd-vs-pd, project-scoping]
status: complete
source: 'https://ocw.mit.edu/courses/15-783j-product-design-and-development-spring-2006/resources/clas1_int_crse_6/'
---

# Lec 1 产品开发的通用流程与课程框架（Introduction to the Course）

> MIT 15.783/2.739 · Product Design and Development · 主讲 Thomas Roemer（Sloan）、Matt Kressy（RISD）、Warren Seering（MIT-ME）

## TL;DR

- 课程由 Sloan、RISD（工业设计）、MIT 机械工程三方教师联合授课，跨学科团队（商科、工业设计、工程）本身就是这门课要训练的能力，而不只是内容安排。
- 研发（R&D）应被拆成两段性质完全不同的工作：技术开发（Technology Development）方法松散、难以计划、结果不可预测；产品开发（Product Development）方法结构化、可计划、结果可预测。课程只聚焦后者。
- 通用产品开发流程分六个阶段：规划（Planning）→ 概念开发（Concept Development）→ 系统层级设计（System-Level Design）→ 详细设计（Detail Design）→ 测试与改进（Testing and Refinement）→ 生产爬坡（Production Ramp-Up），阶段之间以里程碑评审（Mission Approval、Concept Review、System Spec Review、Critical Design Review、Production Approval）作为强制关口。
- 课程用真实的学生项目案例（创可贴分发器、婴儿配方奶分配器、发展中国家用投影仪等）划定项目选题的可行边界：零件数少于 10、原型成本低于 1000 美元、不需要基础技术突破、能接触到 5 人以上（理想 20 人以上）的潜在用户。

## 课程的组织方式：三个学科、一个流程

这门课由三位背景迥异的教师联合执教：Sloan 商学院的 Thomas Roemer 负责管理与流程视角，RISD（罗德岛设计学院）的 Matt Kressy 负责工业设计视角，MIT 机械工程系的 Warren Seering 负责工程实现视角。选课学生也来自 LFM（Leaders for Global Operations）、MBA、MOT（技术管理）、RISD、MIT 工程本科生与研究生等多个项目。这种组成不是巧合——产品开发本身就是一项要求商业判断、用户/美学洞察和工程可行性三者在同一决策里同时生效的工作，任何单一学科背景都无法独立完成。课程的核心教学法是"做中学"（Learning by Doing）：六人跨学科小组在一学期内推进一个真实产品，从需求识别一路走到详细设计与原型，而不是仅通过案例讨论学习方法论。

## 技术开发与产品开发：一对容易被混淆的概念

课程首先划清"研究与开发"（R&D）里 R 和 D 的边界，这个区分决定了整门课的方法论适用范围：

- **技术开发（Technology Development）**：探索尚不确定能否实现、能否满足需求的新技术能力。方法通常是非结构化的，难以制定固定的时间计划，结果本质上不可预测——因为要解决的问题本身包含未知的技术风险。
- **产品开发（Product Development）**：把已经相对成熟、可用的技术，组织进一个满足特定客户需求的产品中。这一过程可以用结构化的方法管理，可以做出较为可靠的时间和资源计划，产出也相对可预测。

::: insight
这个区分的实际意义是：把技术不确定性留给研发前端去消化，产品开发阶段假设关键技术已经"够用"，管理重心从"能不能做出来"转向"如何又快又准地把可行技术变成能上市的产品"。课程的全部工具——从概念生成到原型再到测试——都建立在这个前提之上，因此不适合直接套用到仍存在重大技术不确定性的早期研发项目。
:::

## 通用产品开发流程（Generic Product Development Process）

课程采用 Ulrich & Eppinger《Product Design and Development》教材中的通用六阶段流程模型，作为贯穿全课程的骨架：

1. **规划（Planning）** → 里程碑：任务书批准（Mission Approval）
2. **概念开发（Concept Development）** → 里程碑：概念评审（Concept Review）
3. **系统层级设计（System-Level Design）** → 里程碑：系统规格评审（System Spec Review）
4. **详细设计（Detail Design）** → 里程碑：关键设计评审（Critical Design Review）
5. **测试与改进（Testing and Refinement）**
6. **生产爬坡（Production Ramp-Up）** → 里程碑：生产批准（Production Approval）

每个阶段之间插入一次正式的评审关口，产品只有通过评审才能进入下一阶段。这种"阶段-关口"（stage-gate）结构的价值在于：它把一个模糊、连续的创造过程，切成若干个有明确交付物和决策点的可管理片段，管理层可以在每个关口上评估是否继续投入、调整方向甚至终止项目，而不必等到产品做完才发现方向错了。本课程后续各讲（需求识别、概念生成、概念筛选、原型、测试等）基本按这一流程的顺序展开。

## 项目选题的可行性边界

课程的核心作业是六人小组在一学期内推进一个真实产品项目，为了保证项目能在一学期内走完整个流程，课程对选题设了明确的可行性约束：

::: example 项目提案准则
- 应有可证实的市场需求，且能找到现有产品尝试满足这一需求（用于对比参照）；即便对已有企业而言，这也应是一个有吸引力的市场机会。
- 零件数量大概率少于 10 个。
- 有较高把握把原型成本控制在 1000 美元以内（团队另有 1000 美元项目预算）。
- 不需要任何基础性的技术突破——即产品开发意义上的项目，而非技术研发意义上的项目。
- 能接触到 5 名以上潜在用户（20 名以上更理想），用于需求访谈和测试。
- 高度专有、涉及商业机密的想法建议留到其他场合，因为课程项目会在课堂上公开讨论。
:::

课程展示的历年学生项目——单手操作的创可贴分发器、可 360° 旋转便于放置婴儿的汽车安全座椅、带体温计和自动配比功能的婴儿配方奶分配器、面向发展中国家低成本自制的媒体投影仪等——都是在这些约束下完成的真实案例，说明"小而具体"的日常产品同样能支撑一次完整、有深度的产品开发训练，未必需要宏大的技术突破。

::: pitfall 选题常见误判
课程特别提醒：很多现有产品其实设计得并不好，只要选题满足上述约束，学生做出比市面现有产品更优的方案是完全可能的——"自己用过某产品觉得凑合"不等于"市场上不存在更好的替代方案"，选题前仍需做认真的竞品调研。
:::
