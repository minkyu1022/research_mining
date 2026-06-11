<!-- SECTION: stages -->
Do NOT invoke `train.py` via CLI (it would sample 9060 CIFs, ~10 min).
Write a tiny probe script that imports train.py's components and exercises
critical paths with **1 batch only**. Prefix every python invocation with
`CUDA_VISIBLE_DEVICES=<gpu from manifest>`; use the slot venv python; write
probe artifacts to `<cwd>/runs/staging-gate/`.

### Stage 1: Import probe (≤ 1 s)
`python -c "import sys; sys.path.insert(0,'<cwd>'); import train"`.
ModuleNotFoundError → fail (the gate does not pip install; deps belong to
the generator).

### Stage 2: Model init + 1 training step (≤ 15 s) — highest value
Probe script: instantiate the model on cuda with tiny batch (8–16); print
param count + peak VRAM after init; load ONE training batch; run 1 forward +
backward + optimizer step under the candidate's autocast setting. Assert:
loss finite; grad_norm < 1e4; peak VRAM safely under `vram_total_mb`
(manifest) with headroom for the full batch.

### Stage 2.5 (draft only, or novel learning dynamics): 20–50 step mini-train (≤ 60 s)
Assert loss roughly monotone-decreasing (short spikes allowed). Skip for
improve/debug nodes — the parent already proved trajectory stability.

### Stage 3: 1-batch sampling (≤ 30 s)
Call the candidate's sampling entry point (read train.py to find it) with
n=16 val compositions. Check: all `frac_coords` finite and in `[0,1)` after
wrap; all lattices `|det| > 0.1`; min interatomic distance > 0.5 Å.

### Stage 4: CIF roundtrip (≤ 5 s)
Write 1 sampled structure via the candidate's CIF path; re-parse with
`pymatgen.io.cif.CifParser`; verify the roundtrip is valid.
