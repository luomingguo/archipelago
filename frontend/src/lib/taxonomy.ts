export interface TaxonomyItem {
  label: string;
  description: string;
}

export const DISCIPLINES: Record<string, TaxonomyItem> = {
  cs: {
    label: '计算机科学',
    description: '从计算机体系结构、系统软件到编程语言与理论基础，理解计算系统如何被构造。',
  },
  psy: {
    label: '心理学',
    description: '从认知、发展、社会与神经机制理解人的心智、行为及其研究方法。',
  },
  economics: {
    label: '经济学',
    description: '研究个人、组织与市场如何在约束条件下作出选择并形成经济结果。',
  },
  management: {
    label: '管理学',
    description: '连接组织、金融、运营、战略与技术创新中的分析方法和实践判断。',
  },
  mgnt: {
    label: '管理学',
    description: '连接组织、金融、运营、战略与技术创新中的分析方法和实践判断。',
  },
};

export const CATEGORIES: Record<string, Record<string, TaxonomyItem>> = {
  cs: {
    arch: { label: '计算机架构', description: '处理器、存储层次、并行执行与软硬件接口。' },
    computer_sys: { label: '计算机系统', description: '操作系统、网络、数据库、存储与分布式系统。' },
    language: { label: '编程语言', description: '语言设计、解释器、编译器与程序语义。' },
    opensource: { label: '开源项目', description: '通过真实代码库理解工程实现与设计权衡。' },
    opensrc: { label: '开源项目', description: '通过真实代码库理解工程实现与设计权衡。' },
    security: { label: '计算机安全', description: '密码学、系统安全与攻击防御机制。' },
    sw_eng: { label: '软件工程', description: '软件设计、性能、并发与工程化方法。' },
    tcs: { label: '理论计算机科学', description: '算法、数据结构、计算复杂性与离散数学基础。' },
    index: { label: '知识索引', description: '连接课程、概念与学习路径的全局索引。' },
  },
  psy: {
    intro: { label: '心理学导论', description: '建立心理科学主要问题、理论与证据方法的整体地图。' },
    cognitive: { label: '认知心理学', description: '知觉、语言、记忆、推理与心智表征。' },
    developmental: { label: '发展心理学', description: '认知与行为在婴幼儿至成年阶段的发展机制。' },
    neuroscience: { label: '神经科学', description: '从细胞、系统和认知层面理解脑与行为。' },
    research_methods: { label: '研究方法', description: '实验设计、统计推断与脑认知研究方法。' },
    social: { label: '社会心理学', description: '个体如何受到群体、情境与社会关系影响。' },
  },
  economics: {
    general_theory: { label: '经济学原理', description: '宏观经济学与博弈论等经济分析基础。' },
    industrial_organization: { label: '产业组织', description: '市场结构、企业行为与竞争政策。' },
    microecon_principles: { label: '微观经济学', description: '消费者、企业、价格与资源配置。' },
    organizational_economics: { label: '组织经济学', description: '契约、激励与组织边界的经济分析。' },
    psych_econ: { label: '心理与行为经济学', description: '心理机制如何改变经济判断与选择。' },
  },
  management: {
    acct: { label: '会计', description: '财务报告、税务与经营决策中的会计信息。' },
    comm: { label: '管理沟通', description: '数据表达、领导沟通与学术交流。' },
    emba: { label: '综合管理', description: '面向管理实践的市场、定价与运营课程。' },
    finance: { label: '金融', description: '公司金融、投资、市场与金融科技。' },
    global_econ: { label: '全球经济', description: '全球市场、政策与前沿产业环境。' },
    info_tech: { label: '信息技术管理', description: '数字化、信息经济与技术管理。' },
    law: { label: '商业法律', description: '创业、交易和金融活动中的法律框架。' },
    managerial_econ: { label: '管理经济学', description: '支持企业决策的微观、宏观与博弈分析。' },
    mkt: { label: '市场营销', description: '客户洞察、定价、测量与营销战略。' },
    ops_mngt: { label: '运营管理', description: '供应链、服务、物流与产品开发。' },
    or_stats: { label: '运筹与统计', description: '优化、概率、统计与数据驱动决策。' },
    org_studies: { label: '组织研究', description: '团队、领导、权力与组织设计。' },
    strat_mngt: { label: '战略管理', description: '企业战略、创新战略与高层决策。' },
    sys_dyn: { label: '系统动力学', description: '用反馈、存量与流量理解复杂组织系统。' },
    tech_innov: { label: '技术创新与创业', description: '技术商业化、创新管理与创业实践。' },
  },
};

export function disciplineLabel(slug: string): string {
  return DISCIPLINES[slug]?.label ?? humanizeSlug(slug);
}

export function disciplineDescription(slug: string): string {
  return DISCIPLINES[slug]?.description ?? '由真实课程目录生成的学科知识集合。';
}

export function categoryLabel(discipline: string, category: string): string {
  return CATEGORIES[discipline]?.[category]?.label ?? humanizeSlug(category);
}

export function categoryDescription(discipline: string, category: string): string {
  return CATEGORIES[discipline]?.[category]?.description ?? '由真实课程与笔记生成的知识领域。';
}

function humanizeSlug(slug: string): string {
  return slug.replaceAll('_', ' ').replace(/\b\w/g, (letter) => letter.toUpperCase());
}
