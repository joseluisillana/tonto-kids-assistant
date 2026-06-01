# Audio Pipeline Phase 2A Validation Guide

This guide validates Phase 2A of `specs/audio-pipeline.md`: backend STT with OpenAI `gpt-4o-mini-transcribe`, real upload from Raspberry Pi, real transcript, conversational response, and local playback with `espeak`.

The guide is intentionally command-oriented so another human or agent can execute it and collect evidence. Do not print, paste, or commit the value of `OPENAI_API_KEY`.

## Objective and Scope

Validate that the implemented backend STT path works on real hardware:

```text
Raspberry WAV -> POST /chat/audio -> OpenAI STT backend -> transcript -> response -> espeak local
```

In scope:

- Local backend checks on Windows.
- Raspberry Pi microphone capture using `arecord`.
- Manual upload to `POST /chat/audio` using `curl`.
- Evidence collection for transcript, response, latency, and TTS playback.
- Final documentation update based on the evidence.

Out of scope:

- Automating Raspberry capture/upload in `client/`.
- Wake word.
- STT local on Raspberry.
- Vosk, `whisper.cpp`, or other offline STT integration.
- Persisting audio or transcripts beyond the existing in-memory session history.

## Preconditions

- Current branch is `feature/audio-upload-contract` or another project feature branch for Phase 2A validation.
- Backend dependencies are installed in the repo-local `.venv/`.
- `OPENAI_API_KEY` is configured in the backend terminal environment.
- Raspberry Pi can reach the Windows backend over the LAN.
- Raspberry Pi has `curl`, `arecord`, `aplay`, `espeak`, and `python3`.
- USB microphone is connected to Raspberry Pi.

## Evidence to Collect

Create a local evidence note while executing the guide. Include:

- Date/time and operator.
- Git branch and status.
- Python test result.
- Backend model settings, without API key value.
- Windows PC LAN IP used by Raspberry.
- Raspberry hostname, user, and tooling output.
- `arecord -l` microphone card/device.
- WAV file metadata and playback result.
- `/chat/audio` HTTP status and total time.
- JSON response with `session_id`, `transcript`, and `response`.
- Whether transcript is real and close enough to the spoken phrase.
- Whether `espeak` playback was audible.
- Any ALSA/JACK warnings and whether they block the demo.
- Negative test result.

## 1. Windows Git Preflight

Run from the repository root on Windows:

```powershell
git branch --show-current
git status --short --branch
```

Evidence to record:

- Branch name.
- Whether the branch is `feature/audio-upload-contract` or an equivalent project branch.
- Current modified/untracked files.

Acceptance:

- Do not run validation on `main` unless the user explicitly decided to work on `main`.
- If `main` has uncommitted changes, stop and ask before moving, stashing, committing, discarding, or editing.

## 2. Confirm Python Environment and Tests

Run from the repository root on Windows:

```powershell
.\scripts\setup-dev.ps1
.\scripts\test.ps1 -Target python
```

Evidence to record:

- Setup result.
- Python test summary.

Expected result:

```text
23 passed
```

The exact number may increase later. The acceptance criterion is that the Python test command finishes without failures.

## 3. Confirm STT Configuration Without Revealing Secrets

Run in the backend terminal on Windows:

```powershell
if (-not $env:OPENAI_API_KEY) { throw "OPENAI_API_KEY is not set" }
$env:OPENAI_STT_MODEL = "gpt-4o-mini-transcribe"
$env:OPENAI_MODEL = "gpt-4o-mini"
"OPENAI_API_KEY configured"
"OPENAI_STT_MODEL=$env:OPENAI_STT_MODEL"
"OPENAI_MODEL=$env:OPENAI_MODEL"
```

Evidence to record:

- `OPENAI_API_KEY configured`
- `OPENAI_STT_MODEL=gpt-4o-mini-transcribe`
- `OPENAI_MODEL=gpt-4o-mini`

Do not record the API key value.

## 4. Start Backend for LAN Access

Run from the repository root on Windows:

```powershell
.\scripts\dev.ps1 -Service backend -AllowLan
```

Keep this backend process running. In another Windows terminal, confirm local health:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Find the Windows LAN IP for Raspberry:

```powershell
Get-NetIPAddress -AddressFamily IPv4 |
  Where-Object { $_.IPAddress -notlike "127.*" -and $_.PrefixOrigin -ne "WellKnown" } |
  Select-Object InterfaceAlias,IPAddress
```

Evidence to record:

- Backend startup output.
- `/health` response.
- LAN IP selected for Raspberry, for example `192.168.1.91`.

Expected health response:

```json
{"status":"ok"}
```

## 5. Raspberry Preflight

Run on Raspberry:

```bash
hostname
whoami
pwd
which curl
which arecord
which aplay
which espeak
python3 --version
```

Evidence to record:

- Hostname, expected `tonto-pi` or equivalent.
- User, expected `tonto-pi-user` or equivalent.
- Tool paths.
- Python version.

Acceptance:

- All required tools are available before continuing.

## 6. Confirm Raspberry to Backend Connectivity

Run on Raspberry, replacing `<PC_LAN_IP>` with the Windows LAN IP:

```bash
export BACKEND_URL=http://<PC_LAN_IP>:8000
curl -sS "$BACKEND_URL/health"
```

Evidence to record:

- `BACKEND_URL` used.
- Health response from Raspberry.

Expected result:

```json
{"status":"ok"}
```

If this fails, check Windows firewall, `-AllowLan`, Wi-Fi/LAN connectivity, and the selected IP before continuing.

## 7. Detect Microphone and Select Device

Run on Raspberry:

```bash
arecord -l
arecord -L
```

Evidence to record:

- Capture device name, expected `USB PnP Sound Device`.
- Current `card` and `device` numbers.
- Any unexpected devices or missing microphone issue.

Acceptance:

- Use the current `card` and `device` from `arecord -l`.
- Do not reuse previously documented values such as `plughw:1,0` or `plughw:2,0` without confirming them.

## 8. Record Real STT Sample

Suggested spoken phrase:

```text
Hola TONTO, explicame que es una estrella.
```

Run on Raspberry, replacing `<CARD>,<DEVICE>` with the values from `arecord -l`:

```bash
arecord -D plughw:<CARD>,<DEVICE> -f S16_LE -r 16000 -c 1 -d 6 ~/tonto-stt-phase-2a.wav
ls -lh ~/tonto-stt-phase-2a.wav
file ~/tonto-stt-phase-2a.wav
aplay ~/tonto-stt-phase-2a.wav
```

Evidence to record:

- Recording command used.
- File size.
- `file` output.
- Whether local playback was audible and clear enough.

Expected WAV format:

```text
RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 16000 Hz
```

## 9. Upload Audio to `/chat/audio`

Run on Raspberry:

```bash
curl -sS -X POST "$BACKEND_URL/chat/audio" \
  -F "audio=@/home/tonto-pi-user/tonto-stt-phase-2a.wav;type=audio/wav" \
  -F "session_id=phase-2a-stt-validation" \
  -F "device_id=tonto-pi" \
  -F "duration_ms=6000" \
  -F "sample_rate_hz=16000" \
  -F "channels=1" \
  -F "language=es" \
  -o ~/tonto-stt-phase-2a-response.json \
  -w "HTTP_STATUS=%{http_code}\nTOTAL_TIME=%{time_total}\n"
python3 -m json.tool ~/tonto-stt-phase-2a-response.json
```

If the Raspberry username is not `tonto-pi-user`, adjust only the absolute file path in the `audio=@...` form field.

Evidence to record:

- `HTTP_STATUS`.
- `TOTAL_TIME`.
- Form fields used.
- Pretty-printed JSON response.

Expected result:

- `HTTP_STATUS=200`
- JSON includes:

```json
{
  "session_id": "phase-2a-stt-validation",
  "transcript": "<recognized Spanish text>",
  "response": "<speakable educational response>"
}
```

## 10. Validate Transcript and Response

Run on Raspberry:

```bash
python3 -c "import json; d=json.load(open('/home/tonto-pi-user/tonto-stt-phase-2a-response.json')); print('TRANSCRIPT=' + d.get('transcript','')); print('RESPONSE=' + d.get('response',''))"
```

Evidence to record:

- `TRANSCRIPT=...`
- `RESPONSE=...`
- Manual judgment of transcript quality.

Acceptance:

- `transcript` is not empty.
- `transcript` is not `[audio input captured]`.
- `transcript` reasonably matches the phrase: `Hola TONTO, explicame que es una estrella`.
- `response` is a child-friendly educational answer and can be spoken with TTS.

## 11. Play Response with Local TTS

Run on Raspberry:

```bash
python3 -c "import json, subprocess; d=json.load(open('/home/tonto-pi-user/tonto-stt-phase-2a-response.json')); subprocess.run(['espeak','-v','es',d.get('response','')], check=False)"
```

Evidence to record:

- Whether audio was audible.
- Whether pronunciation was understandable enough for demo.
- Any ALSA/JACK warnings.
- Whether warnings block playback or are only noisy shell output.

Acceptance:

- Response is audible and understandable enough for demo.
- ALSA/JACK warnings may be accepted only if playback works and the warnings are documented.

## 12. Run Negative Upload Check

Run on Raspberry:

```bash
printf "not audio" > ~/not-audio.txt
curl -sS -X POST "$BACKEND_URL/chat/audio" \
  -F "audio=@/home/tonto-pi-user/not-audio.txt;type=text/plain" \
  -F "session_id=phase-2a-negative" \
  -F "duration_ms=1000" \
  -F "sample_rate_hz=16000" \
  -F "channels=1" \
  -F "language=es" \
  -w "\nHTTP_STATUS=%{http_code}\n"
```

Evidence to record:

- Error response body.
- `HTTP_STATUS`.

Acceptance:

- Expected status is `400` or `415`, depending on whether the backend rejects the file as too small or invalid WAV.
- Any `200` response is a validation failure.

## Acceptance Criteria

Phase 2A validation passes only when all of these are true:

- Python tests pass with the STT client mocked.
- Backend starts in LAN mode with `OPENAI_API_KEY`, `OPENAI_MODEL`, and `OPENAI_STT_MODEL`.
- Raspberry reaches backend `/health`.
- Raspberry records a WAV file that is PCM 16-bit mono 16 kHz.
- `POST /chat/audio` returns `HTTP_STATUS=200`.
- Response JSON includes `session_id`, real `transcript`, and `response`.
- `transcript` is not placeholder text and is reasonably close to the spoken phrase.
- `response` is speakable and plays through `espeak`.
- Total request latency is recorded.
- ALSA/JACK warnings, if any, are recorded.
- Negative upload returns a non-`200` error.

If any criterion fails, do not mark Phase 2A as validated. Record the blocker and suggested follow-up instead.

## Final Documentation Update

After collecting evidence, update the repository documentation using the actual results.

Update `docs/project-journal/week-03.md` with a section named:

```markdown
## Fase 2A Validation Evidence
```

Include:

- Date/time.
- Branch and status.
- Python test result.
- Backend model settings, excluding API key.
- Windows LAN IP used.
- Raspberry host/user/tools.
- Microphone `card/device`.
- WAV metadata.
- `/chat/audio` `HTTP_STATUS` and `TOTAL_TIME`.
- Transcript.
- Response.
- TTS playback result.
- Negative test result.
- Final pass/fail conclusion.

Update `specs/audio-pipeline.md`:

- Mark real STT validation as completed only if all acceptance criteria passed.
- If validation failed, leave Phase 2A as implemented but not validated and document the blocker.

Update `docs/roadmap.md`:

- Mark `Pipeline de voz extremo a extremo` as complete only if Raspberry capture, backend STT, response, and TTS playback all passed.
- Otherwise mark it as partial and name the missing step.

Update `docs/specs.md` and `docs/architecture.md`:

- Reflect that STT was manually validated from Raspberry only if validation passed.
- Keep `/chat` as the stable text fallback.

Update `README.md`:

- Refresh the Semana 3 project status with the validation result.

Update `AGENTS.md`:

- State that backend STT with OpenAI `gpt-4o-mini-transcribe` is now active for Semana 3 if validation passed.
- Keep wake word, STT local, local audio models, persistence, auth, and advanced automation out of scope until a new explicit decision.
- Preserve the rule that Raspberry remains a thin client.

Run final local checks from Windows:

```powershell
.\scripts\test.ps1 -Target python
git diff --check
git status --short --branch
```

Evidence to record:

- Python test result after documentation updates.
- `git diff --check` result.
- Final Git status.

## Final Checklist

- [ ] Git preflight recorded.
- [ ] Python tests pass before manual validation.
- [ ] OpenAI STT config confirmed without exposing secrets.
- [ ] Backend started with `-AllowLan`.
- [ ] Windows LAN IP recorded.
- [ ] Raspberry tools confirmed.
- [ ] Raspberry reaches backend `/health`.
- [ ] Microphone device recorded from `arecord -l`.
- [ ] Real WAV sample recorded.
- [ ] WAV format verified.
- [ ] WAV playback verified locally.
- [ ] `/chat/audio` upload returns `HTTP 200`.
- [ ] `TOTAL_TIME` recorded.
- [ ] Transcript recorded and verified as real.
- [ ] Response recorded.
- [ ] Response played with `espeak`.
- [ ] ALSA/JACK warnings recorded if present.
- [ ] Negative upload returns `400` or `415`.
- [ ] `docs/project-journal/week-03.md` updated with evidence.
- [ ] `specs/audio-pipeline.md` updated with validation status.
- [ ] `docs/roadmap.md` updated.
- [ ] `docs/specs.md` updated.
- [ ] `docs/architecture.md` updated.
- [ ] `README.md` updated.
- [ ] `AGENTS.md` updated if validation changes persistent agent instructions.
- [ ] Final `.\scripts\test.ps1 -Target python` passes.
- [ ] Final `git diff --check` passes.
- [ ] Final `git status --short --branch` recorded.
