# Web Listening Indicator Implementation Plan

## Objective

Implement the web listening/time indicator described in `specs/web-listening-indicator.md` without changing the backend audio contract or widening the product UI.

## Source Spec

- Spec: `specs/web-listening-indicator.md`
- Related docs:
  - `specs/week-04-demo-stability.md`
  - `docs/plans/week-04-demo-stability.md`
  - `docs/project-journal/week-04.md`
  - `docs/specs.md`
  - `docs/roadmap.md`
  - `specs/web-validation-client.md`

## Scope

Included:

- Web voice recording time/progress indicator.
- Small changes in the existing React conversation/voice components.
- Focused tests, type coverage, or build verification appropriate to the changed code.
- Week 04 journal update with implementation and browser validation evidence.

Excluded:

- Raspberry client changes.
- Backend changes.
- Manual WAV upload/file picker.
- New dependencies.
- Streaming, silence detection, local STT, local AI, persistence, auth, broad dashboard UI, Arduino, LEDs, or physical states.

## Implementation Plan

1. Read the current web voice capture flow:
   - `web/src/features/conversation/useConversation.ts`
   - `web/src/components/VoiceLoopPanel.tsx`
   - `web/src/lib/audio.ts`
   - `web/src/types/conversation.ts`
2. Identify the current recording state and audio duration limits.
3. Add live elapsed or remaining time while capture status is recording/listening.
4. Display the indicator in the existing voice panel with compact, accessible text and, optionally, a simple progress bar using existing styles.
5. Preserve existing upload, thinking, speaking, and error messages.
6. Do not expose manual file upload.
7. Add or update focused tests if the repo already has suitable web test coverage for this area.
8. Update `docs/project-journal/week-04.md` after implementation and browser validation.

## Acceptance Criteria

- Web recording visibly shows listening/time feedback while active.
- Upload/thinking/speaking/error states remain clear after recording ends.
- Text fallback remains unchanged.
- `/chat/audio` request shape and WAV preparation remain unchanged.
- Web checks pass.
- Manual browser validation is recorded in the Week 04 journal.

## Verification

Use official project scripts whenever possible:

```powershell
.\scripts\test.ps1 -Target web
.\scripts\build.ps1 -Target web
git diff --check
git status --short --branch
```

If browser validation is practical, run the backend and web client:

```powershell
.\scripts\dev.ps1 -Service backend -AllowLan
.\scripts\dev.ps1 -Service web
```

Then validate the microphone loop manually from the browser.

## Implementation Prompt

```text
Implement the spec in specs/web-listening-indicator.md.

Before editing:
- Read AGENTS.md.
- Read docs/ai-assisted-workflow.md.
- Read specs/web-listening-indicator.md.
- Read docs/plans/web-listening-indicator.md.
- Run git branch --show-current and git status --short --branch.
- Preserve unrelated user changes.

Task:
- Add a compact live listening/time indicator to the existing web voice UI.
- Preserve the current browser microphone -> WAV -> /chat/audio flow.
- Preserve text fallback behavior.
- Do not add dependencies.
- Do not expose manual WAV upload.
- Do not implement backend changes, Raspberry changes, Arduino, LEDs, streaming, silence detection, local STT, local AI, persistence, auth, or broad UI redesign.
- Add or update focused tests where appropriate.
- Update docs/project-journal/week-04.md with implementation and validation evidence.

Verification:
- Run .\scripts\test.ps1 -Target web.
- Run .\scripts\build.ps1 -Target web.
- Run git diff --check.
- Run git status --short --branch.
- Record browser validation if available.

Delivery:
- Summarize changed files.
- Summarize the indicator behavior.
- Summarize verification and manual validation results.
```

## Notes / Assumptions

- This plan can run in parallel with `docs/plans/raspberry-listening-indicator.md`.
- If both plans update `docs/project-journal/week-04.md`, reconcile those documentation edits during integration.
- A simple time/progress indicator is enough; do not redesign the web client.

## Workflow Isolation

- Branch: `feature/week-04-phase4-web-listening-indicator`
- Worktree: use a dedicated worktree when running in parallel with the Raspberry indicator plan.
- Parallel-safe: yes, if Raspberry work uses `feature/week-04-phase4-raspberry-listening-indicator` in a separate worktree.
- Collision risk: `docs/project-journal/week-04.md` may overlap during evidence updates.
- Integration note: if the Raspberry PR merges first, update this branch from `main` and reconcile journal entries before merging.
- GitHub tracking: create or reuse an issue for Week 04 Phase 4 web listening indicator implementation and validation.
