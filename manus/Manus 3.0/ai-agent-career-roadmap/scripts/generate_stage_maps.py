#!/usr/bin/env python3
"""Generate independent Mermaid submaps for the six learning stages."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGES = [
    (1, "软件工程基础", "Week 01–04", "Python → Git/HTTP → FastAPI → PostgreSQL → 测试/Docker", "设计需求结构化助手 API"),
    (2, "LLM 应用开发", "Week 05–08", "LLM 基础 → Prompt → Structured Output → Function/Tool Calling → 安全", "UX Research Copilot"),
    (3, "RAG 知识库", "Week 09–12", "解析 → Chunking → Embedding → 检索 → 引用/评测/隔离", "设计规范知识库 Agent"),
    (4, "Agent 工作流", "Week 13–16", "Workflow 边界 → 状态 → 工具 → 分支/终止 → HITL → LangGraph/MCP", "智能设计评审 Agent"),
    (5, "生产化", "Week 17–20", "测试 → Evaluation → Tracing → 安全/权限 → Docker/CI/CD → 部署", "案例分流与合规助手"),
    (6, "求职冲刺", "Week 21–24", "项目整理 → GitHub/README → 简历/Demo → 面试 → 投递/复盘", "全作品集"),
]


def main() -> int:
    overview = ROOT / "overview"
    overview.mkdir(parents=True, exist_ok=True)
    for number, name, weeks, flow, project in STAGES:
        mmd = f"""flowchart LR
  A[{name}\\n{weeks}] --> B[核心技术\\n{flow}]
  B --> C[阶段项目\\n{project}]
  C --> D[验收\\n运行 + 测试 + README + 日志]
  D --> E[下一阶段]
"""
        (overview / f"STAGE_{number:02d}_MAP.mmd").write_text(mmd, encoding="utf-8")
        (overview / f"STAGE_{number:02d}_MAP.md").write_text(
            f"# 阶段 {number}：{name} 学习地图\n\n![阶段 {number} 学习地图](STAGE_{number:02d}_MAP.png)\n\n- 周次：{weeks}\n- 核心技术：{flow}\n- 阶段项目：{project}\n- 验收：可以运行、具备正常与失败验证、README 与学习日志已更新。\n\n可编辑源文件：[STAGE_{number:02d}_MAP.mmd](STAGE_{number:02d}_MAP.mmd)。\n",
            encoding="utf-8",
        )
    print("Six stage maps generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
