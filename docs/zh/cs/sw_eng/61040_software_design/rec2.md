---
title: Recitation 2 HTML 与 CSS 基础
type: lecture
tags: [html, css, web-development, frontend-basics]
status: complete
source: 'https://61040.github.io/fa26/recitations/recitation-2.pdf'
---
# Recitation 2 HTML 与 CSS 基础（HTML & CSS Fundamentals）

官方课件：[Recitation 2](https://61040.github.io/fa26/recitations/recitation-2.pdf) · 配套练习：[Prep 2: HTML & CSS](https://61040.github.io/fa26/preps/html-css/)。本上机实验带练 Web 前端两大骨架技术：语义化 HTML 标记树与基于 Flexbox/Grid 的现代 CSS 盒模型布局。

## TL;DR

- 语义化 HTML 元素（如 `<main>`, `<article>`, `<button>`）为界面提供原生可访问性与无歧义的 DOM 节点树。
- 掌握标准 CSS 盒模型（Content, Padding, Border, Margin）及 `box-sizing: border-box` 的尺寸计算法则。
- 灵活运用 Flexbox（一维流式排列）与 CSS Grid（二维网格系统）构建具备响应式自适应能力的界面。
- 熟练使用浏览器开发者工具（DevTools）检查计算样式、调试盒模型边界与模拟不同屏幕视口。

## 实验核心技能

### 1. 语义化 HTML 规范

- 避免滥用无语义的 `<div>` 和 `<span>`，交互控件必须使用 `<button>` 或 `<a>`。
- 表单元素必须显式绑定 `<label for="id">`，确保辅助设备能够正确识别控件用途。

### 2. 现代 CSS 布局基石

- **盒模型基准**：推荐全局设置 `*, *::before, *::after { box-sizing: border-box; }`，使 padding 和 border 包含在宽高内。
- **Flexbox 轴向控制**：通过 `display: flex`、`flex-direction`、`justify-content` 和 `align-items` 控制一维轴向排版。
- **Grid 网格布局**：使用 `grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))` 实现无媒体查询的流式卡片网格。

::: insight
CSS 的难点从不在于记忆属性，而在于理解浏览器的排版与重绘机制。先用语义化标签建立坚实的 DOM 骨架，再用 Flexbox/Grid 约束流向，远比使用浮动、绝对定位和强制负 margin 拼凑出的界面更加稳固且易于维护。
:::
