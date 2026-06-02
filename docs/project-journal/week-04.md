# Week 04 Kickoff

**Date:** 2026-06-02
**Status:** Documentation kickoff prepared; implementation not started.

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

Start Phase 1.

Run the current system several times before adding behavior:

1. Run official checks if the local environment is ready.
2. Start backend with LAN access.
3. Validate `/health` from Windows and Raspberry.
4. Run at least three Raspberry `--mode voice` turns.
5. Confirm typed fallback still works.
6. Record latency, microphone device, TTS quality, and any failures here.

## AI Tools Used

Codex inspected repository instructions, roadmap, architecture, specs, plans, journal, hardware docs, and backend implementation. Codex prepared documentation-only kickoff artifacts and avoided code changes per the human request.

## Human Decisions

- The Week 04 kickoff product should be documentation and agent handoff material, not code.
- Week 04 should be phased before implementation.
- Arduino should not be treated as automatic implementation work.

## Validation

Documentation-only validation for this kickoff:

```powershell
git diff --check
git status --short --branch
```

No code tests are required for the kickoff because no implementation behavior changes.

## Notes

The local branch was created as `docs-week-4-kickoff` because the sandboxed environment blocked writing slash-prefixed branch refs. The project convention remains `<type>/<short-kebab-description>` in normal Git workflows.
