# Week 06 Kickoff

**Date:** 2026-06-14
**Status:** Phase 3 complete.

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

Known gaps for Week 06:
- No future work list for post-MVP.
- No final report for the AI Expert course.
- No final demo evidence recorded in journal.

## Prepared Documents

- `specs/week-06-closeout.md`
- `docs/plans/week-06-closeout.md`
- `docs/project-journal/week-06.md`
- `docs/demo-checklist.md`

## Proposed Week 06 Phases

0. Documentation kickoff and handoff for agents — completed 2026-06-14.
1. Demo checklist - completed 2026-06-14.
2. Known limitations - completed 2026-06-18.
3. Future work.
4. Final report.
5. Final demo evidence and closeout.

## GitHub Tracking

- Parent issue: #65
- Phase 0: #66
- Phase 1: #67
- Phase 2: #68
- Phase 3: #69
- Phase 4: #70
- Phase 5: #71

## Recommended Next Action

Phase 3: create the future work document.

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
