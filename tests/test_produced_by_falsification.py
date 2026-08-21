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


# A real retained record as the fixture template, so every fixture is a
# record the canonical validator accepts. The v2 fixture was a minimal
# stub that could not validate; when the completion review added canonical
# validation to the evaluator, every stub refused — the same
# fixture-vs-reality lesson as the invented seed shape, caught the same
# review cycle.
_TEMPLATE_PATH = REPO_ROOT / "docs" / "invocations" / "INV-bf521665213e8e83.json"
_TEMPLATE = __import__("json").loads(_TEMPLATE_PATH.read_text())

from ai_lab.providers.invocation_record import invocation_id_for  # noqa: E402


def _fixture_record(session_id: str) -> dict:
    """A canonically valid record derived from a real retained one.

    invocation_id is content-addressed over IDENTITY_FIELDS_V1, so fixtures
    cannot invent ids: each fixture varies session_id and recomputes the id
    the way the system does. INV_A and INV_B below are those computed ids.
    """
    import copy

    record = copy.deepcopy(_TEMPLATE)
    record["session_id"] = session_id
    record["invocation_id"] = invocation_id_for(record)
    return record


INV_A = _fixture_record("produced-by-fixture-a")["invocation_id"]
INV_B = _fixture_record("produced-by-fixture-b")["invocation_id"]
_SESSION_FOR = {INV_A: "produced-by-fixture-a", INV_B: "produced-by-fixture-b"}


def make_record(
    invocation_id: str = None,
    *,
    outcome: dict | None | str = "default",
    digest_of: str | None = None,
) -> dict:
    """A canonically valid InvocationRecord for INV_A or INV_B."""
    if invocation_id is None:
        invocation_id = INV_A
    record = _fixture_record(_SESSION_FOR[invocation_id])
    assert record["invocation_id"] == invocation_id
    if outcome is None:
        record.pop("outcome", None)
        return record
    if outcome != "default":
        record["outcome"] = dict(outcome)
    else:
        record["outcome"].pop("output_text_digest", None)
    if digest_of is not None:
        record["outcome"]["output_text_digest"] = sha256_hex(digest_of)
        record["outcome"]["text_chars"] = len(digest_of)
    return record


def make_artifact(
    sections: list[tuple[str, str, str | None]],
    seeds: list[str] | None = None,
    comparison_id: str = "COMP-9999",
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
        # Exactly the shape produced_by_references emits: the artifact is
        # the source, the invocation is the target. The v1 fixture invented
        # a shape ("invocation_id" key) that the v1 parser happened to
        # accept, so the tests validated the evaluator against a fiction;
        # the deliberate run's seed_not_found refusal exposed both.
        extra = {
            "invocation_produced_by": [
                {
                    "source_id": comparison_id,
                    "predicate": "produced_by",
                    "target_id": inv,
                    "relation_source": "future_edge_seed",
                    "authoritative": False,
                    "scope": "invocation_provenance_slice_a",
                    "evidence": f"docs/invocations/{inv}.json",
                }
                for inv in seeds
            ]
        }
    return build_markdown_artifact(
        prompt="prompt",
        responses=responses,
        created_at="2026-08-20T00:00:00+00:00",
        command="test",
        comparison_id=comparison_id,
        extra_metadata=extra,
    )


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


# --- COMPLETION-REVIEW FALSIFIERS (Sol, 2026-08-21) ----------------------
# Two establishment holes the v2 evaluator had, found by the reviewing
# executor against the real COMP-0141, both reproduced before acceptance.


def test_invalid_record_never_establishes():
    """The v2 evaluator established a record stripped to invocation_id and
    outcome, which the canonical validator rejects. Establishment requires
    a record the repository itself accepts."""
    text = "content"
    art = make_artifact([("Claude", text, INV_A)], seeds=[INV_A])
    full = make_record(INV_A, digest_of=text)
    stripped = {"invocation_id": full["invocation_id"], "outcome": full["outcome"]}
    result = evaluate_produced_by(art, stripped)
    assert result["status"] == "unresolved"
    assert result["reason"] == "invalid_invocation_record"


def test_foreign_source_seed_never_establishes():
    """The v2 evaluator matched target_id alone, so a seed copied from
    another artifact established this one. The whole candidate relation
    (this artifact, produced_by, this record) must be seeded."""
    text = "content"
    art = make_artifact([("Claude", text, INV_A)], seeds=[INV_A])
    rec = make_record(INV_A, digest_of=text)
    assert evaluate_produced_by(art, rec)["status"] == "established"
    foreign = art.replace('"source_id": "COMP-9999"', '"source_id": "COMP-8888"')
    assert foreign != art
    result = evaluate_produced_by(foreign, rec)
    assert result["status"] == "unresolved"
    assert result["reason"] == "seed_not_found"


def test_missing_artifact_identity_fails_closed():
    """Without a retained comparison_id the seed's source cannot be checked
    against the artifact, so nothing establishes."""
    text = "content"
    art = make_artifact([("Claude", text, INV_A)], seeds=[INV_A])
    stripped = "\n".join(
        line for line in art.split("\n") if not line.startswith("- comparison_id:")
    )
    rec = make_record(INV_A, digest_of=text)
    result = evaluate_produced_by(stripped, rec)
    assert result["status"] == "unresolved"
    assert result["reason"] == "artifact_identity_not_found"


def test_malformed_seed_metadata_has_its_own_reason():
    """A seed line that is not valid JSON (the one legacy Python-repr
    serialization is this case) is syntactically invalid candidate
    metadata, distinct from structural ambiguity."""
    text = "content"
    art = make_artifact([("Claude", text, INV_A)], seeds=[INV_A])
    line = next(l for l in art.split("\n") if l.startswith("- invocation_produced_by:"))
    repr_line = line.replace('"', "'").replace("false", "False")
    broken = art.replace(line, repr_line)
    assert broken != art
    rec = make_record(INV_A, digest_of=text)
    result = evaluate_produced_by(broken, rec)
    assert result["status"] == "unresolved"
    assert result["reason"] == "invalid_seed_metadata"


def test_new_capture_with_text_populates_digest_and_without_it_establishes_nothing():
    """Operational requirement (warrant condition 6): the capture path
    populates the digest for a new successful capture with textual output,
    and a record missing it establishes no evidence."""
    from ai_lab.providers.invocation_capture import outcome_block
    from ai_lab.providers.provider import ProviderOutcome

    provider_outcome = ProviderOutcome(
        text="captured answer",
        stop_reason="end_turn",
        stop_reason_field="stop_reason",
        input_tokens=1,
        output_tokens=2,
        content_block_types=["text"],
    )
    block = outcome_block(provider_outcome)
    assert block["output_text_digest"] == sha256_hex("captured answer"), (
        "the capture path must populate the digest from the outcome text"
    )

    art = make_artifact([("Claude", "captured answer", INV_A)], seeds=[INV_A])
    rec = make_record(INV_A, digest_of="captured answer")
    del rec["outcome"]["output_text_digest"]
    result = evaluate_produced_by(art, rec)
    assert result["status"] == "unresolved"
    assert result["reason"] == "outcome_without_output_digest"
