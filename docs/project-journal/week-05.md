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
  for Raspberry `espeak` and browser speech.

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
