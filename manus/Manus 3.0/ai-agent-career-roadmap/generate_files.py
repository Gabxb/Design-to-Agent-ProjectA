#!/usr/bin/env python3
"""Generate the local AI Agent career learning system.

This script creates Markdown, YAML, JSON, Python and shell artifacts. It does not
store secrets, and it preserves existing learning notes unless --force is passed.
Run: python generate_files.py
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
TODAY = "2026-08-20"
GENERATED_AT = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
FORCE = False
WRITTEN: list[str] = []
SKIPPED: list[str] = []

REFERENCES = """\n## 参考资源索引\n\n[1]: https://docs.python.org/3/ "Python 3 Documentation"\n[2]: https://fastapi.tiangolo.com/ "FastAPI Documentation"\n[3]: https://www.postgresql.org/docs/ "PostgreSQL Documentation"\n[4]: https://docs.docker.com/ "Docker Documentation"\n[5]: https://git-scm.com/doc "Git Documentation"\n[6]: https://developers.openai.com/api/docs/guides/function-calling "OpenAI Function Calling Guide"\n[7]: https://developers.openai.com/api/docs/guides/structured-outputs "OpenAI Structured Outputs Guide"\n[8]: https://docs.langchain.com/oss/python/langgraph/overview "LangGraph Overview"\n[9]: https://modelcontextprotocol.io/ "Model Context Protocol Specification"\n[10]: https://owasp.org/www-project-top-10-for-large-language-model-applications/ "OWASP Top 10 for LLM Applications"\n"""

WEEK_TOPICS: list[dict[str, str]] = [
    {"stage": "编程与本地开发基础", "title": "Python 环境、命令行与可维护脚本", "outcome": "可重复运行的 Python 命令行小工具", "must": "虚拟环境、函数、类型提示、文件路径", "understand": "模块与包", "later": "高级打包", "project": "设计需求结构化助手 API"},
    {"stage": "编程与本地开发基础", "title": "Python 数据建模、异常与测试", "outcome": "含单元测试的数据转换模块", "must": "dataclass、异常、pytest", "understand": "面向对象边界", "later": "设计模式", "project": "设计需求结构化助手 API"},
    {"stage": "编程与本地开发基础", "title": "Git、HTTP、JSON 与 FastAPI", "outcome": "带输入验证的 REST API", "must": "Git 分支、HTTP 状态码、Pydantic", "understand": "OpenAPI", "later": "异步并发", "project": "设计需求结构化助手 API"},
    {"stage": "编程与本地开发基础", "title": "SQL、PostgreSQL、日志与集成", "outcome": "设计需求结构化助手 API 阶段版", "must": "SQL CRUD、环境变量、日志、测试", "understand": "迁移", "later": "性能优化", "project": "设计需求结构化助手 API"},
    {"stage": "LLM 应用开发", "title": "LLM、Token 与提示词结构", "outcome": "可版本化的提示词实验记录", "must": "上下文、角色、约束、评估样例", "understand": "采样参数", "later": "微调", "project": "UX Research Copilot"},
    {"stage": "LLM 应用开发", "title": "结构化输出与 JSON Schema", "outcome": "研究访谈洞察结构化 API", "must": "Schema、验证、失败处理", "understand": "严格模式", "later": "复杂组合 Schema", "project": "UX Research Copilot"},
    {"stage": "LLM 应用开发", "title": "Tool Calling、重试与安全边界", "outcome": "受控工具调用循环", "must": "工具契约、超时、重试、审计日志", "understand": "降级策略", "later": "动态工具发现", "project": "UX Research Copilot"},
    {"stage": "LLM 应用开发", "title": "UX Research Copilot 集成冲刺", "outcome": "可演示的研究资料整理助手", "must": "API 集成、成本记录、README", "understand": "提示词 A/B 测试", "later": "多模态输入", "project": "UX Research Copilot"},
    {"stage": "RAG 知识库", "title": "文档解析、Chunking 与 Metadata", "outcome": "可追溯的文档切分流水线", "must": "解析、切分、元数据", "understand": "切分策略取舍", "later": "多模态解析", "project": "设计规范知识库 Agent"},
    {"stage": "RAG 知识库", "title": "Embedding 与向量检索", "outcome": "带过滤条件的基础检索服务", "must": "嵌入、相似度、索引、过滤", "understand": "向量数据库", "later": "索引调优", "project": "设计规范知识库 Agent"},
    {"stage": "RAG 知识库", "title": "Hybrid Search、Reranking 与引用", "outcome": "带引文的高质量问答链路", "must": "关键词检索、重排、引用", "understand": "查询改写", "later": "检索路由", "project": "设计规范知识库 Agent"},
    {"stage": "RAG 知识库", "title": "RAG 评测与数据隔离", "outcome": "设计规范知识库 Agent 阶段版", "must": "Golden Dataset、权限过滤、评测", "understand": "失败分类", "later": "自动优化", "project": "设计规范知识库 Agent"},
    {"stage": "Agent 工作流", "title": "Workflow 与 Agent 的边界", "outcome": "可审计的任务分解工作流", "must": "状态、节点、条件分支", "understand": "ReAct", "later": "多 Agent", "project": "智能设计评审 Agent"},
    {"stage": "Agent 工作流", "title": "LangGraph 状态图与持久化", "outcome": "可恢复的状态化工作流原型", "must": "State、Node、Edge、Checkpoint", "understand": "流式事件", "later": "子图", "project": "智能设计评审 Agent"},
    {"stage": "Agent 工作流", "title": "记忆、Human-in-the-loop 与 MCP", "outcome": "带人工确认的工具工作流", "must": "中断、批准、工具权限、MCP", "understand": "长期记忆", "later": "多服务器编排", "project": "智能设计评审 Agent"},
    {"stage": "Agent 工作流", "title": "智能设计评审 Agent 集成冲刺", "outcome": "可演示的设计评审工作流", "must": "终止条件、Tracing、成本统计", "understand": "失败恢复", "later": "协作型 Agent", "project": "智能设计评审 Agent"},
    {"stage": "生产化", "title": "测试策略与 Agent Evaluation", "outcome": "可重复运行的评测基线", "must": "单元测试、集成测试、Golden Dataset", "understand": "主观质量量表", "later": "在线评测", "project": "案例分流与合规助手"},
    {"stage": "生产化", "title": "Tracing、成本、缓存与安全", "outcome": "具备可观测性与风险控制的服务", "must": "结构化日志、速率限制、密钥管理", "understand": "缓存失效", "later": "威胁建模", "project": "案例分流与合规助手"},
    {"stage": "生产化", "title": "Docker、CI/CD 与部署", "outcome": "容器化、可部署的 Agent Web 产品", "must": "Docker Compose、健康检查、CI", "understand": "环境分层", "later": "Kubernetes", "project": "案例分流与合规助手"},
    {"stage": "生产化", "title": "产品打磨与上线演练", "outcome": "可部署产品的发布候选版", "must": "验收、回滚、运行手册", "understand": "SLO", "later": "容量规划", "project": "案例分流与合规助手"},
    {"stage": "求职冲刺扩展", "title": "作品集重构与架构表达", "outcome": "四个项目的展示版 README 和架构图", "must": "问题—方案—取舍—结果叙事", "understand": "指标表达", "later": "技术写作品牌", "project": "全作品集"},
    {"stage": "求职冲刺扩展", "title": "简历、GitHub 与 Demo", "outcome": "简历素材、主页和 Demo 脚本", "must": "STAR、项目量化、录屏流程", "understand": "个人品牌", "later": "内容运营", "project": "全作品集"},
    {"stage": "求职冲刺扩展", "title": "面试与系统设计", "outcome": "技术问答库与系统设计白板稿", "must": "Python、RAG、Agent、权衡", "understand": "容量估算", "later": "管理面试", "project": "全作品集"},
    {"stage": "求职冲刺扩展", "title": "模拟工作任务与投递复盘", "outcome": "端到端模拟任务和求职跟踪系统", "must": "需求澄清、拆分、交付、复盘", "understand": "协作沟通", "later": "谈判", "project": "全作品集"},
]

DAY_MODES = [
    ("概念与最小示例", "阅读并复现一个最小可运行示例，记录关键术语。"),
    ("基础编码练习", "实现一个小型、可测试的函数或模块，先写测试再补实现。"),
    ("功能开发", "把前两天的概念接到一个可用功能中，确保输入输出明确。"),
    ("工程化改造", "补充配置、日志、异常处理与文档，使功能可交接。"),
    ("项目开发", "将本周能力接入阶段项目，并更新项目任务板。"),
    ("独立挑战与问题修复", "在不查看参考答案的前提下完成变体任务并修复问题。"),
    ("复习、整理和自由补充", "整理笔记、完成自测，并为下一周准备环境与问题清单。"),
]

DETAILED_DAYS: dict[int, list[dict[str, str]]] = {
    1: [
        {"focus": "建立 Python 3.12 虚拟环境与项目骨架", "code": "创建 `src/cli.py`、`src/paths.py` 和 `tests/test_paths.py`；实现安全的项目路径解析函数。", "input": "一个相对路径和一个工作目录。", "output": "规范化后的 `Path` 或清晰的异常。"},
        {"focus": "函数、类型提示与数据验证", "code": "创建 `src/requirement.py`；定义 `DesignRequirement` 数据类与 `validate_title` 函数。", "input": "原始标题和约束列表。", "output": "可验证的需求对象。"},
        {"focus": "文件读写、JSON 与异常边界", "code": "创建 `src/storage.py`；实现读取和写入 UTF-8 JSON 的函数，并处理不存在的文件。", "input": "JSON 文件路径。", "output": "字典数据或可理解的错误消息。"},
        {"focus": "模块拆分、日志与配置", "code": "创建 `src/config.py`、`src/logging_config.py`；从环境变量读取非敏感配置。", "input": "`.env.example` 中定义的变量。", "output": "类型明确的配置对象和结构化日志。"},
        {"focus": "命令行最小产品", "code": "连接 CLI、需求模型与存储模块，支持保存一条设计需求草稿。", "input": "命令行参数或交互输入。", "output": "本地 JSON 草稿文件。"},
        {"focus": "独立实现：需求摘要格式化", "code": "独立新增 `format_requirement_summary`，输出适合交接给工程师的纯文本摘要。", "input": "一条有效需求。", "output": "格式化摘要。"},
        {"focus": "周复习与 Git 提交", "code": "补齐 README 的运行命令，运行测试并创建一条有意义的 Git commit。", "input": "本周代码和笔记。", "output": "可复现的 Week 01 基线。"},
    ],
    2: [
        {"focus": "列表、字典与需求字段转换", "code": "实现 `normalize_constraints`，将逗号分隔的输入转为去重列表。", "input": "原始约束文本。", "output": "规范化约束列表。"},
        {"focus": "类、组合与不可变数据", "code": "为需求对象增加 `AcceptanceCriterion` 值对象，不引入不必要继承。", "input": "验收条件文本。", "output": "可序列化对象。"},
        {"focus": "异常分类与可测试失败", "code": "定义 `ValidationError` 和 `StorageError`，让 CLI 返回不同退出码。", "input": "无效输入或异常文件。", "output": "有含义的错误结果。"},
        {"focus": "pytest 参数化与覆盖关键分支", "code": "为正常、边界和错误输入分别编写参数化测试。", "input": "测试样例表。", "output": "通过的测试套件。"},
        {"focus": "导出设计需求卡片", "code": "实现 Markdown 导出功能，将需求导出为可评审的卡片。", "input": "本地 JSON 需求。", "output": "Markdown 需求卡片。"},
        {"focus": "独立挑战：批量导入", "code": "不查看答案，设计一个批量导入 JSON 列表的接口和错误报告。", "input": "多条需求 JSON。", "output": "成功/失败统计。"},
        {"focus": "代码审查与周复盘", "code": "按模板完成一次自审，重构一个重复点，记录一个未解问题。", "input": "本周差异。", "output": "复盘与重构提交。"},
    ],
    3: [
        {"focus": "Git 工作流与 HTTP 心智模型", "code": "初始化 `project-01-tool-calling` 的仓库骨架，编写一个 `GET /health` 端点。", "input": "浏览器或 curl 请求。", "output": "200 JSON 健康状态。"},
        {"focus": "FastAPI 路径、查询与请求体", "code": "新增 `POST /requirements`，使用 Pydantic 模型验证请求体。", "input": "设计需求 JSON。", "output": "201 与验证后的对象。"},
        {"focus": "REST 设计与状态码", "code": "新增获取和不存在资源分支，显式返回 404。", "input": "有效或无效 ID。", "output": "一致的 API 响应。"},
        {"focus": "依赖注入与配置", "code": "使用依赖注入提供内存仓储；不得把配置硬编码进路由。", "input": "应用配置。", "output": "可替换的仓储接口。"},
        {"focus": "交互式文档与 API 冒烟测试", "code": "验证 `/docs`，写一个 API 测试并在 README 记录示例请求。", "input": "测试客户端。", "output": "可复现 API 示例。"},
        {"focus": "独立挑战：筛选端点", "code": "独立设计按优先级筛选需求的查询参数与异常规则。", "input": "可选 priority。", "output": "筛选后的列表。"},
        {"focus": "复盘：从设计稿到 API 契约", "code": "用一段文字说明 API 契约如何类似组件的接口，并整理下周数据库字段。", "input": "端点定义。", "output": "API 设计笔记。"},
    ],
    4: [
        {"focus": "SQL 与关系建模", "code": "为设计需求定义表结构和最小 CRUD SQL，说明每个字段的约束。", "input": "需求实体。", "output": "schema.sql 草案。"},
        {"focus": "PostgreSQL 连接与仓储边界", "code": "创建仓储接口和 PostgreSQL 实现占位，不在路由内写 SQL。", "input": "数据库 URL 环境变量。", "output": "可替换的数据访问层。"},
        {"focus": "数据库异常与事务", "code": "模拟唯一约束冲突并将其转换为合适的 API 错误。", "input": "重复的业务键。", "output": "409 或定义清楚的错误响应。"},
        {"focus": "日志、测试与测试数据", "code": "为创建需求写集成测试思路和结构化日志字段。", "input": "测试数据库配置。", "output": "测试计划与日志样例。"},
        {"focus": "阶段项目：设计需求结构化助手 API", "code": "完成健康检查、创建、查询、验证、日志和 README 的最小闭环。", "input": "API 请求。", "output": "阶段可演示服务。"},
        {"focus": "独立挑战：错误响应规范", "code": "独立定义错误 JSON 的字段与三种错误示例。", "input": "验证、资源、服务错误。", "output": "错误响应契约。"},
        {"focus": "第一阶段验收与补做", "code": "逐项勾选验收清单；为没完成的项目安排补做时段。", "input": "本周产出。", "output": "阶段复盘和下阶段风险表。"},
    ],
}

PLAN_INFO = {
    "plan-a-foundation": {
        "name": "方案 A：稳健基础版", "duration": "24 周", "hours": "每周 10–15 小时", "audience": "软件工程基础较弱、需要稳定推进的在职学习者", "rhythm": "每周 5 天主任务、1 天补做、1 天复盘；每四周一个阶段产出。", "depth": "基础工程能力优先，LLM 与 Agent 随基础逐层增加。", "projects": "4 个阶段/作品集项目", "direction": "初级后端、AI 应用开发、Agent 工程助理", "strength": "学习风险较低、知识缺口可持续补齐。", "risk": "作品集成型较慢，需要坚持完整周期。", "suggestion": "若每周无法稳定投入 15 小时或 Python 不熟，请优先选择。",
    },
    "plan-b-job-ready": {
        "name": "方案 B：求职冲刺版", "duration": "16 周", "hours": "每周 20–25 小时", "audience": "可集中投入并希望快速获得可展示项目的学习者", "rhythm": "每 4 周交付一个 Demo；工程基础按项目需求即时补齐。", "depth": "项目深度与展示优先，覆盖关键工程底座。", "projects": "4 个展示项目", "direction": "AI 应用/Agent 开发岗位、快速原型岗位", "strength": "作品集、部署、README 和面试叙事形成快。", "risk": "高强度，基础薄弱时容易形成理解债务。", "suggestion": "只有在每周可投入 20 小时以上且能规律复盘时选择。",
    },
    "plan-c-designer-ai": {
        "name": "方案 C：设计师优势版", "duration": "20 周核心 + 4 周求职冲刺扩展", "hours": "每周 15–20 小时", "audience": "具有设计、产品、用户研究或服务设计背景的转型者", "rhythm": "每周以用户问题、交互流程和工程实现三条线并进；每四周完成可讲述成果。", "depth": "Agent 工程主线与 AI 产品体验、人机协同、安全评测并重。", "projects": "3 个设计场景项目 + 1 个非设计综合项目", "direction": "AI Agent 开发、AI 产品工程、设计技术/智能体验岗位", "strength": "把已有设计优势转化为需求定义、评测、人机协同与产品叙事优势。", "risk": "容易偏重体验而忽略测试、数据库、部署等工程细节。", "suggestion": "默认方案。每周严格保留工程验收日，避免只做原型。",
    },
}

PROJECTS = [
    {
        "directory": "project-01-tool-calling", "name": "设计需求分析助手", "tagline": "把模糊设计需求转为可验证、可执行的工程任务。", "domain": "设计协作", "problem": "需求语言含混、验收标准缺失，导致设计与研发反复对齐。", "tools": "需求字段校验、优先级建议、验收标准生成", "stack": "FastAPI、PostgreSQL、Tool Calling、pytest、Docker", "milestone": "可审计的 API 与工具调用演示", "risks": "工具参数越权、模型输出格式错误、缺乏人工复核。",
    },
    {
        "directory": "project-02-rag-knowledge-base", "name": "设计规范知识库 Agent", "tagline": "让团队以引用可追溯的方式查询设计规范。", "domain": "设计知识管理", "problem": "规范分散且版本不清，设计师和工程师无法快速确认依据。", "tools": "上传、文档解析、检索、引用展示、权限过滤", "stack": "FastAPI、PostgreSQL、向量检索、RAG 评测、Docker", "milestone": "带来源引用和租户隔离的问答链路", "risks": "错误引用、跨租户泄露、过时文档、低质量切分。",
    },
    {
        "directory": "project-03-agent-workflow", "name": "智能设计评审 Agent", "tagline": "将设计评审转化为可控的多步骤协作工作流。", "domain": "设计评审", "problem": "评审标准不一致，风险项缺少记录与人工确认机制。", "tools": "规则检查、启发式检查、问题汇总、人工批准、报告导出", "stack": "LangGraph、FastAPI、Tracing、成本统计、Docker", "milestone": "带中断、恢复、终止条件的状态化评审流", "risks": "无限循环、错误自动决策、缺乏可解释轨迹。",
    },
    {
        "directory": "project-04-capstone", "name": "案例分流与合规助手", "tagline": "非设计领域的人工确认型业务流程 Agent。", "domain": "运营合规", "problem": "运营案例需要依据制度分流，自动执行存在高风险且需人工审批。", "tools": "文档检索、案例分类、风险评分、工单草稿、人工确认", "stack": "FastAPI、RAG、Tool Calling、LangGraph、评测、安全、部署", "milestone": "可部署的端到端业务工作流产品", "risks": "敏感数据、错误分流、权限不足、不可追溯决策。",
    },
]

KNOWLEDGE = [
    ("python", "Python", "Python 是本路线的主开发语言；重点是类型提示、模块、异常和测试。", "Python 让你把产品流程转成可读、可测试的步骤，像把设计流程拆成可复用组件。", "Python 3 Documentation", "https://docs.python.org/3/"),
    ("fastapi", "FastAPI", "FastAPI 用类型提示描述 HTTP API，并可生成交互式接口文档。", "把 API 看成跨团队组件的公开接口：输入、输出、状态和错误都应明确。", "FastAPI Documentation", "https://fastapi.tiangolo.com/"),
    ("database", "PostgreSQL 与数据库", "关系数据库保存可查询、可约束、可审计的业务事实。", "它像设计系统的单一事实来源，而不是散落在各处的临时备注。", "PostgreSQL Documentation", "https://www.postgresql.org/docs/"),
    ("git", "Git", "Git 是记录代码和文档演进的版本控制系统。", "它像设计文件的版本历史，但可追踪每一行变化并支持分支协作。", "Git Documentation", "https://git-scm.com/doc"),
    ("docker", "Docker", "Docker 用容器封装运行环境，减少开发与部署环境差异。", "它像把设计交付所需素材、规则和查看器封装为一个可重复打开的包。", "Docker Documentation", "https://docs.docker.com/"),
    ("llm", "LLM 基础", "大语言模型根据上下文生成或变换文本；它不是确定性规则引擎。", "把它当作需要明确任务单、可评审输出和安全边界的协作伙伴。", "OpenAI API Guides", "https://developers.openai.com/api/docs/guides/"),
    ("prompt-engineering", "Prompt Engineering", "提示词工程是把任务目标、上下文、限制与输出格式表达为可维护指令。", "它类似为复杂界面编写交互说明：目标清晰、边界可见、示例有代表性。", "OpenAI Prompting Guide", "https://developers.openai.com/api/docs/guides/prompt-engineering"),
    ("tool-calling", "Tool Calling", "工具调用让模型请求应用执行定义明确的函数，应用负责验证、执行与回传结果。", "模型提出操作意图，工程系统像安全的工作流引擎一样掌控真实执行。", "OpenAI Function Calling Guide", "https://developers.openai.com/api/docs/guides/function-calling"),
    ("rag", "RAG", "检索增强生成先从受控知识库检索证据，再基于证据回答并给出引用。", "它类似在设计评审中先定位规范原文，再做有来源的解释。", "OpenAI Retrieval Guide", "https://developers.openai.com/api/docs/guides/retrieval"),
    ("agent", "Agent", "Agent 将模型、工具、状态与决策循环组合起来完成多步骤任务。", "优先把高风险步骤设计为可视、可中断、可人工确认的服务蓝图。", "OpenAI Agents Guide", "https://developers.openai.com/api/docs/guides/agents"),
    ("langgraph", "LangGraph", "LangGraph 用图表达状态化工作流、分支、持久化和人工介入。", "它如同可执行的服务蓝图，让确定性步骤与模型驱动步骤共存。", "LangGraph Overview", "https://docs.langchain.com/oss/python/langgraph/overview"),
    ("mcp", "Model Context Protocol", "MCP 是为模型应用提供工具和上下文的开放协议。", "它像给不同 AI 客户端提供一致的插件接口，但必须明确权限边界。", "Model Context Protocol", "https://modelcontextprotocol.io/"),
    ("evaluation", "Evaluation", "评测用固定样例、指标和人工检查验证 Agent 是否可靠。", "它类似设计可用性测试：先定义成功，再用代表性任务验证。", "OpenAI Evaluation Guide", "https://developers.openai.com/api/docs/guides/evals"),
    ("security", "Agent 安全", "Agent 安全涵盖密钥、授权、输入隔离、提示词注入和可审计操作。", "安全是体验的一部分：用户应知道系统能做什么、何时需要批准以及为何拒绝。", "OWASP Top 10 for LLM Applications", "https://owasp.org/www-project-top-10-for-large-language-model-applications/"),
    ("deployment", "Deployment", "部署将应用、配置、依赖、监控和回滚策略一起交付到可运行环境。", "将它看作从原型到真实服务的交付规范，而不仅是把代码放到服务器。", "Docker Documentation", "https://docs.docker.com/"),
]


def write(rel: str, content: str, *, force: bool | None = None) -> None:
    """Write UTF-8 text while preserving local work by default."""
    allow = FORCE if force is None else force
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not allow:
        SKIPPED.append(rel)
        return
    if not content.endswith("\n"):
        content += "\n"
    path.write_text(content, encoding="utf-8")
    WRITTEN.append(rel)


def table(headers: list[str], rows: list[list[str]]) -> str:
    separator = "|" + "|".join(["---"] * len(headers)) + "|"
    result = ["| " + " | ".join(headers) + " |", separator]
    result.extend("| " + " | ".join(str(cell) for cell in row) + " |" for row in rows)
    return "\n".join(result)


def section(title: str, body: str) -> str:
    return f"## {title}\n\n{body.strip()}\n"


def plan_comparison() -> str:
    rows = []
    for key in ("plan-a-foundation", "plan-b-job-ready", "plan-c-designer-ai"):
        info = PLAN_INFO[key]
        rows.append([info["name"], info["duration"], info["hours"], info["projects"], info["direction"]])
    details = []
    for key in ("plan-a-foundation", "plan-b-job-ready", "plan-c-designer-ai"):
        info = PLAN_INFO[key]
        details.append(f"""## {info['name']}\n\n{info['audience']}。学习节奏为：{info['rhythm']}。技术深度为：{info['depth']}。\n\n| 维度 | 说明 |\n|---|---|\n| 就业方向 | {info['direction']} |\n| 优势 | {info['strength']} |\n| 风险 | {info['risk']} |\n| 选择建议 | {info['suggestion']} |\n""")
    return f"""# AI Agent 学习方案对比\n\n本地学习系统同时维护三套路线。它们共享工程质量标准和作品集目标，但用不同的时间预算与风险偏好安排课程。**当前默认执行方案为方案 C。**\n\n{table(['方案', '周期', '每周投入', '项目数量', '就业方向'], rows)}\n\n## 选择原则\n\n若你的可投入时间不稳定，选择方案 A；若需要在四个月内高强度形成作品集，选择方案 B；若你希望将设计、用户研究和交互优势转化为 Agent 产品工程能力，选择方案 C。方案 C 的 20 周核心课程后附加 4 周求职冲刺扩展，因此仍可在 24 周总路线图中完成完整的求职闭环。\n\n{''.join(details)}\n## 切换方案\n\n使用 `python update_plan.py switch-plan plan-a-foundation`（或 B/C）切换。脚本会先备份进度、保留个人笔记，并写入迁移记录；已完成任务不会被删除。\n\n{REFERENCES}\n"""


def plan_readme(plan_key: str) -> str:
    info = PLAN_INFO[plan_key]
    rows = [["适合人群", info["audience"]], ["学习周期", info["duration"]], ["每周投入", info["hours"]], ["学习节奏", info["rhythm"]], ["技术深度", info["depth"]], ["项目数量", info["projects"]], ["就业方向", info["direction"]], ["优势", info["strength"]], ["风险", info["risk"]], ["选择建议", info["suggestion"]]]
    if plan_key == "plan-c-designer-ai":
        special = "\n> 本方案为当前默认方案。第 1–20 周是核心训练；第 21–24 周作为作品集、面试与投递扩展，形成 24 周完整闭环。\n"
    else:
        special = "\n"
    return f"""# {info['name']}\n\n{special}\n{table(['维度', '说明'], rows)}\n\n## 使用方式\n\n本方案的高层安排位于 `CURRICULUM.md` 和 `WEEKLY_SCHEDULE.md`。默认执行目录是根目录的 `weeks/`，它按方案 C 创建了 24 周可执行任务；切换方案时请使用 `update_plan.py` 保留历史进度。\n\n{REFERENCES}\n"""


def plan_curriculum(plan_key: str) -> str:
    info = PLAN_INFO[plan_key]
    if plan_key == "plan-a-foundation":
        phases = [("1–4", "工程底座", "Python、Git、API、SQL、测试"), ("5–8", "LLM 应用", "提示词、结构化输出、工具调用"), ("9–12", "RAG", "解析、检索、引用、评测"), ("13–16", "Agent", "工作流、状态、人工确认、MCP"), ("17–20", "生产化", "评测、观测、安全、Docker、部署"), ("21–24", "求职", "作品集、简历、面试、模拟任务")]
    elif plan_key == "plan-b-job-ready":
        phases = [("1–4", "项目一", "API、Tool Calling、部署 Demo"), ("5–8", "项目二", "RAG 知识库与评测"), ("9–12", "项目三", "Agent 工作流与人机协同"), ("13–16", "项目四与求职", "综合产品、GitHub、简历、面试")]
    else:
        phases = [("1–4", "设计需求到 API", "设计语言结构化、Python、FastAPI、数据库"), ("5–8", "研究体验 AI", "UX Research Copilot、提示词、Schema、工具"), ("9–12", "规范知识体验", "RAG、引用、权限、知识架构"), ("13–16", "智能设计评审", "LangGraph、Human-in-the-loop、MCP"), ("17–20", "生产化产品", "评测、安全、部署、运营"), ("21–24", "求职冲刺扩展", "作品集叙事、Demo、面试、模拟工作")]
    return f"""# {info['name']}：课程结构\n\n该课程不将设计背景视为需要绕开的短板，而是将其转化为需求澄清、信息架构、质量评测和人机协同设计能力。每个阶段都要求提交代码、文档、验收记录和复盘。\n\n{table(['周次', '阶段', '关键能力'], [list(item) for item in phases])}\n\n## 统一工程质量线\n\n所有阶段遵守：Python 类型提示；环境变量保存密钥；输入验证；结构化日志；关键功能测试；README 可复现；Docker 化；不使用虚构真实用户数据。框架或模型 API 可能变化，实施前必须核对官方文档。\n\n{REFERENCES}\n"""


def plan_schedule(plan_key: str) -> str:
    factor = {"plan-a-foundation": "以 10–15 小时预算完成核心任务，非核心内容可进入补做区。", "plan-b-job-ready": "以 20–25 小时预算压缩复习时间，但不得跳过测试、README 和 Demo。", "plan-c-designer-ai": "以 15–20 小时预算同时维护工程任务与体验设计证据。"}[plan_key]
    rows = []
    for index, item in enumerate(WEEK_TOPICS, 1):
        if plan_key == "plan-b-job-ready" and index > 16:
            continue
        if plan_key == "plan-c-designer-ai" and 20 < index <= 24:
            label = "扩展"
        else:
            label = item["stage"]
        rows.append([f"{index:02d}", label, item["title"], item["outcome"]])
    return f"""# 每周安排\n\n{factor}\n\n{table(['周', '阶段', '主题', '周产出'], rows)}\n\n> 切换计划后，仅重新安排未完成的后续任务；已经完成的成果和个人笔记仍由 `progress/progress.json` 与备份文件保留。\n"""


def roadmap() -> str:
    rows = [[f"{i:02d}", item["stage"], item["title"], item["outcome"], item["project"]] for i, item in enumerate(WEEK_TOPICS, 1)]
    return f"""# 24 周 AI Agent 开发路线图\n\n本路线图以**方案 C：设计师优势版**为默认执行方案。其 20 周核心能力训练之后，安排 4 周求职冲刺扩展，使你能够把工程产出组织为可面试、可演示、可复盘的作品集。学习计划强调项目驱动，但每周必须有工程验收与复盘，避免停留在界面原型或聊天演示。\n\n## 阶段总览\n\n| 阶段 | 周次 | 核心目标 | 阶段成果 |\n|---|---|---|---|\n| 编程与本地开发基础 | 1–4 | 能独立创建、测试和运行后端服务 | 设计需求结构化助手 API |\n| LLM 应用开发 | 5–8 | 能可靠调用模型、校验输出并安全执行工具 | UX Research Copilot |\n| RAG 知识库 | 9–12 | 能构建带引用、可评测、可隔离的知识服务 | 设计规范知识库 Agent |\n| Agent 工作流 | 13–16 | 能实现状态、分支、终止与人工确认 | 智能设计评审 Agent |\n| 生产化 | 17–20 | 能评测、观测、保护并部署产品 | 可部署 Agent Web 产品 |\n| 求职冲刺扩展 | 21–24 | 能呈现作品集并处理真实工程表达 | 简历、Demo、面试库、模拟任务 |\n\n## 每周地图\n\n{table(['周', '阶段', '主题', '可展示产出', '主项目'], rows)}\n\n## 使用规则\n\n先阅读 `START_HERE.md`，然后打开当前周的 `WEEK_PLAN.md`。每日完成后，把结果、耗时和问题写入 `progress/DAILY_LOG.md` 与 `progress/progress.json`。当工作或生活导致中断时，使用 `update_plan.py pause`；恢复时使用 `update_plan.py resume` 生成恢复清单。\n\n{REFERENCES}\n"""


def day_content(week: int, day: int, item: dict[str, str]) -> str:
    mode, generic = DAY_MODES[day - 1]
    detailed = DETAILED_DAYS.get(week, [])[day - 1] if week in DETAILED_DAYS else None
    focus = detailed["focus"] if detailed else f"{item['title']}：{mode}"
    coding = detailed["code"] if detailed else f"在对应项目的 `src/` 中新增一个小而可测试的模块，围绕“{item['must']}”实现一个明确输入输出。不要复制完整参考实现；先写测试、再完成最小实现。"
    inputs = detailed["input"] if detailed else f"本周笔记、一个最小样例和 `{item['project']}` 的当前代码。"
    outputs = detailed["output"] if detailed else f"一个可运行的小功能、至少一个测试和一条学习记录。"
    level = "基础" if week <= 4 else ("进阶" if week <= 16 else "工程实践")
    depth_note = "这是详细任务日。按顺序执行，并在每项任务结束后记录结果。" if week <= 4 else "这是任务框架日。先依据本周目标补充具体样例，再将你的决策和结果写入日志。"
    return f"""# Day {day:02d}：{focus}\n\n{depth_note}\n\n## 今日目标\n\n- 理解并能用自己的话解释：{item['must']}。\n- 完成一个最小、可运行且可验证的实现。\n- 记录一个工程决策或疑问，形成可复习证据。\n\n## 岗位价值\n\n{item['title']} 对真实 Agent 开发的价值在于：团队需要的不只是一个能演示的模型调用，而是能说明输入、输出、失败路径和责任边界的功能。设计背景可帮助你把用户目标和交互证据说清楚，但必须用代码、测试和日志证明方案可交付。\n\n## 前置知识\n\n- 已完成本周 `WEEK_PLAN.md` 中的上一日任务或完成等价补做。\n- 知道本项目的运行命令与 `.env.example` 的作用。\n- 知道密钥只能通过环境变量提供，不能写入代码或日志。\n\n## 今日学习内容\n\n{generic} 对设计师而言，可以把工程功能理解为一个具有状态、输入规范、异常状态和验收条件的交互组件；代码就是让这个组件在不同情境下稳定工作的规则集合。英文缩写首次出现时请在笔记中写出全称，例如 API（Application Programming Interface，应用程序编程接口）。\n\n## 今日任务\n\n{table(['任务', '预计时间', '难度', '输入', '输出', '文件路径'], [
    ['阅读并复现最小示例', '45 分钟', level, inputs, '可运行记录', f'weeks/week-{week:02d}/notes/'],
    ['实现与测试', '90 分钟', level, '最小样例', outputs, f'projects/{project_dir_for_week(week)}/'],
    ['记录与提交', '30 分钟', '基础', '运行结果', '学习日志与 Git 提交', 'progress/DAILY_LOG.md'],
])}\n\n## 编码任务\n\n{coding}\n\n创建或修改文件时，先在项目 README 的“本周实验”小节列出文件目的。明确写出函数的输入类型、输出类型和错误行为。运行命令以项目 README 为准；成功标准是测试通过、手工样例符合预期、错误输入被可理解地处理。\n\n## 独立完成部分\n\n你必须独立完成：函数签名、至少一个边界测试、错误消息文本，以及对实现取舍的简短说明。不要查看 `reference-solution/`；该目录仅在你明确要求“生成参考实现”后才会包含完整答案。\n\n## 验收标准\n\n- [ ] 功能可以运行。\n- [ ] 输入输出符合要求。\n- [ ] 错误输入被正确处理。\n- [ ] 密钥没有写进代码。\n- [ ] README 已更新。\n- [ ] 学习记录已完成。\n\n## 常见错误\n\n| 现象 | 优先排查方向 |\n|---|---|\n| 代码能运行但测试失败 | 检查函数输入边界、类型和断言是否一致。 |\n| 环境变量未生效 | 检查 `.env` 是否被 Git 忽略、变量名是否与配置一致。 |\n| 模型或外部调用结果不稳定 | 先记录输入、输出、超时和重试；不要用“模型不稳定”代替分析。 |\n| 文档与实现不一致 | 更新 README 命令和示例，并重新执行一次。 |\n\n## 今天需要记录的内容\n\n在 `progress/DAILY_LOG.md` 中记录实际耗时、完成的文件、一次失败及修复方式、仍不理解的概念和明天的第一步。必要时在 `progress/PROBLEMS.md` 中登记可复现问题。\n\n## 补充学习区\n\n### 我的理解\n\n\n### 我遇到的问题\n\n\n### 我的解决方法\n\n\n### 需要以后复习的内容\n\n\n### 自定义补充\n\n\n"""


def project_dir_for_week(week: int) -> str:
    if week <= 8:
        return "project-01-tool-calling"
    if week <= 12:
        return "project-02-rag-knowledge-base"
    if week <= 16:
        return "project-03-agent-workflow"
    return "project-04-capstone"


def week_plan(week: int, item: dict[str, str]) -> str:
    day_rows = []
    for day, (mode, generic) in enumerate(DAY_MODES, 1):
        detailed = DETAILED_DAYS.get(week, [])[day - 1] if week in DETAILED_DAYS else None
        focus = detailed["focus"] if detailed else f"{item['title']}：{mode}"
        day_rows.append([f"Day {day}", focus, "2–3 小时" if day < 6 else "2 小时"])
    weekly_hours = "15–20 小时" if week <= 20 else "12–18 小时"
    return f"""# Week {week:02d}：{item['title']}\n\n## 本周目标\n\n本周处于“{item['stage']}”阶段。完成后，你应能说明并实践：{item['must']}；同时交付 {item['outcome']}。\n\n## 对应岗位能力\n\n将用户问题拆成可验证的技术任务；实现小而清晰的模块；对失败路径负责；以文档和验收标准说明工程决策。\n\n## 每日任务总览\n\n{table(['日程', '主题', '建议投入'], day_rows)}\n\n## 时间分配\n\n建议投入 **{weekly_hours}**：概念与阅读 20%，编码与测试 45%，项目集成 20%，复盘与补做 15%。\n\n## 必须掌握\n\n{item['must']}。\n\n## 需要理解\n\n{item['understand']}。\n\n## 暂时了解\n\n{item['later']}。此部分不应阻塞本周项目。\n\n## 本周编码任务\n\n在 `projects/{project_dir_for_week(week)}/` 中完成一个可运行的最小功能，并至少新增一个正向测试和一个异常/边界测试。代码需要类型提示、异常处理和可读日志；密钥只能从环境变量读取。\n\n## 本周项目里程碑\n\n项目：**{item['project']}**。本周里程碑：**{item['outcome']}**。将实际实现状态记录到项目 `TASKS.md`。\n\n## 工程要求\n\n- 所有新增 Python 函数必须有类型提示。\n- 关键输入必须验证；异常不能被静默吞掉。\n- README 中的命令必须经过一次实际运行验证。\n- 提交前运行测试，并在提交信息中使用英文动词短语。\n\n## 验收标准\n\n- [ ] 本周最小功能可以运行。\n- [ ] 至少包含两类测试样例。\n- [ ] 关键错误被记录并可理解地返回。\n- [ ] 没有提交真实 API Key、令牌或个人数据。\n- [ ] README、学习日志和项目任务表已更新。\n\n## 常见风险\n\n| 风险 | 预防或处理 |\n|---|---|\n| 追逐新框架而没有完成最小闭环 | 先完成本周验收，再把新框架列入“暂时了解”。 |\n| 只展示正常路径 | 在实现前先写一个无效输入或外部调用失败的测试。 |\n| 设计叙事替代工程证据 | 用运行命令、测试结果和日志字段作为证据。 |\n\n## 补做任务\n\n若时间不足，优先保留：最小功能、一个测试、README 运行说明和学习日志。其余优化进入下一周的 Day 7。\n\n## 提前完成后的进阶任务\n\n为本周功能增加一个可观测性字段、一个输入边界测试，或写一段“教学版与生产版”的差异说明。\n\n## 本周面试问题\n\n请用 2 分钟回答：为什么选择当前的数据结构、API 契约或工作流边界？它在输入错误、外部服务失败和需要人工确认时如何表现？\n\n## 周末复盘方式\n\n阅读 `REVIEW.md`，从“完成事实、失败样例、工程改进、下周风险”四个角度各写一段。不要只记录感受。\n\n## 下周准备事项\n\n阅读 Week {min(week + 1, 24):02d} 的 `WEEK_PLAN.md`，检查本地运行环境、未完成任务与需准备的非敏感示例数据。\n\n{REFERENCES}\n"""


def week_readme(week: int, item: dict[str, str]) -> str:
    return f"""# Week {week:02d} 学习包\n\n本周主题：**{item['title']}**。先阅读 `WEEK_PLAN.md`，再按 `days/day-01.md` 至 `day-07.md` 执行。`notes/` 用于个人笔记，`exercises/` 仅放练习题和你的解答；不要把密钥、真实客户数据或隐私材料放入仓库。\n\n## 文件导航\n\n| 文件/目录 | 用途 |\n|---|---|\n| `WEEK_PLAN.md` | 完整周计划与验收要求 |\n| `CHECKLIST.md` | 可勾选执行清单 |\n| `REVIEW.md` | 周末复盘引导 |\n| `days/` | 每日独立任务 |\n| `resources/` | 官方资料索引和检索关键词 |\n| `notes/` | 你的笔记，不会被默认覆盖 |\n| `exercises/` | 独立练习与提交物 |\n"""


def week_checklist(week: int, item: dict[str, str]) -> str:
    return f"""# Week {week:02d} 执行清单\n\n## 开始前\n\n- [ ] 已阅读 `WEEK_PLAN.md`。\n- [ ] 本地环境可运行上周项目或本周最小示例。\n- [ ] `.env` 未被 Git 跟踪，`.env.example` 仅含变量示例。\n\n## 每日完成\n\n- [ ] Day 1：概念和最小示例。\n- [ ] Day 2：基础编码练习。\n- [ ] Day 3：功能开发。\n- [ ] Day 4：工程化改造。\n- [ ] Day 5：项目开发。\n- [ ] Day 6：独立挑战与问题修复。\n- [ ] Day 7：复习、整理和自由补充。\n\n## 周验收\n\n- [ ] 已达到：{item['outcome']}。\n- [ ] 新增功能有可重复的运行命令。\n- [ ] 关键路径至少有正向和错误样例。\n- [ ] 已更新项目 README、`progress/DAILY_LOG.md` 和 `progress/progress.json`。\n- [ ] 已执行一次英文 Git commit，例如 `feat: add week {week:02d} milestone`。\n"""


def week_review(week: int, item: dict[str, str]) -> str:
    return f"""# Week {week:02d} 复盘\n\n## 完成事实\n\n本周实际完成了哪些文件、命令和测试？请写可核验的事实，而不是“学习了很多”。\n\n## 关键概念\n\n用自己的话解释：{item['must']}。指出一个你仍不确定的概念，并写下验证计划。\n\n## 失败样例与修复\n\n记录一次错误输入、依赖问题或逻辑偏差：它如何复现、如何定位、如何修复、以后如何避免？\n\n## 项目证据\n\n本周里程碑“{item['outcome']}”是否已在项目 README 中留下运行步骤、截图/Demo 说明或测试结果？\n\n## 下周承诺\n\n列出最多三个未完成事项，并明确放到下周的哪一天；不要把未完成事项默认为“以后再说”。\n"""


def resource_index(week: int, item: dict[str, str]) -> str:
    keywords = item['must'].replace('、', '，')
    return f"""# Week {week:02d} 参考资源索引\n\n本目录只保存可检索的官方资源入口和学习用途，不复制外部文档。框架、模型和 API 会变化，编码前必须核对当前官方文档。\n\n| 主题 | 为什么阅读 | 官方检索关键词 |\n|---|---|---|\n| 本周主题 | {item['title']} | {keywords} |\n| API 工程 | 输入验证、文档和错误处理 | FastAPI tutorial Pydantic validation |\n| Agent 工程 | 工具、状态和人机协同 | function calling LangGraph human in the loop |\n| 安全 | 避免提示词注入与权限越界 | OWASP LLM prompt injection |\n\n{REFERENCES}\n"""


def knowledge_doc(slug: str, name: str, what: str, designer: str, official: str, url: str) -> str:
    code = """```python\nfrom dataclasses import dataclass\n\n@dataclass(frozen=True)\nclass TaskInput:\n    text: str\n\ndef validate_input(value: str) -> TaskInput:\n    if not value.strip():\n        raise ValueError(\"text must not be empty\")\n    return TaskInput(text=value.strip())\n```"""
    return f"""# {name}\n\n## 这是什么\n\n{what}\n\n## 为什么 Agent 开发需要它\n\nAgent 系统必须把不确定的模型能力放进确定的工程边界中。{name} 能帮助你定义输入、保存证据、控制副作用或验证输出，从而让系统可维护、可测试并能交接。\n\n## 设计师可以如何理解\n\n{designer}\n\n## 最小代码示例\n\n{code}\n\n## 工作中的使用方式\n\n在真实项目中，先把职责写入 API 契约或工作流节点说明，再通过测试、日志和验收标准验证。不要把关键业务规则只藏在提示词或界面说明中。\n\n## 教学简化方案\n\n使用一个本地样例、一个纯函数和两个测试样例完成学习闭环；先不接入真实客户数据、真实密钥或不可逆外部操作。\n\n## 生产环境方案\n\n补充配置分层、认证授权、输入大小限制、超时重试、结构化日志、监控、评测集、数据隔离和回滚方案。具体实现应以团队安全规范和当前官方文档为准。\n\n## 常见错误\n\n- 将演示成功等同于可靠性，没有记录错误路径。\n- 将密钥、内部 URL 或真实样例直接提交到仓库。\n- 忽略版本变化，复制过期代码后不核对官方文档。\n\n## 排查方法\n\n先缩小到可复现的最小输入，记录版本、配置（不含密钥）、请求标识和完整异常堆栈；然后检查输入契约、依赖版本和权限边界。\n\n## 面试问题\n\n如何解释 {name} 在教学原型与生产服务中的差异？当输入异常、外部依赖超时或模型输出不满足约束时，你的系统如何处理？\n\n## 与其他技术的关系\n\n{name} 与 API、数据库、测试、部署和安全并非独立知识点；它应当通过清晰契约连接到项目中的数据流、控制流和可观测性设计。\n\n## 官方文档名称或检索关键词\n\n[{official}]({url})。检索关键词：`{name} Python production guide`。\n\n## 最后核对日期\n\n{TODAY}。\n\n## 我的补充笔记\n\n### 我的理解\n\n\n### 我的项目例子\n\n\n### 待核对问题\n\n\n"""


def project_requirements(project: dict[str, str]) -> str:
    return f"""# {project['name']}：产品需求\n\n## 1. 问题与目标\n\n**问题：**{project['problem']}\n\n**目标：**{project['tagline']} 本项目是作品集工程模板，不使用真实客户、员工或敏感案例数据。\n\n## 2. 目标用户与用户故事\n\n| 用户 | 用户故事 | 成功标准 |\n|---|---|---|\n| 一线使用者 | 当我提交一个结构化任务时，我希望得到有依据、可编辑的建议，以便更快完成下一步。 | 输入被验证，结果包含状态和依据。 |\n| 审核者 | 当系统准备执行高影响操作时，我希望先查看证据并批准或拒绝。 | 未批准时绝不执行副作用操作。 |\n| 维护者 | 当结果异常时，我希望能定位请求、工具调用和错误。 | 日志可关联、密钥不泄露。 |\n\n## 3. 范围与非目标\n\n本项目实现：{project['tools']}。本项目不承诺自主执行不可逆操作、不代替专业判断、不使用未授权数据。\n\n## 4. 功能需求\n\n- 输入验证：拒绝空值、超长值和不符合 Schema 的数据。\n- 业务编排：将确定性规则与模型建议分开，记录每一步状态。\n- 人工确认：对创建工单、导出或高风险结论设置批准节点。\n- 审计与可观测性：记录请求标识、耗时、错误类别和成本估算，不记录密钥。\n\n## 5. API 设计\n\n| 方法 | 路径 | 说明 | 成功响应 |\n|---|---|---|---|\n| `GET` | `/health` | 健康检查 | `200` 状态对象 |\n| `POST` | `/tasks` | 创建待处理任务 | `201` 任务与状态 |\n| `GET` | `/tasks/{{task_id}}` | 查询任务与审计摘要 | `200` 状态对象 |\n| `POST` | `/tasks/{{task_id}}/approve` | 人工确认下一步 | `200` 已批准状态 |\n\n## 6. JSON Schema（示意）\n\n```json\n{{\n  "type": "object",\n  "required": ["title", "content"],\n  "properties": {{\n    "title": {{"type": "string", "minLength": 1, "maxLength": 120}},\n    "content": {{"type": "string", "minLength": 1, "maxLength": 5000}},\n    "requires_approval": {{"type": "boolean", "default": true}}\n  }},\n  "additionalProperties": false\n}}\n```\n\n## 7. 非功能要求\n\n使用环境变量读取配置；关键函数提供类型提示；对外部调用设置超时和有限重试；关键路径具备测试；Docker Compose 能在本地启动依赖；README 中包含准确命令。\n\n## 8. 验收\n\n详见 `ACCEPTANCE_CRITERIA.md`、`TEST_PLAN.md`、`SECURITY.md` 和 `EVALUATION.md`。\n\n{REFERENCES}\n"""


def project_architecture(project: dict[str, str]) -> str:
    return f"""# {project['name']}：架构说明\n\n## 架构目标\n\n架构目标是将用户输入、确定性验证、模型/检索建议、工具调用和人工批准隔离为可测试组件。该项目的技术栈建议为：{project['stack']}。\n\n## 组件与责任\n\n| 组件 | 责任 | 不应承担的责任 |\n|---|---|---|\n| API 层 | 认证入口、请求验证、响应契约 | 直接拼接数据库 SQL 或存放模型密钥 |\n| 应用服务 | 编排用例、事务边界、状态转换 | 依赖具体 Web 框架细节 |\n| Agent/检索层 | 受控推理、检索、工具选择 | 直接执行未批准的外部副作用 |\n| 工具适配层 | 参数验证、超时、重试、审计 | 绕开权限和人工确认 |\n| 数据层 | 持久化业务状态、评测集、审计摘要 | 记录原始密钥或敏感提示词 |\n| 观测层 | 日志、指标、追踪、成本 | 替代业务校验 |\n\n## 数据与控制流\n\n```mermaid\nflowchart LR\n    U[用户] --> A[FastAPI 输入验证]\n    A --> S[应用服务与状态]\n    S --> R[检索或规则]\n    S --> M[模型建议]\n    M --> T[受控工具适配层]\n    T --> H{{需要人工确认?}}\n    H -- 是 --> P[批准/拒绝节点]\n    H -- 否 --> D[(PostgreSQL)]\n    P --> D\n    S --> O[结构化日志与评测]\n```\n\n## 关键边界\n\n1. 模型只能提出工具调用意图，应用代码负责 Schema 校验、权限验证和实际执行。\n2. 检索结果需要带来源标识；生成内容不得伪造引用。\n3. 高影响操作默认需要人工确认，并记录批准者、时间与依据。\n4. 密钥只存在于部署环境变量或秘密管理系统中；日志默认脱敏。\n\n## 教学版与生产版\n\n教学版使用本地示例数据、同步调用和最小日志，目的是学习组件边界。生产版需要认证、限流、队列/超时、持久化检查点、数据隔离、监控告警、备份与回滚。\n\n{REFERENCES}\n"""


def project_task_list(project: dict[str, str]) -> str:
    return f"""# {project['name']}：任务板\n\n## Backlog\n\n- [ ] 明确用户输入、成功标准与拒绝条件。\n- [ ] 建立 FastAPI 路由、配置、日志和健康检查。\n- [ ] 实现核心领域对象与仓储接口。\n- [ ] 为模型、检索或工具调用定义 Schema 和失败路径。\n- [ ] 加入人工确认节点和审计字段。\n- [ ] 编写单元、集成和评测样例。\n- [ ] 容器化、编写运行手册并准备 Demo。\n\n## 本周状态\n\n| 周次 | 计划任务 | 实际结果 | 阻塞项 |\n|---|---|---|---|\n| 待填写 |  |  |  |\n\n> 更新任务时保留历史记录；不要用新的结论覆盖旧的学习证据。\n"""


def project_readme(project: dict[str, str]) -> str:
    return f"""# {project['name']}\n\n{project['tagline']}\n\n## 作品集叙事\n\n本项目面向“{project['domain']}”场景，解决的问题是：{project['problem']}。展示时应说明用户痛点、数据与安全边界、架构选择、失败路径、人工确认点和下一步改进，不应把模型输出包装为完全自动化的正确答案。\n\n## 目录\n\n| 路径 | 用途 |\n|---|---|\n| `src/` | 教学用应用骨架 |\n| `tests/` | 关键路径测试 |\n| `docs/` | 运行、决策与 Demo 资料 |\n| `data/` | 仅存放脱敏/合成样例 |\n| `reference-solution/` | 默认不提供完整答案 |\n\n## 本地运行\n\n```bash\npython -m venv .venv\n# macOS/Linux: source .venv/bin/activate\n# Windows PowerShell: .venv\\Scripts\\Activate.ps1\npip install -e .[dev]\nuvicorn src.main:app --reload\npytest\n```\n\n复制 `.env.example` 为 `.env` 后再填写自己的本地变量；绝不提交 `.env`。运行前请核对当前框架和模型 API 的官方文档。\n\n## 当前状态\n\n- [ ] 需求已确认\n- [ ] 架构已评审\n- [ ] 最小 API 可运行\n- [ ] 安全与评测基线已建立\n- [ ] Docker 本地启动成功\n- [ ] Demo 与作品集叙事已完成\n\n{REFERENCES}\n"""


def project_acceptance(project: dict[str, str]) -> str:
    return f"""# {project['name']}：验收标准\n\n- [ ] 健康检查返回预期状态，且不暴露敏感配置。\n- [ ] 不合法输入收到清晰、稳定的错误响应。\n- [ ] 核心流程含成功、失败和需要批准三类测试。\n- [ ] 工具调用参数通过应用侧 Schema 验证。\n- [ ] 需要人工确认的操作在未批准时不会执行。\n- [ ] 日志包含请求关联标识和错误类别，不含 API Key 或原始敏感数据。\n- [ ] RAG 场景能显示真实来源；无法检索时会诚实说明。\n- [ ] README 的运行命令经过验证，Docker Compose 可启动。\n- [ ] Demo 能在 5 分钟内说明问题、方案、取舍与局限。\n"""


def project_test_plan(project: dict[str, str]) -> str:
    return f"""# {project['name']}：测试计划\n\n| 层级 | 目标 | 最小样例 | 通过条件 |\n|---|---|---|---|\n| 单元测试 | 验证纯函数、Schema 和状态转换 | 空文本、超长文本、正常文本 | 所有分支符合契约 |\n| API 集成测试 | 验证端点与错误码 | 创建、查询、不存在资源 | 响应结构稳定 |\n| 工具调用测试 | 验证参数和副作用边界 | 无效参数、超时、拒绝 | 不执行未批准副作用 |\n| RAG/Agent 评测 | 验证回答依据与流程终止 | Golden Dataset | 引用正确、拒答合理、可追踪 |\n| 手工体验检查 | 验证人工确认体验 | 批准、拒绝、恢复 | 状态可理解、无死循环 |\n\n测试数据只能使用合成或脱敏资料。失败样例应成为回归测试，而不是在修复后删除。\n"""


def project_security(project: dict[str, str]) -> str:
    return f"""# {project['name']}：安全说明\n\n## 威胁与控制\n\n| 风险 | 控制措施 | 验证方式 |\n|---|---|---|\n| 密钥泄露 | 环境变量、`.gitignore`、日志脱敏 | 扫描仓库和日志样例 |\n| 提示词注入 | 不信任外部内容、明确工具白名单、隔离指令 | 恶意文档测试集 |\n| 越权工具调用 | 应用侧授权、Schema 校验、人工确认 | 未授权请求测试 |\n| 跨用户数据泄露 | 租户/用户过滤、最小权限 | 隔离测试 |\n| 不可追溯决策 | 请求标识、审计摘要、引用来源 | 追踪演练 |\n\n## 不可违反的规则\n\n不得把真实 API Key、访问令牌、真实个人数据或内部 URL 写入提交、截图、提示词样例或错误日志。外部文档和工具输出都应视为不可信数据，而非系统指令。\n\n参考：OWASP LLM 应用安全指南 [10]。\n\n{REFERENCES}\n"""


def project_evaluation(project: dict[str, str]) -> str:
    return f"""# {project['name']}：评测设计\n\n## Golden Dataset\n\n建立最少 15 条合成样例，覆盖正常请求、模糊请求、恶意输入、无检索证据、工具失败和人工拒绝。每条样例保留输入、期望行为、允许输出范围、引用要求和人工判定。\n\n## 指标\n\n| 指标 | 定义 | 目标/解释 |\n|---|---|---|\n| 契约合规率 | 输出是否通过 Schema 与业务校验 | 必须持续监控 |\n| 引用正确率 | 引用是否支持关键结论 | RAG 场景核心指标 |\n| 安全拒绝率 | 高风险或越权请求是否被拒绝 | 不以“完成率”替代安全 |\n| 人工批准前拦截率 | 高影响操作是否在批准前停止 | 应为 100% |\n| 任务完成质量 | 由明确量表和人工抽检衡量 | 记录评审依据 |\n\n## 评测运行记录\n\n| 日期 | 数据集版本 | 应用版本 | 结果摘要 | 改进决定 |\n|---|---|---|---|---|\n| 待填写 | v0 |  |  |  |\n"""


def project_deployment(project: dict[str, str]) -> str:
    return f"""# {project['name']}：部署说明\n\n## 本地容器运行\n\n```bash\ncp .env.example .env\ndocker compose up --build\n```\n\n部署前确认 `.env` 仅保存在本机或受控秘密管理系统；不要将其上传到 GitHub。生产部署需要补充认证、TLS、数据库备份、健康检查、监控、速率限制、迁移计划和回滚步骤。\n\n## 发布检查\n\n- [ ] 依赖版本已锁定或记录。\n- [ ] 环境变量清单与部署平台配置一致。\n- [ ] 健康检查与错误日志已验证。\n- [ ] Golden Dataset 已在候选版本运行。\n- [ ] 回滚方式和负责人已明确。\n"""


def project_changelog() -> str:
    return f"""# Changelog\n\n## {TODAY}\n\n### Added\n- 初始化项目文档、应用骨架、测试骨架和安全/评测计划。\n\n### Changed\n- 无。\n\n### Fixed\n- 无。\n\n### Affected Files\n- 项目根目录文档与教学骨架。\n"""


def pyproject(name: str) -> str:
    package = name.replace("-", "_")
    return f"""[build-system]\nrequires = [\"setuptools>=69\"]\nbuild-backend = \"setuptools.build_meta\"\n\n[project]\nname = \"{name}\"\nversion = \"0.1.0\"\ndescription = \"Teaching scaffold for an AI Agent portfolio project\"\nrequires-python = \">=3.12\"\ndependencies = [\n  \"fastapi>=0.115\",\n  \"uvicorn[standard]>=0.30\",\n  \"pydantic>=2.8\",\n]\n\n[project.optional-dependencies]\ndev = [\"pytest>=8.0\", \"httpx>=0.27\", \"ruff>=0.6\"]\n\n[tool.pytest.ini_options]\npythonpath = [\".\"]\ntestpaths = [\"tests\"]\n\n[tool.ruff]\nline-length = 100\n"""


def project_main(project: dict[str, str]) -> str:
    return f'''"""Teaching-only API skeleton for {project['name']}."""
from __future__ import annotations

import logging
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
app = FastAPI(title="{project['name']}", version="0.1.0")


class TaskRequest(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    content: str = Field(min_length=1, max_length=5000)
    requires_approval: bool = True


class TaskResponse(BaseModel):
    task_id: str
    state: Literal["pending_approval", "accepted"]


@app.get("/health")
def health() -> dict[str, str]:
    return {{"status": "ok"}}


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskRequest) -> TaskResponse:
    """Create a local teaching task; replace in exercises, not in this scaffold."""
    task_id = str(uuid4())
    logger.info("task_created task_id=%s title_length=%s", task_id, len(payload.title))
    task_state: Literal["pending_approval", "accepted"] = (
        "pending_approval" if payload.requires_approval else "accepted"
    )
    return TaskResponse(task_id=task_id, state=task_state)


@app.post("/tasks/{{task_id}}/approve")
def approve_task(task_id: str) -> dict[str, str]:
    if not task_id.strip():
        raise HTTPException(status_code=400, detail="task_id must not be empty")
    # Independent task: persist status and add authorization before treating this as production code.
    return {{"task_id": task_id, "state": "approved"}}
'''


def project_test() -> str:
    return '''from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health_returns_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task_requires_content() -> None:
    response = client.post("/tasks", json={"title": "Example", "content": "A safe synthetic example."})
    assert response.status_code == 201
    assert response.json()["state"] == "pending_approval"
'''


def project_compose(project: dict[str, str]) -> str:
    return f"""services:\n  app:\n    build: .\n    command: uvicorn src.main:app --host 0.0.0.0 --port 8000\n    ports:\n      - \"8000:8000\"\n    environment:\n      APP_ENV: development\n      DATABASE_URL: postgresql://app:app@db:5432/{project['directory'].replace('-', '_')}\n    depends_on:\n      db:\n        condition: service_healthy\n  db:\n    image: postgres:16\n    environment:\n      POSTGRES_DB: {project['directory'].replace('-', '_')}\n      POSTGRES_USER: app\n      POSTGRES_PASSWORD: app\n    healthcheck:\n      test: [\"CMD-SHELL\", \"pg_isready -U app\"]\n      interval: 5s\n      timeout: 5s\n      retries: 10\n"""


def update_manifest() -> None:
    entries: list[dict[str, Any]] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".backups" in path.parts or "__pycache__" in path.parts:
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative == "config/file_manifest.json":
            continue
        plan = "plan-c-designer-ai" if relative.startswith(("weeks/", "roadmap/")) else None
        week = None
        for part in path.parts:
            if part.startswith("week-"):
                week = part
                break
        topic = next((slug for slug, *_ in KNOWLEDGE if f"knowledge-base/{slug}/" in relative), None)
        entries.append({
            "path": relative,
            "file_type": path.suffix.lstrip(".") or "no_extension",
            "plan": plan,
            "week": week,
            "topic": topic,
            "created_at": GENERATED_AT,
            "last_updated": GENERATED_AT,
            "user_modified": False,
        })
    manifest = {"schema_version": 1, "generated_at": GENERATED_AT, "root": "ai-agent-career-roadmap", "files": entries}
    path = ROOT / "config/file_manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if "config/file_manifest.json" not in WRITTEN:
        WRITTEN.append("config/file_manifest.json")


def generate_root_files() -> None:
    write("README.md", f"""# AI Agent Career Roadmap\n\n这是一个可脱离聊天记录独立使用的本地 AI Agent 开发学习系统。默认路线为 **方案 C：设计师优势版**，以 20 周核心能力训练加 4 周求职冲刺扩展，形成 24 周完整闭环。所有学习内容、进度、项目定义、模板与脚本都保存在本目录。\n\n## 从哪里开始\n\n1. 阅读 [`START_HERE.md`](START_HERE.md)。\n2. 查看三套方案对比：[`plans/PLAN_COMPARISON.md`](plans/PLAN_COMPARISON.md)。\n3. 默认从 [`weeks/week-01/days/day-01.md`](weeks/week-01/days/day-01.md) 开始。\n4. 每日结束后更新 `progress/`；使用 `python update_plan.py --help` 查看操作。\n\n## 常用命令\n\n```bash\npython generate_files.py\npython update_plan.py status\npython update_plan.py complete --task week-01-day-01\npython scripts/check_files.py\npython scripts/pdf_from_markdown.py --all\n```\n\nWindows PowerShell 用户可使用 `scripts/setup.ps1` 和 `scripts/generate_pdfs.ps1`；macOS/Linux 用户使用对应 `.sh` 脚本。详见 `START_HERE.md`。\n\n## 工程原则\n\n学习项目使用 Python 3.12、FastAPI、PostgreSQL、React/Next.js（在产品阶段）、Git 和 Docker。所有代码、变量名、文件名和 Git commit 使用英文；正文使用中文。真实 API Key 只能在本地 `.env` 或部署平台秘密管理系统中保存，绝不提交。\n\n{REFERENCES}\n""")
    write("START_HERE.md", """# 开始学习\n\n## 第一次使用\n\n先在本地解压目录，并使用 Python 3.12 或更高版本。执行 `python generate_files.py` 会补齐缺失文件而不默认覆盖既有笔记；执行 `python scripts/check_files.py` 检查结构；执行 `python scripts/pdf_from_markdown.py --all` 生成/刷新 PDF。\n\n## 默认执行方案\n\n当前方案为 **方案 C：设计师优势版**。它将设计、用户研究、信息架构与 Human-in-the-loop（人机协同）转化为工程优势，但仍要求每周完成测试、日志、数据库、部署或评测等工程证据。\n\n## 今天应该做什么\n\n打开：`weeks/week-01/days/day-01.md`。完成前不要跳到模型或多 Agent 框架。第一天的目标是建立可重复的 Python 环境、项目结构和最小测试习惯。\n\n## 更新进度\n\n```bash\npython update_plan.py status\npython update_plan.py hours --value 2.5\npython update_plan.py complete --task week-01-day-01\npython update_plan.py note --text \"今天理解了虚拟环境的隔离作用。\"\n```\n\n每次更新前，脚本会在 `.backups/` 创建备份并向 `CHANGELOG.md` 写入记录。\n\n## 暂停、恢复和切换\n\n```bash\npython update_plan.py pause --reason \"出差\"\npython update_plan.py resume\npython update_plan.py switch-plan plan-a-foundation\n```\n\n切换仅重新安排未完成任务；原进度和个人笔记保留。\n""")
    write("CHANGELOG.md", f"""# Changelog\n\n## {TODAY}\n\n### Added\n- 初始化可本地保存的 AI Agent 学习系统、三套学习方案和 24 周路线图。\n- 创建周计划、每日任务、知识库、项目定义、进度管理和自动化脚本。\n\n### Changed\n- 无。\n\n### Fixed\n- 无。\n\n### Affected Files\n- 根目录及所有初始化学习文件。\n""")
    write("LICENSE", """MIT License\n\nCopyright (c) 2026\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.\n\nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.\n""")
    write("requirements.txt", """fastapi>=0.115\nuvicorn[standard]>=0.30\npydantic>=2.8\npytest>=8.0\nhttpx>=0.27\nPyYAML>=6.0\n""")
    write(".gitignore", """.venv/\n__pycache__/\n.pytest_cache/\n.ruff_cache/\n*.py[cod]\n.env\n.env.*\n!.env.example\n*.sqlite3\n.coverage\nhtmlcov/\nnode_modules/\ndist/\nbuild/\n.DS_Store\n.vscode/settings.json\n.backups/\nreports/*.log\n""")
    write(".env.example", """# Copy to .env locally. Never commit real secrets.\nAPP_ENV=development\nLOG_LEVEL=INFO\nDATABASE_URL=postgresql://app:app@localhost:5432/agent_learning\nLLM_API_KEY=replace_with_your_local_secret\nLLM_MODEL=verify_current_provider_model\n""")
    write("config/learner_profile.yaml", """learner:\n  current_role: designer\n  programming_foundation: some_code_experience\n  target_role: ai_agent_development_engineer\n  goal: participate_in_real_projects_and_interviews\n  learning_style: project_driven_engineering_first\n  preferred_language: zh-CN\n  code_language: English\n  default_environment:\n    - VS Code\n    - GitHub\n    - local_computer\n""")
    write("config/current_plan.yaml", """current_plan: plan-c-designer-ai\nplan_name: 方案 C：设计师优势版\ncore_duration_weeks: 20\ncareer_extension_weeks: 4\ncurrent_week: 1\ncurrent_day: 1\nstatus: active\nlast_updated: 2026-08-20\n""")
    write("config/learning_settings.yaml", """schedule:\n  default_weekly_hours: 15\n  target_weekly_hours_min: 15\n  target_weekly_hours_max: 20\n  daily_rhythm:\n    day_1: concept_and_minimum_example\n    day_2: coding_exercise\n    day_3: feature_development\n    day_4: engineering_hardening\n    day_5: project_development\n    day_6: independent_challenge_and_fixes\n    day_7: review_and_buffer\nengineering:\n  python_version: \"3.12\"\n  api_framework: FastAPI\n  database: PostgreSQL\n  frontend: React_or_Next.js\n  version_control: Git\n  container: Docker\ncontent_policy:\n  preserve_user_notes: true\n  create_backup_before_update: true\n  source_of_truth: Markdown\n  pdf_generated_from_markdown: true\n""")
    write(".typst-content-manifest.json", json.dumps({"task_kind": "markdown-to-pdf", "output": "pdf", "signals": [], "hard_constraints": ["Chinese CJK text", "table of contents", "page numbers"], "content_features": {"code_blocks": 12, "defined_terms": 12, "portrait_images": 0}}, ensure_ascii=False, indent=2))


def generate_plans_and_roadmap() -> None:
    write("plans/PLAN_COMPARISON.md", plan_comparison())
    for key in PLAN_INFO:
        write(f"plans/{key}/README.md", plan_readme(key))
        write(f"plans/{key}/CURRICULUM.md", plan_curriculum(key))
        write(f"plans/{key}/WEEKLY_SCHEDULE.md", plan_schedule(key))
    write("roadmap/24_WEEK_ROADMAP.md", roadmap())
    matrix_rows = [["Python/工程", "函数、类型、测试、Git、Docker", "Week 1–4、17–20", "API 与项目代码"], ["LLM 应用", "Prompt、Schema、Tool Calling", "Week 5–8", "UX Research Copilot"], ["RAG", "解析、检索、引用、评测", "Week 9–12", "知识库 Agent"], ["Agent", "状态、HITL、MCP、Tracing", "Week 13–16", "设计评审 Agent"], ["生产化", "安全、评测、部署、运维", "Week 17–20", "综合项目"], ["求职", "叙事、Demo、面试、投递", "Week 21–24", "作品集与简历"]]
    write("roadmap/SKILL_MATRIX.md", f"""# 能力矩阵\n\n{table(['能力簇', '能力要点', '主要周次', '证据'], matrix_rows)}\n\n技能进度以 `progress/SKILL_PROGRESS.md` 为准。每项能力只有在能演示、解释取舍并通过验收后才标记为“已掌握”。\n""")
    write("roadmap/JOB_READY_CHECKLIST.md", """# 求职就绪检查清单\n\n## 工程证据\n\n- [ ] 至少 3 个可运行项目，至少 1 个非设计领域综合项目。\n- [ ] 每个项目都有 README、需求、架构、测试、安全、评测和部署说明。\n- [ ] 每个项目展示失败处理、人工确认或安全边界。\n- [ ] GitHub 提交历史可读，密钥和真实敏感数据未被提交。\n\n## 作品集表达\n\n- [ ] 每个项目能在 3 分钟说明问题、用户、架构、取舍和结果。\n- [ ] 每个项目有 5 分钟可运行 Demo 脚本。\n- [ ] 架构图中的模型、工具、数据、人工确认和日志边界清晰。\n\n## 面试准备\n\n- [ ] 能解释 Python 类型、异常、测试、HTTP、SQL 和 Docker。\n- [ ] 能解释 RAG 的切分、检索、引用、评测与数据隔离。\n- [ ] 能解释 Agent 与 Workflow 的边界、状态、终止、工具权限和 HITL。\n- [ ] 能给出一次失败案例、修复方式和以后预防方案。\n\n## 投递前\n\n- [ ] 简历与目标岗位描述一致。\n- [ ] GitHub 主页置顶项目和联系方式准确。\n- [ ] 投递记录包含岗位、日期、项目版本和后续动作。\n""")


def generate_weeks() -> None:
    for week, item in enumerate(WEEK_TOPICS, 1):
        prefix = f"weeks/week-{week:02d}"
        write(f"{prefix}/README.md", week_readme(week, item))
        write(f"{prefix}/WEEK_PLAN.md", week_plan(week, item))
        write(f"{prefix}/CHECKLIST.md", week_checklist(week, item))
        write(f"{prefix}/REVIEW.md", week_review(week, item))
        write(f"{prefix}/resources/README.md", resource_index(week, item))
        write(f"{prefix}/notes/README.md", f"# Week {week:02d} 个人笔记\n\n此目录用于保存你的术语解释、代码片段、截图说明与复盘。默认生成不会覆盖你新增的个人文件。\n")
        write(f"{prefix}/exercises/README.md", f"# Week {week:02d} 独立练习\n\n将你的独立实现、测试和简短说明放在这里。不要在开始前查看完整参考答案；`reference-solution/` 仅在明确请求后生成。\n")
        for day in range(1, 8):
            write(f"{prefix}/days/day-{day:02d}.md", day_content(week, day, item))


def generate_knowledge() -> None:
    for slug, name, what, designer, official, url in KNOWLEDGE:
        write(f"knowledge-base/{slug}/OVERVIEW.md", knowledge_doc(slug, name, what, designer, official, url))


def generate_projects() -> None:
    for project in PROJECTS:
        base = f"projects/{project['directory']}"
        write(f"{base}/README.md", project_readme(project))
        write(f"{base}/REQUIREMENTS.md", project_requirements(project))
        write(f"{base}/ARCHITECTURE.md", project_architecture(project))
        write(f"{base}/TASKS.md", project_task_list(project))
        write(f"{base}/ACCEPTANCE_CRITERIA.md", project_acceptance(project))
        write(f"{base}/TEST_PLAN.md", project_test_plan(project))
        write(f"{base}/SECURITY.md", project_security(project))
        write(f"{base}/EVALUATION.md", project_evaluation(project))
        write(f"{base}/DEPLOYMENT.md", project_deployment(project))
        write(f"{base}/CHANGELOG.md", project_changelog())
        write(f"{base}/.env.example", "APP_ENV=development\nDATABASE_URL=postgresql://app:app@localhost:5432/app\nLLM_API_KEY=replace_with_your_local_secret\n")
        write(f"{base}/pyproject.toml", pyproject(project['directory']))
        write(f"{base}/docker-compose.yml", project_compose(project))
        write(f"{base}/src/__init__.py", "\"\"\"Teaching package.\"\"\"\n")
        write(f"{base}/src/main.py", project_main(project))
        write(f"{base}/tests/test_smoke.py", project_test())
        write(f"{base}/docs/README.md", "# 项目补充文档\n\n保存 ADR（架构决策记录）、Demo 截图说明和部署运行手册。\n")
        write(f"{base}/data/README.md", "# 示例数据\n\n仅保存合成或已脱敏的示例。不得保存真实用户、客户、公司内部或可识别个人信息。\n")
        write(f"{base}/reference-solution/README.md", "# Reference Solution\n\n默认不包含完整参考实现。先独立完成练习；只有明确请求“生成参考实现”时，才在此目录添加完整答案。\n")


def generate_templates_and_tracking() -> None:
    write("templates/DAILY_NOTE_TEMPLATE.md", """# YYYY-MM-DD 学习记录\n\n## 今日目标\n\n## 实际完成\n\n## 运行命令与结果\n\n## 错误与修复\n\n## 我的理解\n\n## 明天第一步\n""")
    write("templates/WEEKLY_REVIEW_TEMPLATE.md", """# Week XX 复盘\n\n## 完成事实\n\n## 关键概念\n\n## 失败样例与修复\n\n## 项目证据\n\n## 下周承诺\n""")
    write("templates/PROJECT_README_TEMPLATE.md", """# Project Name\n\n## Problem\n\n## Users\n\n## Architecture\n\n## Local Run\n\n## Tests\n\n## Security Boundaries\n\n## Demo Script\n\n## Limitations\n""")
    write("templates/PROJECT_REQUIREMENT_TEMPLATE.md", """# Requirements\n\n## Problem and Goal\n\n## User Stories\n\n## Functional Requirements\n\n## Non-functional Requirements\n\n## API Contract\n\n## Acceptance Criteria\n""")
    write("templates/CODE_REVIEW_TEMPLATE.md", """# Code Review\n\n## Intent\n\n## Correctness\n\n## Error Handling\n\n## Security and Secrets\n\n## Tests\n\n## Documentation\n\n## Follow-up\n""")
    write("templates/LEARNING_LOG_TEMPLATE.md", """# Learning Log\n\n| Date | Week/Day | Planned Hours | Actual Hours | Output | Problem | Next Step |\n|---|---|---:|---:|---|---|---|\n| YYYY-MM-DD | week-XX/day-XX |  |  |  |  |  |\n""")
    write("templates/INTERVIEW_ANSWER_TEMPLATE.md", """# Interview Answer\n\n## Question\n\n## Short Answer\n\n## Context\n\n## Decision and Trade-offs\n\n## Evidence\n\n## Follow-up\n""")
    progress = {"current_plan": "plan-c-designer-ai", "current_week": 1, "current_day": 1, "completed_tasks": [], "learning_hours": 0.0, "skills": {}, "problems": [], "custom_notes": [], "status": "active", "paused_at": None, "last_updated": TODAY}
    write("progress/progress.json", json.dumps(progress, ensure_ascii=False, indent=2))
    write("progress/DAILY_LOG.md", "# 每日学习日志\n\n| 日期 | 周/日 | 实际小时 | 完成事实 | 问题 | 明天第一步 |\n|---|---|---:|---|---|---|\n| 待填写 | week-01/day-01 |  |  |  |  |\n")
    write("progress/WEEKLY_STATUS.md", "# 周状态\n\n| 周次 | 状态 | 计划小时 | 实际小时 | 核心产出 | 阻塞项 |\n|---|---|---:|---:|---|---|\n| Week 01 | not_started | 15 | 0 | Python 基础工程骨架 |  |\n")
    write("progress/SKILL_PROGRESS.md", "# 技能进度\n\n| 技能 | 状态 | 证据 | 下次复习 |\n|---|---|---|---|\n| Python 工程基础 | 未开始 |  |  |\n| FastAPI | 未开始 |  |  |\n| 数据库 | 未开始 |  |  |\n| LLM / Tool Calling | 未开始 |  |  |\n| RAG | 未开始 |  |  |\n| Agent 工作流 | 未开始 |  |  |\n| 评测与安全 | 未开始 |  |  |\n| 部署 | 未开始 |  |  |\n")
    write("progress/PROBLEMS.md", "# 问题记录\n\n| 日期 | 问题 | 复现步骤 | 已尝试 | 下一步 | 状态 |\n|---|---|---|---|---|---|\n| 待填写 |  |  |  |  | open |\n")
    write("progress/COMPLETED_TASKS.md", "# 已完成任务\n\n完成任务后请使用 `update_plan.py complete --task <task-id>`。脚本会同步更新 `progress.json`、本文件和 CHANGELOG。\n")


def generate_interview_and_career() -> None:
    interview_topics = {
        "python": ["什么是类型提示，为什么它对团队协作有价值？", "如何区分异常处理、返回值和日志责任？"],
        "api": ["如何设计一个可演进的 REST API？", "如何处理输入验证、状态码和幂等性？"],
        "database": ["如何从业务需求设计表和约束？", "为什么不要在路由处理函数中直接写复杂 SQL？"],
        "llm": ["Token、上下文窗口和成本如何影响产品设计？", "如何减少结构化输出失败？"],
        "rag": ["如何解释 Chunking、检索、重排和引用？", "如何评测 RAG 的正确性与可追溯性？"],
        "agent": ["Agent 与 Workflow 应如何选择？", "如何避免无限循环和越权工具调用？"],
        "system-design": ["如何设计带人工确认的 Agent 服务？", "如何处理追踪、缓存、限流和数据隔离？"],
        "project-questions": ["你在项目中做过什么关键取舍？", "讲述一次失败、定位和修复过程。"],
        "behavioral": ["如何与设计、产品、工程共同定义模糊需求？", "如何在不确定信息下沟通风险？"],
    }
    for slug, questions in interview_topics.items():
        items = "\n".join(f"## 问题 {i}\n\n{q}\n\n请使用 `templates/INTERVIEW_ANSWER_TEMPLATE.md` 组织回答：先给短答，再给项目证据、权衡和追问方向。\n" for i, q in enumerate(questions, 1))
        write(f"interview/{slug}.md", f"# {slug.replace('-', ' ').title()} 面试资料\n\n{items}\n")
    write("career/RESUME_GUIDE.md", """# 简历指南\n\n简历应以目标岗位要求为准。每个项目用“问题—行动—技术取舍—可验证结果”表达；不要虚构用户数量、性能指标、线上收入或使用公司数据。将设计背景写成需求澄清、体验评测、跨职能协作和 Human-in-the-loop 设计能力，并用项目证据支撑。\n\n## 项目描述模板\n\n`Built <system> for <user/problem> using <stack>; implemented <safety/evaluation boundary>; demonstrated <verifiable outcome>.`\n""")
    write("career/PORTFOLIO_GUIDE.md", """# 作品集指南\n\n每个项目页面至少包含：问题、目标用户、范围/非目标、架构图、数据与安全边界、关键流程、评测、Demo 脚本、失败案例和下一步。避免仅展示聊天界面截图；面试官需要看见你如何定义和约束系统。\n""")
    write("career/GITHUB_CHECKLIST.md", """# GitHub 检查清单\n\n- [ ] 置顶 3–4 个项目。\n- [ ] 每个仓库有清晰 README、架构、运行与测试命令。\n- [ ] `.env`、令牌、下载的私密文件均未提交。\n- [ ] 提交信息使用英文并能表达变化目的。\n- [ ] Issues/Project 看板可展示任务拆分与复盘（若公开不含敏感信息）。\n""")
    write("career/DEMO_SCRIPT.md", """# Demo 脚本\n\n## 0:00–0:30 问题\n\n说明目标用户、痛点与非目标。\n\n## 0:30–2:00 工作流\n\n展示一个正常请求，指出输入验证、检索/模型建议、工具调用和状态变化。\n\n## 2:00–3:00 安全与人工确认\n\n展示一个需要批准或被拒绝的场景，说明系统为何停止。\n\n## 3:00–4:00 工程证据\n\n展示测试、日志/追踪、引用或评测记录。\n\n## 4:00–5:00 取舍与下一步\n\n说明局限、成本/质量取舍及下一次迭代。\n""")
    write("career/JOB_APPLICATION_CHECKLIST.md", """# 投递检查清单\n\n- [ ] 已阅读岗位描述，标记匹配项目证据。\n- [ ] 简历中的技术与 GitHub/作品集一致。\n- [ ] 已准备 60 秒和 3 分钟项目介绍。\n- [ ] 已记录投递日期、版本、联系人和后续动作。\n- [ ] 不在公开材料中包含雇主或客户敏感信息。\n""")


def generate_report() -> None:
    report = {"generated_at": GENERATED_AT, "root": str(ROOT), "written_count": len(WRITTEN), "skipped_count": len(SKIPPED), "written_files": WRITTEN, "skipped_files": SKIPPED, "status": "complete_structure_generated"}
    path = ROOT / "reports/generation_report.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "reports/GENERATION_REPORT.md").write_text(f"# 文件生成报告\n\n- 生成时间：{GENERATED_AT}\n- 根目录：`{ROOT}`\n- 新建/更新文件数：{len(WRITTEN)}\n- 因保护现有内容而跳过的文件数：{len(SKIPPED)}\n- 默认方案：`plan-c-designer-ai`\n- 当前起点：`weeks/week-01/days/day-01.md`\n\nPDF 请运行 `python scripts/pdf_from_markdown.py --all`；完整性检查请运行 `python scripts/check_files.py`。\n", encoding="utf-8")


def main() -> int:
    global FORCE
    parser = argparse.ArgumentParser(description="Create or refresh the local AI Agent learning system.")
    parser.add_argument("--force", action="store_true", help="Overwrite generated files. Back up progress first.")
    parser.add_argument("--pdfs", action="store_true", help="Generate requested PDFs after Markdown generation.")
    args = parser.parse_args()
    FORCE = args.force
    generate_root_files()
    generate_plans_and_roadmap()
    generate_weeks()
    generate_knowledge()
    generate_projects()
    generate_templates_and_tracking()
    generate_interview_and_career()
    update_manifest()
    generate_report()
    if args.pdfs:
        command = [sys.executable, str(ROOT / "scripts/pdf_from_markdown.py"), "--all"]
        completed = subprocess.run(command, cwd=ROOT, check=False)
        if completed.returncode != 0:
            return completed.returncode
    print(f"Generated or updated {len(WRITTEN)} files; preserved {len(SKIPPED)} existing files.")
    print(f"Start with: {ROOT / 'weeks/week-01/days/day-01.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
