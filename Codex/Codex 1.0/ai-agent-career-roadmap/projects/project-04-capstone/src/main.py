"""Minimal runnable API surface for 供应商风险审查 Agent."""

from __future__ import annotations

from fastapi import FastAPI


app = FastAPI(title="供应商风险审查 Agent", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "project": "project-04-capstone"}
