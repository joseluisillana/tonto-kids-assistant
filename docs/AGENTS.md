# Documentation context

Read [root](../AGENTS.md), mandatory [AI workflow](ai-assisted-workflow.md) and
[documentation workflow](documentation-workflow.md) before editing docs or exports.

This directory owns durable architecture/decisions, roadmap, specs index,
project-journal, operating guides and plans. `architecture.md` explains design;
`decisions.md` records dated decisions; `roadmap.md`/`specs.md` plus the newest
dated journal entry give current state. Registered plans and templates live exclusively in ai/. Demo runbook/checklist and Raspberry setup provide
operation context. Releases and final report preserve evidence, not new scope.

Depends on: code/scripts/CI and validated human decisions as evidence;
[specs](../ai/specs/AGENTS.md) for contracts. Used by: every work item, operating
skills and export/NotebookLM synthesis. No product runtime imports Markdown.
Do not duplicate the detailed common rules here or restructure SDD directories.

When changing contracts/architecture/setup/scope/validation, update the relevant
source and paired plan per workflow, with a ready implementation prompt and
branch/worktree/parallel/integration details. Editorial changes can skip the
plan update only when no implementation behavior changes, stated in the summary.
Cross-check related specs and the component's AGENTS.md map; don't turn a closed
phase or historical provider/platform instruction into current work.

Validation: check referenced files, command source and factual evidence, run
`git diff --check`; no runtime tests needed for prose-only changes. Export through
`./scripts/export-docs-for-notebooklm.sh` only when needed, following its existing
source/path safety and avoiding concurrent writes. Output is derived and ignored;
it omits some local AGENTS.md files. The hook installer has linked-worktree limits
documented in documentation workflow. Sources stay public; no credentials/PII.
