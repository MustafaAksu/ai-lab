"""R18 schema bootstrap failures are separate from r2 assessment envelopes."""

from __future__ import annotations

import copy
import hashlib

import pytest

from ai_lab.providers import qualification_records as qr
from ai_lab.providers.qualification import evaluate_production_r2, evaluate_synthetic_r2
from ai_lab.providers.catalog_resolution import resolve_identity
from ai_lab.providers.executor_equivalence import equivalence
from qualification_fixtures import build_fixture


@pytest.fixture(autouse=True)
def fresh_schema_cache():
    qr._schema.cache_clear()
    yield
    qr._schema.cache_clear()


def observe(call):
    """Record the boundary, so a missing guard causes an ordinary assertion."""
    try:
        return call(), None
    except Exception as error:
        return None, error


def assert_bootstrap(observed, code):
    value, error = observed
    expected = getattr(qr, "QualificationBootstrapError", None)
    assert expected is not None, f"no declared bootstrap type; observed {type(error).__name__}"
    assert value is None and isinstance(error, expected), repr(error)
    assert not isinstance(error, qr.QualificationError)
    assert error.code == code
    assert isinstance(error.detail, str) and error.detail
    assert len(str(error)) < 1200


def broken_schema(tmp_path, monkeypatch, mode):
    path = tmp_path / "broken-schema.json"
    if mode == "digest":
        path.write_bytes(qr.SCHEMA_PATH.read_bytes() + b"\n")
    monkeypatch.setattr(qr, "SCHEMA_PATH", path)
    qr._schema.cache_clear()
    return "QUALIFICATION_SCHEMA_UNAVAILABLE" if mode == "missing" else "QUALIFICATION_SCHEMA_DIGEST_MISMATCH"


@pytest.mark.parametrize("mode", ["missing", "digest"])
@pytest.mark.parametrize("entry", ["synthetic", "production"])
def test_r18_missing_or_changed_schema_has_declared_bootstrap_exception(tmp_path, monkeypatch, mode, entry):
    fixture = build_fixture(tmp_path)
    anchor = fixture.anchor()
    query = copy.deepcopy(fixture.query)
    query["domain"] = entry
    code = broken_schema(tmp_path, monkeypatch, mode)
    call = (lambda: evaluate_synthetic_r2(query, anchor=anchor)) if entry == "synthetic" else (lambda: evaluate_production_r2(query))
    assert_bootstrap(observe(call), code)


@pytest.mark.parametrize("entry", ["synthetic", "production"])
def test_r18_bootstrap_failure_precedes_invalid_query_envelope(tmp_path, monkeypatch, entry):
    code = broken_schema(tmp_path, monkeypatch, "missing")
    call = (lambda: evaluate_synthetic_r2(b"invalid-json", anchor=None)) if entry == "synthetic" else (lambda: evaluate_production_r2(b"invalid-json"))
    assert_bootstrap(observe(call), code)


@pytest.mark.parametrize("entry", ["synthetic", "production"])
def test_r18_bootstrap_error_does_not_reload_schema_for_its_own_encoding(monkeypatch, entry):
    class UnavailableSchema:
        reads = 0

        def read_bytes(self):
            self.reads += 1
            raise OSError("unavailable fixture schema")

    source = UnavailableSchema()
    monkeypatch.setattr(qr, "SCHEMA_PATH", source)
    call = (lambda: evaluate_synthetic_r2({}, anchor=None)) if entry == "synthetic" else (lambda: evaluate_production_r2({}))
    assert_bootstrap(observe(call), "QUALIFICATION_SCHEMA_UNAVAILABLE")
    assert source.reads == 1


@pytest.mark.parametrize("mode", ["missing", "digest"])
def test_r18_legacy_adapters_remain_blocking_during_bootstrap_failure(tmp_path, monkeypatch, mode):
    fixture = build_fixture(tmp_path)
    anchor = fixture.anchor()
    left, right = fixture.state["invocations"]
    broken_schema(tmp_path, monkeypatch, mode)
    resolution = resolve_identity(invocation=left, snapshot={}, capture={}, query=fixture.query, anchor=anchor)
    relation = equivalence(left=left, right=right, snapshots=[], query=fixture.query, anchor=anchor)
    assert resolution["resolved"] is False and resolution["assessment_ref"] is None
    assert resolution["diagnostic_codes"] == ["NOT_EVALUATED"]
    assert relation.blocks_adjudication is True and relation.status == "unresolved"
    assert relation.assessment_ref is None and relation.diagnostic_codes == ("NOT_EVALUATED",)


@pytest.mark.parametrize("content", [b"{not-json", b'{"type":7}'])
def test_r18_unparseable_or_invalid_schema_is_typed_bootstrap_failure(tmp_path, monkeypatch, content):
    # Fault injection exercises the decoding/metaschema boundary independently
    # of the immutable production digest; this is not a new accepted schema.
    path = tmp_path / "invalid-schema.json"
    path.write_bytes(content)
    monkeypatch.setattr(qr, "SCHEMA_PATH", path)
    monkeypatch.setattr(qr, "SCHEMA_SHA256", hashlib.sha256(content).hexdigest())
    assert_bootstrap(observe(lambda: evaluate_production_r2({})), "QUALIFICATION_SCHEMA_INVALID")


def test_r18_bootstrap_exception_itself_needs_no_schema(monkeypatch):
    expected = getattr(qr, "QualificationBootstrapError", None)
    assert expected is not None

    def forbidden():
        raise AssertionError("error formatting must not load the failed schema")

    monkeypatch.setattr(qr, "reason_codes", forbidden)
    error = expected("QUALIFICATION_SCHEMA_UNAVAILABLE", "unavailable")
    assert error.code == "QUALIFICATION_SCHEMA_UNAVAILABLE"
    assert str(error) == "QUALIFICATION_SCHEMA_UNAVAILABLE: unavailable"


def test_r18_successfully_pinned_schema_is_a_load_once_snapshot(tmp_path, monkeypatch):
    fixture = build_fixture(tmp_path)
    anchor = fixture.anchor()
    qr.validate_shape(fixture.query, "Query")
    monkeypatch.setattr(qr, "SCHEMA_PATH", tmp_path / "missing-after-valid-bootstrap.json")
    result = evaluate_synthetic_r2(fixture.query, anchor=anchor)
    assert result["validation_status"] == "valid"
    assert result["Q_identity"]["value"] == "conditions_satisfied"
    for key in ("C3", "C10", "Q_C3_C10"):
        assert result[key]["value"] == "unresolved"


def test_r18_valid_schema_keeps_normal_invalid_result_contract():
    result = evaluate_production_r2(b"invalid-json")
    assert result["validation_status"] == "invalid"
    assert result["Q_identity"]["value"] == "withheld"
    assert result["query_ref"] is None
    qr.validate_shape(result, "AssessmentResult")
