#!/usr/bin/env bash
# Build the base venv (numpy only). Idempotent. Gate: prints "gate: ok".
set -euo pipefail
REPO="$(git rev-parse --show-toplevel)"
VENV="$REPO/.base-venv"

if [ ! -d "$VENV" ]; then
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q -U pip
  "$VENV/bin/pip" install -q -r "$REPO/tasks/tsp-heuristics/evaluator/requirements.txt"
fi

"$VENV/bin/python" -c "import numpy"
echo "gate: ok"
