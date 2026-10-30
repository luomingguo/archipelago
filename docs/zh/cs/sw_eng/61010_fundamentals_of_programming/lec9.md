---
title: 继承与面向对象设计
type: lecture
lecture: 9
tags: [object-oriented-design, inheritance, polymorphism, shape-drawing]
status: complete
---

# Lec 9 继承与面向对象设计（Inheritance & OO Design）

> 参考资料：[Inheritance and Object-oriented Design](https://py.mit.edu/spring26/readings/inheritance)

## TL;DR

- **继承体系与环境模型**：子类定义 `class B(A)` 时，在堆中的类对象 B 内部建立指向超类对象 A 的超类指针；方法和属性查找沿着“实例 $	o$ 子类 $	o$ 父类 $	o$ object”逐级向上追溯。
- **模板方法模式（Template Method Pattern）**：基类（如 `Shape`）实现通用的高层算法（如 `draw` 像素光栅化循环），内部调用延迟到具体子类实现的抽象方法（如 `__contains__`），达成极大程度的代码复用。
- **动态属性描述符（@property）**：利用 `@property` 与 `@setter` 将动态计算（如矩形中心点坐标 `center`）伪装为普通属性访问，既符合外界公开 API 契约，又保证内部联动更新。
- **组合优于继承**：利用运算符重载（如 `__or__`、`__and__`）将多个形状实例通过布尔运算组合为复合形状（`UnionShape`），比无休止地派生多重继承子类更加灵活健壮。

## 面向对象中的继承机理

上节课我们引入了 `class` 关键字。类不仅仅是一种自定义类型的封装手段，更是管理大规模软件复杂度的核心组织架构。本讲我们将探讨如何利用“继承”（Inheritance）消除冗余代码，并建立清晰的面向对象设计层次。

## 继承

我们关于属性查找的规则不仅涉及在实例及其类中查找，还可能涉及在其他类中查找（具体来说，如果我们正在处理的类有超类的话，会查找该类的超类）。但是到目前为止，我们还没有在我们的环境图中展示过任何这种关系。

回顾一下，我们上一节提到，变量查找，属性查找。

> [!IMPORTANT]
>
> 要查找一个变量：
>
> 1. 先查找当前帧
> 2. 如果未找到，在父帧中查找
> 3. 如果未找到，查找那个帧的父帧（继续跟随该过程，在父帧中查找）
> 4. 如果未找到，查找全局帧如果未找到，
> 5. 查找内置变量（诸如 print、len 等的绑定）
> 6. 如果未找到，引发 NameError
>
> 我们在这里引入的是一个另外的东西，我们称之为属性查找。这个概念是我们已经找到一个对象，而不是在帧内查找一个变量，我们想要在该对象内部查找一些内容。这个过程略有不同进行：
>
> 1. 首先查找对象本身
> 2. 如果未找到，则查找该对象的类
> 3. 如果未找到，则查找该类的超类
> 4. 如果未找到，则查找该超类的超类
> 5. 如果未找到且没有更多的超类，则引发 AttributeError。

但是到目前为止，我们还没有在我们的环境图中展示过任何这种关系，也没有讨论过这种关系对我们的代码的实际影响，更没有谈到在设计程序时如何利用这种关系。

```python
x = "dog"
class A:
  x = "cat"
class B(A):
  pass
b = B()
print(b.x)
```

这个例子，我们保持 A 的定义不变， 但是我们定义了 B，B 后面括号 A，表示 B 时 A 的子类。但 Python 看到新定义的 B 类后，创建 B 类对象，并且引用父类。通过这种方式，在 A 定义而在 B 类没有定义的属性，也能被 B 类所访问，我们说 B 继承了 A 的属性和方法。

![类B继承自类A时在堆中建立指向父类对象的超类引用](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66753b0486e43.png)

当我们执行到``b=B()``时候，环境图如图

![实例化子类B并在实例属性未命中时沿继承链查找超类A](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/6675465bd4cfe.png)

当我们求解``b.x``时候，Python首先通过名称b找到我们的实例，然后从实例中找名``x``的属性。没有找到，就顺着箭头找到B指向的对象，我们也没找到，进而找到类A，我们找到了``"cat"``

几个例子

```python
class A:
    x = "apple"

class B(A):
    x = "banana"

    def __init__(self) -> None:
        self.x = "potato"
b = B()
print(b.x)
```

> 答案：
>
> potato

需要记住的是，当我们实例化一个类是，Python 回去找名字为\_\_init__函数来初始化实力，并且遵循**“属性查找”**原则，当他找到后，会隐式调用。看下面这个例子。

```python
class A:
    x = "apple"

class B(A):
    x = "banana"

    def __init__(self):
        self.x = "potato"

class C(B):
    x = "peach"
c = C()
print(c.x)
```

> 答案
>
> potato

但我们使用

```python
class A:
    x = "apple"

class B(A):
    x = "banana"

    def __init__(self):
        self.x = "potato"

class C(B):
    x = "peach"
    def __init__(self):
      pass
c = C()
print(c.x)
```

> 答案
>
> peach

## 案例：绘图库

虽然我们学习几个例子感受继承背后的一些原理，这些知识对学好 Python 很重要，但是我们还没了解何时以及为什么要用这些特性在我们代码上。那下面我们就通过案例来更好地说明，我们应该如何通过这些特性来组织我们的代码，从而为管理大型程序的复杂度打下基础

### 需求

#### 基本信息

这个案例需求是实现一个绘图库，实现绘制复杂形状的功能。

在本节最后提供了一个代码框架。如果你感兴趣的话，可以在你电脑上跑。该代码顶部附近的一些辅助函数，但我们的关注点不在上面，而是关于对形状的表示和绘图实现。我们定义形状的方式是像素。

- 相对原点坐标（0, 0）在左下角,x 和 y 都是向上增长

- 一个像素位置是（x, y），如何判断这个形状的一部分吗？
  - 答： 蓝色点像素是形状的一部分，而红色点则不是

![二维图像画布的坐标网格与左下角原点映射](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/667645128ce2b.png)

我们准备用类代表形状。实现上述功能，我们需要用到特殊的魔法方法\_\_contains__，它是用来实现自定义类型``in``关键字功能的，``(x, y) in s``会被解释称``s.__contains__((x, y))``

- 任何图形的中央像素值是什么？
  - 我们用 s.center 来表示（x, y）
- 如何实现绘制图形
  - 给形状类 ``s`` 定义额外的方法``s.draw(im, color)``，其中 im 是实验 2 的格式，color 是（r, g, b）元组

```python
class Shape:
  """
  代表2维形状
  __contain__(self, p) 返回true如果点p在形状内
    ”(x, y) in s“ 在shape的实例中会被自动转成s.__contain__((x, y))

  s.center 返回形状的中心点(x ,y)

  draw(self, image, color) 

  """

  def __contains__(self, p):
    pass
  def draw(self, image):
    pass
```

#### 形状、圆和矩形类定义

首先，我们通过派生具体的子类来扩展 `Shape`。在定义具体的几何对象时，第一要务是明确其在内存中需要维持的最小充分状态集合：
- 对于**圆形（Circle）**：几何学上由中心点坐标 `(cx, cy)` 与标量半径 `radius` 唯一确定；
- 对于**矩形（Rectangle）**：在轴对齐的前提下，由左下角参考点坐标 `(x0, y0)` 以及横向跨度 `width` 和纵向跨度 `height` 唯一确定。

```python
class Circle(Shape):
    pass

class Rectangle(Shape):
    pass
```

通过继承声明，`Circle` 与 `Rectangle` 的类对象在创建之初便持有了指向 `Shape` 的超类指针。接下来，我们为两个子类分别编写构造函数 `__init__`，将各自特有的几何属性固定在实例对象中。在几何判别逻辑上，判定任意测试点 `(px, py)` 是否落在圆内，只需计算点到圆心的欧几里得距离平方 $(px - cx)^2 + (py - cy)^2 \le r^2$；而对于轴对齐矩形，只需检查测试点横纵坐标是否分别严格落在 $[x_0, x_0 + \text{width}]$ 与 $[y_0, y_0 + \text{height}]$ 区间内部。两者的几何公式完全正交，天然适合由各自子类独立承载：

```python
class Circle(Shape):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

class Rectangle(Shape):
    def __init__(self, lower_left, width, height):
        self.lower_left = lower_left
        self.width = width
        self.height = height
```

下一步是确定如何实现点在图形内的包含测试协议 `__contains__`。很多面向对象初学者容易陷入一个严重的“上帝类反模式”（God Class Anti-pattern）：既然所有形状都继承自 `Shape`，是不是可以在父类 `Shape` 的 `__contains__` 中用 `if-isinstance` 把所有子类的计算全包揽下来？例如：

```python
class Shape:

  def __contains__(self, p):
    if isinstance(self, Circle):
      # 基于圆和半径计算
    if isinstance(self, Rectangle):
      # 基于圆和半径计算
  def draw(self, image):
    pass

class Circle(Shape):
  def __init__(self, center, radius):
    self.center = center
    self.raidus = radius
    
class Rectangle(Shape):
	def __init__(self, lower_left, width, height):
    self.low_left = lower_left
    self.width = width
    self.height = height
    
```

值得一提的是，这种结构是可行的，即从技术上讲，可以通过这种方式实现.但是我们会建议避免这种代码（特别是**显式类型检查**的代码），主要有几个原因。

主要原因是要考虑到未来可能会扩展我们的库，不仅仅包含圆形和矩形。目前，如果我们考虑添加一种新形状，那么我们需要在**多个地方修改代码**（需要创建一个新类并确保其设置了正确的属性，但随后我们还需要跳到 Shape 类中，在\_\_contains\_\_方法中添加新的条件，并确保这两个地方是一致的！）。不仅如此，如果我们不断添加形状，这个 v 方法会变得非常庞大和复杂，这会成为一个容易出现错误的地方。

我们希望添加新形状的过程更加简便，即所有与特定形状相关的内容都存在于一个地方（在子类中）。所以，组织上我们要实现的是：

- 只有对所有形状通用的内容才定义在 Shape 类中，
- 而特定形状的所有内容都定义在该形状的子类中

尽管有这个目标，但我们确实需要一种方法来区分这些行为。不过，我们将利用在这篇和上一篇阅读中学到的规则，避免编写显式类型检查代码。

```python
class Shape:

  def __contains__(self, p):
    raise NotImplementedError("Subclass of Shape didn't define __contains__")
  def draw(self, image):
    pass

class Circle(Shape):
  def __init__(self, center, radius):
    self.center = center
    self.raidus = radius
  def __contains__(self, p):
    # todo: 基于圆做计算
    assert isinstance(p, tuple) and len(p) == 2
    return sum(i-j) ** 2 for i, j in zip(self.center, p) <= self.raiius ** 2
    
class Rectangle(Shape):
	def __init__(self, lower_left, width, height):
    self.low_left = lower_left
    self.width = width
    self.height = height
  def __contains__(self, p):
    # todo: 基于矩形做计算
    px, py = p
    llx, lly = self.lower_left
    return {
      llx <= px <= llx+self.width
      and lly <= py <= lly+self.height
    }
    
```

通过这种方法，Python 隐式地为我们进行类型检查，而不是显式地进行，这样可以保持我们的代码更清晰、更模块化（这将使理解、测试、调试和扩展程序变得更容易！）。

#### draw 方法实现

本节我们会再介绍一种组织方式，首先，让我们尝试以与\_\_contains\_\_相同的方式组织代码，即在每个子类中实现 draw 方法。

```python
class Circle(Shape):
  #...
  def draw(self, image, color):
    for x in range(image['width']):
      for y in range(image['height']):
        if(x, y) in self:
          set_pixel(image, x, y, color)
          
    
class Rectangle(Shape):
  #...
  def draw(self, image, color):
    for x in range(image['width']):
      for y in range(image['height']):
        if(x, y) in self:
          set_pixel(image, x, y, color)
          
```

![圆形与矩形绘制在图像画布上的复合图形效果](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/66766b57c6bea.png)

这些函数是完全相同的！通常情况下，像这样复制复杂的代码只会让你的代码更容易出现错误；它们给了错误很多藏身之处，并且使得当出现问题时更难找到并修复这些错误。

但更重要的是，现在实现的 draw 方法是完全通用的。它不仅适用于正方形或矩形，而且适用于任何能够执行包含检查（通过\_\_contains\_\_方法）的形状。

```python
class Shape:

  def __contains__(self, p):
    raise NotImplementedError("Subclass of Shape didn't define __contains__")
  def draw(self, image, color):
    for x in range(image['width']):
      for y in range(image['height']):
        if(x, y) in self:
          set_pixel(image, x, y, color)
```

完成这个步骤后，任何时候在 Shape 类的任何子类中寻找 draw 方法时，我们都找不到 draw 方法，但会沿着链条向上查找到 Shape 类，在那里我们会找到这个方法。

可能有些地方看起来有点奇怪，即我们在 Shape 类中定义了 draw 方法，但在 draw 方法内部却调用了一个\_\_contains\_\_方法。那么我们会不会得到之前在 Shape.\_\_contains\_\_中引发的 NotImplementedError 呢？

事实证明这会完全正常！通常情况下，调用 draw 方法的方式是通过 Circle 或 Square 等形状的实例。因此，在 draw 方法内部，**self 指的是这些子类的实例之一**。因此，当我查找 self.\_\_contains\_\_时，Python 会找到适合我们调用 draw 方法的形状类型的正确\_\_contains\_\_方法。这一点起初可能会感到有些奇怪，但这种将通用代码移到超类中的方法，然后调用子类中定义的特定方法的思想是一种非常常见和强大的组织方式，可以避免重复代码。

#### 动态中心点与 @property 属性描述符

还有规范中的另一部分我们还没有解决：中心点属性。

方便的是，我们的 Circle 类已经实现了这一点，因为我们在类定义中存储了中心点！但是我们需要确保为 Rectangle 类也实现这个功能。

```python
class Rectangle(Shape):
    def __init__(self, lower_left, width, height):
        self.lower_left = lower_left
        self.width = width
        self.height = height
        self.center = (lower_left[0] + width / 2, lower_left[1] + height / 2)
```

也许这是正确的做法（这完全取决于你的实现选择！）。但让我们假设一下，如果我希望允许我的形状是可变的，即我想能够更改某个 Rectangle 实例的 lower_left。在这种情况下，我们可能会遇到一个问题，即移动 lower-left 角应该同时影响到 center，但上面的代码并没有考虑到这一点！

在像这样存在相关值存储在实例中的情况下，避免这个问题的一种方法是将 center 定义为一个方法而不是属性：

```python
class Rectangle(Shape):
    def __init__(self, lower_left, width, height):
        self.lower_left = lower_left
        self.width = width
        self.height = height
    
    def center(self):
        return (self.lower_left[0] + self.width / 2, self.lower_left[1] + self.height / 2)

```

这种结构将解决上面提到的问题，因为如果我们改变了 r.lower_left，那么 r.center()将会相应地调整！但它也有一个缺点，那就是它不再符合我们的规范。我们的规范说 r.center 应该是一个元组，但是使用这种代码我们需要写 r.center()而不是直接访问属性。

不过 Python 为我们提供了一种解决方法，即通过**@property 装饰器**。如果我们在方法的定义上方写上@property：

```python
class Rectangle(Shape):
    def __init__(self, lower_left, width, height):
        self.lower_left = lower_left
        self.width = width
        self.height = height
    
    @property
    def center(self):
        return (self.lower_left[0] + self.width / 2, self.lower_left[1] + self.height / 2)
```

那么当我们使用 r.center（没有圆括号）时，Python 将自动调用这个方法并返回结果（因此即使我们使用动态计算的中心值，也可以满足给定的规范要求！）。

事实证明，带有@符号的这种语法比这个更通用（我们将在下一篇阅读中进一步讨论），但目前来说，将`@property`视为一种特殊的语法是可以的。

除了定义只读属性之外，Python 的属性描述符协议还支持双向绑定。如果我们希望能够执行 `r.center = (2, 3)` 显式移动图形，但 `r.center` 底层并没有真实的存储字段，我们可以通过配置 `@center.setter` 装饰器拦截赋值操作。当外部为 `center` 赋予新坐标时，setter 方法会自动计算出对应的差量，并反向调整底层的 `self.lower_left` 锚点：

```python
class Rectangle(Shape):
    def __init__(self, lower_left, width, height):
        self.lower_left = lower_left
        self.width = width
        self.height = height
    
    @property
    def center(self):
        return (self.lower_left[0] + self.width / 2, self.lower_left[1] + self.height / 2)
    
    @center.setter
    def center(self, value):
      self.lower_left = (value[0] - self.width // 2, value[0] - self.height // 2)
```

### 绘图库完整架构分层实现

在工业级工程落地中，图形渲染库通常分为两个清晰的架构层次：底层的**像素光栅化与文件 I/O 支撑层**，以及上层的**几何对象与多态继承层**。

#### 图像底层缓冲区与坐标映射工具

底层支持模块负责管理平面的像素存储与文件落盘。在图形学与图像处理中，内存布局与数学直觉往往存在冲突：
- 数学坐标系通常将左下角定义为笛卡尔原点 $(0, 0)$，横轴向右为 $X$，纵轴向上为 $Y$；
- 计算机屏幕与位图文件格式（如 PNG/BMP）普遍将左上角定义为原点 $(0, 0)$，行号向下递增。

为了解决这一不一致，辅助函数 `flat_index(image, x, y)` 执行了一个精妙的坐标系翻转映射：计算公式为 `(height - 1 - y) * width + x`。通过在垂直方向进行倒置，调用方可以使用完全符合几何常识的“向上为正”笛卡尔坐标系统，而底层自动将其线性化为适配内存行优先存储的一维偏移量。

此外，我们在 `set_pixel` 函数中加入了严格的防御性断言：确保传入的颜色对象不仅是包含三个分量的元组，而且每个通道的数值都必须是落入 $[0, 255]$ 范围内的整数。这种在基础数据层筑牢防御防线的做法，能够将类型错误拦截在发生的瞬间。

在导出机制上，`save_color_image` 借用了 Python Imaging Library（PIL / Pillow）的高性能 C 底层接口。我们通过 `PILImage.new("RGB", (width, height))` 建立轻量级图像句柄，并调用 `out.putdata(pixels)` 一次性将 Python 列表中的所有颜色三元组高速灌入原生图形缓冲区，最后调用 `out.save(filename)` 完成磁盘持久化。这种架构巧妙地实现了职责解耦：核心的几何数学运算完全使用纯 Python 原生字典与列表表达，仅在最终的落盘渲染步骤借力成熟工业库，既保持了极佳的算法透明度，又保证了工程实用性。

```python
from PIL import Image as PILImage

# 调色盘预设色彩
COLORS = {
    "red": (255, 0, 0),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "green": (0, 100, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 230, 0),
}

def new_image(width, height, fill=(240, 240, 240)):
    """分配一个带有指定背景底色的全新图像字典。"""
    return {
        "height": height,
        "width": width,
        "pixels": [fill for _ in range(height * width)],
    }

def flat_index(image, x, y):
    """将笛卡尔坐标 (x, y) 转换为内存数组的线性索引。"""
    assert 0 <= x < image["width"] and 0 <= y < image["height"]
    return (image["height"] - 1 - y) * image["width"] + x

def set_pixel(image, x, y, color):
    """在有效范围内为指定像素赋予目标 RGB 颜色元组。"""
    if 0 <= x < image["width"] and 0 <= y < image["height"]:
        image["pixels"][flat_index(image, x, y)] = color

def save_color_image(image, filename, mode="PNG"):
    """利用 PIL 将内存中的像素列表导出保存为 PNG 文件。"""
    out = PILImage.new(mode="RGB", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    out.save(filename)
    out.close()
```

#### 形状继承体系与渲染执行

上层模块代表了面向对象设计模式中极富盛名的**模板方法模式（Template Method Pattern）**。基类 `Shape` 充当骨架定义者：它并不了解具体的几何形态，却提供了一个完全通用的 `draw(image, color)` 渲染管线。

该管线执行“全屏光栅化检测”（Rasterization）：通过双重循环遍历画布内的每一个离散坐标 `(x, y)`，并利用 Python 的 `in` 运算符触发 `(x, y) in self`。当执行该判定时，Python 解释器自动将其翻译为调用 `self.__contains__((x, y))`。因为 `self` 是具体子类（如 `Circle` 或 `Rectangle`）的实例，属性查找机制会自动分发调用子类中重写的具体包含逻辑：
- 在 `Circle` 中，依据勾股定理计算当前测试点到圆心 `(cx, cy)` 的欧几里得距离平方，若小于等于半径平方 $r^2$ 则判定为落在圆内；
- 在 `Rectangle` 中，只需检查测试点横纵坐标是否同时落在闭区间 $[x_0, x_0 + 	ext{width}]$ 与 $[y_0, y_0 + 	ext{height}]$ 内部。

这种架构的美妙之处在于其卓越的**开闭原则（Open-Closed Principle）**：未来若需要增加 `Triangle`、`Ellipse` 甚至任意复杂的多边形，超类 `Shape` 与现有的绘图管线完全不需要修改一行代码，只需派生新类并实现专属于该图形的 `__contains__` 几何判定即可无缝融入！

在主程序测试区段 `if __name__ == "__main__":` 中，我们实例化了一个 $300 	imes 300$ 的空白画布，并分别创建了一个蓝色矩形与一个红色圆形。当依次调用 `r.draw(canvas, COLORS["blue"])` 与 `c.draw(canvas, COLORS["red"])` 时，后绘制的红色圆形会自然覆盖重叠区域内的蓝色像素，呈现出完美的图层叠加合成效果。整套代码展现了多态机制在实际图形系统开发中的巨大威力。

```python
class Shape:
    """抽象几何图形基类：定义契约并提供通用的模板方法 draw。"""
    def __contains__(self, point):
        raise NotImplementedError("子类必须实现包含测试 __contains__")

    def draw(self, image, color):
        """模板方法：遍历图像所有像素点，包含在内部的点直接着色。"""
        for x in range(image["width"]):
            for y in range(image["height"]):
                if (x, y) in self:
                    set_pixel(image, x, y, color)

class Circle(Shape):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def __contains__(self, point):
        px, py = point
        cx, cy = self.center
        return (px - cx) ** 2 + (py - cy) ** 2 <= self.radius ** 2

class Rectangle(Shape):
    def __init__(self, lower_left, width, height):
        self.lower_left = lower_left
        self.width = width
        self.height = height

    def __contains__(self, point):
        px, py = point
        x0, y0 = self.lower_left
        return x0 <= px <= x0 + self.width and y0 <= py <= y0 + self.height

if __name__ == "__main__":
    canvas = new_image(300, 300)
    c = Circle((150, 150), 80)
    r = Rectangle((50, 50), 100, 60)
    r.draw(canvas, COLORS["blue"])
    c.draw(canvas, COLORS["red"])
    save_color_image(canvas, "output_shapes.png")
```

### 面向对象架构重构与设计准则

我们放眼整体，看继承在实际程序中作为组织工具的应用。特别是，我们探讨了如何利用继承来减少程序中冗余代码的数量，从而使程序更加清晰和可扩展。

当你考虑将这些想法应用到自己的程序中时，许多这些想法都适合进行一定程度的事先规划。我们可以提前思考要实现哪些类，它们之间的关系，它们支持的操作等等。但有些想法可能在编写代码时突然浮现。如果发生这种情况，不要害怕返回来重构你的代码；现在稍微花点时间进行重构，通常能够在后面的调试过程中节省大量时间！随着时间的推移和更多的实践，你将能够更好地提前识别哪些结构将有效，哪些不会。

这种持续的学习和实践将使你能够更加灵活和精确地设计和构建程序，从而更有效地利用面向对象编程的强大功能。

## 我的理解与工程洞察

::: insight 继承的利剑与枷锁：构建演进式类层次体系
面向对象的继承机制曾被誉为软件复用的银弹，但数十年的软件工程实践证明，滥用继承是导致系统僵化与高耦合的罪魁祸首。

在系统级面向对象设计中，必须把握四条黄金准则：
1. **里氏替换原则（LSP）**：任何使用基类 `Shape` 的代码，必须能够透明地替换为子类 `Circle` 或 `Rectangle`，且程序的行为逻辑不发生破坏。若子类重写父类方法时抛出意料之外的异常或篡改了前置条件，继承体系就已经失效；
2. **多态胜过分支判断**：如果你的代码中充斥着 `if isinstance(s, Circle): ... elif isinstance(s, Rectangle): ...`，说明面向对象设计彻底失败了。应当将分支内部的行为提炼为多态方法调用 `s.draw()`，让对象根据自身类型自主分发执行；
3. **组合优于继承（Composition over Inheritance）**：不要为了复用几个方法就盲目派生子类。通过在对象内部持有其他对象的引用并进行委托（Delegation），例如将两个 `Shape` 组合为 `UnionShape`，能使系统在面对动态需求变更时拥有比深度继承树高出几个数量级的抗震能力；
4. **属性描述符的防御价值**：永远不要在类定义中随意暴露直接可写的公开成员变量。善用 `@property` 与 `@setter` 可以在属性读写时增加校验逻辑、实现脏标记缓存与联动计算，保持外部调用接口的长期稳定。
:::
