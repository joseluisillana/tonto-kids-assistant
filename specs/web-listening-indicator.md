# Web Listening Indicator

**Version:** 0.1
**Status:** Planned for Week 04 Phase 4
**Last Updated:** 2026-06-07

## Objective

Improve the web validation client's voice experience by showing a visible listening/time indicator while browser audio capture is active.

The web client already validates the browser microphone to `/chat/audio` loop. Phase 4 adds only the missing user feedback needed to know when TONTO is listening and how much recording time has elapsed or remains.

## User Experience Goal

When recording from the browser, the user should be able to see:

- TONTO is listening now.
- Recording time is moving.
- The current recording is still inside the accepted audio duration.
- Recording has stopped and the client is uploading or waiting for the backend.

The UI should remain a narrow validation/product surface. It should not become a broad dashboard.

## Scope

Included:

- Web voice UI feedback in the existing React/Vite client.
- Live elapsed time, remaining time, or progress against the relevant audio limit while recording.
- Integration with the existing conversation and capture state model.
- Preservation of the existing browser microphone to WAV to `/chat/audio` contract.
- Focused web tests or component/type coverage appropriate to the implementation.

Excluded:

- Manual WAV upload/file picker in product/demo UI.
- Backend audio format changes.
- Backend transcoding of browser `webm`/`ogg`.
- Streaming audio.
- Voice activity detection or automatic silence detection.
- New runtime or development dependencies.
- Broad UI redesign.
- Arduino, LEDs, or physical hardware state indicators.

## Behavior

During browser audio recording, the UI should show a clear listening state with time/progress. A minimal acceptable presentation is:

```text
Listening... 00:03 / 00:10
```

or an equivalent progress bar plus accessible text.

After recording stops, the existing upload/thinking/speaking/error statuses should remain visible and understandable.

## Implementation Constraints

- Use existing frontend patterns and dependencies.
- Do not add packages.
- Preserve the backend request shape and WAV compatibility.
- Do not expose a manual WAV upload/file picker.
- Keep the UI compact and demo-focused.
- Do not change the Raspberry client as part of this spec.

## Acceptance Criteria

- Starting browser recording shows that TONTO is listening.
- The web UI shows live elapsed or remaining time while capture is active.
- The indicator transitions cleanly into uploading/thinking/speaking/error states.
- Text chat fallback remains unchanged.
- `/chat/audio` remains the only voice backend contract.
- Web typecheck/tests/build pass through official scripts.
- Manual browser validation records evidence in `docs/project-journal/week-04.md`.

## Validation

Suggested local validation:

```powershell
.\scripts\test.ps1 -Target web
.\scripts\build.ps1 -Target web
.\scripts\dev.ps1 -Service backend -AllowLan
.\scripts\dev.ps1 -Service web
```

Manual browser checks:

1. Open the web client.
2. Start a voice capture with the correct microphone selected.
3. Confirm the listening indicator updates while recording.
4. Confirm upload, transcript, response, and browser speech still work.
5. Confirm the text fallback still works.

## Parallelization

This spec can be implemented independently from `specs/raspberry-listening-indicator.md`.

Both implementations must preserve the same backend contracts, but they do not need to share code.
