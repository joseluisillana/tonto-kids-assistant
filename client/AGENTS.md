# Raspberry and touch client context

Read [root](../AGENTS.md) and [workflow](../docs/ai-assisted-workflow.md) first;
also [backend](../backend/AGENTS.md) for HTTP changes,
[scripts](../scripts/AGENTS.md) for startup and [tests](../tests/AGENTS.md) for checks.

## Purpose and structure

Thin Python device client for text/voice HTTP turns and local speech; Kivy touch
UI reuses the same client helpers. `main.py` is the CLI with text/voice/touch modes,
capture_audio, send_message, send_audio and speak. `touch_ui.py` defines
TontoTouchUI/TontoTouchApp, threading and mainthread UI updates. `tonto_face.py`
defines FaceState/TontoFace animations. `requirements.txt` and
`requirements-pc.txt` cover different device/PC needs; `Dockerfile.ui` and
`.dockerignore` define emulator library build, not an image with all repo sources.

## Interfaces and dependency flow

Depends on: backend `/health`, `/chat`, `/chat/audio` over HTTP; Raspberry arecord
and espeak; PC capture uses sounddevice/soundfile/numpy; UI uses Kivy. Machine
configuration uses TONTO_BACKEND_URL, audio and TTS variables, not backend keys.
`touch_ui.py` imports client/main helpers and TontoFace; main imports touch UI
lazily for touch mode. Scripts demo-raspberry/demo-touch and Compose UI emulator
launch this client. tests/test_client.py, test_touch_ui.py and test_tonto_face.py
consume its functions/widgets; spikes/ui_kivy does not replace them.
shared/models.py is not imported. AI orchestration remains in backend.

## Impact, tests and documentation

Helper changes affect terminal and touch flows; state/animation changes affect
touch widget tests. Preserve HTTP shapes, text fallback, timeouts, unavailable
TTS handling and cleanup of captured files. Do not interpret simulated audio or
Xvfb as physical validation. Read [audio spec](../ai/specs/005-audio-pipeline/spec.md),
[touch spec](../ai/specs/021-raspberry-touch-ui/spec.md),
[Kivy coverage](../ai/specs/013-kivy-ui-testing-coverage/spec.md),
[emulator spec](../ai/specs/012-kivy-ui-docker-emulation/spec.md) and
[Raspberry setup](../docs/raspberry-pi-setup.md) as applicable.

From root: `./tonto.sh test python` for client helpers, `./tonto.sh test ui` for
real Kivy widgets under Xvfb. `./tonto.sh dev ui` is the Linux emulator. Raspberry
uses its repo-local .venv via `./scripts/demo-raspberry.sh` or
`./scripts/demo-touch.sh`; follow the [runbook](../docs/demo-runbook.md) and
[checklist](../docs/demo-checklist.md) before operation. Live voice guidance is
[raspberry-voice-demo](../.agents/skills/raspberry-voice-demo/SKILL.md), readable
manually; operation alone does not authorize source edits.
