from __future__ import annotations

from pathlib import Path
import argparse
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai_lab.documentation.abstraction import (
    abstraction_id_from_path,
    auto_abstraction_path,
    build_abstraction_artifact,
    build_abstraction_prompt,
    utc_now_iso,
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


def read_source_artifacts(paths: list[Path]) -> list[tuple[Path, str]]:
    """Read source artifacts from disk."""
    artifacts: list[tuple[Path, str]] = []

    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"Source artifact not found: {path}")

        artifacts.append((path, path.read_text(encoding="utf-8")))

    return artifacts


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a generic AI-Lab abstraction artifact over source artifacts."
    )
    parser.add_argument(
        "sources",
        nargs="+",
        type=Path,
        help="Source artifact paths to abstract over.",
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Title for the abstraction artifact.",
    )
    parser.add_argument(
        "--level",
        type=int,
        default=1,
        help="Numeric abstraction level.",
    )
    parser.add_argument(
        "--provider",
        default="openai",
        choices=["openai", "claude", "anthropic"],
        help="Provider to use for abstraction.",
    )
    parser.add_argument(
        "--save",
        type=Path,
        help="Optional explicit Markdown file path for the abstraction artifact.",
    )
    parser.add_argument(
        "--print-prompt",
        action="store_true",
        help="Print the abstraction prompt without calling a provider.",
    )

    args = parser.parse_args()

    if args.level < 1:
        print("Abstraction level must be >= 1.")
        return 1

    try:
        source_artifacts = read_source_artifacts(args.sources)
    except FileNotFoundError as error:
        print(error)
        return 1

    prompt = build_abstraction_prompt(
        title=args.title,
        abstraction_level=args.level,
        source_artifacts=source_artifacts,
    )

    if args.print_prompt:
        print(prompt)
        return 0

    provider = provider_from_name(args.provider)
    model = getattr(provider, "model", "unknown")
    save_path = args.save or auto_abstraction_path(args.title)
    abstraction_id = abstraction_id_from_path(save_path)

    print(f"Creating abstraction: {abstraction_id}")
    print(f"Title: {args.title}")
    print(f"Level: {args.level}")
    print(f"Provider: {provider.name} ({model})")
    print()

    abstraction_response = provider.ask(prompt)

    print("=== Abstraction ===")
    print(abstraction_response)
    print()

    artifact = build_abstraction_artifact(
        abstraction_id=abstraction_id,
        title=args.title,
        abstraction_level=args.level,
        source_paths=args.sources,
        abstraction_response=abstraction_response,
        abstracter_provider=provider.name,
        abstracter_model=model,
        created_at=utc_now_iso(),
        command=" ".join(sys.argv),
    )

    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_text(artifact, encoding="utf-8")

    print(f"Saved abstraction artifact: {save_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
