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
- **Precondición validada**: el dispositivo aparece en `arecord -l` como `card 2`, `device 0`, y puede grabar una muestra corta reproducible.
- **Validación mínima cumplida**: se grabo un WAV mono de 10 segundos a 16 kHz con `arecord -D plughw:2,0 -f S16_LE -r 16000 -c 1 -d 10 ~/tonto-mic-check.wav` y se reprodujo localmente con `aplay`.

### Procesamiento

- **Conversión prevista**: De audio a texto (STT) en el backend.
- **Filtrado básico**: Eliminación de ruido simple si es necesario, priorizando estabilidad sobre calidad avanzada.
- **No objetivo inicial**: STT local complejo en Raspberry, wake word o modelos locales de audio.
- **Estado de decisión**: STT backend es el default provisional; proveedor, endpoint y formato de audio siguen pendientes.

### Backend

- **Tecnología MVP**: Python/FastAPI.
- **Funciones actuales**: Maneja la lógica conversacional y la integración con OpenAI mediante `/chat`.
- **Preparación semana 3**: la captura WAV ya quedo validada; no se añade endpoint de audio hasta decidir el contrato mínimo.
- **Comunicación actual**: Recibe mensajes HTTP/JSON del cliente y envía respuestas de texto para TTS local.

## Contrato Mínimo Candidato de Subida de Audio

Esta sección define el contrato candidato para la siguiente iteración de voz. No implementa todavía un endpoint real ni activa STT; sirve para aprobar el contrato antes de escribir código.

### Endpoint Candidato

- **Endpoint candidato**: `POST /chat/audio`
- **Método HTTP**: `POST`
- **Estado**: candidato documentado, no implementado.
- **Propósito**: recibir un turno corto de audio capturado por la Raspberry, transcribirlo en el backend cuando se añada STT, reutilizar el flujo conversacional existente de `/chat`, y devolver una respuesta textual speakable para que la Raspberry la reproduzca con `espeak`.

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
arecord -D plughw:2,0 -f S16_LE -r 16000 -c 1 -d 10 ~/tonto-turn.wav
```

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

- `400 Bad Request`: falta `audio`, falta `session_id`, metadatos inválidos, WAV mal formado o duración fuera de rango.
- `413 Payload Too Large`: archivo mayor que el límite aprobado.
- `415 Unsupported Media Type`: formato distinto de WAV PCM mono 16 kHz inicial.
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

- Implementar el endpoint en esta iteración de documentación.
- Elegir o integrar proveedor STT.
- Añadir dependencias.
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

Antes de implementar el endpoint, el contrato se considera aprobado si:

- Mantiene `POST /chat` como contrato estable de texto.
- Permite a la Raspberry seguir como thin client: captura WAV, sube audio, reproduce `response` con `espeak`.
- Usa `multipart/form-data` con un solo WAV y metadatos mínimos claros.
- Acepta inicialmente WAV PCM S16_LE, 16 kHz, mono, alineado con la validación real en Raspberry.
- Define límites de duración y tamaño compatibles con la demo y con una captura de 10 segundos.
- Devuelve una respuesta textual speakable y, cuando exista STT, el transcript reconocido.
- Define errores suficientes para depurar fallos de formato, tamaño, duración, STT y timeouts.
- No introduce STT, wake word, dependencias, persistencia ni cambios de arquitectura.
- Puede probarse primero con un archivo WAV grabado con `arecord` antes de integrarlo en el loop interactivo del cliente.

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
arecord -D plughw:2,0 -f S16_LE -r 16000 -c 1 -d 10 ~/tonto-mic-check.wav
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
