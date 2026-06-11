# auto-research-kernel: operator-driven tree search on the git DAG (main-session protocol)

Every node is a git commit; the commit DAG **is** the search graph. Each
campaign is tagged `<run_tag>`; its nodes live under `agent/<run_tag>/*`
branches and `git log --branches='agent/<run_tag>/*' --oneline` **is** the
per-run memory. Runs are isolated — never pull from another run's branches.

This file is operations-only and task-agnostic. Kernel rules every subagent
follows live in [`protocol-core.md`](protocol-core.md); domain rules live in
the task package (`tasks/<task>/`). Main reads all three.

## Campaign bootstrap (once, before the loop)

1. **Resolve the task package**: the launch prompt names `task` and
   `run_tag`. Run `python kernel/validate.py tasks/<task>` — abort on any
   error.
2. **Compile**: `python kernel/compile.py --task <task> --run-tag <run_tag>`
   renders agent definitions into `.claude/agents/` and writes the resolved
   config + docs to `campaigns/<run_tag>/.resolved/`. Every prompt an agent
   sees is on disk there — never improvise prompt content.
3. **Run task hooks** (each gated; abort campaign on non-zero exit):
   - `hooks/setup_env` — build the base environment (e.g. `.base-venv/`).
     Gate: the hook's own printed `gate: ok` line.
   - `hooks/prepare_data` — idempotent data preparation. Gate: same.
   - `hooks/detect_resources` — prints one JSON line describing the resource
     pool (e.g. `{"type":"gpu","units":[0,1,2],"vram_total_mb":24210}`).
     Slots = one per unit (or `resources.slots` from task.yml if fixed).
4. **Freeze params** to `campaigns/<run_tag>/campaign.json`: `{task, run_tag,
   resources, n_slots, budgets, memory_scope, node_scoring, score_direction}`.
   This file — not prompt memory — is the durable source of truth; re-read it
   on every dispatch and on recovery. Values are frozen for the campaign.
5. Verify `agent/<run_tag>/*` and `runs/<run_tag>/` don't exist
   (`mkdir -p runs/<run_tag>`); be on `agent/root`.

## Main-session discipline (non-negotiable)

- **No candidate authoring from main.** Main never writes, edits, seds, or
  heredocs any candidate artifact, evaluator, hook, protocol doc, or agent
  definition. Generators write artifacts into their slot worktree; the
  on-disk file is the source of truth. Main writes only state files
  (`.slots/*`) and git metadata. (Bootstrap steps 1–4 are the sole exception.)
- **No WebSearch / WebFetch from main.** Literature-level reasoning is
  delegated to `idea` / `draft` / `improve`. Main's decisions use only local
  state: the run-scoped `git log`, commit bodies, `metrics.json`, and logs.
- **No off-protocol candidate invocations.** Run the candidate only at the
  gate stage and the full run, with the exact frozen parameters.
- **No same-cycle retry after a gate fail.** A gate fail commits `[CRASH]`
  and frees the slot; the next attempt is a separate cycle from a fresh
  worktree.
- **Methodology preservation in debug.** Debug keeps the target's approach
  cell intact; approach swaps belong to `draft` / `improve`.
- **Only the 6 subagents** (`idea` / `draft` / `improve` / `debug` / `gate` /
  `analyze`) are dispatched. Commit subject prefix = authoring operator name,
  set by main.
- **No batched cross-cycle fixes.** One idle slot = one operator dispatch per
  cycle.

## State model

| concept | git / fs equivalent |
|---|---|
| node id | commit short SHA |
| parent | git parent (`%P`) |
| operator | commit subject prefix (`draft:` / `improve:` / `debug:`) |
| status | `[score=X]` or `[CRASH]` in subject |
| score | `runs/<run_tag>/<sha>/metrics.json` (subject tag is display) |
| lineage | branch `agent/<run_tag>/n<i>-<op>` |
| per-run memory | `git log --branches='agent/<run_tag>/*' --oneline` |
| campaign params | `campaigns/<run_tag>/campaign.json` (frozen; re-read every dispatch) |
| node artifacts | `runs/<run_tag>/<sha>/` (logs, outputs, metrics.json, slot env) |
| slot N idle | `.worktrees/slot-N/` does not exist |
| slot N busy | `.worktrees/slot-N/` exists (any phase) |
| run events | `.slots/events.log` lines `slot=$N exit=$?` |

## Commit message format

Subject (≤ 72 chars): `<op>: <one-line plan> [score=<float>]` or `[CRASH]`;
in-flight placeholder: `<op>: <strategy> [RUNNING]` (empty commit, body holds
`cell:` + `parent:`), amended in place into the final node on finish.

Body fields: `cell:` (approach pair, inherited verbatim down the lineage),
scalar metrics, `parent:` (improve/debug), `verdict: ok|buggy`,
`analyze_summary:`, `analyze_hints:` bullets. Crash variant replaces scalars
with `error_tail:`; soft-fail keeps the score line annotated
`# uninformative per analyze`.

## Operator selection

On an idle slot:

1. Read `git log --branches='agent/<run_tag>/*' --oneline` — committed and
   `[RUNNING]` nodes in one query.
2. Choose operator + parent/target:
   - **idea** — when filling a DRAFT slot: dispatched with `{run_tag,
     n_cells}`; fetches the exclusion list itself (run-scoped git log) and
     the task's `prior-art.md` novelty boundary; returns N diverse approach
     cells. Main never hand-picks cells.
   - **draft** (`parent_sha: null`) — instantiates a fresh candidate from an
     idea-supplied cell, written with `Write`.
   - **improve** (`parent_sha` = a `[score=]` node) — ONE coherent change,
     applied surgically with `Edit` so the diff is the change.
   - **debug** (`target_sha` = a `[CRASH]` leaf) — minimal,
     methodology-preserving fix.
3. Compose a ≤ 30-word `strategy`; it is recorded by the slot's `[RUNNING]`
   commit — no separate file.

**Selection policy** (judgment-based): read lineages' `analyze_hints` —
tuning-class hints favor more attempts on the approach; methodology-class
hints disfavor it. Trajectory shape beats absolute score. Engineering crashes
route to `debug` first. **Anti-crowding**: don't crowd the top-1; spread
across promising lineages — its `[RUNNING]` children show current crowding.
`node_scoring` (`none`/`greedy`/`uct`, frozen in campaign.json) is an
advisory ranking aid, computed live from the commit tree; it never overrides
judgment, and LLM ranking never overrides evaluator truth.

**memory_scope** (frozen) controls how much cross-node memory `improve`
sees: `global` / `ancestry` / `siblings` / `ancestry+siblings` / `none`.
`idea`+`draft` always global, `debug` always ancestry, main always global.

## Per-slot pipeline

Notation: `$N` slot index, `$LEASE` the slot's resource lease (e.g. physical
GPU id), `$BRANCH=agent/<tag>/n<i>-<op>`, `$WT=.worktrees/slot-$N/`,
`$REPO` repo root. Pipelines are sequential within a slot, interleaved
across slots.

1. **Compose strategy + manifest.** Every manifest carries `run_tag`, the
   resource lease fields, and the frozen budgets — all read from
   `campaign.json`. Generator manifests: `operator`, `slot`, lease,
   `parent_sha`/`target_sha`, `strategy`, `memory_scope` (improve), `cwd`,
   env interpreter path, `fetch_hints` (run-scoped).
2. **Worktree + env.** `git worktree add -b $BRANCH $WT <parent_ref>`
   (parent ref = `parent_sha` or `agent/root`). Link data per task hooks'
   layout. Slot env: environment adapter — for `environment.kind: venv`,
   hard-link clone parent's env (`cp -al`) else the base env. Then the
   `[RUNNING]` empty commit (strategy + cell + parent).
3. **Dispatch generator** (`draft`|`improve`|`debug`) with the manifest.
   Parallel Agent calls when multiple slots are idle.
4. **Verify writes**: every `artifacts.required` file exists non-empty in
   `$WT`, else abort the cycle.
5. **Dispatch gate.** The gate runs the task's `gate.stages` (from the
   resolved gate definition) within `budgets.gate_seconds`. Output contract:
   `verdict: pass|fail`, `summary:`, `checks:` bullets.
   - pass → step 6. fail → consolidate gate artifacts into staging, set
     `status=crash`, skip step 6, jump to steps 7–10. No same-cycle retry.
6. **Launch full run in background** under the slot's lease (e.g.
   `CUDA_VISIBLE_DEVICES=$LEASE`), `timeout` at the frozen OS cap, stdout to
   `$WT/runs/staging/run.log`, then `echo "slot=$N exit=$?" >>
   .slots/events.log`. Main does not wait — back to the event loop.
7. **On event**: run the evaluator if the task separates it from the
   candidate run (per task.yml `evaluator.command`, kernel-invoked, writes
   `runs/staging/metrics.json` in `$WT`). Parse `metrics.json`:
   exit 0 + `valid:true` + score present → `status=ok`; else `status=crash`,
   `error_tail` = last log line.
8. **Dispatch analyze** with status + scalars + fetch_hints (artifact, logs).
   Returns `verdict: ok|buggy`, `summary`, `hints`. `buggy` ⇒ `[CRASH]` tag
   (soft-fail demotion).
9. **Amend commit** in `$WT`: `git add` the artifact set, `git commit
   --amend` replacing the `[RUNNING]` placeholder with the final subject +
   body (formats above).
10. **Finalize**: `mv $WT/runs/staging $REPO/runs/<run_tag>/$SHA`,
    `git worktree remove $WT` → slot idle → immediately dispatch the next
    candidate.

## Initial launch / refill / event loop

- **Initial launch**: one `idea` call (`n_cells` = slot count) → step 2 per
  slot → all `draft` dispatches in one parallel Agent message → verify →
  parallel `gate` dispatches → launch passers in background → start a
  persistent Monitor on `.slots/events.log`.
- **DRAFT refill**: `idea` with `n_cells: 1`, then steps 2–10.
- **Event loop**: for each `slot=$N exit=$code` line → steps 7–10 → steps
  1–6 for slot N. Process events one at a time; `analyze` calls may be
  batched in parallel. Never stop unless the user interrupts.

**Recovery** (main restarted): restore params from
`campaigns/*/campaign.json` first. For each existing `.worktrees/slot-$N/`:
live process (`pgrep -f .worktrees/slot-$N`) → wait for its event; no live
process → `git worktree remove --force`, delete the unfinished `[RUNNING]`
branch, slot idle.
