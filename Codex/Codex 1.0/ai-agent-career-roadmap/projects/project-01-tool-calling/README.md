# 设计需求分析助手

领域：设计需求澄清

## 项目目标

把自然语言设计需求转换为可追踪的目标、约束、风险和待确认问题。

## 目标用户

- 产品设计师
- 产品经理
- 设计负责人

## 核心能力

- FastAPI 接口
- PostgreSQL 持久化
- JSON Schema
- Tool Calling
- 日志和统一异常
- 测试与 Docker

## 开发方式

本目录当前提供完整需求、架构、任务、测试、安全、评测和部署定义，不提供完整参考实现。按照 `TASKS.md` 逐步在 `src/` 和 `tests/` 中实现。

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
pytest
```

具体框架版本和模型 API 可能变化，实施时核对最新官方文档。
