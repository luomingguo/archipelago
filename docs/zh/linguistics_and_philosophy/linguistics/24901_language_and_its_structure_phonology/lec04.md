---
title: '音系交替与生成推导 I：底层形式构拟与重写规则'
type: lecture
lecture: 4
tags: [phonology, alternations, underlying-representation, derivations, rule-ordering]
status: complete
source: 'https://ocw.mit.edu/courses/24-901-language-and-its-structure-i-phonology-fall-2010/'
---

# Lec 04 音系交替与生成推导 I：底层形式构拟与重写规则（Alternations and Derivations I）

在上一讲中，我们探讨了单一语素内部由相邻环境诱发的静态同位异音。然而，生成音系学最具解释力、最核心的领域在于**动态形态音系交替（Morphophonemic Alternations）**。当词根与词缀相互拼装时，交界处经常爆发系统性的语音冲突，迫使语素改变其表层容貌。在麻省理工学院 24.901 第五讲中，Michael Kenstowicz 教授形式化建立了从交替数据逆向构拟单一底层形式（Underlying Representation, UR）的推导原则，并通过波兰语清化、俄语元音弱化与英语屈折交替展现形式推导的数学严谨性。

## TL;DR

- **音系交替的核心命题**：同一个词根或词缀在不同形态环境中表现为不同语音形式，音系学主张其在词库中拥有单一不变的底层形式（UR）。
- **可预测性原则（Predictability Principle）**：交替分析的黄金法则——如果一类词汇稳定不交替，而另一类词汇交替，则交替词汇的底层形式必须选择那个能单向预测所有表层形式的变体。
- **波兰语词尾清化实证**：通过对比 *chleb*（面包，表层清化）与 *nos*（鼻子，稳定清音），确立词尾阻塞音清化规则 `[-son] -> [-voice] / ___ #`。
- **英语屈折后缀的统一推导**：英语复数词缀的底层形式是单一的 $/z/$，通过母音插入与清化规则推导出 $[s], [z], [\partial z]$ 三种表层形式。

## 1. 音系交替分析的假说空间与决策法则

当一个语素表现出 $[A]$ 与 $[B]$ 两个不同的音系交替形式时，理论上存在三种竞争假说：
1. **假说 1**：$/A/$ 为底层形式，在特定环境 $X$ 中发生规则 $A \longrightarrow B$；
2. **假说 2**：$/B/$ 为底层形式，在互补环境 $Y$ 中发生规则 $B \longrightarrow A$；
3. **假说 3**：两者均非底层，底层为一个更抽象的 $/C/$，分别由规则 $C \to A$ 和 $C \to B$ 推导。

在生成语法中，我们通过**奥卡姆剃刀与预测性原则**在这三者之间做出抉择：

::: theorem 可预测性原则（Criterion of Predictability）
若词库中存在两组词汇：
- 集合 1 始终保持稳定的语音 $[A]$（无论环境如何从不改变）；
- 集合 2 则在环境 $X$ 下表现为 $[A]$，在环境 $Y$ 下表现为 $[B]$。

则**严禁将 $/A/$ 设为集合 2 的底层形式**。因为如果两组词汇的底层全都是 $/A/$，任何音系规则都无法区分“为什么集合 1 的 $/A/$ 保持不变，而集合 2 的 $/A/$ 却要在环境 $Y$ 变为 $[B]$”。因此，集合 2 的底层形式必须是 $/B/$。
:::

## 2. 经典波兰语（Polish）名词交替推导

波兰语名词单数主格（无后缀，词尾）与单数属格（带元音后缀 *-a*）的交替是音系学史上的里程碑案例：

| 单词含义 | 单数主格 (Sg. Nom) | 单数属格 (Sg. Gen) | 词尾音段交替模式 |
| :--- | :---: | :---: | :---: |
| **面包** | *chleb* $[\text{xlep}]$ | *chleba* $[\text{xleba}]$ | $[p] \sim [b]$ |
| **鼻子** | *nos* $[\text{nos}]$ | *nosa* $[\text{nosa}]$ | $[s] \sim [s]$（稳定不变） |
| **马车** | *wóz* $[\text{vus}]$ | *woza* $[\text{v\supset za}]$ | $[s] \sim [z]$，且伴随 $[u] \sim [\supset]$ |
| **青蛙** | *żaba* $[\text{zaba}]$ | *żab* $[\text{zap}]$ | 词干以浊音结尾，词尾清化 |

::: example 波兰语清浊交替的形式化分析
1. **对比两组词**：
   - 组 A（稳定清音）：*los* $[\text{los}]$ / *losa* $[\text{losa}]$（命运）；
   - 组 B（清浊交替）：*nos* $[\text{nos}]$ 的对立面——*głaz* $[\text{gwas}]$ / *głazu* $[\text{gwazu}]$（巨石）。
2. **底层确立**：根据可预测性原则，若将交替词的底层设为 $/s/$，则无法解释为何 *los* 的 $/s/$ 在词尾不浊化为 $[z]$；若将底层设为 $/z/$，则只要一条简单的**词尾阻塞音清化规则**即可全量推导：
   $$\left[ -\text{sonorant} \right] \longrightarrow [-\text{voice}] \quad / \quad \text{ \_\_\_ } \#$$
:::

在属格环境中，由于后续存在元音后缀 *-a*，阻塞音处于音节首或元音之间，清化规则环境不满足，底层的浊音 $/b, z, g/$ 如实发音；在主格时词尾孤立暴露在词界符 $\#$，规则被触发强制清化。

## 3. 英语规则名词复数与动词过去时的统一构拟

许多英语语法书罗列了复数后缀的三个不同形式：*cats* $[-\text{s}]$、*dogs* $[-\text{z}]$、*busses* $[-\mathrm{I}\text{z}]$。生成音系学证明，这三个变体完全源自单一底层式。

### 3.1 底层形式的选择：$/z/$ 还是 $/s/$？

考察英语名词词干末尾的环境：
- 清辅音后：*caps* $[p-\text{s}]$, *books* $[k-\text{s}]$；
- 浊音与元音后：*cabs* $[b-\text{z}]$, *dogs* $[g-\text{z}]$, *bees* $[i-\text{z}]$；
- 嘈吵音（Sibilants $[s, z, \int, 3, t\int, d3]$）后：*glasses* $[s-\partial\text{z}]$, *judges* $[d3-\partial\text{z}]$。

若假设底层为 $/s/$，在元音后变为 $[z]$（如 *bees*）将违背音系普遍性，因为元音后的清辅音在英语中极其丰富（如 *peace*, *lease* 从不发生浊化）。若假设底层为 $/z/$，规则推导呈现极佳的局部生理自然性：

::: definition 英语复数推导的两大排序规则
1. **母音插入规则（Schwa Insertion）**：当两个嘈吵音在词界相遇时，为了避免齿龈/硬腭摩擦能量过度重叠导致感知崩溃，强制插入元音 $[\partial]$：
   $$\emptyset \longrightarrow [\partial] \quad / \quad [+\text{strident}] \text{ \_\_\_ } [+\text{strident}] \#$$
2. **渐进同化清化规则（Progressive Devoicing）**：若无母音阻隔，处于清辅音后的浊阻塞音同化清音特征：
   $$\left[ \begin{array}{c} -\text{son} \\ +\text{voice} \end{array} \right] \longrightarrow [-\text{voice}] \quad / \quad [-\text{voice}] \text{ \_\_\_ }$$
:::

推导过程展示如下：

| 输入底层式 (UR) | `/kæt + z/` (*cats*) | `/dɔg + z/` (*dogs*) | `/bʌs + z/` (*busses*) |
| :--- | :---: | :---: | :---: |
| **规则 1：母音插入** | 不适用 | 不适用 | $[\text{b}\Lambda\text{s}-\partial\text{z}]$ |
| **规则 2：清化同化** | $[\text{k}\ae\text{ts}]$ | 不适用 | 不适用（被 $[\partial]$ 阻断） |
| **表层输出 (SR)** | `[kæts]` | `[dɔgz]` | `[bʌsəz]` |

::: insight 规则排序保护底层：流血效应的雏形
注意 *busses* 的推导逻辑：母音插入规则不仅解决了发音难点，还同时**摧毁了清化规则的触发环境**！如果清化规则先于母音插入执行，*busses* 将先变成错误的 $*[\text{b}\Lambda\text{ss}]$，再插入元音得到 $*[\text{b}\Lambda\text{s}\partial\text{s}]$。母音插入“流血”（Bleeds）了清化规则，这一顺序保证了表层输出精确匹配真实语料。
:::

::: pitfall 语音自然度陷阱：不可盲目依赖统计多数
在确定底层形式时，不可单纯清点表面词汇的词频。在许多语言中，发生交替的表层形式可能由于词汇历史原因在数量上少于不交替形式，但只要它展现出单向推导的决定性不对称，就必须服从可预测性原则。
:::
