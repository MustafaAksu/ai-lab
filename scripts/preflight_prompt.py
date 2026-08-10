#!/usr/bin/env python3
"""Pre-flight a prompt against a provider before committing to a round.

Why this exists. COMP-0038 sent a 12,496-token prompt and got back a response
with one empty thinking block and no text: the entire output budget went on
reasoning tokens. It was recorded status success, because no exception was
raised, and nothing in the record could distinguish it from a complete review.
Pre-flighting the largest prompt of a round catches that for the cost of one
call instead of poisoning a round artifact.

SUCCESS CRITERION IS COMPLETION, NOT THE PRESENCE OF TEXT. A response with
stop_reason max_tokens is truncated and is not a working configuration, however
much text it contains. An earlier version of this probe reported a truncated
17,000-character response as working, which is the defect class GAP-0007
records.

This is an EXPERIMENTAL PROBE. It writes nothing and produces no
InvocationRecord: it calls the provider adapter directly rather than going
through scripts/compare_providers.py, so nothing enters the provenance graph.
That is deliberate, and it means a probe's outcome is not governed evidence.

Usage:
    python3 scripts/preflight_prompt.py <prompt-file> [--provider claude|openai]

Exit codes: 0 complete, 2 truncated, 3 no text produced, 4 call failed.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from ai_lab.providers.claude_provider import ClaudeProvider  # noqa: E402
from ai_lab.providers.openai_provider import OpenAIProvider  # noqa: E402
from ai_lab.providers.settings import CLAUDE_MAX_TOKENS  # noqa: E402

# stop_reason values that mean the call ended early rather than finishing.
TRUNCATING = {
    "max_tokens",                      # anthropic
    "model_context_window_exceeded",   # anthropic, added in SDK 0.121.0
    "max_output_tokens",               # openai incomplete_details.reason
    "incomplete",                      # openai status
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("prompt_file", type=pathlib.Path)
    ap.add_argument("--provider", choices=("claude", "openai"), default="claude")
    args = ap.parse_args()

    if not args.prompt_file.exists():
        print(f"ABORT: {args.prompt_file} not found")
        return 4

    text = args.prompt_file.read_text(encoding="utf-8").rstrip("\n")
    provider = ClaudeProvider() if args.provider == "claude" else OpenAIProvider()

    print(f"file        : {args.prompt_file}")
    print(f"chars       : {len(text)}   est input tok: {len(text)//3}  (3.0 ch/tok)")
    print(f"sha256      : {hashlib.sha256(text.encode()).hexdigest()}")
    print(f"provider    : {provider.name}")
    if args.provider == "claude":
        print(f"max_tokens  : {CLAUDE_MAX_TOKENS}")
    print()

    try:
        outcome = provider.ask_with_outcome(text)
    except Exception as exc:  # noqa: BLE001 - a probe reports any failure verbatim
        print(f"EXCEPTION {type(exc).__name__}: {exc}")
        return 4

    print(f"  stop_reason        : {outcome.stop_reason!r} "
          f"(from {outcome.stop_reason_field})")
    print(f"  input_tokens       : {outcome.input_tokens}")
    print(f"  output_tokens      : {outcome.output_tokens}")
    if args.provider == "claude" and outcome.output_tokens is not None:
        print(f"  headroom           : {CLAUDE_MAX_TOKENS - outcome.output_tokens}")
    print(f"  content blocks     : {outcome.content_block_types}")
    print(f"  text chars         : {outcome.text_chars}")
    if outcome.output_tokens is not None:
        est_text = outcome.text_chars // 3
        print(f"  est thinking tok   : {outcome.output_tokens - est_text}")
    print()

    truncated = outcome.stop_reason in TRUNCATING
    if outcome.text_chars and not truncated:
        print("VERDICT: COMPLETE. Safe to run this prompt in the round.")
        print(f"\nfirst 300 chars:\n{outcome.text[:300]!r}")
        return 0
    if truncated:
        print(f"VERDICT: TRUNCATED. stop_reason={outcome.stop_reason!r} with "
              f"{outcome.text_chars} chars of text.")
        print("  NOT usable. Text length is not evidence of completeness.")
        print("  Split the prompt. Raising max_tokens is bounded: the SDK refuses")
        print("  non-streaming calls above roughly 21000 with a duration guard.")
        return 2
    print("VERDICT: NO TEXT. The call returned without producing a text block.")
    print(f"  Blocks returned: {outcome.content_block_types}")
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
