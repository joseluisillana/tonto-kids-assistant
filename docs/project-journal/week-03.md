# Week 03 Kickoff

**Date:** 2026-05-18
**Status:** Repository kickoff prepared; USB microphone capture validated on Raspberry Pi; Phase 2A backend STT validation passed with real Raspberry audio.

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
- The endpoint validates WAV format, size, and duration before returning the temporary audio fallback or, later, calling STT/OpenAI with real text.
- Errors follow the spec: 400, 413, 415, 422, 502, 504.

### Gap: client not updated

The Raspberry client (`client/main.py`) has **not** been modified. WAV capture remains a manual `arecord` command via SSH. There is no automated capture-and-upload loop in the client code.

### Manual test: audio upload to backend (validated)

**Date:** 2026-05-27.
**Branch:** `feature/audio-upload-contract`.
**Backend host:** Windows PC on LAN IP `192.168.1.91`, started with `.\scripts\dev.ps1 -Service backend -AllowLan`.
**Raspberry host:** `tonto-pi`, user `tonto-pi-user`.
**Status:** manual upload contract validated from real Raspberry hardware. A temporary Spanish fallback now prevents the placeholder transcript from producing random English responses.

Pre-flight evidence:

```text
git branch --show-current -> feature/audio-upload-contract
git status --short --branch -> ## feature/audio-upload-contract...origin/feature/audio-upload-contract
.\scripts\setup-dev.ps1 -> Development environment is ready.
.\scripts\test.ps1 -Target python -> 12 passed in 0.09s
OPENAI_API_KEY -> configured in shell, not documented
OPENAI_MODEL -> gpt-4o-mini
PC LAN IPv4 -> 192.168.1.91
Backend health from PC -> {"status":"ok"}
Backend health from Raspberry -> {"status":"ok"}
```

Raspberry tooling evidence:

```text
hostname -> tonto-pi
whoami -> tonto-pi-user
pwd -> /home/tonto-pi-user
which curl -> /usr/bin/curl
which arecord -> /usr/bin/arecord
which aplay -> /usr/bin/aplay
which espeak -> /usr/bin/espeak
python3 --version -> Python 3.13.5
```

Audio capture evidence:

```text
arecord -l
**** List of CAPTURE Hardware Devices ****
card 1: Device [USB PnP Sound Device], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

Recording command used in this run:

```bash
arecord -D plughw:1,0 -f S16_LE -r 16000 -c 1 -d 4 ~/tonto-turn.wav
```

Recording output and file inspection:

```text
Recording WAVE '/home/tonto-pi-user/tonto-turn.wav' : Signed 16 bit Little Endian, Rate 16000 Hz, Mono
-rw-r--r-- 1 tonto-pi-user tonto-pi-user 126K May 27 21:08 /home/tonto-pi-user/tonto-turn.wav
/home/tonto-pi-user/tonto-turn.wav: RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 16000 Hz
aplay ~/tonto-turn.wav -> Playing WAVE ... Signed 16 bit Little Endian, Rate 16000 Hz, Mono
```

Manual upload command used:

```bash
BACKEND_URL=http://192.168.1.91:8000

curl -sS -X POST "$BACKEND_URL/chat/audio" \
  -F "audio=@/home/tonto-pi-user/tonto-turn.wav;type=audio/wav" \
  -F "session_id=demo-session" \
  -F "device_id=tonto-pi" \
  -F "duration_ms=4000" \
  -F "sample_rate_hz=16000" \
  -F "channels=1" \
  -F "language=es" \
  -w "\nHTTP_STATUS=%{http_code}\nTOTAL_TIME=%{time_total}\n"
```

Result:

```text
{"session_id":"demo-session","transcript":"[audio input captured]","response":"He recibido tu audio. Todavia no puedo entenderlo, pero la subida y reproduccion ya funcionan. Pronto podre responder a lo que digas."}
HTTP_STATUS=200
TOTAL_TIME=2.584502
```

A second JSON-file upload also passed:

```text
HTTP_STATUS=200
TOTAL_TIME=1.472030
session_id=demo-session-json
transcript=[audio input captured]
response=He recibido tu audio. Todavia no puedo entenderlo, pero la subida y reproduccion ya funcionan. Pronto podre responder a lo que digas.
```

Negative validation:

```text
text file upload -> {"detail":"File too small to be a valid WAV"} HTTP_STATUS=400
11 second WAV upload -> {"detail":"Audio too long (11000 ms), maximum is 10000 ms"} HTTP_STATUS=400
```

Evidence mapping:

| Validation step | Evidence | Result |
|---|---|---|
| Repo and branch gate | branch/status clean on `feature/audio-upload-contract` | Pass |
| Local setup | `.\scripts\setup-dev.ps1` completed | Pass |
| Automated backend tests | `12 passed in 0.09s` | Pass |
| Backend LAN startup | Uvicorn on `0.0.0.0:8000` | Pass |
| Backend health from PC | `{"status":"ok"}` | Pass |
| Backend health from Raspberry | `{"status":"ok"}` | Pass |
| Raspberry tools | `curl`, `arecord`, `aplay`, `espeak`, `python3` present | Pass |
| Microphone detection | USB PnP Sound Device at `card 1`, `device 0` | Pass |
| WAV capture | 4s, 126K, PCM 16-bit mono 16 kHz | Pass |
| Local WAV playback | `aplay` accepted WAV | Pass; audibility not separately recorded |
| Manual upload | `POST /chat/audio` uploaded `/home/tonto-pi-user/tonto-turn.wav` and returned `HTTP_STATUS=200` | Pass |
| Response contract | `session_id`, `transcript`, `response` present | Pass |
| Latency observation | `2.584502s` and `1.472030s` | Recorded |
| Invalid short text upload | `HTTP_STATUS=400` | Pass as too small/malformed input |
| Too-long WAV upload | `HTTP_STATUS=400` with audio-too-long detail | Pass |
| Speak response locally | `espeak -v es` spoke the JSON response audibly; shell emitted ALSA/JACK warnings | Pass with noisy shell output |

Remaining observations:

| ID | Observation | Evidence | Impact | Suggested follow-up |
|---|---|---|---|---|
| O1 | TTS playback emits noisy ALSA/JACK warnings despite audible output | The JSON response was spoken clearly, but the shell printed unavailable PCM and missing JACK server messages | Voice-output works, but demo logs are noisy and could confuse debugging | Confirm default playback device with `aplay -l`, then configure ALSA/default device or suppress non-actionable stderr for demo scripts |
| O2 | ALSA capture card number changed from previous evidence | Previous docs used `card 2`; current run detected `card 1` | Hard-coded `plughw:2,0` examples may fail across boots/devices | Use the `card` and `device` from `arecord -l`; future client automation should accept an explicit `TONTO_AUDIO_DEVICE` setting |

Conclusion: the manual Raspberry-to-backend upload validates the `POST /chat/audio` multipart contract with real hardware. The returned response was also spoken locally with `espeak`, despite noisy ALSA/JACK shell output. The next implementation phase should not be considered full voice UX yet: STT is still placeholder, Raspberry client automation is pending, and audio logs should be cleaned up for demo clarity.

## OpenCode Tooling Decision

**Date:** 2026-05-26.
**Tool:** OpenCode CLI (WSL2 en Windows).
**Provider:** DevExpert (OpenAI-compatible).
**Base URL:** `https://inference.devexpert.io/v1`.
**Models:** `deepseek-v4-flash` (recommended) y `deepseek-v4-pro` (alternative).
**Access note:** acceso activo durante 60 dias con limite semanal para evitar consumos accidentales.

OpenCode se añade al stack de desarrollo como una herramienta mas para
implementacion, revision y verificacion. Codex conserva el rol de asistente
principal del proyecto. OpenCode sigue las instrucciones de `AGENTS.md` y los
workflows del repositorio, igual que cualquier herramienta AI-assisted que se
incorpore en el futuro.

## Fase 2A: STT Provider Selection and Backend Integration

**Branch:** `feature/audio-upload-contract`.
**Status:** backend STT integration implemented and manually validated with real Raspberry audio.

OpenAI `gpt-4o-mini-transcribe` was selected as the initial STT provider for the Week 03 voice pipeline. The decision prioritizes demo stability, low implementation risk, and reuse of the existing `OPENAI_API_KEY`. The backend now supports `OPENAI_STT_MODEL` for changing the transcription model while keeping `OPENAI_MODEL` dedicated to response generation.

Offline options remain documented but unimplemented:

- Vosk Spanish: zero API cost and small model footprint, but needs real-sample accuracy validation.
- `whisper.cpp`: offline Whisper-style transcription with CPU-only support, but needs setup and latency validation on the Windows backend host.

The `POST /chat/audio` endpoint now validates the WAV, transcribes it in the backend, sends the real transcript through the existing conversation flow, and returns `{session_id, transcript, response}`. It returns `422` for valid audio with empty transcription, `502` for STT provider failures, and `504` for STT timeouts.

Remaining Week 03 work: automate capture and upload in the Raspberry client as Phase 2B, then implement Phase 3 web audio validation.

## Fase 2A Validation Evidence

**Date/time:** 2026-05-30, Europe/Madrid.
**Operator:** Jose Luis Illana Ruiz.
**Branch:** `feature/audio-upload-contract`.
**Initial Git status:** `## feature/audio-upload-contract...origin/feature/audio-upload-contract`; no modified or untracked files before the temporary evidence log was created.
**Conclusion:** pass. Phase 2A was validated with real Raspberry capture, backend STT through OpenAI `gpt-4o-mini-transcribe`, conversational response generation, and local playback with `espeak`.

Pre-flight and setup:

```text
.\scripts\setup-dev.ps1 -> Development environment is ready.
.\scripts\test.ps1 -Target python -> 23 passed in 0.21s
OPENAI_API_KEY -> configured in shell, not documented
OPENAI_STT_MODEL -> gpt-4o-mini-transcribe
OPENAI_MODEL -> gpt-4o-mini
Backend -> .\scripts\dev.ps1 -Service backend -AllowLan
Backend health from Windows -> status ok
Windows LAN IP used by Raspberry -> 192.168.1.91
Backend health from Raspberry -> {"status":"ok"}
```

Raspberry evidence:

```text
hostname -> tonto-pi
whoami -> tonto-pi-user
pwd -> /home/tonto-pi-user/tonto-kids-assistant
curl -> /usr/bin/curl
arecord -> /usr/bin/arecord
aplay -> /usr/bin/aplay
espeak -> /usr/bin/espeak
python3 --version -> Python 3.13.5
```

Microphone and WAV evidence:

```text
arecord -l -> card 1: Device [USB PnP Sound Device], device 0: USB Audio [USB Audio]
Selected device -> plughw:1,0
Recording command -> arecord -D plughw:1,0 -f S16_LE -r 16000 -c 1 -d 6 ~/tonto-stt-phase-2a.wav
File size -> 188K
WAV metadata -> RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 16000 Hz
aplay result -> audible and sufficiently clear
```

`POST /chat/audio` evidence:

```text
session_id -> phase-2a-stt-validation
device_id -> tonto-pi
duration_ms -> 6000
sample_rate_hz -> 16000
channels -> 1
language -> es
HTTP_STATUS -> 200
TOTAL_TIME -> 5.395580
transcript -> Hola tonto, explícame qué es una estrella.
response -> ¡Hola! Una estrella es una gran esfera de gas caliente en el espacio, principalmente compuesta de hidrógeno y helio. Produce luz y calor a través de reacciones nucleares en su interior. El Sol es una estrella que está muy cerca de nosotros y nos brinda luz y calor. ¡Esas luces que ves en el cielo de noche también son estrellas!
```

Manual quality judgment:

- Transcript is real, not `[audio input captured]`, and reasonably matches `Hola TONTO, explicame que es una estrella`.
- Response is educational, child-appropriate, and speakable by TTS.
- `espeak -v es` playback was audible, but in this run it sounded robotic and was not easy to understand; still usable for the demo.
- ALSA/JACK warnings appeared during `espeak` playback, including unavailable PCM entries and missing JACK server messages. They were noisy shell output only and did not block playback.

Negative validation:

```text
text file upload -> {"detail":"File too small to be a valid WAV"}
HTTP_STATUS -> 400
```

Remaining observations:

| ID | Observation | Impact | Suggested follow-up |
|---|---|---|---|
| O1 | `espeak` playback still emits noisy ALSA/JACK warnings while audio works | Demo output can confuse debugging | Confirm default playback device and clean or suppress non-actionable audio stderr in client/demo scripts |
| O2 | ALSA capture card changed across runs (`card 2` in earlier evidence, `card 1` in this validation) | Hard-coded `plughw` values can fail | Always read `arecord -l`; future client automation should accept explicit audio device configuration |
| O3 | Client capture/upload is still manual | Phase 2A validates backend STT but not an interactive client voice loop | Next step is Raspberry client automation for capture, upload, response playback, and timeout handling; Phase 3 web audio validation follows after that |

## Fase 2B: Raspberry Client Automation

**Status:** validated on real Raspberry hardware. The `--mode voice` loop is now closed end to end for the MVP voice turn.

### Changes

| File | Type | Purpose |
|---|---|---|
| `client/main.py` | Rewritten | `--mode text` preserves original chat; `--mode voice` adds interactive capture/upload/speak loop |
| `tests/test_client.py` | New | 21 unit tests covering text mode, multipart audio upload, capture, and TTS without hardware |

### How it works

```text
Enter -> arecord WAV -> POST /chat/audio (multipart) -> transcript + response -> espeak local
```

In voice mode, pressing Enter starts a recording with `arecord`, uploads the WAV via `urllib.request` multipart to `POST /chat/audio`, displays the transcript and response, then speaks the response with `espeak`. Non-empty text input falls back to `POST /chat` for typing.

### Configuration

| Variable | Default | Notes |
|---|---|---|
| `TONTO_BACKEND_URL` | (required) | Backend address |
| `TONTO_AUDIO_DEVICE` | (none) | Optional ALSA device, e.g. `plughw:1,0` |
| `TONTO_RECORD_SECONDS` | `6` | Clamped to 1..10 |
| `TONTO_AUDIO_PATH` | `/tmp/tonto-turn.wav` | WAV file path |
| `TONTO_DEVICE_ID` | `tonto-pi` | Client identifier |
| `TONTO_TTS_COMMAND` | `espeak` | TTS binary |

### Error handling

All specified error paths are handled without breaking the loop: backend unreachable, timeout, arecord missing, capture failure, empty WAV, HTTP 400/413/415/422/502/504, invalid JSON, espeak missing, espeak non-zero exit.

### Tests

21 unit tests pass without real hardware:

- Text mode preserves POST /chat contract
- Multipart contains audio file and all required fields
- Valid /chat/audio response extracts transcript and response
- HTTP errors and invalid JSON reported without breaking loop
- Capture calls arecord with and without TONTO_AUDIO_DEVICE
- Failed arecord or empty WAV does not attempt upload
- TTS handles FileNotFoundError and non-zero exit codes

### Remaining

Manual validation on Raspberry hardware is needed:

```bash
arecord -l
export TONTO_BACKEND_URL=http://<PC_LAN_IP>:8000
export TONTO_AUDIO_DEVICE=plughw:<CARD>,<DEVICE>
.venv/bin/python client/main.py --mode voice
```

Acceptance criteria:
- Enter starts capture
- WAV is uploaded to /chat/audio
- HTTP 200 with transcript and response
- espeak plays the response
- exit or quit closes cleanly
- --mode text still works

## Fase 2B Validation Evidence

Tracking plan: `specs/audio-pipeline-phase-2b-validation-guide.md`.

**Date/time:** 2026-05-30, Europe/Madrid.
**Operator:** Jose Luis Illana Ruiz.
**Branch:** `feature/audio-upload-contract`.
**Initial Git status:** `## feature/audio-upload-contract...origin/feature/audio-upload-contract`; only the validation guide itself was untracked before documentation updates.
**Conclusion:** pass. Phase 2B was validated on real Raspberry hardware with `client/main.py --mode voice`, `arecord`, backend upload to `POST /chat/audio`, transcript, speakable response, `espeak`, text fallback, and clean exit.

Pre-flight and setup:

```text
.\scripts\setup-dev.ps1 -> Development environment is ready.
.\scripts\test.ps1 -Target python -> 44 passed in 0.24s
OPENAI_API_KEY -> configured in shell, not documented
OPENAI_STT_MODEL -> gpt-4o-mini-transcribe
OPENAI_MODEL -> gpt-4o-mini
Backend -> .\scripts\dev.ps1 -Service backend -AllowLan
Backend startup -> 0.0.0.0:8000 with LAN mode enabled
Backend health from Windows -> status ok
Windows LAN IP used by Raspberry -> 192.168.1.91
Backend health from Raspberry -> {"status":"ok"}
```

Raspberry evidence:

```text
hostname -> tonto-pi
whoami -> tonto-pi-user
pwd -> /home/tonto-pi-user/tonto-kids-assistant
curl -> /usr/bin/curl
arecord -> /usr/bin/arecord
aplay -> /usr/bin/aplay
espeak -> /usr/bin/espeak
python3 --version -> Python 3.13.5
git branch --show-current -> feature/audio-upload-contract
git status --short --branch -> ## feature/audio-upload-contract...origin/feature/audio-upload-contract
```

Microphone and WAV evidence:

```text
arecord -l -> card 1: Device [USB PnP Sound Device], device 0: USB Audio [USB Audio]
Selected device -> plughw:1,0
Recording command -> arecord -D plughw:1,0 -f S16_LE -r 16000 -c 1 -d 6 /tmp/tonto-turn-phase-2b.wav
File size -> 188K
WAV metadata -> RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 16000 Hz
```

Voice-mode evidence:

```text
TONTO_BACKEND_URL=http://192.168.1.91:8000
TONTO_AUDIO_DEVICE=plughw:1,0
TONTO_RECORD_SECONDS=6
TONTO_AUDIO_PATH=/tmp/tonto-turn-phase-2b.wav
TONTO_DEVICE_ID=tonto-pi

TONTO Kids Assistant Client
Session: local-session-b5bda2ca-31b5-4c8b-a0b7-bfae899e88af
Voice mode: press Enter to capture audio, or type a message.
Type 'exit' or 'quit' to stop.
```

Recorded turn evidence:

```text
Recording...
Uploading...
Transcript: Hola tonto, explícame qué es una estrella.
TONTO: ¡Hola! Una estrella es un gran cuerpo celeste que brilla en el cielo. Está hecho de gas caliente, principalmente hidrógeno y helio. Las estrellas producen luz y calor a través de reacciones nucleares en su interior. Nuestro Sol es una estrella, y hay millones de otras en el universo. ¡Son fascinantes!
```

TTS and warnings:

```text
espeak playback was audible.
ALSA/JACK warnings appeared in the shell but did not block playback.
```

Typed-message fallback:

```text
> Explicame que es la Luna en una frase.
TONTO: La Luna es el satélite natural de la Tierra, que brilla en el cielo nocturno y orbita a nuestro planeta.
```

Clean exit:

```text
exit -> client returned to shell without traceback
```

Validation notes:

- The transcript was real and close enough to the spoken phrase for the demo.
- The response was child-friendly and speakable.
- The WAV file existed, was non-empty, and matched the expected mono 16 kHz PCM format.
- ALSA/JACK warnings were noisy but non-blocking because `espeak` remained audible.
- The typed fallback stayed on the stable `/chat` path and did not trigger capture.
- `exit` and `quit` both close the loop cleanly.

## Fase 3: Web Audio Loop Planning

**Date:** 2026-05-30.
**Branch:** `feature/audio-upload-contract`.
**Status:** planned in documentation only; no web or backend implementation in this iteration. Sequencing corrected: this phase follows the pending Raspberry client automation from Phase 2B.

Phase 3 is added to Week 03 as a browser-driven validation loop:

```text
web microphone or WAV selection -> compatible WAV -> POST /chat/audio -> transcript -> response -> web evidence
```

The purpose is to validate the real STT backend from the web client after the Raspberry automation step is addressed. This keeps the text path stable, reuses the existing backend contract, and creates a faster demo/debug surface for transcript, response, latency and error evidence.

Key implementation guardrails recorded for the next agent:

- Reuse `POST /chat/audio`; do not add a web-only audio endpoint.
- Send WAV compatible with the current backend contract: PCM 16-bit, 16 kHz, mono.
- Do not upload browser `webm`/`ogg` directly unless a later decision adds backend transcoding.
- Prefer native browser APIs and no new dependency.
- Browser TTS, persistence, streaming, local STT and advanced product UI remain out of scope.
- Preserve `/chat` as the stable text fallback.

Documentation updated for this plan:

- `specs/audio-pipeline-phase-3-web-loop.md`
- `specs/audio-pipeline.md`
- `specs/web-validation-client.md`
- `docs/roadmap.md`
- `docs/specs.md`
- `docs/architecture.md`
- `docs/decisions.md`
- `README.md`
- `AGENTS.md`
