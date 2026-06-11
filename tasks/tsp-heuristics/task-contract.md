# tsp-heuristics task contract (domain rules — read with protocol-core.md)

Task: Euclidean TSP heuristic search. Candidate = `solver.py` (+ `design.md`).
Score = **mean tour-length ratio** against a fixed nearest-neighbor baseline
over the validation instance set — **lower is better** (1.0 = NN quality,
~0.80 ≈ 2-opt quality, optimal is instance-dependent but well below 0.80).

## Data

Validation instances at `data/tsp/val/{idx:05d}.tsp` (64 instances,
generated deterministically by `prepare_data` — seeded, identical for every
campaign). Format: plain text, one city per line, `x y` floats in `[0, 1]²`.
Instance sizes range 50–200 cities. Distance = Euclidean, full symmetric.

| split | count | use |
|---|---|---|
| val | 64 | solver input; scored by the evaluator |

There is no training data — the candidate is a solver, not a model. The
solver must handle any instance in the size range; hardcoding per-instance
answers or conditioning on instance index is a protocol violation (the
evaluator's instances are fixed, so memorization is detectable across
improve lineages — analyze flags suspiciously instance-specific code).

## Candidate contract — solver.py

Single stage, cap enforced by solver.py itself:

| stage | cap | meaning |
|---|---|---|
| solve | `--max_minutes` (default 30) | total wall-clock for ALL instances; poll the clock, write the best tour found so far for each instance before exit |

Budget across instances is the solver's own allocation decision (uniform,
size-proportional, or adaptive — a legitimate search dimension).

Required CLI + outputs:

- Flags: `--max_minutes <float>`, `--run_name <str>`.
- Input: read every `data/tsp/val/*.tsp`.
- Output: `runs/<run_name>/tours/{idx:05d}.tour` — one line, space-separated
  city indices (a permutation of `0..n-1`). Missing or invalid tour for an
  instance scores the penalty ratio 2.0.
- Single process; use multiple threads only within the slot's
  `OMP_NUM_THREADS` / `cpus_per_slot` lease.
- Self-contained at runtime: no pip install inside solver.py.
- No writes outside `runs/<run_name>/`.

Required prints at the end (display lines; `metrics.json` is authoritative):

```
---
total_seconds: <float>
instances_solved: <int>
```

Operators must not break these line prefixes.

## Scoring detail

For each instance: `ratio = candidate_tour_length / nn_baseline_length`
(NN baseline: greedy nearest-neighbor from city 0, fixed in the evaluator).
`score = mean(ratio)` over all 64 instances, penalty 2.0 for
missing/invalid tours. The evaluator validates that each tour is a true
permutation before scoring it.
