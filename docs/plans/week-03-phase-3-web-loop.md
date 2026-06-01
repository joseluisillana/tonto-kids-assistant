# Week 03 Phase 3 Web Voice Loop Handoff

## Objective

Implement the Phase 3 browser validation loop after the Raspberry Phase 2B post-TTS revalidation:

```text
browser microphone -> WAV PCM 16 kHz mono -> POST /chat/audio -> transcript -> response text -> browser speech
```

This is a web validation surface for the existing backend audio contract. It does not replace the Raspberry product path.

## Scope

Included:

- Capture a short Spanish voice turn from the browser microphone.
- Generate WAV PCM 16-bit, 16 kHz, mono in the browser with native APIs.
- Send the generated WAV to the existing `POST /chat/audio` multipart contract.
- Display transcript, text response, latency, status, and technical evidence in the web UI.
- Speak the returned response audibly from the browser using native Web Speech API.
- Keep the existing `/chat` text path working as the stable fallback.

Excluded:

- New backend endpoint.
- Runtime or development dependencies.
- Visible WAV file picker or manual audio upload UI.
- Direct upload of `webm`, `ogg`, or browser-compressed audio.
- Backend transcoding, `ffmpeg`, backend TTS, local STT, streaming, persistence, auth, or advanced product UI.

WAV files may be used only as test fixtures or integration helpers. They are not part of the user/demo web flow.

## Implementation Notes

- Prefer `navigator.mediaDevices.getUserMedia` for microphone permission and capture.
- Prefer Web Audio API for sample capture, mono conversion, downsampling to 16 kHz, and small WAV encoding.
- Use `FormData` fields aligned with the backend contract:
  - `audio`: generated WAV.
  - `session_id`: active web session.
  - `device_id`: `web-validation-client`.
  - `duration_ms`: approximate recorded duration.
  - `sample_rate_hz`: `16000`.
  - `channels`: `1`.
  - `language`: `es`.
- Use `window.speechSynthesis` for audible response playback, preferring Spanish voice/language such as `es-ES` when available.
- Surface browser capability failures as readable validation evidence: no microphone support, permission denied, no speech synthesis support, empty audio, unsupported backend response, timeout, or HTTP error.

## Acceptance Criteria

- `/chat` text flow remains unchanged and usable.
- A browser user can start a voice turn from the microphone.
- The web client sends a generated WAV accepted by `POST /chat/audio`.
- The UI shows real `transcript`, text `response`, latency, status, and technical evidence.
- The returned response is spoken audibly and understandably by the browser.
- No visible file upload is introduced.
- No backend contract or provider change is required.
- `docs/project-journal/week-03.md` receives manual validation evidence after implementation.

## Verification

Use official scripts after implementation:

```powershell
.\scripts\test.ps1 -Target python
.\scripts\test.ps1 -Target web
.\scripts\build.ps1 -Target web
git diff --check
git status --short --branch
```

## Implementation Prompt

```text
Implement the Week 03 Phase 3 Web Voice Loop for TONTO Kids Assistant.

Before editing:
- Read AGENTS.md.
- Read docs/ai-assisted-workflow.md.
- Read specs/audio-pipeline-phase-3-web-loop.md.
- Read specs/web-validation-client.md.
- Read this plan.
- Run git branch --show-current and git status --short --branch.
- Preserve unrelated user changes in the worktree.

Goal:
- Implement browser microphone -> WAV PCM 16 kHz mono -> POST /chat/audio -> transcript -> response text -> browser speech.

Constraints:
- Do not add a backend endpoint.
- Do not add runtime or development dependencies unless explicitly approved.
- Do not expose a visible WAV file picker or manual upload UI.
- Do not upload webm/ogg directly.
- Do not add backend transcoding, ffmpeg, backend TTS, local STT, streaming, persistence, auth, or advanced product UI.
- Preserve /chat as the stable text fallback.

Implementation:
- Use native browser APIs for microphone capture, WAV generation, and speech output.
- Send the existing multipart /chat/audio fields: audio, session_id, device_id=web-validation-client, duration_ms, sample_rate_hz=16000, channels=1, language=es.
- Display transcript, response text, latency, status, and technical evidence.
- Speak the returned response with browser speech synthesis when supported.
- Surface readable errors for microphone permission/support, empty audio, HTTP errors, timeouts, invalid responses, and speech support/playback failures.

Verification:
- Run .\scripts\test.ps1 -Target python.
- Run .\scripts\test.ps1 -Target web.
- Run .\scripts\build.ps1 -Target web.
- Run git diff --check.
- Run git status --short --branch.

Delivery:
- Summarize changed files.
- Summarize the voice-loop behavior implemented.
- Summarize verification results and any manual validation still required.
```
