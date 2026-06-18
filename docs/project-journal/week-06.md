# Week 06 Kickoff

**Date:** 2026-06-14
**Status:** Complete.

## Objective

Close the TONTO MVP with documentation-only deliverables: a presentation checklist, known limitations, future work list, final report, and demo evidence.

## Current State at Kickoff

Week 05 is complete (Phases 0-5).

Validated paths:
- Raspberry voice loop: `client/main.py --mode voice` with listening indicator.
- Web voice loop: browser microphone with visible indicator and auto-stop.
- Text fallback: `POST /chat`.
- Backend: `POST /chat/audio` with STT via provider selection (OpenAI or DevExpert).
- In-memory session history.
- Prompt calibrated for Spanish, child-friendly, short answers.

Current test state:
- 78 Python tests pass.
- Web typecheck: passes.

Remaining gaps for Week 06:
- None. Final demo evidence was recorded on 2026-06-18.

## Prepared Documents

- `specs/week-06-closeout.md`
- `docs/plans/week-06-closeout.md`
- `docs/project-journal/week-06.md`
- `docs/demo-checklist.md`

## Proposed Week 06 Phases

0. Documentation kickoff and handoff for agents — completed 2026-06-14.
1. Demo checklist - completed 2026-06-14.
2. Known limitations - completed 2026-06-18.
3. Future work - completed 2026-06-18.
4. Final report - completed 2026-06-18.
5. Final demo evidence and closeout - completed 2026-06-18.

## GitHub Tracking

- Parent issue: #65
- Phase 0: #66
- Phase 1: #67
- Phase 2: #68
- Phase 3: #69
- Phase 4: #70
- Phase 5: #71

## Recommended Next Action

MVP closeout is complete. Next work should start from the post-MVP backlog in `docs/future-work.md`.

## Phase 1 - Demo Checklist

**Date:** 2026-06-14
**Status:** Complete.
**Tracking:** #67

Created `docs/demo-checklist.md` as the presentation-day operator checklist.

The checklist covers:
- presentation preconditions,
- provider selection for OpenAI and DevExpert,
- backend verification,
- Raspberry verification,
- optional web verification,
- recommended 5-7 turn demo sequence,
- Plan B fallbacks,
- final ready check,
- evidence to record after the final demo.

No code, script, dependency, API, or behavior changes were made.

## Phase 2 - Known Limitations

**Date:** 2026-06-18
**Status:** Complete.
**Tracking:** #68

Created `docs/known-limitations.md` as the audience-facing limitations document for the MVP closeout.

The document covers:
- robotic but functional `espeak` TTS quality,
- in-memory session history with no persistence,
- no wake word or continuous listening,
- no Arduino/LED physical states in the six-week MVP,
- LAN, internet, and provider dependency,
- single validated Raspberry hardware unit,
- expected turn latency,
- DevExpert verbosity compared to OpenAI,
- ALSA/JACK warnings suppressed or filtered but not eliminated at the OS/audio-stack level.

The document frames these as honest MVP boundaries and future productization areas rather than current presentation blockers.

No code, script, dependency, API, or behavior changes were made.

## Phase 3 - Future Work

**Date:** 2026-06-18
**Status:** Complete.
**Tracking:** #69

Created `docs/future-work.md` as the prioritized post-MVP backlog.

The document records the human decision to discard cloud deployment as a near-term post-MVP milestone. It explains that hosted deployment may become useful later for remote demos or multiple devices, but it is not the right next step because it adds operational, privacy, secret-management, and support complexity without improving the physical child-facing experience.

The first post-MVP priority is now the Raspberry touch UI with animated assistant face using the selected Waveshare 5" HDMI touch display. The planned direction keeps the Raspberry as a thin client: UI, touch controls, audio capture, and audio playback run on Raspberry, while the backend remains external and reachable through `TONTO_BACKEND_URL`. The existing Python terminal client remains the fallback path.

The backlog also covers better TTS, inference provider improvements, minimal session persistence, wake word exploration, Arduino/LED physical states, multi-user support, and metrics/demo diagnostics.

No code, script, dependency, API, or behavior changes were made.

## Phase 4 - Final Report

**Date:** 2026-06-18
**Status:** Complete.
**Tracking:** #70

Created `docs/final-report.md` as the AI Expert course final report.

The report expands the original outline into 10 substantive sections:
- project introduction,
- MVP scope,
- architecture,
- development process,
- AI-assisted development,
- implementation,
- validation,
- results,
- future work,
- appendix.

The content is based on repository evidence rather than new claims: Week 03 Raspberry audio validation, Week 04 demo stability and listening indicators, Week 05 OpenAI/DevExpert rehearsal evidence, Week 06 closeout docs, current specs, runbooks, limitations, and future work.

No code, script, dependency, API, or behavior changes were made.

## Phase 5 - Final Demo Evidence and Closeout

**Date:** 2026-06-18
**Status:** Complete.
**Tracking:** #71

Executed the final evidence pass following `docs/demo-checklist.md` and the official project helper scripts.

Environment:
- Branch: `docs/week-06-final-closeout`.
- Backend helper: `.\scripts\agent-backend.ps1 -Action start -AllowLan`.
- Raspberry helper: `.\scripts\agent-raspberry.ps1`.
- Backend LAN URL used by Raspberry: `http://192.168.1.91:8000`.
- Provider used: OpenAI.
- Raspberry host observed by preflight: `tonto-pi`.
- Raspberry repo: `/home/tonto-pi-user/tonto-kids-assistant`.

Validation steps:
- Backend `/health` passed locally.
- Text provider smoke passed through `/chat` with response `¡Ok!`.
- Raspberry preflight passed: identity, repo, `git`, `python3`, `curl`, `arecord`, `aplay`, `espeak`, `.venv/bin/python`, and backend `/health`.
- `arecord -l` showed `USB PnP Sound Device` as card 1, device 0.
- A configured capture test using `plughw:CARD=Device,DEV=0` produced a 3-second WAV successfully.

Observed issue and recovery:
- Two first Raspberry voice attempts reached the backend but returned `422` because STT did not detect recognizable speech.
- The issue was treated as a demo operation/timing problem, not a code defect.
- A coordinated retry used an audible `espeak` cue before capture so the speaker knew when to talk.

Successful voice evidence:

| Turn | Input spoken | Transcript | Result |
|---|---|---|---|
| 1 | Hola TONTO, como estas? | `Hola tonto, ¿cómo estás?` | Passed. TONTO answered with a friendly greeting and asked what to learn. |
| 2 | Que es una estrella? | `¿Qué es una estrella?` | Passed. TONTO gave a short child-friendly explanation and mentioned the Sun. |
| 3 | Y el Sol es una estrella? | `¿Y el Sol es una estrella?` | Passed. TONTO answered contextually that the Sun is the closest star to Earth and gives light and heat. |
| 4 | Gracias TONTO, hasta luego. | `Gracias, tonto. Hasta luego.` | Passed. TONTO gave a natural goodbye-style response. |

Latency and audio observations:
- Each Raspberry turn included the configured 6-second recording window.
- Backend responses completed within the Raspberry client's voice timeout.
- The successful 3-turn mini-demo completed as a single session without code changes.
- `espeak` produced audible output for the successful responses.
- Backend logs showed four successful `POST /chat/audio` responses after the two expected initial `422` attempts.

Fallback checks:
- Text fallback through `/chat` was checked with the provider smoke.
- Web voice was not rechecked during this closeout pass because it is optional for the presentation and was already validated in earlier Week 03/Week 04 evidence.

Final Definition of Done verification:
- [x] Demo funcional reproducible.
- [x] Arquitectura estable.
- [x] Flujo conversacional extremo a extremo.
- [x] Sistema presentable sin configuración manual compleja.
- [x] Proyecto documentado clara y manteniblemente.

Closeout result:
- Week 06 Phase 5 is complete.
- The TONTO MVP is ready for presentation within the documented MVP scope and limitations.
- No code, script, dependency, API, or behavior changes were made.
