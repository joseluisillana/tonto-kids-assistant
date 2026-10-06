# Shared contract context

Read [root](../AGENTS.md) and [workflow](../docs/ai-assisted-workflow.md) first.

This directory reserves shared request/response structures when needed.
`models.py` currently contains only a placeholder comment; `__init__.py` makes
the directory importable. No active client/backend imports of shared models were
found. Do not present the reservation as an implemented contract library.

Depends on: no implemented shared runtime dependencies. Used by: syntax checking
and Compose source mounts; no current runtime model consumers. Actual HTTP models
are in backend/main.py and backend/audio_router.py; web holds TypeScript mirrors.
Future shared model work must review [backend](../backend/AGENTS.md),
[client](../client/AGENTS.md), [web](../web/AGENTS.md) and
[tests](../tests/AGENTS.md), preserving public HTTP contracts.

Read [architecture](../docs/architecture.md),
[conversation](../ai/specs/007-conversation-loop/spec.md) and [audio](../ai/specs/005-audio-pipeline/spec.md).
`./tonto.sh test python` checks syntax here; no dedicated shared behavior tests
exist. A new shared behavior needs focused tests; this placeholder alone does not
justify new abstractions or dependencies.
