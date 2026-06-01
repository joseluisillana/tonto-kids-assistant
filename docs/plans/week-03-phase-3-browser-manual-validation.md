# Week 03 Phase 3 Browser Manual Validation Plan

## Objective

Execute the final browser-based manual validation for Phase 3 Web Voice Loop and capture enough evidence to close the Phase 3 spec and feature.

**Status:** completed on 2026-06-01. The browser voice loop passed against the real backend after selecting the correct microphone input in browser settings.

## Source Spec

- Spec: `specs/audio-pipeline-phase-3-browser-manual-validation.md`
- Related docs:
  - `specs/audio-pipeline-phase-3-web-loop.md`
  - `specs/web-validation-client.md`
  - `specs/audio-pipeline.md`
  - `docs/project-journal/week-03.md`
  - `docs/specs.md`
  - `docs/roadmap.md`
  - `docs/architecture.md`
  - `README.md`
  - `AGENTS.md`

## Scope

Included:

- Run the official automated checks before manual browser validation.
- Start the real backend and web client with the official dev script.
- Validate backend health from the web UI.
- Validate `/chat` text fallback.
- Validate browser microphone capture, generated WAV upload, backend STT transcript, backend response, and browser speech playback.
- Validate readable errors for permission denial, empty audio, backend unavailable/timeout, and speech support/failure where practical.
- Record evidence in `docs/project-journal/week-03.md`.
- Update status docs to mark Phase 3 complete, partial, or blocked.

Excluded:

- New backend endpoint.
- Code changes unless validation reveals a defect.
- New dependencies.
- Backend transcoding, backend TTS, local STT, streaming, persistence, auth, or advanced UI.
- Raspberry hardware revalidation.

## Execution Plan

1. Run the pre-edit Git gate from `AGENTS.md`.
2. Read the source spec and related Phase 3 docs.
3. Run setup/tests/build:

```powershell
.\scripts\setup-dev.ps1
.\scripts\test.ps1 -Target python
.\scripts\test.ps1 -Target web
.\scripts\build.ps1 -Target web
```

4. Configure backend environment without printing secrets:

```powershell
if (-not $env:OPENAI_API_KEY) { throw "OPENAI_API_KEY is not set" }
$env:OPENAI_STT_MODEL = "gpt-4o-mini-transcribe"
$env:OPENAI_MODEL = "gpt-4o-mini"
"OPENAI_API_KEY configured"
"OPENAI_STT_MODEL=$env:OPENAI_STT_MODEL"
"OPENAI_MODEL=$env:OPENAI_MODEL"
```

5. Start backend and web:

```powershell
.\scripts\dev.ps1 -Service all
```

6. Execute the manual cases in `specs/audio-pipeline-phase-3-browser-manual-validation.md`.
   - Before diagnosing backend/STT failures, confirm the browser site settings are using the intended physical microphone.
7. Capture evidence in `docs/project-journal/week-03.md`.
8. If all required cases pass, update the status docs listed in the source spec.
9. Run final checks:

```powershell
.\scripts\test.ps1 -Target python
.\scripts\test.ps1 -Target web
.\scripts\build.ps1 -Target web
git diff --check
git status --short --branch
```

## Acceptance Criteria

- [x] Evidence proves browser microphone capture reached the real `POST /chat/audio` backend.
- [x] Transcript is real, non-empty, and not `[audio input captured]`.
- [x] Response text is visible and educational.
- [x] Browser speech playback is audible.
- [x] `/chat` text fallback still works.
- [x] No visible WAV upload path exists in the web UI.
- [x] No new endpoint, backend transcoding, persistence, auth, local STT, backend TTS, or dependency is introduced.
- [x] Documentation reflects complete status based on evidence.

## Implementation Prompt

```text
Execute the Phase 3 Browser Manual Validation for TONTO Kids Assistant.

Before editing:
- Read AGENTS.md.
- Read docs/ai-assisted-workflow.md.
- Read specs/audio-pipeline-phase-3-browser-manual-validation.md.
- Read specs/audio-pipeline-phase-3-web-loop.md.
- Read specs/web-validation-client.md.
- Read this plan.
- Run git branch --show-current and git status --short --branch.
- Preserve unrelated user changes in the worktree.

Goal:
- Validate the implemented browser microphone -> WAV PCM 16 kHz mono -> POST /chat/audio -> transcript -> response text -> browser speech loop against the real backend.
- Record evidence that closes the Phase 3 spec and feature if validation passes.

Constraints:
- Do not add a backend endpoint.
- Do not add dependencies.
- Do not expose manual WAV upload in the UI.
- Do not add backend transcoding, backend TTS, local STT, streaming, persistence, auth, or advanced UI.
- Keep /chat as the stable fallback.

Execution:
- Run the automated checks listed in this plan.
- Start backend and web with .\scripts\dev.ps1 -Service all.
- Execute every manual case in specs/audio-pipeline-phase-3-browser-manual-validation.md.
- Update docs/project-journal/week-03.md with real evidence.
- If validation passes, update status docs to mark Phase 3 complete.
- If validation fails, document the blocker and keep Phase 3 open.

Verification:
- Run .\scripts\test.ps1 -Target python.
- Run .\scripts\test.ps1 -Target web.
- Run .\scripts\build.ps1 -Target web.
- Run git diff --check.
- Run git status --short --branch.

Delivery:
- Summarize evidence captured.
- State whether Phase 3 is complete, partial, or blocked.
- List files updated and checks run.
```

## Notes / Assumptions

- Manual validation may require browser microphone permission and audible speaker output.
- If `POST /chat/audio` returns `422` for no recognizable speech while the WAV contract is otherwise valid, first check the browser-selected microphone. A wrong host/browser input can produce silence or unusable speech even when the backend is healthy.
- Do not record or commit API keys, audio files, or screenshots containing secrets.
- If a negative case cannot be reproduced reasonably in the chosen browser, record that limitation and the observed supported behavior.
