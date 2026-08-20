# 设计需求分析助手：用户流程

```text
提交任务 → 输入验证 → 规则/检索 → 模型建议 → 工具参数验证
  → 是否需要人工确认？ → 批准/拒绝/修改 → 记录审计 → 返回结果
```

流程场景：设计协作。核心重点：需求结构化、FastAPI、PostgreSQL、Structured Output、Tool Calling、日志、测试、Docker。
