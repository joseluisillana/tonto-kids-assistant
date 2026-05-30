# Pipeline de Audio de TONTO MVP

## Introducción

Este documento describe el pipeline de audio para la versión MVP de TONTO, un asistente para niños. El enfoque está en simplicidad y estabilidad, utilizando un Raspberry Pi 3 como thin client. El audio output ya está validado, y la captura inicial con micrófono USB quedó validada en Raspberry durante Semana 3.

Semana 3 empieza con una fase de preparación: validar hardware de entrada y dejar el repositorio listo para implementar voz sin cambiar todavía contratos públicos ni añadir dependencias. El loop `/chat` de texto sigue siendo la referencia estable mientras se desbloquea la captura de audio. Phase 2A ya validó manualmente el camino Raspberry WAV -> `POST /chat/audio` -> STT backend OpenAI -> respuesta -> `espeak` local. Phase 2B validó inicialmente el loop automatizado en `client/main.py --mode voice` sobre Raspberry real. Después se ajustó el TTS a `espeak -v es -s 135 -g 8` para mejorar inteligibilidad en respuestas largas, y Phase 2B quedó revalidada post-ajuste en Raspberry real el 2026-05-30. Phase 3 web queda desbloqueada dentro del alcance documentado.

La dirección provisional es procesar STT en el backend. Esto deriva de la arquitectura MVP de Raspberry Pi como thin client y de la necesidad de mantener el cliente simple, no de una limitación ya demostrada de la Raspberry. STT local solo se descartará si una prueba concreta demuestra problemas de CPU, memoria, latencia, calidad o complejidad de setup.

## Componentes del Pipeline

### Input Audio

- **Fuente**: Micrófono USB Mini USB Microphone M-305, validado como `USB PnP Sound Device` en ALSA.
- **Captura**: Se realiza en el Raspberry Pi 3.
- **Formato inicial**: WAV básico grabado en Raspberry para minimizar procesamiento y facilitar depuración.
- **Precondición validada**: el dispositivo aparece en `arecord -l` como `USB PnP Sound Device` y puede grabar una muestra corta reproducible. El numero de tarjeta ALSA puede variar entre arranques o conexiones USB; usar siempre el `card` y `device` observados en `arecord -l`.
- **Validación mínima cumplida**: se grabo un WAV mono a 16 kHz con `arecord -D plughw:<CARD>,<DEVICE> -f S16_LE -r 16000 -c 1 ...` y se reprodujo localmente con `aplay`.

### Procesamiento

- **Conversión prevista**: De audio a texto (STT) en el backend.
- **Filtrado básico**: Eliminación de ruido simple si es necesario, priorizando estabilidad sobre calidad avanzada.
- **No objetivo inicial**: STT local complejo en Raspberry, wake word o modelos locales de audio.
- **Estado de decisión**: STT backend sigue siendo el default. OpenAI `gpt-4o-mini-transcribe` es el proveedor inicial para Semana 3; Vosk Spanish y `whisper.cpp` quedan como alternativas offline para un spike posterior si coste, privacidad u offline real pasan a ser requisitos.

### Backend

- **Tecnología MVP**: Python/FastAPI.
- **Funciones actuales**: Maneja la lógica conversacional y la integración con OpenAI mediante `/chat`.
- **Preparación semana 3**: la captura WAV ya quedo validada; `POST /chat/audio` está implementado y usa STT real en backend, validado manualmente desde Raspberry el 2026-05-30.
- **Comunicación actual**: Recibe mensajes HTTP/JSON del cliente y envía respuestas de texto para TTS local.

## Contrato de Subida de Audio

Esta sección define el contrato de subida de audio. El endpoint está implementado en `backend/audio_router.py` con STT backend real mediante OpenAI `gpt-4o-mini-transcribe` por defecto.

### Endpoint

- **Endpoint**: `POST /chat/audio`
- **Método HTTP**: `POST`
- **Estado**: implementado y validado manualmente en rama `feature/audio-upload-contract`.
- **STT**: OpenAI `gpt-4o-mini-transcribe` por defecto, configurable con `OPENAI_STT_MODEL`. El campo `transcript` devuelve texto reconocido; si el audio válido no produce texto, el backend responde `422`.
- **Propósito**: recibir un turno corto de audio capturado por la Raspberry, validar el formato WAV, reutilizar el flujo conversacional existente de `/chat`, y devolver una respuesta textual speakable para que la Raspberry la reproduzca con `espeak`.

### Request Recomendado

Usar `multipart/form-data` para evitar codificar WAV en base64 y mantener la subida simple de depurar con herramientas HTTP estándar.

Campos recomendados:

- `audio`: archivo WAV del turno capturado.
- `session_id`: identificador de sesión local ya usado por `/chat`.
- `device_id`: identificador estable y simple del cliente Raspberry, por ejemplo `tonto-pi`.
- `recorded_at`: timestamp ISO 8601 generado por el cliente si está disponible.
- `duration_ms`: duración aproximada de la captura.
- `sample_rate_hz`: frecuencia de muestreo declarada por el cliente.
- `channels`: número de canales.
- `language`: idioma esperado para STT; valor inicial recomendado `es`.

Metadatos mínimos para aprobar la primera implementación:

- `session_id`
- `audio`
- `duration_ms`
- `sample_rate_hz`
- `channels`

`device_id`, `recorded_at` y `language` son recomendados desde el inicio porque ayudan a depurar, pero pueden tener defaults explícitos en el backend durante el primer prototipo.

### Formato de Audio Inicial

Formato aceptado inicialmente:

- Contenedor: WAV.
- Codificación: PCM signed 16-bit little endian (`S16_LE`).
- Frecuencia: 16 kHz.
- Canales: mono.

Comando de captura compatible con la validación de Semana 3:

```bash
arecord -D plughw:<CARD>,<DEVICE> -f S16_LE -r 16000 -c 1 -d 10 ~/tonto-turn.wav
```

Obtener `<CARD>,<DEVICE>` de `arecord -l` antes de grabar. En validaciones reales el mismo microfono USB aparecio como `card 2` y despues como `card 1`.

No se aceptan inicialmente formatos comprimidos, streaming, múltiples archivos por request, ni audio estéreo salvo decisión explícita posterior.

### Límites Iniciales

Límites candidatos para mantener la demo rápida y evitar requests grandes:

- Duración mínima: 250 ms.
- Duración máxima: 10 segundos.
- Tamaño máximo del archivo: 512 KiB.
- Un solo turno de audio por request.
- El backend debe rechazar archivos vacíos o metadatos incompatibles con el WAV recibido.

Estos límites son deliberadamente conservadores. Una captura WAV mono PCM 16 kHz de 10 segundos pesa aproximadamente 320 KiB, por debajo del límite candidato.

### Respuesta Esperada

La respuesta debe seguir siendo texto speakable para el cliente Raspberry:

```json
{
  "session_id": "demo-session",
  "transcript": "texto reconocido",
  "response": "respuesta educativa para reproducir con espeak"
}
```

Campos mínimos:

- `session_id`: sesión usada para el turno.
- `transcript`: texto reconocido por STT.
- `response`: respuesta final del backend, lista para TTS local.

Campos opcionales de depuración para primeras pruebas:

- `request_id`
- `duration_ms`
- `stt_provider`
- `warnings`

La Raspberry no debe reproducir audio generado por el backend en esta etapa; debe seguir reproduciendo `response` localmente con `espeak`.

### Errores Básicos

Errores candidatos:

- `400 Bad Request`: falta `audio`, falta `session_id`, metadatos inválidos, archivo vacío, archivo demasiado pequeño para ser WAV, WAV mal formado o duración fuera de rango.
- `413 Payload Too Large`: archivo mayor que el límite aprobado.
- `415 Unsupported Media Type`: archivo RIFF/WAV reconocible pero no soportado, o WAV con codificación, canales, frecuencia o bits por muestra fuera del formato inicial.
- `422 Unprocessable Entity`: audio válido pero sin habla reconocible o transcripción vacía.
- `502 Bad Gateway`: fallo del proveedor STT cuando se integre.
- `504 Gateway Timeout`: timeout de STT o del flujo conversacional.

El body de error debe ser simple y depurable:

```json
{
  "error": "audio_too_long",
  "message": "Audio duration exceeds the 10 second limit."
}
```

### Relación con `POST /chat`

`POST /chat` permanece como contrato estable para texto manual y cliente web. El endpoint de audio no reemplaza `/chat`.

Flujo implementado en backend:

```text
Raspberry WAV -> POST /chat/audio -> STT backend -> texto -> lógica existente de /chat -> response -> espeak local
```

La intención es que `/chat/audio` sea una variante de entrada de chat por voz: transforma audio en texto y reutiliza la misma orquestación conversacional que ya sostiene `/chat`. Cualquier cambio al contrato de `/chat` queda fuera de esta decisión.

### Fase 3: Loop Web de Validacion

La Fase 3 de Semana 3 queda documentada en `specs/audio-pipeline-phase-3-web-loop.md` para ejecutarse despues de la revalidacion Raspberry de Fase 2B post-ajuste TTS, completada el 2026-05-30. Su objetivo es usar el cliente web como superficie interactiva para validar el mismo `POST /chat/audio` ya implementado:

```text
navegador -> captura de microfono -> WAV compatible -> POST /chat/audio -> transcript -> response -> UI web
```

Esta fase no cambia el contrato backend ni sustituye al cliente Raspberry como objetivo del producto fisico. Sirve para acelerar validacion, observar latencia y depurar STT desde navegador.

Restricciones iniciales de Fase 3:

- La web debe enviar WAV compatible con el formato actual: PCM 16-bit, 16 kHz, mono.
- No se debe subir `webm`, `ogg` u otro formato comprimido salvo que una decision posterior amplie el backend.
- No se debe introducir transcoding backend ni dependencias nuevas sin aprobacion explicita.
- Browser TTS queda fuera de alcance inicial; la respuesta puede mostrarse como texto en la UI.
- La evidencia debe quedar visible en UI/logs y promoverse despues a `docs/project-journal/week-03.md`.

### Fuera de Alcance

- STT local en Raspberry.
- Integrar Vosk, `whisper.cpp` u otro STT offline en esta fase.
- Wake word.
- Streaming de audio.
- Grabación continua.
- Browser TTS en Fase 3 inicial.
- Autenticación, usuarios o permisos.
- Persistencia de archivos de audio.
- Memoria avanzada.
- Respuestas de audio generadas por el backend.
- Cambios de arquitectura o separación en servicios.

### Criterios de Aceptación del Contrato

El contrato se considera implementado y validado en Raspberry real cuando:

- Mantiene `POST /chat` como contrato estable de texto.
- Permite a la Raspberry seguir como thin client: captura WAV, sube audio, reproduce `response` con `espeak`.
- Usa `multipart/form-data` con un solo WAV y metadatos mínimos claros.
- Acepta inicialmente WAV PCM S16_LE, 16 kHz, mono, alineado con la validación real en Raspberry.
- Define límites de duración y tamaño compatibles con la demo y con una captura de 10 segundos.
- Devuelve una respuesta textual speakable y, cuando exista STT, el transcript reconocido.
- Define errores suficientes para depurar fallos de formato, tamaño, duración, STT y timeouts.
- No introduce STT local, wake word, persistencia ni cambios de arquitectura.
- Puede probarse con un archivo WAV grabado con `arecord` o con tests automatizados.
- El endpoint está implementado y devuelve transcript real + response speakable.
- OpenAI `gpt-4o-mini-transcribe` es el proveedor inicial; `OPENAI_STT_MODEL` permite cambiar el modelo sin tocar el cliente Raspberry.
- `python-multipart` es la única dependencia nueva añadida.
- Tests automatizados cubren: upload válido, audio vacío, tamaño excedido, archivo demasiado pequeno para WAV, formato incorrecto, duración fuera de rango, transcript vacío, errores y timeouts de STT.
- Validación manual Phase 2A pasada el 2026-05-30: Raspberry `tonto-pi` grabó un WAV PCM 16-bit mono 16 kHz de 188K con `arecord -D plughw:1,0`; `POST /chat/audio` devolvió `HTTP_STATUS=200`, `TOTAL_TIME=5.395580`, transcript real `Hola tonto, explícame qué es una estrella.`, y una respuesta educativa reproducida localmente con `espeak`.
- Prueba negativa Phase 2A pasada: archivo de texto no audio devuelto como `HTTP_STATUS=400` con `File too small to be a valid WAV`.

### TTS (Text-to-Speech)

- **Generación**: Conversión de texto a audio localmente en la Raspberry Pi con `espeak`.
- **Salida**: Audio sintetizado simple, enfocado en claridad para niños.

### Output Audio

- **Dispositivo**: Altavoces conectados al Raspberry Pi 3 (ya validado).
- **Reproducción**: Directa desde el backend o cliente.

## Modos Offline

- **Posibilidad**: Vosk Spanish y `whisper.cpp` quedan como alternativas offline para evaluar en `experiment/local-stt-spike` si el coste API, privacidad u operación sin internet pasan a ser requisitos.
- **Limitaciones**: no se integran en Semana 3. Requieren validar precisión con voz real, latencia en el PC Windows y complejidad de setup/modelos antes de sustituir OpenAI STT.

## Responsabilidades

### Raspberry Pi (Thin Client)

- Captura de audio input.
- Reproducción de audio output.
- Comunicación básica con el backend.
- Mantener la entrada manual de texto como fallback durante el desarrollo de voz.

### Backend

- Lógica de conversación.
- Integración con OpenAI.
- Gestión de la conversación y estado.
- STT backend con OpenAI `gpt-4o-mini-transcribe` por defecto.

## Checklist de Preparación Semana 3

- Confirmar rama de trabajo `feature/week-3-audio-capture` antes de editar Semana 3.
- Ejecutar `.\scripts\setup-dev.ps1` si el entorno local no está preparado.
- Ejecutar `.\scripts\test.ps1 -Target all`.
- Ejecutar `.\scripts\build.ps1 -Target all`.
- Arrancar backend con `.\scripts\dev.ps1 -Service backend -AllowLan` para pruebas desde Raspberry.
- Confirmar que el cliente actual de texto sigue hablando respuestas con `espeak`.
- Conectar micrófono USB a Raspberry y comprobar `arecord -l`. Validado en Semana 3 con Mini USB Microphone M-305.
- Grabar una muestra WAV corta. Validado con dispositivo explicito:

```bash
arecord -D plughw:<CARD>,<DEVICE> -f S16_LE -r 16000 -c 1 -d 10 ~/tonto-mic-check.wav
```

- Si hace falta seleccionar el dispositivo explícitamente, usar los números de `arecord -l`:

```bash
arecord -D plughw:<CARD>,<DEVICE> -f S16_LE -r 16000 -c 1 -d 5 ~/tonto-mic-check.wav
```

- Reproducir la muestra localmente. Validado en Semana 3:

```bash
aplay ~/tonto-mic-check.wav
```

- Documentar cualquier bloqueo de hardware antes de implementar endpoints o dependencias. No hubo bloqueo de captura en la validacion de Semana 3.
- Si se considera STT local, documentar la prueba concreta y el motivo técnico antes de cambiar el default.
- Mantener `POST /chat` estable mientras `/chat/audio` añade entrada por voz.
- El endpoint `POST /chat/audio` está implementado y validado con STT real. El cliente Raspberry (Phase 2B) ya automatiza captura/subida: `client/main.py` soporta `--mode voice` con loop interactivo.
- [x] Automatizar captura/subida en cliente Raspberry: Phase 2B validada inicialmente en Raspberry real. `client/main.py` soporta `--mode voice` con loop interactivo (Enter inicia captura con `arecord`, sube WAV a `POST /chat/audio`, muestra transcript/response, reproduce con `espeak`). El modo texto `--mode text` preserva el comportamiento original. El tracking de la evidencia vive en `specs/audio-pipeline-phase-2b-validation-guide.md`. En esta validación, `espeak` sonó audible pero robótico y poco claro para la demo; los warnings ALSA/JACK no bloquearon el turno.
- [x] Revalidar Phase 2B post-ajuste TTS: repetida en Raspberry real con `TONTO_TTS_ARGS="-v es -s 135 -g 8"` siguiendo `specs/audio-pipeline-phase-2b-tts-revalidation.md`. La evidencia vive en `docs/project-journal/week-03.md`: respuesta larga audible, más pausada, palabras no atropelladas, suficientemente entendible para demo, fallback de texto y salida limpia. Phase 3 queda desbloqueada dentro del alcance documentado.
- [x] **Probar subida manual de WAV al backend** con `curl` desde la Raspberry, verificando que el backend responde con `session_id`, `transcript` y `response`. Validado el 2026-05-27 desde `tonto-pi` contra backend LAN `192.168.1.91:8000`.

  ```bash
  # 1. Grabar un turno corto desde la Raspberry
  arecord -D plughw:<CARD>,<DEVICE> -f S16_LE -r 16000 -c 1 -d 4 ~/tonto-turn.wav

  # 2. Enviar el WAV al backend y mostrar la respuesta
  curl -s -X POST http://<TONTO_BACKEND_IP>:8000/chat/audio \
    -F "audio=@/home/tonto-pi-user/tonto-turn.wav" \
    -F "session_id=demo-session" \
    -F "duration_ms=4000" \
    -F "sample_rate_hz=16000" \
    -F "channels=1" | python -m json.tool
  ```

  Resultado esperado tras la integración STT: `HTTP 200` con `{"session_id": "demo-session", "transcript": "<texto reconocido>", "response": "..."}`.

  Resultado validado con STT real el 2026-05-30:

  ```text
  HTTP_STATUS=200
  TOTAL_TIME=5.395580
  session_id=phase-2a-stt-validation
  transcript=Hola tonto, explícame qué es una estrella.
  response=¡Hola! Una estrella es una gran esfera de gas caliente en el espacio, principalmente compuesta de hidrógeno y helio. Produce luz y calor a través de reacciones nucleares en su interior. El Sol es una estrella que está muy cerca de nosotros y nos brinda luz y calor. ¡Esas luces que ves en el cielo de noche también son estrellas!
  ```

  La respuesta fue reproducida con `espeak -v es` y resultó audible y entendible para demo. La shell mostró warnings ALSA/JACK, pero no bloquearon la reproducción.

  Resultado validado antes de STT real:

  ```text
  HTTP_STATUS=200
  TOTAL_TIME=2.584502
  session_id=demo-session
  transcript=[audio input captured]
  response=He recibido tu audio. Todavia no puedo entenderlo, pero la subida y reproduccion ya funcionan. Pronto podre responder a lo que digas.
  ```

  Una segunda subida guardada como JSON tambien devolvio `HTTP_STATUS=200` con `TOTAL_TIME=1.472030`.

  Observaciones durante la validacion:

  - `espeak -v es` reprodujo correctamente la respuesta JSON y se escucho con claridad, pero la shell mostro warnings/errores ALSA/JACK sobre PCMs no disponibles y servidor JACK ausente. No bloquean la salida audible, aunque conviene limpiarlos para una demo mas clara.
  - La prueba negativa con un archivo de texto corto devuelve `400 File too small to be a valid WAV`; esta es la semantica decidida para archivos demasiado pequenos o mal formados.

  Esta prueba es manual y queda como evidencia de Phase 2A; la integración automatizada del cliente Raspberry se abordó después en Phase 2B.

## Riesgos Técnicos Principales

- **Recursos limitados del Raspberry Pi 3**: Posible latencia o inestabilidad en procesamiento de audio.
- **Micrófono USB validado inicialmente**: Phase 2A midió STT real con `TOTAL_TIME=5.395580`; Phase 2B automatizó el loop en el cliente y fue revalidada post-ajuste TTS en Raspberry real el 2026-05-30. Conviene seguir midiendo latencia en flujo interactivo durante la Fase 3 web y futuras demos.
- **Latencia**: Procesamiento en tiempo real puede ser desafiante con hardware limitado.
- **Estabilidad**: Priorizar simplicidad para evitar crashes o comportamientos impredecibles.

## Latencia Objetivo

- **Objetivo**: Menos de 2 segundos desde input hasta output en condiciones normales.
- **Métricas**: Medir tiempo de respuesta end-to-end en pruebas.

## Criterios de Aceptación

- El audio input se captura correctamente con micrófono USB.
- Una muestra WAV corta puede grabarse y reproducirse en Raspberry.
- La validación de captura registra dispositivo, comando usado, duración y notas de calidad.
- El contrato de STT backend queda decidido: OpenAI `gpt-4o-mini-transcribe` por defecto, sin nueva dependencia de SDK.
- Phase 2A queda validada con Raspberry real: captura WAV manual, subida a `POST /chat/audio`, transcript real, respuesta educativa y reproducción local con `espeak`.
- Phase 2B implementada y validada inicialmente: `client/main.py` con `--mode voice` automatiza captura, subida, transcript/response y TTS local. `--mode text` preserva el comportamiento original. Tests unitarios cubren send_message, send_audio, capture_audio y speak sin hardware real.
- Phase 2B post-ajuste TTS completada: el cliente usa por defecto `espeak -v es -s 135 -g 8` y fue revalidado en Raspberry real con respuesta larga audible, más pausada y suficientemente entendible para demo.
- Cualquier descarte de STT local queda respaldado por una prueba técnica, no por una suposición.
- El TTS genera audio claro y comprensible.
- El output audio se reproduce sin interrupciones.
- El loop de texto de semana 2 sigue funcionando como fallback.
- La latencia total se mide durante el primer prototipo de voz, sin optimizar prematuramente.
