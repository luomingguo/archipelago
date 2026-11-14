---
title: 'CSS 盒模型与层叠上下文'
type: concept
tags: [css-box-model, stacking-context, z-index, css-layout, rendering-pipeline]
status: complete
---
# CSS 盒模型与层叠上下文

## 问题情境

在前端工程中，样式开发的两大经典噩梦往往源于对浏览器基础渲染几何模型的误解：
1. **尺寸撑破容器**：一个原本设置了 `width: 50%` 的卡片，在添加了 `padding: 16px` 和 `border: 1px solid` 之后，两个卡片并排摆放却莫名其妙折行掉落，容器水平滚动条被无情撑爆；
2. **`z-index: 99999` 依然被遮挡**：一个弹窗或下拉菜单设置了天文数字的 `z-index: 99999`，却依然被相邻兄弟节点下一个只有 `z-index: 1` 的侧边栏死死盖在身下。

这两个看似玄学的问题，在底层分别由 W3C 规范中的**盒模型（Box Model）**几何算法与**层叠上下文（Stacking Context）**三维渲染树严格判定。

## 概念界定

::: definition [CSS 盒模型（Box Model）与层叠上下文（Stacking Context）]
- **CSS 盒模型（Box Model）**：浏览器渲染引擎在二维平面上为每个元素生成的矩形盒子。由内向外依次由四个同心嵌套区域构成：**内容区（Content）**、**内边距区（Padding）**、**边框区（Border）**与**外边距区（Margin）**；
- **层叠上下文（Stacking Context）**：浏览器渲染引擎在垂直于屏幕的假想三维 Z 轴空间中建立的一套自包含的分层绘制环境。处于某个层叠上下文内部的子元素，其在 Z 轴上的相对堆叠次序仅在该上下文内部生效，**绝不可能突破其父级层叠上下文在全局中的层级地位**。
:::

盒模型主导了二维 X/Y 轴的物理尺寸与排布，层叠上下文主导了三维 Z 轴的遮挡与穿透。

## 解释与依据

### 1. 盒模型算法：`content-box` vs `border-box`

W3C 规范提供了两种互斥的尺寸计算模型：

```text
+-------------------------------------------------------+
|  Margin (外边距)                                       |
|   +-----------------------------------------------+   |
|   |  Border (边框)                                |   |
|   |   +---------------------------------------+   |   |
|   |   |  Padding (内边距)                      |   |   |
|   |   |   +-------------------------------+   |   |   |
|   |   |   |  Content (内容区: width/height)|   |   |   |
|   |   |   +-------------------------------+   |   |   |
|   |   +---------------------------------------+   |   |
|   +-----------------------------------------------+   |
+-------------------------------------------------------+
```

1. **标准盒模型（`box-sizing: content-box`，默认值）**：
   开发者声明的 `width` 和 `height` **仅仅指定内容区（Content）的尺寸**。
   盒子的屏幕总占据宽度为：
   $$\text{Total Width} = \text{width} + \text{padding-left} + \text{padding-right} + \text{border-left} + \text{border-right}$$
   这意味着只要调整内边距或边框，盒子的总宽度就会不断变大，极易破坏网格分栏。
2. **边框盒模型（`box-sizing: border-box`，现代工业标准）**：
   开发者声明的 `width` 和 `height` **包含了 Content + Padding + Border 的总和**。
   内容区宽度自动被内边距与边框挤压自适应收缩：
   $$\text{Content Width} = \text{width} - (\text{padding} + \text{border})$$
   这确保了只要指定了 `width: 50%`，无论后续如何微调内边距和边框，盒子在容器中的尺寸永远纹丝不动。

### 2. 外边距折叠（Margin Collapsing）的三大定律

在常规文档流（Normal Flow）中，垂直方向上相邻的块级外边距会合并为一个单一外边距，遵循以下法则：
- **符号原则**：两个均为正数时取最大值；一正一负时取代数和（$M = M_{\text{pos}} + M_{\text{neg}}$）；均为负数时取绝对值最大的负值；
- **兄弟折叠**：前一个元素的 `margin-bottom` 与后一个元素的 `margin-top` 必然折叠；
- **父子穿透折叠**：如果父元素没有 `border-top`、没有 `padding-top` 且没有建立 BFC（块级格式化上下文），子元素的 `margin-top` 会直接“击穿”父元素，导致父元素整体下移；
- **解法契约**：建立 BFC（如 `overflow: clip` / `display: flow-root`）或使用现代 Flex/Grid 的 `gap` 属性替代垂直 margin，从根源规避折叠。

### 3. 层叠上下文（Stacking Context）的生成与 7 层渲染层级

在同一个层叠上下文中，浏览器严格按照以下 7 个物理层级从后向前绘制（后绘制者覆盖先绘制者）：

```text
[视线远端 / 底层]
  1. 层叠上下文的根背景与根边框
  2. 负值 z-index (z-index < 0)
  3. 常规块级流式盒子 (Non-positioned, Block boxes)
  4. 浮动元素 (Non-positioned, Floats)
  5. 行内级盒子与文本 (Inline boxes)
  6. 具有 z-index: 0 或 z-index: auto 的定位元素
  7. 正值 z-index (z-index > 0)
[视线近端 / 顶层]
```

**触发新层叠上下文的关键属性**：
- 根元素 `<html>`（默认根上下文）；
- `position` 为 `absolute` / `relative` 且 `z-index` 不为 `auto`；
- `position: fixed` 或 `position: sticky`（在大多数现代浏览器中）；
- `opacity` 小于 `1`；
- `transform`、`filter`、`backdrop-filter`、`perspective`、`clip-path` 不为 `none`；
- 显式声明 `isolation: isolate`。

## 边界与辨析

### 1. `z-index: 99999` 失效的层级囚徒困境

假设页面上有两个并列的父容器：
- 父容器 A 设置了 `position: relative; z-index: 1;`；
- 父容器 B 设置了 `position: relative; z-index: 2;`。
即使 A 的子元素配置了 `z-index: 99999`，而 B 的子元素只配置了 `z-index: 0`：
- **物理事实**：由于 A 与 B 分属同级的两个独立层叠上下文，A 的整体层叠权重（1）低于 B 的整体层叠权重（2）；
- **结论**：A 内部的所有子元素无论堆叠多高，都被整体压在 B 的下方，永远无法突破其父容器的层叠天花板！

### 2. 局部隔离武器：`isolation: isolate`

传统上，为了防止内部组件的 `z-index` 污染外部页面或被外部层级干扰，工程师往往被迫滥用 `position: relative; z-index: 0;`。
- 现代 CSS 提供了专属的声明式隔离属性：`isolation: isolate`；
- 它无需指定脱离文档流的定位属性，直接为当前组件创立一个全新、自包含的独立层叠上下文，保护内部弹层或气泡安全运转。

::: insight
现代 Web 工程的黄金重置规则：始终在 CSS 开头写入全局重置规则：
```css
*, *::before, *::after {
  box-sizing: border-box;
}
```
这一行代码彻底规避了百分比分栏被内边距挤爆的二维历史遗留包袱。
:::

## 提取与迁移

- **在现代 Design System 与组件库中**：
  严禁在代码中随意硬编码诸如 `z-index: 999999` 的魔法数字；必须建立全局 Z-Index 语义阶梯（Tokenized Scale）：
  ```css
  :root {
    --z-hide: -1;
    --z-base: 0;
    --z-dropdown: 1000;
    --z-sticky: 1100;
    --z-modal-backdrop: 1200;
    --z-modal: 1300;
    --z-popover: 1400;
    --z-toast: 1500;
  }
  ```
- **在原生 HTML5 `<dialog>` 与 Popover API 中**：
  现代规范引入了浏览器顶层渲染上下文（Top Layer），彻底脱离常规 DOM 树的层叠上下文约束，置于所有页面的绝对最顶层。

## 关联与来源

- **课程讲义关联**：
  - [Lec 6 CSS 的基本概念 I](../lec6.md)：盒模型、外边距折叠与 Normal Flow；
  - [Lec 8 CSS 的基本概念 II](../lec8.md)：层叠上下文、`z-index` 与特异度。
- **经典规范**：
  - W3C CSS Box Model Module Level 3.
  - W3C CSS Positioned Layout Module Level 3.
  - MDN Web Docs: "The Stacking Context."

## TL;DR

- 边框盒模型（`box-sizing: border-box`）将内边距与边框包裹在指定的宽高之内，消除了传统标准盒模型因内边距撑破网格的缺陷。
- 外边距折叠仅发生在常规流的垂直方向，可通过创建 BFC 或使用 Flex/Grid `gap` 规避。
- 层叠上下文决定了元素在 Z 轴上的三维遮挡；子元素的 `z-index` 无法逾越父级层叠上下文的全局权重，组件隔离应优先使用 `isolation: isolate`。
