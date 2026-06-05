# Week 04 Kickoff

**Date:** 2026-06-02
**Status:** Phase 0 complete; Phase 1 in progress.

## Objective

Prepare Week 04 so the next AI-assisted implementation pass starts from the real project state and a narrow MVP scope.

The kickoff intentionally does not change code. It creates the documentation, spec, plan, roadmap alignment, and journal context needed for Codex, OpenCode, or another agent to work safely.

## Current State at Kickoff

Week 03 is complete.

Validated paths:

- Text fallback: `POST /chat`.
- Raspberry voice loop: `client/main.py --mode voice`.
- Audio backend: `POST /chat/audio` with WAV validation and OpenAI `gpt-4o-mini-transcribe`.
- Raspberry TTS: `espeak -v es -s 135 -g 8`.
- Web validation loop: browser microphone to compatible WAV to `/chat/audio` to visible transcript/response and browser speech.

Implementation facts reviewed:

- Backend short session history already exists in memory.
- No persistence exists.
- Arduino/LEDs are available future hardware but not integrated.
- Existing docs warn against adding future-scope behavior without an explicit milestone decision.

## Scope Adjustment

The original Week 04 roadmap target, "memoria simple y estados físicos", is coherent only after narrowing:

- Memory should mean validating and lightly calibrating the current in-memory session context, not adding persistence or advanced memory.
- Physical states should be a decision gate, not automatic Arduino work.
- The first practical Week 04 implementation milestone should be reproducible demo validation.

## Prepared Documents

- `specs/week-04-demo-stability.md`
- `docs/plans/week-04-demo-stability.md`
- `docs/project-journal/week-04.md`

Related summaries updated:

- `docs/roadmap.md`
- `docs/specs.md`
- `docs/decisions.md`

## Proposed Week 04 Phases

Phase 0: Documentation kickoff.

Phase 1: Reproducible demo baseline.

Phase 2: Demo resilience and error handling.

Phase 3: Conversation and memory calibration.

Phase 4: Physical state decision gate.

Phase 5: Week 04 closeout.

## Recommended Next Action

Phase 1 complete. Start Phase 2: Demo resilience and error handling.

## Phase 1 — Reproducible Demo Baseline (2026-06-05)

**Branch:** `feature/week-04-phase1-demo-baseline`

### Validation Results

| Check | Result | Notes |
|---|---|---|
| Python tests (`pytest`) | 45/45 passed | backend, client, STT, audio tests |
| TypeScript typecheck | Clean | No errors |
| Backend start | OK | Binds to `0.0.0.0:8000` (LAN mode) |
| `/health` endpoint | 200 OK | `{"status":"ok"}` from Windows and Raspberry |
| `/chat` text fallback | 200 OK | `OPENAI_API_KEY` configured, response received |
| `/chat/audio` endpoint | Working | WAV validation + STT integration confirmed |
| Raspberry `/health` | 200 OK | `curl -s "$TONTO_BACKEND_URL/health"` from `tonto-pi` |
| Raspberry voice turns | 3/3 OK | All turns completed successfully |
| Memory (in-session) | Validated | TONTO recalled initial greeting in turn 3 |

### Hardware Validation Evidence

**Environment:**
- Windows backend: `192.168.1.91:8000` (WiFi, LAN mode)
- Raspberry Pi: `tonto-pi` with USB PnP Sound Device (card 1, device 0)
- Mic device: `plughw:CARD=Device,DEV=0`
- TTS: `espeak -v es -s 135 -g 8` (default)
- Backend API key: configured via User env var

**Setup commands (Raspberry):**
```bash
export TONTO_BACKEND_URL=http://192.168.1.91:8000
export TONTO_AUDIO_DEVICE=plughw:CARD=Device,DEV=0
source .venv/bin/activate
python3 client/main.py --mode voice
```

**Turn 1:**
- Input: `Hola tonto, ¿cómo estás? ¿Estás bien?`
- Response: `¡Hola! Estoy muy bien, gracias. ¿Y tú? ¿Cómo te va?`
- espeak: Audible, understandable ✅

**Turn 2:**
- Input: `Según va iteración en las pruebas. ¿Qué tal te ves?`
- Response: `¡Me veo genial! Siempre listo para ayudar. ¿Tienes alguna pregunta o tema del que quieras hablar?`
- espeak: Audible ✅

**Turn 3:**
- Input: `¿Qué te he preguntado al principio de la sesión? ¿Te acuerdas?`
- Response: `Sí, me preguntaste cómo estaba y si estaba bien. ¡Gracias por preguntar! ✨ ¿Hay algo más en lo que te pueda ayudar?`
- espeak: Audible ✅
- Memory: TONTO correctly recalled turn 1 question ✅

**Warnings:** ALSA/JACK warnings appeared on every turn (same as Week 03). They do not block audio capture or playback.

### Acceptance Status

- [x] At least one failure documented with clear cause (setup: missing API key — resolved)
- [x] At least three consecutive voice turns on Raspberry (3/3 passed)
- [x] Text fallback usable end-to-end
- [x] Blocker classified and resolved: **setup** (API key) + **hardware** (Raspberry access — validated)

### Phase 1 Complete — Ready for Phase 2

Phase 1 acceptance criteria are met. Next: Phase 2 — Demo Resilience and Error Handling.

## AI Tools Used

Codex: documentation kickoff (Phase 0). OpenCode: Phase 1 validation execution — repo inspection, test runs, backend startup, endpoint validation, journal update.

## Human Decisions

- The Week 04 kickoff product should be documentation and agent handoff material, not code.
- Week 04 should be phased before implementation.
- Arduino should not be treated as automatic implementation work.

## Notes

- The local branch was created as `docs-week-4-kickoff` because the sandboxed environment blocked writing slash-prefixed branch refs. The project convention remains `<type>/<short-kebab-description>` in normal Git workflows.
- Phase 1 branch follows project convention: `feature/week-04-phase1-demo-baseline`.
