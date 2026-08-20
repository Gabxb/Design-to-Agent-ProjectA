# 方案 B：求职冲刺版

- **适合人群：** 能高强度学习、希望尽快形成作品集的人
- **学习周期：** 16 周
- **每周投入：** 20-25 小时
- **学习节奏：** 压缩基础，每 4 周交付一个可展示成果
- **技术深度：** 项目所需知识优先，快速进入 LLM、RAG 与 Agent
- **项目数量：** 4 个可展示成果
- **就业方向：** AI 应用工程师、RAG 工程师、Agent 工程师
- **优势：** 作品和面试材料形成快
- **风险：** 基础缺口容易在调试和系统设计阶段暴露
- **选择建议：** 只有能稳定投入 20 小时以上并接受补课时选择 B。

## 执行原则

- 根目录 `weeks/` 始终保留完整 24 周能力课程。
- 本方案通过下表把完整课程映射到 16 个执行周。
- 已完成任务使用稳定任务 ID 保存；切换方案时不会删除完成记录。
- 每个方案周开始前，根据映射打开对应源课程周，合并安排到自己的日历。

## 周映射

| 方案周 | 源课程周 | 主题 |
|---:|---|---|
| 01 | W01, W02 | Python 与本地开发环境；Git、HTTP 与 FastAPI |
| 02 | W03, W04 | SQL 与 PostgreSQL；工程化 API 阶段项目 |
| 03 | W05 | LLM 基础与 Prompt 结构 |
| 04 | W06, W07 | Structured Output 与 Tool Calling；UX Research Copilot |
| 05 | W08 | 可靠性、安全与阶段交付 |
| 06 | W09 | 文档解析与 Chunking |
| 07 | W10, W11 | Embedding 与向量检索；Hybrid Search、Reranking 与引用 |
| 08 | W12 | RAG 评测与数据隔离 |
| 09 | W13 | Agent、Workflow 与 ReAct |
| 10 | W14 | LangGraph 状态工作流 |
| 11 | W15, W16 | 记忆、Human-in-the-loop 与 MCP；智能设计评审 Agent 交付 |
| 12 | W17 | 测试与 Agent Evaluation |
| 13 | W18, W19 | 可观测性、成本与性能；权限、安全与数据治理 |
| 14 | W20 | Docker、CI/CD 与部署 |
| 15 | W21, W22 | 作品集工程化整理；Python、API 与数据库面试 |
| 16 | W23, W24 | RAG、Agent 与系统设计面试；简历、Demo 与投递 |

## 使用方法

在 `progress/progress.json` 中记录当前方案周和源课程周；使用 `python update_plan.py switch-plan plan-b-job-ready` 切换。切换时会生成迁移说明并备份原进度。
