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
- [x] Start backend with `.\scripts\dev.ps1 -Service backend -AllowLan`.
- [x] Confirm `/health` from the Windows host.
- [x] Confirm Raspberry can still run the Week 02 text loop against `TONTO_BACKEND_URL`.
- [x] Confirm TTS output still works with `espeak`.

PowerShell profile or oh-my-posh warnings are local shell noise unless an official script fails.

The local Week 03 kickoff checklist is complete. Hardware voice validation remains separate and starts with microphone detection, WAV recording, and WAV playback on the Raspberry Pi.

## Hardware Voice Checklist

- [ ] Connect USB microphone to Raspberry Pi.
- [ ] Confirm microphone appears in `arecord -l`.
- [ ] Record a short WAV sample.
- [ ] Replay the WAV sample locally.
- [ ] Note device name, command used, sample duration, and any audio quality issue.
- [ ] Decide the smallest STT/backend contract only after capture is reproducible.

## Raspberry Audio Capture Validation Plan

Run these commands from a terminal on the Raspberry Pi after connecting the USB microphone. They are validation commands only; they do not add STT or change the `/chat` contract.

1. Confirm ALSA can see the capture device:

```bash
arecord -l
```

Expected result: at least one capture card appears. Record the card number, device number, and human-readable device name in the validation notes below.

2. Record a short mono WAV sample using the default capture device:

```bash
arecord -f S16_LE -r 16000 -c 1 -d 5 ~/tonto-mic-check.wav
```

If the default device is not the USB microphone, use the card and device from `arecord -l`:

```bash
arecord -D plughw:<CARD>,<DEVICE> -f S16_LE -r 16000 -c 1 -d 5 ~/tonto-mic-check.wav
```

3. Replay the sample locally:

```bash
aplay ~/tonto-mic-check.wav
```

4. Optional quick file check:

```bash
ls -lh ~/tonto-mic-check.wav
```

Validation evidence to capture:

```text
Date:
Raspberry hostname:
Microphone/card from arecord -l:
Record command used:
Playback command used:
Sample duration:
Result:
Audio quality notes:
Blockers:
```

Decision rule: do not add an audio upload endpoint, STT provider integration, or new audio dependency until a short WAV can be recorded and replayed on the Raspberry Pi.

## Guardrails

- Keep Raspberry as a thin client: capture audio, call backend, play TTS.
- Treat backend STT as the provisional default because it keeps the MVP simple and the Raspberry client thin.
- Do not describe backend STT as caused by proven Raspberry limitations unless a concrete test shows that.
- Keep manual text input available as a fallback while voice is being built.
- Do not introduce wake word, local audio models, persistence, auth, Arduino, or advanced memory in Week 03 kickoff.
