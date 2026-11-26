"""Targeted 3A falsification after review R15–R18.

The original twenty guards remain a separate historical manifest, imported
unchanged. The additional guards below address review 6070899882 under the
existing WARR-20261126-0001. This runner changes no classification rules:
passing baseline, identical selected node IDs and an ordinary failing call
assertion remain necessary. Exceptions, collection/setup errors and timeouts
are not catches. The source repository is copied, never mutated.

    python -I scripts/falsify_qualification_3a_review.py . \
        --report /tmp/qualification-3a-review.json

The complete report retains raw outputs and phase reports. Its score concerns
only these targeted guards, not all 48 planned families, 3B/3C or authority.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile


_previous_path = Path(__file__).resolve().with_name("falsify_qualification_3a.py")
_previous_spec = importlib.util.spec_from_file_location(
    "qualification_3a_original_falsification", _previous_path)
_previous = importlib.util.module_from_spec(_previous_spec)
_previous_spec.loader.exec_module(_previous)
_harness = _previous._harness

REPORT_SCHEMA = "qualification-3a-review-falsification-v1"
REVIEW_ID = 6070899882
REVIEWED_COMMIT = "877b94922fc9acf882930cd275d2889038cada33"
RECORDS = "ai_lab/providers/qualification_records.py"
ENGINE = "ai_lab/providers/qualification.py"


REVIEW_MUTATIONS = [
    ("R15 replacement objects can hide an adverse source", RECORDS,
     'subprocess.run(["git", "--no-replace-objects", "-C", str(repo_root), *args]',
     'subprocess.run(["git", "-C", str(repo_root), *args]',
     "test_r15_replacement_cannot_admit_pruned_inventory_claiming_original_commit",
     "tests/test_qualification_r15_r17.py"),
    ("R15 malformed Git batch trailing bytes accepted", RECORDS,
     '    if offset != len(data):', '    if False:',
     "test_r15_malformed_git_batch_is_typed_refusal and trailing_bytes",
     "tests/test_qualification_r15_r17.py"),
    ("R16 source need only predate event instead of witness assessment", ENGINE,
     '                    parse_timestamp(cap["captured_at"]), assessed, side.side,',
     '                    parse_timestamp(cap["captured_at"]), bound, side.side,',
     "test_r16_witness_cannot_precede_its_exact_source_availability or test_r16_early_same_mid_alternative_cannot_rescue_late_witnessed_chain",
     "tests/test_qualification_r16.py"),
    ("R17 CAS destination containment skipped", RECORDS,
     '    _check_publication_path(base, repository, target)', '    pass',
     "test_r17_both_publication_paths_refuse_symlink_redirection_before_writes and checkout and cas",
     "tests/test_qualification_r15_r17.py"),
    ("R17 display-index destination containment skipped", RECORDS,
     '    _check_publication_path(base, repository, index)', '    pass',
     "test_r17_both_publication_paths_refuse_symlink_redirection_before_writes and checkout and by_id",
     "tests/test_qualification_r15_r17.py"),
    ("R18 unavailable schema leaks an untyped file error", RECORDS,
     '    except OSError as exc:\n'
     '        raise QualificationBootstrapError(\n'
     '            "QUALIFICATION_SCHEMA_UNAVAILABLE", "frozen r2 schema bytes are unavailable"\n'
     '        ) from exc',
     '    except OSError:\n'
     '        raise',
     "test_r18_missing_or_changed_schema_has_declared_bootstrap_exception and missing",
     "tests/test_qualification_r18.py"),
    ("R18 changed schema digest accepted", RECORDS,
     '    if hashlib.sha256(data).hexdigest() != SCHEMA_SHA256:', '    if False:',
     "test_r18_missing_or_changed_schema_has_declared_bootstrap_exception and digest",
     "tests/test_qualification_r18.py"),
    ("R18 malformed schema leaks a schema-dependent error", RECORDS,
     '    except (QualificationError, SchemaError) as exc:\n'
     '        raise QualificationBootstrapError(\n'
     '            "QUALIFICATION_SCHEMA_INVALID", "pinned schema cannot be decoded or validated"\n'
     '        ) from exc',
     '    except (QualificationError, SchemaError):\n'
     '        raise',
     "test_r18_unparseable_or_invalid_schema_is_typed_bootstrap_failure",
     "tests/test_qualification_r18.py"),
]

HISTORICAL_MUTATIONS = tuple(_previous.MUTATIONS)
HISTORICAL_NAMES = frozenset(item[0] for item in HISTORICAL_MUTATIONS)
MUTATIONS = HISTORICAL_MUTATIONS + tuple(REVIEW_MUTATIONS)


def run_mutations(repo: Path, *, timeout: float = 120,
                  python: str = sys.executable) -> dict:
    if not REVIEW_MUTATIONS:
        raise _harness.HarnessError("review guard manifest is not populated")
    report = _harness.run_mutations(repo, MUTATIONS, timeout=timeout, python=python)
    report["classification_harness_schema"] = report["schema"]
    report["schema"] = REPORT_SCHEMA
    report["review_id"] = REVIEW_ID
    report["reviewed_commit"] = REVIEWED_COMMIT
    report["scope"] = "admitted 3A R15–R18 corrections and original guards; no 3B/3C or authority"
    report["falsifier_family_claim"] = "targeted guards, not all 48 proposed families"
    report["historical_manifest"] = {
        "path": "scripts/falsify_qualification_3a.py",
        "sha256": hashlib.sha256(_previous_path.read_bytes()).hexdigest(),
        "guards": len(HISTORICAL_MUTATIONS),
        "standing": "historical manifest preserved; its guards are re-executed on this report's source",
    }
    for result in report["results"]:
        result["group"] = "original_3a_20" if result["name"] in HISTORICAL_NAMES else "r15_r18_corrections"
    report["summary"]["groups"] = {
        group: {
            "mutations": sum(item["group"] == group for item in report["results"]),
            "caught": sum(item["group"] == group and item["status"] == "CAUGHT"
                          for item in report["results"]),
        }
        for group in ("original_3a_20", "r15_r18_corrections")
    }
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path, nargs="?", default=Path("."))
    parser.add_argument("--timeout", type=float, default=120, help="timeout per selected pytest process")
    parser.add_argument("--report", type=Path, help="complete retained evidence outside the source repository")
    args = parser.parse_args(argv)
    repo = args.repo.resolve()
    destination = args.report.resolve() if args.report is not None else None
    if destination is not None and destination.is_relative_to(repo):
        parser.error("--report must be outside the source repository")
    try:
        report = run_mutations(repo, timeout=args.timeout)
    except (_harness.HarnessError, OSError, ValueError) as exc:
        report = {"schema": REPORT_SCHEMA, "error": f"{type(exc).__name__}: {exc}"}
        code = 2
    else:
        for result in report["results"]:
            print(f"{result['name']} | {result['status']} | {result['reason']}", file=sys.stderr)
        print(json.dumps(report["summary"]), file=sys.stderr)
        code = 0 if report["summary"]["not_caught"] == 0 else 1
    content = json.dumps(report, indent=2, ensure_ascii=True) + "\n"
    if destination is None:
        print(content, end="")
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=destination.parent,
                                         prefix=destination.name + ".", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
        try:
            temporary.replace(destination)
        finally:
            temporary.unlink(missing_ok=True)
        print(f"Evidence: {destination}", file=sys.stderr)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
