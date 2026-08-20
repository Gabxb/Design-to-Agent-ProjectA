# 智能设计评审 Agent

领域：结构化设计评审

## 项目目标

依据目标、规范和证据完成多步骤评审，并在高风险结论前请求人工确认。

## 目标用户

- 设计师
- 设计负责人
- 产品团队

## 核心能力

- 状态管理
- 条件分支
- 循环与终止
- 工具调用
- Human-in-the-loop
- 重试
- Tracing
- 成本统计

## 开发方式

本目录当前提供完整需求、架构、任务、测试、安全、评测和部署定义，不提供完整参考实现。按照 `TASKS.md` 逐步在 `src/` 和 `tests/` 中实现。

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
pytest
```

具体框架版本和模型 API 可能变化，实施时核对最新官方文档。
