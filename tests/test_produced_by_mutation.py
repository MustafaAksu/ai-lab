"""Mutation tests for the produced_by evaluator (PLAN-20260817-0002).

Warrant condition 7 and DECISION-20260812-0002: every guard relied upon for
a governance claim is mutation-tested. Each test replaces exactly one guard
with behaviour that would pass where the guard refuses, and demonstrates
that the refusal disappears. That proves the guard, and nothing else in the
pipeline, is what stands between the scenario and a false establishment.

Written alongside the guards they mutate (they cannot precede them); the
scenarios reuse the fixtures of tests/test_produced_by_falsification.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from ai_lab.provenance import produced_by

from tests.test_produced_by_falsification import (
    INV_A,
    INV_B,
    SYNTHETIC,
    make_artifact,
    make_record,
)


def _permit_record_evidence(record):
    return None


def _permit_seed(artifact_text, invocation_id):
    return None


def _permit_digest(body, record):
    return None


def _bind_first_available(artifact_text, invocation_id):
    """The 'take the first match' behaviour the evaluator must not have."""
    sections = produced_by._parse_sections(artifact_text) or []
    for section in sections:
        if section["body"] is not None:
            return section["body"], None
    return None, produced_by.REASON_NO_SECTION


def test_record_evidence_guard_is_load_bearing(monkeypatch):
    """Without the guard, a digestless record slides through to the digest
    comparison and fails there for the wrong reason, or a mutant of both
    guards establishes outright."""
    art = make_artifact([("Claude", "x", INV_A)], seeds=[INV_A])
    rec = make_record(INV_A)  # outcome, no digest
    assert produced_by.evaluate_produced_by(art, rec)["reason"] == "outcome_without_output_digest"
    monkeypatch.setattr(produced_by, "_record_evidence_guard", _permit_record_evidence)
    monkeypatch.setattr(produced_by, "_digest_guard", _permit_digest)
    mutant = produced_by.evaluate_produced_by(art, rec)
    assert mutant["status"] == "established", (
        "with the evidence and digest guards permissive, nothing else "
        "refuses: the guards are load-bearing"
    )


def test_seed_guard_is_load_bearing(monkeypatch):
    text = "content"
    art = make_artifact([("Claude", text, INV_A)], seeds=[])
    rec = make_record(INV_A, digest_of=text)
    assert produced_by.evaluate_produced_by(art, rec)["reason"] == "seed_not_found"
    monkeypatch.setattr(produced_by, "_seed_guard", _permit_seed)
    mutant = produced_by.evaluate_produced_by(art, rec)
    assert mutant["status"] == "established", (
        "with the seed guard permissive, the unseeded artifact establishes: "
        "the seed guard alone refused it"
    )


def test_attribution_guard_refuses_what_first_match_would_bind(monkeypatch):
    """WRONG ATTRIBUTION under mutation: binding to whichever section is
    present converts a refusal into an establishment."""
    text = "content"
    art = make_artifact([("Claude", text, INV_B)], seeds=[INV_A])
    rec = make_record(INV_A, digest_of=text)
    assert produced_by.evaluate_produced_by(art, rec)["reason"] == "attributed_section_not_found"
    monkeypatch.setattr(produced_by, "_attribution_guard", _bind_first_available)
    mutant = produced_by.evaluate_produced_by(art, rec)
    assert mutant["status"] == "established", (
        "first-match binding establishes what identity-keyed attribution "
        "refuses: the attribution guard is load-bearing"
    )


def test_attribution_guard_refuses_synthetic_section_first_match_would_bind(monkeypatch):
    """STRUCTURAL MARKER under mutation: a first-match binder attaches the
    seeded-but-absent record to the real section; the guard refuses."""
    art = make_artifact([("Claude", SYNTHETIC, INV_A)], seeds=[INV_A, INV_B])
    rec_b = make_record(INV_B, digest_of=SYNTHETIC)
    assert produced_by.evaluate_produced_by(art, rec_b)["status"] == "unresolved"
    monkeypatch.setattr(produced_by, "_attribution_guard", _bind_first_available)
    mutant = produced_by.evaluate_produced_by(art, rec_b)
    assert mutant["status"] == "established", (
        "first-match binding attributes INV_B's asserted output to INV_A's "
        "section: only the attribution guard prevented it"
    )


def test_digest_guard_is_load_bearing(monkeypatch):
    """The founding hazard under mutation: with the digest guard permissive,
    length agreement establishes, which is exactly the false check the plan
    exists to remove."""
    text = "A" * 335
    imposter = "B" * 335
    art = make_artifact([("Claude", imposter, INV_A)], seeds=[INV_A])
    rec = make_record(INV_A, digest_of=text)
    assert produced_by.evaluate_produced_by(art, rec)["reason"] == "digest_mismatch"
    monkeypatch.setattr(produced_by, "_digest_guard", _permit_digest)
    mutant = produced_by.evaluate_produced_by(art, rec)
    assert mutant["status"] == "established", (
        "with the digest guard permissive, 335 chars of B establish a "
        "record digested over 335 chars of A: the digest guard is the "
        "difference between assertion and establishment"
    )


def test_exactness_mutation_stripping_extractor_converts_mismatch_to_match(monkeypatch):
    """A normalizing digest converts the constructed mismatch into a match,
    so exactness in output_text_digest is load-bearing."""
    stored = "content"
    actual = "content\n"
    art = make_artifact([("Claude", actual, INV_A)], seeds=[INV_A])
    rec = make_record(INV_A, digest_of=stored)
    assert produced_by.evaluate_produced_by(art, rec)["reason"] == "digest_mismatch"

    exact = produced_by.output_text_digest

    def stripping_digest(text: str) -> str:
        return exact(text.strip())

    monkeypatch.setattr(produced_by, "output_text_digest", stripping_digest)
    mutant = produced_by.evaluate_produced_by(art, rec)
    assert mutant["status"] == "established", (
        "a stripping digest passes the constructed mismatch: exact bytes "
        "are load-bearing"
    )
