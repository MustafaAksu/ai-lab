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

from ai_lab.documentation.context_pack import ContextPackItem
from ai_lab.documentation.context_pack_renderer import compute_source_binding_digest
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
    # The 25 retained manifests predate both source_binding_digest and the
    # content-addressed reference scheme, so no edge from them can be
    # established and the evaluation stops at the reference.
    assert r.coverage == COVERAGE_UNAVAILABLE
    assert "not_content_addressed" in r.reason
    assert r.edges == ()


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
    rec = _record_referencing(tmp_path, trimmed, _write_content_addressed(tmp_path, trimmed))
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
    ref = _write_content_addressed(tmp_path, manifest)
    rec = _record_referencing(tmp_path, manifest, ref,
                              prompt_hash="sha256:" + "1" * 64)
    r = ancestry_edges(invocation=rec, repo_root=tmp_path)
    assert r.coverage == COVERAGE_UNAVAILABLE
    assert r.reason == "manifest_prompt_hash_does_not_identify_the_captured_prompt"
    assert r.edges == ()


def test_manifest_without_a_prompt_hash_yields_unresolved(tmp_path):
    """Three of the 25 retained manifests carry no full_prompt_hash."""

    src, manifest = _a_manifest_with_hash()
    stripped = {k: v for k, v in manifest.items() if k != "full_prompt_hash"}
    rec = _record_referencing(tmp_path, None,
                              _write_content_addressed(tmp_path, stripped),
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
    rec = _record_referencing(tmp_path, altered, _write_content_addressed(tmp_path, altered))
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
    assert "SUBSTITUTED.md" not in r.edges, (
        "a substituted source path was reported as an established ancestry edge"
    )
    assert r.coverage != COVERAGE_COMPLETE
    assert r.establishes_independence is False


def test_retained_manifests_cannot_yield_complete():
    """Every manifest retained before source_binding_digest existed.

    Legacy manifests yield partial, never complete, and their items are not
    reported as established.
    """

    src, manifest = _a_manifest_with_hash()
    rel = str(src.relative_to(REPO))
    rec = _record_referencing(None, manifest, rel)
    r = ancestry_edges(invocation=rec, repo_root=REPO)
    assert r.coverage == COVERAGE_UNAVAILABLE
    assert r.edges == ()


# --- the binding falsification set ---------------------------------------

def _bound_manifest(tmp_path, manifest, *, mutate=None):
    """Write a manifest whose every item carries a correct binding."""

    import os

    bound = copy.deepcopy(manifest)
    for it in bound["items"]:
        p = tmp_path / it["source_path"]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("content of " + it["source_path"])
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        for it in bound["items"]:
            it["source_binding_digest"] = compute_source_binding_digest(
                ContextPackItem(item_type=it["item_type"], item_id=it["item_id"],
                                reason="r", relevance_score=0.5,
                                source_path=it["source_path"]))
    finally:
        os.chdir(cwd)
    if mutate:
        mutate(tmp_path, bound)
    return bound


def _write_content_addressed(tmp_path, manifest):
    """Write a manifest under a content-addressed reference and return it.

    The reference embeds the SHA-256 of the bytes written, which is what
    authenticates the manifest to the InvocationRecord.
    """

    import hashlib

    payload = json.dumps(manifest).encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    ref = f"m.context.{digest}.json"
    (tmp_path / ref).write_bytes(payload)
    return ref


def test_binding_positive_case_reaches_complete(tmp_path):
    """The first input for which COMPLETE is reachable."""

    _, manifest = _a_manifest_with_hash()
    bound = _bound_manifest(tmp_path, manifest)
    rec = _record_referencing(tmp_path, bound, _write_content_addressed(tmp_path, bound))
    r = ancestry_edges(invocation=rec, repo_root=tmp_path)
    assert r.coverage == COVERAGE_COMPLETE
    assert len(r.edges) == len(bound["items"])
    assert r.unbound_sources == ()
    assert r.binding.startswith("bound")
    assert r.establishes_independence is False


def test_binding_rejects_substituted_source_path(tmp_path):
    """Changing source_path while leaving the binding untouched. The falsification
    that found the hole."""

    _, manifest = _a_manifest_with_hash()

    def swap(root, m):
        (root / "OTHER.md").write_text("content of " + m["items"][0]["source_path"])
        m["items"][0]["source_path"] = "OTHER.md"

    bound = _bound_manifest(tmp_path, manifest, mutate=swap)
    rec = _record_referencing(tmp_path, bound, _write_content_addressed(tmp_path, bound))
    r = ancestry_edges(invocation=rec, repo_root=tmp_path)
    assert "OTHER.md" not in r.edges
    assert "OTHER.md" in r.unbound_sources
    assert r.coverage == COVERAGE_PARTIAL


def test_binding_rejects_changed_source_content(tmp_path):
    """Changing what the source renders to, leaving the binding untouched."""

    _, manifest = _a_manifest_with_hash()

    def edit(root, m):
        (root / m["items"][0]["source_path"]).write_text("something else entirely")

    bound = _bound_manifest(tmp_path, manifest, mutate=edit)
    rec = _record_referencing(tmp_path, bound, _write_content_addressed(tmp_path, bound))
    r = ancestry_edges(invocation=rec, repo_root=tmp_path)
    assert bound["items"][0]["source_path"] not in r.edges
    assert bound["items"][0]["source_path"] in r.unbound_sources


def test_binding_rejects_identical_content_at_a_different_path(tmp_path):
    """The path participates in the digest, so identical text elsewhere fails."""

    _, manifest = _a_manifest_with_hash()

    def repoint(root, m):
        original = m["items"][0]["source_path"]
        (root / "TWIN.md").write_text("content of " + original)
        m["items"][0]["source_path"] = "TWIN.md"

    bound = _bound_manifest(tmp_path, manifest, mutate=repoint)
    rec = _record_referencing(tmp_path, bound, _write_content_addressed(tmp_path, bound))
    r = ancestry_edges(invocation=rec, repo_root=tmp_path)
    assert "TWIN.md" not in r.edges, (
        "identical rendered text at a different path preserved the binding; the "
        "path is not participating in the digest"
    )


def test_binding_legacy_manifest_is_partial_not_complete(tmp_path):
    """An item with no binding field at all."""

    _, manifest = _a_manifest_with_hash()

    def strip(root, m):
        m["items"][0].pop("source_binding_digest", None)

    bound = _bound_manifest(tmp_path, manifest, mutate=strip)
    rec = _record_referencing(tmp_path, bound, _write_content_addressed(tmp_path, bound))
    r = ancestry_edges(invocation=rec, repo_root=tmp_path)
    assert r.coverage == COVERAGE_PARTIAL
    assert bound["items"][0]["source_path"] in r.unbound_sources


def test_binding_mixed_one_bound_one_unbound(tmp_path):
    """A valid edge is retained while an unbound sibling makes coverage partial."""

    _, manifest = _a_manifest_with_hash()
    assert len(manifest["items"]) >= 2, "need a multi-item manifest"

    def strip_one(root, m):
        m["items"][0].pop("source_binding_digest", None)

    bound = _bound_manifest(tmp_path, manifest, mutate=strip_one)
    rec = _record_referencing(tmp_path, bound, _write_content_addressed(tmp_path, bound))
    r = ancestry_edges(invocation=rec, repo_root=tmp_path)
    assert bound["items"][0]["source_path"] in r.unbound_sources
    assert bound["items"][1]["source_path"] in r.edges
    assert r.coverage == COVERAGE_PARTIAL


def test_binding_is_not_produced_for_a_placeholder(tmp_path):
    """A missing source renders to a placeholder, which must not be bound."""

    item = ContextPackItem(item_type="abstraction", item_id="GONE", reason="r",
                           relevance_score=0.5, source_path="docs/GONE-FOREVER.md")
    assert compute_source_binding_digest(item) is None


def test_binding_digest_requires_a_source_path():
    """The field is meaningless without the path it binds."""

    from ai_lab.documentation.context_pack import ContextPackError

    with pytest.raises(ContextPackError, match="requires a source_path"):
        ContextPackItem(item_type="abstraction", item_id="X", reason="r",
                        relevance_score=0.5, source_binding_digest="a" * 64)


# --- structural validation and location independence ---------------------

def test_structurally_invalid_manifest_never_reaches_complete(tmp_path):
    """A correctly bound manifest the writer would have rejected.

    Previously produced coverage complete: ancestry_edges JSON-parsed the
    manifest and read its items without applying the rules the writer applied.
    """

    _, manifest = _a_manifest_with_hash()

    def invalidate(root, m):
        m["assembly_policy"] = "NOT_A_VALID_POLICY"

    bound = _bound_manifest(tmp_path, manifest, mutate=invalidate)
    rec = _record_referencing(tmp_path, bound, _write_content_addressed(tmp_path, bound))
    r = ancestry_edges(invocation=rec, repo_root=tmp_path)
    assert r.coverage == COVERAGE_UNAVAILABLE
    assert "does_not_validate" in r.reason
    assert r.edges == ()


def test_inconsistent_manifest_id_is_rejected(tmp_path):
    """manifest_id is checked for consistency on construction; a reader that
    skips construction skips that check too."""

    _, manifest = _a_manifest_with_hash()

    def tamper(root, m):
        m["manifest_id"] = "0" * 16

    bound = _bound_manifest(tmp_path, manifest, mutate=tamper)
    rec = _record_referencing(tmp_path, bound, _write_content_addressed(tmp_path, bound))
    r = ancestry_edges(invocation=rec, repo_root=tmp_path)
    assert r.coverage == COVERAGE_UNAVAILABLE
    assert "does_not_validate" in r.reason


def test_every_retained_manifest_validates():
    """The canonical path must not reject manifests the writer produced."""

    from ai_lab.documentation.context_pack import manifest_from_dict

    files = sorted(glob.glob(str(REPO / "docs/comparisons/*.context.json")))
    assert files, "no retained manifests"
    for f in files:
        manifest_from_dict(json.loads(pathlib.Path(f).read_text()))


def test_evaluation_is_independent_of_process_cwd(tmp_path, monkeypatch):
    """Proves the replacement for os.chdir actually removed the dependency.

    An earlier version changed the process working directory so the renderer
    would resolve source paths against repo_root. This runs the same evaluation
    from two different working directories and requires identical results.
    """

    import os

    _, manifest = _a_manifest_with_hash()
    bound = _bound_manifest(tmp_path, manifest)
    rec = _record_referencing(tmp_path, bound, _write_content_addressed(tmp_path, bound))

    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()

    monkeypatch.chdir(REPO)
    from_repo = ancestry_edges(invocation=rec, repo_root=tmp_path)
    monkeypatch.chdir(elsewhere)
    from_elsewhere = ancestry_edges(invocation=rec, repo_root=tmp_path)

    assert from_repo.coverage == from_elsewhere.coverage == COVERAGE_COMPLETE
    assert from_repo.edges == from_elsewhere.edges
    assert from_repo.unbound_sources == from_elsewhere.unbound_sources == ()
    assert os.getcwd() == str(elsewhere), "the evaluator changed the working directory"


# --- manifest-to-record identity -----------------------------------------

def test_substituted_path_with_recomputed_binding_is_rejected(tmp_path):
    """The mutation the per-item binding alone did not catch.

    The existing suite tested "change the path, KEEP the binding" and rejected
    it. Nobody tested "change the path, RECOMPUTE the binding", and that reached
    coverage complete: per-item bindings prove an item is internally consistent
    with its source, not that this manifest is the one whose selection produced
    the prompt.

    The content-addressed reference closes it. Recomputing the binding changes
    the manifest bytes, so the digest the InvocationRecord's reference commits
    to no longer authenticates them.
    """

    _, manifest = _a_manifest_with_hash()
    honest = _bound_manifest(tmp_path, manifest)
    ref = _write_content_addressed(tmp_path, honest)
    rec = _record_referencing(tmp_path, honest, ref)
    assert ancestry_edges(invocation=rec, repo_root=tmp_path).coverage \
        == COVERAGE_COMPLETE, "the honest baseline must reach complete"

    # substitute a source AND recompute its binding, leaving the record alone
    tampered = copy.deepcopy(honest)
    (tmp_path / "SWAPPED.md").write_text("content of SWAPPED.md")
    tampered["items"][0]["source_path"] = "SWAPPED.md"
    tampered["items"][0]["source_binding_digest"] = compute_source_binding_digest(
        ContextPackItem(item_type=tampered["items"][0]["item_type"],
                        item_id=tampered["items"][0]["item_id"], reason="r",
                        relevance_score=0.5, source_path="SWAPPED.md"),
        repo_root=tmp_path)
    (tmp_path / ref).write_text(json.dumps(tampered))  # same reference, new bytes

    r = ancestry_edges(invocation=rec, repo_root=tmp_path)
    assert r.coverage == COVERAGE_UNAVAILABLE
    assert "do_not_match_the_reference_digest" in r.reason
    assert "SWAPPED.md" not in r.edges


def test_reference_without_a_content_digest_is_rejected(tmp_path):
    """A reference that names a file without authenticating its contents."""

    _, manifest = _a_manifest_with_hash()
    bound = _bound_manifest(tmp_path, manifest)
    (tmp_path / "plain.context.json").write_text(json.dumps(bound))
    rec = _record_referencing(tmp_path, bound, "plain.context.json")
    r = ancestry_edges(invocation=rec, repo_root=tmp_path)
    assert r.coverage == COVERAGE_UNAVAILABLE
    assert "not_content_addressed" in r.reason


def test_unknown_manifest_field_fails_closed(tmp_path):
    """An evaluator must not prove an edge from a manifest it cannot fully read."""

    from ai_lab.documentation.context_pack import ContextPackError, manifest_from_dict

    _, manifest = _a_manifest_with_hash()
    bound = _bound_manifest(tmp_path, manifest)
    bound["some_future_field"] = {"affects": "prompt semantics"}
    ref = _write_content_addressed(tmp_path, bound)
    rec = _record_referencing(tmp_path, bound, ref)
    r = ancestry_edges(invocation=rec, repo_root=tmp_path)
    assert r.coverage == COVERAGE_UNAVAILABLE
    assert "does_not_validate" in r.reason
    # permissive mode still accepts it, for callers that are not proving edges
    manifest_from_dict(bound)
    with pytest.raises(ContextPackError, match="unsupported manifest field"):
        manifest_from_dict(bound, reject_unknown=True)


def test_inconsistent_total_token_estimate_is_rejected(tmp_path):
    """Rendered into the pack as "Total token estimate", so a mismatch means the
    retained manifest is not what the writer would have serialised."""

    from ai_lab.documentation.context_pack import ContextPackError, manifest_from_dict

    _, manifest = _a_manifest_with_hash()
    bound = _bound_manifest(tmp_path, manifest)
    bound["total_token_estimate"] = 999999
    with pytest.raises(ContextPackError, match="does not match the sum"):
        manifest_from_dict(bound)
