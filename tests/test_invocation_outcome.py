"""Outcome capture for GAP-0006.

The defect: ClaudeProvider.ask() returned str, so stop_reason and usage were
discarded inside the adapter. A response with one empty thinking block and a
response with a complete answer both reached the capture path as text, and
both were recorded status=success. INV-b59b93ec9cd8dbe6 is field-identical on
status, governance_marker, execution_profile and spawned to INV-c9fecfbf0964c1d2,
which produced a complete review.

These tests are written as the falsifying cases first, per GAP-0007: each one
constructs input the capture should reject or distinguish, and asserts it does.
"""

from __future__ import annotations

import pytest

from ai_lab.providers.invocation_capture import outcome_block
from ai_lab.providers.invocation_record import (
    InvocationRecordError,
    build_invocation_record,
    invocation_id_for,
    validate_invocation_record,
)
from ai_lab.providers.provider import ProviderOutcome

BASE = dict(
    capture_path="scripts/compare_providers.py",
    executor_kind="model",
    executor_reference="claude-sonnet-5",
    identity_verification_status="unresolved",
    requested_model_name="claude-sonnet-5",
    service_endpoint="anthropic.messages",
    session_id="s-1",
    occurred_at="2026-07-27T00:00:00+00:00",
    rendered_prompt="prompt",
    session_state_mode="stateless",
    completeness_attestation="partial_declared_channels_only",
    status="success",
)

# The two responses that were indistinguishable before this change.
TRUNCATED = ProviderOutcome(
    text="",
    stop_reason="max_tokens",
    stop_reason_field="stop_reason",
    input_tokens=12496,
    output_tokens=16000,
    content_block_types=["thinking"],
)
COMPLETE = ProviderOutcome(
    text="Here is the review.",
    stop_reason="end_turn",
    stop_reason_field="stop_reason",
    input_tokens=12496,
    output_tokens=4900,
    content_block_types=["thinking", "text"],
)


def test_budget_exhaustion_is_distinguishable_from_a_complete_response():
    """The COMP-0038 case. Both are status=success; the outcome separates them."""

    truncated = build_invocation_record(**BASE, outcome=outcome_block(TRUNCATED))
    complete = build_invocation_record(**BASE, outcome=outcome_block(COMPLETE))

    assert truncated["status"] == complete["status"] == "success"
    assert truncated["outcome"] != complete["outcome"]
    assert truncated["outcome"]["stop_reason"] == "max_tokens"
    assert truncated["outcome"]["text_chars"] == 0
    assert truncated["outcome"]["content_block_types"] == ["thinking"]
    assert complete["outcome"]["stop_reason"] == "end_turn"
    assert complete["outcome"]["text_chars"] > 0


def test_outcome_does_not_change_the_invocation_id():
    """Additive means additive: no stored record's identity may shift."""

    without = build_invocation_record(**BASE)
    with_outcome = build_invocation_record(**BASE, outcome=outcome_block(TRUNCATED))
    assert without["invocation_id"] == with_outcome["invocation_id"]
    assert invocation_id_for(with_outcome) == with_outcome["invocation_id"]


def test_a_record_without_an_outcome_is_still_valid():
    """The 182 records captured before this change lack the block, accurately."""

    record = build_invocation_record(**BASE)
    assert "outcome" not in record
    validate_invocation_record(record)


def test_absent_outcome_is_recorded_as_absent_not_as_nulls():
    """A provider that reports nothing yields no block, not a block of nulls.

    A block of nulls would read as capture. Absence says the outcome was not
    captured, which is what happened.
    """

    assert outcome_block(None) is None


def test_partial_outcome_is_rejected():
    """A block missing fields would not say which parts were captured."""

    partial = dict(outcome_block(TRUNCATED))
    del partial["output_tokens"]
    with pytest.raises(InvocationRecordError, match="missing fields"):
        build_invocation_record(**BASE, outcome=partial)


def test_unknown_outcome_field_is_rejected():
    bad = dict(outcome_block(TRUNCATED))
    bad["provider_note"] = "anything"
    with pytest.raises(InvocationRecordError, match="unknown fields"):
        build_invocation_record(**BASE, outcome=bad)


@pytest.mark.parametrize("field", ["input_tokens", "output_tokens", "text_chars"])
def test_negative_token_counts_are_rejected(field):
    bad = dict(outcome_block(TRUNCATED))
    bad[field] = -1
    with pytest.raises(InvocationRecordError, match="non-negative integer"):
        build_invocation_record(**BASE, outcome=bad)


def test_text_chars_may_not_be_null():
    """The capture path always knows how much text it received."""

    bad = dict(outcome_block(TRUNCATED))
    bad["text_chars"] = None
    with pytest.raises(InvocationRecordError, match="text_chars must be an integer"):
        build_invocation_record(**BASE, outcome=bad)


def test_stop_reason_without_its_source_field_is_rejected():
    """The two providers report different fields; an unsourced value hides which."""

    bad = dict(outcome_block(TRUNCATED))
    bad["stop_reason_field"] = None
    with pytest.raises(InvocationRecordError, match="stop_reason_field must name"):
        build_invocation_record(**BASE, outcome=bad)


def test_block_types_must_be_strings():
    bad = dict(outcome_block(TRUNCATED))
    bad["content_block_types"] = ["thinking", 7]
    with pytest.raises(InvocationRecordError, match="list of non-empty strings"):
        build_invocation_record(**BASE, outcome=bad)


def test_provider_stop_reasons_are_not_normalised_across_providers():
    """Anthropic reports stop_reason; the Responses API reports status or
    incomplete_details.reason. Mapping them onto one vocabulary would assert an
    equivalence neither provider states, so the source field is recorded."""

    openai_like = ProviderOutcome(
        text="",
        stop_reason="max_output_tokens",
        stop_reason_field="incomplete_details.reason",
        input_tokens=12496,
        output_tokens=16000,
        content_block_types=["reasoning"],
    )
    record = build_invocation_record(**BASE, outcome=outcome_block(openai_like))
    assert record["outcome"]["stop_reason"] == "max_output_tokens"
    assert record["outcome"]["stop_reason_field"] == "incomplete_details.reason"
