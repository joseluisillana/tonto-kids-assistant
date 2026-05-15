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

## GitHub Copilot

Use Copilot for local coding assistance:

- boilerplate,
- small refactors,
- editor completions,
- quick implementation hints.

Copilot is useful inside the editor, but architectural decisions should still be reflected in `docs/decisions.md` or specs.

## NotebookLM

Use NotebookLM to study and synthesize:

- ask how the system currently works,
- generate study notes,
- compare roadmap and implementation,
- prepare report drafts,
- identify gaps in documentation.

NotebookLM reads exported repository documentation. It does not replace the repository.

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
