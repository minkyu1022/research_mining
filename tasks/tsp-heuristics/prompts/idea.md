<!-- SECTION: domain_role -->
The task is Euclidean TSP heuristic search. A cell = (search paradigm,
move/operator family): paradigm = the *kind* of search process (construction,
local search, metaheuristic, hybrid); move family = the *kind* of solution
transformation it applies. Both axes are first-class. No GPU — designs must
be CPU-budget-realistic (pure-python or numpy-vectorized).

<!-- SECTION: required_reading -->
4. `tasks/tsp-heuristics/evaluator/evaluate.py` — exact scoring (NN-ratio,
   penalty 2.0 for invalid tours).

<!-- SECTION: strategy_demands -->
4. **Adapted to the setting**: 64 instances of 50–200 cities, one shared
   wall-clock budget across all instances, CPU-only. State how the cell
   spends its budget in your rationale.
