# AI Agent 学习方案对比

本地学习系统同时维护三套路线。它们共享工程质量标准和作品集目标，但用不同的时间预算与风险偏好安排课程。**当前默认执行方案为方案 C。**

| 方案 | 周期 | 每周投入 | 项目数量 | 就业方向 |
|---|---|---|---|---|
| 方案 A：稳健基础版 | 24 周 | 每周 10–15 小时 | 4 个阶段/作品集项目 | 初级后端、AI 应用开发、Agent 工程助理 |
| 方案 B：求职冲刺版 | 16 周 | 每周 20–25 小时 | 4 个展示项目 | AI 应用/Agent 开发岗位、快速原型岗位 |
| 方案 C：设计师优势版 | 20 周核心 + 4 周求职冲刺扩展 | 每周 15–20 小时 | 3 个设计场景项目 + 1 个非设计综合项目 | AI Agent 开发、AI 产品工程、设计技术/智能体验岗位 |

## 选择原则

若你的可投入时间不稳定，选择方案 A；若需要在四个月内高强度形成作品集，选择方案 B；若你希望将设计、用户研究和交互优势转化为 Agent 产品工程能力，选择方案 C。方案 C 的 20 周核心课程后附加 4 周求职冲刺扩展，因此仍可在 24 周总路线图中完成完整的求职闭环。

## 方案 A：稳健基础版

软件工程基础较弱、需要稳定推进的在职学习者。学习节奏为：每周 5 天主任务、1 天补做、1 天复盘；每四周一个阶段产出。。技术深度为：基础工程能力优先，LLM 与 Agent 随基础逐层增加。。

| 维度 | 说明 |
|---|---|
| 就业方向 | 初级后端、AI 应用开发、Agent 工程助理 |
| 优势 | 学习风险较低、知识缺口可持续补齐。 |
| 风险 | 作品集成型较慢，需要坚持完整周期。 |
| 选择建议 | 若每周无法稳定投入 15 小时或 Python 不熟，请优先选择。 |
## 方案 B：求职冲刺版

可集中投入并希望快速获得可展示项目的学习者。学习节奏为：每 4 周交付一个 Demo；工程基础按项目需求即时补齐。。技术深度为：项目深度与展示优先，覆盖关键工程底座。。

| 维度 | 说明 |
|---|---|
| 就业方向 | AI 应用/Agent 开发岗位、快速原型岗位 |
| 优势 | 作品集、部署、README 和面试叙事形成快。 |
| 风险 | 高强度，基础薄弱时容易形成理解债务。 |
| 选择建议 | 只有在每周可投入 20 小时以上且能规律复盘时选择。 |
## 方案 C：设计师优势版

具有设计、产品、用户研究或服务设计背景的转型者。学习节奏为：每周以用户问题、交互流程和工程实现三条线并进；每四周完成可讲述成果。。技术深度为：Agent 工程主线与 AI 产品体验、人机协同、安全评测并重。。

| 维度 | 说明 |
|---|---|
| 就业方向 | AI Agent 开发、AI 产品工程、设计技术/智能体验岗位 |
| 优势 | 把已有设计优势转化为需求定义、评测、人机协同与产品叙事优势。 |
| 风险 | 容易偏重体验而忽略测试、数据库、部署等工程细节。 |
| 选择建议 | 默认方案。每周严格保留工程验收日，避免只做原型。 |

## 切换方案

使用 `python update_plan.py switch-plan plan-a-foundation`（或 B/C）切换。脚本会先备份进度、保留个人笔记，并写入迁移记录；已完成任务不会被删除。


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

