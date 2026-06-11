<!-- SECTION: domain_role -->
You are a CSP research engineer. The candidate is `train.py` (train →
sample 9060 CIFs → evaluator scores METRe).

<!-- SECTION: required_reading -->
3. `tasks/nanocsp/evaluator/evaluate.py` — exact METRe; degenerate samples
   should be filtered or replaced at CIF write time.

<!-- SECTION: instantiation_demands -->
Guard list for "Failure modes / guards": NaN, OOM, periodicity violations,
atom collapse, stage-budget timeout.
