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

La preparación de semana 3 no cambia todavía las interfaces públicas. La captura con micrófono USB ya fue validada en Raspberry con un WAV reproducible; antes de implementar nuevos endpoints o dependencias, hay que decidir el contrato mínimo de subida de audio.

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
5. **Cliente web de validación**: interfaz mínima para probar el backend desde navegador.
6. **Voz real**: foco activo de semana 3, con micrófono USB y captura WAV simple ya validados como base de la siguiente iteración.
7. **Estados visuales e integración Arduino**: expansión futura, no parte del arranque de semana 3.

## APIs Base

- POST /chat: Procesar una interacción conversacional con `session_id` y `message`

Durante la preparación de semana 3, `/chat` sigue siendo el contrato estable. Tras validar la captura WAV en Raspberry, `specs/audio-pipeline.md` documentó `POST /chat/audio` como contrato mínimo candidato. Ahora el endpoint está implementado en `backend/audio_router.py` (rama `feature/audio-upload-contract`) sin STT real: usa un transcript fijo `[audio input captured]` como placeholder. El endpoint no reemplaza `/chat`.

## Fuera de Alcance del Arranque de Semana 3

- Wake word.
- STT local complejo en Raspberry.
- Modelos locales de audio.
- Nuevas dependencias sin decisión explícita.
- Nuevos endpoints antes de decidir el contrato mínimo de audio.
- Arduino/LEDs.
- Persistencia.
- Autenticación.
- Multiusuario.
- Memoria avanzada.

## Checklist de Desbloqueo de Voz

- Micrófono USB conectado a la Raspberry Pi. Validado en Semana 3.
- Dispositivo visible con `arecord -l`. Validado como `USB PnP Sound Device`, `card 2`, `device 0`.
- Grabación WAV corta validada con `arecord -D plughw:2,0 -f S16_LE -r 16000 -c 1 -d 10 ~/tonto-mic-check.wav`.
- Reproducción local validada con `aplay ~/tonto-mic-check.wav`.
- Backend arrancado con `.\scripts\dev.ps1 -Service backend -AllowLan`.
- Cliente Raspberry apuntando a `TONTO_BACKEND_URL`.
- Loop de texto de semana 2 confirmado antes de tocar audio input.

## Requisitos No Funcionales

- Simplicidad y claridad
- Velocidad de iteración
- Reproducibilidad para demo
- Documentación viva en el repositorio
