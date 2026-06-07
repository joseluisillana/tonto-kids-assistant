# Raspberry Listening Indicator Implementation Plan

**Status:** Implemented and validated on real hardware (2026-06-07). Issue #27 closed.

## Objective

Implement the Raspberry terminal listening/time indicator described in `specs/raspberry-listening-indicator.md` without changing the backend contract or adding hardware scope.

## Source Spec

- Spec: `specs/raspberry-listening-indicator.md`
- Related docs:
  - `specs/week-04-demo-stability.md`
  - `docs/plans/week-04-demo-stability.md`
  - `docs/project-journal/week-04.md`
  - `docs/specs.md`
  - `docs/roadmap.md`

## Scope

Included:

- Raspberry client terminal indicator during voice recording.
- Small, testable changes in `client/main.py`.
- Focused updates in `tests/test_client.py` if behavior or helper functions change.
- Week 04 journal update with implementation and Raspberry validation evidence.

Excluded:

- Arduino, LEDs, GPIO, and physical states.
- Web client changes.
- Backend changes.
- New dependencies.
- Wake word, silence detection, streaming, local STT, local AI, persistence, auth, or advanced UI.

## Implementation Plan

1. Read the current `client/main.py` voice capture flow.
2. Decide the smallest safe way to show progress during fixed-duration capture.
3. Prefer a helper with deterministic output that can be unit tested.
4. If `capture_audio()` must move from blocking `subprocess.run()` to a narrow polling loop, preserve:
   - `arecord` command arguments,
   - configured device behavior,
   - WAV output path behavior,
   - failure handling.
5. Keep the visible state sequence simple:
   - ready/input prompt,
   - listening with elapsed or remaining time,
   - uploading,
   - transcript/response,
   - speaking or error.
6. Update focused tests.
7. Update `docs/project-journal/week-04.md` after implementation and after Raspberry validation.

## Acceptance Criteria

- `client/main.py --mode voice` shows visible listening/time feedback during recording.
- The indicator completes before `Uploading...` appears.
- Existing voice upload and local TTS behavior remain intact.
- Text mode remains unchanged.
- Python tests pass.
- Real Raspberry validation is recorded in the Week 04 journal.

## Verification

Use official project scripts whenever possible:

```powershell
.\scripts\test.ps1 -Target python
git diff --check
git status --short --branch
```

Manual Raspberry validation should also be recorded:

```bash
export TONTO_BACKEND_URL=http://192.168.1.91:8000
export TONTO_AUDIO_DEVICE=plughw:CARD=Device,DEV=0
source .venv/bin/activate
python3 client/main.py --mode voice
```

## Implementation Prompt

```text
Implement the spec in specs/raspberry-listening-indicator.md.

Before editing:
- Read AGENTS.md.
- Read docs/ai-assisted-workflow.md.
- Read specs/raspberry-listening-indicator.md.
- Read docs/plans/raspberry-listening-indicator.md.
- Run git branch --show-current and git status --short --branch.
- Preserve unrelated user changes.

Task:
- Add a small terminal listening/time indicator to the Raspberry voice client.
- Keep the Raspberry client a thin client.
- Preserve /chat/audio, WAV capture settings, TONTO_RECORD_SECONDS behavior, and TTS behavior.
- Do not add dependencies.
- Do not implement Arduino, LEDs, wake word, silence detection, streaming, local STT, local AI, persistence, auth, or advanced UI.
- Add focused tests for changed behavior.
- Update docs/project-journal/week-04.md with implementation and validation evidence.

Verification:
- Run .\scripts\test.ps1 -Target python.
- Run git diff --check.
- Run git status --short --branch.
- Record Raspberry hardware validation if available.

Delivery:
- Summarize changed files.
- Summarize the indicator behavior.
- Summarize verification and hardware validation results.
```

## Implementation Result

The Raspberry listening indicator was implemented in `client/main.py` with three helper functions:

- `_format_listening_progress()` — returns `"Listening: X/Ys"` string
- `_show_listening_indicator()` — daemon thread that prints countdown during capture
- `_stop_listening_indicator()` — signals thread to stop and joins

The `capture_audio()` function was updated with a `show_progress` parameter, and the voice loop passes `show_progress=True` by default.

Verification completed:

```powershell
.\scripts\test.ps1 -Target python
git diff --check
```

Raspberry real hardware validation passed 2026-06-07: 2/2 voice turns, indicator visible, timer updates live, transition to uploading clear, transcript/response/espeak working. Issue #27 closed.

## Notes / Assumptions

- This plan can run in parallel with `docs/plans/web-listening-indicator.md`.
- If both plans update `docs/project-journal/week-04.md`, reconcile those documentation edits during integration.
- A simple terminal timer is enough; polished terminal animation is not required.

## Workflow Isolation

- Branch: `feature/week-04-phase4-raspberry-listening-indicator`
- Worktree: use a dedicated worktree when running in parallel with the web indicator plan.
- Parallel-safe: yes, if web work uses `feature/week-04-phase4-web-listening-indicator` in a separate worktree.
- Collision risk: `docs/project-journal/week-04.md` may overlap during evidence updates.
- Integration note: if the web PR merges first, update this branch from `main` and reconcile journal entries before merging.
- GitHub tracking: create or reuse an issue for Week 04 Phase 4 Raspberry listening indicator implementation and validation.
