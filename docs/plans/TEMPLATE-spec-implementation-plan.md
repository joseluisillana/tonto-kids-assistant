# <Spec Name> Implementation Plan

## Objective

Describe the concrete outcome this plan should produce. Keep it tied to the source spec and MVP milestone.

## Source Spec

- Spec: `specs/<feature-name>.md`
- Related docs:
  - `docs/specs.md`
  - `docs/roadmap.md`
  - `docs/architecture.md`

## Scope

Included:

- List the behavior, docs, tests, or validation work that belongs in the implementation.

Excluded:

- List explicit non-goals, deferred work, dependencies not allowed, or architecture boundaries.

## Implementation Plan

- Describe the smallest coherent implementation path.
- Name likely subsystems or files only when it prevents ambiguity.
- Preserve existing contracts, fallbacks, and demo paths unless the source spec explicitly changes them.

## Acceptance Criteria

- List observable outcomes that prove the spec is implemented.
- Include UI, API, CLI, documentation, or manual validation outcomes as applicable.

## Verification

Use official project scripts whenever possible:

```powershell
.\scripts\test.ps1 -Target python
.\scripts\test.ps1 -Target web
.\scripts\build.ps1 -Target web
git diff --check
git status --short --branch
```

Adjust the command list only when the source spec makes a narrower or broader check set appropriate.

## Implementation Prompt

```text
Implement the spec in <spec path>.

Before editing:
- Read AGENTS.md.
- Read docs/ai-assisted-workflow.md.
- Read the source spec and this implementation plan.
- Run git branch --show-current and git status --short --branch.
- Preserve unrelated user changes in the worktree.

Task:
- Implement the smallest change that satisfies the source spec.
- Keep the project architecture and MVP scope intact.
- Do not add dependencies or change contracts unless the spec explicitly requires it.
- Update docs or specs only when implementation changes durable project state.

Verification:
- Run the checks listed in this plan.
- Report any checks that could not be run and why.

Delivery:
- Summarize changed files.
- Summarize behavior implemented.
- Summarize verification results.
```

## Notes / Assumptions

- Record defaults chosen for ambiguous implementation details.
- Record any blockers or decisions that must be resolved before implementation.
