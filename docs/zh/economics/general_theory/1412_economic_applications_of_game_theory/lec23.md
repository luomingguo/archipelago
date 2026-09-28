---
title: 不完全信息下的动态讨价还价与科斯猜想
type: lecture
lecture: 23
tags: [bargaining-incomplete-information, coase-conjecture, adverse-selection, screening-over-time]
status: complete
source: 'https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/'
---

# Lec 23 不完全信息下的动态讨价还价与科斯猜想（Bargaining with Incomplete Information）

> MIT 14.12 · Economic Applications of Game Theory · 主讲 Ian Ball

## TL;DR

- 卖方垄断耐用品向具有私人估值的买方跨期报价，面临动态严重的时间不一致性。
- 剖析科斯猜想（Coase Conjecture）：当报价时间间隔趋近于零时，垄断者失去全部定价权，价格瞬间跌至边际成本。
- 考察买方利用时间拖延展示耐受力的筛选博弈机制。

## 核心概念与数学形式化

### 耐用品垄断与科斯猜想模型

垄断卖方生产耐用品，边际成本 $c = 0$。买方估值 $v \sim U[0, 1]$ 为买方私人信息。
博弈分为多期，出价时间间隔为 $\Delta$，有效贴现因子 $\delta = e^{-r\Delta}$。

1. **有限期末期诱惑**：
   在最后一期，卖方总有动机把价格降至极低以捞取最后一波长尾客户；
2. **买方跨期等待套利**：
   高估值买家权衡当期购买剩余 $(v - p_t)$ 与等待一期享受降价的折现剩余 $\delta (v - p_{t+1})$：
   $$v - p_t \ge \delta (v - p_{t+1})$$
   这迫使卖方在当期制定的价格 $p_t$ 受到未来预期降价的极其严厉的束缚。

### 科斯猜想定理（Coase, 1972 / Gul, Sonnenschein, and Wilson, 1986）
当报价时间间隔无限微小（$\Delta \to 0$，即 $\delta \to 1$）且买方估值分布下界紧贴成本线时：
耐用品垄断者的初始开价 $p_0$ 必定瞬间收敛至边际成本 $c$！
垄断者所有的垄断超额利润被剥夺殆尽，资源配置在初始瞬间达到完全竞争的社会福利最优。

### 垄断者的自救反制策略
为了打破科斯猜想诅咒，垄断者必须引入承诺机制：
- **只租不售（Leasing instead of Selling）**：如施乐（Xerox）复印机早期政策；
- **最惠国退差价条款（Most-Favored-Nation Clause）**：承诺若未来降价必向早期买家全额退款；
- **故意限制未来产能**：销毁印版与模具（如限量版艺术品）。

## 经济应用与机制分析

科技硬件（如智能手机与显卡）的“跳水式降价”屡屡遭到老用户抵制。厂商通过推行以旧换新残值保障协议以及锁死下一代芯片发布周期，本质上是在向市场确立反向承诺，以维系旗舰产品的高毛利区间。

## 边界条件与易错点

误以为科斯猜想适用于一次性消耗品（它严格要求商品是耐用品，买家具有跨期跨阶段消费能力）；忽视买方估值下界若高于成本则垄断者仍能保留正利润。

## 官方资源与参考

- [本讲视频讲座](https://www.youtube.com/watch?v=CFELos-uZbE)
- [MIT 14.12 官方课程主页](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/)
- [MIT 14.12 讲义清单（Lists of Lecture Notes）](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/lists/lecture-notes/)

::: insight
科斯猜想展现了垄断者“与未来的自己竞争”所遭遇的毁灭性溃败。一个拥有绝对垄断权的耐用品生产商，今天把商品高价卖给最心急的高估值客户后，明天它就必然有强烈的动机对剩下的低估值客户降价清仓。但如果聪明的消费者早已看穿这套降价把戏，今天就绝不买单！垄断权在瞬间灰飞烟灭。
:::
