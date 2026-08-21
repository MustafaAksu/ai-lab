"""Invocation output binding and produced_by establishment.

PLAN-20260817-0002 under WARR-20260820-0001. One primitive and one relation:

  - output_text_digest: "sha256:" + hex over the UTF-8 bytes of exactly the
    provider's textual output, computed by the capture path from the same
    value the comparison artifact incorporates.
  - evaluate_produced_by: establishes an artifact-to-invocation produced_by
    relation by recomputation, or returns unresolved with an enumerated
    reason. It never reads a seed's authoritative flag and never selects
    among ambiguous candidates.

    Direction, per the predicate registry: the artifact is the source and
    the invocation is the target — COMP produced_by INV means the artifact
    was produced by that invocation. Invocation-to-artifact ancestry is the
    registered inverse, produces, and is not emitted here. The admitted
    plan and warrant used the shorthand "invocation-to-artifact
    produced_by"; that wording error is recorded in the completion
    verification rather than silently rewritten in admitted records.

The parser is fence-aware: content inside a fenced block is response bytes
and is never read as a section heading, metadata line, or seed, so provider
output that mimics the artifact's framing round-trips as content
(STRUCTURAL MARKER IN OUTPUT). A section is attributable only through a
retained `- invocation_id:` metadata line appearing before the section's
fence; the provider heading and model line are display and consistency
metadata and are not read for attribution.

Refusal reasons, exactly one per distinct failure (P5: absent evidence is
an enumerated unresolved, never an empty result):

  invalid_invocation_record      the record fails the canonical
                                 InvocationRecord validator; establishment
                                 requires a record the repository itself
                                 accepts (completion-review finding: the
                                 v2 evaluator established a stripped
                                 record the validator rejects)
  no_outcome_block               record carries no outcome block
  outcome_without_output_digest  outcome present, digest absent
  seed_not_found                 artifact has no seed asserting exactly
                                 (this artifact, produced_by, this record);
                                 a seed naming a different source artifact
                                 does not count (completion-review finding:
                                 the v2 evaluator accepted a foreign
                                 source_id)
  artifact_identity_not_found    the artifact carries no parseable
                                 comparison_id, so the seed's source
                                 cannot be checked against it
  invalid_seed_metadata          a seed metadata line is not valid JSON
                                 (e.g. the one legacy Python-repr
                                 serialization)
  attributed_section_not_found   no parseable section carries the record's
                                 invocation_id
  ambiguous_attribution          more than one section carries it, or the
                                 artifact's framing cannot be parsed
                                 unambiguously
  digest_mismatch                the extracted bytes do not recompute to
                                 the retained digest
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Mapping

DIGEST_PREFIX = "sha256:"
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")

_HEADING_RE = re.compile(r"^## (?P<name>.+) Response$")
_FENCE_RE = re.compile(r"^(?P<fence>`{3,})$")
_INVOCATION_LINE_RE = re.compile(r"^- invocation_id: `(?P<id>[^`]+)`$")
_SEED_LINE_RE = re.compile(r"^- invocation_produced_by: `(?P<json>.*)`$")
_COMPARISON_ID_RE = re.compile(r"^- comparison_id: `(?P<id>[^`]+)`$")

REASON_INVALID_RECORD = "invalid_invocation_record"
REASON_NO_OUTCOME = "no_outcome_block"
REASON_NO_DIGEST = "outcome_without_output_digest"
REASON_NO_SEED = "seed_not_found"
REASON_NO_ARTIFACT_ID = "artifact_identity_not_found"
REASON_BAD_SEED = "invalid_seed_metadata"
REASON_NO_SECTION = "attributed_section_not_found"
REASON_AMBIGUOUS = "ambiguous_attribution"
REASON_MISMATCH = "digest_mismatch"


def output_text_digest(text: str) -> str:
    """Digest of exactly ``text``: no normalization, no stripping.

    The capture path calls this on the same value the artifact incorporates
    (plan constraint: single source). The evaluator calls it on the exact
    extracted bytes. Any transformation between the two is the prohibited
    failure mode the EXACT TEXT ROUND-TRIP criterion falsifies.
    """

    return DIGEST_PREFIX + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _parse_sections(artifact_text: str) -> list[dict[str, Any]] | None:
    """Fence-aware parse of response sections.

    Returns a list of {"invocation_id": str | None, "body": str | None},
    one per top-level ``## <name> Response`` heading, or None when the
    framing cannot be parsed unambiguously (an unterminated fence).

    Inside a fence, every line is content: headings, metadata lines and
    seed lines are only recognised at top level. A fence opens with a line
    that is exactly three or more backticks and closes only with a line
    that is exactly the same backtick string.
    """

    lines = artifact_text.split("\n")
    sections: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    body_lines: list[str] | None = None
    fence: str | None = None

    for line in lines:
        if fence is not None:
            if line == fence:
                # Fence closes. The body is everything between, exactly.
                if current is not None and current["body"] is None:
                    current["body"] = "\n".join(body_lines or [])
                fence = None
                body_lines = None
            elif body_lines is not None:
                body_lines.append(line)
            continue

        fence_match = _FENCE_RE.match(line)
        if fence_match:
            fence = fence_match.group("fence")
            # Only the first fenced block of a section is its response body.
            body_lines = [] if (current is not None and current["body"] is None) else None
            continue

        heading = _HEADING_RE.match(line)
        if heading:
            current = {"invocation_id": None, "body": None}
            sections.append(current)
            continue

        if current is not None and current["body"] is None:
            invocation = _INVOCATION_LINE_RE.match(line)
            if invocation:
                if current["invocation_id"] is not None:
                    # Two invocation_id lines in one section: conflicting.
                    current["invocation_id"] = _CONFLICT
                else:
                    current["invocation_id"] = invocation.group("id")

    if fence is not None:
        # Unterminated fence: the framing failed to contain its content and
        # nothing after the break can be attributed unambiguously.
        return None
    return sections


_CONFLICT = object()


class _SeedParseError(Exception):
    """Seed metadata exists but is not valid JSON (invalid_seed_metadata)."""


def _parse_artifact_identity(artifact_text: str) -> str | None:
    """The artifact's retained comparison_id, or None when absent."""

    lines = artifact_text.split("\n")
    fence: str | None = None
    for line in lines:
        if fence is not None:
            if line == fence:
                fence = None
            continue
        fence_match = _FENCE_RE.match(line)
        if fence_match:
            fence = fence_match.group("fence")
            continue
        ident = _COMPARISON_ID_RE.match(line)
        if ident:
            return ident.group("id")
    return None


def _parse_seeds(artifact_text: str) -> list[tuple[str, str]] | None:
    """(source_id, target_id) pairs of produced_by seeds in the metadata.

    Fence-aware for the same reason as section parsing. Returns None when
    the framing is unparseable (unterminated fence), [] when no seed line
    exists, and raises _SeedParseError when a seed line is present but is
    not valid JSON (the one legacy Python-repr serialization is this case).

    The full pair is returned because the seed asserts a whole relation:
    (artifact, produced_by, invocation). The v1 evaluator read source_id
    where the invocation lives in target_id (exposed by the deliberate
    run); the v2 evaluator matched target_id alone, so a seed copied from
    another artifact could establish this one (exposed by the completion
    review). The caller must check both ends.
    """

    lines = artifact_text.split("\n")
    fence: str | None = None
    pairs: list[tuple[str, str]] = []
    found = False

    for line in lines:
        if fence is not None:
            if line == fence:
                fence = None
            continue
        fence_match = _FENCE_RE.match(line)
        if fence_match:
            fence = fence_match.group("fence")
            continue
        seed = _SEED_LINE_RE.match(line)
        if seed:
            found = True
            try:
                payload = json.loads(seed.group("json"))
            except json.JSONDecodeError:
                raise _SeedParseError()
            if isinstance(payload, list):
                for item in payload:
                    if (
                        isinstance(item, Mapping)
                        and item.get("predicate") == "produced_by"
                        and isinstance(item.get("source_id"), str)
                        and isinstance(item.get("target_id"), str)
                    ):
                        pairs.append((item["source_id"], item["target_id"]))

    if fence is not None:
        return None
    return pairs if (found or pairs) else []


def _unresolved(invocation_id: str, reason: str) -> dict[str, Any]:
    return {"status": "unresolved", "reason": reason, "invocation_id": invocation_id}


def evaluate_produced_by(
    artifact_text: str, record: Mapping[str, Any]
) -> dict[str, Any]:
    """Establish record --produced_by--> artifact by recomputation, or refuse.

    Check order: record evidence, then seed, then attribution, then digest.
    Each guard is a named function below so mutation tests can replace it
    and demonstrate it is load-bearing.
    """

    invocation_id = str(record.get("invocation_id", ""))

    reason = _record_validation_guard(record)
    if reason is not None:
        return _unresolved(invocation_id, reason)

    reason = _record_evidence_guard(record)
    if reason is not None:
        return _unresolved(invocation_id, reason)

    reason = _seed_guard(artifact_text, invocation_id)
    if reason is not None:
        return _unresolved(invocation_id, reason)

    body, reason = _attribution_guard(artifact_text, invocation_id)
    if reason is not None:
        return _unresolved(invocation_id, reason)

    reason = _digest_guard(body, record)
    if reason is not None:
        return _unresolved(invocation_id, reason)

    return {"status": "established", "reason": None, "invocation_id": invocation_id}


def _record_validation_guard(record: Mapping[str, Any]) -> str | None:
    """The record must pass the canonical InvocationRecord validator.

    Completion-review finding: the v2 evaluator established a record
    stripped to invocation_id and outcome, which the repository's own
    validator rejects. Establishment requires a record the repository
    accepts, checked by invoking the canonical validator rather than
    reproducing a subset of its rules here.
    """

    from ai_lab.providers.invocation_record import (
        InvocationRecordError,
        validate_invocation_record,
    )

    try:
        validate_invocation_record(record)
    except InvocationRecordError:
        return REASON_INVALID_RECORD
    return None


def _record_evidence_guard(record: Mapping[str, Any]) -> str | None:
    """The record must carry an outcome block with a well-formed digest."""

    outcome = record.get("outcome")
    if not isinstance(outcome, Mapping):
        return REASON_NO_OUTCOME
    digest = outcome.get("output_text_digest")
    if not isinstance(digest, str) or not DIGEST_RE.match(digest):
        return REASON_NO_DIGEST
    return None


def _seed_guard(artifact_text: str, invocation_id: str) -> str | None:
    """The artifact must seed exactly (this artifact, produced_by, record).

    The whole candidate relation is checked: the seed's source_id must be
    the artifact's own retained comparison_id and its target_id must be
    the record. A seed copied from another artifact establishes nothing
    (completion-review finding). The seed names the candidate to check;
    its authoritative flag is not read anywhere in this module.
    """

    artifact_id = _parse_artifact_identity(artifact_text)
    if artifact_id is None:
        return REASON_NO_ARTIFACT_ID
    try:
        seeds = _parse_seeds(artifact_text)
    except _SeedParseError:
        return REASON_BAD_SEED
    if seeds is None:
        return REASON_AMBIGUOUS
    if (artifact_id, invocation_id) not in seeds:
        return REASON_NO_SEED
    return None


def _attribution_guard(
    artifact_text: str, invocation_id: str
) -> tuple[str | None, str | None]:
    """Exactly one parseable section must carry the record's invocation_id."""

    sections = _parse_sections(artifact_text)
    if sections is None:
        return None, REASON_AMBIGUOUS
    matches = [
        s
        for s in sections
        if s["invocation_id"] == invocation_id and s["body"] is not None
    ]
    if any(s["invocation_id"] is _CONFLICT for s in sections):
        return None, REASON_AMBIGUOUS
    if len(matches) > 1:
        return None, REASON_AMBIGUOUS
    if len(matches) == 0:
        return None, REASON_NO_SECTION
    return matches[0]["body"], None


def _digest_guard(body: str | None, record: Mapping[str, Any]) -> str | None:
    """The extracted bytes must recompute to the retained digest, exactly."""

    if body is None:
        return REASON_NO_SECTION
    retained = record["outcome"]["output_text_digest"]
    if output_text_digest(body) != retained:
        return REASON_MISMATCH
    return None
