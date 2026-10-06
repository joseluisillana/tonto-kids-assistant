# Backend context

Read [root](../AGENTS.md) and the mandatory [workflow](../docs/ai-assisted-workflow.md)
first. For contract changes also read [client](../client/AGENTS.md),
[web](../web/AGENTS.md), [shared](../shared/AGENTS.md) and [tests](../tests/AGENTS.md).

## Purpose and key files

Python/FastAPI monolith owning conversation, provider calls and short in-process
history. `main.py` defines `app`, CORS, `/health`, `/chat` and text models;
`audio_router.py` defines `/chat/audio`, WAV validation and `AudioResponse`.
`openai_client.py` selects chat provider and extracts responses; `stt_client.py`
selects transcription; `state.py` shares bounded history between routes.
`provider_diagnostics.py` logs allowlisted failure metadata. `requirements.txt`
declares FastAPI/multipart/uvicorn; no backend Dockerfile exists, Compose uses a
Python image and mounted code. Read implementation before changing contracts.

## Public interface and dependencies

- `GET /health` → status. `POST /chat` JSON `{session_id, message}` →
  `{success: true, response_text}`; not the audio response shape.
- `POST /chat/audio` multipart includes audio WAV and session/duration/rate/channel
  metadata → `{session_id, transcript, response}`. Read audio_router/spec for
  optional fields, limits and errors; no compressed-format transcoding.
- Depends on: FastAPI/Pydantic, standard-library HTTP, runtime environment
  configuration and provider APIs. Routes call chat/STT adapters and state.
- Used by: client/main.py, web HTTP adapter, scripts health/smoke operations;
  tests/conftest.py and API/provider/diagnostics tests through imports/TestClient.
- `shared/models.py` is not imported here; no runtime Python import relationship
  to client/web. Public provider selection is backend-owned, not a client concern.

## Change impact and validation

Keep client HTTP consumers aligned with response shapes and errors. State changes
affect both text/audio routes. Provider edits preserve both adapters with mocks
and the fixed errors/allowlisted logs of #110; apply D025 before any real calls.
Read [inference specs](../specs/inference-providers.md), their
[plan](../docs/plans/inference-providers.md) and
[provider skill](../.agents/skills/devexpert-inference/SKILL.md) for adapter work.
Read [audio contract](../specs/audio-pipeline.md),
[conversation](../specs/conversation-loop.md) and
[secret protection](../specs/agent-secrets-protection.md) when affected.

Use `./tonto.sh test python` from root (API, audio, chat/STT and diagnostics tests).
Contract changes may require `./tonto.sh test web` and client/UI checks too.
Use `./tonto.sh dev backend` only when runtime operation is needed; setup/tests
use credential-free task Compose, not runtime env files. Test mocks do not
validate provider availability or audible speech.
