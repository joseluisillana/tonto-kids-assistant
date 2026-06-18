# Week 06 Closeout and Presentation

**Version:** 0.1
**Status:** Complete
**Last Updated:** 2026-06-18

## Objective

Prepare the final MVP delivery: a reproducible demo, documented limitations, future work list, presentation checklist, and a final report for the AI Expert course.

Week 05 delivered a stable, repeatable demo with both OpenAI and DevExpert providers, operator-friendly error handling, and a complete runbook. Week 06 focuses on closing the project: documenting what works, what does not, and what comes next.

## Current Baseline

The validated system at the start of Week 06:

```text
Raspberry: Enter -> arecord WAV -> POST /chat/audio -> STT -> response -> espeak
Web:       Mic button -> browser WAV -> POST /chat/audio -> STT -> response -> browser speech
Text:      POST /chat -> response -> visible + TTS
```

Current state:
- 78 Python tests pass.
- Web typecheck passes.
- Backend runs on `0.0.0.0:8000` with LAN access.
- OpenAI rehearsal: 6/6 voice turns on Raspberry.
- DevExpert smoke: 1/1 voice turn on Raspberry.
- Demo runbook exists (`docs/demo-runbook.md`).
- Error messages are operator-friendly.
- ALSA/JACK warnings suppressed.
- Agent Capability Pack operational.
- Inference provider selection operational (OpenAI + DevExpert).

Known gaps for Week 06:
- None. Final demo evidence is recorded in `docs/project-journal/week-06.md`.

## Week 06 Framing

The MVP rule applies: no new features unless they directly unblock the presentation.

Week 06 is about:
1. **Presentation readiness** — a checklist the operator follows on demo day.
2. **Honest limitations** — what the audience should know does not work.
3. **Future direction** — what comes after the MVP.
4. **Course deliverable** — a final report documenting the project.
5. **Final evidence** — a recorded demo proving the MVP works.

Week 06 is NOT about:
- New features.
- Architecture changes.
- New dependencies.
- Code refactoring.
- Bug fixes unless they block the demo.

## Phased Milestones

### Phase 0 - Documentation Kickoff

Purpose: prepare agents before implementation.

Included:
- Create this spec.
- Create paired implementation plan.
- Create Week 06 journal.
- Create GitHub Issues for each implementation phase.
- Update roadmap and specs summary.

Excluded:
- Code changes.
- Tests or build changes.
- New dependencies.

Acceptance:
- Week 06 spec exists.
- Paired plan exists in `docs/plans/`.
- Journal is started.
- GitHub Issues exist for Phases 1-5.
- Roadmap and specs summary point to Week 06.

### Phase 1 - Demo Checklist

Status: completed 2026-06-14. The checklist lives in `docs/demo-checklist.md`.

Purpose: create a step-by-step checklist the operator follows on presentation day to verify everything works before starting.

Included:
- A `docs/demo-checklist.md` document with:
  - Pre-conditions (hardware, network, API keys configured).
  - Backend verification (health check, provider smoke test).
  - Raspberry verification (SSH, audio device, microphone).
  - Web verification (if used in presentation).
  - Recommended demo sequence (5-7 questions).
  - Plan B if something fails.
- Coverage of both providers (OpenAI and DevExpert).

Excluded:
- Code changes.
- New scripts.
- New dependencies.

Acceptance:
- `docs/demo-checklist.md` exists.
- Checklist covers pre-conditions, verification steps, demo sequence, and fallback.
- Checklist is actionable (operator can follow it without guessing).

### Phase 2 - Known Limitations

Status: completed 2026-06-18. The limitations document lives in `docs/known-limitations.md`.

Purpose: create an honest list of what does not work, what is fragile, and what the audience should know.

Included:
- A `docs/known-limitations.md` document covering:
  - TTS quality (`espeak` is robotic).
  - No persistence (backend restart loses session context).
  - No wake word.
  - No Arduino/LED states.
  - Network dependency for STT and chat.
  - Single hardware unit (no backup Raspberry).
  - Latency (~2-5s per turn).
  - DevExpert verbosity compared to OpenAI.
  - ALSA/JACK warnings (suppressed but not eliminated).

Excluded:
- Code changes.
- Workarounds or fixes.

Acceptance:
- `docs/known-limitations.md` exists.
- Each limitation has a clear description and impact.
- Document is suitable for presentation audience.

### Phase 3 - Future Work

Status: completed 2026-06-18. The future work document lives in `docs/future-work.md`.

Purpose: create a prioritized backlog for continuing the project after the MVP.

Included:
- A `docs/future-work.md` document covering:
  - Inference provider improvements (issue #53: fallback, balancing, Gemini, DevExpert TTS).
  - Raspberry touch UI with animated assistant face using the selected Waveshare 5" HDMI touch display.
  - TTS alternatives (better voice quality).
  - Session persistence.
  - Wake word integration.
  - Arduino/LED physical states.
  - Multi-user support.
  - Metrics dashboard.
- Each item has priority, description, and estimated complexity.
- Cloud deployment is explicitly not prioritized after the MVP; the next direction is the physical Raspberry experience while keeping the backend external and simple.

Excluded:
- Implementation of any future work item.
- New specs for future work items.

Acceptance:
- `docs/future-work.md` exists.
- Items are prioritized.
- Each item has enough description to be actionable in a future iteration.

### Phase 4 - Final Report

Status: completed 2026-06-18. The report lives in `docs/final-report.md`.

Purpose: prepare the AI Expert course final deliverable.

Included:
- Expand `docs/final-report-outline.md` into a full `docs/final-report.md`.
- Sections based on the existing outline:
  1. Project Introduction.
  2. MVP Scope.
  3. Architecture.
  4. Development Process.
  5. AI-Assisted Development.
  6. Implementation.
  7. Validation.
  8. Results.
  9. Future Work (link to `docs/future-work.md`).
  10. Appendix.
- Content based on real repository documentation, tested behavior, and project evidence.

Excluded:
- Code changes.
- New documentation beyond the report.

Acceptance:
- `docs/final-report.md` exists.
- All 10 sections have substantive content.
- Content references real project evidence (tests, validation, journal entries).
- Report is suitable for AI Expert course submission.

### Phase 5 - Final Demo Evidence and Closeout

Status: completed 2026-06-18. Final evidence lives in `docs/project-journal/week-06.md`.

Purpose: end the project with recorded evidence and a clear final state.

Included:
- Execute the demo following `docs/demo-checklist.md`.
- Record evidence in `docs/project-journal/week-06.md`:
  - Turn-by-turn results (input, transcript, response, TTS).
  - Provider used.
  - Latency observations.
  - Any issues encountered.
- Update `docs/specs.md` with final Week 06 status.
- Update `docs/roadmap.md` with Week 06 completion.
- Verify Definition of Done:
  - [x] Demo funcional reproducible.
  - [x] Arquitectura estable.
  - [x] Flujo conversacional extremo a extremo.
  - [x] Sistema presentable sin configuración manual compleja.
  - [x] Proyecto documentado clara y manteniblemente.

Excluded:
- Code changes.
- New features.

Acceptance:
- Week 06 journal has clear validation evidence.
- Definition of Done is verified and checked.
- Specs and roadmap reflect final state.
- Project is ready for presentation.

## AI Agent Instructions

Agents working from this spec must:

- Read `AGENTS.md`, `docs/ai-assisted-workflow.md`, this spec, and the paired plan before editing.
- Run the pre-edit Git gate.
- Use project branches and official scripts.
- Do not add code, features, or dependencies.
- Focus on documentation only.
- Update journal whenever a phase completes.
- Reference real project evidence in all documentation.

## Risks

- Adding features instead of closing documentation.
- Spending too much time on the final report.
- Not recording enough demo evidence.
- Making changes that break the validated demo.
- Over-engineering the checklist or limitations document.

## Definition of Done

Week 06 is done when:
- `docs/demo-checklist.md` exists and is actionable.
- `docs/known-limitations.md` exists and is honest.
- `docs/future-work.md` exists and is prioritized.
- `docs/final-report.md` exists with all 10 sections.
- Final demo evidence is recorded in the journal.
- Definition of Done checklist is verified.
- Specs and roadmap reflect final state.
