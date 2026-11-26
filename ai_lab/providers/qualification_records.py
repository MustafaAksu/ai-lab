"""Byte-bound inputs and closed record shapes for admitted Step 3A.

The synthetic factory is a trusted test-harness operation, outside Query. It
checks an actual immutable Git tree, then freezes all bytes before evaluation.
It establishes fixture integrity, never a live executor binding or authority.
There is intentionally no installed production-context factory or registry.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from functools import lru_cache
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import tempfile
from types import MappingProxyType
from typing import Any, Mapping

from jsonschema import Draft202012Validator, FormatChecker


SCHEMA_VERSION = "ai_lab.qualification.r2/1"
SCHEMA_SHA256 = "72126b1cb18d529d8ce3f59a573a05c58bc7250963cca37d0db48c25303c8327"
SCHEMA_PATH = Path(__file__).resolve().parents[2] / "docs/reviews/qualification_semantics/r2/ASSESSMENT-SCHEMA.json"
CATALOG_ROOTS = (
    "docs/catalog/eid/", "docs/catalog/mid/", "docs/catalog/snap/",
    "docs/catalog/cap/", "docs/catalog/payloads/",
)
_SHA1 = re.compile(r"[0-9a-f]{40}\Z")
_TIME = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?(?:Z|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])\Z")
_ID_FIELDS = ("record_id", "context_id", "inventory_id", "fixture_id", "query_id",
              "witness_id", "availability_id", "assessment_id", "invocation_id",
              "verification_id", "verify_id", "rule_id")
_ANCHOR_KEY = object()


class QualificationError(ValueError):
    """Typed refusal; its references name real bytes, not invented placeholders."""

    def __init__(self, code: str, detail: str, refs=(), stage: int = 1):
        self.code = code
        self.detail = str(detail).replace("\x00", "")[:1024]
        self.refs = tuple(dict(ref) for ref in refs)
        self.stage = stage
        super().__init__(f"{code}: {self.detail}")


def strict_loads(value: bytes | str) -> Any:
    def pairs(items):
        result = {}
        for key, item in items:
            if key in result:
                raise ValueError("duplicate JSON key")
            result[key] = item
        return result

    def constant(_):
        raise ValueError("nonfinite JSON number")

    def finite_float(text):
        item = float(text)
        if not math.isfinite(item):
            raise ValueError("nonfinite JSON number")
        return item

    try:
        if isinstance(value, bytes):
            value = value.decode("utf-8", errors="strict")
        if not isinstance(value, str):
            raise ValueError("expected UTF-8 JSON bytes or text")
        return json.loads(value, object_pairs_hook=pairs, parse_constant=constant,
                          parse_float=finite_float)
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise QualificationError("INVALID_SCHEMA", str(exc), stage=0) from exc


def _json_value(value):
    if value is None or type(value) in (bool, int, str):
        return
    if type(value) is float and math.isfinite(value):
        return
    if type(value) is list:
        for item in value:
            _json_value(item)
        return
    if type(value) is dict and all(type(key) is str for key in value):
        for item in value.values():
            _json_value(item)
        return
    raise ValueError("value is not finite JSON data")


def canonical_bytes(value: Any) -> bytes:
    """Total byte tie-break for valid finite JSON; never silently coerce types."""
    try:
        _json_value(value)
        return json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        raise QualificationError("INVALID_SCHEMA", str(exc), stage=0) from exc


def sha256(data: bytes) -> str:
    if not isinstance(data, bytes):
        raise QualificationError("INVALID_SCHEMA", "digest requires actual bytes")
    return "sha256:" + hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def parse_timestamp(value: str) -> datetime:
    # fromisoformat normalizes offset minutes such as +00:60. The lexical
    # boundary rejects these before parsing; an offset must not be coerced.
    if not isinstance(value, str) or not _TIME.fullmatch(value):
        raise QualificationError("INVALID_TIMESTAMP", "timestamp requires an explicit supported offset", stage=0)
    try:
        stamp = datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
        if stamp.tzinfo is None or stamp.utcoffset() is None:
            raise ValueError("timestamp has no offset")
        return stamp
    except ValueError as exc:
        raise QualificationError("INVALID_TIMESTAMP", "invalid calendar timestamp", stage=0) from exc


def _valid_timestamp(value):
    if not isinstance(value, str):
        return True
    try:
        parse_timestamp(value)
        return True
    except QualificationError:
        return False


@lru_cache(maxsize=1)
def _schema():
    data = SCHEMA_PATH.read_bytes()
    if hashlib.sha256(data).hexdigest() != SCHEMA_SHA256:
        raise QualificationError("ARTIFACT_DIGEST_MISMATCH", "frozen r2 schema bytes changed")
    schema = strict_loads(data)
    Draft202012Validator.check_schema(schema)
    return schema


def reason_codes() -> tuple[str, ...]:
    return tuple(_schema()["$defs"]["ReasonCode"]["enum"])


def validate_shape(value: Any, definition: str) -> None:
    canonical_bytes(value)  # reject non-JSON Python values before jsonschema
    schema = _schema()
    if definition not in schema["$defs"]:
        raise QualificationError("INVALID_SCHEMA", "unknown schema definition", stage=0)
    checker = FormatChecker()
    checker.checks("date-time")(_valid_timestamp)
    fragment = {"$schema": schema["$schema"], "$ref": "#/$defs/" + definition,
                "$defs": schema["$defs"]}
    errors = list(Draft202012Validator(fragment, format_checker=checker).iter_errors(value))
    if errors:
        details = [{"path": list(error.absolute_path), "schema_path": list(error.absolute_schema_path),
                    "validator": error.validator, "constraint": error.validator_value,
                    "instance_type": type(error.instance).__name__} for error in errors]
        details.sort(key=canonical_bytes)
        code = "INVALID_TIMESTAMP" if any(error.validator == "format" and error.validator_value == "date-time" for error in errors) else "INVALID_SCHEMA"
        raise QualificationError(code, canonical_bytes(details).decode("utf-8"), stage=0)


def _declared_id(data: bytes) -> str | None:
    try:
        value = strict_loads(data)
    except QualificationError:
        return None
    if not isinstance(value, dict):
        return None
    for key in _ID_FIELDS:
        item = value.get(key)
        if isinstance(item, str):
            return item
    return None


def record_ref(record_id: str, data: bytes) -> dict:
    if _declared_id(data) != record_id:
        raise QualificationError("SCHEMA_ID_MISMATCH", "record reference does not match retained bytes")
    ref = {"record_id": record_id, "sha256": sha256(data)}
    validate_shape(ref, "RecordRef")
    return ref


def artifact_ref(path: str, data: bytes, record_id: str | None = None,
                 git_blob_sha1: str | None = None) -> dict:
    ref = {"path": path, "record_id": record_id, "sha256": sha256(data),
           "git_blob_sha1": git_blob_sha1}
    validate_shape(ref, "ArtifactRef")
    if record_id is not None and _declared_id(data) != record_id:
        raise QualificationError("SCHEMA_ID_MISMATCH", "artifact ID does not match retained bytes")
    if git_blob_sha1 is not None and globals()["git_blob_sha1"](data) != git_blob_sha1:
        raise QualificationError("ARTIFACT_DIGEST_MISMATCH", "artifact Git blob hash mismatch")
    return ref


def assessment_reference(result: dict) -> dict:
    validate_shape(result, "AssessmentResult")
    return record_ref(result["assessment_id"], canonical_bytes(result))


@dataclass(frozen=True)
class GitCatalog:
    commit: str
    tree_sha1: str
    files: Mapping[str, bytes] = field(repr=False)
    blobs: Mapping[str, str] = field(repr=False)
    modes: Mapping[str, str] = field(repr=False)

    @property
    def catalog_entries(self):
        return [artifact_ref(path, data, _declared_id(data), self.blobs[path])
                for path, data in sorted(self.files.items()) if path.startswith(CATALOG_ROOTS)]


def load_git_catalog(repo_root: Path | str, commit: str) -> GitCatalog:
    """Read immutable object bytes eagerly; evaluators subsequently perform no I/O."""
    if not isinstance(commit, str) or not _SHA1.fullmatch(commit):
        raise QualificationError("INVENTORY_PIN_MISMATCH", "a full lowercase commit SHA is required", stage=2)
    repo_root = Path(repo_root)

    def git(*args, input=None):
        try:
            return subprocess.run(["git", "-C", str(repo_root), *args], input=input,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout
        except (OSError, subprocess.CalledProcessError) as exc:
            raise QualificationError("INVENTORY_PIN_MISMATCH", "pinned Git objects unavailable", stage=2) from exc

    if git("rev-parse", "--verify", commit + "^{commit}").decode().strip() != commit:
        raise QualificationError("INVENTORY_PIN_MISMATCH", "pin is not a commit", stage=2)
    tree = git("rev-parse", commit + "^{tree}").decode().strip()
    blobs, modes = {}, {}
    for row in git("ls-tree", "-rz", "--full-tree", commit).split(b"\x00"):
        if not row:
            continue
        header, path_raw = row.split(b"\t", 1)
        mode, kind, object_id = header.decode("ascii").split()
        try:
            path = path_raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise QualificationError("INVENTORY_PIN_MISMATCH", "non-UTF-8 pinned path", stage=2) from exc
        modes[path] = mode
        if mode not in ("100644", "100755") or kind != "blob":
            if path.startswith(CATALOG_ROOTS):
                raise QualificationError("INVENTORY_PIN_MISMATCH", "catalog tree contains a nonregular file", stage=2)
            continue
        blobs[path] = object_id
    ids = sorted(set(blobs.values()))
    data = git("cat-file", "--batch", input=("\n".join(ids) + ("\n" if ids else "")).encode("ascii"))
    offset, objects = 0, {}
    for expected in ids:
        end = data.index(b"\n", offset)
        object_id, kind, count = data[offset:end].decode("ascii").split()
        size = int(count)
        body = data[end + 1:end + 1 + size]
        if object_id != expected or kind != "blob" or len(body) != size or git_blob_sha1(body) != expected:
            raise QualificationError("ARTIFACT_DIGEST_MISMATCH", "pinned Git batch object mismatch")
        objects[expected] = body
        offset = end + 1 + size + 1
    files = {path: objects[blob] for path, blob in blobs.items()}
    return GitCatalog(commit, tree, MappingProxyType(files), MappingProxyType(blobs), MappingProxyType(modes))


@dataclass(frozen=True, init=False)
class EvidenceAnchor:
    """Frozen harness capability; a Query or a schema-valid dictionary is not one."""
    domain: str
    artifacts: Mapping[str, bytes] = field(repr=False)
    git: GitCatalog
    _context_ref: bytes = field(repr=False)
    _context: bytes = field(repr=False)
    _inventory: bytes = field(repr=False)
    _records: Mapping[str, tuple[str, ...]] = field(repr=False)

    def __init__(self, *, _key, git, artifacts, context_ref):
        if _key is not _ANCHOR_KEY:
            raise QualificationError("CONTEXT_ANCHOR_MISMATCH", "anchor must be loaded by the harness")
        object.__setattr__(self, "domain", "synthetic")
        object.__setattr__(self, "git", git)
        object.__setattr__(self, "artifacts", MappingProxyType(dict(artifacts)))
        records = {}
        for path, data in sorted(artifacts.items()):
            identity = _declared_id(data)
            if identity is not None:
                records.setdefault(identity, []).append(path)
        object.__setattr__(self, "_records", MappingProxyType({key: tuple(value) for key, value in records.items()}))
        for identity, paths in sorted(records.items()):
            if len({artifacts[path] for path in paths}) > 1:
                variants = sorted({sha256(artifacts[path]) for path in paths})
                raise QualificationError("CONFLICTING_ARTIFACT_BYTES", canonical_bytes({"record_id": identity, "digests": variants}).decode())
        context_ref = strict_loads(canonical_bytes(context_ref))
        object.__setattr__(self, "_context_ref", canonical_bytes(context_ref))
        context_artifact = self.resolve(context_ref)
        context_bytes = self.read(context_artifact)
        context = strict_loads(context_bytes)
        validate_shape(context, "EvidenceContext")
        if context["domain"] != "synthetic":
            raise QualificationError("DOMAIN_MISMATCH", "synthetic factory refuses production context", stage=8)
        object.__setattr__(self, "_context", context_bytes)
        inventory_ref = self.resolve(context["inventory_ref"])
        inventory_bytes = self.read(inventory_ref)
        inventory = strict_loads(inventory_bytes)
        validate_shape(inventory, "SourceInventory")
        if inventory["domain"] != "synthetic":
            raise QualificationError("DOMAIN_MISMATCH", "synthetic context requires synthetic inventory", stage=8)
        object.__setattr__(self, "_inventory", inventory_bytes)

    @property
    def context_ref(self):
        return strict_loads(self._context_ref)

    @property
    def context(self):
        return strict_loads(self._context)

    @property
    def inventory(self):
        return strict_loads(self._inventory)

    @property
    def catalog_entries(self):
        return self.git.catalog_entries

    def read(self, ref: dict) -> bytes:
        validate_shape(ref, "ArtifactRef")
        path = ref["path"]
        if path not in self.artifacts:
            raise QualificationError("KNOWN_SOURCE_UNAVAILABLE", f"missing artifact: {path}")
        data = self.artifacts[path]
        if sha256(data) != ref["sha256"]:
            raise QualificationError("ARTIFACT_DIGEST_MISMATCH", f"artifact digest mismatch: {path}")
        if ref["record_id"] is not None and _declared_id(data) != ref["record_id"]:
            raise QualificationError("SCHEMA_ID_MISMATCH", f"artifact record ID mismatch: {path}")
        if ref["git_blob_sha1"] is not None:
            if self.git.blobs.get(path) != ref["git_blob_sha1"] or git_blob_sha1(data) != ref["git_blob_sha1"]:
                raise QualificationError("INVENTORY_PIN_MISMATCH", f"artifact is not this pinned Git path: {path}", stage=2)
        return data

    read_artifact = read

    def resolve(self, ref: dict) -> dict:
        validate_shape(ref, "RecordRef")
        paths = self._records.get(ref["record_id"], ())
        matches = [path for path in paths if sha256(self.artifacts[path]) == ref["sha256"]]
        if not matches:
            code = "ARTIFACT_DIGEST_MISMATCH" if paths else "KNOWN_SOURCE_UNAVAILABLE"
            raise QualificationError(code, f"record unavailable at its pinned digest: {ref['record_id']}", refs=(ref,))
        path = min(matches)
        return artifact_ref(path, self.artifacts[path], ref["record_id"], self.git.blobs.get(path))

    def record(self, ref: dict, definition: str | None = None) -> dict:
        data = self.read(ref if "path" in ref else self.resolve(ref))
        value = strict_loads(data)
        if not isinstance(value, dict):
            raise QualificationError("INVALID_SCHEMA", "record must be a JSON object", stage=0)
        if definition is not None:
            validate_shape(value, definition)
        return value


def load_synthetic_anchor(repo_root: Path | str, *, context_ref: dict,
                          artifacts: Mapping[str, bytes]) -> EvidenceAnchor:
    """Load a complete real Git fixture tree and out-of-band harness artifacts.

    Factory inputs are trusted harness configuration. They are never fields
    accepted from Query. Missing references fail explicitly and are not filled.
    """
    validate_shape(context_ref, "RecordRef")
    supplied = {}
    for path, data in artifacts.items():
        if not isinstance(data, bytes):
            raise QualificationError("INVALID_SCHEMA", "artifact store values must be immutable bytes")
        artifact_ref(path, data)
        supplied[path] = data

    def preliminary(ref, definition):
        candidates = [(path, data) for path, data in sorted(supplied.items()) if _declared_id(data) == ref["record_id"]]
        if len({data for _, data in candidates}) > 1:
            detail = {"record_id": ref["record_id"], "digests": sorted({sha256(data) for _, data in candidates})}
            raise QualificationError("CONFLICTING_ARTIFACT_BYTES", canonical_bytes(detail).decode())
        matches = [data for _, data in candidates if sha256(data) == ref["sha256"]]
        if not matches:
            raise QualificationError("KNOWN_SOURCE_UNAVAILABLE", f"missing anchor record: {ref['record_id']}", refs=(ref,))
        value = strict_loads(matches[0])
        validate_shape(value, definition)
        return value

    context = preliminary(context_ref, "EvidenceContext")
    inventory = preliminary(context["inventory_ref"], "SourceInventory")
    git = load_git_catalog(repo_root, inventory["repository_commit"])
    if inventory["root_tree_sha1"] != git.tree_sha1:
        raise QualificationError("INVENTORY_PIN_MISMATCH", "inventory root tree does not match commit", stage=2)
    combined = dict(git.files)
    for path, data in supplied.items():
        if path in git.modes and path not in git.files:
            raise QualificationError("INVENTORY_PIN_MISMATCH", f"auxiliary bytes shadow a nonregular pinned path: {path}", stage=2)
        if path in combined and combined[path] != data:
            raise QualificationError("CONFLICTING_ARTIFACT_BYTES", f"external bytes override pinned Git path: {path}")
        if path.startswith(CATALOG_ROOTS) and path not in git.files:
            raise QualificationError("INVENTORY_PIN_MISMATCH", f"untracked catalog artifact: {path}", stage=2)
        combined[path] = data
    expected = {item["path"]: item for item in git.catalog_entries}
    declared = {}
    for item in sorted(inventory["entries"], key=canonical_bytes):
        path = item["path"]
        if path in declared and declared[path] != item:
            raise QualificationError("CONFLICTING_ARTIFACT_BYTES", f"conflicting inventory entries: {path}")
        declared[path] = item
    missing = sorted(set(expected) - set(declared))
    if missing:
        raise QualificationError("INVENTORY_OMISSION", canonical_bytes({"missing_paths": missing}).decode(), stage=2)
    if declared != expected:
        raise QualificationError("INVENTORY_PIN_MISMATCH", "inventory entries differ from complete pinned catalog tree", stage=2)
    return EvidenceAnchor(_key=_ANCHOR_KEY, git=git, artifacts=combined, context_ref=context_ref)


def _publish_no_replace(target: Path, data: bytes) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".assessment-", dir=target.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, target)
        except FileExistsError:
            if target.is_symlink() or target.read_bytes() != data:
                raise QualificationError("CONFLICTING_ARTIFACT_BYTES", "assessment publication would overwrite different bytes")
    finally:
        Path(temporary).unlink(missing_ok=True)


def write_assessment(result: dict, *, anchor: EvidenceAnchor, query_bytes: bytes,
                     output_dir: Path | str) -> Path:
    """Recompute and atomically retain a synthetic assessment; never a live store.

    An arbitrary schema-valid result is not a checked envelope. The identity
    evaluator recomputes it before persistence; display IDs cannot overwrite.
    """
    validate_shape(result, "AssessmentResult")
    if result["validation_status"] != "valid":
        raise QualificationError("INVALID_SCHEMA", "invalid-result diagnostics are not accepted assessment publications", stage=8)
    if not isinstance(anchor, EvidenceAnchor) or result["domain"] != "synthetic":
        raise QualificationError("DOMAIN_MISMATCH", "only isolated synthetic assessment persistence is enabled", stage=8)
    from ai_lab.providers.qualification import evaluate_synthetic_r2

    recomputed = evaluate_synthetic_r2(query_bytes, anchor=anchor)
    data = canonical_bytes(result)
    if data != canonical_bytes(recomputed):
        raise QualificationError("CONTEXT_ANCHOR_MISMATCH", "result differs from exact-input recomputation", stage=8)
    base = Path(output_dir).resolve()
    repository = Path(__file__).resolve().parents[2]
    if base == repository or repository in base.parents:
        raise QualificationError("DOMAIN_MISMATCH", "synthetic outputs require a store outside the production checkout", stage=8)
    digest = hashlib.sha256(data).hexdigest()
    target = base / "synthetic" / "sha256" / digest[:2] / (digest + ".json")
    display_key = hashlib.sha256(result["assessment_id"].encode("utf-8")).hexdigest()
    index = base / "synthetic" / "by-id" / (display_key + ".json")
    if index.exists() and index.read_bytes() != data:
        raise QualificationError("CONFLICTING_ARTIFACT_BYTES", "assessment display ID already names different bytes")
    try:
        _publish_no_replace(target, data)
        _publish_no_replace(index, data)
    except OSError as exc:
        raise QualificationError("KNOWN_SOURCE_UNAVAILABLE", "assessment storage failed; no accepted publication", stage=8) from exc
    return target
