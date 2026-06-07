# Week 04 Demo Stability Implementation Plan

## Objective

Prepare and execute Week 04 as a phased MVP stabilization effort, starting from the completed Week 03 voice milestone.

This plan is paired with the kickoff spec and is intended as a ready handoff for Codex, OpenCode, or another AI-assisted agent.

## Source Spec

- Spec: `specs/week-04-demo-stability.md`
- Related docs:
  - `docs/specs.md`
  - `docs/roadmap.md`
  - `docs/architecture.md`
  - `docs/project-journal/week-04.md`
  - `docs/ai-assisted-workflow.md`

## Scope

Included:

- Documentation-only kickoff.
- Phased plan for the next implementation work.
- Explicit gates for demo reproducibility, resilience, conversation calibration, and optional physical states.
- Agent-ready prompt.

Excluded:

- Code changes during the kickoff.
- Runtime or development dependency changes.
- Arduino implementation.
- Persistent memory.
- Contract changes to `/chat` or `/chat/audio`.
- Advanced UI, wake word, streaming, local STT, local AI, auth, or multi-user behavior.

## Implementation Plan

Phase 0: Documentation kickoff

- Read the current documentation and implementation state.
- Create or update Week 04 docs.
- Make the roadmap precise enough that agents do not start with Arduino by default.
- Start the Week 04 journal.

Phase 1: Reproducible demo baseline (completed 2026-06-05)

- Run official checks: 45 Python tests passed, TypeScript typecheck clean.
- Start backend with `0.0.0.0:8000` (LAN mode).
- Validate `/health` from Windows and Raspberry: 200 OK.
- Validate `/chat` text fallback: 200 OK with educational response.
- Validate `/chat/audio` endpoint: WAV validation + STT integration confirmed.
- Run Raspberry `--mode voice` for 3 turns: all passed, espeak audible.
- Confirm in-memory session history: TONTO recalled initial greeting in turn 3.
- Record evidence in `docs/project-journal/week-04.md`.

Phase 2: Demo resilience and error handling (completed 2026-06-05)

- Client timeout split: TEXT 10s, VOICE 30s.
- URLError timeout handling added to send_message and send_audio.
- 48/48 tests passed (3 new timeout tests).
- Journal updated.

Phase 3: Conversation and memory calibration (completed 2026-06-07)

Purpose: make TONTO feel coherent enough for a short educational demo without adding memory architecture.

Execution plan:

1. Validate in-memory context across 5+ related turns on Raspberry.
2. Use child-friendly educational questions in Spanish.
3. Check if TONTO maintains context without losing coherence.
4. If prompt tuning is needed:
   a. Adjust instructions in `backend/openai_client.py` (Spanish, shorter answers, child-friendly).
   b. Optionally reduce `max_output_tokens` if responses are too long.
   c. Keep changes small and reversible.
5. If no tuning is needed: document in journal that validation passed.

Validation commands (Raspberry):

```bash
export TONTO_BACKEND_URL=http://192.168.1.91:8000
export TONTO_AUDIO_DEVICE=plughw:CARD=Device,DEV=0
source .venv/bin/activate
python3 client/main.py --mode voice
```

Suggested test sequence (5 turns):

1. "Hola TONTO, ¿qué es una estrella?"
2. "¿Y el sol es una estrella?"
3. "¿De qué está hecho el sol?"
4. "¿Por qué brilla?"
5. "¿Qué pasaría si el sol no existiera?"

Acceptance criteria:

- TONTO answers all 5 questions without losing context.
- If context is lost, the issue is classified (prompt, token limit, or model behavior).
- Any code change is documented and tested.
- If no change is needed, journal says so.

Result:

- Prompt calibration was needed and was implemented in `backend/openai_client.py`.
- Python tests passed: 49/49.
- Raspberry real validation passed: 5/5 related voice turns returned 200 OK through `POST /chat/audio`.
- Responses were coherent, Spanish, child-friendly, and audible enough through Raspberry `espeak` for MVP.
- Non-blocking ALSA/JACK warnings persisted.
- Follow-up candidate: decide whether to add time/listening/progress indicators to Raspberry and web clients.

Phase 4: Physical state decision gate (human decision recorded 2026-06-07)

- Define state vocabulary.
- Use Phase 3 evidence: users do not have clear feedback for when to stop speaking in Raspberry or web.
- Decision recorded: LED/Arduino work is deferred outside the 6-week MVP.
- Decision recorded: implement non-physical time/listening/progress indicators first for Raspberry and web.
- Follow-up decision recorded for web issue #23: auto-stop browser capture at the configured limit, show a simple warning, and keep upload manual.
- Separate spec and plan created for Raspberry:
  - `specs/raspberry-listening-indicator.md`
  - `docs/plans/raspberry-listening-indicator.md`
- Separate spec and plan created for web:
  - `specs/web-listening-indicator.md`
  - `docs/plans/web-listening-indicator.md`
- Raspberry and web implementation can proceed in parallel because they share no code and preserve the same `/chat/audio` contract.

Decision options:

1. Defer state work and keep current terminal/web messages.
2. Implement non-physical indicators first:
   - Raspberry terminal countdown/progress during recording.
   - Web visible recording time/progress against the audio limit, plus auto-stop, warning, and manual `Enviar voz`.
3. Prepare Arduino/LED physical states through a separate spec and plan.

Recommended default:

- Choose option 2 unless the final demo specifically needs visible physical LEDs.
- It addresses a validated operator UX gap with lower scope and risk than Arduino.

Acceptance criteria:

- Human decision recorded in `docs/project-journal/week-04.md`.
- Paired specs and plans exist before code.
- Arduino/LED deferral rationale is recorded.
- MVP exclusions remain intact: no persistence, wake word, local STT, local AI, auth, multi-user behavior, or advanced UI.

Phase 5: Closeout

- Update `docs/project-journal/week-04.md`.
- Update roadmap/specs only for actual durable changes.
- Record Week 05 risks and next steps.

## Acceptance Criteria

- Week 04 kickoff docs exist and are internally consistent.
- The roadmap no longer implies Arduino must be implemented before proving demo repeatability.
- The plan gives agents a safe order of operations.
- Kickoff makes no code behavior changes.
- Any later implementation phase records verification commands and evidence.

## Verification

For this documentation-only kickoff:

```powershell
git diff --check
git status --short --branch
```

For later Week 04 implementation work, use the relevant official checks:

```powershell
.\scripts\test.ps1 -Target python
.\scripts\test.ps1 -Target web
.\scripts\build.ps1 -Target web
git diff --check
git status --short --branch
```

Hardware validation commands depend on the active phase and should be recorded in `docs/project-journal/week-04.md`.

## Implementation Prompt

```text
Prepare or implement the next Week 04 phase for TONTO Kids Assistant.

Before editing:
- Read AGENTS.md.
- Read docs/ai-assisted-workflow.md.
- Read specs/week-04-demo-stability.md.
- Read docs/plans/week-04-demo-stability.md.
- Read docs/project-journal/week-04.md.
- Run git branch --show-current and git status --short --branch.
- If on main, create or switch to a project branch before editing.
- Preserve unrelated user changes.

Current baseline:
- Week 03 voice milestone is complete.
- Raspberry --mode voice has been validated on real hardware.
- Web voice loop has been validated from browser microphone to /chat/audio.
- /chat remains the text fallback.
- Backend memory is short in-memory session history.

Task:
- Work only on the next explicitly selected Week 04 phase.
- For Phase 4, make or record the human decision before implementation.
- Treat Arduino/LEDs and non-physical indicators as separate scope options.
- Prefer reproducible demo validation before new behavior.
- Keep changes small and aligned with the MVP.
- Do not add dependencies.
- Do not implement Arduino, persistence, wake word, local STT, local AI, streaming, auth, or advanced UI unless a later explicit decision and paired spec approve it.
- Preserve /chat and /chat/audio contracts.
- Update docs/project-journal/week-04.md with evidence.
- Update specs, plans, roadmap, or decisions only if durable project scope or behavior changes.

Verification:
- Use official scripts from scripts/ whenever possible.
- For docs-only work, run git diff --check and git status --short --branch.
- For code changes, run the relevant python/web tests and builds from this plan.
- For hardware validation, record commands, environment, result, and human judgment.

Delivery:
- Summarize changed files.
- State which Week 04 phase was completed.
- Summarize verification results.
- List remaining blockers or next phase.
```

## Notes / Assumptions

- The kickoff branch in this local environment may use `docs-week-4-kickoff` because sandboxed Git metadata blocked creating slash-prefixed branches. The project convention remains `<type>/<short-kebab-description>` for normal Git environments.
- The next implementation action after the Phase 4 decision should be the Raspberry and/or web listening indicator work, not Arduino.
- For web follow-up #23, the implementation action should use `feature/week-04-phase4-web-recording-limit` in a dedicated worktree and preserve manual send after auto-stop.
- Arduino/LED work is deferred outside the 6-week MVP and should return only through a future spec and plan.
