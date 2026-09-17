---
title: 15.783 产品设计与开发
type: course
course: 15.783 产品设计与开发
course_id: '15.783'
tags: [product-development-process, agile-development, design-thinking, prototyping, customer-needs]
status: complete
source: 'https://studylib.net/doc/28287998/syllabuspdd-spring-2026--1-'
---
# 15.783 产品设计与开发（Product Design and Development）

> MIT Sloan (15.783J) · MIT Mechanical Engineering (2.739J) · RISD Industrial Design Studio · Spring 2026  
> 教学团队：Prof. Steven Eppinger (MIT Sloan)、Kamala Grasso (MIT MechE)、Heewon Lee (RISD ID)

## TL;DR

- 课程整合商业管理（Sloan）、工程实现（MIT MechE）与工业设计（RISD），以跨学科团队为载体，完整演练从市场机会挖掘到 Alpha 原型落地的端到端产品创新流程。
- 教学架构由传统的阶段门（Phase-Gate）瀑布流程全面演进为 **6 个双周冲刺（Sprint 0–5）的敏捷硬件与数字产品开发模式**，并将生成式 AI 工具链深度融入概念探索与提示词推演。
- 全学期 24 次教学研讨采用“理论方法讲授”与“敏捷工坊评审（Demo & Retro）”双轨制，以量化需求权衡、系统级模块化架构与严谨的经济学模型支撑关键设计决策。
- 知识体系以 Ulrich、Eppinger 与 Yang 合著的《Product Design and Development》（第 8 版，2026）为理论基石，辅以 Stripe 支付架构、Airbnb 战略转向等当代商业与硬科技案例。

::: definition [敏捷双周冲刺（Two-Week Sprints）]
在 15.783J 的现代教学体系中，产品开发被划分为 6 个为期两周的迭代冲刺（Sprint 0 至 Sprint 5）。每个 Sprint 均设定明确的交付物目标（如机会池评分、概念草模、工作功能原型、精细测试模型、Alpha 样机），并在末尾执行敏捷团队评审（Sprint Demo & Review）与复盘会议（Sprint Retrospective），替代传统耗时冗长的线性阶段评审。
:::

## 课程定位与跨学科协同机制

15.783J（同列为 MIT 机械工程系 2.739J 及罗德岛设计学院 RISD 工业设计高年级毕业工作室）是全球极富盛名的旗舰级跨学科产品开发实践课。课程面向 MIT Sloan MBA/LGO、工科研究生与 RISD 工业设计学者开放，通过组建跨职能团队破解三大领域的认知孤岛：

1. **商业与管理（Business / Sloan）**：聚焦市场规模评估、商业模式构建、客户细分、目标成本法（Target Costing）与项目经济学分析（NPV/敏感度推演）。
2. **工程与技术（Engineering / MechE）**：负责功能架构分解、参数规格定义、详细设计、物料选型、可制造性与可装配性验证（DFMA）及性能测试。
3. **设计与体验（Design / RISD）**：主导深度用户调研（Needfinding）、感官美学、人机工程学（Ergonomics）、交互界面（UI/UX）与高保真外观模型制作。

::: insight [独立开发者视角：硬科技与软服务的产品化统一]
对于独立开发者与技术型创业者而言，15.783J 最大的启示在于**将产品设计从“凭直觉造轮子”转变为“结构化假说验证”**。无论是开发硬件设备、SaaS 工具还是 AI 原生应用，从寻找高价值真实痛点（R-W-W 过滤）、将非结构化访谈翻译为量化需求规格（Customer Needs & Specs）、运用模块化架构解耦系统依赖，到利用最小可行原型（MVP）与单元经济学测算商业底线，其核心底层方法论高度统一。
:::

## 敏捷冲刺架构与 24 讲全景大纲

Spring 2026 教学大纲由 6 个敏捷冲刺阶段驱动，共 24 次正式课（每周二、周四 13:00–16:00），前半段为理论剖析，后半段为冲刺评审与教练辅导：

| 冲刺阶段 | 讲次与日期 | 核心主题 | 推荐阅读材料与参考资料 | 团队里程碑与交付物 |
| :--- | :--- | :--- | :--- | :--- |
| **Sprint 0**<br>机会分析<br>(Opportunity Analysis) | **Class 1**<br>2月3日 | **引论与设计思维**<br>(Introduction + Design Thinking) | • PDD Ch. 1: Introduction<br>• PDD Ch. 2: Processes & Organizations<br>• PDD Ch. 3: Opportunity Identification<br>• *(选读)* Irene Au: *Design and the Self* | 提交 2 个产品创新机会提案 |
| | **Class 2**<br>2月5日 | **系统化创新与 R-W-W 评估法**<br>(Systematic Innovation & R-W-W) | • PDD Ch. 3 (Real-Win-Worth-it 章节)<br>• Day: *Is It Real? Can We Win? Is It Worth Doing?* (HBR)<br>• *(选读)* Tim Brown: *Design Thinking* (HBR) | 对全班 50 个机会完成盲审打分 |
| | **Class 3**<br>2月10日 | **客户需求分析与待办任务**<br>(Customer Needs Analysis & JTBD) | • PDD Ch. 5: Identifying Customer Needs<br>• Parallel (2026): *What Are Jobs-To-Be-Done (JTBD)*<br>• Patnaik: *Needfinding: The Why and How* | 小组深入调研排名前列的潜在机会 |
| | **Class 4**<br>2月12日 | **项目路演与跨学科组队**<br>(Project Selection & Pitching) | • 课堂提案路演与导师评审 | 中午提交 Pitch 演示，确定跨学科团队构成 |
| **Sprint 1**<br>田野研究<br>(Field Research) | **Class 5**<br>2月19日 | **敏捷开发与硬件 Scrum 流程**<br>(Agile Development Process) | • PDD Ch. 19: Agile Project Management<br>• Scrum Alliance: *The Essence of Scrum*<br>• CoLab / Eppinger: *Agile for Hardware Development* | 建立冲刺 Backlog 与团队看板 |
| | **Class 6**<br>2月24日 | **创造力激荡与概念生成**<br>(Creativity & Concept Generation) | • PDD Ch. 7: Concept Generation<br>• TED: *The Creative Spark Playlist*<br>• Square Sequel: *Design Thinking Ideation Techniques* | 发散探索多种工作原理与解决方案草图 |
| | **Class 7**<br>2月26日 | **生成式 AI 赋能产品创新**<br>(Generative AI for Innovation) | • HBR (2025): *To Jumpstart Creativity, Try These 8 Prompts*<br>• 随堂 AI 提示工程实践（LLM + 扩散模型多模态推演） | **Sprint 1 成果演示与复盘**<br>(Demo, Review, Retro) |
| **Sprint 2**<br>概念模型<br>(Concept Model) | **Class 8**<br>3月3日 | **产品规格定义与参数矩阵**<br>(Product Specifications) | • PDD Ch. 6: Product Specifications<br>• 练习：需求矩阵向工程指标的映射转化 | 确立目标规格矩阵（Target Specs） |
| | **Class 9**<br>3月5日 | **原型制作实务与现代制造法**<br>(Prototyping & Modern Fabrication) | • PDD Ch. 14: Prototyping<br>• Wevolver (2025): *How to 3D Print: Guide for Engineers*<br>• Teel (2026): *How to Prototype Electronic Hardware* | 构建首轮低保真功能验证模型（PoC） |
| | **Class 10**<br>3月10日 | **体验与服务设计**<br>(Experience & Service Design) | • PDD Ch. 17: Design of Services (Zipcar 案例)<br>• Wired: *Disney's $1 Billion Bet on a Magical Wristband*<br>• Don Norman: *Words Matter: People, Not Users* | 绘制端到端客户体验旅程图 |
| | **Class 11**<br>3月12日 | **工业设计、人因工程与美学**<br>(Industrial Design & Ergonomics) | • PDD Ch. 11: Industrial Design<br>• Yves Béhar (fuseproject): *TED Talk on Design*<br>• Gembah (2025): *Industrial Design Trends for 2025* | **Report 1 提交**<br>**Sprint 2 成果演示与复盘** |
| *休整周* | 3月16–27日 | *Sloan SIP Week 与 MIT/RISD 春假* | 团队自主维护关键物料采购与前期测试 | 预订长周期交付件 |
| **Sprint 3**<br>工作原型<br>(Working Model) | **Class 12**<br>3月31日 | **环境可持续设计与循环经济**<br>(Design for Environment) | • PDD Ch. 12: Design for Environment (DfE)<br>• Ellen MacArthur Foundation: *Circular Design Guide*<br>• Franklin-Wallis (NYT): *I'm Appalled by Recycling* | 完成产品全生命周期环保评估（LCA 预审） |
| | **Class 13**<br>4月2日 | **客座讲座：专利与知识产权**<br>(Guest Lecture – Patents) | • 特邀专利律师 Andrew Gathy 主讲<br>• PDD Ch. 16: Patents and Intellectual Property<br>• USPTO Patent Public Search / Google Patents 检索练习 | **Peer Eval 1 匿名同侪互评** |
| | **Class 14**<br>4月7日 | **产品系统架构与模块化**<br>(Product Architecture & Modularity) | • PDD Ch. 10: Product Architecture<br>• Alizon et al. (2007): *Improving Product Family Modularity*<br>• Simpson (2004): *Product Platform Design* | 确定产品模块划分与几何/能量接口定义 |
| | **Class 15**<br>4月9日 | **用户体验设计与界面原则**<br>(User Experience Design) | • Maven: *Six UX Principles with Real-World Products*<br>• 软硬件融合交互动线优化 | **Sprint 3 成果演示与复盘**<br>运行工作模型（Working Rig）展示 |
| **Sprint 4**<br>精炼模型<br>(Refined Model) | **Class 16**<br>4月14日 | **产品开发经济学与现金流估算**<br>(Product Development Economics) | • PDD Ch. 18: Product Development Economics<br>• 基础财务净现值（NPV）与敏感度分析模型 | 建立首版全生命周期财务收益模型 |
| | **Class 17**<br>4月16日 | **目标成本法与商业模式画布**<br>(Product Costing & Business Models) | • Cooper & Slagmulder: *Develop Products with Target Costing*<br>• Ovans (HBR): *What Is a Business Model?*<br>• Strategyzer: *The Business Model Canvas* | 完成物料清单（BOM）预估与单位经济模型 |
| | **Class 18**<br>4月21日 | **特邀讲座：Stripe 数字化产品管理**<br>(Guest Lecture – Stripe) | • Duke Dukellis（Stripe 产品负责人，前 Google 产品 VP）<br>• 剖析现代支付架构、数字化平台规模化与 AI 赋能研运 | 吸收行业一线数字化产品管理实战经验 |
| | **Class 19**<br>4月23日 | **产品测试、假说实验与战略转向**<br>(Testing & Pivots: Airbnb Case) | • BreakoutLearning 在线案例研讨：*Airbnb Case Study*<br>• PDD Ch. 9: Concept Testing<br>• 针对产品市场契合点（PMF）的假说验证与转向机制 | **Sprint 4 成果演示与复盘**<br>精细外观与性能模型验证 |
| **Sprint 5**<br>Alpha 原型<br>(Alpha Prototype) | **Class 20**<br>4月28日 | **特邀前沿讲座与专利防侵权审查**<br>(Guest Lecture & Patent Review) | • 行业特邀嘉宾专题分享<br>• 针对团队最终原型的防侵权（FTO）与可专利点排查 | 原型专利风险与改进闭环 |
| | **Class 21**<br>4月30日 | **产品领导力与跨职能团队组织**<br>(Product Leadership) | • UpGrad: *Product Management Roles & Career Pathways*<br>• Productboard: *The Ultimate Guide to Product Management* | **Report 2 最终报告提交** |
| | **Class 22**<br>5月5日 | **原型冲刺工坊（无授课）**<br>(Team Working Session) | • 全体团队在实验室攻坚最终样机装配、调试与演示视频制作 | 完成最终功能样机封版 |
| | **Class 23**<br>5月7日 | **期末设计大展与正式路演**<br>(Final Project Presentations) | • 三个平行分会场进行全功能原型实物路演与评委打分 | **Sprint 5 最终成果评审** |
| | **Class 24**<br>5月12日 | **精选项目路演与全课程复盘**<br>(Featured Presentations & Retro) | • 全班得票前三名项目在公开大厅进行最终展示<br>• 总结个人成长与团队敏捷复盘 | **Sprint 5 冲刺复盘**<br>**Peer Eval 2 终期同侪互评** |

## 现有精读笔记对照与知识继承说明

知识库中保留了 10 篇根据 MIT 讲义幻灯片深度重构的高质量长文笔记。虽然 2026 最新大纲采用了更加前沿的 6-Sprint 敏捷编排与数字化案例，但原有笔记所详尽推导的经典数理模型（联合分析回归、Pugh 矩阵、Bass 扩散模型、DSM 矩阵）依然是各冲刺阶段坚实的理论底座：

| 现有讲义笔记 | 核心议题与数学模型 | 2026 敏捷冲刺对应讲次 | 教材对应章节 | 重点参考价值 |
| :--- | :--- | :--- | :--- | :--- |
| [Lec 1 通用流程与课程框架](./lec1.md) | 产品开发六阶段通用流程、里程碑评审机制、R&D 与 PD 边界 | Sprint 0: Class 1 | Ch. 1, 2 | 建立产品开发的系统全局观与边界意识 |
| [Lec 4 识别客户需求](./lec4.md) | 深入访谈法、需求陈述五原则、Kano 模型分类、Sweetwater 案例 | Sprint 0: Class 3 | Ch. 5 | 结构化挖掘显性需求与未被满足的潜在需求 |
| [Lec 5 联合分析量化偏好](./lec5.md) | 属性水平设计、可加分效用函数 $U(X)$、虚拟变量回归估计、净水器实例 | Sprint 0: Class 3 / Sprint 2: Class 8 | 专题工具 | 用严谨计量模型解决客户偏好打分的“全重要”失真 |
| [Lec 6 工业设计与硬模型](./lec6.md) | 工业设计在功能/美学/人因中的定位、从草图到硬模型（Hard Model）全流程 | Sprint 2: Class 11 | Ch. 11 | 工业设计师的推演逻辑、造型语言与人机工程要求 |
| [Lec 7 概念生成与系统探索](./lec7.md) | 功能分解黑盒模型、内外检索策略、TRIZ 矛盾矩阵、概念组合表 | Sprint 1: Class 6 | Ch. 7 | 突破思维惯性，穷尽系统解空间的高效工具 |
| [Lec 8 原型制作实务与五级模型](./lec8.md) | 原型四大用途、五级模型体系（概念草模到工程核验模）、快速成型法 | Sprint 2: Class 9 | Ch. 14 | 物理制造原型的阶段规划与降风险原型测试策略 |
| [Lec 9 概念筛选与评分决策](./lec9.md) | Pugh 概念筛选矩阵、参考项基准法、多属性加权评分矩阵 | Sprint 1: Class 6 / Sprint 2 决策 | Ch. 8 | 团队结构化决策机制，落实“完善而非简单淘汰”原则 |
| [Lec 12 知识产权策略与技术许可](./lec12.md) | 专利/商标/版权/商业秘密权利边界、绕开设计、Bayh-Dole 法案与大学 TLO | Sprint 3: Class 13 | Ch. 16 | 科技创业者的技术壁垒构筑与侵权防御全景 |
| [Lec 17 新产品需求预测](./lec17.md) | Bass 扩散模型（创新系数 $p$ / 模仿系数 $q$）、Rogers 采纳五要素、A-T-A-R 漏斗 | Sprint 4: Class 16, 17 | Ch. 18 | 评估新产品市场渗透曲线与销量爬坡的量化推演 |
| [Lec 20 设计结构矩阵（DSM）](./lec20.md) | 任务依赖与参数耦合、DSM 排序分块算法、撕裂迭代仿真、跨职能团队聚类 | Sprint 3: Class 14 (产品架构专题) | Ch. 10 | 解决复杂工程项目中循环迭代与组织协同的图论利器 |

## 权威参考书目与核心文献

### 核心教材
- **《Product Design and Development》**（第 8 版，2026 年最新版），Karl T. Ulrich, Steven D. Eppinger, Maria C. Yang 著，McGraw-Hill 出版。全书全面覆盖现代敏捷开发、服务设计、数字/物理混合系统与产品开发经济学。

### 核心专题文献
- **机会与需求发现**：
  - Day, G. S. (2007). *Is It Real? Can We Win? Is It Worth Doing?* Harvard Business Review.
  - Patnaik, D., & Becker, R. (1999). *Needfinding: The Why and How of Uncovering People's Needs.* Design Management Journal.
  - Christensen, C. M., et al. (2016). *Know Your Customers' "Jobs to Be Done".* Harvard Business Review.
- **敏捷与现代制造**：
  - Eppinger, S. D., et al. (2021). *Agile for Hardware Development.* CoLab Technical Keynote.
  - Wevolver (2025). *How to 3D Print: A Quick-Start Guide for Engineers.*
  - Teel, J. (2026). *How to Prototype a New Electronic Hardware Product.* Predictable Designs.
- **商业模式与战略转向**：
  - Cooper, R., & Slagmulder, R. (1999). *Develop Profitable New Products with Target Costing.* Sloan Management Review.
  - Ovans, A. (2015). *What Is a Business Model?* Harvard Business Review.
  - BreakoutLearning (2025). *Airbnb: Testing Hypotheses and Iterative Pivoting toward Product-Market Fit.*
- **生成式 AI 与未来创新**：
  - Harvard Business Review (2025). *To Jumpstart Creativity, Try These 8 Prompts.*
