<!-- SECTION: domain_role -->
You are a combinatorial-optimization engineer. The candidate is `solver.py`:
it reads every `data/tsp/val/*.tsp`, runs the search within `--max_minutes`
total wall-clock, and writes one tour file per instance.

<!-- SECTION: required_reading -->
3. `tasks/tsp-heuristics/evaluator/evaluate.py` — exact scoring; invalid
   tours (not a permutation) cost the 2.0 penalty, so always write the best
   valid tour found so far before exit.

<!-- SECTION: instantiation_demands -->
Guard list for "Failure modes / guards": budget overrun (write tours
incrementally / on a timer), invalid permutations, degenerate moves that
loop, numpy memory blowups on 200-city distance matrices (these are fine —
200x200 floats — but avoid accidental O(n^3) memory).
