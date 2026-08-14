#!/bin/bash
# Install the self-model pre-commit hook.
#
# The hook refuses a commit whose staged self-model index does not describe the
# staged records. Four index-lag incidents on 2026-08-12, with four different
# causes, each landed the repository in a state that failed its own audit.
#
# It compares record-derived content only. repo_head, generated_at and
# audit_summary are excluded because during a pre-commit hook `git rev-parse
# HEAD` names the PARENT of the commit being made, so none of the three can be
# what the commit will carry.
#
# git commit --no-verify bypasses it. That is stated rather than prevented.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
chmod +x scripts/hooks/pre_commit_self_model.py
ln -sf ../../scripts/hooks/pre_commit_self_model.py .git/hooks/pre-commit
echo "installed: .git/hooks/pre-commit -> scripts/hooks/pre_commit_self_model.py"
echo
echo "Also recommended, to stop the laptop/server divergence that produced a"
echo "merge commit on 2026-08-12:"
echo "  git config pull.rebase true"
