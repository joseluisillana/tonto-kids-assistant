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

## Codex

Codex helps maintain documentation while the project evolves.

Useful Codex tasks:

- summarize recent changes,
- update the weekly journal,
- reconcile docs after code changes,
- identify contradictions between README, specs, roadmap, and decisions,
- prepare source exports for NotebookLM.

Codex output is not final until it is reviewed and committed.

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

1. Ask Codex to update the journal and docs affected by the work.
2. Run tests or checks relevant to the change.
3. Commit code and documentation together.
4. Let the `pre-commit` hook regenerate `exports/notebooklm/`.
5. Refresh NotebookLM sources from that export when you want deeper synthesis.

## Manual Export

Run this whenever you want to refresh NotebookLM sources outside a commit:

```powershell
.\scripts\export-docs-for-notebooklm.ps1
```

The export is derived output and is ignored by Git.

The script writes individual source files, `INDEX.md`, and `NOTEBOOKLM_COMBINED.md`. Use the combined file as the primary NotebookLM source unless you need to inspect or import a specific document separately.

## Hook Installation

Run this once per clone:

```powershell
.\scripts\install-git-hooks.ps1
```

It installs a local `pre-commit` hook that regenerates NotebookLM export files before each commit.
