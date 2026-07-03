from __future__ import annotations

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai_lab.documentation.prompt_context import (
    build_latest_context_pack_text,
    build_prompt,
    context_task_label,
    context_task_slug,
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
            print("Resolved latest-context policy:")
            print(
                format_provider_latest_context_policy(
                    require_admission=args.require_admission,
                    max_warning_admissions=args.max_warning_admissions,
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
