# NotebookLM Research Workflow

NotebookLM is used as a study and synthesis assistant for TONTO.

It should consume exported copies of project documentation, not become the source of truth.

## Create the Notebook

Create a NotebookLM notebook named:

```text
TONTO Kids Assistant
```

Use it for research, summaries, questions, and final-report drafting.

## Source Export

Generate sources from the repository:

```powershell
.\scripts\export-docs-for-notebooklm.ps1
```

The script writes source files to:

```text
exports/notebooklm/
```

Upload or refresh those files in NotebookLM when you want it to understand the current project state.

## Recommended Initial Sources

Start with these exported files:

- `README.md`
- `AGENTS.md`
- `docs__README.md`
- `docs__architecture.md`
- `docs__roadmap.md`
- `docs__specs.md`
- `docs__decisions.md`
- `docs__documentation-workflow.md`
- `docs__ai-assisted-workflow.md`
- `specs__conversation-loop.md`

The generated `INDEX.md` explains what was exported.

## Good Questions to Ask

```text
Explain the current TONTO architecture in simple terms.
What is in scope for the current MVP milestone?
What is explicitly out of scope right now?
Which decisions are stable and which remain open?
Summarize the progress of week 1.
What documentation seems missing or contradictory?
Draft a final report section about AI-assisted development.
```

## Promotion Rule

NotebookLM can draft and synthesize, but final documentation must be reviewed and copied back into the repo.

If a NotebookLM answer changes understanding of the project, update the relevant Markdown file and commit it.

## Sync Limit

NotebookLM is not treated as a Git-connected documentation system.

The reliable sync boundary is:

```text
repo -> export script -> exports/notebooklm -> NotebookLM
```

The return path is human-reviewed:

```text
NotebookLM idea -> Codex/developer review -> repo docs
```
