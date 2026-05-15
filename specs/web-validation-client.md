# Web Validation Client - MVP Specification

**Version:** 0.1
**Status:** Planning Scaffold
**Last Updated:** May 2026

---

# Objective

Add a lightweight web client that helps validate the TONTO backend from a browser without requiring constant Raspberry Pi testing.

This client exists to speed up development, continuous integration, preview deployment, and demo preparation. It does not replace the Raspberry Pi client as the target product experience.

---

# Initial Scope

## Included

- React + TypeScript + Vite scaffold.
- Minimal hello world screen.
- Project scripts for development, typecheck, build, and preview.
- Clear folder structure for future chat integration.

## Deferred

- Chat UI implementation.
- Backend `/chat` integration.
- Browser TTS.
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
    styles/       # Global styles
```

The first real feature should be a chat validation screen that sends the same request contract used by the Raspberry Pi client:

```json
{
  "session_id": "string",
  "message": "string"
}
```

---

# Technical Decisions

- Use React for the UI layer.
- Use TypeScript for maintainable client contracts.
- Use Vite for fast local development and simple build output.
- Use Tailwind CSS as the styling foundation.
- Keep shadcn/ui and Radix UI as the preferred path for future polished, accessible components.
- Do not add frontend state libraries until the app needs them.
- Do not add routing until there is more than one meaningful screen.

---

# Acceptance Criteria

- [x] A `web/` project exists in the monorepo.
- [x] The project has a minimal hello world screen.
- [x] The project can be installed and built independently from backend/client code.
- [x] CI can run web typecheck/build.
- [ ] A future chat screen can consume the same backend `/chat` contract as the Raspberry Pi client.
