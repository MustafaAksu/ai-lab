"""Targeted falsification of admitted Step 3A guards (WARR-20261126-0001).

Each mutation must first select passing baseline tests. The identical nodeids
must run after mutation, with ordinary call-phase assertions failing. Collection,
setup/teardown, runtime exceptions, usage/internal errors and timeouts never count
as caught. The strict VERIFY v2 harness is reused without modifying its history.

    python -I scripts/falsify_qualification_3a.py . --report /tmp/qualification-3a.json

The complete baseline/mutant outputs, pytest phase reports and exact failed
nodeids are retained in JSON. These selected guard mutations are not a claim
that all 48 r2 falsifier families, 3B or 3C have been implemented or executed.
The source repository is observed and copied; its files are never mutated.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys
import tempfile


_harness_spec = importlib.util.spec_from_file_location(
    "qualification_strict_falsification_harness",
    Path(__file__).resolve().with_name("falsify_verify_v2.py"))
_harness = importlib.util.module_from_spec(_harness_spec)
_harness_spec.loader.exec_module(_harness)

ENGINE = "ai_lab/providers/qualification.py"
TESTS = "tests/test_qualification_model.py"
REPORT_SCHEMA = "qualification-3a-falsification-v1"


def mutation(name, old, new, selector):
    return (name, ENGINE, old, new, selector, TESTS)


MUTATIONS = [
    mutation("F14 snapshot endpoint binding skipped",
        '            elif snap["service_endpoint_id"] != side.endpoint["record_id"]:',
        '            elif False:',
        "test_f14_wrong_endpoint_cannot_resolve_same_requested_name"),
    mutation("F32 failed capture accepted",
        '            elif not cap["capture_success"]:', '            elif False:',
        "test_f32_failed_capture_cannot_supply_positive_or_name_absence"),
    mutation("F36/F29 unsupported scope and supersession treated as wildcard",
        '                elif any(a["scope"] is not None or a["superseded_by"] is not None for a in active):',
        '                elif False:',
        "test_f36_null_scope_control_and_unsupported_scope or test_f29_supersession_is_not_newest_source_override"),
    mutation("F22 applicable contradicted capture ignored",
        '                    if cap["content_evidence_status"] == "contradicted":',
        '                    if False:',
        "test_f02_f24_f43_evidence_class_pair_matrix and contradicted"),
    mutation("F24 aggregation stops at first target",
        '                        targets.update(local_targets)\n'
        '                        if state == "available":\n'
        '                            strict_targets.update(local_targets)',
        '                        if not targets:\n'
        '                            targets.update(local_targets)\n'
        '                        if state == "available":\n'
        '                            if not strict_targets:\n'
        '                                strict_targets.update(local_targets)',
        "test_f24_cross_source_disagreement_survives_corroboration"),
    mutation("F42 selected source pruning accepted",
        '        if set(self.context["selected_source_ids"]) != set(captures):',
        '        if False:',
        "test_f42_selected_sources_cannot_prune_pinned_inventory"),
    mutation("A1/F42 source target manifest not checked",
        '            if _unique(row["target_refs"]) != _unique(targets):',
        '            if False:',
        "test_a1_f42_source_target_manifest_cannot_drop_decoded_target"),
    mutation("F34 capture payload digest not checked",
        '                if payload is not None and sha256(payload) != cap["content_digest"]:',
        '                if False:',
        "test_f34_payload_hash_mismatch_is_not_corroboration"),
    mutation("F35 unknown release receives witness qualification",
        '        if side.clean is None or side.clean["version_identity"] == "unknown":',
        '        if side.clean is None:',
        "test_f35_unknown_release_blocks_identity_not_catalog_relation"),
    mutation("A1/F38 availability may refer to other artifacts",
        '            if not required.issubset({canonical_bytes(x) for x in value["subject_refs"]}):',
        '            if False:',
        "test_a1_f38_missing_witness_availability_is_not_assessed_at"),
    mutation("A1/F38 late witness availability accepted",
        '            elif moment > bound:', '            elif False:',
        "test_a1_f38_late_witness_not_cleared_by_early_assessed_at"),
    mutation("A1/F43 witness accepts wrong source payload",
        '                    and all(canonical_bytes(x) in evidence for x in chain)):',
        '                    and True):',
        "test_a1_f43_witness_payload_from_other_side_is_rejected"),
    mutation("A1/F43 corroborated label borrowed from another source",
        '                if (cap["content_evidence_status"] == "independently_corroborated"',
        '                if (True',
        "test_a1_f43_borrowed_corroboration_label_cannot_qualify_other_chain"),
    mutation("A1/F43 concrete verification premise not checked",
        '            if verification != expected_verification:', '            if False:',
        "test_a1_f43_verification_premise_is_bound_to_exact_chain"),
    mutation("F43 harness proof row binding skipped",
        '            if canonical_bytes(row_value) not in {canonical_bytes(x) for x in rows}:',
        '            if False:',
        "test_f43_proof_row_pins_checker_rule_version_and_scope"),
    mutation("F43 revocation boundary incorrectly exclusive",
        'interval["revoked_at"] is not None and event >= parse_timestamp(interval["revoked_at"])',
        'interval["revoked_at"] is not None and event > parse_timestamp(interval["revoked_at"])',
        "test_f43_witness_revocation_boundary"),
    mutation("A2 successful missing payload accepted without omission",
        '            if cap["capture_success"] and payload_ref is None and not self._declared_missing(digest=cap["content_digest"]):',
        '            if False:',
        "test_f34_missing_chain_never_invents_refs and payload"),
    mutation("A2 orphan snapshot silently dropped",
        '            if snapshot["record_kind"] == "catalog_snapshot" and identifier not in captured_snapshots:',
        '            if False:',
        "test_a2_f42_orphan_snapshot_cannot_be_silently_dropped"),
    mutation("F43 conflicting proof-row identities accepted",
        '                if len(values) > 1:', '                if False:',
        "test_f43_duplicate_conflicting_fixture_row_identity_is_invalid"),
    mutation("F38 malformed availability hidden by endpoint exclusion",
        '            self._availability_chronology(value, ref)', '            pass',
        "test_f38_availability_chronology_checked_before_endpoint_exclusion"),
]


def run_mutations(repo: Path, *, timeout: float = 120, python: str = sys.executable) -> dict:
    report = _harness.run_mutations(repo, MUTATIONS, timeout=timeout, python=python)
    report["classification_harness_schema"] = report["schema"]
    report["schema"] = REPORT_SCHEMA
    report["scope"] = "admitted 3A model and refusal guards; synthetic only; no 3B/3C or authority"
    report["falsifier_family_claim"] = "targeted admitted subset, not all 48 planned r2 families"
    for result in report["results"]:
        result["group"] = "qualification_3a"
    report["summary"]["groups"] = {"qualification_3a": {
        "mutations": report["summary"]["mutations"], "caught": report["summary"]["caught"]}}
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path, nargs="?", default=Path("."))
    parser.add_argument("--timeout", type=float, default=120, help="timeout per selected pytest process")
    parser.add_argument("--report", type=Path, help="complete retained evidence outside the source repository")
    args = parser.parse_args(argv)
    repo = args.repo.resolve()
    destination = args.report.resolve() if args.report is not None else None
    if destination is not None and destination.is_relative_to(repo):
        parser.error("--report must be outside the source repository")
    try:
        report = run_mutations(repo, timeout=args.timeout)
    except (_harness.HarnessError, OSError, ValueError) as exc:
        report = {"schema": REPORT_SCHEMA, "error": f"{type(exc).__name__}: {exc}"}
        code = 2
    else:
        for result in report["results"]:
            print(f"{result['name']} | {result['status']} | {result['reason']}", file=sys.stderr)
        print(json.dumps(report["summary"]), file=sys.stderr)
        code = 0 if report["summary"]["not_caught"] == 0 else 1
    content = json.dumps(report, indent=2, ensure_ascii=True) + "\n"
    if destination is None:
        print(content, end="")
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=destination.parent,
                                         prefix=destination.name + ".", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
        try:
            temporary.replace(destination)
        finally:
            temporary.unlink(missing_ok=True)
        print(f"Evidence: {destination}", file=sys.stderr)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
