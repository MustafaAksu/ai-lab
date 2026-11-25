#!/usr/bin/env python3
"""Reproduce R9-R11 using fixture receipts and the real canonical/store validator.

All generated data is temporary. Historical source bytes are read at a pinned
commit. This probe makes no claim that its synthetic receipts describe a run.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path

BASE = "68f6f103b1e3cae37c8fb15b7214d10d941aa5a3"
STORE = "docs/self_model/verification_outputs"


def git_bytes(repo, path):
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=repo)


def put(root, data):
    digest = hashlib.sha256(data).hexdigest()
    relative = f"sha256/{digest[:2]}/{digest}"
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return {"sha256": digest, "store_path": relative}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("validator", type=Path)
    parser.add_argument("--repo", required=True, type=Path)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("reviewed_validator", args.validator)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    historical = json.loads(git_bytes(args.repo, "docs/self_model/verifications/VERIFY-20261124-0001.json"))
    original = json.loads(git_bytes(args.repo, STORE + "/" + historical["receipt"]["store_path"]))
    receipt = copy.deepcopy(original)
    receipt["commands"] = receipt["commands"][:1]
    profile = {
        "profile_schema": "ai-lab/verify-v2-profile/1",
        "profile_id": "VPROF-REVIEW-FIXTURE",
        "environment": {"PYTHONDONTWRITEBYTECODE": "1"},
        "permitted_tree_changes": [],
        "commands": [{"argv": ["{python}", "-c", "print(1)"],
                      "timeout_seconds": 30, "declared_property": "synthetic review fixture"}],
    }
    command = receipt["commands"][0]
    command.update(argv_template=profile["commands"][0]["argv"],
                   argv=[receipt["verifier"]["interpreter"]["path"], "-c", "print(1)"],
                   timeout_seconds=30, declared_property="synthetic review fixture")
    receipt["inputs"]["profile"]["profile_id"] = profile["profile_id"]
    cases = ["valid_control", "R9_required_fields_absent", "R10_resolved_argv_and_cwd",
             "R11_secret_profile_variable", "R11_negative_timeout", "negative_control_wrong_result"]
    results = []
    for case in cases:
        r, p = copy.deepcopy(receipt), copy.deepcopy(profile)
        if case == "R9_required_fields_absent":
            del r["history"]
            del r["subject"]["tree_id"]
            del r["inputs"]["trees"]
            for key in ("subject_blob_sha", "interpreter"):
                del r["verifier"][key]
            for key in ("python", "platform"):
                del r["environment"][key]
            for key in ("argv", "cwd", "started_at", "finished_at"):
                del r["commands"][0][key]
        elif case == "R10_resolved_argv_and_cwd":
            r["commands"][0].update(argv=["/usr/bin/true"], cwd="/other")
        elif case == "R11_secret_profile_variable":
            p["environment"]["MY_API_KEY"] = "fixture-literal"
            r["environment"]["command_environment"]["MY_API_KEY"] = "fixture-literal"
        elif case == "R11_negative_timeout":
            p["commands"][0]["timeout_seconds"] = -1
            r["commands"][0]["timeout_seconds"] = -1
        elif case == "negative_control_wrong_result":
            r["result"] = "incomplete"
        with tempfile.TemporaryDirectory(prefix="verify-v2-review-probe-") as temp:
            root = Path(temp)
            store = root / STORE
            refs = [original["environment"]["installed_distributions"]]
            refs.extend(original["commands"][0][stream] for stream in ("stdout", "stderr"))
            for ref in refs:
                put(store, git_bytes(args.repo, STORE + "/" + ref["store_path"]))
            r["inputs"]["profile"].update(put(store, json.dumps(p, sort_keys=True).encode()))
            receipt_ref = put(store, (json.dumps(r, sort_keys=True) + "\n").encode())
            record = copy.deepcopy(historical)
            record.update(receipt=receipt_ref, summary=module.summary_from_receipt(r))
            try:
                module.validate_against_store(record, root)
                results.append({"case": case, "outcome": "ACCEPTED", "result": r["result"]})
            except module.VerificationV2Error as error:
                results.append({"case": case, "outcome": "REJECTED", "reason": str(error)})
    print(json.dumps({"fixture_source_commit": BASE,
                      "validator_sha256": hashlib.sha256(args.validator.read_bytes()).hexdigest(),
                      "results": results}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
