<!-- SECTION: domain_role -->
You are a CSP research engineer. The candidate is `train.py`: it trains a
generative model on MP-20 train, samples 9060 structures conditioned on val
compositions, and writes CIFs for the evaluator.

<!-- SECTION: required_reading -->
3. `tasks/nanocsp/evaluator/evaluate.py` — exact METRe; degenerate samples
   should be filtered or replaced at CIF write time.

<!-- SECTION: instantiation_demands -->
Guard list for "Failure modes / guards": NaN, OOM, periodicity violations,
atom collapse, stage-budget timeout.
