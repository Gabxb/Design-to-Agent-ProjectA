# 设计规范知识库 Agent

让团队以引用可追溯的方式查询设计规范。

## 作品集叙事

本项目面向“设计知识管理”场景，解决的问题是：规范分散且版本不清，设计师和工程师无法快速确认依据。。展示时应说明用户痛点、数据与安全边界、架构选择、失败路径、人工确认点和下一步改进，不应把模型输出包装为完全自动化的正确答案。

## 目录

| 路径 | 用途 |
|---|---|
| `src/` | 教学用应用骨架 |
| `tests/` | 关键路径测试 |
| `docs/` | 运行、决策与 Demo 资料 |
| `data/` | 仅存放脱敏/合成样例 |
| `reference-solution/` | 默认不提供完整答案 |

## 本地运行

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e .[dev]
uvicorn src.main:app --reload
pytest
```

复制 `.env.example` 为 `.env` 后再填写自己的本地变量；绝不提交 `.env`。运行前请核对当前框架和模型 API 的官方文档。

## 当前状态

- [ ] 需求已确认
- [ ] 架构已评审
- [ ] 最小 API 可运行
- [ ] 安全与评测基线已建立
- [ ] Docker 本地启动成功
- [ ] Demo 与作品集叙事已完成


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

