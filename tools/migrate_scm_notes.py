#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migrate MIT CTL.SC4x Supply Chain Technology and Systems
from /Users/mac/Documents/MIT/SupplyChainManagement/05-供应链技术与系统
into docs/zh/management/ops_mngt/ctl_sc4x_supply_chain_technology_and_systems/
Strictly conforming to NOTESTYLE.md.
"""

import os
import re

SRC_DIR = '/Users/mac/Documents/MIT/SupplyChainManagement/05-供应链技术与系统'
DEST_DIR = '/Users/mac/Documents/MIT/archipelago/docs/zh/management/ops_mngt/ctl_sc4x_supply_chain_technology_and_systems'

LECTURES_DATA = {
    1: {
        'title': '数据洪流与 CRISP-DM 方法论',
        'en_title': 'Looking to Data for Answers',
        'tags': ['crisp-dm', 'big-data', 'data-cleaning', 'business-analytics'],
        'tldr': [
            '现代供应链从经验驱动转向数据驱动，数据爆炸与脏数据、数据孤岛构成企业核心痛点。',
            'CRISP-DM 提供跨行业数据挖掘标准流程：商业理解、数据理解、数据准备、建模、评估与部署六大闭环。',
            '商业理解是决定数据分析成败的前提，严禁脱离供应链业务痛点盲目调用算法模型。',
        ],
        'insight': """::: insight 业务驱动而非算法驱动
在供应链数字化转型中，数据分析团队最容易犯的错误是“手握锤子找钉子”。现实中 80% 的模型失败并非算法不够先进，而是在商业理解阶段未能厘清真实的成本函数——例如未能准确量化缺货导致的市场份额永久损失，或是忽略了仓库现场物理动线的约束。坚持 CRISP-DM 的首要原则：模型目标必须由业务关键 KPI 倒推定义。
:::"""
    },
    2: {
        'title': '数据建模——关系模型、ER 图与键',
        'en_title': 'Data Modeling',
        'tags': ['data-modeling', 'relational-model', 'entity-relationship', 'primary-key'],
        'tldr': [
            '数据建模是将现实业务实体及其关联转化为规范化数据库物理模式的核心桥梁。',
            '关系模型以一阶谓词逻辑为基础，通过二维表（关系）、元组（行）与属性（列）组织结构化数据。',
            '主键确保实体唯一性，外键与基数约束（1:1、1:N、M:N）确保跨业务表引用完整性。',
        ],
        'insight': """::: insight 联结表解耦与多对多陷阱
在供应链核心业务流程中，“多对多（M:N）”关系无处不在——如一张采购订单可包含多个物料 SKU，而一个物料又会出现在多个订单中。初学者常犯的错误是在单表中堆叠冗余字段，这会引发更新异常与数据不一致。工程实践中必须通过联结表（Junction Table / Associative Entity）将其拆解为两个一对多关系，保证关系模式满足第三范式（3NF）。
:::"""
    },
    3: {
        'title': 'SQL 基础——数据类型、建库建表与 SELECT',
        'en_title': 'Database Queries',
        'tags': ['sql-basics', 'relational-database', 'ddl-statements', 'query-optimization'],
        'tldr': [
            '结构化查询语言（SQL）是提取与操作关系数据库的标准声明式语言。',
            'DDL 负责定义数据库架构（CREATE、ALTER、DROP）与字段精度（VARCHAR、INT、DECIMAL）。',
            'SELECT 基础语句通过列投影、算术运算与别名实现高效基础数据过滤与重构。',
        ],
        'insight': """::: insight 供应链数据精度的底层雷区
在设计物料价格、运费结算与高精度称重计量字段时，绝对不能使用 `FLOAT` 或 `REAL` 等浮点数类型。浮点数的二进制近似表示会在海量聚合运算中累积舍入误差，导致月底财务账目出现不可对齐的“神秘几分钱”。必须无条件选用定点数 `DECIMAL(M, D)` 或 `NUMERIC`，这是供应链与金融系统最基础的工程底线。
:::"""
    },
    4: {
        'title': 'SQL 进阶——条件、分组、排序与多表连接',
        'en_title': 'Database Conditional, Grouping, and Joins',
        'tags': ['sql-joins', 'aggregate-functions', 'group-by', 'query-filtering'],
        'tldr': [
            '进阶 SQL 通过 WHERE 条件表达式、ORDER BY 排序与 LIMIT 分页实现精准数据截取。',
            '聚合函数（SUM、AVG、COUNT）结合 GROUP BY 与 HAVING 实现多维度指标汇总与后验过滤。',
            '内连接（INNER JOIN）与左连接（LEFT JOIN）满足跨供应商、订单与物料表的复杂全景关联。',
        ],
        'insight': """::: insight 统计缺货率时的连接语义陷阱
在分析供应商履约表现时，新手分析师往往直接使用 `INNER JOIN` 将订单表与发货表关联。但这样会直接过滤掉“从未发货”的完全违约订单，导致计算出的供应商准时交付率（OTIF）被严重虚高美化。正确的做法是始终以全量订单表为基准使用 `LEFT JOIN`，并通过 `WHERE shipment_id IS NULL` 精准捕获违约记录。
:::"""
    },
    5: {
        'title': '数据库专题——索引、OLTP/OLAP、NoSQL 与数据清洗',
        'en_title': 'Topics in Databases',
        'tags': ['database-indexing', 'oltp-olap', 'nosql-databases', 'etl-pipeline'],
        'tldr': [
            'B 树索引大幅降低数据检索时间复杂度（$O(\log N)$），但需权衡高频写入下的维护开销。',
            'OLTP 侧重高并发事务一致性（ACID），OLAP 数据仓库与数据湖面向海量多维聚合分析。',
            '非结构化物联网数据依赖 NoSQL 弹性存储，ETL 数据清洗是下游分析质量的生命线。',
        ],
        'insight': """::: insight 读写分离与架构隔离原则
在大型电商与制造企业中，严禁允许数据分析师或 BI 报表直接连接承载实时交易的生产 OLTP 数据库执行大范围 `GROUP BY` 查询。一次未加索引的全表扫描足以锁死核心库存表，导致前端下单接口超时瘫痪。现代架构必须通过基于日志的变更数据捕获（CDC）将数据准实时异步写入 OLAP 列式数据库，实现交易与分析的物理级隔离。
:::"""
    },
    6: {
        'title': '机器学习导论——算法分类与模型质量',
        'en_title': 'Introduction to Machine Learning',
        'tags': ['machine-learning', 'supervised-learning', 'model-evaluation', 'train-test-split'],
        'tldr': [
            '机器学习通过数据驱动自动发现复杂非线性规律，分为监督学习、无监督学习与强化学习。',
            '模型质量评估区分回归指标（RMSE、MAE、MAPE）与分类指标（精确率、召回率、F1 分数、ROC-AUC）。',
            '严防过拟合（Overfitting），通过训练集/验证集/测试集严格划分与交叉验证确保模型泛化能力。',
        ],
        'insight': """::: insight 非对称损失下的损失函数定制
统计学标准评估通常采用均方根误差（RMSE），它假设正负预测误差对业务的惩罚是均等的。但在供应链管理中，高估需求带来的库存持有成本与低估需求导致的产线停工、客户流失成本存在数量级的差距。资深算法工程师必须结合具体品类特性设计非对称加权损失函数（如 Pinball Loss 或自定义成本矩阵），使算法的优化方向与企业财务风险完全共振。
:::"""
    },
    7: {
        'title': '机器学习算法——降维、PCA、聚类与分类',
        'en_title': 'Machine Learning Algorithms',
        'tags': ['principal-component-analysis', 'kmeans-clustering', 'decision-trees', 'random-forest'],
        'tldr': [
            '主成分分析（PCA）通过正交变换实现高维特征降维，化解维度灾难并消除多重共线性。',
            'K-Means 聚类无监督识别客户群体与物料分类，肘部法则与轮廓系数指导最优簇数选取。',
            '决策树与随机森林（Random Forest）集成算法在物流履约时效预测与供应商违约风险评估中表现卓越。',
        ],
        'insight': """::: insight 量纲归一化是距离度量的生命线
在将 K-Means 聚类应用于物料分类（如同时输入 SKU 年出货金额数百万元与出货频次几十次）时，若不进行标准化，欧氏距离计算将被数值庞大的金额特征完全主导，频次特征几乎彻底失效。在调用任何基于距离度量的聚类与降维算法前，必须先执行 Z-Score 标准化（StandardScaler），避免伪相关的失真聚类结果。
:::"""
    },
    8: {
        'title': '供应链信息系统——ERP',
        'en_title': 'Supply Chain Systems - ERP',
        'tags': ['enterprise-resource-planning', 'master-data', 'business-processes', 'mrpii-logic'],
        'tldr': [
            'ERP 是企业运营的核心中枢，打破部门信息壁垒，实现财务、供应链与生产数据的单一真理源。',
            '主数据管理（物料主数据、BOM、工艺路线）是 ERP 稳定运行的基石，直接决定 MRP 准确性。',
            '物料需求计划（MRP）逻辑将独立需求通过 BOM 逐级展开为相关需求，生成采购与生产指令。',
        ],
        'insight': """::: insight “垃圾进，垃圾出”与主数据治理
许多企业花费千万资金实施 SAP 或 Oracle ERP 却未能提升周转率，根源往往不在软件本身，而在于物料主数据（Master Data）的极其混乱——例如同一规格轴承在不同车间有五个不同编码、BOM 层级配比错误或提前期（Lead Time）未随季节更新。ERP 本质上是一个确定性的确定性推理机；主数据治理如果不到位，ERP 只会以更高效率加速制造错误。
:::"""
    },
    9: {
        'title': '供应链信息系统——APS、TMS 与 MES',
        'en_title': 'Supply Chain Systems - Supply Chain Modules',
        'tags': ['advanced-planning-systems', 'transportation-management', 'manufacturing-execution', 'warehouse-execution'],
        'tldr': [
            'APS 基于有限产能约束与全局优化算法，弥补传统 ERP/MRP 无限产能假设的计划短板。',
            'TMS 聚焦干线与配送运输路线优化、配载拼车（Consolidation）及承运商运费核结算。',
            'MES 直连生产制造车间设备，实现工单排产、在制品追踪（WIP）与质量溯源实时闭环。',
        ],
        'insight': """::: insight 核心业务系统集成中的“数据时延断层”
在复杂企业 IT 架构中，ERP（偏宏观计划）、APS（偏战术调度）与 MES/TMS（偏现场执行）往往来自不同软件厂商。最容易产生系统性混乱的地方在于接口的同步频率。若 MES 的完工报工每日才批处理同步一次到 ERP，而 APS 却在按小时重新计算计划，那么计划系统将永远依据过时的假象做决策。必须采用事件驱动的实时集成中间件保障状态同步。
:::"""
    },
    10: {
        'title': '仓储管理——仓库类型、核心作业与绩效评估',
        'en_title': 'Warehousing Operations',
        'tags': ['warehouse-operations', 'order-picking', 'slotting-optimization', 'warehouse-kpi'],
        'tldr': [
            '仓储兼具库存缓冲、订单拼装（Consolidation）与延迟制造（Postponement）等多元战略职能。',
            '核心作业涵盖收货验收、上架存储、拣选分拣（Picking）与出库，拣货占总人工作业成本 50% 以上。',
            '货位优化（Slotting）依据 SKU 动销率（ABC 分类）与关联度布局，核心衡量准时率与拣货准确率。',
        ],
        'insight': """::: insight 货位动态优化与死区消除
很多传统仓库的货位分配是静态的，导致新入库的爆款商品被放置在仓库最深处的死角，迫使拣选工每天徒增数万步无效行走。现代高绩效 WMS 必须具备“动态货位重排（Dynamic Re-slotting）”能力，每周甚至每天分析订单相关性（Market Basket Analysis），将高频关联 SKU（如洗发水与护发素）就近安放在靠近打包台的黄金拣选面，从而系统性压缩拣选动线。
:::"""
    },
    11: {
        'title': '供应链可视性',
        'en_title': 'Supply Chain Visibility',
        'tags': ['supply-chain-visibility', 'track-and-trace', 'control-tower', 'rfid-technology'],
        'tldr': [
            '供应链可视性指跨多级节点实时追踪货物状态、在途位置、库存水平及突发异常的洞察能力。',
            '自动识别与数据采集技术（条码、RFID、GPS、IoT 传感器）为供应链透明化提供底层感知。',
            '供应链控制塔（Control Tower）整合端到端数据，赋能从被动事后告警跃升为前瞻预测与自主处置。',
        ],
        'insight': """::: insight 可视性若无执行闭环便毫无价值
许多企业投入巨资搭建大屏幕控制塔（Control Tower），看板上闪烁着实时的在途货车 GPS 轨迹与各港口拥堵指数。但当系统发出“苏伊士运河突发拥堵”的告警时，企业却没有任何预案去调整后续批次的订货或空运备选。可视性仅仅是信息的透传，真正的竞争力在于将监控指标与自动化调度决策引擎强绑定，实现“感知—决策—执行”的闭环自动化响应。
:::"""
    },
    12: {
        'title': '软件选型与实施',
        'en_title': 'Software Selection & Implementation',
        'tags': ['software-selection', 'rfp-process', 'total-cost-of-ownership', 'change-management'],
        'tldr': [
            '企业级软件选型遵循严格流程：需求定义、RFI/RFP 编制、供应商演示、概念验证（POC）与谈判。',
            '总体拥有成本（TCO）除初始许可费外，必须充分计入二次开发、数据迁移、云资源及长期运维开销。',
            '实施核心风险在于组织变革阻力与流程定制泛滥，倡导“尽量调整业务适应标准系统”而非深度二开。',
        ],
        'insight': """::: insight 定制化诅咒（Customization Trap）
在供应链软件实施中，企业管理层最常见的失误是试图让软件 100% 复制过去的纸质或 Excel 工作习惯，要求厂商做成百上千处定制化开发。这不仅导致项目交付工期严重延宕、预算翻倍，而且在未来系统升级时会陷入巨大的维护深渊。除非某项特有流程是企业不可替代的垄断核心优势，否则应当坚定利用成熟商用软件的“最佳业务实践（Best Practice）”倒逼企业组织流程再造。
:::"""
    },
    13: {
        'title': '供应链自动化',
        'en_title': 'Supply Chain Automation',
        'tags': ['warehouse-automation', 'autonomous-mobile-robots', 'asrs-systems', 'automation-roi'],
        'tldr': [
            '自动化技术涵盖高密度立库（AS/RS）、自主移动机器人（AMR/AGV）、机械臂码垛与输送分拣线。',
            '自动化投资决策建立在严谨的现金流折现与回收期（Payback Period）测算上，权衡灵活性与通量。',
            '“货到人”（Goods-to-Person）模式彻底消除人工无效行走，极大提升高峰期拣选吞吐韧性与人效。',
        ],
        'insight': """::: insight 刚性自动化与柔性自动化的权衡
过去许多企业盲目追求巨型钢结构 AS/RS 穿梭车立体库，结果在几年后产品包装规格或业务形态突变时，数亿元建成的立库由于缺乏空间柔性而成为沉没包袱。当下智能仓储的演进趋势正明显转向模块化、可按需扩缩容的自主移动机器人（AMR）与料箱搬运机器人。在规划自动化投资时，“系统应对业务波动的适应柔性”其权重往往高于单点最高理论通量。
:::"""
    }
}

def clean_body(raw_text, lec_num):
    # Strip existing top heading and source quote
    lines = raw_text.split('\n')
    idx = 0
    # skip title lines
    while idx < len(lines) and (lines[idx].startswith('# ') or lines[idx].startswith('>') or lines[idx].strip() == '' or lines[idx].strip() == '---'):
        idx += 1
    remaining = '\n'.join(lines[idx:]).strip()

    # Fix vague headings
    if lec_num == 13:
        remaining = re.sub(r'^##\s+1\.\s+引言\s*$', '## 1. 供应链自动化演进背景与核心概念', remaining, flags=re.M)

    # Fix code blocks without language
    # Replace opening ```\n with ```text\n
    def replace_fence(m):
        code_all = m.group(0)
        # if language is missing
        if m.group(1) == '':
            return f"```text\n{m.group(2)}```"
        return code_all

    remaining = re.sub(r'```([a-zA-Z0-9_-]*)\n([\s\S]*?)```', replace_fence, remaining)

    # Fix multiple blank lines (3 or more \n to 2 \n)
    remaining = re.sub(r'\n{3,}', '\n\n', remaining)

    return remaining

def main():
    os.makedirs(DEST_DIR, exist_ok=True)
    
    # 1. Generate index.md
    index_path = os.path.join(DEST_DIR, 'index.md')
    index_content = """---
title: CTL.SC4x 供应链技术与系统 (Supply Chain Technology and Systems)
type: course
course: CTL.SC4x 供应链技术与系统 (Supply Chain Technology and Systems)
course_id: CTL.SC4x
tags: [supply-chain-systems, database-modeling, enterprise-resource-planning, supply-chain-analytics]
status: complete
source: 'https://mitxonline.mit.edu/courses/course-v1:MITxT+CTL.SC4x/'
---

# CTL.SC4x 供应链技术与系统 (Supply Chain Technology and Systems)

> MIT Center for Transportation & Logistics · MITx MicroMasters SCM · 课号 CTL.SC4x / 15.762J

## TL;DR

- 现代供应链从经验驱动转向数据与算法驱动，技术与信息系统是企业高效低成本运转的基础设施。
- 贯穿数据建模、SQL 查询、机器学习、企业核心系统（ERP/APS/TMS/MES/WMS）全链路技术架构。
- 深入探讨供应链端到端可视性监控、企业级软件科学选型实施方法论与现代仓储自动化前沿演进。

## 课程体系与讲义目录

本课程包含 13 篇长篇系统讲义，从底层数据技术到上层企业系统与前沿自动化全面展开：

| 讲次 | 讲义标题 | 英文主题 | 核心内容焦点 |
| :--- | :--- | :--- | :--- |
| [Lec 1](./lec1.md) | 数据洪流与 CRISP-DM 方法论 | Looking to Data for Answers | 大数据挑战与跨行业数据挖掘标准流程 |
| [Lec 2](./lec2.md) | 数据建模——关系模型、ER 图与键 | Data Modeling | 实体属性、关系模型、主外键与基数约束 |
| [Lec 3](./lec3.md) | SQL 基础——数据类型、建库建表与 SELECT | Database Queries | DDL 架构设计、数据类型精度与基础查询 |
| [Lec 4](./lec4.md) | SQL 进阶——条件、分组、排序与多表连接 | Joins and Grouping | 条件过滤、聚合函数、GROUP BY 与多表关联 |
| [Lec 5](./lec5.md) | 数据库专题——索引、OLTP/OLAP、NoSQL 与数据清洗 | Topics in Databases | 索引优化、读写分离、NoSQL 与 ETL 数据清洗 |
| [Lec 6](./lec6.md) | 机器学习导论——算法分类与模型质量 | Introduction to ML | 监督与无监督学习、过拟合防范与评估指标 |
| [Lec 7](./lec7.md) | 机器学习算法——降维、PCA、聚类与分类 | ML Algorithms | PCA 正交降维、K-Means 聚类与随机森林分类 |
| [Lec 8](./lec8.md) | 供应链信息系统——ERP | Supply Chain ERP | 企业资源计划、主数据治理与 MRP 展开逻辑 |
| [Lec 9](./lec9.md) | 供应链信息系统——APS、TMS 与 MES | Execution Systems | 有限产能高级计划、运输管理与车间执行系统 |
| [Lec 10](./lec10.md) | 仓储管理——仓库类型、核心作业与绩效评估 | Warehousing Operations | 仓储职能、动线优化、货位 Slotting 与作业 KPI |
| [Lec 11](./lec11.md) | 供应链可视性 | Supply Chain Visibility | 自动识别感知技术、控制塔建设与前瞻处置 |
| [Lec 12](./lec12.md) | 软件选型与实施 | Software Selection & Implementation | RFP 采购流程、总体拥有成本与变革管理 |
| [Lec 13](./lec13.md) | 供应链自动化 | Supply Chain Automation | AS/RS 立库、AMR/AGV 柔性机器人与货到人拣选 |

## 学习建议与知识路径

1. **技术底座（Lec 1 ~ Lec 5）**：重点打通从业务理解到关系数据库与 SQL 进阶分析的工程能力，建立严谨的数据思维。
2. **算法赋能（Lec 6 ~ Lec 7）**：掌握降维、聚类与分类算法在物料分类、履约时效预测与违约风控中的实战应用。
3. **企业中枢（Lec 8 ~ Lec 10）**：理解 ERP、APS、TMS、MES 与 WMS 各系统间的边界与数据流转契约，掌握主数据治理原则。
4. **管理与前沿（Lec 11 ~ Lec 13）**：从企业高层视角审视全局可视性控制塔、IT 投资决策与柔性自动化转型演进。

---

本课程笔记整理自 MIT CTL.SC4x 官方课件与讲义材料，遵循 Creative Commons BY-NC-SA 4.0 许可协议。
"""
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    print(f'Created {index_path}')

    # 2. Process each lec1.md to lec13.md
    for num in range(1, 14):
        src_file = os.path.join(SRC_DIR, f'lec{num}.md')
        if not os.path.exists(src_file):
            print(f'[WARN] Missing source {src_file}')
            continue
            
        spec = LECTURES_DATA[num]
        raw_text = open(src_file, 'r', encoding='utf-8').read()
        body_content = clean_body(raw_text, num)
        
        # Build frontmatter
        fm_title = spec['title']
        tags_str = ', '.join(spec['tags'])
        tldr_bullets = '\n'.join([f'- {b}' for b in spec['tldr']])
        h1_line = f"# Lec {num} {spec['title']}（{spec['en_title']}）"
        
        insight_block = spec['insight']
        
        new_content = f"""---
title: {fm_title}
type: lecture
lecture: {num}
tags: [{tags_str}]
status: complete
source: 'https://mitxonline.mit.edu/courses/course-v1:MITxT+CTL.SC4x/'
---

{h1_line}

> 对应 MIT CTL.SC4x · Supply Chain Technology and Systems · 第 {num} 讲  
> 核心参考：*SC4x Key Concept Document* (Summer 2019) & MITx MicroMasters SCM 课程大纲

## TL;DR

{tldr_bullets}

{insight_block}

{body_content}
"""
        dest_file = os.path.join(DEST_DIR, f'lec{num}.md')
        with open(dest_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Migrated and standardized {dest_file}')

    print('Successfully processed CTL.SC4x!')

if __name__ == '__main__':
    main()
