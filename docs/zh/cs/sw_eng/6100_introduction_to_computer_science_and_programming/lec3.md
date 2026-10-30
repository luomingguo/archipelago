---
title: 列表序列、原地可变性与作用域环境
type: lecture
lecture: 3
tags: [lists, mutability, aliasing, cloning, environment-model]
status: complete
source: https://introcomp.mit.edu/fall26
---

# Lec 3 列表序列、原地可变性与作用域环境（Lists, Mutation & Scope）

> MIT 6.100 · 计算机科学与 Python 编程导论 · Fall 2026 · 教材参考：Guttag 5.3, 4.1–4.3

## TL;DR

- **复合数据结构与可变性**：列表（List）是可容纳异构元素的有序序列，属于可变对象（Mutable Object），支持在保持原内存地址不变的情况下就地增删改。
- **别名（Aliasing）与幽灵修改**：当多个变量指向同一可变列表时，任一变量的修改均会在所有引用方立即生效；通过切片语法 `L[:]` 或 `L.copy()` 可生成浅拷贝副本以规避副作用。
- **可变参数传递机制**：Python 采用对象引用传递（Pass by Assignment），向函数传入可变对象并在内部就地修改时，将直接影响外部调用方的原始数据结构。

## 1. 列表数据结构与序列操作

列表是 Python 中最常用的可变复合数据容器。与不可变的标量（如整数、浮点数）和只读序列（如字符串、元组）不同，列表支持动态伸缩和就地元素重写。开发者可以在不创建全新数据对象的情况下，直接改变列表内部的内容与容量：

```python
tech_stack = ["Python", "Rust", "Go"]
tech_stack.append("TypeScript")
tech_stack[1] = "C++"
print(tech_stack)  # ['Python', 'C++', 'Go', 'TypeScript']
```

列表在 Python 内部基于动态数组（Dynamic Array）实现，其常用的时间复杂度特性如下：
- **按索引访问**：`L[i]` 为 $O(1)$ 常数时间操作，基于连续内存块的基地址加偏移量直接寻址。
- **末尾追加**：`L.append(x)` 为均摊 $O(1)$ 操作，利用底层的过量内存预分配机制，仅在容量耗尽时触发数据搬迁扩容。
- **切片复制**：`L[i:j]` 为 $O(k)$ 操作（$k = j - i$），在堆中分配一块新的内存连续区域，并将原切片区间内的对象引用逐一拷贝填充进去。

---

## 2. 别名现象与浅拷贝克隆

深入理解别名（Aliasing）以及变量在堆内存中的指向关系，是每一个 Python 程序员彻底摆脱幽灵数据污染 Bug 的必经门槛。

当我们简单地把一个变量名赋值给另一个变量名时，初学者往往误以为计算机会自动在内存中把整个列表完整克隆一份。然而在引用语义模型下，这种赋值操作仅仅是给原本的对象增加了一个新的访问别名：

```python
warm = ["red", "yellow", "orange"]
hot = warm
hot.append("pink")

print(warm)  # ['red', 'yellow', 'orange', 'pink']
```

在执行 `hot = warm` 这条语句时，Python 解释器既没有分配新的列表堆块，也没有拷贝列表中的任何字符串引用。此时变量 `warm` 和 `hot` 仅仅是在栈帧中各自持有一个指向堆中同一列表地址的指针：

```text
栈帧 (Frame)                   堆内存 (Heap)
┌───────────┐                 ┌─────────────────────────────────┐
│   warm    ├────────────────►│  列表对象 0x7F                   │
└───────────┘                 │  [0] -> "red"                   │
                              │  [1] -> "yellow"                │
┌───────────┐                 │  [2] -> "orange"                │
│    hot    ├────────────────►│  [3] -> "pink"                  │
└───────────┘                 └─────────────────────────────────┘
```

::: definition 别名（Aliasing）
在执行环境中，两个或多个变量名同时绑定到堆内存中的同一个可变对象，通过任何一个变量执行的原地修改（In-place Mutation）都会反映在所有关联变量的观测视图中。
:::

### 消除副作用：浅拷贝克隆（Cloning）

如果我们的算法逻辑确实需要在修改数据的同时保留原始状态，就必须显式指示解释器对可变列表进行克隆。克隆操作会在堆中开辟独立的新列表容器，新容器内的各元素位置分别指向原列表中的对应对象：

```python
# 方法一：利用全区间切片语法克隆
cool = ["blue", "green"]
chill = cool[:]

# 方法二：调用列表内建的 copy() 方法
chill = cool.copy()

chill.append("grey")
print(cool)   # ['blue', 'green'] (保持不受影响)
print(chill)  # ['blue', 'green', 'grey']
```

需要特别注意的是，无论切片还是 `copy()` 方法均属于浅拷贝（Shallow Copy）。如果列表中嵌套了更深层的子列表，子列表本身的内存地址依然会在父容器之间被共享。

---

## 3. 函数参数中的可变性与副作用

在 Python 的函数调用机制中，实参向形参的传递本质上是一次局部的变量赋值操作（Pass by Assignment）。如果传入实参是一个不可变标量（如整数），局部操作无论如何都不会波及外部；但如果实参是一个可变列表，情况就会发生质的变化。

形式参数在函数调用时绑定的仍然是外部列表对象的堆内存地址。因此，如果在函数体内部执行了原地修改方法（如 `append`、`pop` 或索引重新赋值），这些改动将直接穿透局部栈帧的隔离屏障，影响调用方的原始数据结构。这种在计算返回值之外对系统状态造成的持久变动被称为函数的副作用（Side Effect）：

```python
def remove_duplicates(target_list: list) -> None:
    """
    就地剔除列表中的重复项（存在迭代时删除陷阱的典型案例）
    """
    for item in target_list:
        if target_list.count(item) > 1:
            target_list.remove(item)
```

在实际工程中，如果未能清晰声明副作用，将给系统调试带来灾难性的隐蔽故障。更致命的是，初学者常常试图在遍历列表的同时动态修改其结构。

::: pitfall 遍历中修改容器陷阱
在上述 `remove_duplicates` 代码中，Python 内部通过索引计数器维护当前遍历位置。当执行 `target_list.remove(item)` 后，被删除元素之后的所有元素会自动左移填补空缺，导致迭代器的内部指针在下一轮循环中跳过紧邻的下一个元素，造成某些重复元素未能被正确扫描。
正确的做法是遍历原始列表的只读克隆副本，而只在目标列表上执行修改操作：
```python
def remove_duplicates_safe(target_list: list) -> None:
    # 遍历副本，修改原件
    for item in target_list[:]:
        if target_list.count(item) > 1:
            target_list.remove(item)
```
:::

## 我的理解

::: insight 可变性是灵活也是脆弱的源泉
不可变对象（如字符串与元组）天然具备线程安全与引用透明性，因为无论如何共享，它的状态都永远固定。而可变列表为动态算法与大规模数据更新提供了高效的原地执行机制。理解别名与作用域环境，就是要学会清晰界定“何时应该共享内存提高效率，何时必须深浅拷贝构建隔离屏障”。
:::
