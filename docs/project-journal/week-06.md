# Week 06 Kickoff

**Date:** 2026-06-14
**Status:** Phase 1 complete.

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
- No documented limitations list for the audience.
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
2. Known limitations.
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

Phase 2: create the known limitations document.

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
