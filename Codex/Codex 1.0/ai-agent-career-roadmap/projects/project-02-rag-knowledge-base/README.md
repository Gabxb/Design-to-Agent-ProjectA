# 设计规范知识库 Agent

领域：企业设计规范检索

## 项目目标

让团队从多版本规范中获得带引用、可核查且受权限约束的答案。

## 目标用户

- 设计师
- 前端工程师
- 设计系统维护者

## 核心能力

- 文档上传
- Chunking
- Embedding
- Metadata
- Hybrid Search
- Reranking
- 引用
- 评测与权限隔离

## 开发方式

本目录当前提供完整需求、架构、任务、测试、安全、评测和部署定义，不提供完整参考实现。按照 `TASKS.md` 逐步在 `src/` 和 `tests/` 中实现。

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
pytest
```

具体框架版本和模型 API 可能变化，实施时核对最新官方文档。
