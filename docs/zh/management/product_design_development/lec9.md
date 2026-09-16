---
title: 概念选择——从筛选到评分的结构化决策
type: lecture
lecture: 9
tags: [concept-selection, pugh-matrix, concept-screening, concept-scoring, decision-matrix]
status: complete
source: 'https://ocw.mit.edu/courses/15-783j-product-design-and-development-spring-2006/resources/cls9_cncpt_sel_6/'
---

# Lec 9 概念选择——从筛选到评分的结构化决策（Concept Selection）

> MIT 15.783 · Product Design and Development

## TL;DR

- 概念选择是产品开发流程七个阶段中的第四步，紧接在"生成产品概念"之后、"测试产品概念"之前，与经济分析、竞品对标、模型与原型搭建这三条贯穿全程的支持活动并行。
- 结构化方法分两级：**概念筛选（concept screening）**用粗粒度的 +/0/− 相对基准概念快速淘汰明显劣势方案；**概念评分（concept scoring）**对通过筛选的少数概念用 1–5 分乘以权重做精细排序。两者都以一个"参考概念"（reference concept，通常是已有产品或行业基准）作为比较锚点，而不是让团队凭空打绝对分。
- 课程反复强调一个容易被忽视的心法：概念选择的目标**不是从现有选项中挑一个最好的**，而是**通过比较、拆解、重组，开发出比任何单一初始概念都更好的新概念**——即"combine and improve"步骤和最后"Remember…"那页幻灯片的核心论点。
- 配套的四个警示（caveats）：警惕"平均最优"的伪劣结果；对不同客户群体分别做选择并比较结果；检验选择结果对权重和评分的敏感度；决赛阶段可能需要展开为更细的规格而非停留在粗粒度标准上。
- 阅读材料指向 Stuart Pugh 的《Total Design》——概念筛选矩阵在文献中常被称为 Pugh 矩阵（Pugh Matrix），是这套方法论的原始出处。

## 概念选择在产品开发流程中的位置

课程用两张流程图给出上下文。宏观上，产品开发分六个阶段：Planning → Concept Development → System-Level Design → Detail Design → Testing and Refinement → Production Ramp-Up，阶段之间以 Mission Approval、Concept Review、System Spec Review、Critical Design Review、Production Approval 五个评审节点分隔。

概念选择本身发生在"Concept Development"这一阶段内部，是七个子步骤中的第四步：

Identify Customer Needs → Establish Target Specifications → Generate Product Concepts → **Select Product Concept(s)** → Test Product Concept(s) → Set Final Specifications → Plan Downstream Development

三条支持性活动（Perform Economic Analysis、Benchmark Competitive Products、Build and Test Models and Prototypes）贯穿整个概念开发阶段，为选择过程提供输入，而不是选择之后才做的独立工作。

## 概念开发漏斗：从发散到收敛的两级过滤

课程用一个"漏斗"图形象化整个流程：概念生成（宽口，产出大量候选概念）→ 概念筛选（第一次收窄）→ 概念评分（第二次收窄）→ 概念测试（出口，剩下极少数候选进入下一阶段）。这张图的价值在于强调筛选和评分是**两个不同粒度的独立步骤**，不能用一次打分代替两次收敛：

- **概念筛选**：目的是快速砍掉明显不如基准的方案，用粗粒度的相对判断（好/一样/差），成本低、速度快，适合候选数量还很多的阶段。
- **概念评分**：目的是在少数幸存概念之间做精细排序，用加权数值评分，成本更高（需要更细的评分标准和团队讨论），适合候选数量已经收窄到可以逐一深入比较的阶段。

## 概念选择流程的六个步骤

1. **准备矩阵（Prepare the Matrix）**：确定评价标准（criteria）、选定参考概念（reference concept）、（评分阶段）确定各标准的权重（weightings）。
2. **评分（Rate Concepts）**：筛选阶段用 (+ / − / 0) 三档，评分阶段用 1–5 分连续量表，两种都以参考概念为比较对象，而不是绝对打分。
3. **排序（Rank Concepts）**：加权求和得到每个概念的总分。
4. **合并与改进（Combine and Improve）**：去掉明显的缺点特征，把不同概念中的优点组合到一起，产生新的、更优的混合概念——这一步是整套方法论真正的价值所在，见下文。
5. **选出最佳概念（Select Best Concept）**：结果可能不止一个概念进入下一轮；同时要警惕"平均概念"陷阱（见下文）。
6. **反思流程（Reflect on the Process）**：作为持续改进的输入，为后续项目积累更好的标准设定和评分校准经验。

## 概念筛选：Pugh 矩阵的实例

课程给出的实例是某种医疗给药/计量装置（从"Dose Metering""Load Handling"等标准判断，很可能是胰岛素笔或类似的剂量装置）的概念筛选矩阵。评价标准为 Ease of Handling、Ease of Use、Number Readability、Dose Metering、Load Handling、Manufacturing Ease、Portability 共 7 项，7 个候选概念 A–G 相对于一个参考概念（REF，全部记为 0）逐项打 +（优于参考）、−（劣于参考）、0（与参考相当）：

| 标准 | A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|---|
| Ease of Handling | 0 | 0 | − | 0 | 0 | − | − |
| Ease of Use | 0 | − | − | 0 | 0 | + | 0 |
| Number Readability | 0 | 0 | + | 0 | + | 0 | + |
| Dose Metering | + | + | + | + | + | 0 | + |
| Load Handling | 0 | 0 | 0 | 0 | 0 | + | 0 |
| Manufacturing Ease | + | − | − | 0 | 0 | − | 0 |
| Portability | + | + | − | − | 0 | − | − |
| **Pluses / Sames / Minuses** | 3/4/0 | 2/3/2 | 2/1/4 | 1/5/1 | 2/5/0 | 2/2/3 | 2/3/2 |
| **Net（+ 数 − − 数）** | 3 | 0 | −2 | 0 | 2 | −1 | 0 |
| **Rank** | 1 | 3 | 7 | 5 | 2 | 6 | 4 |
| **Continue?** | Yes | Yes | No | No | Yes | No | Yes |

净分（Net）= 加号数 − 减号数，直接决定排名；净分为负或明显落后的概念（C、F）以及并列靠后且无差异化优势的概念（D）被淘汰，A、B、E、G 四个概念进入下一轮评分。这里能看出筛选阶段的本质：**它只回答"谁明显更差"，不试图精确回答"谁更好多少"**——这正是为什么后面还需要评分阶段。

## 概念评分：加权量化排序

筛选后幸存的概念（课程实例中经过合并改进，变成 A/DF/E/G+ 四个概念，其中 DF 和 G+ 的命名本身就暗示了"合并"步骤已经发生——DF 大概率是概念 D 和 F 优点的组合，G+ 是在 G 基础上的改进版）进入评分阶段。评价标准不变，但每项标准被赋予权重（合计 100%），每个概念在每项标准上打 1–5 分（而非 +/−/0），加权分数 = 评分 × 权重，加权分数求和得总分：

| 标准 | 权重 | A（参考）Master Cylinder | DF Lever Stop | E Swash Ring | G+ Dial Screw+ |
|---|---|---|---|---|---|
| Ease of Handling | 5% | 3 → 0.15 | 3 → 0.15 | 4 → 0.20 | 4 → 0.20 |
| Ease of Use | 15% | 3 → 0.45 | 4 → 0.60 | 4 → 0.60 | 3 → 0.45 |
| Readability of Settings | 10% | 2 → 0.20 | 3 → 0.30 | 5 → 0.50 | 5 → 0.50 |
| Dose Metering Accuracy | 25% | 3 → 0.75 | 3 → 0.75 | 2 → 0.50 | 3 → 0.75 |
| Durability | 15% | 2 → 0.30 | 5 → 0.75 | 4 → 0.60 | 3 → 0.45 |
| Ease of Manufacture | 20% | 3 → 0.60 | 3 → 0.60 | 2 → 0.40 | 2 → 0.40 |
| Portability | 10% | 3 → 0.30 | 3 → 0.30 | 3 → 0.30 | 3 → 0.30 |
| **Total Score** | | **2.75** | **3.45** | **3.10** | **3.05** |
| **Rank** | | 4 | 1 | 2 | 3 |
| **Continue?** | | No | Develop | No | No |

结果：Lever Stop（DF）以 3.45 分明显领先，被选为唯一继续开发的概念；参考概念本身（Master Cylinder，充当行业基准的既有设计）反而排名最后，说明这次概念开发确实产生了优于基准的新方案——这是概念选择流程"成功"的标志，而不是选出一个和现状打平的概念。

值得注意两个方法论细节：

::: insight 参考概念的作用
参考概念（reference concept）在筛选和评分两个阶段中角色不同：筛选阶段它是全场唯一的比较基准（所有候选都相对它打分，它本身恒为 0）；评分阶段它作为候选之一直接参与排名（如上表中 A 就是参考概念，最终排名垫底）。这样设计的好处是团队始终有一个具体、已知的对象可以锚定判断，避免"凭感觉打绝对分"导致的评分漂移，同时评分阶段还能验证——如果连参考概念都打不过，说明这轮概念生成没有真正创造增量价值。
:::

::: pitfall 权重与评分的主观性
25% 的权重压在"Dose Metering Accuracy"上，20% 压在"Ease of Manufacture"，这两项合计接近总权重一半——权重设置本身就是一次隐含的战略判断（这里明显偏向医疗器械的安全性与可制造性，而非可携带性或外观）。课程在 Caveats 中明确要求检验选择结果对权重和评分的敏感度（sensitivity），因为像本例这样权重差异悬殊的矩阵，排名结果可能会随权重的小幅调整而反转，团队必须确认结论是稳健的，而不是被某一项权重的主观设定单方面决定。
:::

## Concept Selection Exercise：机械铅笔

课程用一组实拍的机械铅笔照片（摆成 "MIT RISD" 字样）作为课堂练习素材，并给出五款铅笔的零售价作为附加信息：Classic \$13.26、Side Fox \$2.55、Retro \$0.93、Plasma \$6.55、Flex Fit \$4.85。这组练习让学生亲手为真实产品套用筛选/评分矩阵，价格数据用于讨论"评价标准是否应该包含成本/性价比"，以及高价产品在功能类标准上未必占优时该如何权衡。

## 核心提醒：目标是开发，不是挑选

::: insight Remember…
课程用一整页强调这一点：概念选择的目标**不是（not）**从已有候选中"选出"最好的一个，而是**通过比较、拆解、重组来"开发出"最好的概念**。换句话说，矩阵打分只是诊断工具，真正创造价值的动作发生在"Combine and Improve"这一步——把 A 的可制造性优点和 F 的手感优点拼到一起，才可能产生比 A、F 单独都强的新概念（如实例中的 DF/Lever Stop）。如果团队把这一步简化为"打完分选最高的走人"，就丢掉了概念选择方法论里最有价值的部分。
:::

## 四条实操警示（Caveats）

1. **警惕"最优平均品"**：加权求和容易选出一个在每项标准上都不差、但没有任何一项突出的"平庸"概念，而不是有清晰差异化优势的概念——团队需要额外审视排名靠前的概念是否只是"各项都凑合"。
2. **对不同客户群体分别选择并比较**：不同细分客户对同一组标准的权重判断可能完全不同，用单一矩阵覆盖所有客户群体会掩盖这种差异，应分别跑一遍流程再比较结果是否一致。
3. **检验选择对权重与评分的敏感度**：调整权重或个别评分后重新计算，确认排名结论不是被某个主观判断单方面决定的（呼应上文 Dose Metering 25% 权重的例子）。
4. **决赛阶段可能需要展开为完整的细化需求**：粗粒度的评价标准（如"Ease of Use"）到了最终决策阶段可能不够精确，需要还原为更具体的详细规格（detailed requirements）来做最后比较；同时应记录哪些优点特征可以迁移应用到其他候选概念上，为后续迭代积累。

## 延伸阅读

Stuart Pugh，《Total Design》——概念筛选矩阵方法论的原始出处，文献中常称为 Pugh Matrix（Pugh 矩阵）。
