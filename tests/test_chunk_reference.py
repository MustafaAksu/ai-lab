import pytest

from ai_lab.documentation.chunk_reference import (
    ChunkReference,
    ChunkReferenceError,
    compute_chunk_id,
    create_chunk_reference,
)
from ai_lab.documentation.citations import CitationSpan


def test_compute_chunk_id_is_deterministic():
    span = CitationSpan(unit="b", start=10, end=20)

    first = compute_chunk_id("3ac9f2b1d0af", "a1c2d3e", span)
    second = compute_chunk_id("3ac9f2b1d0af", "a1c2d3e", span)

    assert first == second
    assert len(first) == 64


def test_create_chunk_reference_builds_valid_reference():
    reference = create_chunk_reference(
        artifact_cid="3ac9f2b1d0af",
        version="a1c2d3e",
        span=CitationSpan(unit="b", start=1024, end=2047),
        path="docs/example.md",
        artifact_type="doc",
        language="markdown",
        embedding_ids=("emb_001",),
        redaction_level="none",
    )

    assert reference.artifact_cid == "3ac9f2b1d0af"
    assert reference.version == "a1c2d3e"
    assert str(reference.citation) == "3ac9f2b1d0af@a1c2d3e|b:1024-2047"
    assert reference.embedding_ids == ("emb_001",)


def test_chunk_reference_rejects_wrong_chunk_id():
    with pytest.raises(ChunkReferenceError):
        ChunkReference(
            chunk_id="wrong",
            artifact_cid="3ac9f2b1d0af",
            version="a1c2d3e",
            span=CitationSpan(unit="b", start=10, end=20),
        )


def test_chunk_reference_rejects_invalid_artifact_type():
    with pytest.raises(ChunkReferenceError):
        create_chunk_reference(
            artifact_cid="3ac9f2b1d0af",
            version="a1c2d3e",
            span=CitationSpan(unit="b", start=10, end=20),
            artifact_type="unknown-type",
        )


def test_chunk_reference_rejects_invalid_redaction_level():
    with pytest.raises(ChunkReferenceError):
        create_chunk_reference(
            artifact_cid="3ac9f2b1d0af",
            version="a1c2d3e",
            span=CitationSpan(unit="b", start=10, end=20),
            redaction_level="secretish",
        )


def test_chunk_reference_to_dict_serializes_span_and_metadata():
    reference = create_chunk_reference(
        artifact_cid="3ac9f2b1d0af",
        version="a1c2d3e",
        span=CitationSpan(unit="t", start=10, end=40, tokenizer="mistral-v3"),
        path="src/module.py",
        artifact_type="code",
        language="python",
        embedding_ids=("emb_001", "emb_002"),
        redaction_level="partial",
    )

    data = reference.to_dict()

    assert data["artifact_cid"] == "3ac9f2b1d0af"
    assert data["span"] == {
        "unit": "t",
        "start": 10,
        "end": 40,
        "tokenizer": "mistral-v3",
    }
    assert data["path"] == "src/module.py"
    assert data["artifact_type"] == "code"
    assert data["language"] == "python"
    assert data["embedding_ids"] == ["emb_001", "emb_002"]
    assert data["redaction_level"] == "partial"
