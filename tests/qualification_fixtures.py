"""Real-byte, locally committed synthetic model fixtures for admitted 3A tests.

These constructors stipulate fictional evidence. They do not register a live
context/profile or establish executor identity, ancestry or independent review.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any, Callable

from ai_lab.providers.catalog import (
    build_assertion, build_capture, build_endpoint_identity, build_model_identity,
    build_snapshot, catalog_id_for, catalog_relative_path,
)
from ai_lab.providers.invocation_record import build_invocation_record, invocation_relative_path

VERSION = "ai_lab.qualification.r2/1"
ROOTS = ["docs/catalog/eid/", "docs/catalog/mid/", "docs/catalog/snap/",
         "docs/catalog/cap/", "docs/catalog/payloads/"]
OBSERVED = "2026-11-20T00:00:00+00:00"
SOURCE_AVAILABLE = "2026-11-20T00:00:01+00:00"
ASSESSED = "2026-11-20T01:00:00+00:00"
WITNESS_AVAILABLE = "2026-11-20T01:00:01+00:00"
EVENT = "2026-11-21T12:00:00+00:00"
LATE = "2026-11-22T00:00:00+00:00"


def encode(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def ref(path: str, data: bytes, record_id: str | None = None, *, git: bool = False) -> dict:
    return {"path": path, "sha256": digest(data), "record_id": record_id,
            "git_blob_sha1": blob_sha(data) if git else None}


def rref(identifier: str, data: bytes) -> dict:
    return {"record_id": identifier, "sha256": digest(data)}


def _git(root: Path, *argv: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *argv], text=True,
                                   stderr=subprocess.PIPE).strip()


def invocation(index: int, *, name: str | None = None, endpoint: str | None = None,
               occurred_at: str = EVENT, kind: str = "model") -> dict:
    return build_invocation_record(
        capture_path="scripts/compare_providers.py", executor_kind=kind,
        executor_reference=name or f"model-{index}", identity_verification_status="unresolved",
        requested_model_name=name or f"model-{index}",
        service_endpoint=endpoint or f"fixture.endpoint.{index}",
        session_id=f"SESSION-fixture-{index}", occurred_at=occurred_at,
        rendered_prompt=f"fictional invocation {index}", session_state_mode="stateless",
        completeness_attestation="partial_declared_channels_only", status="success", output_token_limit=8,
    )


def subject(record: dict, artifact: dict) -> dict:
    model = record["executor"]["kind"] == "model"
    return {"invocation_ref": artifact, "kind": record["executor"]["kind"],
            "executor_reference": record["executor"]["reference"],
            "occurred_at": record["occurred_at"],
            "requested_model_name": record["requested_model_name"] if model else None,
            "service_endpoint": record["service_endpoint"] if model else None}


def refresh_source_ids(source: dict) -> None:
    """Explicitly use when a test changes identity-bearing snapshot/capture fields."""
    source["snapshot"]["record_id"] = catalog_id_for(source["snapshot"])
    source["capture"]["snapshot_id"] = source["snapshot"]["record_id"]
    source["capture"]["record_id"] = catalog_id_for(source["capture"])


def extra_source(state: dict, *, side: int = 0, target: int | None = None,
                 endpoint: int | None = None, evidence: str = "self_asserted",
                 name: str = "extra") -> dict:
    endpoint = side if endpoint is None else endpoint
    target = side if target is None else target
    payload = encode({"fictional_source": name, "target": state["models"][target]["record_id"]})
    assertion = build_assertion(assertion_subject=state["invocations"][side]["requested_model_name"],
        assertion_predicate="resolves_to", assertion_value_or_target=state["models"][target]["record_id"],
        valid_from=OBSERVED, source=f"fixture {name}")
    snapshot = build_snapshot(service_endpoint_id=state["endpoints"][endpoint]["record_id"],
        observed_at=OBSERVED, assertions=[assertion], source_set=f"fixture source {name}")
    capture = build_capture(snapshot_id=snapshot["record_id"], capture_method="fixture",
        source_type="third_party_record", captured_at=OBSERVED, capture_success=True,
        capturing_executor="fixture:observer", payload=payload.decode(),
        channel_authentication_status="verified_current", content_evidence_status=evidence)
    result = {"name": name, "side": side, "snapshot": snapshot, "capture": capture,
              "payload": payload, "payload_present": True, "snapshot_present": True,
              "capture_present": True, "availability": True, "available_at": SOURCE_AVAILABLE}
    state["sources"].append(result)
    return result


@dataclass
class FixtureBundle:
    root: Path
    state: dict
    artifacts: dict[str, bytes]
    refs: dict[str, dict]
    inventory: dict
    context: dict
    fixture: dict
    query: dict
    source_refs: list[dict]
    witnesses: list[dict | None]

    @property
    def invocations(self) -> list[dict]:
        return self.state["invocations"]

    def seal(self) -> None:
        """Recompute only auxiliary record bytes/links after a contract mutation."""
        fixture_path = "fixture/fixture.json"
        self.artifacts[fixture_path] = encode(self.fixture)
        self.context["synthetic_fixture_ref"] = rref(self.fixture["fixture_id"], self.artifacts[fixture_path])
        inventory_path = "fixture/inventory.json"
        self.artifacts[inventory_path] = encode(self.inventory)
        self.context["inventory_ref"] = rref(self.inventory["inventory_id"], self.artifacts[inventory_path])
        context_path = "fixture/context.json"
        self.artifacts[context_path] = encode(self.context)
        self.query["evidence_context_ref"] = rref(self.context["context_id"], self.artifacts[context_path])

    def rewrite_aux(self, path: str, obj: dict | bytes, *, update_fixture_row: bool = True) -> None:
        """Rewrite real auxiliary bytes and all dependent refs, then reseal.

        Use this to build a coherent adversarial premise, not a fabricated digest.
        Frozen Git catalog files cannot be changed through this helper.
        """
        if any(path.startswith(root) for root in ROOTS):
            raise ValueError("catalog mutations must precede the Git commit")
        pending = [(path, copy.deepcopy(obj))]
        protected = {"fixture/context.json", "fixture/inventory.json", "fixture/fixture.json"}
        def replace(node, old, new):
            if isinstance(node, dict):
                if node == old:
                    node.clear(); node.update(copy.deepcopy(new)); return
                for value in node.values(): replace(value, old, new)
            elif isinstance(node, list):
                for value in node: replace(value, old, new)
        if update_fixture_row and isinstance(obj, dict):
            if obj.get("record_kind") == "availability_evidence":
                rows = self.fixture["model_witness_profile"]["availability_rows"]
                for n, row in enumerate(rows):
                    if row["availability_id"] == obj["availability_id"]: rows[n] = copy.deepcopy(obj)
            if obj.get("record_kind") == "corroboration_witness":
                rows = self.fixture["model_witness_profile"]["witness_rows"]
                for n, row in enumerate(rows):
                    if row["witness_id"] == obj["witness_id"]:
                        rows[n] = {k: copy.deepcopy(v) for k, v in obj.items()
                                   if k not in {"schema_version", "record_kind", "domain", "profile_id"}}
        seen = set()
        replacements = []
        while pending:
            current, value = pending.pop(0)
            # A dependency can be queued by multiple changed parents. Apply
            # earlier replacements again so a stale queue item cannot restore
            # an older sibling digest in an otherwise coherent fixture.
            for previous, revised in replacements:
                replace(value, previous, revised)
            data = value if isinstance(value, bytes) else encode(value)
            if self.artifacts.get(current) == data: continue
            old = copy.deepcopy(self.refs[current])
            new = ref(current, data, old["record_id"])
            replacements.append((old, copy.deepcopy(new)))
            self.artifacts[current] = data
            for node in [self.context, self.inventory, self.fixture, self.query, self.source_refs]:
                replace(node, old, new)
            self.refs[current] = new
            for other, retained in list(self.artifacts.items()):
                if other == current or other in protected or not other.startswith("fixture/"): continue
                try: parsed = json.loads(retained)
                except (ValueError, UnicodeDecodeError): continue
                before = encode(parsed)
                replace(parsed, old, new)
                if encode(parsed) != before:
                    marker = (other, digest(encode(parsed)))
                    if marker not in seen:
                        seen.add(marker); pending.append((other, parsed))
        self.seal()

    def anchor(self):
        from ai_lab.providers.qualification_records import load_synthetic_anchor
        return load_synthetic_anchor(self.root, context_ref=self.query["evidence_context_ref"],
                                     artifacts=self.artifacts)

    def evaluate(self) -> dict:
        from ai_lab.providers.qualification import evaluate_synthetic_r2
        return evaluate_synthetic_r2(self.query, anchor=self.anchor())


def build_fixture(
    tmp_path: Path, *, catalog_mutator: Callable[[dict], None] | None = None,
    contract_mutator: Callable[[FixtureBundle], None] | None = None,
    witness_states: tuple[str, str] = ("valid", "valid"),
    evidence_classes: tuple[str, str] = ("independently_corroborated", "independently_corroborated"),
    release_identities: tuple[str, str] = ("release-0", "release-1"),
) -> FixtureBundle:
    """Create an isolated Git tree and a complete externally pinned context.

    catalog_mutator edits fictional source inputs before Git commit; contract_mutator
    edits the separate consumer contract before its bytes/digest are pinned. Neither
    is a Query capability. Runtime tests mutate Query only when testing that boundary.
    """
    root = tmp_path / "catalog-repo"
    root.mkdir(parents=True)
    state = {
        "models": [build_model_identity(originator_id=f"fixture:originator:{i}",
            canonical_name=f"canonical-{i}", release_identity=release_identities[i]) for i in range(2)],
        "endpoints": [build_endpoint_identity(operating_organization=f"fixture:org:{i}",
            endpoint_identifier=f"fixture.endpoint.{i}") for i in range(2)],
        "invocations": [invocation(i) for i in range(2)], "sources": [],
        "extra_records": [], "missing_model_ids": set(), "extra_bytes": {},
    }
    for i in range(2):
        extra_source(state, side=i, evidence=evidence_classes[i], name=f"source-{i}")
    if catalog_mutator:
        catalog_mutator(state)
    records: dict[str, dict] = {}
    for item in state["endpoints"] + state["models"] + state["extra_records"]:
        if item["record_id"] not in state["missing_model_ids"]:
            records[catalog_relative_path(item["record_id"])] = item
    for s in state["sources"]:
        if s["snapshot_present"]:
            records[catalog_relative_path(s["snapshot"]["record_id"])] = s["snapshot"]
        if s["capture_present"]:
            records[catalog_relative_path(s["capture"]["record_id"])] = s["capture"]
    artifacts: dict[str, bytes] = {path: encode(obj) for path, obj in records.items()}
    for s in state["sources"]:
        s["payload_path"] = f"docs/catalog/payloads/{s['name']}.json"
        if s["payload_present"]:
            artifacts[s["payload_path"]] = s["payload"]
    for inv in state["invocations"]:
        artifacts[invocation_relative_path(inv["invocation_id"])] = encode(inv)
    artifacts.update(state["extra_bytes"])
    for path, data in artifacts.items():
        destination = root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    _git(root, "init", "-q")
    _git(root, "add", "--all")
    _git(root, "-c", "user.name=Qualification fixture", "-c", "user.email=fixture@ai-lab.invalid",
         "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null",
         "commit", "-qm", "fictional catalog source universe")
    commit, tree = _git(root, "rev-parse", "HEAD"), _git(root, "rev-parse", "HEAD^{tree}")
    refs = {path: ref(path, data, (records[path]["record_id"] if path in records else
                  next((i["invocation_id"] for i in state["invocations"]
                        if invocation_relative_path(i["invocation_id"]) == path), None)), git=True)
            for path, data in artifacts.items()}
    by_id = {r["record_id"]: r for r in refs.values() if r["record_id"] is not None}
    catalog_refs = sorted((r for r in refs.values() if any(r["path"].startswith(p) for p in ROOTS)),
                          key=lambda r: r["path"])

    def auxiliary(path: str, obj: Any, identifier: str | None = None) -> dict:
        data = encode(obj) if not isinstance(obj, bytes) else obj
        artifacts[path] = data
        result = ref(path, data, identifier)
        refs[path] = result
        return result

    observer = auxiliary("fixture/observer.json", {"fictional_observer": "observer"})
    rule = auxiliary("fixture/rule.json", {"rule": "SYN-MODEL-WITNESS-1", "version": 1})
    verifier = auxiliary("fixture/verifier.json", {"fictional_verifier": "checker"})
    verifier_version = auxiliary("fixture/verifier-version.json", {"version": "fixture-v1"})
    scope = auxiliary("fixture/scope.json", {"scope": "fictional model binding only"})
    availability_rows = []
    source_refs: list[dict] = []
    for index, s in enumerate(state["sources"]):
        # An unavailable snapshot cannot be represented by ModelSourceRef. Omit
        # the row and let the evaluator return a named refusal; never invent it.
        snap_ref = by_id.get(s["snapshot"]["record_id"])
        cap_ref = by_id.get(s["capture"]["record_id"])
        if snap_ref is None or cap_ref is None:
            continue
        payload_ref = refs.get(s["payload_path"])
        endpoint_refs = [by_id[s["snapshot"]["service_endpoint_id"]]] if s["snapshot"]["service_endpoint_id"] in by_id else []
        target_refs = []
        for a in s["snapshot"]["assertions"]:
            target = a["assertion_value_or_target"]
            if isinstance(target, str) and target in by_id:
                target_refs.append(by_id[target])
        availability_refs = []
        if s["availability"] and payload_ref is not None:
            observation = auxiliary(f"fixture/source-observation-{index}.json", {"source": s["name"], "fictional": True})
            av = {"schema_version": VERSION, "record_kind": "availability_evidence", "domain": "synthetic",
                  "availability_id": f"AV-source-{index}", "subject_refs": [snap_ref, cap_ref, payload_ref],
                  "available_at": s["available_at"], "observation_ref": observation,
                  "observer_executor_ref": observer, "rule_version_ref": rule}
            availability_refs.append(auxiliary(f"fixture/source-availability-{index}.json", av, av["availability_id"]))
            availability_rows.append(copy.deepcopy(av))
        source_refs.append({"source_id": s["capture"]["record_id"], "snapshot_ref": snap_ref,
            "capture_ref": cap_ref, "payload_ref": payload_ref, "endpoint_refs": endpoint_refs,
            "target_refs": sorted({encode(r): r for r in target_refs}.values(), key=encode),
            "availability_evidence_refs": availability_refs})

    witness_rows, witness_refs, witnesses = [], [], []
    for i, state_name in enumerate(witness_states):
        if state_name == "missing":
            witnesses.append(None)
            continue
        s = state["sources"][i]
        source = next((r for r in source_refs if r["source_id"] == s["capture"]["record_id"]), None)
        if source is None or source["payload_ref"] is None or not source["endpoint_refs"] or not source["target_refs"]:
            witnesses.append(None)
            continue
        target_ref = next((r for r in source["target_refs"] if r["record_id"].startswith("MID-")), source["target_refs"][0])
        witness_subject = {"endpoint_ref": source["endpoint_refs"][0],
            "requested_model_name": state["invocations"][i]["requested_model_name"],
            "target_model_ref": target_ref, "event_at": state["invocations"][i]["occurred_at"],
            "property_id": "model_reference_resolves_to_identity"}
        if state_name == "mismatched":
            witness_subject["requested_model_name"] = "different-name"
        evidence_refs = [source["capture_ref"], source["snapshot_ref"], source["payload_ref"], target_ref]
        verification = auxiliary(f"fixture/verification-{i}.json", {
            "profile_id": "SYN-MODEL-WITNESS-1", "subject": witness_subject,
            "evidence_refs": evidence_refs})
        witness = {"schema_version": VERSION, "record_kind": "corroboration_witness", "domain": "synthetic",
            "witness_id": f"WIT-{i}", "profile_id": "SYN-MODEL-WITNESS-1",
            "subject": witness_subject,
            "evidence_refs": evidence_refs,
            "verifier_executor_ref": verifier, "verifier_version_ref": verifier_version, "rule_version_ref": rule,
            "verification_ref": verification, "assessed_at": ASSESSED,
            "applicable_interval": {"valid_from": OBSERVED, "valid_until": None, "revoked_at": None},
            "assessment_scope_ref": scope}
        row = {k: copy.deepcopy(v) for k, v in witness.items() if k not in {"schema_version", "record_kind", "domain", "profile_id"}}
        witness_rows.append(row)
        witness_ref = auxiliary(f"fixture/witness-{i}.json", witness, witness["witness_id"])
        witness_refs.append(witness_ref)
        witnesses.append(witness)
        observation = auxiliary(f"fixture/witness-observation-{i}.json", {"witness": i, "fictional": True})
        av = {"schema_version": VERSION, "record_kind": "availability_evidence", "domain": "synthetic",
              "availability_id": f"AV-witness-{i}", "subject_refs": [witness_ref, verification],
              "available_at": WITNESS_AVAILABLE, "observation_ref": observation,
              "observer_executor_ref": observer, "rule_version_ref": rule}
        auxiliary(f"fixture/witness-availability-{i}.json", av, av["availability_id"])
        availability_rows.append(copy.deepcopy(av))

    inventory = {"schema_version": VERSION, "record_kind": "source_inventory", "domain": "synthetic",
        "inventory_id": "INVENTORY-fixture", "selector_id": "REPO-CATALOG-ALL-1", "repository": "MustafaAksu/ai-lab",
        "repository_commit": commit, "root_tree_sha1": tree, "catalog_roots": ROOTS.copy(),
        "entries": catalog_refs, "model_sources": source_refs, "known_source_declarations": [], "omission_declarations": []}
    fixture = {"schema_version": VERSION, "record_kind": "synthetic_fixture_bindings", "domain": "synthetic",
        "fixture_id": "FIXTURE-model", "fixture_artifact_refs": list(refs.values()),
        "tool_profile": {"profile_id": "SYN-TOOL-1", "namespace": "fixture:tools", "issuer_rows": [], "release_rows": [], "alias_rows": [], "execution_rows": []},
        "human_profile": {"profile_id": "SYN-HUMAN-1", "namespace": "fixture:human-persons", "principal_rows": [], "alias_rows": [], "actor_rows": []},
        "model_witness_profile": {"profile_id": "SYN-MODEL-WITNESS-1", "witness_rows": witness_rows, "availability_rows": availability_rows},
        "c3_conflict_fixture": {"rule_id": "SYN-C3-CONFLICT-1", "context_rows": []}}
    invocation_refs = [by_id[inv["invocation_id"]] for inv in state["invocations"]]
    context = {"schema_version": VERSION, "record_kind": "evidence_context", "domain": "synthetic", "context_id": "CTX-fixture",
        "inventory_ref": {}, "context_policy": {"selector_id": "REPO-CATALOG-ALL-1", "mode": "event_time", "knowledge_cutoff": EVENT,
            "freshness_window_days": 30,
            "production_profiles": {k: [] for k in ["endpoint_binding", "model_witness", "tool_binding", "human_binding", "ancestry", "availability"]},
            "synthetic_profiles": {"model_witness": ["SYN-MODEL-WITNESS-1"], "tool_binding": ["SYN-TOOL-1"], "human_binding": ["SYN-HUMAN-1"], "ancestry": []}},
        "subject_refs": invocation_refs, "selected_source_ids": [r["source_id"] for r in source_refs],
        "provided_artifact_refs": list(refs.values()), "known_source_declaration_refs": [], "omission_declaration_refs": [],
        "corroboration_witness_refs": witness_refs, "synthetic_fixture_ref": {}, "c3_context": None, "c10_context": None}
    query = {"schema_version": VERSION, "record_kind": "query", "domain": "synthetic", "query_id": "QUERY-fixture",
        "entry_point": "evaluate_synthetic_r2", "evidence_context_ref": {},
        "left": subject(state["invocations"][0], invocation_refs[0]),
        "right": subject(state["invocations"][1], invocation_refs[1])}
    result = FixtureBundle(root, state, artifacts, refs, inventory, context, fixture, query, source_refs, witnesses)
    if contract_mutator:
        contract_mutator(result)
    result.seal()
    return result
