# AGENTS.md

Persistent instructions for Codex, OpenCode, and AI assistants working on TONTO Kids Assistant.

## Project Goal

TONTO Kids Assistant is an educational physical assistant for children. The MVP goal is to validate a simple, reproducible conversation loop using accessible hardware:

1. A Raspberry Pi client sends a child interaction to a backend.
2. The backend generates an educational response.
3. The Raspberry Pi speaks the response aloud.

The project is demo-first. Prefer working, understandable prototypes over broad platform design.

## Current MVP Architecture

- Monorepo with separate `backend/`, `client/`, `web/`, `shared/`, `docs/`, `specs/`, `scripts/`, and `tests/` areas.
- Backend for the MVP is Python with FastAPI.
- Raspberry client is Python.
- Communication is simple HTTP/JSON.
- Go is not part of the active MVP implementation or CI gate. Treat any Go files as legacy/evaluation artifacts unless the user explicitly reactivates Go and updates the docs/specs.
- The Raspberry Pi is a thin client. It handles local device I/O and audio playback, not AI orchestration.
- The backend owns conversation orchestration and model/API integration.
- Shared request/response contracts belong in `shared/` when needed.
- Documentation and specs live in `docs/` and `specs/`.

## Current Implementation Milestone

The Week 04 Phase 1 (Reproducible Demo Baseline) is complete. The system has been validated end-to-end on real hardware:

- Week 03 voice milestone was complete: text loop, voice loop from Raspberry, voice loop from web.
- Week 04 Phase 1 validated on 2026-06-05: 3 consecutive voice turns on Raspberry real (`tonto-pi`) against backend LAN (`192.168.1.91:8000`), in-memory session history confirmed (TONTO recalled initial greeting in turn 3), `/chat` and `/chat/audio` working.
- The next milestone is Week 04 Phase 2: Demo Resilience and Error Handling.
- Do not expose a manual WAV upload/file picker as part of the Phase 3 product/demo UI; WAV files are only acceptable as test fixtures or integration helpers.
- Keep state in memory only if state is needed at all.
- Optimize for clarity, debuggability, and a real demo.

Explicitly out of scope for this first milestone:

- No wake word.
- No Arduino integration.
- No advanced product UI beyond the web validation client and its narrow Phase 3 audio validation surface.
- No persistence.
- No authentication.
- No user accounts.
- No advanced memory.
- No multi-agent architecture.
- No local AI models.
- No local STT or local audio models.
- No backend transcoding of browser `webm`/`ogg` audio unless explicitly decided later.
- No automated audio capture/upload beyond the narrow web validation loop or Raspberry client work explicitly requested for the active milestone.

## Coding Rules

- Keep code small, direct, and easy to inspect.
- Prefer plain Python and FastAPI patterns already present in the repo.
- Keep the backend as a lightweight monolith for the MVP.
- Do not add or restore Go CI checks until Go is explicitly selected for an active backend implementation.
- Keep the Raspberry client as a simple Python process.
- Use typed data structures where they clarify request/response contracts.
- Use clear names over clever abstractions.
- Handle obvious failure cases, especially backend timeouts and unavailable TTS.
- Add or update focused tests when changing behavior.
- Do not silently change architecture or milestone scope.
- Do not rewrite unrelated files.
- Do not implement future-scope features unless the user explicitly asks.

## Local Environment and Automation

- Treat the host machine as clean. Do not install Python packages globally.
- Use the official PowerShell scripts in `scripts/` before inventing ad hoc setup, dev, test, or build commands.
- Python dependencies must be installed into the repo-local `.venv/`.
- On Windows, use `.\.venv\Scripts\python.exe` when a direct Python command is unavoidable.
- On Linux/macOS, use `.venv/bin/python` when a direct Python command is unavoidable.
- Run Python tests through `.\scripts\test.ps1 -Target python` or the `.venv` Python executable, never through a global `pytest`.
- Frontend dependencies must stay local to `web/node_modules/`.
- Use `npm ci` or `npm install` only inside `web/`; never use `npm install -g` unless the user explicitly approves it.
- Keep dependency caches local to `.cache/` when scripts support it; do not rely on user-profile caches such as global pip/npm caches.
- If Codex or OpenCode sandboxing blocks network access or writes inside `.venv/`, `web/node_modules/`, or `.cache/`, request escalation for the official script command instead of switching to global tools.
- If the build, test, setup, or dev workflow changes, update the scripts and documentation in the same change.
- CI, humans, and agents should share the same command surface whenever practical:
  - `.\scripts\setup-dev.ps1`
  - `.\scripts\dev.ps1 -Service backend|web|all`
  - `.\scripts\test.ps1 -Target python|web|all`
  - `.\scripts\build.ps1 -Target web|all`

## Git and Contribution Workflow

- Use the project branch convention `<type>/<short-kebab-description>`.
- Use `feature/`, `fix/`, `docs/`, `chore/`, or `experiment/` as the initial branch types.
- Prefer `docs/` for documentation-only changes.
- Do not use tool-owned branch prefixes such as `codex/` unless the user explicitly asks for them.
- Use one branch and one PR per coherent work item.
- Keep work item branches short-lived and focused.
- For parallel agent work, use one Git worktree per agent/work item. Do not run parallel agents in the same working tree or on the same branch.
- Use `git` for local repository operations such as status, diff, branch, switch, worktree, add, commit, and log.
- Prefer GitHub CLI (`gh`) for GitHub operations such as PR creation/view/checks/merge and issue creation/view/update.
- For phases, parallel work, hardware validation, or multi-session work, create or reuse a GitHub Issue before implementation and reference it from the PR.
- Use Conventional Commits when preparing commits, such as `feat:`, `fix:`, `docs:`, `chore:`, `test:`, or `refactor:`.
- Keep PRs focused on one coherent change.
- Include docs or specs in the same change when behavior, architecture, setup, scope, or workflow changes.
- Follow `docs/ai-assisted-workflow.md` for the shared human and AI-assisted Git workflow.

## Pre-Edit AI Workflow Gate

Before any repository edit, agents must follow `docs/ai-assisted-workflow.md`.

Minimum pre-edit gate:

1. Run `git branch --show-current` and `git status --short --branch`.
2. If the current branch is `main`, do not edit files yet. First create or switch to a project branch using `<type>/<short-kebab-description>`, unless the user explicitly says to work on `main`.
3. Use `docs/` for documentation-only work, `fix/` for bug fixes, `feature/` for new behavior, `chore/` for maintenance, and `experiment/` for exploratory work.
4. Do not use tool-owned prefixes such as `codex/` unless the user explicitly asks for them.
5. If `main` has uncommitted changes, stop and ask before moving, stashing, committing, discarding, or editing those changes.
6. Apply the same gate before running formatters, generators, export scripts, or other commands that write repository files.
7. If another agent is working in parallel, create or use a separate Git worktree for this work item before editing.
8. If a related PR merges while this work item is still active, update from `main` and reconcile conflicts before continuing.

## Simplicity Rules

- Start with the simplest end-to-end path that can work.
- Prefer one endpoint before multiple endpoints.
- Prefer one client loop before a framework or plugin system.
- Prefer in-memory data before storage.
- Prefer direct function calls before event buses, queues, or background workers.
- Prefer explicit configuration before dynamic discovery.
- Prefer readable scripts before complex automation.

## Do Not Overengineer

Avoid introducing:

- microservices,
- message brokers,
- databases,
- ORMs,
- auth frameworks,
- plugin systems,
- background job systems,
- observability stacks,
- container orchestration,
- complex dependency injection,
- premature hardware abstractions,
- production deployment machinery.

These may become useful later, but they are not part of the current MVP milestone.

## Dependencies

Ask the user before introducing any new runtime or development dependency.

When proposing a dependency, explain:

- why it is needed now,
- what simpler option was considered,
- where it will be used,
- whether it affects Raspberry Pi setup.

Do not add packages just for convenience.

## Documentation and Specs

Always update docs or specs when decisions change.

Use:

- `docs/architecture.md` for architecture decisions,
- `docs/roadmap.md` for milestone or scope changes,
- `docs/specs.md` or files in `specs/` for behavior and implementation specs,
- `README.md` only for high-level project orientation and setup guidance.

When a spec is created or materially changed, also create or update its execution plan in `docs/plans/`. A material spec change is any change to behavior, scope, contracts, architecture, validation, or acceptance criteria. The plan must include an implementation prompt ready for Codex/OpenCode handoff. Purely editorial spec changes may skip a new plan, but the change summary must say that no implementation behavior changed.

If implementation and documentation disagree, pause and make the decision explicit before continuing.

## Assistant Behavior

- Read the existing repo context before making changes.
- Respect the current milestone and keep scope narrow.
- Ask before adding dependencies or changing architecture.
- If a request conflicts with this file, follow the user's latest explicit instruction and update this file or the relevant docs if the decision is persistent.
- When unsure, choose the smallest reversible change that advances the MVP.

## Tool Environment

OpenCode runs on Windows through WSL2 with the DevExpert provider
(OpenAI-compatible API) at `https://inference.devexpert.io/v1`.

Use `deepseek-v4-flash` as the recommended model and `deepseek-v4-pro`
as the alternative model. OpenCode follows the same repository rules as
Codex: use official scripts, keep dependencies local, stay on project
branches, and do not change architecture or milestone scope without an
explicit decision.
