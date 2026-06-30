from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import argparse
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai_lab.providers.claude_provider import ClaudeProvider
from ai_lab.providers.openai_provider import OpenAIProvider


def utc_now_iso() -> str:
    """Return current UTC time in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def markdown_escape_fence(text: str) -> str:
    """
    Prevent accidental Markdown fence breakage.

    If a provider response contains triple backticks, use a longer fence.
    """
    if "```" in text:
        return "````"
    return "```"


def build_markdown_artifact(
    prompt: str,
    responses: dict[str, dict[str, str]],
    created_at: str,
    command: str,
) -> str:
    """Build a Markdown artifact containing one provider comparison run."""
    lines: list[str] = [
        "# Provider Comparison",
        "",
        "## Metadata",
        "",
        f"- created_at: `{created_at}`",
        f"- command: `{command}`",
        f"- providers: `{', '.join(responses.keys())}`",
        "",
        "### Models",
        "",
    ]

    for provider_name, data in responses.items():
        lines.append(f"- {provider_name}: `{data['model']}`")

    lines.extend(
        [
            "",
            "## Prompt",
            "",
            prompt,
            "",
        ]
    )

    for provider_name, data in responses.items():
        response = data["response"]
        fence = markdown_escape_fence(response)
        lines.extend(
            [
                f"## {provider_name} Response",
                "",
                f"- model: `{data['model']}`",
                "",
                fence,
                response,
                fence,
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the same prompt against OpenAI and Claude."
    )
    parser.add_argument("prompt", nargs="+", help="Prompt to send to both providers.")
    parser.add_argument(
        "--save",
        type=Path,
        help="Optional Markdown file path to save the comparison artifact.",
    )

    args = parser.parse_args()
    prompt = " ".join(args.prompt)

    providers = [
        OpenAIProvider(),
        ClaudeProvider(),
    ]

    responses: dict[str, dict[str, str]] = {}

    print("Prompt:")
    print(prompt)
    print()

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

    if args.save:
        created_at = utc_now_iso()
        command = " ".join(sys.argv)
        artifact = build_markdown_artifact(
            prompt=prompt,
            responses=responses,
            created_at=created_at,
            command=command,
        )

        args.save.parent.mkdir(parents=True, exist_ok=True)
        args.save.write_text(artifact, encoding="utf-8")
        print(f"Saved comparison artifact: {args.save}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
