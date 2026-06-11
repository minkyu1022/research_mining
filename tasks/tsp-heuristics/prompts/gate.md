<!-- SECTION: stages -->
Do NOT run `solver.py` on the full 64-instance set (that costs the solve
budget). Probe with 1–2 instances only, using the slot venv python from the
manifest, writing probe artifacts to `<cwd>/runs/staging-gate/`.

### Stage 1: Import probe (≤ 1 s)
`python -c "import sys; sys.path.insert(0,'<cwd>'); import solver"`.
ImportError → fail (the gate does not pip install; deps belong to the
generator).

### Stage 2: Single-instance solve (≤ 30 s) — highest value
Run the candidate end-to-end on ONE instance with a tiny budget. Two ways
(read solver.py first to pick): call its per-instance entry point directly
on `data/tsp/val/00000.tsp`, or run the CLI against a probe dir holding one
copied instance with `--max_minutes 0.25`. Assert: a `.tour` file is
written; it is a valid permutation of `0..n-1`; it appears within the
budget.

### Stage 3: Tour quality sanity (≤ 5 s)
Compute the probe tour's length and the instance's nearest-neighbor length
(short numpy snippet — see evaluator/evaluate.py for both formulas).
Assert ratio < 1.5 — a fresh heuristic doing much worse than NN on one
instance signals broken move logic, not bad luck.

### Stage 4: Budget-exit behavior (≤ 20 s)
From solver.py source, verify the wall-clock poll exists and tours are
written before exit (incrementally or on the timer path). If the only write
happens after the full search loop, fail: a budget hit would produce zero
tours.
