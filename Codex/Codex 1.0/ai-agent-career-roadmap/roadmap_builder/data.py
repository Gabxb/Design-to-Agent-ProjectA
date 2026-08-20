"""Structured curriculum data used by all generated artifacts."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WeekSpec:
    number: int
    title: str
    focus: str
    deliverable: str
    job_value: str
    must: tuple[str, ...]
    understand: tuple[str, ...]
    explore: tuple[str, ...]
    interview: tuple[str, ...]
    risk: str
    project: str


WEEKS: tuple[WeekSpec, ...] = (
    WeekSpec(1, "Python 与本地开发环境", "Python 3.12、虚拟环境、类型提示、函数、类、模块与调试", "可运行的需求数据清洗命令行工具", "能独立阅读和修改 Agent 项目的 Python 代码，并建立可复现环境。", ("虚拟环境", "类型提示", "函数与模块", "异常信息阅读"), ("类与数据模型", "包结构"), ("生成器与上下文管理器",), ("为什么需要虚拟环境？", "类型提示能解决什么问题？"), "容易把时间耗在语法细节；以可运行的小程序为主。", "阶段项目：设计需求结构化助手 API"),
    WeekSpec(2, "Git、HTTP 与 FastAPI", "Git 工作流、HTTP、JSON、REST API、FastAPI 路由与测试", "带三个接口的需求助手 API 原型", "真实 Agent 通常通过 API 接收任务、返回结构化结果，并用 Git 协作。", ("提交与分支", "HTTP 方法和状态码", "JSON", "FastAPI 路由"), ("REST 约束", "依赖注入"), ("异步接口",), ("PUT 与 PATCH 有何区别？", "如何设计可维护的 API？"), "只会复制接口代码但不理解输入输出契约。", "阶段项目：设计需求结构化助手 API"),
    WeekSpec(3, "SQL 与 PostgreSQL", "关系模型、SQL、PostgreSQL、CRUD、事务与迁移", "可持久化需求记录的 API", "Agent 需要可靠保存用户、任务、工具调用和评测结果。", ("表与主键", "SELECT/INSERT/UPDATE", "CRUD", "数据库连接配置"), ("索引", "事务", "迁移"), ("查询计划",), ("索引何时会失效？", "事务解决什么问题？"), "本地数据库配置可能占用过多时间；先完成最小闭环。", "阶段项目：设计需求结构化助手 API"),
    WeekSpec(4, "工程化 API 阶段项目", "分层、日志、异常处理、测试、环境变量与 README", "设计需求结构化助手 API v1", "把零散知识收束为可展示、可运行、可解释的小项目。", ("配置隔离", "日志", "错误响应", "API 测试"), ("服务层", "测试替身"), ("可观测性字段设计",), ("如何设计统一错误格式？", "怎样证明接口可维护？"), "功能堆积导致无法验收；严格按接受标准收尾。", "阶段项目交付"),
    WeekSpec(5, "LLM 基础与 Prompt 结构", "Token、上下文窗口、消息角色、指令层级与 Prompt 模板", "可复用的访谈摘要 Prompt 套件", "理解模型边界，才能设计稳定的 Agent 输入与输出。", ("Token", "上下文", "系统指令", "Prompt 模板"), ("采样参数", "上下文压缩"), ("模型路由",), ("上下文窗口与记忆有什么区别？", "如何减少 Prompt 歧义？"), "把 Prompt 调整当成玄学；必须记录输入、版本和结果。", "阶段项目：UX Research Copilot"),
    WeekSpec(6, "Structured Output 与 Tool Calling", "JSON Schema、结构化输出、函数调用、参数验证", "能稳定输出研究洞察 JSON 的工具调用原型", "Agent 与业务系统协作依赖机器可验证的结构化契约。", ("JSON Schema", "Pydantic 模型", "工具定义", "参数校验"), ("模式兼容", "失败修复"), ("并行工具调用",), ("Structured Output 与普通 JSON Prompt 有何差别？", "工具参数为何需要校验？"), "只验证成功路径，忽略模型返回缺字段或错误类型。", "阶段项目：UX Research Copilot"),
    WeekSpec(7, "UX Research Copilot", "研究资料解析、洞察提取、工具编排与人工确认", "可处理一份访谈记录的 Copilot", "将设计研究能力转化为 AI 产品与 Agent 工程优势。", ("任务拆分", "工具调用", "证据引用", "人工确认"), ("批处理", "提示词版本"), ("多模态研究资料",), ("何时必须加入人工确认？", "如何避免模型编造洞察？"), "输出看似合理但缺乏原文证据。", "阶段项目：UX Research Copilot"),
    WeekSpec(8, "可靠性、安全与阶段交付", "超时、重试、降级、成本记录、Prompt Injection 与 Demo", "UX Research Copilot v1", "生产应用必须在模型超时、拒答和恶意输入下仍可控。", ("超时", "指数退避", "降级", "输入隔离", "成本日志"), ("幂等性", "内容过滤"), ("红队测试",), ("重试何时会放大故障？", "Prompt Injection 如何进入系统？"), "只做正常演示，没有故障和安全场景。", "阶段项目交付"),
    WeekSpec(9, "文档解析与 Chunking", "文档加载、清洗、切块策略、重叠与元数据", "设计规范文档摄取流水线", "RAG 质量首先取决于进入索引的数据结构。", ("解析", "Chunk", "重叠", "Metadata"), ("语义切块", "表格处理"), ("版面感知解析",), ("Chunk 过大或过小有什么影响？", "元数据如何帮助检索？"), "直接套固定字符数，破坏章节语义。", "阶段项目：设计规范知识库 Agent"),
    WeekSpec(10, "Embedding 与向量检索", "Embedding、相似度、向量库、过滤与召回", "支持元数据过滤的检索 API", "把自然语言问题映射到可搜索的知识空间。", ("Embedding", "Top-k", "相似度", "过滤"), ("向量索引", "召回率"), ("多向量表示",), ("Embedding 模型更换会带来什么影响？", "Top-k 如何选择？"), "只看单条结果，不建立代表性查询集。", "阶段项目：设计规范知识库 Agent"),
    WeekSpec(11, "Hybrid Search、Reranking 与引用", "关键词+向量混合、重排、查询改写、证据引用", "可返回引用片段的问答链路", "提高长尾查询命中率，并让答案可核查。", ("Hybrid Search", "Reranking", "Query Rewrite", "Citation"), ("融合分数", "无答案策略"), ("多跳检索",), ("为什么需要 Reranker？", "引用怎样降低业务风险？"), "把检索分数当作答案正确率。", "阶段项目：设计规范知识库 Agent"),
    WeekSpec(12, "RAG 评测与数据隔离", "Golden Dataset、检索评测、答案评测、租户隔离与阶段交付", "设计规范知识库 Agent v1", "用可重复的评测而非主观感觉迭代 RAG。", ("测试集", "Recall@k", "引用正确性", "权限过滤"), ("评测偏差", "回归测试"), ("合成数据集",), ("RAG 应分别评测哪些环节？", "权限过滤应放在哪一层？"), "用模型自评代替全部人工核验。", "阶段项目交付"),
    WeekSpec(13, "Agent、Workflow 与 ReAct", "Agent 边界、确定性工作流、ReAct、状态与终止条件", "可解释的多步骤任务图", "选择正确的自动化形式，避免把所有逻辑都交给模型。", ("Workflow", "ReAct", "State", "终止条件"), ("计划与执行", "状态持久化"), ("动态规划",), ("何时不应该使用 Agent？", "ReAct 的主要风险是什么？"), "循环没有预算或终止条件。", "阶段项目：智能设计评审 Agent"),
    WeekSpec(14, "LangGraph 状态工作流", "节点、边、条件分支、循环、检查点与错误路由", "设计评审工作流骨架", "用显式状态图构建可调试、可恢复的 Agent 流程。", ("节点", "条件边", "状态更新", "Checkpoint"), ("子图", "并行分支"), ("事件驱动图",), ("状态图相比链式调用有什么优势？", "如何防止无限循环？"), "状态字段无所有权约定，节点互相覆盖。", "阶段项目：智能设计评审 Agent"),
    WeekSpec(15, "记忆、Human-in-the-loop 与 MCP", "短期/长期记忆、人工审批、MCP 工具接入", "带审批节点和外部工具的工作流", "在自动化效率与人的控制权之间建立清晰边界。", ("短期记忆", "长期记忆", "审批中断", "MCP"), ("记忆淘汰", "工具权限"), ("跨 Agent 上下文",), ("记忆和数据库记录有什么不同？", "MCP 解决了什么集成问题？"), "把全部聊天历史当作长期记忆。", "阶段项目：智能设计评审 Agent"),
    WeekSpec(16, "智能设计评审 Agent 交付", "多步骤评审、证据、重试、日志、Tracing 与成本", "智能设计评审 Agent v1", "形成体现设计背景、工程能力和产品判断的核心作品。", ("完整状态流", "人工确认", "错误恢复", "追踪"), ("成本预算", "离线回放"), ("多 Agent 对比实验",), ("如何解释你的 Agent 架构取舍？", "怎样证明评审结果可靠？"), "为了炫技使用过多 Agent，增加不确定性。", "阶段项目交付"),
    WeekSpec(17, "测试与 Agent Evaluation", "单元测试、集成测试、Golden Dataset、回归评测", "项目统一测试与评测框架", "团队需要知道每次修改是否让系统变好或变坏。", ("单元测试", "集成测试", "Golden Dataset", "回归"), ("评测抽样", "评分 Rubric"), ("在线实验",), ("非确定性系统怎样做回归测试？", "Golden Dataset 如何维护？"), "只测模型输出文本完全相等。", "生产化阶段"),
    WeekSpec(18, "可观测性、成本与性能", "结构化日志、Tracing、指标、缓存、限流与成本分析", "可观测的 Agent 服务", "定位慢、贵、错发生在哪个模型、工具和状态节点。", ("Trace ID", "延迟指标", "缓存", "限流"), ("采样", "成本分摊"), ("语义缓存",), ("缓存 LLM 响应有哪些风险？", "Agent 应记录哪些关键指标？"), "日志包含隐私或完整 Prompt。", "生产化阶段"),
    WeekSpec(19, "权限、安全与数据治理", "认证授权、租户隔离、密钥、Prompt Injection、防泄漏", "项目安全基线与威胁模型", "AI 应用会连接高权限工具，安全边界必须先于自动化能力。", ("最小权限", "Secret 管理", "数据隔离", "输入输出过滤"), ("审计日志", "威胁建模"), ("策略引擎",), ("Tool Calling 的主要攻击面是什么？", "如何做租户级数据隔离？"), "只在 Prompt 中写禁止事项，不做代码级权限。", "生产化阶段"),
    WeekSpec(20, "Docker、CI/CD 与部署", "容器、健康检查、持续集成、环境配置与云端部署", "可部署的 Agent Web 产品", "作品必须能由他人按说明复现、测试并部署。", ("Dockerfile", "Compose", "CI", "健康检查"), ("滚动发布", "迁移策略"), ("基础设施即代码",), ("容器化解决了什么问题？", "部署时如何管理数据库迁移？"), "本地可运行但部署说明不完整。", "生产化阶段交付"),
    WeekSpec(21, "作品集工程化整理", "README、架构图、决策记录、截图、演示数据与仓库卫生", "三至四个可审阅的项目仓库", "招聘方首先通过仓库结构判断工程成熟度。", ("README", "架构说明", "运行指南", "演示路径"), ("ADR", "版本发布"), ("开源协作规范",), ("优秀项目 README 应回答什么？", "如何解释技术债？"), "只展示最终界面，没有问题、约束和取舍。", "求职冲刺"),
    WeekSpec(22, "Python、API 与数据库面试", "高频基础题、代码阅读、调试题、API 设计与 SQL", "基础面试答案库与两次模拟", "基础工程能力决定能否通过第一轮技术筛选。", ("Python 数据模型", "HTTP", "SQL", "测试"), ("性能权衡", "并发基础"), ("解释器细节",), ("如何排查慢 API？", "事务隔离级别如何选择？"), "背答案但无法结合项目举例。", "求职冲刺"),
    WeekSpec(23, "RAG、Agent 与系统设计面试", "架构题、容量估算、评测、安全、故障与模拟工作任务", "系统设计稿与限时开发演练", "中高级面试更关注边界、失败模式和可验证性。", ("RAG 链路", "Agent 状态", "评测", "安全"), ("容量估算", "故障演练"), ("多区域部署",), ("如何设计企业知识助手？", "如何控制 Agent 失控成本？"), "只描述组件名，没有数据流和失败路径。", "求职冲刺"),
    WeekSpec(24, "简历、Demo 与投递", "技术简历、项目叙事、Demo 视频、GitHub 主页、行为面试与投递", "完整求职材料包和首轮投递", "把已完成能力翻译为招聘方能快速验证的证据。", ("成果量化", "项目叙事", "Demo", "投递检查"), ("岗位定制", "跟进记录"), ("技术内容输出",), ("请介绍一个最困难的技术取舍。", "为什么从设计转向 Agent 工程？"), "继续打磨而不开始投递。", "求职冲刺交付"),
)


DETAILED_DAY_TOPICS: dict[int, tuple[str, ...]] = {
    1: ("安装 Python 3.12 与建立虚拟环境", "变量、集合与类型提示", "函数、输入输出与异常", "类、数据模型与职责", "模块、包与配置", "独立完成需求清洗器", "复习、调试与学习记录"),
    2: ("Git 仓库、提交与分支", "HTTP、JSON 与状态码", "REST API 与接口契约", "创建 FastAPI 最小服务", "实现需求 CRUD 路由", "独立补充测试与错误响应", "复习、整理 README 与演示"),
    3: ("关系模型与 SQL 基础", "安装并连接 PostgreSQL", "表设计与 CRUD", "关系、索引与事务", "FastAPI 接入数据库", "迁移、测试与故障排查", "复习并完成数据层验收"),
    4: ("明确阶段项目范围与用户故事", "定义 Pydantic Schema 与 API", "实现服务层和核心规则", "加入日志、配置与异常处理", "完成数据库和接口集成", "独立修复问题并补测试", "验收、演示与阶段复盘"),
}


DAY_MODES: tuple[tuple[str, str], ...] = (
    ("概念与最小示例", "建立清晰心智模型，并跑通一个最小例子"),
    ("基础编码练习", "用短练习确认输入、处理和输出"),
    ("功能开发", "把本周概念接入当前项目"),
    ("工程化改造", "加入验证、错误处理、日志或测试"),
    ("项目开发", "完成可演示的项目里程碑"),
    ("独立挑战与问题修复", "独立完成关键部分并记录排查过程"),
    ("复习、整理和自由补充", "复盘、补缺、更新文档并准备下周"),
)


PLANS: dict[str, dict[str, object]] = {
    "plan-a-foundation": {
        "name": "方案 A：稳健基础版", "weeks": 24, "hours": "10-15 小时", "audience": "软件工程基础较弱、需要在职稳定推进的学习者", "pace": "每周一个主题，固定复习和补做缓冲", "depth": "工程基础最完整，LLM 与 Agent 逐步加深", "projects": "4 个阶段项目", "jobs": "初级 AI 应用工程师、Python 后端工程师、Agent 开发助理", "strength": "基础扎实、返工风险低", "risk": "作品集形成较慢，需坚持较长周期", "advice": "如果每周可投入时间不稳定，优先选择 A。", "mapping": [[i] for i in range(1, 25)],
    },
    "plan-b-job-ready": {
        "name": "方案 B：求职冲刺版", "weeks": 16, "hours": "20-25 小时", "audience": "能高强度学习、希望尽快形成作品集的人", "pace": "压缩基础，每 4 周交付一个可展示成果", "depth": "项目所需知识优先，快速进入 LLM、RAG 与 Agent", "projects": "4 个可展示成果", "jobs": "AI 应用工程师、RAG 工程师、Agent 工程师", "strength": "作品和面试材料形成快", "risk": "基础缺口容易在调试和系统设计阶段暴露", "advice": "只有能稳定投入 20 小时以上并接受补课时选择 B。", "mapping": [[1, 2], [3, 4], [5], [6, 7], [8], [9], [10, 11], [12], [13], [14], [15, 16], [17], [18, 19], [20], [21, 22], [23, 24]],
    },
    "plan-c-designer-ai": {
        "name": "方案 C：设计师优势版", "weeks": 20, "hours": "15-20 小时", "audience": "希望把设计、研究和产品能力转化为差异化优势的人", "pace": "保留工程主线，同时强化研究、体验与 Human-in-the-loop", "depth": "Agent 产品体验与工程实现并重", "projects": "3 个设计优势项目 + 1 个非设计项目", "jobs": "AI Agent 工程师、AI 产品工程师、Design Engineer、AI 原型工程师", "strength": "能形成清晰个人定位和差异化作品集", "risk": "容易偏重体验表达而忽略测试、数据库和部署", "advice": "与你的背景最匹配，默认从 C 开始；每周保留工程验收时间。", "mapping": [[1], [2], [3, 4], [5], [6], [7, 8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21, 22], [23, 24]],
    },
}


PROJECTS: tuple[dict[str, object], ...] = (
    {"dir": "project-01-tool-calling", "name": "设计需求分析助手", "domain": "设计需求澄清", "problem": "把自然语言设计需求转换为可追踪的目标、约束、风险和待确认问题。", "users": "产品设计师、产品经理、设计负责人", "workflow": ("提交原始需求", "校验并保存需求", "模型生成结构化分析", "调用项目规则工具", "用户确认或修订", "导出需求摘要"), "features": ("FastAPI 接口", "PostgreSQL 持久化", "JSON Schema", "Tool Calling", "日志和统一异常", "测试与 Docker"), "risks": ("模型遗漏硬约束", "敏感项目资料进入日志", "重复提交产生重复记录"), "metrics": ("结构化字段有效率", "人工修订率", "P95 API 延迟", "失败请求率")},
    {"dir": "project-02-rag-knowledge-base", "name": "设计规范知识库 Agent", "domain": "企业设计规范检索", "problem": "让团队从多版本规范中获得带引用、可核查且受权限约束的答案。", "users": "设计师、前端工程师、设计系统维护者", "workflow": ("上传文档", "解析清洗与切块", "生成 Embedding 和索引", "查询改写与混合检索", "Reranking", "生成带引用答案", "记录反馈与评测"), "features": ("文档上传", "Chunking", "Embedding", "Metadata", "Hybrid Search", "Reranking", "引用", "评测与权限隔离"), "risks": ("过期规范被优先召回", "跨团队数据泄漏", "引用与答案不一致"), "metrics": ("Recall@5", "引用正确率", "无答案识别率", "权限违规数")},
    {"dir": "project-03-agent-workflow", "name": "智能设计评审 Agent", "domain": "结构化设计评审", "problem": "依据目标、规范和证据完成多步骤评审，并在高风险结论前请求人工确认。", "users": "设计师、设计负责人、产品团队", "workflow": ("接收评审任务", "解析目标和设计说明", "检索规范", "分别检查可用性、一致性和可访问性", "合并证据", "人工确认高风险项", "输出行动清单"), "features": ("状态管理", "条件分支", "循环与终止", "工具调用", "Human-in-the-loop", "重试", "Tracing", "成本统计"), "risks": ("把主观偏好当作规则", "工作流无限循环", "评审证据不足"), "metrics": ("证据覆盖率", "人工接受率", "平均工具调用数", "单次评审成本")},
    {"dir": "project-04-capstone", "name": "供应商风险审查 Agent", "domain": "采购与合规", "problem": "自动整理供应商资料、检索政策、调用风险工具并生成需人工审批的审查建议。", "users": "采购专员、合规人员、业务负责人", "workflow": ("创建审查单", "解析供应商材料", "RAG 检索内部政策", "调用制裁与财务风险工具", "生成风险分级", "人工审批", "写入审计记录并通知结果"), "features": ("业务状态机", "RAG", "Tool Calling", "Agent 工作流", "人工确认", "最小权限", "评测", "容器化部署"), "risks": ("外部工具数据过期", "模型结论被误当最终决定", "敏感商业资料泄漏"), "metrics": ("高风险召回率", "误报率", "人工处理时长", "审计记录完整率")},
)


KNOWLEDGE_TOPICS: dict[str, dict[str, str]] = {
    "python": {"title": "Python 工程基础", "what": "用于快速开发 API、数据处理、评测和 Agent 工作流的通用编程语言。", "analogy": "像设计系统中的组件语言：语法是组件，模块是页面，包是产品。", "code": "def normalize_brief(text: str) -> str:\n    return ' '.join(text.strip().split())", "work": "编写服务、工具、数据流水线和自动化脚本。", "prod": "使用类型提示、测试、日志、依赖管理和清晰包结构。", "related": "FastAPI、数据库、LLM SDK、评测", "keywords": "Python 3.12 tutorial, typing, packaging, pytest"},
    "fastapi": {"title": "FastAPI", "what": "基于 Python 类型提示构建 Web API 的框架。", "analogy": "像给不同用户旅程定义清晰入口，每个路由都有输入、状态和结果。", "code": "from fastapi import FastAPI\napp = FastAPI()\n@app.get('/health')\ndef health() -> dict[str, str]:\n    return {'status': 'ok'}", "work": "把 Agent 能力封装为前端、自动化或其他服务可调用的接口。", "prod": "加入校验、认证、错误格式、日志、测试和健康检查。", "related": "HTTP、Pydantic、PostgreSQL、Docker", "keywords": "FastAPI official tutorial, dependency injection, testing"},
    "database": {"title": "PostgreSQL 与数据建模", "what": "可靠保存结构化业务数据的关系数据库。", "analogy": "像信息架构：表是内容类型，外键是内容关系，索引是快速入口。", "code": "SELECT id, title FROM requirements WHERE status = 'open' ORDER BY created_at DESC;", "work": "保存用户、任务、文档元数据、工具调用和评测结果。", "prod": "使用迁移、事务、索引、连接池、备份和权限。", "related": "FastAPI、RAG Metadata、Agent State", "keywords": "PostgreSQL tutorial, transactions, indexes, EXPLAIN"},
    "git": {"title": "Git 与协作", "what": "记录代码变化、支持分支协作和可追溯发布的版本控制系统。", "analogy": "像可合并的设计版本历史，但每次变更都有精确差异和上下文。", "code": "git switch -c feat/requirement-api\ngit add .\ngit commit -m 'feat: add requirement endpoint'", "work": "代码评审、发布、回滚和多人协作。", "prod": "小提交、清晰消息、受保护主分支和自动化检查。", "related": "GitHub、CI/CD、代码评审", "keywords": "Pro Git, branching, pull requests, conventional commits"},
    "docker": {"title": "Docker", "what": "把应用及运行依赖封装为可重复启动的容器。", "analogy": "像把字体、组件和素材连同设计稿一起打包，减少环境差异。", "code": "FROM python:3.12-slim\nWORKDIR /app\nCOPY . .\nCMD [\"python\", \"-m\", \"src.main\"]", "work": "统一本地、测试和部署环境。", "prod": "使用非 root 用户、健康检查、多阶段构建和最小镜像。", "related": "Compose、PostgreSQL、CI/CD、部署", "keywords": "Dockerfile best practices, Docker Compose, healthcheck"},
    "llm": {"title": "大语言模型基础", "what": "根据上下文预测并生成文本或结构化内容的模型。", "analogy": "像能力很强但没有项目背景、会受表达方式影响的协作者。", "code": "messages = [{'role': 'system', 'content': 'Return concise JSON.'}, {'role': 'user', 'content': brief}]", "work": "提取、分类、生成、规划和自然语言交互。", "prod": "记录模型版本、Token、延迟、成本、失败和评测结果。", "related": "Prompt、Structured Output、Tool Calling、Agent", "keywords": "LLM tokens, context window, model behavior, official API docs"},
    "prompt-engineering": {"title": "Prompt Engineering", "what": "通过明确目标、上下文、约束、示例和输出格式设计模型任务。", "analogy": "像一份高质量设计 Brief：目标、受众、限制和交付格式必须清楚。", "code": "prompt = f'''目标：提取约束\n输入：{brief}\n输出：JSON 数组，不要补充未知信息'''", "work": "提高输出一致性并降低误解。", "prod": "版本化 Prompt，用数据集回归评测，不把安全只寄托在 Prompt。", "related": "LLM、JSON Schema、评测", "keywords": "prompt engineering guide, few-shot, instruction hierarchy"},
    "tool-calling": {"title": "Tool Calling", "what": "让模型选择经过定义的函数，并生成符合模式的调用参数。", "analogy": "模型像服务设计中的调度员，工具才是真正执行动作的后台岗位。", "code": "def get_policy(section: str) -> dict[str, str]:\n    return {'section': section, 'content': '...'}", "work": "查询数据库、调用 API、计算、发送通知或创建工单。", "prod": "参数校验、权限检查、超时、幂等、审计和人工审批。", "related": "JSON Schema、API、Agent、MCP", "keywords": "function calling, tool use, structured outputs, JSON Schema"},
    "rag": {"title": "RAG", "what": "Retrieval-Augmented Generation（检索增强生成）先检索外部知识，再基于证据生成答案。", "analogy": "像设计评审前先翻规范并标出出处，而不是只靠记忆回答。", "code": "contexts = retriever.search(query, top_k=5)\nanswer = generate(query=query, contexts=contexts)", "work": "企业知识问答、政策检索、文档助手和研究资料分析。", "prod": "评测解析、检索、引用、权限和无答案策略。", "related": "Embedding、Metadata、Reranking、评测", "keywords": "RAG retrieval evaluation, hybrid search, reranking"},
    "agent": {"title": "AI Agent", "what": "能根据目标和状态选择步骤、调用工具并持续到终止条件的系统。", "analogy": "像有操作权限的项目协作者，不只给建议，还会按流程执行。", "code": "while state.steps < state.max_steps and not state.done:\n    state = run_next_step(state)", "work": "多步骤调查、审查、运营和知识工作流。", "prod": "显式状态、预算、终止、权限、审计和人工控制。", "related": "Workflow、Tool Calling、LangGraph、MCP", "keywords": "agent design patterns, ReAct, workflows, guardrails"},
    "langgraph": {"title": "LangGraph", "what": "用状态图组织可分支、循环、暂停和恢复的 Agent 工作流框架。", "analogy": "像服务蓝图：节点是触点，边是转移条件，状态是跨步骤共享信息。", "code": "builder.add_node('review', review_node)\nbuilder.add_edge('retrieve', 'review')", "work": "实现可观察、可恢复的复杂 Agent 流程。", "prod": "定义状态所有权、检查点、重试、终止和版本迁移。", "related": "Agent、状态机、Human-in-the-loop", "keywords": "LangGraph official docs, state graph, checkpointing"},
    "mcp": {"title": "MCP", "what": "Model Context Protocol（模型上下文协议）为模型应用提供统一的工具与资源接入方式。", "analogy": "像统一插件插口，让不同工具用一致方式被发现和调用。", "code": "# 伪代码：客户端先列出工具，再以结构化参数调用\ntools = client.list_tools()\nresult = client.call_tool('search_docs', {'query': query})", "work": "连接文件、数据库、设计工具和企业服务。", "prod": "限制服务器信任边界、工具权限、参数和返回数据。", "related": "Tool Calling、Agent、权限", "keywords": "Model Context Protocol specification, MCP servers, tool security"},
    "evaluation": {"title": "Agent Evaluation", "what": "用可重复数据、指标和人工 Rubric 判断系统是否可靠。", "analogy": "像可用性测试：不能只看一个顺利案例，要覆盖代表性任务和失败路径。", "code": "score = sum(case.passed for case in cases) / len(cases)", "work": "比较 Prompt、模型、检索和工作流版本。", "prod": "Golden Dataset、分层指标、回归门槛和抽样人工复核。", "related": "测试、RAG、Tracing、CI", "keywords": "LLM evaluation, golden dataset, retrieval metrics, regression testing"},
    "security": {"title": "AI 应用安全", "what": "保护数据、工具权限和业务流程免受泄漏、注入与越权。", "analogy": "像后台权限设计：界面上的提示不能替代真正的访问控制。", "code": "if tool_name not in user.allowed_tools:\n    raise PermissionError('tool not allowed')", "work": "认证、授权、输入过滤、审计和敏感信息处理。", "prod": "最小权限、租户隔离、Secret 管理、威胁建模和红队测试。", "related": "Tool Calling、RAG、部署、日志", "keywords": "OWASP LLM Top 10, prompt injection, least privilege"},
    "deployment": {"title": "部署与运维", "what": "把应用稳定发布到可访问环境，并持续监控和更新。", "analogy": "像把设计系统真正接入产品，而不只是留在演示稿中。", "code": "@app.get('/health')\ndef health() -> dict[str, str]:\n    return {'status': 'ok'}", "work": "提供 Demo、团队测试和真实用户访问。", "prod": "CI/CD、健康检查、回滚、日志、指标、备份和成本告警。", "related": "Docker、测试、安全、数据库", "keywords": "CI/CD, container deployment, observability, rollback"},
}
