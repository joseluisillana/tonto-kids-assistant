# TONTO Demo Checklist

**Audience:** demo operator
**Purpose:** verify the TONTO MVP before presentation day and follow a stable demo sequence.
**Last Updated:** 2026-06-14

Use this checklist with `docs/demo-runbook.md`. The runbook explains the full operating flow; this file is the presentation-day checklist.

## 1. Presentation Preconditions

- [ ] Windows development PC is available and connected to power.
- [ ] Raspberry Pi 3 is available, powered, and on the same LAN as the Windows PC.
- [ ] USB microphone and speaker/audio output are connected to the Raspberry.
- [ ] The active LAN IP of the Windows PC is known.
- [ ] Windows Firewall allows backend traffic on port `8000` for the current network.
- [ ] Repository is available on Windows at the expected project path.
- [ ] Repository is available on Raspberry at `~/tonto-kids-assistant` or `TONTO_PI_REPO`.
- [ ] Python virtual environment exists on Windows and Raspberry.
- [ ] Raspberry has `arecord`, `aplay`, `espeak`, `curl`, `git`, and `.venv/bin/python`.
- [ ] Required provider API key is configured in the backend PowerShell terminal.
- [ ] No real API keys, tokens, passwords, or SSH private keys are printed, recorded, or committed.

## 2. Choose Provider

Use OpenAI as the primary presentation provider unless there is a specific reason to demonstrate DevExpert.

### OpenAI

In the backend PowerShell terminal:

```powershell
$env:TONTO_INFERENCE_PROVIDER = "openai"
$env:OPENAI_API_KEY = "<your-openai-api-key>"
$env:OPENAI_MODEL = "gpt-4o-mini"
$env:OPENAI_STT_MODEL = "gpt-4o-mini-transcribe"
```

Expected use:

- Primary demo path.
- Previously validated with 6/6 Raspberry voice turns on 2026-06-13.

### DevExpert

In the backend PowerShell terminal:

```powershell
$env:TONTO_INFERENCE_PROVIDER = "devexpert"
$env:DEVEXPERT_API_KEY = "<your-devexpert-api-key>"
$env:DEVEXPERT_BASE_URL = "https://inference.devexpert.io/v1"
$env:DEVEXPERT_CHAT_MODEL = "mimo-v2.5"
$env:DEVEXPERT_STT_MODEL = "gpt-4o-mini-transcribe"
```

Expected use:

- Optional provider smoke or course alignment note.
- Previously validated with 1/1 Raspberry voice smoke on 2026-06-13.
- If DevExpert responses are too verbose during presentation, switch back to OpenAI.

## 3. Backend Verification

Start the backend with LAN access from the configured backend PowerShell terminal:

```powershell
.\scripts\dev.ps1 -Service backend -AllowLan
```

Keep the backend terminal open.

Verify local health from another PowerShell terminal:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -Method Get
```

Expected result:

```json
{"status":"ok"}
```

Run a text provider smoke:

```powershell
$body = @{ session_id = "presentation-smoke"; message = "Responde solo: ok" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/chat" -Method Post -ContentType "application/json" -Body $body
```

Expected result:

- HTTP request succeeds.
- Response is short and confirms the active provider can answer.

Optional agent helper:

```powershell
.\scripts\agent-backend.ps1 -Action health
```

## 4. Raspberry Verification

Set the backend URL in the Windows terminal used for Raspberry helper commands:

```powershell
$env:TONTO_BACKEND_URL = "http://<WINDOWS_LAN_IP>:8000"
```

Run the Raspberry preflight when the dedicated SSH key is configured:

```powershell
.\scripts\agent-raspberry.ps1 -Action preflight
```

Expected checks:

- Raspberry identity is correct.
- Repository is present.
- Required tools exist.
- `.venv/bin/python` exists.
- Backend `/health` responds when `TONTO_BACKEND_URL` is set.

If operating manually over SSH, run:

```bash
cd ~/tonto-kids-assistant
git status --short --branch
arecord -l
curl http://<WINDOWS_LAN_IP>:8000/health
```

Expected result:

- `arecord -l` shows the USB microphone.
- Backend health returns `{"status":"ok"}`.

Optional microphone check:

```bash
arecord -D plughw:<CARD>,<DEVICE> -f S16_LE -r 16000 -c 1 -d 5 ~/tonto-mic-check.wav
aplay ~/tonto-mic-check.wav
```

Expected result:

- Recording succeeds.
- Playback is audible enough for demo.

## 5. Raspberry Demo Start

On the Raspberry:

```bash
cd ~/tonto-kids-assistant
export TONTO_BACKEND_URL=http://<WINDOWS_LAN_IP>:8000
./scripts/demo-raspberry.sh
```

Expected startup:

- Backend health passes.
- Client starts in voice mode.
- Prompt says `Voice mode: press Enter to capture audio`.
- Listening indicator appears during capture.
- After capture, the client prints `Uploading...`, `Transcript:`, and `TONTO:`.
- `espeak` plays the answer aloud.

Before the live demo, run one short smoke:

```text
Hola TONTO, dime solo hola.
```

Accept the smoke if:

- Transcript is recognizable.
- Response is short.
- Audio output is audible.

## 6. Web Verification (Optional)

Use the web client if it is part of the presentation or as a fallback.

Start the web client on Windows:

```powershell
.\scripts\dev.ps1 -Service web
```

Open:

```text
http://127.0.0.1:5173/
```

Verify:

- [ ] Browser microphone permission is granted.
- [ ] Correct microphone is selected in browser settings.
- [ ] Voice capture shows visible timer/progress.
- [ ] Capture auto-stops at the configured limit.
- [ ] `Enviar voz` sends the recorded audio.
- [ ] Transcript and response appear on screen.
- [ ] Browser speech plays the answer when supported.
- [ ] Text chat still works as fallback through `/chat`.

If the web voice path returns `422 Audio did not contain recognizable speech`, select the correct microphone and retry.

## 7. Recommended Demo Sequence

Keep questions short and speak clearly. Wait for TONTO to finish speaking before the next turn.

1. Greeting:

```text
Hola TONTO, como estas?
```

Expected: friendly greeting, short answer, asks what to learn.

2. Simple science:

```text
Que es una estrella?
```

Expected: child-friendly explanation in Spanish.

3. Context follow-up:

```text
Y el Sol es una estrella?
```

Expected: uses short-session context and explains that the Sun is the closest star to Earth.

4. Everyday learning:

```text
Por que llueve?
```

Expected: simple explanation with water/cloud cycle.

5. Safety or factual-care check:

```text
Si me duele la barriga, que hago?
```

Expected: gentle, non-diagnostic answer that suggests telling an adult.

6. Short creative turn:

```text
Inventame una frase divertida sobre aprender.
```

Expected: brief playful educational sentence.

7. Closing:

```text
Gracias TONTO, hasta luego.
```

Expected: natural goodbye.

Do not force all seven turns if the presentation time is short. The minimum live sequence is greeting, one educational question, one follow-up, and goodbye.

## 8. Plan B

### Raspberry voice fails

Use the web voice loop if the browser microphone works:

```powershell
.\scripts\dev.ps1 -Service web
```

Then open `http://127.0.0.1:5173/`.

### Raspberry microphone is not detected

Run:

```bash
arecord -l
```

If the USB microphone is missing:

- Reconnect the USB audio device.
- Reboot the Raspberry only if there is time.
- Switch to web voice or text fallback.

### Raspberry audio output is too quiet

- Check speaker power and volume first.
- Use the visible response text as backup evidence.
- Switch to web speech if the browser audio is clearer.

### Backend is unreachable from Raspberry

Check:

- Backend terminal is still running.
- Backend was started with `-AllowLan`.
- `TONTO_BACKEND_URL` uses the Windows LAN IP, not `127.0.0.1`.
- Windows Firewall allows port `8000`.
- Raspberry and Windows PC are on the same network.

Fallback:

- Use local web/text checks from Windows if LAN debugging would take too long.

### Provider fails

- If DevExpert fails, restart backend with OpenAI.
- If OpenAI fails, retry once with a shorter prompt.
- If both providers fail, use the already recorded Week 05 evidence and demonstrate the local UI/runbook rather than changing code live.

### STT returns poor transcript

- Repeat the turn once, closer to the microphone.
- Use shorter questions.
- Confirm browser/Raspberry selected the intended microphone.

### Response is too long

- Ask a shorter question.
- Prefer OpenAI for the polished live demo.
- Do not change prompt or token settings during the presentation.

## 9. Final Ready Check

Run this immediately before presenting:

- [ ] Backend is running and `/health` returns `ok`.
- [ ] Active provider is known: OpenAI or DevExpert.
- [ ] Raspberry can reach `http://<WINDOWS_LAN_IP>:8000/health`.
- [ ] Raspberry voice smoke passed.
- [ ] Speaker output is audible in the room.
- [ ] Web client is open if used as fallback.
- [ ] Browser microphone is correct if web voice is used.
- [ ] Demo questions are ready.
- [ ] Operator knows the Plan B path.
- [ ] No untested code or configuration changes are made after this point.

## 10. Evidence To Record After Demo

For Week 06 closeout, record in `docs/project-journal/week-06.md`:

- Date and provider used.
- Whether Raspberry voice, web voice, and text fallback were checked.
- Turn-by-turn inputs.
- Transcript quality.
- Response quality.
- TTS or browser speech audibility.
- Approximate latency per turn.
- Any issue encountered and which Plan B step was used.
