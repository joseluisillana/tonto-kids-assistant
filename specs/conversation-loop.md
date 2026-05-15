# Conversation Loop - MVP Specification

**Version:** 0.1
**Status:** Active MVP Spec
**Last Updated:** May 2026

---

# Objective

Validate the first functional end-to-end conversational loop of TONTO Kids Assistant.

The MVP flow must prove that:

1. A user can send a message from the Raspberry Pi client or the web validation client.
2. The backend can process the request using OpenAI.
3. TONTO can return a response.
4. The Raspberry Pi can reproduce that response using local TTS.

This is the first complete functional validation of the TONTO architecture.

---

# MVP Scope

## Included

- Manual text input
- HTTP communication
- Backend conversation processing
- OpenAI integration
- Local TTS using `espeak`
- Simple session context in memory
- Basic error handling
- Web validation client scaffold for browser-based backend testing

## Explicitly Out of Scope

- Speech-to-text (STT)
- Wake word detection
- Persistent memory
- Arduino integration
- Advanced product UI
- Multi-user support
- Authentication
- Offline AI models
- Advanced orchestration

---

# High-Level Flow

```text
User
  ↓
Raspberry Pi Client or Web Validation Client
  ↓
HTTP POST /chat
  ↓
Backend
  ↓
OpenAI
  ↓
Backend Response
  ↓
Raspberry Pi
  ↓
Local TTS (espeak)
  ↓
Audio Output
```

---

# System Responsibilities

## Raspberry Pi Client

Responsible for:

- reading user input,
- sending HTTP requests,
- receiving backend responses,
- reproducing local TTS,
- maintaining temporary session state,
- displaying simple logs/errors.

The Raspberry Pi is NOT responsible for:

- AI reasoning,
- long-term memory,
- orchestration,
- conversation logic.

---

## Web Validation Client

Responsible for:

- providing a browser-based way to test the backend,
- sending the same JSON request shape as the Raspberry Pi client,
- displaying backend responses and basic client-side states,
- supporting CI and independent frontend deployment experiments.

The web validation client is NOT responsible for:

- AI reasoning,
- long-term memory,
- orchestration,
- replacing the Raspberry Pi as the target product client.

---

## Backend

Responsible for:

- exposing the `/chat` endpoint,
- calling OpenAI,
- maintaining short conversation history in memory,
- generating conversational responses,
- returning structured JSON responses.

The backend is NOT responsible for:

- audio playback,
- hardware control,
- wake word detection,
- physical interaction.

---

# Initial MVP Flow

## Step 1 - Client Starts

The Raspberry Pi client starts locally:

```bash
python client/main.py
```

The client:

- creates a temporary session id,
- shows a terminal prompt,
- waits for user input.

---

## Step 2 - User Sends Message

Example input:

```text
What is 2 + 2?
```

The client builds a simple JSON request:

```json
{
  "session_id": "local-session-001",
  "message": "What is 2 + 2?"
}
```

The request is sent to the backend using HTTP POST.

---

## Step 3 - Backend Processes Message

The backend:

1. receives the request,
2. validates basic fields,
3. builds a minimal conversation context,
4. sends the request to OpenAI,
5. receives the AI response,
6. returns structured JSON.

Example response:

```json
{
  "success": true,
  "response_text": "2 + 2 equals 4."
}
```

---

## Step 4 - Raspberry Pi Reproduces Response

The client:

1. extracts `response_text`,
2. executes local TTS using `espeak`,
3. reproduces audio locally.

Example:

```bash
espeak "2 plus 2 equals 4"
```

---

## Step 5 - Loop Continues

The client waits for the next user input.

The same temporary session id is reused during execution.

---

# Initial API Contract

## Request

```json
{
  "session_id": "string",
  "message": "string"
}
```

---

## Response

```json
{
  "success": true,
  "response_text": "string"
}
```

---

# Acceptance Criteria

## AC1 - Client Execution

- [x] Raspberry Pi client starts correctly.
- [x] User can manually enter text.

---

## AC2 - Backend Communication

- [x] Client can send HTTP request to backend.
- [x] Backend responds successfully.

---

## AC3 - OpenAI Integration

- [x] Backend successfully calls OpenAI.
- [x] Response text is returned correctly.

---

## AC4 - Local TTS

- [x] Raspberry Pi reproduces response using `espeak`.
- [x] Audio is understandable.

---

## AC5 - End-to-End Loop

- [x] User can complete multiple conversation turns.
- [x] The system remains stable during repeated interactions.

Manual validation on 2026-05-15 confirmed repeated Raspberry -> backend LAN -> OpenAI -> local TTS turns on real hardware.

---

# Current Technical Decisions

## Confirmed

- Raspberry Pi 3 acts as thin client.
- Web validation client exists as a development/demo surface.
- Backend runs initially on Windows.
- Backend MVP implementation is Python/FastAPI.
- Go is deferred and excluded from CI gates until explicitly reactivated.
- HTTP + JSON communication.
- OpenAI as primary conversational engine.
- Local TTS on Raspberry Pi using `espeak`.

## Still Open

- Whether Go is worth re-evaluating after the Python/FastAPI MVP is validated.
- Persistent memory strategy.
- STT provider.
- Wake word implementation.
- Arduino integration details.

---

# Known MVP Limitations

- Input is manual text only.
- No persistent memory between executions.
- No offline mode.
- No advanced personality system.
- No voice recognition yet.
- No visual states yet.

These limitations are acceptable for the initial MVP validation phase.

---

# Risks

## Network Dependency

The system currently depends on backend connectivity and OpenAI availability.

---

## Raspberry Pi Resources

The Raspberry Pi 3 has limited CPU and RAM resources.

The client must remain lightweight.

---

## Latency

The conversational experience depends on response time between:

- Raspberry Pi,
- backend,
- OpenAI.

---

# MVP Simplification Rules

During implementation:

- simplicity is preferred over perfect architecture,
- premature optimization should be avoided,
- abstractions should remain minimal,
- technical debt is acceptable if it accelerates validation,
- any feature that does not directly improve the MVP demo should be postponed.

The goal is to validate the conversational loop as quickly and reliably as possible.

---

# Definition of Done

This spec is considered complete when:

- the Raspberry Pi client can communicate with the backend,
- OpenAI responses are returned successfully,
- local TTS works reliably,
- multiple conversation turns succeed,
- the system can be demonstrated consistently on real hardware.

---

# Related Backlog

## Immediate Priorities

- [x] Create backend skeleton
- [x] Create `/chat` endpoint
- [x] Connect OpenAI API
- [x] Create Raspberry Pi client
- [x] Implement HTTP communication
- [x] Implement local TTS playback
- [ ] Add basic logging
- [ ] Add minimal configuration handling

---

# Next Step

After the first end-to-end validation:

1. validate multiple repeated conversation turns,
2. improve basic logging and configuration handling,
3. stabilize the demo path for repeatable hardware runs.
