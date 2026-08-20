# P1：设计需求分析助手

## 这个项目训练什么

把自然语言设计需求转换为可追踪的目标、约束、风险和待确认问题。

## 用户和业务流程

1. 提交原始需求
2. 校验并保存需求
3. 模型生成结构化分析
4. 调用项目规则工具
5. 用户确认或修订
6. 导出需求摘要

## 核心工程能力

- FastAPI 接口
- PostgreSQL 持久化
- JSON Schema
- Tool Calling
- 日志和统一异常
- 测试与 Docker

## 必须证明的结果

- 结构化字段有效率
- 人工修订率
- P95 API 延迟
- 失败请求率

## 风险边界

- 模型遗漏硬约束
- 敏感项目资料进入日志
- 重复提交产生重复记录

## 实施入口

- [项目 README](../../projects/project-01-tool-calling/README.md)
- [产品需求](../../projects/project-01-tool-calling/REQUIREMENTS.md)
- [架构说明](../../projects/project-01-tool-calling/ARCHITECTURE.md)
- [开发任务](../../projects/project-01-tool-calling/TASKS.md)
- [验收标准](../../projects/project-01-tool-calling/ACCEPTANCE_CRITERIA.md)
- [测试计划](../../projects/project-01-tool-calling/TEST_PLAN.md)
- [安全说明](../../projects/project-01-tool-calling/SECURITY.md)
- [评测方案](../../projects/project-01-tool-calling/EVALUATION.md)
- [部署说明](../../projects/project-01-tool-calling/DEPLOYMENT.md)

## 项目完成标准

不要只展示正常路径。至少演示一个输入错误、一个外部依赖失败、一个权限或安全边界，以及一个人工确认或明确的无答案结果。
