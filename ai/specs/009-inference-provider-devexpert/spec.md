---
id: "009-inference-provider-devexpert"
title: "Inference Provider - DevExpert"
status: done
owner: "Unknown — legacy ownership not recorded"
created: "2026-06-13"
updated: "2026-10-06"
related:
  - "specs/inference-provider-devexpert.md"
  - "ai/specs/001-historical-records-migration/metadata-review.md"
  - "https://github.com/joseluisillana/tonto-kids-assistant/issues/48"
  - "https://github.com/joseluisillana/tonto-kids-assistant/issues/51"
  - "https://github.com/joseluisillana/tonto-kids-assistant/issues/49"
  - "docs/project-journal/week-05.md"
  - "ai/specs/009-inference-provider-devexpert/plan.md"
---

# Inference Provider - DevExpert

**Status:** Chat and STT provider implemented
**Last Updated:** 2026-06-13

## Objective

Document the planned DevExpert Inference provider for TONTO.

DevExpert should let the project run the same MVP backend contracts using the AI Expert course gateway instead of paid OpenAI credentials.

## External Documentation

Live docs:

- `https://portal.devexpert.io/docs`
- `https://portal.devexpert.io/docs/endpoint`
- `https://portal.devexpert.io/docs/chat`
- `https://portal.devexpert.io/docs/stt`
- `https://portal.devexpert.io/docs/tts`

Repo-local agent guidance:

- `.agents/skills/devexpert-inference/SKILL.md`
- `.agents/skills/devexpert-inference/references/endpoint-summary.md`

Agents should verify live docs when endpoint behavior, model availability, or provider examples matter.

## Planned Role

DevExpert will be an alternate backend inference provider.

Planned TONTO paths:

- `POST /chat` -> DevExpert Chat Completions -> TONTO JSON response. Implemented in Phase 1 of `ai/specs/011-inference-providers/spec.md`.
- `POST /chat/audio` -> DevExpert STT -> DevExpert Chat Completions -> TONTO JSON response. Implemented in Phase 2 of `ai/specs/011-inference-providers/spec.md`.

Speech output remains unchanged in the initial implementation:

- Raspberry uses local `espeak`.
- Web uses browser native speech synthesis.

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `TONTO_INFERENCE_PROVIDER` | `openai` | Set to `devexpert` to use DevExpert. |
| `DEVEXPERT_API_KEY` | unset | Required for DevExpert calls. |
| `DEVEXPERT_BASE_URL` | `https://inference.devexpert.io/v1` | DevExpert OpenAI-compatible base URL. |
| `DEVEXPERT_CHAT_MODEL` | `mimo-v2.5` | Planned default chat model. |
| `DEVEXPERT_STT_MODEL` | `gpt-4o-mini-transcribe` | Planned STT model. |

The API key must never be committed, printed, or documented with a real value.

## Text Generation

Planned endpoint:

```text
POST /chat/completions
```

Full default URL:

```text
https://inference.devexpert.io/v1/chat/completions
```

Planned request shape:

```json
{
  "model": "mimo-v2.5",
  "messages": [
    {"role": "system", "content": "TONTO instructions"},
    {"role": "user", "content": "Recent context and new user message"}
  ]
}
```

Response extraction:

```text
choices[0].message.content
```

Do not assume DevExpert supports OpenAI `/responses` unless the live docs explicitly add that support.

## Instructions

The DevExpert provider must preserve the same TONTO assistant behavior as OpenAI:

- answer in Spanish,
- use clear, warm, child-friendly language,
- keep answers short,
- be factually careful,
- answer directly first,
- use one simple example or comparison when helpful,
- avoid long lists, markdown, and lecture-style answers,
- use recent conversation context,
- respond naturally to greetings and farewells.

## STT

Planned endpoint:

```text
POST /audio/transcriptions
```

Full default URL:

```text
https://inference.devexpert.io/v1/audio/transcriptions
```

Model:

```text
gpt-4o-mini-transcribe
```

Request shape:

- `multipart/form-data`,
- `model`,
- `language` when supported by the provider,
- `response_format=json` when supported by the provider,
- `file`.

Response extraction:

- read `text`,
- strip surrounding whitespace,
- return `422` at `/chat/audio` level when the transcript is empty.

## Error Behavior

The DevExpert provider should use clear backend errors:

- missing `DEVEXPERT_API_KEY` -> `500`,
- provider HTTP error -> `502`,
- provider network failure -> `502`,
- provider timeout -> `504`,
- invalid provider JSON -> `502` where applicable,
- missing response text or transcript -> `502`.

Provider errors must not expose API keys.

## Acceptance Criteria

When DevExpert is implemented:

- `TONTO_INFERENCE_PROVIDER=devexpert` routes text generation to DevExpert. Implemented in Phase 1.
- `TONTO_INFERENCE_PROVIDER=devexpert` routes STT to DevExpert. Implemented in Phase 2.
- `/chat` response shape stays unchanged.
- `/chat/audio` response shape stays unchanged.
- DevExpert text payload and response extraction are covered by tests.
- DevExpert STT payload and response extraction are covered by tests.
- Missing key and provider failure behavior are covered by tests.

## Out of Scope

- DevExpert TTS.
- Provider fallback or balancing.
- Frontend provider selector.
- Gemini or any non-DevExpert provider.
- Local STT or local AI models.

## Migration provenance and supported current state

- Original repository source: `specs/inference-provider-devexpert.md` at baseline 818e88e.
- First recorded Git date: 2026-06-13; actual original authoring date is unknown
  unless explicitly recorded in the preserved body.
- Last source Git date before migration: 2026-06-13.
- Migration/update date: 2026-10-06. Legacy owner/authorship is not established;
  the current owner field records that uncertainty, not a fabricated attribution.
- Status decision: Provider phases 0-3 completed 2026-06-13. D025 deprecates real DevExpert operation; done records historical adapter delivery, not current provider availability.
- Evidence: [source](../../../docs/project-journal/week-05.md).
- Corresponding GitHub tracking issues: [GitHub issue](https://github.com/joseluisillana/tonto-kids-assistant/issues/48), [GitHub issue](https://github.com/joseluisillana/tonto-kids-assistant/issues/51), [GitHub issue](https://github.com/joseluisillana/tonto-kids-assistant/issues/49).

Historical headings below/above retain the original reported state. YAML status
and this provenance annotation express the supported state after evidence review.
Do not execute archived proposals or historical operating examples without a new
authorized work item. No runtime or acceptance behavior changed by relocation.

Maintain plan.md/journal.md and synchronize status/updated with the parent INDEX.md
in the same change. No secrets, credentials, tokens, connection strings, PII or
real customer data; sensitive configuration is described by parameter name only.
