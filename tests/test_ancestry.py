"""Falsification set for the first evidence-ancestry edge class.

Implements scope item 6 and success criteria 1 to 10 of PLAN-20260817-0001,
under WARR-20260817-0001. Cases are constructed before the checks they exercise
are relied upon, per DECISION-20260812-0002.

The two cases that matter most are the ones a naive implementation answers
wrongly:

- UNPOPULATED REFERENCE. All 210 retained records have
  context_manifest_reference null. Reporting an empty ancestor set for them
  would present absence of a recorded edge as absence of an edge, which C14
  forbids and which the plan's risk statement names.

- SIBLING NEGATIVE. The repository holds 105 pairs sharing a rendered_prompt
  digest. C13 forbids counting that as ancestry.
"""

from __future__ import annotations

import copy
import glob
import json
import pathlib

import pytest

from ai_lab.documentation.prompt_context import prompt_sha256
from ai_lab.providers.ancestry import (
    COVERAGE_COMPLETE,
    COVERAGE_PARTIAL,
    COVERAGE_UNAVAILABLE,
    AncestryResult,
    ancestry_edges,
    normalise_digest,
)
from ai_lab.providers.invocation_record import digest_text

REPO = pathlib.Path(__file__).resolve().parents[1]


def _records():
    return [json.loads(pathlib.Path(f).read_text())
            for f in sorted(glob.glob(str(REPO / "docs/invocations/INV-*.json")))]


def _a_manifest_with_hash():
    for f in sorted(glob.glob(str(REPO / "docs/comparisons/*.context.json"))):
        m = json.loads(pathlib.Path(f).read_text())
        if m.get("full_prompt_hash") and m.get("items"):
            return pathlib.Path(f), m
    raise AssertionError("no retained manifest with a full_prompt_hash and items")


def _record_referencing(tmp_path, manifest, rel_ref, prompt_hash=None):
    """A record shaped like a captured one, referencing a manifest."""

    rec = copy.deepcopy(_records()[0])
    m = rec["effective_input_manifest"]
    m["context_manifest_reference"] = rel_ref
    if prompt_hash is not None:
        m["rendered_prompt_digest"] = prompt_hash
    elif manifest and manifest.get("full_prompt_hash"):
        m["rendered_prompt_digest"] = "sha256:" + manifest["full_prompt_hash"]
    return rec


# --- criterion 8: hash comparability, answered by evidence ------------------

def test_the_two_prompt_hashes_are_comparable_after_normalisation():
    """Success criterion 8, and the reason normalise_digest exists.

    ContextManifest.full_prompt_hash comes from prompt_sha256 and is bare hex.
    InvocationRecord's rendered_prompt_digest comes from digest_text and is
    "sha256:" plus the same hex. Both are SHA-256 over the UTF-8 encoding of the
    same provider_prompt string. Naive equality returns False on a VALID pair,
    which would report every genuine edge as a prompt mismatch.
    """

    s = "identical rendered prompt text"
    bare, prefixed = prompt_sha256(s), digest_text(s)
    assert bare != prefixed, "if these were equal, normalisation would be unnecessary"
    assert normalise_digest(bare) == normalise_digest(prefixed)
    assert normalise_digest(prefixed) == bare


@pytest.mark.parametrize("value,expected", [
    (None, None), ("", None),
    ("ABCDEF", "abcdef"),
    ("sha256:ABCDEF", "abcdef"),
    ("  sha256:abcdef  ", "abcdef"),
])
def test_normalise_digest_cases(value, expected):
    assert normalise_digest(value) == expected


# --- criterion 7: the case all 210 records exhibit -------------------------

def test_unpopulated_reference_is_unavailable_not_empty():
    """Success criterion 7. The C14 case, against real data.

    Every retained record has context_manifest_reference null. The result must
    say the edge class could not be evaluated, not that no ancestor exists.
    """

    recs = _records()
    assert recs, "no retained invocation records"
    for rec in recs:
        r = ancestry_edges(invocation=rec, repo_root=REPO)
        assert r.coverage == COVERAGE_UNAVAILABLE
        assert r.reason == "no_context_manifest_reference_recorded"
        assert r.edges == ()
        assert r.evaluated is False


def test_every_retained_record_is_currently_unevaluable():
    """Pins the state the plan measured: 0 of the records carry a reference."""

    recs = _records()
    unavailable = [r for r in recs
                   if ancestry_edges(invocation=r, repo_root=REPO).coverage
                   == COVERAGE_UNAVAILABLE]
    assert len(unavailable) == len(recs), (
        "some record now carries a context_manifest_reference; the first retained "
        "instance has arrived and this test should be replaced by one exercising it"
    )


# --- criterion 1: the positive edge ---------------------------------------

def test_positive_edge(tmp_path):
    """Success criterion 1.

    A source artifact listed in a retained manifest, referenced by an
    invocation, with the prompt hashes agreeing, is reported as an ancestor.
    """

    src, manifest = _a_manifest_with_hash()
    rel = str(src.relative_to(REPO))
    rec = _record_referencing(tmp_path, manifest, rel)
    r = ancestry_edges(invocation=rec, repo_root=REPO)
    assert r.edges, "no edge established from a manifest with items"
    assert r.manifest_id == manifest.get("manifest_id")
    for item in manifest["items"]:
        if (REPO / item["source_path"]).exists():
            assert item["source_path"] in r.edges
    # COMPLETE is unreachable while source selection is unbound to the prompt.
    assert r.coverage == COVERAGE_PARTIAL
    assert r.binding is not None and r.binding.startswith("unbound")
    assert "not_bound_to_the_rendered_prompt" in r.reason


# --- criterion 2: the sibling negative, protecting C13 -------------------

def test_sibling_negative_no_edge_between_same_prompt_invocations():
    """Success criterion 2. C13 against the 105 real pairs.

    Two invocations sharing an identical rendered_prompt_digest, with no
    manifest linking either to the other, have no ancestry edge between them.
    """

    recs = _records()
    by = {}
    for r in recs:
        by.setdefault(r["effective_input_manifest"]["rendered_prompt_digest"], []).append(r)
    pairs = [v for v in by.values() if len(v) == 2]
    assert len(pairs) >= 100, f"expected the ~105 same-prompt pairs, found {len(pairs)}"
    for left, right in pairs[:5]:
        assert left["effective_input_manifest"]["rendered_prompt_digest"] == \
               right["effective_input_manifest"]["rendered_prompt_digest"]
        # The narrower fact only: an equal prompt digest creates no edge. This
        # module does not answer whether one invocation is an ancestor of
        # another, and must not be asked to: that relation is outside the
        # implemented edge class, and answering False would collapse "outside
        # scope" into "no relation exists", which P5 forbids.
        assert ancestry_edges(invocation=left, repo_root=REPO).edges == ()
        assert ancestry_edges(invocation=right, repo_root=REPO).edges == ()


# --- criterion 3: an artifact not selected is not an ancestor ------------

def test_manifest_item_absent_is_not_an_ancestor(tmp_path):
    """Success criterion 3. Existing nearby is not being an ancestor."""

    src, manifest = _a_manifest_with_hash()
    trimmed = copy.deepcopy(manifest)
    dropped = trimmed["items"].pop()["source_path"]
    p = tmp_path / "m.context.json"
    p.write_text(json.dumps(trimmed))
    rec = _record_referencing(tmp_path, trimmed, "m.context.json")
    r = ancestry_edges(invocation=rec, repo_root=tmp_path)
    assert dropped not in r.edges
    assert (REPO / dropped).exists(), "the dropped artifact does exist in the repository"


# --- criterion 4: dangling manifest ------------------------------------

def test_dangling_manifest_is_unresolved_not_no_ancestry(tmp_path):
    """Success criterion 4. C14: unresolved, never no-ancestry."""

    rec = _record_referencing(tmp_path, None, "docs/comparisons/NOT-A-FILE.context.json",
                              prompt_hash="sha256:" + "0" * 64)
    r = ancestry_edges(invocation=rec, repo_root=REPO)
    assert r.coverage == COVERAGE_UNAVAILABLE
    assert "not_retained" in r.reason
    assert r.edges == ()
    assert r.evaluated is False


def test_unreadable_manifest_is_unresolved(tmp_path):
    p = tmp_path / "broken.context.json"
    p.write_text("{ not json")
    rec = _record_referencing(tmp_path, None, "broken.context.json",
                              prompt_hash="sha256:" + "0" * 64)
    r = ancestry_edges(invocation=rec, repo_root=tmp_path)
    assert r.coverage == COVERAGE_UNAVAILABLE
    assert "unreadable" in r.reason


# --- criterion 5: prompt mismatch --------------------------------------

def test_prompt_mismatch_yields_no_valid_edge(tmp_path):
    """Success criterion 5.

    A manifest whose recorded prompt hash does not identify the captured prompt
    yields unresolved, even though its items exist and its path resolves.
    """

    src, manifest = _a_manifest_with_hash()
    rel = str(src.relative_to(REPO))
    rec = _record_referencing(tmp_path, manifest, rel,
                              prompt_hash="sha256:" + "1" * 64)
    r = ancestry_edges(invocation=rec, repo_root=REPO)
    assert r.coverage == COVERAGE_UNAVAILABLE
    assert r.reason == "manifest_prompt_hash_does_not_identify_the_captured_prompt"
    assert r.edges == ()


def test_manifest_without_a_prompt_hash_yields_unresolved(tmp_path):
    """Three of the 25 retained manifests carry no full_prompt_hash."""

    src, manifest = _a_manifest_with_hash()
    stripped = {k: v for k, v in manifest.items() if k != "full_prompt_hash"}
    p = tmp_path / "m.context.json"
    p.write_text(json.dumps(stripped))
    rec = _record_referencing(tmp_path, None, "m.context.json",
                              prompt_hash="sha256:" + "2" * 64)
    r = ancestry_edges(invocation=rec, repo_root=tmp_path)
    assert r.coverage == COVERAGE_UNAVAILABLE
    assert r.reason == "manifest_records_no_full_prompt_hash"


# --- criterion 6: a source that cannot be reconstructed ----------------

def test_missing_source_path_yields_partial_coverage(tmp_path):
    """Success criterion 6. Partial coverage, and independence not inferred."""

    src, manifest = _a_manifest_with_hash()
    altered = copy.deepcopy(manifest)
    altered["items"][0]["source_path"] = "docs/abstractions/GONE-FOREVER.md"
    p = tmp_path / "m.context.json"
    p.write_text(json.dumps(altered))
    rec = _record_referencing(tmp_path, altered, "m.context.json")
    r = ancestry_edges(invocation=rec, repo_root=tmp_path)
    assert r.coverage == COVERAGE_PARTIAL
    gone = "docs/abstractions/GONE-FOREVER.md"
    assert gone in r.unreconstructable_sources
    # The renderer substitutes a "[source file not found]" placeholder, so the
    # artifact's contents did not necessarily reach the executor. Visible as
    # unreconstructable, absent from the established-edge set.
    assert gone not in r.edges
    assert r.establishes_independence is False
    assert "cannot be reconstructed" in r.reason


# --- the property no result may ever assert ---------------------------

@pytest.mark.parametrize("coverage", [COVERAGE_COMPLETE, COVERAGE_PARTIAL,
                                      COVERAGE_UNAVAILABLE])
def test_no_result_ever_establishes_independence(coverage):
    """C14, at every coverage level including complete.

    This edge class is one of several Section 4.19 names, so even complete
    coverage of it establishes nothing about the others.
    """

    assert AncestryResult(edges=("a",), coverage=coverage).establishes_independence is False
    # The dangerous incorrect implementation is `coverage == COMPLETE and not
    # edges`: a complete traversal that found nothing, read as independence.
    # That is the negative result most likely to be promoted later.
    assert AncestryResult(edges=(), coverage=coverage).establishes_independence is False


def test_substituted_source_path_is_not_reported_as_complete(tmp_path):
    """The reviewing executor's falsification, retained.

    Substituting a manifest's source_path while leaving manifest_id and
    full_prompt_hash untouched previously produced coverage COMPLETE with the
    substituted path reported as an established ancestor. compute_manifest_id
    hashes task, assembly_policy and item_ids and neither source_path nor source
    content, so nothing in the retained evidence detects the substitution.

    The hole is not closed by this test; COMPLETE is capped at PARTIAL and the
    binding field says why. This case exists so that a future change which
    reintroduces COMPLETE without a source-to-prompt binding fails here.
    """

    src, manifest = _a_manifest_with_hash()
    tampered = copy.deepcopy(manifest)
    tampered["items"][0]["source_path"] = "SUBSTITUTED.md"
    (tmp_path / "SUBSTITUTED.md").write_text("x")
    for it in tampered["items"][1:]:
        p = tmp_path / it["source_path"]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("x")
    (tmp_path / "m.context.json").write_text(json.dumps(tampered))
    rec = _record_referencing(tmp_path, tampered, "m.context.json")

    r = ancestry_edges(invocation=rec, repo_root=tmp_path)
    assert "SUBSTITUTED.md" in r.edges, (
        "the substitution is still undetected, which is the recorded hole"
    )
    assert r.coverage != COVERAGE_COMPLETE, (
        "COMPLETE coverage was reported for an unbound source selection"
    )
    assert r.binding is not None and r.binding.startswith("unbound")
    assert r.establishes_independence is False


def test_complete_coverage_is_currently_unreachable():
    """No input may yield COMPLETE while the binding hole is open.

    If this fails, either a binding was implemented and the module docstring,
    PLAN-20260817-0001 scope item 4, and this test must all be updated, or
    COMPLETE was reintroduced without one.
    """

    src, manifest = _a_manifest_with_hash()
    rel = str(src.relative_to(REPO))
    rec = _record_referencing(None, manifest, rel)
    assert ancestry_edges(invocation=rec, repo_root=REPO).coverage != COVERAGE_COMPLETE
