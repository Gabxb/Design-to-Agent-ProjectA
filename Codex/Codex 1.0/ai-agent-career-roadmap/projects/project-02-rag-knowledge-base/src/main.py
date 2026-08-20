"""Minimal runnable API surface for 设计规范知识库 Agent."""

from __future__ import annotations

from fastapi import FastAPI


app = FastAPI(title="设计规范知识库 Agent", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "project": "project-02-rag-knowledge-base"}
