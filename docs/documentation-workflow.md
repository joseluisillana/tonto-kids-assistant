# Documentation Workflow

TONTO uses a simple documentation loop:

```text
Repo docs -> NotebookLM export -> NotebookLM synthesis -> reviewed repo docs
```

The goal is to avoid stale notes while still using AI tools to understand and summarize the project.

## Roles

## Repository

The repository is the official source of truth.

Stable information belongs in Markdown files tracked by Git:

- architecture decisions,
- active specs,
- roadmap changes,
- setup instructions,
- weekly project journal,
- final report drafts.

## Codex and OpenCode

Codex is the primary project assistant. OpenCode is an additional tool that can also help maintain documentation while the project evolves.

Useful Codex/OpenCode tasks:

- summarize recent changes,
- update the weekly journal,
- reconcile docs after code changes,
- identify contradictions between README, specs, roadmap, and decisions,
- prepare source exports for NotebookLM.

Codex and OpenCode output is not final until it is reviewed and committed.

## GitHub

GitHub preserves the project history.

Commits should include documentation updates when behavior, architecture, setup, or scope changes. This makes the final course report easier to reconstruct from real evidence instead of memory.

## NotebookLM

NotebookLM is a research and synthesis layer.

It should read exported copies of repository files from `exports/notebooklm/`. It should not become the place where final project truth lives.

For routine refreshes, prefer the generated combined source:

```text
exports/notebooklm/NOTEBOOKLM_COMBINED.md
```

NotebookLM can duplicate imported files when many sources are refreshed manually. The combined source keeps the update loop simple because one document can be replaced while still preserving all repository context.

Good uses:

- ask questions about the current architecture,
- generate weekly summaries,
- compare decisions,
- find missing documentation,
- draft final report sections.

Avoid:

- editing final docs only inside NotebookLM,
- keeping important decisions only in Google Drive,
- trusting generated summaries without bringing reviewed changes back to Git.

## Update Routine

Use this routine at the end of meaningful work sessions:

1. Ask Codex or OpenCode to update the journal and docs affected by the work.
2. Run tests or checks relevant to the change.
3. Commit code and documentation together.
4. Let the `pre-commit` hook regenerate `exports/notebooklm/`.
5. Refresh NotebookLM sources from that export when you want deeper synthesis.

When a phase, week, or active milestone changes, also check that agent-facing summaries did not become stale:

- `AGENTS.md` maps the architecture and mandates reading `docs/specs.md`, `docs/roadmap.md` and the newest dated journal entry. Do not copy active sprint/phase status into the map.
- High-level summaries in `docs/architecture.md`, `docs/specs.md`, `docs/roadmap.md`, and `README.md` should not point agents toward an already completed phase.
- This is a documentation consistency check only; it does not imply a product, architecture, or implementation change.

## Work Item Evidence

Each coherent work item should leave enough evidence to reconstruct what happened later for the course report.

For every branch/PR, record the relevant items:

- source spec or issue,
- implementation plan,
- human decisions made during the work,
- AI tools used and their role,
- checks or scripts run,
- manual browser or Raspberry validation,
- GitHub Issue or PR link when used,
- remaining risks or follow-up work.

For parallel work, keep evidence attached to the branch that produced it. If multiple parallel PRs update the same journal or roadmap section, merge one PR first, update the remaining branch from `main`, and reconcile the documentation before the second PR merges.

## Spec Handoff Routine

For new/migrated specs and issues, follow [ai/README.md](../ai/README.md) and
use the record's plan.md/journal.md and INDEX.md. Legacy records retain their
sources until migration; new indexes are not full history. Global journals
retain milestone context and link record-specific evidence.

Before creating or materially changing a spec, follow the canonical
[Spec Handoff Workflow](ai-assisted-workflow.md#spec-handoff-workflow), including
the paired plan, ready-to-paste implementation prompt, editorial exception,
naming, and workflow-isolation details required by the plan template. This
procedure stays in the repository instead of only in a chat.

## Manual Export

Run this whenever you want to refresh NotebookLM sources outside a commit:

```bash
./scripts/export-docs-for-notebooklm.sh
```

The export is derived output and is ignored by Git.

The script writes individual source files, `INDEX.md`, and `NOTEBOOKLM_COMBINED.md`. Use the combined file as the primary NotebookLM source unless you need to inspect or import a specific document separately.

The default destination remains `exports/notebooklm`. Custom destinations must
be subdirectories of `exports/`; absolute equivalents are accepted. Repository
root, source directories, `exports` itself, outside paths and symbolic links in
the destination path are rejected before writing or deleting anything.

Sources remain README/AGENTS, Markdown under docs/specs, and web/README.
The current selection excludes ai/: read it directly for the new process and
records. This instrumentation does not change exporter coverage or scripts. The
export rejects symbolic links in source trees (including broken/internal links),
hardlinked files and protected filename categories before reading contents.
Validation failures leave the previous export intact. Output is prepared in a
private staging directory and then replaces only the validated derived-output
directory. Errors contain fixed messages rather than arbitrary paths/content.
The pre-commit hook uses the same checks and stops the commit on export failure.

Keep source documents public and avoid concurrent modifications during export.
This validates paths and file types; it does not scan Markdown for credentials
copied into a regular document. No credentials should be stored in those sources.

## Hook Installation

Run this once per clone:

```bash
./scripts/install-git-hooks.sh
```

The installer currently requires a clone with a `.git/` directory; do not assume it supports a linked worktree where `.git` is a file. This documents its existing limitation without changing the script.

It installs a local `pre-commit` hook that regenerates NotebookLM export files before each commit.

Local AGENTS.md files under backend/client/shared/scripts/tests/spikes/.agents
are not all included by the current export source selection. Read the repository
for the complete instruction hierarchy; do not treat NotebookLM as its loader.
The export script and source selection are unchanged by the reorganization.
