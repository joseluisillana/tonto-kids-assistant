# Inference Providers Implementation Plan

**Status:** Implemented through Phase 3
**Source Spec:** `specs/inference-providers.md`
**Tracking:** GitHub parent issue #48

## Objective

Execute the extra MVP line that lets TONTO run against either OpenAI or DevExpert Inference while keeping the existing demo contracts and architecture stable.

This plan is intentionally phased. The first PR should prepare the repository and tracking only. Backend implementation should happen in later focused PRs.

## Source Specs

- General spec: `specs/inference-providers.md`
- OpenAI provider baseline: `specs/inference-provider-openai.md`
- DevExpert provider target: `specs/inference-provider-devexpert.md`
- Agent Skill: `.agents/skills/devexpert-inference/SKILL.md`
- Related docs:
  - `AGENTS.md`
  - `docs/ai-assisted-workflow.md`
  - `docs/specs.md`
  - `docs/roadmap.md`
  - `docs/demo-runbook.md`
  - `docs/project-journal/week-05.md`

## Scope

Included:

- Prepare the repo-local Agent Skill for DevExpert Inference.
- Document the provider line as an extra MVP work item.
- Document the current OpenAI provider baseline.
- Document the planned DevExpert provider.
- Implement OpenAI and DevExpert adapters for chat and STT in separate phases.
- Keep existing TONTO API contracts stable.
- Add tests that make both providers part of the required inference behavior.

Excluded:

- No provider hot switching.
- No fallback or balancing in the initial provider implementation.
- No Gemini implementation yet.
- No DevExpert TTS implementation yet.
- No new dependencies unless explicitly approved later.
- No frontend provider selector.

## Phase Plan

### Phase 0 - Planning, Provider Specs, and Repository Skill

Tracking: GitHub issue #50

Branch:

```text
docs/inference-providers-line
```

Tasks:

- Add `specs/inference-providers.md`.
- Add `specs/inference-provider-openai.md`.
- Add `specs/inference-provider-devexpert.md`.
- Add `docs/plans/inference-providers.md`.
- Add `.agents/skills/devexpert-inference/SKILL.md`.
- Add `.agents/skills/devexpert-inference/references/endpoint-summary.md`.
- Update `docs/ai-assisted-workflow.md` with Agent Skills guidance and DevExpert skill discovery.
- Update `AGENTS.md`, `docs/specs.md`, `docs/roadmap.md`, and `docs/project-journal/week-05.md` with the new extra line.
- Create GitHub issues for parent tracking and phases.

Verification:

```powershell
git diff --check
git status --short --branch
```

Implementation prompt:

```text
Prepare the TONTO repository for the extra MVP line "Inference Providers".

Before editing:
- Read AGENTS.md.
- Read docs/ai-assisted-workflow.md.
- Read docs/specs.md, docs/roadmap.md, and docs/project-journal/week-05.md.
- Run git branch --show-current and git status --short --branch.
- Work on docs/inference-providers-line, not main.

Task:
- Add the inference providers spec and paired plan.
- Add provider-specific specs for the current OpenAI baseline and planned DevExpert provider.
- Add a repo-local Agent Skill at .agents/skills/devexpert-inference/SKILL.md.
- Add a concise DevExpert endpoint summary under the skill references directory.
- Update workflow, roadmap, specs, and Week 05 journal so future agents can discover this extra line.
- Create GitHub issues for the parent line and implementation phases.
- Do not change backend, client, web, scripts, or runtime behavior in this phase.

Verification:
- Run git diff --check.
- Run git status --short --branch.

Delivery:
- Summarize the planned phases.
- List created GitHub issues.
- Recommend PR sequencing for the implementation phases.
```

### Phase 1 - Chat Provider Adapter

Tracking: GitHub issue #51

Status: implemented on 2026-06-13 in branch `feature/inference-provider-chat-adapter`.

Recommended branch:

```text
feature/inference-provider-chat-adapter
```

Tasks:

- Introduce a small backend provider boundary for text generation.
- Keep OpenAI using `/v1/responses`.
- Add DevExpert chat generation using `/v1/chat/completions`.
- Add `TONTO_INFERENCE_PROVIDER=openai|devexpert`.
- Add clear errors for missing provider-specific keys.
- Preserve `/chat` response model.
- Update focused tests.

Suggested files:

- `backend/openai_client.py` or a new small provider module under `backend/`.
- `tests/test_openai_client.py` or new focused provider tests.
- Relevant docs only if implementation changes durable behavior.

Verification:

```powershell
.\scripts\test.ps1 -Target python
git diff --check
git status --short --branch
```

Implementation prompt:

```text
Implement Phase 1 of specs/inference-providers.md: Chat Provider Adapter.

Before editing:
- Read AGENTS.md.
- Read docs/ai-assisted-workflow.md.
- Read specs/inference-providers.md and docs/plans/inference-providers.md.
- Read specs/inference-provider-openai.md and specs/inference-provider-devexpert.md.
- Read .agents/skills/devexpert-inference/SKILL.md because this phase touches DevExpert Inference.
- Run git branch --show-current and git status --short --branch.
- Work on feature/inference-provider-chat-adapter or another project branch, not main.

Task:
- Add backend provider selection for text generation with TONTO_INFERENCE_PROVIDER=openai|devexpert.
- Preserve OpenAI Responses API behavior for the openai provider.
- Add DevExpert /chat/completions behavior for the devexpert provider.
- Keep /chat request and response contracts unchanged.
- Add focused tests for both providers, provider selection, missing API keys, payloads, and response extraction.
- Do not add dependencies.
- Do not implement STT provider switching in this phase.

Verification:
- Run .\scripts\test.ps1 -Target python.
- Run git diff --check and git status --short --branch.

Delivery:
- Summarize provider behavior.
- Link the phase GitHub issue.
- State any manual credential-based validation that was or was not run.
```

### Phase 2 - STT Provider Adapter

Tracking: GitHub issue #49

Status: implemented on 2026-06-13 in branch `feature/inference-provider-stt-adapter`.

Recommended branch:

```text
feature/inference-provider-stt-adapter
```

Tasks:

- Extend provider selection to STT.
- Keep OpenAI STT behavior stable.
- Add DevExpert `/audio/transcriptions` behavior.
- Preserve `/chat/audio` request and response contracts.
- Add focused tests.

Verification:

```powershell
.\scripts\test.ps1 -Target python
git diff --check
git status --short --branch
```

Implementation prompt:

```text
Implement Phase 2 of specs/inference-providers.md: STT Provider Adapter.

Before editing:
- Read AGENTS.md.
- Read docs/ai-assisted-workflow.md.
- Read specs/inference-providers.md and docs/plans/inference-providers.md.
- Read specs/inference-provider-openai.md and specs/inference-provider-devexpert.md.
- Read .agents/skills/devexpert-inference/SKILL.md because this phase touches DevExpert Inference.
- Run git branch --show-current and git status --short --branch.
- Work on feature/inference-provider-stt-adapter or another project branch, not main.

Task:
- Extend TONTO_INFERENCE_PROVIDER selection to backend STT.
- Preserve OpenAI /audio/transcriptions behavior.
- Add DevExpert /audio/transcriptions behavior with DEVEXPERT_STT_MODEL.
- Keep WAV validation and /chat/audio response contract unchanged.
- Add tests for both provider STT request construction, missing keys, provider selection, response extraction, and provider errors.
- Do not add dependencies.
- Do not implement TTS provider switching.

Verification:
- Run .\scripts\test.ps1 -Target python.
- Run git diff --check and git status --short --branch.

Delivery:
- Summarize STT provider behavior.
- Link the phase GitHub issue.
- State any manual credential-based validation that was or was not run.
```

### Phase 3 - Runbook, Scripts, and Dual-Provider Validation

Tracking: GitHub issue #52

Status: implemented on 2026-06-13 in branch `docs/inference-provider-runbook`.

Recommended branch:

```text
docs/inference-provider-runbook
```

Tasks:

- Document how to run with OpenAI and DevExpert.
- Decide whether official scripts need a `-Provider` option or whether environment variables are sufficient.
- Update `.env.example`, demo runbook, and workflow docs as needed.
- Record validation evidence for both providers without exposing secrets.

Verification:

```powershell
.\scripts\test.ps1 -Target python
git diff --check
git status --short --branch
```

Implementation prompt:

```text
Implement Phase 3 of specs/inference-providers.md: Runbook, Scripts, and Dual-Provider Validation.

Before editing:
- Read AGENTS.md.
- Read docs/ai-assisted-workflow.md.
- Read specs/inference-providers.md and docs/plans/inference-providers.md.
- Read specs/inference-provider-openai.md and specs/inference-provider-devexpert.md.
- Read .agents/skills/devexpert-inference/SKILL.md.
- Run git branch --show-current and git status --short --branch.
- Work on docs/inference-provider-runbook or another project branch, not main.

Task:
- Update docs so humans and agents can start TONTO with OpenAI or DevExpert.
- If scripts need a provider option, keep it narrow and update docs in the same change.
- Update .env.example or setup docs with provider variables, without secrets.
- Record validation evidence for both providers where credentials are available.
- Keep existing demo contracts and clients unchanged.

Verification:
- Run .\scripts\test.ps1 -Target python.
- Run git diff --check and git status --short --branch.

Delivery:
- Summarize docs and script changes.
- Link the phase GitHub issue.
- State exact validation performed for each provider.
```

## Acceptance Criteria

- The extra MVP line is tracked by a parent GitHub issue and phase issues.
- The OpenAI provider baseline is documented before implementation changes begin.
- The DevExpert Inference Agent Skill exists in the repo and is discoverable by skills-compatible agents.
- Backend implementation phases keep OpenAI and DevExpert working through tests.
- TONTO clients remain provider-agnostic.
- Future Gemini work can add a provider without rewriting the whole inference flow.

## GitHub Tracking

| Work item | Issue |
|---|---|
| Parent line | #48 |
| Phase 0 - Planning, Provider Specs, and Repository Skill | #50 |
| Phase 1 - Chat Provider Adapter | #51 |
| Phase 2 - STT Provider Adapter | #49 |
| Phase 3 - Runbook, Scripts, and Dual-Provider Validation | #52 |
| Future backlog - fallback, balancing, DevExpert TTS, Gemini | #53 |

## Workflow Isolation

- Phase 0 branch: `docs/inference-providers-line`.
- Later phases should each use their own branch and PR.
- Parallel-safe: Phase 1 and Phase 2 both touch backend provider code and should not run in parallel unless they use separate worktrees and reconcile carefully.
- Collision risk:
  - `backend/openai_client.py`
  - `backend/stt_client.py`
  - `backend/audio_router.py`
  - `tests/test_openai_client.py`
  - `tests/test_stt_client.py`
  - `docs/ai-assisted-workflow.md`
  - `docs/demo-runbook.md`
- Integration note: merge Phase 0 first, then implement Phase 1 before Phase 2 so STT can reuse the provider selection shape.

## Notes / Assumptions

- DevExpert default chat model is planned as `mimo-v2.5` because the public docs recommend it for everyday use.
- `deepseek-v4-flash` remains the recommended OpenCode model unless a later decision changes that tool setup.
- DevExpert TTS is intentionally deferred so the existing Raspberry `espeak` demo remains stable.
