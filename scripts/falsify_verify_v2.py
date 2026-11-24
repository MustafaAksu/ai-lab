"""Falsification before reliance for tests/test_verify_v2.py (PLAN-20261124-0001).

Each mutation breaks one property in a working-copy file, runs the tests meant to
guard it and expects at least one failure; the file is restored after each case.
Run from a clean clone; it modifies and restores tracked files, so it is not part
of the test suite:
    python3 -I scripts/falsify_verify_v2.py .
"""

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(sys.argv[1])
W = "scripts/verify_v2.py"
V = "ai_lab/documentation/verification_v2.py"
I = "scripts/import_verification_v2.py"
C = "scripts/check_verification_outputs.py"
Y = ".github/workflows/verify-v2.yml"
T = "tests/test_verify_v2.py"

MUTATIONS = [
    ("F1 writer accepts an exit code", W,
     '    parser.add_argument("--runner-kind"', '    parser.add_argument("--exit-code")\n    parser.add_argument("--runner-kind"', "test_f1"),
    ("F2 failed mapped to success", W,
     '    if any(c["exit_code"] != 0 for c in commands):\n        return "one_or_more_commands_failed"\n    return "all_commands_exit_zero"\n\n\ndef compute_output_retention',
     '    return "all_commands_exit_zero"\n\n\ndef compute_output_retention', "test_f2 or test_f10_stale"),
    ("F3 abbreviated commit accepted", W,
     'FULL_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")', 'FULL_COMMIT_RE = re.compile(r"^[0-9a-f]{7,40}$")', "test_f3_abbreviated"),
    ("F3 invoking clone's working files leak into run", W,
     '        _git(repo, "worktree", "add", "--detach", str(worktree), commit)\n',
     '        _git(repo, "worktree", "add", "--detach", str(worktree), commit)\n        shutil.copyfile(repo / "tracked.txt", worktree / "tracked.txt") if (repo / "tracked.txt").exists() else None\n        _git(worktree, "update-index", "--assume-unchanged", "tracked.txt", check=False)\n',
     "test_f3_uncommitted"),
    ("F4 checker ignores blob address", C,
     '            if relative != verification_v2.store_relative_path(path.name) or path.name != digest:', '            if False:', "test_f4"),
    ("F5 profile read from invoking clone", W,
     "        profile_bytes, profile = _load_profile(worktree, profile_arg)", "        profile_bytes, profile = _load_profile(repo, profile_arg)", "test_f5_profile_is_read"),
    ("F5 escaping profile accepted", W,
     '    if ".." in posix.parts:\n        raise Refusal("profile path must not escape the subject tree")\n    path = (worktree / profile_arg).resolve()\n    if worktree.resolve() not in path.parents:\n        raise Refusal("profile path resolves outside the subject tree")',
     '    path = (worktree / profile_arg).resolve()', "test_f5_absolute or test_f5_dotdot or test_f5_symlink"),
    ("F6 worktree left behind", W,
     '        _git(repo, "worktree", "remove", "--force", str(worktree), check=False)\n        _git(repo, "worktree", "prune", check=False)\n        shutil.rmtree(temp, ignore_errors=True)', "        pass", "test_f6"),
    ("F7 v2 summary block not required", V,
     '    summary = _mapping(record.get("summary"), "$.summary")\n    if summary.get("result") not in RESULTS:\n        _fail("$.summary.result is not a defined result")\n    if summary.get("output_retention") not in ("complete", "partial"):\n        _fail("$.summary.output_retention must be complete or partial")\n    if not isinstance(summary.get("commands"), list) or not summary["commands"]:\n        _fail("$.summary.commands must be a non-empty list")',
     "    pass", "test_f7_v2"),
    ("F8 writer claims independent lineage", W,
     'LINEAGE = "self_authored_unreviewed"', 'LINEAGE = "independent"', "test_f8"),
    ("F9 re-import not refused", I,
     "    if receipt_sha in _existing_receipt_shas(repo_root):", "    if False:", "test_f9"),
    ("F10/F14 boundaries ignored by result", W,
     "    if not complete or disallowed_change:\n        return \"incomplete\"\n    if any(c[\"exit_code\"] != 0 for c in commands):\n        return \"one_or_more_commands_failed\"\n    return \"all_commands_exit_zero\"\n\n\ndef compute_output_retention(commands: list[dict]) -> str:\n    for command in commands:",
     "    if not complete:\n        return \"incomplete\"\n    if any(c[\"exit_code\"] != 0 for c in commands):\n        return \"one_or_more_commands_failed\"\n    return \"all_commands_exit_zero\"\n\n\ndef compute_output_retention(commands: list[dict]) -> str:\n    for command in commands:",
     "test_f10_old or test_f14"),
    ("F11 foreign writer not refused", W,
     "        if matches is not True and not foreign_verifier:", "        if False:", "test_f11"),
    ("F12 timeout recorded as exit 0", W,
     '        termination = "timeout"\n', '        exit_code = 0\n', "test_f12"),
    ("F13 no retention limit", W,
     "    retained = data[:RETENTION_LIMIT_BYTES]", "    retained = data", "test_f13"),
    ("F14 ignored paths not observed", W,
     '"--untracked-files=all", "--ignored", "-z", check=False', '"--untracked-files=all", "-z", check=False', "test_f14_any"),
    ("F14 untracked paths not observed", W,
     '"--untracked-files=all", "--ignored", "-z", check=False', '"--untracked-files=no", "-z", check=False', "test_f14_any"),
    ("F14/Cond1 HEAD not checked", W,
     '        "head_matches_subject": head_text == subject,', '        "head_matches_subject": True,', "test_f14_head"),
    ("F15 upload not on always()", Y,
     "        if: always()\n", "", "test_f15"),
    ("F15 credentials persisted", Y,
     "          persist-credentials: false\n", "", "test_f15"),
    ("F16 store resolved from cwd", V,
     "    store_root = Path(repo_root) / STORE_RELATIVE_ROOT", "    store_root = Path.cwd() / STORE_RELATIVE_ROOT", "test_f16"),
    ("F17 result not recomputed", V,
     "    if receipt.get(\"result\") != expected_result:", "    if False:", "test_f17_receipt"),
    ("F17/Cond2 completeness against profile count dropped", V,
     "    expected_result = compute_result(len(profile_commands), commands, observation[\"initial\"])",
     "    expected_result = compute_result(len(commands), commands, observation[\"initial\"])", "test_f17_receipt"),
    ("F17/Cond2 argv template not compared", V,
     "        if data.get(\"argv_template\") != spec.get(\"argv\"):", "        if False:", "test_f17_receipt"),
    ("F17/Cond2 capture_complete not checked", V,
     "    if data.get(\"capture_complete\") is not (retained == observed):", "    if False:", "test_f17_receipt"),
    ("F17 repo_commit invariant dropped", V,
     "    if record[\"repo_commit\"] != receipt[\"subject\"][\"candidate_commit\"]:", "    if False:", "test_f17_record"),
    ("F17 origin not required unverified", V,
     "    if origin.get(\"origin_verification\") != ORIGIN_VERIFICATION:", "    if False:", "test_f17_record"),
    ("F17 store path not derived", V,
     "    if value != store_relative_path(digest):", "    if False:", "test_f17_record or test_f17_non_derived"),
    ("F17 store root containment dropped", V,
     "    if store_root.resolve() not in path.parents:\n        _fail(f\"{where} resolves outside the store root\")", "    pass", "test_f17_store"),
    ("F18/Cond3 parent environment passed", W,
     "    environment.update(profile[\"environment\"])\n    return environment", "    environment.update(profile[\"environment\"])\n    environment.update(os.environ)\n    return environment", "test_f18_environment"),
    ("F18/Cond3 secret-like profile names allowed", W,
     "        if SECRET_NAME_RE.search(name):", "        if False:", "test_f18_profile"),
    ("F18/Cond3 env allowlist not checked by validator", V,
     "    if set(command_env) != allowed:", "    if False:", "test_f17_receipt"),
    ("agreement: validator copy diverges", V,
     "        and len(commands) == profile_command_count\n", "", "test_result_and_retention_copies_agree"),
]


def main() -> int:
    results = []
    for name, rel, old, new, selector in MUTATIONS:
        if selector is None:
            continue
        path = REPO / rel
        original = path.read_text()
        if original.count(old) != 1:
            results.append((name, "MUTATION NOT APPLICABLE", ""))
            continue
        path.write_text(original.replace(old, new))
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", T, "-k", selector],
                cwd=REPO, capture_output=True, text=True, timeout=900,
            )
            last = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else proc.stderr[-200:]
            results.append((name, "CAUGHT" if proc.returncode != 0 else "NOT CAUGHT", last))
        finally:
            path.write_text(original)
    for row in results:
        print(" | ".join(row))
    bad = [r for r in results if r[1] != "CAUGHT"]
    print(json.dumps({"mutations": len(results), "caught": len(results) - len(bad), "not_caught": len(bad)}))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
