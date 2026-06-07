# Week 04 Kickoff

**Date:** 2026-06-05
**Status:** Week 04 complete (Phases 0-5).

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

Phase 4 decision recorded. Next: implement non-physical listening/time indicators, using separate Raspberry and web branches if parallel work is useful.

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

## Phase 2 — Demo Resilience and Error Handling (2026-06-05)

**Branch:** `fix/week-04-phase2-demo-resilience`

### Issues Identified from Phase 1

1. **Client timeout too short for voice mode** — `REQUEST_TIMEOUT_SECONDS = 10` was shared for text and voice. Voice mode does STT + OpenAI + response, which can exceed 10s.
2. **URLError timeout not caught** — client caught `TimeoutError` but `urlopen` also raises `URLError` with timeout reason. The STT client handled this but the main client did not.
3. **Error messages unclear for demo** — technical messages not suitable for operators.

### Changes Made

**`client/main.py`:**
- Split timeout into `TEXT_TIMEOUT_SECONDS = 10` and `VOICE_TIMEOUT_SECONDS = 30`
- Added `_is_timeout_reason()` helper (matches `stt_client.py` pattern)
- `send_message()` now handles `URLError` timeout reasons
- `send_audio()` now handles `URLError` timeout reasons
- Added `socket` import for `socket.timeout` detection

**`tests/test_client.py`:**
- Added `test_send_message_url_error_timeout` — URLError with socket.timeout
- Added `test_send_audio_timeout` — TimeoutError in voice mode
- Added `test_send_audio_url_error_timeout` — URLError with socket.timeout in voice mode

### Test Results

- 48/48 tests passed (3 new tests added)
- TypeScript typecheck: clean (no web changes)

### Acceptance Status

- [x] Observed critical failures have a fix or documented workaround
- [x] Official relevant tests pass (48/48)
- [x] Documentation records what changed and why

### Phase 2 Complete — Ready for Phase 3

Phase 2 acceptance criteria are met. Next: Phase 3 — Conversation and Memory Calibration.

## Phase 3 — Conversation and Memory Calibration (completed 2026-06-07)

**Branch:** `feature/week-04-phase3-conversation-calibration`

### Objective

Make TONTO feel coherent enough for a short educational demo without adding memory architecture.

### Execution Plan

1. Validate in-memory context across 5+ related turns on Raspberry.
2. Use child-friendly educational questions in Spanish.
3. Check if TONTO maintains context without losing coherence.
4. If prompt tuning is needed:
   a. Adjust instructions in `backend/openai_client.py` (Spanish, shorter answers, child-friendly).
   b. Optionally reduce `max_output_tokens` if responses are too long.
   c. Keep changes small and reversible.
5. If no tuning is needed: document in journal that validation passed.

### Validation Setup (Raspberry)

```bash
export TONTO_BACKEND_URL=http://192.168.1.91:8000
export TONTO_AUDIO_DEVICE=plughw:CARD=Device,DEV=0
source .venv/bin/activate
python3 client/main.py --mode voice
```

### Suggested Test Sequence (5 turns)

1. "Hola TONTO, ¿qué es una estrella?"
2. "¿Y el sol es una estrella?"
3. "¿De qué está hecho el sol?"
4. "¿Por qué brilla?"
5. "¿Qué pasaría si el sol no existiera?"

### Acceptance Criteria

- [x] TONTO answers all 5 questions without losing context.
- [x] Context was not lost in an obvious way.
- [x] Prompt tuning code change is documented and tested.
- [x] Journal records the validation result.

### Prompt Calibration (2026-06-07)

Code calibration was applied before the final Raspberry 5-turn validation because the previous prompt was generic English-only guidance and did not explicitly enforce the Week 04 demo target: short, Spanish, child-friendly educational answers that use recent context.

Changes:

- Added reusable `OPENAI_INSTRUCTIONS` in `backend/openai_client.py`.
- Instructions now explicitly require Spanish answers.
- Instructions now request clear, warm, child-friendly language for children ages 6 to 10.
- Instructions now request 2 or 3 simple sentences unless the child asks for more.
- Instructions now tell TONTO to use recent conversation context for follow-up questions.
- Reduced `max_output_tokens` from `300` to `220`.

Tests:

- Added `tests/test_openai_client.py` to verify the OpenAI payload includes the calibrated instructions, recent context, and output-token limit.
- `.\scripts\test.ps1 -Target python` passed: 49/49 tests.

### Raspberry Validation Evidence (2026-06-07)

**Environment:**
- Branch: `feature/week-04-phase3-conversation-calibration`
- Raspberry branch status: tracking `origin/feature/week-04-phase3-conversation-calibration`
- Backend: `.\scripts\dev.ps1 -Service backend -AllowLan`
- Backend URL from Raspberry: `http://192.168.1.91:8000`
- Raspberry audio device: `plughw:CARD=Device,DEV=0`
- Raspberry client: `python3 client/main.py --mode voice`
- Session: same Raspberry voice client session for all 5 turns
- `/health` from Raspberry: `{"status":"ok"}`

**Backend evidence:**

- `GET /health` from `192.168.1.183`: 200 OK
- `POST /chat/audio` from `192.168.1.183`: 5/5 requests returned 200 OK

**Conversation sequence:**

| Turn | Child prompt | Transcript | TONTO result |
|---|---|---|---|
| 1 | `Hola TONTO, ¿qué es una estrella?` | `Hola tonto, ¿qué es una estrella?` | Explained a star as a hot ball of gas that shines in the sky. |
| 2 | `¿Y el sol es una estrella?` | `¿Y el Sol es una estrella?` | Correctly answered that the Sun is a nearby star and provides light and heat. |
| 3 | `¿De qué está hecho el sol?` | `¿De qué está hecho el sol?` | Answered hydrogen and helium, with a simple energy explanation. |
| 4 | `¿Por qué brilla?` | `Por qué brilla?` | Kept the Sun context and explained fusion as the reason it shines. |
| 5 | `¿Qué pasaría si el sol no existiera?` | `¿Qué pasaría si el Sol no existiera?` | Explained that Earth would be cold and dark and life would not work as it does now. |

**Human judgment:**

- Responses were coherent with expectations.
- Responses were in Spanish, educational, and suitable for the MVP demo.
- The Raspberry `espeak` voice remains robotic but slow and understandable enough for MVP validation.
- ALSA/JACK warnings appeared again after each response. They are the same known non-blocking warnings from previous hardware validations and did not prevent capture, upload, response, or playback.

**Improvement identified:**

- The operator experience does not clearly show when the user should stop talking.
- This affects both Raspberry and web validation flows.
- A time/progress/listening indicator should be considered as a small future demo-resilience improvement before the final demo.

### Previous Prompt (for reference)

```python
instructions: (
    "You are TONTO, a friendly educational assistant for children. "
    "Answer clearly, briefly, and helpfully."
)
max_output_tokens: 300
```

### Current Prompt Intent

- Always answer in Spanish.
- Keep responses short and understandable for children.
- Use recent conversation context for follow-up questions.
- Preserve the existing in-memory session architecture and `/chat` + `/chat/audio` contracts.

### Status

- [x] Validation on Raspberry (5 turns)
- [x] Decision: prompt tuning needed
- [x] Implementation: small prompt/output-token calibration
- [x] Tests updated
- [x] Journal updated with implementation evidence
- [x] Journal updated with Raspberry validation evidence

### Phase 3 Complete — Ready for Phase 4

Phase 3 acceptance criteria are met. The calibrated prompt is sufficient for the current MVP demo. The next phase is the Week 04 Phase 4 decision gate, with one concrete non-physical state candidate already identified: a time/listening/progress indicator for Raspberry and web.

## Phase 4 — Physical State Decision Gate (kickoff prepared 2026-06-07)

**Branch:** `docs/week-04-phase4-kickoff`

### Objective

Decide whether the final MVP demo needs explicit state feedback before adding any implementation.

Phase 4 is a decision gate, not automatic Arduino work. The decision should compare physical LEDs against simpler non-physical indicators and the option to defer both.

### Inputs from Phase 3

- Raspberry 5-turn validation passed.
- TONTO responses are coherent enough for the current MVP demo.
- Audio playback is understandable but robotic.
- ALSA/JACK warnings remain noisy but non-blocking.
- The main operator UX gap is knowing when the user should stop speaking.
- The same timing/listening uncertainty exists in both Raspberry and web validation flows.

### Candidate State Vocabulary

- `idle`: ready for the next interaction.
- `listening`: recording audio.
- `uploading`: sending audio to backend.
- `thinking`: waiting for STT and response generation.
- `speaking`: playing the response.
- `error`: capture, network, STT, backend, or playback failure.

### Decision Options

1. **Defer physical and non-physical state work.**
   - Use current terminal/web messages only.
   - Lowest scope, but leaves the known operator uncertainty in place.

2. **Implement non-physical time/listening indicators first.**
   - Raspberry: terminal countdown/progress during fixed-duration recording.
   - Web: visible recording time/progress against the audio limit.
   - No new hardware, no new dependencies expected, directly addresses the Phase 3 UX gap.

3. **Prepare Arduino/LED physical states.**
   - Create a separate spec and plan before any code.
   - Higher demo value if the physical assistant needs visible presence, but higher hardware and integration risk.

### Recommendation for Decision

For the MVP demo, prefer option 2 unless the final presentation specifically needs physical LEDs. It addresses a validated usability problem with less scope than Arduino and keeps the Raspberry as a thin client.

### Human Decision (2026-06-07)

- Arduino and LED integration are deferred outside the 6-week MVP.
- Physical indicators remain a future TONTO improvement for another version.
- Phase 4 implementation should start with non-physical listening/time indicators.
- Raspberry and web need separate specs and plans because their implementations can run in parallel.
- No code should be changed until those specs and plans exist.

### Prepared Indicator Specs and Plans

- `specs/raspberry-listening-indicator.md`
- `docs/plans/raspberry-listening-indicator.md`
- `specs/web-listening-indicator.md`
- `docs/plans/web-listening-indicator.md`

### Web Recording Limit Follow-up Decision (2026-06-07)

**Tracking:** GitHub issue #23 (closed 2026-06-07), part of #18.

After reviewing the merged web listening indicator, a follow-up gap was identified: the UI shows elapsed recording time against the 10 second validation limit, but the capture does not yet make the end of that limit operationally clear.

Human decision:

- The web client should automatically stop browser audio capture when the configured recording limit is reached.
- The UI should show a short warning that the limit was reached.
- Sending should remain manual after auto-stop; reaching the timer must not automatically upload audio.
- The interaction should stay simple and demo-friendly enough for a child to understand: TONTO stopped listening, time is up, and the next step is pressing `Enviar voz`.

Documentation updated on branch `docs/week-04-phase4-web-recording-limit`:

- `specs/web-listening-indicator.md`
- `docs/plans/web-listening-indicator.md`
- `docs/specs.md`
- `docs/roadmap.md`

Implementation should use `feature/week-04-phase4-web-recording-limit` in a dedicated worktree and preserve the existing browser microphone -> WAV PCM -> `/chat/audio` contract.

### Acceptance Criteria

- [x] Human decision recorded: defer Arduino/LEDs outside the 6-week MVP and implement non-physical indicators first.
- [x] Separate Raspberry spec and plan exist before code changes.
- [x] Separate web spec and plan exist before code changes.
- [x] Follow-up web recording limit decision recorded before implementation.
- [x] Journal records the Arduino/LED deferral and rationale.
- [x] Scope remains inside MVP: no persistence, no wake word, no new AI architecture, no broad UI redesign.

### Kickoff Status

- [x] Phase 3 evidence reviewed.
- [x] Candidate state vocabulary drafted.
- [x] Decision options drafted.
- [x] Recommendation documented.
- [x] Human scope decision recorded.
- [x] Parallelizable indicator specs and plans prepared.

## Phase 4 — Web Recording Duration Indicator (implemented 2026-06-07)

**Branch:** `fix/web-recording-duration-indicator`

**Tracking:** GitHub issue #25 (closed 2026-06-07), related to #23 (closed) and parent #18.

### Objective

Repair the web client so a recording duration indicator is visible in the main TONTO interaction surface while browser microphone capture is active.

### Changes

- Added a visible `TONTO esta escuchando` recording indicator to the main web surface.
- Shows a live `00:SS / 00:10` counter and progress bar while capture is active.
- Automatically stops browser capture at the configured web validation limit.
- Keeps upload manual after auto-stop through `Enviar voz`.
- Shows a simple time-up notice after auto-stop.
- Keeps the existing browser microphone -> WAV PCM -> `/chat/audio` contract.
- Added focused web utility coverage for the recording duration label.

### Validation

- `.\scripts\test.ps1 -Target web` passed.
- `.\scripts\build.ps1 -Target web` passed.
- `git diff --check` passed.
- In-app browser loaded `http://127.0.0.1:5173/` with no console errors on initial load.
- Human manual browser validation with backend and web client running confirmed the behavior is now exactly as expected.

### Status

- [x] Counter visible in the main web interaction surface.
- [x] Counter updates while recording.
- [x] Counter resets after stop/cancel/send.
- [x] Capture auto-stops at the configured limit.
- [x] User still manually sends with `Enviar voz`.
- [x] Issue #25 ready to close through the PR.

## Phase 4 — Raspberry Listening Indicator Validation (planned 2026-06-07)

**Branch:** `docs/week-04-phase4-raspberry-listening-validation`
**Tracking:** GitHub issue #27 (closed 2026-06-07), part of #18.

### Objective

Validate the Raspberry listening indicator on real hardware per `specs/raspberry-listening-indicator.md` and close issue #27.

### Pre-conditions (all met)

- [x] Indicator implementation merged into `main` (`client/main.py:114-192`).
- [x] Unit tests pass (`_format_listening_progress`, `_show_listening_indicator`, `_stop_listening_indicator`).
- [x] Spec exists: `specs/raspberry-listening-indicator.md`.
- [x] Plan exists: `docs/plans/raspberry-listening-indicator.md`.

### Implementation Status

The following code is already on `main`:

| Function | Location | Purpose |
|---|---|---|
| `_format_listening_progress()` | `client/main.py:168` | Returns `"Listening: X/Ys"` string |
| `_show_listening_indicator()` | `client/main.py:172` | Daemon thread: prints countdown during capture |
| `_stop_listening_indicator()` | `client/main.py:185` | Signals thread to stop and joins |
| `capture_audio(show_progress=True)` | `client/main.py:98` | Voice loop already passes `show_progress=True` |

### Validation Steps (completed 2026-06-07)

1. Pull latest `main` on Raspberry:
   ```bash
   cd ~/tonto-kids-assistant
   git checkout main
   git pull
   ```

2. Activate venv and set env vars:
   ```bash
   source .venv/bin/activate
   export TONTO_BACKEND_URL=http://192.168.1.91:8000
   export TONTO_AUDIO_DEVICE=plughw:CARD=Device,DEV=0
   ```

3. Run the client:
   ```bash
   python3 client/main.py --mode voice
   ```

4. Complete at least 2 voice turns and confirm:
   - [ ] `Listening for 6s...` appears when recording starts.
   - [ ] `Listening: 1/6s`, `Listening: 2/6s`, ... updates live.
   - [ ] `Listening complete.` or `Uploading...` appears after capture ends.
   - [ ] Transcript, response, and espeak playback still work.
   - [ ] Text mode (`--mode text`) is unchanged.

5. Record evidence below.

### Evidence (2026-06-07)

**Environment:**
- Branch: `main` (synced with `origin/main`)
- Backend: `http://192.168.1.91:8000` (Windows, LAN mode)
- Raspberry audio device: `plughw:CARD=Device,DEV=0`
- Session: `local-session-9f5600d5-e159-484f-a961-d078753e8f9f`
- Commands used:
  ```bash
  git checkout main && git pull
  source .venv/bin/activate
  export TONTO_BACKEND_URL=http://192.168.1.91:8000
  export TONTO_AUDIO_DEVICE=plughw:CARD=Device,DEV=0
  python3 client/main.py --mode voice
  ```

**Turn 1:**
- Indicator visible: `Listening for 6s...` then `Listening: 1/6s` through `Listening: 6/6s` ✅
- `Listening complete.` appeared after capture ✅
- `Uploading...` transition clear ✅
- Transcript: `Esta es una prueba, esta es una prueba, esta es una prueba, esta es una prueba.`
- TONTO: `¡Hola! ¿Cómo te puedo ayudar hoy? Si tienes alguna pregunta o algo que quieras aprender, aquí estoy.`
- espeak: Audible ✅

**Turn 2:**
- Indicator visible: `Listening for 6s...` then `Listening: 1/6s` through `Listening: 6/6s` ✅
- `Listening complete.` appeared after capture ✅
- `Uploading...` transition clear ✅
- Transcript: `¿Cuál es la última película que se ha hecho sobre Superman?`
- TONTO: `La última película de Superman que se lanzó fue "Zack Snyder's Justice League" en 2021. También hay una nueva película de Superman en camino llamada "Superman: Legacy". ¿Te gusta Superman?`
- espeak: Audible ✅

**Observations:**

| Check | Result | Notes |
|---|---|---|
| Indicator visible during capture | ✅ | `Listening for 6s...` + live counter |
| Timer updates live | ✅ | 1/6s through 6/6s, 1 per second |
| Transition to uploading clear | ✅ | `Listening complete.` → `Uploading...` |
| Transcript works | ✅ | Both turns accurate |
| Response works | ✅ | Both turns coherent |
| espeak works | ✅ | Audible and understandable |
| ALSA/JACK warnings | ✅ Known, non-blocking | Same warnings as previous validations, do not affect capture or playback |

**Human judgment:**
- Does the indicator improve the demo operator experience? **Yes.** The operator now has clear visual feedback for when the child should stop speaking and when capture is complete. This directly addresses the Phase 3 UX gap.
- Any errors observed? **No.** Only the known ALSA/JACK warnings that have been present since Week 03.

### Acceptance Criteria

- [x] Listening indicator visible in terminal during audio capture.
- [x] Elapsed or remaining time updates live while recording.
- [x] Transition from listening to uploading is clear in the terminal.
- [x] Existing voice loop (transcript, response, espeak) still works.
- [x] Text mode (`--mode text`) is unchanged.
- [x] Evidence recorded in this journal section.

### Status

- [x] Raspberry hardware validation completed.
- [x] Evidence recorded above.
- [x] Issue #27 closed.

## Phase 5 — Week 04 Closeout (active 2026-06-07)

### Objective

End Week 04 with evidence, not loose impressions.

### Completed Work

| Phase | Status | Key Evidence |
|---|---|---|
| Phase 0: Kickoff | ✅ | Specs, plans, roadmap, journal created |
| Phase 1: Demo Baseline | ✅ | 3 voice turns on Raspberry, memory validated |
| Phase 2: Resilience | ✅ | Timeouts split, 48/48 tests passed |
| Phase 3: Calibration | ✅ | Prompt calibrated, 5 voice turns on Raspberry, 49/49 tests |
| Phase 4: Indicators | ✅ | Raspberry validated (2/2), web validated, issues #23/#25/#27 closed |
| Phase 5: Closeout | ✅ | This section |

### Open Issues at Close

- None. All Week 04 issues (#23, #25, #27) are closed.

### Risks for Week 05

- ALSA/JACK warnings persist but do not block demo.
- espeak remains robotic but understandable for MVP.
- Demo repeatability depends on manual env setup (backend URL, audio device).

### Recommended Next Action

Week 05 should focus on demo stability and experience polish per `docs/roadmap.md`.

## AI Tools Used

Codex: documentation kickoff (Phase 0); Phase 3 planning, prompt calibration, tests, and journal update. OpenCode: Phase 1 validation execution — repo inspection, test runs, backend startup, endpoint validation, journal update.

## Human Decisions

- The Week 04 kickoff product should be documentation and agent handoff material, not code.
- Week 04 should be phased before implementation.
- Arduino should not be treated as automatic implementation work.
- On 2026-06-07, Arduino/LEDs were explicitly deferred outside the 6-week MVP.
- On 2026-06-07, non-physical Raspberry and web listening/time indicators were approved as the first Phase 4 implementation path.
- On 2026-06-07, the web recording limit follow-up was decided: auto-stop at the configured limit, show a child-friendly limit warning, and keep `Enviar voz` manual.

## Notes

- The local branch was created as `docs-week-4-kickoff` because the sandboxed environment blocked writing slash-prefixed branch refs. The project convention remains `<type>/<short-kebab-description>` in normal Git workflows.
- Phase 1 branch follows project convention: `feature/week-04-phase1-demo-baseline`.
