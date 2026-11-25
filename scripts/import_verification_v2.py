#!/usr/bin/env python3
"""Import a VERIFY v2 receipt as a canonical VERIFY v2 record.

PLAN-20261124-0001 S6. This is the single path by which a receipt, local or CI,
becomes a canonical record.

The importer accepts a producer's receipt and says so. It validates the receipt
schema and invariants against the source store, re-checks every blob digest,
copies the receipt and its blobs into the repository store, derives the summary
from the receipt, assigns the next free VERIFY id for the import date and writes
the record exclusively. It does NOT establish that the claimed run took place: a
self-consistent receipt with a fabricated run id and matching digests passes
these checks, which is why every record carries origin_verification
"unverified". Observation time and producer are kept distinct from import time
and the importing executor.

Refusals: a receipt whose digests do not match, a receipt already imported, an
id that would overwrite a file, a receipt whose command environment holds a
variable outside the stored profile's allowlist.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ai_lab.documentation import verification_v2  # noqa: E402
from ai_lab.documentation.self_model import (  # noqa: E402
    SelfModelError,
    write_new_self_model_record,
)


class ImportRefusal(Exception):
    pass


def _put(store_root: Path, data: bytes) -> str:
    digest = hashlib.sha256(data).hexdigest()
    relative = verification_v2.store_relative_path(digest)
    path = store_root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise ImportRefusal(f"store collision with different bytes at {relative}")
    else:
        with path.open("xb") as handle:
            handle.write(data)
    return relative


def _referenced_blobs(receipt: dict) -> list[tuple[str, str]]:
    refs = [
        (receipt["inputs"]["profile"]["sha256"], receipt["inputs"]["profile"]["store_path"]),
        (receipt["environment"]["installed_distributions"]["sha256"],
         receipt["environment"]["installed_distributions"]["store_path"]),
    ]
    for command in receipt["commands"]:
        for stream in ("stdout", "stderr"):
            refs.append((command[stream]["sha256"], command[stream]["store_path"]))
    return refs


def _existing_receipt_shas(repo_root: Path) -> set[str]:
    shas = set()
    for path in (repo_root / "docs" / "self_model" / "verifications").glob("VERIFY-*.json"):
        record = json.loads(path.read_text(encoding="utf-8"))
        if record.get("schema_version") == "v2":
            shas.add(record["receipt"]["sha256"])
    return shas


def _next_id(repo_root: Path, date: str) -> str:
    directory = repo_root / "docs" / "self_model" / "verifications"
    used = {p.stem for p in directory.glob(f"VERIFY-{date}-*.json")}
    for number in range(1, 10000):
        candidate = f"VERIFY-{date}-{number:04d}"
        if candidate not in used:
            return candidate
    raise ImportRefusal(f"no free VERIFY id for {date}")


def import_receipt(
    repo_root: Path,
    receipt_path: Path,
    source_store: Path,
    recorded_by: dict,
    now: _dt.datetime | None = None,
    verification_id: str | None = None,
) -> Path:
    receipt_bytes = receipt_path.read_bytes()
    receipt_sha = hashlib.sha256(receipt_bytes).hexdigest()
    try:
        receipt = json.loads(receipt_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ImportRefusal(f"receipt is not valid JSON: {error}") from error
    try:
        verification_v2.validate_receipt(receipt, source_store)
    except verification_v2.VerificationV2Error as error:
        raise ImportRefusal(f"receipt refused: {error}") from error
    if receipt_sha in _existing_receipt_shas(repo_root):
        raise ImportRefusal(f"receipt already imported: {receipt_sha}")

    repo_store = repo_root / verification_v2.STORE_RELATIVE_ROOT
    for digest, relative in _referenced_blobs(receipt):
        data = (source_store / relative).read_bytes()
        if hashlib.sha256(data).hexdigest() != digest:
            raise ImportRefusal(f"blob digest mismatch at {relative}")
        _put(repo_store, data)
    receipt_relative = _put(repo_store, receipt_bytes)

    moment = now or _dt.datetime.now(_dt.timezone.utc)
    identifier = verification_id or _next_id(repo_root, moment.strftime("%Y%m%d"))
    importer_sha = hashlib.sha256(Path(__file__).resolve().read_bytes()).hexdigest()
    record = {
        "schema_version": "v2",
        "verification_id": identifier,
        "repo_commit": receipt["subject"]["candidate_commit"],
        "recorded_by": recorded_by,
        "created_at": moment.isoformat(timespec="seconds"),
        "observed_at": receipt["finished_at"],
        "receipt": {"sha256": receipt_sha, "store_path": receipt_relative},
        "summary": verification_v2.summary_from_receipt(receipt),
        "origin": {"claimed_runner": receipt["environment"]["runner"], "origin_verification": "unverified"},
        "import": {"importer_sha256": importer_sha, "imported_at": moment.isoformat(timespec="seconds")},
        "verifier_lineage_status": verification_v2.LINEAGE,
    }
    try:
        return write_new_self_model_record(repo_root, "verification", record)
    except SelfModelError as error:
        raise ImportRefusal(str(error)) from error


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Import a VERIFY v2 receipt as a canonical record.")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--source-store", type=Path, required=True, help="store holding the receipt's blobs")
    parser.add_argument("--peer-id", required=True, help="importing executor, declared")
    parser.add_argument("--substrate", required=True)
    parser.add_argument("--role", required=True)
    args = parser.parse_args(argv)
    try:
        path = import_receipt(
            repo_root=args.repo_root.resolve(),
            receipt_path=args.receipt.resolve(),
            source_store=args.source_store.resolve(),
            recorded_by={"peer_id": args.peer_id, "substrate": args.substrate, "role": args.role},
        )
    except ImportRefusal as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
