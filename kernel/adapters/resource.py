#!/usr/bin/env python3
"""Resource adapter — map a slot index to its lease.

The kernel is resource-agnostic: a slot leases one unit from the pool that
the task's detect_resources hook reported. This adapter turns (pool, slot)
into the env vars and manifest fields for that slot.

    python kernel/adapters/resource.py lease --pool '<json>' --slot N

Pool JSON (from detect_resources):
    gpu: {"type":"gpu","units":[0,1,2],"vram_total_mb":24210}
    cpu: {"type":"cpu","units":[0,1,2,3],"cpus_per_slot":2}
    api: {"type":"api","units":[0,1],"requests_per_minute":60}

Output: one JSON line {"env": {...}, "fields": {...}}
    env    — exported when launching the slot's candidate / gate probes
    fields — copied verbatim into every subagent manifest for this slot
"""
import argparse
import json
import sys


def lease(pool: dict, slot: int) -> dict:
    units = pool.get("units")
    if not isinstance(units, list) or not units:
        raise SystemExit("pool.units must be a non-empty list")
    if not 0 <= slot < len(units):
        raise SystemExit(f"slot {slot} out of range for {len(units)} units")
    unit = units[slot]
    rtype = pool.get("type")

    if rtype == "gpu":
        return {
            "env": {"CUDA_VISIBLE_DEVICES": str(unit)},
            "fields": {"gpu": unit, "vram_total_mb": pool.get("vram_total_mb")},
        }
    if rtype == "cpu":
        return {
            "env": {"OMP_NUM_THREADS": str(pool.get("cpus_per_slot", 1))},
            "fields": {"worker": unit, "cpus_per_slot": pool.get("cpus_per_slot", 1)},
        }
    if rtype == "api":
        # Key material itself is NEVER in the pool or the manifest — only the
        # index; the environment resolves it (e.g. API_KEY_3) outside git.
        return {
            "env": {"API_KEY_INDEX": str(unit)},
            "fields": {"key_index": unit, "requests_per_minute": pool.get("requests_per_minute")},
        }
    raise SystemExit(f"unknown resource type: {rtype!r}")


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    pl = sub.add_parser("lease")
    pl.add_argument("--pool", required=True, help="pool JSON from detect_resources")
    pl.add_argument("--slot", type=int, required=True)
    args = p.parse_args()

    print(json.dumps(lease(json.loads(args.pool), args.slot)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
