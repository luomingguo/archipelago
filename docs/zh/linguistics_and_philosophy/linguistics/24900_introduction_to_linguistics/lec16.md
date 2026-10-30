---
title: 句法学（六）：中心语方向参数、FOFC 普适禁令与三大移位体系
type: lecture
lecture: 16
tags: [head-directionality, fofc, v2-movement, movement-trinity, that-trace-effect]
status: complete
source: 'https://ocw.mit.edu/courses/24-900-introduction-to-linguistics-spring-2022/'
---
# Lec 16 句法学 VI ：Head Directionality、FOFC、Movement & Islands





## 中心语方向参数

在英语中，我们发现了一个压倒一切的普遍规律：**中心语在前（Head-Initial）**。也就是说，中心语永远位于它的补足语（*sister/complement*）之前：

- 动词先于宾语：`[eat] sushi`（吃 寿司）；
- 介词先于名词短语：`[with] chopsticks`（用 筷子）；
- 补足语引导词（C）先于时态短语（TP）：`[that] Mary could eat sushi`（玛丽可以用筷子吃寿司）。

但是，如果我们把中心语的位置镜像对调，语言会变成什么样？在世界语言中，有许多语言系统性地执行**中心语在后（Head-Final）**。比如日语、韩语或土耳其语：

- 宾语先于动词（SOV）：*sushi-o taberu*（寿司 吃）；
- 名词先于介词（使用后置词 Postposition）：*hashi-de*（筷子 用）；
- 句子先于时态助动词：动词短语在前，时态在后；
- 从句补足语引导词挂在整句的最末端：*to* 出现在整个从句之后！

所以，在日语这样的语言中，中心语永远跟在补足语后面。英语是中心语在前，日语是中心语在后。这就是著名的**中心语方向参数（Head-Directionality Parameter）**

世界上的语言并非非黑即白地全盘选择“在前”或“在后”。很多语言具有混合中心语方向。

比如德语（German）的内嵌从句：

- 引导词是前置的：`dass`（that）放在句首；
- 介词是前置的：`mit`（with）放在名词短语之前；
- 但是动词短语和时态是中心语在后的：宾语在动词前，动词短语在助动词前！
  $$\text{“...dass Mary mit Stäbchen Sushi essen konnte.”} $$ （玛丽用筷子寿司吃能够）

又比如西弗拉芒语（West Flemish，比利时的一种日耳曼语方言）：

- 引导词在前：`dat`（that）；
- 但时态助动词在前：`wilt`（wants）；
- 动词却在宾语之后：中心语在后！$$\text{“...dat Jan wilt een huis kopen.”} \quad (\text{“...即扬想要一座房子买”})$$



## 终结优先禁令（Final-over-Final Condition, FOFC）

既然语言可以在不同层级上混合“在前”与“在后”，那么在一个从句的动词投射链条（$TP \rightarrow VP \rightarrow NP$​​）中，理论上存在四种数学组合逻辑：

| 逻辑组合       | 结构示例                             | 时态 T 的方向                | 动词 V 的方向                | 现实语言分布                          |
| -------------- | ------------------------------------ | ---------------------------- | ---------------------------- | ------------------------------------- |
| **1. 前 + 前** | `[that Mary [could [eat sushi]]]`    | 中心语在前（T 在 VP 前）     | 中心语在前（V 在 NP 前）     | **极度普遍**（英语、罗曼语族等）✅     |
| **2. 后 + 后** | `[dass Mary [[Sushi essen] konnte]]` | 中心语在后（T 在 VP 后）     | 中心语在后（V 在 NP 后）     | **极度普遍**（德语、日语、土耳其语）✅ |
| **3. 前 + 后** | `[dat Jan [wilt [een huis kopen]]]`  | 中心语在前（T 在 VP 前）     | 中心语在后（V 在 NP 后）     | **存在**（西弗拉芒语等）✅             |
| **4. 后 + 前** | `*[that Mary [[eat sushi] could]]`   | **中心语在后（T 在 VP 后）** | **中心语在前（V 在 NP 前）** | 全球彻底绝迹！❌❌❌                     |

