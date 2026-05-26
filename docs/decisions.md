# Decisions

## D001 - Backend MVP language

Use Python/FastAPI for the MVP backend.

## D002 - First API endpoint

Use POST /chat.

## D003 - TTS ownership

Use local Raspberry Pi TTS with espeak for the first milestone.

## D004 - Memory

Use in-memory short session history only.

## D005 - Network configuration

Raspberry uses TONTO_BACKEND_URL; never localhost unless backend runs on Raspberry.

## D006 - Latency target

Target < 5 seconds end-to-end for MVP; improve later.

## D007 - First implementation scope

No STT, wake word, Arduino, advanced product UI, persistent memory or auth in the first implementation slice.

## D008 - Web validation client

Add a lightweight React + TypeScript + Vite web client under `web/` as a validation and demo surface. It consumes the same backend HTTP contracts as the Raspberry Pi client and must not duplicate AI orchestration or hardware responsibilities.

## D009 - Go checks deferred from CI

Do not run Go checks in CI while the MVP backend language is Python/FastAPI and Go is not selected in the active specs. Existing Go files are treated as legacy or evaluation artifacts, not as release gates. Reintroduce Go CI only if a future decision makes Go part of the active implementation.

## D010 - Local automation and isolated environments

Use PowerShell scripts under `scripts/` as the official command surface for setup, dev servers, tests, and builds. Python dependencies live in the repo-local `.venv/`; frontend dependencies live in `web/node_modules/`. Agents, humans, and CI should use the same scripts instead of installing packages globally or inventing one-off commands.

## D011 - Documentation source of truth

Use Markdown files in the repository as the source of truth for durable project documentation. NotebookLM is a synthesis and research layer that reads exported copies from `exports/notebooklm/`, and useful NotebookLM output must be reviewed and promoted back into repo docs before it becomes official.

## D012 - NotebookLM export automation

Generate NotebookLM source files with `scripts/export-docs-for-notebooklm.ps1`. Install the local Git `pre-commit` hook with `scripts/install-git-hooks.ps1` so the export is refreshed before commits. The export folder is derived output and is ignored by Git.

## D013 - Backend LAN exposure for Raspberry validation

Keep the backend bound to `127.0.0.1` by default for local development. Use `.\scripts\dev.ps1 -Service backend -AllowLan` when the Raspberry Pi must reach the backend over the local network; the Raspberry should use the Windows PC LAN IP or a resolvable hostname in `TONTO_BACKEND_URL`.

## D014 - AI-assisted Git workflow

Use a lightweight GitHub Flow for human and AI-assisted project changes. Branch names use `<type>/<short-kebab-description>` with initial types `feature/`, `fix/`, `docs/`, `chore/`, and `experiment/`. Commit messages use Conventional Commits such as `feat:`, `fix:`, `docs:`, `chore:`, `test:`, and `refactor:`. Project branches describe the work, not the assistant or tool that helped with it.

## D015 - NotebookLM combined source export

Extend `scripts/export-docs-for-notebooklm.ps1` to generate `exports/notebooklm/NOTEBOOKLM_COMBINED.md` alongside the individual Markdown exports and `INDEX.md`. The combined file is the preferred source for routine NotebookLM refreshes because NotebookLM can duplicate many re-uploaded files instead of replacing them cleanly. The repository remains the source of truth, and `exports/notebooklm/` remains derived output ignored by Git.

## D016 - Provisional STT ownership

Use backend STT as the default direction for Week 03 voice work, but treat it as a provisional MVP design choice rather than a proven Raspberry Pi limitation.

The rationale is simplicity: the Raspberry Pi remains a thin client that captures audio and plays TTS, while the backend owns orchestration, provider integration, and future STT changes. This keeps the client small and makes the STT provider easier to replace.

This decision does not prove that local Raspberry Pi STT is infeasible. Local STT should only be ruled out after a concrete hardware test shows unacceptable CPU, memory, latency, quality, or setup complexity. Until then, local STT, wake word, and local audio models remain out of scope for the MVP kickoff, not technically disproven.

## D017 - OpenCode as AI-assisted project tool

Use OpenCode as an additional AI-assisted project tool for implementation, repository inspection, documentation updates, review, and verification. Codex remains the primary project assistant. OpenCode uses the DevExpert OpenAI-compatible provider at `https://inference.devexpert.io/v1`, with `deepseek-v4-flash` as the recommended model and `deepseek-v4-pro` as the alternative model.

This is a workflow decision, not a product architecture change. OpenCode must follow the same repository rules as Codex: use official scripts, keep dependency installs local, follow project branch naming, avoid tool-owned branch prefixes, and promote durable decisions back into repository documentation. The AI-assisted workflow can incorporate more compatible tools over time under the same rules.
