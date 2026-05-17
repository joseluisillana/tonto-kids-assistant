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

Use a lightweight GitHub Flow:

1. Start from `main`.
2. Create a short-lived branch for one focused change.
3. Keep implementation, tests, and documentation together when they describe the same change.
4. Open a small PR back to `main`.
5. Merge only after the change is reviewed and the relevant checks or manual validations are clear.

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
