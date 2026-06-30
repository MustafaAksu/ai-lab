from __future__ import annotations

from pathlib import Path
import argparse
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai_lab.documentation.reask import (
    ReaskPromptError,
    extract_suggested_reask_prompt,
)
from scripts.compare_providers import (
    auto_comparison_path,
    build_markdown_artifact,
    utc_now_iso,
)
from ai_lab.providers.claude_provider import ClaudeProvider
from ai_lab.providers.openai_provider import OpenAIProvider


def compare_prompt(prompt: str) -> dict[str, dict[str, str]]:
    """Run a prompt against all comparison providers."""
    providers = [
        OpenAIProvider(),
        ClaudeProvider(),
    ]

    responses: dict[str, dict[str, str]] = {}

    for provider in providers:
        model = getattr(provider, "model", "unknown")
        print(f"=== {provider.name} ({model}) ===")
        answer = provider.ask(prompt)
        responses[provider.name] = {
            "model": model,
            "response": answer,
        }
        print(answer)
        print()

    return responses


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Extract the suggested re-ask prompt from a SYNCOMP artifact "
            "and run it as a new provider comparison."
        )
    )
    parser.add_argument(
        "synthesis",
        type=Path,
        help="Path to a saved SYNCOMP Markdown artifact.",
    )
    parser.add_argument(
        "--title",
        help="Optional title for the new comparison artifact.",
    )
    parser.add_argument(
        "--save",
        type=Path,
        help="Optional explicit Markdown path for the new comparison artifact.",
    )
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="Only print the extracted re-ask prompt; do not call providers.",
    )

    args = parser.parse_args()

    if not args.synthesis.exists():
        print(f"Synthesis artifact not found: {args.synthesis}")
        return 1

    artifact = args.synthesis.read_text(encoding="utf-8")

    try:
        prompt = extract_suggested_reask_prompt(artifact)
    except ReaskPromptError as error:
        print(f"Could not extract re-ask prompt: {error}")
        return 1

    print("Re-ask prompt:")
    print(prompt)
    print()

    if args.print_only:
        return 0

    title = args.title or f"Re-Ask from {args.synthesis.stem}"
    save_path = args.save or auto_comparison_path(title)

    responses = compare_prompt(prompt)

    created_at = utc_now_iso()
    command = " ".join(sys.argv)
    comparison_id = save_path.name.split("-")[0] + "-" + save_path.name.split("-")[1]

    artifact = build_markdown_artifact(
        prompt=prompt,
        responses=responses,
        created_at=created_at,
        command=command,
        comparison_id=comparison_id,
        title=title,
        extra_metadata={
            "source_synthesis": args.synthesis.as_posix(),
        },
    )

    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_text(artifact, encoding="utf-8")

    print(f"Saved re-ask comparison artifact: {save_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
