---
title: 6.5910 复杂数字系统设计
type: course
course: 6.5910 复杂数字系统设计
course_id: '6.5910'
tags: [digital-systems, bsv, fpga, hardware-synthesis, bluespec]
status: draft
---
# 6.5910 复杂数字系统设计

## TL;DR

- **高级硬件设计方法学**：采用 Bluespec SystemVerilog (BSV) 基于保护性原子动作（Guarded Atomic Actions）的形式化硬件描述语言，实现从高层语义到可综合数字电路的构造式正确。
- **模块化微架构与原型验证**：系统覆盖模块化时序电路、多周期与流水线处理器、缓存层级与硬件加速器设计，并在大型 FPGA 平台上完成多百万门原型验证。
- **工业级软硬件协同实践**：结合商业 EDA 与开源综合工具链，通过音视频流水线、FFT 信号处理加速器与多核系统综合项目构建端到端数字系统工程能力。

---

## 课程概述与定位

6.5910（原 6.375）复杂数字系统设计（*Complex Digital Systems Design*）是对大规模数字系统设计和实现的进阶介绍，使用硬件描述语言和高级综合工具，并结合标准的商业电子设计自动化（EDA）工具。

课程强调模块化和稳健设计、可重用模块、通过构建确保正确性（Correctness by Construction）、架构探索、满足面积和时序约束，以及开发功能性现场可编程门阵列（FPGA）原型。在每周实验中广泛使用计算机辅助设计（CAD）工具，为在多百万门 FPGA 上进行的多人设计项目做准备。

6.5910 是一个以项目为导向的高阶硬件设计课程，旨在教授一种系统化方法：使用 Bluespec SystemVerilog (BSV) 结合开源和商业 EDA 工具来设计数百万门芯片。课程的前半部分介绍 BSV 这门基于保护性原子动作的硬件描述语言，使用复杂度逐步增加的实例。在实验中，学生将学习设计信号处理加速器和简单的流水线处理器，首先仅在仿真中进行，然后在 FPGA 平台上实现。同时，还将强调开发正确的测试设计基础设施。这些实验将为学生接下来的课程项目做好准备。

在课程的后半部分，学生将在课程工作人员和导师的监督下，分小组进行大型硬件设计项目。过去的项目包括乱序处理器、缓存一致性内存系统、先进的 DRAM 访问调度器、支持 1Gbps 线路速率的垃圾邮件过滤器以及 802.11a 协议的物理层处理。

- **授课教师**：[Arvind](http://csg.csail.mit.edu/Users/arvind)
- **先行条件**：6.1910 / 6.004 计算结构（*Computation Structures*）

---

## 课程主题大纲

- **L01**: Complex Digital Systems Introduction [ [L01-IntroductionSplit.pdf](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/lectures/L01-IntroductionSplit.pdf) ]
- **L02**: Combinational Circuits [ [L02-CombinationalCircuits.pdf](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/lectures/L02-CombinationalCircuits.pdf) ]
- **L03**: Complex Combinational Circuits in BSV [ [L03-ComplexCombinationalCircuits.pdf](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/lectures/L03-ComplexCombinationalCircuits.pdf) ]
- **L04**: Sequential Circuits as Modules [ [L04-SequentialCircuitsasModules.pdf](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/lectures/L04-SequentialCircuitsasModules.pdf) ]
- **L05**: Folded and Pipelined Circuits [ [L05-FoldedandPipeliendCircuits.pdf](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/lectures/L05-FoldedandPipeliendCircuits.pdf) ]
- **L06**: Hardware Synthesis [ [L06-HardwareSynthesis.pdf](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/lectures/L06-HardwareSynthesis.pdf) ]
- **L07**: Bypasses and EHRs [ [L07-BypassesandEHRs.pdf](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/lectures/L07-BypassesandEHRs.pdf) ] [ [Ehr.bsv](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/Ehr.bsv) ]
- **L08**: Serializability [ [L08-Serializability.pdf](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/lectures/L08-Serializability.pdf) ]
- **L09**: IP Lookup [ [L09-IP_Lookup.pdf](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/lectures/L09-IP_Lookup.pdf) ]
- **L10**: Non-pipelined Processors [ [L10-NonPipelinedProcessors.pdf](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/lectures/L10-NonPipelinedProcessors.pdf) ]
- **L11**: Multicycle Processors and Pipelined Processors [ [L11-MulticycleProcessorsAndPipelinedProcessors.pdf](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/lectures/L11-MulticycleProcessorsAndPipelinedProcessors.pdf) ]
- **L12**: Pipelined Processors [ [L12-PipelinedProcessors.pdf](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/lectures/L12-Pipelined_Processors.pdf) ]
- **L13**: Cache Design and Implementation [ [L13-CacheImplementation.pdf](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/lectures/L13-CacheImplementation.pdf) ]

---

## 实验系列（Labs）

- **Lab 0**: BSV 与实验环境入门 [ [S01-BSVandLabs.pdf](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/supplements/S01-BSVandLabs.pdf) ]
- **Lab 1**: A Simple Audio Pipeline [ [lab1.pdf](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/labs/lab1.pdf) ]
- **Lab 2**: Fast Fourier Transforms: Extending the Audio Pipeline [ [lab2.pdf](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/labs/lab2.pdf) ] [ [lab2-harness.tar.gz](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/labs/lab2-harness.tar.gz) ]
- **Lab 3**: Pitch Shifting: Completing the Audio Pipeline [ [lab3.pdf](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/labs/lab3.pdf) ] [ [lab3-harness.tar.gz](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/labs/lab3-harness.tar.gz) ]
- **Lab 4**: Audio Pipeline on an FPGA [ [lab4.pdf](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/labs/lab4.pdf) ] [ [lab4-harness.tar.gz](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/labs/lab4-harness.tar.gz) ]
- **Lab 5**: RISC-V Processors [ [lab5.pdf](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/labs/lab5.pdf) ] [ [lab5-harness.tar.gz](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/labs/lab5-harness.tar.gz) ]

---

## 期末大作业精选（Final Projects）

- [Final Project Overview](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/finalproject.pdf)
- **Hardware Accelerated Genetic Optimization for PCB Layer Assignment**
  - Heather Berlin, Zachary Zumbo (Mentored by Chanwoo Chung)
  - [Final Report](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/finals/Group_1_report.pdf) · [Final Presentation](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/finals/Group_1_Slides.pptx)
- **RISC-V Processor with "F" Extension**
  - Kathy Camenzind, Miguel Gomez (Mentored by Andy Wright)
  - [Final Report](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/finals/Group_2_report.pdf) · [Final Presentation](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/finals/Group_2_Slides.pptx)
- **Stereo Vision for Driverless Cars**
  - Marc de Cea, Ravi Rahman (Mentored by Jamey Hicks)
  - [Final Report](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/finals/Group_3_report.pdf) · [Final Presentation](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/finals/Group_3_Slides.pptx)
- **Multi-tiered Branch Predictor for Pipelined Processors**
  - Francis Wang, Shana Matthew (Mentored by Joonwon Choi)
  - [Final Report](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/finals/Group_4_report.pdf) · [Final Presentation](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/finals/Group_4_Slides.pptx)
- **SpMV Accelerator**
  - Ziheng Wang (Mentored by Shuotao Xu)
  - [Final Report](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/finals/Group_5_report.pdf) · [Final Presentation](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/finals/Group_5_Slides.pptx)
- **Fixed Function Configurable Graphics Pipeline**
  - Thomas Watson (Mentored by Thomas Bourgeat)
  - [Final Report](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/finals/Group_6_report.pdf) · [Final Presentation](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/finals/Group_6_Slides.pptx)
- **A Minimal Network Stack on FPGA**
  - Tianhao Huang
  - [Final Report](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/finals/Group_7_report.pdf) · [Final Presentation](http://csg.csail.mit.edu/6.375/6_375_2019_www/handouts/finals/Group_7_Slides.pptx)

---

## 参考文献与学习资料

- **教材**：
  - *Introduction to Digital Design as Cooperating Sequential Machines*, by Arvind, Rishiyur S. Nikhil, James E. Hoe, Silvina Hanono Wachman [ [Logic_Design.pdf](http://csg.csail.mit.edu/6.375/6_375_2019_www/resources/Logic_Design.pdf) ]
  - *BSV By Example*, Rishiyur S. Nikhil and Kathy R. Czeck [ [bsv_by_example.pdf](http://csg.csail.mit.edu/6.375/6_375_2019_www/resources/bsv_by_example.pdf) ]
  - *Computer Organization and Design: the Hardware/Software Interface*, John L. Hennessy and David A. Patterson
  - *Computer Architecture: A Quantitative Approach*, John L. Hennessy and David A. Patterson
- **语言与规范参考**：
  - [Bluespec Reference Guide](http://csg.csail.mit.edu/6.375/6_375_2019_www/resources/bsv-reference-guide.pdf)
  - [Bluespec User Guide](http://csg.csail.mit.edu/6.375/6_375_2019_www/resources/bsv-user-guide.pdf)
  - [RISC-V User-Level ISA Specification](https://riscv.org/specifications)
  - [RISC-V Privileged ISA Specification](https://riscv.org/specifications/privileged-isa)
