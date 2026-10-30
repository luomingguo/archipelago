---
title: 循环结构、数值枚举与函数抽象
type: lecture
lecture: 2
tags: [loops, enumeration, functions, abstraction, scoping]
status: complete
source: https://introcomp.mit.edu/fall26
---

# Lec 2 循环结构、数值枚举与函数抽象（Looping, Enumeration & Functions）

> MIT 6.100 · 计算机科学与 Python 编程导论 · Fall 2026 · 教材参考：Guttag 2.5–2.7, 3.1, 5.2, 4.1.1

## TL;DR

- **迭代与状态更新**：While 循环基于条件维持迭代，For 循环遍历有限迭代序列；状态变量在循环体中的单调递增/递减确保算法有限步终止。
- **猜想与检验（Guess and Check）**：穷举枚举（Exhaustive Enumeration）是利用计算机计算速度寻找问题解的最直接方法，通过逐个扫描离散候选空间判定条件。
- **函数抽象与解耦**：函数作为代码复用的基本单元，通过形式参数（Parameters）与返回值建立严格契约，实现实现细节与调用方的彻底隔离。

## 1. 循环控制与终止性论证

当处理重复性计算时，循环机制赋予程序以极简代码操纵大规模状态演进的能力。

### While 循环与循环不变式

While 循环依靠循环条件表达式的真假维持运行：

```python
x = 5
ans = 0
iters_left = x
while iters_left != 0:
    ans = ans + x
    iters_left = iters_left - 1
print(f"{x} * {x} = {ans}")
```

::: definition 循环终止函数（Loop Variant）
为了防止程序陷入死循环，必须存在一个单调向终止条件逼近的整型指标（如上例中的 `iters_left`），每次循环执行至少减小 1 且具有非负下界，由此在数学上确保循环必然在有限步内终止。
:::

### For 循环与 `range` 迭代器

Python 的 For 循环本质上是一个迭代器消费协议，遍历任何可迭代对象（Iterable）：

```python
# range(start, stop, step) 产生左闭右开的惰性数字序列
total = 0
for i in range(1, 101, 2):  # 1, 3, 5, ..., 99
    total += i
print(f"1 到 100 的奇数和为：{total}")
```

---

## 2. 算法思维雏形：穷举枚举法（Guess and Check）

在掌握算法分析前，计算机最直接的解题手段是**穷举搜索**（Exhaustive Enumeration）。

考虑寻找正整数 $x$ 的整数立方根问题：

```python
x = int(input("请输入一个正整数："))
ans = 0

# 穷举枚举所有可能的非负整数
while ans ** 3 < abs(x):
    ans += 1

if ans ** 3 != abs(x):
    print(f"{x} 不是一个完全立方数")
else:
    if x < 0:
        ans = -ans
    print(f"{x} 的立方根为 {ans}")
```

对于现代处理器而言，在一秒钟内完成千万级简单运算轻而易举。只要搜索空间有限，猜想与检验策略能以极高的开发效率解决复杂的离散约束问题。

---

## 3. 函数机制与抽象屏障

函数是管理软件复杂度的第一道重要护城河。它将一组具体的操作封装为一个逻辑黑盒，调用者只需了解该黑盒的输入参数要求与输出契约，而无需关心其内部实现采用了循环、递归抑或查找表。这种将“做什么”与“怎么做”彻底分离开的设计思想，被称为程序设计中的抽象屏障（Abstraction Barrier）。

在定义函数时，良好的工程实践要求通过规范的文档字符串（Docstring）描述其前置条件（Preconditions）与后置条件（Postconditions）：

```python
def is_even(i: int) -> bool:
    """
    输入参数：
        i: 正整数或负整数
    返回值：
        若 i 是偶数返回 True，否则返回 False
    """
    return i % 2 == 0
```

### 函数环境模型与局部栈帧（Local Frame）

当一个函数被调用时，Python 解释器并不会直接在当前环境中就地展开代码，而是会建立一个全新的独立栈帧（Local Frame）。局部栈帧中存放该次调用所独有的局部命名空间：

```text
全局帧 (Global Frame)
┌─────────────────┬──────────────────────┐
│ is_even         ├────► [函数对象 0x1A] │
│ x               │ 8                    │
└─────────────────┴──────────────────────┘
                           ▲ 父指针
局部帧 (is_even Frame)     │
┌─────────────────┬────────┴─────────────┐
│ i (形参)        │ 8                    │
│ return value    │ True                 │
└─────────────────┴──────────────────────┘
```

函数调用生命周期涉及三个不可混淆的关键机制：
1. **形参绑定（Parameter Binding）**：调用发生时，实参表达式首先在调用方环境中完成求值，随后将求值得到的结果对象引用绑定至被调用函数的局部形参变量名上。
2. **作用域隔离（Scope Isolation）**：函数执行过程中所有新创建的局部变量均被限制在当前局部帧内。一旦执行流遭遇 `return` 语句或到达函数末尾，该局部帧即从调用栈中弹出并销毁，有效防止了全局命名空间的非预期污染。
3. **闭合父帧指针（Static Enclosing Pointer）**：每个局部栈帧内部隐式持有一个指向其父环境的指针。在变量解析过程中，若当前局部命名空间中未找到对应标识符，解释器将顺着作用域指针链向外层环境逐级回溯检索，这构成了 Python 词法作用域（Lexical Scoping）的基础。

::: pitfall 隐式全局变量修改陷阱
在函数内部可以直接读取全局变量，但如果尝试对同名变量赋值，Python 会将其判定为局部变量：
```python
val = 10

def mutate():
    # 报错：UnboundLocalError: local variable 'val' referenced before assignment
    val = val + 1

mutate()
```
如需显式修改全局变量，必须使用 `global` 关键字，但应尽量通过参数传递和返回值替代全局共享状态以保持纯函数性质。
:::

## 我的理解

::: insight 抽象屏障的工程价值
“不要告诉我你怎么算出来的，只要告诉我接口契约是什么”。函数定义的本质是建立抽象屏障（Abstraction Barrier）。一旦为某个特定子任务赋予了精确的函数契约，该子任务即可被作为更高阶架构的基本构件。这种分层组合思想是所有现代软件工程演进的根本逻辑。
:::
