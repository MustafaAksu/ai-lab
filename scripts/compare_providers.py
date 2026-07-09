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
    format_provider_context_budget_preview,
    provider_context_summary_payload,
    provider_l0_invariant_validation_result,
    format_provider_latest_context_policy,
    prompt_sha256,
    provider_latest_context_metadata,
    read_context_pack,
    resolve_provider_warning_admission_cap,
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
        "--print-context-policy",
        action="store_true",
        help=(
            "Print the resolved provider latest-context policy and do not call "
            "providers."
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
        "--auto-include-l0-discovery",
        action="store_true",
        help=(
            "Opt in to automatic L0 summary inclusion from deterministic "
            "L0 discovery advisor suggestions. Requires --latest-context."
        ),
    )
    parser.add_argument(
        "--auto-include-l0-discovery-max-items",
        type=int,
        default=None,
        help="Optional cap for automatic L0 discovery inclusions.",
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

    if args.include_l0 and not args.latest_context:
        parser.error("--include-l0 requires --latest-context.")

    if args.auto_include_l0_discovery and not args.latest_context:
        parser.error("--auto-include-l0-discovery requires --latest-context.")

    if (
        args.auto_include_l0_discovery_max_items is not None
        and not args.auto_include_l0_discovery
    ):
        parser.error(
            "--auto-include-l0-discovery-max-items requires "
            "--auto-include-l0-discovery."
        )

    if args.include_l0 and args.print_context_summary and args.summary_format != "json":
        parser.error("--include-l0 with --print-context-summary requires --summary-format json.")

    if args.validate_l0_invariants and not args.print_context_summary:
        parser.error("--validate-l0-invariants requires --print-context-summary.")

    if args.validate_l0_invariants and args.summary_format != "json":
        parser.error("--validate-l0-invariants requires --summary-format json.")

    if args.fail_on_invalid_l0 and not args.validate_l0_invariants:
        parser.error("--fail-on-invalid-l0 requires --validate-l0-invariants.")

    if args.context_pack:
        context_pack = read_context_pack(args.context_pack)
        extra_metadata["context_pack"] = str(args.context_pack)

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
        task_label = context_task_slug(raw_prompt)
        context_kwargs = {
            "task": context_task_label(raw_prompt),
            "token_budget": args.token_budget,
            "model_target": args.model_target,
            "scope": args.scope,
            "require_admission": args.require_admission,
            "max_warning_admissions": resolved_max_warning_admissions,
            "task_label": task_label,
        }

        if args.include_l0:
            context_kwargs["include_l0"] = tuple(args.include_l0)
            context_kwargs["l0_store"] = args.l0_store

        if args.auto_include_l0_discovery:
            context_kwargs["auto_include_l0_discovery"] = True
            context_kwargs["l0_store"] = args.l0_store

        if args.auto_include_l0_discovery_max_items is not None:
            context_kwargs["auto_include_l0_discovery_max_items"] = (
                args.auto_include_l0_discovery_max_items
            )

        context_manifest = build_latest_context_pack_manifest(**context_kwargs)
        context_manifest = replace(context_manifest, task_label=task_label)
        context_pack = render_context_pack_markdown(context_manifest)

        extra_metadata.update(
            provider_latest_context_metadata(
                require_admission=args.require_admission,
                max_warning_admissions=args.max_warning_admissions,
            )
        )

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
