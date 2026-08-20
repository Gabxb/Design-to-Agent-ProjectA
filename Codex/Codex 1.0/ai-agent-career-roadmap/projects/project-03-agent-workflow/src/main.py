"""Minimal runnable API surface for 智能设计评审 Agent."""

from __future__ import annotations

from fastapi import FastAPI


app = FastAPI(title="智能设计评审 Agent", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "project": "project-03-agent-workflow"}
