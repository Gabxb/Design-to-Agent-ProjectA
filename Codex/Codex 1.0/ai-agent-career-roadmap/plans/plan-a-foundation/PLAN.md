# 方案 A：稳健基础版

- **适合人群：** 软件工程基础较弱、需要在职稳定推进的学习者
- **学习周期：** 24 周
- **每周投入：** 10-15 小时
- **学习节奏：** 每周一个主题，固定复习和补做缓冲
- **技术深度：** 工程基础最完整，LLM 与 Agent 逐步加深
- **项目数量：** 4 个阶段项目
- **就业方向：** 初级 AI 应用工程师、Python 后端工程师、Agent 开发助理
- **优势：** 基础扎实、返工风险低
- **风险：** 作品集形成较慢，需坚持较长周期
- **选择建议：** 如果每周可投入时间不稳定，优先选择 A。

## 执行原则

- 根目录 `weeks/` 始终保留完整 24 周能力课程。
- 本方案通过下表把完整课程映射到 24 个执行周。
- 已完成任务使用稳定任务 ID 保存；切换方案时不会删除完成记录。
- 每个方案周开始前，根据映射打开对应源课程周，合并安排到自己的日历。

## 周映射

| 方案周 | 源课程周 | 主题 |
|---:|---|---|
| 01 | W01 | Python 与本地开发环境 |
| 02 | W02 | Git、HTTP 与 FastAPI |
| 03 | W03 | SQL 与 PostgreSQL |
| 04 | W04 | 工程化 API 阶段项目 |
| 05 | W05 | LLM 基础与 Prompt 结构 |
| 06 | W06 | Structured Output 与 Tool Calling |
| 07 | W07 | UX Research Copilot |
| 08 | W08 | 可靠性、安全与阶段交付 |
| 09 | W09 | 文档解析与 Chunking |
| 10 | W10 | Embedding 与向量检索 |
| 11 | W11 | Hybrid Search、Reranking 与引用 |
| 12 | W12 | RAG 评测与数据隔离 |
| 13 | W13 | Agent、Workflow 与 ReAct |
| 14 | W14 | LangGraph 状态工作流 |
| 15 | W15 | 记忆、Human-in-the-loop 与 MCP |
| 16 | W16 | 智能设计评审 Agent 交付 |
| 17 | W17 | 测试与 Agent Evaluation |
| 18 | W18 | 可观测性、成本与性能 |
| 19 | W19 | 权限、安全与数据治理 |
| 20 | W20 | Docker、CI/CD 与部署 |
| 21 | W21 | 作品集工程化整理 |
| 22 | W22 | Python、API 与数据库面试 |
| 23 | W23 | RAG、Agent 与系统设计面试 |
| 24 | W24 | 简历、Demo 与投递 |

## 使用方法

在 `progress/progress.json` 中记录当前方案周和源课程周；使用 `python update_plan.py switch-plan plan-a-foundation` 切换。切换时会生成迁移说明并备份原进度。
