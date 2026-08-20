# P2：设计规范知识库 Agent

## 这个项目训练什么

让团队从多版本规范中获得带引用、可核查且受权限约束的答案。

## 用户和业务流程

1. 上传文档
2. 解析清洗与切块
3. 生成 Embedding 和索引
4. 查询改写与混合检索
5. Reranking
6. 生成带引用答案
7. 记录反馈与评测

## 核心工程能力

- 文档上传
- Chunking
- Embedding
- Metadata
- Hybrid Search
- Reranking
- 引用
- 评测与权限隔离

## 必须证明的结果

- Recall@5
- 引用正确率
- 无答案识别率
- 权限违规数

## 风险边界

- 过期规范被优先召回
- 跨团队数据泄漏
- 引用与答案不一致

## 实施入口

- [项目 README](../../projects/project-02-rag-knowledge-base/README.md)
- [产品需求](../../projects/project-02-rag-knowledge-base/REQUIREMENTS.md)
- [架构说明](../../projects/project-02-rag-knowledge-base/ARCHITECTURE.md)
- [开发任务](../../projects/project-02-rag-knowledge-base/TASKS.md)
- [验收标准](../../projects/project-02-rag-knowledge-base/ACCEPTANCE_CRITERIA.md)
- [测试计划](../../projects/project-02-rag-knowledge-base/TEST_PLAN.md)
- [安全说明](../../projects/project-02-rag-knowledge-base/SECURITY.md)
- [评测方案](../../projects/project-02-rag-knowledge-base/EVALUATION.md)
- [部署说明](../../projects/project-02-rag-knowledge-base/DEPLOYMENT.md)

## 项目完成标准

不要只展示正常路径。至少演示一个输入错误、一个外部依赖失败、一个权限或安全边界，以及一个人工确认或明确的无答案结果。
