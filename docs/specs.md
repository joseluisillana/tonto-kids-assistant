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

Fase 2B fue validada inicialmente en Raspberry real: el cliente Raspberry (`client/main.py`) automatiza captura y subida con `--mode voice`. Después de esa validación se ajustó el TTS a `espeak -v es -s 135 -g 8` para mejorar inteligibilidad en respuestas largas. La revalidación post-ajuste pasó en Raspberry real el 2026-05-30 siguiendo `specs/audio-pipeline-phase-2b-tts-revalidation.md`: respuesta larga audible, más pausada, no atropellada y suficientemente entendible para demo. Fase 3 quedó implementada y validada el 2026-06-01 con captura desde microfono web, transcript visible, respuesta textual visible y respuesta audible desde navegador.

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
5. **Cliente web de validación**: interfaz mínima para probar el backend desde navegador; Fase 3 valida voz contra `POST /chat/audio` con captura de microfono, transcript, respuesta textual y speech output del navegador. El chat de texto web mantiene `/chat` como contrato estable y reproduce tambien la respuesta con speech nativo cuando el navegador lo soporta.
6. **Voz real**: semana 3 completada con micrófono USB/Raspberry, cliente Raspberry automatizado y loop web de voz validado.
7. **Estados visuales e integración Arduino**: expansión futura, no parte del arranque de semana 3.

## APIs Base

- POST /chat: Procesar una interacción conversacional con `session_id` y `message`
- POST /chat/audio: Procesar un turno corto de audio WAV con STT backend, devolver `transcript` y `response`

Durante semana 3, `/chat` sigue siendo el contrato estable. Tras validar la captura WAV en Raspberry, `specs/audio-pipeline.md` documentó `POST /chat/audio` como contrato mínimo candidato. Ahora el endpoint está implementado en `backend/audio_router.py` (rama `feature/audio-upload-contract`) con STT real en backend mediante OpenAI `gpt-4o-mini-transcribe` por defecto, configurable con `OPENAI_STT_MODEL`. La subida manual de un WAV desde Raspberry con `curl` quedó validada el 2026-05-30 contra el backend LAN con transcripción real, respuesta educativa y reproducción local con `espeak`. El endpoint no reemplaza `/chat`.

Fase 3 queda cerrada como validada en `specs/audio-pipeline-phase-3-web-loop.md`, `specs/web-validation-client.md` y `specs/audio-pipeline-phase-3-browser-manual-validation.md`. La web usa el contrato existente, captura desde microfono, envia WAV compatible, muestra transcript/response, reproduce la response de forma audible desde el navegador y registra evidencia visible; no añade endpoint propio, no cambia proveedor STT, no introduce dependencias ni expone subida manual de WAV como flujo de producto/demo. Como mejora posterior de UX web, las respuestas recibidas por el chat de texto `/chat` tambien se reproducen con Web Speech API cuando esta disponible, degradando a texto visible si speech falla o no esta soportado.

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
- Phase 2B automatizada fue validada inicialmente en Raspberry real y revalidada tras el ajuste `TONTO_TTS_ARGS="-v es -s 135 -g 8"` el 2026-05-30; esa revalidacion desbloqueó una Fase 3 que ya quedó validada dentro de su alcance documentado.
- Phase 3 web validada el 2026-06-01 contra backend real; el fallo inicial `422 Audio did not contain recognizable speech` se resolvió seleccionando el microfono correcto en los ajustes del navegador.
- Loop de texto de semana 2 confirmado antes de tocar audio input.

## Requisitos No Funcionales

- Simplicidad y claridad
- Velocidad de iteración
- Reproducibilidad para demo
- Documentación viva en el repositorio
