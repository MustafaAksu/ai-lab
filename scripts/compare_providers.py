from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
import argparse
import json
import re
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai_lab.documentation.context_pack_renderer import render_context_pack_markdown
from ai_lab.documentation.prompt_context import (
    build_latest_context_pack_manifest,
    build_prompt,
    context_task_label,
    context_task_slug,
    prompt_sha256,
    read_context_pack,
)
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
    parser.add_argument(
        "--context-pack",
        type=Path,
        default=None,
        help="Optional rendered context pack Markdown file.",
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
    parser.add_argument(
        "--print-prompt",
        action="store_true",
        help="Print the final comparison prompt and do not call providers.",
    )

    args = parser.parse_args()
    raw_prompt = " ".join(args.prompt)
    title = args.title
    context_pack = None
    context_manifest = None
    context_manifest_path: Path | None = None
    extra_metadata: dict[str, str] = {}

    if args.context_pack and args.latest_context:
        parser.error("Use either --context-pack or --latest-context, not both.")

    if args.context_pack:
        context_pack = read_context_pack(args.context_pack)
        extra_metadata["context_pack"] = str(args.context_pack)

    if args.latest_context:
        task_label = context_task_slug(raw_prompt)
        context_manifest = build_latest_context_pack_manifest(
            task=context_task_label(raw_prompt),
            token_budget=args.token_budget,
            model_target=args.model_target,
            scope=args.scope,
            require_admission=args.require_admission,
            task_label=task_label,
        )
        context_manifest = replace(context_manifest, task_label=task_label)
        context_pack = render_context_pack_markdown(context_manifest)
        extra_metadata["context_policy"] = "latest_context"

        if args.token_budget is not None:
            extra_metadata["token_budget"] = str(args.token_budget)

        if args.model_target:
            extra_metadata["model_target"] = args.model_target

    provider_prompt = build_prompt(raw_prompt, context_pack=context_pack)

    if args.latest_context and context_manifest is not None:
        context_manifest = replace(
            context_manifest,
            full_prompt_hash=prompt_sha256(provider_prompt),
        )
        context_pack = render_context_pack_markdown(context_manifest)
        provider_prompt = build_prompt(raw_prompt, context_pack=context_pack)

    if args.print_prompt:
        print(provider_prompt)
        return 0

    save_path: Path | None = args.save

    if save_path is None and title:
        save_path = auto_comparison_path(title, args.out_dir)

    if save_path is not None and title is None:
        title = title_from_prompt(raw_prompt)

    if save_path is not None and context_manifest is not None:
        context_manifest_path = save_path.with_suffix(".context.json")
        extra_metadata["context_manifest"] = str(context_manifest_path)

    providers = [
        OpenAIProvider(),
        ClaudeProvider(),
    ]

    responses: dict[str, dict[str, str]] = {}

    print("Prompt:")
    print(raw_prompt)
    print()

    for provider in providers:
        model = getattr(provider, "model", "unknown")
        print(f"=== {provider.name} ({model}) ===")
        answer = provider.ask(provider_prompt)
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
            prompt=raw_prompt,
            responses=responses,
            created_at=created_at,
            command=command,
            comparison_id=comparison_id,
            title=title,
            extra_metadata=extra_metadata or None,
        )

        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text(artifact, encoding="utf-8")
        print(f"Saved comparison artifact: {save_path}")

        if context_manifest is not None and context_manifest_path is not None:
            context_manifest_json = (
                json.dumps(context_manifest.to_dict(), indent=2, sort_keys=True)
                + "\n"
            )
            context_manifest_path.write_text(context_manifest_json, encoding="utf-8")
            print(f"Saved context manifest: {context_manifest_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
