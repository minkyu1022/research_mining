# nanocsp task contract (domain rules — read with protocol-core.md)

Task: crystal structure prediction (CSP) on the MP-20 polymorph split.
Score: **METRe** (validation match rate, higher is better), computed by the
read-only evaluator. Candidate = `train.py` (+ `design.md`).

## Data

Three split files `data/mp20_ps_{train,val,test}.pt`, each a
`torch.load`-able `list[dict]`. Record schema:

| key | dtype | shape | note |
|---|---|---|---|
| `lattice` | `float32` | `[3, 3]` | basis matrix in Å, rows = a, b, c |
| `frac_coords` | `float32` | `[N, 3]` | in `[0, 1)` |
| `atomic_numbers` | `int64` | `[N]` | atomic number Z |
| `identifier` | `str` | — | MP-ID; do not condition on |

`N` is variable per record, `N ∈ [1, 20]`. Batching must accept variable `N`.

| split | count | use |
|---|---|---|
| train | 27137 | gradient updates |
| val | 9060 | sample conditioning on `atomic_numbers` only; scored by evaluator |
| test | held out | leaderboard only — never access during search |

**Polymorph split**: polymorphs of one composition stay on the same side, so
`p(structure | composition)` is genuinely multi-modal — the central modeling
difficulty. **Niggli prior**: every lattice is Niggli-reduced (cell angles in
`[60°, 120°]`). **Scoring**: pymatgen `StructureMatcher(ltol=0.3, stol=0.5,
angle_tol=10°)`.

Schema probe (run before committing to an internal representation):

```python
import torch
d = torch.load("data/mp20_ps_train.pt", weights_only=False)
print({k: (type(v).__name__, tuple(getattr(v, "shape", ())), getattr(v, "dtype", None)) for k, v in d[0].items()})
```

## Data access rules (hard constraints)

- Training reads only `mp20_ps_train.pt`.
- `mp20_ps_val.pt` is accessed only after training, and only its per-record
  `atomic_numbers` may reach the sampler.
- Test data untouched.
- The evaluator always scores against the full val split (n=9060); never
  subset or alias.

## Candidate contract — train.py

Three stages in sequence, each cap enforced by train.py itself:

| stage | cap | meaning |
|---|---|---|
| training | `--max_minutes` (default 120) | poll wall-clock, exit the loop immediately at the cap |
| sampling | `--sample_minutes` (default 60) | produce up to 9060 CIFs; on budget, write the partial set and proceed (missing CIF = no candidate for that composition) |
| evaluate | ≤ 60 min, fixed | kernel-invoked evaluator subprocess; on timeout the node is `[CRASH]` |

Caps are campaign-frozen and uniform across nodes. A debug whose only fix is
"raise the cap" is not a debug — fix efficiency instead.

Required CLI + outputs:

- Flags: `--max_minutes <float>`, `--sample_minutes <float>`, `--run_name <str>`.
- Sample output: 9060 CIFs at `runs/<run_name>/val_samples/{idx:05d}.cif`,
  idx-aligned with val record order, canonical form (lattice `[3,3]` Å,
  `frac_coords ∈ [0,1)`, integer Z).
- Internal representation is free — any form continuous and invertible with
  the canonical I/O form.
- Single GPU; the slot sets `CUDA_VISIBLE_DEVICES`, just use `cuda`.
- Self-contained at runtime: no pip install inside train.py.
- **No model checkpoints / auxiliary writes** (`torch.save(state_dict)`,
  EMA-save, `save_pretrained`, …). Only `runs/<run_name>/val_samples/*.cif`;
  no writes outside `runs/<run_name>/`.

Required prints at the end (display lines; the evaluator writes the
authoritative `metrics.json`):

```
---
training_seconds: <float>
total_seconds:    <float>
peak_vram_mb:     <float>
```

Operators must not break these line prefixes.

## Hardware

GPU count and per-GPU VRAM are detected at bootstrap, not hardcoded. The
detected `vram_total_mb` arrives in every manifest; size models to sit
safely under it with headroom for allocator slack — an OOM wastes the run.
