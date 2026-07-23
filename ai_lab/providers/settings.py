"""Provider configuration defaults for AI-Lab.

These are code-level defaults, not secrets.
Secrets remain in local git-ignored files.

Environment overrides are optional and intended for high-stakes
provider comparisons, not as a global default policy change.
"""

from __future__ import annotations

import os


# Defaults advanced by DECISION-20260723-0001 on the evidence of the first
# live catalog capture (SNAP-35fbd338ad148fb9, SNAP-c111fceb0ec3809f).
# The prior defaults were literals chosen when this file was written and
# never revisited; claude-sonnet-4-5 was ten months old and absent from the
# provider listing while still accepted by the endpoint.
#
# gpt-5.6-terra: present in the captured listing. Its tier relative to the
# other 5.6 entries is NOT established by any captured evidence; the listing
# carries only id and owned_by. The choice rests on an unverified account
# (ADVISOR-0000) and on operator judgment, both disclosed in the decision
# record. Pricing is unknown because no captured source publishes it.
OPENAI_MODEL = os.getenv("AI_LAB_OPENAI_MODEL", "gpt-5.6-terra")
OPENAI_REASONING_EFFORT = os.getenv("AI_LAB_OPENAI_REASONING_EFFORT") or None

# claude-sonnet-5: present in the captured listing, released 2026-06-29 per
# the provider's own created_at. Deliberately NOT claude-opus-4-8: the
# drafting executor in AI-Lab sessions reports itself as Claude Opus 4.8, so
# configuring the reviewer slot to that identity would collapse reviewer and
# author into one ModelIdentity and fire ABS-0004 C3 on every review of
# drafted work. Sonnet-5 keeps the two identities distinct.
CLAUDE_MODEL = os.getenv("AI_LAB_CLAUDE_MODEL", "claude-sonnet-5")
CLAUDE_EFFORT = os.getenv("AI_LAB_CLAUDE_EFFORT") or None
# Raised from 4096 by PLAN-20260722-0001 (WARR-20260722-0001) as a governed
# settings rider: the COMP-0032 challenge round was truncated at 4096 and the
# saved artifact could not explain the truncation from its own contents.
# ExecutionProfile capture now records the limit in effect for every call.
# Environment and per-call overrides still take precedence; no other default
# is altered (warrant condition 6).
CLAUDE_MAX_TOKENS = int(os.getenv("AI_LAB_CLAUDE_MAX_TOKENS", "16000"))
