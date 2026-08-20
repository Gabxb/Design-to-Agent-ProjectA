# P3：智能设计评审 Agent

## 这个项目训练什么

依据目标、规范和证据完成多步骤评审，并在高风险结论前请求人工确认。

## 用户和业务流程

1. 接收评审任务
2. 解析目标和设计说明
3. 检索规范
4. 分别检查可用性、一致性和可访问性
5. 合并证据
6. 人工确认高风险项
7. 输出行动清单

## 核心工程能力

- 状态管理
- 条件分支
- 循环与终止
- 工具调用
- Human-in-the-loop
- 重试
- Tracing
- 成本统计

## 必须证明的结果

- 证据覆盖率
- 人工接受率
- 平均工具调用数
- 单次评审成本

## 风险边界

- 把主观偏好当作规则
- 工作流无限循环
- 评审证据不足

## 实施入口

- [项目 README](../../projects/project-03-agent-workflow/README.md)
- [产品需求](../../projects/project-03-agent-workflow/REQUIREMENTS.md)
- [架构说明](../../projects/project-03-agent-workflow/ARCHITECTURE.md)
- [开发任务](../../projects/project-03-agent-workflow/TASKS.md)
- [验收标准](../../projects/project-03-agent-workflow/ACCEPTANCE_CRITERIA.md)
- [测试计划](../../projects/project-03-agent-workflow/TEST_PLAN.md)
- [安全说明](../../projects/project-03-agent-workflow/SECURITY.md)
- [评测方案](../../projects/project-03-agent-workflow/EVALUATION.md)
- [部署说明](../../projects/project-03-agent-workflow/DEPLOYMENT.md)

## 项目完成标准

不要只展示正常路径。至少演示一个输入错误、一个外部依赖失败、一个权限或安全边界，以及一个人工确认或明确的无答案结果。
