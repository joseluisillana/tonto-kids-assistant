# Web validation context

Read [root](../AGENTS.md) and [workflow](../docs/ai-assisted-workflow.md) first.
For HTTP/audio changes also read [backend](../backend/AGENTS.md) and the affected
contracts. This client validates the physical product; it does not orchestrate AI.

## Structure and public interface

React/TypeScript/Vite. `src/main.tsx` starts the app; `src/app/App.tsx` and
`routes.ts` select TontoPage `/` and AdminPage `/admin`. Conversation state is
shared in memory by `src/features/conversation/useConversation.ts`.
`src/api/backendClient.ts` owns health/text/audio requests, timeout and response
validation; `src/types/conversation.ts` holds TypeScript contracts/state types.
`src/lib/audio.ts` encodes WAV and handles native browser speech; components and
pages consume these helpers. `package.json`, lockfile, Vite and tsconfig files
define tooling. `tests/run-tests.mjs` runs backendClient/audio-utils tests.

Depends on: backend HTTP, React, native microphone/Web Audio/speech browser APIs.
Used by: browser demo/technical operator pages; web tests import compiled helper
output under .tmp-test. No shared Python models or backend provider imports.
Text `/chat` returns success/response_text; audio returns session_id/transcript/
response. Changing these shapes affects backend and client tests as well.

## Impact and testing

Capture, WAV resampling and indicator timing changes affect useConversation,
VoiceLoopPanel and audio-utils tests. Keep compatible WAV, visible evidence,
text fallback, native speech degradation, auto-stop at limit and manual send.
Global Phase 3 constraints forbid a product WAV picker and direct webm/ogg upload.
Do not introduce backend TTS or provider UI through this validation work.

From root: `./tonto.sh setup`, `./tonto.sh dev web`, `./tonto.sh test web`,
`./tonto.sh build web`. Local dependencies stay in web/node_modules; task
commands use Compose, not host/global npm. package.json has typecheck/build/test/
preview scripts but no lint/format targets. Current Docker runtime supplies
VITE_BACKEND_URL explicitly and does not mount web/.env; the older README .env
instruction is not the Docker configuration path.

Read [web README](README.md), [validation spec](../specs/web-validation-client.md),
[Phase 3](../specs/audio-pipeline-phase-3-web-loop.md),
[manual validation](../specs/audio-pipeline-phase-3-browser-manual-validation.md),
[listening indicator](../specs/web-listening-indicator.md) and
[text speech plan](../docs/plans/web-text-chat-spoken-response.md) when affected.
Automated helper tests/build do not validate microphone permissions or audibility;
manual browser evidence follows the relevant spec.
