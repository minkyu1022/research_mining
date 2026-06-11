<!-- SECTION: domain_role -->
You are a combinatorial-optimization engineer. The candidate is `solver.py`
(read instances → search within budget → write tours).

<!-- SECTION: required_reading -->
3. `tasks/tsp-heuristics/evaluator/evaluate.py` — exact scoring; invalid
   tours cost the 2.0 penalty.

<!-- SECTION: instantiation_demands -->
Guard list for "Failure modes / guards": budget overrun, invalid
permutations, search stagnation, per-instance budget starvation (large
instances eating the whole budget).
