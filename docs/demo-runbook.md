# TONTO Demo Runbook

**Audience:** Demo operator
**Last Updated:** 2026-06-08

## Prerequisites

- Windows PC with backend running.
- Raspberry Pi connected to the same LAN as the Windows PC.
- USB audio device (microphone + speaker) connected to the Raspberry.
- Python venv set up on the Raspberry.
- Node.js and npm installed on Windows (for web client, optional).

## Quick Start

### 1. Start the backend (Windows)

```powershell
.\scripts\dev.ps1 -Service backend -AllowLan
```

The backend starts on `0.0.0.0:8000`. Keep this terminal open.

### 2. Start the Raspberry client

```bash
cd ~/tonto-kids-assistant
./scripts/demo-raspberry.sh
```

The script checks backend health, sets default env vars, and starts voice mode with `.venv/bin/python`.

### 3. Start the web client (optional, Windows)

```powershell
.\scripts\dev.ps1 -Service web
```

Open `http://127.0.0.1:5173/` in a browser.

## Demo Flow — Raspberry

### Step 1: Start the demo

Run `./scripts/demo-raspberry.sh` on the Raspberry. You should see:

```
=== TONTO Demo Client (Raspberry) ===

Checking backend health (1/5)...
Backend is healthy.

Starting TONTO client in voice mode...
  Backend: http://192.168.1.91:8000
  Audio device: plughw:CARD=Device,DEV=0
  Recording duration: 6s

TONTO Kids Assistant Client
Session: local-session-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Voice mode: press Enter to capture audio, or type a message.
Type 'exit' or 'quit' to stop.
>
```

### Step 2: First voice turn (greeting)

Press **Enter** to start recording. Speak clearly for 6 seconds:

```
> [Enter]
Listening for 6s...
Listening: 1/6s
Listening: 2/6s
Listening: 3/6s
Listening: 4/6s
Listening: 5/6s
Listening: 6/6s
Listening complete.
Uploading...
Transcript: Hola TONTO, ¿cómo estás?
TONTO: ¡Hola! Estoy muy bien, gracias. ¿Y tú? ¿Qué quieres aprender hoy?
```

Wait for espeak to finish speaking before the next turn.

### Step 3: Educational questions

Press **Enter** again and ask a question:

```
> [Enter]
Listening for 6s...
...
Transcript: ¿Qué es una estrella?
TONTO: Una estrella es una bola muy caliente de gas que brilla en el cielo. El Sol es una estrella.
```

### Step 4: Follow-up questions (context)

Ask follow-up questions to test in-memory context:

```
> [Enter]
...
Transcript: ¿Y el Sol es una estrella?
TONTO: ¡Sí! El Sol es la estrella más cercana a la Tierra. Nos da luz y calor.
```

### Step 5: End the demo

Type `exit` and press Enter:

```
> exit
```

## Demo Flow — Web

### Step 1: Start the backend

```powershell
.\scripts\dev.ps1 -Service backend -AllowLan
```

### Step 2: Start the web client

```powershell
.\scripts\dev.ps1 -Service web
```

### Step 3: Open the browser

Navigate to `http://127.0.0.1:5173/`.

### Step 4: Select microphone

If prompted, select the correct microphone in the browser settings.

### Step 5: Record and send

1. Press the microphone button to start recording.
2. Speak clearly (maximum 10 seconds, auto-stop at limit).
3. Press **"Enviar voz"** to send.
4. View transcript and response on screen.
5. Response plays through browser speech.

## Known Warnings (Safe to Ignore)

### ALSA/JACK warnings (Raspberry)

These warnings appear after every espeak playback. They are non-blocking and do not affect the demo:

```
ALSA lib confmisc.c:1377:(snd_func_refer) Unable to find definition ...
ALSA lib conf.c:5205:(_snd_config_evaluate) function snd_func_refer returned error ...
...
Cannot connect to server socket err = No such file or directory
Cannot connect to server request channel
jack server is not running or cannot be started
```

**Action:** Ignore. The demo continues normally.

## Troubleshooting

### "Backend not reachable"

**Symptom:** Script shows `ERROR: Backend at http://... is not reachable`.

**Fix:**
1. Check the backend is running on Windows: `.\scripts\dev.ps1 -Service backend -AllowLan`
2. Check the IP is correct: `ping <windows-pc-ip>` from Raspberry.
3. Check firewall allows port 8000 on Windows.
4. Verify `TONTO_BACKEND_URL` matches the Windows PC IP.

### "arecord not found"

**Symptom:** `arecord: command not found`

**Fix:** Install alsa-utils:
```bash
sudo apt-get update && sudo apt-get install -y alsa-utils
```

### "No audio device"

**Symptom:** Recording fails with device error.

**Fix:**
1. List devices: `arecord -l`
2. Set the correct device: `export TONTO_AUDIO_DEVICE=plughw:CARD=<card>,DEV=<device>`
3. Re-run the script.

### "espeak not found"

**Symptom:** `espeak: command not found`

**Fix:** Install espeak:
```bash
sudo apt-get update && sudo apt-get install -y espeak
```

### Web: "422 Audio did not contain recognizable speech"

**Symptom:** Backend returns 422 error.

**Fix:** Select the correct microphone in the browser settings. The browser may be using the wrong audio input.

### Script fails with "permission denied"

**Symptom:** `./scripts/demo-raspberry.sh: Permission denied`

**Fix:** Make the script executable:
```bash
chmod +x scripts/demo-raspberry.sh
```
