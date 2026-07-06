from __future__ import annotations

from datetime import datetime, timezone
import json
import math
from pathlib import Path
import re
from statistics import mean, pstdev
from typing import Iterable

from ai_lab.documentation.l0_summary import (
    L0SummaryError,
    validate_l0_summary_record,
)


class L0RetrievalSimulatorError(ValueError):
    """Raised when L0 retrieval simulator diagnostics are malformed."""


SIMULATOR_SCHEMA_VERSION = "v1"
SIMULATOR_ID = "l0_hybrid_retrieval_simulator.v1"
CANONICAL_SECTION_PATH = "manifest.diagnostics.l0_retrieval_simulator"
COMPATIBILITY_ALIAS_PATH = "context_pack.selection_diagnostics.retrieval_candidates"


def utc_now_iso() -> str:
    """Return current UTC time in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def _read_json_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise L0RetrievalSimulatorError(f"{path} must contain a JSON object.")
    return value


def _tokenize(text: str, stoplist: Iterable[str] = ()) -> list[str]:
    stopwords = {item.lower() for item in stoplist}
    return [
        token
        for token in re.findall(r"[A-Za-z0-9_]+", text.lower())
        if token and token not in stopwords
    ]


def _non_empty_string(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value:
        raise L0RetrievalSimulatorError(f"{field_name} must be a non-empty string.")
    return value


def _number(value: object, field_name: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise L0RetrievalSimulatorError(f"{field_name} must be a number.")

    result = float(value)
    if not math.isfinite(result):
        raise L0RetrievalSimulatorError(f"{field_name} must be finite.")

    return result


def _score_stats(values: list[float]) -> dict[str, float]:
    if not values:
        return {"min": 0.0, "max": 0.0, "mean": 0.0, "std": 0.0}

    return {
        "min": round(min(values), 6),
        "max": round(max(values), 6),
        "mean": round(mean(values), 6),
        "std": round(pstdev(values), 6),
    }


def _normalize_values(values: list[float], method: str) -> list[float]:
    if method == "none":
        return values

    if not values:
        return []

    if method == "minmax":
        low = min(values)
        high = max(values)
        if high == low:
            return [0.0 for _ in values]
        return [(value - low) / (high - low) for value in values]

    if method == "zscore":
        sigma = pstdev(values)
        if sigma == 0:
            return [0.0 for _ in values]
        mu = mean(values)
        return [(value - mu) / sigma for value in values]

    raise L0RetrievalSimulatorError(
        "normalization.method must be one of: none, minmax, zscore."
    )


def _normalize_score_fields(
    bm25_scores: list[float],
    dense_scores: list[float],
    normalization: dict[str, object],
) -> tuple[list[float], list[float]]:
    method = _non_empty_string(normalization.get("method"), "normalization.method")
    per_field = normalization.get("per_field")

    if not isinstance(per_field, bool):
        raise L0RetrievalSimulatorError("normalization.per_field must be a boolean.")

    if method == "none":
        return bm25_scores, dense_scores

    if per_field:
        return (
            _normalize_values(bm25_scores, method),
            _normalize_values(dense_scores, method),
        )

    combined = _normalize_values([*bm25_scores, *dense_scores], method)
    return combined[: len(bm25_scores)], combined[len(bm25_scores) :]


def _bm25_scores(
    query_text: str,
    documents: list[str],
    bm25_params: dict[str, object],
) -> list[float]:
    tokenizer = _non_empty_string(bm25_params.get("tokenizer"), "bm25_params.tokenizer")
    if tokenizer != "simple":
        raise L0RetrievalSimulatorError("Only bm25_params.tokenizer='simple' is supported.")

    stoplist = bm25_params.get("stoplist")
    if not isinstance(stoplist, list) or not all(isinstance(item, str) for item in stoplist):
        raise L0RetrievalSimulatorError("bm25_params.stoplist must be a list of strings.")

    k1 = _number(bm25_params.get("k1"), "bm25_params.k1")
    b = _number(bm25_params.get("b"), "bm25_params.b")

    query_tokens = _tokenize(query_text, stoplist)
    doc_tokens = [_tokenize(document, stoplist) for document in documents]

    if not documents:
        return []

    avgdl = mean([len(tokens) for tokens in doc_tokens] or [0]) or 1.0
    n_docs = len(doc_tokens)
    scores: list[float] = []

    for tokens in doc_tokens:
        score = 0.0
        dl = len(tokens) or 1

        for query_token in query_tokens:
            tf = tokens.count(query_token)
            if tf == 0:
                continue

            df = sum(1 for candidate_tokens in doc_tokens if query_token in candidate_tokens)
            idf = math.log(1 + (n_docs - df + 0.5) / (df + 0.5))
            denom = tf + k1 * (1 - b + b * dl / avgdl)
            score += idf * (tf * (k1 + 1)) / denom

        scores.append(round(score, 6))

    return scores


def _chunk_text(record: dict[str, object]) -> str:
    parts: list[str] = []

    for key in ("l0_summary",):
        value = record.get(key)
        if isinstance(value, str):
            parts.append(value)

    for key in ("keyphrases", "claims", "risks"):
        values = record.get(key)
        if isinstance(values, list):
            for value in values:
                if isinstance(value, str):
                    parts.append(value)
                elif isinstance(value, dict):
                    parts.extend(str(item) for item in value.values() if isinstance(item, str))

    entities = record.get("entities")
    if isinstance(entities, list):
        for entity in entities:
            if isinstance(entity, str):
                parts.append(entity)
            elif isinstance(entity, dict):
                parts.extend(str(item) for item in entity.values() if isinstance(item, str))

    return "\n".join(parts)


def l0_candidate_inputs_from_store(
    l0_store: Path,
    dense_scores: dict[str, float],
) -> list[dict[str, object]]:
    """Build simulator inputs from a read-only L0 snapshot and external dense scores."""

    if not l0_store.is_dir():
        raise L0RetrievalSimulatorError(f"l0_store is not a directory: {l0_store}")

    candidates: list[dict[str, object]] = []

    for path in sorted(l0_store.glob("*.json")):
        record = _read_json_object(path)

        try:
            validate_l0_summary_record(record)
        except L0SummaryError as exc:
            raise L0RetrievalSimulatorError(
                f"Invalid L0 summary record for simulator input: {path}"
            ) from exc

        chunk_reference = record["chunk_reference"]
        if not isinstance(chunk_reference, dict):
            raise L0RetrievalSimulatorError("chunk_reference must be an object.")

        chunk_id = _non_empty_string(
            chunk_reference.get("chunk_id"),
            "chunk_reference.chunk_id",
        )

        if chunk_id not in dense_scores:
            raise L0RetrievalSimulatorError(
                f"Missing externally provided dense score for chunk_id: {chunk_id}"
            )

        span = chunk_reference.get("span")
        if not isinstance(span, dict):
            raise L0RetrievalSimulatorError("chunk_reference.span must be an object.")

        candidates.append(
            {
                "chunk_id": chunk_id,
                "artifact_id": _non_empty_string(
                    chunk_reference.get("artifact_cid"),
                    "chunk_reference.artifact_cid",
                ),
                "version": _non_empty_string(
                    chunk_reference.get("version"),
                    "chunk_reference.version",
                ),
                "span": {
                    "start_token": int(_number(span.get("start"), "chunk_reference.span.start")),
                    "end_token": int(_number(span.get("end"), "chunk_reference.span.end")),
                },
                "provenance_path": str(chunk_reference.get("path") or path),
                "text": _chunk_text(record),
                "dense_score": dense_scores[chunk_id],
                "notes": "dense_score supplied by external fixture or read-only snapshot",
            }
        )

    return candidates


def _validate_required_config(
    *,
    bm25_params: dict[str, object],
    dense_params: dict[str, object],
    combine_policy: dict[str, object],
    normalization: dict[str, object],
    embedding_model: dict[str, object],
) -> None:
    _number(bm25_params.get("k1"), "bm25_params.k1")
    _number(bm25_params.get("b"), "bm25_params.b")
    _non_empty_string(bm25_params.get("tokenizer"), "bm25_params.tokenizer")
    if not isinstance(bm25_params.get("stoplist"), list):
        raise L0RetrievalSimulatorError("bm25_params.stoplist must be supplied.")

    _non_empty_string(dense_params.get("metric"), "dense_params.metric")
    _number(dense_params.get("top_k"), "dense_params.top_k")
    _number(dense_params.get("ef_search"), "dense_params.ef_search")

    method = _non_empty_string(combine_policy.get("method"), "combine_policy.method")
    if method != "weighted_sum":
        raise L0RetrievalSimulatorError("Only combine_policy.method='weighted_sum' is supported.")

    weights = combine_policy.get("weights")
    if not isinstance(weights, dict):
        raise L0RetrievalSimulatorError("combine_policy.weights must be supplied.")

    _number(weights.get("bm25"), "combine_policy.weights.bm25")
    _number(weights.get("dense"), "combine_policy.weights.dense")

    _non_empty_string(normalization.get("method"), "normalization.method")
    if not isinstance(normalization.get("per_field"), bool):
        raise L0RetrievalSimulatorError("normalization.per_field must be supplied.")

    _non_empty_string(embedding_model.get("name"), "embedding_model.name")
    _non_empty_string(embedding_model.get("version"), "embedding_model.version")
    _number(embedding_model.get("dimension"), "embedding_model.dimension")


def build_l0_retrieval_simulator_record(
    *,
    query_text: str,
    query_kind: str,
    candidate_inputs: list[dict[str, object]],
    bm25_params: dict[str, object],
    dense_params: dict[str, object],
    combine_policy: dict[str, object],
    normalization: dict[str, object],
    embedding_model: dict[str, object],
    corpus_snapshot_id: str,
    l0_index_namespace: str,
    run_id: str,
    timestamp_utc: str | None = None,
    request_id: str | None = None,
    episode_id: str | None = None,
    manifest_id: str | None = None,
    manifest_version: str | None = None,
    reranker: str | None = "none",
) -> dict[str, object]:
    """Build manifest.diagnostics.l0_retrieval_simulator without side effects."""

    query_text = _non_empty_string(query_text, "query_text")
    query_kind = _non_empty_string(query_kind, "query_kind")
    corpus_snapshot_id = _non_empty_string(corpus_snapshot_id, "corpus_snapshot_id")
    l0_index_namespace = _non_empty_string(l0_index_namespace, "l0_index_namespace")
    run_id = _non_empty_string(run_id, "run_id")

    if reranker not in (None, "none"):
        raise L0RetrievalSimulatorError("reranker must be omitted or equal to 'none'.")

    _validate_required_config(
        bm25_params=bm25_params,
        dense_params=dense_params,
        combine_policy=combine_policy,
        normalization=normalization,
        embedding_model=embedding_model,
    )

    documents = [
        _non_empty_string(candidate.get("text"), "candidate.text")
        for candidate in candidate_inputs
    ]
    bm25_scores = _bm25_scores(query_text, documents, bm25_params)
    dense_scores = [
        _number(candidate.get("dense_score"), "candidate.dense_score")
        for candidate in candidate_inputs
    ]

    normalized_bm25, normalized_dense = _normalize_score_fields(
        bm25_scores,
        dense_scores,
        normalization,
    )

    weights = combine_policy["weights"]
    assert isinstance(weights, dict)
    bm25_weight = _number(weights.get("bm25"), "combine_policy.weights.bm25")
    dense_weight = _number(weights.get("dense"), "combine_policy.weights.dense")

    scored_candidates: list[dict[str, object]] = []
    retrieval_scores: list[float] = []

    for index, candidate in enumerate(candidate_inputs):
        bm25_score = bm25_scores[index]
        dense_score = dense_scores[index]
        retrieval_score = round(
            normalized_bm25[index] * bm25_weight
            + normalized_dense[index] * dense_weight,
            6,
        )
        retrieval_scores.append(retrieval_score)

        if bm25_score > 0 and dense_score > 0:
            match_reason = "hybrid_top_k"
        elif bm25_score > 0:
            match_reason = "bm25_keyword_match"
        elif dense_score > 0:
            match_reason = "dense_semantic_match"
        else:
            match_reason = "no_match"

        scored_candidates.append(
            {
                "chunk_id": _non_empty_string(candidate.get("chunk_id"), "candidate.chunk_id"),
                "artifact_id": _non_empty_string(candidate.get("artifact_id"), "candidate.artifact_id"),
                "version": _non_empty_string(candidate.get("version"), "candidate.version"),
                "span": candidate.get("span"),
                "provenance_path": _non_empty_string(
                    candidate.get("provenance_path"),
                    "candidate.provenance_path",
                ),
                "bm25_score": bm25_score,
                "dense_score": dense_score,
                "retrieval_score": retrieval_score,
                "rank": 0,
                "match_reason": match_reason,
                "selection_effect": "none",
                "notes": candidate.get("notes", ""),
            }
        )

    scored_candidates.sort(
        key=lambda item: (-float(item["retrieval_score"]), str(item["chunk_id"]))
    )

    for rank, candidate in enumerate(scored_candidates, start=1):
        candidate["rank"] = rank

    record: dict[str, object] = {
        "schema_version": SIMULATOR_SCHEMA_VERSION,
        "diagnostic_type": "l0_retrieval_simulator",
        "simulator_id": SIMULATOR_ID,
        "run_id": run_id,
        "timestamp_utc": timestamp_utc or utc_now_iso(),
        "query_text": query_text,
        "query_kind": query_kind,
        "algorithm": "bm25+dense",
        "corpus_snapshot_id": corpus_snapshot_id,
        "l0_index_namespace": l0_index_namespace,
        "embedding_model": embedding_model,
        "bm25_params": bm25_params,
        "dense_params": dense_params,
        "combine_policy": combine_policy,
        "normalization": normalization,
        "candidates": scored_candidates,
        "aggregates": {
            "total_candidates": len(scored_candidates),
            "top_k": int(_number(dense_params.get("top_k"), "dense_params.top_k")),
            "score_stats": {
                "bm25": _score_stats(bm25_scores),
                "dense": _score_stats(dense_scores),
                "retrieval": _score_stats(retrieval_scores),
            },
            "normalization_applied": normalization.get("method") != "none",
            "warnings": [],
        },
        "guardrails": {
            "side_effects_blocked": True,
            "writes_performed": 0,
            "index_mutations": 0,
            "embedding_creations": 0,
        },
    }

    if reranker == "none":
        record["reranker"] = "none"

    optional_header_fields = {
        "request_id": request_id,
        "episode_id": episode_id,
        "manifest_id": manifest_id,
        "manifest_version": manifest_version,
    }

    for key, value in optional_header_fields.items():
        if value is not None:
            record[key] = _non_empty_string(value, key)

    validate_l0_retrieval_simulator_record(record)
    return record


def validate_l0_retrieval_simulator_record(record: dict[str, object]) -> None:
    """Validate the diagnostic simulator section admitted by WARR-20260706-0003."""

    required = {
        "schema_version",
        "diagnostic_type",
        "simulator_id",
        "run_id",
        "timestamp_utc",
        "query_text",
        "query_kind",
        "algorithm",
        "corpus_snapshot_id",
        "l0_index_namespace",
        "embedding_model",
        "bm25_params",
        "dense_params",
        "combine_policy",
        "normalization",
        "candidates",
        "aggregates",
        "guardrails",
    }

    for field_name in sorted(required):
        if field_name not in record:
            raise L0RetrievalSimulatorError(f"Missing required field: {field_name}")

    if record["schema_version"] != SIMULATOR_SCHEMA_VERSION:
        raise L0RetrievalSimulatorError("Unsupported schema_version.")

    if record["diagnostic_type"] != "l0_retrieval_simulator":
        raise L0RetrievalSimulatorError("diagnostic_type must be l0_retrieval_simulator.")

    if record["algorithm"] != "bm25+dense":
        raise L0RetrievalSimulatorError("algorithm must be bm25+dense.")

    if record.get("reranker", "none") != "none":
        raise L0RetrievalSimulatorError("reranker must be omitted or equal to 'none'.")

    for field_name in ("embedding_model", "bm25_params", "dense_params", "combine_policy", "normalization"):
        if not isinstance(record[field_name], dict):
            raise L0RetrievalSimulatorError(f"{field_name} must be an object.")

    _validate_required_config(
        bm25_params=record["bm25_params"],  # type: ignore[arg-type]
        dense_params=record["dense_params"],  # type: ignore[arg-type]
        combine_policy=record["combine_policy"],  # type: ignore[arg-type]
        normalization=record["normalization"],  # type: ignore[arg-type]
        embedding_model=record["embedding_model"],  # type: ignore[arg-type]
    )

    candidates = record["candidates"]
    if not isinstance(candidates, list):
        raise L0RetrievalSimulatorError("candidates must be a list.")

    for candidate in candidates:
        if not isinstance(candidate, dict):
            raise L0RetrievalSimulatorError("candidate entries must be objects.")

        if candidate.get("selection_effect") != "none":
            raise L0RetrievalSimulatorError("candidate.selection_effect must be 'none'.")

        for field_name in (
            "chunk_id",
            "artifact_id",
            "version",
            "provenance_path",
            "match_reason",
        ):
            _non_empty_string(candidate.get(field_name), f"candidate.{field_name}")

        for field_name in ("bm25_score", "dense_score", "retrieval_score", "rank"):
            _number(candidate.get(field_name), f"candidate.{field_name}")

        span = candidate.get("span")
        if not isinstance(span, dict):
            raise L0RetrievalSimulatorError("candidate.span must be an object.")

        _number(span.get("start_token"), "candidate.span.start_token")
        _number(span.get("end_token"), "candidate.span.end_token")

    guardrails = record["guardrails"]
    if not isinstance(guardrails, dict):
        raise L0RetrievalSimulatorError("guardrails must be an object.")

    expected_guardrails = {
        "side_effects_blocked": True,
        "writes_performed": 0,
        "index_mutations": 0,
        "embedding_creations": 0,
    }

    for key, expected in expected_guardrails.items():
        if guardrails.get(key) != expected:
            raise L0RetrievalSimulatorError(f"guardrails.{key} must be {expected!r}.")


def l0_retrieval_simulator_manifest_document(
    simulator_record: dict[str, object],
    *,
    include_alias: bool = True,
) -> dict[str, object]:
    """Wrap simulator diagnostics under the admitted manifest diagnostics path."""

    validate_l0_retrieval_simulator_record(simulator_record)

    document: dict[str, object] = {
        "manifest": {
            "diagnostics": {
                "l0_retrieval_simulator": simulator_record,
            }
        }
    }

    if include_alias:
        document["context_pack"] = {
            "selection_diagnostics": {
                "retrieval_candidates": {
                    "alias_for": CANONICAL_SECTION_PATH,
                    "deprecated": True,
                    "selection_effect": "none",
                    "candidates": simulator_record["candidates"],
                }
            }
        }

    return document
