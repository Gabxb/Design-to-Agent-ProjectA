"""Offline evaluation runner for the learning starter.

This runner uses scripted expected outcomes, not an LLM-as-judge, so its result is
reproducible. Extend it with labeled retrieval and answer-faithfulness graders later.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import time
from pathlib import Path
from statistics import quantiles
from typing import Any

from agent_app.agent_loop import AgentRunner
from agent_app.config import Settings
from agent_app.model_client import ScriptedModelClient
from agent_app.schemas import EvaluationCase, ModelDecision, ToolCall
from agent_app.tools import ToolRegistry


def load_cases(path: Path) -> list[EvaluationCase]:
    return [EvaluationCase.model_validate_json(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def scripted_decisions(case: EvaluationCase) -> list[ModelDecision]:
    tool = case.expected.get("tool")
    if isinstance(tool, dict):
        return [
            ModelDecision(
                kind="tool_call",
                tool_call=ToolCall(call_id=f"eval-{case.case_id}", name=tool["name"], arguments=tool["arguments"]),
            ),
            ModelDecision(kind="final", answer=case.expected.get("answer", "已处理。")),
        ]
    return [ModelDecision(kind="final", answer=case.expected.get("answer", "已处理。"))]


async def evaluate_case(case: EvaluationCase, settings: Settings) -> dict[str, Any]:
    model = ScriptedModelClient(scripted_decisions(case))
    runner = AgentRunner(settings, model, ToolRegistry(settings))
    started = time.perf_counter()
    reply = await runner.run(case.user_message, f"eval-{case.case_id}", case.principal, f"trace-{case.case_id}")
    elapsed_ms = (time.perf_counter() - started) * 1000

    expected = case.expected
    passed = True
    failure_type: str | None = None
    if "contains" in expected and expected["contains"] not in reply.answer:
        passed, failure_type = False, "model_or_prompt"
    if expected.get("requires_approval") and reply.pending_approval is None:
        passed, failure_type = False, "tool_or_permission"
    if expected.get("forbidden") and "无权" not in reply.answer:
        passed, failure_type = False, "permission"
    if expected.get("citations_min", 0) > len(reply.citations):
        passed, failure_type = False, "retrieval_or_citation"

    return {
        "case_id": case.case_id,
        "category": case.category,
        "passed": passed,
        "failure_type": failure_type,
        "latency_ms": round(elapsed_ms, 2),
        "steps": reply.steps,
        "trace_id": reply.trace_id,
    }


async def main(input_path: Path, output_path: Path) -> None:
    settings = Settings(model_api_key="eval-key", enable_write_tools=True)
    rows = [await evaluate_case(case, settings) for case in load_cases(input_path)]
    passed = sum(1 for row in rows if row["passed"])
    latencies = [row["latency_ms"] for row in rows]
    p95 = quantiles(latencies, n=20)[18] if len(latencies) >= 20 else max(latencies, default=0)
    report = {
        "summary": {
            "total": len(rows),
            "passed": passed,
            "task_success_rate": round(passed / len(rows), 4) if rows else 0,
            "average_latency_ms": round(sum(latencies) / len(latencies), 2) if latencies else 0,
            "p95_latency_ms": round(p95, 2),
            "note": "Token usage and cost require provider usage data; do not fabricate them.",
        },
        "cases": rows,
    }
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("eval/cases.jsonl"))
    parser.add_argument("--output", type=Path, default=Path("eval/report.json"))
    args = parser.parse_args()
    asyncio.run(main(args.input, args.output))
