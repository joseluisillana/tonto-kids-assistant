# Audio Pipeline Phase 3 Web Loop

## Objetivo

La Fase 3 de Semana 3 planifica el loop interactivo de voz desde el cliente web de validacion:

```text
navegador -> captura de microfono -> WAV PCM 16 kHz mono -> POST /chat/audio -> transcript -> response text -> browser speech
```

Esta fase no sustituye al objetivo fisico con Raspberry. Su proposito es acelerar la validacion del backend STT ya activo, reducir friccion de demo y recoger evidencia desde navegador despues de cerrar la automatizacion del cliente Raspberry y su revalidacion post-TTS en Fase 2B.

La mision revisada de Fase 3 incluye respuesta audible desde el navegador. No basta con mostrar evidencia textual: la web debe capturar audio por microfono, mostrar la transcripcion, mostrar la respuesta textual y reproducir esa respuesta de forma audible y entendible usando APIs nativas del navegador.

## Alcance

Incluido:

- Usar el cliente web existente como superficie de validacion de voz.
- Capturar un turno corto desde el microfono del navegador.
- Generar un WAV compatible con el contrato actual de `POST /chat/audio`.
- Reutilizar `session_id`, `language=es` y el backend STT OpenAI `gpt-4o-mini-transcribe`.
- Mostrar `transcript`, `response`, latencia y estado tecnico en la UI.
- Reproducir la `response` de forma audible y entendible desde el navegador.
- Mantener el flujo de texto `/chat` como fallback estable.
- Documentar evidencia manual despues de validar el flujo.

Fuera de alcance:

- Wake word.
- Streaming de audio.
- STT local, Vosk, `whisper.cpp` o modelos locales.
- Transcoding backend de `webm`, `ogg` u otros formatos comprimidos.
- Selector o subida manual de archivos WAV como flujo visible de producto/demo web.
- Persistencia de audios, transcripts o evidencias fuera de la documentacion.
- Autenticacion, usuarios o permisos persistentes.
- UI avanzada de producto.
- Sustituir la validacion final en Raspberry.

Los archivos WAV pregrabados pueden usarse como fixtures o helpers internos de testing unitario/integracion, pero no deben aparecer como mecanismo de uso en la UI de demo.

## Decision Tecnica Inicial

El backend `POST /chat/audio` acepta inicialmente WAV PCM 16-bit, 16 kHz y mono. Los navegadores suelen producir `webm` u `ogg` con `MediaRecorder`, por lo que la Fase 3 debe evitar subir esos formatos directamente.

La implementacion debe producir WAV en el navegador usando APIs nativas (`getUserMedia`, Web Audio API y codificacion WAV propia pequena), sin dependencia nueva. La captura de microfono es requisito de esta fase; un selector manual de WAV no es un sustituto aceptable para la UI de producto/demo.

La respuesta audible debe hacerse en el navegador con Web Speech API (`speechSynthesis`) u otra API nativa equivalente disponible en el browser. No se debe ampliar el backend para generar audio, aceptar formatos comprimidos ni introducir `ffmpeg`/transcoding salvo decision explicita posterior.

## Cambios Documentales Requeridos

Antes de implementar codigo, mantener alineados:

- `docs/roadmap.md`: registrar Fase 3 como trabajo pendiente de Semana 3 posterior a Fase 2B, incluyendo respuesta audible web.
- `specs/audio-pipeline.md`: referenciar este plan como extension web del contrato `/chat/audio`.
- `specs/web-validation-client.md`: ampliar el rol del cliente web a validacion de audio y speech output.
- `docs/specs.md`: resumir el nuevo alcance activo.
- `docs/architecture.md`: describir la variante web de audio sin cambiar la arquitectura principal.
- `docs/project-journal/week-03.md`: registrar plan revisado y, despues de validar, evidencia.
- `README.md`: reflejar estado actual de Semana 3.
- `AGENTS.md`: indicar a agentes que la web debe validar captura de microfono, transcript, respuesta textual y respuesta audible, manteniendo el producto fisico y Raspberry como objetivo MVP.

## Instrumentacion Esperada

La implementacion futura deberia exponer evidencia visible en la web o en logs de desarrollo:

- `backendUrl` usado.
- Estado `/health`.
- Soporte de microfono en navegador.
- Estado de permiso de microfono.
- Estado de grabacion: idle, requesting-permission, recording, encoding, uploading, transcribing, complete, error.
- Soporte de Web Speech API / `speechSynthesis`.
- Estado de reproduccion audible: idle, speaking, complete, error.
- Duracion grabada aproximada.
- Tamano del WAV generado.
- Tipo MIME enviado.
- `session_id` usado.
- `language` usado.
- HTTP status de `/chat/audio`.
- Latencia total percibida por el navegador.
- `transcript` devuelto por STT.
- `response` devuelta por el backend.
- Voz/idioma usado para speech si el navegador lo expone.
- Mensaje de error legible si falla permiso, formato, timeout, STT, backend o speech output.

No se deben registrar secretos ni persistir audio por defecto.

## Contrato HTTP

La web debe usar el mismo contrato ya validado:

```text
POST /chat/audio
Content-Type: multipart/form-data
```

Campos:

- `audio`: WAV generado desde el microfono del navegador.
- `session_id`: sesion activa del cliente web.
- `device_id`: valor recomendado `web-validation-client`.
- `duration_ms`: duracion aproximada del turno.
- `sample_rate_hz`: `16000` si se genera WAV compatible.
- `channels`: `1`.
- `language`: `es`.

Respuesta esperada:

```json
{
  "session_id": "web-phase-3-validation",
  "transcript": "texto reconocido",
  "response": "respuesta educativa"
}
```

## Validacion Manual Prevista

Comandos base en Windows:

```powershell
git branch --show-current
git status --short --branch
.\scripts\setup-dev.ps1
.\scripts\test.ps1 -Target python
.\scripts\test.ps1 -Target web
.\scripts\build.ps1 -Target web
```

Configurar backend sin revelar secretos:

```powershell
if (-not $env:OPENAI_API_KEY) { throw "OPENAI_API_KEY is not set" }
$env:OPENAI_STT_MODEL = "gpt-4o-mini-transcribe"
$env:OPENAI_MODEL = "gpt-4o-mini"
"OPENAI_API_KEY configured"
"OPENAI_STT_MODEL=$env:OPENAI_STT_MODEL"
"OPENAI_MODEL=$env:OPENAI_MODEL"
```

Arrancar backend y web:

```powershell
.\scripts\dev.ps1 -Service all
```

Evidencia a recoger:

- Navegador y version.
- URL web usada.
- Backend URL usada.
- Frase grabada, por ejemplo: `Hola TONTO, explicame que es una estrella`.
- Duracion de audio.
- Tamano y formato del WAV.
- HTTP status.
- Latencia total.
- Transcript.
- Response.
- Resultado de reproduccion audible en navegador.
- Captura o transcripcion del panel tecnico.
- Resultado de prueba negativa: permiso denegado, audio vacio, navegador sin microfono o navegador sin soporte de speech si aplica.

## Criterios de Aceptacion

- El cliente web conserva el flujo de texto `/chat`.
- El usuario puede iniciar un turno de voz desde el microfono web.
- El turno de voz no depende de un selector WAV visible.
- La web envia un WAV aceptado por `POST /chat/audio` sin cambiar el contrato backend.
- El backend devuelve `HTTP 200` con `session_id`, `transcript` real y `response`.
- El transcript no es `[audio input captured]` ni esta vacio.
- La respuesta aparece como texto y se reproduce de forma audible y entendible desde el navegador.
- La UI muestra estado, errores y latencia suficiente para depurar.
- No se introduce STT local, streaming, persistencia ni nueva dependencia sin decision explicita.
- `.\scripts\test.ps1 -Target web`, `.\scripts\build.ps1 -Target web` y los tests Python relevantes pasan.

## Paso Final Documental

Cuando la Fase 3 se implemente y valide, actualizar:

- `docs/project-journal/week-03.md`: seccion `Fase 3 Web Loop Validation Evidence`.
- `specs/audio-pipeline.md`: marcar Fase 3 como implementada o documentar bloqueo.
- `specs/web-validation-client.md`: actualizar criterios de aceptacion.
- `docs/roadmap.md`: marcar Fase 3 completa, parcial o bloqueada.
- `docs/specs.md` y `docs/architecture.md`: reflejar el estado real validado.
- `README.md`: refrescar estado actual de Semana 3.
- `AGENTS.md`: si la fase queda activa, ajustar instrucciones persistentes para futuros agentes.

Ejecutar despues:

```powershell
.\scripts\test.ps1 -Target python
.\scripts\test.ps1 -Target web
.\scripts\build.ps1 -Target web
git diff --check
git status --short --branch
```
