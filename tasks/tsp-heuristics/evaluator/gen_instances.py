#!/usr/bin/env python3
"""Generate the fixed validation instance set. Deterministic (seeded) —
every campaign scores against identical instances. Idempotent."""
import sys
from pathlib import Path

import numpy as np

N_INSTANCES = 64
SIZE_RANGE = (50, 200)
SEED = 20260611


def main() -> int:
    out_dir = Path("data/tsp/val")
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    for idx in range(N_INSTANCES):
        n = int(rng.integers(SIZE_RANGE[0], SIZE_RANGE[1] + 1))
        coords = rng.random((n, 2))
        path = out_dir / f"{idx:05d}.tsp"
        path.write_text("\n".join(f"{x:.9f} {y:.9f}" for x, y in coords) + "\n")
    print(f"gate: ok — {N_INSTANCES} instances in {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
