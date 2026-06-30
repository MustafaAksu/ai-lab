from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


BOOTSTRAP_PREDICATES = {
    "based_on",
    "reviews",
    "supersedes",
    "supports",
    "disputes",
    "resolves",
}

BOOTSTRAP_VOCABULARY = "bootstrap_predicates"
BOOTSTRAP_VOCABULARY_VERSION = "0.1"

VALID_SCOPES = {"version", "lineage", "exact"}


def load_yaml_file(path: Path) -> dict[str, Any]:
    """Load a YAML file as a dictionary."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    if data is None:
        return {}

    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")

    return data


def validate_edge_record(edge: dict[str, Any]) -> list[str]:
    """
    Validate a bootstrap EDGE record according to ADR-0003 v0.2.

    The validator intentionally covers only the minimal bootstrap rules.
    It does not attempt to compute full graph state yet.
    """
    errors: list[str] = []

    _require_string(edge, "id", errors)
    _require_string(edge, "origin_type", errors)
    _require_string(edge, "current_type", errors)
    _require_string(edge, "title", errors)
    _require_string(edge, "created_at", errors)

    if edge.get("origin_type") != "relation_record":
        errors.append("origin_type must be 'relation_record'.")

    if edge.get("current_type") != "relation_record":
        errors.append("current_type must be 'relation_record'.")

    if "status" in edge:
        errors.append("EDGE records must not contain mutable 'status'.")

    created_at = edge.get("created_at")
    if isinstance(created_at, str):
        _validate_iso_utc(created_at, errors)

    _validate_reference(edge.get("subject"), "subject", errors)
    _validate_reference(edge.get("object"), "object", errors)
    _validate_predicate(edge.get("predicate"), errors)
    _validate_warrant(edge.get("warrant"), errors)
    _validate_contributors(edge.get("contributors"), errors)

    return errors


def validate_edge_file(path: Path) -> list[str]:
    """Validate one EDGE YAML file."""
    try:
        edge = load_yaml_file(path)
    except Exception as exc:
        return [f"Failed to load YAML: {exc}"]

    return validate_edge_record(edge)


def validate_edges_directory(path: Path) -> dict[Path, list[str]]:
    """Validate all YAML EDGE files in a directory."""
    results: dict[Path, list[str]] = {}

    if not path.exists():
        return results

    for edge_file in sorted(path.glob("*.yaml")):
        results[edge_file] = validate_edge_file(edge_file)

    return results


def _require_string(data: dict[str, Any], key: str, errors: list[str]) -> None:
    value = data.get(key)

    if not isinstance(value, str) or not value.strip():
        errors.append(f"Missing or invalid required string field: {key}.")


def _validate_iso_utc(value: str, errors: list[str]) -> None:
    if not value.endswith("Z"):
        errors.append("created_at must be ISO-8601 UTC and end with 'Z'.")
        return

    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append("created_at is not a valid ISO-8601 datetime.")


def _validate_reference(value: Any, name: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{name} must be a mapping.")
        return

    ref_id = value.get("id")
    scope = value.get("scope")

    if not isinstance(ref_id, str) or not ref_id.strip():
        errors.append(f"{name}.id is required.")

    if scope not in VALID_SCOPES:
        errors.append(
            f"{name}.scope must be one of {sorted(VALID_SCOPES)}."
        )

    if scope == "version":
        version = value.get("version")
        if not isinstance(version, str) or not version.strip():
            errors.append(f"{name}.version is required when scope is 'version'.")

    if scope in {"lineage", "exact"} and "version" in value:
        errors.append(
            f"{name}.version should not be used when scope is '{scope}'."
        )


def _validate_predicate(value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("predicate must be a mapping.")
        return

    predicate_id = value.get("id")
    vocabulary = value.get("vocabulary")
    version = value.get("version")

    if predicate_id not in BOOTSTRAP_PREDICATES:
        errors.append(
            f"predicate.id must be one of {sorted(BOOTSTRAP_PREDICATES)}."
        )

    if vocabulary != BOOTSTRAP_VOCABULARY:
        errors.append(f"predicate.vocabulary must be '{BOOTSTRAP_VOCABULARY}'.")

    if version != BOOTSTRAP_VOCABULARY_VERSION:
        errors.append(
            f"predicate.version must be '{BOOTSTRAP_VOCABULARY_VERSION}'."
        )


def _validate_warrant(value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("warrant must be a mapping.")
        return

    summary = value.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        errors.append("warrant.summary is required.")


def _validate_contributors(value: Any, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append("contributors must be a non-empty list.")
        return

    for index, contributor in enumerate(value):
        if not isinstance(contributor, dict):
            errors.append(f"contributors[{index}] must be a mapping.")
            continue

        peer_id = contributor.get("peer_id")
        role = contributor.get("role")
        substrate = contributor.get("substrate")

        if not isinstance(peer_id, str) or not peer_id.strip():
            errors.append(f"contributors[{index}].peer_id is required.")

        if not isinstance(role, str) or not role.strip():
            errors.append(f"contributors[{index}].role is required.")

        if not isinstance(substrate, str) or not substrate.strip():
            errors.append(f"contributors[{index}].substrate is required.")
