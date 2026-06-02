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

Phase 1: Reproducible demo baseline

- Run official checks if the environment is ready.
- Start backend with `.\scripts\dev.ps1 -Service backend -AllowLan`.
- Validate backend health from Windows and Raspberry.
- Run multiple Raspberry voice turns with `client/main.py --mode voice`.
- Record evidence and failures in the journal.

Phase 2: Demo resilience and error handling

- Only after Phase 1 evidence, decide whether code fixes are needed.
- Keep fixes small and covered by focused tests.
- Preserve existing contracts and the text fallback.
- Update docs and journal.

Phase 3: Conversation and memory calibration

- Validate existing in-memory context.
- Tune only if the demo shows a clear issue.
- Do not add persistence or advanced memory.

Phase 4: Physical state decision gate

- Define state vocabulary.
- Decide whether LED/Arduino implementation is worth it for the MVP demo.
- If yes, create a separate spec and plan before code.
- If no, document the deferral and use existing status surfaces.

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
- The first implementation action after kickoff should be Phase 1 baseline validation, not Arduino.
- Arduino/LED work remains possible, but only after the Phase 4 decision gate.
