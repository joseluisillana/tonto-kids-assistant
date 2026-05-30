# Web Validation Client - MVP Specification

**Version:** 0.2
**Status:** Active MVP Implementation; Phase 3 audio loop planned
**Last Updated:** May 2026

---

# Objective

Add a lightweight web client that helps validate the TONTO backend from a browser without requiring constant Raspberry Pi testing.

This client exists to speed up development, continuous integration, preview deployment, and demo preparation. It does not replace the Raspberry Pi client as the target product experience.

For Week 03 Phase 3, after the completed Phase 2B Raspberry capture/upload automation and post-TTS revalidation, the web client is also the planned validation surface for a browser-driven audio loop against the already implemented `POST /chat/audio` backend contract.

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
- Planned Phase 3 after completed Phase 2B revalidation: browser audio validation loop using `POST /chat/audio`, visible transcript/response evidence, and latency/status instrumentation.

## Deferred

- Browser TTS.
- Backend transcoding of `webm`, `ogg`, or other compressed browser audio formats.
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

The Phase 3 audio feature should use the existing backend audio contract instead of adding a web-only endpoint:

```text
browser microphone or WAV file -> WAV PCM mono -> POST /chat/audio -> transcript -> response -> UI evidence
```

The browser must not upload `webm` or `ogg` directly unless a later backend decision explicitly adds transcoding support. The preferred implementation path is a small native browser WAV path with `getUserMedia` and Web Audio APIs, without adding a dependency. A manual WAV file picker is an acceptable first fallback if it helps validate instrumentation before live microphone capture.

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

---

# Phase 3 Audio Instrumentation

The planned web loop should make these values visible for manual evidence capture:

- Backend URL and `/health` state.
- Browser microphone support and permission state.
- Recording/encoding/upload/transcription status.
- Recording duration.
- Generated WAV size and MIME type.
- `session_id`, `device_id=web-validation-client`, and `language=es`.
- `/chat/audio` HTTP status.
- Total browser-observed latency.
- Returned `transcript`.
- Returned `response`.
- Human-readable error message for permission, format, timeout, STT, and backend failures.

---

# Acceptance Criteria

- [x] A `web/` project exists in the monorepo.
- [x] The project has `TontoPage` and `AdminPage`.
- [x] The project can be installed and built independently from backend/client code.
- [x] CI can run web typecheck/build.
- [x] The web client can use the same backend `/chat` contract as the Raspberry Pi client.
- [x] The web client can check backend health.
- [ ] Phase 3 planned: the web client can validate `POST /chat/audio` with a WAV compatible with the backend contract.
- [ ] Phase 3 planned: the web client displays transcript, response, latency, and enough evidence to update `docs/project-journal/week-03.md`.
