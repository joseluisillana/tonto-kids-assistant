# Week 04 Demo Stability and Scope Kickoff

**Version:** 0.3
**Status:** Phase 2 complete, Phase 3 ready for implementation
**Last Updated:** 2026-06-05

## Objective

Prepare Week 04 as a documentation-first kickoff for the next MVP work.

The goal is not to add code in this kickoff. The goal is to leave a clear, phased handoff for Codex, OpenCode, and other AI-assisted agents so future implementation work starts from the real state of the project, keeps the validated Week 03 voice loop intact, and avoids scope creep.

Week 04 should move TONTO from "voice loop validated" toward "demo loop repeatable and easier to operate".

## Current Baseline

The validated baseline at the start of Week 04 is:

```text
Raspberry voice mode -> arecord WAV -> POST /chat/audio ->
backend STT -> response -> local espeak
```

The web validation baseline is:

```text
browser microphone -> WAV PCM 16 kHz mono -> POST /chat/audio ->
transcript -> response -> browser speech
```

The text fallback remains:

```text
POST /chat -> response_text -> visible response -> local or browser TTS
```

Existing implementation facts:

- `/chat` is stable for text.
- `/chat/audio` is implemented and validated with OpenAI `gpt-4o-mini-transcribe`.
- The Raspberry client supports `--mode text` and `--mode voice`.
- The Raspberry TTS default is tuned to `espeak -v es -s 135 -g 8`.
- The backend already has short in-memory session history.
- No persistent memory exists and none is required for Week 04 kickoff.
- Arduino and LEDs are available as future hardware, but not yet integrated.

## Week 04 Framing Decision

The original roadmap described Week 04 as "memoria simple y estados físicos". That needs a narrow MVP adjustment:

- "Memoria simple" should mean validating and, only if needed, lightly tuning the existing short in-memory session behavior. It must not become persistence, vector memory, user profiles, or advanced personalization.
- "Estados físicos" should be treated as a decision gate and optional spike, not an automatic Arduino implementation. Arduino/LED work should begin only if it clearly improves the final demo and the user explicitly accepts that scope.
- The main Week 04 value should be repeatability: fewer surprises, clearer failure modes, and a runbook agents and humans can follow.

## Phased Milestones

### Phase 0 - Documentation Kickoff

Purpose: prepare agents before implementation.

Included:

- Record Week 04 scope and phase gates.
- Update roadmap language so it matches the current MVP.
- Create an implementation plan and agent prompt.
- Start `docs/project-journal/week-04.md`.

Excluded:

- Code changes.
- Tests or build changes.
- New dependencies.
- Hardware integration.

Acceptance:

- Week 04 spec exists.
- Paired plan exists in `docs/plans/`.
- Roadmap and specs summary point to this kickoff.
- Journal captures the state and recommended next step.

### Phase 1 - Reproducible Demo Baseline (completed 2026-06-05)

Purpose: prove the current system can be run repeatedly before adding behavior.

Included:

- Run official setup/test/build checks as appropriate.
- Start backend with LAN access.
- Validate `/health` from Windows and Raspberry.
- Run Raspberry `--mode voice` for multiple turns.
- Confirm typed fallback still works.
- Run web audio validation only if useful for diagnosis.
- Record latency, microphone device, TTS quality, errors, and operator steps.

Excluded:

- Feature work.
- Prompt/personality tuning.
- Arduino.
- Persistence.

Acceptance:

- At least three consecutive voice turns complete on Raspberry or each failure is documented with a clear cause.
- Text fallback remains usable.
- Any blocker is classified as setup, backend, STT, client capture, TTS, or network.

Evidence:

- 45 Python tests passed, TypeScript typecheck clean.
- Backend started on `0.0.0.0:8000` (LAN mode).
- `/health` returned 200 from Windows and Raspberry.
- `/chat` returned 200 with educational response.
- `/chat/audio` validated (WAV + STT integration confirmed).
- 3 voice turns on Raspberry real (`tonto-pi`) against `192.168.1.91:8000`:
  - Turn 1: "Hola tonto, ¿cómo estás?" -> greeting response, espeak audible.
  - Turn 2: "¿Qué tal te ves?" -> response maintaining context, espeak audible.
  - Turn 3: "¿Qué te he preguntado al principio?" -> TONTO recalled turn 1, espeak audible.
- In-memory session history validated (TONTO recalled initial greeting in turn 3).
- Blockers: ALSA/JACK warnings (expected, documented from Week 03, do not block audio).

### Phase 2 - Demo Resilience and Error Handling

Purpose: fix only blockers that make the demo unreliable or confusing.

Included:

- Improve handling of observed backend timeouts, STT empty transcripts, capture failures, or TTS command failures if they appear in Phase 1.
- Keep fixes small and covered by focused tests.
- Preserve `/chat` and `/chat/audio` contracts.
- Improve demo-facing logs or messages only when they reduce operator confusion.

Excluded:

- New APIs.
- New runtime dependencies unless explicitly approved.
- Offline STT.
- Backend TTS.
- Authentication or persistence.

Acceptance:

- Observed critical failures have either a fix or a documented runbook workaround.
- Official relevant tests pass.
- Documentation records what changed and why.

Evidence:

- Client timeout split: `TEXT_TIMEOUT_SECONDS=10`, `VOICE_TIMEOUT_SECONDS=30`.
- URLError timeout handling added to `send_message()` and `send_audio()`.
- `_is_timeout_reason()` helper added (matches `stt_client.py` pattern).
- 48/48 tests passed (3 new timeout tests added).
- Journal updated with Phase 2 changes.

### Phase 3 - Conversation and Memory Calibration (ready for implementation)

Purpose: make TONTO feel coherent enough for a short educational demo without adding memory architecture.

Included:

- Validate the existing in-memory history across several turns.
- Decide whether prompt wording needs a small adjustment for shorter, clearer Spanish educational answers.
- Keep any future code change small and reversible.

Excluded:

- Persistent memory.
- Vector databases.
- Child profiles.
- User accounts.
- Multi-session personalization.
- Multi-agent orchestration.

Acceptance:

- TONTO can answer a short sequence of related child-friendly questions without losing context in an obvious way.
- If no code change is needed, the journal says so.
- If prompt tuning is needed, it is documented and tested through the existing conversation paths.

### Phase 4 - Physical State Decision Gate

Purpose: decide whether physical LED states are worth implementing before the final demo.

Included:

- Define the minimum useful state vocabulary on paper:
  - idle,
  - listening,
  - thinking,
  - speaking,
  - error.
- Decide whether those states need Arduino LEDs, terminal/web status only, or no implementation for the MVP.
- If Arduino is accepted later, prepare a separate narrow spec and plan before code.

Excluded:

- Automatic Arduino implementation in this kickoff.
- Complex animations.
- Sensors.
- Buttons.
- GPIO abstractions.
- Multi-device hardware control.

Acceptance:

- A human decision is recorded: implement LEDs now, defer LEDs, or use existing non-physical status indicators.
- If implementation is approved, a separate spec and plan exist before code changes.

### Phase 5 - Week 04 Closeout

Purpose: end the week with evidence, not loose impressions.

Included:

- Update `docs/project-journal/week-04.md`.
- Update roadmap/specs only for actual changes.
- Export NotebookLM sources if part of the weekly routine.
- Record remaining demo risks for Week 05.

Acceptance:

- Week 04 has clear validation evidence.
- Week 05 starts from a known state.

## AI Agent Instructions

Agents working from this spec must:

- Read `AGENTS.md`, `docs/ai-assisted-workflow.md`, this spec, and the paired plan before editing.
- Run the pre-edit Git gate.
- Use project branches and official scripts.
- Preserve the Week 03 voice loop and text fallback.
- Avoid adding dependencies.
- Avoid Arduino, persistence, auth, wake word, local AI, local STT, streaming, or advanced UI unless a later explicit decision changes scope.
- Update docs/journal whenever behavior, validation, or scope changes.

## Risks

- Treating Arduino as mandatory and spending Week 04 on hardware complexity.
- Reworking memory even though short in-memory history already exists.
- Adding polish before proving repeated runs.
- Confusing the web validation client with the physical product.
- Making documentation too vague for agents to execute safely.

## Definition of Done for Kickoff

This kickoff is done when:

- This spec exists.
- The paired implementation plan exists.
- Roadmap and specs summary align with the adjusted Week 04 scope.
- The Week 04 journal is started with current state, AI usage, and next action.
- No code behavior has changed in the kickoff.
