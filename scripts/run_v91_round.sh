#!/bin/bash
# Run the five re-review questions for ABS-0004 v9.1.
# Scope fixed by DECISION-20260811-0001: only the questions whose v9 evidence
# sets prevented reliable judgment. Resumable.
set -uo pipefail
cd /root/AI-Lab || { echo "ABORT: /root/AI-Lab not found"; exit 1; }
D=docs/comparisons/comp_v91
[ -f "$D/MANIFEST.json" ] || { echo "ABORT: run build_v91_round.py first"; exit 1; }
RAN=0; DONE=0; FAILED=0
for f in "$D"/R[1-5]-*.txt; do
  QID=$(basename "$f" | cut -d- -f1)
  SLUG=$(basename "$f" .txt | cut -d- -f2-)
  if ls docs/comparisons/COMP-*-v91-rereview-"${QID,,}"-*.md >/dev/null 2>&1; then
    echo "$QID already run, skipping"; DONE=$((DONE+1)); continue
  fi
  echo "=== $QID $SLUG ==="
  if python3 scripts/compare_providers.py \
       --title "v9.1 re-review $QID $SLUG" "$(cat "$f")" 2>&1 | grep -E "Captured invocation|outcome:"; then
    RAN=$((RAN+1))
  else
    echo "  FAILED -- continuing"; FAILED=$((FAILED+1))
  fi
done
echo "================================================"
echo "ran $RAN, skipped $DONE, failed $FAILED"
echo
echo "Read the outcome line on each capture. stop_reason max_tokens means that"
echo "answer is truncated and is not a review, however much text it carries."
