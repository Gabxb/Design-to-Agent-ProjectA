"""Minimal runnable API surface for 设计需求分析助手."""

from __future__ import annotations

from fastapi import FastAPI


app = FastAPI(title="设计需求分析助手", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "project": "project-01-tool-calling"}
