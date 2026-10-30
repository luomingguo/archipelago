---
title: 辅音发音机制与二元区别性特征系统
type: lecture
lecture: 2
tags: [phonetics, consonants, distinctive-features, natural-classes, phonology]
status: complete
source: 'https://ocw.mit.edu/courses/24-901-language-and-its-structure-i-phonology-fall-2010/'
---

# Lec 02 辅音发音机制与二元区别性特征系统（Consonants & Distinctive Features）

在经典结构主义语音学中，语音通常被视作不可分割的原子式符号。然而，音系学革命性的一步在于认识到：**音位（Phonemes）绝非不可分割的基元，而是由更底层的二元区别性特征（Distinctive Features）正负取值构成的特征矩阵**。在麻省理工学院 24.901 的第二、三讲中，Michael Kenstowicz 教授系统推导辅音的发音生理机制，并构建以罗曼·雅各布森（Roman Jakobson）与莫里斯·哈勒（Morris Halle）为先驱的二元特征体系，论证自然类（Natural Classes）如何奠定生成音系学规则的形式基础。

## TL;DR

- **音位的内部矩阵解构**：音位是由二元特征构成的向量集合，音系规则的本质是改写特定特征值。
- **辅音三大解剖学轴线**：发音部位（主动与被动发音器官）、发音方法（阻塞程度与气流通路）以及声门状态（清/浊/送气）。
- **主要类别特征（Major Class Features）**：$[ \pm\text{consonantal} ]$ 与 $[ \pm\text{sonorant} ]$ 将自然语言所有音段严格划分为元音、滑音、流音、鼻音与阻塞音五大阶层。
- **自然类的数学简洁性**：共享相同特征组合的音段集合构成自然类，音系规则只作用于自然类而非任意符号列表。

## 1. 辅音发音生理机制：部位、方法与声门状态

与元音完全开放的共鸣腔不同，辅音（Consonants）是在声道某处形成完全闭塞、局部狭窄或受控气流所产生的声音。描写辅音必须确立三大生理维度：

### 1.1 发音部位（Place of Articulation）

发音部位由**主动发音器官（Active Articulator）**向**被动发音器官（Passive Articulator）**运动形成：
- **双唇音（Bilabial）**：如下唇贴合上唇，$[p], [b], [m]$；
- **唇齿音（Labiodental）**：下唇轻触上齿，$[f], [v]$；
- **齿间音/齿音（Interdental / Dental）**：舌尖置于上下齿之间或抵住上齿背，$[\theta], [\eth]$；
- **齿龈音（Alveolar）**：舌尖或舌叶贴向牙龈嵴，$[t], [d], [s], [z], [n], [l]$；
- **齿龈后/硬腭龈音（Postalveolar / Palato-alveolar）**：舌叶移至齿龈嵴后方，$[\int], [3], [t\int], [d3]$；
- **卷舌音（Retroflex）**：舌尖向上卷起反折向硬腭前部，$[t], [\mathrm{d}], [s], [z]$（如印地语、泰米尔语）；
- **硬腭音（Palatal）**：舌前部隆起紧贴硬腭，$[j], [c], [\mathcal{J}]$；
- **软腭音（Velar）**：舌后部隆起抵住软腭，$[k], [g], [\eta]$；
- **小舌音（Uvular）**：舌根后缩抵住小舌，$[q], [\mathrm{G}], [\chi], [\mathrm{s}]$（如阿拉伯语、法语 $r$）；
- **咽音（Pharyngeal）**：会厌软骨向咽后壁紧缩，$[\hbar], [\mathcal{S}]$；
- **声门音（Glottal）**：声带本身作为阻塞点，$[?], [h]$。

### 1.2 发音方法（Manner of Articulation）

- **塞音/爆破音（Stops / Plosives）**：声道完全闭合，气流蓄积后突然释放冲出；
- **擦音（Fricatives）**：声道形成极窄裂缝，高速气流通过产生湍流摩擦噪声；
- **塞擦音（Affricates）**：先形成完全闭塞，随后以极慢速度狭窄释放，产生同部位摩擦（如 $[t\int], [ts]$）；
- **鼻音（Nasals）**：软腭下垂打开鼻咽通道，口腔完全阻塞，声波完全经由鼻腔共鸣辐射；
- **近音/流音/滑音（Approximants: Liquids & Glides）**：声道形成轻微收缩但不足以引发湍流噪声（如边音 $[l]$、半元音 $[j], [w]$）。

---

## 2. 二元区别性特征体系（The Binary Feature System）

若音系规则仅以单个 IPA 符号书写，规则将退化为离散符号的任意罗列，无法解释为什么某些音群总是一同参与交替。SPE（Chomsky & Halle 1968）确立了二元特征体系（$[+\text{Feature}]$ 或 $[-\text{Feature}]$）。

### 2.1 主要类别特征（Major Class Features）

主要类别特征定义了声带振动自发性与声道阻碍的根本拓扑：

::: definition 主要类别二元特征
- **$[ \pm\text{consonantal} ]$（辅音性）**：声道中线上是否存在显著的局部阻塞阻碍。塞音、擦音、塞擦音、鼻音与流音为 $[+\text{cons}]$；元音与滑音（$[j], [w]$）为 $[-\text{cons}]$；
- **$[ \pm\text{sonorant} ]$（响音性）**：构型是否允许声带在无阻力条件下自发振动（Spontaneous Voicing）。元音、滑音、流音、鼻音为 $[+\text{son}]$；阻塞音（Obstruents: 塞音、擦音、塞擦音）为 $[-\text{son}]$；
- **$[ \pm\text{syllabic} ]$（音节主峰性）**：能否作为音节的核（Nucleus）。元音与成音节辅音为 $[+\text{syll}]$，其他辅音为 $[-\text{syll}]$。
:::

主要音段类型的特征划分矩阵如下：

| 特征类别 | 元音 (V) | 滑音 (G: $j, w$) | 流音 (L: $l, r$) | 鼻音 (N: $m, n$) | 阻塞音 (Obs: $p, s$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **$[\text{consonantal}]$** | $-$ | $-$ | $+$ | $+$ | $+$ |
| **$[\text{sonorant}]$** | $+$ | $+$ | $+$ | $+$ | $-$ |
| **$[\text{syllabic}]$** | $+$ | $-$ | $-$ (可$+变$) | $-$ (可$+变$) | $-$ |

### 2.2 发音部位与腔体特征（Cavity & Place Features）

以舌叶（Coronal）与舌面（Dorsal）为核心解剖基准：
1. **舌冠特征（Coronal Node）**：
   - **$[ \pm\text{coronal} ]$**：以舌尖或舌叶为主动发音器官（齿音、齿龈音、卷舌音、硬腭龈音为 $[+\text{cor}]$）；
   - **$[ \pm\text{anterior} ]$**：发音部位是否位于牙龈嵴的前方（含牙龈嵴）。齿龈音、齿音为 $[+\text{ant}]$；齿龈后、硬腭音、卷舌音为 $[-\text{ant}]$；
   - **$[ \pm\text{distributed} ]$**：舌体与发音部位接触面沿气流方向是否延伸较宽。舌叶音为 $[+\text{dist}]$，舌尖音为 $[-\text{dist}]$。
2. **舌背特征（Dorsal Node）**：
   - **$[ \pm\text{high} ]$**：舌体是否高于中位静止状态（高元音与软腭音 $[k, g]$ 为 $[+\text{high}]$）；
   - **$[ \pm\text{low} ]$**：舌体是否低于中位（低元音为 $[+\text{low}]$）；
   - **$[ \pm\text{back} ]$**：舌根向后缩（后元音与软腭音为 $[+\text{back}]$）。
3. **唇音特征（Labial）**：
   - **$[ \pm\text{round} ]$**：双唇收圆。

### 2.3 发音方式与喉部特征（Manner & Laryngeal Features）

- **$[ \pm\text{continuant} ]$**：声道中心线上气流是否持续逸出。擦音、元音、滑音为 $[+\text{cont}]$；塞音与鼻音（口腔闭死）为 $[-\text{cont}]$；
- **$[ \pm\text{nasal} ]$**：软腭下垂打开鼻咽腔；
- **$[ \pm\text{strident} ]$**：高强度摩擦噪声（Sibilants 嘈吵音 $[s, z, \int, 3]$ 为 $[+\text{strid}]$）；
- **$[ \pm\text{voice} ]$**：声带周期性闭合振动；
- **$[ \pm\text{spread glottis} ]$（[±s.g.]）**：声门开张，对应送气音（Aspirated stops $[p^h, t^h, k^h]$）；
- **$[ \pm\text{constricted glottis} ]$（[±c.g.]）**：声门紧闭，对应喉化音或声门塞音。

---

## 3. 自然类（Natural Classes）与规则经济性

为什么形式音系学抛弃独立的字母标记？其核心数学依据是**自然类的符号经济性**。

::: theorem 自然类公理（Natural Class Axiom）
一个音段集合如果能够在给定语言中用少于指称其中任何单个成员所需的特征组合完全定义，该集合即构成一个**自然类（Natural Class）**。
自然语言的音系规则只作用于自然类，禁止针对任意无序的符号集合。
:::

::: example 关岛查莫罗语（Chamorro）后元音前移
在查莫罗语中，当后元音 $/u, o, \alpha/$ 出现在带特定前缀（如定冠词 *i*、前缀 *mi-*、*in-*）后时，会系统性前移为前元音 $[i, e, \ae]$：
- *guma'*（房子） $\to$ *i gima'*（那座房子）
- *tommo*（膝盖） $\to$ *i temmo*（那个膝盖）
- *lågu*（北方） $\to$ *i lægu*（去北方）

若用 IPA 单独表达，需要穷举三条并列规则；但若采用二元特征，后元音集合被形式化为自然类 $[-\text{cons}, +\text{back}]$，规则可精炼写为：
$$\left[ \begin{array}{c} -\text{cons} \\ +\text{back} \end{array} \right] \longrightarrow [-\text{back}] \quad / \quad \left[ \begin{array}{c} -\text{cons} \\ -\text{back} \\ +\text{high} \end{array} \right] \mathrm{C}_0 \text{ \_\_\_ }$$
一个统一的改写操作（$[-\text{back}]$ 扩散）瞬间解释了全部三种元音的平行交替。
:::

::: insight 特征系统的本体论地位：心智计算的最小原语
二元区别性特征不仅仅是语音学分类的便利工具，它构成了人类语言计算能力的底层硬件接口。婴儿在语言习得过程中，并不是逐一记忆母语中几千个离散音节组合，而是通过统计分布迅速确立各特征维度的正负对立。音系演变中的链式转移（Chain Shifts）与同化现象之所以成系统地波及整个音系，正是因为大脑在特征层级上执行统一的宏指令。
:::
