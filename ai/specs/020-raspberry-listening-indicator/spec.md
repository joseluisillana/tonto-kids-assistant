---
id: "020-raspberry-listening-indicator"
title: "Raspberry Listening Indicator"
status: done
owner: "Unknown — legacy ownership not recorded"
created: "2026-06-07"
updated: "2026-10-06"
related:
  - "specs/raspberry-listening-indicator.md"
  - "ai/specs/001-historical-records-migration/metadata-review.md"
  - "https://github.com/joseluisillana/tonto-kids-assistant/issues/18"
  - "https://github.com/joseluisillana/tonto-kids-assistant/issues/20"
  - "https://github.com/joseluisillana/tonto-kids-assistant/issues/27"
  - "docs/project-journal/week-04.md"
  - "ai/specs/020-raspberry-listening-indicator/plan.md"
---

# Raspberry Listening Indicator

**Version:** 0.1
**Status:** Implemented and validated on real hardware (2026-06-07)
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

- [x] Starting a voice capture shows that TONTO is listening.
- [x] The terminal shows elapsed or remaining time while capture is active.
- [x] The terminal clearly transitions from listening to uploading.
- [x] Existing text mode behavior is unchanged.
- [x] The generated WAV remains compatible with the backend.
- [x] `duration_ms` still matches the configured capture duration.
- [x] Relevant Python tests pass.
- [x] A real Raspberry validation records commands, environment, result, and human judgment in `docs/project-journal/week-04.md`.

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

Implemented validation evidence (2026-06-07):

- Branch: `main` (synced with `origin/main`)
- Backend: `http://192.168.1.91:8000` (Windows, LAN mode)
- 2/2 voice turns passed on `tonto-pi`
- Indicator visible: `Listening for 6s...` then `Listening: 1/6s` through `Listening: 6/6s`
- `Listening complete.` appeared after capture
- `Uploading...` transition clear
- Transcript, response, and espeak all working
- Known ALSA/JACK warnings (non-blocking, same as previous validations)
- Human judgment: indicator improves demo operator experience
- Issue #27 closed

## Parallelization

This spec can be implemented independently from `ai/specs/024-web-listening-indicator/spec.md`.

Both implementations must preserve the same backend contracts, but they do not need to share code.

## Migration provenance and supported current state

- Original repository source: `specs/raspberry-listening-indicator.md` at baseline 818e88e.
- First recorded Git date: 2026-06-07; actual original authoring date is unknown
  unless explicitly recorded in the preserved body.
- Last source Git date before migration: 2026-06-07.
- Migration/update date: 2026-10-06. Legacy owner/authorship is not established;
  the current owner field records that uncertainty, not a fabricated attribution.
- Status decision: Raspberry indicator accepted 2026-06-07 with two real voice turns; #20/#27 closed with evidence.
- Evidence: [source](../../../docs/project-journal/week-04.md).
- Corresponding GitHub tracking issues: [GitHub issue](https://github.com/joseluisillana/tonto-kids-assistant/issues/18), [GitHub issue](https://github.com/joseluisillana/tonto-kids-assistant/issues/20), [GitHub issue](https://github.com/joseluisillana/tonto-kids-assistant/issues/27).

Historical headings below/above retain the original reported state. YAML status
and this provenance annotation express the supported state after evidence review.
Do not execute archived proposals or historical operating examples without a new
authorized work item. No runtime or acceptance behavior changed by relocation.

Maintain plan.md/journal.md and synchronize status/updated with the parent INDEX.md
in the same change. No secrets, credentials, tokens, connection strings, PII or
real customer data; sensitive configuration is described by parameter name only.
