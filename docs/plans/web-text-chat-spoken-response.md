# Web Text Chat Spoken Response Implementation Plan

## Objective

Implement the web client UX change documented in `specs/web-validation-client.md`: typed `/chat` responses should stay visible in the chat and also be spoken aloud by the browser when Web Speech API is available.

## Source Spec

- Spec: `specs/web-validation-client.md`
- Related docs:
  - `docs/specs.md`

## Scope

Included:

- Reuse the existing browser speech synthesis path for typed chat responses.
- Preserve the current `/chat` request/response contract.
- Keep text chat usable if speech synthesis is unsupported or playback fails.
- Add focused web tests for speech playback success and fallback behavior.

Excluded:

- Backend changes, backend TTS, new endpoints, Raspberry client changes, new dependencies, persistence, settings toggles, or manual audio upload UI.

## Implementation Plan

- Update the web conversation state so `sendMessage` speaks `response_text` after adding the assistant message to the visible transcript.
- Use existing speech status fields to show speaking state and record the selected browser voice.
- Treat typed-chat speech failures as a non-blocking degradation: keep the response visible and return the conversation to idle.
- Add a small reusable speech fallback helper in the web audio utilities so the behavior is testable without a React test harness.
- Update the spec and global specs summary to reflect the new durable web behavior.

## Acceptance Criteria

- Typed chat responses are displayed and then spoken aloud automatically in browsers with speech synthesis.
- The UI returns to idle after speech completes.
- If speech is unsupported or fails, the written response remains visible and the chat is not blocked.
- The Phase 3 microphone voice flow remains unchanged.
- No backend contract, dependency, or Raspberry behavior changes.

## Verification

Use official project scripts:

```powershell
.\scripts\test.ps1 -Target web
.\scripts\build.ps1 -Target web
.\scripts\test.ps1 -Target all
git diff --check
git status --short --branch
```

## Implementation Prompt

```text
Implement the web text chat spoken response change for TONTO Kids Assistant.

Before editing:
- Read AGENTS.md.
- Read docs/ai-assisted-workflow.md.
- Read specs/web-validation-client.md.
- Read docs/plans/web-text-chat-spoken-response.md.
- Run git branch --show-current and git status --short --branch.
- If on main, create a project branch such as feature/web-text-spoken-response before editing.
- Preserve unrelated user changes in the worktree.

Task:
- Keep POST /chat unchanged.
- When sendMessage receives response_text, add it to the visible chat and speak the same text with native browser speech synthesis.
- Reuse the existing speech synthesis helpers and Spanish voice preference.
- Show speaking state while playback is active.
- If browser speech is unsupported or playback fails, keep text chat working and do not treat the whole chat turn as failed.
- Keep repeatLatest working for the latest assistant response regardless of whether it came from typed text or microphone input.
- Do not add dependencies, backend TTS, new endpoints, persistence, settings toggles, or manual audio upload UI.

Verification:
- Run .\scripts\test.ps1 -Target web.
- Run .\scripts\build.ps1 -Target web.
- Run .\scripts\test.ps1 -Target all.
- Run git diff --check.
- Run git status --short --branch.

Delivery:
- Summarize changed files.
- Summarize the new typed-chat spoken response behavior.
- Summarize verification results and any remaining manual validation.
```

## Notes / Assumptions

- Spoken response for typed chat is automatic by default.
- Web Speech API remains the MVP path; no backend TTS is introduced.
- The feature applies only to the web validation/demo client.
