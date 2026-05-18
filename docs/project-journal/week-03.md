# Week 03 Kickoff

**Date:** 2026-05-18
**Status:** Repository kickoff prepared; hardware voice validation pending.

## Objective

Start Week 03 from a clean, reproducible local repo state and unblock the first real voice pipeline without implementing audio changes yet.

The target for the week remains:

```text
voice -> Raspberry capture -> backend STT -> /chat -> response -> local TTS
```

## Repo Preparation

- Branch: `docs/week-3-kickoff`.
- Current stable contract: `POST /chat` with `session_id` and `message`.
- No audio endpoint added during kickoff preparation.
- No new runtime or development dependency added during kickoff preparation.
- Go remains outside the active MVP and CI gate.

## Local Validation Checklist

- [x] Run `.\scripts\setup-dev.ps1` if `.venv` or `web/node_modules` are missing.
- [x] Run `.\scripts\test.ps1 -Target all`.
- [x] Run `.\scripts\build.ps1 -Target all`.
- [ ] Start backend with `.\scripts\dev.ps1 -Service backend -AllowLan`.
- [x] Confirm `/health` from the Windows host.
- [ ] Confirm Raspberry can still run the Week 02 text loop against `TONTO_BACKEND_URL`.
- [ ] Confirm TTS output still works with `espeak`.

PowerShell profile or oh-my-posh warnings are local shell noise unless an official script fails.

`/health` was confirmed with a temporary direct uvicorn process on the Windows host. The LAN-mode `dev.ps1` startup remains pending for Raspberry validation.

## Hardware Voice Checklist

- [ ] Connect USB microphone to Raspberry Pi.
- [ ] Confirm microphone appears in `arecord -l`.
- [ ] Record a short WAV sample.
- [ ] Replay the WAV sample locally.
- [ ] Note device name, command used, sample duration, and any audio quality issue.
- [ ] Decide the smallest STT/backend contract only after capture is reproducible.

## Guardrails

- Keep Raspberry as a thin client: capture audio, call backend, play TTS.
- Treat backend STT as the provisional default because it keeps the MVP simple and the Raspberry client thin.
- Do not describe backend STT as caused by proven Raspberry limitations unless a concrete test shows that.
- Keep manual text input available as a fallback while voice is being built.
- Do not introduce wake word, local audio models, persistence, auth, Arduino, or advanced memory in Week 03 kickoff.
