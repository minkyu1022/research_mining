#!/usr/bin/env bash
# Generate the fixed validation instances (seeded, deterministic). Idempotent.
set -euo pipefail
REPO="$(git rev-parse --show-toplevel)"

"$REPO/.base-venv/bin/python" "$REPO/tasks/tsp-heuristics/evaluator/gen_instances.py"

n=$(ls "$REPO/data/tsp/val/"*.tsp 2>/dev/null | wc -l)
[ "$n" -eq 64 ] || { echo "gate: fail — expected 64 instances, found $n" >&2; exit 1; }
echo "gate: ok"
