#!/usr/bin/env python3
"""Kernel-invoked evaluator wrapper for the tsp-heuristics task.

Runs evaluate.py against a tours directory and writes the kernel score
contract: metrics.json {"score": <float>, "valid": <bool>, "metrics": {...}}.
The kernel parses this file — never stdout. Only this kernel-owned stage
writes metrics.json; candidate code never does.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--tours_dir", required=True)
    p.add_argument("--out", required=True, help="path to write metrics.json")
    p.add_argument("--timeout", type=int, default=600)
    args = p.parse_args()

    result = {"score": None, "valid": False, "metrics": {}}
    try:
        proc = subprocess.run(
            [sys.executable, str(HERE / "evaluate.py"), "--tours_dir", args.tours_dir],
            capture_output=True, text=True, timeout=args.timeout,
        )
        out = proc.stdout + "\n" + proc.stderr
        m = re.search(r"^tsp_ratio:\s*([\d.naif+-]+)\s*$", out, re.MULTILINE | re.IGNORECASE)
        if m:
            try:
                score = float(m.group(1))
            except ValueError:
                score = float("nan")
            if score == score:  # not NaN
                result["score"] = score
                result["valid"] = proc.returncode == 0
        m2 = re.search(r"^instances_scored:\s*(\d+)/(\d+)", out, re.MULTILINE)
        if m2:
            result["metrics"]["instances_scored"] = int(m2.group(1))
            result["metrics"]["instances_total"] = int(m2.group(2))
        result["metrics"]["evaluator_returncode"] = proc.returncode
    except subprocess.TimeoutExpired:
        result["metrics"]["error"] = f"evaluator timeout after {args.timeout}s"

    Path(args.out).write_text(json.dumps(result, indent=2) + "\n")
    print(f"score: {result['score']}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
