# AI Agent Career Roadmap

这是一个可脱离聊天记录独立使用的本地 AI Agent 开发学习系统。默认路线为 **方案 C：设计师优势版**，以 20 周核心能力训练加 4 周求职冲刺扩展，形成 24 周完整闭环。所有学习内容、进度、项目定义、模板与脚本都保存在本目录。

## 从哪里开始

1. 阅读 [`START_HERE.md`](START_HERE.md)。
2. 先查看系统总目录：[`INDEX.md`](INDEX.md)。
3. 使用 [`roadmap/LEARNING_OUTLINE.md`](roadmap/LEARNING_OUTLINE.md) 阅读能力主线，使用 [`roadmap/LEARNING_MINDMAP.md`](roadmap/LEARNING_MINDMAP.md) 一眼把握整体方向。
4. 查看三套方案对比：[`plans/PLAN_COMPARISON.md`](plans/PLAN_COMPARISON.md)。
5. 默认从 [`weeks/week-01/days/day-01.md`](weeks/week-01/days/day-01.md) 开始。
6. 每日结束后更新 `progress/`；使用 `python update_plan.py --help` 查看操作。

## 常用命令

```bash
python generate_files.py
python update_plan.py status
python update_plan.py complete --task week-01-day-01
python scripts/check_files.py
python scripts/pdf_from_markdown.py --all
```

Windows PowerShell 用户可使用 `scripts/setup.ps1` 和 `scripts/generate_pdfs.ps1`；macOS/Linux 用户使用对应 `.sh` 脚本。详见 `START_HERE.md`。

## 工程原则

学习项目使用 Python 3.12、FastAPI、PostgreSQL、React/Next.js（在产品阶段）、Git 和 Docker。所有代码、变量名、文件名和 Git commit 使用英文；正文使用中文。真实 API Key 只能在本地 `.env` 或部署平台秘密管理系统中保存，绝不提交。


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

