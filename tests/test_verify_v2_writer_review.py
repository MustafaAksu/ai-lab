"""Writer review cases: profile domain, observation limits, and failure publication.

All command execution uses disposable fixture repositories and local commands.
The status-hidden mutation is a documented observation limit, not a claim of
byte-level tree integrity. Failure diagnostics are deliberately non-importable.
"""

from __future__ import annotations

import copy
import json
import os
from pathlib import Path

import pytest

from ai_lab.documentation import verification_v2 as v2
from tests.test_verify_v2 import (
    OK,
    PROFILE_PATH,
    RECORDED_BY,
    _load_importer_module,
    _load_writer_module,
    _target_repo,
    blob,
    cmd,
    make_repo,
    profile,
    receipt_of,
    run_writer,
)


def _bad_profiles():
    cases = [("not-object", None), ("list", []), ("empty", {})]
    changes = {
        "profile_schema": [None, [], "other"],
        "profile_id": [None, False, "", "bad\0id"],
        "permitted_tree_changes": [None, {}, ["allowed"]],
        "environment": [None, [], {1: "x"}, {"BAD\n": "x"}, {"HOME": "x"},
                        {"MY_TOKEN": "x"}, {"VALUE": None}, {"VALUE": False},
                        {"VALUE": "$HOME"}, {"VALUE": "bad\0value"}],
        "commands": [None, [], [None], [False]],
    }
    for field, values in changes.items():
        for index, value in enumerate(values):
            p = profile(copy.deepcopy(OK))
            p[field] = value
            cases.append((f"{field}-{index}", p))
    command_changes = {
        "argv": [None, "python", [], [False], [""], ["bad\0arg"]],
        "timeout_seconds": [None, True, "1", [], 0, -1, 86400, 10 ** 400,
                            float("nan"), float("inf"), -float("inf")],
        "declared_property": [None, False, "", "bad\0property"],
    }
    for field, values in command_changes.items():
        for index, value in enumerate(values):
            p = profile(copy.deepcopy(OK))
            p["commands"][0][field] = value
            cases.append((f"command-{field}-{index}", p))
    return cases


@pytest.mark.parametrize("name,invalid", _bad_profiles(), ids=lambda value: value if isinstance(value, str) else None)
def test_profile_domain_rejects_malformed_values_without_unexpected_errors(name, invalid):
    writer = _load_writer_module()
    with pytest.raises(writer.Refusal):
        writer._check_profile(invalid)


@pytest.mark.parametrize("timeout", [0.001, 1, 86399.5])
def test_profile_domain_accepts_finite_timeouts_and_literal_empty_environment_value(timeout):
    writer = _load_writer_module()
    p = profile(cmd("print('ok')", timeout=timeout), environment={"VALUE": ""})
    writer._check_profile(p)
    assert v2.load_profile(json.dumps(p).encode()) == p


def _args(tmp_path, repo, commit, *, receipt=None, store=None):
    return ["--repo", str(repo), "--commit", commit, "--profile", PROFILE_PATH,
            "--store-root", str(store or tmp_path / "store"),
            "--receipt-out", str(receipt or tmp_path / "receipt.json")]


def _fail(secret):
    def failure(*args, **kwargs):
        raise OSError(secret)
    return failure


def _diagnostic(tmp_path, stderr, *, directory=None):
    notice = json.loads(stderr)
    assert notice["receipt_written"] is False
    path = Path(notice["failure_diagnostic"])
    assert path.parent == (directory or tmp_path)
    raw = path.read_bytes()
    failure = json.loads(raw)
    assert failure["failure_schema"] == "ai-lab/verify-v2-failure/1"
    assert failure["receipt_written"] is False
    assert failure["exit_code"] == 3
    assert len(raw) <= _load_writer_module().FAILURE_DIAGNOSTIC_LIMIT_BYTES
    assert "receipt_schema" not in failure and "schema_version" not in failure
    return path, failure


def _stored_receipts(store):
    receipts = []
    for path in store.rglob("*"):
        if not path.is_file():
            continue
        try:
            payload = json.loads(path.read_bytes())
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        if isinstance(payload, dict) and payload.get("receipt_schema") == v2.RECEIPT_SCHEMA:
            receipts.append(path)
    return receipts


def test_profile_refusal_occurs_before_any_command_and_writes_no_diagnostic(tmp_path, monkeypatch, capsys):
    writer = _load_writer_module()
    invalid = profile(OK, environment={"VALUE": "bad\0value"})
    repo, commit = make_repo(tmp_path, invalid)
    monkeypatch.setattr(writer, "_run_command", lambda *a, **kw: pytest.fail("malformed profile executed"))
    assert writer.main(_args(tmp_path, repo, commit)) == 2
    assert not (tmp_path / "receipt.json").exists()
    assert not list(tmp_path.glob("verify-v2-failure-*.json"))
    assert "refused" in capsys.readouterr().err


def test_tree_scope_explicitly_records_status_hidden_assume_unchanged_limit(tmp_path):
    mutate = cmd(
        "import subprocess; from pathlib import Path; "
        "subprocess.run(['git', 'update-index', '--assume-unchanged', 'tracked.txt'], check=True); "
        "Path('tracked.txt').write_text('hidden mutation'); print(Path('tracked.txt').read_text())"
    )
    repo, commit = make_repo(tmp_path, profile(mutate))
    proc, receipt_path, store = run_writer(tmp_path, repo, commit)
    assert proc.returncode == 0, proc.stderr
    receipt = receipt_of(receipt_path)
    assert blob(store, receipt["commands"][0]["stdout"]) == b"hidden mutation\n"
    assert receipt["commands"][0]["boundary_after"]["status_clean"] is True
    assert receipt["result"] == "all_commands_exit_zero"
    scope = receipt["tree_observation"]["scope"]
    assert "Git-status-reported paths only" in scope
    assert "not byte-level tree equality" in scope
    assert "assume-unchanged" in scope
    v2.validate_receipt(receipt, store)


def test_atomic_write_failure_does_not_publish_partial_bytes(tmp_path, monkeypatch):
    writer = _load_writer_module()
    target = tmp_path / "receipt.json"
    monkeypatch.setattr(writer.os, "fsync", _fail("private failure detail"))
    with pytest.raises(OSError):
        writer._atomic_write_exclusive(target, b"complete receipt bytes")
    assert not target.exists()
    assert not list(tmp_path.glob(".verify-v2-*"))


def test_atomic_write_never_overwrites_a_concurrent_destination(tmp_path, monkeypatch):
    writer = _load_writer_module()
    target = tmp_path / "receipt.json"
    original_link = os.link

    def raced_link(source, destination):
        Path(destination).write_bytes(b"competing receipt")
        return original_link(source, destination)

    monkeypatch.setattr(writer.os, "link", raced_link)
    with pytest.raises(FileExistsError):
        writer._atomic_write_exclusive(target, b"our receipt")
    assert target.read_bytes() == b"competing receipt"
    assert not list(tmp_path.glob(".verify-v2-*"))


def test_atomic_store_failure_does_not_leave_a_partial_digest_blob(tmp_path, monkeypatch):
    writer = _load_writer_module()
    store = writer.Store(tmp_path / "store")
    monkeypatch.setattr(writer.os, "fsync", _fail("disk detail"))
    with pytest.raises(OSError):
        store.put(b"blob bytes")
    assert not [p for p in store.root.rglob("*") if p.is_file()]


@pytest.mark.parametrize("existing_kind", ["regular", "broken_symlink"])
def test_existing_receipt_name_is_refused_without_overwrite(tmp_path, existing_kind, capsys):
    writer = _load_writer_module()
    repo, commit = make_repo(tmp_path, profile(OK))
    target = tmp_path / "receipt.json"
    elsewhere = tmp_path / "absent-target.json"
    if existing_kind == "regular":
        target.write_bytes(b"existing receipt")
    else:
        target.symlink_to(elsewhere)
    assert writer.main(_args(tmp_path, repo, commit)) == 2
    if existing_kind == "regular":
        assert target.read_bytes() == b"existing receipt"
    else:
        assert target.is_symlink() and not elsewhere.exists()
    assert not list(tmp_path.glob("verify-v2-failure-*.json"))
    assert "overwrite" in capsys.readouterr().err


@pytest.mark.parametrize("stage", ["capture_environment", "run_command", "serialize_receipt",
                                  "store_receipt", "publish_receipt"])
def test_unexpected_failure_has_no_receipt_and_bounded_nonimportable_diagnostic(
    tmp_path, monkeypatch, capsys, stage,
):
    writer = _load_writer_module()
    repo, commit = make_repo(tmp_path, profile(OK))
    secret = "private-exception-payload-do-not-retain-9342"
    receipt_out = tmp_path / "receipt.json"
    store = tmp_path / "store"
    if stage == "capture_environment":
        monkeypatch.setattr(writer, "_installed_distributions", _fail(secret))
    elif stage == "run_command":
        monkeypatch.setattr(writer, "_run_command", _fail(secret))
    elif stage == "serialize_receipt":
        original = writer.json.dumps

        def fail_receipt_dump(value, *args, **kwargs):
            if isinstance(value, dict) and "receipt_schema" in value:
                raise OSError(secret)
            return original(value, *args, **kwargs)

        monkeypatch.setattr(writer.json, "dumps", fail_receipt_dump)
    elif stage == "store_receipt":
        original = writer.Store.put

        def fail_receipt_put(self, data):
            if b'"receipt_schema"' in data:
                raise OSError(secret)
            return original(self, data)

        monkeypatch.setattr(writer.Store, "put", fail_receipt_put)
    else:
        original = writer._atomic_write_exclusive

        def fail_receipt_publish(path, data):
            if path == receipt_out:
                raise OSError(secret)
            return original(path, data)

        monkeypatch.setattr(writer, "_atomic_write_exclusive", fail_receipt_publish)

    assert writer.main(_args(tmp_path, repo, commit)) == 3
    captured = capsys.readouterr()
    assert captured.out == ""
    assert secret not in captured.err
    assert not receipt_out.exists()
    assert _stored_receipts(store) == []
    diagnostic, failure = _diagnostic(tmp_path, captured.err)
    assert failure["stage"] == stage
    assert failure["error_type"] == "OSError"
    assert secret.encode() not in diagnostic.read_bytes()
    assert store not in diagnostic.parents
    with pytest.raises(v2.VerificationV2Error):
        v2.validate_receipt(failure, store)
    with pytest.raises(v2.VerificationV2Error):
        v2.validate_canonical_structure(failure)
    importer = _load_importer_module()
    destination = _target_repo(tmp_path / "target")
    with pytest.raises(importer.ImportRefusal):
        importer.import_receipt(destination, diagnostic, store, RECORDED_BY)
    assert list((destination / "docs/self_model/verifications").iterdir()) == []


def test_failure_diagnostic_stays_outside_cas_when_receipt_requested_inside_it(tmp_path, monkeypatch, capsys):
    writer = _load_writer_module()
    repo, commit = make_repo(tmp_path, profile(OK))
    store = tmp_path / "store"
    monkeypatch.setattr(writer, "_installed_distributions", _fail("private"))
    assert writer.main(_args(tmp_path, repo, commit, receipt=store / "receipt.json", store=store)) == 3
    path, _ = _diagnostic(tmp_path, capsys.readouterr().err)
    assert store not in path.parents
    assert not (store / "receipt.json").exists()


def test_failure_diagnostic_unavailable_still_reports_exit_three_without_raw_exception(
    tmp_path, monkeypatch, capsys,
):
    writer = _load_writer_module()
    repo, commit = make_repo(tmp_path, profile(OK))
    monkeypatch.setattr(writer, "_installed_distributions", _fail("private crash"))
    original = writer._atomic_write_exclusive

    def fail_diagnostic(path, data):
        if path.name.startswith("verify-v2-failure-"):
            raise PermissionError("private diagnostic detail")
        return original(path, data)

    monkeypatch.setattr(writer, "_atomic_write_exclusive", fail_diagnostic)
    assert writer.main(_args(tmp_path, repo, commit)) == 3
    captured = capsys.readouterr()
    notice = json.loads(captured.err)
    assert notice["failure_diagnostic"] is None
    assert "private" not in captured.err
    assert not (tmp_path / "receipt.json").exists()


@pytest.mark.parametrize("command,exit_code,result", [
    (OK, 0, "all_commands_exit_zero"),
    (cmd("raise SystemExit(7)"), 1, "one_or_more_commands_failed"),
    (cmd("import time; time.sleep(1)", timeout=0.05), 3, "incomplete"),
])
def test_exit_table_receipt_results_are_distinct_from_failure_diagnostics(tmp_path, command, exit_code, result):
    repo, commit = make_repo(tmp_path, profile(command))
    proc, receipt_path, store = run_writer(tmp_path, repo, commit)
    assert proc.returncode == exit_code, proc.stderr
    receipt = receipt_of(receipt_path)
    assert receipt["result"] == result
    v2.validate_receipt(receipt, store)
    assert not list(tmp_path.glob("verify-v2-failure-*.json"))


@pytest.mark.parametrize("payload", [[], {"repo_head": False}, {"repo_head": "short"}, {"repo_head": {}}])
def test_history_malformed_stored_head_remains_explicitly_unavailable(tmp_path, payload):
    repo, commit = make_repo(tmp_path, profile(OK),
                             files={"docs/self_model/SELF_MODEL.json": json.dumps(payload)})
    proc, receipt_path, store = run_writer(tmp_path, repo, commit)
    assert proc.returncode == 0, proc.stderr
    receipt = receipt_of(receipt_path)
    assert receipt["history"]["stored_repo_head"] is None
    assert receipt["history"]["stored_repo_head_reachable"] is None
    v2.validate_receipt(receipt, store)


@pytest.mark.parametrize("event_name", ["pull_request", "pull_request_target"])
def test_missing_pull_request_metadata_fails_without_malformed_receipt(tmp_path, monkeypatch, capsys, event_name):
    writer = _load_writer_module()
    repo, commit = make_repo(tmp_path, profile(OK))
    monkeypatch.setenv("GITHUB_EVENT_NAME", event_name)
    monkeypatch.delenv("GITHUB_EVENT_PATH", raising=False)
    assert writer.main([*_args(tmp_path, repo, commit), "--runner-kind", "github_actions"]) == 3
    _, failure = _diagnostic(tmp_path, capsys.readouterr().err)
    assert failure["stage"] == "capture_runner"
    assert not (tmp_path / "receipt.json").exists()
