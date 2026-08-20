# P4：供应商风险审查 Agent

## 这个项目训练什么

自动整理供应商资料、检索政策、调用风险工具并生成需人工审批的审查建议。

## 用户和业务流程

1. 创建审查单
2. 解析供应商材料
3. RAG 检索内部政策
4. 调用制裁与财务风险工具
5. 生成风险分级
6. 人工审批
7. 写入审计记录并通知结果

## 核心工程能力

- 业务状态机
- RAG
- Tool Calling
- Agent 工作流
- 人工确认
- 最小权限
- 评测
- 容器化部署

## 必须证明的结果

- 高风险召回率
- 误报率
- 人工处理时长
- 审计记录完整率

## 风险边界

- 外部工具数据过期
- 模型结论被误当最终决定
- 敏感商业资料泄漏

## 实施入口

- [项目 README](../../projects/project-04-capstone/README.md)
- [产品需求](../../projects/project-04-capstone/REQUIREMENTS.md)
- [架构说明](../../projects/project-04-capstone/ARCHITECTURE.md)
- [开发任务](../../projects/project-04-capstone/TASKS.md)
- [验收标准](../../projects/project-04-capstone/ACCEPTANCE_CRITERIA.md)
- [测试计划](../../projects/project-04-capstone/TEST_PLAN.md)
- [安全说明](../../projects/project-04-capstone/SECURITY.md)
- [评测方案](../../projects/project-04-capstone/EVALUATION.md)
- [部署说明](../../projects/project-04-capstone/DEPLOYMENT.md)

## 项目完成标准

不要只展示正常路径。至少演示一个输入错误、一个外部依赖失败、一个权限或安全边界，以及一个人工确认或明确的无答案结果。
