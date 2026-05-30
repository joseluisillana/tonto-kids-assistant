# TONTO Kids Assistant - Especificaciones Base

## Visión General

Sistema educativo de IA física para niños.

El primer loop mínimo ya quedó validado en las semanas 1 y 2:

```text
texto manual -> backend -> OpenAI -> respuesta -> TTS local en Raspberry
```

El foco activo de la semana 3 es preparar y validar el primer pipeline de voz real:

```text
voz -> captura Raspberry -> STT backend -> /chat -> respuesta -> TTS local en Raspberry
```

La preparación de semana 3 mantuvo estable `/chat` y añadió `POST /chat/audio` como entrada de voz. La captura con micrófono USB ya fue validada en Raspberry con un WAV reproducible.

Fase 2B fue validada inicialmente en Raspberry real: el cliente Raspberry (`client/main.py`) automatiza captura y subida con `--mode voice`. Después de esa validación se ajustó el TTS a `espeak -v es -s 135 -g 8` para mejorar inteligibilidad en respuestas largas. El tracking operativo vive en `specs/audio-pipeline-phase-2b-validation-guide.md` y la revalidación post-ajuste vive en `specs/audio-pipeline-phase-2b-tts-revalidation.md`. Fase 3 queda documentada, pero bloqueada hasta repetir y aprobar Phase 2B en Raspberry real con el TTS ajustado.

## Arquitectura

- **Cliente físico**: Raspberry Pi 3 (Python)
- **Cliente web de validación**: React + TypeScript + Vite
- **Backend**: Windows local inicialmente, Python/FastAPI para el MVP
- **Comunicación**: APIs HTTP

## Componentes Principales

1. **Entrada manual de texto**: modo validado y fallback de desarrollo.
2. **TTS**: Text-to-Speech local con `espeak` en Raspberry.
3. **Memoria de sesión**: historial corto en memoria de proceso.
4. **Personalidad educativa**: respuestas breves, claras y adaptadas a niños.
5. **Cliente web de validación**: interfaz mínima para probar el backend desde navegador; Fase 3 planifica validacion de voz contra `POST /chat/audio`.
6. **Voz real**: foco activo de semana 3, con micrófono USB y captura WAV simple ya validados como base de la siguiente iteración.
7. **Estados visuales e integración Arduino**: expansión futura, no parte del arranque de semana 3.

## APIs Base

- POST /chat: Procesar una interacción conversacional con `session_id` y `message`
- POST /chat/audio: Procesar un turno corto de audio WAV con STT backend, devolver `transcript` y `response`

Durante semana 3, `/chat` sigue siendo el contrato estable. Tras validar la captura WAV en Raspberry, `specs/audio-pipeline.md` documentó `POST /chat/audio` como contrato mínimo candidato. Ahora el endpoint está implementado en `backend/audio_router.py` (rama `feature/audio-upload-contract`) con STT real en backend mediante OpenAI `gpt-4o-mini-transcribe` por defecto, configurable con `OPENAI_STT_MODEL`. La subida manual de un WAV desde Raspberry con `curl` quedó validada el 2026-05-30 contra el backend LAN con transcripción real, respuesta educativa y reproducción local con `espeak`. El endpoint no reemplaza `/chat`.

Fase 3 queda planificada en `specs/audio-pipeline-phase-3-web-loop.md` y `specs/web-validation-client.md` para despues de la revalidacion Raspberry de Fase 2B post-ajuste TTS. La web debe usar el contrato existente, enviar WAV compatible y registrar evidencia visible; no debe añadir un endpoint propio ni requerir cambios de proveedor STT.

## Fuera de Alcance del Arranque de Semana 3

- Wake word.
- STT local complejo en Raspberry.
- Modelos locales de audio.
- Integración offline con Vosk, `whisper.cpp` u otro motor local sin spike técnico previo.
- Nuevas dependencias sin decisión explícita.
- Arduino/LEDs.
- Persistencia.
- Autenticación.
- Multiusuario.
- Memoria avanzada.

## Checklist de Desbloqueo de Voz

- Micrófono USB conectado a la Raspberry Pi. Validado en Semana 3.
- Dispositivo visible con `arecord -l`. Validado como `USB PnP Sound Device`; el numero `card` puede variar y debe leerse antes de grabar.
- Grabación WAV corta validada con `arecord -D plughw:<CARD>,<DEVICE> -f S16_LE -r 16000 -c 1 -d 10 ~/tonto-mic-check.wav`.
- Reproducción local validada con `aplay ~/tonto-mic-check.wav`.
- Backend arrancado con `.\scripts\dev.ps1 -Service backend -AllowLan`.
- Cliente Raspberry apuntando a `TONTO_BACKEND_URL`.
- Subida manual a `POST /chat/audio` validada desde Raspberry con `curl` y respuesta `HTTP 200`.
- STT backend validado manualmente desde Raspberry real el 2026-05-30: transcript `Hola tonto, explícame qué es una estrella.`, `TOTAL_TIME=5.395580`, respuesta educativa y TTS local audible.
- Phase 2B automatizada fue validada inicialmente en Raspberry real, pero queda pendiente repetir la validacion tras el ajuste `TONTO_TTS_ARGS="-v es -s 135 -g 8"` antes de pasar a Fase 3.
- Loop de texto de semana 2 confirmado antes de tocar audio input.

## Requisitos No Funcionales

- Simplicidad y claridad
- Velocidad de iteración
- Reproducibilidad para demo
- Documentación viva en el repositorio
