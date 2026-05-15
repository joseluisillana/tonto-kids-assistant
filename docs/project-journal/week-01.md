# Week 01 Project Journal

## Goal

Establish the project foundation and keep the first MVP slice narrow: a minimal text-to-speech conversation loop using a Raspberry Pi thin client, a Python/FastAPI backend, and local `espeak` playback.

## Current State

- Repository structure exists for backend, client, shared models, docs, specs, tests, scripts, and web validation client.
- Raspberry Pi 3 Model B v1.2 is the target physical client.
- Local TTS with `espeak` is the first audio output path.
- Backend MVP language is Python/FastAPI.
- Go is deferred and excluded from active MVP CI gates.
- React + TypeScript + Vite web validation client exists for backend testing and demo support.
- Official PowerShell scripts exist for setup, dev, tests, and builds.

## Key Decisions

- Keep the Raspberry Pi as a thin client.
- Keep AI orchestration in the backend.
- Use HTTP/JSON for the first client/backend contract.
- Use Markdown in the repo as the source of truth.
- Use NotebookLM as a synthesis layer, not as the canonical documentation store.
- Use Codex to help maintain documentation and project journal entries.

## AI Usage

- Codex is used for repository inspection, implementation planning, documentation updates, and verification.
- GitHub Copilot is intended for editor-level coding assistance.
- NotebookLM will be used for research, synthesis, and final-report drafting from exported repo sources.

## Risks and Watch Items

- Documentation can drift if decisions are made only in chat or NotebookLM.
- README, roadmap, and specs must stay aligned with the narrow first milestone.
- Hardware work should not pull STT, wake word, or Arduino integration into the first implementation slice too early.

## Next Documentation Tasks

- Keep this journal updated after meaningful project sessions.
- Add week 2 journal when backend/OpenAI integration begins.
- Promote any stable NotebookLM insights back into `docs/`.
