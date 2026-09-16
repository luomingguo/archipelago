---
title: 6.1100 计算机语言工程
type: course
course: 6.1100 计算机语言工程
course_id: '6.1100'
tags: [compiler-construction, code-generation, program-analysis, optimization]
status: complete
source: https://6110-sp25.github.io/lecture-notes
---
# 6.1100 计算机语言工程

> MIT 6.1100 / 6.035 Computer Language Engineering · Spring 2025 · Martin Rinard

## TL;DR

- 课程以「Decaf 源程序 → 可执行 x86-64 代码」为完整工程主线，串联解析、IR、语义检查、代码生成与优化。
- 学习重点不只是单个算法，而是如何选择程序表示，让正确性、可分析性与高效代码生成能逐层衔接。
- 建议按 L1–L6 完成前端与未优化后端，再读 L7–L12 的数据流、循环、寄存器分配和并行化。

## 资料来源与整理说明

- 官方入口：[课程大纲](https://6110-sp25.github.io/syllabus)、[课程进度](https://6110-sp25.github.io/schedule)、[逐讲 lecture notes / slides](https://6110-sp25.github.io/lecture-notes)与[编译器项目](https://6110-sp25.github.io/project)。
- 各讲以官方 slides 为主来源，并吸收与本讲直接相关的 re-lecture 讲义和 recitation 材料；页面 frontmatter 保留对应主讲义链接。
- 官网列出的课堂录像位于 MIT Panopto，需登录才能访问，当前无法取得可公开核验的 transcript；因此本轮没有把未核验的字幕当作课程原文。

## 先行条件

6.1020/6.031 Software Construction

6.1903 Introduction to Low-level Programming in C and Assembly

6.1910/6.004 Computation Structures

## 课程定位与范围

分析与实现高级编程语言相关的问题。编译器的基本概念、功能和结构。理论与实践的互动。使用工具构建软件。包括一个关于编译器设计和实现项目。

主讲教师：Martin Rinard。

## 资源

### 推荐教材

这门课没有必备教材，但如果你坚持，我们认为这是一本不错的参考教材：

**Cooper， Keith D.， 和 Torczon， Linda，《[Engineering a Compiler](https://shop.elsevier.com/books/engineering-a-compiler/cooper/978-0-12-815412-0)》，第3版，Morgan Kaufmann，2022 年**

- 一本帮助理解现代编译器的新型参考教材。涵盖本课程中提到的许多优化内容（如数据流、指令调度、寄存器分配），以及现代编译器中常见的一些高级优化（如[静态单赋值（SSA）](https://en.wikipedia.org/wiki/Static_single-assignment_form)）。

你可能感兴趣的其他编译器教材：

- 虎书： 一本经典之作。引导你完成一个有深度的代码组织编译器项目。
- 龙书： 这是一篇非常非常厚重的经典参考文献，讲述为类 C 语言（例如 Decaf）编写优化编译器的过程。
- 鲸书：全面涵盖高级编译器优化。
- 《Lisp in Small Pieces》, 1996： 这是一本非常酷的书，从零开始构建*了多个*解释器，展示了语言设计选择之间的相互作用。
- 《Crafting Interpretres》, 2021：我们对想学习编译器一般知识的人（即本课程之外）的默认推荐。

### 参考文献

你会发现这些参考文献对编写编译器很有帮助。

1. 完整的 [Intel x64 manual](http://www.intel.com/content/dam/www/public/us/en/documents/manuals/64-ia-32-architectures-software-developer-manual-325462.pdf)——包含所有细节的官方PDF。
2. [x86 和 amd64 指令参考](https://www.felixcloutier.com/x86/)——由 Félix Cloutier 根据英特尔手册导出的可导航参考
3. [x86 维基](https://en.wikibooks.org/wiki/X86_Assembly/X86_Instructions) — 关于 x86 指令工作原理的好入门介绍
4. [x64 速查表](https://cs.brown.edu/courses/cs033/docs/guides/x64_cheatsheet.pdf)——布朗大学CS033中详细介绍寄存器和汇编命令的列表和表格
5. [Agner Fog 的优化页面](https://agner.org/optimize/)——这是一个非常有用的参考页面，里面有关于如何优化x86-64代码的手册。特别是，看看[指令表](https://agner.org/optimize/instruction_tables.pdf)。
6. [Godbolt](https://godbolt.org/) —— 允许你输入 C 代码，并提供各种编译器（如 gcc 和 clang）的逐行汇编输出，非常有用，有助于了解如何将某些操作转换为汇编。

### 工具

1. Shell
   1. [The Missing Semester of Your CS Education](https://missing.csail.mit.edu/2020/) — Learn about the shell and the terminal, then you look like a pro.
2. Scala
   1. [Tour of Scala](https://docs.scala-lang.org/tour/tour-of-scala.html)
   2. [Scala Book](https://docs.scala-lang.org/overviews/scala-book/introduction.html)
   3. [Scala Patterns for Compiler Design](https://gist.github.com/rcoh/4992969)

### 其他灵感来源

**概述**

1. [LLVM compiler architecture](http://www.aosabook.org/en/llvm.html)
2. [GCC compiler architecture](http://en.wikibooks.org/wiki/GNU_C_Compiler_Internals/GNU_C_Compiler_Architecture)

**博客**

1. [Russ Cox 的博客](http://research.swtch.com/)——Russ是Go语言的开发者之一，Go是一种流行语言。
2. [Matt Might 的博客](http://matt.might.net/articles/)——Matt是犹他大学的教授，写过一些非常有趣的文章（例如《Yacc已经死了》）
3. [Ralf 的胡言乱语](https://www.ralfj.de/blog/)——Ralf写了很多热门博客文章，探讨C++和Rust等系统语言背后的复杂性。
4. [学术界的嵌入](https://blog.regehr.org/)——同理。

**论文**

1. [寄存器分配与通过图着色溢出](http://dl.acm.org/citation.cfm?id=806984)——G.J. Chaitin / 1982。关于简单寄存器分配的优秀（简短）论文。
2. [线性扫描寄存器分配](https://dl.acm.org/citation.cfm?id=330250)
3. [《迭代寄存器融合](http://dl.acm.org/citation.cfm?id=229546)》— Lal George / 1996。对柴廷设计提出了改进和替代方案。如果 Chaitin 风格（+/-Briggs）寄存器分配还不够，这篇论文值得一读——实际上，理解权衡本身就很有价值
4. [superword 级 并行性](http://dl.acm.org/citation.cfm?id=358438)结合循环展开，是一种实现向量化编译器的简单方法

**理论**

1. [Order Theory for Computer Scientists](https://matt.might.net/articles/partial-orders/)——Matt Might 关于数据流分析基础的总结。
2. Davey， B. A. 和 H. A. Priestley，[*Introduction to Lattices and Order*](https://doi.org/10.1017/CBO9780511809088)，第二版，剑桥大学出版社，2002年。

## Decaf 编译器项目

项目的真实主线是把 C 语言子集 Decaf 编译为可执行的 x86-64 代码，不包含 MITScript 解释器或垃圾回收器。五个阶段对应课程的纵向切片：

1. **词法与语法分析**：把 Decaf 字符流变成 token 和语法树，报告词法 / 语法错误。
2. **IR 与语义检查**：建立符号表与中间表示，检查声明、类型和函数调用等上下文相关约束。
3. **未优化代码生成**：先以正确性为目标，将 IR 降级为符合 ABI 的 x86-64 汇编。
4. **数据流优化**：建立可复用的数据流框架，并用必需的优化 pass 验证它。
5. **开放式优化**：根据基准测试选择常量传播、CSE、循环不变式外提、寄存器分配、窥孔优化或并行化等技术。

## 相关课程

你可能会发现其他公开课程的讲座幻灯片或笔记很有用，尤其是在项目后期阶段：

- [卡内基梅隆大学的 15-411 编译器设计课程](https://www.cs.cmu.edu/~janh/courses/411/23/schedule.html)。
- [哈佛的 CS153 编译器课程](https://groups.seas.harvard.edu/courses/cs153/2019fa/schedule.html)。

如果你渴望更高级的内容，可以看看这个：

- [康奈尔大学的自导在线高级编译员课程](https://www.cs.cornell.edu/courses/cs6120/2020fa/self-guided/)。

中文课程：

- [中科大 2023 编译器设计 实验代码 GitLab](https://cscourse.ustc.edu.cn/vdir/Gitlab/compiler_staff/2023ustc-jianmu-compiler)

- 湖南大学 编译原理

  - bison, flex, C++, LLVM
  - 词法分析，语法分析，LLVM-IR， 优化

## 讲义目录

| 单元 | 讲义 | 学习主线 |
|---|---|---|
| 全景与前端 | [L1 编译器概览](./lec1.md) · [L2 语言规范](./lec2.md) · [L3 自顶向下分析](./lec3.md) | 从源语言到 token、语法树和 AST |
| IR 与语义 | [L4 中间表示](./lec4.md) · [L5 语义分析](./lec5.md) | 用符号表、类型与 IR 固化程序含义 |
| 后端 | [L6 代码生成](./lec6.md) | 结构化 IR、CFG、SSA 与 x86-64 |
| 程序分析 | [L7 块内优化](./lec7.md) · [L8 数据流分析](./lec8.md) · [L12 数据流理论](./lec12.md) | 从局部事实到 CFG 上的不动点 |
| 高级优化 | [L9 循环优化](./lec9.md) · [L10 寄存器分配](./lec10.md) · [L11 并行化](./lec11.md) | 利用支配、活跃性与依赖信息改写程序 |
