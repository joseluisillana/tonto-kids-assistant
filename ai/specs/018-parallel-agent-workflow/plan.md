# Parallel Agent Workflow Implementation Plan

## Objective

Implement the repository documentation changes required by `ai/specs/018-parallel-agent-workflow/spec.md` so TONTO has clear, standard rules for isolated parallel AI-assisted development.

## Source Spec

- Spec: `ai/specs/018-parallel-agent-workflow/spec.md`
- Related docs:
  - `AGENTS.md`
  - `docs/ai-assisted-workflow.md`
  - `docs/documentation-workflow.md`
  - `ai/specs/_template/plan.md`
  - `docs/decisions.md`
  - `ai/specs/020-raspberry-listening-indicator/plan.md`
  - `ai/specs/024-web-listening-indicator/plan.md`

## Scope

Included:

- Documentation-only workflow update.
- Formal rules for one work item per branch/PR.
- Formal rules for one worktree per parallel agent/work item.
- Formal rules for using GitHub Issues to track phases, parallel tasks, validation, and multi-session work.
- Formal rules for using `gh` as the preferred tool for GitHub PR/check/issue operations.
- References to standard GitHub Flow, trunk-based development, small changes, and Git worktrees.
- Updates to existing Phase 4 indicator plans so they can be launched safely in parallel.

Excluded:

- Code behavior changes.
- New dependencies.
- New Git hooks or automation scripts.
- Branch protection changes in GitHub settings.
- Changes to the product architecture.

## Implementation Plan

1. Add `ai/specs/018-parallel-agent-workflow/spec.md`.
2. Add this paired plan in `ai/specs/018-parallel-agent-workflow/plan.md`.
3. Update `docs/ai-assisted-workflow.md`:
   - keep GitHub Flow as the base,
   - add isolated work item rules,
   - add worktree rules for parallel agents,
   - add merge/reconciliation guidance for parallel PRs.
4. Update `AGENTS.md` with mandatory agent rules:
   - do not edit on `main`,
   - do not share worktrees for parallel work,
   - one branch/PR per coherent work item,
   - update from `main` after related PRs merge.
5. Update `docs/documentation-workflow.md` with evidence expectations for each work item.
6. Update `ai/specs/_template/plan.md` with a `Workflow Isolation` section.
7. Update existing Raspberry and web indicator plans to state they should run in separate branches/worktrees.
8. Add GitHub CLI guidance:
   - `git` remains the default for local repo state and content changes.
   - `gh` is preferred for PRs, checks, merges, issues, and GitHub metadata.
9. Add issue-tracking guidance for work items that span phases, parallel branches, hardware validation, or multiple sessions.
10. Record the durable process decision in `docs/decisions.md`.

## Acceptance Criteria

- The repository has a spec and plan for parallel agent workflow isolation.
- Agent-facing rules are present in `AGENTS.md`.
- Human-facing workflow guidance is present in `docs/ai-assisted-workflow.md`.
- Documentation evidence expectations are present in `docs/documentation-workflow.md`.
- Future plans have a place to state whether they are parallelizable.
- Future plans can state whether a GitHub Issue should track the work.
- Agents are told to prefer `gh` for GitHub PR/check/issue operations.
- Raspberry and web listening indicator plans explicitly use separate branches/worktrees.
- No code behavior changes are made.

## Verification

For this documentation-only workflow change:

```bash
git diff --check
git status --short --branch
```

No Python or web tests are required because no product code changes.

## Implementation Prompt

```text
Implement the spec in specs/parallel-agent-workflow.md.

Before editing:
- Read AGENTS.md.
- Read docs/ai-assisted-workflow.md.
- Read specs/parallel-agent-workflow.md.
- Read docs/plans/parallel-agent-workflow.md.
- Run git branch --show-current and git status --short --branch.
- If on main, create or switch to a docs branch before editing.
- Preserve unrelated user changes.

Task:
- Update repository workflow documentation so every coherent work item uses its own branch and PR.
- Add explicit Git worktree isolation rules for parallel agents.
- Add explicit GitHub Issue tracking rules for phases, parallel tasks, validation, and multi-session work.
- Add explicit `gh` usage guidance for GitHub PR/check/issue operations.
- Keep GitHub Flow and short-lived branches as the base workflow.
- Update AGENTS.md, docs/ai-assisted-workflow.md, docs/documentation-workflow.md, ai/specs/_template/plan.md, docs/decisions.md, and the Phase 4 indicator plans.
- Do not change product code.
- Do not add scripts or dependencies.

Verification:
- Run git diff --check.
- Run git status --short --branch.

Delivery:
- Summarize changed files.
- Summarize the workflow rules added.
- Summarize verification results.
```

## Workflow Isolation

- Branch: `docs/parallel-agent-workflow`
- Worktree: the current repository checkout is acceptable because this is a single documentation work item.
- Parallel-safe: no other agent should edit workflow docs in the same branch while this plan is active.
- Integration: merge this documentation PR before starting the Raspberry and web indicator implementation branches.

## Notes / Assumptions

- This change documents the manual workflow first.
- A Bash helper script can be considered later only if the manual workflow becomes repetitive.


## Migration provenance

Original source: `docs/plans/parallel-agent-workflow.md` at baseline 818e88e. Relocated 2026-10-06;
original content/language retained with path references adjusted. Historical
commands, approvals and pending notes retain their original context.

## Record maintenance after migration

For future work, read [spec.md](spec.md), this plan and [journal.md](journal.md).
Revise the plan before implementation; preserve historical prompts as evidence,
not authorization to execute outdated commands. Mandatory root/common workflow,
Linux/Docker operation and D025 govern current work. Maintain the local journal
and synchronize definition status/updated with the parent INDEX.md in the same
change. No secrets, credentials, tokens, connection strings, PII or real customer
data; sensitive configuration uses parameter names only.
