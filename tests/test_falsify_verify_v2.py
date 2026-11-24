"""R12: falsification evidence must be a test failure, not a broken test run."""

from __future__ import annotations

import base64
import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/falsify_verify_v2.py"


def load_harness():
    spec = importlib.util.spec_from_file_location("falsify_under_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def harness():
    return load_harness()


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), "-c", "core.hooksPath=/dev/null",
                           "-c", "commit.gpgsign=false", "-c", "user.name=Test",
                           "-c", "user.email=test@example.invalid", *args],
                          check=True, capture_output=True, text=True).stdout.strip()


def source_repo(tmp_path: Path, *, expected=1) -> Path:
    repo = tmp_path / "source"
    (repo / "tests").mkdir(parents=True)
    (repo / "sample.py").write_text("def value():\n    return 1\n")
    (repo / "tests/test_probe.py").write_text(
        "import pytest\nfrom sample import value\n"
        "@pytest.mark.parametrize('label', ['a', 'b'])\n"
        "def test_probe(label):\n"
        f"    assert value() == {expected}\n"
    )
    git(repo, "init", "-q")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "fixture")
    return repo


def mutation(new="return 2", *, selector="test_probe", name="guard"):
    return (name, "sample.py", "return 1", new, selector, "tests/test_probe.py")


def test_import_is_safe_without_arguments(monkeypatch):
    monkeypatch.setattr(sys, "argv", [])
    module = load_harness()
    assert callable(module.main)
    assert len(module.MUTATIONS) >= 33
    # Historical cases must remain individually identifiable when new cases land.
    assert module.MUTATIONS[0][0] == "F1 writer accepts an exit code"
    assert any(m[0] == "agreement: validator copy diverges" for m in module.MUTATIONS)


@pytest.mark.parametrize(("new", "expected_status"), [
    ("return 2", "CAUGHT"),
    ("return 1  # a surviving mutation", "NOT_CAUGHT"),
    ("return (", "ERROR"),  # Collection SyntaxError must never look caught.
    ("raise ModuleNotFoundError('missing dependency')", "ERROR"),
    ("raise FileNotFoundError('missing executable')", "ERROR"),
    ("raise RuntimeError('unrelated runtime failure')", "ERROR"),
])
def test_real_pytest_outcomes_are_not_inferred_from_nonzero_exit(harness, tmp_path, new, expected_status):
    repo = source_repo(tmp_path)
    original = (repo / "sample.py").read_bytes()
    report = harness.run_mutations(repo, [mutation(new)])
    result = report["results"][0]
    assert result["status"] == expected_status
    baseline = report["baselines"][result["baseline_id"]]
    assert baseline["returncode"] == 0
    assert baseline["pytest"]["selected_nodeids"] == [
        "tests/test_probe.py::test_probe[a]", "tests/test_probe.py::test_probe[b]"]
    if expected_status == "CAUGHT":
        assert result["failed_nodeids"] == result["expected_nodeids"]
        assert "assert 2 == 1" in result["mutation_run"]["stdout"]["data"]
        failures = [r for r in result["mutation_run"]["pytest"]["reports"] if r["outcome"] == "failed"]
        assert all(r["when"] == "call" and r["longrepr"] for r in failures)
    assert (repo / "sample.py").read_bytes() == original
    assert git(repo, "status", "--porcelain") == ""


def test_baseline_failure_blocks_mutation(harness, tmp_path):
    repo = source_repo(tmp_path, expected=99)
    report = harness.run_mutations(repo, [mutation()])
    result = report["results"][0]
    assert result["status"] == "ERROR"
    assert "baseline did not pass" in result["reason"]
    assert result["mutation_run"] is None
    assert report["summary"]["caught"] == 0


def test_empty_baseline_selection_is_an_error(harness, tmp_path):
    repo = source_repo(tmp_path)
    report = harness.run_mutations(repo, [mutation(selector="nothing_matches")])
    result = report["results"][0]
    assert result["status"] == "ERROR"
    assert result["mutation_run"] is None
    baseline = report["baselines"][result["baseline_id"]]
    assert baseline["returncode"] == 5
    assert baseline["pytest"]["selected_nodeids"] == []


def test_mutation_must_execute_the_exact_baseline_nodeids(harness, tmp_path):
    repo = source_repo(tmp_path)
    change = ("renamed test", "tests/test_probe.py", "def test_probe", "def test_other",
              "probe", "tests/test_probe.py")
    result = harness.run_mutations(repo, [change])["results"][0]
    assert result["status"] == "ERROR"
    assert result["reason"] == "mutation changed the exact selected nodeids"


def test_pytest_fail_is_a_test_failure(harness, tmp_path):
    repo = source_repo(tmp_path)
    change = ("pytest fail", "tests/test_probe.py", "assert value() == 1", "pytest.fail('guard failed')",
              "test_probe", "tests/test_probe.py")
    result = harness.run_mutations(repo, [change])["results"][0]
    assert result["status"] == "CAUGHT"
    assert {r["failure_kind"] for r in result["mutation_run"]["pytest"]["reports"]
            if r["outcome"] == "failed"} == {"pytest_fail"}


def test_each_mutation_starts_fresh_and_caller_flags_cannot_hide_tests(harness, tmp_path, monkeypatch):
    repo = source_repo(tmp_path)
    monkeypatch.setenv("PYTEST_ADDOPTS", "--collect-only -k nothing_matches")
    monkeypatch.setenv("PYTEST_PLUGINS", "plugin_that_does_not_exist")
    report = harness.run_mutations(repo, [mutation(name="two"), mutation("return 3", name="three")])
    assert [r["status"] for r in report["results"]] == ["CAUGHT", "CAUGHT"]
    assert len(report["baselines"]) == 1  # Same immutable baseline, same selected tests.
    assert "assert 3 == 1" in report["results"][1]["mutation_run"]["stdout"]["data"]
    assert (repo / "sample.py").read_text() == "def value():\n    return 1\n"


def test_timeout_never_counts_as_caught_and_preserves_source(harness, tmp_path):
    repo = source_repo(tmp_path)
    result = harness.run_mutations(repo, [mutation("__import__('time').sleep(30); return 2")],
                                   timeout=3)["results"][0]
    assert result["status"] == "ERROR"
    assert result["reason"] == "pytest timed out"
    assert result["mutation_run"]["timed_out"] is True
    assert git(repo, "status", "--porcelain") == ""


def good_run(*, failed=False):
    nodeid = "tests/test_probe.py::test_probe"
    reports = [dict(nodeid=nodeid, when=when, outcome="passed", wasxfail=None,
                    failure_kind=None, exception=None, longrepr="")
               for when in ("setup", "call", "teardown")]
    if failed:
        reports[1].update(outcome="failed", failure_kind="assertion",
                          exception="builtins.AssertionError", longrepr="assert 2 == 1")
    return {"returncode": int(failed), "timed_out": False, "start_error": None, "report_error": None,
            "pytest": {"schema": "pytest-falsification-v1", "selected_nodeids": [nodeid], "reports": reports,
                       "collection_errors": [], "internal_errors": [], "interrupted": False,
                       "session_finished": True, "exitstatus": int(failed)}}


@pytest.mark.parametrize("damage", [
    "collection", "internal", "interrupted", "incomplete", "missing_report", "bad_report",
    "setup", "teardown", "skipped", "xfail", "unrelated_exception", "missing_call",
    "missing_failure_output", "duplicate_call", "unexpected_node", "status_mismatch",
    "usage_exit", "internal_exit", "timeout", "failed_to_start",
])
def test_report_protocol_fails_closed_for_non_test_failures(harness, damage):
    run = good_run(failed=True)
    data = run["pytest"]
    if damage in ("collection", "internal"):
        data[damage + "_errors"] = ["broken environment"]
    elif damage == "interrupted":
        data["interrupted"] = True
    elif damage == "incomplete":
        data["session_finished"] = False
    elif damage == "missing_report":
        run["pytest"] = None
    elif damage == "bad_report":
        run["report_error"] = "invalid JSON"
    elif damage in ("setup", "teardown"):
        data["reports"][0 if damage == "setup" else 2]["outcome"] = "failed"
    elif damage == "skipped":
        data["reports"][1]["outcome"] = "skipped"
    elif damage == "xfail":
        data["reports"][1]["wasxfail"] = "known failure"
    elif damage == "unrelated_exception":
        data["reports"][1].update(failure_kind="exception", exception="builtins.OSError")
    elif damage == "missing_call":
        del data["reports"][1]
    elif damage == "missing_failure_output":
        data["reports"][1]["longrepr"] = ""
    elif damage == "duplicate_call":
        data["reports"].append(copy.deepcopy(data["reports"][1]))
    elif damage == "unexpected_node":
        data["reports"][1]["nodeid"] = "tests/test_probe.py::unselected"
    elif damage == "status_mismatch":
        data["exitstatus"] = 0
    elif damage in ("usage_exit", "internal_exit"):
        run["returncode"] = 4 if damage == "usage_exit" else 3
    elif damage == "timeout":
        run["timed_out"] = True
    elif damage == "failed_to_start":
        run["start_error"] = "executable missing"
    assert harness._run_problem(run) is not None


def test_protocol_accepts_complete_pass_and_assertion_failure(harness):
    assert harness._run_problem(good_run()) is None
    assert harness._run_problem(good_run(failed=True)) is None


def test_report_retains_baseline_nodeids_and_failure_output(harness, tmp_path, monkeypatch):
    repo = source_repo(tmp_path)
    monkeypatch.setattr(harness, "MUTATIONS", [mutation()])
    path = tmp_path / "reports/evidence.json"
    assert harness.main([str(repo), "--report", str(path)]) == 0
    report = json.loads(path.read_text())
    result = report["results"][0]
    assert result["failed_nodeids"] == report["baselines"][result["baseline_id"]]["pytest"]["selected_nodeids"]
    assert "assert 2 == 1" in result["mutation_run"]["stdout"]["data"]
    with pytest.raises(SystemExit) as exc:
        harness.main([str(repo), "--report", str(repo / "evidence.json")])
    assert exc.value.code == 2
    assert not (repo / "evidence.json").exists()


def test_unapplicable_anchor_and_empty_registry_cannot_pass(harness, tmp_path):
    repo = source_repo(tmp_path)
    change = ("missing", "sample.py", "not present", "different", "test_probe", "tests/test_probe.py")
    report = harness.run_mutations(repo, [change])
    assert report["summary"]["caught"] == 0
    assert report["results"][0]["status"] == "NOT_APPLICABLE"
    with pytest.raises(harness.HarnessError, match="at least one"):
        harness.run_mutations(repo, [])


def test_binary_output_is_retained_losslessly(harness):
    original = b"bad byte: \xff\x00\n"
    retained = harness._stream(original)
    assert retained["encoding"] == "base64"
    assert base64.b64decode(retained["data"]) == original
    assert retained["bytes"] == len(original)
