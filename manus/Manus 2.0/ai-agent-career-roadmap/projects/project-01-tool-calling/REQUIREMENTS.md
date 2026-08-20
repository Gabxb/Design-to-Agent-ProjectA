# 设计需求分析助手：产品需求

## 1. 问题与目标

**问题：**需求语言含混、验收标准缺失，导致设计与研发反复对齐。

**目标：**把模糊设计需求转为可验证、可执行的工程任务。 本项目是作品集工程模板，不使用真实客户、员工或敏感案例数据。

## 2. 目标用户与用户故事

| 用户 | 用户故事 | 成功标准 |
|---|---|---|
| 一线使用者 | 当我提交一个结构化任务时，我希望得到有依据、可编辑的建议，以便更快完成下一步。 | 输入被验证，结果包含状态和依据。 |
| 审核者 | 当系统准备执行高影响操作时，我希望先查看证据并批准或拒绝。 | 未批准时绝不执行副作用操作。 |
| 维护者 | 当结果异常时，我希望能定位请求、工具调用和错误。 | 日志可关联、密钥不泄露。 |

## 3. 范围与非目标

本项目实现：需求字段校验、优先级建议、验收标准生成。本项目不承诺自主执行不可逆操作、不代替专业判断、不使用未授权数据。

## 4. 功能需求

- 输入验证：拒绝空值、超长值和不符合 Schema 的数据。
- 业务编排：将确定性规则与模型建议分开，记录每一步状态。
- 人工确认：对创建工单、导出或高风险结论设置批准节点。
- 审计与可观测性：记录请求标识、耗时、错误类别和成本估算，不记录密钥。

## 5. API 设计

| 方法 | 路径 | 说明 | 成功响应 |
|---|---|---|---|
| `GET` | `/health` | 健康检查 | `200` 状态对象 |
| `POST` | `/tasks` | 创建待处理任务 | `201` 任务与状态 |
| `GET` | `/tasks/{task_id}` | 查询任务与审计摘要 | `200` 状态对象 |
| `POST` | `/tasks/{task_id}/approve` | 人工确认下一步 | `200` 已批准状态 |

## 6. JSON Schema（示意）

```json
{
  "type": "object",
  "required": ["title", "content"],
  "properties": {
    "title": {"type": "string", "minLength": 1, "maxLength": 120},
    "content": {"type": "string", "minLength": 1, "maxLength": 5000},
    "requires_approval": {"type": "boolean", "default": true}
  },
  "additionalProperties": false
}
```

## 7. 非功能要求

使用环境变量读取配置；关键函数提供类型提示；对外部调用设置超时和有限重试；关键路径具备测试；Docker Compose 能在本地启动依赖；README 中包含准确命令。

## 8. 验收

详见 `ACCEPTANCE_CRITERIA.md`、`TEST_PLAN.md`、`SECURITY.md` 和 `EVALUATION.md`。


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

