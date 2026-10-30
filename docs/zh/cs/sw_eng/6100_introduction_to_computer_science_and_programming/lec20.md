---
title: 异常处理、防御性编程与断言契约
type: lecture
lecture: 20
tags: [exceptions, assertions, defensive-programming, error-handling, contracts]
status: complete
source: https://introcomp.mit.edu/fall26
---

# Lec 20 异常处理、防御性编程与断言契约（Exceptions & Assertions）

> MIT 6.100 · 计算机科学与 Python 编程导论 · Fall 2026 · 教材参考：Guttag 9

## TL;DR

- **显式优于隐式（EAFP 原则）**：Python 崇尚“请求原谅比索求许可更容易”（EAFP），通过 `try-except-else-finally` 结构捕获和处理特定异常，避免用层层嵌套的 `if` 掩盖核心算法逻辑。
- **自定义异常与错误分类**：通过继承内置 `Exception` 基类，构建领域专属的异常层次结构，携带精确的上下文错误载荷并支持上层精细化分类捕获。
- **断言（Assertions）与防御性前置契约**：`assert condition, msg` 是面向开发者的防御性排错探针，用于在函数入口强制校验不可违反的前置后置条件，确保在系统发生状态破坏的最早时刻立即原地崩溃。

## 1. 运行时异常机制：从崩溃到受控处理

在现实世界中，程序必然遭遇预期之外的非正常状态（如用户输入非数字字符、除数为零、尝试读取不存在的文件或网络连接瞬间中断）。

在传统 C 语言中，函数通常通过返回特殊的错误码（如 `-1` 或 `NULL`）表达失败，这导致调用方必须充斥着海量防御性 `if (res < 0)` 检查。如果某处遗漏了检查，错误将像幽灵一样在系统深处静默蔓延，直到很久之后在完全不相干的代码处引发神秘崩溃。

Python 采用了基于堆栈回溯的**异常处理模型（Exception Handling）**：当遇到不可恢复的错误状态时，解释器立即抛出（`raise`）一个异常对象。若当前函数未做拦截，异常将沿着调用栈逐级向上冒泡，直至被捕获或者最终在顶层打印出完整的错误堆栈追踪（Traceback）：

```python
def compute_ratio(a: float, b: float) -> float:
    try:
        result = a / b
    except ZeroDivisionError as e:
        print("警告：除数不能为 0，返回缺省值 0.0")
        return 0.0
    else:
        # 仅在 try 块完全没有抛出任何异常时才执行
        print("计算顺利完成")
        return result
    finally:
        # 无论发生什么（正常返回或抛出异常），最终都百分之百保证执行
        print("资源清理完成")
```

---

## 2. Pythonic 哲学：LBYL 与 EAFP 的理念对决

在错误防护的编程风格上，软件工程存在两大经典派系：

### 1. 三思而后行（LBYL: Look Before You Leap）
在执行可能危险的操作前，通过密集的条件判断进行前置排查：
```python
# LBYL 风格：繁琐且存在竞态条件
if "score" in student_dict:
    score = student_dict["score"]
else:
    score = 0
```

### 2. 请求原谅容易于索求许可（EAFP: Easier to Ask for Forgiveness than Permission）
直接大胆执行核心操作，假设一切正常，仅在真正遇到异常时由 `except` 块兜底补救：
```python
# EAFP 风格：清爽、直观且天然线程安全
try:
    score = student_dict["score"]
except KeyError:
    score = 0
```

::: definition EAFP 原则
Python 官方强烈推荐的编程哲学。在正常情况下，`try` 块的执行开销几乎为零；相比于 LBYL 每次都需要执行额外的条件检查与哈希查找，EAFP 不仅性能更高，还能完美杜绝检查与执行之间的时间差竞态问题（Time-of-Check to Time-of-Use, TOCTOU）。
:::

---

## 3. 自定义领域异常与断言契约

在构建复杂系统时，标准库的 `ValueError` 或 `TypeError` 往往过于宽泛，无法精准表达业务语义。我们可以通过继承 `Exception` 定义领域专属异常：

```python
class InsufficientFundsError(Exception):
    """
    当账户余额不足以扣减提现金额时抛出的领域异常
    """
    def __init__(self, balance: float, amount: float):
        super().__init__(f"账户当前余额 {balance} 不足以提现 {amount}")
        self.balance = balance
        self.amount = amount
```

### 断言契约：主动设置自毁防御开关

断言（Assertion）是防御性编程的最强探针。它不是用来处理普通用户输入错误的，而是用来检验**“程序员自己的代码逻辑是否处于自洽状态”**：

```python
def calculate_grade(assignments: list) -> float:
    # 前置条件契约：作业列表绝对不能为空，且每一项必须在 [0, 100] 之间
    assert len(assignments) > 0, "计算成绩时作业列表不能为空"
    assert all(0 <= score <= 100 for score in assignments), "单项分数必须在 0 到 100 之间"
    
    final_score = sum(assignments) / len(assignments)
    
    # 后置条件契约：输出结果绝对不可能超出合理区间
    assert 0 <= final_score <= 100, "后置条件违背：计算出的最终成绩超出边界"
    return final_score
```

断言的核心价值在于**尽早崩溃（Fail-Fast）**：一旦系统的不变式被破坏，程序立刻在最靠近犯罪现场的第一时间自毁并打印错误信息，防止破坏性状态向外污染。

::: pitfall 严禁使用裸 `except:` 吞没所有异常
编写类似 `except:` 或 `except Exception:` 且内部仅写 `pass` 的代码，被称为“犯罪式错误处理”。它不仅捕获了预期的业务错误，还会连带静默吞没拼写错误导致的 `NameError`、调用超时的 `KeyboardInterrupt` 以及系统退出信号，使整个程序变为无法调试的黑洞。必须永远显式捕获具体异常类型（如 `except (KeyError, ValueError):`）。
:::

## 我的理解

::: insight 异常是程序健壮性的骨架
平庸的程序员只为阳光灿烂的“正常流程（Happy Path）”写代码；卓越的软件工程师花费一半以上的心血为乌云密布的“异常边界（Failure Modes）”修筑堤坝。异常处理与断言不是事后打补丁，而是软件规格契约的前置设计。敢于让程序在出现逻辑矛盾时立即抛出异常原地自省，是系统能够演化为高可靠工业级产品的根本基石。
:::
