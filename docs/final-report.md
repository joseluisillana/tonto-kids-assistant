# TONTO Kids Assistant - Final Report

**Course:** AI Expert
**Project:** TONTO Kids Assistant
**Status:** MVP closeout report
**Last Updated:** 2026-06-18

## 1. Project Introduction

TONTO Kids Assistant is an educational physical assistant prototype for children. The MVP validates a simple voice conversation loop with accessible hardware:

```text
child voice -> Raspberry Pi capture -> backend STT/chat -> spoken answer
```

The project exists to test whether a small, understandable system can create a child-friendly educational interaction without building a large product platform first. The goal is not to build a finished robot. The goal is to prove that a child can ask a question aloud, receive a short educational answer, and hear that answer through a physical Raspberry Pi client.

The educational motivation is to make learning feel conversational and approachable. TONTO answers in Spanish, uses warm child-friendly language, keeps responses short, and tries to answer directly before adding a simple example or comparison.

The personal and course motivation was to build a real AI-assisted project with evidence: specs, implementation, tests, hardware validation, runbooks, known limitations, and a final report. The project also became a practical exercise in responsible AI-assisted development: AI tools accelerated implementation and documentation, while product scope, architecture decisions, hardware validation, and final acceptance remained human-owned.

## 2. MVP Scope

The MVP was constrained to six weeks. That constraint shaped the project more than any single technology choice.

The included scope was:

- a Raspberry Pi 3 client as the physical assistant surface,
- a Python/FastAPI backend running locally during development and demos,
- HTTP/JSON contracts for text and audio turns,
- OpenAI-backed conversation and STT as the initial inference path,
- DevExpert Inference as an alternate provider for AI Expert course alignment,
- local Raspberry TTS with `espeak`,
- a React/Vite web validation client for faster browser-based testing,
- short in-memory session history,
- demo scripts, runbooks, and closeout documentation.

The intentionally excluded scope was:

- wake word detection,
- local AI models or local STT,
- persistent memory,
- user accounts or authentication,
- multi-user support,
- cloud deployment,
- advanced dashboarding,
- Arduino/LED physical states inside the six-week MVP,
- advanced product UI beyond the web validation client,
- backend Go as an active implementation requirement.

This scope kept the project demo-first. Each phase had to move the project closer to a reproducible physical conversation loop, not toward a generic platform.

## 3. Architecture

TONTO uses a thin-client architecture.

The Raspberry Pi handles local device work:

- microphone capture with `arecord`,
- local playback with `espeak`,
- operator interaction through the Python client,
- session ID management,
- HTTP calls to the backend.

The backend owns orchestration:

- `/chat` for text turns,
- `/chat/audio` for short WAV audio turns,
- WAV validation,
- STT provider calls,
- conversational response generation,
- short in-memory session history,
- child-friendly system behavior.

The web validation client exists to accelerate development and demos. It uses browser microphone capture, produces compatible WAV audio, calls the same backend contract, shows transcript and response evidence, and can speak responses through browser speech synthesis. It does not replace the physical Raspberry client.

The public MVP contracts are:

```text
POST /chat
POST /chat/audio
GET /health
```

The backend provider layer supports:

- OpenAI as the default provider through `TONTO_INFERENCE_PROVIDER=openai`,
- DevExpert through `TONTO_INFERENCE_PROVIDER=devexpert`.

OpenAI keeps the Responses API for text generation and audio transcriptions for STT. DevExpert uses its OpenAI-compatible Chat Completions and audio transcription endpoints. Raspberry and web clients stay provider-agnostic.

## 4. Development Process

The repository is organized as a small monorepo:

- `backend/` for FastAPI and provider logic,
- `client/` for the Raspberry Python client,
- `web/` for the React/Vite validation client,
- `shared/` for common models,
- `specs/` for behavior and implementation specs,
- `docs/` for architecture, workflow, runbooks, journal, and reports,
- `scripts/` for official setup, dev, test, build, demo, and agent helper commands,
- `tests/` for Python backend/client tests.

The process was spec-driven. Material behavior changes were documented before or alongside implementation, and paired execution plans were added under `docs/plans/` when needed.

The weekly journal captured real progress and evidence:

- Week 03 validated the real audio pipeline.
- Week 04 stabilized the demo and added non-physical listening indicators.
- Week 05 converted the system into a repeatable demo and added dual-provider operation.
- Week 06 prepared closeout documents, limitations, future work, this report, and final demo evidence.

Official scripts kept humans and AI agents on the same command surface:

```powershell
.\scripts\setup-dev.ps1
.\scripts\dev.ps1 -Service backend|web|all
.\scripts\test.ps1 -Target python|web|all
.\scripts\build.ps1 -Target web|all
```

For hardware operation and agent-supported validation, Week 05 added:

```powershell
.\scripts\agent-backend.ps1
.\scripts\agent-raspberry.ps1
```

The main development rule was to keep the MVP small, inspectable, and reversible.

## 5. AI-Assisted Development

AI assistance was used throughout the project, but not as an unchecked source of truth.

Codex was used for repository-level work:

- reading project context,
- implementing focused code changes,
- creating and updating specs,
- updating weekly journals,
- running official tests,
- reconciling documentation after implementation,
- preparing final closeout documents.

OpenCode was documented as an additional CLI assistant using DevExpert Inference through `https://inference.devexpert.io/v1`, with `deepseek-v4-flash` as the recommended model and `deepseek-v4-pro` as the alternative.

GitHub Copilot was positioned as local editor assistance for boilerplate and small implementation hints.

NotebookLM was used as a study and synthesis layer over exported repository documentation. The repository remains the source of truth; NotebookLM helps review and summarize but does not replace committed docs.

The project captured a clear responsibility boundary:

```text
AI accelerates the work. The developer owns the decisions.
```

Human-owned decisions included:

- keeping the Raspberry as a thin client,
- deferring Arduino/LEDs outside the six-week MVP,
- choosing non-physical listening indicators first,
- prioritizing Raspberry touch UI over cloud deployment after the MVP,
- accepting `espeak` quality as sufficient for MVP validation,
- using OpenAI as the primary live demo provider and DevExpert as an alternate provider path.

Risks of AI assistance were mitigated by:

- pre-edit Git gates,
- short project branches,
- specs and plans before material changes,
- official scripts instead of ad hoc commands,
- tests for backend and client behavior,
- real Raspberry validation before claiming hardware success,
- documentation updates whenever behavior or scope changed.

## 6. Implementation

The implementation progressed in layers.

First, the text conversation loop established the basic system:

```text
manual text -> backend /chat -> inference provider -> response -> Raspberry TTS
```

Then the voice path added `POST /chat/audio`. The endpoint accepts one short WAV turn, validates size and duration, transcribes the audio, routes the transcript through the same conversational path, and returns transcript plus response.

The Raspberry client supports:

- text mode,
- voice mode with `--mode voice`,
- `arecord` capture,
- multipart audio upload,
- transcript and response display,
- local TTS playback,
- listening progress,
- operator-friendly error handling.

The web validation client supports:

- text chat through `/chat`,
- browser microphone capture,
- WAV generation compatible with `/chat/audio`,
- visible timer/progress while listening,
- auto-stop at the configured recording limit,
- transcript and response display,
- browser speech output when supported.

Provider support was added without changing the public TONTO contracts. The backend selects OpenAI or DevExpert at startup through `TONTO_INFERENCE_PROVIDER`. This keeps provider complexity behind the backend boundary.

The implementation deliberately avoids persistence, auth, multi-user state, local AI models, and extra infrastructure. That restraint is part of the MVP design.

## 7. Validation

Validation combined automated checks and real hardware evidence.

Automated validation included:

- Python tests for backend, audio endpoint, client behavior, OpenAI adapter behavior, and STT behavior,
- web typecheck for the React/TypeScript validation client,
- focused tests added as behavior expanded.

Key recorded automated states:

- Week 03 Phase 2A: `23 passed` after backend STT integration.
- Week 04: `49/49` Python tests after conversation calibration.
- Week 05 provider work: `62/62` Python tests.
- Week 05 error resilience: `78/78` Python tests and web typecheck passed.
- Week 06 kickoff baseline: 78 Python tests pass and web typecheck passes.

Hardware validation included:

- 2026-05-23: USB microphone capture and playback validated on Raspberry Pi.
- 2026-05-27: manual Raspberry WAV upload to `/chat/audio` validated with `HTTP_STATUS=200`.
- 2026-05-30: real STT validation from Raspberry audio using OpenAI `gpt-4o-mini-transcribe`, including transcript, response, and local `espeak` playback.
- 2026-05-30: Raspberry `--mode voice` client automation validated and then revalidated after TTS tuning.
- 2026-06-01: web voice loop validated from browser microphone to transcript, response, and browser speech.
- 2026-06-05: 3 consecutive Raspberry voice turns validated with short-session memory.
- 2026-06-07: Raspberry and web listening/time indicators validated.
- 2026-06-11: conversational UX polish validated with 6/6 real Raspberry questions.
- 2026-06-13: error resilience validated with 4/4 Raspberry voice turns.
- 2026-06-13: demo rehearsal validated with 6/6 OpenAI Raspberry voice turns and 1/1 DevExpert smoke turn.

The demo checklist records the final presentation-day validation flow: backend health, provider smoke, Raspberry preflight, optional web verification, demo sequence, and Plan B fallbacks.

## 8. Results

The MVP works within its intended scope.

TONTO can:

- accept voice input through Raspberry,
- send audio to the backend,
- transcribe the audio,
- generate a Spanish child-friendly educational answer,
- speak the answer aloud through Raspberry,
- preserve short session context during a running backend process,
- run the same backend contracts with OpenAI or DevExpert,
- use the web client as validation and fallback.

The most important result is that the project moved from an idea to a reproducible demo path with real hardware evidence. The Raspberry remains simple, the backend remains small, and the system can be operated with documented scripts and runbooks.

Several lessons shaped the final MVP:

- Physical audio validation must happen early because microphone and playback assumptions are fragile.
- A web validation client is extremely useful, but it should not replace hardware proof.
- Demo stability benefits more from runbooks, clear errors, and rehearsals than from adding late features.
- `espeak` is enough to validate the loop, but not enough for a polished child-facing voice.
- Provider abstraction is useful only when it stays invisible to clients and preserves existing contracts.
- AI-assisted development works best when the repo contains durable specs, plans, and evidence.

What changed from the original idea:

- Arduino/LED physical states were deferred outside the six-week MVP.
- The first post-MVP priority became a Raspberry touch UI with a Waveshare 5" HDMI display and animated assistant face.
- Cloud deployment was explicitly deprioritized after the MVP because it does not improve the immediate physical child-facing experience.
- DevExpert support became an extra MVP line to align with the AI Expert course.

## 9. Future Work

The prioritized post-MVP backlog lives in `docs/future-work.md`.

The highest-priority next step is a Raspberry touch UI with an animated assistant face using the selected Waveshare 5" HDMI touch display. This would make TONTO feel more like a physical assistant and less like a terminal voice demo while preserving the Raspberry thin-client architecture.

Other important future work includes:

- better TTS for a more natural child-facing voice,
- inference provider improvements such as fallback, diagnostics, or future provider support,
- minimal session persistence,
- wake word exploration,
- Arduino/LED physical states,
- multi-user support,
- metrics and demo diagnostics.

Cloud deployment is intentionally not prioritized immediately after the MVP. It may become useful later for remote demos or multiple devices, but it adds operational, privacy, secret-management, and support complexity before improving the child-facing physical experience.

## 10. Appendix

### Key Project Documents

- `README.md`
- `docs/architecture.md`
- `docs/specs.md`
- `docs/roadmap.md`
- `docs/demo-runbook.md`
- `docs/demo-checklist.md`
- `docs/known-limitations.md`
- `docs/future-work.md`
- `docs/ai-assisted-workflow.md`

### Key Specs

- `specs/audio-pipeline.md`
- `specs/audio-pipeline-phase-3-web-loop.md`
- `specs/web-validation-client.md`
- `specs/raspberry-listening-indicator.md`
- `specs/web-listening-indicator.md`
- `specs/week-04-demo-stability.md`
- `specs/week-05-demo-stability.md`
- `specs/week-06-closeout.md`
- `specs/inference-providers.md`
- `specs/inference-provider-openai.md`
- `specs/inference-provider-devexpert.md`

### Key Journal Evidence

- `docs/project-journal/week-03.md`: real audio pipeline and Raspberry voice validation.
- `docs/project-journal/week-04.md`: demo stability, memory calibration, and listening indicators.
- `docs/project-journal/week-05.md`: runbook, error resilience, dual-provider rehearsal, and closeout evidence.
- `docs/project-journal/week-06.md`: presentation checklist, known limitations, future work, final report, and final demo closeout tracking.

### Common Commands

Backend:

```powershell
.\scripts\dev.ps1 -Service backend -AllowLan
```

Web client:

```powershell
.\scripts\dev.ps1 -Service web
```

Python tests:

```powershell
.\scripts\test.ps1 -Target python
```

Web checks:

```powershell
.\scripts\test.ps1 -Target web
```

Raspberry demo:

```bash
cd ~/tonto-kids-assistant
export TONTO_BACKEND_URL=http://<WINDOWS_LAN_IP>:8000
./scripts/demo-raspberry.sh
```

### Final MVP Statement

TONTO Kids Assistant validates the core MVP promise: an accessible Raspberry Pi client can capture a child's spoken question, send it to a simple backend, receive an educational AI response, and speak that response aloud in a repeatable demo.
