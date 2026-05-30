# Phase 2B TTS Revalidation After Speech Tuning

This spec defines the required revalidation pass after the Raspberry client TTS tuning committed as `fix: tune raspberry espeak demo speech`.

Phase 2B was previously validated on real Raspberry hardware, but that pass found the `espeak` playback audible yet robotic and unclear for demo. The client now defaults to:

```bash
espeak -v es -s 135 -g 8 "<response>"
```

Phase 3 must not begin until this adjusted Phase 2B loop is revalidated on real Raspberry hardware.

## Objective

Revalidate the full automated Raspberry voice loop with the tuned TTS arguments:

```text
Enter in client -> arecord WAV -> POST /chat/audio -> transcript + response -> espeak -v es -s 135 -g 8
```

The pass must prove that long responses are understandable enough for MVP/demo and that words do not run together.

## Scope

In scope:

- Windows host/backend checks using official scripts.
- Raspberry LAN connectivity to the backend.
- `client/main.py --mode voice` on real Raspberry hardware.
- Default or explicit `TONTO_TTS_ARGS=-v es -s 135 -g 8`.
- One voice turn intended to produce a longer response.
- Typed-message fallback inside `--mode voice`.
- Clean exit.
- Documentation of pass/fail evidence.

Out of scope:

- Running the Raspberry client on the Windows host.
- Changing `POST /chat` or `POST /chat/audio`.
- Changing backend STT provider or audio format.
- Adding dependencies.
- Browser/web Phase 3 work.
- Wake word, local STT, persistence, auth, or advanced UI.

## Windows Host Steps

Run from the repo root on the Windows host:

```powershell
git branch --show-current
git status --short --branch
.\scripts\test.ps1 -Target python
```

Start the backend for LAN access:

```powershell
.\scripts\dev.ps1 -Service backend -AllowLan
```

In another Windows terminal, verify health and record the LAN IP:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
Get-NetIPAddress -AddressFamily IPv4 |
  Where-Object { $_.IPAddress -notlike "127.*" -and $_.PrefixOrigin -ne "WellKnown" } |
  Select-Object InterfaceAlias,IPAddress
```

Record:

- Branch and status.
- Python test summary.
- Backend model settings, excluding `OPENAI_API_KEY`.
- Windows LAN IP used by Raspberry.

## Raspberry Steps

Run on Raspberry from the repo root:

```bash
git branch --show-current
git status --short --branch
git log -1 --oneline
which espeak
which arecord
arecord -l
```

Configure the client, replacing placeholders with current values:

```bash
export TONTO_BACKEND_URL=http://<PC_LAN_IP>:8000
export TONTO_AUDIO_DEVICE=plughw:<CARD>,<DEVICE>
export TONTO_RECORD_SECONDS=6
export TONTO_AUDIO_PATH=/tmp/tonto-turn-phase-2b-tts.wav
export TONTO_DEVICE_ID=tonto-pi
export TONTO_TTS_ARGS="-v es -s 135 -g 8"
printf 'TONTO_TTS_ARGS=%s\n' "$TONTO_TTS_ARGS"
curl -sS "$TONTO_BACKEND_URL/health"
```

Run the client:

```bash
.venv/bin/python client/main.py --mode voice
```

At the prompt, press Enter and say a prompt likely to produce a long response:

```text
Hola TONTO, explicame que es una estrella y por que brilla en el cielo.
```

From another Raspberry terminal, inspect the recorded WAV:

```bash
ls -lh /tmp/tonto-turn-phase-2b-tts.wav
file /tmp/tonto-turn-phase-2b-tts.wav
```

Then validate typed fallback inside the same client:

```text
Explicame que es la Luna en una frase.
```

Exit cleanly:

```text
exit
```

## Evidence to Record

Record the following in `docs/project-journal/week-03.md` after the real hardware run:

- Date/time and operator.
- Windows branch/status and Python test result.
- Backend model settings, excluding API key value.
- Windows LAN IP used by Raspberry.
- Raspberry branch/status and latest commit.
- Raspberry tools: `which espeak`, `which arecord`, `which aplay`.
- `arecord -l` card/device and selected `TONTO_AUDIO_DEVICE`.
- Exact `TONTO_TTS_ARGS`.
- Client startup output.
- WAV size and metadata.
- `Transcript:` line.
- `TONTO:` response.
- Whether `espeak` playback was audible.
- Whether long-response words were separated enough and not rushed.
- Any ALSA/JACK warnings and whether they blocked the demo.
- Typed-message fallback result.
- Clean exit result.
- Final pass/fail conclusion.

## Acceptance Criteria

The post-adjustment Phase 2B revalidation passes only when all of these are true:

- Python tests pass on the Windows host.
- Raspberry reaches backend `/health` over LAN.
- `--mode voice` starts on Raspberry without dependency changes.
- Pressing Enter records a non-empty WAV through `arecord`.
- The client uploads to `POST /chat/audio` and receives a real non-empty transcript.
- The backend returns a child-friendly response.
- The response is played with `espeak -v es -s 135 -g 8` by default or equivalent `TONTO_TTS_ARGS`.
- A long response is audible, slower than the previous pass, and understandable enough for MVP/demo.
- Words do not noticeably run together in the long response.
- ALSA/JACK warnings are recorded and are acceptable only if playback works.
- Typed fallback inside `--mode voice` still uses `/chat` successfully.
- `exit` or `quit` closes without traceback.

If any criterion fails, Phase 2B remains implemented with TTS tuning but not revalidated after the tuning. Record the blocker and do not proceed to Phase 3.

## Documentation Updates After the Run

If the revalidation passes:

- Mark Phase 2B as revalidated post-TTS adjustment in `specs/audio-pipeline.md`.
- Unblock Phase 3 in `docs/roadmap.md`, `docs/specs.md`, `README.md`, and `AGENTS.md`.
- Add evidence to `docs/project-journal/week-03.md`.

If the revalidation fails or is not run:

- Keep Phase 2B as implemented and previously validated, but pending post-TTS revalidation.
- Keep Phase 3 blocked.
- Document the failure or pending state and next follow-up.

Final local checks after documentation updates:

```powershell
.\scripts\test.ps1 -Target python
git diff --check
git status --short --branch
```
