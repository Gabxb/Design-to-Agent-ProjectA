# 方案 A：稳健基础版：课程结构

该课程不将设计背景视为需要绕开的短板，而是将其转化为需求澄清、信息架构、质量评测和人机协同设计能力。每个阶段都要求提交代码、文档、验收记录和复盘。

| 周次 | 阶段 | 关键能力 |
|---|---|---|
| 1–4 | 工程底座 | Python、Git、API、SQL、测试 |
| 5–8 | LLM 应用 | 提示词、结构化输出、工具调用 |
| 9–12 | RAG | 解析、检索、引用、评测 |
| 13–16 | Agent | 工作流、状态、人工确认、MCP |
| 17–20 | 生产化 | 评测、观测、安全、Docker、部署 |
| 21–24 | 求职 | 作品集、简历、面试、模拟任务 |

## 统一工程质量线

所有阶段遵守：Python 类型提示；环境变量保存密钥；输入验证；结构化日志；关键功能测试；README 可复现；Docker 化；不使用虚构真实用户数据。框架或模型 API 可能变化，实施前必须核对官方文档。


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

