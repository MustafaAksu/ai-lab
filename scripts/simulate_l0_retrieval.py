from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ai_lab.documentation.l0_retrieval_simulator import (
    build_l0_retrieval_simulator_record,
    l0_candidate_inputs_from_store,
    l0_retrieval_simulator_manifest_document,
)


def _read_json_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return value


def _read_dense_scores(path: Path) -> dict[str, float]:
    value = _read_json_object(path)
    result: dict[str, float] = {}

    for key, score in value.items():
        if not isinstance(score, (int, float)) or isinstance(score, bool):
            raise ValueError(f"Dense score for {key!r} must be numeric.")
        result[str(key)] = float(score)

    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build diagnostic-only L0 hybrid retrieval simulator output."
    )
    parser.add_argument("--query", required=True)
    parser.add_argument("--query-kind", default="user")
    parser.add_argument("--l0-store", type=Path, default=Path("docs/memory/l0"))
    parser.add_argument("--dense-scores", type=Path, required=True)
    parser.add_argument("--bm25-params", type=Path, required=True)
    parser.add_argument("--dense-params", type=Path, required=True)
    parser.add_argument("--combine-policy", type=Path, required=True)
    parser.add_argument("--normalization", type=Path, required=True)
    parser.add_argument("--embedding-model", type=Path, required=True)
    parser.add_argument("--corpus-snapshot-id", required=True)
    parser.add_argument("--l0-index-namespace", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--request-id")
    parser.add_argument("--episode-id")
    parser.add_argument("--manifest-id")
    parser.add_argument("--manifest-version")
    parser.add_argument(
        "--omit-reranker",
        action="store_true",
        help="Omit header.reranker. Readers must treat omission as reranker='none'.",
    )
    parser.add_argument(
        "--no-alias",
        action="store_true",
        help="Do not include the deprecated read-only compatibility alias.",
    )
    parser.add_argument("--output", type=Path)

    args = parser.parse_args()

    dense_scores = _read_dense_scores(args.dense_scores)
    candidate_inputs = l0_candidate_inputs_from_store(
        l0_store=args.l0_store,
        dense_scores=dense_scores,
    )

    record = build_l0_retrieval_simulator_record(
        query_text=args.query,
        query_kind=args.query_kind,
        candidate_inputs=candidate_inputs,
        bm25_params=_read_json_object(args.bm25_params),
        dense_params=_read_json_object(args.dense_params),
        combine_policy=_read_json_object(args.combine_policy),
        normalization=_read_json_object(args.normalization),
        embedding_model=_read_json_object(args.embedding_model),
        corpus_snapshot_id=args.corpus_snapshot_id,
        l0_index_namespace=args.l0_index_namespace,
        run_id=args.run_id,
        request_id=args.request_id,
        episode_id=args.episode_id,
        manifest_id=args.manifest_id,
        manifest_version=args.manifest_version,
        reranker=None if args.omit_reranker else "none",
    )

    document = l0_retrieval_simulator_manifest_document(
        record,
        include_alias=not args.no_alias,
    )

    output = json.dumps(document, indent=2, sort_keys=True) + "\n"

    if args.output is None:
        print(output, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"Saved L0 retrieval simulator diagnostics: {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
