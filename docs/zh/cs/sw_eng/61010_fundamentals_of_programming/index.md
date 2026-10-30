---
title: 课程主页 | 6.1010 程序设计基础（Fall 26）
type: course
course: 6.1010 程序设计基础（Fall 26）
course_id: '6.1010'
tags: [python, programming-paradigms, recursion, software-design]
status: complete
---

# 6.1010 程序设计基础（Python 版）

> MIT 6.1010 · Fundamentals of Programming · 官方主页：[py.mit.edu/fall26](https://py.mit.edu/fall26)（备用归档：[py.mit.edu/spring26](https://py.mit.edu/spring26)）

## TL;DR

- **课程定位**：MIT 计算机科学核心编程基石课，专注于从机械式编码进阶为具备规范工程思维与抽象能力的软件构建者。
- **知识体系**：以执行环境模型贯穿，系统涵盖函数式闭包、图搜索与路径规划、树与图递归、回溯剪枝以及面向对象类型系统。
- **工程训练**：通过音频处理、二维卷积图像滤镜、推箱子游戏求解与 SAT 算法等深度实验，全面建立测试驱动与防御性调试能力。

## 课程定位与学习目标

6.1010（原 6.009 / 6.101）是 MIT 面向计算机专业学生的核心软件开发与算法实战课程。与简单的 Python 语法入门不同，本课程旨在帮助学习者建立关于计算机执行的深层心智模型，掌握管理软件系统复杂度的三大基石：基本构件、组合手段与抽象屏障。

### 编程技能目标

- **地道 Pythonic 设计**：熟练运用生成器、解包、列表推导、一等函数和魔法方法（dunder methods）编写清晰高效的代码。
- **测试与调试闭环**：熟练利用 `pytest` 编写单元测试，掌握断言、交互式 REPL、Traceback 分析及科学假设排除法。
- **工程规范与工具链**：掌握虚拟环境隔离（venv）、静态代码检查（ruff/pylint）及代码风格约束（PEP 8）。

### 认知模型目标

- **脱离计算机的心智推演**：借助“环境模型图”（Environment Model），准确推演闭包、高阶函数、递归调用栈和面向对象属性查找链的内存行为。
- **算法权衡与复杂度直觉**：理解不同数据结构（列表、集合、字典、生成器）在时空开销上的本质差异，避免意外引入 $O(n^2)$ 瓶颈。
- **问题分解与状态空间抽象**：将现实问题（迷宫、拼图、游戏、表达式求值）抽象为状态图，利用 BFS、DFS 与回溯剪枝实现高效求解。

## 课程知识体系与讲义清单

课程内容分为四大模块：运行机理与函数抽象、搜索算法与递归模式、面向对象系统构建、函数式编程与性能优化。

### 模块一：运行机理与函数抽象

- [Lec 0 设计程序指南与命令行工具](./lec0.md)：波利亚解题四步法、模块化分解、虚拟环境配置与自动化测试套件。
- [Lec 1 执行环境模型](./lec1.md)：堆栈分离、变量绑定、引用语义、不可变与可变对象、列表切片内存布局及垃圾回收机制。
- [Lec 2 函数的高级用法与闭包](./lec2.md)：函数作为一等公民、嵌套作用域、闭包帧、延迟绑定陷阱与柯里化工厂函数。

### 模块二：搜索算法与状态空间

- [Lec 3 洪水填充与调试排错](./lec3.md)：图像染色问题、基于待办议程（Agenda）的搜索骨架、集合去重加速与防御性调试技巧。
- [Lec 4 图搜索与抽象路径规划](./lec4.md)：图的抽象定义与字典表示、广度优先搜索（BFS）求最短路径、深度优先搜索（DFS）与死循环防范。
- [Lec 5 递归基石与递归环境模型](./lec5.md)：递归两要素（基准情形与递推步骤）、调用栈帧推演、数字与扁平列表的递归处理。
- [Lec 6 树与图的递归模式及生成器](./lec6.md)：嵌套列表与树形结构遍历、尾递归与索引优化、生成器函数与 `yield from` 惰性求值。
- [Lec 7 递归回溯搜索](./lec7.md)：约束满足问题、决策树与剪枝机制、可变默认参数陷阱、数独与布尔可满足性（SAT）求解。

### 模块三：面向对象与类型系统

- [Lec 8 自定义类型与环境模型](./lec8.md)：类与实例在环境模型中的表示、方法分发规则与 `self` 的本质、链表实现与魔法方法协议。
- [Lec 9 继承与面向对象设计模式](./lec9.md)：单继承与多层继承、属性查找继承链、`super()` 调用机制、形状绘图库案例与组合优于继承。

### 模块四：函数式范式与高级特性

- [Lec 10 函数式编程与记忆化](./lec10.md)：纯函数与无副作用原则、函数对象模拟类、`nonlocal` 状态封装、记忆化缓存与装饰器模式。

## 实验与工程训练

- [基础设施与实验指南（Lab 0 & Lab 1/2）](./lab.md)：涵盖开发环境配置、Lab 0 单声道音频处理（倒放、混音、一维卷积与回声效果）以及 Lab 1/2 二维图像卷积滤镜（灰度反转、高斯模糊、锐化、边缘检测与接缝裁剪）。

## 官方资源与参考书目

- **官方教学站点**：[py.mit.edu/fall26](https://py.mit.edu/fall26)
- **往期归档平台**：[py.mit.edu/spring26](https://py.mit.edu/spring26)
- **推荐参考书**：
  - *Think Python: How to Think Like a Computer Scientist* by Allen B. Downey
  - *Structure and Interpretation of Computer Programs (Python Version)* by Harold Abelson, Gerald Jay Sussman
  - *Debugging: The 9 Indispensable Rules for Finding Even the Most Elusive Software and Hardware Problems* by David J. Agans
