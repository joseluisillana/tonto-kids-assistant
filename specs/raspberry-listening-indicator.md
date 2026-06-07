# Raspberry Listening Indicator

**Version:** 0.1
**Status:** Planned for Week 04 Phase 4
**Last Updated:** 2026-06-07

## Objective

Improve the Raspberry voice demo operator experience by showing a clear terminal indicator while TONTO is listening.

The Phase 3 Raspberry validation showed that the conversation loop works, but the operator does not have enough feedback for when the child should stop speaking. This spec adds a small non-physical time/listening indicator before any physical Arduino/LED work.

## User Experience Goal

When the Raspberry client starts recording, the terminal must make these facts obvious:

- TONTO is listening now.
- Recording has a fixed duration.
- The operator can see elapsed or remaining time while capture is active.
- Uploading starts only after listening ends.

The indicator is for the demo operator and Raspberry terminal session. It is not a product UI framework.

## Scope

Included:

- Raspberry client terminal feedback in `client/main.py --mode voice`.
- A live countdown, elapsed timer, or progress-style text during fixed-duration audio capture.
- Preservation of `TONTO_RECORD_SECONDS`, including the existing default and bounds.
- Preservation of the current WAV capture settings and `POST /chat/audio` contract.
- Focused Python tests for any helper or capture behavior changed by the implementation.
- Real Raspberry validation after implementation.

Excluded:

- Arduino, LEDs, GPIO, or physical state hardware.
- Wake word.
- Voice activity detection or automatic silence detection.
- Streaming audio.
- Local STT or local AI.
- Backend API changes.
- New runtime or development dependencies.
- Broad terminal UI redesign.

## Behavior

The Raspberry voice loop should keep the existing operator flow:

```text
press Enter -> record short WAV -> upload -> transcript/response -> speak
```

During the record step, the client should show a visible listening indicator for the configured recording duration. A minimal acceptable implementation is:

```text
Listening for 6s...
Listening: 1/6s
Listening: 2/6s
...
Uploading...
```

The exact text may differ, but it must be readable on a Raspberry terminal and must not hide errors from `arecord`.

## Implementation Constraints

- Use Python standard library only.
- Keep the Raspberry client as a thin client.
- Keep state local to the current process and current turn.
- Do not change the backend request payload, response parsing, or session behavior.
- Do not change the configured audio device behavior.
- If live progress requires changing `capture_audio`, keep the refactor narrow and testable.

## Acceptance Criteria

- Starting a voice capture shows that TONTO is listening.
- The terminal shows elapsed or remaining time while capture is active.
- The terminal clearly transitions from listening to uploading.
- Existing text mode behavior is unchanged.
- The generated WAV remains compatible with the backend.
- `duration_ms` still matches the configured capture duration.
- Relevant Python tests pass.
- A real Raspberry validation records commands, environment, result, and human judgment in `docs/project-journal/week-04.md`.

## Validation

Suggested Raspberry validation:

```bash
cd ~/tonto-kids-assistant
git status --short --branch
source .venv/bin/activate
export TONTO_BACKEND_URL=http://192.168.1.91:8000
export TONTO_AUDIO_DEVICE=plughw:CARD=Device,DEV=0
python3 client/main.py --mode voice
```

Validate at least two voice turns:

1. Confirm the listening indicator is visible during capture.
2. Confirm upload starts after the listening indicator completes.
3. Confirm transcript, response, and local `espeak` playback still work.

## Parallelization

This spec can be implemented independently from `specs/web-listening-indicator.md`.

Both implementations must preserve the same backend contracts, but they do not need to share code.
