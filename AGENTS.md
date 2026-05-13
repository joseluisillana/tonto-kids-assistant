# AGENTS.md

Persistent instructions for Codex and AI assistants working on TONTO Kids Assistant.

## Project Goal

TONTO Kids Assistant is an educational physical assistant for children. The MVP goal is to validate a simple, reproducible conversation loop using accessible hardware:

1. A Raspberry Pi client sends a child interaction to a backend.
2. The backend generates an educational response.
3. The Raspberry Pi speaks the response aloud.

The project is demo-first. Prefer working, understandable prototypes over broad platform design.

## Current MVP Architecture

- Monorepo with separate `backend/`, `client/`, `shared/`, `docs/`, `specs/`, `scripts/`, and `tests/` areas.
- Backend for the MVP is Python with FastAPI.
- Raspberry client is Python.
- Communication is simple HTTP/JSON.
- The Raspberry Pi is a thin client. It handles local device I/O and audio playback, not AI orchestration.
- The backend owns conversation orchestration and model/API integration.
- Shared request/response contracts belong in `shared/` when needed.
- Documentation and specs live in `docs/` and `specs/`.

## Current Implementation Milestone

The current milestone is the first minimal text-to-speech conversation loop:

- Build the smallest backend/client path needed to send a request and receive a speakable response.
- Use local `espeak` on the Raspberry client for TTS.
- Keep state in memory only if state is needed at all.
- Optimize for clarity, debuggability, and a real demo.

Explicitly out of scope for this first milestone:

- No speech-to-text.
- No wake word.
- No Arduino integration.
- No UI.
- No persistence.
- No authentication.
- No user accounts.
- No advanced memory.
- No multi-agent architecture.
- No local AI models.

## Coding Rules

- Keep code small, direct, and easy to inspect.
- Prefer plain Python and FastAPI patterns already present in the repo.
- Keep the backend as a lightweight monolith for the MVP.
- Keep the Raspberry client as a simple Python process.
- Use typed data structures where they clarify request/response contracts.
- Use clear names over clever abstractions.
- Handle obvious failure cases, especially backend timeouts and unavailable TTS.
- Add or update focused tests when changing behavior.
- Do not silently change architecture or milestone scope.
- Do not rewrite unrelated files.
- Do not implement future-scope features unless the user explicitly asks.

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

If implementation and documentation disagree, pause and make the decision explicit before continuing.

## Assistant Behavior

- Read the existing repo context before making changes.
- Respect the current milestone and keep scope narrow.
- Ask before adding dependencies or changing architecture.
- If a request conflicts with this file, follow the user's latest explicit instruction and update this file or the relevant docs if the decision is persistent.
- When unsure, choose the smallest reversible change that advances the MVP.
