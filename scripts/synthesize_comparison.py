from __future__ import annotations

from pathlib import Path
import argparse
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai_lab.documentation.comparison_synthesis import (
    auto_synthesis_path,
    build_synthesis_artifact,
    build_synthesis_prompt,
    title_from_comparison_path,
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


def synthesis_id_from_path(path: Path) -> str:
    """Extract SYNCOMP-XXXX from a synthesis artifact path."""
    parts = path.name.split("-")
    if len(parts) >= 2 and parts[0] == "SYNCOMP":
        return f"{parts[0]}-{parts[1]}"

    return path.stem


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Synthesize a saved provider comparison artifact."
    )
    parser.add_argument(
        "comparison",
        type=Path,
        help="Path to a saved COMP Markdown artifact.",
    )
    parser.add_argument(
        "--provider",
        default="openai",
        choices=["openai", "claude", "anthropic"],
        help="Provider to use for synthesis.",
    )
    parser.add_argument(
        "--title",
        help="Optional synthesis title. Defaults to the comparison artifact title.",
    )
    parser.add_argument(
        "--save",
        type=Path,
        help="Optional explicit Markdown file path for the synthesis artifact.",
    )

    args = parser.parse_args()

    if not args.comparison.exists():
        print(f"Comparison artifact not found: {args.comparison}")
        return 1

    comparison_markdown = args.comparison.read_text(encoding="utf-8")
    title = args.title or title_from_comparison_path(args.comparison)
    save_path = args.save or auto_synthesis_path(title)

    provider = provider_from_name(args.provider)
    model = getattr(provider, "model", "unknown")

    synthesis_prompt = build_synthesis_prompt(comparison_markdown)

    print(f"Source comparison: {args.comparison}")
    print(f"Synthesizer: {provider.name} ({model})")
    print()

    synthesis_response = provider.ask(synthesis_prompt)

    print("=== Synthesis ===")
    print(synthesis_response)
    print()

    created_at = utc_now_iso()
    command = " ".join(sys.argv)
    synthesis_id = synthesis_id_from_path(save_path)

    artifact = build_synthesis_artifact(
        synthesis_id=synthesis_id,
        title=title,
        comparison_path=args.comparison,
        comparison_markdown=comparison_markdown,
        synthesis_response=synthesis_response,
        synthesizer_provider=provider.name,
        synthesizer_model=model,
        created_at=created_at,
        command=command,
    )

    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_text(artifact, encoding="utf-8")

    print(f"Saved synthesis artifact: {save_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
