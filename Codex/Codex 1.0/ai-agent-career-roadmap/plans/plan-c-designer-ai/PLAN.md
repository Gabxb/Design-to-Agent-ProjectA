# 方案 C：设计师优势版

- **适合人群：** 希望把设计、研究和产品能力转化为差异化优势的人
- **学习周期：** 20 周
- **每周投入：** 15-20 小时
- **学习节奏：** 保留工程主线，同时强化研究、体验与 Human-in-the-loop
- **技术深度：** Agent 产品体验与工程实现并重
- **项目数量：** 3 个设计优势项目 + 1 个非设计项目
- **就业方向：** AI Agent 工程师、AI 产品工程师、Design Engineer、AI 原型工程师
- **优势：** 能形成清晰个人定位和差异化作品集
- **风险：** 容易偏重体验表达而忽略测试、数据库和部署
- **选择建议：** 与你的背景最匹配，默认从 C 开始；每周保留工程验收时间。

## 执行原则

- 根目录 `weeks/` 始终保留完整 24 周能力课程。
- 本方案通过下表把完整课程映射到 20 个执行周。
- 已完成任务使用稳定任务 ID 保存；切换方案时不会删除完成记录。
- 每个方案周开始前，根据映射打开对应源课程周，合并安排到自己的日历。

## 周映射

| 方案周 | 源课程周 | 主题 |
|---:|---|---|
| 01 | W01 | Python 与本地开发环境 |
| 02 | W02 | Git、HTTP 与 FastAPI |
| 03 | W03, W04 | SQL 与 PostgreSQL；工程化 API 阶段项目 |
| 04 | W05 | LLM 基础与 Prompt 结构 |
| 05 | W06 | Structured Output 与 Tool Calling |
| 06 | W07, W08 | UX Research Copilot；可靠性、安全与阶段交付 |
| 07 | W09 | 文档解析与 Chunking |
| 08 | W10 | Embedding 与向量检索 |
| 09 | W11 | Hybrid Search、Reranking 与引用 |
| 10 | W12 | RAG 评测与数据隔离 |
| 11 | W13 | Agent、Workflow 与 ReAct |
| 12 | W14 | LangGraph 状态工作流 |
| 13 | W15 | 记忆、Human-in-the-loop 与 MCP |
| 14 | W16 | 智能设计评审 Agent 交付 |
| 15 | W17 | 测试与 Agent Evaluation |
| 16 | W18 | 可观测性、成本与性能 |
| 17 | W19 | 权限、安全与数据治理 |
| 18 | W20 | Docker、CI/CD 与部署 |
| 19 | W21, W22 | 作品集工程化整理；Python、API 与数据库面试 |
| 20 | W23, W24 | RAG、Agent 与系统设计面试；简历、Demo 与投递 |

## 使用方法

在 `progress/progress.json` 中记录当前方案周和源课程周；使用 `python update_plan.py switch-plan plan-c-designer-ai` 切换。切换时会生成迁移说明并备份原进度。
