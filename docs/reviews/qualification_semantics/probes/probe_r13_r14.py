#!/usr/bin/env python3
"""Offline baseline observations; synthetic fixtures, no qualification or admission.

Imports unchanged repository code with bytecode writing disabled. All synthetic
records are fixture data: no actual invocation, capture, corroboration or
independence is asserted. Outputs belong outside the repository.
"""
from __future__ import annotations

import argparse
import copy
from dataclasses import asdict
import hashlib
import itertools
import json
from pathlib import Path
import platform
import subprocess
import sys


EXPECTED_HEAD = "5515f55894b10ad70c321340257f67a960dcc382"
SOURCE_PATHS = (
    "ai_lab/providers/catalog.py",
    "ai_lab/providers/catalog_resolution.py",
    "ai_lab/providers/executor_equivalence.py",
    "ai_lab/providers/invocation_record.py",
    "ai_lab/documentation/verification_outcome.py",
    "tests/test_catalog.py",
    "tests/test_executor_equivalence.py",
    "docs/self_model/CATALOG_RECORDS.md",
    "docs/self_model/decisions/DECISION-20260814-0001.json",
    "docs/self_model/warrants/WARR-20260723-0001.json",
    "docs/abstractions/ABS-0004-invocation-authorization-ontology.md",
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo, output = args.repo.resolve(), args.output.resolve()
    if output.is_relative_to(repo):
        raise SystemExit("output must be outside the repository")
    head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    if head != EXPECTED_HEAD:
        raise SystemExit(f"unexpected baseline HEAD: {head}")
    source_hashes = {}
    for path in SOURCE_PATHS:
        working = (repo / path).read_bytes()
        committed = subprocess.check_output(["git", "-C", str(repo), "show", f"{head}:{path}"])
        if working != committed:
            raise SystemExit(f"source differs from baseline commit: {path}")
        source_hashes[path] = {"sha256": sha(working), "bytes": len(working)}
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(repo))
    from ai_lab.providers.catalog import (
        build_assertion, build_capture, build_endpoint_identity, build_model_identity,
        build_snapshot, validate_catalog_record,
    )
    from ai_lab.providers.catalog_resolution import resolve_identity
    from ai_lab.providers.executor_equivalence import equivalence
    from ai_lab.providers.invocation_record import build_invocation_record

    endpoints = {
        key: build_endpoint_identity(operating_organization=f"synthetic-{key}",
                                     endpoint_identifier=f"synthetic.{key}.endpoint")
        for key in ("a", "b")
    }
    models = {
        key: build_model_identity(originator_id=f"synthetic-{key}",
                                  canonical_name=f"synthetic-model-{key}", release_identity="r1")
        for key in ("a", "b")
    }

    def invocation(name: str, endpoint: str):
        return build_invocation_record(
            capture_path="scripts/compare_providers.py", executor_kind="model",
            executor_reference=name, identity_verification_status="unresolved",
            requested_model_name=name, service_endpoint=endpoint,
            session_id="synthetic-offline-probe", occurred_at="2026-07-20T12:00:00+00:00",
            rendered_prompt="SYNTHETIC FIXTURE ONLY; no model call occurred",
            session_state_mode="unknown_state", completeness_attestation="unknown",
            status="success", governance_marker="experimental",
        )

    invocations = {
        "left": invocation("alpha", endpoints["a"]["endpoint_identifier"]),
        "right": invocation("beta", endpoints["b"]["endpoint_identifier"]),
        "left_wrong_known_endpoint": invocation("alpha", endpoints["b"]["endpoint_identifier"]),
        "left_unbound_endpoint": invocation("alpha", "synthetic.unbound.endpoint"),
    }
    pairs = {}

    def pair(key, *, endpoint="a", subject="alpha", targets=("a",),
             content="self_asserted", observed="2026-07-19T00:00:00+00:00",
             valid_from="2026-05-01T00:00:00+00:00", valid_until=None):
        assertions = [build_assertion(
            assertion_subject=subject, assertion_predicate="resolves_to",
            assertion_value_or_target=models[target]["record_id"],
            valid_from=valid_from, valid_until=valid_until, source=f"synthetic:{key}",
        ) for target in targets]
        snapshot = build_snapshot(service_endpoint_id=endpoints[endpoint]["record_id"],
                                  observed_at=observed, assertions=assertions,
                                  source_set=json.dumps({"fixture": key, "assertions": assertions}, sort_keys=True))
        capture = build_capture(
            snapshot_id=snapshot["record_id"], capture_method="synthetic_offline_fixture",
            source_type="third_party_record" if content == "independently_corroborated" else "provider_self_report",
            captured_at=observed, capture_success=True, capturing_executor="tool:synthetic_fixture",
            payload=json.dumps(snapshot, sort_keys=True), channel_authentication_status="unverifiable",
            content_evidence_status=content,
        )
        pairs[key] = [snapshot, capture]

    pair("left_self")
    pair("left_corroborated", content="independently_corroborated")
    pair("right_corroborated", endpoint="b", subject="beta", targets=("b",), content="independently_corroborated")
    pair("left_conflicting_corroborated", targets=("b",), content="independently_corroborated")
    pair("applicable_contradicted", targets=("b",), content="contradicted")
    pair("applicable_ambiguous", targets=("a", "b"))
    pair("wrong_endpoint_conflict", endpoint="b", targets=("b",), content="independently_corroborated")
    pair("wrong_endpoint_contradicted", endpoint="b", targets=("b",), content="contradicted")
    pair("expired_contradicted", targets=("b",), content="contradicted", observed="2026-05-01T00:00:00+00:00")
    pair("after_event_contradicted", targets=("b",), content="contradicted", observed="2026-07-21T00:00:00+00:00")
    pair("other_name_contradicted", subject="gamma", targets=("b",), content="contradicted")
    pair("outside_interval_contradicted", targets=("b",), content="contradicted", valid_until="2026-07-19T23:59:59+00:00")
    pair("expired_clean", observed="2026-05-01T00:00:00+00:00")
    pair("after_event_clean", observed="2026-07-21T00:00:00+00:00")
    pair("other_name_clean", subject="gamma")
    for values in pairs.values():
        for record in values:
            validate_catalog_record(record)

    valid_pair_count = len(pairs)
    pairs["mismatched_capture"] = [pairs["left_corroborated"][0], pairs["right_corroborated"][1]]
    malformed = copy.deepcopy(pairs["left_corroborated"])
    malformed[0]["service_endpoint_id"] = ""
    pairs["malformed_snapshot"] = malformed
    observations = []

    def observe(label, api, inputs, operation):
        try:
            outcome = {"kind": "returned", "value": operation()}
        except Exception as exc:
            outcome = {"kind": "raised", "exception_type": type(exc).__name__, "message": str(exc)}
        observations.append({"label": label, "api": api, "inputs": inputs, "outcome": outcome})

    def single(label, invocation_key, pair_key):
        snapshot, capture = pairs[pair_key]
        observe(label, "resolve_identity", {"invocation": invocation_key, "pair": pair_key},
                lambda: resolve_identity(invocation=invocations[invocation_key], snapshot=snapshot, capture=capture))

    def compare(label, ordered_pairs, left="left"):
        def operation():
            result = equivalence(left=invocations[left], right=invocations["right"],
                                 snapshots=[pairs[key] for key in ordered_pairs])
            return {**asdict(result), "blocks_adjudication": result.blocks_adjudication}
        observe(label, "equivalence", {"left": left, "right": "right", "pairs": list(ordered_pairs)}, operation)

    single("positive_control_correct_endpoint", "left", "left_self")
    single("R13_known_other_endpoint", "left_wrong_known_endpoint", "left_self")
    single("R13_unbound_endpoint", "left_unbound_endpoint", "left_self")
    compare("R13_wrong_endpoint_synthetic_permission", ("left_corroborated", "right_corroborated"), "left_wrong_known_endpoint")
    for key in ("applicable_contradicted", "applicable_ambiguous", "wrong_endpoint_contradicted",
                "expired_contradicted", "after_event_contradicted", "other_name_contradicted",
                "outside_interval_contradicted", "expired_clean", "after_event_clean", "other_name_clean",
                "mismatched_capture", "malformed_snapshot"):
        single(f"single_{key}", "left", key)
    for key in ("applicable_contradicted", "applicable_ambiguous", "left_conflicting_corroborated",
                "left_self", "wrong_endpoint_conflict", "wrong_endpoint_contradicted",
                "expired_contradicted", "after_event_contradicted", "other_name_contradicted",
                "outside_interval_contradicted", "mismatched_capture", "malformed_snapshot"):
        for order in itertools.permutations((key, "left_corroborated", "right_corroborated")):
            compare(f"aggregate_with_{key}", order)

    for path, record in source_hashes.items():
        if sha((repo / path).read_bytes()) != record["sha256"]:
            raise SystemExit(f"source changed during probe: {path}")
    report = {
        "schema": "step3_r13_r14_baseline_probe_v1", "source_commit": head,
        "script_sha256": sha(Path(__file__).read_bytes()), "python_version": platform.python_version(),
        "method": "Unchanged baseline code; synthetic schema-valid records except explicitly marked malformed/mismatched cases; no provider calls or test/mutation suite runs; observations are not qualified verification.",
        "source_hashes": source_hashes,
        "fixtures": {"endpoints": endpoints, "models": models, "invocations": invocations, "snapshot_capture_pairs": pairs},
        "schema_valid_snapshot_capture_pairs": valid_pair_count,
        "negative_input_pairs": ["mismatched_capture", "malformed_snapshot"],
        "observations": observations,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output), "sha256": sha(output.read_bytes()),
                      "bytes": output.stat().st_size, "observations": len(observations),
                      "script_sha256": report["script_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
