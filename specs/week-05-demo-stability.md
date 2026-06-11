# Week 05 Demo Stability and Experience

**Version:** 0.1
**Status:** Phases 0-2 complete
**Last Updated:** 2026-06-08

## Objective

Convert the validated TONTO voice loop into a stable, repeatable demo that an operator can run confidently multiple times.

Week 04 delivered demo baseline validation, resilience fixes, conversation calibration, and non-physical listening indicators. Week 05 focuses on making the existing system demo-ready: clear startup, polished conversational UX, graceful error handling, and a successful multi-run rehearsal.

## Current Baseline

The validated system at the start of Week 05:

```text
Raspberry: Enter -> arecord WAV -> POST /chat/audio -> STT -> response -> espeak
Web:       Mic button -> browser WAV -> POST /chat/audio -> STT -> response -> browser speech
Text:      POST /chat -> response -> visible + TTS
```

Current state:
- 52 Python tests pass.
- Backend runs on `0.0.0.0:8000` with LAN access.
- Raspberry voice loop validated with 2+ consecutive turns.
- Web voice loop validated with visible indicator and auto-stop.
- In-memory session history works.
- Prompt calibrated for Spanish, child-friendly, short answers.
- Listening indicators implemented and validated for both Raspberry and web.
- ALSA/JACK warnings present but non-blocking.

Known gaps for demo readiness:
- Demo startup requires multiple manual commands and env vars.
- No single runbook for demo operators.
- Error messages are technical, not demo-friendly.
- ALSA/JACK warnings clutter the terminal.
- No structured demo rehearsal evidence.

## Week 05 Framing

The MVP rule applies: no new features unless they directly unblock the demo.

Week 05 is about:
1. **Reproducibility** — a demo operator can start and run the demo with minimal friction.
2. **Conversational polish** — TONTO responses feel natural and educational for children.
3. **Error clarity** — when something fails, the operator sees a clear message, not a stack trace.
4. **Rehearsal proof** — the demo runs 3+ consecutive times without blocking failures.

Week 05 is NOT about:
- New features (wake word, Arduino, persistence, streaming).
- Architecture changes.
- New dependencies.
- Broad UI redesign.

## Phased Milestones

### Phase 0 - Documentation Kickoff

Purpose: prepare agents before implementation.

Included:
- Create this spec.
- Create paired implementation plan.
- Create Week 05 journal.
- Create GitHub Issues for each implementation phase.
- Update roadmap and specs summary.

Excluded:
- Code changes.
- Tests or build changes.
- New dependencies.

Acceptance:
- Week 05 spec exists.
- Paired plan exists in `docs/plans/`.
- Journal is started.
- GitHub Issues exist for Phases 1-4.
- Roadmap and specs summary point to Week 05.

### Phase 1 - Demo Runbook and Startup Scripts

Purpose: reduce the friction of starting a TONTO demo.

Included:
- A single startup script for the Raspberry demo flow.
- A documented runbook with step-by-step operator instructions.
- Environment variable documentation and defaults.
- Health check before starting the demo.

Excluded:
- Backend changes.
- Client behavior changes.
- New dependencies.

Acceptance:
- A demo operator can start the demo with one or two commands.
- The runbook documents the full demo flow: start, voice turns, stop.
- The runbook documents known warnings (ALSA/JACK) and what to ignore.

### Phase 2 - Conversational UX Polish

Purpose: make TONTO responses feel more natural and engaging for children.

Implementation note, 2026-06-08: Phase 2 applied a small prompt polish in
`backend/openai_client.py`. TONTO now starts with a direct answer, uses one simple
example or comparison when useful, avoids long lists/markdown/lecture-style
answers, uses simple accurate facts instead of guessing, handles
greetings/farewells naturally, and keeps using recent context for follow-up
questions. `MAX_OUTPUT_TOKENS` was reduced from `220` to `180` to
keep demo answers more speakable through Raspberry `espeak` and browser speech.

Validation note, 2026-06-11: Phase 2 was validated from the real Raspberry with
6 text-mode demo questions against the Windows LAN backend. See
`docs/project-journal/week-05.md` for the command evidence and turn-by-turn
results.

Included:
- Review current prompt calibration in `backend/openai_client.py`.
- Test with real demo scenarios (greeting, questions, farewell).
- Adjust response length, tone, or personality if needed.
- Ensure context use feels natural across 3+ related turns.

Excluded:
- New AI models or providers.
- Memory architecture changes.
- Persistence.
- Multi-agent orchestration.

Acceptance:
- TONTO answers a sequence of demo questions coherently.
- Responses are short, Spanish, child-friendly, and educational.
- The prompt changes (if any) are documented and tested.

### Phase 3 - Error Resilience

Purpose: make demo failures understandable and recoverable.

Included:
- Improve error messages for demo-facing scenarios.
- Handle common failures gracefully: no mic, no backend, timeout, empty transcript.
- Suppress or redirect ALSA/JACK warnings if possible without changing audio behavior.
- Ensure the client recovers cleanly from errors (no hung processes).

Excluded:
- New APIs or endpoints.
- Backend architecture changes.
- New dependencies.

Acceptance:
- Common demo failures show a clear, non-technical message.
- The client recovers from errors and can continue the demo.
- ALSA/JACK warnings are either suppressed or documented as ignorable.

### Phase 4 - Demo Rehearsal

Purpose: prove the demo works repeatedly.

Included:
- Run the full demo flow 3+ consecutive times on Raspberry.
- Run the full demo flow 3+ consecutive times on web (if practical).
- Record timing, success/failure, and any issues.
- Document operator steps and any friction points.

Excluded:
- Code changes during rehearsal.
- New features.

Acceptance:
- 3+ consecutive voice turns complete without blocking failures.
- Any failure is documented with clear cause.
- Evidence is recorded in `docs/project-journal/week-05.md`.

### Phase 5 - Week 05 Closeout

Purpose: end the week with evidence and a clear state for Week 06.

Included:
- Update `docs/project-journal/week-05.md`.
- Update roadmap/specs for actual changes.
- Record remaining risks for Week 06.

Acceptance:
- Week 05 has clear validation evidence.
- Week 06 starts from a known state.

## Risks

- Adding features instead of polishing existing ones.
- Over-engineering error handling.
- Spending too much time on ALSA/JACK warnings.
- Not running enough rehearsal turns.

## Definition of Done

Week 05 is done when:
- A demo operator can start and run the demo with minimal friction.
- TONTO responses are polished for the demo scenario.
- Common errors are handled gracefully.
- 3+ consecutive demo turns have been validated.
- Evidence is recorded in the journal.
