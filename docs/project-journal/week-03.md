# Week 03 Kickoff

**Date:** 2026-05-18
**Status:** Repository kickoff prepared; USB microphone capture validated on Raspberry Pi.

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

- [x] Connect USB microphone to Raspberry Pi.
- [x] Confirm microphone appears in `arecord -l`.
- [x] Record a short WAV sample.
- [x] Replay the WAV sample locally.
- [x] Note device name, command used, sample duration, and any audio quality issue.
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

## Raspberry USB Microphone Validation Evidence

**Date:** 2026-05-23, 09:00 local time.
**Raspberry hostname:** `tonto-pi`.
**Microphone:** Mini USB Microphone M-305, connected by USB.
**Detected device:** `card 2: Device [USB PnP Sound Device], device 0: USB Audio [USB Audio]`.
**ALSA capture aliases:** `hw:CARD=Device,DEV=0`, `plughw:CARD=Device,DEV=0`, `default:CARD=Device`, `sysdefault:CARD=Device`, `front:CARD=Device,DEV=0`, and `dsnoop:CARD=Device,DEV=0`.

Command used to list capture hardware:

```bash
arecord -l
```

Output:

```text
**** List of CAPTURE Hardware Devices ****
card 2: Device [USB PnP Sound Device], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

Additional ALSA device listing:

```bash
arecord -L
```

Output:

```text
null
    Discard all samples (playback) or generate zero samples (capture)
hw:CARD=Device,DEV=0
    USB PnP Sound Device, USB Audio
    Direct hardware device without any conversions
plughw:CARD=Device,DEV=0
    USB PnP Sound Device, USB Audio
    Hardware device with all software conversions
default:CARD=Device
    USB PnP Sound Device, USB Audio
    Default Audio Device
sysdefault:CARD=Device
    USB PnP Sound Device, USB Audio
    Default Audio Device
front:CARD=Device,DEV=0
    USB PnP Sound Device, USB Audio
    Front output / input
dsnoop:CARD=Device,DEV=0
    USB PnP Sound Device, USB Audio
    Direct sample snooping device
```

Recording command used:

```bash
arecord -D plughw:2,0 -f S16_LE -r 16000 -c 1 -d 10 ~/tonto-mic-check.wav
```

Recording output:

```text
Recording WAVE '/home/tonto-pi-user/tonto-mic-check.wav' : Signed 16 bit Little Endian, Rate 16000 Hz, Mono
```

Playback command used:

```bash
aplay ~/tonto-mic-check.wav
```

Playback output:

```text
Playing WAVE '/home/tonto-pi-user/tonto-mic-check.wav' : Signed 16 bit Little Endian, Rate 16000 Hz, Mono
```

File size check:

```bash
ls -lh ~/tonto-mic-check.wav
```

Output:

```text
-rw-r--r-- 1 tonto-pi-user tonto-pi-user 157K May 23 08:59 /home/tonto-pi-user/tonto-mic-check.wav
```

**Sample duration:** 10 seconds.
**Recorded file size:** 157K.
**Result:** capture and local playback worked correctly on Raspberry Pi.
**Audio quality notes:** recording gain was raised to maximum with `alsamixer` before the successful capture. Playback was audible and correct according to the manual validation.
**Blockers:** no capture blocker found.
**AI tools used:** Codex reviewed `AGENTS.md`, `docs/ai-assisted-workflow.md`, `docs/project-journal/week-03.md`, `specs/audio-pipeline.md`, `docs/specs.md`, and `docs/hardware.md`, then recorded the human-provided Raspberry validation evidence.
**Human decision:** capture validation is recorded only; no STT, wake word, audio endpoint, new dependency, or architecture change is introduced in this iteration.
**Validation:** USB microphone capture is reproducible enough to unblock the next design step. The next iteration may decide the minimum audio upload contract to the backend while keeping `POST /chat` stable until that decision is explicit.

## Guardrails

- Keep Raspberry as a thin client: capture audio, call backend, play TTS.
- Treat backend STT as the provisional default because it keeps the MVP simple and the Raspberry client thin.
- Do not describe backend STT as caused by proven Raspberry limitations unless a concrete test shows that.
- Keep manual text input available as a fallback while voice is being built.
- Do not introduce wake word, local audio models, persistence, auth, Arduino, or advanced memory in Week 03 kickoff.

## Next Iteration: Audio Upload Contract Candidate

After `v0.2.4-week3-microphone-validation`, the next design step documented `POST /chat/audio` as the minimum candidate contract for uploading one short WAV turn from Raspberry to the backend. The full candidate contract lives in `specs/audio-pipeline.md`.

## Audio Upload Contract Implementation

**Branch:** `feature/audio-upload-contract`.
**Commit:** `71ad57c docs: define audio upload contract` → implementado en esta iteración.

The audio upload contract was implemented in `backend/` without adding STT, wake word, or changing the `/chat` contract.

### Changes

| File | Type | Purpose |
|---|---|---|
| `backend/requirements.txt` | Modified | Added `python-multipart` (required by FastAPI for multipart form data) |
| `backend/state.py` | New | Shared app state: `session_history` and `MAX_HISTORY_MESSAGES` |
| `backend/openai_client.py` | New | Extracted OpenAI orchestration (`call_openai`, `build_openai_input`, `extract_response_text`) |
| `backend/main.py` | Refactored | Uses `state.py` and `openai_client.py`; includes `audio_router` |
| `backend/audio_router.py` | New | `POST /chat/audio` with WAV validation, fixed STT placeholder, and conversation flow |
| `tests/conftest.py` | New | TestClient fixture mocking OpenAI calls |
| `tests/test_audio.py` | New | 11 tests: valid upload, missing fields, empty file, size limit, format validation, duration bounds |
| `specs/audio-pipeline.md` | Updated | Marked endpoint as implemented, STT as pending placeholder |
| `docs/specs.md` | Updated | Reflects endpoint implementation status |
| `scripts/test.ps1` | Fixed | Syntax check heredoc quoting (pre-existing bug) |

### How it works

```text
Raspberry WAV → POST /chat/audio (multipart/form-data) → validate WAV → 
transcript fijo "[audio input captured]" → call_openai() → 
response educativa → {session_id, transcript, response}
```

STT is a placeholder. When a real STT provider is chosen, replacing the fixed transcript is a single-line change.

### What was NOT done

- No STT provider chosen or integrated.
- No changes to `POST /chat` contract.
- No changes to Raspberry client (`client/`).
- No wake word, persistence, auth, Arduino, or architecture changes.
- No new dependencies beyond `python-multipart`.

### Guardrails

- `/chat` remains stable.
- Raspberry remains a thin client.
- The endpoint validates WAV format, size, and duration before calling OpenAI.
- Errors follow the spec: 400, 413, 415, 422, 502, 504.

### Gap: client not updated

The Raspberry client (`client/main.py`) has **not** been modified. WAV capture remains a manual `arecord` command via SSH. There is no automated capture-and-upload loop in the client code.

### Manual test: audio upload to backend (pending)

Test the endpoint from the Raspberry using `curl`:

```bash
# On the Raspberry Pi, after recording a sample:
curl -s -X POST http://<TONTO_BACKEND_IP>:8000/chat/audio \
  -F "audio=@/home/tonto-pi-user/tonto-turn.wav" \
  -F "session_id=demo-session" \
  -F "duration_ms=5000" \
  -F "sample_rate_hz=16000" \
  -F "channels=1" | python -m json.tool
```

Expected result:
```json
{
  "session_id": "demo-session",
  "transcript": "[audio input captured]",
  "response": "..."
}
```

This test is **not executed** — it documents the command for the next iteration when the client is updated and the test can be run from real hardware.

## OpenCode Tooling Decision

**Date:** 2026-05-26.
**Tool:** OpenCode CLI (WSL2 en Windows).
**Provider:** DevExpert (OpenAI-compatible).
**Models:** `deepseek-v4-flash` (default) y `deepseek-v4-pro`.

OpenCode se añade al stack de desarrollo como asistente principal para
implementación, revisión y verificación, siguiendo las instrucciones de
`AGENTS.md` y los workflows del repositorio.
