# Decisions

## D001 - Backend MVP language

Use Python/FastAPI for the MVP backend.

## D002 - First API endpoint

Use POST /chat.

## D003 - TTS ownership

Use local Raspberry Pi TTS with espeak for the first milestone.

## D004 - Memory

Use in-memory short session history only.

## D005 - Network configuration

Raspberry uses TONTO_BACKEND_URL; never localhost unless backend runs on Raspberry.

## D006 - Latency target

Target < 5 seconds end-to-end for MVP; improve later.

## D007 - First implementation scope

No STT, wake word, Arduino, advanced product UI, persistent memory or auth in the first implementation slice.

## D008 - Web validation client

Add a lightweight React + TypeScript + Vite web client under `web/` as a validation and demo surface. It consumes the same backend HTTP contracts as the Raspberry Pi client and must not duplicate AI orchestration or hardware responsibilities.

## D009 - Go checks deferred from CI

Do not run Go checks in CI while the MVP backend language is Python/FastAPI and Go is not selected in the active specs. Existing Go files are treated as legacy or evaluation artifacts, not as release gates. Reintroduce Go CI only if a future decision makes Go part of the active implementation.

## D010 - Local automation and isolated environments

Use PowerShell scripts under `scripts/` as the official command surface for setup, dev servers, tests, and builds. Python dependencies live in the repo-local `.venv/`; frontend dependencies live in `web/node_modules/`. Agents, humans, and CI should use the same scripts instead of installing packages globally or inventing one-off commands.
