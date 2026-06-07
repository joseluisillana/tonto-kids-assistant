# Web Listening Indicator

**Version:** 0.2
**Status:** Planned for Week 04 Phase 4; recording limit decision recorded
**Last Updated:** 2026-06-07

## Objective

Improve the web validation client's voice experience by showing a visible listening/time indicator while browser audio capture is active, and by making the configured recording limit clear enough for a child to understand.

The web client already validates the browser microphone to `/chat/audio` loop. Phase 4 adds only the missing user feedback needed to know when TONTO is listening and how much recording time has elapsed or remains.

## User Experience Goal

When recording from the browser, the user should be able to see:

- TONTO is listening now.
- Recording time is moving.
- The current recording is still inside the accepted audio duration.
- Recording has stopped at the configured limit.
- The UI warns that the time is up.
- The user still decides when to send the captured voice.

The UI should remain a narrow validation/product surface. It should not become a broad dashboard.

## Scope

Included:

- Web voice UI feedback in the existing React/Vite client.
- Live elapsed time, remaining time, or progress against the relevant audio limit while recording.
- Automatic stop when the configured recording limit is reached.
- A simple, child-friendly warning when the limit is reached.
- Manual send remains available after auto-stop so the demo operator or child can choose when to upload.
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

### Recording Limit Decision

Human decision recorded on 2026-06-07:

- The web client must automatically stop capturing audio when the configured recording limit is reached.
- The UI must show a clear warning that the limit was reached.
- Sending remains manual after auto-stop. The client must not automatically upload just because the timer ended.
- The experience should stay simple and demo-friendly: a child should understand that TONTO has stopped listening and that the next step is to send the voice.

Minimal acceptable copy:

```text
Tiempo terminado. TONTO dejó de escuchar.
Pulsa Enviar voz para mandarlo.
```

The exact text may differ, but it should be short, friendly, and non-technical.

After recording stops, the existing upload/thinking/speaking/error statuses should remain visible and understandable.

## Implementation Constraints

- Use existing frontend patterns and dependencies.
- Do not add packages.
- Preserve the backend request shape and WAV compatibility.
- Do not expose a manual WAV upload/file picker.
- Keep the UI compact and demo-focused.
- Do not change the Raspberry client as part of this spec.
- Do not auto-upload audio when the recording limit is reached.
- Reuse the existing configured web validation recording limit rather than adding a second hard-coded timer.

## Acceptance Criteria

- Starting browser recording shows that TONTO is listening.
- The web UI shows live elapsed or remaining time while capture is active.
- Browser capture automatically stops at the configured recording limit.
- The web UI shows a clear, child-friendly warning when the recording limit is reached.
- After auto-stop, the user can still manually choose `Enviar voz`.
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
4. Let recording reach the configured limit without pressing `Enviar voz`.
5. Confirm capture stops automatically.
6. Confirm a child-friendly limit warning is visible.
7. Press `Enviar voz` manually.
8. Confirm upload, transcript, response, and browser speech still work.
9. Confirm the text fallback still works.

## Parallelization

This spec can be implemented independently from `specs/raspberry-listening-indicator.md`.

Both implementations must preserve the same backend contracts, but they do not need to share code.
