from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
import re


class ContextPackError(ValueError):
    """Raised when a context pack manifest is malformed or invalid."""


VALID_CONTEXT_ITEM_TYPES = {
    "artifact_summary",
    "l0_summary",
    "chunk_reference",
    "raw_chunk",
    "raw_artifact",
    "abstraction",
    "synthesis",
    "comparison",
    "episode_l1",
}

VALID_ASSEMBLY_POLICIES = {
    "manual",
    "latest_context",
    "lineage",
    "semantic",
    "hybrid",
}

VALID_EXCLUSION_REASONS = {
    "duplicate",
    "low_relevance",
    "stale",
    "too_large",
    "redacted",
    "policy",
    "superseded",
}

VALID_ADMISSION_DECISIONS = {
    "admit",
    "admit_with_warning",
    "exclude",
}

VALID_FRESHNESS_STATES = {
    "fresh",
    "stale",
    "unknown",
}

VALID_WARRANT_STATES = {
    "supported",
    "disputed",
    "unreviewed",
    "superseded",
    "rejected",
}


def utc_now_iso() -> str:
    """Return current UTC time in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def _validate_identifier(value: str, field_name: str) -> None:
    if not re.fullmatch(r"[A-Za-z0-9._:/@|+-]+", value):
        raise ContextPackError(f"{field_name} contains unsupported characters.")


def _validate_short_text(value: str, field_name: str, max_length: int = 500) -> None:
    if not value.strip():
        raise ContextPackError(f"{field_name} must not be empty.")

    if len(value) > max_length:
        raise ContextPackError(f"{field_name} must be <= {max_length} characters.")


def _validate_task_label(value: str, field_name: str = "task_label") -> None:
    _validate_short_text(value, field_name, max_length=120)

    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise ContextPackError(f"{field_name} must be lowercase kebab-case.")


def _validate_sha256_hex(value: str, field_name: str) -> None:
    if not re.fullmatch(r"[a-f0-9]{64}", value):
        raise ContextPackError(f"{field_name} must be a lowercase SHA-256 hex digest.")


def _validate_telemetry_counts(
    value: dict[str, int],
    field_name: str,
) -> None:
    for key, count in value.items():
        if not re.fullmatch(r"[a-z][a-z0-9_]*", key):
            raise ContextPackError(f"{field_name} contains an unsupported key.")

        if not isinstance(count, int) or count < 0:
            raise ContextPackError(f"{field_name} counts must be non-negative integers.")


def compute_manifest_id(
    task: str,
    assembly_policy: str,
    item_ids: tuple[str, ...],
) -> str:
    """Compute a deterministic manifest ID from task, policy, and selected item IDs."""
    payload = "|".join((task.strip(), assembly_policy, *item_ids))
    return sha256(payload.encode("utf-8")).hexdigest()[:16]


@dataclass(frozen=True)
class ContextPackItem:
    """One selected item inside a context pack."""

    item_type: str
    item_id: str
    reason: str
    relevance_score: float
    token_estimate: int = 0
    source_path: str | None = None
    citation: str | None = None
    admission_verdict_id: str | None = None
    admission_decision: str | None = None
    freshness_state: str | None = None
    warrant_state: str | None = None

    def __post_init__(self) -> None:
        if self.item_type not in VALID_CONTEXT_ITEM_TYPES:
            raise ContextPackError(f"Unsupported context item type: {self.item_type}")

        _validate_identifier(self.item_id, "item_id")
        _validate_short_text(self.reason, "reason", max_length=240)

        if not (0 <= self.relevance_score <= 1):
            raise ContextPackError("relevance_score must be between 0 and 1.")

        if self.token_estimate < 0:
            raise ContextPackError("token_estimate must be >= 0.")

        if self.source_path:
            _validate_identifier(self.source_path, "source_path")

        if self.citation:
            _validate_identifier(self.citation, "citation")

        if self.admission_verdict_id:
            _validate_identifier(self.admission_verdict_id, "admission_verdict_id")

        if self.admission_decision and self.admission_decision not in VALID_ADMISSION_DECISIONS:
            raise ContextPackError("Unsupported admission_decision.")

        if self.freshness_state and self.freshness_state not in VALID_FRESHNESS_STATES:
            raise ContextPackError("Unsupported freshness_state.")

        if self.warrant_state and self.warrant_state not in VALID_WARRANT_STATES:
            raise ContextPackError("Unsupported warrant_state.")

    def to_dict(self) -> dict[str, object]:
        """Serialize the context item into a JSON-compatible dictionary."""
        data: dict[str, object] = {
            "item_type": self.item_type,
            "item_id": self.item_id,
            "reason": self.reason,
            "relevance_score": self.relevance_score,
            "token_estimate": self.token_estimate,
        }

        if self.source_path:
            data["source_path"] = self.source_path

        if self.citation:
            data["citation"] = self.citation

        if self.admission_verdict_id:
            data["admission_verdict_id"] = self.admission_verdict_id

        if self.admission_decision:
            data["admission_decision"] = self.admission_decision

        if self.freshness_state:
            data["freshness_state"] = self.freshness_state

        if self.warrant_state:
            data["warrant_state"] = self.warrant_state

        return data


@dataclass(frozen=True)
class ContextPackExclusion:
    """One candidate item excluded from a context pack."""

    item_id: str
    reason: str
    note: str | None = None

    def __post_init__(self) -> None:
        _validate_identifier(self.item_id, "exclusion.item_id")

        if self.reason not in VALID_EXCLUSION_REASONS:
            raise ContextPackError(f"Unsupported exclusion reason: {self.reason}")

        if self.note:
            _validate_short_text(self.note, "exclusion.note", max_length=240)

    def to_dict(self) -> dict[str, object]:
        """Serialize the exclusion into a JSON-compatible dictionary."""
        data: dict[str, object] = {
            "item_id": self.item_id,
            "reason": self.reason,
        }

        if self.note:
            data["note"] = self.note

        return data


@dataclass(frozen=True)
class ContextPackManifest:
    """
    Manifest describing the exact context selected for one task.

    This is the bridge between memory retrieval and prompt construction.
    """

    task: str
    assembly_policy: str
    items: tuple[ContextPackItem, ...]
    manifest_id: str | None = None
    token_budget: int | None = None
    exclusions: tuple[ContextPackExclusion, ...] = field(default_factory=tuple)
    created_at: str = field(default_factory=utc_now_iso)
    model_target: str | None = None
    pipeline_run_id: str | None = None
    task_label: str | None = None
    full_prompt_hash: str | None = None
    admission_summary: dict[str, int] | None = None

    def __post_init__(self) -> None:
        _validate_short_text(self.task, "task", max_length=500)

        if self.assembly_policy not in VALID_ASSEMBLY_POLICIES:
            raise ContextPackError(f"Unsupported assembly policy: {self.assembly_policy}")

        if not self.items:
            raise ContextPackError("Context pack must contain at least one item.")

        if self.token_budget is not None and self.token_budget < 0:
            raise ContextPackError("token_budget must be >= 0.")

        if self.model_target:
            _validate_identifier(self.model_target, "model_target")

        if self.pipeline_run_id:
            _validate_identifier(self.pipeline_run_id, "pipeline_run_id")

        if self.task_label:
            _validate_task_label(self.task_label)

        if self.full_prompt_hash:
            _validate_sha256_hex(self.full_prompt_hash, "full_prompt_hash")

        if self.admission_summary is not None:
            _validate_telemetry_counts(self.admission_summary, "admission_summary")

        expected_manifest_id = compute_manifest_id(
            task=self.task,
            assembly_policy=self.assembly_policy,
            item_ids=tuple(item.item_id for item in self.items),
        )

        if self.manifest_id is not None and self.manifest_id != expected_manifest_id:
            raise ContextPackError("manifest_id does not match task/policy/items.")

        object.__setattr__(self, "manifest_id", expected_manifest_id)

    @property
    def total_token_estimate(self) -> int:
        """Return the total estimated token cost of selected items."""
        return sum(item.token_estimate for item in self.items)

    def to_dict(self) -> dict[str, object]:
        """Serialize the manifest into a JSON-compatible dictionary."""
        data: dict[str, object] = {
            "manifest_id": self.manifest_id,
            "task": self.task,
            "assembly_policy": self.assembly_policy,
            "items": [item.to_dict() for item in self.items],
            "exclusions": [exclusion.to_dict() for exclusion in self.exclusions],
            "total_token_estimate": self.total_token_estimate,
            "created_at": self.created_at,
        }

        if self.token_budget is not None:
            data["token_budget"] = self.token_budget

        if self.model_target:
            data["model_target"] = self.model_target

        if self.task_label:
            data["task_label"] = self.task_label

        if self.full_prompt_hash:
            data["full_prompt_hash"] = self.full_prompt_hash

        if self.admission_summary is not None:
            data["admission_summary"] = dict(self.admission_summary)

        if self.pipeline_run_id:
            data["provenance"] = {
                "pipeline_run_id": self.pipeline_run_id,
            }

        return data
