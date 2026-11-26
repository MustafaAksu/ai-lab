"""Admitted Step 3A model evidence evaluation (WARR-20261126-0001).

Query cannot select the source universe, policy or trust domain. The separate
harness loader freezes a complete Git tree and evidence context first. This
module reads only those bytes, consults no clock and performs no I/O. It does
not implement tool/human binding, C3/C10 evaluation, or authority activation.
Catalog-record equality is not affirmative real-executor equivalence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any

from ai_lab.providers.catalog import catalog_id_for
from ai_lab.providers.invocation_record import validate_invocation_record
from ai_lab.providers.qualification_records import (
    SCHEMA_VERSION, EvidenceAnchor, QualificationError, canonical_bytes,
    parse_timestamp, reason_codes, record_ref, require_qualification_schema,
    sha256, strict_loads, validate_shape,
)


def _unique(items):
    """Exact duplicates are idempotent; no equality coercion or first winner."""
    return [item for _, item in sorted({canonical_bytes(x): x for x in items}.items())]


def _record_refs(refs):
    return _unique([
        {"record_id": r["record_id"], "sha256": r["sha256"]}
        for r in refs if isinstance(r, dict) and r.get("record_id") is not None
        and "sha256" in r
    ])


def reason(code, detail, *, stage=3, side="none", refs=()):
    return {"code": code, "stage": stage, "side": side,
            "subject_refs": _record_refs(refs),
            "detail": str(detail).replace("\x00", "")[:1024]}


def canonicalize_reasons(items):
    """A3 total order, including complete canonical diagnostic bytes at ties."""
    order = {code: i for i, code in enumerate(reason_codes())}
    normalized = []
    for item in items:
        item = dict(item)
        item["subject_refs"] = _unique(item["subject_refs"])
        validate_shape(item, "Reason")
        normalized.append(item)
    return sorted(_unique(normalized), key=lambda x: (
        x["stage"], order[x["code"]], x["side"],
        canonical_bytes(x["subject_refs"]), canonical_bytes(x),
    ))


def _constraint():
    return {"value": "unresolved", "reasons": [reason(
        "NOT_EVALUATED", "3C is not admitted; Step 3A evaluates no ancestry or C3/C10 condition",
        stage=7)]}


def _empty_relation(reasons=()):
    return {"value": "unresolved", "left_identity": None, "right_identity": None,
            "reasons": canonicalize_reasons(reasons)}


def _finish(result):
    # Identity is over the complete deterministic output excluding its own ID.
    result["assessment_id"] = "QASSESS-" + sha256(canonical_bytes(result)).split(":")[1]
    validate_shape(result, "AssessmentResult")
    return result


def _invalid(domain, errors):
    reasons = canonicalize_reasons(errors)
    return _finish({
        "schema_version": SCHEMA_VERSION, "record_kind": "assessment_result",
        "domain": domain, "entry_point": f"evaluate_{domain}_r2",
        "query_ref": None, "evidence_context_ref": None,
        "validation_status": "invalid", "validation_reasons": reasons,
        "supplied_relation": _empty_relation(reasons), "R_identity": _empty_relation(reasons),
        "Q_identity": {"value": "withheld", "reasons": reasons},
        "C3": _constraint(), "C10": _constraint(), "Q_C3_C10": _constraint(),
        "coverage": {"value": "undetermined", "inventory_ref": None,
                     "omission_refs": [], "reasons": reasons},
        "source_findings": [], "corroboration_witness_refs": [],
        "shared_ancestry_evidence_refs": [],
    })


def _error_reason(exc, side="none"):
    return reason(exc.code, exc.detail, stage=exc.stage, side=side, refs=exc.refs)


@dataclass
class _Side:
    subject: dict
    side: str
    declared: dict | None = None
    clean: dict | None = None
    endpoint: dict | None = None
    sources: list = field(default_factory=list)
    reasons: list = field(default_factory=list)
    unknown: bool = False


class _Evaluation:
    def __init__(self, query, query_bytes, anchor):
        self.query, self.query_bytes, self.anchor = query, query_bytes, anchor
        self.context, self.inventory = anchor.context, anchor.inventory
        self.policy = self.context["context_policy"]
        self.errors, self.findings, self.coverage_reasons, self.omission_refs = [], [], [], []
        self.catalog, self.refs, self.source_rows = {}, {}, []
        self.fixture = None
        self.witnesses, self.availability = [], []
        self.sides = [_Side(query[name], name) for name in ("left", "right")]
        self.cutoff = parse_timestamp(self.policy["knowledge_cutoff"])

    def error(self, code, detail, *, stage=1, refs=(), side="none"):
        self.errors.append(reason(code, detail, stage=stage, refs=refs, side=side))

    def read(self, ref, definition=None):
        try:
            return self.anchor.record(ref, definition)
        except QualificationError as exc:
            self.errors.append(_error_reason(exc))
            return None

    def bytes(self, ref):
        try:
            return self.anchor.read(ref)
        except QualificationError as exc:
            self.errors.append(_error_reason(exc))
            return None

    def interval(self, start, end, *, refs=()):
        if end is not None and parse_timestamp(end) < parse_timestamp(start):
            self.error("INVALID_INTERVAL", "interval upper bound precedes lower bound", refs=refs)
            return False
        return True

    def prepare(self):
        if self.query["evidence_context_ref"] != self.anchor.context_ref:
            self.error("CONTEXT_ANCHOR_MISMATCH", "Query cannot replace the pinned consumer context")
        subject_refs = {canonical_bytes(x) for x in self.context["subject_refs"]}
        for side in self.sides:
            sub = side.subject
            if canonical_bytes(sub["invocation_ref"]) not in subject_refs:
                self.error("CONTEXT_ANCHOR_MISMATCH", "subject is absent from the pinned context", side=side.side)
            inv = self.read(sub["invocation_ref"])
            if inv is None:
                continue
            try:
                validate_invocation_record(inv)
            except (ValueError, TypeError, KeyError) as exc:
                self.error("INVALID_SCHEMA", f"invalid retained invocation: {exc}", refs=[sub["invocation_ref"]])
                continue
            expected = {
                "kind": inv["executor"]["kind"], "executor_reference": inv["executor"]["reference"],
                "occurred_at": inv["occurred_at"],
                "requested_model_name": inv["requested_model_name"] if inv["executor"]["kind"] == "model" else None,
                "service_endpoint": inv["service_endpoint"] if inv["executor"]["kind"] == "model" else None,
            }
            if any(sub[k] != value for k, value in expected.items()):
                self.error("CONTEXT_ANCHOR_MISMATCH", "Query subject differs from retained invocation bytes", side=side.side)
            if self.policy["mode"] == "retrospective" and self.cutoff < parse_timestamp(sub["occurred_at"]):
                self.error("INVALID_TIMESTAMP", "retrospective cutoff precedes the subject event", side=side.side)
        for ref in _unique(self.context["provided_artifact_refs"]):
            self.bytes(ref)
        self._catalog()
        self._sources()
        self._fixture()
        self._declarations()

    def _catalog(self):
        definitions = {"eid": "CatalogEID", "mid": "CatalogMID", "snap": "CatalogSnapshot", "cap": "CatalogCapture"}
        # The factory checks entries against independent full Git enumeration.
        for ref in self.anchor.catalog_entries:
            component = ref["path"].split("/")[2]
            if component == "payloads":
                continue
            record = self.read(ref, definitions[component])
            if record is None:
                continue
            if catalog_id_for(record) != record["record_id"]:
                self.error("SCHEMA_ID_MISMATCH", "catalog record has an invalid v1 identity", refs=[ref])
                continue
            identifier = record["record_id"]
            if identifier in self.catalog and canonical_bytes(record) != canonical_bytes(self.catalog[identifier]):
                self.error("CONFLICTING_ARTIFACT_BYTES", f"catalog identity has conflicting bytes: {identifier}", refs=[ref, self.refs[identifier]])
                continue
            # Equal-byte duplicate paths choose a deterministic reference, not evidence weight.
            if identifier not in self.refs or canonical_bytes(ref) < canonical_bytes(self.refs[identifier]):
                self.catalog[identifier], self.refs[identifier] = record, ref
            if component == "snap":
                for assertion in record["assertions"]:
                    self.interval(assertion["valid_from"], assertion["valid_until"], refs=[ref])
                    if assertion["assertion_predicate"] == "resolves_to":
                        target = assertion["assertion_value_or_target"]
                        if type(target) is not str or not target:
                            self.error("ASSERTION_TARGET_INVALID", "resolves_to requires a nonempty MID string", refs=[ref])

    def _declared_missing(self, *, record_id=None, digest=None):
        """Match a real, timely omission; never synthesize missing artifact bytes."""
        return any(
            parse_timestamp(row["known_at"]) <= self.cutoff
            and (record_id is None or row["unavailable_ref"]["expected_record_id"] == record_id)
            and (digest is None or row["unavailable_ref"]["expected_sha256"] == digest)
            for row in self.inventory["omission_declarations"]
        )

    def _sources(self):
        captures = {k: v for k, v in self.catalog.items() if v["record_kind"] == "catalog_capture"}
        captured_snapshots = {value["snapshot_id"] for value in captures.values()}
        for identifier, snapshot in sorted(self.catalog.items()):
            if snapshot["record_kind"] == "catalog_snapshot" and identifier not in captured_snapshots:
                # ModelSourceRef requires a real capture. A fabricated CAP ref is
                # not a representation for an unlinked retained snapshot.
                self.error("KNOWN_SOURCE_UNAVAILABLE", "retained snapshot has no capture linkage",
                           stage=2, refs=[self.refs[identifier]])
        rows = {}
        for row in _unique(self.inventory["model_sources"]):
            identifier = row["source_id"]
            if identifier in rows and rows[identifier] != row:
                self.error("CONFLICTING_ARTIFACT_BYTES", f"different source descriptions for {identifier}", stage=2)
            else:
                rows[identifier] = row
        if set(rows) != set(captures):
            self.error("INVENTORY_OMISSION", canonical_bytes({"missing_source_ids": sorted(set(captures) - set(rows)),
                       "unexpected_source_ids": sorted(set(rows) - set(captures))}).decode(), stage=2)
        if set(self.context["selected_source_ids"]) != set(captures):
            self.error("INVENTORY_OMISSION", "selected sources differ from all pinned catalog captures", stage=2)
        for identifier, cap in sorted(captures.items()):
            row = rows.get(identifier)
            if row is None:
                continue
            cap_ref = row["capture_ref"]
            if cap_ref != self.refs[identifier]:
                self.error("CAPTURE_SNAPSHOT_MISMATCH", "capture reference does not match enumerated source", refs=[cap_ref])
            snap_id = cap["snapshot_id"]
            snap = self.catalog.get(snap_id)
            if snap is None:
                self.error("KNOWN_SOURCE_UNAVAILABLE", f"capture names missing snapshot: {snap_id}", refs=[cap_ref])
                continue
            if snap["record_kind"] != "catalog_snapshot" or row["snapshot_ref"] != self.refs[snap_id]:
                self.error("CAPTURE_SNAPSHOT_MISMATCH", "source snapshot reference differs from capture linkage", refs=[cap_ref])
                continue
            if parse_timestamp(cap["captured_at"]) < parse_timestamp(snap["observed_at"]):
                self.error("INVALID_TIMESTAMP", "capture precedes snapshot observation", refs=[cap_ref, row["snapshot_ref"]])
            eid = snap["service_endpoint_id"]
            endpoint = self.catalog.get(eid)
            if endpoint is None:
                if row["endpoint_refs"]:
                    self.error("KNOWN_SOURCE_UNAVAILABLE", f"missing endpoint cannot have a fabricated reference: {eid}")
            elif endpoint["record_kind"] != "service_endpoint_identity":
                self.error("TARGET_WRONG_KIND", "snapshot endpoint names another record kind")
            elif _unique(row["endpoint_refs"]) != [self.refs[eid]]:
                self.error("CONTEXT_ANCHOR_MISMATCH", "source endpoint references do not match snapshot")
            payload_ref = row["payload_ref"]
            payload = self.bytes(payload_ref) if payload_ref is not None else None
            if cap["capture_success"] and payload_ref is None and not self._declared_missing(digest=cap["content_digest"]):
                self.error("KNOWN_SOURCE_UNAVAILABLE", "missing successful-capture payload requires an explicit timely omission",
                           stage=2, refs=[cap_ref])
            if payload_ref is not None:
                if not payload_ref["path"].startswith("docs/catalog/payloads/"):
                    self.error("INVENTORY_PIN_MISMATCH", "source payload must be in the pinned payload root", stage=2)
                if payload is not None and sha256(payload) != cap["content_digest"]:
                    self.error("ARTIFACT_DIGEST_MISMATCH", "capture payload digest mismatch", refs=[cap_ref])
            targets = []
            for assertion in snap["assertions"]:
                if assertion["assertion_predicate"] != "resolves_to":
                    continue
                target = assertion["assertion_value_or_target"]
                if type(target) is not str or not target:
                    continue  # already a typed invalid target; never feed a scalar to sets
                target_record = self.catalog.get(target)
                if target_record is None:
                    code = "TARGET_MISSING" if re.fullmatch(r"MID-[0-9a-f]{16}", target) else "ASSERTION_TARGET_INVALID"
                    if code != "TARGET_MISSING" or not self._declared_missing(record_id=target):
                        self.error(code, f"unavailable model target: {target}", refs=[row["snapshot_ref"]])
                elif target_record["record_kind"] != "model_identity":
                    self.error("TARGET_WRONG_KIND", f"target is not ModelIdentity: {target}", refs=[self.refs[target]])
                else:
                    targets.append(self.refs[target])
            if _unique(row["target_refs"]) != _unique(targets):
                self.error("CONTEXT_ANCHOR_MISMATCH", "source target reference set does not match decoded assertions", refs=[row["snapshot_ref"]])
            self.source_rows.append((row, cap, snap))

    def _fixture(self):
        fixture = self.read(self.context["synthetic_fixture_ref"], "SyntheticFixtureBindings")
        if fixture is None:
            return
        self.fixture = fixture
        for ref in _unique(fixture["fixture_artifact_refs"]):
            self.bytes(ref)
        for field_name, id_field in (("witness_rows", "witness_id"), ("availability_rows", "availability_id")):
            variants = {}
            for row in fixture["model_witness_profile"][field_name]:
                variants.setdefault(row[id_field], set()).add(canonical_bytes(row))
            for identifier, values in sorted(variants.items()):
                if len(values) > 1:
                    self.error("CONFLICTING_ARTIFACT_BYTES", canonical_bytes({
                        "profile_record_id": identifier,
                        "variant_sha256": sorted(sha256(value) for value in values),
                    }).decode(), refs=[self.context["synthetic_fixture_ref"]])
        availability_values = []
        for row in fixture["model_witness_profile"]["availability_rows"]:
            # No acceptance from a label; rows stipulate only fictional model evidence.
            validate_shape(row, "AvailabilityEvidence")
            availability_values.append((row, self.context["synthetic_fixture_ref"]))
        linked_availability = [ref for source, _, _ in self.source_rows
                               for ref in source["availability_evidence_refs"]]
        for ref in _unique(linked_availability + self.context["provided_artifact_refs"]):
            data = self.bytes(ref)
            if data is None:
                continue
            try:
                value = strict_loads(data)
            except QualificationError:
                if ref in linked_availability:
                    self.error("INVALID_SCHEMA", "linked availability bytes are not valid JSON", refs=[ref])
                continue  # other provided artifacts may be non-JSON payload bytes
            if isinstance(value, dict) and value.get("record_kind") == "availability_evidence":
                validate_shape(value, "AvailabilityEvidence")
                availability_values.append((value, ref))
            elif ref in linked_availability:
                self.error("INVALID_SCHEMA", "linked availability reference is not AvailabilityEvidence", refs=[ref])
        for value, ref in availability_values:
            self._availability_chronology(value, ref)
        for ref in _unique(self.context["corroboration_witness_refs"]):
            witness = self.read(ref, "CorroborationWitness")
            if witness is None:
                continue
            self.interval(witness["applicable_interval"]["valid_from"], witness["applicable_interval"]["valid_until"], refs=[ref])
            self.witnesses.append((ref, witness))

    def _availability_chronology(self, value, evidence_ref):
        """Internal chronology is invalid before endpoint/name/time exclusion."""
        available = parse_timestamp(value["available_at"])
        for ref in value["subject_refs"] + [value[key] for key in (
                "observation_ref", "observer_executor_ref", "rule_version_ref")]:
            data = self.bytes(ref)
            if data is None or ref not in value["subject_refs"]:
                continue
            try:
                subject = strict_loads(data)
            except QualificationError:
                continue
            if not isinstance(subject, dict):
                continue
            time_field = {"catalog_capture": "captured_at", "catalog_snapshot": "observed_at",
                          "corroboration_witness": "assessed_at"}.get(subject.get("record_kind"))
            if time_field is not None:
                if time_field not in subject or available < parse_timestamp(subject[time_field]):
                    self.error("INVALID_TIMESTAMP", "availability precedes the linked artifact's capture/observation/assessment",
                               refs=[evidence_ref, ref])

    def _declarations(self):
        for key, ref_key in (("known_source_declarations", "known_source_declaration_refs"),
                             ("omission_declarations", "omission_declaration_refs")):
            declarations = self.inventory[key]
            if _unique([x["declaration_ref"] for x in declarations]) != _unique(self.context[ref_key]):
                self.error("CONTEXT_ANCHOR_MISMATCH", "context declaration set differs from the pinned inventory", stage=2)
            for declaration in _unique(declarations):
                ref = declaration["declaration_ref"]
                body = self.read(ref)
                expected = {k: v for k, v in declaration.items() if k != "declaration_ref"}
                if body != expected:
                    self.error("CONTEXT_ANCHOR_MISMATCH", "declaration bytes differ from the pinned scope declaration", stage=2, refs=[ref])
                    continue
                if parse_timestamp(declaration["known_at"]) > self.cutoff:
                    continue
                declared = declaration.get("source_refs", [declaration.get("unavailable_ref")])
                for item in declared:
                    if "path" in item:
                        # All known, available catalog sources must belong to the enumerated tree.
                        data = self.bytes(item)
                        if data is not None and item["path"].startswith("docs/catalog/") and item not in self.anchor.catalog_entries:
                            self.error("INVENTORY_OMISSION", "known catalog artifact is outside the pinned inventory", stage=2, refs=[item])
                        elif data is not None and not any(item["sha256"] == known["sha256"] for known in self.anchor.catalog_entries):
                            for side in self.sides:
                                side.unknown = True
                                finding = reason("COVERAGE_UNDETERMINED", "known source bytes have no supported catalog applicability path", stage=2, side=side.side, refs=[ref, item])
                                side.reasons.append(finding)
                                self.coverage_reasons.append(finding)
                        continue
                    for side in self.sides:
                        name, endpoint = item["requested_name"], item["endpoint_id"]
                        if name is not None and name != side.subject["requested_model_name"]:
                            continue
                        endpoint_record = self.catalog.get(endpoint)
                        if endpoint_record and endpoint_record.get("record_kind") == "service_endpoint_identity" and endpoint_record["endpoint_identifier"] != side.subject["service_endpoint"]:
                            continue
                        side.unknown = True
                        finding = reason("KNOWN_SOURCE_UNAVAILABLE", f"known unavailable source: {item['source_key']}", stage=2, side=side.side, refs=[ref])
                        side.reasons.append(finding)
                        self.coverage_reasons.append(finding)
                        self.omission_refs.append(ref)

    def _bound(self, side):
        event = parse_timestamp(side.subject["occurred_at"])
        return min(event, self.cutoff) if self.policy["mode"] == "event_time" else self.cutoff

    def _available(self, required_refs, evidence_refs, lower_bound, bound, side,
                   *, accepted_evidence=None):
        """Exact pinned availability, separate from assessed/observed timestamps."""
        required = {canonical_bytes(x) for x in required_refs}
        accepted, late = False, False
        findings = []
        rows = self.fixture["model_witness_profile"]["availability_rows"] if self.fixture else []
        for ref in _unique(evidence_refs):
            value = self.read(ref, "AvailabilityEvidence")
            if value is None:
                continue
            if value["domain"] != "synthetic":
                continue
            if not required.issubset({canonical_bytes(x) for x in value["subject_refs"]}):
                continue
            if canonical_bytes(value) not in {canonical_bytes(x) for x in rows}:
                continue
            for item in value["subject_refs"] + [value["observation_ref"], value["observer_executor_ref"], value["rule_version_ref"]]:
                self.bytes(item)
            moment = parse_timestamp(value["available_at"])
            if moment < lower_bound:
                self.error("INVALID_TIMESTAMP", "availability precedes the bytes' capture/assessment", refs=[ref], side=side)
            elif moment > bound:
                late = True
            else:
                accepted = True
                if accepted_evidence is not None:
                    accepted_evidence.append((ref, value))
        if accepted:
            return "available", findings
        code = "EVIDENCE_AFTER_CUTOFF" if late else "EVENT_AVAILABILITY_UNPROVEN"
        findings.append(reason(code, "availability is not established by the applicable bound", side=side, refs=required_refs))
        return ("late" if late else "unproven"), findings

    def _identity(self, target):
        record = self.catalog[target]
        return {"kind": "model", "identity_ref": target, "version_identity": record["release_identity"],
                "record_ref": self.refs[target], "basis": "catalog_declared"}

    def one(self, side):
        subject, name = side.subject, side.side
        if subject["kind"] != "model":
            side.unknown = True
            side.reasons.append(reason("PROFILE_UNAVAILABLE", "3B is not admitted; no tool/human identity profile is evaluated", side=name, stage=6))
            return
        candidates = [self.refs[k] for k, v in self.catalog.items() if v["record_kind"] == "service_endpoint_identity" and v["endpoint_identifier"] == subject["service_endpoint"]]
        if len(candidates) != 1:
            side.unknown = True
            side.reasons.append(reason("ENDPOINT_MAPPING_UNRESOLVED", "exact endpoint spelling has no unique catalog mapping", side=name))
            if not candidates:
                side.reasons.append(reason("ENDPOINT_ALIAS_UNRESOLVED", "3A supplies no endpoint alias rule", side=name))
            return
        side.endpoint = candidates[0]
        event, bound = parse_timestamp(subject["occurred_at"]), self._bound(side)
        targets, strict_targets, declared_block, strict_block = set(), set(), False, False
        for row, cap, snap in sorted(self.source_rows, key=lambda x: canonical_bytes(x[0])):
            findings, local_targets = [], set()
            applicability, declared_support = "applicable", False

            def add(code, detail, stage=3):
                findings.append(reason(code, detail, stage=stage, side=name, refs=[row["capture_ref"], row["snapshot_ref"]]))

            endpoint = self.catalog.get(snap["service_endpoint_id"])
            if endpoint is None:
                applicability = "undetermined"
                add("ENDPOINT_MAPPING_UNRESOLVED", "snapshot endpoint definition is unavailable")
            elif snap["service_endpoint_id"] != side.endpoint["record_id"]:
                applicability = "inapplicable"
                add("WRONG_ENDPOINT", "source belongs to another catalog-declared endpoint")
            elif parse_timestamp(snap["observed_at"]) > event:
                applicability = "inapplicable"
                add("FUTURE_OBSERVATION", "catalog observation follows invocation")
            elif (event - parse_timestamp(snap["observed_at"])).days > self.policy["freshness_window_days"] or (
                (event - parse_timestamp(snap["observed_at"])).days == self.policy["freshness_window_days"]
                and ((event - parse_timestamp(snap["observed_at"])).seconds or (event - parse_timestamp(snap["observed_at"])).microseconds)
            ):
                applicability = "inapplicable"
                add("FRESHNESS_EXPIRED", "catalog observation is outside the pinned freshness window")
            elif parse_timestamp(cap["captured_at"]) > bound:
                applicability = "inapplicable"
                add("EVIDENCE_AFTER_CUTOFF", "declared capture time follows the applicable bound")
            elif not cap["capture_success"]:
                applicability = "undetermined"
                add("CAPTURE_UNSUCCESSFUL", "failed capture supplies neither support nor proof of name absence")
            elif row["payload_ref"] is None:
                applicability = "undetermined"
                add("KNOWN_SOURCE_UNAVAILABLE", "successful capture payload is unavailable; no reference was fabricated")
            else:
                matching = [a for a in snap["assertions"] if a["assertion_predicate"] == "resolves_to" and a["assertion_subject"] == subject["requested_model_name"]]
                active = [a for a in matching if parse_timestamp(a["valid_from"]) <= event and (a["valid_until"] is None or event <= parse_timestamp(a["valid_until"]))]
                if not matching:
                    applicability = "inapplicable"
                    add("ASSERTION_NAME_ABSENT", "intact successful snapshot has no requested-name mapping")
                elif not active:
                    applicability = "inapplicable"
                    add("ASSERTION_INTERVAL_INAPPLICABLE", "no matching assertion covers the event")
                elif any(a["assertion_value_or_target"] not in self.catalog for a in active):
                    applicability = "undetermined"
                    add("TARGET_MISSING", "active assertion target is explicitly declared unavailable; no MID reference was fabricated")
                elif any(a["scope"] is not None or a["superseded_by"] is not None for a in active):
                    applicability = "undetermined"
                    if any(a["scope"] is not None for a in active):
                        add("ASSERTION_SCOPE_UNSUPPORTED", "non-null assertion scope is not a supported wildcard")
                    if any(a["superseded_by"] is not None for a in active):
                        add("SUPERSESSION_UNRESOLVED", "supersession cannot erase a relevant assertion")
                else:
                    local_targets = {a["assertion_value_or_target"] for a in active}
                    if cap["content_evidence_status"] == "contradicted":
                        add("CAPTURE_CONTRADICTED", "applicable capture-wide adverse evidence", stage=4)
                        declared_block = strict_block = True
                    if len(local_targets) > 1:
                        add("TARGETS_AMBIGUOUS", "multiple applicable targets in the snapshot", stage=4)
                        declared_block = strict_block = True
                    state, availability_reasons = self._available(
                        [row["capture_ref"], row["snapshot_ref"], row["payload_ref"]],
                        row["availability_evidence_refs"], parse_timestamp(cap["captured_at"]), bound, name)
                    findings.extend(availability_reasons)
                    if state == "late":
                        applicability = "inapplicable"
                        # A time-proven irrelevant source must not veto another source.
                        # Adverse flags are recomputed below only for retained relevant rows.
                    else:
                        declared_support = True
                        targets.update(local_targets)
                        if state == "available":
                            strict_targets.update(local_targets)
                            side.sources.append((row, cap, snap, local_targets))
                        else:
                            applicability = "undetermined"
                            strict_block = True
            if applicability == "undetermined":
                side.unknown = True
                strict_block = True
                if not declared_support:
                    declared_block = True
            if not findings:
                add("CONDITIONS_SATISFIED", "this synthetic catalog source passed applicability checks; not qualification")
            self.findings.append({"source_id": row["source_id"], "side": name,
                                  "applicability": applicability,
                                  "target_refs": _unique([self.refs[x] for x in local_targets if x in self.refs]),
                                  "reasons": canonicalize_reasons(findings)})
            side.reasons.extend(findings)
        # A contradiction/ambiguity only governs when the source is not proven inapplicable.
        relevant = [x for x in self.findings if x["side"] == name and x["applicability"] != "inapplicable"]
        if any(r["code"] in ("CAPTURE_CONTRADICTED", "TARGETS_AMBIGUOUS") for x in relevant for r in x["reasons"]):
            declared_block = strict_block = True
        else:
            # Remove adverse flags from time-proven irrelevant sources without erasing unknowns.
            declared_block = any(x["applicability"] == "undetermined" and not any(r["code"] == "EVENT_AVAILABILITY_UNPROVEN" for r in x["reasons"]) for x in relevant)
            strict_block = any(x["applicability"] == "undetermined" for x in relevant)
        if len(targets) > 1:
            declared_block = strict_block = True
            side.reasons.append(reason("TARGETS_CONFLICT", "applicable source targets disagree: " + ",".join(sorted(targets)), stage=4, side=name))
        if not targets:
            side.reasons.append(reason("NO_APPLICABLE_SOURCE", "no applicable valid model target", stage=4, side=name))
        if len(targets) == 1 and not declared_block:
            side.declared = self._identity(next(iter(targets)))
        if len(strict_targets) == 1 and not strict_block and not side.unknown:
            side.clean = self._identity(next(iter(strict_targets)))
        if side.declared and side.declared["version_identity"] == "unknown":
            side.reasons.append(reason("TARGET_RELEASE_UNKNOWN", "catalog record has no known release identity", side=name, stage=6, refs=[side.declared["record_ref"]]))

    def relation(self, attribute):
        left, right = (getattr(side, attribute) for side in self.sides)
        findings = [r for s in self.sides for r in s.reasons]
        if self.query["left"]["kind"] != self.query["right"]["kind"]:
            findings.append(reason("CROSS_KIND_UNDEFINED", "cross-kind comparisons remain unresolved", stage=6))
            return _empty_relation(findings)
        value = "unresolved"
        if left is not None and right is not None:
            value = "equivalent" if left["identity_ref"] == right["identity_ref"] else "non_equivalent"
            findings.append(reason("EQUIVALENT_IDENTITY" if value == "equivalent" else "NON_EQUIVALENT_IDENTITY",
                                   "catalog-record relation only, not established real-executor equivalence or independence", stage=6))
        return {"value": value, "left_identity": left, "right_identity": right,
                "reasons": canonicalize_reasons(findings)}

    def witness(self, side):
        findings, accepted = [], []
        if side.clean is None or side.clean["version_identity"] == "unknown":
            return accepted, [reason("WITNESS_MISSING", "no clean known-release binding for this side", side=side.side, stage=5)]
        expected_subject = {"endpoint_ref": side.endpoint,
                            "requested_model_name": side.subject["requested_model_name"],
                            "target_model_ref": side.clean["record_ref"],
                            "event_at": side.subject["occurred_at"],
                            "property_id": "model_reference_resolves_to_identity"}
        rows = self.fixture["model_witness_profile"]["witness_rows"] if self.fixture else []
        availability_refs = []
        # Availability artifacts are explicitly provided, never inferred from assessed_at.
        for ref in _unique(self.context["provided_artifact_refs"]):
            data = self.anchor.read(ref)
            try:
                value = strict_loads(data)
            except QualificationError:
                continue
            if isinstance(value, dict) and value.get("record_kind") == "availability_evidence":
                availability_refs.append(ref)
        for ref, witness in self.witnesses:
            if witness["subject"]["requested_model_name"] != expected_subject["requested_model_name"]:
                continue
            if witness["subject"] != expected_subject or witness["domain"] != "synthetic":
                findings.append(reason("WITNESS_SCOPE_MISMATCH", "witness property does not match this exact side", stage=5, side=side.side, refs=[ref]))
                continue
            row_value = {k: v for k, v in witness.items() if k not in ("schema_version", "record_kind", "domain", "profile_id")}
            if canonical_bytes(row_value) not in {canonical_bytes(x) for x in rows}:
                findings.append(reason("WITNESS_EVIDENCE_MISMATCH", "witness differs from the exact harness-pinned proof row", stage=5, side=side.side, refs=[ref]))
                continue
            for item in witness["evidence_refs"] + [witness[k] for k in (
                    "verifier_executor_ref", "verifier_version_ref", "rule_version_ref", "verification_ref", "assessment_scope_ref")]:
                self.bytes(item)
            evidence = {canonical_bytes(x) for x in witness["evidence_refs"]}
            chain_matches = []
            for source, cap, _, targets in side.sources:
                chain = [source["capture_ref"], source["snapshot_ref"], source["payload_ref"], side.clean["record_ref"]]
                if (cap["content_evidence_status"] == "independently_corroborated"
                    and side.clean["identity_ref"] in targets
                    and all(canonical_bytes(x) in evidence for x in chain)):
                    chain_matches.append((source, cap, chain))
            if not chain_matches:
                findings.append(reason("WITNESS_EVIDENCE_MISMATCH", "witness does not cover this same corroborating capture-snapshot-payload-MID chain", stage=5, side=side.side, refs=[ref]))
                continue
            verification = self.read(witness["verification_ref"])
            expected_verification = {"profile_id": "SYN-MODEL-WITNESS-1",
                                     "subject": witness["subject"], "evidence_refs": witness["evidence_refs"]}
            if verification != expected_verification:
                findings.append(reason("WITNESS_EVIDENCE_MISMATCH", "verification premise differs from the exact witness source chain", stage=5, side=side.side, refs=[ref, witness["verification_ref"]]))
                continue
            interval, event, bound = witness["applicable_interval"], parse_timestamp(side.subject["occurred_at"]), self._bound(side)
            if (event < parse_timestamp(interval["valid_from"])
                or (interval["valid_until"] is not None and event > parse_timestamp(interval["valid_until"]))
                or (interval["revoked_at"] is not None and event >= parse_timestamp(interval["revoked_at"]))):
                findings.append(reason("WITNESS_SCOPE_MISMATCH", "witness interval/revocation excludes this event", stage=5, side=side.side, refs=[ref]))
                continue
            assessed = parse_timestamp(witness["assessed_at"])
            if assessed > bound:
                findings.append(reason("EVIDENCE_AFTER_CUTOFF", "witness assessment is after the applicable bound", stage=5, side=side.side, refs=[ref]))
                continue
            # Each candidate was available by the event/knowledge bound, but
            # this witness can rely only on its own chain available when assessed.
            timely_chains = []
            for source, cap, chain in chain_matches:
                source_proofs = []
                source_state, source_findings = self._available(
                    chain[:3], source["availability_evidence_refs"],
                    parse_timestamp(cap["captured_at"]), assessed, side.side,
                    accepted_evidence=source_proofs)
                findings.extend(source_findings)
                if source_state == "available":
                    timely_chains.append((source, cap, chain, source_proofs))
            if not timely_chains:
                findings.append(reason("WITNESS_EVIDENCE_MISMATCH", "this exact witnessed source chain was not available by assessed_at", stage=5, side=side.side, refs=[ref]))
                continue
            witness_proofs = []
            state, availability_reasons = self._available(
                [ref, witness["verification_ref"]], availability_refs, assessed,
                bound, side.side, accepted_evidence=witness_proofs)
            findings.extend(availability_reasons)
            if state == "available":
                accepted.append(ref)
                # Retain a real proof pair per accepted chain. Earliest accepted
                # time, then canonical reference bytes, is a deterministic
                # diagnostic choice among proofs that all satisfy the rule.
                def proof_key(item):
                    return parse_timestamp(item[1]["available_at"]), canonical_bytes(item[0])

                witness_av_ref, witness_av = min(witness_proofs, key=proof_key)
                witness_av_record = record_ref(
                    witness_av["availability_id"], self.anchor.read(witness_av_ref))
                for source, cap, chain, proofs in timely_chains:
                    source_av_ref, source_av = min(proofs, key=proof_key)
                    source_av_record = record_ref(
                        source_av["availability_id"], self.anchor.read(source_av_ref))
                    timing = {"captured_at": cap["captured_at"],
                              "source_available_at": source_av["available_at"],
                              "assessed_at": witness["assessed_at"],
                              "witness_available_at": witness_av["available_at"],
                              "bound": bound.isoformat(),
                              "payload_sha256": source["payload_ref"]["sha256"],
                              "verification_sha256": witness["verification_ref"]["sha256"]}
                    findings.append(reason(
                        "CONDITIONS_SATISFIED", "accepted fictional witness chain timing: " + canonical_bytes(timing).decode("utf-8"),
                        stage=5, side=side.side,
                        refs=[ref, *chain, source_av_record, witness_av_record]))
        if not accepted:
            findings.append(reason("WITNESS_MISSING", "no exact and timely same-side corroborating witness", stage=5, side=side.side))
        return _unique(accepted), findings

    def run(self):
        self.prepare()
        if self.errors:
            return _invalid("synthetic", self.errors)
        for side in self.sides:
            self.one(side)
        if self.errors:
            return _invalid("synthetic", self.errors)
        supplied, clean = self.relation("declared"), self.relation("clean")
        witness_refs, witness_reasons, both = [], [], True
        for side in self.sides:
            accepted, findings = self.witness(side)
            witness_refs.extend(accepted)
            witness_reasons.extend(findings)
            both = both and bool(accepted)
        if self.errors:
            return _invalid("synthetic", self.errors)
        coverage = "missing_items" if self.omission_refs else ("undetermined" if any(x.unknown for x in self.sides) else "pinned_inventory_exhausted")
        if clean["value"] == "non_equivalent" and both and coverage == "pinned_inventory_exhausted":
            condition = "conditions_satisfied"
            witness_reasons.append(reason("CONDITIONS_SATISFIED", "exact synthetic model witness conditions only", stage=6))
        else:
            condition = "withheld"
        witness_reasons.append(reason("SYNTHETIC_DOMAIN_ONLY", "fictional premises cannot establish live binding, independence or authority", stage=8))
        self.coverage_reasons.append(reason("OUTSIDE_SCOPE_UNASSESSED", "coverage is bounded to this consumer-pinned inventory, not all possible sources", stage=2))
        return _finish({
            "schema_version": SCHEMA_VERSION, "record_kind": "assessment_result",
            "domain": "synthetic", "entry_point": "evaluate_synthetic_r2",
            "query_ref": record_ref(self.query["query_id"], self.query_bytes),
            "evidence_context_ref": self.anchor.context_ref,
            "validation_status": "valid", "validation_reasons": [],
            "supplied_relation": supplied, "R_identity": clean,
            "Q_identity": {"value": condition, "reasons": canonicalize_reasons(witness_reasons)},
            "C3": _constraint(), "C10": _constraint(), "Q_C3_C10": _constraint(),
            "coverage": {"value": coverage, "inventory_ref": self.context["inventory_ref"],
                         "omission_refs": _unique(self.omission_refs), "reasons": canonicalize_reasons(self.coverage_reasons)},
            "source_findings": sorted(_unique(self.findings), key=lambda x: (x["source_id"], x["side"], canonical_bytes(x))),
            "corroboration_witness_refs": _unique(witness_refs), "shared_ancestry_evidence_refs": [],
        })


def _query(value):
    try:
        data = value if isinstance(value, bytes) else (value.encode("utf-8") if isinstance(value, str) else canonical_bytes(value))
    except UnicodeError as exc:
        raise QualificationError("INVALID_SCHEMA", "Query text is not valid UTF-8", stage=0) from exc
    query = strict_loads(data)
    validate_shape(query, "Query")
    return query, data


def evaluate_synthetic_r2(query: Any, *, anchor: EvidenceAnchor) -> dict:
    """Evaluate only synthetic model conditions under an out-of-band anchor.

    Raises QualificationBootstrapError if the pinned schema is unavailable or
    invalid. That boundary produces no AssessmentResult and grants nothing.
    Ordinary input failures after bootstrap remain typed invalid envelopes.
    """
    require_qualification_schema()
    try:
        value, data = _query(query)
        if value["domain"] != "synthetic":
            raise QualificationError("DOMAIN_MISMATCH", "synthetic entry point cannot evaluate a production Query", stage=8)
        if not isinstance(anchor, EvidenceAnchor) or anchor.domain != "synthetic":
            raise QualificationError("CONTEXT_ANCHOR_MISMATCH", "an accepted frozen synthetic harness anchor is required")
        return _Evaluation(value, data, anchor).run()
    except QualificationError as exc:
        return _invalid("synthetic", [_error_reason(exc)])


def evaluate_production_r2(query: Any, *, anchor=None) -> dict:
    """Refuse production qualification; Query cannot construct a live context.

    QualificationBootstrapError propagates without an assessment if the pinned
    schema cannot load. Bootstrap success enables only the ordinary refusal
    envelope; no production profile is installed.
    """
    require_qualification_schema()
    try:
        value, _ = _query(query)
        if value["domain"] != "production" or anchor is not None:
            raise QualificationError("DOMAIN_MISMATCH", "synthetic or caller-created contexts cannot enter production", stage=8)
        raise QualificationError("CONTEXT_ANCHOR_MISMATCH", "no governed production context anchor is installed")
    except QualificationError as exc:
        return _invalid("production", [_error_reason(exc)])
