from app.rag.ingest import chunk_text


def test_chunk_text_preserves_tenant_and_source() -> None:
    chunks = chunk_text("A" * 1200, tenant_id="acme", source="handbook.md", chunk_size=500, overlap=50)
    assert len(chunks) >= 3
    assert all(chunk.tenant_id == "acme" for chunk in chunks)
    assert all(chunk.source == "handbook.md" for chunk in chunks)
