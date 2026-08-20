# 智能设计评审 Agent：安全说明

## 威胁与控制

| 风险 | 控制措施 | 验证方式 |
|---|---|---|
| 密钥泄露 | 环境变量、`.gitignore`、日志脱敏 | 扫描仓库和日志样例 |
| 提示词注入 | 不信任外部内容、明确工具白名单、隔离指令 | 恶意文档测试集 |
| 越权工具调用 | 应用侧授权、Schema 校验、人工确认 | 未授权请求测试 |
| 跨用户数据泄露 | 租户/用户过滤、最小权限 | 隔离测试 |
| 不可追溯决策 | 请求标识、审计摘要、引用来源 | 追踪演练 |

## 不可违反的规则

不得把真实 API Key、访问令牌、真实个人数据或内部 URL 写入提交、截图、提示词样例或错误日志。外部文档和工具输出都应视为不可信数据，而非系统指令。

参考：OWASP LLM 应用安全指南 [10]。


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

