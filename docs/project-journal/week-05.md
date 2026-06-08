# Week 05 Kickoff

**Date:** 2026-06-08
**Status:** Phases 0-2 complete.

## Objective

Prepare Week 05 so the next AI-assisted implementation pass starts from the real project state and a narrow MVP scope.

Week 04 is complete. The system has been validated end-to-end with listening indicators, conversation calibration, and demo resilience. Week 05 focuses on making the existing system demo-ready: clear startup, polished conversational UX, graceful error handling, and a successful multi-run rehearsal.

## Current State at Kickoff

Week 04 is complete (Phases 0-5).

Validated paths:
- Raspberry voice loop: `client/main.py --mode voice` with listening indicator.
- Web voice loop: browser microphone with visible indicator and auto-stop.
- Text fallback: `POST /chat`.
- Backend: `POST /chat/audio` with STT via OpenAI `gpt-4o-mini-transcribe`.
- In-memory session history.
- Prompt calibrated for Spanish, child-friendly, short answers.

Current test state:
- 52 Python tests pass.
- Web typecheck: to be verified.

Known gaps:
- Demo startup requires multiple manual commands.
- No single runbook for demo operators.
- Error messages are technical.
- ALSA/JACK warnings clutter terminal.
- No structured demo rehearsal evidence.

## Prepared Documents

- `specs/week-05-demo-stability.md`
- `docs/plans/week-05-demo-stability.md`
- `docs/project-journal/week-05.md`

## Proposed Week 05 Phases

0. Documentation kickoff and handoff for agents.
1. Demo runbook and startup scripts.
2. Conversational UX polish.
3. Error resilience.
4. Demo rehearsal (3+ consecutive runs).
5. Closeout with evidence.

## Recommended Next Action

Phase 1: create a demo runbook and startup script to reduce operator friction.
## Phase 1 — Demo Runbook and Startup Scripts (implemented 2026-06-07)

**Branch:** `feature/week-05-phase1-demo-runbook`
**Tracking:** GitHub issue #35

### Objective

Reduce the friction of starting a TONTO demo so an operator can start with 1-2 commands.

### Changes

**`scripts/demo-raspberry.sh`** (new):
- Bash script for Raspberry Pi demo startup.
- Default env vars: `TONTO_BACKEND_URL`, `TONTO_AUDIO_DEVICE`, `TONTO_RECORD_SECONDS`.
- Health check with 5 retries and 2s delay before starting.
- Activates venv and starts client in voice mode.
- Tracked as executable in git (mode 100755).

**`docs/demo-runbook.md`** (new):
- Prerequisites section.
- Quick start: 3 commands (backend, Raspberry, web).
- Full demo flow for Raspberry (5 steps).
- Full demo flow for web (5 steps).
- Known warnings (ALSA/JACK) documented as ignorable.
- Troubleshooting: 6 common failures with fixes.

### Validation Evidence (2026-06-08)

**Environment:**
- Branch: `feature/week-05-phase1-demo-runbook`
- Backend: `http://192.168.1.91:8000` (Windows, LAN mode)
- Raspberry audio device: `plughw:CARD=Device,DEV=0`
- Commands used:

```bash
chmod +x scripts/demo-raspberry.sh
./scripts/demo-raspberry.sh
```
**Observations (voice turns):**

| Check | Result | Notes |
|---|---|---|
| Health check (curl /health) | OK (1/5) | Backend responded immediately |
| Venv activation | OK | Activate found and sourced |
| Client starts in voice mode | OK | `--mode voice` launched correctly |
| Turn 1: indicator visible | OK | Live countdown 1-6s |
| Turn 1: transcript | Accurate | Transcription worked |
| Turn 1: response | Coherent | Spanish, child-friendly |
| Turn 1: espeak | Audible | Standard quality |
| Turn 2: indicator visible | OK | Same as turn 1 |
| Turn 2: transcript | Accurate | Transcription worked |
| Turn 2: response | Educational, coherent | Spanish, child-friendly |
| Turn 2: espeak | Audible | Standard quality |
| ALSA/JACK warnings | Known, non-blocking | Same as previous validations |

**Observations (health check retries):**

| Scenario | Result | Notes |
|---|---|---|
| Backend stopped | ERROR after 5 retries | Clear error message with instructions |
| Backend started mid-retries | Connected on attempt 5/5 | Recovery works correctly |
| Retry interval | 2s delay, ~7s total | `--connect-timeout 5` prevents hangs |
| Script executable in git | Fixed | Tracked as 100755, no manual chmod needed |

**Issues found and fixed during validation:**
- UTF-8 BOM at start of script caused warning (non-blocking). Fixed by saving without BOM.
- Venv setup instructions in script referenced PowerShell command. Fixed to show bash instructions.
- Backend requirements incorrectly included in venv setup message. Fixed to only include client requirements.
- `curl` hung without `--connect-timeout` when backend was unreachable. Fixed with 5s timeout.
- Script lost execute permissions after `git pull`. Fixed by tracking as 100755 in git.

**Human judgment:**
- The script reduces demo startup from 4 manual commands to 1.
- Health check provides clear feedback before starting, with retries and recovery.
- The operator experience is smoother than the previous manual setup.

### Acceptance Criteria

- [x] Demo operator can start with 1-2 commands.
- [x] Health check with reintentos funciona.
- [x] Runbook cubre flujo completo de demo Raspberry.
- [x] Runbook cubre flujo completo de demo web.
- [x] Warnings ALSA/JACK documentados como ignorables.
- [x] Troubleshooting cubre fallos comunes de ambos clientes.

### Status

- [x] Raspberry hardware validation completed.
- [x] All issues fixed.
- [x] Issue #35 ready to close.

## Phase 2 — Conversational UX Polish (implemented 2026-06-08)

**Branch:** `feature/week-05-phase2-conversational-ux`
**Tracking:** GitHub issue #36

### Objective

Make TONTO responses feel more natural and demo-ready for children while keeping
the MVP architecture unchanged.

### Changes

**`backend/openai_client.py`:**
- Kept the existing Spanish, child-friendly, short-answer requirement.
- Added guidance to start with a direct answer before adding supporting detail.
- Added guidance to use one simple example or comparison when useful.
- Added guidance to avoid long lists, markdown, and lecture-style answers.
- Added guidance for natural greetings/farewells with a gentle invitation to ask
  one small educational question.
- Reduced `MAX_OUTPUT_TOKENS` from `220` to `180` so spoken answers stay tighter
  for Raspberry `espeak` and browser speech.

**`tests/test_openai_client.py`:**
- Updated the OpenAI payload test to verify the new conversational UX guidance.

### Demo Scenario Review

The Phase 2 prompt now explicitly supports the expected demo sequence:

| Scenario | Expected behavior |
|---|---|
| Greeting | Natural Spanish greeting, then a small educational invitation |
| Educational question | Direct answer first, then a short child-friendly explanation |
| Follow-up question | Uses recent in-memory context coherently |
| Farewell | Natural goodbye without introducing new architecture or state |

### Validation

- Automated validation: `tests/test_openai_client.py` checks the prompt payload
  includes Spanish, short answers, direct-answer style, no long lists/markdown,
  greeting/farewell guidance, recent context, and the configured token limit.
- Full Python suite: `.\scripts\test.ps1 -Target python` passed with 52/52 tests
  on 2026-06-08. The first sandboxed run hit a temp-file `PermissionError`; the
  same official command passed when rerun outside the sandbox.

### Acceptance Criteria

- [x] TONTO prompt supports coherent demo question sequences.
- [x] Responses remain short, Spanish, child-friendly, and educational.
- [x] Prompt changes are documented.
- [x] Prompt changes are covered by focused tests.

### Status

- [x] Code prompt polish implemented.
- [x] Focused test updated.
- [x] Full Python test suite passed.
