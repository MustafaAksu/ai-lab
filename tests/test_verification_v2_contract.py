"""R9-R11: reject incomplete/contradictory receipts even with valid CAS digests.

The retained S9 receipts provide independent, immutable positive controls. The
negative cases change one contractual fact at a time; profile mutations are
stored under their correct new digest, so refusal cannot be credited to a stale
checksum. No test invokes the standard verification profile or a provider.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import shutil
from pathlib import Path

import pytest

from ai_lab.documentation import verification_v2 as v2


REPO = Path(__file__).resolve().parents[1]
STORE = REPO / v2.STORE_RELATIVE_ROOT
RECORDS = REPO / "docs/self_model/verifications"
HISTORICAL = {
    "VERIFY-20261124-0001": (
        "83e7a9ad89751634ac33cb4caf808774f7f3e8ecca458eee5802111557975cb9",
        "b6d6cbf68ced64bd6a80d866d12812334c674e63c0433e501f0a0b31a05a56f6",
        "all_commands_exit_zero",
    ),
    "VERIFY-20261124-0002": (
        "9c38b015606034d107912b8cdd1dc20dcb41fa3eaa73a4d48e352811db515436",
        "54c1e0930c410c7440d17ab210ddf018fa74700aa1b5d6f156f3790eab875532",
        "all_commands_exit_zero",
    ),
    "VERIFY-20261124-0003": (
        "7b7ecdbacc5c7742f9155a4d7d772a9f5dff65d3acce7d0104c8d927b17c5664",
        "7518e714679f75f5ee4a8f979e7a8ca693aec74bccf4468dbd6f2a6156fa246f",
        "one_or_more_commands_failed",
    ),
}


def _record(identifier: str = "VERIFY-20261124-0001") -> dict:
    return json.loads((RECORDS / f"{identifier}.json").read_text())


def _receipt(identifier: str = "VERIFY-20261124-0001") -> dict:
    return json.loads((STORE / _record(identifier)["receipt"]["store_path"]).read_text())


def _at(data: dict, path: tuple):
    for part in path:
        data = data[part]
    return data


def _set(data: dict, path: tuple, value: object) -> None:
    _at(data, path[:-1])[path[-1]] = value


def _required_paths(data: dict, prefix: tuple = ()) -> list[tuple]:
    """All keys of the frozen positive control, including nullable fields.

    Command schema is checked on the first command; later commands use exactly
    the same contract. Their execution order is exercised separately below.
    """
    paths = []
    for name, value in data.items():
        path = prefix + (name,)
        paths.append(path)
        if isinstance(value, dict):
            paths.extend(_required_paths(value, path))
        elif name == "commands" and value:
            paths.extend(_required_paths(value[0], path + (0,)))
    return paths


LOCAL_PATHS = _required_paths(_receipt())
CI_PATHS = [path for path in _required_paths(_receipt("VERIFY-20261124-0002")) if path not in LOCAL_PATHS]
CANONICAL_PATHS = _required_paths(_record())


def _path_name(path: tuple) -> str:
    return ".".join(str(part) for part in path)


@pytest.mark.parametrize("identifier", sorted(HISTORICAL))
def test_r9_historical_canonical_and_cas_bytes_stay_valid(identifier):
    canonical_digest, receipt_digest, result = HISTORICAL[identifier]
    payload = (RECORDS / f"{identifier}.json").read_bytes()
    assert hashlib.sha256(payload).hexdigest() == canonical_digest
    record = json.loads(payload)
    assert record["receipt"]["sha256"] == receipt_digest
    receipt = v2.validate_against_store(record, REPO)
    assert receipt["result"] == result
    assert receipt["receipt_schema"] == "ai-lab/verify-v2-receipt/1"


@pytest.mark.parametrize("path", LOCAL_PATHS, ids=_path_name)
def test_r9_receipt_requires_each_field(path):
    receipt = _receipt()
    del _at(receipt, path[:-1])[path[-1]]
    with pytest.raises(v2.VerificationV2Error):
        v2.validate_receipt(receipt, STORE)


@pytest.mark.parametrize("path", CI_PATHS, ids=_path_name)
def test_r9_ci_receipt_requires_runner_and_pr_fields(path):
    receipt = _receipt("VERIFY-20261124-0002")
    del _at(receipt, path[:-1])[path[-1]]
    with pytest.raises(v2.VerificationV2Error):
        v2.validate_receipt(receipt, STORE)


@pytest.mark.parametrize("path", CANONICAL_PATHS, ids=_path_name)
def test_r9_canonical_requires_each_field(path):
    record = _record()
    del _at(record, path[:-1])[path[-1]]
    with pytest.raises(v2.VerificationV2Error):
        v2.validate_canonical_structure(record)


INVALID_SCALARS = [
    (("subject", "candidate_commit"), "a" * 40 + "\n"),
    (("subject", "tree_id"), None),
    (("subject", "tree_id"), 1),
    (("history", "shallow"), 0),
    (("history", "stored_repo_head"), {}),
    (("history", "stored_repo_head_reachable"), 1),
    (("verifier", "tool"), None),
    (("verifier", "running_sha256"), "b" * 64 + "\n"),
    (("verifier", "subject_blob_sha"), None),
    (("verifier", "verifier_matches_subject"), 1),
    (("verifier", "verifier_matches_subject"), 0),
    (("verifier", "interpreter", "path"), "python"),
    (("verifier", "interpreter", "version"), False),
    (("inputs", "trees", "root"), "c" * 40),
    (("inputs", "trees", "tests"), []),
    (("inputs", "profile", "path"), "../profile.json"),
    (("inputs", "profile", "path"), "/tmp/profile.json"),
    (("inputs", "profile", "profile_id"), "different"),
    (("environment", "python", "implementation"), None),
    (("environment", "python", "version"), "different"),
    (("environment", "platform"), []),
    (("environment", "requirements_sha256"), 0),
    (("environment", "installed_distributions", "count"), True),
    (("environment", "installed_distributions", "count"), 1),
    (("environment", "command_environment", "PATH"), "relative/bin"),
    (("environment", "command_environment", "HOME"), "/tmp/run/elsewhere"),
    (("environment", "command_environment", "LANG"), "en_US.UTF-8"),
    (("environment", "command_environment", "TZ"), "Europe/Istanbul"),
    (("environment", "runner", "kind"), []),
    (("tree_observation", "method"), None),
    (("tree_observation", "scope"), "byte-level equality"),
    (("tree_observation", "initial", "head"), 0),
    (("tree_observation", "initial", "head_matches_subject"), 1),
    (("tree_observation", "initial", "status_clean"), 1),
    (("tree_observation", "initial", "changed_paths"), [False]),
    (("retention_limit_bytes",), True),
    (("commands", 0, "index"), False),
    (("commands", 0, "timeout_seconds"), True),
    (("commands", 0, "exit_code"), False),
    (("commands", 0, "stderr", "observed_bytes"), False),
    (("commands", 0, "stderr", "retained_bytes"), False),
    (("commands", 0, "stderr", "capture_complete"), 1),
    (("commands", 0, "boundary_after", "changed_paths"), [1]),
    (("commands", 0, "argv"), None),
    (("commands", 0, "argv_template"), [False]),
]


@pytest.mark.parametrize(("path", "value"), INVALID_SCALARS, ids=[_path_name(p) + ":" + repr(v) for p, v in INVALID_SCALARS])
def test_r9_receipt_rejects_invalid_scalar_types(path, value):
    receipt = _receipt()
    _set(receipt, path, value)
    with pytest.raises(v2.VerificationV2Error):
        v2.validate_receipt(receipt, STORE)


@pytest.mark.parametrize("value", [None, [], "receipt", 1, True])
def test_r9_nonobject_inputs_raise_contract_error(value):
    with pytest.raises(v2.VerificationV2Error):
        v2.validate_receipt(value, STORE)
    with pytest.raises(v2.VerificationV2Error):
        v2.validate_canonical_structure(value)


def test_r9_explicit_absence_is_valid_but_missing_fields_are_not():
    receipt = _receipt()
    receipt["history"].update(stored_repo_head=None, stored_repo_head_reachable=None)
    receipt["verifier"].update(verifier_matches_subject="absent_at_subject", subject_blob_sha=None)
    receipt["inputs"]["trees"].update(tests=None, scripts=None, ai_lab=None)
    receipt["environment"]["requirements_sha256"] = None
    v2.validate_receipt(receipt, STORE)
    for path in [("history", "stored_repo_head"), ("verifier", "subject_blob_sha"),
                 ("inputs", "trees", "tests"), ("environment", "requirements_sha256")]:
        incomplete = copy.deepcopy(receipt)
        del _at(incomplete, path[:-1])[path[-1]]
        with pytest.raises(v2.VerificationV2Error):
            v2.validate_receipt(incomplete, STORE)


def test_r9_absence_flags_must_agree():
    for mutation in [
        lambda r: r["history"].update(stored_repo_head=None),
        lambda r: r["history"].update(stored_repo_head_reachable=None),
        lambda r: r["verifier"].update(verifier_matches_subject="absent_at_subject"),
    ]:
        receipt = _receipt()
        mutation(receipt)
        with pytest.raises(v2.VerificationV2Error):
            v2.validate_receipt(receipt, STORE)


def test_r9_failed_head_observation_is_explicit_incomplete():
    receipt = _receipt()
    receipt["commands"][0]["boundary_after"].update(head=None, head_matches_subject=False)
    receipt["result"] = "incomplete"
    v2.validate_receipt(receipt, STORE)


def test_r9_unknown_ci_environment_values_are_explicit_null():
    receipt = _receipt("VERIFY-20261124-0002")
    runner = receipt["environment"]["runner"]
    for name in ("run_id", "run_attempt", "workflow_ref", "event_name", "runner_os", "image_os", "image_version", "workflow_file_sha256"):
        runner[name] = None
    v2.validate_receipt(receipt, STORE)


@pytest.mark.parametrize(("name", "value"), [
    ("run_id", 1), ("run_id", "0"), ("run_id", "01"), ("run_attempt", "-1"),
    ("run_attempt", True), ("image_version", []), ("workflow_ref", ""),
    ("workflow_file_sha256", False), ("reported_by", None),
])
def test_r9_ci_runner_types_are_checked(name, value):
    receipt = _receipt("VERIFY-20261124-0002")
    receipt["environment"]["runner"][name] = value
    with pytest.raises(v2.VerificationV2Error):
        v2.validate_receipt(receipt, STORE)


@pytest.mark.parametrize(("name", "value"), [("pull_request", True), ("pull_request", 0), ("head_sha", None), ("base_sha", "short")])
def test_r9_pr_subject_types_are_checked(name, value):
    receipt = _receipt("VERIFY-20261124-0002")
    receipt["subject"][name] = value
    with pytest.raises(v2.VerificationV2Error):
        v2.validate_receipt(receipt, STORE)


@pytest.mark.parametrize("path", [("started_at",), ("finished_at",), ("commands", 0, "started_at"), ("commands", 0, "finished_at")], ids=_path_name)
@pytest.mark.parametrize("value", [None, 1, "yesterday", "2026-11-24", "2026-11-24T15:16:24", "2026-02-30T12:00:00Z"])
def test_r9_timestamps_require_valid_timezone_aware_values(path, value):
    receipt = _receipt()
    _set(receipt, path, value)
    with pytest.raises(v2.VerificationV2Error):
        v2.validate_receipt(receipt, STORE)


@pytest.mark.parametrize("case", ["run_reversed", "command_reversed", "command_outside_run", "commands_overlap"])
def test_r9_timestamps_follow_run_and_command_order(case):
    receipt = _receipt()
    if case == "run_reversed":
        receipt["finished_at"] = "2000-01-01T00:00:00Z"
    elif case == "command_reversed":
        receipt["commands"][0]["finished_at"] = receipt["started_at"]
    elif case == "command_outside_run":
        receipt["commands"][2]["finished_at"] = "2099-01-01T00:00:00Z"
    else:
        receipt["commands"][1]["started_at"] = receipt["commands"][0]["started_at"]
    with pytest.raises(v2.VerificationV2Error):
        v2.validate_receipt(receipt, STORE)


@pytest.mark.parametrize("termination", ["timeout", "failed_to_start", "signal"])
def test_r9_nonexit_terminations_require_explicit_null_exit(termination):
    receipt = _receipt()
    command = receipt["commands"][0]
    command.update(termination=termination, exit_code=None)
    if termination == "signal":
        command["signal"] = 15
    receipt["result"] = "incomplete"
    v2.validate_receipt(receipt, STORE)
    del command["exit_code"]
    with pytest.raises(v2.VerificationV2Error):
        v2.validate_receipt(receipt, STORE)


@pytest.mark.parametrize("signal", [None, True, 0, -1, "15"])
def test_r9_signal_termination_requires_positive_integer_signal(signal):
    receipt = _receipt()
    receipt["commands"][0].update(termination="signal", exit_code=None, signal=signal)
    receipt["result"] = "incomplete"
    with pytest.raises(v2.VerificationV2Error):
        v2.validate_receipt(receipt, STORE)


@pytest.mark.parametrize("case", ["executable", "literal", "scratch", "interpreter_claim", "home_claim", "cwd"])
def test_r10_resolved_command_cannot_contradict_template(case):
    receipt = _receipt()
    if case == "executable":
        receipt["commands"][0]["argv"][0] = "/bin/echo"
    elif case == "literal":
        receipt["commands"][0]["argv"][1] = "different.py"
    elif case == "scratch":
        receipt["commands"][1]["argv"][-1] = "/tmp/another/scratch/SELF_MODEL.rebuilt.json"
    elif case == "interpreter_claim":
        receipt["verifier"]["interpreter"]["path"] = "/opt/other/python"
    elif case == "home_claim":
        receipt["environment"]["command_environment"]["HOME"] = "/tmp/another/home"
    else:
        receipt["commands"][0]["cwd"] = "/tmp/elsewhere"
    with pytest.raises(v2.VerificationV2Error):
        v2.validate_receipt(receipt, STORE)


def test_r10_resolution_uses_recorded_interpreter_and_home_sibling():
    receipt = _receipt()
    receipt["verifier"]["interpreter"]["path"] = "/opt/reported/python"
    receipt["environment"]["command_environment"]["HOME"] = "/tmp/reported-run/home"
    for command in receipt["commands"]:
        command["argv"] = ["/opt/reported/python" if t == "{python}" else t.replace("{scratch}", "/tmp/reported-run/scratch")
                           for t in command["argv_template"]]
    # Internal consistency only: the validator makes no claim these paths exist
    # now or that this synthetic report describes an actual execution.
    v2.validate_receipt(receipt, STORE)


def _profile() -> dict:
    return {
        "profile_schema": v2.PROFILE_SCHEMA,
        "profile_id": "VPROF-TEST",
        "environment": {"PYTHONDONTWRITEBYTECODE": "1"},
        "permitted_tree_changes": [],
        "commands": [{"argv": ["{python}", "-c", "print('ok')"], "timeout_seconds": 30,
                      "declared_property": "fixture command completes"}],
    }


PROFILE_INVALID = [
    (("profile_id",), ""), (("profile_id",), None), (("profile_id",), "id\0"),
    (("permitted_tree_changes",), ["README.md"]),
    (("environment",), {"MY_API_KEY": "literal"}),
    (("environment",), {"AUTH_MODE": "literal"}),
    (("environment",), {"PATH": "/bin"}),
    (("environment",), {"lowercase": "literal"}),
    (("environment",), {"SAFE": "$PARENT"}),
    (("environment",), {"SAFE": 1}),
    (("environment",), {"SAFE": "literal\0"}),
    (("commands",), []),
    (("commands", 0, "argv"), []),
    (("commands", 0, "argv"), [""]),
    (("commands", 0, "argv"), [1]),
    (("commands", 0, "argv"), ["echo\0"]),
    (("commands", 0, "timeout_seconds"), None),
    (("commands", 0, "timeout_seconds"), True),
    (("commands", 0, "timeout_seconds"), 0),
    (("commands", 0, "timeout_seconds"), -1),
    (("commands", 0, "timeout_seconds"), float("inf")),
    (("commands", 0, "timeout_seconds"), float("nan")),
    (("commands", 0, "timeout_seconds"), 86400),
    (("commands", 0, "timeout_seconds"), 10**1000),
    (("commands", 0, "declared_property"), ""),
    (("commands", 0, "declared_property"), "property\0"),
]


@pytest.fixture(scope="module")
def writer_module():
    spec = importlib.util.spec_from_file_location("verify_v2_profile_contract", REPO / "scripts/verify_v2.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(("path", "value"), PROFILE_INVALID, ids=[_path_name(p) + ":" + str(i) for i, (p, _) in enumerate(PROFILE_INVALID)])
def test_r11_stored_profile_and_writer_reject_same_invalid_values(writer_module, path, value):
    profile = _profile()
    _set(profile, path, value)
    with pytest.raises(writer_module.Refusal):
        writer_module._check_profile(profile)
    with pytest.raises(v2.VerificationV2Error):
        v2.load_profile(json.dumps(profile).encode())


@pytest.mark.parametrize("path", [p for p in _required_paths(_profile()) if not (p[0] == "environment" and len(p) > 1)], ids=_path_name)
def test_r11_stored_profile_requires_each_supported_field(writer_module, path):
    profile = _profile()
    del _at(profile, path[:-1])[path[-1]]
    with pytest.raises(writer_module.Refusal):
        writer_module._check_profile(profile)
    with pytest.raises(v2.VerificationV2Error):
        v2.load_profile(json.dumps(profile).encode())


@pytest.mark.parametrize("timeout", [0.001, 1, 86399.9])
def test_r11_supported_profiles_have_writer_validator_agreement(writer_module, timeout):
    profile = _profile()
    profile["commands"][0]["timeout_seconds"] = timeout
    profile["environment"]["EMPTY"] = ""
    writer_module._check_profile(profile)
    assert v2.load_profile(json.dumps(profile).encode()) == profile


def _store_profile(store: Path, receipt: dict, profile: dict) -> None:
    raw = (json.dumps(profile, sort_keys=True) + "\n").encode()
    digest = hashlib.sha256(raw).hexdigest()
    relative = v2.store_relative_path(digest)
    destination = store / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(raw)
    receipt["inputs"]["profile"].update(sha256=digest, store_path=relative)


@pytest.mark.parametrize("case", ["secret_environment", "negative_timeout", "empty_profile", "tree_change_permission"])
def test_r11_valid_cas_digest_does_not_admit_invalid_stored_profile(tmp_path, case):
    store = tmp_path / "store"
    shutil.copytree(STORE, store)
    receipt = _receipt()
    reference = receipt["inputs"]["profile"]
    profile = json.loads((store / reference["store_path"]).read_text())
    if case == "secret_environment":
        profile["environment"]["MY_API_KEY"] = "a-non-secret-test-literal"
        receipt["environment"]["command_environment"]["MY_API_KEY"] = "a-non-secret-test-literal"
    elif case == "negative_timeout":
        profile["commands"][0]["timeout_seconds"] = -1
        receipt["commands"][0]["timeout_seconds"] = -1
    elif case == "empty_profile":
        profile["commands"] = []
        receipt["commands"] = []
        receipt["result"] = "incomplete"
    else:
        profile["permitted_tree_changes"] = ["README.md"]
    _store_profile(store, receipt, profile)
    assert hashlib.sha256((store / reference["store_path"]).read_bytes()).hexdigest() == reference["sha256"]
    with pytest.raises(v2.VerificationV2Error):
        v2.validate_receipt(receipt, store)
