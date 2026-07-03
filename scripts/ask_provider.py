from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai_lab.documentation.prompt_context import (
    build_latest_context_pack_text,
    build_prompt,
    context_task_label,
    context_task_slug,
    format_provider_context_budget_preview,
    provider_context_summary_payload,
    provider_l0_invariant_validation_result,
    format_provider_latest_context_policy,
    prompt_sha256,
    read_context_pack,
    resolve_provider_warning_admission_cap,
)
from ai_lab.providers.claude_provider import ClaudeProvider
from ai_lab.providers.openai_provider import OpenAIProvider


def provider_from_name(name: str):
    normalized = name.strip().lower()

    if normalized == "openai":
        return OpenAIProvider()

    if normalized in {"claude", "anthropic"}:
        return ClaudeProvider()

    raise ValueError(f"Unknown provider: {name}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Ask one configured AI provider."
    )
    parser.add_argument(
        "provider",
        help="Provider name: openai or claude.",
    )
    parser.add_argument(
        "prompt",
        nargs="+",
        help="Prompt text.",
    )
    parser.add_argument(
        "--context-pack",
        type=Path,
        default=None,
        help="Optional rendered context pack Markdown file.",
    )
    parser.add_argument(
        "--print-prompt",
        action="store_true",
        help="Print the final prompt and do not call the provider.",
    )
    parser.add_argument(
        "--latest-context",
        action="store_true",
        help="Build and include a latest-context pack from repository artifacts.",
    )
    parser.add_argument(
        "--print-context-policy",
        action="store_true",
        help=(
            "Print the resolved provider latest-context policy and do not call "
            "the provider."
        ),
    )
    parser.add_argument(
        "--print-context-summary",
        action="store_true",
        help=(
            "Print the resolved latest-context policy before --print-prompt "
            "dry-run output."
        ),
    )
    parser.add_argument(
        "--context-window",
        type=int,
        help=(
            "Optional context window size for --print-context-summary budget "
            "preview token counts."
        ),
    )
    parser.add_argument(
        "--summary-format",
        choices=("text", "json"),
        default="text",
        help=(
            "Output format for --print-context-summary. Defaults to text."
        ),
    )
    parser.add_argument(
        "--include-l0",
        action="append",
        default=[],
        help=(
            "Explicit L0 chunk id to surface in JSON --print-context-summary. "
            "Repeatable."
        ),
    )
    parser.add_argument(
        "--l0-store",
        type=Path,
        default=Path("docs/memory/l0"),
        help="Directory containing L0 chunk summary JSON files.",
    )
    parser.add_argument(
        "--validate-l0-invariants",
        action="store_true",
        help=(
            "Validate provider L0 summary invariants in JSON "
            "--print-context-summary output."
        ),
    )
    parser.add_argument(
        "--fail-on-invalid-l0",
        action="store_true",
        help=(
            "Return a non-zero exit code when --validate-l0-invariants "
            "finds invalid L0 summary output."
        ),
    )
    parser.add_argument(
        "--token-budget",
        type=int,
        default=None,
        help="Optional token budget when using --latest-context.",
    )
    parser.add_argument(
        "--model-target",
        default=None,
        help="Optional model target when using --latest-context.",
    )
    parser.add_argument(
        "--scope",
        default=None,
        help="Optional L1 memory scope/stream when using --latest-context.",
    )
    parser.add_argument(
        "--require-admission",
        action="store_true",
        help="Require latest-context items to have an admitting admission verdict.",
    )
    parser.add_argument(
        "--max-warning-admissions",
        type=int,
        default=None,
        help=(
            "Optional cap for admit_with_warning items when using latest-context "
            "assembly. Defaults to 1 when --require-admission is enabled "
                "and this option is omitted. Explicit values, including 0, "
                "are preserved."
        ),
    )

    args = parser.parse_args()

    prompt = " ".join(args.prompt)
    context_pack = None

    if args.context_pack and args.latest_context:
        parser.error("Use either --context-pack or --latest-context, not both.")

    if args.print_context_policy and not args.latest_context:
        parser.error("--print-context-policy requires --latest-context.")

    if args.print_context_summary and not args.latest_context:
        parser.error("--print-context-summary requires --latest-context.")

    if args.print_context_summary and not args.print_prompt:
        parser.error("--print-context-summary requires --print-prompt.")

    if args.context_window is not None and args.context_window < 1:
        parser.error("--context-window must be positive.")

    if args.context_window is not None and not args.print_context_summary:
        parser.error("--context-window requires --print-context-summary.")

    if args.summary_format == "json" and not args.print_context_summary:
        parser.error("--summary-format json requires --print-context-summary.")

    if args.include_l0 and not args.print_context_summary:
        parser.error("--include-l0 requires --print-context-summary.")

    if args.include_l0 and args.summary_format != "json":
        parser.error("--include-l0 requires --summary-format json.")

    if args.validate_l0_invariants and not args.print_context_summary:
        parser.error("--validate-l0-invariants requires --print-context-summary.")

    if args.validate_l0_invariants and args.summary_format != "json":
        parser.error("--validate-l0-invariants requires --summary-format json.")

    if args.fail_on_invalid_l0 and not args.validate_l0_invariants:
        parser.error("--fail-on-invalid-l0 requires --validate-l0-invariants.")

    if args.context_pack:
        context_pack = read_context_pack(args.context_pack)

    resolved_max_warning_admissions = resolve_provider_warning_admission_cap(
        require_admission=args.require_admission,
        max_warning_admissions=args.max_warning_admissions,
    )

    if args.print_context_policy:
        print(
            format_provider_latest_context_policy(
                require_admission=args.require_admission,
                max_warning_admissions=args.max_warning_admissions,
            )
        )
        return 0

    if args.latest_context:
        task_label = context_task_slug(prompt)
        context_pack = build_latest_context_pack_text(
            task=context_task_label(prompt),
            token_budget=args.token_budget,
            model_target=args.model_target,
            scope=args.scope,
            require_admission=args.require_admission,
            max_warning_admissions=resolved_max_warning_admissions,
            task_label=task_label,
        )

    final_prompt = build_prompt(prompt=prompt, context_pack=context_pack)

    if args.latest_context:
        context_pack = build_latest_context_pack_text(
            task=context_task_label(prompt),
            token_budget=args.token_budget,
            model_target=args.model_target,
            scope=args.scope,
            require_admission=args.require_admission,
            max_warning_admissions=resolved_max_warning_admissions,
            task_label=context_task_slug(prompt),
            full_prompt_hash=prompt_sha256(final_prompt),
        )
        final_prompt = build_prompt(prompt=prompt, context_pack=context_pack)

    if args.print_prompt:
        if args.print_context_summary:
            if args.summary_format == "json":
                summary = provider_context_summary_payload(
                    require_admission=args.require_admission,
                    max_warning_admissions=args.max_warning_admissions,
                    context_window=args.context_window,
                    include_l0=tuple(args.include_l0),
                    l0_store=args.l0_store,
                )
                validation_failed = False

                if args.validate_l0_invariants:
                    validation = provider_l0_invariant_validation_result(summary)
                    validation_failed = not bool(validation["ok"])
                    summary["validation"] = {"l0_invariants": validation}

                print(json.dumps(summary, indent=2, sort_keys=True))

                if validation_failed and args.fail_on_invalid_l0:
                    return 1
            else:
                print("Resolved latest-context policy:")
                print(
                    format_provider_latest_context_policy(
                        require_admission=args.require_admission,
                        max_warning_admissions=args.max_warning_admissions,
                    )
                )
                print()
                print(
                    format_provider_context_budget_preview(
                        context_window=args.context_window
                    )
                )
            print()
            print("Final prompt:")
        print(final_prompt)
        return 0

    provider = provider_from_name(args.provider)

    print(f"Provider: {provider.name}")
    print()
    print(provider.ask(final_prompt))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
