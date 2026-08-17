"""Artifact-level evidence ancestry, first edge class.

Implements scope items 1 and 4 of PLAN-20260817-0001 under WARR-20260817-0001,
against ABS-0004 v9.2 Section 4.19 as admitted.

WHAT THIS ESTABLISHES

One edge class only: a repository artifact selected into a retained
ContextManifest and rendered into a captured invocation's effective input is a
direct artifact-level evidence ancestor of that invocation.

    artifact A --(manifest.items[n].source_path)--> ContextManifest M
    ContextManifest M --(context_manifest_reference)--> Invocation I
    therefore A --potential_information_dependence--> I

That is the explicit directional effective-input linkage C13 requires as the
additional retained relation beyond common input. It is NOT inferred from
rendered_prompt_digest equality, which C13 forbids: two invocations sharing a
prompt digest are siblings, and this function never reports an edge between
them.

WHAT THIS DOES NOT ESTABLISH

- Invocation-to-invocation ancestry. The edges are artifact-to-invocation.
  Composing prior invocation -> produced_by -> artifact -> effective input ->
  later invocation needs a produced_by edge class that is out of scope.
- Transitive closure. One edge, no traversal.
- Claim-level lineage. Section 4.15 states an artifact may mix original
  observation, copied finding, paraphrase and new inference, so an
  artifact-level path establishes potential dependence only.
- Independence. C14: where coverage is incomplete the result is unresolved, and
  a negative path result is never evidence of independence. `coverage` is
  returned alongside `edges` for exactly this reason, and an empty `edges` with
  coverage other than COMPLETE means nothing was evaluated rather than nothing
  was found.

THE COMPLETENESS CONDITION (scope item 4) IS NOT YET SATISFIED

An edge should exist only where the referenced manifest is durably retained,
parses, and validates as the manifest used to render the captured prompt. The
third part is NOT achieved by the check implemented here, and that is recorded
rather than concealed.

Comparing the manifest's full_prompt_hash against the record's
rendered_prompt_digest establishes only that two stored hash fields agree. It
does not bind the manifest's current items or source_path values to the prompt
that was rendered. The reviewing executor falsified this against the repository:
substituting a real manifest's first source_path for README.md, leaving
manifest_id and full_prompt_hash untouched, and supplying the matching record
digest produced coverage complete with README.md reported as an established
ancestor. The packaging executor reproduced it.

manifest_id does not close the hole either: compute_manifest_id hashes
task, assembly_policy and item_ids, and neither source_path nor source content.

Until a retained binding exists between source selection, the content actually
rendered, and the captured prompt, NO result from this module reports COMPLETE
coverage. The ceiling is PARTIAL, and `binding` records why. Candidate bindings
include a per-source content digest in the manifest, a rendered-context digest,
or a content-addressed manifest; choosing one is a design decision this slice
does not make.

Those two are comparable, established by evidence rather than assumed: both are
SHA-256 over the UTF-8 encoding of the same `provider_prompt` variable, computed
at scripts/compare_providers.py line 454 for the manifest and lines 548 and 566
for the records. They differ only in that digest_text prefixes "sha256:" and
prompt_sha256 does not. Naive string equality therefore returns False on a
VALID pair, which would report every genuine edge as a prompt mismatch: safe,
because it fails closed, but silently wrong. normalise_digest exists for that
reason.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

# coverage of the edge class this function depends on
COVERAGE_COMPLETE = "complete"
COVERAGE_PARTIAL = "partial"
COVERAGE_UNAVAILABLE = "unavailable"


def normalise_digest(value: str | None) -> str | None:
    """Return the bare lowercase hex of a digest, or None.

    ContextManifest.full_prompt_hash is bare hex; InvocationRecord's
    rendered_prompt_digest is "sha256:" plus the same hex. Comparing them
    unnormalised returns False for a valid pair.
    """

    if not value:
        return None
    v = value.strip().lower()
    return v.split(":", 1)[1] if ":" in v else v


@dataclass(frozen=True)
class AncestryResult:
    """Established edges together with the coverage they rest on.

    `edges` empty with `coverage` other than COMPLETE means the edge class was
    not evaluable, not that no ancestor exists. C14 forbids reading the second
    from the first, which is why both are returned and why `reason` is always
    populated when coverage is not complete.
    """

    edges: tuple[str, ...] = ()
    coverage: str = COVERAGE_UNAVAILABLE
    reason: str | None = None
    manifest_id: str | None = None
    unreconstructable_sources: tuple[str, ...] = ()
    binding: str | None = None

    @property
    def establishes_independence(self) -> bool:
        """Always False. Present so no caller has to infer it.

        C14: a negative traversal result may not be treated as evidence of
        independence. This edge class is one of several the definition names, so
        even COMPLETE coverage of this class establishes nothing about the
        others.
        """

        return False

    @property
    def evaluated(self) -> bool:
        """Whether a USABLE ancestry-edge evaluation is available.

        Not whether evaluation was attempted. A prompt-hash mismatch was
        evaluated and failed validation; it returns UNAVAILABLE because no
        usable edge results, and this property is False for it.
        """

        return self.coverage != COVERAGE_UNAVAILABLE


def ancestry_edges(
    *,
    invocation: Mapping[str, Any],
    repo_root: Path | str = ".",
) -> AncestryResult:
    """Report the artifact-to-invocation ancestry edges for one invocation.

    Pure apart from reading the referenced manifest and testing source-path
    existence. Never raises for a non-establishment: every failure to establish
    returns UNAVAILABLE or PARTIAL coverage with an enumerated reason.
    """

    root = Path(repo_root)
    manifest_ref = (invocation.get("effective_input_manifest") or {}).get(
        "context_manifest_reference"
    )

    # The case all 210 retained records exhibit. Reporting no ancestors here
    # would be the C14 defect: an unpopulated edge is indistinguishable from an
    # absent one unless coverage says so.
    if not manifest_ref:
        return AncestryResult(
            coverage=COVERAGE_UNAVAILABLE,
            reason="no_context_manifest_reference_recorded",
        )

    path = root / manifest_ref
    if not path.exists():
        return AncestryResult(
            coverage=COVERAGE_UNAVAILABLE,
            reason=f"referenced_manifest_not_retained: {manifest_ref}",
        )
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - any parse failure is unavailable
        return AncestryResult(
            coverage=COVERAGE_UNAVAILABLE,
            reason=f"referenced_manifest_unreadable: {type(exc).__name__}",
        )

    manifest_id = manifest.get("manifest_id")

    # Validate that this manifest is the one that rendered the captured prompt.
    recorded = normalise_digest(
        (invocation.get("effective_input_manifest") or {}).get("rendered_prompt_digest")
    )
    claimed = normalise_digest(manifest.get("full_prompt_hash"))
    if claimed is None:
        return AncestryResult(
            coverage=COVERAGE_UNAVAILABLE,
            reason="manifest_records_no_full_prompt_hash",
            manifest_id=manifest_id,
        )
    if recorded is None:
        return AncestryResult(
            coverage=COVERAGE_UNAVAILABLE,
            reason="invocation_records_no_rendered_prompt_digest",
            manifest_id=manifest_id,
        )
    if claimed != recorded:
        return AncestryResult(
            coverage=COVERAGE_UNAVAILABLE,
            reason="manifest_prompt_hash_does_not_identify_the_captured_prompt",
            manifest_id=manifest_id,
        )

    items = manifest.get("items") or []
    edges: list[str] = []
    missing: list[str] = []
    for item in items:
        src = item.get("source_path")
        if not src:
            missing.append(str(item.get("item_id", "<no item_id>")))
            continue
        if not (root / src).exists():
            # The renderer substitutes "[source file not found: <path>]" when a
            # source is absent, so an unreconstructable source does NOT
            # establish that the artifact's contents reached the executor: the
            # executor may have received only the placeholder. The path stays
            # visible in unreconstructable_sources so potential ancestry is not
            # under-reported, and stays OUT of edges so it is not over-reported.
            missing.append(src)
            continue
        edges.append(src)

    # COMPLETE is unreachable until a source-to-prompt binding exists. Capping
    # here rather than at the call site means no caller can obtain COMPLETE from
    # this module while the binding hole is open.
    reasons = ["source_selection_not_bound_to_the_rendered_prompt"]
    if missing:
        reasons.append(
            f"{len(missing)} manifest item(s) name a source that cannot be "
            "reconstructed")
    return AncestryResult(
        edges=tuple(edges),
        coverage=COVERAGE_PARTIAL,
        reason="; ".join(reasons) + "; independence is not inferred",
        manifest_id=manifest_id,
        unreconstructable_sources=tuple(missing),
        binding="unbound: manifest source selection is not tied to the captured "
                "prompt by any retained digest; see the module docstring",
    )
