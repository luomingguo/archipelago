#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migrate external MIT Course 15 course outlines from /Users/mac/Documents/courses/
and /Users/mac/Documents/MIT/15_Marketing/ into docs/zh/management/<group>/<course_slug>/index.md
Strictly adhering to NOTESTYLE.md:
- title, type: course, course, course_id, tags, status: stub, source
- Unique ## TL;DR as first H2 (3-5 bullets, 80-350 chars)
- Preserves full description, syllabus, lecture notes list, and OCW links.
"""

import os
import re
import sys

BASE_REPO = '/Users/mac/Documents/MIT/archipelago'
DOCS_MGMT = os.path.join(BASE_REPO, 'docs/zh/management')
BASE_COURSES = '/Users/mac/Documents/courses'
BASE_MKT = '/Users/mac/Documents/MIT/15_Marketing'

GROUP_NAMES = {
    'acct': 'Accounting · 会计学',
    'comm': 'Communication · 沟通与传播',
    'emba': 'Executive MBA · 高管工商管理硕士',
    'finance': 'Finance · 金融学',
    'global_econ': 'Global Economics & Management · 全球经济与管理',
    'info_tech': 'Information Technologies · 信息技术',
    'law': 'Law · 法律',
    'managerial_econ': 'Managerial Economics · 管理经济学',
    'mkt': 'Marketing · 市场营销',
    'ops_mngt': 'Operations Management · 运营管理',
    'or_stats': 'Operations Research/Statistics · 运筹与统计',
    'org_studies': 'Work and Organizational Studies · 工作与组织研究',
    'strat_mngt': 'Strategic Management · 战略管理',
    'tech_innov': 'Technology, Innovation, and Entrepreneurship · 技术、创新与创业',
    'sys_dyn': 'System Dynamics · 系统动力学',
}

# Detailed metadata for each course
COURSES_SPEC = {
    # ── acct 会计学 ──
    '15.501': {
        'group': 'acct',
        'dir_name': '15501_corporate_financial_accounting',
        'zh_title': '企业财务会计',
        'en_title': 'Corporate Financial Accounting',
        'tags': ['financial-accounting', 'corporate-reporting', 'accrual-accounting'],
        'tldr': [
            '财务报表是企业经济活动与外部利益相关者的核心信息桥梁，遵循权责发生制与会计恒等式。',
            '资产负债表反映财务状况存量，利润表衡量经营业绩流量，现金流量表揭示资金流动性真实性。',
            '通过会计政策选择与应计项分析，识别管理层盈余管理动机并评估企业收益质量。',
        ]
    },
    '15.511': {
        'group': 'acct',
        'dir_name': '15511_financial_accounting',
        'zh_title': '财务会计基础',
        'en_title': 'Financial Accounting',
        'tags': ['financial-accounting', 'balance-sheet', 'income-statement', 'cash-flow'],
        'tldr': [
            '系统掌握以通用会计准则（GAAP）为基础的复式记账法与三大财务报表编制逻辑。',
            '重点剖析收入确认、存货计价（FIFO/LIFO）及长期资产折旧摊销对利润分配的影响。',
            '从报表使用者视角拆解企业流动性风险、长期偿债能力与资产营运效率。',
        ]
    },
    '15.515': {
        'group': 'acct',
        'dir_name': '15515_financial_accounting',
        'zh_title': '研究生财务会计',
        'en_title': 'Financial Accounting',
        'tags': ['financial-accounting', 'revenue-recognition', 'deferred-taxes', 'leasings'],
        'tldr': [
            '面向 MBA 与管理研究生的财务报告进阶体系，侧重复杂经济交易的会计确认与计量。',
            '深入探讨递延所得税资产与负债、经营租赁与融资租赁表外化、金融资产公允价值计量。',
            '建立依据财务比率分解（DuPont 分析法）评估企业净资产收益率驱动因素的分析框架。',
        ]
    },
    '15.518': {
        'group': 'acct',
        'dir_name': '15518_taxes_and_business_strategy',
        'zh_title': '税收与商业战略',
        'en_title': 'Taxes and Business Strategy',
        'tags': ['tax-strategy', 'corporate-taxation', 'business-structuring', 'after-tax-returns'],
        'tldr': [
            '税收筹划是企业顶层商业架构与投融资决策不可分割的核心变量，追求税后净收益最大化。',
            '运用微观经济学框架分析多方契约中的税收套利机会、组织形式选择及跨国转让定价。',
            '评估企业并购重组、股权激励方案以及资产处置中的显性税负与隐性税负权衡。',
        ]
    },
    '15.521': {
        'group': 'acct',
        'dir_name': '15521_accounting_information_for_decision_makers',
        'zh_title': '决策者会计信息',
        'en_title': 'Accounting Information for Decision Makers',
        'tags': ['managerial-accounting', 'activity-based-costing', 'variance-analysis', 'budgeting'],
        'tldr': [
            '管理会计聚焦企业内部资源配置与战略控制，打破传统财务报表合规性限制。',
            '作业成本法（ABC）与本量利分析（CVP）为产品定价、客户盈利能力及外包决策提供精准边际依据。',
            '通过全面预算编制、责任会计中心与标准成本差异分析实现组织运营闭环反馈。',
        ]
    },
    '15.535': {
        'group': 'acct',
        'dir_name': '15535_business_analysis_using_financial_statements',
        'zh_title': '基于财务报表的商业分析',
        'en_title': 'Business Analysis Using Financial Statements',
        'tags': ['financial-statement-analysis', 'equity-valuation', 'credit-risk', 'accounting-quality'],
        'tldr': [
            '融合行业竞争战略、会计质量甄别、财务比率预测与股权估值的四步商业分析范式。',
            '通过调整非经常性损益与消除激进会计估计，重构真实的自由现金流与经济增加值（EVA）。',
            '将财务分析深度应用于股票估值、杠杆收购（LBO）、信用违约评级与困境重组决策。',
        ]
    },

    # ── comm 沟通与传播 ──
    '15.276': {
        'group': 'comm',
        'dir_name': '15276_communicating_with_data',
        'zh_title': '数据沟通与可视化表达',
        'en_title': 'Communicating with Data',
        'tags': ['data-visualization', 'visual-storytelling', 'executive-presentation'],
        'tldr': [
            '数据沟通的核心在于将复杂量化分析提炼为驱动高管决策的清晰叙事与行动方案。',
            '遵循认知感知原则设计统计图表，避免图表垃圾，提升信息信噪比与关键洞察传达效率。',
            '构建从数据发现、假设验证到逻辑论证的完整管理层汇报架构与互动应对策略。',
        ]
    },
    '15.279': {
        'group': 'comm',
        'dir_name': '15279_management_communication_for_undergraduates',
        'zh_title': '本科生管理沟通',
        'en_title': 'Management Communication for Undergraduates',
        'tags': ['management-communication', 'business-writing', 'oral-presentation', 'persuasion'],
        'tldr': [
            '管理沟通是未来技术领导者必备的核心软实力，涵盖商务写作、口头演讲与团队协作。',
            '掌握金字塔原理与受众中心法则，撰写结构严密、导向明确的管理备忘录与商业提案。',
            '通过即席演讲录像复盘与高压问答演练，建立自信清晰的专业商务表达气场。',
        ]
    },
    '15.281': {
        'group': 'comm',
        'dir_name': '15281_advanced_leadership_communication',
        'zh_title': '卓越领导力沟通',
        'en_title': 'Advanced Leadership Communication',
        'tags': ['leadership-communication', 'crisis-communication', 'executive-presence', 'strategic-messaging'],
        'tldr': [
            '聚焦高管在组织变革、危机应对与利益相关者冲突中的战略性信息传递与愿景塑造。',
            '剖析信任重建、共情叙事与道德领导力的互动机制，在不确定性情境下凝聚组织共识。',
            '掌握媒体应对、全员沟通（Town Hall）与董事会博弈中的关键修辞与非语言表达策略。',
        ]
    },
    '15.289': {
        'group': 'comm',
        'dir_name': '15289_communication_skills_for_academics',
        'zh_title': '学者学术沟通技巧',
        'en_title': 'Communication Skills for Academic Success',
        'tags': ['academic-writing', 'conference-presentation', 'peer-review', 'scholarly-communication'],
        'tldr': [
            '面向跨学科研究人员的学术成果传播指南，涵盖顶级期刊论文撰写与学术会议答辩。',
            '提炼科学研究的核心贡献点与研究方法论，克服知识诅咒，实现跨领域清晰阐述。',
            '提升同行评议回复、科研基金申请（Grant Proposal）及教职求职汇报的专业说服力。',
        ]
    },

    # ── emba 高管工商管理硕士 ──
    '15.726': {
        'group': 'emba',
        'dir_name': '15726_pricing',
        'zh_title': '战略定价决策',
        'en_title': 'Pricing',
        'tags': ['pricing-strategy', 'willingness-to-pay', 'price-discrimination', 'value-based-pricing'],
        'tldr': [
            '定价是企业盈利杠杆中最敏锐的要素，需从成本加成转向以客户支付意愿为核心的价值定价。',
            '运用一、二、三级价格歧视、动态差别定价、版本划分（Versioning）与捆绑销售机制捕获消费者剩余。',
            '结合博弈论评估行业价格战风险，并在双边平台与订阅经济模式下优化长期客户生命周期价值。',
        ]
    },
    '15.732': {
        'group': 'emba',
        'dir_name': '15732_marketing_management',
        'zh_title': 'EMBA 营销管理',
        'en_title': 'Marketing Management',
        'tags': ['marketing-management', 'market-positioning', 'customer-centricity', 'strategic-marketing'],
        'tldr': [
            '面向企业高管的系统性营销战略设计，统筹 5C 市场环境分析与 STP 核心定位法则。',
            '深度整合产品生命周期管理、全渠道分销策略与品牌溢价塑造，实现差异化竞争护城河。',
            '在数字化浪潮中平衡短期获客转化与长期品牌资产沉淀，驱动可持续业务增长。',
        ]
    },
    '15.734': {
        'group': 'emba',
        'dir_name': '15734_introduction_to_operations_management',
        'zh_title': 'EMBA 运营管理导论',
        'en_title': 'Introduction to Operations Management',
        'tags': ['operations-strategy', 'process-analysis', 'supply-chain-risk', 'bottleneck-theory'],
        'tldr': [
            '从企业最高经营层视角审视运营流程架构，将运营卓越性转化为战略竞争壁垒。',
            '运用利特尔法则（Little\'s Law）、瓶颈识别与排队论优化端到端服务与制造周转效率。',
            '评估全球供应链韧性、柔性产能投资与突发中断风险下的多情景应急决策。',
        ]
    },

    # ── finance 金融学 ──
    '15.401': {
        'group': 'finance',
        'dir_name': '15401_managerial_finance',
        'zh_title': '管理金融学与金融理论 I',
        'en_title': 'Managerial Finance',
        'tags': ['capital-budgeting', 'net-present-value', 'portfolio-theory', 'capm'],
        'tldr': [
            '现代公司金融与资产定价的基石框架，确立以净现值（NPV）和现金流贴现为核心的价值评估准则。',
            '均值-方差投资组合理论与资本资产定价模型（CAPM）揭示了系统性风险与预期收益的量化对应关系。',
            '涵盖固定收益证券期限结构分析、有效市场假说（EMH）及衍生品初步定价机制。',
        ]
    },
    '15.402': {
        'group': 'finance',
        'dir_name': '15402_corporate_finance',
        'zh_title': '公司金融理论 II',
        'en_title': 'Corporate Finance',
        'tags': ['capital-structure', 'modigliani-miller', 'wacc', 'mergers-acquisitions'],
        'tldr': [
            '深入探讨企业资本结构与资本成本，剖析 MM 定理、税收盾效应与财务困境成本的权衡机制。',
            '综合加权平均资本成本（WACC）与调整现值法（APV）评估高度杠杆化项目与战略投资价值。',
            '全面覆盖企业并购重组（M&A）、杠杆收购（LBO）、破产重整与股利分配政策的博弈实务。',
        ]
    },
    '15.414': {
        'group': 'finance',
        'dir_name': '15414_financial_management',
        'zh_title': '财务管理学',
        'en_title': 'Financial Management',
        'tags': ['corporate-valuation', 'cash-flow-forecasting', 'working-capital', 'cost-of-capital'],
        'tldr': [
            '面向管理者的实用财务分析工具箱，贯穿营运资金管理、自由现金流预测与资本预算。',
            '运用敏感性分析与蒙特卡洛情景模拟评估高不确定性商业投资项目的财务可行性。',
            '建立规范的公司估值模型，深入理解企业生命周期演进与外部股权债权融资工具的匹配。',
        ]
    },
    '15.426J': {
        'group': 'finance',
        'dir_name': '15426j_real_estate_finance_and_investment',
        'zh_title': '房地产金融与投资',
        'en_title': 'Real Estate Finance and Investment',
        'tags': ['real-estate-finance', 'commercial-real-estate', 'mortgage-backed-securities', 'reits'],
        'tldr': [
            '商业地产资产的估值模型、资本化率（Cap Rate）测算与杠杆投资现金流瀑布结构。',
            '按揭抵押贷款结构设计、违约与提前偿还风险建模，以及抵押贷款支持证券（MBS）证券化机制。',
            '分析房地产投资信托基金（REITs）的公开市场运作与私人私募地产基金的激励契约。',
        ]
    },
    '15.431': {
        'group': 'finance',
        'dir_name': '15431_entrepreneurial_finance_and_venture_capital',
        'zh_title': '创业金融与风险投资',
        'en_title': 'Entrepreneurial Finance and Venture Capital',
        'tags': ['venture-capital', 'entrepreneurial-finance', 'term-sheet', 'valuation-methods'],
        'tldr': [
            '初创企业全生命周期的资本运作机制，涵盖天使轮、风投（VC）机构化融资与战略退出。',
            '投资意向书（Term Sheet）深度博弈：优先清算权、防稀释条款、董事会席位与创始人既得权。',
            '初创企业特殊估值法（分阶段里程碑估值、风险投资法与可转债结构）与上市（IPO）机制。',
        ]
    },
    '15.433': {
        'group': 'finance',
        'dir_name': '15433_financial_markets',
        'zh_title': '金融市场与投资学',
        'en_title': 'Financial Markets',
        'tags': ['asset-pricing', 'factor-investing', 'market-microstructure', 'derivatives'],
        'tldr': [
            '全球金融市场架构与资产配置理论，涵盖多因子资产定价模型（Fama-French）与异象回测。',
            '债券收益率曲线拟合、久期与凸性对冲，以及利率期限结构模型的实务应用。',
            '期权与期货定价逻辑（Black-Scholes-Merton），及高频交易环境下的市场微观结构与流动性风险。',
        ]
    },
    '15.450': {
        'group': 'finance',
        'dir_name': '15450_analytics_of_finance',
        'zh_title': '金融量化分析',
        'en_title': 'Analytics of Finance',
        'tags': ['quantitative-finance', 'stochastic-calculus', 'risk-management', 'monte-carlo'],
        'tldr': [
            '运用随机微积分、偏微分方程与数值算法构建连续时间资产定价与动态对冲模型。',
            '蒙特卡洛模拟与有限差分法在美式期权、奇异衍生品与结构化产品定价中的工程化实现。',
            '基于历史模拟与极值理论的在险价值（VaR）与预期亏损（CVaR）全面风险管理体系。',
        ]
    },
    '15.483': {
        'group': 'finance',
        'dir_name': '15483_consumer_finance_and_fintech',
        'zh_title': '消费金融与金融科技',
        'en_title': 'Consumer Finance and FinTech',
        'tags': ['fintech', 'consumer-finance', 'credit-scoring', 'robo-advising'],
        'tldr': [
            '数字化浪潮下个人借贷、财富管理、移动支付与保险科技（InsurTech）的商业重塑。',
            '大数据与机器学习算法在个人信用评分模型、反欺诈风控与合规审查中的应用与偏见纠正。',
            '智能投顾算法底层逻辑、监管科技（RegTech）边界及普惠金融政策平衡。',
        ]
    },

    # ── global_econ 全球经济与管理 ──
    '15.223': {
        'group': 'global_econ',
        'dir_name': '15223_global_markets_national_policies',
        'zh_title': '全球市场、国家政策与企业竞争优势',
        'en_title': 'Global Markets, National Policies and the Competitive Advantages of Firms',
        'tags': ['global-strategy', 'geopolitics', 'multinational-corporations', 'trade-policy'],
        'tldr': [
            '跨国企业在全球化退潮与地缘政治竞争重构中的战略定位与国家风险评估。',
            '产业政策、关税壁垒、外商直接投资（FDI）规制与跨国企业非市场战略（Non-market Strategy）。',
            '结合比较优势理论与制度经济学，构建兼顾本地响应与全球一体化的全球价值链网络。',
        ]
    },
    '15.224J': {
        'group': 'global_econ',
        'dir_name': '15224j_global_business_of_quantum_computing',
        'zh_title': '量子计算全球商业战略',
        'en_title': 'Global Business of Quantum Computing',
        'tags': ['quantum-computing', 'deep-tech-strategy', 'technology-geopolitics', 'emerging-ecosystems'],
        'tldr': [
            '颠覆性深科技量子计算从实验室走向商业化落地的全球生态系统与战略图景。',
            '分析量子计算在密码学破坏、金融高频优化、新药研发及材料科学中的经济价值释放周期。',
            '国家安全博弈、出口管制、主权量子投资与科技巨头平台标准争夺战的战略推演。',
        ]
    },
    '15.225': {
        'group': 'global_econ',
        'dir_name': '15225_modern_economy_and_business_in_china',
        'zh_title': '当代中国经济与商业',
        'en_title': 'Modern Economy and Business in China',
        'tags': ['chinese-economy', 'state-capitalism', 'emerging-markets', 'industrial-policy'],
        'tldr': [
            '系统复盘改革开放以来中国经济增长的制度动能、地方政府锦标赛与金融体制演变。',
            '国有企业、民营经济与跨国合资在新能源、硬科技与消费互联网赛道的竞合格局。',
            '双循环格局下的人口结构转型、供应链重塑、监管政策逻辑及全球商业竞合影响。',
        ]
    },
    '15.232': {
        'group': 'global_econ',
        'dir_name': '15232_breakthrough_ventures_in_frontier_markets',
        'zh_title': '前沿市场突破性商业模式',
        'en_title': 'Breakthrough Ventures: Effective Business Models in Frontier Markets',
        'tags': ['frontier-markets', 'inclusive-business', 'frugal-innovation', 'social-impact'],
        'tldr': [
            '在基础设施缺乏、制度空缺（Institutional Voids）的发展中与前沿市场探索盈利商业模式。',
            '金字塔底层（BOP）市场的极简创新、本地化逆向创新与最后一公里分销网络攻坚。',
            '将社会效益、公共卫生普惠与财务自负盈亏机制深度绑定的可持续商业闭环设计。',
        ]
    },
    '15.235': {
        'group': 'global_econ',
        'dir_name': '15235_blockchain_and_money',
        'zh_title': '区块链与货币',
        'en_title': 'Blockchain and Money',
        'tags': ['blockchain', 'cryptocurrency', 'central-bank-digital-currency', 'decentralized-finance'],
        'tldr': [
            'Gary Gensler 讲授的经典加密经济学课程，从法币历史与支付结算演进切入中本聪共识。',
            '剖析比特币、以太坊智能合约、公链安全机制与稳定币的货币经济学本质。',
            '全面评估央行数字货币（CBDC）、去中心化金融（DeFi）应用场景及全球证券法律监管红线。',
        ]
    },

    # ── info_tech 信息技术 ──
    '15.561': {
        'group': 'info_tech',
        'dir_name': '15561_digital_revolution_foundations_to_future',
        'zh_title': '数字革命：基础理论与未来趋势',
        'en_title': 'Digital Revolution: From Foundations to Future Trends',
        'tags': ['digital-transformation', 'information-architecture', 'network-effects', 'cloud-infrastructure'],
        'tldr': [
            '解构推动现代商业变革的底层信息技术架构，从计算机硬件演进到分布式云原生计算。',
            '网络外部性、两边市场与边际成本递减规律如何共同塑造数字经济中的垄断与生态竞争。',
            '面向技术领导者的架构选型方法论，权衡遗留系统技术债务与前沿技术采纳窗口。',
        ]
    },
    '15.568': {
        'group': 'info_tech',
        'dir_name': '15568_practical_information_technology_management',
        'zh_title': 'IT 实践管理与技术领导力',
        'en_title': 'The Art of Leading: Experiencing Leadership in Practice',
        'tags': ['it-management', 'cio-leadership', 'digital-governance', 'enterprise-systems'],
        'tldr': [
            '聚焦 CIO 与技术主管在企业数字化转型中的关键领导力挑战与组织治理结构。',
            'IT 投资与战略业务目标对齐，建立基于风险收益比的企业级技术资产组合管理机制。',
            '跨越业务部门与技术研发团队的沟通断层，敏捷推动端到端大型系统落地与变革管理。',
        ]
    },
    '15.575': {
        'group': 'info_tech',
        'dir_name': '15575_economics_of_information_technology',
        'zh_title': '信息与信息技术经济学',
        'en_title': 'Economics of Information and Information Technology',
        'tags': ['information-economics', 'platform-economics', 'intellectual-property', 'network-theory'],
        'tldr': [
            '运用微观经济学前沿理论探究信息商品的特殊属性：高沉没固定成本与零边际复制成本。',
            '锁定效应（Lock-in）、转换成本、标准兼容性博弈与平台补贴最优定价策略。',
            '知识产权保护、数据要素产权、隐私保护激励与人工智能时代的劳动生产率悖论。',
        ]
    },

    # ── law 法律 ──
    '15.615': {
        'group': 'law',
        'dir_name': '15615_essential_law_for_entrepreneurs_and_managers',
        'zh_title': '创业者与管理者必备法学',
        'en_title': 'Essential Law',
        'tags': ['business-law', 'corporate-governance', 'intellectual-property-law', 'contract-law'],
        'tldr': [
            '商业决策不可忽视的法律防火墙，涵盖企业组织形式设立、有限责任与股权架构绑定。',
            '合同法核心救济机制、商业秘密保护、专利侵权防范与保密协议（NDA）签署雷区。',
            '创始人劳动雇佣合规、离职竞业禁止条款以及董事会受信义务（Fiduciary Duties）。',
        ]
    },
    '15.617': {
        'group': 'law',
        'dir_name': '15617_deals_finance_and_the_law',
        'zh_title': '交易、金融与公司法',
        'en_title': 'Deals, Finance, and the Law',
        'tags': ['mergers-law', 'securities-regulation', 'deal-structuring', 'corporate-control'],
        'tldr': [
            '复杂资本市场交易中的公司法演进、证券监管规则（SEC 法规）与交易架构设计。',
            '上市公司控制权争夺、敌意收购防范措施（毒丸计划）与特拉华州公司法核心裁判准则。',
            '债权人保护机制、破产法第 11 章重组程序以及私募股权并购合约中的陈述保证条款。',
        ]
    },

    # ── managerial_econ 管理经济学 ──
    '15.010': {
        'group': 'managerial_econ',
        'dir_name': '15010_economic_analysis_for_business_decisions',
        'zh_title': '商业决策经济学分析',
        'en_title': 'Economic Analysis for Business Decisions',
        'tags': ['managerial-economics', 'market-structure', 'elasticity-analysis', 'strategic-pricing'],
        'tldr': [
            '企业微观决策的核心经济学基准，涵盖供求弹性测算、生产边际成本曲线与规模报酬。',
            '完全竞争、垄断竞争、寡头垄断与完全垄断市场结构下的最优定价与产量均衡决策。',
            '识别机会成本、沉没成本与外部性，规避企业资源配置中的典型认知偏差。',
        ]
    },
    '15.012': {
        'group': 'managerial_econ',
        'dir_name': '15012_applied_macro_and_international_economics',
        'zh_title': '应用宏观与国际经济学 I',
        'en_title': 'Applied Macro- and International Economics',
        'tags': ['macroeconomics', 'monetary-policy', 'fiscal-policy', 'exchange-rates'],
        'tldr': [
            '面向跨国商业领袖的宏观经济指标体系解读，涵盖 GDP 增长动能、通胀形成与失业率。',
            'IS-LM 框架、央行货币政策利率传导机制、量化宽松（QE）与主权财政赤字可持续性。',
            '开放经济三元悖论、名义汇率与实际汇率决定机制，以及国际收支平衡表（BOP）危机预警。',
        ]
    },
    '15.014': {
        'group': 'managerial_econ',
        'dir_name': '15014_applied_macro_and_international_economics_ii',
        'zh_title': '应用宏观与国际经济学 II',
        'en_title': 'Applied Macro- and International Economics II',
        'tags': ['sovereign-debt', 'financial-crises', 'currency-unions', 'global-imbalances'],
        'tldr': [
            '宏观经济危机与国际金融架构的进阶研讨，重点解构主权债务危机与银行业系统性挤兑。',
            '最优货币区理论（OCA）视角下的欧元区架构缺陷与欧洲主权债务危机应对得失。',
            '全球宏观失衡背景下的大宗商品超级周期、主权财富基金运作与资本管制有效性。',
        ]
    },
    '15.015': {
        'group': 'managerial_econ',
        'dir_name': '15015_macroeconomic_policy_reforms',
        'zh_title': '宏观经济政策改革',
        'en_title': 'Macroeconomic Policy Reforms',
        'tags': ['economic-reform', 'structural-adjustment', 'privatization', 'inflation-stabilization'],
        'tldr': [
            '发展中国家与转轨经济体面临的结构性改革难题，从恶性通货膨胀治理到休克疗法经验。',
            '汇率锚定、财政重整、要素市场自由化与国有企业私有化改革的政治经济学博弈。',
            '汲取拉美、东欧与东亚金融危机的经验教训，构建具备宏观审慎防线的发展战略。',
        ]
    },
    '15.020': {
        'group': 'managerial_econ',
        'dir_name': '15020_economics_of_energy_innovation_and_sustainability',
        'zh_title': '能源、创新与可持续发展经济学',
        'en_title': 'Economics of Energy, Innovation, and Sustainability',
        'tags': ['energy-economics', 'carbon-pricing', 'renewable-energy', 'sustainability'],
        'tldr': [
            '全球能源结构低碳转型过程中的市场化机制，包括碳排放权交易体系（ETS）与碳税设计。',
            '可再生能源（光伏、风电）平准化度电成本（LCOE）下降曲线与电网调峰储能经济性。',
            '应对气候变化负外部性的公共政策干预工具与企业 ESG 投资的长期财务回报权衡。',
        ]
    },
    '15.021J': {
        'group': 'managerial_econ',
        'dir_name': '15021j_real_estate_economics',
        'zh_title': '房地产经济学',
        'en_title': 'Real Estate Economics',
        'tags': ['urban-economics', 'real-estate-market', 'land-use', 'housing-bubbles'],
        'tldr': [
            '空间市场（Space Market）与资产市场（Asset Market）双重四象限均衡模型（DiPasquale-Wheaton）。',
            '城市集聚经济、地租梯度理论、土地用途规划规制对城市扩张与住宅供给弹性的影响。',
            '房地产周期波动的宏观驱动要素，理性预期与投机狂热下的房地产泡沫识别与预警。',
        ]
    },
    '15.024': {
        'group': 'managerial_econ',
        'dir_name': '15024_applied_economics_for_managers',
        'zh_title': '经理人应用经济学',
        'en_title': 'Applied Economics for Managers',
        'tags': ['microeconomic-tools', 'pricing-tactics', 'market-entry', 'cost-structure'],
        'tldr': [
            '结合真实商业案例的应用微观经济学，指导企业在新市场进入、产能扩张中的理性决策。',
            '差别定价与价格弹性测算、长期与短期成本分摊、多产品线范围经济（Economies of Scope）。',
            '剖析不对称信息市场中的逆向选择与道德风险，设计激励相容的商业契约。',
        ]
    },
    '15.025': {
        'group': 'managerial_econ',
        'dir_name': '15025_game_theory_for_strategic_advantage',
        'zh_title': '博弈论与企业战略竞争优势',
        'en_title': 'Game Theory for Strategic Advantage',
        'tags': ['game-theory', 'nash-equilibrium', 'strategic-moves', 'auction-theory'],
        'tldr': [
            '将非合作博弈论应用于企业商业竞争、合作谈判与先发优势（First-mover Advantage）确立。',
            '纳什均衡、子博弈精炼均衡、可信承诺（Commitment）与威胁在价格竞争中的实际威力。',
            '拍卖机制设计（英式、荷式、第一价格与第二价格密封拍卖）及竞标防合谋策略。',
        ]
    },
    '15.026J': {
        'group': 'managerial_econ',
        'dir_name': '15026j_global_climate_change_economics_science_policy',
        'zh_title': '全球气候变化：经济、科学与政策',
        'en_title': 'Global Climate Change: Economics, Science, and Policy',
        'tags': ['climate-economics', 'integrated-assessment', 'environmental-policy', 'carbon-abatement'],
        'tldr': [
            '融合地球气候物理模型与宏观经济综合评估模型（IAM），量化碳排放社会成本（SCC）。',
            '贴现率选取的代际伦理争论（Stern vs. Nordhaus）、气候灾难尾部极端风险评估。',
            '联合国气候谈判（COP）机制、巴黎协定下国家自主贡献（NDC）与边境调节关税（CBAM）博弈。',
        ]
    },

    # ── mkt 市场营销 ──
    '15.821': {
        'group': 'mkt',
        'dir_name': '15821_listening_to_the_customer',
        'zh_title': '聆听客户心声与质性调研',
        'en_title': 'Listening to the Customer',
        'tags': ['qualitative-research', 'voice-of-customer', 'customer-discovery', 'focus-groups'],
        'tldr': [
            '深度客户洞察的质性研究方法论，强调挖掘客户未言明的潜在隐性需求与情感诉求。',
            '掌握人种学观察（Ethnography）、客户深度访谈与焦点小组（Focus Group）的实操规范。',
            '构建从客户原声（VOC）到工程产品功能规格的质量功能展开（QFD）转化框架。',
        ]
    },
    '15.822': {
        'group': 'mkt',
        'dir_name': '15822_strategic_market_measurement',
        'zh_title': '战略市场测量与量化调研',
        'en_title': 'Strategic Market Measurement',
        'tags': ['conjoint-analysis', 'market-research', 'factor-analysis', 'cluster-segmentation'],
        'tldr': [
            '市场调研的量化分析进阶，运用多变量统计方法精确量化消费者效用偏好与支付意愿。',
            '联合分析（Conjoint Analysis）在最优化产品概念设计与特征权衡中的工程化落地。',
            '因子分析与聚类算法在市场细分（STP）中的实证检验，指导精准营销资源投放。',
        ]
    },
    '15.834': {
        'group': 'mkt',
        'dir_name': '15834_marketing_strategy',
        'zh_title': '营销战略学',
        'en_title': 'Marketing Strategy',
        'tags': ['marketing-strategy', 'competitive-positioning', 'customer-equity', 'brand-architecture'],
        'tldr': [
            '将营销职能提升至企业公司层战略高度，建立以客户终身价值（CLV）为核心的战略飞轮。',
            '防御性营销战略对战进攻性市场掠夺，维持成熟期产品现金牛地位并开辟第二增长曲线。',
            '品牌架构演进、跨品类延伸边界与全渠道消费者旅程接触点的统合协同管理。',
        ]
    },
    '15.835': {
        'group': 'mkt',
        'dir_name': '15835_entrepreneurial_marketing',
        'zh_title': '创业营销与增长攻坚',
        'en_title': 'Entrepreneurial Marketing',
        'tags': ['entrepreneurial-marketing', 'growth-hacking', 'go-to-market', 'early-adopters'],
        'tldr': [
            '在零品牌知名度、预算极端匮乏的不确定性约束下，推动初创项目冷启动与破局增长。',
            '跨越鸿沟理论（Crossing the Chasm），识别早期创新采用者并建立灯塔客户标杆效应。',
            '低成本增长黑客（Growth Hacking）、病毒式裂变传播机制与精准获客漏斗迭代。',
        ]
    },
    '15.840': {
        'group': 'mkt',
        'dir_name': '15840_seminar_in_marketing',
        'zh_title': '营销管理高级专题研讨',
        'en_title': 'Seminar in Marketing',
        'tags': ['marketing-analytics', 'digital-marketing', 'customer-retention', 'omnichannel'],
        'tldr': [
            '追踪现代营销学前沿突破，聚焦大数据驱动的归因模型、算法推荐与个性化动态营销。',
            '消费者流失预警模型、再营销召回战略与全渠道无缝融合体验设计。',
            '品牌资产的财务量化评估、公关危机公关治理及数字化时代的消费者信任重塑。',
        ]
    },

    # ── ops_mngt 运营管理 ──
    '15.136J': {
        'group': 'ops_mngt',
        'dir_name': '15136j_principles_and_practice_of_drug_development',
        'zh_title': '新药研发原理与实践运营',
        'en_title': 'Principles and Practice of Drug Development',
        'tags': ['drug-development', 'clinical-trials', 'biotech-operations', 'regulatory-strategy'],
        'tldr': [
            '创新药从靶点发现、临床前验证到 I-III 期临床试验的高资本、长周期、高失败率运营管理。',
            'FDA 药品监管合规流程、适应症选择、临床试验供应链管理及加速审批通道策略。',
            '生物医药知识产权布局、药品专利悬崖应对、定价医保准入谈判与商业化估值模型。',
        ]
    },
    '15.763J': {
        'group': 'ops_mngt',
        'dir_name': '15763j_supply_chain_capacity_analytics',
        'zh_title': '供应链产能分析与系统设计',
        'en_title': 'Supply Chain: Capacity Analytics',
        'tags': ['capacity-planning', 'supply-chain-analytics', 'stochastic-inventory', 'network-design'],
        'tldr': [
            '量化建模分析离散制造与服务供应链中的产能约束、利用率与排队等待时延。',
            '报童模型进阶、多级库存缓冲配置（Safety Stock）与风险汇聚（Risk Pooling）效应。',
            '非确定性需求波动下的全球柔性制造网络设计与外包契约（Buyback/Revenue-sharing）。',
        ]
    },
    '15.764J': {
        'group': 'ops_mngt',
        'dir_name': '15764j_the_theory_of_operations_management',
        'zh_title': '运营管理理论',
        'en_title': 'The Theory of Operations Management',
        'tags': ['operations-theory', 'inventory-theory', 'stochastic-control', 'queueing-models'],
        'tldr': [
            '运营管理学界的数学理论根基，涵盖连续时间马尔可夫决策过程与动态规划求解。',
            '古典库存理论（$(s, S)$ 与基准存货策略）的最优性证明与多梯队系统控制。',
            '排队网络理论（Jackson 网络）、流体近似模型及收益管理中的动态联合定价博弈。',
        ]
    },
    '15.768': {
        'group': 'ops_mngt',
        'dir_name': '15768_management_of_services',
        'zh_title': '服务运营管理：为客户、员工与股东创造价值',
        'en_title': 'Management of Services: Creating Value for Customers, Employees, and Investors',
        'tags': ['service-operations', 'service-profit-chain', 'customer-satisfaction', 'service-design'],
        'tldr': [
            '服务经济下运营模式与传统产品制造的本质差异：无形性、不可储存性与即时生产消费协同。',
            '服务利润链（Service-Profit Chain）理论：员工满意度驱动服务价值，进而驱动客户忠诚与股东回报。',
            '服务失误补救机制、排队心理感知管理与数字化自助服务（Self-service）的体验边界。',
        ]
    },
    '15.769': {
        'group': 'ops_mngt',
        'dir_name': '15769_operations_strategy',
        'zh_title': '运营战略学',
        'en_title': 'Operations Strategy',
        'tags': ['operations-strategy', 'strategic-alignment', 'manufacturing-footprint', 'vertical-integration'],
        'tldr': [
            '将企业顶层商业竞争战略解构为运营层面的四个核心维度：成本、质量、交付速度与柔性。',
            '垂直一体化与外包边界划分、全球工厂网络布局布局（Offshoring vs. Reshoring）。',
            '战略性产能扩张时机的先发抢占与跟随机会评估，实现技术工艺与市场生命周期的动态协同。',
        ]
    },
    '15.770J': {
        'group': 'ops_mngt',
        'dir_name': '15770j_logistics_systems',
        'zh_title': '物流系统工程',
        'en_title': 'Logistics Systems',
        'tags': ['logistics-systems', 'freight-transportation', 'facility-location', 'vehicle-routing'],
        'tldr': [
            '综合物流网络中的核心算法与决策架构，涵盖设施选址问题（Facility Location Problem）。',
            '多式联运货运网络成本权衡、集装箱班轮调度与车辆路径问题（VRP）启发式求解。',
            '现代自动化物流配送中心（DC）内部越库作业（Cross-docking）与最后一公里配送优化。',
        ]
    },
    '15.772J': {
        'group': 'ops_mngt',
        'dir_name': '15772j_d_lab_supply_chains',
        'zh_title': 'D-Lab 发展中地区供应链',
        'en_title': 'D-Lab: Supply Chains',
        'tags': ['humanitarian-logistics', 'sustainable-supply-chain', 'developing-markets', 'last-mile-logistics'],
        'tldr': [
            '面向全球发展中国家与资源受限情境的低成本实用供应链系统设计与落地。',
            '小农经济农产品采后损失控制、冷链物流平民化替代方案与乡村微型商业生态。',
            '人道主义灾后救援物资应急调拨模型与非政府组织（NGO）公私合作协同机制。',
        ]
    },
    '15.778': {
        'group': 'ops_mngt',
        'dir_name': '15778_introduction_to_operations_management',
        'zh_title': '运营管理核心导论',
        'en_title': 'Introduction to Operations Management',
        'tags': ['process-improvement', 'lean-manufacturing', 'total-quality-management', 'six-sigma'],
        'tldr': [
            '现代企业核心运营流程的系统化诊断与优化框架，掌握流程图分析与工序节拍（Takt Time）。',
            '丰田精益生产方式（TPS）、消除七大浪费与全面质量管理（TQM / 六西格玛 DMAIC 循环）。',
            '统筹预测计划、生产排程与安全库存管理，实现企业供应链端到端高效周转。',
        ]
    },

    # ── org_studies 工作与组织研究 ──
    '15.301-carroll': {
        'group': 'org_studies',
        'dir_name': '15301_managerial_psychology',
        'zh_title': '管理心理学',
        'en_title': 'People, Teams, and Organizations Laboratory',
        'tags': ['managerial-psychology', 'organizational-behavior', 'group-dynamics', 'social-cognition'],
        'tldr': [
            '基于实证行为科学视角的组织管理，探索个体认知偏差、情绪智力与工作激励机制。',
            '小团队群体动力学、冲突化解策略与高效协作团队的心理安全感（Psychological Safety）塑造。',
            '运用“三重视角（战略、政治、文化）”综合诊断组织变革阻力并设计干预路径。',
        ]
    },
    '15.301-ariely': {
        'group': 'org_studies',
        'dir_name': '15301_managerial_psychology_laboratory',
        'zh_title': '管理心理学实验研究',
        'en_title': 'People, Teams, and Organizations Laboratory',
        'tags': ['behavioral-economics', 'experimental-design', 'heuristic-biases', 'decision-making'],
        'tldr': [
            'Dan Ariely 领衔的行为经济学实验实验室，揭示人类在管理决策中普遍存在的非理性模式。',
            '框架效应（Framing Effect）、损失厌恶、社会规范与市场规范冲突的实证检验。',
            '掌握行为科学严谨的双盲随机对照实验（A/B Testing）设计与因果推断数据分析。',
        ]
    },
    '15.302J': {
        'group': 'org_studies',
        'dir_name': '15302j_power_interpersonal_organizational_global',
        'zh_title': '权力学：人际、组织与全球维度',
        'en_title': 'Power: Interpersonal, Organizational, and Global Dimensions',
        'tags': ['organizational-power', 'social-networks', 'political-influence', 'coalition-building'],
        'tldr': [
            '去道德化、冷静客观地审视权力的本质：权力作为依赖关系的不对称性与资源控制能力。',
            '人际政治影响力、说服技巧与组织内部非正式权力网络的构建与维护机制。',
            '联盟构建（Coalition Building）、议程设置（Agenda Setting）及应对权力滥用的制度制衡。',
        ]
    },
    '15.310': {
        'group': 'org_studies',
        'dir_name': '15310_people_teams_and_organizations',
        'zh_title': '人、团队与组织',
        'en_title': 'People, Teams, and Organizations',
        'tags': ['team-effectiveness', 'leadership-styles', 'organizational-culture', 'change-management'],
        'tldr': [
            '解析当代知识型经济中组织行为的核心动力学，从个人工作满意度到跨部门协同阻滞。',
            '领导力风格情境适应理论（Situational Leadership）、分布式领导与跨文化团队领导。',
            '组织深层文化假设的识别、解冻与重构，驱动大型企业在颠覆性技术冲击下的成功转型。',
        ]
    },
    '15.316': {
        'group': 'org_studies',
        'dir_name': '15316_building_and_leading_effective_teams',
        'zh_title': '建设与领导高效团队',
        'en_title': 'Building and Leading Effective Teams',
        'tags': ['team-building', 'collaborative-leadership', 'conflict-resolution', 'collective-intelligence'],
        'tldr': [
            '高绩效团队构建的工程化指南，涵盖团队生命周期各阶段（形成、震荡、规范、成熟）。',
            '群体盲思（Groupthink）防范、建设性异见引入与跨职能多元背景团队的认同整合。',
            '提升团队集体智力（Collective Intelligence）、远程分布式办公协作规范与考核激励设计。',
        ]
    },
    '15.320': {
        'group': 'org_studies',
        'dir_name': '15320_strategic_organizational_design',
        'zh_title': '战略组织架构设计',
        'en_title': 'Strategic Organizational Design',
        'tags': ['organizational-design', 'matrix-organization', 'governance-structures', 'contingency-theory'],
        'tldr': [
            '结构服从战略（Structure Follows Strategy），权衡职能型、事业部制与矩阵式架构的利弊。',
            '跨边界信息流动通道设计、集权与分权边界、激励考核与决策权力的对称匹配。',
            '应对技术不确定性与动态环境的双元组织（Ambidextrous Organization）探索与利用平衡。',
        ]
    },
    '15.322': {
        'group': 'org_studies',
        'dir_name': '15322_leading_organizations',
        'zh_title': '领导组织变革',
        'en_title': 'Leading Organizations',
        'tags': ['transformational-leadership', 'organizational-change', 'stakeholder-management', 'sensemaking'],
        'tldr': [
            '高管层领导力的核心要素，聚焦在充满模糊性与不确定性的复杂系统中实现意义建构（Sensemaking）。',
            '解构变革阻力的心理与制度根源，运用阶梯式沟通策略与速赢成果（Quick Wins）建立变革势能。',
            '自我领导力觉察、面对重大危机与道德困境时的决策韧性与价值观坚守。',
        ]
    },
    '15.665': {
        'group': 'org_studies',
        'dir_name': '15665_power_and_negotiation',
        'zh_title': '权力与商务谈判',
        'en_title': 'Power and Negotiation',
        'tags': ['negotiation-strategy', 'batna', 'integrative-bargaining', 'dispute-resolution'],
        'tldr': [
            '哈佛谈判学派与麻省理工博弈实战的融合，区分分配型谈判（零和分饼）与整合型谈判（做大蛋糕）。',
            '最佳替代方案（BATNA）、保留价值与可能达成协议空间（ZOPA）的精准测算与锚定。',
            '多方多议题复杂谈判、跨文化商业谈判雷区应对与破坏性僵局的建设性化解机制。',
        ]
    },
    '15.676': {
        'group': 'org_studies',
        'dir_name': '15676_work_and_employment_relations_theory',
        'zh_title': '工作与雇佣关系理论',
        'en_title': 'Work and Employment Relations Theory',
        'tags': ['labor-relations', 'collective-bargaining', 'employment-systems', 'future-of-work'],
        'tldr': [
            '从制度学派、马克思主义与人力资本视角审视现代劳动契约与雇佣关系的制度演进。',
            '工会集体谈判制度、劳资共决（Codetermination）机制与全球化对蓝领白领工资差距的冲击。',
            '零工经济（Gig Economy）、算法管理与自动化技术对劳动者自主权及社会保障网的重构。',
        ]
    },
    '15.677J': {
        'group': 'org_studies',
        'dir_name': '15677j_labor_markets_and_employment_policy',
        'zh_title': '劳动力市场与就业政策',
        'en_title': 'Labor Markets and Employment Policy',
        'tags': ['labor-economics', 'minimum-wage', 'human-capital', 'employment-policy'],
        'tldr': [
            '运用劳动经济学实证工具评估公共就业政策的社会福利与经济效率效应。',
            '最低工资标准设定的双刃剑效应、失业保险激励机制与职业技能培训计划的因果评估。',
            '劳动力市场分割、代际流动性壁垒、职场性别与种族薪酬歧视的政策干预路径。',
        ]
    },

    # ── strat_mngt 战略管理 ──
    '15.902': {
        'group': 'strat_mngt',
        'dir_name': '15902_advanced_strategic_management',
        'zh_title': '高级战略管理学',
        'en_title': 'Advanced Strategic Management',
        'tags': ['strategic-management', 'competitive-advantage', 'industry-analysis', 'resource-based-view'],
        'tldr': [
            '企业获取并维持持续竞争优势（SCA）的核心理论框架，统合波特五力模型与定位学派。',
            '基于资源的视角（RBV）与 VRIO 框架，识别企业稀缺、不可替代的核心能力与战略资产。',
            '公司层战略：业务组合矩阵管理、纵向一体化边界确立与非相关多元化折价的防范。',
        ]
    },
    '15.904': {
        'group': 'strat_mngt',
        'dir_name': '15904_strategy_and_the_ceo',
        'zh_title': 'CEO 战略与最高决策',
        'en_title': 'Strategy and the CEO',
        'tags': ['ceo-strategy', 'corporate-governance', 'capital-allocation', 'executive-decision'],
        'tldr': [
            '站在首席执行官（CEO）视角审视企业顶层战略设计、资本配置与利益相关者平衡。',
            'CEO 作为首席资源分配官的纪律性：股票回购、股利分红、再投资与战略并购的权衡。',
            '董事会治理博弈、管理层激励考核与在激进做空机构攻击下的战略定力维护。',
        ]
    },
    '15.912': {
        'group': 'strat_mngt',
        'dir_name': '15912_strategic_management_of_innovation',
        'zh_title': '创新与创业战略管理',
        'en_title': 'Strategic Management of Innovation and Entrepreneurship',
        'tags': ['innovation-strategy', 'disruptive-innovation', 'technology-s-curve', 'platform-competition'],
        'tldr': [
            '技术变迁与产业演进的动态战略规律，掌握技术 S 曲线、主导设计（Dominant Design）确立。',
            '克里斯坦森颠覆式创新理论剖析：成熟巨头如何陷入创新者的窘境与新进入者的破局战术。',
            '平台生态圈竞争、网络效应临界质量突破与创新价值捕获（Profiting from Innovation / Teece 模型）。',
        ]
    },

    # ── tech_innov 技术、创新与创业 ──
    '15.350': {
        'group': 'tech_innov',
        'dir_name': '15350_managing_technological_innovation',
        'zh_title': '技术创新与创业管理',
        'en_title': 'Managing Technological Innovation and Entrepreneurship',
        'tags': ['technology-management', 'r-and-d-management', 'innovation-funnel', 'stage-gate-process'],
        'tldr': [
            '高科技企业技术研发从前沿概念到量产商业化的系统化管理工具与组织流程。',
            '阶段门径流程（Stage-Gate Process）与研发项目组合风险收益折衷评估。',
            '建立支持容错、鼓励跨界探索的创新企业文化，构建开放式创新（Open Innovation）生态。',
        ]
    },
    '15.351J': {
        'group': 'tech_innov',
        'dir_name': '15351j_making_and_hardware_ventures',
        'zh_title': '硬科技创客与硬件创业导论',
        'en_title': 'Introduction to Making and Hardware Ventures',
        'tags': ['hardware-entrepreneurship', 'rapid-prototyping', 'design-for-manufacturing', 'hardware-costing'],
        'tldr': [
            '硬科技硬件创业的核心全流程，涵盖快速原型开发（3D 打印/CNC/PCB）与用户迭代。',
            '面向制造与装配的设计（DFMA）、模具开发周期（NPI / EVT-DVT-PVT）与供应链寻源。',
            '硬件初创企业独特的现金流陷阱、BOM 成本控制与全球分销渠道铺设策略。',
        ]
    },
    '15.352J': {
        'group': 'tech_innov',
        'dir_name': '15352j_startmit_exploring_entrepreneurship',
        'zh_title': 'StartMIT 创业实战探索',
        'en_title': 'StartMIT: Exploring Entrepreneurship and Innovation',
        'tags': ['entrepreneurship-bootcamp', 'lean-startup', 'pitching', 'founder-journey'],
        'tldr': [
            'MIT 标志性寒假创业特训营，为技术背景学生搭建从科研论文走向商业公司的跳板。',
            '精益创业核心方法论：最小可行产品（MVP）构建、假设快速验证与战略支点转向（Pivot）。',
            '创业合伙人寻找、股权分配协议设计与向顶级风险投资人进行电梯路演（Pitch）实战。',
        ]
    },
    '15.356': {
        'group': 'tech_innov',
        'dir_name': '15356_lead_user_innovation_methods',
        'zh_title': '领先用户创新方法论',
        'en_title': 'Lead User Innovation Methods',
        'tags': ['lead-user-method', 'user-innovation', 'product-conceptualization', 'market-foresight'],
        'tldr': [
            'Eric von Hippel 开创的领先用户理论：突破性商业创新往往首先源于用户而非厂商。',
            '如何在目标市场趋势的最前沿识别遭遇极端需求并自主开发解决方案的领先用户。',
            '将领先用户的民间发明原型系统化转化为具备规模商业价值的突破性工业产品。',
        ]
    },
    '15.358': {
        'group': 'tech_innov',
        'dir_name': '15358_strategy_in_the_age_of_digital_platforms',
        'zh_title': '数字平台时代的商业战略',
        'en_title': 'Strategy in the Age of Digital Platforms',
        'tags': ['platform-strategy', 'digital-ecosystems', 'two-sided-markets', 'network-orchestration'],
        'tldr': [
            '剖析软件、互联网与移动生态中平台商业模式的治理机制与竞争动态。',
            '解决平台冷启动的“鸡与蛋”悖论，设计双边多边市场的开放程度与 API 生态激励。',
            '平台所有者与生态应用开发者的竞合格局，应对围墙花园（Walled Garden）反垄断审查。',
        ]
    },
    '15.369': {
        'group': 'tech_innov',
        'dir_name': '15369_corporate_entrepreneurship_lab',
        'zh_title': '企业内部创业实战实验室',
        'en_title': 'Corporate Entrepreneurship Lab',
        'tags': ['corporate-venture', 'intrapreneurship', 'incubator-management', 'strategic-renewal'],
        'tldr': [
            '大型成熟企业如何克服大企业病，在现存母体组织内孵化具备高成长性的创新业务。',
            '企业风险投资（CVC）策略、外部加速器合作与内部独立特种作战团队（Skunkworks）治理。',
            '平衡成熟核心业务的现金流保护与高风险新兴业务的自主权，防范母体免疫排斥。',
        ]
    },
    '15.387': {
        'group': 'tech_innov',
        'dir_name': '15387_entrepreneurial_sales',
        'zh_title': '创业企业战略销售',
        'en_title': 'Entrepreneurial Sales',
        'tags': ['b2b-sales', 'sales-pipeline', 'customer-acquisition-cost', 'complex-selling'],
        'tldr': [
            'B2B 企业级复杂销售的工程化科学，打破销售仅仅依赖天赋或关系的传统误区。',
            '销售漏斗（Sales Pipeline）各阶段转化率量化分析、理想客户画像（ICP）精准锁定。',
            '大客户决策委员会（DMU）多利益方利益对齐、价值证明（POC）与定价谈判收单。',
        ]
    },
    '15.389': {
        'group': 'tech_innov',
        'dir_name': '15389_global_entrepreneurship_lab',
        'zh_title': '全球创业实战实验室 (G-Lab)',
        'en_title': 'Global Entrepreneurship Lab',
        'tags': ['action-learning', 'international-entrepreneurship', 'scale-up-strategy', 'emerging-enterprises'],
        'tldr': [
            'MIT Sloan 经典行动学习项目，组建 MBA 顾问团队直插全球新兴市场高成长初创企业。',
            '实地调研企业扩张瓶颈，量身定制战略定位、全渠道增长与组织规模化（Scaling）方案。',
            '在跨文化不确定性商业情境下快速交付具备可落地性的管理咨询洞察与商业成果。',
        ]
    },
    '15.390': {
        'group': 'tech_innov',
        'dir_name': '15390_entrepreneurship_101',
        'zh_title': '创业 101：系统性创建新创企业',
        'en_title': 'Entrepreneurship 101: Systematic Approach to New Venture Creation',
        'tags': ['disciplined-entrepreneurship', 'customer-persona', 'tam-analysis', 'value-proposition'],
        'tldr': [
            'Bill Aulet 创立的 24 步严谨创业法（Disciplined Entrepreneurship）体系化指导纲领。',
            '从市场细分、海滩阵地（Beachhead Market）选择、最终用户画像到总潜在市场（TAM）测算。',
            '全面验证客户终身价值（LTV）必须大幅超越获客成本（COCA），确立可持续核心竞争优势。',
        ]
    },
    '15.394': {
        'group': 'tech_innov',
        'dir_name': '15394_entrepreneurial_founding_and_teams',
        'zh_title': '创业团队创建与领导力',
        'en_title': 'Entrepreneurial Founding and Teams',
        'tags': ['founder-dilemmas', 'equity-split', 'startup-culture', 'early-hires'],
        'tldr': [
            '深度剖析创始人困境（Founder\'s Dilemmas）：在追求财富（Rich）与追求控制权（King）间的抉择。',
            '早期合伙人股权分配的动态调整机制（动态既得权）、合伙人权责边界与退出补偿约定。',
            '初创团队前十名员工的招聘准则、激励体系设计以及公司向规模化发展时的领导力进化。',
        ]
    },
}

def extract_content(src_path):
    idx_path = os.path.join(src_path, 'index.md')
    if not os.path.exists(idx_path):
        return None
    raw = open(idx_path, 'r', encoding='utf-8').read()
    
    # Extract source url
    src_match = re.search(r'\[MIT OpenCourseWare\]\((https?://[^\)]+)\)', raw)
    source_url = src_match.group(1).strip() if src_match else ''
    
    # Extract description
    desc = ''
    desc_match = re.search(r'## 课程简介 / Description\s*\n+([\s\S]*?)(?=\n##|\n---|$)', raw)
    if desc_match:
        desc = desc_match.group(1).strip()
    
    # Extract lectures
    lectures = ''
    lec_match = re.search(r'## 讲义 / Lecture Notes\s*\n+([\s\S]*?)(?=\n---|$)', raw)
    if lec_match:
        lectures = lec_match.group(1).strip()
        
    return {
        'source_url': source_url,
        'description': desc,
        'lectures': lectures
    }

def main():
    print('Starting Course 15 outline migration...')
    
    # Collect all sources
    source_dirs = {}
    
    # 1. From /Users/mac/Documents/courses
    folder_mapping = {
        '会计学': 'acct',
        '信息技术': 'info_tech',
        '全球经济与管理': 'global_econ',
        '医疗卫生管理': 'ops_mngt',
        '工业关系与人力资源管理': 'org_studies',
        '工作与组织研究': 'org_studies',
        '战略管理': 'strat_mngt',
        '技术、创新与创业': 'tech_innov',
        '沟通与传播': 'comm',
        '法律': 'law',
        '管理经济学': 'managerial_econ',
        '运营管理': 'ops_mngt',
        '通识基础课程': 'or_stats',
        '金融学': 'finance',
        '高管工商管理硕士（EMBA）课程': 'emba'
    }
    
    for fld, grp in folder_mapping.items():
        p = os.path.join(BASE_COURSES, fld)
        if not os.path.exists(p): continue
        for sub in sorted(os.listdir(p)):
            subpath = os.path.join(p, sub)
            if not os.path.isdir(subpath) or sub.startswith('.'): continue
            
            # Key matching
            if '15.301 Managerial Psychology Laboratory' in sub:
                source_dirs['15.301-ariely'] = subpath
            elif '15.301 Managerial Psychology' in sub:
                source_dirs['15.301-carroll'] = subpath
            else:
                m = re.search(r'15\.[0-9A-Z]+(?:\[?J\]?)?', sub, re.I)
                if m:
                    cid = m.group(0).upper().replace('[', '').replace(']', '')
                    source_dirs[cid] = subpath
                    
    # 2. From /Users/mac/Documents/MIT/15_Marketing
    for sub in sorted(os.listdir(BASE_MKT)):
        subpath = os.path.join(BASE_MKT, sub)
        if not os.path.isdir(subpath) or sub.startswith('.') or 'Pricing' in sub or '15.810' in sub: continue
        m = re.search(r'15\.[0-9A-Z]+', sub, re.I)
        if m:
            cid = m.group(0).upper()
            source_dirs[cid] = subpath
            
    print(f'Total mapped source courses: {len(source_dirs)}')
    
    migrated_count = 0
    skipped_count = 0
    
    for cid_key, spec in COURSES_SPEC.items():
        src_path = source_dirs.get(cid_key)
        if not src_path:
            # Try plain cid
            clean_k = cid_key.split('-')[0]
            src_path = source_dirs.get(clean_k)
            
        if not src_path:
            print(f'[WARN] No source found for {cid_key}')
            continue
            
        extracted = extract_content(src_path)
        if not extracted:
            print(f'[WARN] Could not extract content from {src_path}')
            continue
            
        # Target path
        grp = spec['group']
        target_dir = os.path.join(DOCS_MGMT, grp, spec['dir_name'])
        target_index = os.path.join(target_dir, 'index.md')
        
        # Don't overwrite if it's an existing full course (like 15.783)
        if os.path.exists(target_index):
            existing_txt = open(target_index, 'r', encoding='utf-8').read()
            if 'status: complete' in existing_txt:
                print(f'[SKIP] Target has status: complete: {target_dir}')
                skipped_count += 1
                continue
                
        os.makedirs(target_dir, exist_ok=True)
        
        # Build frontmatter & markdown
        clean_cid_display = cid_key.split('-')[0]
        full_title = f"{clean_cid_display} {spec['zh_title']} ({spec['en_title']})"
        tags_str = ', '.join(spec['tags'])
        source_url = extracted['source_url'] if extracted['source_url'] else 'https://ocw.mit.edu/'
        
        tldr_bullets = '\n'.join([f'- {point}' for point in spec['tldr']])
        
        desc_body = extracted['description'] if extracted['description'] else '本课程提供系统的理论框架与实务方法论。'
        lec_body = extracted['lectures'] if extracted['lectures'] else '- 详见课程教学日历与讲义大纲。'
        
        content = f"""---
title: {full_title}
type: course
course: {full_title}
course_id: '{clean_cid_display}'
tags: [{tags_str}]
status: stub
source: '{source_url}'
---

# {full_title}

> MIT Course 15 · {GROUP_NAMES[grp]} · 课号 {clean_cid_display}

## TL;DR

{tldr_bullets}

## 课程简介 / Description

{desc_body}

## 讲义 / Lecture Notes

{lec_body}

---

本资料整理自 [MIT OpenCourseWare]({source_url})，遵循 Creative Commons BY-NC-SA 4.0 许可协议，仅供个人学习使用。
"""
        with open(target_index, 'w', encoding='utf-8') as f:
            f.write(content)
            
        migrated_count += 1

    print(f'Done! Successfully migrated: {migrated_count}, Skipped: {skipped_count}')

if __name__ == '__main__':
    main()
