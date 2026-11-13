---
title: Recitation 1 Markdown 与作品集搭建
type: lecture
tags: [markdown, github, documentation, portfolio]
status: complete
source: 'https://61040.github.io/fa26/recitations/recitation-1.pdf'
---
# Recitation 1 Markdown 与作品集搭建（Markdown & Portfolio Setup）

官方课件：[Recitation 1](https://61040.github.io/fa26/recitations/recitation-1.pdf) · 配套练习：[Prep 1: Markdown](https://61040.github.io/fa26/preps/markdown/)。本上机实验课指导学生建立个人 GitHub 作业作品集仓库，熟练掌握 Markdown 严谨排版与 Git commit hash 提交流水线。

## TL;DR

- Markdown 以纯文本实现轻量化结构排版，天然适配 Git 版本控制与多平台静态网站生成。
- 个人作品集仓库 README 是课程交付总入口，必须维护清晰规范的相对路径与文档索引。
- 课程作业提交严格依托提交哈希（commit hash），提交前必须在本地与 GitHub 预览校验格式与相对链接。
- 严禁在 Markdown 中硬编码本地绝对路径，媒体资源须通过统一托管路径或规范图床维护。

## 实验核心技能

### 1. 结构化排版规范

- **标题阶梯**：每个页面仅允许一个主 `# H1`，章节使用 `## H2`，子节使用 `### H3`，严禁跳级使用标题。
- **列表与表格**：有序列表表达严密步骤，无序列表表达并列属性，表格必须带表头与对齐分隔线。
- **代码与公式围栏**：代码块必须声明语言标识符（如 `ts`, `json`, `bash`）；数学公式统一使用 LaTeX 语法。

### 2. Git 作品集与提交契约

1. 创建个人作业公开/私有仓库，克隆至本地。
2. 编写 `README.md`，构建个人主页与作业导航。
3. 每次作业完成时执行提交：`git commit -m "feat: complete assignment"`。
4. 推送至远程：`git push origin main`。
5. 复制目标提交哈希（形如 `8a3f9c1...`）填入官方 Google 表单完成提交。

::: insight
作品集仓库不仅是一门课的作业归档，更是工程师个人设计心智与交付规范的长期资产。写清晰的提交信息、保持整洁的相对路径链接、建立易读的 README 索引，这些看似基础的习惯正是专业工程素养与随意拼凑的核心分水岭。
:::
