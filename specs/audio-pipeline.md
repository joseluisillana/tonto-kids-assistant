# Pipeline de Audio de TONTO MVP

## Introducción

Este documento describe el pipeline de audio para la versión MVP de TONTO, un asistente para niños. El enfoque está en simplicidad y estabilidad, utilizando un Raspberry Pi 3 como thin client. El audio output ya está validado, y la captura inicial con micrófono USB quedó validada en Raspberry durante Semana 3.

Semana 3 empieza con una fase de preparación: validar hardware de entrada y dejar el repositorio listo para implementar voz sin cambiar todavía contratos públicos ni añadir dependencias. El loop `/chat` de texto sigue siendo la referencia estable mientras se desbloquea la captura de audio.

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
- **Estado de decisión**: STT backend es el default provisional. El contrato mínimo `POST /chat/audio` y el formato WAV PCM mono 16 kHz ya están definidos y validados manualmente desde Raspberry; el proveedor STT sigue pendiente.

### Backend

- **Tecnología MVP**: Python/FastAPI.
- **Funciones actuales**: Maneja la lógica conversacional y la integración con OpenAI mediante `/chat`.
- **Preparación semana 3**: la captura WAV ya quedo validada; no se añade endpoint de audio hasta decidir el contrato mínimo.
- **Comunicación actual**: Recibe mensajes HTTP/JSON del cliente y envía respuestas de texto para TTS local.

## Contrato de Subida de Audio

Esta sección define el contrato de subida de audio. El endpoint está implementado en `backend/audio_router.py` sin STT real: usa un transcript fijo `[audio input captured]` y una respuesta temporal fija en espanol hasta que se integre un proveedor STT.

### Endpoint

- **Endpoint**: `POST /chat/audio`
- **Método HTTP**: `POST`
- **Estado**: implementado en rama `feature/audio-upload-contract`.
- **STT**: placeholder. El campo `transcript` devuelve `"[audio input captured]"` hasta que se decida e integre un proveedor STT. Mientras el transcript sea placeholder, el backend devuelve una respuesta fija en espanol y no envia ese placeholder a OpenAI como si fuera contenido del usuario.
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

`POST /chat` permanece como contrato estable para texto manual y cliente web. El endpoint candidato de audio no reemplaza `/chat`.

Flujo previsto cuando se implemente:

```text
Raspberry WAV -> POST /chat/audio -> STT backend -> texto -> lógica existente de /chat -> response -> espeak local
```

La intención es que `/chat/audio` sea una variante de entrada de chat por voz: transforma audio en texto y reutiliza la misma orquestación conversacional que ya sostiene `/chat`. Cualquier cambio al contrato de `/chat` queda fuera de esta decisión.

### Fuera de Alcance

- Elegir o integrar proveedor STT.
- STT real (el endpoint usa un placeholder `[audio input captured]`).
- STT local en Raspberry.
- Wake word.
- Streaming de audio.
- Grabación continua.
- Autenticación, usuarios o permisos.
- Persistencia de archivos de audio.
- Memoria avanzada.
- Respuestas de audio generadas por el backend.
- Cambios de arquitectura o separación en servicios.

### Criterios de Aceptación del Contrato

El contrato se considera implementado cuando:

- Mantiene `POST /chat` como contrato estable de texto.
- Permite a la Raspberry seguir como thin client: captura WAV, sube audio, reproduce `response` con `espeak`.
- Usa `multipart/form-data` con un solo WAV y metadatos mínimos claros.
- Acepta inicialmente WAV PCM S16_LE, 16 kHz, mono, alineado con la validación real en Raspberry.
- Define límites de duración y tamaño compatibles con la demo y con una captura de 10 segundos.
- Devuelve una respuesta textual speakable y, cuando exista STT, el transcript reconocido.
- Define errores suficientes para depurar fallos de formato, tamaño, duración, STT y timeouts.
- No introduce STT real, wake word, persistencia ni cambios de arquitectura.
- Puede probarse con un archivo WAV grabado con `arecord` o con tests automatizados.
- El endpoint está implementado y devuelve transcript + response speakable.
- El transcript es un placeholder fijo `[audio input captured]` hasta que se integre STT; mientras tanto, la respuesta es un fallback fijo en espanol para evitar respuestas aleatorias en ingles.
- `python-multipart` es la única dependencia nueva añadida.
- Tests automatizados cubren: upload válido, audio vacío, tamaño excedido, archivo demasiado pequeno para WAV, formato incorrecto, duración fuera de rango.

### TTS (Text-to-Speech)

- **Generación**: Conversión de texto a audio localmente en la Raspberry Pi con `espeak`.
- **Salida**: Audio sintetizado simple, enfocado en claridad para niños.

### Output Audio

- **Dispositivo**: Altavoces conectados al Raspberry Pi 3 (ya validado).
- **Reproducción**: Directa desde el backend o cliente.

## Modos Offline

- **Posibilidad**: Soporte básico para modos offline, procesando audio localmente en el Raspberry Pi si es factible.
- **Limitaciones**: Dependiente de recursos disponibles; no priorizado en MVP.

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
- STT backend como default provisional cuando se decida el contrato de audio.

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
- Mantener `POST /chat` estable hasta decidir el contrato mínimo de audio.
- El endpoint `POST /chat/audio` está implementado pero el cliente Raspberry no ha sido modificado: la captura y subida de audio no están automatizadas.
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

  Resultado esperado: `HTTP 200` con `{"session_id": "demo-session", "transcript": "[audio input captured]", "response": "..."}`.

  Resultado validado:

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

  Esta prueba es manual y no sustituye la integración automatizada en el cliente Raspberry, que queda como trabajo pendiente de la Fase 2.

## Riesgos Técnicos Principales

- **Recursos limitados del Raspberry Pi 3**: Posible latencia o inestabilidad en procesamiento de audio.
- **Micrófono USB validado inicialmente**: queda pendiente medir calidad suficiente para STT real y latencia end-to-end.
- **Latencia**: Procesamiento en tiempo real puede ser desafiante con hardware limitado.
- **Estabilidad**: Priorizar simplicidad para evitar crashes o comportamientos impredecibles.

## Latencia Objetivo

- **Objetivo**: Menos de 2 segundos desde input hasta output en condiciones normales.
- **Métricas**: Medir tiempo de respuesta end-to-end en pruebas.

## Criterios de Aceptación

- El audio input se captura correctamente con micrófono USB.
- Una muestra WAV corta puede grabarse y reproducirse en Raspberry.
- La validación de captura registra dispositivo, comando usado, duración y notas de calidad.
- El contrato de STT backend queda decidido antes de añadir dependencias o endpoints.
- Cualquier descarte de STT local queda respaldado por una prueba técnica, no por una suposición.
- El TTS genera audio claro y comprensible.
- El output audio se reproduce sin interrupciones.
- El loop de texto de semana 2 sigue funcionando como fallback.
- La latencia total se mide durante el primer prototipo de voz, sin optimizar prematuramente.
