import pytest

from ai_lab.documentation.chunk_reference import create_chunk_reference
from ai_lab.documentation.citations import CitationSpan
from ai_lab.documentation.l0_summary import (
    Claim,
    Entity,
    L0ChunkSummary,
    L0SummaryError,
    Risk,
)


def make_reference():
    return create_chunk_reference(
        artifact_cid="3ac9f2b1d0af",
        version="a1c2d3e",
        span=CitationSpan(unit="b", start=100, end=200),
        path="docs/example.md",
        artifact_type="doc",
        language="markdown",
        embedding_ids=("emb_001",),
    )


def test_l0_chunk_summary_builds_valid_summary():
    summary = L0ChunkSummary(
        chunk_reference=make_reference(),
        l0_summary="Defines citation format and validation rules.",
        keyphrases=("citation", "span", "validation"),
        entities=(Entity(type="schema", name="Citation"),),
        claims=(Claim(text="Citations use cid@version|span.", polarity="pro"),),
        risks=(Risk(text="Token spans require tokenizer versioning.", severity="med"),),
        generator_model="gpt-5",
        generator_version="v1",
        pipeline_run_id="run_001",
    )

    assert summary.citation == "3ac9f2b1d0af@a1c2d3e|b:100-200"
    assert summary.keyphrases == ("citation", "span", "validation")


def test_l0_summary_requires_compact_summary():
    with pytest.raises(L0SummaryError):
        L0ChunkSummary(
            chunk_reference=make_reference(),
            l0_summary="",
            keyphrases=("citation", "span", "validation"),
        )


def test_l0_summary_rejects_too_long_summary():
    with pytest.raises(L0SummaryError):
        L0ChunkSummary(
            chunk_reference=make_reference(),
            l0_summary="x" * 301,
            keyphrases=("citation", "span", "validation"),
        )


def test_l0_summary_requires_three_to_ten_keyphrases():
    with pytest.raises(L0SummaryError):
        L0ChunkSummary(
            chunk_reference=make_reference(),
            l0_summary="Valid summary.",
            keyphrases=("only-one",),
        )

    with pytest.raises(L0SummaryError):
        L0ChunkSummary(
            chunk_reference=make_reference(),
            l0_summary="Valid summary.",
            keyphrases=tuple(f"k{i}" for i in range(11)),
        )


def test_claim_rejects_invalid_polarity():
    with pytest.raises(L0SummaryError):
        Claim(text="A claim.", polarity="maybe")


def test_risk_rejects_invalid_severity():
    with pytest.raises(L0SummaryError):
        Risk(text="A risk.", severity="critical")


def test_l0_summary_to_dict_serializes_reference_and_metadata():
    summary = L0ChunkSummary(
        chunk_reference=make_reference(),
        l0_summary="Defines citation format and validation rules.",
        keyphrases=("citation", "span", "validation"),
        entities=(Entity(type="schema", name="Citation"),),
        claims=(Claim(text="Citations use cid@version|span.", polarity="pro"),),
        risks=(Risk(text="Token spans require tokenizer versioning.", severity="med"),),
        created_at="2026-06-30T00:00:00+00:00",
        last_refreshed_at="2026-06-30T00:00:00+00:00",
        generator_model="gpt-5",
        generator_version="v1",
        pipeline_run_id="run_001",
    )

    data = summary.to_dict()

    assert data["citation"] == "3ac9f2b1d0af@a1c2d3e|b:100-200"
    assert data["l0_summary"] == "Defines citation format and validation rules."
    assert data["keyphrases"] == ["citation", "span", "validation"]
    assert data["entities"] == [{"type": "schema", "name": "Citation"}]
    assert data["claims"] == [
        {
            "text": "Citations use cid@version|span.",
            "polarity": "pro",
        }
    ]
    assert data["risks"] == [
        {
            "text": "Token spans require tokenizer versioning.",
            "severity": "med",
        }
    ]
    assert data["generator"] == {
        "model": "gpt-5",
        "version": "v1",
    }
    assert data["provenance"] == {
        "pipeline_run_id": "run_001",
    }
