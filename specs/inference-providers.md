# Extra MVP Line - Inference Providers

**Status:** Implemented through Phase 3
**Tracking:** GitHub parent issue #48
**Last Updated:** 2026-06-13

## Objective

Define and implement a small provider layer so TONTO can run the same MVP stack with either OpenAI or DevExpert Inference.

This is an extra MVP line for the AI Expert course context. It must preserve the current demo-first architecture: Raspberry and web clients keep calling the same TONTO backend contracts, while the backend selects the configured inference provider at startup.

## Why This Exists

TONTO currently uses OpenAI directly:

- text response generation through OpenAI Responses API,
- backend STT through OpenAI-compatible audio transcriptions,
- local Raspberry speech output through `espeak`,
- browser speech output through native Web Speech API.

DevExpert Inference is the AI Expert course gateway. It exposes an OpenAI-compatible API at:

```text
https://inference.devexpert.io/v1
```

Using it inside TONTO makes the final project better aligned with the course environment and reduces dependency on paid OpenAI credits during development and demos.

## Related Provider Specs

- `specs/inference-provider-openai.md` documents the current OpenAI baseline.
- `specs/inference-provider-devexpert.md` documents the planned DevExpert provider.

Future providers, such as Gemini, should add their own provider spec before implementation.

## GitHub Tracking

| Work item | Issue |
|---|---|
| Parent line | #48 |
| Phase 0 - Planning, Provider Specs, and Repository Skill | #50 |
| Phase 1 - Chat Provider Adapter | #51 |
| Phase 2 - STT Provider Adapter | #49 |
| Phase 3 - Runbook, Scripts, and Dual-Provider Validation | #52 |
| Future backlog - fallback, balancing, DevExpert TTS, Gemini | #53 |

## Source of Truth

Project decisions and implementation requirements live in these specs and their paired plan:

- `specs/inference-providers.md`
- `specs/inference-provider-openai.md`
- `specs/inference-provider-devexpert.md`
- `docs/plans/inference-providers.md`

Agent operating knowledge lives in the repo-local Agent Skill:

- `.agents/skills/devexpert-inference/SKILL.md`
- `.agents/skills/devexpert-inference/references/endpoint-summary.md`

DevExpert public documentation remains the live external source:

- `https://portal.devexpert.io/docs`
- `https://portal.devexpert.io/docs/endpoint`
- `https://portal.devexpert.io/docs/chat`
- `https://portal.devexpert.io/docs/stt`
- `https://portal.devexpert.io/docs/tts`

Agents must not treat copied summaries as a substitute for checking the live docs when endpoint behavior, models, or provider capabilities matter.

## Common Provider Contract

The backend provider layer should expose the smallest behavior TONTO needs:

- generate a child-friendly educational response from recent conversation history and a new user message,
- transcribe a short WAV audio turn to text,
- surface clear provider errors without leaking secrets.

The provider layer must not change the public TONTO API contracts:

- `POST /chat`
- `POST /chat/audio`

The Raspberry client and web validation client must remain provider-agnostic.

## Design Principles

- Keep TONTO clients provider-agnostic.
- Select the provider at backend startup by configuration; no hot switching is required.
- Preserve the existing `/chat` and `/chat/audio` TONTO contracts.
- Use the most appropriate API shape per provider:
  - OpenAI text generation may continue using `/v1/responses`.
  - DevExpert text generation should use `/v1/chat/completions`.
- Keep provider-specific request and response mapping behind a small backend adapter boundary.
- Keep tests provider-aware so changes to inference must preserve both OpenAI and DevExpert behavior.
- Leave the design open for a future Gemini provider without implementing Gemini in this line.

## Provider Configuration

Initial provider selector:

| Variable | Values | Default | Purpose |
|---|---|---|---|
| `TONTO_INFERENCE_PROVIDER` | `openai`, `devexpert` | `openai` | Selects the backend inference provider at startup. |

Provider-specific variables are documented in:

- `specs/inference-provider-openai.md`
- `specs/inference-provider-devexpert.md`

Secrets must never be committed or printed in logs.

## Scope

Included:

- Document the extra line and phase issues.
- Add a repo-local Agent Skill for DevExpert Inference.
- Add backend provider selection for OpenAI and DevExpert.
- Keep OpenAI text generation on the current Responses API path unless a later explicit decision changes it.
- Add DevExpert chat generation through `/chat/completions`.
- Add DevExpert STT through `/audio/transcriptions`.
- Update docs, runbooks, and validation instructions so either provider can run the stack.
- Require tests or mocks proving both providers still work when inference code changes.

Excluded:

- No hot switching between providers.
- No automatic fallback or balancing between providers.
- No Gemini implementation in this line.
- No DevExpert TTS integration unless a later phase explicitly adds a separate spike.
- No local AI models.
- No local STT.
- No persistence, auth, multi-user state, or advanced memory.
- No frontend provider selector.
- No new runtime or development dependency without an explicit decision.

## Phases

### Phase 0 - Planning, Provider Specs, and Repository Skill

Prepare the project to execute this line:

- create this spec and paired implementation plan,
- document the current OpenAI provider baseline,
- document the planned DevExpert provider,
- create the repo-local Agent Skill for DevExpert Inference,
- update AI-assisted workflow docs so agents know when to use the skill,
- update roadmap and journal with this extra MVP line,
- create GitHub issues for the parent line and implementation phases.

Acceptance:

- The repository explains where this line lives and why it is outside the normal Week 05 phases.
- The OpenAI baseline is explicit before DevExpert implementation starts.
- Agents can discover `.agents/skills/devexpert-inference/SKILL.md`.
- The plan includes implementation prompts for future phases.
- GitHub tracking issues exist.

### Phase 1 - Chat Provider Adapter

Status: implemented on 2026-06-13 in branch `feature/inference-provider-chat-adapter`.

Add provider selection for text response generation while preserving the `/chat` contract.

Expected behavior:

- `TONTO_INFERENCE_PROVIDER=openai` keeps OpenAI behavior.
- `TONTO_INFERENCE_PROVIDER=devexpert` sends TONTO chat requests to DevExpert `/chat/completions`.
- Both paths apply the same TONTO system behavior: Spanish, child-friendly, short, factual, and context-aware.
- Missing provider-specific API keys fail with clear backend errors.

Acceptance:

- Focused tests cover OpenAI payload and response extraction.
- Focused tests cover DevExpert payload and response extraction.
- `/chat` response shape remains unchanged.
- No client or web contract changes are required.

### Phase 2 - STT Provider Adapter

Status: implemented on 2026-06-13 in branch `feature/inference-provider-stt-adapter`.

Extend provider selection to backend STT for `/chat/audio`.

Expected behavior:

- OpenAI continues to use the current transcription path.
- DevExpert uses `/audio/transcriptions` with `DEVEXPERT_STT_MODEL`.
- WAV validation, duration limits, transcript handling, and `422` empty transcript behavior remain unchanged.

Acceptance:

- Focused tests cover OpenAI STT request construction.
- Focused tests cover DevExpert STT request construction.
- `/chat/audio` response shape remains unchanged.
- No manual WAV upload/file picker is introduced into the product/demo UI.

### Phase 3 - Runbook, Scripts, and Dual-Provider Validation

Status: implemented on 2026-06-13 in branch `docs/inference-provider-runbook`.

Make provider selection easy to operate for humans and agents.

Expected behavior:

- Docs explain how to start the backend with OpenAI or DevExpert.
- Official scripts either accept a narrow provider option or document the required environment variables clearly.
- Validation evidence records that both providers can run the demo stack, at least through mocked automated tests and one manual provider-specific check where credentials are available.

Acceptance:

- `docs/demo-runbook.md` explains provider selection without exposing secrets.
- `.env.example` or equivalent setup docs list provider variables.
- `docs/ai-assisted-workflow.md` states that inference changes must preserve both OpenAI and DevExpert.
- Verification commands are documented and use official scripts.

### Future Phase - Fallbacks, Balancing, and Additional Providers

Deferred possibilities:

- fallback to the inactive provider when the active provider fails,
- provider balancing,
- DevExpert TTS spike,
- Gemini provider integration.

These require separate specs or explicit spec amendments before implementation.

## Validation Requirements

Any change that touches inference provider behavior must keep both providers working.

Minimum automated coverage:

- provider selection,
- missing API key errors,
- OpenAI text adapter request and response extraction,
- DevExpert text adapter request and response extraction,
- OpenAI STT adapter request and response extraction,
- DevExpert STT adapter request and response extraction,
- unchanged `/chat` and `/chat/audio` response contracts.

Manual validation with real credentials is encouraged for provider integration phases, but CI must not require real OpenAI or DevExpert keys.

## Open Questions

- Should scripts expose `-Provider openai|devexpert`, or should provider selection remain purely environment-variable based for the first implementation?
- Should DevExpert default to `mimo-v2.5` for demo consistency or `deepseek-v4-flash` to match the current OpenCode recommendation?
- Should DevExpert TTS become a later quality spike after the provider switch is stable?
