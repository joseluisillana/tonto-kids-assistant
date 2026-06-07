# AI-Assisted Workflow

TONTO is both an AI product and an AI-assisted development project for the AI Expert course.

The rule is simple:

```text
AI accelerates the work. The developer owns the decisions.
```

## Tool Roles

## Codex

Use Codex for project-level work:

- implement focused code changes,
- inspect the repository,
- update documentation,
- maintain the weekly journal,
- reconcile docs after implementation,
- generate test ideas and run official checks.

Codex should follow the repo instructions in `AGENTS.md` and prefer the official scripts in `scripts/`.

Codex can execute full repository changes, but the repository workflow is tool-agnostic. Codex-specific skills may help later, but they must not become the source of truth for project rules.

## OpenCode

OpenCode is an additional interactive CLI used for implementation,
repository inspection, documentation updates, review, and test verification.

It runs on Windows through WSL2.

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

### OpenCode Configuration Reference

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

## GitHub Copilot

Use Copilot for local coding assistance:

- boilerplate,
- small refactors,
- editor completions,
- quick implementation hints.

Copilot is useful inside the editor, but architectural decisions should still be reflected in `docs/decisions.md` or specs.

## Cursor and Claude

Cursor, Claude, or other assistants may be used for implementation help, review, exploration, or drafting.

They should follow the same repository rules as Codex:

- read `AGENTS.md` and the relevant docs before changing behavior,
- keep changes narrow and aligned with the active MVP,
- use the official scripts in `scripts/`,
- promote durable decisions back into repository documentation.

## NotebookLM

Use NotebookLM to study and synthesize:

- ask how the system currently works,
- generate study notes,
- compare roadmap and implementation,
- prepare report drafts,
- identify gaps in documentation.

NotebookLM reads exported repository documentation. It does not replace the repository.

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

Avoid tool-owned prefixes such as `codex/` for project branches. Branch names should describe the work, not the assistant that helped with it.

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

```powershell
git switch main
git pull --ff-only
git worktree add ..\tonto-worktrees\week-04-phase4-raspberry-listening-indicator -b feature/week-04-phase4-raspberry-listening-indicator main
git worktree add ..\tonto-worktrees\week-04-phase4-web-listening-indicator -b feature/week-04-phase4-web-listening-indicator main
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

```powershell
git worktree list
git worktree remove ..\tonto-worktrees\<worktree-name>
git worktree prune
```

The detailed project spec for this workflow is `specs/parallel-agent-workflow.md`, with its paired plan in `docs/plans/parallel-agent-workflow.md`.

## Spec Handoff Workflow

Whenever a spec is created or materially changed, the same change should also create or update an execution plan in `docs/plans/`.

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

Execution plans should use `docs/plans/TEMPLATE-spec-implementation-plan.md` unless an existing phase-specific plan already provides the same structure. The plan should include:

- objective and source spec,
- included and excluded scope,
- implementation outline,
- acceptance criteria,
- verification commands,
- an implementation prompt ready to paste into Codex, OpenCode, or another project assistant.

Naming convention:

```text
specs/<feature-name>.md
docs/plans/<feature-name>-implementation-plan.md
```

Existing phase plans may keep their established names, for example:

```text
docs/plans/week-03-phase-3-web-loop.md
```

The prompt belongs inside the plan file by default. Create separate prompt files only if one spec truly needs multiple distinct implementation handoffs.

Codex and OpenCode should treat this as project workflow, not as a model-specific skill. GitHub Copilot can help draft implementation details, but durable decisions and prompts must live in the repository.

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
8. If the work item depends on a recently merged PR, update from `main` before editing.

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

At the end of each week:

1. Review changes made during the week.
2. Update `docs/project-journal/week-XX.md`.
3. Update specs, roadmap, architecture, or decisions only if the project actually changed.
4. Export sources for NotebookLM.
5. Ask NotebookLM for a weekly summary and missing-docs checklist.
6. Bring reviewed improvements back into the repo.

## Evidence for the Course

Keep evidence of:

- what AI tools were used for,
- what decisions were human-owned,
- what was validated by tests or hardware,
- what changed after experimentation,
- what limitations remain.

The final report should explain not only what TONTO is, but how AI helped build it responsibly.
