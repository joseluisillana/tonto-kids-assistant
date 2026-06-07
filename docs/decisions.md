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

## D018 - Initial STT provider

Use OpenAI `gpt-4o-mini-transcribe` as the initial backend STT provider for the Week 03 voice pipeline.

The rationale is demo stability and implementation efficiency: the backend already uses `OPENAI_API_KEY`, the audio endpoint already accepts short WAV uploads, and the integration can be implemented with the Python standard library without adding an SDK or a heavy local model dependency. The model can be overridden with `OPENAI_STT_MODEL`; `OPENAI_MODEL` remains dedicated to conversational response generation.

Two offline options remain candidates for a later spike, not active implementation: Vosk Spanish for a small zero-API-cost recognizer, and `whisper.cpp` for offline Whisper-style transcription with CPU-only support. Both need real sample validation before they replace the online STT default because the current MVP priority is a stable demo loop, not proving offline STT.

## D019 - Week 03 Phase 3 web audio validation

Use the existing React web validation client as the Week 03 Phase 3 surface for an interactive audio loop against `POST /chat/audio`, after the Phase 2 Raspberry capture/upload automation and post-TTS revalidation are addressed.

The goal is to reduce integration risk and collect visible evidence from a browser after the Raspberry voice client automation has been validated. The web path must reuse the existing backend audio contract and STT provider: it should send a compatible WAV, receive `{session_id, transcript, response}`, and display transcript, response, latency, status, and errors.

This is a validation decision, not a product architecture change. The Raspberry Pi remains the physical MVP client, local `espeak` remains the target TTS path, and browser TTS, audio persistence, streaming, local STT, and backend transcoding of browser formats remain out of scope unless a later decision changes that.

## D020 - Week 04 stabilization-first scope

Prepare Week 04 as a stabilization and demo-readiness milestone before adding new behavior.

The original roadmap theme of memory and physical states is narrowed for the MVP. Memory means validating and, only if necessary, lightly calibrating the existing short in-memory session context. It does not mean persistence, vector memory, user profiles, or advanced personalization.

Physical states are a decision gate, not automatic Arduino work. Arduino/LED implementation may be considered only after the current voice demo is run repeatedly and a human decision confirms that physical indicators directly improve the final demo. If accepted, Arduino work needs its own narrow spec and plan before code changes.

The Week 04 kickoff itself is documentation-only: spec, implementation plan, roadmap alignment, and journal setup for AI-assisted agents.

## D021 - Week 04 Phase 4 indicator scope

Defer Arduino and LED integration outside the 6-week MVP. Treat physical indicators as future TONTO work for a later version, not as active Week 04 implementation scope.

Implement non-physical listening/time indicators first because Phase 3 Raspberry validation showed that operators do not clearly know when the child should stop speaking. This affects both the Raspberry terminal voice loop and the web voice validation loop.

Raspberry and web indicators must be specified and planned separately before code so they can be implemented in parallel while preserving the same backend contracts. The paired specs and plans are:

- `specs/raspberry-listening-indicator.md`
- `docs/plans/raspberry-listening-indicator.md`
- `specs/web-listening-indicator.md`
- `docs/plans/web-listening-indicator.md`

## D022 - Parallel agent workflow isolation

Use a standard small-team workflow for AI-assisted parallel development: GitHub Flow with short-lived branches, small PRs, and Git worktrees when multiple agents or work items run at the same time.

Each coherent work item gets one branch and one PR. When work runs in parallel, each work item also gets a separate Git worktree so agents do not share the same checkout or branch.

The rationale is to reduce collisions, keep `main` as the integration branch, preserve reviewable history, and make the project evidence easier to explain for the AI course. This is a workflow decision, not a product architecture change.

The detailed spec and plan are:

- `specs/parallel-agent-workflow.md`
- `docs/plans/parallel-agent-workflow.md`
