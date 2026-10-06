---
id: "010-inference-provider-openai"
title: "Inference Provider - OpenAI"
status: done
owner: "Unknown — legacy ownership not recorded"
created: "2026-06-13"
updated: "2026-10-06"
related:
  - "specs/inference-provider-openai.md"
  - "ai/specs/001-historical-records-migration/metadata-review.md"
  - "https://github.com/joseluisillana/tonto-kids-assistant/issues/48"
  - "https://github.com/joseluisillana/tonto-kids-assistant/issues/51"
  - "https://github.com/joseluisillana/tonto-kids-assistant/issues/49"
  - "docs/project-journal/week-05.md"
  - "ai/specs/010-inference-provider-openai/plan.md"
---

# Inference Provider - OpenAI

**Status:** Current baseline with chat and STT provider selector
**Last Updated:** 2026-06-13

## Objective

Document the OpenAI provider behavior TONTO already uses before adding additional providers.

This spec is a baseline. It should protect current behavior while the shared provider layer is introduced.

## Current Role

OpenAI is the current default inference provider for the MVP backend.

Current TONTO paths:

- `POST /chat` -> OpenAI text response -> TONTO JSON response.
- `POST /chat/audio` -> OpenAI STT -> OpenAI text response -> TONTO JSON response.

As of Phase 1 of `ai/specs/011-inference-providers/spec.md`, OpenAI text generation is selected by `TONTO_INFERENCE_PROVIDER=openai` or by leaving `TONTO_INFERENCE_PROVIDER` unset. As of Phase 2, OpenAI STT is selected the same way.

Speech output is not handled by OpenAI in the current MVP:

- Raspberry uses local `espeak`.
- Web uses browser native speech synthesis.

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `TONTO_INFERENCE_PROVIDER` | `openai` | Selects OpenAI as the active provider. Planned as part of `ai/specs/011-inference-providers/spec.md`. |
| `OPENAI_API_KEY` | unset | Required for OpenAI calls. |
| `OPENAI_MODEL` | `gpt-4o-mini` | Current text response model default in `backend/openai_client.py`. |
| `OPENAI_STT_MODEL` | `gpt-4o-mini-transcribe` | Current STT model default in `backend/stt_client.py`. |

The API key must never be committed, printed, or documented with a real value.

## Text Generation

Current endpoint:

```text
POST https://api.openai.com/v1/responses
```

Current implementation sends:

- `model`,
- `instructions`,
- `input`,
- `max_output_tokens`.

The response extraction currently accepts:

- top-level `output_text`, or
- message content items of type `output_text`.

This path is acceptable for OpenAI because the Responses API is the current OpenAI-native response generation surface and fits TONTO's simple "instructions + input -> output text" shape.

## Instructions

The OpenAI provider must preserve the shared TONTO instructions:

- answer in Spanish,
- use clear, warm, child-friendly language,
- keep answers short,
- be factually careful,
- answer directly first,
- use one simple example or comparison when helpful,
- avoid long lists, markdown, and lecture-style answers,
- use recent conversation context,
- respond naturally to greetings and farewells.

These instructions may live in a shared provider-neutral constant after the provider layer is introduced.

## STT

Current endpoint:

```text
POST https://api.openai.com/v1/audio/transcriptions
```

Current request shape:

- `multipart/form-data`,
- `model`,
- `language`,
- `response_format=json`,
- `file`.

Current response extraction:

- read `text`,
- strip surrounding whitespace,
- return `422` at `/chat/audio` level when the transcript is empty.

## Error Behavior

The OpenAI provider should keep clear backend errors:

- missing `OPENAI_API_KEY` -> `500`,
- provider HTTP error -> `502`,
- provider network failure -> `502`,
- provider timeout -> `504`,
- invalid provider JSON -> `502` where applicable,
- missing response text or transcript -> `502`.

Provider errors must not expose API keys.

## Acceptance Criteria

When the shared provider layer is introduced:

- `TONTO_INFERENCE_PROVIDER=openai` remains the default.
- `/chat` response shape stays unchanged.
- `/chat/audio` response shape stays unchanged.
- Existing OpenAI text payload behavior remains covered by tests.
- Existing OpenAI STT payload behavior remains covered by tests.
- Missing key and provider failure behavior remain covered by tests.

## Out of Scope

- Migrating OpenAI text generation from Responses API to Chat Completions.
- Adding OpenAI TTS.
- Changing the active OpenAI default models unless a separate explicit decision is made.
- Adding OpenAI Assistants, Realtime, Agents SDK, or tool calling.

## Migration provenance and supported current state

- Original repository source: `specs/inference-provider-openai.md` at baseline 818e88e.
- First recorded Git date: 2026-06-13; actual original authoring date is unknown
  unless explicitly recorded in the preserved body.
- Last source Git date before migration: 2026-06-13.
- Migration/update date: 2026-10-06. Legacy owner/authorship is not established;
  the current owner field records that uncertainty, not a fabricated attribution.
- Status decision: Provider phases 0-3 completed 2026-06-13; current adapter contract remains covered, no new real-provider validation in migration.
- Evidence: [source](../../../docs/project-journal/week-05.md).
- Corresponding GitHub tracking issues: [GitHub issue](https://github.com/joseluisillana/tonto-kids-assistant/issues/48), [GitHub issue](https://github.com/joseluisillana/tonto-kids-assistant/issues/51), [GitHub issue](https://github.com/joseluisillana/tonto-kids-assistant/issues/49).

Historical headings below/above retain the original reported state. YAML status
and this provenance annotation express the supported state after evidence review.
Do not execute archived proposals or historical operating examples without a new
authorized work item. No runtime or acceptance behavior changed by relocation.

Maintain plan.md/journal.md and synchronize status/updated with the parent INDEX.md
in the same change. No secrets, credentials, tokens, connection strings, PII or
real customer data; sensitive configuration is described by parameter name only.
