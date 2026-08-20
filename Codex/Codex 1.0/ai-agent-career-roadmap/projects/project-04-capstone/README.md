# 供应商风险审查 Agent

领域：采购与合规

## 项目目标

自动整理供应商资料、检索政策、调用风险工具并生成需人工审批的审查建议。

## 目标用户

- 采购专员
- 合规人员
- 业务负责人

## 核心能力

- 业务状态机
- RAG
- Tool Calling
- Agent 工作流
- 人工确认
- 最小权限
- 评测
- 容器化部署

## 开发方式

本目录当前提供完整需求、架构、任务、测试、安全、评测和部署定义，不提供完整参考实现。按照 `TASKS.md` 逐步在 `src/` 和 `tests/` 中实现。

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
pytest
```

具体框架版本和模型 API 可能变化，实施时核对最新官方文档。
