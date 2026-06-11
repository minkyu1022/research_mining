#!/usr/bin/env bash
# Build the base venv from the task's requirements. Idempotent.
# Gate: prints "gate: ok" on success, exits non-zero on failure.
set -euo pipefail
REPO="$(git rev-parse --show-toplevel)"
VENV="$REPO/.base-venv"

if [ ! -d "$VENV" ]; then
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q -U pip
  "$VENV/bin/pip" install -q -r "$REPO/tasks/nanocsp/evaluator/requirements.txt"
fi

# A venv that imports torch but can't see the GPU silently poisons every node.
"$VENV/bin/python" - <<'EOF'
import torch, sys
sys.exit(0 if torch.cuda.is_available() else 1)
EOF

echo "gate: ok"
