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

## D007 - Scope freeze

No STT, wake word, Arduino, UI, persistent memory or auth in the first implementation slice.
