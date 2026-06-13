# Week 05 Demo Stability Implementation Plan

**Status:** Complete (Phases 0-5)

## Objective

Prepare and execute Week 05 as a demo-readiness effort, starting from the completed Week 04 state.

This plan is paired with `specs/week-05-demo-stability.md` and is intended as a ready handoff for Codex, OpenCode, or another AI-assisted agent.

## Source Spec

- Spec: `specs/week-05-demo-stability.md`
- Related docs:
  - `docs/specs.md`
  - `docs/roadmap.md`
  - `docs/architecture.md`
  - `docs/project-journal/week-05.md`
  - `docs/ai-assisted-workflow.md`

## Scope

Included:
- Documentation kickoff.
- Phased plan for implementation work.
- Demo runbook and startup scripts.
- Conversational UX polish.
- Error resilience improvements.
- Demo rehearsal with evidence.

Excluded:
- New features (wake word, Arduino, persistence, streaming).
- Architecture changes.
- New runtime or development dependencies.
- Broad UI redesign.

## Implementation Plan

### Phase 0: Documentation kickoff (current)

- Read the current documentation and implementation state.
- Create `specs/week-05-demo-stability.md`.
- Create `docs/plans/week-05-demo-stability.md`.
- Create `docs/project-journal/week-05.md`.
- Create GitHub Issues for Phases 1-4.
- Update `docs/roadmap.md` and `docs/specs.md` with Week 05 scope.

### Phase 1: Demo runbook and startup scripts

Purpose: reduce the friction of starting a TONTO demo.

Execution plan:

1. Read current demo startup commands from `docs/project-journal/week-04.md` and existing scripts.
2. Create `scripts/demo-raspberry.ps1` (or equivalent) that:
   - Checks backend is running and healthy.
   - Sets required env vars with sensible defaults.
   - Starts the Raspberry client in voice mode.
3. Create `docs/demo-runbook.md` with:
   - Prerequisites (backend running, Raspberry connected, audio device configured).
   - Step-by-step operator instructions.
   - Known warnings and what to ignore.
   - Troubleshooting tips.
4. Test the runbook on real hardware if available.

Acceptance:
- Demo operator can start with 1-2 commands.
- Runbook covers the full demo flow.
- Known warnings are documented.

### Phase 2: Conversational UX polish

Purpose: make TONTO responses feel natural and engaging for children.

Execution plan:

1. Read current prompt in `backend/openai_client.py`.
2. Run a sequence of 5+ demo questions on Raspberry and record responses.
3. Evaluate: are responses short enough? Are they warm? Do they use context naturally?
4. If adjustments needed:
   a. Tune `OPENAI_INSTRUCTIONS` for better demo flow.
   b. Adjust `max_output_tokens` if responses are too long/short.
   c. Keep changes small and reversible.
5. If no adjustments needed: document in journal that validation passed.
6. Run `.\scripts\test.ps1 -Target python` after any code changes.

Acceptance:
- TONTO answers demo questions coherently.
- Responses are Spanish, short, child-friendly, educational.
- Prompt changes (if any) are documented and tested.

### Phase 3: Error resilience

Purpose: make demo failures understandable and recoverable.

Execution plan:

1. Review current error handling in `client/main.py`.
2. Identify demo-facing error scenarios:
   - No microphone connected.
   - Backend unreachable.
   - STT timeout or empty transcript.
   - TTS command failure.
3. Improve error messages to be operator-friendly, not developer-focused.
4. Investigate ALSA/JACK warning suppression options (without changing audio behavior).
5. Ensure the client recovers from errors and can continue.
6. Add focused tests for any changed error handling.
7. Run `.\scripts\test.ps1 -Target python` after changes.

Acceptance:
- Common demo failures show clear messages.
- Client recovers from errors.
- ALSA/JACK warnings are suppressed or documented.

### Phase 4: Demo rehearsal

Purpose: prove the demo works repeatedly with both supported inference providers.

Execution plan:

1. Set up Raspberry with backend running and primary provider configured (OpenAI by default).
2. Run the full demo flow 3+ consecutive times on Raspberry:
   - Greeting turn.
   - Educational question turns (3+).
   - Context follow-up turn.
3. Record for each turn:
   - Input (what was said).
   - Transcript (what STT produced).
   - Response (what TONTO said).
   - Timing (approximate).
   - Any errors or warnings.
4. Switch backend to alternative provider (DevExpert) and run 1 smoke turn on Raspberry.
5. Record smoke turn evidence with the same fields.
6. Run web demo 3+ times if practical.
7. Document any failures with clear cause.
8. Record evidence in `docs/project-journal/week-05.md` for both providers.

Acceptance:
- 3+ consecutive voice turns complete on primary provider.
- 1 smoke turn completes on alternative provider.
- Any failure is documented.
- Evidence is in the journal for both providers.

### Phase 5: Closeout

- Update `docs/project-journal/week-05.md`.
- Update roadmap/specs for actual changes.
- Record Week 06 risks.
- Create git tag `week-05-close`.

## Verification

For documentation-only work:

```powershell
git diff --check
git status --short --branch
```

For code changes:

```powershell
.\scripts\test.ps1 -Target python
.\scripts\test.ps1 -Target web
.\scripts\build.ps1 -Target web
git diff --check
git status --short --branch
```

For hardware validation, record commands, environment, result, and human judgment in the journal.

## Implementation Prompt

```text
Prepare or implement the next Week 05 phase for TONTO Kids Assistant.

Before editing:
- Read AGENTS.md.
- Read docs/ai-assisted-workflow.md.
- Read specs/week-05-demo-stability.md.
- Read docs/plans/week-05-demo-stability.md.
- Read docs/project-journal/week-05.md.
- Run git branch --show-current and git status --short --branch.
- If on main, create or switch to a project branch before editing.
- Preserve unrelated user changes.

Current baseline:
- Week 04 is complete.
- 52 Python tests pass.
- Raspberry voice loop validated with listening indicator.
- Web voice loop validated with auto-stop and indicator.
- Prompt calibrated for Spanish, child-friendly answers.
- In-memory session history works.

Task:
- Work only on the next explicitly selected Week 05 phase.
- Prefer reproducible demo validation before new behavior.
- Keep changes small and aligned with the MVP.
- Do not add dependencies.
- Do not implement new features unless they directly unblock the demo.
- Preserve /chat and /chat/audio contracts.
- Update docs/project-journal/week-05.md with evidence.
- Update specs, plans, roadmap, or decisions only if durable project scope changes.

Verification:
- Use official scripts from scripts/ whenever possible.
- For docs-only work, run git diff --check and git status --short --branch.
- For code changes, run the relevant python/web tests.
- For hardware validation, record commands, environment, result, and human judgment.

Delivery:
- Summarize changed files.
- State which Week 05 phase was completed.
- Summarize verification results.
- List remaining blockers or next phase.
```
