# Agent Starter

面向学习与作品集的 production-minded Agent 工程骨架。它故意保持业务简单，但把工程边界做完整：服务端 Schema 校验、最大步数、重复工具调用保护、模型/工具超时、写工具人工审批 fail-closed、幂等存储、租户上下文、RAG 摄取/检索、日志/Trace、单元测试与离线评测入口。

## 本地运行

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e '.[dev]'
pytest -q
uvicorn app.main:app --reload
```

健康检查：`GET http://127.0.0.1:8000/health`

## Docker

```bash
cp .env.example .env
docker compose up --build
```

## 关键安全原则

- 模型输出永远不是授权结果；工具参数在服务端再次通过 Pydantic 校验。
- `risk="write"` 的工具必须同时满足业务权限和服务端 `ApprovalChecker`，否则 fail closed。
- 写操作带 `idempotency_key`；`IdempotencyStore` 用 `(tenant_id, key)` 防重复。
- 外部模型与工具调用都有 timeout；Agent Loop 有 `max_steps` 和重复调用指纹。
- 测试默认使用 FakeModel，不产生真实模型费用；真实密钥只放 `.env`，绝不提交 Git。
- `RagService` 只是可测试 baseline；生产项目需替换为带 ACL metadata 的 embedding + hybrid + rerank，并在检索前/后双重做 tenant/权限过滤。

## 当前测试

```bash
PYTHONPATH=. pytest -q
# 预期：6 passed
```
