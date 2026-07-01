import pytest

from ai_lab.documentation.artifact_summary import (
    ArtifactDependency,
    ArtifactSummary,
    ArtifactSummaryError,
)


def test_artifact_summary_builds_valid_discovery_record():
    dependency = ArtifactDependency(
        artifact_cid="4bc9f2b1d0af",
        version="b1c2d3e",
        path="docs/architecture/context.md",
        reason="Provides manifest design.",
    )

    summary = ArtifactSummary(
        artifact_cid="3ac9f2b1d0af",
        version="a1c2d3e",
        path="docs/example.md",
        artifact_type="doc",
        language="markdown",
        size_bytes=2048,
        complexity_score=0.4,
        tags=("memory", "citation", "manifest"),
        dependencies=(dependency,),
        synopsis="Defines the memory artifact discovery record.",
        generator_model="gpt-5",
        generator_version="v1",
        pipeline_run_id="run_001",
    )

    assert summary.artifact_ref == "3ac9f2b1d0af@a1c2d3e"
    assert summary.dependencies == (dependency,)


def test_artifact_dependency_serializes_reason_when_present():
    dependency = ArtifactDependency(
        artifact_cid="4bc9f2b1d0af",
        version="b1c2d3e",
        path="docs/architecture/context.md",
        reason="Provides manifest design.",
    )

    assert dependency.to_dict() == {
        "artifact_cid": "4bc9f2b1d0af",
        "version": "b1c2d3e",
        "path": "docs/architecture/context.md",
        "reason": "Provides manifest design.",
    }


def test_artifact_summary_rejects_invalid_cid():
    with pytest.raises(ArtifactSummaryError):
        ArtifactSummary(
            artifact_cid="nothex",
            version="a1c2d3e",
            path="docs/example.md",
            artifact_type="doc",
            language="markdown",
            size_bytes=2048,
            complexity_score=0.4,
        )


def test_artifact_summary_rejects_invalid_artifact_type():
    with pytest.raises(ArtifactSummaryError):
        ArtifactSummary(
            artifact_cid="3ac9f2b1d0af",
            version="a1c2d3e",
            path="docs/example.md",
            artifact_type="unknown",
            language="markdown",
            size_bytes=2048,
            complexity_score=0.4,
        )


def test_artifact_summary_rejects_negative_size_or_complexity():
    with pytest.raises(ArtifactSummaryError):
        ArtifactSummary(
            artifact_cid="3ac9f2b1d0af",
            version="a1c2d3e",
            path="docs/example.md",
            artifact_type="doc",
            language="markdown",
            size_bytes=-1,
            complexity_score=0.4,
        )

    with pytest.raises(ArtifactSummaryError):
        ArtifactSummary(
            artifact_cid="3ac9f2b1d0af",
            version="a1c2d3e",
            path="docs/example.md",
            artifact_type="doc",
            language="markdown",
            size_bytes=2048,
            complexity_score=-0.1,
        )


def test_artifact_summary_rejects_too_many_tags():
    with pytest.raises(ArtifactSummaryError):
        ArtifactSummary(
            artifact_cid="3ac9f2b1d0af",
            version="a1c2d3e",
            path="docs/example.md",
            artifact_type="doc",
            language="markdown",
            size_bytes=2048,
            complexity_score=0.4,
            tags=tuple(f"tag{i}" for i in range(21)),
        )


def test_artifact_summary_to_dict_serializes_metadata():
    dependency = ArtifactDependency(
        artifact_cid="4bc9f2b1d0af",
        version="b1c2d3e",
        path="docs/architecture/context.md",
    )

    summary = ArtifactSummary(
        artifact_cid="3ac9f2b1d0af",
        version="a1c2d3e",
        path="docs/example.md",
        artifact_type="doc",
        language="markdown",
        size_bytes=2048,
        complexity_score=0.4,
        tags=("memory", "citation"),
        dependencies=(dependency,),
        synopsis="Defines artifact summary metadata.",
        created_at="2026-06-30T00:00:00+00:00",
        last_refreshed_at="2026-06-30T00:00:00+00:00",
        generator_model="gpt-5",
        generator_version="v1",
        pipeline_run_id="run_001",
    )

    data = summary.to_dict()

    assert data["artifact_ref"] == "3ac9f2b1d0af@a1c2d3e"
    assert data["path"] == "docs/example.md"
    assert data["artifact_type"] == "doc"
    assert data["language"] == "markdown"
    assert data["size_bytes"] == 2048
    assert data["complexity_score"] == 0.4
    assert data["tags"] == ["memory", "citation"]
    assert data["dependencies"] == [
        {
            "artifact_cid": "4bc9f2b1d0af",
            "version": "b1c2d3e",
            "path": "docs/architecture/context.md",
        }
    ]
    assert data["generator"] == {
        "model": "gpt-5",
        "version": "v1",
    }
    assert data["provenance"] == {
        "pipeline_run_id": "run_001",
    }
