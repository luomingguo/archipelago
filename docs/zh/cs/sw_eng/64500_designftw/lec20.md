---
title: 'Web API 与组件架构'
type: lecture
lecture: 20
tags: [http, web-api, ajax, rest, web-components, vue-components]
status: complete
source: https://designftw.mit.edu/lectures/
---

# Lec 20 Web API 与现代组件架构（Web APIs & Component-Based Architecture）

## TL;DR

- **HTTP 协议与方法语义**：HTTP 通过请求动词、状态码、头部和报文体构筑客户端与服务端的通信管道，安全方法（Safe）与幂等方法（Idempotent）的语义约束决定了接口调用的重试与缓存策略；
- **AJAX 与 RESTful 架构**：AJAX 彻底终结了全页刷新的交互历史，REST 架构通过将瞬态会话状态下沉至客户端，实现了无状态、高扩展且面向资源的服务解耦；
- **基于 Token 的安全授权机制**：客户端通过初始认证获取经数字签名的不可伪造令牌（如 JWT / Bearer Token），并在后续无状态请求中通过 Authorization 头部携带，彻底消除服务端的会话负担；
- **组件化架构演进**：界面设计从早期宏观的“关注点分离（HTML/CSS/JS 拆分）”演变为“按独立自治组件分离”，配合 Web Components 原生标准与现代响应式框架，将复杂 UI 封装为声明式自闭合构件。

---

## 1. HTTP 协议基础与交互语义

自 1990 年代万维网诞生以来，浏览器与后端服务器之间的每一次数据往来均依托超文本传输协议（Hypertext Transfer Protocol, HTTP）。

与最初 Tim Berners-Lee 定义的极简规范相比，现代 HTTP 确立了语义严密的请求方法集合：

- **`GET`**：向服务器请求获取指定资源（纯读取操作）；
- **`POST`**：向服务器提交数据，通常用于创建全新的下级资源；
- **`PUT`**：使用请求体中的完整内容，全新替换目标 URL 处的已有资源；
- **`PATCH`**：对已存在资源的某些局部字段应用差量修改；
- **`DELETE`**：指示服务器永久移除目标 URL 处的资源；
- **`OPTIONS`**：向服务器询问该资源所支持的通信选项与跨域权限（CORS 预检）。

### 1.1 请求与响应报文解剖

```mermaid
flowchart LR
    subgraph Request ["HTTP 请求报文 (Request)"]
        R1["方法与路径: GET /api/v1/users HTTP/1.1"]
        R2["请求头: Host, Accept, Authorization, Cookie"]
        R3["请求体 (Body): JSON 序列化数据 (POST/PUT)"]
        R1 --> R2 --> R3
    end
    
    subgraph Response ["HTTP 响应报文 (Response)"]
        S1["状态行: HTTP/1.1 200 OK / 404 Not Found"]
        S2["响应头: Content-Type, Set-Cookie, Cache-Control"]
        S3["响应体 (Body): HTML / JSON / 图像二进制数据"]
        S1 --> S2 --> S3
    end
    
    Request --> |"网络传输 (TCP/TLS)"| Response
```

- **请求包含**：
  - **URL / Path**：目标资源的绝对路径与查询参数（Query Parameters）；
  - **Body**：`POST`, `PUT`, `PATCH` 携带的具体业务数据载荷；
  - **Headers（头部）**：`Referer`（来源页面）、`Accept`（客户端声明能接收的 MIME 类型，如 `application/json`）、`Cookie` 与认证凭据。
- **响应包含**：
  - **Status Code（状态码）**：`2xx` 成功、`3xx` 重定向、`4xx` 客户端错误（如 401 未认证、403 无权限、404 不存在）、`5xx` 服务端崩溃；
  - **Headers**：`Content-Type`（响应载荷格式）、`Set-Cookie`（指令客户端保存会话）、`Location`（指示客户端重定向的目标 URL）。

### 1.2 幂等性（Idempotence）与安全性（Safety）

理解 HTTP 方法的物理副作用，是设计稳健 API 与处理网络重试的关键：

| 语义分类 | 严格学术定义 | 包含的 HTTP 方法 | 网络工程影响 |
| :--- | :--- | :--- | :--- |
| **安全方法（Safe）** | 操作**绝不引起服务器任何状态改变**，纯粹用于只读检索。 | `GET`, `HEAD`, `OPTIONS` | 可以被代理服务器、CDN 和浏览器无条件安全缓存。 |
| **幂等方法（Idempotent）** | **执行一次与连续执行 $N$ 次产生的服务端副作用完全相同**。 | `GET`, `PUT`, `DELETE` | 当遇到网络超时或丢包时，**客户端可以自动安全重试**，绝不会造成数据多次累加！ |
| **非安全且非幂等** | 每次调用都会在服务端产生新的、累积的状态变化。 | `POST`, `PATCH`（取决于具体实现） | 遇到网络中断时**绝不能盲目自动重试**，否则可能导致用户银行卡被重复扣款两次。 |

---

## 2. AJAX 与异步 Web API 的诞生

在 1990 年代，Web 应用几乎完全运行在服务器端。当用户点击一个按钮时，浏览器必须提交一个完整的 `<form>` 表单，整张网页白屏数秒，等待后端重新渲染整张 HTML 页面并全量回传刷新。

### 2.1 局部更新的洞察：AJAX 革命

工程师们很快发现了一个核心痛点：用户的大多数交互往往**仅仅修改了屏幕上极其微小的一块局部区域**（例如点赞数增加 1、列表动态追加一条评论），为什么还要每次都强迫整张页面白屏重载？

![AJAX 异步局部更新与传统全页同步刷新对比](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20251017181015263.png)

2005 年，**AJAX（Asynchronous JavaScript and XML）** 范式横空出世：
1. JavaScript 在后台通过 `XMLHttpRequest`（现代统一采用 `fetch()`）发起异步网络请求；
2. 浏览器主线程绝不阻塞，用户可以继续流畅滚动浏览页面；
3. 后端返回精简的结构化数据（早期使用 XML，如今全面采用 **JSON**）；
4. JavaScript 接收到 JSON 数据后，仅仅使用 DOM API 精准修改相关 DOM 节点。

### 2.2 API 调用的分层封装（Encapsulation）

在现代软件工程中，业务代码绝对不应该充斥着底层的网络请求拼装逻辑。工业级架构采用清晰的分层封装：

```mermaid
flowchart TD
    App["业务层 UI 组件 (如 ProfileCard.vue)"] --> |"直接调用业务方法 api.getUserProfile(id)"| ClientLib["客户端 API 封装库 (API Client)"]
    ClientLib --> |"接收参数，组织请求头与 JSON 载荷"| Fetch["浏览器 Fetch / HTTP 协议栈"]
    Fetch --> |"TCP/IP 字节流传输"| Network["互联网路由"]
    Network --> Server["后端网关与 Web 服务器"]
    Server --> |"解析 HTTP 报文，反序列化 JSON"| BusinessLogic["后端业务逻辑与数据库检索"]
```

客户端 API 封装库的核心职责：
- 隐藏构造 HTTP 消息的低级细节；
- 统一拦截并注入认证令牌（Auth Token）；
- 统一解析并格式化服务端错误，向上层返回强类型的结构化 Promise 对象。

---

## 3. RESTful 架构风格：让服务器摆脱会话包袱

在早期的状态化（Stateful）Web 服务中，服务器必须在内存中苦苦记忆与每一个客户端的会话状态（Session State）：
- 当前登录的用户是谁？
- 该用户在向导中走到了第 3 步还是第 4 步？
- 接下来该执行哪个动作？

**有状态服务的致命弊端**：服务器根本无法知道用户是否已经悄悄关闭了浏览器，必须为数以百万计的访客在内存中长期保留状态，导致服务器横向扩展（Scale-out）极难实现。

### 3.1 REST 的无状态核心哲学（Statelessness）

Roy Fielding 提出的 **REST（Representational State Transfer）** 架构彻底解决了这一难题：
- **瞬态会话状态全部转移到客户端保管**；
- **服务器保持彻底的“无状态（Stateless）”**：每一次来自客户端的请求，必须完整包含服务器处理该请求所必需的**所有上下文信息与授权凭证**；
- 服务器只需专注管理持久化资源（Persistent Resources，如数据库中的订单记录、用户信息），任何一台后端的无状态服务器均可任意接管处理来自任何客户端的请求。

---

## 4. 基于令牌（Token）的现代安全预授权

在无状态的 RESTful 架构中，客户端不能再依赖服务端的内存 Session。那么，客户端如何证明自己拥有执行某项受保护操作的权限？

### 4.1 Token 授权的闭环生命周期

```mermaid
sequenceDiagram
    autonumber
    actor User as 用户
    participant Client as 客户端 (Vue/React 单页应用)
    participant AuthServer as 认证授权中心 (Auth Server)
    participant ResourceServer as 业务资源服务器 (Resource API)
    
    User->>Client: 1. 输入账号与密码
    Client->>AuthServer: 2. POST /auth/login (凭据交换)
    AuthServer->>AuthServer: 3. 校验密码，生成非对称加密签名的 JWT 令牌
    AuthServer-->>Client: 4. 返回 Token (形如 Bearer eyJhbGciOi...)
    
    Note over Client: 客户端将 Token 安全保存在内存中
    
    Client->>ResourceServer: 5. GET /api/orders (请求头携带 Authorization: Bearer <Token>)
    ResourceServer->>ResourceServer: 6. 验证签名防伪，提取用户 ID 与角色权限
    ResourceServer-->>Client: 7. 确认无误，返回受保护的订单数据
```

1. **令牌的获取（Token Issuance）**：
   - 客户端最初通过用户名/密码凭据、第三方 OAuth 2.0（如 Google/GitHub 授权登录）向认证端点发起一次性握手；
   - 认证中心在验证凭据合法后，向客户端签发经过密码学私钥签名的**令牌（如 JSON Web Token, JWT）**；
2. **防伪与自包含特性**：
   - 令牌由三部分构成：头部（Header）、载荷（Payload，包含过期时间、用户 ID、角色列表）与数字签名（Signature）；
   - 由于只有官方服务器掌握私钥，客户端任何篡改载荷的行为都会导致签名失效，因此令牌是**不可伪造的授权证明**；
3. **每次请求的主动附带**：
   - 客户端在后续发起的每一个 RESTful 请求中，通过 HTTP 头部自动附带：
     ```http
     Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
     ```

---

## 5. 组件化架构革命：按组件分离 vs. 按关注点分离

在早期的 Web 理念中，“关注点分离（Separation of Concerns）”被刻板地理解为**文件物理技术类型的分离**：
- 所有的 HTML 放在一个巨大的 `index.html`；
- 所有的样式写在一个巨大的 `style.css`；
- 所有的脚本写在一个庞大的 `main.js`。

### 5.1 传统模式在大型应用中的崩溃

当界面变得极其庞大时，修改一个卡片标题的字号，需要程序员在 3,000 行的 CSS 文件中全局搜索类名，且提心吊胆生怕破坏了其他页面的相同样式；当删除一个不再使用的按钮时，遗留在 JS 里的事件监听函数往往无人敢删，代码迅速腐化为历史包袱。

![按技术类型分离 vs 按自包含独立组件分离的文件结构对比](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20260514021614611.png)

现代 Web 确立了新的架构共识：**按自包含、独立、可重用的组件进行纵向切分（Separation by Component）**。每个组件拥有专属的独立文件夹，内部封装它自身所需的 HTML 结构、CSS 作用域样式与 JS 交互逻辑。

### 5.2 组件的封装目标

![复杂的卡片界面如果不进行封装，会导致海量冗余标签堆砌](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20260514021054740.png)

![组件封装目标：将冗长标签压缩为整洁自解释的自定义标签](https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/image-20260514021308406.png)

通过将几十行复杂的标记折叠为单一语义标签，页面呈现出极高的自解释性：

```html
<!-- 优雅的组件化使用方式 -->
<location-card
  name="Turtle Rock"
  subtitle="Joshua Tree National Park"
  region="California"
  map-src="map.jpg"
  photo-src="turtle-rock.jpg"
  description="Descriptive text goes here.">
</location-card>
```

---

## 6. Vue.js 单文件组件与响应式实现

在 Vue 3 中，组件是纯粹且完备的自包含实体。使用 Composition API 可以极其优雅地实现上述 `LocationCard`：

```html
<!-- LocationCard.vue -->
<template>
  <div class="location-card">
    <div class="card-map-header">
      <img :src="mapSrc" :alt="`${name} map`">
      <div class="card-photo-ring">
        <img class="card-photo" :src="photoSrc" :alt="name">
      </div>
    </div>
    <div class="card-body">
      <div class="card-title-row">
        <div class="card-titles">
          <h2 class="card-name">{{ name }}</h2>
          <p class="card-subtitle">{{ subtitle }}</p>
        </div>
        <span class="card-region">{{ region }}</span>
      </div>
      <hr class="card-divider">
      <section class="card-about">
        <h3>About {{ name }}</h3>
        <p>{{ description }}</p>
        <!-- 响应式点赞交互 -->
        <button class="like-btn" @click="handleLike">
          ❤️ 喜欢 ({{ likes }})
        </button>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 声明组件的输入属性契约 (Props)
const props = defineProps({
  name: { type: String, required: true },
  subtitle: { type: String, default: '' },
  region: { type: String, default: '' },
  mapSrc: { type: String, required: true },
  photoSrc: { type: String, required: true },
  description: { type: String, default: '' }
});

// 声明组件向外派发的事件契约 (Emits)
const emit = defineEmits(['like-updated']);

// 组件内部独立的响应式状态
const likes = ref(0);

function handleLike() {
  likes.value++;
  emit('like-updated', { name: props.name, totalLikes: likes.value });
}
</script>

<style scoped>
/* scoped 属性保证所有样式被哈希隔离，绝不污染全局外部页面！ */
.location-card {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  background: white;
}
</style>
```

---

## 7. Web Components 原生浏览器标准

组件化并非仅仅存在于 Vue 或 React 等第三方框架中。W3C 与 WHATWG 联合为浏览器原生平台注入了完整的 **Web Components 标准规范体系**：

```mermaid
mindmap
  root((Web Components 原生标准三大件))
    Custom Elements (自定义元素)
      customElements.define
      生命周期回调函数
      属性监听 attributeChanged
    Shadow DOM (影子 DOM)
      attachShadow
      彻底隔离 CSS 样式
      内部 DOM 节点隐身封装
    HTML Templates (模板与插槽)
      &lt;template&gt; 惰性渲染标签
      &lt;slot&gt; 声明式内容投影
```

::: example 使用原生 JavaScript 编写纯原生 Web Component
```javascript
class NativeLocationCard extends HTMLElement {
  constructor() {
    super();
    // 1. 创建封闭的 Shadow Root，样式彻底隔离
    this.attachShadow({ mode: 'open' });
  }

  // 2. 生命周期回调：当元素被挂载插入到页面真实 DOM 时触发
  connectedCallback() {
    const name = this.getAttribute('name') || 'Unnamed';
    const photo = this.getAttribute('photo-src') || '';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          border: 1px solid #e5e7eb;
          border-radius: 8px;
          padding: 16px;
        }
        h2 { color: #111827; margin: 0; }
        img { border-radius: 50%; width: 64px; height: 64px; }
      </style>
      <div class="card">
        <img src="${photo}" alt="${name}">
        <h2>${name}</h2>
        <!-- 插槽：允许外部在使用该标签时投影自定义描述段落 -->
        <slot></slot>
      </div>
    `;
  }
}

// 3. 在浏览器全局注册自定义标签名（规范强制要求标签名必须包含短横线连字符！）
customElements.define('native-location-card', NativeLocationCard);
```
:::
