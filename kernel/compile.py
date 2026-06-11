#!/usr/bin/env python3
"""Compile a task package into runnable agent definitions + resolved campaign config.

    python kernel/compile.py --task nanocsp --run-tag may31a

Renders kernel/agent-skeletons/*.md with the task's prompt sections and
task.yml-derived variables, then writes:

    .claude/agents/<agent>.md                      (what Claude Code dispatches)
    campaigns/<run_tag>/.resolved/prompts/*.md     (audit copy — what agents saw)
    campaigns/<run_tag>/.resolved/{task.yml,task-contract.md,protocol-core.md}

Substitution is deliberately dumb (no template engine): {{section:NAME}} is
replaced by the named section of tasks/<task>/prompts/<agent>.md (empty if the
task omits it), {{var}} by a task.yml-derived scalar. Unknown {{var}} fails.
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

REPO = Path(__file__).resolve().parent.parent
AGENTS = ["idea", "draft", "improve", "debug", "gate", "analyze"]
SECTION_RE = re.compile(r"<!--\s*SECTION:\s*(\w+)\s*-->")
VAR_RE = re.compile(r"\{\{(?!section:)(\w+)\}\}")
SECTION_REF_RE = re.compile(r"\{\{section:(\w+)\}\}")


def parse_sections(text: str) -> dict:
    """Split a task prompt file into named sections by <!-- SECTION: x --> markers."""
    sections, matches = {}, list(SECTION_RE.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[m.group(1)] = text[m.end():end].strip()
    return sections


def build_vars(cfg: dict, run_tag: str) -> dict:
    required = cfg["artifacts"]["required"]
    return {
        "task_name": cfg["name"],
        "run_tag": run_tag,
        "cell_axes": cfg.get("cell_axes", "approach"),
        "ambition_bar": cfg.get("ambition_bar", "a strong published baseline"),
        "artifacts_list": ", ".join(required),
        "artifacts_bullets": "\n".join(f"- `<cwd>/{a}`" for a in required),
    }


def strip_web_tools(rendered: str, agent: str, cfg: dict) -> str:
    """Remove WebSearch/WebFetch from the frontmatter tools line for agents
    the task does not grant web access (permissions.agents_web)."""
    allowed = (cfg.get("permissions") or {}).get("agents_web", [])
    if agent in allowed:
        return rendered

    def fix(m):
        tools = [t.strip() for t in m.group(1).split(",")]
        tools = [t for t in tools if t not in ("WebSearch", "WebFetch")]
        return "tools: " + ", ".join(tools)

    return re.sub(r"^tools:\s*(.+)$", fix, rendered, count=1, flags=re.MULTILINE)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--task", required=True)
    p.add_argument("--run-tag", required=True)
    args = p.parse_args()

    task_dir = REPO / "tasks" / args.task
    cfg = yaml.safe_load((task_dir / "task.yml").read_text())
    variables = build_vars(cfg, args.run_tag)

    resolved = REPO / "campaigns" / args.run_tag / ".resolved"
    (resolved / "prompts").mkdir(parents=True, exist_ok=True)
    agents_dir = REPO / ".claude" / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)

    for agent in AGENTS:
        skeleton = (REPO / "kernel" / "agent-skeletons" / f"{agent}.md").read_text()
        prompt_file = task_dir / "prompts" / f"{agent}.md"
        sections = parse_sections(prompt_file.read_text()) if prompt_file.exists() else {}

        rendered = SECTION_REF_RE.sub(lambda m: sections.get(m.group(1), ""), skeleton)

        unknown = [v for v in VAR_RE.findall(rendered) if v not in variables]
        if unknown:
            sys.exit(f"{agent}.md: unknown variables {unknown}")
        rendered = VAR_RE.sub(lambda m: str(variables[m.group(1)]), rendered)
        rendered = re.sub(r"\n{3,}", "\n\n", rendered)  # collapse holes from empty sections
        rendered = strip_web_tools(rendered, agent, cfg)

        (agents_dir / f"{agent}.md").write_text(rendered)
        (resolved / "prompts" / f"{agent}.md").write_text(rendered)

    for src in [task_dir / "task.yml", task_dir / "task-contract.md", REPO / "protocol-core.md"]:
        shutil.copy(src, resolved / src.name)

    print(f"compiled task '{args.task}' for run '{args.run_tag}'")
    print(f"  agents   -> {agents_dir.relative_to(REPO)}/")
    print(f"  resolved -> {resolved.relative_to(REPO)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
