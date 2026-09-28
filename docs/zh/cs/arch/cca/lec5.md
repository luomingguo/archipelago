---
title: 非流水线处理器
type: lecture
lecture: 5
tags: [riscv-rv32i, single-cycle-processor, instruction-execution, bsv-rules, processor-datapaths]
status: complete
---
# Lec 5 非流水线处理器

## TL;DR

- 基于 RV32I 基础整数指令集，构建覆盖取指、译码、执行、访存、写回的五阶段处理器核心。
- BSV 单规则（One-Rule）处理器在一个原子事务中串行串联全部执行阶段，概念简明且天然规避流水线冒险。
- 纯函数式 `exec` 模块将 ALU 运算、分支目标计算与访存地址生成收敛为统一的无状态组合逻辑。
- 单规则处理器的时钟周期受制于各阶段组合延迟累加的最长路径，为后续多阶段流水线切分提供了基准。

> MIT 6.1920 · Constructive Computer Architecture
> 讲师：Arvind · 日期：2024-02-20

## 1. RISC-V 指令集概述

::: definition
**定义 — RISC-V（*Reduced Instruction Set Computer V*）**

RISC-V 是一个开放的精简指令集（*ISA*），本课程使用 RV32I（32 位整数基础子集）。寄存器 x0 恒为 0；31 个通用寄存器（x1–x31）；PC（程序计数器）；所有指令定长 32 位。
:::

**主要指令格式**：
- **R 型**：`add rd, rs1, rs2`——寄存器-寄存器运算
- **I 型**：`addi rd, rs1, imm`——立即数运算；`lw rd, imm(rs1)`——加载
- **S 型**：`sw rs2, imm(rs1)`——存储
- **B 型**：`beq rs1, rs2, offset`——条件跳转
- **J 型**：`jal rd, offset`——无条件跳转并链接

---

## 2. 指令执行的五个阶段

::: definition
**定义 — 五阶段执行（*Five-Stage Execution*）**

每条指令按顺序经历：取指（*Fetch, IF*）→ 译码（*Decode, ID*）→ 执行（*Execute, EX*）→ 访存（*Memory, MEM*）→ 写回（*Writeback, WB*）。非流水线处理器中这五步串行完成，CPI（每指令周期数）约为 5。
:::

---

## 3. BSV 非流水线实现

### 3.1 状态元素

在 BSV 中，处理器的所有持久化架构状态（Architectural State）均由专用状态原语维护：

```bsv
Reg#(Addr)                    pc  <- mkReg(0);
RegisterFile#(RIndx, Data)    rf  <- mkRegFileFull;
Memory                       mem  <- mkMemory;
```

各核心组件的微架构职责与时序特性如下：
- **程序计数器（`pc`）**：32 位标准寄存器，存放当前待提取指令的物理内存地址，每个指令周期按顺序（$+4$）或跳转目标地址更新。
- **通用寄存器堆（`rf`）**：包含 32 个 32 位寄存器的阵列。提供两个完全独立的组合逻辑读端口（`rd1`, `rd2`）和一个同步写端口（`wr`），支持在同一周期内无延迟读取源操作数。
- **存储器子系统（`mem`）**：在初期单周期/非流水线模型中，通常假设为理想化的单周期响应存储器（Magic Memory），将指令内存与数据内存统一抽象，便于验证执行逻辑的语义正确性。

### 3.2 单规则实现

在单规则处理器模型中，整条指令的完整生命周期被封装在单一原子规则 `doInst` 中。该规则在单个时钟周期内按序触发并推进全部微操作：

```bsv
rule doInst;
    // 1. Fetch
    Data inst = mem.req(MemReq{op: Ld, addr: pc, data: ?});
    
    // 2. Decode
    DecodedInst dInst = decode(inst);
    
    // 3. Register Read
    Data rVal1 = rf.rd1(dInst.src1);
    Data rVal2 = rf.rd2(dInst.src2);
    
    // 4. Execute
    ExecInst eInst = exec(dInst, rVal1, rVal2, pc);
    
    // 5. Memory Access
    if (eInst.iType == Ld) eInst.data = mem.req(MemReq{op:Ld, addr:eInst.addr, ...});
    if (eInst.iType == St) mem.req(MemReq{op:St, addr:eInst.addr, data:eInst.data});
    
    // 6. Writeback
    if (isValid(eInst.dst)) rf.wr(fromMaybe(?,eInst.dst), eInst.data);
    
    // 7. PC Update
    pc <= eInst.nextPc;
endrule
```

**执行流各阶段的硬件行为分析**：
- **组合逻辑串联**：从 `pc` 发起存储器请求开始，指令数据返回后立即送入 `decode` 组合逻辑，接着通过寄存器堆组合端口读取操作数，再流经 `exec` 组合运算网络，最后根据指令类型执行访存请求并写回 `rf`。
- **关键路径与频率惩罚**：在单规则模型中，一个时钟周期必须容纳取指（$T_{IF}$）、译码（$T_{ID}$）、执行（$T_{EX}$）、访存（$T_{MEM}$）和写回（$T_{WB}$）的全部组合逻辑延迟之和。这意味着整个处理器的最高工作频率将受到这条超级长路径的严重压制。
- **硬件资源浪费**：由于一条指令必须串行走完所有阶段，在 ALU 进行计算时，存储器接口处于空闲状态；在访存阶段，ALU 硬件资源又被闲置，各子系统的时空并行度为零。

::: theorem 推论 — 单规则的局限性
单规则实现清晰但低效：每条指令独占整个处理器 1 个或多个时钟周期（取决于存储器延迟），硬件利用率低。流水线将各阶段并行化，使 CPI 趋近于 1。
:::

---

## 4. 执行函数（exec）

执行函数 `exec` 是处理器数据通路的核心，它被实现为一个无时钟、无内部状态的纯函数式组合逻辑块。它接收译码后的指令包 `dInst`、源操作数值 `rVal1`, `rVal2` 以及当前指令地址 `pc`，统一产生结构体 `ExecInst`：

```bsv
function ExecInst exec(DecodedInst dInst, Data rVal1, Data rVal2, Addr pc);
    ExecInst eInst = ?;
    eInst.iType = dInst.iType;
    
    Data aluVal2 = (dInst.iType == Alu) ? rVal2 : signExtend(dInst.imm);
    eInst.data = alu(rVal1, aluVal2, dInst.aluFunc);
    
    eInst.addr  = rVal1 + signExtend(dInst.imm);  // 存储/加载地址
    eInst.nextPc = (brTaken) ? pc + signExtend(dInst.imm) : pc + 4;
    eInst.dst   = dInst.dst;
    return eInst;
endfunction
```

**`exec` 函数的内部计算映射**：
- **ALU 操作数多路选择**：第二操作数根据指令是寄存器类型还是立即数类型，通过多路选择器在 `rVal2` 与带符号扩展的立即数 `signExtend(dInst.imm)` 之间切换。
- **访存物理地址计算**：对于 Load/Store 指令，基址加偏移的加法运算在 `exec` 内部完成计算并填入 `eInst.addr`。
- **分支与返回地址生成**：对于分支指令，若条件成立则跳转至 $pc + imm$，否则顺序递增到 $pc + 4$；对于链接跳转指令（`jal`/`jalr`），`nextPc` 被设为跳转目标，同时运算结果 `eInst.data` 赋为 $pc + 4$ 并写回目标寄存器。

---

## 5. 性能分析

::: example 例题 — CPI 计算

:::

假设指令存储器（I-Mem）和数据存储器（D-Mem）各需 1 周期（理想化），则：
- 所有指令：取指 1 周期 + 执行 1 周期 = **2 周期**（无访存）
- 加载/存储指令：+ 访存 1 周期 = **3 周期**

Sol：若 30% 指令为加载/存储，则平均 $\text{CPI} = 0.7 \times 2 + 0.3 \times 3 = 2.3$。

---

## 6. 处理器测试

**RISC-V 测试套件**：标准测试程序（`rv32ui-p-*`）验证每条指令的正确性，通过向特殊地址写入 `1`（pass）或错误码（fail）来报告结果。

```bsv
if (req.addr == 'hf000_fff8) begin
    if (req.data == 0) $fdisplay(stderr, "PASS");
    else $fdisplay(stderr, "FAIL (%0d)", req.data);
    $finish;
end
```

---

## 核心机制小结与单周期架构权衡

RISC-V RV32I 提供简洁的 32 位指令集；非流水线处理器用单规则实现所有执行阶段，CPI 约 2–3，硬件利用率低；exec 函数统一处理 ALU、分支和存储器地址计算；性能瓶颈为各阶段串行执行，流水线是提升的核心方向。

## 核心机制思考与底层洞察

::: insight 单规则处理器的形式化优势与物理时序困境
单规则（One-Rule）处理器是建构式计算机架构中最纯粹的教学基准，其价值在于向设计者揭示了 ISA 形式化规范与物理时序之间的本真矛盾：

1. **形式化语义的精确镜像**：在 ISA 规范手册中，一条指令的执行被定义为一个不可分割的原子状态跃迁：$(PC, RF, Mem) \to (PC', RF', Mem')$。BSV 的单规则 `doInst` 是这一数学模型的直接物理投射——没有流水线冲突，没有分支错误预测的投机恢复，也没有 RAW（写后读）数据冒险。在验证功能正确性与指令完备性时，单规则处理器是无懈可击的黄金参考模型（Golden Model）。
2. **VLSI 物理层面的关键路径灾难**：在真实的硅片布局布线中，单规则意味着一条指令的数据流必须在**单个时钟周期的时钟上升沿与建立时间（Setup Time）之间**，连续穿越取指 SRAM 读取、指令译码逻辑门、寄存器堆读多路器、32 位 ALU 加法树、数据 SRAM 读取选通以及写回数据 MUX。这条长达数万皮秒的超级组合路径直接将芯片时钟频率压低到了极点。流水线设计的本质，绝不是发明更聪明的运算算法，而是**在巨长的组合路径上切断连线并插入流水寄存器（Pipeline Registers）**，用吞吐换时钟，用微架构的并发复杂度换取极高的主频。
:::
