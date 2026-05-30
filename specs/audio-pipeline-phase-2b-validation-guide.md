# Audio Pipeline Phase 2B Validation Guide

This guide validates Phase 2B of `specs/audio-pipeline.md`: the automated Raspberry Pi voice client loop using `client/main.py --mode voice`.

After the TTS tuning commit `fix: tune raspberry espeak demo speech`, the final Phase 2B gate was the post-adjustment revalidation in `specs/audio-pipeline-phase-2b-tts-revalidation.md`. That revalidation passed on real Raspberry hardware on 2026-05-30, so Phase 3 is unblocked within its documented scope.

The guide is intentionally command-oriented so another human or agent can execute it and collect evidence. Do not print, paste, or commit the value of `OPENAI_API_KEY`.

## Objective and Scope

Validate that the implemented Raspberry client can automate the voice turn that was validated manually in Phase 2A:

```text
Enter in client -> arecord WAV -> POST /chat/audio -> transcript + response -> espeak -v es -s 135 -g 8
```

In scope:

- Local backend checks on Windows.
- Raspberry Pi connectivity to the backend over LAN.
- Raspberry Pi microphone capture through the client using `arecord`.
- Automated upload to `POST /chat/audio` from `client/main.py --mode voice`.
- Transcript, response, and local `espeak -v es -s 135 -g 8` playback from the client loop.
- TTS intelligibility after the slower speed and word-gap tuning.
- Typed-message fallback inside `--mode voice`, which should still use `/chat`.
- Evidence collection for transcript, response, latency notes, TTS playback, and failures.
- Final documentation update based on the evidence.

Out of scope:

- Changing the backend audio contract.
- Changing `client/main.py` behavior during validation.
- Adding Python dependencies.
- Wake word.
- STT local on Raspberry.
- Vosk, `whisper.cpp`, or other offline STT integration.
- Persisting audio or transcripts beyond the existing in-memory session history.

## Preconditions

- Current branch is `feature/audio-upload-contract` or another project branch for Phase 2B validation.
- Backend dependencies are installed in the repo-local `.venv/`.
- `OPENAI_API_KEY` is configured in the backend terminal environment.
- Raspberry Pi can reach the Windows backend over the LAN.
- Raspberry Pi has `curl`, `arecord`, `aplay`, `espeak`, and `python3`.
- USB microphone is connected to Raspberry Pi.
- The repository on Raspberry contains the Phase 2B client implementation.
- The repository on Raspberry contains the TTS tuning commit `fix: tune raspberry espeak demo speech` or a later commit with equivalent default `TONTO_TTS_ARGS`.
- The Raspberry client virtual environment exists and can run `.venv/bin/python client/main.py`.

## Evidence to Collect

Create a local evidence note while executing the guide. Include:

- Date/time and operator.
- Git branch and status on Windows.
- Python test result on Windows.
- Backend model settings, without API key value.
- Windows PC LAN IP used by Raspberry.
- Raspberry hostname, user, repo path, and tooling output.
- `arecord -l` microphone card/device.
- Chosen `TONTO_AUDIO_DEVICE`.
- Client environment values used: `TONTO_BACKEND_URL`, `TONTO_RECORD_SECONDS`, `TONTO_AUDIO_PATH`, `TONTO_DEVICE_ID`, and `TONTO_TTS_ARGS`.
- WAV file metadata after the client records a turn.
- Client output for `Transcript:` and `TONTO:`.
- Whether the transcript is real and close enough to the spoken phrase.
- Whether the response is child-friendly and speakable.
- Whether `espeak -v es -s 135 -g 8` playback was audible.
- Whether a long response sounded slower, understandable, and not word-smeared.
- Any ALSA/JACK warnings and whether they block the demo.
- Typed-message fallback result inside `--mode voice`.
- Clean exit result using `exit` or `quit`.
- Any failure mode observed and suggested follow-up.

## 1. Windows Git Preflight

Run from the repository root on Windows:

```powershell
git branch --show-current
git status --short --branch
git log -1 --oneline
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

- The Python test command finishes without failures.
- The exact test count may increase later.

## 3. Confirm Backend Configuration Without Revealing Secrets

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
git branch --show-current
git status --short --branch
```

Evidence to record:

- Hostname, expected `tonto-pi` or equivalent.
- User, expected `tonto-pi-user` or equivalent.
- Repo path, expected `/home/tonto-pi-user/tonto-kids-assistant` or equivalent.
- Tool paths.
- Python version.
- Raspberry repo branch and status.
- Latest commit, confirming the TTS tuning commit is present.

Acceptance:

- All required tools are available before continuing.
- Raspberry repo contains the Phase 2B client implementation.
- Do not install Python packages globally.

## 6. Confirm Raspberry to Backend Connectivity

Run on Raspberry, replacing `<PC_LAN_IP>` with the Windows LAN IP:

```bash
export TONTO_BACKEND_URL=http://<PC_LAN_IP>:8000
curl -sS "$TONTO_BACKEND_URL/health"
```

Evidence to record:

- `TONTO_BACKEND_URL` used.
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

## 8. Configure the Voice Client

Run on Raspberry, replacing `<PC_LAN_IP>`, `<CARD>`, and `<DEVICE>`:

```bash
export TONTO_BACKEND_URL=http://<PC_LAN_IP>:8000
export TONTO_AUDIO_DEVICE=plughw:<CARD>,<DEVICE>
export TONTO_RECORD_SECONDS=6
export TONTO_AUDIO_PATH=/tmp/tonto-turn-phase-2b.wav
export TONTO_DEVICE_ID=tonto-pi
export TONTO_TTS_ARGS="-v es -s 135 -g 8"
printf 'TONTO_TTS_ARGS=%s\n' "$TONTO_TTS_ARGS"
```

Optional: if the default ALSA capture device is already the USB microphone, leave `TONTO_AUDIO_DEVICE` unset and record that decision:

```bash
unset TONTO_AUDIO_DEVICE
```

Evidence to record:

- Exact environment values used.
- Whether `TONTO_AUDIO_DEVICE` was explicit or unset.
- Exact `TONTO_TTS_ARGS` value.

Acceptance:

- `TONTO_BACKEND_URL` points to the Windows backend LAN address, not `localhost`.
- `TONTO_RECORD_SECONDS` stays within the supported `1..10` range.
- `TONTO_AUDIO_PATH` points to a writable Raspberry path.
- `TONTO_TTS_ARGS` is `-v es -s 135 -g 8`, unless explicitly testing an equivalent later tuning.

## 9. Run the Client in Voice Mode

Run on Raspberry from the repository root:

```bash
.venv/bin/python client/main.py --mode voice
```

Expected startup output includes:

```text
TONTO Kids Assistant Client
Session: local-session-...
Voice mode: press Enter to capture audio, or type a message.
Type 'exit' or 'quit' to stop.
```

Evidence to record:

- Exact command used.
- Startup output.
- Session ID prefix, without requiring a fixed UUID.

Acceptance:

- Client starts without dependency changes.
- Client does not require any new Python package.

## 10. Validate Enter-to-Capture Voice Turn

At the client prompt, press Enter on an empty line.

Suggested spoken phrase during recording:

```text
Hola TONTO, explicame que es una estrella y por que brilla en el cielo.
```

Expected client flow:

```text
>
Recording...
Uploading...
Transcript: <recognized Spanish text>
TONTO: <child-friendly educational response>
```

After the turn completes, inspect the generated WAV from another Raspberry terminal:

```bash
ls -lh /tmp/tonto-turn-phase-2b.wav
file /tmp/tonto-turn-phase-2b.wav
```

If `file` is unavailable, record `ls -lh` and continue; do not install new packages just for this check.

Evidence to record:

- Whether pressing Enter started recording.
- Whether `Recording...` and `Uploading...` appeared.
- WAV file size.
- WAV metadata if available.
- `Transcript:` line.
- `TONTO:` line.
- Whether `espeak -v es -s 135 -g 8` played the response.
- Whether the long response was slower and understandable enough for demo.
- Whether words still sounded rushed or ran together.
- Any ALSA/JACK warnings.

Expected WAV format:

```text
RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 16000 Hz
```

Acceptance:

- Pressing Enter records through `arecord`.
- WAV file exists and is non-empty.
- Client uploads to `POST /chat/audio` and receives a valid response.
- Transcript is non-empty and not `[audio input captured]`.
- Transcript is reasonably close to the spoken phrase.
- Response is child-friendly and speakable.
- `espeak -v es -s 135 -g 8` playback is audible, slower than the previous `-v es` pass, and understandable enough for demo.
- The long response does not noticeably smear words together.

## 11. Validate Typed-Message Fallback Inside Voice Mode

At the same `--mode voice` prompt, type a text message instead of pressing Enter:

```text
Explicame que es la Luna en una frase.
```

Expected client flow:

```text
> Explicame que es la Luna en una frase.
TONTO: <child-friendly text response>
```

Evidence to record:

- Typed prompt.
- `TONTO:` response.
- Whether `espeak` played the response.
- Any backend or TTS errors.

Acceptance:

- Typed input inside `--mode voice` still works through the stable `/chat` text path.
- Audio capture is not triggered for non-empty typed input.

## 12. Validate Clean Exit

At the same client prompt, run either:

```text
exit
```

or:

```text
quit
```

Evidence to record:

- Exit command used.
- Whether the process returned to the shell without traceback.

Acceptance:

- `exit` or `quit` closes cleanly.
- No Python traceback appears.

## Troubleshooting

### Backend Unreachable

Client output may show:

```text
Could not reach backend: ...
```

Check:

- `TONTO_BACKEND_URL` uses the Windows LAN IP, not `localhost`.
- Backend was started with `.\scripts\dev.ps1 -Service backend -AllowLan`.
- Raspberry and Windows PC are on the same network.
- Windows firewall allows the backend port on the active network.
- `curl -sS "$TONTO_BACKEND_URL/health"` works from Raspberry.

### Backend Timeout

Client output may show:

```text
Backend request timed out
```

Record:

- Which step timed out.
- Whether backend logs show STT or chat provider latency.
- Whether a shorter `TONTO_RECORD_SECONDS` value changes the result.

Do not optimize or change timeouts during validation unless a separate implementation task is opened.

### Missing `arecord`

Client output may show:

```text
arecord not found. Install alsa-utils on the Raspberry Pi.
```

Resolution:

```bash
sudo apt update
sudo apt install -y alsa-utils
```

Record the package install as Raspberry environment repair, not as a Python dependency change.

### Capture Failure

Client output may show:

```text
arecord failed with exit code ...
arecord stderr: ...
```

Check:

- `arecord -l` still shows the USB microphone.
- `TONTO_AUDIO_DEVICE` matches the current `card,device`.
- No other process is using the capture device.
- Manual capture works:

```bash
arecord -D "$TONTO_AUDIO_DEVICE" -f S16_LE -r 16000 -c 1 -d 3 /tmp/tonto-manual-check.wav
aplay /tmp/tonto-manual-check.wav
```

### Missing or Empty WAV

Client output may show:

```text
WAV file was not created at ...
WAV file is empty at ...
```

Check:

- `TONTO_AUDIO_PATH` points to a writable path such as `/tmp/tonto-turn-phase-2b.wav`.
- The Raspberry has enough free disk space.
- Manual `arecord` can write to the same path.

### HTTP Errors

Client output may show:

```text
Backend error 400: ...
Backend error 413: ...
Backend error 415: ...
Backend error 422: ...
Backend error 502: ...
Backend error 504: ...
```

Interpretation:

- `400`: missing fields, invalid metadata, empty file, malformed WAV, or duration issue.
- `413`: uploaded WAV is too large.
- `415`: WAV format is unsupported.
- `422`: valid audio but no recognizable speech or empty transcript.
- `502`: STT provider failure.
- `504`: STT or conversational timeout.

Record the full status and response body. Do not change the backend contract during validation.

### Invalid JSON

Client output may show:

```text
Backend returned invalid JSON
```

Check:

- Backend logs for traceback or proxy errors.
- Whether `/health` still returns JSON.
- Whether the backend process is still running.

### Missing or Failing `espeak`

Client output may show:

```text
TTS command not found: espeak
TTS command failed with exit code ...
```

Check:

```bash
which espeak
printf 'TONTO_TTS_ARGS=%s\n' "${TONTO_TTS_ARGS:-<unset>}"
espeak -v es -s 135 -g 8 "Prueba de audio lenta y clara para TONTO"
```

If needed:

```bash
sudo apt update
sudo apt install -y espeak
```

Record whether the issue blocks the demo. A successful transcript and response without audible TTS is not a full Phase 2B pass.

## Acceptance Criteria

Phase 2B validation passes only when all of these are true:

- Raspberry reaches backend `/health`.
- `--mode voice` starts with no Python dependency changes.
- Pressing Enter records a WAV through `arecord`.
- Client uploads to `POST /chat/audio` and receives a valid response.
- Client prints a real non-empty `Transcript:` line.
- Client prints a child-friendly `TONTO:` response.
- `espeak -v es -s 135 -g 8` or equivalent `TONTO_TTS_ARGS` audibly plays the response.
- The long response is slower, understandable, and does not noticeably run words together.
- Typing a text message in voice mode still uses `/chat` successfully.
- `exit` or `quit` closes cleanly.
- ALSA/JACK warnings, if any, are recorded and judged non-blocking only if audio works.

If any criterion fails, do not mark Phase 2B as validated. Record the blocker and suggested follow-up instead.

## Final Documentation Update After Real Validation

After collecting evidence, update the repository documentation using the actual results.

Update `docs/project-journal/week-03.md` with a section named:

```markdown
## Fase 2B Validation Evidence
```

Include:

- Date/time.
- Branch and status.
- Python test result.
- Backend model settings, excluding API key.
- Windows LAN IP used.
- Raspberry host/user/tools.
- Microphone `card/device`.
- Client environment values.
- WAV metadata.
- Transcript.
- Response.
- TTS playback result.
- Typed-message fallback result.
- Clean exit result.
- Final pass/fail conclusion.

Update `specs/audio-pipeline.md`:

- Mark post-adjustment Phase 2B Raspberry validation as completed only if all acceptance criteria passed.
- If validation failed or was not rerun after the TTS tuning, leave Phase 2B as implemented and previously validated, but pending post-TTS revalidation.

Update `docs/roadmap.md`:

- Replace the pending post-TTS revalidation note only after hardware validation passes.
- Otherwise keep Phase 2B as implemented and Phase 3 blocked pending post-TTS revalidation.

Update `docs/specs.md` and `docs/architecture.md` only if the validation result changes durable project status.

Update `README.md` only if the public project status should change.

Update `AGENTS.md` after the post-TTS revalidation passes or fails so future agents know whether Phase 3 is still blocked.

Run final local checks from Windows after documentation updates:

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
- [ ] `TONTO_BACKEND_URL` configured.
- [ ] `TONTO_AUDIO_DEVICE` selected or explicitly left unset.
- [ ] `TONTO_RECORD_SECONDS` configured.
- [ ] `TONTO_AUDIO_PATH` configured.
- [ ] `TONTO_DEVICE_ID` configured.
- [ ] `TONTO_TTS_ARGS=-v es -s 135 -g 8` confirmed.
- [ ] Client starts with `.venv/bin/python client/main.py --mode voice`.
- [ ] Enter starts recording.
- [ ] Client prints `Recording...`.
- [ ] Client prints `Uploading...`.
- [ ] WAV file exists and is non-empty.
- [ ] WAV format verified when `file` is available.
- [ ] Client prints real transcript.
- [ ] Client prints response.
- [ ] Response played with `espeak -v es -s 135 -g 8`.
- [ ] Long response is slower and understandable enough for demo.
- [ ] Words do not noticeably run together in the long response.
- [ ] ALSA/JACK warnings recorded if present.
- [ ] Typed-message fallback works in `--mode voice`.
- [ ] `exit` or `quit` closes cleanly.
- [ ] `docs/project-journal/week-03.md` updated with evidence after validation.
- [ ] `specs/audio-pipeline.md` updated with validation status after validation.
- [ ] `docs/roadmap.md` updated after validation.
- [ ] `AGENTS.md` updated with whether Phase 3 remains blocked.
- [ ] Final `.\scripts\test.ps1 -Target python` passes after documentation updates.
- [ ] Final `git diff --check` passes.
- [ ] Final `git status --short --branch` recorded.
