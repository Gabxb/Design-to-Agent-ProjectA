# 24 周 AI Agent 开发路线图

本路线图以**方案 C：设计师优势版**为默认执行方案。其 20 周核心能力训练之后，安排 4 周求职冲刺扩展，使你能够把工程产出组织为可面试、可演示、可复盘的作品集。学习计划强调项目驱动，但每周必须有工程验收与复盘，避免停留在界面原型或聊天演示。

## 阶段总览

| 阶段 | 周次 | 核心目标 | 阶段成果 |
|---|---|---|---|
| 编程与本地开发基础 | 1–4 | 能独立创建、测试和运行后端服务 | 设计需求结构化助手 API |
| LLM 应用开发 | 5–8 | 能可靠调用模型、校验输出并安全执行工具 | UX Research Copilot |
| RAG 知识库 | 9–12 | 能构建带引用、可评测、可隔离的知识服务 | 设计规范知识库 Agent |
| Agent 工作流 | 13–16 | 能实现状态、分支、终止与人工确认 | 智能设计评审 Agent |
| 生产化 | 17–20 | 能评测、观测、保护并部署产品 | 可部署 Agent Web 产品 |
| 求职冲刺扩展 | 21–24 | 能呈现作品集并处理真实工程表达 | 简历、Demo、面试库、模拟任务 |

## 每周地图

| 周 | 阶段 | 主题 | 可展示产出 | 主项目 |
|---|---|---|---|---|
| 01 | 编程与本地开发基础 | Python 环境、命令行与可维护脚本 | 可重复运行的 Python 命令行小工具 | 设计需求结构化助手 API |
| 02 | 编程与本地开发基础 | Python 数据建模、异常与测试 | 含单元测试的数据转换模块 | 设计需求结构化助手 API |
| 03 | 编程与本地开发基础 | Git、HTTP、JSON 与 FastAPI | 带输入验证的 REST API | 设计需求结构化助手 API |
| 04 | 编程与本地开发基础 | SQL、PostgreSQL、日志与集成 | 设计需求结构化助手 API 阶段版 | 设计需求结构化助手 API |
| 05 | LLM 应用开发 | LLM、Token 与提示词结构 | 可版本化的提示词实验记录 | UX Research Copilot |
| 06 | LLM 应用开发 | 结构化输出与 JSON Schema | 研究访谈洞察结构化 API | UX Research Copilot |
| 07 | LLM 应用开发 | Tool Calling、重试与安全边界 | 受控工具调用循环 | UX Research Copilot |
| 08 | LLM 应用开发 | UX Research Copilot 集成冲刺 | 可演示的研究资料整理助手 | UX Research Copilot |
| 09 | RAG 知识库 | 文档解析、Chunking 与 Metadata | 可追溯的文档切分流水线 | 设计规范知识库 Agent |
| 10 | RAG 知识库 | Embedding 与向量检索 | 带过滤条件的基础检索服务 | 设计规范知识库 Agent |
| 11 | RAG 知识库 | Hybrid Search、Reranking 与引用 | 带引文的高质量问答链路 | 设计规范知识库 Agent |
| 12 | RAG 知识库 | RAG 评测与数据隔离 | 设计规范知识库 Agent 阶段版 | 设计规范知识库 Agent |
| 13 | Agent 工作流 | Workflow 与 Agent 的边界 | 可审计的任务分解工作流 | 智能设计评审 Agent |
| 14 | Agent 工作流 | LangGraph 状态图与持久化 | 可恢复的状态化工作流原型 | 智能设计评审 Agent |
| 15 | Agent 工作流 | 记忆、Human-in-the-loop 与 MCP | 带人工确认的工具工作流 | 智能设计评审 Agent |
| 16 | Agent 工作流 | 智能设计评审 Agent 集成冲刺 | 可演示的设计评审工作流 | 智能设计评审 Agent |
| 17 | 生产化 | 测试策略与 Agent Evaluation | 可重复运行的评测基线 | 案例分流与合规助手 |
| 18 | 生产化 | Tracing、成本、缓存与安全 | 具备可观测性与风险控制的服务 | 案例分流与合规助手 |
| 19 | 生产化 | Docker、CI/CD 与部署 | 容器化、可部署的 Agent Web 产品 | 案例分流与合规助手 |
| 20 | 生产化 | 产品打磨与上线演练 | 可部署产品的发布候选版 | 案例分流与合规助手 |
| 21 | 求职冲刺扩展 | 作品集重构与架构表达 | 四个项目的展示版 README 和架构图 | 全作品集 |
| 22 | 求职冲刺扩展 | 简历、GitHub 与 Demo | 简历素材、主页和 Demo 脚本 | 全作品集 |
| 23 | 求职冲刺扩展 | 面试与系统设计 | 技术问答库与系统设计白板稿 | 全作品集 |
| 24 | 求职冲刺扩展 | 模拟工作任务与投递复盘 | 端到端模拟任务和求职跟踪系统 | 全作品集 |

## 使用规则

先阅读 `START_HERE.md`，然后打开当前周的 `WEEK_PLAN.md`。每日完成后，把结果、耗时和问题写入 `progress/DAILY_LOG.md` 与 `progress/progress.json`。当工作或生活导致中断时，使用 `update_plan.py pause`；恢复时使用 `update_plan.py resume` 生成恢复清单。


## 参考资源索引

[1]: https://docs.python.org/3/ "Python 3 Documentation"
[2]: https://fastapi.tiangolo.com/ "FastAPI Documentation"
[3]: https://www.postgresql.org/docs/ "PostgreSQL Documentation"
[4]: https://docs.docker.com/ "Docker Documentation"
[5]: https://git-scm.com/doc "Git Documentation"
[6]: https://developers.openai.com/api/docs/guides/function-calling "OpenAI Function Calling Guide"
[7]: https://developers.openai.com/api/docs/guides/structured-outputs "OpenAI Structured Outputs Guide"
[8]: https://docs.langchain.com/oss/python/langgraph/overview "LangGraph Overview"
[9]: https://modelcontextprotocol.io/ "Model Context Protocol Specification"
[10]: https://owasp.org/www-project-top-10-for-large-language-model-applications/ "OWASP Top 10 for LLM Applications"

