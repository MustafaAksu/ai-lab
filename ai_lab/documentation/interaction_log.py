"""Interaction-log and episode-level memory summary schemas.

These schemas are the first rolling-memory primitives for AI-Lab.

They intentionally do not implement graph persistence, topological context
packing, embeddings, or automatic provider execution. They preserve enough
structured provenance that future WarrantEdge/MemoryEdge records can be derived
without losing citation or source-event information.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
from typing import Any

from ai_lab.documentation.citations import CitationError, parse_citation


class InteractionLogError(ValueError):
    """Raised when an interaction-log object is invalid."""


VALID_EVENT_TYPES = {
    "user_message",
    "assistant_message",
    "system_message",
    "tool_call",
    "tool_result",
    "command",
    "command_result",
    "provider_request",
    "provider_response",
    "commit",
    "test_run",
    "decision",
    "observation",
    "error",
    "artifact_created",
}

VALID_ROLES = {
    "user",
    "assistant",
    "system",
    "tool",
    "provider",
    "human",
    "process",
}

VALID_ACCESS_LEVELS = {
    "public",
    "internal",
    "private",
}

VALID_REDACTION_LEVELS = {
    "none",
    "partial",
    "full",
}

VALID_FRESHNESS_STATES = {
    "fresh",
    "stale",
    "unknown",
}

_HASH_RE = re.compile(r"^[0-9a-f]{64}$")
_COMMIT_RE = re.compile(r"^[0-9a-f]{7,40}$")
_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$")


def _validate_id(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value:
        raise InteractionLogError(f"{field_name} must be a non-empty string.")
    if not _ID_RE.match(value):
        raise InteractionLogError(
            f"{field_name} must start with an alphanumeric character and "
            "contain only letters, numbers, '_', '.', ':', or '-'."
        )


def _validate_optional_id(value: str | None, field_name: str) -> None:
    if value is not None:
        _validate_id(value, field_name)


def _validate_short_text(
    value: str,
    field_name: str,
    *,
    max_length: int,
    allow_empty: bool = False,
) -> None:
    if not isinstance(value, str):
        raise InteractionLogError(f"{field_name} must be a string.")
    if not allow_empty and not value.strip():
        raise InteractionLogError(f"{field_name} must not be empty.")
    if len(value) > max_length:
        raise InteractionLogError(f"{field_name} must be <= {max_length} characters.")


def _validate_iso_datetime(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value:
        raise InteractionLogError(f"{field_name} must be a non-empty ISO datetime string.")
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise InteractionLogError(f"{field_name} must be an ISO datetime string.") from exc


def _validate_optional_iso_datetime(value: str | None, field_name: str) -> None:
    if value is not None:
        _validate_iso_datetime(value, field_name)


def _validate_optional_hash(value: str | None, field_name: str) -> None:
    if value is not None and not _HASH_RE.match(value):
        raise InteractionLogError(f"{field_name} must be a lowercase sha256 hex digest.")


def _validate_optional_commit(value: str | None, field_name: str) -> None:
    if value is not None and not _COMMIT_RE.match(value):
        raise InteractionLogError(f"{field_name} must be a git commit hash.")


def _as_tuple(values: tuple[str, ...] | list[str], field_name: str) -> tuple[str, ...]:
    if not isinstance(values, (tuple, list)):
        raise InteractionLogError(f"{field_name} must be a tuple or list of strings.")
    normalized = tuple(values)
    for value in normalized:
        _validate_short_text(value, field_name, max_length=512)
    if len(set(normalized)) != len(normalized):
        raise InteractionLogError(f"{field_name} must not contain duplicates.")
    return normalized


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _coerce_tuple_fields(payload: dict[str, Any], fields: tuple[str, ...]) -> dict[str, Any]:
    normalized = dict(payload)
    for field_name in fields:
        if field_name in normalized and isinstance(normalized[field_name], list):
            normalized[field_name] = tuple(normalized[field_name])
    return normalized


def _write_json(path: str | Path, payload: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def _read_json(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text())
    if not isinstance(payload, dict):
        raise InteractionLogError("JSON payload must be an object.")
    return payload


@dataclass(frozen=True)
class InteractionLogEvent:
    """Append-only record of one interaction or process event."""

    event_id: str
    episode_id: str
    turn_id: int
    created_at: str
    event_type: str
    role: str
    actor: str
    summary: str
    request_text_hash: str | None = None
    response_text_hash: str | None = None
    prompt_manifest_id: str | None = None
    selected_context_manifest_id: str | None = None
    artifact_ids: tuple[str, ...] = field(default_factory=tuple)
    commit_hash: str | None = None
    topics: tuple[str, ...] = field(default_factory=tuple)
    scope: str = "default"
    namespace: str = "public"
    access_level: str = "public"
    redaction_level: str = "none"
    model_used: str | None = None
    model_version: str | None = None
    tokens_prompt: int | None = None
    tokens_completion: int | None = None
    duration_ms: int | None = None
    outcome_code: str | None = None
    error_code: str | None = None
    error_message: str | None = None

    def __post_init__(self) -> None:
        _validate_id(self.event_id, "event_id")
        _validate_id(self.episode_id, "episode_id")
        if not isinstance(self.turn_id, int) or self.turn_id < 0:
            raise InteractionLogError("turn_id must be a non-negative integer.")
        _validate_iso_datetime(self.created_at, "created_at")
        if self.event_type not in VALID_EVENT_TYPES:
            raise InteractionLogError(f"event_type must be one of {sorted(VALID_EVENT_TYPES)}.")
        if self.role not in VALID_ROLES:
            raise InteractionLogError(f"role must be one of {sorted(VALID_ROLES)}.")
        _validate_short_text(self.actor, "actor", max_length=128)
        _validate_short_text(self.summary, "summary", max_length=2000)
        _validate_optional_hash(self.request_text_hash, "request_text_hash")
        _validate_optional_hash(self.response_text_hash, "response_text_hash")
        _validate_optional_id(self.prompt_manifest_id, "prompt_manifest_id")
        _validate_optional_id(self.selected_context_manifest_id, "selected_context_manifest_id")
        object.__setattr__(self, "artifact_ids", _as_tuple(self.artifact_ids, "artifact_ids"))
        _validate_optional_commit(self.commit_hash, "commit_hash")
        object.__setattr__(self, "topics", _as_tuple(self.topics, "topics"))
        _validate_short_text(self.scope, "scope", max_length=128)
        _validate_short_text(self.namespace, "namespace", max_length=128)
        if self.access_level not in VALID_ACCESS_LEVELS:
            raise InteractionLogError(
                f"access_level must be one of {sorted(VALID_ACCESS_LEVELS)}."
            )
        if self.redaction_level not in VALID_REDACTION_LEVELS:
            raise InteractionLogError(
                f"redaction_level must be one of {sorted(VALID_REDACTION_LEVELS)}."
            )
        for field_name in ("model_used", "model_version", "outcome_code", "error_code"):
            value = getattr(self, field_name)
            if value is not None:
                _validate_short_text(value, field_name, max_length=128)
        if self.error_message is not None:
            _validate_short_text(
                self.error_message,
                "error_message",
                max_length=1000,
                allow_empty=True,
            )
        for field_name in ("tokens_prompt", "tokens_completion", "duration_ms"):
            value = getattr(self, field_name)
            if value is not None and (not isinstance(value, int) or value < 0):
                raise InteractionLogError(f"{field_name} must be a non-negative integer.")

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "InteractionLogEvent":
        """Load an event from a JSON-style dictionary."""

        if not isinstance(payload, dict):
            raise InteractionLogError("InteractionLogEvent payload must be a dictionary.")
        return cls(**_coerce_tuple_fields(payload, ("artifact_ids", "topics")))

    def write_json(self, path: str | Path) -> None:
        """Write this event as stable, human-readable JSON."""

        _write_json(path, self.to_dict())

    @classmethod
    def read_json(cls, path: str | Path) -> "InteractionLogEvent":
        """Read an event from JSON."""

        return cls.from_dict(_read_json(path))

    @classmethod
    def from_text(
        cls,
        *,
        event_id: str,
        episode_id: str,
        turn_id: int,
        created_at: str,
        event_type: str,
        role: str,
        actor: str,
        summary: str,
        request_text: str | None = None,
        response_text: str | None = None,
        **kwargs: Any,
    ) -> "InteractionLogEvent":
        """Create an event while hashing raw request/response text instead of storing it."""

        request_text_hash = _sha256_text(request_text) if request_text is not None else None
        response_text_hash = _sha256_text(response_text) if response_text is not None else None
        return cls(
            event_id=event_id,
            episode_id=episode_id,
            turn_id=turn_id,
            created_at=created_at,
            event_type=event_type,
            role=role,
            actor=actor,
            summary=summary,
            request_text_hash=request_text_hash,
            response_text_hash=response_text_hash,
            **kwargs,
        )


@dataclass(frozen=True)
class EpisodeL1Summary:
    """Summary of a bounded episode window.

    This object is deliberately edge-compatible but not graph-persistent.
    ``future_edge_seed_records`` exposes deterministic, non-authoritative edge
    seeds that a later WarrantEdge/MemoryEdge implementation can lift into
    real graph records.
    """

    l1_id: str
    episode_id: str
    created_at: str
    summary_version: str
    summary_text: str
    source_event_ids: tuple[str, ...]
    citations: tuple[str, ...]
    key_decisions: tuple[str, ...] = field(default_factory=tuple)
    completed_work: tuple[str, ...] = field(default_factory=tuple)
    open_questions: tuple[str, ...] = field(default_factory=tuple)
    risks: tuple[str, ...] = field(default_factory=tuple)
    next_actions: tuple[str, ...] = field(default_factory=tuple)
    topics: tuple[str, ...] = field(default_factory=tuple)
    scope: str = "default"
    generation_model: str | None = None
    generation_prompt_id: str | None = None
    coverage_score: float = 0.0
    freshness_state: str = "unknown"
    ttl_until: str | None = None
    namespace: str = "public"
    access_level: str = "public"
    redaction_level: str = "none"
    content_hash: str | None = None

    def __post_init__(self) -> None:
        _validate_id(self.l1_id, "l1_id")
        _validate_id(self.episode_id, "episode_id")
        _validate_iso_datetime(self.created_at, "created_at")
        _validate_short_text(self.summary_version, "summary_version", max_length=64)
        _validate_short_text(self.summary_text, "summary_text", max_length=5000)
        object.__setattr__(
            self,
            "source_event_ids",
            _as_tuple(self.source_event_ids, "source_event_ids"),
        )
        if not self.source_event_ids:
            raise InteractionLogError("source_event_ids must not be empty.")

        object.__setattr__(self, "citations", _as_tuple(self.citations, "citations"))
        for citation in self.citations:
            try:
                parse_citation(citation)
            except CitationError as exc:
                raise InteractionLogError(f"Invalid citation: {citation}") from exc

        for field_name in (
            "key_decisions",
            "completed_work",
            "open_questions",
            "risks",
            "next_actions",
            "topics",
        ):
            object.__setattr__(self, field_name, _as_tuple(getattr(self, field_name), field_name))

        _validate_short_text(self.scope, "scope", max_length=128)
        _validate_optional_id(self.generation_prompt_id, "generation_prompt_id")
        if self.generation_model is not None:
            _validate_short_text(self.generation_model, "generation_model", max_length=128)
        if not isinstance(self.coverage_score, (int, float)):
            raise InteractionLogError("coverage_score must be a number.")
        if not 0.0 <= float(self.coverage_score) <= 1.0:
            raise InteractionLogError("coverage_score must be between 0 and 1.")
        object.__setattr__(self, "coverage_score", float(self.coverage_score))
        if self.freshness_state not in VALID_FRESHNESS_STATES:
            raise InteractionLogError(
                f"freshness_state must be one of {sorted(VALID_FRESHNESS_STATES)}."
            )
        _validate_optional_iso_datetime(self.ttl_until, "ttl_until")
        _validate_short_text(self.namespace, "namespace", max_length=128)
        if self.access_level not in VALID_ACCESS_LEVELS:
            raise InteractionLogError(
                f"access_level must be one of {sorted(VALID_ACCESS_LEVELS)}."
            )
        if self.redaction_level not in VALID_REDACTION_LEVELS:
            raise InteractionLogError(
                f"redaction_level must be one of {sorted(VALID_REDACTION_LEVELS)}."
            )
        _validate_optional_hash(self.content_hash, "content_hash")

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "EpisodeL1Summary":
        """Load an L1 summary from a JSON-style dictionary."""

        if not isinstance(payload, dict):
            raise InteractionLogError("EpisodeL1Summary payload must be a dictionary.")
        return cls(
            **_coerce_tuple_fields(
                payload,
                (
                    "source_event_ids",
                    "citations",
                    "key_decisions",
                    "completed_work",
                    "open_questions",
                    "risks",
                    "next_actions",
                    "topics",
                ),
            )
        )

    def write_json(self, path: str | Path) -> None:
        """Write this L1 summary as stable, human-readable JSON."""

        _write_json(path, self.to_dict())

    @classmethod
    def read_json(cls, path: str | Path) -> "EpisodeL1Summary":
        """Read an L1 summary from JSON."""

        return cls.from_dict(_read_json(path))

    def stable_content_hash(self) -> str:
        """Return a deterministic content hash for idempotent refresh checks."""

        payload = "\n".join(
            [
                self.episode_id,
                self.summary_version,
                self.summary_text,
                "\n".join(self.source_event_ids),
                "\n".join(self.citations),
                "\n".join(self.key_decisions),
                "\n".join(self.completed_work),
                "\n".join(self.open_questions),
                "\n".join(self.risks),
                "\n".join(self.next_actions),
                self.scope,
                self.namespace,
                self.access_level,
                self.redaction_level,
            ]
        )
        return _sha256_text(payload)

    def future_edge_seed_records(self) -> tuple[dict[str, str], ...]:
        """Return deterministic seed records for later graph-edge lifting.

        These are intentionally not WarrantEdge records. They are a bridge:
        they preserve source-event and citation mappings so a future edge layer
        can create proper DERIVED_FROM / CITES records without reparsing prose.
        """

        seeds: list[dict[str, str]] = []
        for event_id in self.source_event_ids:
            seeds.append(
                {
                    "source_id": self.l1_id,
                    "predicate": "derived_from",
                    "target_id": event_id,
                }
            )
        for citation in self.citations:
            seeds.append(
                {
                    "source_id": self.l1_id,
                    "predicate": "cites",
                    "target_id": citation,
                }
            )
        return tuple(seeds)
