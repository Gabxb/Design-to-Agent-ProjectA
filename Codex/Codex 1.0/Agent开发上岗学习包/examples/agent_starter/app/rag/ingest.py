from __future__ import annotations

from pathlib import Path

from app.rag.service import Chunk


def chunk_text(
    text: str,
    *,
    tenant_id: str,
    source: str,
    chunk_size: int = 800,
    overlap: int = 120,
) -> list[Chunk]:
    """Deterministic starter chunker; production systems should preserve headings/ACL metadata."""
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("require chunk_size > overlap >= 0")
    normalized = "\n".join(line.rstrip() for line in text.splitlines()).strip()
    chunks: list[Chunk] = []
    start = 0
    index = 0
    while start < len(normalized):
        end = min(len(normalized), start + chunk_size)
        body = normalized[start:end].strip()
        if body:
            chunks.append(
                Chunk(
                    chunk_id=f"{Path(source).name}:{index}",
                    tenant_id=tenant_id,
                    text=body,
                    source=source,
                )
            )
            index += 1
        if end >= len(normalized):
            break
        start = end - overlap
    return chunks


def ingest_text_file(path: str | Path, tenant_id: str) -> list[Chunk]:
    file_path = Path(path)
    if file_path.suffix.lower() not in {".txt", ".md"}:
        raise ValueError("starter ingester only accepts .txt or .md")
    text = file_path.read_text(encoding="utf-8")
    return chunk_text(text, tenant_id=tenant_id, source=str(file_path))
