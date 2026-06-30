from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import argparse
import re
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai_lab.providers.claude_provider import ClaudeProvider
from ai_lab.providers.openai_provider import OpenAIProvider


DEFAULT_COMPARISON_DIR = Path("docs/comparisons")


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


def slugify(text: str) -> str:
    """Convert a title into a filesystem-safe slug."""
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug or "comparison"


def next_comparison_id(directory: Path) -> str:
    """Return the next COMP-XXXX identifier for a comparison directory."""
    max_number = 0

    if directory.exists():
        for path in directory.glob("COMP-*.md"):
            match = re.match(r"COMP-(\d{4})", path.name)
            if match:
                max_number = max(max_number, int(match.group(1)))

    return f"COMP-{max_number + 1:04d}"


def auto_comparison_path(title: str, directory: Path = DEFAULT_COMPARISON_DIR) -> Path:
    """Build the next comparison artifact path from a title."""
    comparison_id = next_comparison_id(directory)
    slug = slugify(title)
    return directory / f"{comparison_id}-{slug}.md"


def title_from_prompt(prompt: str) -> str:
    """Derive a compact title from a prompt when no title is provided."""
    words = prompt.strip().split()
    title = " ".join(words[:8])
    return title.rstrip(".,:;!?") or "Provider Comparison"


def build_markdown_artifact(
    prompt: str,
    responses: dict[str, dict[str, str]],
    created_at: str,
    command: str,
    comparison_id: str | None = None,
    title: str | None = None,
    extra_metadata: dict[str, str] | None = None,
) -> str:
    """Build a Markdown artifact containing one provider comparison run."""
    heading = "# Provider Comparison"

    if comparison_id and title:
        heading = f"# {comparison_id}: Provider Comparison — {title}"
    elif comparison_id:
        heading = f"# {comparison_id}: Provider Comparison"
    elif title:
        heading = f"# Provider Comparison — {title}"

    lines: list[str] = [
        heading,
        "",
        "## Metadata",
        "",
    ]

    if comparison_id:
        lines.append(f"- comparison_id: `{comparison_id}`")

    if title:
        lines.append(f"- title: `{title}`")

    if extra_metadata:
        for key, value in extra_metadata.items():
            lines.append(f"- {key}: `{value}`")

    lines.extend(
        [
            f"- created_at: `{created_at}`",
            f"- command: `{command}`",
            f"- providers: `{', '.join(responses.keys())}`",
            "",
            "### Models",
            "",
        ]
    )

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
        help="Optional explicit Markdown file path to save the comparison artifact.",
    )
    parser.add_argument(
        "--title",
        help=(
            "Optional comparison title. If --save is omitted, this auto-saves "
            "to the next COMP-XXXX file under docs/comparisons."
        ),
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_COMPARISON_DIR,
        help="Directory for auto-saved comparison artifacts.",
    )

    args = parser.parse_args()
    prompt = " ".join(args.prompt)
    title = args.title

    save_path: Path | None = args.save

    if save_path is None and title:
        save_path = auto_comparison_path(title, args.out_dir)

    if save_path is not None and title is None:
        title = title_from_prompt(prompt)

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

    if save_path:
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
        )

        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text(artifact, encoding="utf-8")
        print(f"Saved comparison artifact: {save_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
