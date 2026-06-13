---
name: devexpert-inference
description: Use when working with DevExpert Inference, the OpenAI-compatible portal at inference.devexpert.io, including chat completions, STT, TTS, embeddings, provider configuration, API docs lookup, or TONTO provider integration.
---

# DevExpert Inference

Use this skill when a task touches DevExpert Inference or TONTO inference provider behavior.

This skill is designed for skills-compatible coding agents working in this repository. It requires internet access to verify live DevExpert docs when endpoint behavior or model availability matters.

## Required Context

Before changing repository behavior:

1. Read `AGENTS.md`.
2. Read `docs/ai-assisted-workflow.md`.
3. Read `specs/inference-providers.md`.
4. Read `docs/plans/inference-providers.md`.
5. Read `references/endpoint-summary.md`.

For current external details, consult the live DevExpert docs:

- `https://portal.devexpert.io/docs`
- `https://portal.devexpert.io/docs/endpoint`
- `https://portal.devexpert.io/docs/chat`
- `https://portal.devexpert.io/docs/stt`
- `https://portal.devexpert.io/docs/tts`

Do not rely on memory for model availability or endpoint behavior.

## Core Rules

- Keep the repository as the source of truth for TONTO decisions.
- Treat this skill as operational guidance, not as the canonical product spec.
- Never commit or print `DEVEXPERT_API_KEY`.
- Use `DEVEXPERT_API_KEY` from the local environment.
- Use `https://inference.devexpert.io/v1` as the default DevExpert base URL.
- Do not assume DevExpert supports OpenAI `/responses`; use `/chat/completions` for DevExpert chat unless the live docs explicitly change.
- Preserve TONTO public backend contracts: `/chat` and `/chat/audio`.
- Keep OpenAI and DevExpert working whenever inference provider code changes.
- Do not add dependencies unless the user explicitly approves them.

## TONTO Defaults

For DevExpert provider work, prefer:

| Variable | Default | Purpose |
|---|---|---|
| `TONTO_INFERENCE_PROVIDER` | `devexpert` when testing DevExpert | Select provider. |
| `DEVEXPERT_BASE_URL` | `https://inference.devexpert.io/v1` | OpenAI-compatible base URL. |
| `DEVEXPERT_CHAT_MODEL` | `mimo-v2.5` | Default chat model from public docs. |
| `DEVEXPERT_STT_MODEL` | `gpt-4o-mini-transcribe` | STT model from public docs. |

Keep OpenAI defaults separate:

| Variable | Purpose |
|---|---|
| `OPENAI_API_KEY` | OpenAI provider key. |
| `OPENAI_MODEL` | OpenAI chat/response model. |
| `OPENAI_STT_MODEL` | OpenAI STT model. |

## Validation Expectations

If changing inference code, add or maintain tests for:

- provider selection,
- missing provider-specific API keys,
- DevExpert chat `/chat/completions` payload and response extraction,
- DevExpert STT `/audio/transcriptions` payload and response extraction,
- OpenAI behavior remaining intact,
- unchanged TONTO `/chat` and `/chat/audio` response contracts.

Do not require real DevExpert or OpenAI keys in automated tests.

## Deferred Work

Do not implement these unless a spec explicitly asks for them:

- provider hot switching,
- provider fallback or balancing,
- DevExpert TTS,
- Gemini provider integration,
- frontend provider selector,
- local STT or local AI models.
