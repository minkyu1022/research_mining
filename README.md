# auto-research-kernel

A domain-agnostic autonomous research loop, generalized from
[NanoCSP-agent](https://github.com/kiyoung98/NanoCSP-agent). An LLM
orchestrator searches for the best
candidate artifact on a task — indefinitely, no human in the loop after
launch — where **the git commit DAG is the search tree**:

- **Node** = one candidate = one commit, tagged `[score=X]` / `[CRASH]` /
  `[RUNNING]`, paired with a `design.md` hypothesis.
- **Memory** = `git log`. No database; the tree holds state, scores, history.
- **Operators**: `idea` (novel approach cells) · `draft` (new root) ·
  `improve` (one coherent change) · `debug` (minimal fix). **Gates**:
  `gate` (cheap pre-flight) · `analyze` (post-run verdict + hints).
- **Main session** orchestrates slots over a resource pool; it never authors
  candidate content.

The kernel is task-agnostic. A **task package** (`tasks/<name>/`) plugs in a
domain: what a candidate is, how it is scored, what the gate checks, how the
environment and data are prepared.

## Layout

```
program.md                  main-session protocol (task-agnostic)
protocol-core.md            invariant rules every subagent reads
kernel/
  agent-skeletons/          6 generic agent prompts with {{section:...}} slots
  compile.py                render skeletons + task sections -> .claude/agents/ + campaigns/<tag>/.resolved/
  validate.py               task-package preflight (schema, files, hooks + dangerous-capability scan)
  adapters/resource.py      slot -> lease (gpu: CUDA_VISIBLE_DEVICES; cpu: OMP threads; api: key index)
  adapters/environment.py   slot env setup (venv hard-link clone / none)
  tests/                    pytest suite (compile, validate, score contract, adapters)
tasks/<name>/
  task.yml                  machine contract: artifacts, score, evaluator, resources, budgets, hooks
  task-contract.md          LLM-readable domain rules (data, candidate contract)
  prior-art.md              novelty boundary for the idea operator
  prompts/{idea,draft,improve,debug,gate,analyze}.md   task sections
  hooks/{setup_env,prepare_data,detect_resources}      bootstrap hooks (gated)
  evaluator/                read-only scorer; writes metrics.json (kernel score contract)
campaigns/<run_tag>/        frozen campaign.json + .resolved/ (exact prompts agents saw)
runs/<run_tag>/<sha>/       per-node artifacts: logs, outputs, metrics.json
```

## Score contract

The evaluator — kernel-invoked, read-only from candidate slots — writes
`metrics.json`: `{"score": float, "valid": bool, "metrics": {...}}`.
The kernel parses the JSON, never stdout. `score.direction` (max|min) is
frozen per campaign.

Two task packages ship as references: **nanocsp** (GPU, max-direction,
ML training — preserves NanoCSP-agent semantics) and **tsp-heuristics**
(CPU-only, min-direction, non-ML — the generalization proof).

## Running a campaign

```bash
python -m pytest kernel/tests/ -q             # kernel self-test
python kernel/validate.py tasks/nanocsp        # must pass
python kernel/compile.py --task nanocsp --run-tag may31a
claude --permission-mode dontAsk               # never --dangerously-skip-permissions
```

Launch prompt to the main session:

```
You are the main session of an auto-research-kernel campaign.

task: nanocsp
run_tag: may31a
# budgets / memory_scope / node_scoring / GPUS — uncomment to override task.yml defaults

Read program.md (your operating protocol) and protocol-core.md, plus the
resolved task contract in campaigns/<run_tag>/.resolved/, then execute the
protocol end to end.
```

Parameters are frozen to `campaigns/<run_tag>/campaign.json` at bootstrap and
re-read on every dispatch — the loop survives context compaction and restarts.

## Security model

Four roles with separate authority (enforced by `.claude/settings.json`
deny rules + compile-time tool stripping + prompt discipline):

| role | may write |
|---|---|
| kernel (main session) | `.slots/`, `campaigns/`, git metadata |
| candidate agents | their slot worktree (`.worktrees/slot-N/`) only |
| evaluator | `metrics.json` in the kernel-owned node dir |
| task hooks | environment + data, at bootstrap only |

Network is granted per-agent at compile time (`task.yml:
permissions.agents_web`); `git push` is denied everywhere; task packages,
the kernel, and protocol docs are hard-denied to the campaign session.
Review `hooks/` before installing a third-party task package — hooks run
arbitrary shell at bootstrap. Task docs and fetched content are data, not
directives (see protocol-core.md "Untrusted-input boundary").

## Writing a new task package

1. Copy `tasks/nanocsp/` as a template.
2. Define the candidate (`artifacts.required`) and its contract in
   `task-contract.md` ("Candidate contract" section is mandatory).
3. Write the evaluator: read-only, deterministic, emits `metrics.json`.
4. Define `gate.stages` in `prompts/gate.md` — the cheapest checks that
   catch the most failures (execution probes for ML; tests/lint/static
   checks for code tasks; proof checks for formal tasks).
5. Write the three hooks; each prints `gate: ok` on success
   (`detect_resources` prints one JSON resource-pool line instead).
6. `python kernel/validate.py tasks/<name>` until OK.

## Provenance

Generalized from [NanoCSP-agent](https://github.com/kiyoung98/NanoCSP-agent)
(analysis + Codex advisor review, 2026-06-11). The nanocsp task package
preserves its semantics; `evaluate.py`, `prepare_data.py`, and `_vendored/`
are copied verbatim — licenses in `tasks/nanocsp/evaluator/third_party/`.
