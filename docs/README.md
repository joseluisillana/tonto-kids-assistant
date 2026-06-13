# TONTO Documentation Index

This folder is the official documentation home for TONTO Kids Assistant.

The repository is the source of truth. NotebookLM is a reading and synthesis tool that consumes exported copies of these files, but final decisions and durable documentation must come back here.

## What to Read First

1. `../README.md` - project orientation, setup, and current MVP shape.
2. `project-genesis.md` - autonomous prompt to rebuild the entire project from scratch with AI assistance.
3. `architecture.md` - how the Raspberry Pi client, backend, and web validation client fit together.
4. `raspberry-pi-setup.md` - reproducible setup and recovery guide for the Raspberry Pi client.
5. `roadmap.md` - 6-week delivery plan and MVP boundaries.
6. `specs.md` - active behavior-level specification summary.
7. `decisions.md` - compact record of technical decisions.
8. `documentation-workflow.md` - how docs, NotebookLM, Codex, OpenCode, and GitHub stay aligned.

For the current Week 05 Phase 3 kickoff, read `../specs/week-05-demo-stability.md`, `plans/week-05-demo-stability.md`, and `project-journal/week-05.md` before starting implementation work.

## Working Notes

- `project-journal/` records weekly progress, decisions, blockers, and AI usage.
- `plans/` stores implementation handoff plans for specs, including prompts ready for Codex/OpenCode.
- `research/` stores research notes and source guidance.
- `final-report-outline.md` tracks the eventual course delivery document structure.
- `ai-assisted-workflow.md` explains how Codex, OpenCode, GitHub Copilot, and NotebookLM are used responsibly.
- `project-genesis.md` is the autonomous genesis prompt to rebuild the project from zero.

## Documentation Rule

If knowledge is stable and affects the project, document it in this repo.

If knowledge is exploratory, use NotebookLM or research notes first.

If NotebookLM generates something useful, revise it and promote it back into this folder.

When a spec changes behavior, scope, contracts, validation, or acceptance criteria, update or create its paired execution plan in `plans/` using `plans/TEMPLATE-spec-implementation-plan.md`.
