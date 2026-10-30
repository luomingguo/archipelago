---
title: 语音学基础与元音描写体系
type: lecture
lecture: 1
tags: [phonetics, vowels, ipa, articulation, grimms-law]
status: complete
source: 'https://ocw.mit.edu/courses/24-901-language-and-its-structure-i-phonology-fall-2010/'
---

# Lec 01 语音学基础与元音描写体系（Course Overview & Vowel Articulation）

人类语言在物理层面上表现为连续的声学空气振动，但在人类心智中却被感知为离散、抽象的语音单元。在麻省理工学院 24.901 音系学第一讲中，Michael Kenstowicz 教授带领我们确立语言学研究的核心视域：从 19 世纪的历史历时比较（如格里姆定律 Grimm's Law）跃迁至 20 世纪索绪尔（Ferdinand de Saussure）确立的共时语言系统（Synchronic System），并形式化建立语音学的生理描写基准——元音的发音几何与国际音标（IPA）转写体系。

## TL;DR

- **语言的心智离散性**：人类语音在物理声学上是连续谱，但在认知上被离散化为抽象语音表征。
- **元音三维几何**：舌位高度（高/中/低）、前后位置（前/央/后）与唇形圆展（圆唇/展唇）构成元音描述的通用生理坐标系。
- **声学对应关系**：第一共振峰（$F_1$）与舌位高度呈反比，第二共振峰（$F_2$）与舌位靠前程度呈正比。
- **跨语言元音格局**：普遍的五元音系统（/i, e, a, o, u/）呈现声学最大分散原则，而英语则演化出高度复杂的松紧元音对立。

## 1. 语言作为科学研究对象：从历史历时到形式共时

在 19 世纪，语言学被视为历史文化演变的产物。要理解一种语言的现状，必须追溯其祖语演变史。这一时期的巅峰成就是原始印欧语（Proto-Indo-European, PIE）的重构，以及标志性的**格里姆定律（Grimm's Law）**。

::: definition 格里姆定律（Grimm's Law）
格里姆定律揭示了原始印欧语（PIE）塞音向原始日耳曼语演变时的系统性音变链条：
1. **无声不送气塞音演化为清擦音**：$*p, *t, *k, *k^w \to f, \theta, h, h^w$（例：PIE $*p\acute{e}d- \to$ 梵语 *pāda*, 拉丁语 *pēs*, 英语 *foot*；PIE $*trey- \to$ 拉丁语 *trēs*, 英语 *three*）；
2. **浊不送气塞音演化为清塞音**：$*b, *d, *g, *g^w \to p, t, k, k^w$（例：PIE $*dwo- \to$ 拉丁语 *duo*, 英语 *two*；PIE $*gen- \to$ 拉丁语 *genū*, 英语 *knee*）；
3. **浊送气塞音演化为浊擦音或浊塞音**：$*b^h, *d^h, *g^h, *g^{wh} \to b, d, g, w$（例：PIE $*b^hr\acute{a}t\bar{e}r \to$ 梵语 *bhrātar*, 拉丁语 *frāter*, 英语 *brother*）。
:::

到了 20 世纪初，索绪尔指出语言的核心研究对象应当是**共时系统（Synchronic System）**：说话人在特定时间点的心智语法网络，其语言符号由能指（Signifier，声音意象）与所指（Signified，概念）的任意性结合构成。现代音系学正是探讨这种共时心智系统的内部形式规则。

## 2. 元音发音机制与生理几何空间

元音（Vowels）是在声道完全通畅、呼出气流不受剧烈阻塞阻碍的情况下，通过声带振动激励声道共鸣腔产生的乐音。

### 2.1 元音描写的核心生理维度

元音在传统生理语音学中由三大核心生理参数确定：
1. **舌位高度（Tongue Height）**：舌面最高点与上颚硬腭/软腭的垂直距离。划分为：
   - 高元音（High / Close）：如 $[i], [u]$；
   - 半高/半低中元音（Mid: Close-mid / Open-mid）：如 $[e], [o], [\varepsilon], [\supset]$；
   - 低元音（Low / Open）：如 $[a], [\alpha]$。
2. **舌位前后（Tongue Backness）**：舌面隆起的水平位置。划分为：前元音（Front）、央元音（Central）、后元音（Back）。
3. **唇形圆展（Lip Rounding）**：双唇向前撅起呈圆形（Rounded）或平展放松（Unrounded）。
4. **舌根松紧度（Tenseness / ATR）**：先进舌根（Advanced Tongue Root, [+ATR]）带来咽腔扩大与肌肉紧张（Tense），对应紧元音；紧随舌根（[-ATR]）对应松元音（Lax）。

```text
               前 (Front)          央 (Central)          后 (Back)
高 (High)       i    y               ɨ    ʉ               ɯ    u
半高 (Mid-high)  e    ø               ɘ    ɵ               ɤ    o
半低 (Mid-low)   ɛ    œ               ɜ    ɞ               ʌ    ɔ
低 (Low)        æ                    ɐ                    a    ɑ
             (展唇  圆唇)         (展唇  圆唇)          (展唇  圆唇)
```

::: insight 舌位几何的非线性声学投射
传统元音四边形看似是纯粹的解剖学位置图，但现代声学语音学揭示：**发音器官微小的非线性位移会在特定声学共振峰上产生极大的跃迁**。人类大脑并不是记忆舌肌肉的绝对位移坐标，而是将声道建模为一个自适应的声学滤波器。发音位置的生理边界本质上是由声学听觉的可辨度极大化（Acoustic Dispersion Theory）反向塑造的。
:::

## 3. 美式英语元音系统与国际音标转写

美式英语（General American）拥有极其丰富的元音对立，其核心特征是紧元音（Tense）与松元音（Lax）的成对分布，以及双元音的广泛运用：

| 单词样本 | 国际音标 | 发音生理特征 | 特性 |
| :--- | :---: | :--- | :--- |
| *beet* | $[i]$ | 前高紧元音（High Front Tense） | 紧元音，音长较长，可处于开音节 |
| *bit* | $[\mathrm{I}]$ | 前半高松元音（Lax High-Mid Front） | 松元音，仅出现在闭音节 |
| *bait* | $[e\mathrm{I}]$ | 前中紧双元音（Mid Front Closing Diphthong） | 伴随向 $[\mathrm{I}]$ 抬升滑动 |
| *bet* | $[\varepsilon]$ | 前半低松元音（Open-mid Front Lax） | 松元音 |
| *bat* | $[\ae]$ | 前低松元音（Low Front Lax） | 英语典型特色低前元音 |
| *boot* | $[u]$ | 后高圆唇紧元音（High Back Round Tense） | 紧元音 |
| *book* | $[\mathrm{\upsilon}]$ | 后半高圆唇松元音（Lax High-Mid Back Round） | 松元音 |
| *boat* | $[o\mathrm{\upsilon}]$ | 后中圆唇双元音（Mid Back Round Closing Diphthong） | 伴随向 $[\mathrm{\upsilon}]$ 滑动 |
| *bought* | $[\supset]$ | 后半低圆唇元音（Open-mid Back Round） | 在许多 GA 方言中与 $[\alpha]$ 合并 |
| *father* | $[\alpha]$ | 后低展唇元音（Open Back Unrounded） | 咽腔收缩 |
| *but* | $[\Lambda]$ | 央半低展唇元音（Open-mid Central Unrounded） | 重读音节特有 |
| *sofa* | $[\partial]$ | 央中非重读元音（Schwa / Mid-Central） | 英语最核心的非重读弱化元音 |

::: example 英语三大经典双元音
- **$[a\mathrm{I}]$ (*bite*, *ride*)**：从低展唇元音向高前位元音滑动；
- **$[a\mathrm{\upsilon}]$ (*bout*, *cow*)**：从低展唇元音向高后圆唇位滑动；
- **$[\supset\mathrm{I}]$ (*boy*, *coin*)**：从后半低圆唇向高前位滑动。
:::

## 4. 跨语言元音系统对比与感知边界

人类语言并不是随机选取元音库的。跨语言调查显示，全球绝大多数语言遵循声学能量最大分散原则（Principle of Maximal Dispersion）：
- **经典三元音系统（如古典阿拉伯语、因纽特语）**：$/i, u, a/$，占据元音四边形三个极点；
- **五元音系统（如西班牙语、日语、斯瓦希里语）**：$/i, e, a, o, u/$，在极点与中位均匀分布，稳定性最高；
- **复杂元音系统（如法语、德语、瑞典语、英语）**：引入前圆唇元音（如德语 *über* $[y]$, *schön* $[\varnothing]$）或鼻化元音（如法语 *un bon vin blanc*）。

::: pitfall 汉英发音负迁移：忽视松紧元音对立
许多以汉语为母语的学习者倾向于将英语 $[i]$ (*sheep*) 与 $[\mathrm{I}]$ (*ship*) 简单理解为“长音与短音”的区别。实际上，两者的本质分歧是**舌位高度与肌肉张力（[±ATR]）**的质性差异。若仅缩短 $[i]$ 的发音时长而不降低舌位并放松舌根，英语母语者依然会感知为带口音的 $[i]$，导致词义混淆。
:::
