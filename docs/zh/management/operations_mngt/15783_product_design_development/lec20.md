---
title: 产品开发的行业趋势与设计结构矩阵（DSM）
type: lecture
lecture: 20
tags: [npd-process, stage-gate, design-structure-matrix, iteration, team-integration, product-architecture]
status: complete
source: 'https://ocw.mit.edu/courses/15-783j-product-design-and-development-spring-2006/resources/cls20_tol_trds/'
---

# Lec 20 产品开发的行业趋势与设计结构矩阵（Tools & Trends in Product Development）

> MIT 15.783 · Product Design and Development · 主讲 Thomas A. Roemer

## TL;DR

- 本讲分两部分：前半部分基于 PDMA（Product Development & Management Association）行业调研数据，勾勒美国企业新产品开发（NPD）流程、工具使用现状与项目绩效基准；后半部分由 Thomas Roemer 系统讲授设计结构矩阵（DSM，Design Structure Matrix），一种比 Gantt/PERT 更能刻画信息依赖与迭代的项目建模工具。
- 行业数据显示 56% 的企业采用某种 Stage-Gate 流程，但"重要性"与"实际使用程度"之间存在系统性落差：客户之声（VOC）、客户现场访问、快速原型、项目排期工具、产品champion 被评为最重要的五项工具/实践。
- DSM 把传统 Gantt/PERT 忽略的迭代（iteration）和返工（rework）显性建模：通过对角线外的依赖标记（X）区分串行、并行、耦合三种任务关系，再用排序算法把矩阵重排为尽量下三角的形式，暴露出真正需要迭代求解的耦合任务块。
- 制动系统设计（13 个参数）和半导体研发流程两个真实案例显示，DSM 分区（partitioning）能把杂乱的依赖网络重排成清晰的顺序—并行—耦合结构；某公司（STC）应用 DSM 重构工程流程后，试点项目周期从 116 天降至 85 天，节省 27%。
- DSM 同样可用于组织设计：把"活动型 DSM"换成"团队型 DSM"就能做团队聚类（clustering），GM 动力总成部门用此方法把 22 个开发子系统重组为 4 个系统团队加 1 个跨系统集成团队，减少了团队间不必要的耦合。

## 第一部分：新产品开发流程与工具的行业实证

本讲开篇引用 PDMA《New Product Development Handbook》的调研数据，为后续讨论的工具选择提供行业基准。

### 新产品对销售和利润的贡献

::: example 新产品贡献度与企业绩效分层相关
按企业自评的行业地位分组（Bottom Third / Middle Third / Top Third / Most Successful），新产品对当期销售额的贡献比例呈明显阶梯：High-Tech 企业从约 10% 升到近 60%，全行业均值从约 10% 升到约 45%，Low-Tech 企业则始终垫底（约 8% 升到 32%）。这说明新产品产出能力本身就是区分行业头部与尾部企业的变量，而不只是结果。
:::

同时给出的"衰减曲线"（Decay Curve）显示，从创意（Ideas，计为 100）到测试（Tested）、上市（Launched）、成功（Success）的漏斗在 1990 到 1995 年间有所改善：1990 年 100 个创意最终只剩 10 个成功产品，1995 年则提高到约 20 个，反映出企业在创意筛选和流程管理上的进步。

### Stage-Gate 流程的普及与任务分布

::: example NPD 流程使用现状
调研显示，采用某种 Stage-Gate 流程（含第三代 Stage-Gate、Facilitated Stage Gate、经典 Stage Gate 三种变体）的企业合计占 56%；其余企业采用功能顺序型（Functional, sequential）、非正式流程（Informal）甚至完全没有流程（None）。
:::

流程通常包含九类任务：产品线规划（Product Line Planning）、战略制定（Strategy Development）、创意/概念生成（Idea/Concept Generation）、创意筛选（Idea Screening）、商业分析（Business Analysis）、开发（Development）、测试与验证（Test & Validation）、制造开发（Manufacturing Development）、商业化（Commercialization）。调研进一步给出：

- **任务被纳入流程的比例**：Development 接近 100%，Commercialization、Test & Validation 也在 90% 以上，而 Product Line Planning 只有约 60%——说明企业更愿意把"怎么做产品"流程化，而不是"该不该做这个产品"。
- **实际完成任务的项目比例**：各任务普遍在 75%-85% 区间，Screening 略低（约 74%）。
- **平均耗时**：Development 阶段耗时最长（约 32 周），其后依次是 Test & Validation（约 21 周）、Manufacturing Development 和 Commercialization（约 18-19 周），前期的 Product Line Planning、Project Strategy、Idea Generation、Screening、Business Analysis 都在 10 周以内。

### 多职能团队的使用与工具重要性—使用度落差

多职能团队（Multifunctional Teams）的采用率随项目创新程度递增：New-to-World 和 New-to-Firm 项目中约 80% 采用多职能团队，Major Revision 约 77%，而 Cost Reduction、Repositioning、Minor Improvement 等渐进型项目仅 40%-46%，说明企业倾向于把跨部门协作资源集中投向高风险、高不确定性的项目。

调研进一步以雷达图对比"感知重要性"与"实际使用程度"，覆盖三类工具：

::: example 三类工具的重要性—使用度对比
- **营销研究类**：客户之声（Voice of Customer）、客户现场访问（Customer Site Visits）、概念测试（Concept Tests）、焦点小组（Focus Groups）、Beta 测试、联合分析（Conjoint Analysis）、测试市场（Test Markets）、预测试市场（Pre-Test Markets）——各项目的"重要性"评分普遍高于"使用度"，Voice of Customer 缺口最明显。
- **工程类**：快速原型（Rapid Prototyping）、并行工程（Concurrent Engineering）、面向制造的设计（DFM）、CAD、CAE、价值分析（Value Analysis）、FMEA、性能仿真（Performance Simulation）、虚拟设计（Virtual Design）——同样呈现"认为重要但用得较少"的模式。
- **组织类**：项目排期工具（CPM/PERT/Gantt）、产品champion、流程负责人（Process Owner）、团队建设、重量级项目经理（Heavyweight Manager）、自我管理团队、矩阵组织、QFD、同地办公团队（Colocated Teams）、无领导团队（Leaderless Teams）——组织类工具的重要性—使用度落差相对最小，说明组织机制比营销/工程工具更容易被真正落地。
:::

最终榜单：**感知重要性 Top 5** 为客户之声（4.2 分）、客户现场访问（3.9）、快速原型（3.9）、项目排期工具（3.9）、产品champion（3.9）；**实际使用频率 Top 5** 为项目排期工具（3.7）、客户之声（3.6）、客户现场访问（3.5）、CAD（3.4）、矩阵组织（3.2）。两份榜单高度重叠但排序不同，说明项目排期工具、客户之声和客户现场访问是少数"既重要又真被用"的核心实践，而快速原型和产品champion则更多停留在"认为重要但落地不足"的状态。

### 产品成功率与项目周期基准

::: example 新产品成功率与开发周期
- 主观认定"成功"的产品比例为 55.9%；盈利的比例为 51.7%；上市 5 年后仍在市场上的比例为 74.1%。
- 客户接受度、财务表现、技术表现三类绩效标准的相对权重因项目类型而异：New-to-World 项目中客户接受度权重最高，而 Repositioning 等渐进型项目中财务表现权重相对更高。
- 平均开发周期随创新程度显著拉长：渐进式改进（Incremental Improvement）约 8 周，下一代产品（Next Generation）约 18 周，新产品线（New Product Line）约 29 周，全新产品（New-to-World）约 42 周。
:::

这部分数据来自 Rosenau 等编著的《PDMA Handbook of New Product Development》，Stage-Gate 相关内容参考 Robert G. Cooper《Winning at New Products》。

## 第二部分：设计结构矩阵（DSM）——刻画迭代与集成的工具

后半部分由 Thomas Roemer 讲授。切入点是一个明确的批判：传统项目管理工具（Gantt 图、PERT/CPM 网络图、IDEF 流程图）虽然直观，但共享三个系统性缺陷——**只描绘工作流而非信息流**、**假设任务可以被最优分解且忽略集成问题**、**完全忽略迭代与返工**。产品开发本质上是高度耦合、充满迭代的过程，这些工具因此系统性低估了真实的开发时间和复杂度。

### DSM 的基本结构与四种类型

DSM 是一个 N×N 方阵，行和列代表同一组任务（或参数、团队、产品模块），非对角线上的标记表示"行任务需要列任务提供的信息（输入）"。与传统网络图相比，DSM 的优势在于：**信息流比工作流更容易被准确捕捉**，且**输入关系比输出关系更容易被工程师准确描述**（工程师通常清楚自己需要什么信息，却不一定清楚自己的产出被谁使用）。

课程区分了四种 DSM，并对应两类核心问题：

::: note DSM 的四种类型与对应问题
- **活动型 DSM（Activity-based）**、**参数型 DSM（Parameter-based）** → 用于解决**迭代问题**：排序（Sequencing）、分区（Partitioning）、仿真（Simulation）。
- **团队型 DSM（Team-based）**、**产品架构型 DSM（Product Architecture DSM）** → 用于解决**集成问题**：聚类（Clustering），进而映射到组织结构和产品架构设计。
:::

DSM 的构建方式包括查阅设计手册、流程文档，以及更常用的**结构化专家访谈**（访谈工程师和经理，列出任务/参数清单，逐一询问输入输出与依赖强度，填入矩阵，再回访确认）和问卷调查。

### 迭代问题：排序、分区与仿真

三种任务关系被明确定义：**串行（Dependent/Series）**——B 依赖 A 的输出，只能先 A 后 B；**并行（Independent/Parallel）**——A、B 互不依赖，可同时进行；**耦合（Interdependent/Coupled）**——A、B 互为输入输出，必须迭代求解。

**排序算法（Sequencing Algorithm）** 用于把一个杂乱的依赖矩阵重排成尽量接近下三角的形式：

::: example DSM 排序算法的七个步骤
1. 调度所有"空行"（不依赖任何其他任务）的任务，排在最前。
2. 从矩阵中删除该任务对应的行和列。
3. 重复步骤 1-2，直到没有空行任务为止。
4. 转而调度所有"空列"（没有任何任务依赖它）的任务，排在最后。
5. 删除对应行列。
6. 重复步骤 4-5。
7. 剩余未被调度的任务即互相耦合，需要围绕对角线成块（block）聚合，作为需要联合迭代求解的任务集合。
:::

::: example 制动系统设计（13 个设计参数）
课程给出一个真实的制动系统设计 DSM：13 个参数（客户需求、车轮扭矩、踏板机械优势、系统级参数、转子直径、ABS 显示模块、前衬片摩擦系数、后活塞尺寸、卡钳顺应性、前活塞尺寸、后衬片摩擦系数、助力器最大行程、助力器反应比）之间存在密集的相互依赖。原始顺序下矩阵充满对角线上方（前瞻）的 X 标记，意味着大量隐藏迭代；经排序算法重排后（新顺序：1,4,2,10,8,3,11,7,13,5,12,9,6），矩阵中大部分依赖被压入下三角区域，只剩下"助力器反应比"等少数几个高度耦合的参数块，直观暴露出真正需要联合求解的设计变量子集。
:::

课程还展示了一个**半导体产品开发流程**的大型 DSM（约 50 个任务，从"设定客户目标"到"交付产品给客户"），用方框标出三类结构：并行活动块（Concurrent Activity Blocks）、顺序活动（Sequential Activities）、代际学习反馈（Generational Learning Feedback）与潜在迭代环（Potential Iterative Loops），说明真实产品开发流程是"顺序段—并行段—耦合段"交替出现的复杂结构，而非教科书式的单向瀑布。

**排序不仅可用于定性分析，也可形式化为优化问题。** 课程给出"块分解"（Block Decomposition）的整数规划模型：目标是最小化跨阶段的高权重反馈弧数量（$\min \sum_{ij \in A} a_{ij} n_{ij} y_{ij}$），约束条件包括每个活动必须被分配到唯一阶段、每阶段容量上限 C、以及反馈弧的判定逻辑。该模型应用到一个涡轮/火箭发动机相关的"概念设计模块"（27 个活动）真实案例，把原本杂乱的依赖矩阵重排为清晰的分阶段结构（对应 Space Shuttle Main Engine 的部件设计场景：燃烧室、涡轮泵、喷嘴等高度耦合子系统）。

::: example STC 案例：DSM 驱动的流程重组，周期缩短 27%
某公司（STC）原有流程是概念设计→谈判→详细设计→制造与测试的严格串行结构，项目办公室（Program Office）与项目团队（Project Team）、职能部门（Functional Departments）彼此隔离。基于 DSM 分析，提出的新流程让核心设计团队（Core Design Team）打通项目办公室与职能部门的壁垒，允许概念设计、详细设计等阶段并行推进。试点项目结果：概念设计从 9 天延长到 20 天（前期投入更多信息交换以减少下游返工），但详细设计从 39 天压缩到 25 天，制造与测试从 68 天压缩到 40 天，总周期从 116 天降到 85 天，**节省 27%**。这是"以前期慢换后期快"的典型迭代管理效果——通过在耦合阶段提前充分交换信息，减少下游的意外返工。
:::

**DSM 仿真**进一步把迭代概率和影响程度量化。以三任务耦合环 A→B→C→A 为例：任务 A 需要任务 C 的输出，做法是先假设 C 的输出值执行 A，再把结果依次传给 B、C，最后用 C 的真实输出检验 A 的初始假设。矩阵中引入两个参数：

- **R（返工概率，Rework Probability）**：C 完成后 A 被要求重做的概率，R=0 表示完全不会返工，R=1 表示必然返工。
- **I（返工影响，Rework Impact）**：若 A 确实被要求返工，需要重复其原始工期的比例，I=0 表示零成本重做，I=1 表示需要完全重新执行。
- 此外还存在**二阶返工（2nd Order Rework）**：A 的返工可能进一步触发依赖 A 的下游任务（如 B）连锁返工。

把这些概率和影响参数填入 DSM 后，结合信息流矩阵做蒙特卡洛式多次仿真运行，可以得到项目总工期/成本的概率分布（课程引用 Tyson R. Browning 的 MIT 博士论文数据，展示一个围绕目标（Target）呈右偏态分布的工期直方图），并可比较不同任务排序方案下的分布差异。课程也用一张"带迭代的 Gantt 图"对比：标准 Gantt 图呈现单调推进的假象，而真实项目行为包含任务停止、重启、重复、连锁影响其他任务的复杂动态。

::: insight 迭代方面的核心结论
产品开发本质上是迭代的；理解任务间的耦合关系是管理开发过程的前提。迭代虽然消耗时间，但也是提升质量的必要环节，不能简单当作"浪费"消除。加速迭代的三条路径分别是信息技术（缩短单次迭代周期）、协调机制（提升迭代效率）、降低耦合本身（减少迭代次数，即从架构层面减少不必要的依赖）。此外要区分**计划内迭代**（Planned Iteration，主动追求第一次就做对）与**计划外迭代**（Unplanned Iteration，出错后被动补救），两者管理逻辑完全不同。
:::

### 集成问题：DSM 聚类与组织/架构设计

第二类问题是团队/架构层面的集成：如何基于依赖结构而非传统职能分工来组建团队。课程指出团队组建在实践中往往是机会主义的（"我们就是抓手边有空的人"），而信息流分析可以给出更合理的分组依据。

**团队型 DSM 聚类（Clustering）**：以 7 个任务（A-G）为例，依赖强度分为无依赖（No Dependency，白）、低（Low，黄）、高（Hi，红）三档；聚类算法通过重排行列顺序（例如从原始顺序 A-B-C-D-E-F-G 重排为 A-F-E-D-B-C-G），把高强度依赖尽量集中到对角线附近的小块中，从而识别出应当组成同一团队的任务子集（如 {A,F} 与 {D,B,C,G} 两个紧密集群）。课程还展示了**重叠团队（Overlapped Teams）**方案：允许某些任务（如 E）同时属于两个相邻集群的边界，用于处理集群间仍存在的中等强度依赖，避免生硬切分导致的协调缺口。

::: example GM 动力总成部门的团队重组
GM Powertrain 部门原有 22 个开发子系统（曲轴、活塞、连杆、飞轮、润滑、气缸盖、凸轮轴/气门机构、水泵/冷却、进气歧管、燃油系统、附件驱动、空气滤清器、节气门体、排气、EGR、EVAP、点火、ECM、电气系统、发动机总成等），按传统职能被组织进 22 个独立开发团队，团队间高强度依赖（用大黑点标记）散布于矩阵各处，缺乏清晰边界。经 DSM 聚类分析后，重组为 **4 个系统团队**——短机体（Short Block：机体、曲轴、活塞、连杆、飞轮、润滑）、气门系统（Valve Train：气缸盖、凸轮轴/气门机构、水泵/冷却）、进气系统（Induction：进气歧管、附件驱动、空气滤清器、节气门体、燃油系统）、排放与电气（Emissions & Electrical：排气、EGR、EVAP、电气系统、电子系统、点火）——加上一个跨越所有子系统的**系统集成团队（System Integration Team）**，专门负责点火、ECM、电气系统、发动机总成等高连接度、跨团队依赖强的模块。重排后的矩阵显示，四个系统团队内部依赖高度集中在各自的对角线方块中，团队间残留依赖被显性地收拢到集成团队负责的区域，而非散落在整个组织里。
:::

::: insight 集成方面的核心结论
大型开发项目必然要求多个活动并行推进，众多子系统必须被集成为一个整体系统解决方案。对信息依赖关系进行系统性映射，能够揭示系统工程背后的真实结构；组织架构和产品架构都可以（也应当）基于这一结构来设计，而不是沿用历史职能分工或凭经验拍板。
:::

## 结语

课程总结 DSM 满足了产品开发中一个长期被忽视的核心需求——**把被交换的信息显性地记录下来**。相比传统 Gantt/PERT 工具，DSM 提供了一种在视觉上更强大的方式，用于设计、优化和沟通产品开发活动的真实结构，并已在工业界（制动系统、半导体、火箭发动机、汽车动力总成等）被验证有效。延伸阅读指向 Eppinger 发表于《Harvard Business Review》（2001 年 1 月）的文章 "Innovation at the Speed of Information"。
