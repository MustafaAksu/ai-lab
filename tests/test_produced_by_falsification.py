"""Falsification set for PLAN-20260817-0002 (WARR-20260820-0001).

Written BEFORE the implementation, per warrant condition 7. Every test here
encodes one success criterion of the admitted plan as a requirement on code
that does not yet exist. The tests define the contract:

  ai_lab/provenance/produced_by.py
    output_text_digest(text: str) -> str
        "sha256:" + hex digest of the UTF-8 bytes of exactly `text`.
    evaluate_produced_by(artifact_text: str, record: dict) -> dict
        Returns {"status": "established" | "unresolved",
                 "reason": None | <enumerated>,
                 "invocation_id": str}.
        Enumerated reasons, exactly one per distinct refusal:
          "no_outcome_block"            (criterion NO OUTCOME)
          "outcome_without_output_digest" (criterion OUTCOME WITHOUT DIGEST)
          "seed_not_found"              (artifact carries no produced_by seed
                                         naming the record)
          "attributed_section_not_found" (criterion WRONG ATTRIBUTION)
          "ambiguous_attribution"       (criterion AMBIGUOUS OR DUPLICATE,
                                         and the fail-closed branch of
                                         STRUCTURAL MARKER IN OUTPUT)
          "digest_mismatch"             (criterion DIGEST MISMATCH)

Artifact-side contract (implementation step in scripts/compare_providers.py):
  build_markdown_artifact writes, for each response whose data dict carries an
  "invocation_id" key, a retained line
      - invocation_id: `INV-...`
  inside that response section, before the fenced response body. Responses
  without the key render as today (historical format).

Mutation tests (final criterion) are added alongside the evaluator
implementation: they replace each guard with permissive behaviour and require
a test failure. They cannot precede the guards they mutate.

Digest field: record["outcome"]["output_text_digest"], "sha256:<hex>",
matching the existing rendered_prompt_digest convention. Optional in schema;
operationally required for new captures (criterion MISSING DIGEST ON NEW
CAPTURE is enforced in the capture-path tests added with the
compare_providers.py change, plus the completion gate).
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from compare_providers import build_markdown_artifact  # noqa: E402

produced_by = pytest.importorskip(
    "ai_lab.provenance.produced_by",
    reason="evaluator not implemented yet; this red skip is the pre-implementation state",
)
output_text_digest = produced_by.output_text_digest
evaluate_produced_by = produced_by.evaluate_produced_by


def sha256_hex(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def make_record(
    invocation_id: str = "INV-aaaaaaaaaaaaaaaa",
    *,
    outcome: dict | None | str = "default",
    digest_of: str | None = None,
) -> dict:
    """Minimal InvocationRecord stub carrying the fields the evaluator reads."""
    record = {
        "invocation_id": invocation_id,
        "executor": {"kind": "model", "reference": "claude-sonnet-5"},
    }
    if outcome == "default":
        outcome = {
            "stop_reason": "end_turn",
            "text_chars": 0,
            "content_block_types": ["text"],
        }
    if outcome is not None:
        record["outcome"] = dict(outcome)
        if digest_of is not None:
            record["outcome"]["output_text_digest"] = sha256_hex(digest_of)
            record["outcome"]["text_chars"] = len(digest_of)
    return record


def make_artifact(
    sections: list[tuple[str, str, str | None]],
    seeds: list[str] | None = None,
) -> str:
    """Build a real artifact via build_markdown_artifact.

    sections: (provider_name, response_text, invocation_id_or_None)
    seeds: invocation ids to place in the invocation_produced_by metadata.
    """
    responses = {}
    for provider, text, inv in sections:
        data = {"model": "claude-sonnet-5", "response": text}
        if inv is not None:
            data["invocation_id"] = inv
        responses[provider] = data
    extra = None
    if seeds is not None:
        extra = {
            "invocation_produced_by": [
                {
                    "invocation_id": inv,
                    "relation": "produced_by",
                    "relation_source": "future_edge_seed",
                    "authoritative": False,
                }
                for inv in seeds
            ]
        }
    return build_markdown_artifact(
        prompt="prompt",
        responses=responses,
        created_at="2026-08-20T00:00:00+00:00",
        command="test",
        comparison_id="COMP-9999",
        extra_metadata=extra,
    )


INV_A = "INV-aaaaaaaaaaaaaaaa"
INV_B = "INV-bbbbbbbbbbbbbbbb"


# --- POSITIVE -------------------------------------------------------------

def test_positive_establishes_relation():
    text = "The answer is 42.\n"
    art = make_artifact([("Claude", text, INV_A)], seeds=[INV_A])
    rec = make_record(INV_A, digest_of=text)
    result = evaluate_produced_by(art, rec)
    assert result["status"] == "established"
    assert result["reason"] is None


# --- NO OUTCOME / OUTCOME WITHOUT DIGEST ---------------------------------

def test_no_outcome_block_yields_unresolved():
    art = make_artifact([("Claude", "x", INV_A)], seeds=[INV_A])
    rec = make_record(INV_A, outcome=None)
    result = evaluate_produced_by(art, rec)
    assert result == {
        "status": "unresolved",
        "reason": "no_outcome_block",
        "invocation_id": INV_A,
    }


def test_outcome_without_digest_yields_distinct_reason():
    art = make_artifact([("Claude", "x", INV_A)], seeds=[INV_A])
    rec = make_record(INV_A)  # outcome present, no digest
    result = evaluate_produced_by(art, rec)
    assert result["status"] == "unresolved"
    assert result["reason"] == "outcome_without_output_digest"
    assert result["reason"] != "no_outcome_block"


# --- DIGEST MISMATCH / ALTERED RESPONSE ----------------------------------

def test_digest_mismatch_yields_unresolved():
    art = make_artifact([("Claude", "actual text", INV_A)], seeds=[INV_A])
    rec = make_record(INV_A, digest_of="asserted different text")
    result = evaluate_produced_by(art, rec)
    assert result["status"] == "unresolved"
    assert result["reason"] == "digest_mismatch"


def test_single_character_edit_breaks_establishment():
    text = "immutable evidence"
    art = make_artifact([("Claude", text, INV_A)], seeds=[INV_A])
    rec = make_record(INV_A, digest_of=text)
    assert evaluate_produced_by(art, rec)["status"] == "established"
    tampered = art.replace("immutable evidence", "immutable evidenze")
    assert evaluate_produced_by(tampered, rec)["status"] == "unresolved"


def test_length_agreement_alone_establishes_nothing():
    """The founding hazard: text_chars agrees, content differs."""
    text = "A" * 335
    imposter = "B" * 335
    art = make_artifact([("Claude", imposter, INV_A)], seeds=[INV_A])
    rec = make_record(INV_A, digest_of=text)  # text_chars == 335 on both
    result = evaluate_produced_by(art, rec)
    assert result["status"] == "unresolved"
    assert result["reason"] == "digest_mismatch"


# --- SEEDS ---------------------------------------------------------------

def test_seed_not_found_yields_unresolved():
    art = make_artifact([("Claude", "x", INV_A)], seeds=[])
    rec = make_record(INV_A, digest_of="x")
    result = evaluate_produced_by(art, rec)
    assert result["status"] == "unresolved"
    assert result["reason"] == "seed_not_found"


def test_seed_authoritative_flag_is_never_read():
    """SEED WITHOUT EVIDENCE: flipping authoritative to true changes nothing."""
    text = "y"
    art = make_artifact([("Claude", text, INV_A)], seeds=[INV_A])
    lied = art.replace('"authoritative": false', '"authoritative": true')
    assert lied != art, "fixture must actually contain the flag"
    rec_no_digest = make_record(INV_A)
    assert evaluate_produced_by(lied, rec_no_digest)["status"] == "unresolved"
    rec = make_record(INV_A, digest_of=text)
    assert (
        evaluate_produced_by(art, rec) == evaluate_produced_by(lied, rec)
    ), "authoritative flag must not influence the result in either direction"


# --- ATTRIBUTION ---------------------------------------------------------

def test_wrong_attribution_never_binds_to_present_section():
    art = make_artifact([("Claude", "content", INV_B)], seeds=[INV_A])
    rec = make_record(INV_A, digest_of="content")
    result = evaluate_produced_by(art, rec)
    assert result["status"] == "unresolved"
    assert result["reason"] == "attributed_section_not_found"


def test_duplicate_invocation_id_fails_closed():
    text = "same id twice"
    art = make_artifact(
        [("Claude", text, INV_A), ("OpenAI", text, INV_A)], seeds=[INV_A]
    )
    result = evaluate_produced_by(art, make_record(INV_A, digest_of=text))
    assert result["status"] == "unresolved"
    assert result["reason"] == "ambiguous_attribution"


def test_two_records_two_sections_each_binds_to_its_own():
    ta, tb = "alpha output", "beta output"
    art = make_artifact(
        [("Claude", ta, INV_A), ("OpenAI", tb, INV_B)], seeds=[INV_A, INV_B]
    )
    assert evaluate_produced_by(art, make_record(INV_A, digest_of=ta))["status"] == "established"
    assert evaluate_produced_by(art, make_record(INV_B, digest_of=tb))["status"] == "established"
    crossed = evaluate_produced_by(art, make_record(INV_A, digest_of=tb))
    assert crossed["status"] == "unresolved"
    assert crossed["reason"] == "digest_mismatch"


def test_display_metadata_is_not_attribution_in_both_directions():
    text = "stable content"
    art = make_artifact([("Claude", text, INV_A)], seeds=[INV_A])
    rec = make_record(INV_A, digest_of=text)
    restyled = art.replace("## Claude Response", "## Anthropic Response").replace(
        "- model: `claude-sonnet-5`", "- model: `renamed-model`"
    )
    assert evaluate_produced_by(restyled, rec)["status"] == "established", (
        "changing display metadata must not change attribution"
    )
    reid = art.replace(INV_A, INV_B)
    result = evaluate_produced_by(reid, rec)
    assert result["status"] == "unresolved", (
        "changing the invocation_id must change attribution"
    )


# --- EXACT TEXT ROUND-TRIP -----------------------------------------------

@pytest.mark.parametrize(
    "text",
    [
        "  leading spaces",
        "trailing newline\n",
        "trailing newlines\n\n",
        "trailing spaces   ",
        "\n leading newline",
        "interior\n\n\nblank lines",
        "fence-like content\n```\ncode\n```\nafter",
    ],
    ids=[
        "leading_spaces",
        "trailing_newline",
        "double_trailing_newline",
        "trailing_spaces",
        "leading_newline",
        "interior_blanks",
        "single_fence_content",
    ],
)
def test_exact_text_round_trip(text: str):
    art = make_artifact([("Claude", text, INV_A)], seeds=[INV_A])
    rec = make_record(INV_A, digest_of=text)
    result = evaluate_produced_by(art, rec)
    assert result["status"] == "established", (
        "exact bytes must round-trip; a normalizing extractor is the "
        "prohibited failure mode"
    )


def test_normalized_extraction_cannot_convert_mismatch_to_match():
    """Digest retained over stripped text + extractor that strips = false match.

    The evaluator must compare the digest of the EXACT extracted text. If it
    normalized, this constructed mismatch would pass; it must not.
    """
    stored = "content"          # what a normalizing pipeline would digest
    actual = "content\n"        # what the provider actually returned
    art = make_artifact([("Claude", actual, INV_A)], seeds=[INV_A])
    rec = make_record(INV_A, digest_of=stored)
    result = evaluate_produced_by(art, rec)
    assert result["status"] == "unresolved"
    assert result["reason"] == "digest_mismatch"


# --- STRUCTURAL MARKER IN OUTPUT -----------------------------------------

SYNTHETIC = (
    "## Claude Response\n"
    "\n"
    "- model: `claude-sonnet-5`\n"
    "\n"
    f"- invocation_id: `{INV_B}`\n"
    "\n"
    "innocent-looking body"
)


def test_structural_marker_round_trips_as_content():
    art = make_artifact([("Claude", SYNTHETIC, INV_A)], seeds=[INV_A])
    rec = make_record(INV_A, digest_of=SYNTHETIC)
    result = evaluate_produced_by(art, rec)
    assert result["status"] == "established", (
        "framing-mimicking content inside a fence is still just content"
    )


def test_structural_marker_never_creates_a_bindable_section():
    art = make_artifact([("Claude", SYNTHETIC, INV_A)], seeds=[INV_A, INV_B])
    rec_b = make_record(INV_B, digest_of="innocent-looking body")
    result = evaluate_produced_by(art, rec_b)
    assert result["status"] == "unresolved", (
        "the synthetic section must never be bound"
    )
    assert result["reason"] in ("attributed_section_not_found", "ambiguous_attribution")


def test_fence_collision_content_round_trips_or_unresolved():
    """KNOWN RED FINDING candidate: content containing both ``` and ````.

    markdown_escape_fence escalates exactly once; content containing the
    escalated fence terminates it early. The requirement: exact round-trip
    or unresolved — never a silent wrong extraction that establishes.
    """
    hostile = "text\n```\ninner\n```\nand\n````\ndeeper\n````\ndone"
    art = make_artifact([("Claude", hostile, INV_A)], seeds=[INV_A])
    rec = make_record(INV_A, digest_of=hostile)
    result = evaluate_produced_by(art, rec)
    assert result["status"] in ("established", "unresolved")
    if result["status"] == "unresolved":
        assert result["reason"] in (
            "attributed_section_not_found",
            "ambiguous_attribution",
            "digest_mismatch",
        )
    # The strong form, which currently cannot hold without a fence fix:
    # extraction of the exact hostile bytes. Marked as the acceptance target.
    assert result["status"] == "established", (
        "KNOWN FRAMING LIMIT: markdown_escape_fence must guarantee the fence "
        "string is absent from the content it fences; see finding report"
    )


# --- HISTORICAL SEEDS ----------------------------------------------------

def test_historical_format_without_invocation_id_yields_unresolved():
    """The 106 existing seeded artifacts carry model lines and no
    invocation_id; they must remain unresolved, not be promoted."""
    art = make_artifact([("Claude", "old content", None)], seeds=[INV_A])
    rec = make_record(INV_A, digest_of="old content")
    result = evaluate_produced_by(art, rec)
    assert result["status"] == "unresolved"
    assert result["reason"] == "attributed_section_not_found"


def test_digest_function_convention():
    assert output_text_digest("x") == sha256_hex("x")
    assert output_text_digest("x") != output_text_digest("x\n")
