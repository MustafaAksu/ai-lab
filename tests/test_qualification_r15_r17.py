"""R15/R17 full-boundary regressions; fictional identities, real Git and paths."""

from __future__ import annotations

import copy
import hashlib
from pathlib import Path
import subprocess

import pytest

from ai_lab.providers import qualification_records as qr
from ai_lab.providers.qualification import evaluate_synthetic_r2
from qualification_fixtures import build_fixture, encode, extra_source


def git(root, *args, input=None):
    return subprocess.check_output(["git", "-C", str(root), *args], input=input,
                                   stderr=subprocess.PIPE).decode().strip()


def outcome(call):
    """Unexpected exceptions are assertion observations, never mutation catches."""
    try:
        return call(), None
    except Exception as error:
        return None, error


def codes(value):
    result = set()
    if isinstance(value, dict):
        if isinstance(value.get("code"), str):
            result.add(value["code"])
        for item in value.values():
            result.update(codes(item))
    elif isinstance(value, list):
        for item in value:
            result.update(codes(item))
    return result


def replacement_fixtures(tmp_path):
    def adverse(state):
        extra_source(state, side=0, target=1, evidence="contradicted", name="adverse")

    original = build_fixture(tmp_path / "original", catalog_mutator=adverse)
    favorable = build_fixture(tmp_path / "favorable")
    assert original.evaluate()["Q_identity"]["value"] == "withheld"
    assert favorable.evaluate()["Q_identity"]["value"] == "conditions_satisfied"
    a, b = original.inventory["repository_commit"], favorable.inventory["repository_commit"]
    tree_a, tree_b = original.inventory["root_tree_sha1"], favorable.inventory["root_tree_sha1"]
    assert tree_a != tree_b
    git(original.root, "fetch", "--no-tags", str(favorable.root), b)
    return original, favorable, a, b, tree_a, tree_b


@pytest.mark.parametrize("replacement_kind", ["commit", "tree"])
def test_r15_original_anchor_keeps_adverse_source_despite_replacement(tmp_path, replacement_kind):
    original, favorable, a, b, tree_a, tree_b = replacement_fixtures(tmp_path)
    git(original.root, "replace", *( (a, b) if replacement_kind == "commit" else (tree_a, tree_b) ))
    assert git(original.root, "rev-parse", "--verify", a + "^{commit}") == a
    if replacement_kind == "commit":
        assert git(original.root, "rev-parse", a + "^{tree}") == tree_b
    result, error = outcome(original.evaluate)
    assert error is None, f"replacement changed a genuine pin: {error!r}"
    assert result["validation_status"] == "valid"
    assert result["Q_identity"]["value"] == "withheld"
    assert "CAPTURE_CONTRADICTED" in codes(result)
    assert original.anchor().git.tree_sha1 == tree_a
    adverse_id = original.state["sources"][-1]["capture"]["record_id"]
    assert adverse_id in {finding["source_id"] for finding in result["source_findings"]}


def test_r15_replacement_cannot_admit_pruned_inventory_claiming_original_commit(tmp_path):
    original, favorable, a, b, tree_a, tree_b = replacement_fixtures(tmp_path)
    git(original.root, "replace", a, b)
    favorable.root = original.root
    favorable.inventory["repository_commit"] = a
    favorable.seal()
    result, error = outcome(favorable.evaluate)
    assert isinstance(error, qr.QualificationError), (
        "replacement hid the adverse source and admitted a false commit pin", result, error)
    assert error.code == "INVENTORY_PIN_MISMATCH"
    assert tree_a != tree_b


def test_r15_blob_replacement_does_not_change_retained_payload(tmp_path):
    fixture = build_fixture(tmp_path)
    payload_ref = fixture.source_refs[0]["payload_ref"]
    original_bytes = fixture.artifacts[payload_ref["path"]]
    replacement_bytes = b"replacement payload is not the committed payload\n"
    replacement = git(fixture.root, "hash-object", "-w", "--stdin", input=replacement_bytes)
    git(fixture.root, "replace", payload_ref["git_blob_sha1"], replacement)
    assert subprocess.check_output(["git", "-C", str(fixture.root), "cat-file", "blob",
                                    payload_ref["git_blob_sha1"]]) == replacement_bytes
    anchor, error = outcome(fixture.anchor)
    assert error is None, f"blob replacement affected the pinned object read: {error!r}"
    assert anchor.read(payload_ref) == original_bytes
    assert evaluate_synthetic_r2(fixture.query, anchor=anchor)["Q_identity"]["value"] == "conditions_satisfied"


@pytest.mark.parametrize("malformation", [
    "empty", "missing", "partial_header", "non_ascii_header", "invalid_size", "negative_size",
    "truncated_body", "missing_separator", "trailing_bytes", "wrong_object", "wrong_kind", "body_mismatch",
])
def test_r15_malformed_git_batch_is_typed_refusal(tmp_path, monkeypatch, malformation):
    fixture = build_fixture(tmp_path)
    original_run = qr.subprocess.run

    def altered_run(command, **kwargs):
        result = original_run(command, **kwargs)
        if command[-2:] != ["cat-file", "--batch"]:
            return result
        data = result.stdout
        header, rest = data.split(b"\n", 1)
        object_id, kind, size_text = header.split()
        size = int(size_text)
        body, after = rest[:size], rest[size + 1:]
        variants = {
            "empty": b"", "missing": object_id + b" missing\n",
            "partial_header": header, "non_ascii_header": b"\xff blob 1\nx\n",
            "invalid_size": object_id + b" blob nope\n",
            "negative_size": object_id + b" blob -1\n",
            "truncated_body": header + b"\n" + body[:-1],
            "missing_separator": header + b"\n" + body + after,
            "trailing_bytes": data + b"unexpected trailing bytes",
            "wrong_object": b"0" * 40 + b" blob " + size_text + b"\n" + rest,
            "wrong_kind": object_id + b" tree " + size_text + b"\n" + rest,
            "body_mismatch": header + b"\n" + bytes([body[0] ^ 1]) + body[1:] + b"\n" + after,
        }
        result.stdout = variants[malformation]
        return result

    monkeypatch.setattr(qr.subprocess, "run", altered_run)
    value, error = outcome(lambda: qr.load_git_catalog(fixture.root, fixture.inventory["repository_commit"]))
    assert isinstance(error, qr.QualificationError), (malformation, value, repr(error))
    assert error.code in {"INVENTORY_PIN_MISMATCH", "ARTIFACT_DIGEST_MISMATCH"}


def path_state(root):
    result = {}
    for path in root.rglob("*"):
        key = path.relative_to(root).as_posix()
        if path.is_symlink():
            result[key] = ("symlink", str(path.readlink()))
        elif path.is_file():
            result[key] = ("file", path.read_bytes())
        elif path.is_dir():
            result[key] = ("directory",)
    return result


@pytest.fixture
def accepted_assessment(tmp_path):
    fixture = build_fixture(tmp_path / "fixture")
    anchor = fixture.anchor()
    result = evaluate_synthetic_r2(fixture.query, anchor=anchor)
    assert result["Q_identity"]["value"] == "conditions_satisfied"
    return anchor, encode(fixture.query), result


@pytest.mark.parametrize("redirect", ["synthetic", "cas", "cas_shard", "by_id", "cas_leaf", "by_id_leaf"])
@pytest.mark.parametrize("destination_kind", ["checkout", "outside_store", "inside_store"])
def test_r17_both_publication_paths_refuse_symlink_redirection_before_writes(
        tmp_path, monkeypatch, accepted_assessment, redirect, destination_kind):
    anchor, query_bytes, result = accepted_assessment
    checkout, store = tmp_path / "isolated_checkout", tmp_path / "store"
    checkout.mkdir(); store.mkdir()
    monkeypatch.setattr(qr, "__file__", str(checkout / "ai_lab/providers/qualification_records.py"))
    destinations = {"checkout": checkout, "outside_store": tmp_path / "escaped",
                    "inside_store": store / "redirected"}
    destination = destinations[destination_kind]
    destination.mkdir(exist_ok=True)
    (destination / "sentinel").write_bytes(b"must remain unchanged")
    digest = hashlib.sha256(qr.canonical_bytes(result)).hexdigest()
    display = hashlib.sha256(result["assessment_id"].encode()).hexdigest()
    paths = {"synthetic": store / "synthetic", "cas": store / "synthetic/sha256",
             "cas_shard": store / "synthetic/sha256" / digest[:2],
             "by_id": store / "synthetic/by-id",
             "cas_leaf": store / "synthetic/sha256" / digest[:2] / (digest + ".json"),
             "by_id_leaf": store / "synthetic/by-id" / (display + ".json")}
    redirected = paths[redirect]
    redirected.parent.mkdir(parents=True, exist_ok=True)
    if redirect.endswith("leaf"):
        destination = destination / "destination.json"
        destination.write_bytes(qr.canonical_bytes(result))
    redirected.symlink_to(destination, target_is_directory=not redirect.endswith("leaf"))
    before = path_state(tmp_path)
    value, error = outcome(lambda: qr.write_assessment(result, anchor=anchor,
        query_bytes=query_bytes, output_dir=store))
    assert isinstance(error, qr.QualificationError), (redirect, destination_kind, value, repr(error))
    assert error.code == "DOMAIN_MISMATCH"
    assert path_state(tmp_path) == before, "redirected store must refuse before either publication"


def test_r17_isolated_real_directories_preserve_atomic_idempotent_publication(tmp_path, accepted_assessment):
    anchor, query_bytes, result = accepted_assessment
    store = tmp_path / "isolated-store"
    first = qr.write_assessment(result, anchor=anchor, query_bytes=query_bytes, output_dir=store)
    before = path_state(store)
    second = qr.write_assessment(copy.deepcopy(result), anchor=anchor, query_bytes=query_bytes, output_dir=store)
    assert first == second and path_state(store) == before
    assert first.resolve().is_relative_to(store.resolve())
    assert first.read_bytes() == qr.canonical_bytes(result)
    assert len(list((store / "synthetic/by-id").glob("*.json"))) == 1
