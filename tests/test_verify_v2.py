"""VERIFY v2 falsification and integration tests (PLAN-20261124-0001 S7, F1-F18).

Every test uses small fixture repositories and fixture profiles. None invokes the
standard triple, so the suite never runs itself recursively.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from ai_lab.documentation import verification_v2 as v2
from ai_lab.documentation.self_model import (
    SelfModelError,
    SelfModelRegistry,
    validate_verification_record,
)

REPO = Path(__file__).resolve().parents[1]
WRITER = REPO / "scripts" / "verify_v2.py"
IMPORTER = REPO / "scripts" / "import_verification_v2.py"
CHECKER = REPO / "scripts" / "check_verification_outputs.py"
WORKFLOW = REPO / ".github" / "workflows" / "verify-v2.yml"
PROFILE_PATH = "profiles/P.json"
RECORDED_BY = {"peer_id": "test", "substrate": "pytest", "role": "test_importer"}


def _load_writer_module():
    spec = importlib.util.spec_from_file_location("verify_v2_writer_under_test", WRITER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_importer_module():
    spec = importlib.util.spec_from_file_location("import_v2_under_test", IMPORTER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


def cmd(code: str, timeout: float = 30, prop: str = "fixture property") -> dict:
    return {"argv": ["{python}", "-c", code], "timeout_seconds": timeout, "declared_property": prop}


def profile(*commands: dict, environment: dict | None = None) -> dict:
    return {
        "profile_schema": v2.PROFILE_SCHEMA,
        "profile_id": "VPROF-FIXTURE",
        "environment": environment if environment is not None else {"PYTHONDONTWRITEBYTECODE": "1"},
        "permitted_tree_changes": [],
        "commands": list(commands),
    }


OK = cmd("print('ok')")


def make_repo(tmp: Path, prof: dict | None, files: dict[str, str] | None = None, writer_bytes: bytes | None = None,
              parent_commit: bool = False) -> tuple[Path, str]:
    repo = tmp / "repo"
    repo.mkdir(parents=True)
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@example.invalid")
    _git(repo, "config", "user.name", "test")
    if parent_commit:
        (repo / "parent.txt").write_text("parent\n")
        _git(repo, "add", "-A")
        _git(repo, "commit", "-q", "-m", "parent")
    (repo / "scripts").mkdir(exist_ok=True)
    if writer_bytes is not False:
        (repo / "scripts" / "verify_v2.py").write_bytes(writer_bytes if writer_bytes is not None else WRITER.read_bytes())
    (repo / ".gitignore").write_text("ignored/\n")
    (repo / "tracked.txt").write_text("committed content\n")
    for name, content in (files or {}).items():
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    if prof is not None:
        (repo / "profiles").mkdir(exist_ok=True)
        (repo / PROFILE_PATH).write_text(json.dumps(prof, indent=1))
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "fixture")
    return repo, _git(repo, "rev-parse", "HEAD")


def run_writer(tmp: Path, repo: Path, commit: str, *extra: str, writer: Path | None = None, env: dict | None = None,
               profile_path: str = PROFILE_PATH, name: str = "r") -> tuple[subprocess.CompletedProcess, Path, Path]:
    store = tmp / "store"
    receipt = tmp / f"{name}.json"
    writer_path = writer or (repo / "scripts" / "verify_v2.py")
    run_env = dict(os.environ if env is None else env)
    result = subprocess.run(
        [sys.executable, str(writer_path), "--repo", str(repo), "--commit", commit, "--profile", profile_path,
         "--store-root", str(store), "--receipt-out", str(receipt), *extra],
        capture_output=True, text=True, env=run_env,
    )
    return result, receipt, store


def receipt_of(path: Path) -> dict:
    return json.loads(path.read_text())


def blob(store: Path, stream: dict) -> bytes:
    return (store / stream["store_path"]).read_bytes()


# ---------------------------------------------------------------- semantics agreement


def test_result_and_retention_copies_agree_exhaustively():
    writer = _load_writer_module()
    terminations = ["exited", "timeout", "signal", "failed_to_start"]
    exit_codes = [0, 1, None, True]
    boundary = [
        {"head_matches_subject": True, "status_clean": True},
        {"head_matches_subject": False, "status_clean": True},
        {"head_matches_subject": True, "status_clean": False},
    ]
    def command(t, e, b, complete):
        return {"termination": t, "exit_code": e, "boundary_after": b,
                "stdout": {"capture_complete": complete}, "stderr": {"capture_complete": True}}
    singles = [command(t, e, b, c) for t, e, b, c in itertools.product(terminations, exit_codes, boundary, [True, False])]
    cases = 0
    for count in (0, 1, 2):
        for initial in boundary:
            for n in (0, 1, 2):
                for combo in itertools.product(singles[:24], repeat=n):
                    commands = [dict(c) for c in combo]
                    assert writer.compute_result(count, commands, initial) == v2.compute_result(count, commands, initial)
                    assert writer.compute_output_retention(commands) == v2.compute_output_retention(commands)
                    cases += 1
    assert cases > 1000
    assert writer.store_relative_path("ab" * 32) == v2.store_relative_path("ab" * 32)
    assert writer.RETENTION_LIMIT_BYTES == v2.RETENTION_LIMIT_BYTES
    assert writer.LINEAGE == v2.LINEAGE
    assert set(writer.BASE_ENVIRONMENT_NAMES) == set(v2.BASE_ENVIRONMENT_NAMES)


# ---------------------------------------------------------------- F1


def test_f1_no_writer_argument_accepts_a_result():
    parser = _load_writer_module().build_parser()
    options = [s for action in parser._actions for s in action.option_strings]
    for forbidden in ("exit", "result", "output", "summary", "status", "stdout", "stderr", "pass"):
        assert not any(forbidden in option for option in options), (forbidden, options)
    for attempt in (["--exit-code", "0"], ["--result", "all_commands_exit_zero"], ["--summary", "ok"]):
        with pytest.raises(SystemExit):
            parser.parse_args(["--commit", "a" * 40, "--profile", "p", "--store-root", "s", "--receipt-out", "r", *attempt])


# ---------------------------------------------------------------- F2


def test_f2_failing_command_yields_failed_result_and_nonzero_exit(tmp_path):
    repo, commit = make_repo(tmp_path, profile(OK, cmd("import sys; sys.exit(7)"), OK))
    proc, receipt_path, _ = run_writer(tmp_path, repo, commit)
    receipt = receipt_of(receipt_path)
    assert proc.returncode == 1
    assert receipt["result"] == "one_or_more_commands_failed"
    assert [c["termination"] for c in receipt["commands"]] == ["exited"] * 3
    assert [c["exit_code"] for c in receipt["commands"]] == [0, 7, 0]


def test_f2_control_all_ok_is_success(tmp_path):
    repo, commit = make_repo(tmp_path, profile(OK, OK))
    proc, receipt_path, _ = run_writer(tmp_path, repo, commit)
    assert proc.returncode == 0, proc.stderr
    assert receipt_of(receipt_path)["result"] == "all_commands_exit_zero"


# ---------------------------------------------------------------- F3


def test_f3_abbreviated_and_unresolvable_commits_are_refused(tmp_path):
    repo, commit = make_repo(tmp_path, profile(OK))
    for bad in (commit[:12], "0" * 40, commit.upper()):
        proc, receipt_path, _ = run_writer(tmp_path, repo, bad, name=f"r-{bad[:6]}")
        assert proc.returncode == 2, (bad, proc.stderr)
        assert not receipt_path.exists()


def test_f3_uncommitted_changes_in_invoking_clone_do_not_reach_the_worktree(tmp_path):
    repo, commit = make_repo(tmp_path, profile(cmd("print(open('tracked.txt').read(), end='')")))
    (repo / "tracked.txt").write_text("UNCOMMITTED\n")
    proc, receipt_path, store = run_writer(tmp_path, repo, commit)
    assert proc.returncode == 0, proc.stderr
    assert blob(store, receipt_of(receipt_path)["commands"][0]["stdout"]) == b"committed content\n"


# ---------------------------------------------------------------- F4


def test_f4_checker_detects_altered_blob_and_altered_digest(tmp_path):
    repo_root = _repo_with_imported_record(tmp_path)
    assert subprocess.run([sys.executable, str(CHECKER), "--repo-root", str(repo_root)]).returncode == 0
    record_path = next((repo_root / "docs/self_model/verifications").glob("VERIFY-*.json"))
    record = json.loads(record_path.read_text())
    receipt = json.loads((repo_root / v2.STORE_RELATIVE_ROOT / record["receipt"]["store_path"]).read_text())
    target = repo_root / v2.STORE_RELATIVE_ROOT / receipt["commands"][0]["stdout"]["store_path"]
    original = target.read_bytes()
    target.write_bytes(original + b"tampered")
    assert subprocess.run([sys.executable, str(CHECKER), "--repo-root", str(repo_root)]).returncode == 1
    target.write_bytes(original)
    stray = repo_root / v2.STORE_RELATIVE_ROOT / "sha256" / "00" / ("0" * 64)
    stray.parent.mkdir(parents=True, exist_ok=True)
    stray.write_bytes(b"unreferenced bytes that do not hash to their address")
    assert subprocess.run([sys.executable, str(CHECKER), "--repo-root", str(repo_root)]).returncode == 1
    stray.unlink()
    assert subprocess.run([sys.executable, str(CHECKER), "--repo-root", str(repo_root)]).returncode == 0
    record["receipt"]["sha256"] = "f" * 64
    record["receipt"]["store_path"] = v2.store_relative_path("f" * 64)
    record_path.write_text(json.dumps(record))
    assert subprocess.run([sys.executable, str(CHECKER), "--repo-root", str(repo_root)]).returncode == 1


# ---------------------------------------------------------------- F5


def test_f5_profile_is_read_from_subject_tree(tmp_path):
    repo, commit = make_repo(tmp_path, profile(OK))
    (repo / PROFILE_PATH).write_text(json.dumps(profile(cmd("import sys; sys.exit(9)"))))
    proc, receipt_path, _ = run_writer(tmp_path, repo, commit)
    assert proc.returncode == 0, proc.stderr
    assert receipt_of(receipt_path)["commands"][0]["exit_code"] == 0


@pytest.mark.parametrize("profile_arg", ["/etc/passwd", "../outside.json", "profiles/absent.json"])
def test_f5_absolute_escaping_or_absent_profile_is_refused(tmp_path, profile_arg):
    repo, commit = make_repo(tmp_path, profile(OK))
    proc, receipt_path, _ = run_writer(tmp_path, repo, commit, profile_path=profile_arg)
    assert proc.returncode == 2, proc.stderr
    assert not receipt_path.exists()


def test_f5_dotdot_path_to_an_existing_profile_is_refused(tmp_path):
    repo, commit = make_repo(tmp_path, profile(OK))
    proc, receipt_path, _ = run_writer(tmp_path, repo, commit, profile_path="profiles/../profiles/P.json")
    assert proc.returncode == 2 and "escape" in proc.stderr
    assert not receipt_path.exists()


def test_f5_symlink_resolving_outside_the_subject_tree_is_refused(tmp_path):
    outside = tmp_path / "outside.json"
    outside.write_text(json.dumps(profile(OK)))
    repo, _ = make_repo(tmp_path, profile(OK))
    (repo / "profiles" / "link.json").symlink_to(outside)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "symlink")
    commit = _git(repo, "rev-parse", "HEAD")
    proc, receipt_path, _ = run_writer(tmp_path, repo, commit, profile_path="profiles/link.json")
    assert proc.returncode == 2 and "outside" in proc.stderr
    assert not receipt_path.exists()


def test_f5_empty_profile_is_refused(tmp_path):
    repo, commit = make_repo(tmp_path, profile())
    proc, receipt_path, _ = run_writer(tmp_path, repo, commit)
    assert proc.returncode == 2
    assert not receipt_path.exists()


# ---------------------------------------------------------------- F6


@pytest.mark.parametrize("command", [OK, cmd("import sys; sys.exit(1)"), cmd("import time; time.sleep(5)", timeout=0.5)])
def test_f6_worktree_and_temporary_directories_are_removed(tmp_path, command):
    repo, commit = make_repo(tmp_path, profile(command))
    tmpdir = tmp_path / "tmpdir"
    tmpdir.mkdir()
    env = dict(os.environ, TMPDIR=str(tmpdir))
    run_writer(tmp_path, repo, commit, env=env)
    worktrees = [line for line in _git(repo, "worktree", "list", "--porcelain").splitlines() if line.startswith("worktree ")]
    assert len(worktrees) == 1
    assert list(tmpdir.iterdir()) == []


# ---------------------------------------------------------------- F7


def test_f7_every_v1_record_still_validates():
    records = sorted((REPO / "docs/self_model/verifications").glob("VERIFY-*.json"))
    v1 = [json.loads(p.read_text()) for p in records]
    v1 = [r for r in v1 if r.get("schema_version") == "v1"]
    assert len(v1) >= 39
    for record in v1:
        validate_verification_record(record)


@pytest.mark.parametrize("block", ["repo_commit", "observed_at", "receipt", "summary", "origin", "import",
                                   "verifier_lineage_status", "recorded_by", "verification_id", "created_at"])
def test_f7_v2_record_lacking_a_required_block_is_refused(tmp_path, block):
    record = _valid_canonical_record(tmp_path)
    validate_verification_record(record)
    del record[block]
    with pytest.raises(SelfModelError):
        validate_verification_record(record)


# ---------------------------------------------------------------- F8


def test_f8_lineage_is_never_stronger_than_self_authored_unreviewed(tmp_path):
    source = WRITER.read_text()
    assert source.count('LINEAGE = "self_authored_unreviewed"') == 1
    assert "independent" not in source.split("LINEAGE =")[1].split("\n")[0]
    repo, commit = make_repo(tmp_path, profile(OK))
    _, receipt_path, _ = run_writer(tmp_path, repo, commit)
    assert receipt_of(receipt_path)["verifier_lineage_status"] == "self_authored_unreviewed"
    record = _valid_canonical_record(tmp_path / "second")
    for stronger in ("independent", "self_authored_with_review"):
        record["verifier_lineage_status"] = stronger
        with pytest.raises(SelfModelError):
            validate_verification_record(record)


# ---------------------------------------------------------------- F9


def test_f9_importer_refusals(tmp_path):
    importer = _load_importer_module()
    repo_root = _target_repo(tmp_path / "target")
    source = tmp_path / "source"
    source.mkdir()
    repo, commit = make_repo(source, profile(OK))
    _, receipt_path, store = run_writer(source, repo, commit)
    receipt = receipt_of(receipt_path)

    stream = store / receipt["commands"][0]["stdout"]["store_path"]
    original = stream.read_bytes()
    stream.write_bytes(b"altered")
    with pytest.raises(importer.ImportRefusal):
        importer.import_receipt(repo_root, receipt_path, store, RECORDED_BY)
    stream.write_bytes(original)

    collision = repo_root / "docs/self_model/verifications/VERIFY-20990101-0001.json"
    collision.write_text("{}")
    with pytest.raises((importer.ImportRefusal, SelfModelError)):
        importer.import_receipt(repo_root, receipt_path, store, RECORDED_BY, verification_id="VERIFY-20990101-0001")
    collision.unlink()

    importer.import_receipt(repo_root, receipt_path, store, RECORDED_BY)
    with pytest.raises(importer.ImportRefusal, match="already imported"):
        importer.import_receipt(repo_root, receipt_path, store, RECORDED_BY)


# ---------------------------------------------------------------- F10


AUDIT_FIXTURE = (
    "import sys\n"
    "records = open('records.txt').read().split()\n"
    "index = open('index.txt').read().strip()\n"
    "sys.exit(0 if index == str(len(records)) else 1)\n"
)
BUILD_FIXTURE = (
    "import sys\n"
    "out = sys.argv[sys.argv.index('--output') + 1] if '--output' in sys.argv else 'index.txt'\n"
    "open(out, 'w').write(str(len(open('records.txt').read().split())) + '\\n')\n"
)


def _triple_files(index: str) -> dict:
    return {"records.txt": "a\nb\nc\n", "index.txt": index, "audit.py": AUDIT_FIXTURE, "build.py": BUILD_FIXTURE}


def _file_cmd(*argv: str) -> dict:
    return {"argv": ["{python}", *argv], "timeout_seconds": 30, "declared_property": "fixture triple step"}


def test_f10_stale_committed_index_fails_even_though_build_succeeds(tmp_path):
    triple = profile(_file_cmd("audit.py"), _file_cmd("build.py", "--output", "{scratch}/index.txt"), OK)
    repo, commit = make_repo(tmp_path, triple, files=_triple_files("999\n"))
    proc, receipt_path, _ = run_writer(tmp_path, repo, commit)
    receipt = receipt_of(receipt_path)
    assert [c["exit_code"] for c in receipt["commands"]] == [1, 0, 0]
    assert receipt["result"] == "one_or_more_commands_failed"
    assert proc.returncode == 1


def test_f10_old_build_then_audit_order_is_caught_as_tree_change(tmp_path):
    old_order = profile(_file_cmd("build.py"), _file_cmd("audit.py"))
    repo, commit = make_repo(tmp_path, old_order, files=_triple_files("999\n"))
    _, receipt_path, _ = run_writer(tmp_path, repo, commit)
    receipt = receipt_of(receipt_path)
    assert [c["exit_code"] for c in receipt["commands"]] == [0, 0]
    assert receipt["result"] == "incomplete"


def test_f10_control_fresh_index_passes(tmp_path):
    triple = profile(_file_cmd("audit.py"), _file_cmd("build.py", "--output", "{scratch}/index.txt"), OK)
    repo, commit = make_repo(tmp_path, triple, files=_triple_files("3\n"))
    proc, receipt_path, _ = run_writer(tmp_path, repo, commit)
    assert proc.returncode == 0, proc.stderr
    assert receipt_of(receipt_path)["result"] == "all_commands_exit_zero"


# ---------------------------------------------------------------- F11


def test_f11_foreign_writer_is_refused_by_default_and_recorded_when_allowed(tmp_path):
    repo, commit = make_repo(tmp_path, profile(OK))
    foreign = tmp_path / "foreign_verify_v2.py"
    foreign.write_bytes(WRITER.read_bytes() + b"\n# modified writer\n")
    proc, receipt_path, _ = run_writer(tmp_path, repo, commit, writer=foreign)
    assert proc.returncode == 2
    assert not receipt_path.exists()
    proc, receipt_path, _ = run_writer(tmp_path, repo, commit, "--foreign-verifier", writer=foreign, name="r2")
    verifier = receipt_of(receipt_path)["verifier"]
    assert verifier["verifier_matches_subject"] is False
    assert verifier["running_sha256"] == hashlib.sha256(foreign.read_bytes()).hexdigest()


def test_f11_writer_absent_at_subject(tmp_path):
    repo, commit = make_repo(tmp_path, profile(OK), writer_bytes=False)
    proc, _, _ = run_writer(tmp_path, repo, commit, writer=WRITER)
    assert proc.returncode == 2
    proc, receipt_path, _ = run_writer(tmp_path, repo, commit, "--foreign-verifier", writer=WRITER, name="r2")
    assert receipt_of(receipt_path)["verifier"]["verifier_matches_subject"] == "absent_at_subject"


# ---------------------------------------------------------------- F12


@pytest.mark.parametrize(
    "command,termination",
    [
        (cmd("import time; time.sleep(10)", timeout=0.5), "timeout"),
        (cmd("import os, signal; os.kill(os.getpid(), signal.SIGKILL)"), "signal"),
        ({"argv": ["/nonexistent/program"], "timeout_seconds": 5, "declared_property": "p"}, "failed_to_start"),
    ],
)
def test_f12_unfinished_commands_yield_incomplete_never_success(tmp_path, command, termination):
    repo, commit = make_repo(tmp_path, profile(OK, command))
    proc, receipt_path, _ = run_writer(tmp_path, repo, commit)
    receipt = receipt_of(receipt_path)
    assert receipt["commands"][1]["termination"] == termination
    assert receipt["commands"][1]["exit_code"] is None
    assert receipt["result"] == "incomplete"
    assert proc.returncode == 3


# ---------------------------------------------------------------- F13


def test_f13_stream_over_retention_limit_is_partial(tmp_path):
    big = 9 * 1024 * 1024
    repo, commit = make_repo(tmp_path, profile(cmd(f"import sys; sys.stdout.buffer.write(b'x' * {big})")))
    proc, receipt_path, store = run_writer(tmp_path, repo, commit)
    receipt = receipt_of(receipt_path)
    stdout = receipt["commands"][0]["stdout"]
    assert stdout["observed_bytes"] == big
    assert stdout["retained_bytes"] == v2.RETENTION_LIMIT_BYTES
    assert stdout["capture_complete"] is False
    assert len(blob(store, stdout)) == v2.RETENTION_LIMIT_BYTES
    assert receipt["output_retention"] == "partial"
    assert receipt["result"] == "all_commands_exit_zero"


# ---------------------------------------------------------------- F14 (and WARR Condition 1)


CHANGES = {
    "tracked": "open('tracked.txt', 'a').write('changed')",
    "untracked": "open('new_untracked.txt', 'w').write('x')",
    "ignored": "import os; os.makedirs('ignored', exist_ok=True); open('ignored/f', 'w').write('x')",
}


@pytest.mark.parametrize("position", [0, 1, 2])
@pytest.mark.parametrize("kind", sorted(CHANGES))
def test_f14_any_tree_change_at_any_boundary_is_incomplete(tmp_path, position, kind):
    commands = [OK, OK, OK]
    commands[position] = cmd(CHANGES[kind])
    repo, commit = make_repo(tmp_path, profile(*commands))
    proc, receipt_path, _ = run_writer(tmp_path, repo, commit)
    receipt = receipt_of(receipt_path)
    assert all(c["exit_code"] == 0 for c in receipt["commands"])
    assert receipt["commands"][position]["boundary_after"]["status_clean"] is False
    assert receipt["result"] == "incomplete"
    assert proc.returncode == 3


@pytest.mark.parametrize("position", [0, 1, 2])
def test_f14_head_move_with_clean_status_is_incomplete(tmp_path, position):
    commands = [OK, OK, OK]
    commands[position] = cmd("import subprocess; subprocess.run(['git', 'checkout', '-q', '--detach', 'HEAD~1'], check=True)")
    repo, commit = make_repo(tmp_path, profile(*commands), parent_commit=True)
    proc, receipt_path, _ = run_writer(tmp_path, repo, commit)
    receipt = receipt_of(receipt_path)
    boundary = receipt["commands"][position]["boundary_after"]
    assert boundary["status_clean"] is True
    assert boundary["head_matches_subject"] is False
    assert receipt["result"] == "incomplete"
    assert proc.returncode == 3


# ---------------------------------------------------------------- F15


def test_f15_workflow_static_properties():
    workflow = yaml.safe_load(WORKFLOW.read_text())
    triggers = workflow.get("on", workflow.get(True))
    assert "pull_request" in triggers and triggers["push"]["branches"] == ["main"]
    assert workflow["permissions"] == {"contents": "read"}
    steps = workflow["jobs"]["verify-v2"]["steps"]
    checkout = next(s for s in steps if str(s.get("uses", "")).startswith("actions/checkout@"))
    assert checkout["with"]["fetch-depth"] == 0
    assert checkout["with"].get("persist-credentials") is False
    writer = next(s for s in steps if s.get("id") == "writer")
    assert "continue-on-error" not in writer
    upload = next(s for s in steps if str(s.get("uses", "")).startswith("actions/upload-artifact@"))
    assert upload.get("if") == "always()"
    for step in steps:
        if "uses" in step:
            assert len(step["uses"].split("@")[1]) == 40, step["uses"]
    assert "secrets." not in WORKFLOW.read_text()


# ---------------------------------------------------------------- F16 integration


def _copy_repository(destination: Path) -> Path:
    ignore = shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache", "*.pyc")
    shutil.copytree(REPO, destination, ignore=ignore)
    _git(destination, "init", "-q")
    _git(destination, "config", "user.email", "t@example.invalid")
    _git(destination, "config", "user.name", "test")
    _git(destination, "add", "-A")
    _git(destination, "commit", "-q", "-m", "copy")
    return destination


def _build(repo_root: Path, cwd: Path) -> None:
    subprocess.run([sys.executable, str(repo_root / "scripts/build_self_model.py"), "--repo-root", str(repo_root),
                    "--output", str(repo_root / "docs/self_model/SELF_MODEL.json")],
                   cwd=cwd, check=True, capture_output=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))


def _audit(repo_root: Path, cwd: Path) -> dict:
    proc = subprocess.run([sys.executable, str(repo_root / "scripts/audit_self_model_index.py"), "--repo-root",
                           str(repo_root)], cwd=cwd, capture_output=True, text=True,
                          env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    return json.loads(proc.stdout)


def test_f16_v1_and_v2_records_pass_registry_index_and_audit_together(tmp_path):
    repo_root = _copy_repository(tmp_path / "copy")
    existing_v2 = sum(
        json.loads(p.read_text()).get("schema_version") == "v2"
        for p in (repo_root / "docs/self_model/verifications").glob("VERIFY-*.json")
    )
    _build(repo_root, repo_root)
    _git(repo_root, "commit", "-q", "-am", "index")
    (repo_root / "profiles").mkdir()
    (repo_root / PROFILE_PATH).write_text(json.dumps(profile(OK)))
    _git(repo_root, "add", "-A")
    _git(repo_root, "commit", "-q", "-m", "fixture profile")
    commit = _git(repo_root, "rev-parse", "HEAD")
    importer = _load_importer_module()

    _, local_receipt, store = run_writer(tmp_path, repo_root, commit, name="local")
    event = tmp_path / "event.json"
    event.write_text(json.dumps({"pull_request": {"number": 1, "head": {"sha": "a" * 40}, "base": {"sha": "b" * 40}}}))
    ci_env = dict(os.environ, GITHUB_RUN_ID="1", GITHUB_RUN_ATTEMPT="1", GITHUB_EVENT_NAME="pull_request",
                  GITHUB_EVENT_PATH=str(event))
    _, ci_receipt, _ = run_writer(tmp_path, repo_root, commit, "--runner-kind", "github_actions", env=ci_env, name="ci")
    assert receipt_of(ci_receipt)["subject"]["pull_request"] == 1
    for receipt_path in (local_receipt, ci_receipt):
        try:
            importer.import_receipt(repo_root, receipt_path, store, RECORDED_BY)
        except (importer.ImportRefusal, SelfModelError) as error:
            pytest.fail(
                "a valid receipt must import using the explicit repository/store roots, "
                f"independently of the process working directory: {error}"
            )
    _build(repo_root, repo_root)
    _git(repo_root, "add", "-A")
    _git(repo_root, "commit", "-q", "-m", "records")

    registry = SelfModelRegistry(repo_root)
    entries = list(registry.entries("verification"))
    schemas = [json.loads((repo_root / e.source_path).read_text())["schema_version"] for e in entries]
    assert schemas.count("v1") >= 39 and schemas.count("v2") == existing_v2 + 2
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    for cwd in (repo_root, elsewhere):
        audit = _audit(repo_root, cwd)
        assert audit["ok"] is True and audit["verification_outcome"] == "verified_current", audit
        assert subprocess.run([sys.executable, str(repo_root / "scripts/check_verification_outputs.py"),
                               "--repo-root", str(repo_root)], cwd=cwd, capture_output=True).returncode == 0


# ---------------------------------------------------------------- F17


def _target_repo(root: Path) -> Path:
    (root / "docs/self_model/verifications").mkdir(parents=True)
    return root


def _base_receipt(tmp: Path) -> tuple[dict, Path]:
    repo, commit = make_repo(tmp, profile(OK, OK, OK))
    proc, receipt_path, store = run_writer(tmp, repo, commit)
    assert proc.returncode == 0, proc.stderr
    return receipt_of(receipt_path), store


def _canonical_for(receipt: dict, store: Path, repo_root: Path) -> dict:
    """Store receipt bytes under repo_root and return a record derived from them."""

    target_store = repo_root / v2.STORE_RELATIVE_ROOT
    for path in store.rglob("*"):
        if path.is_file():
            destination = target_store / path.relative_to(store)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, destination)
    data = (json.dumps(receipt, indent=1, sort_keys=True) + "\n").encode()
    digest = hashlib.sha256(data).hexdigest()
    destination = target_store / v2.store_relative_path(digest)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    return {
        "schema_version": "v2",
        "verification_id": "VERIFY-20990101-0001",
        "repo_commit": receipt["subject"]["candidate_commit"],
        "recorded_by": RECORDED_BY,
        "created_at": "2099-01-01T00:00:00+00:00",
        "observed_at": receipt["finished_at"],
        "receipt": {"sha256": digest, "store_path": v2.store_relative_path(digest)},
        "summary": v2.summary_from_receipt(receipt),
        "origin": {"claimed_runner": receipt["environment"]["runner"], "origin_verification": "unverified"},
        "import": {"importer_sha256": "0" * 64, "imported_at": "2099-01-01T00:00:00+00:00"},
        "verifier_lineage_status": "self_authored_unreviewed",
    }


def _valid_canonical_record(tmp: Path) -> dict:
    receipt, store = _base_receipt(tmp / "src")
    return _canonical_for(receipt, store, _target_repo(tmp / "target"))


def _repo_with_imported_record(tmp: Path) -> Path:
    receipt, store = _base_receipt(tmp / "src")
    repo_root = _target_repo(tmp / "target")
    record = _canonical_for(receipt, store, repo_root)
    (repo_root / "docs/self_model/verifications" / f"{record['verification_id']}.json").write_text(json.dumps(record))
    return repo_root


def _mutate_receipt(receipt: dict, case: str) -> dict:
    r = json.loads(json.dumps(receipt))
    if case == "exit_one_but_success":
        r["commands"][1]["exit_code"] = 1
    elif case == "retention_mismatch":
        r["output_retention"] = "partial"
    elif case == "truncated_to_first_command":
        r["commands"] = r["commands"][:1]
    elif case == "argv_template_differs":
        r["commands"][0]["argv_template"] = ["{python}", "-c", "print('other')"]
    elif case == "capture_complete_inconsistent":
        r["commands"][0]["stdout"]["capture_complete"] = False
        r["output_retention"] = "partial"
    elif case == "retained_length_differs":
        r["commands"][0]["stdout"]["retained_bytes"] += 1
        r["commands"][0]["stdout"]["observed_bytes"] += 1
    elif case == "extra_environment_variable":
        r["environment"]["command_environment"]["ANTHROPIC_API_KEY"] = "x"
    elif case == "profile_variable_value_differs":
        r["environment"]["command_environment"]["PYTHONDONTWRITEBYTECODE"] = "0"
    elif case == "head_flag_inconsistent":
        r["commands"][2]["boundary_after"]["head"] = "0" * 40
    elif case == "lineage_in_receipt":
        r["verifier_lineage_status"] = "independent"
    else:
        raise AssertionError(case)
    return r


RECEIPT_CASES = [
    "exit_one_but_success", "retention_mismatch", "truncated_to_first_command", "argv_template_differs",
    "capture_complete_inconsistent", "retained_length_differs", "extra_environment_variable",
    "profile_variable_value_differs", "head_flag_inconsistent", "lineage_in_receipt",
]


def test_f17_valid_record_passes(tmp_path):
    receipt, store = _base_receipt(tmp_path / "src")
    repo_root = _target_repo(tmp_path / "target")
    v2.validate_against_store(_canonical_for(receipt, store, repo_root), repo_root)


@pytest.mark.parametrize("case", RECEIPT_CASES)
def test_f17_receipt_invariant_violations_are_refused_even_with_matching_summary(tmp_path, case):
    receipt, store = _base_receipt(tmp_path / "src")
    repo_root = _target_repo(tmp_path / "target")
    mutated = _mutate_receipt(receipt, case)
    record = _canonical_for(mutated, store, repo_root)  # summary derived from the mutated receipt: it matches
    assert record["summary"] == v2.summary_from_receipt(mutated)
    with pytest.raises(v2.VerificationV2Error):
        v2.validate_against_store(record, repo_root)


RECORD_CASES = {
    "summary_differs": lambda r: r["summary"].update(result="incomplete"),
    "repo_commit_differs": lambda r: r.update(repo_commit="0" * 40),
    "observed_at_differs": lambda r: r.update(observed_at="2000-01-01T00:00:00+00:00"),
    "origin_verified": lambda r: r["origin"].update(origin_verification="verified"),
    "claimed_runner_differs": lambda r: r["origin"].update(claimed_runner={"kind": "github_actions"}),
    "lineage_stronger": lambda r: r.update(verifier_lineage_status="independent"),
    "store_path_not_derived": lambda r: r["receipt"].update(store_path="sha256/../../../etc/passwd"),
    "receipt_sha_mismatch": lambda r: r["receipt"].update(sha256="e" * 64, store_path=v2.store_relative_path("e" * 64)),
}


@pytest.mark.parametrize("case", sorted(RECORD_CASES))
def test_f17_record_invariant_violations_are_refused(tmp_path, case):
    receipt, store = _base_receipt(tmp_path / "src")
    repo_root = _target_repo(tmp_path / "target")
    record = _canonical_for(receipt, store, repo_root)
    RECORD_CASES[case](record)
    with pytest.raises(v2.VerificationV2Error):
        v2.validate_against_store(record, repo_root)


def test_f17_non_derived_store_path_inside_store_with_correct_bytes_is_refused(tmp_path):
    receipt, store = _base_receipt(tmp_path / "src")
    repo_root = _target_repo(tmp_path / "target")
    record = _canonical_for(receipt, store, repo_root)
    target_store = repo_root / v2.STORE_RELATIVE_ROOT
    copy = target_store / "sha256" / "zz" / "copy-of-receipt"
    copy.parent.mkdir(parents=True, exist_ok=True)
    copy.write_bytes((target_store / record["receipt"]["store_path"]).read_bytes())
    record["receipt"]["store_path"] = "sha256/zz/copy-of-receipt"
    with pytest.raises(v2.VerificationV2Error, match="derived"):
        v2.validate_against_store(record, repo_root)


def test_f17_store_path_escaping_store_root_is_refused(tmp_path):
    receipt, store = _base_receipt(tmp_path / "src")
    repo_root = _target_repo(tmp_path / "target")
    outside = tmp_path / "outside"
    outside.write_bytes(b"x")
    digest = hashlib.sha256(b"x").hexdigest()
    with pytest.raises(v2.VerificationV2Error):
        v2._read_blob(repo_root / v2.STORE_RELATIVE_ROOT, "../../../../outside", digest, "probe")


# ---------------------------------------------------------------- F18 (and WARR Condition 3)


def test_f18_environment_outside_allowlist_reaches_neither_command_nor_receipt(tmp_path):
    secret = "sk-fixture-secret-value-0123456789"
    repo, commit = make_repo(tmp_path, profile(cmd("import os, json; print(json.dumps(dict(os.environ)))")))
    env = dict(os.environ, FAKE_PROVIDER_API_KEY=secret, ANTHROPIC_API_KEY=secret, OPENAI_API_KEY=secret,
               HTTPS_PROXY="http://proxy.invalid:1", GITHUB_TOKEN=secret)
    proc, receipt_path, store = run_writer(tmp_path, repo, commit, env=env)
    assert proc.returncode == 0, proc.stderr
    receipt = receipt_of(receipt_path)
    child_env = json.loads(blob(store, receipt["commands"][0]["stdout"]))
    assert set(child_env) <= {"PATH", "HOME", "LANG", "TZ", "PYTHONDONTWRITEBYTECODE", "PWD", "SHLVL", "_", "LC_CTYPE"}
    assert secret.encode() not in receipt_path.read_bytes()
    for path in store.rglob("*"):
        if path.is_file():
            assert secret.encode() not in path.read_bytes()
    assert set(receipt["environment"]["command_environment"]) == {"PATH", "HOME", "LANG", "TZ", "PYTHONDONTWRITEBYTECODE"}


@pytest.mark.parametrize("environment", [{"MY_API_KEY": "x"}, {"PATH": "/x"}, {"VALUE": "$HOME"}, {"lower": "x"}])
def test_f18_profile_variables_must_be_explicit_non_secret_literals(tmp_path, environment):
    repo, commit = make_repo(tmp_path, profile(OK, environment=environment))
    proc, receipt_path, _ = run_writer(tmp_path, repo, commit)
    assert proc.returncode == 2
    assert not receipt_path.exists()
