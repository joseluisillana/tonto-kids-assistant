# Parallel Agent Workflow

**Version:** 0.1
**Status:** Planned and ready for documentation implementation
**Last Updated:** 2026-06-07

## Objective

Define how TONTO uses isolated work items, short-lived branches, pull requests, and Git worktrees when humans and AI agents work in parallel.

The goal is to reduce collisions, preserve evidence for the AI course, and keep the repository compatible with standard software development workflows instead of inventing a custom process.

## Standard Pattern

TONTO uses a small-team workflow based on:

- GitHub Flow: branch from `main`, open a focused PR, run checks, merge to `main`, delete the branch.
- Trunk-based development principles: keep branches short-lived and integrate small changes frequently.
- Small changes: each PR should be one coherent, reviewable change with its tests and documentation.
- Git worktrees for parallel agent execution: each parallel agent gets a separate working tree and branch.

## Definitions

### Work Item

A work item is one coherent change that can be planned, implemented, reviewed, verified, and merged independently.

Examples:

- Add the Raspberry listening indicator.
- Add the web listening indicator.
- Update workflow documentation.
- Fix one backend timeout bug.

Non-examples:

- "Improve everything in Week 04."
- "Refactor backend and redesign web UI."
- "Let two agents edit the same branch until it works."

### Workflow Branch

Each work item uses one project branch:

```text
<type>/<short-kebab-description>
```

Examples:

```text
feature/week-04-phase4-raspberry-listening-indicator
feature/week-04-phase4-web-listening-indicator
docs/parallel-agent-workflow
```

### Workflow Worktree

When multiple agents or work items run in parallel, each work item should use its own Git worktree. The worktree is a separate checkout of the repository tied to a single branch.

Example layout:

```text
tonto-kids-assistant/
../tonto-worktrees/
  week-04-phase4-raspberry-listening-indicator/
  week-04-phase4-web-listening-indicator/
```

## Rules

- Never run parallel agents in the same working tree.
- Never let two agents edit the same branch at the same time.
- Do not edit on `main` unless the developer explicitly asks for it.
- Keep one work item per branch and PR.
- Keep branches short-lived; merge or close them once the work item is resolved.
- Keep PRs small enough to review, verify, and revert.
- Include docs/spec updates in the same work item when behavior, scope, architecture, setup, or validation changes.
- If a work item materially changes a spec, update or create its paired plan in `docs/plans/`.
- When two parallel PRs both need journal or roadmap updates, merge one first, then rebase or merge `main` into the other and reconcile the documentation.
- Delete merged branches and remove stale worktrees.

## Work Item Lifecycle

1. Define the work item and its source spec or issue.
2. Check `main` is clean and current.
3. Create a branch for the work item.
4. For parallel work, create or use a dedicated worktree for that branch.
5. Run the pre-edit gate in that worktree.
6. Implement the smallest change that satisfies the work item.
7. Run official verification scripts.
8. Update journal/docs with evidence.
9. Commit with a Conventional Commit message.
10. Push and open a focused PR.
11. Merge only after checks and validation are clear.
12. Delete the branch and remove the worktree.

## Recommended Commands

Create a parallel worktree from `main`:

```powershell
git switch main
git pull --ff-only
git worktree add ..\tonto-worktrees\week-04-phase4-raspberry-listening-indicator -b feature/week-04-phase4-raspberry-listening-indicator main
```

List active worktrees:

```powershell
git worktree list
```

Remove a completed worktree:

```powershell
git worktree remove ..\tonto-worktrees\week-04-phase4-raspberry-listening-indicator
```

Prune stale worktree metadata:

```powershell
git worktree prune
```

## Acceptance Criteria

- `docs/ai-assisted-workflow.md` documents isolated work items and parallel worktrees.
- `AGENTS.md` includes mandatory rules for branch and worktree isolation.
- `docs/documentation-workflow.md` explains how workflow evidence is captured.
- `docs/plans/TEMPLATE-spec-implementation-plan.md` asks every plan to document workflow isolation.
- Existing Phase 4 indicator plans state that Raspberry and web work should run in separate branches/worktrees.
- `docs/decisions.md` records the workflow decision.

## Non-Goals

- Do not introduce a heavyweight project-management framework.
- Do not require GitFlow release/develop branches.
- Do not add automation scripts until the manual workflow is proven repetitive enough.
- Do not require multiple agents for every change.
- Do not use worktrees for tiny solo edits unless useful.

## Notes

This workflow is intentionally a small-team variant of common industry practice. The project keeps `main` as the integration branch, uses short-lived PR branches for review and checks, and uses worktrees only when concurrent implementation would otherwise collide in one checkout.

## References

- GitHub Flow: `https://docs.github.com/en/get-started/using-github/github-flow`
- Git worktree: `https://git-scm.com/docs/git-worktree`
- Trunk-Based Development: `https://trunkbaseddevelopment.com/`
- Google Engineering Practices, Small CLs: `https://google.github.io/eng-practices/review/developer/small-cls.html`
