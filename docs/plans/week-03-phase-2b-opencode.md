# OpenCode Task: Implementar Fase 2B Semana 3 - Cliente Raspberry de Voz

Repositorio: `C:\dev\projects\tonto-kids-assistant`

## Objetivo

Implementar la Fase 2B de Semana 3: automatizar en el cliente Raspberry el flujo ya validado manualmente:

```text
Enter en cliente -> arecord WAV -> POST /chat/audio -> transcript + response -> espeak local
```

El cambio debe preservar el loop de texto actual como fallback estable, no anadir dependencias Python nuevas, no tocar el contrato backend y mantener la Raspberry como thin client.

## Reglas previas obligatorias

Antes de editar:

```powershell
git branch --show-current
git status --short --branch
```

- No trabajar en `main`.
- Usar rama de proyecto tipo `feature/raspberry-voice-loop` si hace falta crear una.
- No usar prefijos `codex/` u otros tool-owned.
- Respetar `AGENTS.md` y `docs/ai-assisted-workflow.md`.
- No anadir dependencias sin aprobacion humana.

## Cambios de implementacion

Actualizar `client/main.py` para soportar:

- `--mode text`: comportamiento actual, `POST /chat`, entrada manual, TTS local.
- `--mode voice`: loop interactivo por turnos; Enter graba audio, sube WAV, muestra transcript/response y reproduce `response`.

Configuracion:

- `TONTO_BACKEND_URL`: obligatorio.
- `TONTO_AUDIO_DEVICE`: opcional, ejemplo `plughw:1,0`; si falta, usar `arecord` sin `-D`.
- `TONTO_RECORD_SECONDS`: default `6`, permitido `1..10`.
- `TONTO_AUDIO_PATH`: default `/tmp/tonto-turn.wav` o equivalente compatible.
- `TONTO_DEVICE_ID`: default `tonto-pi`.
- `TONTO_TTS_COMMAND`: default `espeak`.

Captura:

```bash
arecord [-D "$TONTO_AUDIO_DEVICE"] -f S16_LE -r 16000 -c 1 -d <seconds> <wav_path>
```

Subida:

- Usar solo libreria estandar Python (`urllib.request`) y multipart manual.
- Enviar a `POST /chat/audio`:
  - `audio`
  - `session_id`
  - `device_id`
  - `duration_ms`
  - `sample_rate_hz=16000`
  - `channels=1`
  - `language=es`

Errores a manejar claramente:

- backend no alcanzable,
- timeout,
- `arecord` no instalado,
- fallo de captura,
- WAV no creado o vacio,
- HTTP `400/413/415/422/502/504`,
- JSON invalido,
- `espeak` no instalado o codigo no cero.

## Documentacion a actualizar

Actualizar solo lo necesario:

- `specs/audio-pipeline.md`
- `docs/project-journal/week-03.md`
- `docs/raspberry-pi-setup.md`
- `docs/specs.md`
- `docs/roadmap.md`

No actualizar `AGENTS.md` salvo que la validacion real cambie instrucciones persistentes.

## Tests

Anadir tests unitarios del cliente sin hardware real:

- modo texto conserva `/chat`,
- multipart contiene archivo y campos requeridos,
- respuesta valida de `/chat/audio` extrae `transcript` y `response`,
- errores HTTP y JSON invalido se reportan sin romper el loop,
- captura llama a `arecord` con y sin `TONTO_AUDIO_DEVICE`,
- fallo de `arecord` o WAV vacio no intenta subir,
- TTS maneja `FileNotFoundError` y codigos no cero.

Ejecutar:

```powershell
.\scripts\test.ps1 -Target python
git diff --check
```

## Validacion manual esperada en Raspberry

Backend en Windows:

```powershell
.\scripts\dev.ps1 -Service backend -AllowLan
```

Raspberry:

```bash
arecord -l
export TONTO_BACKEND_URL=http://<PC_LAN_IP>:8000
export TONTO_AUDIO_DEVICE=plughw:<CARD>,<DEVICE>
.venv/bin/python client/main.py --mode voice
```

Criterios de aceptacion:

- Enter inicia captura.
- Se genera WAV compatible.
- `/chat/audio` devuelve `HTTP 200`.
- Se muestra transcript real.
- Se muestra respuesta educativa.
- `espeak` reproduce la respuesta.
- `exit` o `quit` cierra limpio.
- El modo texto sigue funcionando.
