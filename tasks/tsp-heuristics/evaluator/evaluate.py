#!/usr/bin/env python3
"""Score a tours directory against the fixed validation set.

For each instance: ratio = tour_length / nearest-neighbor baseline length.
Missing or invalid tours (not a permutation) score the penalty ratio 2.0.
Prints `tsp_ratio: <float>` (mean ratio, lower is better) — display only;
run_eval.py wraps this into the kernel's metrics.json contract.
"""
import argparse
import sys
from pathlib import Path

import numpy as np

PENALTY_RATIO = 2.0
VAL_DIR = Path("data/tsp/val")


def load_instance(path: Path) -> np.ndarray:
    return np.loadtxt(path, ndmin=2)


def tour_length(coords: np.ndarray, tour: np.ndarray) -> float:
    pts = coords[tour]
    return float(np.linalg.norm(pts - np.roll(pts, -1, axis=0), axis=1).sum())


def nn_baseline(coords: np.ndarray) -> float:
    n = len(coords)
    visited = np.zeros(n, dtype=bool)
    tour = [0]
    visited[0] = True
    for _ in range(n - 1):
        last = coords[tour[-1]]
        dists = np.linalg.norm(coords - last, axis=1)
        dists[visited] = np.inf
        nxt = int(dists.argmin())
        tour.append(nxt)
        visited[nxt] = True
    return tour_length(coords, np.array(tour))


def read_tour(path: Path, n: int):
    try:
        tour = np.array([int(t) for t in path.read_text().split()])
    except (ValueError, OSError):
        return None
    if len(tour) != n or not np.array_equal(np.sort(tour), np.arange(n)):
        return None
    return tour


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--tours_dir", required=True)
    args = p.parse_args()
    tours_dir = Path(args.tours_dir)

    instances = sorted(VAL_DIR.glob("*.tsp"))
    if not instances:
        print("tsp_ratio: nan")
        print("error: no validation instances — run prepare_data first", file=sys.stderr)
        return 1

    ratios, solved = [], 0
    for inst in instances:
        coords = load_instance(inst)
        tour = read_tour(tours_dir / f"{inst.stem}.tour", len(coords))
        if tour is None:
            ratios.append(PENALTY_RATIO)
            continue
        ratios.append(tour_length(coords, tour) / nn_baseline(coords))
        solved += 1

    print(f"tsp_ratio: {np.mean(ratios):.6f}")
    print(f"instances_scored: {solved}/{len(instances)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
