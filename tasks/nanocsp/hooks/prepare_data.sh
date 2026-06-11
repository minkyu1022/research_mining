#!/usr/bin/env bash
# Download / build the MP-20 polymorph-split data. Idempotent.
# Gate: prints "gate: ok" when all three splits exist.
set -euo pipefail
REPO="$(git rev-parse --show-toplevel)"

"$REPO/.base-venv/bin/python" "$REPO/tasks/nanocsp/evaluator/prepare_data.py"

for split in train val test; do
  [ -f "$REPO/data/mp20_ps_${split}.pt" ] || { echo "gate: fail — missing $split split" >&2; exit 1; }
done

echo "gate: ok"
