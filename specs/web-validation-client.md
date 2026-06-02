# Web Validation Client - MVP Specification

**Version:** 0.3
**Status:** Active MVP Implementation; Phase 3 microphone audio loop validated; text chat spoken response enabled
**Last Updated:** June 2026

---

# Objective

Add a lightweight web client that helps validate the TONTO backend from a browser without requiring constant Raspberry Pi testing.

This client exists to speed up development, continuous integration, preview deployment, and demo preparation. It does not replace the Raspberry Pi client as the target product experience.

For Week 03 Phase 3, after the completed Phase 2B Raspberry capture/upload automation and post-TTS revalidation, the web client validated a browser-driven audio loop against the already implemented `POST /chat/audio` backend contract. The validated Phase 3 mission includes browser microphone capture, visible transcript, visible text response, and audible browser playback of the response.

After the Week 03 voice milestone, the web text chat flow also speaks backend responses aloud. A typed `/chat` turn still uses the stable JSON chat contract, displays the returned `response_text`, and then reuses native browser speech synthesis to play that same answer audibly. If speech synthesis is unsupported or playback fails, the written response remains available and the chat does not block.

---

# Initial Scope

## Included

- React + TypeScript + Vite scaffold.
- `TontoPage` as the main user/demo web surface.
- `AdminPage` as the technical validation panel.
- Browser-based `/chat` integration using the same backend contract as the Raspberry Pi client.
- Backend `/health` checks.
- Project scripts for development, typecheck, build, and preview.
- Clear folder structure for UI, API, and conversation state.
- Validated Phase 3 after completed Phase 2B revalidation: browser microphone audio validation loop using `POST /chat/audio`, visible transcript/response evidence, browser speech output, and latency/status instrumentation.
- Browser speech output for Phase 3 using native Web Speech API.
- Browser speech output for typed `/chat` responses using the same native Web Speech API path.

## Deferred

- Backend transcoding of `webm`, `ogg`, or other compressed browser audio formats.
- Visible WAV file picker or manual audio upload UI for product/demo use.
- Authentication.
- Persistence.
- Advanced routing.
- Component library setup beyond the initial styling foundation.

---

# Intended Architecture

```text
web/
  src/
    app/          # Application composition
    api/          # Future backend HTTP clients
    features/     # Future feature modules, starting with chat
    components/   # Shared UI components
    lib/          # Small reusable utilities
    pages/        # TontoPage and AdminPage
    styles/       # Global styles
```

The first real feature should be a chat validation screen that sends the same request contract used by the Raspberry Pi client:

```json
{
  "session_id": "string",
  "message": "string"
}
```

Typed chat responses are rendered in the conversation history and spoken from the browser when `speechSynthesis` is available:

```text
typed message -> POST /chat -> response_text -> visible chat response + browser speech
```

The Phase 3 audio feature uses the existing backend audio contract instead of adding a web-only endpoint:

```text
browser microphone -> WAV PCM mono -> POST /chat/audio -> transcript -> response text -> browser speech + UI evidence
```

The browser must not upload `webm` or `ogg` directly unless a later backend decision explicitly adds transcoding support. The implementation path is a small native browser WAV path with `getUserMedia` and Web Audio APIs, without adding a dependency. A manual WAV file picker is not part of the visible product/demo UI; WAV files may only be used as test fixtures or integration helpers.

---

# Technical Decisions

- Use React for the UI layer.
- Use TypeScript for maintainable client contracts.
- Use Vite for fast local development and simple build output.
- Use Tailwind CSS as the styling foundation.
- Keep shadcn/ui and Radix UI as the preferred path for future polished, accessible components.
- Do not add frontend state libraries until the app needs them.
- Do not add routing until there is more than one meaningful screen.
- Keep audio evidence in memory/UI only; do not persist recordings or transcripts by default.
- Reuse `OPENAI_STT_MODEL` backend behavior through `/chat/audio`; the web client must not know provider internals.
- Use native browser speech (`speechSynthesis`) for audible Phase 3 response playback; do not add backend TTS or frontend dependencies.
- Use the same native browser speech path for typed `/chat` responses; unsupported or failed speech playback degrades to text-only chat instead of failing the conversation.

---

# Phase 3 Audio Instrumentation

The implemented web loop makes these values visible for manual evidence capture:

- Backend URL and `/health` state.
- Browser microphone support and permission state.
- Browser/site microphone input must be the intended physical microphone. A wrong selected input can still produce a valid WAV upload but lead to empty STT/`422` because the backend receives no recognizable speech.
- Recording/encoding/upload/transcription status.
- Browser speech support and playback status.
- Recording duration.
- Generated WAV size and MIME type.
- `session_id`, `device_id=web-validation-client`, and `language=es`.
- `/chat/audio` HTTP status.
- Total browser-observed latency.
- Returned `transcript`.
- Returned `response`.
- Audible playback result for the returned response.
- Human-readable error message for permission, format, timeout, STT, and backend failures.

The final browser validation runbook and closure criteria are defined in `specs/audio-pipeline-phase-3-browser-manual-validation.md`. The closure validation passed on 2026-06-01 after selecting the correct browser microphone input.

---

# Text Chat Spoken Response

The web text composer remains the stable fallback and validation path for `POST /chat`. When a typed message receives a successful backend response, the client must:

- Keep the visible chat transcript as the source of truth for the response.
- Automatically speak the returned `response_text` with native browser speech synthesis.
- Show the existing speaking state while playback is active.
- Preserve the visible response and return the UI to an idle state even when browser speech is unsupported or playback fails.
- Keep `repeatLatest()` able to replay the latest assistant response whether it came from typed chat or microphone input.

This behavior does not add backend TTS, a new endpoint, a settings toggle, persistence, or extra dependencies.

---

# Acceptance Criteria

- [x] A `web/` project exists in the monorepo.
- [x] The project has `TontoPage` and `AdminPage`.
- [x] The project can be installed and built independently from backend/client code.
- [x] CI can run web typecheck/build.
- [x] The web client can use the same backend `/chat` contract as the Raspberry Pi client.
- [x] The web client can check backend health.
- [x] Phase 3 validated: the web client captures audio from the browser microphone and validates `POST /chat/audio` with a generated WAV compatible with the backend contract.
- [x] Phase 3 validated: the web client displays transcript, response, latency, and enough evidence to update `docs/project-journal/week-03.md`.
- [x] Phase 3 validated: the web client speaks the returned response audibly and understandably from the browser.
- [x] Phase 3 validated: the product/demo UI does not expose a manual WAV upload path.
- [x] Typed `/chat` responses are displayed and then spoken aloud automatically when browser speech synthesis is available.
- [x] Typed `/chat` remains usable as text-only fallback when browser speech synthesis is unavailable or playback fails.
