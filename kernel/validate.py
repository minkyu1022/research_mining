#!/usr/bin/env python3
"""Validate a task package before a campaign may launch.

    python kernel/validate.py tasks/<name>

Checks the machine contract (task.yml schema), required files, hook
executability, and that every {{var}} the skeletons use is derivable.
Exit 0 = launchable; non-zero = abort.
"""
import re
import stat
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

REPO = Path(__file__).resolve().parent.parent
ERRORS, WARNINGS = [], []


def err(msg): ERRORS.append(msg)
def warn(msg): WARNINGS.append(msg)


def main() -> int:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    task_dir = (REPO / sys.argv[1]).resolve() if not Path(sys.argv[1]).is_absolute() else Path(sys.argv[1])
    if not task_dir.is_dir():
        sys.exit(f"not a directory: {task_dir}")

    # --- task.yml schema ---
    yml = task_dir / "task.yml"
    if not yml.exists():
        sys.exit("missing task.yml")
    cfg = yaml.safe_load(yml.read_text())

    for key in ("name", "artifacts", "score", "evaluator", "resources", "environment", "budgets", "hooks"):
        if key not in cfg:
            err(f"task.yml: missing top-level key '{key}'")

    arts = (cfg.get("artifacts") or {}).get("required") or []
    if "design.md" not in arts:
        err("artifacts.required must include design.md (the per-node hypothesis record)")
    if len(arts) < 2:
        err("artifacts.required must list at least one candidate file besides design.md")

    score = cfg.get("score") or {}
    if score.get("direction") not in ("max", "min"):
        err("score.direction must be 'max' or 'min'")
    if not score.get("primary_key"):
        err("score.primary_key required")

    ev = cfg.get("evaluator") or {}
    if not ev.get("command"):
        err("evaluator.command required")
    else:
        # first token after optional interpreter should exist if it is a path into the task dir
        for tok in ev["command"].split():
            if tok.startswith("tasks/") and not (REPO / tok).exists():
                err(f"evaluator.command references missing file: {tok}")

    if (cfg.get("resources") or {}).get("type") not in ("gpu", "cpu", "api"):
        err("resources.type must be one of gpu|cpu|api")
    if (cfg.get("environment") or {}).get("kind") not in ("venv", "conda", "none"):
        err("environment.kind must be one of venv|conda|none")
    if "gate_seconds" not in (cfg.get("budgets") or {}):
        err("budgets.gate_seconds required")

    # --- required files ---
    for rel in ("task-contract.md", "prior-art.md"):
        if not (task_dir / rel).exists():
            err(f"missing {rel}")
    for agent in ("idea", "draft", "improve", "debug", "gate", "analyze"):
        if not (task_dir / "prompts" / f"{agent}.md").exists():
            warn(f"prompts/{agent}.md missing — skeleton sections will be empty")
    gate_prompt = task_dir / "prompts" / "gate.md"
    if gate_prompt.exists() and "SECTION: stages" not in gate_prompt.read_text():
        err("prompts/gate.md must define SECTION: stages (the gate is task-defined)")

    # --- hooks ---
    for hook_name, rel in (cfg.get("hooks") or {}).items():
        hook = task_dir / rel
        if not hook.exists():
            err(f"hooks.{hook_name}: missing file {rel}")
        elif not hook.stat().st_mode & stat.S_IXUSR:
            err(f"hooks.{hook_name}: {rel} not executable (chmod +x)")

    # --- skeleton variable coverage ---
    derivable = {"task_name", "run_tag", "cell_axes", "ambition_bar", "artifacts_list", "artifacts_bullets"}
    for skel in (REPO / "kernel" / "agent-skeletons").glob("*.md"):
        for var in re.findall(r"\{\{(?!section:)(\w+)\}\}", skel.read_text()):
            if var not in derivable:
                err(f"skeleton {skel.name} uses underivable variable {{{{{var}}}}}")

    for w in WARNINGS:
        print(f"WARN  {w}")
    for e in ERRORS:
        print(f"ERROR {e}")
    print(f"{task_dir.name}: {'FAIL' if ERRORS else 'OK'} ({len(ERRORS)} errors, {len(WARNINGS)} warnings)")
    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
