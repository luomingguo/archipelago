---
title: '6.4500 Web 设计：语言和用户接口'
type: course
course: '6.4500 Web 设计：语言和用户接口'
course_id: '6.4500'
tags: [human-computer-interaction, usability, web-design, user-interface, front-end-development]
status: complete
source: https://designftw.mit.edu/
---
# 6.4500 Web 设计：语言和用户接口

https://designftw.mit.edu/


## TL;DR

- 课程把人机交互原则与 Web 实现放在同一条学习路径中，同时衡量可学习性、效率、安全性与视觉表达。
- 技术主线从 HTML、CSS、JavaScript 和 DOM 延伸到异步编程、Web API、数据可视化、动效与响应式界面。
- 设计主线通过需求发现、原型、用户测试、启发式评估和设计批评，把用户证据转化为可迭代的界面决策。
- 实验与课程项目要求学习者同时验证代码行为和用户体验，而不是把设计与工程拆成两个孤立阶段。

## 课程描述

### 先修课程

- **MIT 6.1010**（原 6.009）计算机编程基础（Fundamentals of Programming）：熟练掌握 Python 或面向对象编程、递归、基础数据结构及算法思维。

### 官方课程描述

MIT 6.4500（原 6.S063）*Design for the Web: Languages and User Interfaces* 将人机交互（HCI）的核心人本理论与当代 Web 前端工程实践融为一体。课程打破“设计交由视觉设计师、实现留给后端/工程师”的传统孤岛思维，深入剖析现代 Web 标准技术（HTML5、CSS3、ES2020+、SVG 及 Web API）的表达力与工程约束。学生将掌握以用户为中心的设计全生命周期——从需求发现、纸面原型、尼尔森启发式走查，到真实用户测试、信息架构组织、无障碍合规设计（WCAG），并最终独立构建出可交互、高保真、具备工业级可用性的现代 Web 应用程序。

### 培养目标

1. **掌握经典可用性评估模型**：深入理解并能定量/定性衡量界面的三维核心指标——可学习性（Learnability）、效率（Efficiency）与安全性（Safety）；
2. **精通 Web 平台三层架构契约**：
   - **结构层（Structure）**：HTML 语义树与无障碍辅助技术树（Accessibility Tree）映射；
   - **表现层（Presentation）**：CSS 逻辑属性、文档流与盒模型、Flexbox/Grid 二维布局、模块化字阶、知觉均匀色彩空间（OKLCH）与 GPU 硬件加速动画；
   - **行为层（Behavior）**：DOM 事件流三阶段、闭包与原型链、现代异步管道（Promises / async-await）以及组件化响应式架构（Vue 3 / Web Components）；
3. **建立严谨的用户研究与工程迭代能力**：能独立执行双阶段启发式走查、泊松分布严重度评级、纸面原型真实被试“出声思维”测试，并将用户行为反馈转化为代码架构演进。

### 参考资料与规范

- **核心教材**：唐·诺曼（Don Norman）著《设计心理学：日常事物的设计》（*The Design of Everyday Things: Revised and Expanded Edition*）——人机交互领域的基石经典；
- **官方技术规范**：
  - [WHATWG HTML Living Standard](https://html.spec.whatwg.org/multipage/)
  - [W3C CSS Specifications & Drafts](https://www.w3.org/Style/CSS/specs.en.html)
  - [ECMAScript 语言规范（ECMA-262）](https://www.ecma-international.org/ecma-262/)
  - [W3C Web 内容无障碍指南（WCAG 2.2）](https://www.w3.org/TR/WCAG22/)
- **开发者文档**：[MDN Web Docs](https://developer.mozilla.org/en-US/)

### 本地开发环境搭建

在现代 Web 平台中，许多核心特性（包括 ES Modules `type="module"`、Service Workers、CORS 跨源资源共享、Fetch API 以及部分现代 CSS/Web Components 特性）在直接双击打开的 `file://` 协议下会被浏览器的同源安全策略完全阻断。

因此，进行课程练习与实验必须在本地运行一个简易 HTTP 静态服务器：

1. **Node.js 环境（推荐）**：
   ```bash
   # 安装并在项目根目录下启动
   npx http-server -p 8000
   ```
2. **VS Code 编辑器扩展**：安装 `Live Server` 扩展，点击右下角状态栏的 **Go Live**，即可启动本地开发服务器并享受热更新（Live Reload）功能。

## 课程内容全景

### 模块架构

全课程 24 讲讲义划分为四大有机融合的知识模块：

- **模块一：可用性基础与认知工程（Lec 1, 3, 5, 7, 9, 11）**：系统阐述人机交互三大支柱（可学习性、效率、安全性）、纸面原型设计、双阶段尼尔森启发式走查与出声思维用户测试；
- **模块二：表现层与视觉设计系统（Lec 2, 4, 6, 8, 10, 13, 17, 19）**：从语义 HTML 到 CSS 盒模型、Grid/Flexbox 网格、国际化逻辑属性、排版几何学、OKLCH 知觉色彩与统一 Web 设计哲学；
- **模块三：交互驱动与现代组件架构（Lec 12, 14, 15, 16, 18, 20, 21, 22）**：从现代 JavaScript/DOM 事件流延伸至函数式编程、原型继承、异步事件循环、RESTful/Token 授权、Vue 3 响应式、信息可视化通道与 GPU 合成动效；
- **模块四：开放生态与未来交互（Lec 23, 24）**：解密万维网标准化组织运转机制（W3C/WHATWG/IETF/TC39）以及面向概率性 AI 系统的人机协作信任校准与伦理设计。

### 讲义全景列表

- [Lec 1 介绍与总览](./lec1.md)：课程双主线、人机交互核心价值与可用性三大支柱。
- [Lec 2 Web 网页结构：HTML](./lec2.md)：HTML 语义化、可访问性树映射、常用标签契约与响应式表单。
- [Lec 3 可学习性](./lec3.md)：目标导向学习、信息觅食理论、指示物与可供性、响应时间阈值与因果闭环反馈。
- [Lec 4 图形设计](./lec4.md)：格式塔视知觉六大律、爱德华·塔夫特数据油墨比、视觉层级与战略留白。
- [Lec 5 效率](./lec5.md)：菲茨定律运动时间对数模型、击键级模型（KLM）操作预测与专家级快捷键加速。
- [Lec 6 CSS 的基本概念 I](./lec6.md)：文档流、盒模型（content-box vs border-box）、外边距折叠与现代伪类选择器。
- [Lec 7 安全性](./lec7.md)：人类差错分类学（Slips vs Mistakes）、捕获/模式差错、强制功能与撤销模型。
- [Lec 8 CSS 的基本概念 II](./lec8.md)：层叠上下文（Stacking Context）、特异度（Specificity）计算与 DRY 可维护原则。
- [Lec 9 启发式评估](./lec9.md)：打折可用性工程、尼尔森十大原则逐条剖析、专家走查流程与泊松模型边际收益。
- [Lec 10 布局](./lec10.md)：常规流、一维 Flexbox、二维 CSS Grid、声明式 CSS 锚定定位（Anchor Positioning）。
- [Lec 11 原型和用户测试](./lec11.md)：保真度取舍、纸面原型实验流、出声思维测试法与关键事件伦理规范。
- [Lec 12 现代 JavaScript 和 DOM](./lec12.md)：ES6+ 核心语法、变量作用域、DOM 查询遍历与节点生命周期操作。
- [Lec 13 统一 Web 设计](./lec13.md)：能力连续谱模型、WCAG POUR 核心原则、CSS 逻辑属性全套映射与无障碍表单。
- [Lec 14 事件](./lec14.md)：浏览器事件循环、W3C 捕获/目标/冒泡三阶段事件流、事件委托模式与 CustomEvent。
- [Lec 15 设计模式与函数式 JavaScript](./lec15.md)：高阶函数、纯函数契约、不可变性与数据流水线。
- [Lec 16 函数、类和 this](./lec16.md)：一等公民函数、词法作用域闭包、原型链机制、class 语法糖与 ES 模块化。
- [Lec 17 字体](./lec17.md)：字体心理学、模块化字阶（Modular Scales）、舒适阅读行长与 Web Font 性能优化。
- [Lec 18 异步编程](./lec18.md)：单线程 Event Loop、微任务队列、Promise 状态机、async/await 与并发模式。
- [Lec 19 色彩](./lec19.md)：视觉感光生理学、sRGB/HSL 感知缺陷、知觉均匀色彩空间（OKLCH）与 APCA 对比度计算。
- [Lec 20 Web API 与组件架构](./lec20.md)：HTTP 通信演进、RESTful 语义规范、无状态 Token 认证、Vue 3 响应式与 Web Components。
- [Lec 21 信息可视化](./lec21.md)：雅克·贝尔廷 7 大视觉变量、麦金利通道精确度排序、图表决策树与刷选联动。
- [Lec 22 动画与反馈](./lec22.md)：注意力引导心理学、CSS Houdini 动画、GPU 合成管道优化与前庭无障碍防护。
- [Lec 23 Web 标准](./lec23.md)：浏览器大战历史沉浮、W3C/WHATWG 标准化全流程、规范测试驱动与开源参与路径。
- [Lec 24 面向 AI 系统的设计](./lec24.md)：概率性系统的范式转移、不确定性应对模式、人机协作四种范式与校准信任。

### 核心概念索引

课程沉淀了 14 篇符合 7 步标准论证结构的独立核心概念笔记（Concept Notes）：

- [可用性三要素](./concept/usability-dimensions.md)：可学习性、效率、安全性的正交权衡与生命周期演进。
- [指示物与可供性](./concept/affordance-and-signifier.md)：客观能力与主观视觉线索的四象限模型与诺曼门解法。
- [信息觅食与信息气味](./concept/information-foraging.md)：动物觅食类比、三级认知代价阶梯与具象超链接文本设计。
- [菲茨定律](./concept/fittss-law.md)：目标到达时间对数预测模型、屏幕边缘无限大宽度与触控热区底线。
- [击键级模型（KLM）](./concept/keystroke-level-model.md)：GOMS 专家级无差错操作时间量化预测与键鼠切换惩罚。
- [差错分类与强制功能](./concept/human-errors-and-forcing-functions.md)：失误 vs 错误、互锁/闭锁/锁入机制与撤销优先原则。
- [启发式评估与打折工程](./concept/heuristic-evaluation.md)：尼尔森十大原则、泊松 3–5 人拐点与严重度分级。
- [CSS 盒模型与层叠上下文](./concept/css-box-model-and-stacking-context.md)：边框盒尺寸隔离、外边距折叠定律与 Z 轴三维渲染层级树。
- [CSS 锚定定位](./concept/css-anchor-positioning.md)：W3C 原生声明式浮层几何吸附、`@position-try` 视口智能翻转与无 JS 方案。
- [能力连续谱与统一 Web 设计](./concept/universal-design-and-accessibility.md)：永久/暂时/情境障碍等效性、WCAG POUR 支柱与 CSS 逻辑属性自适应。
- [DOM 事件流与事件委托](./concept/dom-event-flow.md)：捕获/目标/冒泡三阶段、`closest()` 委托模式与事件传播阻断边界。
- [Vue 响应式模板](./concept/vue.md)：数据模型依赖追踪、`v-if` vs `v-show` 性能权衡与计算属性缓存。
- [知觉均匀色彩空间与 APCA 对比度](./concept/perceptually-uniform-color.md)：HSL 伪明度缺陷、OKLCH 正交模型、Display P3 广色域与神经感知对比度。
- [人机协作模式与校准信任](./concept/human-ai-collaboration.md)：概率性系统范式转变、AI 先行/人类先行四种协同模式与自动化偏见治理。

### 作业与实验工坊（Studio & Assignments）

课程配套了 13 个实践作业与 13 个动手工坊，引导学生从零开始迭代一个全功能即时通讯应用（Chat/Messaging App）：

- **作业（Assignments）**：
  - [HW 1: 日常事物设计观察与基础 HTML](https://designftw.mit.edu/assignments/hw1)
  - [HW 2: 图形设计与可学习性评估](https://designftw.mit.edu/assignments/hw2)
  - [HW 3: 用 CSS 修复 Web 页面与安全性案例](https://designftw.mit.edu/assignments/hw3)
  - [HW 4: 交互式 CSS 动效与样式评估](https://designftw.mit.edu/assignments/hw4)
  - [HW 5: 个人主页重构与即时通讯 UI 评估](https://designftw.mit.edu/assignments/hw5)
  - [HW 6: 网页抓取器与即时通讯需求发现](https://designftw.mit.edu/assignments/hw6)
  - [HW 7: 统一 Web 改造与纸面原型设计](https://designftw.mit.edu/assignments/hw7)
  - [HW 8: 纸面原型用户测试与内容屏蔽小书签](https://designftw.mit.edu/assignments/hw8)
  - [HW 9: Figma 高保真模型与排版优化](https://designftw.mit.edu/assignments/hw9)
  - [HW 10: 高保真原型用户测试与色彩优化](https://designftw.mit.edu/assignments/hw10)
  - [HW 11: 客户端路由与组件化重构](https://designftw.mit.edu/assignments/hw11)
  - [HW 12: 动效添加与中期检查点](https://designftw.mit.edu/assignments/hw12)
  - [HW 13: 即时通讯项目最终提交与展示](https://designftw.mit.edu/assignments/hw13)

- **实验工坊（Studios）**：
  - [Studio 1 至 Studio 13 官方在线指导](https://designftw.mit.edu/studio/1/)：覆盖命令行、Git 协作、Flexbox 排版、DOM 脚本、Vue 响应式与状态管理实践。
