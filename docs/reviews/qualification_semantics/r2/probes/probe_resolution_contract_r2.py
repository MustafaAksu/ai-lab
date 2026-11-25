#!/usr/bin/env python3
"""Offline r2 source-behavior probes; synthetic data, not qualified evidence.

No repository writes or provider calls. The two writer probes use only the
explicit external scratch output directory. R1 artifacts are read and hashed.
"""
from __future__ import annotations

import argparse
import copy
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys


HEAD = "8b8e24d133eaa3a585eefa14e76a02a519b73b03"
RUNTIME_BASELINE = "5515f55894b10ad70c321340257f67a960dcc382"
SOURCE_PATHS = (
    "ai_lab/providers/catalog.py",
    "ai_lab/providers/catalog_resolution.py",
    "ai_lab/providers/executor_equivalence.py",
    "ai_lab/providers/invocation_record.py",
    "ai_lab/providers/catalog_capture.py",
    "ai_lab/providers/catalog_transport.py",
    "ai_lab/documentation/verification_outcome.py",
    "ai_lab/documentation/graph_neighborhood.py",
    "tests/test_catalog.py",
    "tests/test_executor_equivalence.py",
    "tests/test_catalog_transport.py",
    "docs/self_model/CATALOG_RECORDS.md",
    "docs/self_model/decisions/DECISION-20260814-0001.json",
    "docs/self_model/warrants/WARR-20260723-0001.json",
    "docs/abstractions/ABS-0004-invocation-authorization-ontology.md",
)
R1_HASHES = {
    "probe_r13_r14.py": "5c1be890715584481898bd4df7cecb33c50b193da4b0c1da9398caa769e11bf7",
    "r13_r14_baseline.json": "7f8640d7fa4ccf27865d667a7c7c292aec0b8c341f02193f91fb3f92c7c9a6e1",
    "r13_r14_reproduction.json": "3e05154e11e5b08280aa8ff2af7869ce2a17472fc7812c917b982797f6d399b7",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo, output = args.repo.resolve(), args.output.resolve()
    if output.is_relative_to(repo):
        raise SystemExit("all outputs must be outside the repository")
    head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    if head != HEAD:
        raise SystemExit(f"unexpected baseline HEAD {head}")
    source_hashes = {}
    for path in SOURCE_PATHS:
        working = (repo / path).read_bytes()
        baseline = subprocess.check_output(["git", "-C", str(repo), "show", f"{RUNTIME_BASELINE}:{path}"])
        if working != baseline:
            raise SystemExit(f"source changed from runtime baseline: {path}")
        source_hashes[path] = {"bytes": len(working), "sha256": sha(working)}
    r1_before = {}
    for name, expected in R1_HASHES.items():
        path = repo / "docs/reviews/qualification_semantics/probes" / name
        content = path.read_bytes()
        if sha(content) != expected:
            raise SystemExit(f"R1 artifact differs: {name}")
        r1_before[name] = {"bytes": len(content), "sha256": sha(content)}
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(repo))
    from ai_lab.providers.catalog import (
        build_endpoint_identity, build_model_identity, catalog_id_for,
        canonical_catalog_json, digest_text, validate_catalog_record,
    )
    from ai_lab.providers.catalog_resolution import (
        resolve_identity, build_resolution_record, validate_resolution_record,
        resolution_relations, write_resolution_record, canonical_resolution_json,
    )
    from ai_lab.providers.executor_equivalence import equivalence, EquivalenceResult
    from ai_lab.providers.invocation_record import build_invocation_record
    from ai_lab.providers.catalog_capture import write_catalog_records

    endpoint = build_endpoint_identity(operating_organization="synthetic", endpoint_identifier="synthetic.endpoint")
    models = {name: build_model_identity(originator_id="synthetic", canonical_name=name,
                                        release_identity=release)
              for name, release in (("model-a", "r1"), ("model-b", "r1"), ("model-unknown", "unknown"))}

    def invocation(name):
        return build_invocation_record(
            capture_path="scripts/compare_providers.py", executor_kind="model", executor_reference=name,
            identity_verification_status="unresolved", requested_model_name=name,
            service_endpoint=endpoint["endpoint_identifier"], session_id="synthetic-r2-probe",
            occurred_at="2026-07-20T12:00:00+00:00", rendered_prompt="SYNTHETIC ONLY; no actual invocation",
            session_state_mode="unknown_state", completeness_attestation="unknown", status="success",
        )

    invocations = {"left": invocation("alpha"), "right": invocation("beta")}
    pairs = {}

    def pair(name, *, targets=None, subject="alpha", assertion_fields=None, capture_fields=None,
             observed="2026-07-19T00:00:00+00:00", remove_assertion_fields=()):
        if targets is None:
            targets = [models["model-a"]["record_id"]]
        assertions = []
        for target in targets:
            a = {"assertion_subject": subject, "assertion_predicate": "resolves_to",
                 "assertion_value_or_target": target, "unit": None, "scope": None,
                 "valid_from": "2026-07-01T00:00:00+00:00", "valid_until": None,
                 "superseded_by": None, "source": f"synthetic:{name}"}
            a.update(assertion_fields or {})
            for field in remove_assertion_fields:
                a.pop(field)
            assertions.append(a)
        snapshot = {"schema_version": "v1", "record_kind": "catalog_snapshot",
                    "service_endpoint_id": endpoint["record_id"], "observed_at": observed,
                    "source_set_digest": digest_text(json.dumps({"case": name, "assertions": assertions}, sort_keys=True)),
                    "assertions": assertions}
        snapshot["record_id"] = catalog_id_for(snapshot)
        capture = {"schema_version": "v1", "record_kind": "catalog_capture",
                   "snapshot_id": snapshot["record_id"], "capture_method": "synthetic_offline_fixture",
                   "source_type": "third_party_record", "captured_at": observed,
                   "capture_success": True, "capturing_executor": "tool:synthetic_fixture",
                   "content_digest": digest_text(json.dumps(snapshot, sort_keys=True)),
                   "content_evidence_status": "independently_corroborated",
                   "channel_authentication_status": "unverifiable"}
        capture.update(capture_fields or {})
        capture["record_id"] = catalog_id_for(capture)
        pairs[name] = [snapshot, capture]

    pair("positive_mid")
    pair("right_mid", subject="beta", targets=[models["model-b"]["record_id"]])
    pair("capture_success_false", capture_fields={"capture_success": False})
    pair("capture_success_non_boolean", capture_fields={"capture_success": "false"})
    for name, target in (
        ("target_dangling_mid", "MID-0000000000000000"),
        ("target_wrong_kind_eid", endpoint["record_id"]),
        ("target_non_mid_string", "not-a-model-id"),
        ("target_integer", 7), ("target_zero", 0), ("target_true", True),
        ("target_false", False), ("target_float", 1.5), ("target_empty_string", ""),
        ("target_null", None), ("target_list", ["MID-0000000000000000"]),
        ("target_unknown_release", models["model-unknown"]["record_id"]),
    ):
        pair(name, targets=[target])
    pair("mixed_scalar_ambiguity", targets=[7, "not-a-model-id"])
    pair("boolean_integer_target_collapse", targets=[True, 1])
    pair("scope_unsupported_string", assertion_fields={"scope": "uninterpreted-region-and-profile"})
    pair("scope_unsupported_object", assertion_fields={"scope": {"region": "uninterpreted"}})
    pair("reversed_interval", assertion_fields={"valid_from": "2026-07-21T00:00:00+00:00", "valid_until": "2026-07-19T00:00:00+00:00"})
    pair("zero_length_interval_control", assertion_fields={"valid_from": invocations["left"]["occurred_at"], "valid_until": invocations["left"]["occurred_at"]})
    pair("invalid_interval_timestamp", assertion_fields={"valid_until": "not-a-timestamp"})
    pair("missing_interval_field", remove_assertion_fields=("valid_until",))
    pair("capture_after_event", capture_fields={"captured_at": "2026-07-21T00:00:00+00:00"})
    pair("capture_before_observation", capture_fields={"captured_at": "2026-07-18T00:00:00+00:00"})
    pair("snapshot_after_event_control", observed="2026-07-21T00:00:00+00:00")
    pair("superseded_by_uninterpreted", assertion_fields={"superseded_by": "uninterpreted-source-reference"})

    observations, annotations = [], {}

    def observe(label, api, inputs, operation):
        try:
            outcome = {"kind": "returned", "value": operation()}
        except Exception as exc:
            outcome = {"kind": "raised", "exception_type": type(exc).__name__, "message": str(exc)}
        observations.append({"label": label, "api": api, "inputs": inputs, "outcome": outcome})
        return outcome

    def compare(order):
        result = equivalence(left=invocations["left"], right=invocations["right"], snapshots=[pairs[k] for k in order])
        return {**asdict(result), "blocks_adjudication": result.blocks_adjudication}

    for name, (snapshot, capture) in pairs.items():
        if name == "right_mid":
            continue
        observe(name, "validate_catalog_record(snapshot)", {"pair": name}, lambda s=snapshot: validate_catalog_record(s))
        observe(name, "validate_catalog_record(capture)", {"pair": name}, lambda c=capture: validate_catalog_record(c))
        resolved = observe(name, "resolve_identity", {"pair": name, "invocation": "left"},
                           lambda s=snapshot, c=capture: resolve_identity(invocation=invocations["left"], snapshot=s, capture=c))
        for order in ((name, "right_mid"), ("right_mid", name)):
            observe(name, "equivalence", {"pairs": list(order), "left": "left", "right": "right"}, lambda o=order: compare(o))
        if resolved["kind"] == "returned":
            annotation = observe(name, "build_resolution_record", {"source_observation": name, "resolved_at": "2026-07-22T00:00:00+00:00"},
                                 lambda r=resolved["value"]: build_resolution_record(invocation=invocations["left"], outcome=r, resolved_at="2026-07-22T00:00:00+00:00"))
            if annotation["kind"] == "returned":
                annotations[name] = annotation["value"]
                observe(name, "resolution_relations", {"annotation": name},
                        lambda a=annotation["value"]: [asdict(x) for x in resolution_relations(a)])

    # Target records cannot be supplied to either legacy resolver interface.
    # Preserve the missing/conflicting records to expose that structural boundary.
    target_evidence = {"valid": models["model-a"], "unknown_release": models["model-unknown"]}
    target_evidence["same_id_extra_bytes"] = {**models["model-a"], "uninterpreted_note": "different retained bytes"}
    target_evidence["same_id_changed_release"] = {**models["model-a"], "release_identity": "r2"}
    target_evidence["wrong_kind"] = endpoint
    for name, record in target_evidence.items():
        observe(name, "validate_catalog_record(target)", {"target_evidence": name}, lambda r=record: validate_catalog_record(r))
    for context in ("no_target_registry", "valid_target_registry", "conflicting_same_id_bytes", "invalid_target_record"):
        observe(context, "resolve_identity(no target-registry parameter)",
                {"pair": "positive_mid", "target_evidence_context_not_consumed_by_api": context},
                lambda: resolve_identity(invocation=invocations["left"], snapshot=pairs["positive_mid"][0], capture=pairs["positive_mid"][1]))

    fake_outcome = {"resolved": True, "resolved_identity": "not-a-model-id",
                    "snapshot_id": "not-a-snapshot-id", "capture_id": "not-a-capture-id",
                    "content_evidence_status": "not-a-valid-evidence-enum", "channel_authentication_status": "not-a-valid-channel-enum"}
    fabricated = observe("fabricated_outcome", "build_resolution_record", {"outcome": fake_outcome},
                         lambda: build_resolution_record(invocation=invocations["left"], outcome=fake_outcome, resolved_at="2026-07-22T00:00:00+00:00"))
    observe("truthy_non_boolean_resolution", "build_resolution_record", {"outcome": {**fake_outcome, "resolved": "false"}},
            lambda: build_resolution_record(invocation=invocations["left"], outcome={**fake_outcome, "resolved": "false"}, resolved_at="2026-07-22T00:00:00+00:00"))
    observe("direct_boolean_without_identities", "EquivalenceResult.blocks_adjudication", {"status": "non_equivalent", "left_identity": None, "right_identity": None, "evidence_classes": "synthetic corroborated enum on both sides"},
            lambda: EquivalenceResult("non_equivalent", "synthetic_direct_construction", left_evidence_class="independently_corroborated", right_evidence_class="independently_corroborated").blocks_adjudication)

    writer_root = output.parent / "writer-sandbox"
    writer_root.mkdir(parents=True, exist_ok=True)

    def annotation_overwrite():
        original = annotations["positive_mid"]
        changed = {**original, "resolved_identity": models["model-b"]["record_id"]}
        validate_resolution_record(changed)
        path = write_resolution_record(original, writer_root / "resolution")
        before = path.read_bytes()
        path2 = write_resolution_record(changed, writer_root / "resolution")
        after = path2.read_bytes()
        return {"same_record_id": original["record_id"] == changed["record_id"], "same_path": path == path2,
                "relative_path": str(path.relative_to(output.parent)), "before_sha256": sha(before), "after_sha256": sha(after),
                "overwritten": before != after, "before_record": original, "after_record": changed}

    observe("same_id_resolution_overwrite", "write_resolution_record", {"output_root": "writer-sandbox/resolution"}, annotation_overwrite)

    def catalog_overwrite():
        original = pairs["positive_mid"][1]
        changed = {**original, "capture_success": False}
        validate_catalog_record(changed)
        path = write_catalog_records([original], writer_root / "catalog")[0]
        before = path.read_bytes()
        path2 = write_catalog_records([changed], writer_root / "catalog")[0]
        after = path2.read_bytes()
        return {"same_record_id": original["record_id"] == changed["record_id"], "same_path": path == path2,
                "relative_path": str(path.relative_to(output.parent)), "before_sha256": sha(before), "after_sha256": sha(after),
                "overwritten": before != after, "before_record": original, "after_record": changed}

    observe("same_id_catalog_overwrite", "write_catalog_records", {"output_root": "writer-sandbox/catalog"}, catalog_overwrite)
    if fabricated["kind"] == "returned":
        def write_fabricated():
            path = write_resolution_record(fabricated["value"], writer_root / "fabricated")
            return {"relative_path": str(path.relative_to(output.parent)), "sha256": sha(path.read_bytes()), "record": json.loads(path.read_text())}
        observe("fabricated_annotation_write", "write_resolution_record", {"output_root": "writer-sandbox/fabricated"}, write_fabricated)

    for path, record in source_hashes.items():
        if sha((repo / path).read_bytes()) != record["sha256"]:
            raise SystemExit(f"source changed during probe: {path}")
    for name, expected in R1_HASHES.items():
        if sha((repo / "docs/reviews/qualification_semantics/probes" / name).read_bytes()) != expected:
            raise SystemExit(f"R1 artifact changed during probe: {name}")
    report = {"schema": "step3_resolution_contract_r2_baseline_v1", "checkout_commit": head,
              "runtime_source_commit": RUNTIME_BASELINE, "python_version": platform.python_version(),
              "script_sha256": sha(Path(__file__).read_bytes()), "source_hashes": source_hashes,
              "r1_artifacts_before_and_after_identical": r1_before,
              "method": "Unchanged baseline code; synthetic fixtures and enum labels only. No provider calls, live qualification, admission or pytest/mutation campaign. Writer probes write only under the external output directory. Target-evidence context is explicitly not consumed by the legacy API.",
              "fixtures": {"endpoint": endpoint, "models": models, "invocations": invocations,
                           "snapshot_capture_pairs": pairs, "target_evidence": target_evidence},
              "observations": observations}
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output), "bytes": output.stat().st_size, "sha256": sha(output.read_bytes()),
                      "observations": len(observations), "pairs": len(pairs), "script_sha256": report["script_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
