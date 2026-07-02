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
    read_context_pack,
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

    args = parser.parse_args()

    prompt = " ".join(args.prompt)
    context_pack = None

    if args.context_pack and args.latest_context:
        parser.error("Use either --context-pack or --latest-context, not both.")

    if args.context_pack:
        context_pack = read_context_pack(args.context_pack)

    if args.latest_context:
        context_pack = build_latest_context_pack_text(
            task=context_task_label(prompt),
            token_budget=args.token_budget,
            model_target=args.model_target,
            scope=args.scope,
            require_admission=args.require_admission,
        )

    final_prompt = build_prompt(prompt=prompt, context_pack=context_pack)

    if args.print_prompt:
        print(final_prompt)
        return 0

    provider = provider_from_name(args.provider)

    print(f"Provider: {provider.name}")
    print()
    print(provider.ask(final_prompt))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
