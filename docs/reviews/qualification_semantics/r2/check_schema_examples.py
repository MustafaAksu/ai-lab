#!/usr/bin/env python3
"""Syntax-only review utility; no resolver, binding, or qualification evaluation.

Requires an already installed jsonschema package. Writes one JSON report to
stdout and makes no filesystem changes. It is not registered in the runtime or
pytest workflow. A successful run establishes only the declared schema/parse
oracles; references in SCHEMA-EXAMPLES.json are deliberately dummy values.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import re
import sys
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


RFC3339 = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
    r"(?:\.[0-9]{1,6})?(?:Z|[+-][0-9]{2}:[0-9]{2})"
)


class StrictJSONError(ValueError):
    """Duplicate keys or a nonfinite JSON number are rejected before schema checks."""


def strict_json(text: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                raise StrictJSONError("duplicate JSON object key")
            result[key] = value
        return result

    def constant(_: str) -> Any:
        raise StrictJSONError("nonfinite JSON number")

    def finite_float(text: str) -> float:
        value = float(text)
        if not math.isfinite(value):
            raise StrictJSONError("nonfinite JSON number")
        return value

    return json.loads(
        text,
        object_pairs_hook=pairs,
        parse_constant=constant,
        parse_float=finite_float,
    )


def timestamp(value: Any) -> bool:
    """The proposed timestamp subset: real calendar date and explicit offset.

    Uppercase T/Z and at most six fractional digits match the schema. Naive
    datetimes and leap-second spellings are unsupported. datetime validates
    calendar fields and UTC-offset bounds after the lexical check.
    """
    if not isinstance(value, str):
        return True  # JSON Schema's type constraint owns non-string rejection.
    if RFC3339.fullmatch(value) is None:
        return False
    try:
        instant = dt.datetime.fromisoformat(
            value[:-1] + "+00:00" if value.endswith("Z") else value
        )
    except ValueError:
        return False
    return instant.tzinfo is not None and instant.utcoffset() is not None


def digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def check_local_refs(node: Any) -> None:
    if isinstance(node, dict):
        if "$ref" in node and not node["$ref"].startswith("#/$defs/"):
            raise ValueError("schema contains a non-local $ref")
        for value in node.values():
            check_local_refs(value)
    elif isinstance(node, list):
        for value in node:
            check_local_refs(value)


def check_oracles(schema: dict[str, Any], corpus: dict[str, Any]) -> list[dict[str, Any]]:
    checker = FormatChecker()
    # jsonschema can omit optional RFC3339 dependencies. Register an actual
    # calendar/timezone checker instead of silently accepting all date-times.
    checker.checks("date-time")(timestamp)
    seen: set[str] = set()
    results: list[dict[str, Any]] = []

    for case in corpus["schema_cases"]:
        case_id = case["case_id"]
        if case_id in seen:
            raise ValueError("duplicate corpus case_id")
        seen.add(case_id)
        expected = case["expected_schema_valid"]
        if type(expected) is not bool:
            raise ValueError("expected_schema_valid must be a Boolean oracle")
        definition = case["definition"]
        if definition not in schema["$defs"]:
            raise ValueError("corpus names an undefined local schema")
        fragment = {
            "$schema": schema["$schema"],
            "$ref": "#/$defs/" + definition,
            "$defs": schema["$defs"],
        }
        validator = Draft202012Validator(fragment, format_checker=checker)
        errors = sorted(
            validator.iter_errors(case["document"]),
            key=lambda error: (
                "/".join(map(str, error.absolute_path)),
                "/".join(map(str, error.absolute_schema_path)),
            ),
        )
        observed = not errors
        results.append({
            "case_id": case_id,
            "kind": "schema",
            "definition": definition,
            "expected_valid": expected,
            "observed_valid": observed,
            "passed": observed == expected,
            "diagnostics": [
                {
                    "instance_path": list(error.absolute_path),
                    "schema_path": list(error.absolute_schema_path),
                    "validator": error.validator,
                    "message": error.message[:500],
                }
                for error in errors
            ],
        })

    for case in corpus["parsing_cases"]:
        case_id = case["case_id"]
        if case_id in seen:
            raise ValueError("duplicate corpus case_id")
        seen.add(case_id)
        expected = case["expected_parse_valid"]
        if type(expected) is not bool:
            raise ValueError("expected_parse_valid must be a Boolean oracle")
        error_name = None
        try:
            strict_json(case["raw_json"])
            observed = True
        except (StrictJSONError, json.JSONDecodeError, ValueError) as error:
            observed = False
            error_name = type(error).__name__
        results.append({
            "case_id": case_id,
            "kind": "strict_json_parsing",
            "expected_valid": expected,
            "observed_valid": observed,
            "passed": observed == expected,
            "error_type": error_name,
        })
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    folder = Path(__file__).resolve().parent
    parser.add_argument("--schema", type=Path, default=folder / "ASSESSMENT-SCHEMA.json")
    parser.add_argument("--corpus", type=Path, default=folder / "SCHEMA-EXAMPLES.json")
    args = parser.parse_args()

    schema_bytes = args.schema.read_bytes()
    corpus_bytes = args.corpus.read_bytes()
    schema = strict_json(schema_bytes.decode("utf-8"))
    corpus = strict_json(corpus_bytes.decode("utf-8"))
    check_local_refs(schema)
    Draft202012Validator.check_schema(schema)
    results = check_oracles(schema, corpus)
    ok = all(result["passed"] for result in results)
    report = {
        "report_kind": "qualification_r2_syntax_only_validation",
        "status": "pass" if ok else "fail",
        "observed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "jsonschema_version": importlib.metadata.version("jsonschema"),
        "schema_sha256": digest(schema_bytes),
        "corpus_sha256": digest(corpus_bytes),
        "checker_sha256": digest(Path(__file__).read_bytes()),
        "meta_schema": "draft-2020-12",
        "meta_schema_valid": True,
        "reference_policy": "local #/$defs references only; no remote resolution",
        "format_policy": "explicit offset, real calendar date, uppercase T/Z, 0-6 fractional digits; no leap-second spelling",
        "scope": "Syntax/parse oracles only. No digest dereference, source selection, identity binding, qualification, independent review or runtime registration.",
        "schema_cases": sum(result["kind"] == "schema" for result in results),
        "parsing_cases": sum(result["kind"] == "strict_json_parsing" for result in results),
        "passed_cases": sum(result["passed"] for result in results),
        "results": results,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
