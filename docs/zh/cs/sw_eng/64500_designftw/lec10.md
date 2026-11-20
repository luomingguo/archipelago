---
title: '布局'
type: lecture
lecture: 10
tags: [css-layout, positioning, anchor-positioning, css-grid, responsive-design]
status: complete
---
# Lec 10 布局（Layout）

## TL;DR

- 认识CSS元素
- 锚定定位把浮层与触发元素建立显式关系，减少手工计算位置和视口边界的代码。
- Web 网格必须随容器和内容伸缩，CSS Grid 等布局原语比固定画布更能表达二维对齐关系。

## 课程组织

- **CSS的元素分类**
- **定位（Positioning）**
- **一维布局**（Flexbox, Multi-col）
- **二维网格系统（Grid Systems）**

## CSS元素分类

所有通过 CSS 显示的内容都是一个盒子。因此，理解 CSS 盒模型的工作原理是掌握 CSS 的核心基础。无论是使用 `border-radius` 看起来像圆形的盒子，还是仅仅一段纯文本：**需要记住的关键点是，万物皆盒子。从头到尾全都是盒子**！

<iframe src="https://css.land/box-model/" width="100%" height="600px" frameborder="0" allowfullscreen></iframe>

有几个属性对于决定这些盒子的尺寸至关重要：

- [`padding`](https://developer.mozilla.org/en-US/docs/Web/CSS/padding)（内边距）控制元素内容到元素边缘之间的距离。

- [`margin`](https://developer.mozilla.org/en-US/docs/Web/CSS/margin)（外边距）指定元素边缘到其周围其他元素之间的距离，并且可以设为负值，使元素与周围元素靠得**更近**而不是更远。

- [`border`](https://developer.mozilla.org/en-US/docs/Web/CSS/border)（边框）允许你设置可见的边框，它位于 `padding` 的外侧。

**默认情况下，padding 和 border 的宽度是“累加”到 `width` 和 `height` 上的，而不是从中减去**（因此图中内容宽 `500px`，加上左右各 `10px` 的内边距和边框后，实际总宽度变成了 `540px`；**若开启 box-sizing: border-box 则会变为从总宽度中减去**。外轮廓（`outline`）、阴影（`box-shadow`）等修饰效果不会以任何方式影响盒子的占位尺寸。

始终使用充足的内边距（`padding`），否则文字读起来会非常局促难受。正如你在[lec 4 平面设计](./lec4.md)中学到的那样，**水平方向通常需要比垂直方向更多的内边距**。

### 块级元素（Block elements）

- 从上到下排列

- 独占一行（盒子宽度会占满所有可用空间）
- 盒子高度随内部所有（折行后的）内容自动撑开
- 文本在盒子内部正常折行
- 可以自由设置宽度（`width`）、高度（`height`）和外边距（`margin`）

### 行内元素（Inline elements）

- **自左向右**排列
- 与周围文本处于同一行
- 盒子宽度仅包裹其自身内容
- 盒子高度仅为单行行高
- 文本换行时通过盒子**碎裂分段**（折断成多个跨行片段）来实现
- 设置 `width`、`height`（以及垂直方向的 `margin`）均不起作用。

### 行内块级元素（inline-block）

*通俗总结：`inline-block` 就是**“对外表现得像行内元素（能和别的元素并排站在一行），对内表现得像块级元素（有完整的矩形盒子边界、内部文字整体折行、且能自由设置宽高和上下外边距）”

### 替换元素（Replaced elements）

替换元素常见如 `<img>`、`<video>`、`<iframe>`、`<canvas>` 等），其展现内容超出了 CSS 管辖范围的元素”（即浏览器直接把外部资源或原生控件塞进这个盒子里，CSS 只能控制盒子本身的位置、边框和尺寸，管不着盒子里面画了什么。 实际表现：在排版流中与周围内容的关系表现得像一个 `inline-block`（行内块级元素），且其内部内容不受当前文档 CSS 样式的影响。

固有尺寸特性：**只有替换元素才可能拥有**固有尺寸 或 固有宽高比（intrinsic aspect ratio）

> 我们如何脱离文档流（Normal Flow）并将元素叠加在其他元素之上？

定位！

![叠加元素](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20261119163832658.png) 

## 定位（Positioning）

**定位** 允许你将元素移出常规的文档布局流，并使其表现出不同的行为——例如互相叠加在一起，或者无论页面如何滚动都始终固定在同一个位置。

属性控制使用哪种定位方案。它的初始值是 **`static`**（静态定位），对应默认的正常文档流。

> 当应用 **`position: absolute`**（绝对定位）时，你注意到了什么？

要控制元素的偏移位置，我们使用  `top` 、`right`、`bottom`、`left` 属性。这些偏移量是相对于该元素的 *包含块（containing block）*来计算的。默认情况下，这个包含块就是 初始包含块（initial containing block）——一个与视口（viewport）尺寸相同、并锚定在文档顶部的矩形区域。

**“已定位元素（Positioned element）”是指任何 [`position`](https://developer.mozilla.org/en-US/docs/Web/CSS/position) 属性值不等于 `static` 的元素**（即 `position` 为 `relative`、`absolute`、`fixed` 或 `sticky` 的元素），使用偏移属性来控制位置。

`inset` 属性包含了 `top` 、`right`、`bottom`、`left` 属性，常用于让绝对定位元素瞬间铺满整个父容器。就像 `margin` 可以简写四边外边距一样。

### 相对定位

**相对定位**（`position: relative`）的元素仍然占据原本的文档流空间，但可以通过偏移属性**（`top`、`right`、`bottom`、`left`）进行位置移动**（即视觉上偏离原位，但周围其他元素依然按它“没移动前的原位”来排版，**原位置会留出一个空白占位**）

### 绝对定位

**绝对定位**（`position: absolute`）会将元素完全移出正常文档流，并将其置于其他所有内容之上（即原来的位置不再保留空白，**后面的元素会直接顶上来填补空缺**，而该元素自身会悬浮在页面上层，相对于最近的“已定位祖先元素”进行定位）。

任何已定位元素都会成为其所有已定位后代元素的 containing block。 这就是偏移属性 `top`、`right`、`bottom`、`left` 计算距离的基准参照物——也就是**前端常说的“子绝父相”原理**：想让子元素相对于某个父容器绝对定位，只需给父容器加上 `position: relative` 使其成为已定位元素即可。

### 固定定位

**固定定位（`position: fixed`）允许我们将元素固定在屏幕的同一位置，无论页面如何滚动都保持不变**（即相对于浏览器视口定位，常用于固定在顶部的导航栏、右下角的“回到顶部”按钮或全局

#### 实战： newsletter弹窗居中

```html
<section class="newsletter">
	<form>
		<label>
			Sign up for our <del>evil</del> <ins>amazing</ins> newsletter:
			<input type="email">
		</label>

		<footer>
			<button class="primary">Yes, yes, yes!</button>
			<button>No, I'm dumb</button>
		</footer>
	</form>
</section>
<p>Cat ipsum dolor sit amet, bite the neighbor's bratty kid love you, then bite you or need to check on human, have not seen in an hour might be dead oh look, human is alive, hiss at human, feed me. Run outside as soon as door open.</p>
<p>Rub against owner because nose is wet dream about hunting birds climb a tree, wait for a fireman jump to fireman then scratch his face. You are a captive audience while sitting on the toilet, pet me i vomit in the bed in the middle of the night for sleep all day whilst slave is at work, play all night whilst slave is sleeping stretch, yet find a way to fit in tiny box. </p>

```

尝试一：

```css
.newsletter {
	position: absolute;
	top: 50%;
	left: 50%;
}
```

结果：弹窗整体偏右下。 原因是，此语义是“把左上角放到正中间”；，而不是弹窗的中心放到正中间

![第一次尝试结果](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20261119170328730.png)

尝试2：弹窗中间放在屏幕中心

```css
.newsletter {
	position: absolute;
	top: 50%;
	left: 50%;
  transform: translate(-50%, -50%); /*让元素沿着水平（X 轴）向左移动“自身宽度的一半”，同时沿着垂直（Y 轴）向上移动“自身高度的一半”。*/
}
```

结果，是确实在中心。但是，绝对定位的参照物是初始包含块，所以当你往下滚动看文章时，这个订阅弹窗会跟着页面一起往上滚走，无法一直停留在眼前。

尝试3：固定悬浮窗

```css
.newsletter {
	position: fixed;
	top: 50%;
	left: 50%;
  transform: translate(-50%, -50%); /*让元素沿着水平（X 轴）向左移动“自身宽度的一半”，同时沿着垂直（Y 轴）向上移动“自身高度的一半”。*/
}
```

结果： 弹窗无论怎么滚动页面都死死钉在屏幕正中央。 它的定位基准永远是浏览器视口（viewport）本身，不会受页面滚动影响

### 粘性定位

**粘性定位（`position: sticky`）**：它的行为就像 **`relative`**（跟着页面正常滚动）。当元素即将滚出可视区域（用户向下滚动了页面），但它的 containing block 仍在视野内时它的行为就像 **`fixed`**（吸顶固定在屏幕边缘不动，比如这里的表头 `thead` 在浏览长表格时一直吸在顶部）。当它的父容器（整个表格）也完全滚出可视区域时，它又变回 `relative`（跟着父容器一起被带走，不会一直霸占屏幕）。

- 注意：`position: sticky` 单独写没有任何效果，你必须同时指定偏移量！
- **水平滚动时会发生什么？**（同理，如果设置了 `left: 0;` 或 `right: 0;`，在横向滚动宽表格时，首列或末列也会吸在左右边缘）。

### 绝对定位（勿用）

**绝对定位（`position: absolute `**： **硬算像素坐标**来排布九宫格猫咪照片的反面教材示例。不要为了逃避真正搞懂页面布局而滥用绝对定位（`position: absolute`）：它以后*一定会*反过来坑你一把！

### 锚定定位

CSS的锚定定位（*anchor positioning*），——即如何让一个弹窗、提示框（Tooltip）或下拉菜单直接“吸附”在页面上任意指定按钮或元素的旁边，而不需要它们之间必须是父子嵌套关系。

我们经常需要相对于页面上的其他元素来定位 UI 组件。例如：工具提示（Tooltips）、下拉菜单（dropdowns）、气泡浮窗（popovers）和右键上下文菜单（context menus）。过去，我们只能用 JavaScript 加上手动计算坐标尺寸来“模拟”实现这种效果。从今年起，纯 CSS 已经可以直接原生实现这一功能了！

锚点定位是一项全新的 CSS 特性（2026 年初， 全浏览器正式普及 / Baseline）：

- 它允许一个元素直接相对于另一个元素来定位自己。

- 无需再手动测量元素坐标。

- 无需再监听窗口大小变化事件。

锚定定位将“触发者”与“依附者”在视觉空间中解耦，其核心工作流分为三步：

1. **注册锚点（Anchor Registration）**：通过 `anchor-name` 属性为宿主元素分配一个 CSS 虚线标识符（Dashed Ident，以 `--` 开头，如 `--info-btn`）。该标识符遵循类似 CSS 自定义属性的作用域规则；
2. **声明依附关联（Target Binding）**：在浮动元素上设置 `position: fixed` 或 `position: absolute`，并通过 `position-anchor: --info-btn` 显式指定依附的目标；
3. **空间几何吸附（Coordinate Alignment）**：在定位偏移属性中调用 `anchor()` 函数。`anchor()` 接受锚点边缘作为参数（如 `top`, `bottom`, `left`, `right`, `center`），由浏览器自动计算偏移量。

```html
<!-- 1. 触发锚点按钮 -->
<button class="anchor-btn">Hover me</button>

<!-- 2. 悬浮提示框 -->
<div class="tooltip" role="tooltip">Anchored tooltip</div>
```

```css
/* 1. 按钮起个锚点名字叫 --demo-anchor（注意锚点名必须像 CSS 变量一样以 -- 开头） */
.anchor-btn {
  anchor-name: --info-btn;
}

/* 2. 让提示框绑定到 --info-anchor，并把提示框的顶边（top）对齐按钮的底边（anchor(bottom)），提示框的左边（left）对齐按钮的右边（anchor(right)），形成右侧预览区中“右下角对角线紧贴”的效果 */
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

**锚点元素（Anchor element）通过 `anchor-name` 声明自身**（即“被别人盯住当参照物”的那个元素，比如按钮）。**被锚定元素（Anchored element）通过 `position-anchor` 引用该锚点**（即“跟着锚点走、吸附在锚点旁边”的那个元素，比如提示框或下拉菜单）。

**锚点定位（Anchor positioning）允许元素以声明式的方式相对于其他元素进行定位**（即只需通过纯 CSS 属性声明“对齐到哪个元素的哪条边”，无需再依赖 JavaScript 手动计算坐标）。

锚点定位支持回退（备选位置）策略。

- 先尝试放在下方
- 如果下方放不下，再尝试放在上方
- 如果上下都放不下，再尝试放在侧边

这与知名定位库 popper.js（现为 Floating UI）所做的自动翻转防遮挡逻辑类似。但它是声明式的，且由浏览器原生支持（无需任何 JS 代码）。

## Floats

这段了解即可。

CSS 中的 [`float`](https://developer.mozilla.org/en-US/docs/Web/CSS/float) 属性，原本设计用于实现杂志排版中的“文字环绕图片”效果，早期在 Flexbox 和 Grid 出现之前也曾被广泛用来做多栏网页布局。

**[`float`](https://developer.mozilla.org/en-US/docs/Web/CSS/float)（浮动）属性会将元素移出正常文档流，并将其贴靠在父容器的左侧（或右侧）。** 在正常布局流中排在浮动元素下方的任何内容，现在都会环绕着它排列，填满其右侧（或左侧）的空间，最高可一直向上延伸到浮动元素的顶部。

![设置了float效果但没有外边距](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20261119234907913.png)

```css
img {
	float: left;
	margin-right: 1em;
}

img:nth-of-type(even) {
	float: right;
	margin-right: 0;
	margin-left: 1em;
}
```

虽然我们可以给浮动元素添加外边距（`margin`）来把文字推开，但我们不能给文字添加外边距来让它远离浮动元素。

**这是因为浮动元素已经脱离了正常文档流，后续段落元素的盒子模型（boxes）实际上是直接从浮动元素“背后”穿过去的——如果我们给段落加上背景色，就能清楚地看到这一点。**

![设置了float效果但没有外边距](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20261119235127780.png)

**我们该如何让这个排版在视觉上更有趣，让图片一左一右交替浮动呢？**（提示：后面会演示用。

![Wireframe layout comparison](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/layout-wireframe-comparison.jpg)

> 虽然 CSS 技术上很容易做出“左图右文、右图左文”交替的时髦排版，但眼动实验证明，如果图片只是纯装饰性的，这种交错排版反而会变成视线“障碍物”，不如把所有图片对齐放在同一侧（右图的 *Aligned Layout*）更好读。

### 浮动带来的问题

当所有设置了浮动的图片交错挤在一起时，会发生什么？（多张不同高度的浮动图片会像“楼梯台阶”一样互相卡住、错位堆叠，导致布局彻底乱套。）

当文字内容不够多，不足以填满图片整个垂直侧边时，会发生什么？（如果最后一段文字很短，排在后面的 `<footer>` 页脚也会被吸上去、挤到图片旁边，而不是乖乖待在页面最底部。）

我们能把最后一张图片往上移动吗？（提示：后面会演示在 `img:last-of-type` 里用负的 `margin-top` 硬拽，但这只是非常脆弱的权宜之计。）

给页脚加上 `clear: both`（清除两侧浮动）虽然能把页脚推回图片下方，但也并不理想（试试给它加一点 `margin-top` 上外边距看看……你会发现，因为上方浮动元素高度的影响，`margin-top` 常常会“失灵”或表现得非常反直觉）。

在2015年之前都是这么干的；

## 一维设计——Flexbox、Multicol

（待补充）

## 二维设计——Grid

### 网格布局示意

在平面设计中，就像在建筑中一样，成品的核心部分是由一个底层支撑结构支撑的，这个结构通常对观众来说是不可见的，但它却能轻易地成就或毁掉一个设计。

![设计原则：网格系统I](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20261120001429232.png)

![设计原则：网格系统II](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20260513085011442.png)

![设计原则：网格系统III](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20260513085043230.png)

![设计原则：IV网格系统](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20260513085112703.png)

**在 Web，网格必须灵活**

![flexible-grid](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/flexible-grid.gif)

### 如何做？

`display: grid` 会在一个元素上启用网格布局。该元素会成为网格容器（Grid Container），而它的直接子元素则被称为网格项（Grid Items）。

单独写一个 `display: grid` 不会产生太明显的变化，你还需要定义网格模板（Grid template）有多个属性可以用来定义网格模板，例如：

- `grid-template-rows`：定义网格的行高与数量
- `grid-template-columns`：定义网格的列宽与数量
- `grid-template`：行、列及区域模板的简写属性
- ……以及更多相关属性

`1fr` 单位（分数单位 / fraction）允许我们按比例分配剩余可用空间，而无需自己去算复杂的百分比数学题。

`gap` 属性可以设置网格单元之间的间距。

`grid-row` 和 `grid-column` 属性允许我们将网格项放置到指定的行和/或列上。注意：多个网格项*可以*被放置在同一个单元格中，此时它们将会相互重叠！

![圣杯式三栏网格布局](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20261120003310122.png)

```css
/* 将 body 设为网格容器（2列 × 3行） */
body {
	display: grid;                      /* 开启 Grid 网格布局 */
	grid-template-columns: 10em 1fr;    /* 定义 2 列：第 1 列固定宽 10em，第 2 列占满剩余全部宽度（1fr） */
	grid-template-rows: auto 1fr 3em;   /* 定义 3 行：第 1 行高度随内容自适应（auto），第 2 行占满剩余高度（1fr），第 3 行固定高 3em */
	background: hsl(220 10% 85%);       /* 页面背景设为浅灰蓝色 */
}

/* 页眉区域 */
header {
	grid-column: 1 / span 2;            /* 从第 1 列网格线开始，向右跨越 2 列（即占满整行顶部） */
}

/* 侧边栏区域（黄色） */
aside {
	background: gold;                   /* 背景色设为金黄色 */
	grid-row-end: span 2;               /* 向下跨越 2 行（让侧边栏从第 2 行一直延伸到底部，把页脚挤到右下角） */
}

/* 主内容区域（白色） */
main {
	background: white;                  /* 背景色设为白色（自动填入第 2 行第 2 列） */
}

/* 页脚区域（绿色） */
footer {
	background: green;                  /* 背景色设为绿色（因为左下角被 aside 占了，所以它自动排到第 3 行第 2 列） */
}
```

### 网格系统的核心术语

- **网格单元格（Grid Cell）**：CSS 网格中的最小单个基本单元。
- **网格线（Grid Line）**：划分网格并将列与行分隔开的垂直线和水平线，编号从 1 开始（支持负索引，-1 表示末尾线）。
- **网格区域（Grid area）**：由任意数量的矩形网格单元格组成的逻辑区域。注意网格区域**必须是矩形**
- **网格轨道（Grid Track）**：就是一整行（Row）**或**一整列（Column）的总称。
- **网格槽（Gutter / Gap）**：网格中行与行、列与列之间的空隙。
- 网格容器： 有`display: grid`的元素

![CSS Grid 网格线与网格区域示意](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20260513091742408.png)

定义命名区域是指定网格布局最优雅的方式。`grid-area` 可以让你把一个元素分配到某个命名区域中。之后，只需要在容器上修改 `grid-template-areas` 模板，就可以完全重排页面布局，甚至适配移动端

![猫咪照片拼贴画](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20261120011121162.png)

```css
/* 将 body 设为 4×4 的固定正方形网格容器 */
body {
	display: grid;                        
	grid-template-columns: repeat(4, 200px);
	grid-template-rows: repeat(4, 200px);  
	grid-auto-flow: dense;       /* 开启“密集填充”模式：如果前面因为放不下大图留下了空洞，允许后面的小图自动“回头”把空洞填满 */
}

/* 设置所有图片的填充方式 */
img {
	width: 100%;        /* 让图片宽度填满它所在的网格单元格（否则图片会按原图像素大小撑破网格） */
	height: 100%;       /* 让图片高度填满它所在的网格单元格 */
	object-fit: cover;  /* 保持图片原始比例裁剪缩放，使其完全覆盖单元格而不变形拉伸 */
}

/* 选中图片路径（src）中包含数字 "3" 或 "5" 的图片（即第 3 张和第 5 张图） */
img[src*="3"],
img[src*="5"] {
	grid-column-end: span 2; /* 水平方向向右跨越 2 列（宽变成 400px） */
	grid-row-end: span 2;    /* 垂直方向向下跨越 2 行（高变成 400px，最终变成 2×2 的大图） */
}
```

![关于布局的总结](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20261120011852101.png)

知名 CSS 专家 Jen Simmons 的经典布局对比实验（**[Teaser cards in various layouts](https://labs.jensimmons.com/2017/01-009.html)**），用来对比 12 种不同 CSS 布局方式实现“卡片列表”的效果差异
