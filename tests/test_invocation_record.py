"""Tests for ABS-0004 Slice A invocation provenance capture.

Covers the schema, every validator rejection class, and each of the eight
conditions binding PLAN-20260722-0001 under WARR-20260722-0001.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_lab.providers.invocation_record import (
    ATTESTATION_COMPLETE,
    ATTESTATION_PARTIAL,
    CAPTURE_PATH_COMPARE_PROVIDERS,
    CAPTURE_PATHS,
    EXECUTOR_KIND_MODEL,
    EXECUTOR_KIND_TOOL,
    IDENTITY_FIELDS_V1,
    IDENTITY_UNRESOLVED,
    INVOCATION_SCHEMA_VERSION,
    MARKER_EXPERIMENTAL,
    SESSION_STATELESS,
    SESSION_UNKNOWN,
    SLICE_A_PREDICATES,
    STATUS_FAILURE,
    STATUS_SUCCESS,
    InvocationRecordError,
    build_invocation_record,
    canonical_invocation_json,
    digest_text,
    invocation_id_for,
    invocation_relations,
    invocation_relative_path,
    validate_invocation_record,
    write_invocation_record,
)


def make_record(**overrides):
    kwargs = dict(
        capture_path=CAPTURE_PATH_COMPARE_PROVIDERS,
        executor_kind=EXECUTOR_KIND_MODEL,
        executor_reference="claude-sonnet-4-5",
        identity_verification_status=IDENTITY_UNRESOLVED,
        requested_model_name="claude-sonnet-4-5",
        service_endpoint="anthropic.messages",
        session_id="SESSION-20260722-0001",
        occurred_at="2026-07-22T12:00:00+00:00",
        rendered_prompt="review the plan",
        session_state_mode=SESSION_STATELESS,
        completeness_attestation=ATTESTATION_PARTIAL,
        status=STATUS_SUCCESS,
        output_token_limit=16000,
    )
    kwargs.update(overrides)
    return build_invocation_record(**kwargs)


# --- schema shape -----------------------------------------------------


def test_build_invocation_record_produces_valid_slice_a_record():
    record = make_record()

    validate_invocation_record(record)
    assert record["schema_version"] == INVOCATION_SCHEMA_VERSION
    assert record["capture_path"] == CAPTURE_PATH_COMPARE_PROVIDERS
    assert record["executor"]["identity_verification_status"] == IDENTITY_UNRESOLVED
    assert record["effective_input_manifest"]["rendered_prompt_digest"] == digest_text(
        "review the plan"
    )
    assert record["execution_profile"]["output_token_limit"] == 16000
    assert record["spawned"] == []


def test_manifest_and_profile_carry_every_slice_a_field():
    record = make_record()

    manifest = record["effective_input_manifest"]
    for field in (
        "rendered_prompt_digest",
        "system_instruction_digest",
        "developer_instruction_digest",
        "context_manifest_reference",
        "tool_schema_digest",
        "prior_tool_result_references",
        "session_state_mode",
        "completeness_attestation",
    ):
        assert field in manifest

    profile = record["execution_profile"]
    for field in (
        "service_endpoint",
        "requested_model_name",
        "output_token_limit",
        "sampling_parameters",
        "reasoning_parameters",
        "provider_request_flags",
        "runtime_version",
    ):
        assert field in profile


# --- condition 7: session identity present, not mode alone ------------


def test_session_identity_is_required_in_every_record():
    record = make_record()
    assert record["session_id"]

    del record["session_id"]
    with pytest.raises(InvocationRecordError, match=r"\$\.session_id"):
        validate_invocation_record(record)


def test_session_state_mode_is_recorded_on_the_manifest():
    record = make_record(session_state_mode=SESSION_UNKNOWN)

    assert record["effective_input_manifest"]["session_state_mode"] == SESSION_UNKNOWN


# --- condition 2: determinism -----------------------------------------


def test_identical_semantic_content_serializes_to_identical_bytes():
    first = make_record()
    second = make_record()

    assert canonical_invocation_json(first) == canonical_invocation_json(second)
    assert first["invocation_id"] == second["invocation_id"]


def test_distinct_records_produce_distinct_identities():
    base = make_record()
    other_prompt = make_record(rendered_prompt="a different prompt")
    other_session = make_record(session_id="SESSION-20260722-0002")
    other_time = make_record(occurred_at="2026-07-22T13:00:00+00:00")

    identities = {
        base["invocation_id"],
        other_prompt["invocation_id"],
        other_session["invocation_id"],
        other_time["invocation_id"],
    }
    assert len(identities) == 4


def test_key_order_does_not_affect_canonical_serialization():
    record = make_record()
    reordered = dict(reversed(list(record.items())))

    assert canonical_invocation_json(record) == canonical_invocation_json(reordered)


# --- condition 4: schema versioning and identity stability ------------


def test_identity_ignores_fields_outside_the_enumerated_subset():
    record = make_record()
    original = record["invocation_id"]

    # Fields a later slice would add must not disturb existing identities.
    record["resolved_model_identity"] = "MODEL-0001"
    record["authorization_reference"] = "AUTH-0001"
    record["execution_profile"]["output_token_limit"] = 4096
    record["status"] = STATUS_FAILURE

    assert invocation_id_for(record) == original


def test_identity_subset_is_explicitly_enumerated_and_version_scoped():
    assert "schema_version" in IDENTITY_FIELDS_V1
    assert len(IDENTITY_FIELDS_V1) == 9

    record = make_record()
    mutated = dict(record)
    mutated["schema_version"] = "v2"

    assert invocation_id_for(mutated) != record["invocation_id"]


def test_recorded_identity_must_match_computed_identity():
    record = make_record()
    record["invocation_id"] = "INV-0000000000000000"

    with pytest.raises(InvocationRecordError, match="does not match"):
        validate_invocation_record(record)


# --- condition 1: capture path gate -----------------------------------


def test_capture_paths_admit_only_the_comparison_path():
    assert CAPTURE_PATHS == frozenset({"scripts/compare_providers.py"})


def test_record_from_an_unadmitted_capture_path_is_rejected():
    with pytest.raises(InvocationRecordError, match="outside the admitted capture"):
        make_record(capture_path="scripts/ask_provider.py")


def test_ask_provider_script_emits_no_invocation_record():
    source = Path("scripts/ask_provider.py").read_text(encoding="utf-8")

    assert "invocation_record" not in source
    assert "write_invocation_record" not in source


# --- condition 6: marker default --------------------------------------


def test_governance_marker_defaults_to_experimental():
    record = make_record()

    assert record["governance_marker"] == MARKER_EXPERIMENTAL


# --- condition 8 and constraint 2: predicates and relation shape ------


def test_relations_use_graph_relation_shape_and_slice_a_predicates_only():
    from ai_lab.documentation.graph_neighborhood import GraphRelation

    record = make_record()
    relations = invocation_relations(record, produced_artifact_id="COMP-0099")

    assert all(isinstance(relation, GraphRelation) for relation in relations)
    assert all(relation.predicate in SLICE_A_PREDICATES for relation in relations)
    assert all(relation.authoritative is False for relation in relations)

    predicates = {relation.predicate for relation in relations}
    assert predicates == {
        "produced_by",
        "executed_by",
        "requested_via",
        "used_execution_profile",
        "used_inputs",
        "member_of",
    }


def test_produced_by_links_the_comparison_artifact_to_the_invocation():
    record = make_record()
    relations = invocation_relations(record, produced_artifact_id="COMP-0099")

    produced = [r for r in relations if r.predicate == "produced_by"]
    assert len(produced) == 1
    assert produced[0].source_id == "COMP-0099"
    assert produced[0].target_id == record["invocation_id"]


def test_spawned_edges_are_emitted_for_subordinate_executions():
    child = make_record(rendered_prompt="subordinate call")
    parent = make_record(spawned=[child["invocation_id"]])

    relations = invocation_relations(parent)
    spawned = [r for r in relations if r.predicate == "spawned"]

    assert len(spawned) == 1
    assert spawned[0].target_id == child["invocation_id"]


def test_slice_a_predicate_list_matches_the_admitted_seven():
    assert SLICE_A_PREDICATES == (
        "produced_by",
        "executed_by",
        "requested_via",
        "used_execution_profile",
        "used_inputs",
        "member_of",
        "spawned",
    )


# --- validator rejection classes --------------------------------------


def test_rejects_wrong_schema_version():
    record = make_record()
    record["schema_version"] = "v2"
    record["invocation_id"] = invocation_id_for(record)

    with pytest.raises(InvocationRecordError, match="schema_version"):
        validate_invocation_record(record)


def test_rejects_unknown_executor_kind():
    with pytest.raises(InvocationRecordError, match=r"\$\.executor\.kind"):
        make_record(executor_kind="oracle")


def test_rejects_unknown_identity_verification_status():
    with pytest.raises(InvocationRecordError, match="identity_verification_status"):
        make_record(identity_verification_status="probably_fine")


def test_rejects_unknown_session_state_mode():
    with pytest.raises(InvocationRecordError, match="session_state_mode"):
        make_record(session_state_mode="mystery")


def test_rejects_unknown_completeness_attestation():
    with pytest.raises(InvocationRecordError, match="completeness_attestation"):
        make_record(completeness_attestation="probably_complete")


def test_rejects_unknown_status():
    with pytest.raises(InvocationRecordError, match=r"\$\.status"):
        make_record(status="partial")


def test_rejects_malformed_prompt_digest():
    record = make_record()
    record["effective_input_manifest"]["rendered_prompt_digest"] = "notadigest"

    with pytest.raises(InvocationRecordError, match="rendered_prompt_digest"):
        validate_invocation_record(record)


def test_rejects_unknown_manifest_field():
    record = make_record()
    record["effective_input_manifest"]["invented_field"] = "x"

    with pytest.raises(InvocationRecordError, match="unknown fields"):
        validate_invocation_record(record)


def test_rejects_unknown_profile_field():
    record = make_record()
    record["execution_profile"]["invented_field"] = "x"

    with pytest.raises(InvocationRecordError, match="unknown fields"):
        validate_invocation_record(record)


def test_rejects_missing_manifest_field():
    record = make_record()
    del record["effective_input_manifest"]["tool_schema_digest"]

    with pytest.raises(InvocationRecordError, match="tool_schema_digest is required"):
        validate_invocation_record(record)


def test_rejects_non_positive_output_token_limit():
    record = make_record()
    record["execution_profile"]["output_token_limit"] = 0

    with pytest.raises(InvocationRecordError, match="output_token_limit"):
        validate_invocation_record(record)


def test_rejects_malformed_spawned_entries():
    record = make_record()
    record["spawned"] = ["not-an-invocation-id"]

    with pytest.raises(InvocationRecordError, match=r"\$\.spawned"):
        validate_invocation_record(record)


def test_rejects_unknown_governance_marker():
    with pytest.raises(InvocationRecordError, match="governance_marker"):
        make_record(governance_marker="blessed")


# --- paths and writing -------------------------------------------------


def test_invocation_path_is_deterministic():
    record = make_record()

    assert invocation_relative_path(record["invocation_id"]) == (
        f"docs/invocations/{record['invocation_id']}.json"
    )


def test_malformed_identity_has_no_path():
    with pytest.raises(InvocationRecordError, match="malformed invocation id"):
        invocation_relative_path("INV-nope")


def test_write_invocation_record_round_trips_byte_identically(tmp_path):
    record = make_record()

    written = write_invocation_record(record, tmp_path)
    reloaded = json.loads(written.read_text(encoding="utf-8"))

    validate_invocation_record(reloaded)
    assert reloaded == record
    assert written.read_text(encoding="utf-8") == canonical_invocation_json(record)


def test_write_rejects_invalid_record_before_touching_disk(tmp_path):
    record = make_record()
    record["status"] = "partial"

    with pytest.raises(InvocationRecordError):
        write_invocation_record(record, tmp_path)

    assert not (tmp_path / "docs" / "invocations").exists()


# --- executor kinds ----------------------------------------------------


def test_tool_executor_is_representable():
    record = make_record(
        executor_kind=EXECUTOR_KIND_TOOL,
        executor_reference="pytest",
        requested_model_name="none",
    )

    validate_invocation_record(record)
    assert record["executor"]["kind"] == EXECUTOR_KIND_TOOL


def test_complete_attestation_is_representable():
    record = make_record(completeness_attestation=ATTESTATION_COMPLETE)

    assert (
        record["effective_input_manifest"]["completeness_attestation"]
        == ATTESTATION_COMPLETE
    )


# --- condition 6: rider discipline -------------------------------------


def test_claude_max_tokens_default_is_the_ridered_value():
    import importlib

    import ai_lab.providers.settings as settings

    importlib.reload(settings)
    assert settings.CLAUDE_MAX_TOKENS == 16000


def test_environment_override_takes_precedence_over_the_default(monkeypatch):
    import importlib

    monkeypatch.setenv("AI_LAB_CLAUDE_MAX_TOKENS", "2048")
    import ai_lab.providers.settings as settings

    importlib.reload(settings)
    try:
        assert settings.CLAUDE_MAX_TOKENS == 2048
    finally:
        monkeypatch.delenv("AI_LAB_CLAUDE_MAX_TOKENS", raising=False)
        importlib.reload(settings)


def test_model_defaults_are_the_adjudicated_ones():
    """Defaults advanced by DECISION-20260723-0001.

    The prior values (gpt-5, claude-sonnet-4-5) were unrevisited literals;
    claude-sonnet-4-5 was absent from the provider listing captured on
    2026-07-23 while still accepted by the endpoint. claude-opus-4-8 is
    deliberately not chosen: it is the drafting executor's own reported
    identity, and selecting it would collapse reviewer and author into one
    ModelIdentity under ABS-0004 C3.
    """

    import importlib

    import ai_lab.providers.settings as settings

    importlib.reload(settings)
    assert settings.CLAUDE_MODEL == "claude-sonnet-5"
    assert settings.OPENAI_MODEL == "gpt-5.6-terra"
    assert settings.CLAUDE_MODEL != "claude-opus-4-8"
    assert settings.OPENAI_REASONING_EFFORT is None
    assert settings.CLAUDE_EFFORT is None


def test_chosen_defaults_are_present_in_the_captured_listings():
    """The defaults are names the providers actually listed.

    This is the check that would have caught claude-sonnet-4-5 drifting out
    of the catalog. It reads the retained payloads, not the network.
    """

    payload_dir = Path("docs/catalog/payloads")
    if not payload_dir.exists():  # pragma: no cover - captures not present
        pytest.skip("no retained catalog payloads in this checkout")

    import importlib

    import ai_lab.providers.settings as settings

    importlib.reload(settings)

    listed: dict[str, set[str]] = {}
    for path in sorted(payload_dir.glob("*.json")):
        body = json.loads(path.read_text(encoding="utf-8"))
        listed.setdefault(body["surface"], set()).update(
            entry["id"] for entry in body["payload"]["data"]
        )

    assert settings.CLAUDE_MODEL in listed["anthropic"]
    assert settings.OPENAI_MODEL in listed["openai"]


def test_per_call_override_takes_precedence_over_the_default():
    import inspect

    from ai_lab.providers.claude_provider import ClaudeProvider

    signature = inspect.signature(ClaudeProvider.__init__)
    assert "max_tokens" in signature.parameters


# --- condition 3: capture failure reporting ----------------------------


class _StubProvider:
    name = "Claude"
    model = "claude-sonnet-4-5"
    _max_tokens = 16000
    _effort = None

    def ask(self, prompt: str) -> str:
        return "stub answer"


def test_capture_failure_is_reported_and_the_call_result_survives(tmp_path, capsys):
    from ai_lab.providers.invocation_capture import (
        capture_provider_invocation,
        report_capture_failure,
    )

    provider = _StubProvider()
    answer = provider.ask("prompt")

    unwritable = tmp_path / "blocked"
    unwritable.write_text("not a directory", encoding="utf-8")

    record, error = capture_provider_invocation(
        repo_root=unwritable,
        provider=provider,
        rendered_prompt="prompt",
        session_id="SESSION-failuretest01",
        session_state_mode=SESSION_STATELESS,
        occurred_at="2026-07-22T12:00:00+00:00",
        status=STATUS_SUCCESS,
    )

    assert record is None
    assert error is not None

    report_capture_failure(provider.name, error)
    captured = capsys.readouterr()
    assert "invocation capture failed" in captured.err

    # The provider result is unaffected by capture failure.
    assert answer == "stub answer"


def test_capture_writes_a_valid_record_on_the_admitted_path(tmp_path):
    from ai_lab.providers.invocation_capture import capture_provider_invocation

    record, error = capture_provider_invocation(
        repo_root=tmp_path,
        provider=_StubProvider(),
        rendered_prompt="prompt",
        session_id="SESSION-successtest1",
        session_state_mode=SESSION_STATELESS,
        occurred_at="2026-07-22T12:00:00+00:00",
        status=STATUS_SUCCESS,
    )

    assert error is None
    assert record is not None
    validate_invocation_record(record)
    assert record["capture_path"] == CAPTURE_PATH_COMPARE_PROVIDERS
    assert record["execution_profile"]["output_token_limit"] == 16000
    assert (tmp_path / invocation_relative_path(record["invocation_id"])).exists()


def test_capture_records_the_effective_output_token_limit(tmp_path):
    from ai_lab.providers.invocation_capture import capture_provider_invocation

    provider = _StubProvider()
    provider._max_tokens = 4096

    record, error = capture_provider_invocation(
        repo_root=tmp_path,
        provider=provider,
        rendered_prompt="prompt",
        session_id="SESSION-limitcapture",
        session_state_mode=SESSION_STATELESS,
        occurred_at="2026-07-22T12:00:00+00:00",
        status=STATUS_SUCCESS,
    )

    assert error is None
    assert record["execution_profile"]["output_token_limit"] == 4096


def test_session_state_mode_is_observed_from_the_run(tmp_path):
    from ai_lab.providers.invocation_capture import session_state_mode_for_run

    assert session_state_mode_for_run(False) == SESSION_STATELESS
    assert session_state_mode_for_run(True) == "explicit_replayed_context"


def test_session_identity_is_unique_per_run():
    from ai_lab.providers.invocation_capture import new_session_id

    assert new_session_id() != new_session_id()


def test_comparison_path_imports_capture_and_ask_provider_does_not():
    compare_source = Path("scripts/compare_providers.py").read_text(encoding="utf-8")
    ask_source = Path("scripts/ask_provider.py").read_text(encoding="utf-8")

    assert "invocation_capture" in compare_source
    assert "invocation_capture" not in ask_source


# --- documentation and registry artifacts ------------------------------


def test_predicate_registry_documents_every_slice_a_predicate():
    registry = Path("docs/self_model/PREDICATE_REGISTRY.md").read_text(encoding="utf-8")

    for predicate in SLICE_A_PREDICATES:
        assert f"### {predicate}" in registry

    for required in ("source type", "target type", "cardinality", "temporal semantics"):
        assert required in registry


def test_invocation_record_documentation_states_the_limitations():
    doc = Path("docs/self_model/INVOCATION_RECORDS.md").read_text(encoding="utf-8")

    assert "IDENTITY_FIELDS_V1" in doc
    assert "pre-provenance" in doc
    assert "partial_declared_channels_only" in doc
    assert "unresolved" in doc


# --- integration: capture on the comparison path without network -------


def test_comparison_run_captures_one_record_per_provider(tmp_path, monkeypatch, capsys):
    from scripts import compare_providers

    class _FakeProvider:
        def __init__(self, name, model):
            self._name = name
            self._model = model
            self._max_tokens = 16000
            self._effort = None

        @property
        def name(self):
            return self._name

        @property
        def model(self):
            return self._model

        def ask(self, prompt):
            return f"{self._name} answer"

    monkeypatch.setattr(compare_providers, "CAPTURE_REPO_ROOT", tmp_path)
    monkeypatch.setattr(
        compare_providers, "OpenAIProvider", lambda: _FakeProvider("OpenAI", "gpt-5")
    )
    monkeypatch.setattr(
        compare_providers,
        "ClaudeProvider",
        lambda: _FakeProvider("Claude", "claude-sonnet-4-5"),
    )
    out_dir = tmp_path / "comparisons"
    monkeypatch.setattr(
        "sys.argv",
        [
            "compare_providers.py",
            "integration probe",
            "--title",
            "Slice A integration",
            "--out-dir",
            str(out_dir),
        ],
    )

    assert compare_providers.main() == 0

    written = sorted((tmp_path / "docs" / "invocations").glob("INV-*.json"))
    assert len(written) == 2

    records = [json.loads(path.read_text(encoding="utf-8")) for path in written]
    for record in records:
        validate_invocation_record(record)
        assert record["capture_path"] == CAPTURE_PATH_COMPARE_PROVIDERS
        assert record["status"] == STATUS_SUCCESS
        assert record["governance_marker"] == MARKER_EXPERIMENTAL
        assert record["session_id"]
        assert record["execution_profile"]["output_token_limit"] == 16000

    # One session per run: both calls share the same continuity boundary.
    assert len({record["session_id"] for record in records}) == 1
    assert len({record["invocation_id"] for record in records}) == 2

    artifact = next(out_dir.glob("*.md")).read_text(encoding="utf-8")
    for record in records:
        assert record["invocation_id"] in artifact


def test_comparison_run_reports_capture_failure_and_still_completes(
    tmp_path, monkeypatch, capsys
):
    from scripts import compare_providers

    class _FakeProvider:
        name = "Claude"
        model = "claude-sonnet-4-5"
        _max_tokens = 16000
        _effort = None

        def ask(self, prompt):
            return "answer despite capture failure"

    blocked = tmp_path / "blocked"
    blocked.write_text("not a directory", encoding="utf-8")

    monkeypatch.setattr(compare_providers, "CAPTURE_REPO_ROOT", blocked)
    monkeypatch.setattr(compare_providers, "OpenAIProvider", lambda: _FakeProvider())
    monkeypatch.setattr(compare_providers, "ClaudeProvider", lambda: _FakeProvider())
    monkeypatch.setattr(
        "sys.argv",
        ["compare_providers.py", "probe", "--print-prompt"],
    )

    assert compare_providers.main() == 0


# --- capture fidelity (findings from the first real run) ---------------


def test_absent_token_limit_is_recorded_as_explicitly_unset(tmp_path):
    from ai_lab.providers.invocation_capture import capture_provider_invocation

    class _NoLimitProvider:
        name = "OpenAI"
        model = "gpt-5"

        def ask(self, prompt):
            return "answer"

    record, error = capture_provider_invocation(
        repo_root=tmp_path,
        provider=_NoLimitProvider(),
        rendered_prompt="prompt",
        session_id="SESSION-nolimitcase",
        session_state_mode=SESSION_STATELESS,
        occurred_at="2026-07-22T12:00:00+00:00",
        status=STATUS_SUCCESS,
    )

    assert error is None
    profile = record["execution_profile"]
    assert profile["output_token_limit"] is None
    # Null must not be ambiguous between "unset" and "not captured".
    assert profile["provider_request_flags"]["max_tokens_source"] == "provider_default_unset"


def test_environment_sourced_limit_is_labelled(tmp_path, monkeypatch):
    from ai_lab.providers.invocation_capture import capture_provider_invocation

    monkeypatch.setenv("AI_LAB_CLAUDE_MAX_TOKENS", "2048")

    record, error = capture_provider_invocation(
        repo_root=tmp_path,
        provider=_StubProvider(),
        rendered_prompt="prompt",
        session_id="SESSION-envsourced1",
        session_state_mode=SESSION_STATELESS,
        occurred_at="2026-07-22T12:00:00+00:00",
        status=STATUS_SUCCESS,
    )

    assert error is None
    assert (
        record["execution_profile"]["provider_request_flags"]["max_tokens_source"]
        == "environment"
    )


def test_runtime_version_is_captured_when_the_sdk_is_known(tmp_path):
    from ai_lab.providers.invocation_capture import capture_provider_invocation

    record, error = capture_provider_invocation(
        repo_root=tmp_path,
        provider=_StubProvider(),
        rendered_prompt="prompt",
        session_id="SESSION-runtimevers",
        session_state_mode=SESSION_STATELESS,
        occurred_at="2026-07-22T12:00:00+00:00",
        status=STATUS_SUCCESS,
    )

    assert error is None
    runtime = record["execution_profile"]["runtime_version"]
    assert runtime is None or runtime.startswith("anthropic==")


def test_structured_artifact_metadata_is_json_not_python_repr():
    import json as _json

    from scripts.compare_providers import build_markdown_artifact

    artifact = build_markdown_artifact(
        prompt="p",
        responses={"Claude": {"model": "m", "response": "r"}},
        created_at="2026-07-22T00:00:00+00:00",
        command="cmd",
        comparison_id="COMP-9999",
        title="t",
        extra_metadata={
            "invocation_produced_by": [
                {"source_id": "COMP-9999", "predicate": "produced_by", "authoritative": False}
            ]
        },
    )

    line = next(
        l for l in artifact.splitlines() if l.startswith("- invocation_produced_by:")
    )
    payload = line.split("`", 1)[1].rsplit("`", 1)[0]
    parsed = _json.loads(payload)
    assert parsed[0]["source_id"] == "COMP-9999"
    assert parsed[0]["authoritative"] is False
