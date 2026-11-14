---
title: '布局'
type: lecture
lecture: 10
tags: [css-layout, positioning, anchor-positioning, css-grid, responsive-design]
status: complete
---
# Lec 10 布局

## TL;DR

- 定位适合脱离或相对常规文档流放置元素，但应避免让绝对坐标承担整个页面结构。
- 锚定定位把浮层与触发元素建立显式关系，减少手工计算位置和视口边界的代码。
- Web 网格必须随容器和内容伸缩，CSS Grid 等布局原语比固定画布更能表达二维对齐关系。

## Web 布局机制

在现代 Web 体系中，页面布局经历了从“hack 式模拟”到“专用声明式原语”的完整演进：

1. **常规文档流与盒模型（Normal Flow & Box Model）**：块级与行内元素的自然排列，默认支撑自上而下、随内容伸展的文档排版。
2. **定位（Positioning）**：通过 `static`、`relative`、`absolute`、`fixed`、`sticky` 实现元素脱离文档流、局部微调或视口固定。
3. **浮动元素（Floats）**：最初设计用于报纸式的图文环绕，曾被滥用于分栏布局（伴随臭名昭著的 clearfix 清浮动），现代开发已回归其本质。
4. **一维弹性盒（Flexbox）**：`display: flex`，专门解决单行或单列内的空间分配、伸缩比例与轴线对齐。
5. **二维网格系统（Grid Systems）**：`display: grid`，在二维平面上同时控制行轨道与列轨道，彻底解决复杂的页面骨架排版。
6. **锚定定位（Anchor Positioning）**：现代 W3C 新规范，在脱离文档流的浮动元素（Tooltip、Dropdown、Popover）与参考锚点元素之间建立声明式依附关系。

## 定位

有几个属性对于这些盒子的尺寸计算非常关键：

- `padding`（内边距）控制的是元素内容到元素边缘之间的间距。
- `margin`（外边距）指定的是元素边缘与周围其他元素之间的距离，它甚至可以是负值，这样元素会更靠近其他元素，而不是更远。

- `border`（边框）允许你为元素设置可见边框，它位于 `padding` 的外侧。

- `padding` 和 `border` 的宽度会被加到 `width` 和 `height` 上，而不是从中扣除。

- `outline`（轮廓）、阴影等效果不会以任何方式影响盒子的实际尺寸。

- 始终要使用足够的 `padding`，否则文字会让人阅读起来不舒服。正如你在图形设计课程中学到的那样，通常水平方向需要的内边距会比垂直方向更多。

块级元素：

- 从上到下排列
- 元素前后会自动换行
- 盒子宽度会占满所有可用空间
- 盒子高度由其内容决定（内容会自动换行）
- 文本会在盒子内部换行
- 我们可以设置 [`width`](https://developer.mozilla.org/en-US/docs/Web/CSS/width), [`height`](https://developer.mozilla.org/en-US/docs/Web/CSS/height), [`margin`](https://developer.mozilla.org/en-US/docs/Web/CSS/margin)

行内元素：

- 按从左到右的方式排列
- 与周围文本处于同一行
- 盒子的宽度由内容决定
- 盒子的高度通常只有一行高
- 文本换行是通过盒子被拆分到多行中实现的
- [`width`](https://developer.mozilla.org/en-US/docs/Web/CSS/width), [`height`](https://developer.mozilla.org/en-US/docs/Web/CSS/height), [`margin`](https://developer.mozilla.org/en-US/docs/Web/CSS/margin)  属性不起作用

行内块级元素（inline-block）：

- 按从左到右的方式排列
- 与周围块处于同一行
- 盒子的宽度由内容决定

- 盒子宽度会占满所有可用空间
- 盒子高度由其内容决定（内容会自动换行）
- 文本会在盒子内部换行
- 我们可以设置 [`width`](https://developer.mozilla.org/en-US/docs/Web/CSS/width), [`height`](https://developer.mozilla.org/en-US/docs/Web/CSS/height), [`margin`](https://developer.mozilla.org/en-US/docs/Web/CSS/margin)

**替换元素（Replaced elements）**

理论上： 替换元素指的是一种元素，它的具体呈现内容不由 CSS 本身控制，而是来自外部资源或浏览器内部机制。

它们在布局中的行为通常类似于 `inline-block`，会与周围内容一起排布；但它们内部的内容不会受到当前文档样式的影响。

只有替换元素才可能拥有固有尺寸和固有宽高比。常见的替换元素有：

- `<img>`
- `<video>`
- `<iframe>`
- `<canvas>`
- `<input>`

**定位元素**

定位元素（positioned element）指的是任何 `position != static` 的元素。也就是说，只要元素的 `position` 不是默认的 `static`，它就是“定位元素”。

使用偏移属性来控制定位元素的位置，这些偏移属性包括`top、right、bottom、left`

使用相对定位的元素，仍然会占据原来的空间，但可以通过偏移属性移动自己的显示位置

绝对定位元素会让元素脱离正常文档流，并覆盖在其他内容之上。

## 锚定定位（CSS Anchor Positioning）

在 Web 开发历史上，工具提示（Tooltip）、下拉菜单（Dropdown Menu）、上下文菜单和悬浮卡片等“浮动层（Floating UI）”是实现成本最高、Bug 最频发的交互之一。

传统解决方案的痛点：
- **脱离 DOM 树的定位断裂**：浮动层通常为了避免被父级容器的 `overflow: hidden` 裁剪，必须挂载在 `document.body` 根节点下；
- **重度依赖 JavaScript**：必须引入数百 KB 的第三方库（如 Popper.js / Floating UI），在页面滚动（`scroll`）与视口缩放（`resize`）时高频监听事件，反复调用 `getBoundingClientRect()` 计算绝对像素坐标；
- **渲染不同步与布局抖动**：JS 计算与浏览器重排重绘管道存在时差，滚动较快时浮层容易发生肉眼可见的“飘移”或“脱靶”。

::: definition [CSS 锚定定位（Anchor Positioning）]
CSS 锚定定位是 W3C 推出的一套原生声明式定位标准，允许任意脱离文档流的元素（绝对定位或固定定位）将自身的坐标边缘锚定到页面中任意指定的“锚点元素（Anchor Element）”上，由浏览器底层图形管线直接在合成阶段完成贴合渲染，无需任何 JavaScript 坐标计算。
:::

### 核心语法与最小示例

锚定定位将“触发者”与“依附者”在视觉空间中解耦，其核心工作流分为三步：

1. **注册锚点（Anchor Registration）**：通过 `anchor-name` 属性为宿主元素分配一个 CSS 虚线标识符（Dashed Ident，以 `--` 开头，如 `--info-btn`）。该标识符遵循类似 CSS 自定义属性的作用域规则；
2. **声明依附关联（Target Binding）**：在浮动元素上设置 `position: fixed` 或 `position: absolute`，并通过 `position-anchor: --info-btn` 显式指定依附的目标；
3. **空间几何吸附（Coordinate Alignment）**：在定位偏移属性中调用 `anchor()` 函数。`anchor()` 接受锚点边缘作为参数（如 `top`, `bottom`, `left`, `right`, `center`），由浏览器自动计算偏移量。

```html
<!-- 1. 触发锚点按钮 -->
<button class="anchor-btn">悬停查看详情</button>

<!-- 2. 悬浮提示框 -->
<div class="tooltip" role="tooltip">这是锚定在按钮正下方的浮层提示</div>
```

```css
/* 1. 为锚点元素命名虚线标识符（Dashed Ident） */
.anchor-btn {
  anchor-name: --info-btn;
}

/* 2. 浮动层绑定锚点并定位 */
.tooltip {
  position: fixed;
  position-anchor: --info-btn; /* 绑定目标锚点 */
  
  /* 将 tooltip 的顶部贴合到锚点的底部，水平居中对齐 */
  top: anchor(bottom);
  left: anchor(center);
  transform: translateX(-50%);
  
  margin-top: 8px; /* 保持间距 */
  padding: 8px 12px;
  background: #1e293b;
  color: #fff;
  border-radius: 6px;
}
```

在上例中，当用户滚动页面或改变视口大小时，浏览器渲染引擎会在合成阶段（Compositor Thread）直接重算 `.tooltip` 的位置，完全跳过主线程 JS 计算与重排，达到 60fps / 120fps 的黄油般顺滑跟手效果。同时，`anchor-size()` 函数还能让浮动层的宽高根据锚点尺寸动态缩放（如制作与输入框完全等宽的下拉搜索结果列表）。

### 智能边界回退：`@position-try`

浮动层最棘手的问题是**视口边界碰撞（Collision Handling）**——当锚点靠近屏幕底部时，默认贴在底部的 tooltip 会被屏幕边缘截断。

在锚定定位中，可以使用 `@position-try` 规则声明降级方案，浏览器会自动检测溢出并切换到最佳位置：

```css
/* 定义备选位置方案：翻转到锚点上方 */
@position-try --flip-top {
  top: auto;
  bottom: anchor(top);
  margin-top: 0;
  margin-bottom: 8px;
}

.tooltip {
  position: fixed;
  position-anchor: --info-btn;
  top: anchor(bottom);
  left: anchor(center);
  transform: translateX(-50%);
  
  /* 当下方空间不足时，自动应用翻转规则 */
  position-try-fallbacks: --flip-top;
}
```

::: insight
原生 HTML 的 `popover` 属性解决了顶层渲染堆叠上下文（Top Layer）与 Esc 键轻量关闭（Light Dismiss），而 CSS Anchor Positioning 解决了空间几何贴合。两者结合，彻底淘汰了过去的庞大浮动层 JS 胶水代码。
:::

## 网格系统

在平面设计中，就像在建筑中一样，成品的核心部分是由一个底层支撑结构支撑的，这个结构通常对观众来说是不可见的，但它却能轻易地成就或毁掉一个设计。

网格无处不在。

![img](https://media-s3-us-east-1.ceros.com/ceros-marketing/images/2016/10/24/ddad31747373bd0169a985ebbd60cad2/poster.jpg?imageOpt=1&fit=bounds&width=510)

![image-20260513085011442](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20260513085011442.png)

![image-20260513085043230](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20260513085043230.png)

![image-20260513085112703](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20260513085112703.png)

**在 Web，网格必须灵活**

![flexible-grid](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/flexible-grid.gif)

### 如何做？

`display: grid` 会在一个元素上启用网格布局。这个元素会变成“网格容器”，它的子元素则称为“网格项”。

`display: grid` 本身并不会产生太多效果，你还需要定义网格模板（Grid template）。可以使用多种属性来完成，例如：

- `grid-template-rows`：定义行
- `grid-template-columns`：定义列
- `grid-template`：同时定义行和列的简写方式
- ……以及更多相关属性

`fr` 单位允许我们以“分数”的方式分配可用空间，而不需要使用百分比进行复杂计算。

`gap` 属性可以设置网格单元之间的间距。

`grid-row` 和 `grid-column` 属性可以用来将元素放置到指定的行或列中。注意，多个元素可以被放在同一个网格单元格中，此时它们会发生重叠。

```css
/* 经典响应式三栏与卡片网格布局 */
.layout-container {
  display: grid;
  /* 左侧固定侧边栏 260px，主内容自适应撑开 1fr，右侧信息栏 280px */
  grid-template-columns: 260px 1fr 280px;
  grid-template-rows: auto 1fr auto;
  gap: 1.5rem;
  min-height: 100vh;
}

/* 响应式自适应卡片网格（无需媒体查询） */
.card-grid {
  display: grid;
  /* 自动填充：每列最小 280px，最大占满 1fr 分数空间 */
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}
```

### 网格系统的核心术语

- **网格槽（Gutter / Gap）**：网格中行与行、列与列之间的空隙。
- **网格轨道（Grid Track）**：相邻两条网格线之间的水平行或垂直列空间。
- **网格线（Grid Line）**：构成网格结构的水平与垂直分割线，编号从 1 开始（支持负索引，-1 表示末尾线）。
- **网格单元格（Grid Cell）**：由四条网格线相交围成的单一最小单元。
- **网格区域（Grid Area）**：由任意数量的矩形网格单元格组成的逻辑区域。

![image-20260513091742408](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20260513091742408.png)

定义命名区域是指定网格布局最优雅的方式。`grid-area` 可以让你把一个元素分配到某个命名区域中。之后，只需要在容器上修改 `grid-template-areas` 模板，就可以完全重排页面布局，甚至适配移动端：

```css
.site-layout {
  display: grid;
  grid-template-areas:
    "header  header"
    "sidebar main"
    "footer  footer";
  grid-template-columns: 240px 1fr;
  grid-template-rows: 64px 1fr 48px;
}

/* 移动端只需重塑 areas 结构 */
@media (max-width: 768px) {
  .site-layout {
    grid-template-areas:
      "header"
      "main"
      "sidebar"
      "footer";
    grid-template-columns: 1fr;
  }
}

.site-header  { grid-area: header; }
.site-sidebar { grid-area: sidebar; }
.site-main    { grid-area: main; }
.site-footer  { grid-area: footer; }
```

::: insight
布局技术的选择应跟随关系：文档流表达顺序，Grid 表达二维轨道，定位表达覆盖或锚定。先确认元素之间的关系，再选 CSS 机制，通常比从坐标和像素开始更稳定。
:::
