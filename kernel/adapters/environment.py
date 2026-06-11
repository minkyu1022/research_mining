#!/usr/bin/env python3
"""Environment adapter — set up a slot's execution environment.

    python kernel/adapters/environment.py setup --kind venv \
        --wt .worktrees/slot-0 [--parent-env runs/<tag>/<sha>/.venv]

Prints the slot's interpreter path on the last line (`python: <path>`).

Kinds:
    venv  — hard-link clone (cp -al) of the parent node's venv when given
            (children inherit deps cheaply, copy-on-write), else of
            .base-venv built by the task's setup_env hook.
    none  — no per-slot environment; system python3.
    conda — not implemented (add when a task package needs it).
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def setup_venv(wt: Path, parent_env: Path | None) -> Path:
    staging = wt / "runs" / "staging"
    staging.mkdir(parents=True, exist_ok=True)
    dst = staging / ".venv"
    if dst.exists():
        raise SystemExit(f"slot env already exists: {dst}")
    src = parent_env if parent_env and parent_env.is_dir() else Path(".base-venv")
    if not src.is_dir():
        raise SystemExit(f"base env missing: {src} (run the task's setup_env hook first)")
    # Hard-link clone: near-free, and pip installs into the clone break the
    # links for changed files only (copy-on-write at file granularity).
    subprocess.run(["cp", "-al", str(src), str(dst)], check=True)
    return dst / "bin" / "python"


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    ps = sub.add_parser("setup")
    ps.add_argument("--kind", required=True, choices=["venv", "none", "conda"])
    ps.add_argument("--wt", required=True, help="slot worktree path")
    ps.add_argument("--parent-env", default=None, help="parent node's env dir to inherit")
    args = p.parse_args()

    if args.kind == "venv":
        python = setup_venv(Path(args.wt), Path(args.parent_env) if args.parent_env else None)
    elif args.kind == "none":
        python = Path(shutil.which("python3") or "/usr/bin/python3")
    else:
        raise SystemExit("environment.kind=conda not implemented")

    print(f"python: {python}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
