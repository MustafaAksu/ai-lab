"""Provider configuration defaults for AI-Lab.

These are code-level defaults, not secrets.
Secrets remain in local git-ignored files.

Environment overrides are optional and intended for high-stakes
provider comparisons, not as a global default policy change.
"""

from __future__ import annotations

import os


OPENAI_MODEL = os.getenv("AI_LAB_OPENAI_MODEL", "gpt-5")
OPENAI_REASONING_EFFORT = os.getenv("AI_LAB_OPENAI_REASONING_EFFORT") or None

CLAUDE_MODEL = os.getenv("AI_LAB_CLAUDE_MODEL", "claude-sonnet-4-5")
CLAUDE_EFFORT = os.getenv("AI_LAB_CLAUDE_EFFORT") or None
# Raised from 4096 by PLAN-20260722-0001 (WARR-20260722-0001) as a governed
# settings rider: the COMP-0032 challenge round was truncated at 4096 and the
# saved artifact could not explain the truncation from its own contents.
# ExecutionProfile capture now records the limit in effect for every call.
# Environment and per-call overrides still take precedence; no other default
# is altered (warrant condition 6).
CLAUDE_MAX_TOKENS = int(os.getenv("AI_LAB_CLAUDE_MAX_TOKENS", "16000"))
