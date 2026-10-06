# TONTO Demo Runbook

Before provider operation, apply [D025](decisions.md#d025---devexpert-deprecado-para-la-validación-post-migración):
OpenAI is the real validated path. DevExpert examples below preserve historical
setup and smoke knowledge, not permission to operate it. Do not request its
credentials, run a real smoke or reactivate it without a new operator decision.

**Audience:** Demo operator
**Last Updated:** 2026-10-05

## Prerequisites

- Linux host with backend running.
- Raspberry Pi connected to the same LAN as the Linux host.
- USB audio device (microphone + speaker) connected to the Raspberry.
- Waveshare 5" Touch Screen connected to the Raspberry (HDMI for video, USB for power/touch).
- Python venv set up on the Raspberry.
- Docker Engine and Docker Compose installed; Node and npm run in containers.
- One backend inference provider configured in the backend configuration in `.env`: OpenAI or DevExpert.

## Provider Selection

TONTO selects the backend inference provider at backend startup through `TONTO_INFERENCE_PROVIDER`.

The supported values are:

| Value | Text generation | STT |
|---|---|---|
| `openai` | OpenAI Responses API | OpenAI audio transcriptions |
| `devexpert` | DevExpert Chat Completions | DevExpert audio transcriptions |

Docker Compose carga `.env` mediante `env_file`. El operador configura proveedor y credenciales tomando `.env.example` como plantilla. Los agentes no deben leer ni imprimir el archivo de secretos. Reiniciar el backend tras cambiar su configuración.

### OpenAI backend

El operador configura estos valores en `.env` (no mostrar ni registrar claves reales):

```dotenv
TONTO_INFERENCE_PROVIDER="openai"
OPENAI_API_KEY="<your-openai-api-key>"
OPENAI_MODEL="gpt-4o-mini"
OPENAI_STT_MODEL="gpt-4o-mini-transcribe"
```

OpenAI is also the default when `TONTO_INFERENCE_PROVIDER` is unset.

### DevExpert backend

El operador configura estos valores en `.env` (no mostrar ni registrar claves reales):

```dotenv
TONTO_INFERENCE_PROVIDER="devexpert"
DEVEXPERT_API_KEY="<your-devexpert-api-key>"
DEVEXPERT_BASE_URL="https://inference.devexpert.io/v1"
DEVEXPERT_CHAT_MODEL="mimo-v2.5"
DEVEXPERT_STT_MODEL="gpt-4o-mini-transcribe"
```

Do not print or commit real API keys. If using `scripts/agent-backend.sh`, configure the same values in `.env` first and then run:

```bash
./scripts/agent-backend.sh start
```

### Provider smoke check

After the backend starts, a text turn validates the active text provider:

```bash
curl --fail --silent --show-error http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d '{"session_id":"provider-smoke","message":"Responde solo: ok"}'
```

The voice loop validates the active STT provider through `POST /chat/audio`; use the Raspberry or web demo flow below.

## Quick Start

### 1. Start the backend (Linux/Docker)

```bash
./tonto.sh dev backend
```

The backend starts on `0.0.0.0:8000` with the provider configured by the operator in `.env`. Keep this terminal open.

### 2. Start the Raspberry client

```bash
cd ~/tonto-kids-assistant
./scripts/demo-raspberry.sh
```

The script checks backend health, sets default env vars, and starts voice mode with `.venv/bin/python`.

### 3. Start the web client (optional, Linux/Docker)

```bash
./tonto.sh dev web
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

```bash
./tonto.sh dev backend
```

### Step 2: Start the web client

```bash
./tonto.sh dev web
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
1. Check the backend is running in Docker on Linux: `./tonto.sh dev backend`
2. Check the IP is correct: `ping <linux-host-ip>` from Raspberry.
3. Check firewall allows port 8000 on Linux.
4. Verify `TONTO_BACKEND_URL` matches the Linux host IP.

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
