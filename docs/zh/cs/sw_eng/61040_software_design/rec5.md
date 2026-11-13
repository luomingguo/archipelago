---
title: Recitation 5 响应式前端与 Vue 单文件组件
type: lecture
tags: [vue, reactive-programming, frontend, component-design]
status: complete
source: 'https://61040.github.io/fa26/preps/vue/'
---
# Recitation 5 响应式前端与 Vue 单文件组件（Vue SFC & Reactive Programming）

配套练习：[Prep 5: Vue](https://61040.github.io/fa26/preps/vue/)。本实验探讨响应式编程的核心机制，带练 Vue 3 组合式 API（Composition API）与单文件组件（Single File Components），实现状态驱动的高内聚视图。

## TL;DR

- 响应式前端的本质是“视图是状态的纯函数”（$View = f(State)$），杜绝手工操作 DOM 带来的分支复杂性。
- Vue 3 组合式 API 通过 `ref`（基本类型）与 `reactive`（对象）建立响应式依赖追踪。
- 单文件组件（SFC）将模板结构（`<template>`）、交互逻辑（`<script setup>`）与局部样式（`<style scoped>`）内聚在单一 `.vue` 文件中。
- 配合后端自动生成的强类型客户端（Typed Client），前端调用 API 获得端到端类型提示与编译期检查。

## 实验核心技能

### 1. 响应式状态与派生计算

```vue
<script setup lang="ts">
import { ref, computed } from "vue";

const count = ref(0);
const isMax = computed(() => count.value >= 10);

function increment() {
  if (!isMax.value) count.value++;
}
</script>

<template>
  <div class="counter">
    <p>当前票数：{{ count }}</p>
    <button :disabled="isMax" @click="increment">赞同</button>
  </div>
</template>
```

### 2. 组件间通讯与边界

- **父传子（Props）**：通过 `defineProps<{ item: string }>()` 传递只读数据。
- **子传父（Events）**：通过 `defineEmits<['update']>()` 向父级发出事件，避免子组件私自越权修改外部全局状态。

::: insight
前端框架的发展历程证明：手工直接操纵 DOM 是一切 UI 状态 Bug 的温床。响应式框架让开发者只需关注“状态当前是什么”以及“动作如何改变状态”，界面渲染与差异化更新完全交给运行时自动完成。
:::
