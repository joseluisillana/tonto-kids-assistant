# TONTO Documentation Index

This folder is the official documentation home for TONTO Kids Assistant.

The repository is the source of truth. NotebookLM is a reading and synthesis tool that consumes exported copies of these files, but final decisions and durable documentation must come back here.

## What to Read First

1. `../README.md` - project orientation, setup, and current MVP shape.
2. `architecture.md` - how the Raspberry Pi client, backend, and web validation client fit together.
3. `raspberry-pi-setup.md` - reproducible setup and recovery guide for the Raspberry Pi client.
4. `roadmap.md` - 6-week delivery plan and MVP boundaries.
5. `specs.md` - active behavior-level specification summary.
6. `decisions.md` - compact record of technical decisions.
7. `documentation-workflow.md` - how docs, NotebookLM, Codex, OpenCode, and GitHub stay aligned.

## Working Notes

- `project-journal/` records weekly progress, decisions, blockers, and AI usage.
- `plans/` stores implementation handoff plans for specs, including prompts ready for Codex/OpenCode.
- `research/` stores research notes and source guidance.
- `final-report-outline.md` tracks the eventual course delivery document structure.
- `ai-assisted-workflow.md` explains how Codex, OpenCode, GitHub Copilot, and NotebookLM are used responsibly.

## Documentation Rule

If knowledge is stable and affects the project, document it in this repo.

If knowledge is exploratory, use NotebookLM or research notes first.

If NotebookLM generates something useful, revise it and promote it back into this folder.

When a spec changes behavior, scope, contracts, validation, or acceptance criteria, update or create its paired execution plan in `plans/` using `plans/TEMPLATE-spec-implementation-plan.md`.
