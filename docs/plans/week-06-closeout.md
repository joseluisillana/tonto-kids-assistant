# Week 06 Closeout — Implementation Plan

**Spec:** `specs/week-06-closeout.md`
**Tracking:** GitHub parent issue #65

## Overview

Week 06 closes the TONTO MVP with documentation-only deliverables: a presentation checklist, known limitations, future work list, final report, and demo evidence. No code changes are expected.

## Phase 0 — Documentation Kickoff

**Issue:** #66

### Tasks

1. Create `specs/week-06-closeout.md`.
2. Create `docs/plans/week-06-closeout.md`.
3. Create `docs/project-journal/week-06.md` with kickoff.
4. Create GitHub Issues for Phases 1-5.
5. Update `docs/specs.md` with Week 06 section.
6. Update `docs/roadmap.md` Week 06 status.

### Acceptance

- All documents exist.
- GitHub Issues track each phase.
- Roadmap points to Week 06.

---

## Phase 1 — Demo Checklist

**Issue:** #67

**Status:** Complete - 2026-06-14

### Tasks

1. Create `docs/demo-checklist.md` with:
   - Pre-conditions section (hardware, network, API keys).
   - Backend verification steps (health, provider smoke).
   - Raspberry verification steps (SSH, audio, mic).
   - Web verification steps (optional).
   - Recommended demo sequence (5-7 questions).
   - Plan B / fallback section.
2. Validate checklist is actionable by reading it as an operator.

### Acceptance

- `docs/demo-checklist.md` exists.
- Covers pre-conditions, verification, demo sequence, fallback.
- Actionable without guessing.

---

## Phase 2 — Known Limitations

**Issue:** #68

**Status:** Complete - 2026-06-18

### Tasks

1. Create `docs/known-limitations.md` covering:
   - TTS quality (espeak robotic).
   - No persistence.
   - No wake word.
   - No Arduino/LEDs.
   - Network dependency.
   - Single hardware unit.
   - Latency (~2-5s).
   - DevExpert verbosity.
   - ALSA/JACK warnings.
2. Each limitation has description and impact.

### Acceptance

- `docs/known-limitations.md` exists.
- Each limitation is clearly described.
- Suitable for presentation audience.

---

## Phase 3 — Future Work

**Issue:** #69

### Tasks

1. Create `docs/future-work.md` covering:
   - Inference provider improvements (#53).
   - TTS alternatives.
   - Session persistence.
   - Wake word.
   - Arduino/LEDs.
   - Cloud deployment.
   - Multi-user.
   - Metrics dashboard.
2. Each item has priority, description, complexity.

### Acceptance

- `docs/future-work.md` exists.
- Items are prioritized.
- Each item is actionable.

---

## Phase 4 — Final Report

**Issue:** #70

### Tasks

1. Expand `docs/final-report-outline.md` into `docs/final-report.md`.
2. Fill all 10 sections with substantive content:
   - 1. Project Introduction.
   - 2. MVP Scope.
   - 3. Architecture.
   - 4. Development Process.
   - 5. AI-Assisted Development.
   - 6. Implementation.
   - 7. Validation.
   - 8. Results.
   - 9. Future Work (link to `docs/future-work.md`).
   - 10. Appendix.
3. Reference real project evidence (tests, journals, validation).

### Acceptance

- `docs/final-report.md` exists.
- All 10 sections have content.
- Content references real evidence.
- Suitable for AI Expert course submission.

---

## Phase 5 — Final Demo Evidence and Closeout

**Issue:** #71

### Tasks

1. Execute demo following `docs/demo-checklist.md`.
2. Record evidence in `docs/project-journal/week-06.md`:
   - Turn-by-turn results.
   - Provider used.
   - Latency.
   - Issues encountered.
3. Update `docs/specs.md` with final status.
4. Update `docs/roadmap.md` with completion.
5. Verify Definition of Done checklist.

### Acceptance

- Journal has demo evidence.
- Definition of Done verified.
- Specs and roadmap updated.
- Project ready for presentation.

---

## Agent Prompt

You are closing the TONTO MVP project. Your job is documentation only — no code changes, no new features, no new dependencies.

Read these files before starting:
- `AGENTS.md`
- `docs/ai-assisted-workflow.md`
- `specs/week-06-closeout.md`
- This plan

Follow the pre-edit Git gate. Use project branches. Create one branch per phase if working in parallel.

For each phase:
1. Create or update the specified document.
2. Use real project evidence (tests, journals, validation records).
3. Update `docs/project-journal/week-06.md` when the phase completes.
4. Do not change code, tests, or scripts.

When all phases are complete, verify the Definition of Done and update specs/roadmap.
