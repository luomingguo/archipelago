---
title: Recitation 9 GitHub 团队高级协作流与冲突解决
type: lecture
tags: [git, github, collaboration, code-review]
status: complete
source: 'https://61040.github.io/fa26/preps/github/'
---
# Recitation 9 GitHub 团队高级协作流与冲突解决（GitHub Team Collaboration）

配套练习：[Prep 9: GitHub](https://61040.github.io/fa26/preps/github/)。本实验直接服务于 11 月正式启动的 3~4 人期末大团队项目（Final Team Project），掌握基于分支策略、Pull Request 代码审查与 Git 三方合并冲突排解的专业协作规范。

## TL;DR

- 团队协作采用特性分支工作流（Feature Branch Workflow）：主分支（main）保持稳定可部署，新功能在独立分支开发。
- Pull Request（PR）是团队知识共享与架构审查的核心阵地，包含清晰的改动摘要、测试截图与逐行代码反馈。
- Git 合并冲突产生于多人同时修改同一文件的相邻上下文，必须理清“本地基线、远程最新、目标变更”三方逻辑并显式解决。
- 团队项目严格遵循小步高频提交，杜绝交付前夕的大规模代码空投（Big Bang Integration）。

## 实验核心技能

### 1. 标准特性分支开发流水线

```bash
# 1. 切换并拉取最新 main
git checkout main
git pull origin main

# 2. 开辟个人特性分支
git checkout -b feat/upvoting-concept

# 3. 本地小步提交
git commit -m "feat(upvoting): add SSF state declaration and schema"

# 4. 推送并创建 PR
git push -u origin feat/upvoting-concept
```

### 2. 三方合并冲突（Merge Conflict）排解

当远程 main 已有同事提交，本地合并或 rebase 触发冲突标记：

```text
<<<<<<< HEAD (Current Change - 本地修改)
const port = process.env.PORT ?? 3000;
=======
const port = process.env.BACKEND_PORT ?? 8080;
>>>>>>> main (Incoming Change - 远程修改)
```

**排解步骤**：
1. 召集相关改动同事沟通，确认业务意图。
2. 保留正确代码并彻底移除 `<<<<<<<`, `=======`, `>>>>>>>` 冲突标记。
3. 运行本地自动化测试与 linter 验证语法。
4. `git add <file>` 并执行 `git commit` 完成合并记录。

::: insight
版本控制不是简单的云端网盘备份，而是一个团队在时间维度上共同演进的思维契约树。干净的提交历史、明确的分支命名和审慎的 PR 审查，是保障复杂软件系统在多人并行开发下不至于分崩离析的基石。
:::
