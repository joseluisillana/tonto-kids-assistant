# Parallel Agent Workflow Implementation Plan

## Objective

Implement the repository documentation changes required by `specs/parallel-agent-workflow.md` so TONTO has clear, standard rules for isolated parallel AI-assisted development.

## Source Spec

- Spec: `specs/parallel-agent-workflow.md`
- Related docs:
  - `AGENTS.md`
  - `docs/ai-assisted-workflow.md`
  - `docs/documentation-workflow.md`
  - `docs/plans/TEMPLATE-spec-implementation-plan.md`
  - `docs/decisions.md`
  - `docs/plans/raspberry-listening-indicator.md`
  - `docs/plans/web-listening-indicator.md`

## Scope

Included:

- Documentation-only workflow update.
- Formal rules for one work item per branch/PR.
- Formal rules for one worktree per parallel agent/work item.
- References to standard GitHub Flow, trunk-based development, small changes, and Git worktrees.
- Updates to existing Phase 4 indicator plans so they can be launched safely in parallel.

Excluded:

- Code behavior changes.
- New dependencies.
- New Git hooks or automation scripts.
- Branch protection changes in GitHub settings.
- Changes to the product architecture.

## Implementation Plan

1. Add `specs/parallel-agent-workflow.md`.
2. Add this paired plan in `docs/plans/parallel-agent-workflow.md`.
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
6. Update `docs/plans/TEMPLATE-spec-implementation-plan.md` with a `Workflow Isolation` section.
7. Update existing Raspberry and web indicator plans to state they should run in separate branches/worktrees.
8. Record the durable process decision in `docs/decisions.md`.

## Acceptance Criteria

- The repository has a spec and plan for parallel agent workflow isolation.
- Agent-facing rules are present in `AGENTS.md`.
- Human-facing workflow guidance is present in `docs/ai-assisted-workflow.md`.
- Documentation evidence expectations are present in `docs/documentation-workflow.md`.
- Future plans have a place to state whether they are parallelizable.
- Raspberry and web listening indicator plans explicitly use separate branches/worktrees.
- No code behavior changes are made.

## Verification

For this documentation-only workflow change:

```powershell
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
- Keep GitHub Flow and short-lived branches as the base workflow.
- Update AGENTS.md, docs/ai-assisted-workflow.md, docs/documentation-workflow.md, docs/plans/TEMPLATE-spec-implementation-plan.md, docs/decisions.md, and the Phase 4 indicator plans.
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
- A helper script such as `scripts/new-workflow.ps1` can be considered later only if the manual workflow becomes repetitive.
