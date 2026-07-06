from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

from ai_lab.documentation.l0_retrieval_simulator import (
    L0RetrievalSimulatorError,
    build_l0_retrieval_simulator_record,
    l0_candidate_inputs_from_store,
    l0_retrieval_simulator_manifest_document,
    validate_l0_retrieval_simulator_record,
)


def _write_l0_record(path: Path, summary_text: str = "retrieval simulator memory") -> None:
    helper_path = Path("tests/test_context_pack_builder.py")
    spec = importlib.util.spec_from_file_location(
        "context_pack_builder_test_helper",
        helper_path,
    )
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    module.write_l0_record(path, summary_text=summary_text)


def _config() -> dict[str, dict[str, object]]:
    return {
        "bm25_params": {
            "k1": 1.2,
            "b": 0.75,
            "tokenizer": "simple",
            "stoplist": [],
        },
        "dense_params": {
            "metric": "cosine",
            "top_k": 10,
            "ef_search": 32,
        },
        "combine_policy": {
            "method": "weighted_sum",
            "weights": {
                "bm25": 0.5,
                "dense": 0.5,
            },
        },
        "normalization": {
            "method": "none",
            "per_field": True,
        },
        "embedding_model": {
            "name": "mock-embedding",
            "version": "fixture-v1",
            "dimension": 3,
        },
    }


def _record() -> dict[str, object]:
    cfg = _config()
    return build_l0_retrieval_simulator_record(
        query_text="retrieval memory",
        query_kind="user",
        candidate_inputs=[
            {
                "chunk_id": "chunk-a",
                "artifact_id": "artifact-a",
                "version": "v1",
                "span": {"start_token": 1, "end_token": 5},
                "provenance_path": "docs/memory/l0/chunk-a.json",
                "text": "retrieval simulator memory",
                "dense_score": 0.75,
                "notes": "fixture",
            },
            {
                "chunk_id": "chunk-b",
                "artifact_id": "artifact-b",
                "version": "v1",
                "span": {"start_token": 6, "end_token": 10},
                "provenance_path": "docs/memory/l0/chunk-b.json",
                "text": "other topic",
                "dense_score": 0.10,
                "notes": "fixture",
            },
        ],
        bm25_params=cfg["bm25_params"],
        dense_params=cfg["dense_params"],
        combine_policy=cfg["combine_policy"],
        normalization=cfg["normalization"],
        embedding_model=cfg["embedding_model"],
        corpus_snapshot_id="snapshot-1",
        l0_index_namespace="read-only/l0/test",
        run_id="run-1",
        timestamp_utc="2026-07-06T00:00:00+00:00",
    )


def test_build_l0_retrieval_simulator_record_is_diagnostic_only():
    record = _record()

    validate_l0_retrieval_simulator_record(record)

    assert record["diagnostic_type"] == "l0_retrieval_simulator"
    assert record["algorithm"] == "bm25+dense"
    assert record["reranker"] == "none"
    assert record["guardrails"] == {
        "side_effects_blocked": True,
        "writes_performed": 0,
        "index_mutations": 0,
        "embedding_creations": 0,
    }

    candidates = record["candidates"]
    assert candidates[0]["rank"] == 1
    assert all(candidate["selection_effect"] == "none" for candidate in candidates)


def test_l0_retrieval_simulator_validator_rejects_selection_effect_change():
    record = _record()
    record["candidates"][0]["selection_effect"] = "included"

    with pytest.raises(L0RetrievalSimulatorError, match="selection_effect"):
        validate_l0_retrieval_simulator_record(record)


def test_l0_retrieval_simulator_reranker_may_be_omitted_and_is_treated_as_none():
    record = _record()
    del record["reranker"]

    validate_l0_retrieval_simulator_record(record)


def test_l0_retrieval_simulator_rejects_non_none_reranker():
    record = _record()
    record["reranker"] = "cross_encoder"

    with pytest.raises(L0RetrievalSimulatorError, match="reranker"):
        validate_l0_retrieval_simulator_record(record)


def test_l0_retrieval_simulator_manifest_document_uses_canonical_path_and_alias():
    record = _record()

    document = l0_retrieval_simulator_manifest_document(record)

    canonical = document["manifest"]["diagnostics"]["l0_retrieval_simulator"]
    alias = document["context_pack"]["selection_diagnostics"]["retrieval_candidates"]

    assert canonical["diagnostic_type"] == "l0_retrieval_simulator"
    assert alias["alias_for"] == "manifest.diagnostics.l0_retrieval_simulator"
    assert alias["deprecated"] is True
    assert alias["selection_effect"] == "none"
    assert alias["candidates"] == canonical["candidates"]


def test_l0_candidate_inputs_from_store_requires_external_dense_scores(tmp_path):
    l0_store = tmp_path / "l0"
    l0_store.mkdir()
    _write_l0_record(l0_store / "chunk-a.json")

    with pytest.raises(L0RetrievalSimulatorError, match="Missing externally provided dense score"):
        l0_candidate_inputs_from_store(l0_store=l0_store, dense_scores={})


def test_simulate_l0_retrieval_script_outputs_manifest_diagnostics(tmp_path):
    l0_store = tmp_path / "l0"
    l0_store.mkdir()
    _write_l0_record(l0_store / "chunk-a.json", summary_text="retrieval simulator memory")

    cfg = _config()
    config_paths = {}

    for name, value in cfg.items():
        path = tmp_path / f"{name}.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        config_paths[name] = path

    dense_scores = tmp_path / "dense_scores.json"
    dense_scores.write_text(json.dumps({"chunk-a": 0.8}), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/simulate_l0_retrieval.py",
            "--query",
            "retrieval memory",
            "--l0-store",
            str(l0_store),
            "--dense-scores",
            str(dense_scores),
            "--bm25-params",
            str(config_paths["bm25_params"]),
            "--dense-params",
            str(config_paths["dense_params"]),
            "--combine-policy",
            str(config_paths["combine_policy"]),
            "--normalization",
            str(config_paths["normalization"]),
            "--embedding-model",
            str(config_paths["embedding_model"]),
            "--corpus-snapshot-id",
            "snapshot-1",
            "--l0-index-namespace",
            "read-only/l0/test",
            "--run-id",
            "run-1",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode == 0, result.stderr

    data = json.loads(result.stdout)
    record = data["manifest"]["diagnostics"]["l0_retrieval_simulator"]
    validate_l0_retrieval_simulator_record(record)

    assert record["guardrails"]["writes_performed"] == 0
    assert record["guardrails"]["index_mutations"] == 0
    assert record["guardrails"]["embedding_creations"] == 0
    assert record["candidates"][0]["chunk_id"] == "chunk-a"
    assert record["candidates"][0]["selection_effect"] == "none"
