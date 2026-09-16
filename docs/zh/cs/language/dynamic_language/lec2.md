---
title: 词法分析（Lexing）
type: lecture
lecture: 2
tags: [lexical-analysis, regular-expression, finite-automata, lexer]
status: complete
---
# Lec 2 词法分析（Lexing）

> Phase 1 前半。先看一个语言设计议题（语法糖），再讲词法规范（正则表达式 / 自动机）

## TL;DR

- lexer 把字符流分成带类别与原始文本的 token，并过滤空白、注释与报告非法输入。
- 正则表达式以生成式视角定义词法类别，有限自动机以识别式视角执行判定；两者可自动互转。
- 实现链条是「正则表达式 → NFA → 子集构造 → DFA → 扫描 token」；语法糖则展示了高层构造如何降解为较小的语义核心。

---

## 1. 语言设计：语法糖（Syntactic Sugar）

MITScript 很精简，但能力不弱：有函数（`fun`，即闭包，等同 Python 的 `lambda`）、命令行输入（`input`/`intcast`）、`while` 循环、**记录 `{}`**（本质是字典）。

::: example 例题（用记录 + 闭包模拟"类"）
```text
Point = fun(a, b) {
  self = {
    x : a;  y : b;
    print : fun(){ log("Point(" + self.x + ", " + self.y + ")"); };
  };
  return self;
};
p1 = Point(5,5); p1.print();
```

这段在语义上等价于 Python 的 `class Point` 定义——对象 = 一个有 x/y/print 字段的记录，方法通过 `self` 指针访问字段。
:::

::: definition 定义（语法糖 Syntactic Sugar）
当一个语言特性的**语法**可以被翻译（reduce）为一组更简单的原语（primitives）的组合时，称该特性为**语法糖**。如 Python 的 class 可降解为"记录 + 闭包"。
:::

> 语言设计的核心权衡：**可用性**（提供易用语法）vs. **语言复杂度**（只实现一组核心原语）。判断一个新抽象能否/应否降解为简单原语，是设计语言的关键任务。

---

## 2. 语言定义的分层结构

::: definition 定义（语言定义的四层）
- **字母表**：语言中的字母集合 $\Sigma$；

- **词法结构 (lexical)**：识别"词 (words)"，每词是字母序列；

- **语法结构 (syntactic)**：识别"句子"，每句是词序列；

- **语义 (semantics)**：程序含义（对每个输入应得什么结果）。

本讲：词法（对应 Phase 1）。
:::

---

## 3. 词法类别（Lexical Categories）

每门语言有若干词类，每类用一个正则表达式（*regular expression*）定义：

```text
IfKeyword  = if          Integer    = [0-9][0-9]*
WhileKeyword = while      Float      = [0-9]*.[0-9]*
Operator   = + | - | * | / Identifier = [a-z]([a-z]|[0-9])*
```

其中 `[0-9] = (0|1|…|9)`，`[a-z] = (a|b|…|z)`。

**分词目标**：把字符流 `(2-1)+1` 切成带类别与文本的 token 序列：`Open "("`、`Int "2"`、`Op "-"`、`Int "1"`、`Close ")"`、`Op "+"`、`Int "1"`。

---

## 4. 两种对偶视角：生成式 vs. 识别式

::: definition 定义（生成式与识别式）
- **生成式 (generative)**：正则表达式 / 文法，**生成**语言中所有串。

- **识别式 (recognition)**：自动机 (*automaton*)，**判定**某串是否在语言中。

二者哲学不同但**理论等价**，且可自动互转。标准做法：用正则表达式定义、自动转成自动机实现。
:::

### 4.1 正则表达式构造

由以下归纳构造：<span>$\varepsilon$</span>（空串）、字母、序列 <span>$r_1 r_2$</span>、选择 <span>$r_1\mid r_2$</span>、克莱尼星 <span>$r^* = \varepsilon\mid r\mid rr\mid\cdots$</span>、括号分组。生成语义靠重写：<span>$r_1\mid r_2\to r_1$</span>、<span>$\to r_2$</span>，<span>$r^*\to rr^*$</span>、<span>$\to\varepsilon$</span>。所有可生成串的集合是该表达式的**语言**，串常称 **token**。

示例（<span>$\Sigma=\{0,1,.\}$</span>）：`(0|1)*.(0|1)*` 二进制浮点数；`(00)*` 偶数长全 0 串；`1*(01*01*)*` 含偶数个 0 的串。

---

## 5. 有限状态自动机（Finite-State Automata）

由字母表 <span>$\Sigma$</span>、带初始/接受标记的状态集、带字母标签的转移构成。运行：从起始态与首字母开始，每步匹配同标签转移，到串尾停在接受态则**接受**。

::: definition 定义（DFA vs. NFA）
- **DFA**：无 $\varepsilon$ 转移，每态对每字母至多一条转移。

- **NFA**：放宽两限制——允许 $\varepsilon$（空串）转移与同标签多转移；只要存在一条路径接受即接受。
:::

### 5.1 正则表达式 → NFA（结构归纳）

假设每子表达式可转为"单起始 + 单接受"的自动机，给出各构造子的拼装：
- **基本**：<span>$\varepsilon$</span> 用 <span>$\varepsilon$</span> 边，字母 <span>$a$</span> 用 <span>$a$</span> 边；
- **序列**：旧接受态 <span>$\to_\varepsilon$</span> 下一段旧起始态；
- **选择**：新起始 <span>$\to_\varepsilon$</span> 两支，两支接受态 <span>$\to_\varepsilon$</span> 新接受；
- **克莱尼星**：新起始 <span>$\to_\varepsilon$</span> 旧起始/新接受，旧接受 <span>$\to_\varepsilon$</span> 旧起始/新接受。

产物总是 NFA。

### 5.2 NFA → DFA（子集构造）

::: definition 定义（子集构造 Subset Construction）
DFA 每个状态对应 NFA 状态的一个子集；起始态 = NFA 起始态的 $\varepsilon$-闭包；某 DFA 状态为接受态 ⟺ 其集合含某 NFA 接受态；对字母 $a$ 的转移 = 集合内各 NFA 态读 $a$（含后续 $\varepsilon$）可达状态的并集。代价：DFA 可能**指数级**大于 NFA。
:::

---

## 6. Phase 1 的 Lexer 任务

::: definition 定义（Lexer 规格）
**输入**：一组词法类别（正则表达式）+ 一个输入字符串；**输出**：一个 token 序列，每个 token 带其匹配文本。
:::

实现路线即上面的链条：正则表达式 → NFA → DFA → 用 DFA 对输入扫描分词。

---

## 7. 本讲小结

- 语言设计权衡可用性与复杂度；语法糖把高层特性降解为核心原语（class → 记录 + 闭包）。
- 语言分层：字母表 → 词法 → 语法 → 语义；词法用正则表达式定义词类。
- 生成式（正则表达式/文法）与识别式（自动机）对偶且可自动互转：正则表达式 → NFA →（子集构造）→ DFA。
- Phase 1 的 lexer：以词法类别 + 输入串为输入，产出带文本的 token 序列。
