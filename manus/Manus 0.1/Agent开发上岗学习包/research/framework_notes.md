# 官方框架研究筆記

資料核對日期：2026-08-12（GMT+8）。本筆記僅記錄已查核的官方資料；教程將提示讀者在實作前再次確認版本與 API。

| 技術 | 已核對的定位與能力 | 課程採用方式 | 官方來源 |
|---|---|---|---|
| OpenAI Agents SDK | Python SDK 的核心原語為 Agent、Agents as tools／Handoffs、Guardrails；文件列出 function tools、MCP、Sessions、Human-in-the-loop 與 Tracing。文件頁面顯示版本 `v0.20.0`。 | 在第 11–12 週作為輕量 SDK 對照案例；示例主線保留手寫 loop 以理解可控性。 | https://openai.github.io/openai-agents-python/ |
| LangGraph | 官方文件區分：工作流具有預定程式路徑；Agent 動態決定程序與工具使用。文件列出 persistence、streaming、interrupt、memory、testing、deployment 與 observability。 | 第 10 週以狀態圖、checkpoint、人工中斷與恢復為主線，適合長流程與顯式控制。 | https://docs.langchain.com/oss/python/langgraph/workflows-agents |
| Microsoft Agent Framework | 支援 Agent、Harness Agent、明確路徑的 functional／graph workflow、模型與工具整合、session、memory/context、middleware、MCP client、telemetry。文件明示 Go 版仍為 public preview，部分功能不可用。 | 第 12 週作為跨供應商與企業特性導讀，標註 API 快速變動與預覽風險；不作為作品集的硬性依賴。 | https://learn.microsoft.com/en-us/agent-framework/overview/ |

## 選型原則（官方文件可支持）

1. 若可用確定性程式函式解決，優先以一般服務或工作流完成，不將 Agent 當成預設解法。
2. 當任務開放、需要模型在受控工具集合中規劃與選擇工具時，才評估 Agent。
3. 長流程、跨步狀態、恢復與人類審批應視為獨立工程需求，而非僅依賴模型提示。
4. 安全、權限、輸入與輸出驗證、追蹤、評測與成本界線應由應用服務端掌控。

## 已知變動風險

Agent SDK、圖編排框架與雲端 Agent Framework 均快速演進；教程會鎖定「概念與工程介面」，示例以 2026-08-12 可查核的公開文件為依據。套件安裝前應先查閱 release notes、Python 版本需求及遷移指南。

| Model Context Protocol（MCP） | MCP 是 LLM 應用與外部資料來源、工具連接的開放協定，以 JSON-RPC 2.0 溝通；伺服器可提供 Resources、Prompts、Tools。規範要求使用者明確同意資料存取與工具操作，並將工具視為任意程式碼執行。HTTP 傳輸的授權規範以 OAuth 2.1 為基礎，強調最小權限 scope、受眾驗證與禁止 token passthrough。安全文件討論 confused deputy、SSRF、state-handle hijacking 與本地伺服器妥協。 | 第 13 週會實作最小 MCP server/client，並將顯式同意、scope 最小化、工具 allowlist、伺服端鑑權、state 歸屬驗證、網路 egress 與秘密保護列為驗收條件。 | https://modelcontextprotocol.io/specification/2026-07-28；https://modelcontextprotocol.io/specification/draft/basic/authorization；https://modelcontextprotocol.io/specification/draft/basic/security_best_practices |

## MCP 工程落地準則

- 將 MCP tool description 視為不可信輸入；MCP client 只連接經審核的伺服器，並在執行任何有副作用工具前請求明確人工批准。
- HTTP MCP 應要求 HTTPS、做 OAuth token audience 與 scope 驗證；不得把非本伺服器簽發給自己的 token 直接轉交下游服務。
- 工具 schema 的 `user_id`、`tenant_id`、角色與允許目錄不得由模型決定；必須由已驗證主體及伺服端政策導出或覆寫。
- 存取網路型 MCP 端點時使用 allowlist、重導驗證與 egress policy，降低 SSRF 風險；state handle 必須使用不可預測 ID 並與 authenticated user 綁定。

| Structured Outputs 與 Function Calling | 官方文件區分：Function Calling 用於把模型連到應用程式的工具、資料與動作；`text.format` 的 JSON Schema 則適合約束最終回覆的結構。Structured Outputs 可配合 Pydantic；工具參數以 JSON Schema 表達，並可啟用 strict。 | 作品集所有模型→服務、規劃→執行的跨邊界資料均使用 Pydantic 驗證；模型產生的工具參數仍由服務端再次檢查，不視為已授權。 | https://developers.openai.com/api/docs/guides/structured-outputs；https://developers.openai.com/api/docs/guides/function-calling |
| Retrieval／RAG | 官方 Retrieval API 將 vector store 定義為資料索引，支援 semantic search、metadata attribute filtering、query rewrite、ranker／score threshold 與 hybrid search 權重。 | 作品集一以可替換 RAG 介面實作：先做權限過濾，後做 hybrid retrieval、rerank、帶引用生成與無答案拒答。託管 vector store 僅作為可選方案，主線示例以 SQLite FTS + embedding 介面展示可測試概念。 | https://developers.openai.com/api/docs/guides/retrieval |
| Agent 安全 | 官方安全指南將 prompt injection 與 private data leakage 視為主要風險；建議不把不可信字串放入高權限 developer instructions、使用結構化輸出限制資料流、工具審批、護欄與 trace graders／evals。 | 所有範例具備：可信／不可信資料分離、輸入限制、server-side authorization、讀寫工具分級、寫入工具人工審批、拒絕與審計事件、注入與越權測試集。 | https://developers.openai.com/api/docs/guides/agent-builder-safety |

## 核心實作結論

教程不將模型輸出當成指令、身分或權限事實。模型只能提出受到 schema 約束的意圖；身分、租戶、存取範圍、資源所有權、寫入確認、速率限制、逾時、重試與冪等必須由服務端在執行工具之前判定。對任何外部文件、RAG 片段、工具輸出與 MCP metadata，均以「不可信資料」處理。

RAG 不是把文件丟進向量庫就結束。可展示專案需具備攝取可追溯性、內容／metadata 清洗、切分策略的實驗紀錄、租戶與 ACL filter、hybrid search、重排、citation mapping、無答案行為、以標註集衡量的 retrieval 與 answer 指標，以及失敗分類。資料、模型、embedding 與索引參數一律寫入 run metadata，讓結果可重現。

| Agent 評測與 Trace grading | 官方文件建議在行為仍不穩定時先從 trace 著手；trace 記錄模型、工具、護欄與 handoff。再以可重複資料集與 eval runs 比較版本與找回歸。Trace grading 可給決策、工具選擇與安全遵循加上結構化分數／標籤。 | 教材要求每項失敗寫入分類，包含模型、prompt、檢索、工具、權限、狀態、基礎設施與測試資料；每週建立可重跑 JSONL case。 | https://developers.openai.com/api/docs/guides/agent-evals；https://developers.openai.com/api/docs/guides/trace-grading |
| 可觀測性 | LangSmith 將可觀測性定義為由單次 trace 到生產層效能指標的可見性，支援 trace、dashboard、alert、feedback 與線上評測。OpenTelemetry Python 文件列出 metrics、logs、traces，且 Trace／Metrics 標示為 stable、Logs 為 development。 | 示例預設輸出結構化 JSON logs 與自製 trace ID；列出可選的 OpenTelemetry／LangSmith 匯出介面，不強制外部 SaaS。 | https://docs.langchain.com/langsmith/observability；https://opentelemetry.io/docs/languages/python/ |

## 評測順序

先建立能辨認錯誤來源的最小 trace，再用固定資料集量化成功率與安全行為，最後才在真實流量下觀察延遲、成本、人工接管與回歸。任何指標不應單獨解讀：高任務成功率若伴隨越權工具呼叫或錯誤引用，仍屬不可上線的失敗。線上評測必須經過資料脫敏、取樣、存留時間與權限審核。
