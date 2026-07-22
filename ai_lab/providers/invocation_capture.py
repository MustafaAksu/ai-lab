"""Invocation capture for the provider-comparison path (ABS-0004 Slice A).

Admitted by WARR-20260722-0001. This module is the only caller-facing
capture surface, and it is restricted to scripts/compare_providers.py
(warrant condition 1). scripts/ask_provider.py must not import it.

Capture failure is reported and never fatal: a provider call whose record
cannot be written still returns its result (plan constraint 3, warrant
condition 3).
"""

from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path
from typing import Any, Mapping, Sequence

from ai_lab.providers.invocation_record import (
    ATTESTATION_PARTIAL,
    CAPTURE_PATH_COMPARE_PROVIDERS,
    EXECUTOR_KIND_MODEL,
    IDENTITY_UNRESOLVED,
    SESSION_EXPLICIT_REPLAYED,
    SESSION_STATELESS,
    STATUS_FAILURE,
    STATUS_SUCCESS,
    build_invocation_record,
    invocation_relations,
    write_invocation_record,
)


ENDPOINTS = {
    "OpenAI": "openai.responses",
    "Claude": "anthropic.messages",
}


def new_session_id() -> str:
    """One session per comparison run.

    Slice A records session identity, not mode alone (warrant condition 5);
    the identity is a field, not a Run or ProtocolRound object, which remain
    deferred per ABS-0004 Section 11.
    """

    return "SESSION-" + uuid.uuid4().hex[:16]


def session_state_mode_for_run(has_context_pack: bool) -> str:
    """Observed, not assumed.

    This path replays its entire input explicitly on every call and holds no
    provider-managed thread, so the mode is stateless without a context pack
    and explicit_replayed_context with one.
    """

    return SESSION_EXPLICIT_REPLAYED if has_context_pack else SESSION_STATELESS


def execution_profile_inputs(provider: Any) -> dict[str, Any]:
    """Read the execution configuration actually in effect for this call."""

    sampling: dict[str, Any] = {}
    reasoning: dict[str, Any] = {}
    flags: dict[str, Any] = {}

    effort = getattr(provider, "_effort", None) or getattr(
        provider, "_reasoning_effort", None
    )
    if effort:
        reasoning["effort"] = effort

    limit = getattr(provider, "_max_tokens", None)
    if isinstance(limit, bool) or not isinstance(limit, int):
        limit = None

    if limit is not None:
        flags["max_tokens_source"] = (
            "environment"
            if os.getenv("AI_LAB_CLAUDE_MAX_TOKENS")
            else "settings_default"
        )

    return {
        "output_token_limit": limit,
        "sampling_parameters": sampling,
        "reasoning_parameters": reasoning,
        "provider_request_flags": flags,
    }


def capture_provider_invocation(
    *,
    repo_root: Path,
    provider: Any,
    rendered_prompt: str,
    session_id: str,
    session_state_mode: str,
    occurred_at: str,
    status: str,
    context_manifest_reference: str | None = None,
    spawned: Sequence[str] | None = None,
) -> tuple[Mapping[str, Any] | None, str | None]:
    """Build and write one InvocationRecord.

    Returns (record, error_message). On failure the record is None and the
    error message is populated; the caller reports it and continues.
    """

    try:
        profile_inputs = execution_profile_inputs(provider)
        record = build_invocation_record(
            capture_path=CAPTURE_PATH_COMPARE_PROVIDERS,
            executor_kind=EXECUTOR_KIND_MODEL,
            executor_reference=getattr(provider, "model", "unknown"),
            identity_verification_status=IDENTITY_UNRESOLVED,
            requested_model_name=getattr(provider, "model", "unknown"),
            service_endpoint=ENDPOINTS.get(
                getattr(provider, "name", ""), "unknown_endpoint"
            ),
            session_id=session_id,
            occurred_at=occurred_at,
            rendered_prompt=rendered_prompt,
            session_state_mode=session_state_mode,
            completeness_attestation=ATTESTATION_PARTIAL,
            status=status,
            context_manifest_reference=context_manifest_reference,
            spawned=spawned,
            **profile_inputs,
        )
        write_invocation_record(record, repo_root)
        return record, None
    except Exception as error:  # capture must never break the call path
        return None, f"{type(error).__name__}: {error}"


def report_capture_failure(provider_name: str, message: str) -> None:
    """Report a capture failure without swallowing it and without aborting."""

    print(
        f"WARNING: invocation capture failed for {provider_name}: {message}",
        file=sys.stderr,
    )


def produced_by_references(records: Sequence[Mapping[str, Any]], artifact_id: str) -> list[dict[str, Any]]:
    """produced_by relations from a comparison artifact to its invocations."""

    references: list[dict[str, Any]] = []
    for record in records:
        for relation in invocation_relations(record, produced_artifact_id=artifact_id):
            if relation.predicate == "produced_by":
                references.append(
                    {
                        "source_id": relation.source_id,
                        "predicate": relation.predicate,
                        "target_id": relation.target_id,
                        "relation_source": relation.relation_source,
                        "authoritative": relation.authoritative,
                        "scope": relation.scope,
                        "evidence": relation.evidence,
                    }
                )
    return references
