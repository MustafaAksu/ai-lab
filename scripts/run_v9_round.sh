#!/bin/bash
# Run the eight atomic questions of the v9 admission round.
# Resumable. Partial completion is representable, which is why the round is
# atomic. Q8 carries the whole document and MUST be pre-flighted first.
set -uo pipefail
cd /root/AI-Lab || { echo "ABORT: /root/AI-Lab not found"; exit 1; }
D=docs/comparisons/comp_v9
[ -f "$D/MANIFEST.json" ] || { echo "ABORT: run build_v9_round.py first"; exit 1; }
RAN=0; DONE=0; FAILED=0
for f in "$D"/Q*-*.txt; do
  QID=$(basename "$f" | cut -d- -f1)   # Q1..Q7, Q8a, Q8b
  SLUG=$(basename "$f" .txt | cut -d- -f2-)
  if ls docs/comparisons/COMP-*-v9-admission-"${QID,,}"-*.md >/dev/null 2>&1; then
    echo "$QID already run, skipping"; DONE=$((DONE+1)); continue
  fi
  echo "=== $QID $SLUG ==="
  if python3 scripts/compare_providers.py \
       --title "v9 admission $QID $SLUG" "$(cat "$f")" 2>&1 | grep -E "Captured invocation|outcome:"; then
    RAN=$((RAN+1))
  else
    echo "  FAILED -- continuing; questions are independent"; FAILED=$((FAILED+1))
  fi
done
echo "================================================"
echo "ran $RAN, skipped $DONE, failed $FAILED"
echo
echo "This is the first round whose records carry stop_reason (GAP-0006)."
echo "An outcome line reading stop_reason='max_tokens' means that answer is"
echo "TRUNCATED and must not be treated as a review, however much text it has."
