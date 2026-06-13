# Week 05 Kickoff

**Date:** 2026-06-08
**Status:** Phases 0-2 complete.

## Objective

Prepare Week 05 so the next AI-assisted implementation pass starts from the real project state and a narrow MVP scope.

Week 04 is complete. The system has been validated end-to-end with listening indicators, conversation calibration, and demo resilience. Week 05 focuses on making the existing system demo-ready: clear startup, polished conversational UX, graceful error handling, and a successful multi-run rehearsal.

## Current State at Kickoff

Week 04 is complete (Phases 0-5).

Validated paths:
- Raspberry voice loop: `client/main.py --mode voice` with listening indicator.
- Web voice loop: browser microphone with visible indicator and auto-stop.
- Text fallback: `POST /chat`.
- Backend: `POST /chat/audio` with STT via OpenAI `gpt-4o-mini-transcribe`.
- In-memory session history.
- Prompt calibrated for Spanish, child-friendly, short answers.

Current test state:
- 52 Python tests pass.
- Web typecheck: to be verified.

Known gaps:
- Demo startup requires multiple manual commands.
- No single runbook for demo operators.
- Error messages are technical.
- ALSA/JACK warnings clutter terminal.
- No structured demo rehearsal evidence.

## Prepared Documents

- `specs/week-05-demo-stability.md`
- `docs/plans/week-05-demo-stability.md`
- `docs/project-journal/week-05.md`

## Proposed Week 05 Phases

0. Documentation kickoff and handoff for agents.
1. Demo runbook and startup scripts.
2. Conversational UX polish.
3. Error resilience.
4. Demo rehearsal (3+ consecutive runs).
5. Closeout with evidence.

## Recommended Next Action

Phase 1: create a demo runbook and startup script to reduce operator friction.
## Phase 1 — Demo Runbook and Startup Scripts (implemented 2026-06-07)

**Branch:** `feature/week-05-phase1-demo-runbook`
**Tracking:** GitHub issue #35

### Objective

Reduce the friction of starting a TONTO demo so an operator can start with 1-2 commands.

### Changes

**`scripts/demo-raspberry.sh`** (new):
- Bash script for Raspberry Pi demo startup.
- Default env vars: `TONTO_BACKEND_URL`, `TONTO_AUDIO_DEVICE`, `TONTO_RECORD_SECONDS`.
- Health check with 5 retries and 2s delay before starting.
- Activates venv and starts client in voice mode.
- Tracked as executable in git (mode 100755).

**`docs/demo-runbook.md`** (new):
- Prerequisites section.
- Quick start: 3 commands (backend, Raspberry, web).
- Full demo flow for Raspberry (5 steps).
- Full demo flow for web (5 steps).
- Known warnings (ALSA/JACK) documented as ignorable.
- Troubleshooting: 6 common failures with fixes.

### Validation Evidence (2026-06-08)

**Environment:**
- Branch: `feature/week-05-phase1-demo-runbook`
- Backend: `http://192.168.1.91:8000` (Windows, LAN mode)
- Raspberry audio device: `plughw:CARD=Device,DEV=0`
- Commands used:

```bash
chmod +x scripts/demo-raspberry.sh
./scripts/demo-raspberry.sh
```
**Observations (voice turns):**

| Check | Result | Notes |
|---|---|---|
| Health check (curl /health) | OK (1/5) | Backend responded immediately |
| Venv activation | OK | Activate found and sourced |
| Client starts in voice mode | OK | `--mode voice` launched correctly |
| Turn 1: indicator visible | OK | Live countdown 1-6s |
| Turn 1: transcript | Accurate | Transcription worked |
| Turn 1: response | Coherent | Spanish, child-friendly |
| Turn 1: espeak | Audible | Standard quality |
| Turn 2: indicator visible | OK | Same as turn 1 |
| Turn 2: transcript | Accurate | Transcription worked |
| Turn 2: response | Educational, coherent | Spanish, child-friendly |
| Turn 2: espeak | Audible | Standard quality |
| ALSA/JACK warnings | Known, non-blocking | Same as previous validations |

**Observations (health check retries):**

| Scenario | Result | Notes |
|---|---|---|
| Backend stopped | ERROR after 5 retries | Clear error message with instructions |
| Backend started mid-retries | Connected on attempt 5/5 | Recovery works correctly |
| Retry interval | 2s delay, ~7s total | `--connect-timeout 5` prevents hangs |
| Script executable in git | Fixed | Tracked as 100755, no manual chmod needed |

**Issues found and fixed during validation:**
- UTF-8 BOM at start of script caused warning (non-blocking). Fixed by saving without BOM.
- Venv setup instructions in script referenced PowerShell command. Fixed to show bash instructions.
- Backend requirements incorrectly included in venv setup message. Fixed to only include client requirements.
- `curl` hung without `--connect-timeout` when backend was unreachable. Fixed with 5s timeout.
- Script lost execute permissions after `git pull`. Fixed by tracking as 100755 in git.

**Human judgment:**
- The script reduces demo startup from 4 manual commands to 1.
- Health check provides clear feedback before starting, with retries and recovery.
- The operator experience is smoother than the previous manual setup.

### Acceptance Criteria

- [x] Demo operator can start with 1-2 commands.
- [x] Health check with reintentos funciona.
- [x] Runbook cubre flujo completo de demo Raspberry.
- [x] Runbook cubre flujo completo de demo web.
- [x] Warnings ALSA/JACK documentados como ignorables.
- [x] Troubleshooting cubre fallos comunes de ambos clientes.

### Status

- [x] Raspberry hardware validation completed.
- [x] All issues fixed.
- [x] Issue #35 ready to close.

## Phase 2 — Conversational UX Polish (implemented 2026-06-08)

**Branch:** `feature/week-05-phase2-conversational-ux`
**Tracking:** GitHub issue #36

### Objective

Make TONTO responses feel more natural and demo-ready for children while keeping
the MVP architecture unchanged.

### Changes

**`backend/openai_client.py`:**
- Kept the existing Spanish, child-friendly, short-answer requirement.
- Added guidance to start with a direct answer before adding supporting detail.
- Added guidance to use one simple example or comparison when useful.
- Added guidance to use simple accurate facts and avoid guessing.
- Added guidance to avoid long lists, markdown, and lecture-style answers.
- Added guidance for natural greetings/farewells with a gentle invitation to ask
  one small educational question.
- Reduced `MAX_OUTPUT_TOKENS` from `220` to `180` so spoken answers stay tighter
  for Raspberry `espeak` and browser speech (later raised to `300` in Phase 3
  fix, see below).

**`tests/test_openai_client.py`:**
- Updated the OpenAI payload test to verify the new conversational UX guidance.

### Demo Scenario Review

The Phase 2 prompt now explicitly supports the expected demo sequence:

| Scenario | Expected behavior |
|---|---|
| Greeting | Natural Spanish greeting, then a small educational invitation |
| Educational question | Direct answer first, then a short child-friendly explanation |
| Follow-up question | Uses recent in-memory context coherently |
| Farewell | Natural goodbye without introducing new architecture or state |

### Validation

- Automated validation: `tests/test_openai_client.py` checks the prompt payload
  includes Spanish, short answers, direct-answer style, no long lists/markdown,
  factual care, greeting/farewell guidance, recent context, and the configured
  token limit.
- Full Python suite: `.\scripts\test.ps1 -Target python` passed with 52/52 tests
  on 2026-06-08. The first sandboxed run hit a temp-file `PermissionError`; the
  same official command passed when rerun outside the sandbox.
- Full Python suite: `.\scripts\test.ps1 -Target python` passed with 52/52 tests
  on 2026-06-11 after the final factual-care prompt adjustment.

### Raspberry Validation Evidence (2026-06-11)

**Environment:**
- Branch: `feature/week-05-phase2-conversational-ux`
- Windows LAN IP from `ipconfig`: `192.168.1.91`
- Backend helper: `.\scripts\agent-backend.ps1 -Action start -AllowLan`
- Backend URL from Raspberry: `http://192.168.1.91:8000`
- Raspberry helper: `.\scripts\agent-raspberry.ps1`
- Raspberry identity: `tonto-pi` / `tonto-pi-user`
- Raspberry repo state during validation: `feature/week-05-phase1-demo-runbook`
  client, calling the Windows backend from this Phase 2 branch.

**Base checks:**

| Check | Result | Notes |
|---|---|---|
| `.\scripts\agent-backend.ps1 -Action start -AllowLan` | Passed | Backend started on `0.0.0.0:8000`; final validation PID was `28168`. |
| `.\scripts\agent-raspberry.ps1 -Action preflight` with `TONTO_BACKEND_URL=http://192.168.1.91:8000` | Passed | Confirmed SSH identity, repo, required tools, `.venv/bin/python`, and backend `/health` returned `{"status":"ok"}`. |
| First 6-question Raspberry run | Failed | Raspberry reached backend, but backend returned OpenAI 502 because it had been started inside the sandbox and inherited a blocking proxy. |
| Backend restart outside sandbox | Passed | Stopped recorded PID and restarted with the same official helper outside the sandbox so OpenAI calls could complete. |

**Final 6-question Raspberry text-mode run:**

The command executed on Raspberry via `agent-raspberry.ps1 -Action exec`, piping
six inputs into `.venv/bin/python client/main.py --mode text` with one generated
session ID: `local-session-e5866fdb-8930-430b-9ba2-081740636db8`.

| Turn | User input | Result |
|---|---|---|
| 1 | `Hola TONTO, ¿cómo estás?` | Warm Spanish greeting, short, invited a question. |
| 2 | `¿Qué es una estrella?` | Direct child-friendly explanation with a simple comparison. |
| 3 | `¿Y el Sol es una estrella?` | Coherent follow-up; confirmed the Sol is a star and related it to Earth. |
| 4 | `¿Por qué nos da luz y calor?` | Short educational answer; avoided the earlier incorrect "chemical reactions" phrasing after the factual-care prompt adjustment. |
| 5 | `¿Puedes recordarme qué te pregunté al principio?` | Correctly used session context and recalled the first educational question about stars. |
| 6 | `Gracias, adiós.` | Natural farewell in Spanish. |

**Observations:**
- The final run completed 6/6 Raspberry-originated questions successfully.
- Responses were Spanish, warm, short enough for the demo, and child-friendly.
- In-memory context worked across the sequence.
- Raspberry `espeak` ran after each answer; ALSA/JACK warnings appeared but were
  the already documented non-blocking Raspberry audio warnings.
- No architecture, dependency, persistence, or scope changes were introduced.

### Acceptance Criteria

- [x] TONTO prompt supports coherent demo question sequences.
- [x] Responses remain short, Spanish, child-friendly, and educational.
- [x] Raspberry real validation completed with 5+ demo questions.
- [x] Prompt changes are documented.
- [x] Prompt changes are covered by focused tests.

### Status

- [x] Code prompt polish implemented.
- [x] Focused test updated.
- [x] Full Python test suite passed.
- [x] Raspberry 5+ question validation completed.

## Extra — Agent Capability Pack Planning (created 2026-06-09)

**Branch:** `docs/week-05-agent-capability-pack`
**Tracking:** GitHub issue #43

### Objective

Plan a portable AI development asset so Codex, OpenCode, and future agents can operate common backend and Raspberry validation tasks through repo-owned documentation and PowerShell helpers.

### Context

During the attempt to complete Week 05 Phase 2, Codex correctly identified the need to validate 5+ demo questions on Raspberry, but started to improvise backend startup and Raspberry SSH commands. The project already has official PowerShell scripts and workflow docs, but it does not yet have a dedicated portable capability layer for agent-operated backend/Raspberry tasks.

### Documents Created

- `specs/week-05-agent-capability-pack.md`
- `docs/plans/week-05-agent-capability-pack.md`

### Decisions Captured

- The source of truth is repository Markdown plus official scripts, not a Codex-only skill.
- Tool-specific assets may wrap the capability pack later, but must delegate to repo-owned docs and scripts.
- Raspberry access should use a dedicated SSH key stored outside the repo.
- Password-based SSH automation and committed secrets are out of scope.

### Follow-up

After issue #43 is implemented, resume issue #36 and complete the Raspberry 5+ demo-question validation for Week 05 Phase 2.

## Step 3 — Agent Capability Pack Implementation (implemented 2026-06-09)

**Branch:** `feature/week-05-agent-capability-pack`
**Tracking:** GitHub issue #43

### Objective

Implement the portable Agent Capability Pack so AI-assisted agents and humans can use repository-owned helpers for backend lifecycle checks and Raspberry SSH preflight work.

### Changes

**`scripts/agent-backend.ps1`** (new):
- Supports `-Action start|stop|status|health`.
- Supports `-AllowLan` for Raspberry-accessible backend validation.
- Starts the backend in the background through `scripts/dev.ps1 -Service backend`.
- Stores process metadata and logs under `.cache/agent/`.
- Waits for `http://127.0.0.1:8000/health`.
- Stops only the PID recorded in `.cache/agent/backend.pid`.
- Uses an internal `scripts/dev.ps1 -Service backend` agent mode that starts uvicorn without reload and redirects logs from the Python process itself. This avoids a Windows background-process hang seen when `Start-Process` owned the stdout/stderr redirection for a long-running backend.

**`scripts/agent-raspberry.ps1`** (new):
- Supports `-Action preflight|exec`.
- Uses `TONTO_PI_HOST`, `TONTO_PI_USER`, `TONTO_PI_SSH_KEY`, `TONTO_PI_REPO`, and optional `TONTO_BACKEND_URL`.
- Uses OpenSSH with `BatchMode=yes`, `IdentitiesOnly=yes`, and `ConnectTimeout=5`.
- Does not automate passwords or print private key contents.
- Preflight checks SSH identity, repo presence, git status, required tools, and optional backend health from the Raspberry.
- Preflight also confirms `.venv/bin/python` exists in the Raspberry repo so project Python stays inside the virtual environment.

**`scripts/demo-raspberry.sh`** (updated):
- Starts the voice client with `.venv/bin/python` directly instead of relying on `source .venv/bin/activate` plus bare `python3`.

**Documentation:**
- `docs/raspberry-pi-setup.md` now documents dedicated SSH key generation, installation, validation, and revocation.
- `docs/ai-assisted-workflow.md` now documents the Capability Pack as the portable agent command surface.

**Test infrastructure:**
- `tests/conftest.py` now keeps the custom `tmp_path` fixture under repo-local `.cache/pytest-fixtures` and creates directories with `pathlib`, avoiding inaccessible Windows temp directories in sandboxed agent runs.

### Validation Evidence

| Check | Result | Notes |
|---|---|---|
| `.\scripts\agent-backend.ps1 -Action start -AllowLan` | Passed | Backend started in background, wrote PID/logs, and waited for `/health`. |
| `.\scripts\agent-backend.ps1 -Action health` | Passed | Returned `Health: ok`. |
| `.\scripts\agent-backend.ps1 -Action status` | Passed | Reported recorded PID alive and health OK. |
| `.\scripts\agent-backend.ps1 -Action stop` | Passed | Stopped the recorded PID only; follow-up `/health` was unavailable and no Python backend process remained. |
| Dedicated SSH key setup | Passed | Human generated and installed `tonto_agent_ed25519` with comment `tonto-agent`; exact key contents, fingerprint, and randomart are intentionally not recorded. |
| SSH key validation | Passed | Human validated `ssh -o BatchMode=yes -o IdentitiesOnly=yes -o ConnectTimeout=5 -i "$env:USERPROFILE\.ssh\tonto_agent_ed25519" tonto-pi-user@tonto-pi.local hostname` returned `tonto-pi`. |
| `.\scripts\agent-raspberry.ps1 -Action exec -Command "echo hello; hostname; whoami; pwd"` | Passed | Returned `hello`, `tonto-pi`, `tonto-pi-user`, and `/home/tonto-pi-user/tonto-kids-assistant` after changing the default host to `tonto-pi.local`. |
| `.\scripts\agent-raspberry.ps1 -Action preflight` | Passed | Confirmed SSH identity, repo path, git status, required tools, and `.venv/bin/python` at `/home/tonto-pi-user/tonto-kids-assistant/.venv/bin/python` after changing the default host to `tonto-pi.local`. |
| `.\scripts\agent-raspberry.ps1 -Action preflight` with `TONTO_BACKEND_URL=http://192.168.1.99:8000` | Failed as expected | Raspberry could not connect because `192.168.1.99` was not the current Windows PC LAN IP. |
| `.\scripts\agent-raspberry.ps1 -Action preflight` with `TONTO_BACKEND_URL=http://192.168.1.91:8000` | Passed | Raspberry reached backend health and returned `{"status":"ok"}`. |
| `.\scripts\test.ps1 -Target python` | Passed | 52 tests passed. |
| `bash -n scripts/demo-raspberry.sh` | Blocked | Local Bash/WSL returned `Access is denied` in this Windows session. |

### Issues Found and Fixed

- Initial backend helper attempts hung in the Codex desktop shell because `Start-Process` owned redirected stdout/stderr for a long-running uvicorn process. Fixed by having the Python runner redirect its own logs and by disabling uvicorn reload for agent background startup.
- `uvicorn --reload` in background produced repeated Windows `multiprocessing.resource_sharer` `PermissionError: [WinError 5] Access is denied` traces. Fixed by keeping reload enabled for normal human `scripts/dev.ps1` use but disabling it only for agent background mode.
- Test runs initially failed because the custom `tmp_path` fixture used temp directories that were inaccessible under this sandbox. Fixed by creating fixture directories under repo-local `.cache/pytest-fixtures`.
- Raspberry backend health initially failed because `TONTO_BACKEND_URL` pointed to stale LAN IP `192.168.1.99`. The current Windows PC LAN IP was `192.168.1.91`, and preflight backend health passed with `http://192.168.1.91:8000`.

### Status

Issue #43 was completed and closed after PR #45 merged. Real Raspberry preflight passed after setting the default host to `tonto-pi.local`, and the pack is now the official agent command surface for backend and Raspberry operations.

## Extra — Inference Providers / DevExpert Inference Planning (created 2026-06-13)

**Branch:** `docs/inference-providers-line`
**Tracking:** GitHub parent issue #48; phase issues #50, #51, #49, #52; future backlog #53

### Objective

Plan an extra MVP line so TONTO can run the same backend-facing demo contracts with either OpenAI or DevExpert Inference.

This supports the AI Expert course context without changing the MVP product goal. Raspberry and web clients should remain provider-agnostic; the backend should select the provider at startup configuration.

### Documents Created

- `specs/inference-providers.md`
- `specs/inference-provider-openai.md`
- `specs/inference-provider-devexpert.md`
- `docs/plans/inference-providers.md`
- `.agents/skills/devexpert-inference/SKILL.md`
- `.agents/skills/devexpert-inference/references/endpoint-summary.md`

### Decisions Captured

- Treat this as an extra MVP line, not Week 05 Phase 3.
- Document the current OpenAI provider baseline before implementation changes begin.
- Keep OpenAI and DevExpert support behind backend provider adapters.
- OpenAI may continue using `/v1/responses` for text generation.
- DevExpert should use its documented `/v1/chat/completions` endpoint for text generation.
- Both providers should support STT through provider-specific `/audio/transcriptions`.
- Do not implement hot switching, fallback, balancing, DevExpert TTS, Gemini, or frontend provider selection in the initial phases.
- Add a repo-local Agent Skill so skills-compatible agents can discover DevExpert Inference guidance without relying on Codex-only local skills.

### Proposed PR Strategy

Open one initial documentation PR from `docs/inference-providers-line` to `main` that only adds planning, skill, and tracking context.

After that PR merges:

1. implement the chat provider adapter in its own feature branch,
2. implement the STT provider adapter in a second feature branch after chat provider selection is stable,
3. update runbooks/scripts and record dual-provider validation in a final focused branch.

### Status

Planning in progress. No runtime behavior changed in this phase. GitHub tracking issues were created for the parent line, implementation phases, and future backlog.

## Extra — Inference Providers Phase 1: Chat Provider Adapter (implemented 2026-06-13)

**Branch:** `feature/inference-provider-chat-adapter`
**Tracking:** GitHub issue #51

### Objective

Add backend text-generation provider selection while preserving TONTO's public `/chat` and `/chat/audio` response contracts.

### Changes

**`backend/openai_client.py`:**
- Added `TONTO_INFERENCE_PROVIDER=openai|devexpert` selection through `call_inference`.
- Kept OpenAI text generation on `https://api.openai.com/v1/responses`.
- Added DevExpert chat generation through `DEVEXPERT_BASE_URL + /chat/completions`.
- Added DevExpert defaults: `DEVEXPERT_BASE_URL=https://inference.devexpert.io/v1` and `DEVEXPERT_CHAT_MODEL=mimo-v2.5`.
- Kept the shared TONTO child-friendly Spanish instructions for both providers.
- Added clear errors for unsupported providers and missing `DEVEXPERT_API_KEY`.
- Added timeout handling for provider text requests without exposing secrets.

**`backend/main.py` and `backend/audio_router.py`:**
- Switched text response generation to `call_inference`.
- Kept request/response contracts unchanged.
- STT provider selection is not implemented in this phase; `/chat/audio` still uses the existing STT client before calling the selected text provider.

**Tests:**
- Updated audio endpoint mocks from `call_openai` to `call_inference`.
- Added focused tests for OpenAI default routing, DevExpert routing, DevExpert default URL/model, missing DevExpert key, unsupported provider, and DevExpert timeout behavior.

### Validation

- `.\scripts\test.ps1 -Target python` passed with 58/58 tests.

### Status

Implemented. Phase 2 followed with STT provider selection.

## Extra — Inference Providers Phase 2: STT Provider Adapter (implemented 2026-06-13)

**Branch:** `feature/inference-provider-stt-adapter`
**Tracking:** GitHub issue #49

### Objective

Extend provider selection to backend STT while preserving `/chat/audio` request validation and response shape.

### Changes

**`backend/stt_client.py`:**
- Added `TONTO_INFERENCE_PROVIDER=openai|devexpert` selection for STT.
- Preserved OpenAI `/audio/transcriptions` behavior and `OPENAI_STT_MODEL`.
- Added DevExpert `/audio/transcriptions` behavior with `DEVEXPERT_BASE_URL` and `DEVEXPERT_STT_MODEL`.
- Kept the same multipart WAV upload shape with `model`, `language`, `response_format=json`, and `file`.
- Added clear errors for unsupported providers and missing `DEVEXPERT_API_KEY`.

**Tests:**
- Preserved existing OpenAI STT tests as the default path.
- Added focused DevExpert STT tests for custom URL/model, default URL/model, missing key, and unsupported provider.

### Validation

- `.\scripts\test.ps1 -Target python` passed with 62/62 tests.

### Status

Implemented. Phase 3 remains responsible for runbook/scripts and real dual-provider validation guidance.

## Extra — Inference Providers Phase 3: Runbook and Dual-Provider Operation (implemented 2026-06-13)

**Branch:** `docs/inference-provider-runbook`
**Tracking:** GitHub issue #52

### Objective

Document the operator path for running TONTO with either OpenAI or DevExpert without adding extra script surface area.

### Decision

No new script flag is added in this phase. `scripts/dev.ps1` and `scripts/agent-backend.ps1` already inherit environment variables from the starting shell, so `TONTO_INFERENCE_PROVIDER=openai|devexpert` is the simplest startup mechanism.

### Changes

- Added root `.env.example` as a safe provider-variable reference; scripts do not auto-load it.
- Updated `docs/demo-runbook.md` with OpenAI and DevExpert backend startup commands.
- Added a provider smoke check for `/chat`.
- Updated `README.md` setup guidance to show OpenAI and DevExpert provider selection.
- Updated specs, roadmap, and plan status through Phase 3.

### Validation

- `.\scripts\test.ps1 -Target python` passed with 62/62 tests after provider adapter changes.
- `git diff --check` passed.
- Real credential-backed OpenAI/DevExpert calls were not run in this phase to avoid assuming local secrets or consuming quota automatically.

### Status

Implemented through Phase 3. Future fallback, balancing, DevExpert TTS, and Gemini remain tracked separately in issue #53.

## Extra — Inference Providers Real Credential Validation (validated 2026-06-13)

**Branch:** `docs/inference-provider-real-validation`
**Tracking:** GitHub parent issue #48 (closed)

### Objective

Validate that the implemented inference provider layer works end-to-end with real API credentials for both OpenAI and DevExpert, without changing architecture or adding features.

### Validation Evidence

**Environment:**
- Branch: `docs/inference-provider-real-validation` (from `main`)
- Backend: `http://127.0.0.1:8000` via `agent-backend.ps1 -Action start -AllowLan`
- Python tests: 62/62 passed
- `git diff --check`: clean

#### A. OpenAI Real Validation

| Check | Result | Notes |
|---|---|---|
| Provider env | `$env:TONTO_INFERENCE_PROVIDER="openai"` | |
| Models | `OPENAI_MODEL=gpt-4o-mini`, `OPENAI_STT_MODEL=gpt-4o-mini-transcribe` | |
| `/health` | OK | `{"status":"ok"}` |
| `POST /chat` smoke | OK | `success: true`, `response_text` in Spanish, child-friendly |
| Latency (chat) | ~1.3-2.0s | Two consecutive calls measured |
| STT + chat (web voice) | OK | Browser microphone via web client at `http://127.0.0.1:5173/` |

**Voice test (OpenAI STT + chat) — Web:**
- User spoke: "¿Qué es un planeta?"
- STT transcript: accurate
- TONTO response: child-friendly Spanish explanation about planets orbiting a star, with Earth as example. Correct system prompt behavior.

**Voice test (OpenAI STT + chat) — Raspberry:**
- User spoke Spanish: "¿Qué es un planeta?" → transcript accurate, response in Spanish, child-friendly. Correct.
- User spoke Catalan: "Què és un planeta?" → transcript accurate (Catalan detected), but TONTO responded in Catalan instead of Spanish. The system prompt says "Always answer in Spanish" but the model matched the input language. This is a model behavior edge case, not a provider integration issue; the STT and chat pipeline worked correctly.

#### B. DevExpert Real Validation

| Check | Result | Notes |
|---|---|---|
| Provider env | `$env:TONTO_INFERENCE_PROVIDER="devexpert"` | |
| Base URL | `https://inference.devexpert.io/v1` | |
| Chat model | `mimo-v2.5` | |
| STT model | `gpt-4o-mini-transcribe` | |
| `/health` | OK | `{"status":"ok"}` |
| `POST /chat` smoke | OK | `success: true`, `response_text` in Spanish, child-friendly |
| Latency (chat) | ~2.0-2.9s | Two consecutive calls measured |
| STT + chat (web voice) | OK | Browser microphone via web client at `http://127.0.0.1:5173/` |

**Voice test (DevExpert STT + chat) — Web:**
- User spoke: "¿Cuántos planetas hay?"
- STT transcript: accurate
- TONTO response: listed 8 planets with size facts, child-friendly Spanish. Correct system prompt behavior.

**Voice test (DevExpert STT + chat) — Raspberry:**
- User spoke: "¿Qué es una estrella?"
- STT transcript: accurate
- TONTO response: child-friendly Spanish explanation comparing stars to distant suns. Correct system prompt behavior. Response was more verbose than typical OpenAI, consistent with `mimo-v2.5` model behavior noted earlier.

**Sample response to "Responde solo: ok":**
- DevExpert `mimo-v2.5` produced a longer child-friendly Spanish greeting.
- The model tends to be more verbose than OpenAI `gpt-4o-mini` for simple prompts.
- Provider integration worked correctly: request routed to DevExpert `/chat/completions`, response extracted, TONTO contract preserved.

**Observation on model behavior:**
- DevExpert `mimo-v2.5` appears more conversational/verbose than OpenAI `gpt-4o-mini` for the same TONTO system prompt.
- This is a model behavior difference, not a provider integration issue.
- For demo consistency, an operator may prefer to adjust `DEVEXPERT_CHAT_MODEL` if shorter answers are needed, but this is not a blocker.
- **Update (2026-06-13):** The verbosity combined with the 180-token limit caused responses to truncate mid-sentence. Fixed in #59 by raising `MAX_OUTPUT_TOKENS` to 300.

#### C. Automated Tests

| Check | Result |
|---|---|
| `.\scripts\test.ps1 -Target python` | 62/62 passed |
| `git diff --check` | Clean |

### Summary

Both OpenAI and DevExpert providers work end-to-end with real credentials. The provider selection mechanism (`TONTO_INFERENCE_PROVIDER`), chat generation, STT transcription, response extraction, and TONTO public contracts (`/chat`, `/chat/audio`) are all functional. No architecture changes, no new dependencies, no fallback/balancing implemented.

### Next Steps

- If DevExpert `mimo-v2.5` verbosity is a demo concern, consider testing alternative models (tracked in #53).
- Future: fallback, balancing, DevExpert TTS, Gemini (all tracked in #53).

## Bug Fix — DevExpert response truncation (fixed 2026-06-13)

**Branch:** `fix/devexpert-max-tokens-truncation`
**Tracking:** GitHub issue #59, PR #60

### Problem

DevExpert responses were cut off mid-sentence. Example:

- **Input:** "¿Qué le pasó a la gente que no pudo ser rescatada cuando naufragó el Titanic?"
- **Before fix (180 tokens):** "Muchas personas que no pudieron subirse a los botes salvavidas terminaron en el agua muy fría del océano. Las personas que no pudieron" — truncated, `finish_reason: length`.
- **After fix (300 tokens):** Complete response with explanation and follow-up question (363 chars).

### Root Cause

`MAX_OUTPUT_TOKENS = 180` was insufficient for Spanish text. Spanish uses more tokens than English; 180 tokens could not fit 2-3 child-friendly sentences with examples.

### Fix

- Increased `MAX_OUTPUT_TOKENS` from `180` to `300` in `backend/openai_client.py:32`.
- All 62 Python tests pass.
- Manual verification shows complete responses for the same Titanic question.

### Validation

| Test | Result |
|---|---|
| `.\scripts\test.ps1 -Target python` | 62/62 passed |
| Titanic question (pre-fix) | 143 chars, truncated |
| Titanic question (post-fix) | 363 chars, complete |
| Smoke check (`Responde solo: ok`) | OK |

## Phase 3 — Error Resilience (implemented 2026-06-13)

**Branch:** `fix/week-05-phase3-error-resilience`
**Tracking:** GitHub issue #37

### Objective

Make demo failures understandable and recoverable for the operator.

### Changes

**`client/main.py`:**

- **Operator-friendly error messages:** Replaced technical messages with clear, actionable text:
  - `arecord` not found → `"Recording tool not found. Make sure the microphone is connected and alsa-utils is installed."`
  - `arecord` fails → `"Recording failed. Check that the microphone is connected and not in use by another program."`
  - WAV not created → `"Recording did not produce an audio file. The microphone may not be working."`
  - Backend unreachable → `"Could not reach the backend. Make sure it is running and accessible."`
  - Backend timeout → `"Backend took too long to respond. It may be slow or unreachable."`
  - Audio 413 → `"Recording is too long. Try a shorter question."`
  - Audio 400 → `"Could not understand the recording. Try speaking more clearly."`
  - TTS not found → `"Speech output not available. Make sure espeak is installed."`
  - TTS failure → `"Speech output failed. The response is shown above as text."`

- **ALSA/JACK warning suppression:**
  - `speak()` now redirects stderr to `subprocess.DEVNULL`, suppressing ALSA/JACK noise from espeak.
  - `capture_audio()` filters ALSA/JACK/Unknown PCM lines from arecord stderr before printing, showing only real errors.

- **Recovery:** Client already recovered from errors (returns `None` and continues loop). No changes needed.

**`tests/test_client.py`:**
- Added `_filter_alsa_warnings` import.
- Added 11 new focused tests:
  - `test_filter_alsa_warnings_removes_alsa_lines`
  - `test_filter_alsa_warnings_removes_unknown_pcm`
  - `test_filter_alsa_warnings_removes_cannot_find_card`
  - `test_filter_alsa_warnings_returns_empty_for_only_alsa`
  - `test_filter_alsa_warnings_returns_empty_for_empty_input`
  - `test_capture_audio_prints_friendly_message_when_arecord_not_found`
  - `test_capture_audio_prints_friendly_message_when_arecord_fails`
  - `test_capture_audio_filters_alsa_warnings_from_stderr`
  - `test_send_message_prints_friendly_message_on_timeout`
  - `test_send_message_prints_friendly_message_on_url_error`
  - `test_send_audio_prints_friendly_message_for_413`
  - `test_send_audio_prints_friendly_message_for_400`
  - `test_send_audio_prints_friendly_message_on_timeout`
  - `test_speak_prints_friendly_message_when_not_found`
  - `test_speak_prints_friendly_message_on_failure`
  - `test_speak_suppresses_stderr`

### Validation

| Check | Result |
|---|---|
| `.\scripts\test.ps1 -Target python` | 78/78 passed |
| `.\scripts\test.ps1 -Target web` | Web typecheck passed |
| Error messages | Operator-friendly, no stack traces |
| ALSA/JACK warnings | Suppressed in speak(), filtered in capture_audio() |
| Client recovery | Continues loop after errors |

### Acceptance Criteria

- [x] Common demo failures show a clear, non-technical message.
- [x] Client recovers from errors and can continue the demo.
- [x] ALSA/JACK warnings are suppressed (speak) and filtered (capture_audio).

### Status

- [x] Code changes implemented.
- [x] Focused tests added.
- [x] Full test suite passes.
- [x] Hardware validation completed (4/4 voice turns on Raspberry).

### Hardware Validation Evidence (2026-06-13)

**Environment:**
- Branch: `fix/week-05-phase3-error-resilience`
- Backend: `http://192.168.1.91:8000` (Windows, LAN mode)
- Raspberry audio device: `plughw:CARD=Device,DEV=0`
- `TONTO_RECORD_SECONDS`: 6 (default)

**4-turn voice validation:**

| Turn | Input | Transcript | Response | espeak | ALSA warnings |
|---|---|---|---|---|---|
| 1 | "Hola tonto, ¿cómo estás?" | Exact | Natural greeting + invitation | OK | None visible |
| 2 | "¿Qué es un planeta?" | Exact | Child-friendly definition with example | OK | None visible |
| 3 | "¿Cuántos planetas hay?" | Exact | 8 planets + follow-up question | OK | None visible |
| 4 | "Gracias, adiós." | Exact | Natural farewell | OK | None visible |

**Observations:**
- All 4 voice turns completed without errors.
- ALSA/JACK warnings fully suppressed in terminal output.
- Listening indicator visible (6/6s) on every turn.
- STT transcription accurate on all turns.
- Responses in Spanish, short, child-friendly, educational.
- In-memory context worked (turn 3 follow-up was coherent with turn 2).
- No technical error messages shown to operator.

## Phase 4 — Demo Rehearsal (validated 2026-06-13)

**Branch:** `docs/week-05-phase4-demo-rehearsal`
**Tracking:** GitHub issue #38

### Objective

Prove the demo works repeatedly with both supported inference providers.

### Environment

- Backend: `http://192.168.1.91:8000` (Windows, LAN mode)
- Raspberry: `tonto-pi` / `tonto-pi-user`
- Audio device: `plughw:CARD=Device,DEV=0`
- `TONTO_RECORD_SECONDS`: 6 (default)
- Session: single session per provider run

### A. Primary Provider — OpenAI (6 voice turns)

**Provider config:**
- `TONTO_INFERENCE_PROVIDER=openai`
- `OPENAI_MODEL=gpt-4o-mini`
- `OPENAI_STT_MODEL=gpt-4o-mini-transcribe`

**Smoke check:** `POST /chat` with `Responde solo: ok` → OK

**Voice turns:**

| Turn | Input | Transcript | Response | espeak | ALSA |
|---|---|---|---|---|---|
| 1 | "Hola tonto, ¿cómo estás?" | Exact | Natural greeting + invitation | OK | None |
| 2 | "¿Qué es el Sol?" | Exact | Child-friendly explanation with comparison ("como una gran lámpara en el cielo") | OK | None |
| 3 | "Es una estrella." | Exact | Confirmed and expanded | OK | None |
| 4 | "Porque nos dá luz e calor." | Exact | Confirmed and explained | OK | None |
| 5 | "¿Por qué nos da luz y calor?" | Exact | Simplified explanation (gases, energy) | OK | None |
| 6 | "Gracias. Adiós." | Exact | Natural farewell | OK | None |

**Observations:**
- 6/6 voice turns completed without errors.
- STT transcription accurate on all turns.
- Responses in Spanish, short, child-friendly, educational.
- In-memory context worked across the sequence.
- ALSA/JACK warnings fully suppressed.
- Listening indicator visible (6/6s) on every turn.
- No technical error messages shown to operator.

### B. Alternative Provider — DevExpert (1 smoke turn)

**Provider config:**
- `TONTO_INFERENCE_PROVIDER=devexpert`
- `DEVEXPERT_CHAT_MODEL=mimo-v2.5`
- `DEVEXPERT_STT_MODEL=gpt-4o-mini-transcribe`

**Smoke check:** `POST /chat` with `Responde solo: ok` → OK

**Voice turn:**

| Turn | Input | Transcript | Response | espeak | ALSA |
|---|---|---|---|---|---|
| 1 | "¿Qué es un planeta?" | Exact | Child-friendly definition ("objeto grande y redondo que viaja alrededor de una estrella") | OK | None |

**Observations:**
- 1/1 smoke turn completed without errors.
- STT transcription accurate.
- Response in Spanish, short, child-friendly.
- DevExpert `mimo-v2.5` response was concise (shorter than typical OpenAI for same prompt).
- No ALSA/JACK warnings.
- Provider switch from OpenAI to DevExpert worked correctly (backend restart with env var).

### Acceptance Criteria

- [x] 3+ consecutive voice turns complete without blocking failures on primary provider (OpenAI: 6/6).
- [x] 1 smoke turn completes successfully on alternative provider (DevExpert: 1/1).
- [x] Any failure documented with clear cause (no failures in this rehearsal).
- [x] Evidence recorded in journal for both providers.

### Status

- [x] OpenAI rehearsal: 6/6 voice turns passed.
- [x] DevExpert smoke turn: 1/1 passed.
- [x] Evidence recorded.
