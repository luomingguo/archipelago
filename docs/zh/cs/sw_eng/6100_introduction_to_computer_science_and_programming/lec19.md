---
title: 类、属性与面向对象设计
type: lecture
lecture: 19
tags: [oop, classes, encapsulation, methods, data-abstraction]
status: complete
source: https://introcomp.mit.edu/fall26
---

# Lec 19 类、属性与面向对象设计（Classes, Attributes & Methods）

> MIT 6.100 · 计算机科学与 Python 编程导论 · Fall 2026 · 教材参考：Guttag 10.1

## TL;DR

- **面向对象与数据抽象**：类（Class）是创建对象的蓝图，将状态（属性/Attributes）与操作状态的行为（方法/Methods）高内聚封装，建立自定义抽象数据类型（ADT）。
- **实例初始化与 self 绑定**：`__init__` 初始化器在对象实例化时自动触发，首位形参 `self` 指向当前正在被操纵的具体堆内存实例，方法调用 `a.m(b)` 等价于 `Class.m(a, b)`。
- **特殊双下划线方法（Dunder Methods）**：通过实现 `__str__`、`__repr__`、`__add__`、`__len__` 等内置魔法协议，让自定义类型无缝融入 Python 原生操作符与内置函数体系。

## 1. 面向对象编程（OOP）的心智模型

在编程初阶，我们通过散乱的列表、字典和全局函数组织逻辑。但随着系统规模不断膨胀，数据结构与操作该数据的函数发生剥离脱节，极易导致状态被外部代码非法篡改。

**面向对象编程（Object-Oriented Programming, OOP）** 提供了全新的系统设计范式：
- **状态（State）**：对象持有的内部数据字段；
- **行为（Behavior）**：对象能够响应外部请求并合法改变自身状态的接口函数；
- **封装（Encapsulation）**：对外隐藏具体的内部内存表示，只向外界暴露安全、合法的公有方法。

::: definition 类（Class）与实例（Instance）
类是定义新型数据结构的抽象模具与规约；实例则是依照该类模板在堆内存中独立分配的具体实体对象。一个类可以派生实例化出成千上万个状态各异的独立对象。
:::

---

## 2. 类的定义、实例属性与 self 机制

在 Python 中，通过 `class` 关键字声明新类型。

当调用 `Coordinate(3, 4)` 时，解释器在堆内存中新开辟一块专属命名空间，并隐式调用类的 `__init__` 方法。此时，形参 `self` 自动被绑定到这块新开辟的实例内存地址上：

```python
class Coordinate:
    """
    表示二维平面直角坐标系中的一个点
    """
    def __init__(self, x: float, y: float):
        # 实例属性：保存在该对象独有的堆空间中
        self.x = x
        self.y = y
        
    def distance_from_origin(self) -> float:
        """
        计算点到坐标原点 (0, 0) 的欧氏距离
        """
        return (self.x ** 2 + self.y ** 2) ** 0.5
```

### 深入理解方法调用语法糖

当我们写下 `point.distance_from_origin()` 时，初学者往往困惑为什么定义时有形参 `self`，而调用时圆括号内却无需传参？

这是 Python 解释器的一层语法糖。底层执行的本质等价转换是：
$$\text{point.distance\_from\_origin}() \iff \text{Coordinate.distance\_from\_origin}(\text{point})$$
Python 自动将点号左侧的调用对象作为第一个实参隐式塞入 `self` 槽位，确保函数体能够准确锁定要读取哪一个实例的属性。

---

## 3. 特殊魔法方法（Dunder Methods）与操作符重载

Python 的强大之处在于其全局统一且高度一致的数据模型（Data Model）。在许多其他编程语言中，自定义对象往往只能通过繁琐的方法调用（如 `c1.add(c2)` 或 `c1.equals(c2)`）来表达基本运算；而在 Python 中，通过重写以双下划线开头和结尾的特殊方法（即 Dunder Methods，源自 Double Underscore），自定义类可以像内置的 `int` 或 `list` 一样直接支持 `+`、`-`、`==`、索引切片和打印展示。

在这套协议中，最核心的两对方法是用于文本化表达的 `__str__` 与 `__repr__`，以及用于数学重载的二元操作符：
- **`__str__` 协议**：面向终端用户的友好可读文本，由 `print(obj)` 或 `str(obj)` 隐式触发；
- **`__repr__` 协议**：面向开发人员的严谨无歧义代码级表达，由交互式 REPL 或调试器调用；
- **操作符重载协议**：例如 `__add__` 拦截 `+` 操作符，`__eq__` 拦截判等操作符。如果传入的右操作数类型不匹配，良好实践是返回 `NotImplemented` 以便 Python 尝试调用反向操作符或降级报错。

```python
class Coordinate:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        
    def __str__(self) -> str:
        # 面向终端用户的友好可读文本表示 (供 print() 和 str() 调用)
        return f"({self.x}, {self.y})"
        
    def __repr__(self) -> str:
        # 面向开发者的严谨无歧义表示 (供 REPL 和调试器调用)
        return f"Coordinate({self.x}, {self.y})"
        
    def __add__(self, other: "Coordinate") -> "Coordinate":
        # 重载 '+' 加法运算符，实现向量相加
        if not isinstance(other, Coordinate):
            return NotImplemented
        return Coordinate(self.x + other.x, self.y + other.y)
        
    def __eq__(self, other: object) -> bool:
        # 重载 '==' 判等运算符，从比对内存地址升级为比对数学值
        if not isinstance(other, Coordinate):
            return False
        return self.x == other.x and self.y == other.y

# 优雅的面向对象调用体验
c1 = Coordinate(3, 4)
c2 = Coordinate(1, 2)
c3 = c1 + c2  # 隐式触发 Coordinate.__add__(c1, c2)

print(c3)           # 输出: (4, 6)
print(c1 == c2)     # 输出: False
print(c3 == Coordinate(4, 6))  # 输出: True!
```

这种设计使得数据结构的使用体验极其自然流畅。调用方完全不需要记忆类似 `vector_sum` 之类的专用函数名，只需要使用通用数学符号即可完成计算，这就是高级语言“多态接口”所带来的表达力解放。

::: pitfall 直接绕过接口篡改内部属性
Python 哲学信奉“大家都是成年人（We are all consenting adults here）”，并未像 Java/C++ 那样在编译器层面通过 `private` 关键字物理锁死外部写入。但外部代码随意书写 `c1.x = "broken"` 将直接破坏类的内部不变式（Representation Invariants）。在团队工程中，约定以下划线开头的属性（如 `_x`）为私有内部细节，严禁外部代码直接越界访问。
:::

## 我的理解

::: insight 面向对象是主客体世界的代码投射
过程式编程让开发者像上帝一样站在云端，通过一条条指令操纵无生命的被动数据。而面向对象编程让每一个数据对象苏醒过来，成为具备自主职责的主体（Agent）。对象守护自己的状态，通过发送消息（方法调用）与其他对象协同。这种由自治微观实体涌现出宏观复杂系统的架构思想，是应对大规模软件工程复杂度的终极利器。
:::
