# DevExpert Inference Endpoint Summary

Last reviewed from public docs on 2026-06-13.

Live docs:

- `https://portal.devexpert.io/docs`
- `https://portal.devexpert.io/docs/endpoint`
- `https://portal.devexpert.io/docs/chat`
- `https://portal.devexpert.io/docs/stt`
- `https://portal.devexpert.io/docs/tts`
- `https://portal.devexpert.io/docs/embeddings`
- `https://portal.devexpert.io/docs/images`

## Base URL

```text
https://inference.devexpert.io/v1
```

The portal describes DevExpert Inference as OpenAI-compatible. Tools that accept a base URL, API key, and model name can usually use it.

## Authentication

Use:

```text
Authorization: Bearer <DEVEXPERT_API_KEY>
```

Recommended local environment variable:

```text
DEVEXPERT_API_KEY
```

Never commit or print the key.

## Chat

Endpoint:

```text
POST /chat/completions
```

Recommended default model:

```text
mimo-v2.5
```

Other documented chat models:

```text
deepseek-v4-flash
deepseek-v4-pro
mimo-v2.5-pro
```

Use the standard chat completions shape:

```json
{
  "model": "mimo-v2.5",
  "messages": [
    {"role": "system", "content": "System instruction"},
    {"role": "user", "content": "User message"}
  ]
}
```

Read response text from `choices[0].message.content`.

## STT

Endpoint:

```text
POST /audio/transcriptions
```

Model:

```text
gpt-4o-mini-transcribe
```

Use `multipart/form-data` with a `file` field and `model` field. TONTO sends WAV fixtures and browser/Raspberry WAV captures through `/chat/audio`.

## TTS

Endpoint:

```text
POST /audio/speech
```

Model:

```text
gpt-4o-mini-tts
```

TTS is documented by DevExpert, but TONTO should not adopt it without a separate explicit phase. The current MVP demo uses Raspberry `espeak` and browser native speech output.

## Embeddings

Endpoint:

```text
POST /embeddings
```

Model:

```text
text-embedding-3-small
```

Embeddings are out of scope for the current MVP provider switch.

## Images

Endpoints:

```text
POST /images/generations
POST /images/edits
```

Models:

```text
nano-banana
nano-banana-edit
```

Image generation and editing are out of scope for the current MVP provider switch.
