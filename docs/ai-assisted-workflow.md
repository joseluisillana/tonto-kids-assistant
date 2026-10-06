# AI-Assisted Workflow

TONTO is both an AI product and an AI-assisted development project for the AI
Expert course. AI accelerates the work; the developer owns the decisions.

This is the canonical detailed operating procedure for all agents and humans.
The [ai/ process](../ai/README.md) owns planning/tracking for new and migrated
records; this document retains environment, Git, approvals and operation.
Read it before any edit, formatter, generator or command that writes repository
files. Start with [root instructions](../AGENTS.md), then read the applicable
local AGENTS.md files and the sections triggered by the task below. No provider,
model, IDE, extension, CLI of an agent, plugin or MCP is required to follow it.

## Agent roles

Development agents may perform focused implementation, repository inspection,
documentation updates, weekly journal maintenance, reconciliation after
implementation, review, exploration, drafting, test ideas and official checks.
Editor assistants can also help with boilerplate, small refactors, completions
and implementation hints. All follow the same project rules, keep changes narrow
and promote durable decisions back into repository documentation. Architecture
decisions belong in decisions/specs, independent of which assistant helped.
Project-level changes are allowed under the same workflow; tool-specific assets
never become the source of truth for project rules.

## Agent Capability Pack

The Week 05 Agent Capability Pack is the portable command surface for AI-assisted agents and humans when operating backend and Raspberry validation tasks.

Its source of truth is repository-owned Markdown and Bash scripts:

- `specs/week-05-agent-capability-pack.md`
- `docs/plans/week-05-agent-capability-pack.md`
- `scripts/agent-backend.sh`
- `scripts/agent-raspberry.sh`
- `docs/raspberry-pi-setup.md`

Tool-specific wrappers, Codex skills, OpenCode prompts, plugins, or MCP tools may be added later, but they must delegate to this repo-owned pack. They should not become the canonical workflow.

Use the pack when an agent needs to:

- start, stop, status-check, or health-check the backend for validation,
- run a Raspberry preflight over SSH,
- execute a narrow command inside the Raspberry repo for evidence capture,
- launch the Raspberry touch UI client (`./scripts/agent-raspberry.sh exec "./scripts/demo-touch.sh"`).

The pack deliberately does not automate passwords, store secrets, replace human voice demo validation, or change product behavior. Machine-specific values belong in local environment variables such as `TONTO_PI_HOST`, `TONTO_PI_USER`, `TONTO_PI_SSH_KEY`, `TONTO_PI_REPO`, and `TONTO_BACKEND_URL`.

## Repo-Local Agent Skills

TONTO may include repo-local Agent Skills under:

```text
.agents/skills/<skill-name>/SKILL.md
```

These skills follow the portable Agent Skills pattern: a folder with `SKILL.md` frontmatter (`name`, `description`) and optional `references/`, `scripts/`, or `assets/` resources. Skills-compatible agents can discover them from the repository and load them when the task matches the description.

Repo-local skills are useful for agent operating knowledge, but they do not replace project specs, plans, or durable decisions. Canonical behavior lives in registered definitions/plans and implementation: ai/ for new/migrated records, specs/ and docs/plans/ for unmigrated history.

Use `.agents/skills/devexpert-inference/SKILL.md` when working with:

- DevExpert Inference documentation,
- the `https://inference.devexpert.io/v1` OpenAI-compatible gateway,
- TONTO inference provider selection,
- DevExpert chat, STT, TTS, embeddings, or model configuration,
- the extra MVP line in `specs/inference-providers.md`.

When an inference change touches provider behavior, agents must preserve both OpenAI and DevExpert support through focused tests or documented validation.
Apply [D025](decisions.md#d025---devexpert-deprecado-para-la-validación-post-migración)
before using any provider operating instructions: preserve both adapters with
mock tests; do not request credentials, run a real DevExpert smoke or reactivate
it without a new operator decision. Historical model defaults are not a live
availability guarantee. Read SKILL.md and its public resources directly if your
agent does not support skill discovery; no loader is required.
Do not make DevExpert skill contents the only source of truth; keep the provider
specs and plan updated when behavior, contracts, or validation requirements change.

Use `.agents/skills/raspberry-voice-demo/SKILL.md` when operating live TONTO voice turns through the Raspberry client, including:

- starting or checking the backend with official scripts,
- running Raspberry SSH preflight,
- launching the Raspberry voice client,
- coordinating spoken `espeak` prompts so the operator knows when to ask questions,
- optionally starting the web validation client if requested.

The Raspberry voice demo skill is for operation only. It must not create product features, replace the demo runbook/checklist, or change repository behavior unless the user explicitly asks for documentation updates.

## NotebookLM

Use NotebookLM to study and synthesize:

- ask how the system currently works,
- generate study notes,
- compare roadmap and implementation,
- prepare report drafts,
- identify gaps in documentation.

NotebookLM reads exported repository documentation. It does not replace the repository.

## Development environment

- Linux + Docker + Bash is the active development workflow. Do not add Windows
  shell runtime paths or restore removed platform scripts. Keep historical
  migration evidence as history, not as operating instructions.

- Treat the host machine as clean. Do not install Python packages globally.
- Use the official Bash scripts in `scripts/` or `tonto.sh` before inventing ad hoc setup, dev, test, or build commands.
- Python dependencies must be installed into the repo-local `.venv/`.
- Use `.venv/bin/python` when a direct Python command is unavoidable.
- Run Python tests through `./tonto.sh test python` or the `.venv` Python executable, never through a global `pytest`.
- Frontend dependencies must stay local to `web/node_modules/`.
- Use `npm ci` or `npm install` only inside `web/`; never use `npm install -g` unless the user explicitly approves it.
- Keep dependency caches local to `.cache/` when scripts support it; do not rely on user-profile caches such as global pip/npm caches.
- If agent sandboxing blocks network access or writes inside `.venv/`, `web/node_modules/`, or `.cache/`, request escalation for the official script command instead of switching to global tools.
- If the build, test, setup, or dev workflow changes, update the scripts and documentation in the same change.
- CI, humans, and agents should share the same command surface whenever practical:
  - `./tonto.sh setup`
  - `./tonto.sh dev [backend|web|all]`
  - `./tonto.sh test [python|web|all]`
  - `./tonto.sh build [web|all]`

Python execution for project code must stay inside the repository virtual environment:

- Linux backend, tests, and setup use the official Docker commands through `./tonto.sh`.
- Raspberry client/demo commands use `.venv/bin/python`.
- Host `python` or `python3` may be used only to create the virtual environment or to verify that the system Python exists.
- Agents should not run project modules with bare `python`, `python3`, `pip`, or `pytest`.

Scope clarification from the Linux/Docker scripts: the normal host command
surface uses the Docker-managed backend-venv volume at /app/.venv. The host
.venv is optional IDE/direct-Python support via ./tonto.sh setup host; Raspberry
uses its own repo-local .venv. Keep these separate. The setup/test/build task
model excludes runtime credentials; do not introduce them into those tasks.
Use ./tonto.sh test ui for Kivy and test all for Python + Kivy + web. Build all
currently builds web. Read tonto.sh, docker-compose.tasks.yml and CI before
assuming command coverage. There are no public lint/format targets to invent.


## Coding and simplicity rules

- Keep code small, direct, and easy to inspect.
- Prefer plain Python and FastAPI patterns already present in the repo.
- Keep the backend as a lightweight monolith for the MVP.
- Do not add or restore Go CI checks until Go is explicitly selected for an active backend implementation.
- Keep the Raspberry client as a simple Python process.
- Use typed data structures where they clarify request/response contracts.
- Use clear names over clever abstractions.
- Handle obvious failure cases, especially backend timeouts and unavailable TTS.
- Add or update focused tests when changing behavior.
- Do not silently change architecture or milestone scope.
- Do not rewrite unrelated files.
- Do not implement future-scope features unless the user explicitly asks.

### Simplicity rules

- Start with the simplest end-to-end path that can work.
- Prefer one endpoint before multiple endpoints.
- Prefer one client loop before a framework or plugin system.
- Prefer in-memory data before storage.
- Prefer direct function calls before event buses, queues, or background workers.
- Prefer explicit configuration before dynamic discovery.
- Prefer readable scripts before complex automation.

### Do not overengineer

Avoid introducing:

- microservices,
- message brokers,
- databases,
- ORMs,
- auth frameworks,
- plugin systems,
- background job systems,
- observability stacks,
- container orchestration,
- complex dependency injection,
- premature hardware abstractions,
- production deployment machinery.

These may become useful later, but they are not part of the current MVP milestone.

## Approval boundaries

Ask the user before introducing any new runtime or development dependency.

When proposing a dependency, explain:

- why it is needed now,
- what simpler option was considered,
- where it will be used,
- whether it affects Raspberry Pi setup.

Do not add packages just for convenience.

Ask before changing architecture. Preserve existing authorization from the operator; do not silently change milestone scope.


## Decisions and conflicts

Read the existing repo context before making changes. Respect the current
milestone and keep scope narrow. If a request conflicts with repository
instructions, follow the user's latest explicit instruction and update the
relevant docs when the decision is persistent. When unsure, choose the smallest
reversible change that advances the MVP.

If implementation and documentation disagree, pause the affected decision and
make it explicit before continuing. Code is evidence, not permission to change a
rule. Local instructions complement ancestors and do not relax global rules.
Apply recorded current decisions to historical guidance; neither a deeper path
nor a newer file modification date is sufficient to resolve a conflict. Session
instructions and execution-environment permissions keep their own precedence.

The root instructions intentionally do not track the active sprint or phase.
Read roadmap, specs and the newest dated entry in project-journal before choosing
or executing work; consult the affected contracts/plans. Preserve historical MVP
limits while applying explicitly approved post-MVP work through its own spec.


## Git and PR Workflow

Use a lightweight GitHub Flow with trunk-based principles:

1. Start from `main`.
2. Create a short-lived branch for one focused change.
3. Keep implementation, tests, and documentation together when they describe the same change.
4. Open a small PR back to `main`.
5. Merge only after the change is reviewed and the relevant checks or manual validations are clear.

This is the project default because it matches common small-team practice: `main` is the integration branch, PR branches are temporary review/check units, and each PR should be small enough to understand and revert.

Branch names use:

```text
<type>/<short-kebab-description>
```

Initial branch types:

- `feature/` for new user-visible or workflow capability,
- `fix/` for bug fixes,
- `docs/` for documentation-only changes,
- `chore/` for maintenance, automation, or internal cleanup,
- `experiment/` for exploratory work that may not merge.

Examples:

```text
feature/notebooklm-combined-export
fix/backend-timeout-handling
docs/formalize-ai-git-workflow
chore/update-test-script
experiment/local-stt-spike
```

Avoid tool-owned prefixes such as `codex/` for project branches unless the
developer explicitly requests one. Branch names should describe the work, not
the assistant that helped with it. Each coherent work item uses one branch and
one focused PR, kept short-lived; related code, tests and documentation stay together.

## Parallel Agent Workflow

When multiple agents or work items run at the same time, isolate them with Git worktrees.

The rule is:

```text
one coherent work item -> one branch -> one worktree when parallel -> one PR
```

A work item is a change that can be planned, implemented, verified, reviewed, and merged independently. It can include code, tests, docs, and specs when they describe the same behavior.

Good work items:

- `feature/week-04-phase4-raspberry-listening-indicator`
- `feature/week-04-phase4-web-listening-indicator`
- `docs/parallel-agent-workflow`

Too broad:

- `feature/week-04-everything`
- `docs/update-all-docs`
- one branch shared by two agents editing unrelated areas.

Use a separate worktree whenever two agents could otherwise edit the same checkout:

```bash
git switch main
git pull --ff-only
git worktree add ../tonto-worktrees/week-04-phase4-raspberry-listening-indicator -b feature/week-04-phase4-raspberry-listening-indicator main
git worktree add ../tonto-worktrees/week-04-phase4-web-listening-indicator -b feature/week-04-phase4-web-listening-indicator main
git worktree list
```

Rules for parallel agents:

- Do not run parallel agents in the same working tree.
- Do not let two agents edit the same branch at the same time.
- Do not edit on `main` unless the developer explicitly asks for it.
- Keep each branch short-lived and focused.
- Push and open a PR for each work item.
- Merge parallel PRs one at a time.
- After one parallel PR merges, update the remaining branches from `main` and reconcile docs or journal changes before merging the next PR.
- Delete merged branches and remove stale worktrees.

Cleanup commands:

```bash
git worktree list
git worktree remove ../tonto-worktrees/<worktree-name>
git worktree prune
```

The detailed project spec for this workflow is `specs/parallel-agent-workflow.md`, with its paired plan in `docs/plans/parallel-agent-workflow.md`.

## GitHub CLI and Issues

### Secret-safe diagnostics (#110)

Never read credential files for diagnosis or capture shell traces. Use official helpers with bounded output.

Keep the existing `.env` and automated backend/SSH workflow. Do not capture
expanded Compose configuration, environment dumps, raw provider errors or
credential files for diagnosis. Cleanup uses metadata with env-file resolution
and interpolation disabled and reports only operation/exit code. Provider
errors expose fixed messages and upstream HTTP status, never response bodies
or exception reasons/chains. These controls reduce accidental exposure; they
do not deny deliberate filesystem/Docker access. See
`specs/agent-secrets-protection.md` and its paired plan.

Provider failures also emit WARNING JSON events through standard logging:
provider, chat/stt operation, bounded failure category and optional HTTP status.
No raw exceptions, payloads, URLs, credentials, conversations or audio are
passed to the logger. No dedicated log files or new dependencies are introduced.

Use `git` for local repository operations:

- `git status --short --branch`
- `git diff`
- `git switch`
- `git worktree`
- `git add`
- `git commit`
- `git log`

Prefer GitHub CLI (`gh`) for GitHub operations:

- `gh pr create`
- `gh pr view`
- `gh pr checks`
- `gh pr merge`
- `gh issue create`
- `gh issue view`
- `gh issue list`
- `gh issue edit`

If `gh` is unavailable, unauthenticated, or blocked by sandbox/network restrictions, report that clearly and use the safest fallback only when it still preserves the workflow.

Use GitHub Issues when a work item needs coordination beyond one immediate PR:

- each active implementation phase,
- each parallel work item with its own branch/worktree,
- Raspberry or browser validation tasks,
- known demo risks,
- follow-up decisions that should not live only in chat.

Do not create issues for every tiny edit. Prefer an issue when tracking improves coordination, evidence, or handoff quality.

When an issue exists, reference it from the PR body to maintain tracking. Use GitHub closing keywords (e.g., `Closes #XYZ`) ONLY for the specific Phase/Child issue that the PR fully completes. NEVER use closing keywords for a Parent/Epic issue unless all child issues and any other un-tracked tasks within the parent are fully completed. To link a PR to a Parent issue without closing it, use phrasing like `Part of #XYZ` or just mention the issue number.

## Spec Handoff Workflow

The [ai/ process](../ai/README.md) owns planning, lifecycles, journals, indexes
and work without a registered record. New definitions use ai/specs/ or ai/issues/
and their own plan.md/journal.md. Read all three files before acting. Existing
legacy definitions and GitHub issues count as registered work and retain their
locations until migration; do not create duplicates. Historical plans/prompts
remain valid. Scope, handoff, verification and isolation requirements below
still apply; legacy naming/template paths apply only to unmigrated records.


Always update affected definitions and docs when decisions change. Use
docs/architecture.md for architecture decisions, docs/roadmap.md for milestone/scope,
ai/ for new/migrated records, docs/specs.md and specs/ for unmigrated history,
and README.md only for high-level orientation
and setup. Include related docs/specs in the same change as behavior,
architecture, setup, scope or workflow changes. Repo-local skills provide
portable operating guidance, not canonical specs, plans or durable decisions.
Read [documentation workflow](documentation-workflow.md) when updating docs,
journal or exports; it owns the documentation routine and evidence details.


Whenever a spec is created or materially changed, the same change must create
or update its execution plan: plan.md beside new/migrated definitions, or the
existing paired docs/plans/ plan for unmigrated records.

A material spec change is any change to:

- behavior,
- milestone scope,
- public API or request/response contract,
- architecture,
- validation workflow,
- acceptance criteria.

Purely editorial changes can skip a new execution plan, but the change summary should say that no implementation behavior changed.

The expected flow is:

```text
spec -> execution plan -> implementation prompt -> implementation -> validation evidence
```

New/migrated plans use the corresponding ai/ template. Unmigrated plans use `docs/plans/TEMPLATE-spec-implementation-plan.md` unless an existing phase-specific plan already provides the same structure. The plan should include:

- objective and source spec,
- included and excluded scope,
- implementation outline,
- acceptance criteria,
- verification commands,
- an implementation prompt ready to paste into Codex, OpenCode, or another project assistant.

Every plan also states branch name, whether a dedicated worktree is required,
whether it can run in parallel, collision risks and integration order if related
work merges first. Purely editorial changes may omit a plan update only when the
summary explicitly states that no implementation behavior changed.

Legacy naming convention (new records follow ai/):

```text
specs/<feature-name>.md
docs/plans/<feature-name>-implementation-plan.md
```

Existing phase plans may keep their established names, for example:

```text
docs/plans/week-03-phase-3-web-loop.md
```

The prompt belongs inside the plan file by default. Create separate prompt files only if one spec truly needs multiple distinct implementation handoffs.

All agents should treat this as project workflow, not as a model-specific skill. Editor assistants can help draft implementation details, but durable decisions and prompts must live in the repository.

## Pre-Edit Gate for AI Assistants

Before any repository edit, AI assistants must verify the Git context and align with the project branch workflow.

Minimum required gate:

1. Run `git branch --show-current` and `git status --short --branch`.
2. If the current branch is `main`, do not edit files yet. First create or switch to a project branch using `<type>/<short-kebab-description>`, unless the developer explicitly says to work on `main`.
3. Use `docs/` for documentation-only work, `fix/` for bug fixes, `feature/` for new behavior, `chore/` for maintenance, and `experiment/` for exploratory work.
4. Do not use tool-owned prefixes such as `codex/` unless the developer explicitly asks for them.
5. If `main` has uncommitted changes, stop and ask before moving, stashing, committing, discarding, or editing those changes.
6. Apply the same gate before running formatters, generators, export scripts, or other commands that write repository files.
7. For parallel work, confirm the current checkout is the dedicated worktree for this work item.
8. If a related PR merges while this work item is active, update from `main`
   and reconcile conflicts before continuing, including documentation changes.

## Commit Messages

Use Conventional Commits for human and AI-assisted changes:

```text
<type>: <short imperative summary>
```

Common commit types:

- `feat:` for new capability,
- `fix:` for bug fixes,
- `docs:` for documentation-only changes,
- `chore:` for maintenance or automation,
- `test:` for test-only changes,
- `refactor:` for behavior-preserving code changes.

Examples:

```text
feat: add combined NotebookLM export
fix: handle Raspberry backend timeouts
docs: formalize AI-assisted Git workflow
chore: update local test automation
```

PRs should include:

- what changed,
- why it changed,
- which docs/specs were updated,
- which checks, scripts, or hardware validations were run.

## Weekly Routine

At week end, follow [Update Routine](documentation-workflow.md#update-routine)
and [Work Item Evidence](documentation-workflow.md#work-item-evidence): review
the week's work, update its journal, update specs/roadmap/architecture/decisions
only if the project changed, export sources, ask NotebookLM for a weekly summary
and missing-docs checklist, and bring reviewed improvements back into the repo.
NotebookLM remains optional synthesis of exported sources, never final truth.

## Evidence for the Course

Keep evidence of:

- what AI tools were used for,
- what decisions were human-owned,
- what was validated by tests or hardware,
- what changed after experimentation,
- what limitations remain.

The final report should explain not only what TONTO is, but how AI helped build it responsibly.

## Historical tool context

The following records earlier course tooling and local machine configuration,
not requirements for a development agent or active operating instructions.
Codex was the primary assistant; OpenCode was an additional project-level tool.
Copilot supported editor tasks; Cursor, Claude and other assistants supported
implementation, review, exploration and drafting under the same rules. These
roles are preserved by the neutral Agent roles section above.

Linux/Docker/Bash is now the active workflow. Do not restore removed Windows
runtime scripts. D025 deprecates DevExpert operation: no credentials or real
smoke without a new operator decision. The Windows path, models and access
window below are historical references, not current availability claims.

### OpenCode (historical)

OpenCode is an additional interactive CLI used for implementation,
repository inspection, documentation updates, review, and test verification.

It runs in Linux (including WSL2 when applicable).

- **Provider**: DevExpert (OpenAI-compatible API).
- **Base URL**: `https://inference.devexpert.io/v1`.
- **Recommended model**: `deepseek-v4-flash`.
- **Alternative model**: `deepseek-v4-pro`.
- **Access note**: course access is active for 60 days and has a weekly limit to avoid accidental usage spikes.

Codex remains the primary project assistant. OpenCode is part of the same AI-assisted tool stack and can also be used for project-level work:

- implement focused code changes,
- inspect the repository,
- update documentation,
- maintain the weekly journal,
- reconcile docs after implementation,
- generate test ideas and run official checks.

OpenCode should follow the repo instructions in `AGENTS.md` and prefer the official scripts in `scripts/`, as Codex does.

OpenCode can execute full repository changes when used for that work, but the repository workflow is tool-agnostic and may include more compatible tools over time.

### OpenCode Configuration Reference (historical)

If OpenCode needs to be reconfigured on the Windows/WSL2 development machine, the local configuration file is expected at:

```text
C:\Users\[Usuario]\.config\opencode\opencode.jsonc
```

This file is local machine configuration, not repository configuration. Never commit a real API key. Keep `apiKey` masked in documentation and examples:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "model": "DevExpert/deepseek-v4-flash",
  "provider": {
    "DevExpert": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "DevExpert",
      "options": {
        "baseURL": "https://inference.devexpert.io/v1",
        "apiKey": "xxxxxxxxx"
      },
      "models": {
        "deepseek-v4-flash": {
          "name": "DevExpert deepseek-v4-flash",
          "limit": {
            "context": 200000,
            "output": 65536
          }
        },
        "deepseek-v4-pro": {
          "name": "DevExpert deepseek-v4-pro",
          "limit": {
            "context": 200000,
            "output": 65536
          }
        }
      }
    }
  }
}
```



The former root Tool Environment described Windows/WSL2 use with this provider
and these same recommended/alternative models. That history is consolidated here;
the common scripts, local dependencies, branches and scope rules now apply to all
agents through the canonical sections above.
