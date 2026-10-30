---
title: 继承层次、多态与设计原则
type: lecture
lecture: 21
tags: [inheritance, polymorphism, oop, liskov-substitution, super]
status: complete
source: https://introcomp.mit.edu/fall26
---

# Lec 21 继承层次、多态与设计原则（Inheritance & Polymorphism）

> MIT 6.100 · 计算机科学与 Python 编程导论 · Fall 2026 · 教材参考：Guttag 10.2

## TL;DR

- **继承机制与代码复用**：派生子类（Subclass）自动继承基类（Superclass）的全部属性与方法，通过局部增量扩展或方法覆写（Override）实现类型层次化构建。
- **`super()` 协议与方法调度**：子类通过 `super().__init__(...)` 安全调用父类初始化器，顺着方法解析顺序（MRO）协同初始化基础状态，避免重复定义。
- **里氏替换原则（LSP）与多态**：多态（Polymorphism）允许上层调用方对基类抽象接口编程，任何子类实例在语义上都可以安全替代父类出现，而不破坏程序的整体正确性。

## 1. 继承（Inheritance）的抽象威力

在现实世界中，概念天然具有分类继承体系：例如“学生”和“教授”都是“人（Person）”的特化子类。他们共享人所拥有的共有属性（如姓名、出生年份、身份证号），但同时又各自具备独特的特化职责（如学生的选课清单、教授的工资和指导研究生列表）。

如果为每个人类角色单独从零编写一个类，不仅会产生天量的重复代码，而且一旦“人”的基础属性发生变动，就需要修改所有相关类。

**继承（Inheritance）** 允许我们建立自顶向下的类型演化树：
- **基类 / 父类（Superclass / Parent Class）**：抽取共性特征，定义顶层通用的状态与接口；
- **派生类 / 子类（Subclass / Child Class）**：继承父类的全部资产，仅针对局部差异进行增量编程。

---

## 2. 类的继承实现与方法覆写（Override）

在 Python 中，通过在类声明后的圆括号内指明父类名称建立继承关系。子类自动获得父类所有可访问的方法和属性，构成了面向对象体系中自顶向下的知识复用链。

在实现派生子类时，最核心的初始化约定是通过内置的 `super()` 函数委派调用父类的 `__init__` 方法。这保证了父类所维护的基础状态（如底层的姓名与出生年）能够被规范地初始化，子类只需专注于初始化自己特有的新增字段（如学号）。如果不调用父类的初始化器，子类实例将缺失父类必要属性的赋值，导致后续继承的方法在运行时抛出 `AttributeError` 崩溃。

此外，Python 允许类持有**类变量（Class Variables）**。类变量直接定义在类体内部、方法外部，由该类所派生出的所有具体实例全局共享同一份内存引用。这非常适合用来实现自增的全局唯一标识生成器：

```python
class Person:
    """
    通用人类基类：维护姓名与出生年份基础信息
    """
    def __init__(self, name: str, birth_year: int):
        self.name = name
        self.birth_year = birth_year
        
    def get_age(self, current_year: int) -> int:
        return current_year - self.birth_year
        
    def __str__(self) -> str:
        return f"{self.name} (出生于 {self.birth_year})"

class MITPerson(Person):
    """
    MIT 社区成员：继承自 Person，分配唯一的学校 ID
    """
    _next_id_num = 0  # 类变量：所有实例共享的自增 ID 计数器
    
    def __init__(self, name: str, birth_year: int):
        # 必须显式调用父类初始化器，以建立 name 和 birth_year
        super().__init__(name, birth_year)
        self.id_num = MITPerson._next_id_num
        MITPerson._next_id_num += 1
        
    def get_id(self) -> int:
        return self.id_num
        
    def __lt__(self, other: "MITPerson") -> bool:
        # 重载 '<' 操作符，规定 MIT 成员默认按学号/工号排序
        return self.id_num < other.id_num
```

在上述代码中，`MITPerson` 继承了 `Person` 的 `get_age()` 方法，因此调用 `mit_person.get_age(2026)` 时，Python 解释器在子类中未找到该方法，便会自动顺着方法解析顺序（Method Resolution Order, MRO）向基类平滑回溯找到并正确执行。

### 方法覆写（Method Overriding）

子类不仅可以扩展新增方法，更可以通过定义与父类同名同签名的方法，来彻底替换或定制父类的默认行为，这一机制被称为**方法覆写（Overriding）**。

例如，对于通用的 `MITPerson`，其默认的 `__str__` 仅展示名字和出生年。但对于特定的本科生或研究生（`Student` 子类），我们希望在其打印文本中显式追加其主修专业代号：

```python
class Student(MITPerson):
    """
    学生子类：特化其字符串展示方式
    """
    def __init__(self, name: str, birth_year: int, major: str):
        super().__init__(name, birth_year)
        self.major = major
        
    def __str__(self) -> str:
        # 覆写父类的 __str__ 方法，追加专业信息
        return f"学生: {self.name} | 专业: {self.major} | ID: {self.id_num}"
```

当外部代码执行 `print(student_instance)` 时，Python 的动态分发机制（Dynamic Dispatch）首先在最具体的 `Student` 命名空间中定位到 `__str__`，直接执行子类的特化输出，而无需改动父类的任何一行原始代码。

---

## 3. 多态（Polymorphism）与里氏替换原则（LSP）

继承的最崇高境界是**多态（Polymorphism）**：即同一个接口调用，作用于不同形态的具体子类对象时，能够自动表现出各自正确的行为响应。

高水平的面向对象架构设计应当牢牢遵守由图灵奖得主芭芭拉·利斯科夫（Barbara Liskov，MIT 荣休教授）提出的**里氏替换原则（Liskov Substitution Principle, LSP）**：

::: definition 里氏替换原则（LSP）
如果 $S$ 是 $T$ 的子类型，那么程序中任意使用基类 $T$ 对象的地方，在语义上都可以安全地用子类 $S$ 的对象替换，而不会改变程序的原有预期行为和正确性。
:::

这意味着子类在扩展父类时：
- 不能削弱父类方法的前置条件（不能要求更苛刻的输入）；
- 不能违背父类方法的后置条件（返回值的类型与保证必须与父类契约完全兼容）。

```python
def process_census(community: list, current_year: int) -> None:
    """
    多态消费函数：仅依赖 Person 基类接口，无论传入的是学生、教授还是普通员工，均能正确处理
    """
    for member in community:
        print(f"{member} -> 当前年龄: {member.get_age(current_year)}")

# 混合各种子类实例的异构列表
mit_group = [
    Person("Bob", 1980),
    MITPerson("Alice", 2002),
    Student("Charlie", 2005, "Course 6-3")
]

process_census(mit_group, 2026)
```

调用方代码 `process_census` 完全不需要使用 `isinstance()` 去繁琐地分辨“你是学生还是普通人”。多态消除了根据类型做 `if-elif-else` 分流的坏味道，使系统在未来新增“访学学者”等新子类时具备极高的开闭原则（Open-Closed Principle）扩展性。

::: pitfall “优先组合而非继承”（Composition over Inheritance）
初学者常滥用继承，将具有包含关系（Has-a）的对象强行写成继承关系（Is-a），例如“大学继承自学生列表”或“汽车继承自发动机”。不恰当的深层继承会导致子类与父类的内部实现产生强耦合（脆弱基类问题）。在工业级工程中，只有当两者在语义上严格满足泛化与特化关系且服从 LSP 时，才使用继承；其余情况应优先采用将组件对象作为属性嵌入的组合（Composition）设计。
:::

## 我的理解

::: insight 面向抽象编程是应对演化的根本之道
继承让代码具备了分类学的整洁，而多态则让系统拥有了演化适应力。多态的精髓在于“调用方只与稳定的抽象契约对话，具体的差异由派生实体各自封装自理”。当每一个新加入的模块都严格信守父类契约，系统便能在不改动任何核心业务逻辑的前提下，实现无缝横向扩展。
:::
