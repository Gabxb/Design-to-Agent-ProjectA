# Secure Agent Starter

這是一個面向教學的 **FastAPI + Pydantic + 受控 Agent Loop** 範例。它不是可直接用於生產的完整工單系統；其目的在於把模型決策、服務端授權、工具驗證、人工確認、可觀測性與評測，拆成可檢查的工程邊界。

## 核心安全邊界

模型只能提出受 JSON Schema 約束的工具呼叫。使用者、租戶、角色、資源所有權與寫入權限由已驗證的 `Principal` 和服務端政策決定，不能由模型輸出或工具參數提供。`draft_ticket` 是高風險寫工具，預設停用，且即使開啟也必須先產生待確認操作。每輪 Agent 有最大步數，工具執行有逾時，重複的相同工具呼叫會拒絕。

## 本機啟動

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn agent_app.main:app --reload
```

以下請求中的 headers 僅供本機教學。真正的服務必須使用驗簽 JWT、OIDC session 或企業身分提供者的 middleware 來建立主體。

```bash
curl -X POST http://127.0.0.1:8000/v1/chat \
  -H 'content-type: application/json' \
  -H 'x-user-id: user-001' \
  -H 'x-tenant-id: tenant-a' \
  -H 'x-role: support_agent' \
  -d '{"message":"查询工单创建规范","conversation_id":"demo-001"}'
```

## 測試與評測

```bash
pytest -q
mypy src
python eval/run_eval.py --input eval/cases.jsonl --output eval/report.json
```

`eval/cases.jsonl` 包含任務、權限、人工確認與提示注入樣本。報告會輸出可重現的任務成功率、平均延遲與 P95 延遲；Token 與成本必須從實際模型供應商回傳的 usage 資料計算，不可捏造。

## 部署與風險提醒

```bash
cp .env.example .env
# 在 .env 填入真正的模型配置；不要提交 .env
docker compose up --build
```

部署前應新增：身分驗證與角色／租戶政策、PostgreSQL 與 migration、機密管理、速率限制、審計留存策略、監控與告警、回滾方案、資料保留與刪除流程。將任意外部文件、RAG 片段、MCP 描述或工具輸出視為不可信資料；它們不能覆寫系統策略，也不能直接驅動有副作用操作。
