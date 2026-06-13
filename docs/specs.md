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
7. **Semana 4 demo stability**: kickoff documental y fases para convertir el loop de voz validado en una demo repetible antes de añadir comportamiento nuevo.
8. **Estados visuales e integración Arduino**: expansión futura fuera del MVP de 6 semanas; Semana 4 usa primero indicadores no físicos.

## APIs Base

- POST /chat: Procesar una interacción conversacional con `session_id` y `message`
- POST /chat/audio: Procesar un turno corto de audio WAV con STT backend, devolver `transcript` y `response`

Durante semana 3, `/chat` sigue siendo el contrato estable. Tras validar la captura WAV en Raspberry, `specs/audio-pipeline.md` documentó `POST /chat/audio` como contrato mínimo candidato. Ahora el endpoint está implementado en `backend/audio_router.py` (rama `feature/audio-upload-contract`) con STT real en backend mediante OpenAI `gpt-4o-mini-transcribe` por defecto, configurable con `OPENAI_STT_MODEL`. La subida manual de un WAV desde Raspberry con `curl` quedó validada el 2026-05-30 contra el backend LAN con transcripción real, respuesta educativa y reproducción local con `espeak`. El endpoint no reemplaza `/chat`.

Fase 3 queda cerrada como validada en `specs/audio-pipeline-phase-3-web-loop.md`, `specs/web-validation-client.md` y `specs/audio-pipeline-phase-3-browser-manual-validation.md`. La web usa el contrato existente, captura desde microfono, envia WAV compatible, muestra transcript/response, reproduce la response de forma audible desde el navegador y registra evidencia visible; no añade endpoint propio, no cambia proveedor STT, no introduce dependencias ni expone subida manual de WAV como flujo de producto/demo. Como mejora posterior de UX web, las respuestas recibidas por el chat de texto `/chat` tambien se reproducen con Web Speech API cuando esta disponible, degradando a texto visible si speech falla o no esta soportado.

## Semana 4 - Estabilidad de demo y decisión de estados físicos (completada)

La spec de Semana 4 vive en `specs/week-04-demo-stability.md`, con plan emparejado en `docs/plans/week-04-demo-stability.md`.

Semana 4 empieza como una preparación documental para agentes IA y después avanza por fases:

1. ~~Kickoff documental~~ — completado 2026-06-02.
2. **Baseline reproducible de la demo actual** — completado 2026-06-05. 3 voice turns en Raspberry real validados, memoria corta confirmada, `/chat` y `/chat/audio` funcionando.
3. **Resiliencia y errores observados** — completado 2026-06-05. Timeouts de cliente ajustados y 48/48 tests pasados.
4. **Calibración conversacional con la memoria corta en proceso ya existente** — completado 2026-06-07. Prompt calibrado, 49/49 tests pasados y 5 voice turns relacionados en Raspberry real validados.
5. **Decisión explícita sobre estados físicos mínimos e indicadores no físicos de tiempo/escucha** — decisión humana registrada 2026-06-07: Arduino/LEDs quedan fuera del MVP de 6 semanas; indicadores no físicos aprobados primero. Implementación completada y validada en hardware real 2026-06-07: Raspberry #27 cerrada, web #23/#25 cerradas.
6. Closeout con evidencia.

Specs y planes de Phase 4 preparados antes de código:

- `specs/raspberry-listening-indicator.md` + `docs/plans/raspberry-listening-indicator.md`
- `specs/web-listening-indicator.md` + `docs/plans/web-listening-indicator.md`

La spec web registra la decisión humana del 2026-06-07 para el follow-up #23 (cerrada): la captura web debe hacer auto-stop al llegar al límite configurado, mostrar un aviso simple de límite alcanzado y mantener el envío manual con `Enviar voz`. Issue #25 reparó la superficie principal del cliente web para mostrar un contador visible `00:SS / 00:10` y una barra de progreso mientras TONTO escucha. La validación manual humana confirmó que el comportamiento esperado queda cubierto sin cambiar el contrato `/chat/audio` ni añadir dependencias. Ambas issues (#23 y #25) quedan cerradas.

El indicador de escucha Raspberry fue implementado en `client/main.py` (funciones `_show_listening_indicator`, `_format_listening_progress`, `_stop_listening_indicator`) y validado en hardware real el 2026-06-07: 2/2 turnos de voz pasados, indicador visible `Listening: X/6s`, transición a `Uploading...` clara, transcript/response/espeak funcionando. Issue #27 cerrada.

La memoria de Semana 4 no implica persistencia, perfiles, memoria vectorial ni multiusuario. La decisión de Fase 4 difiere Arduino/LEDs fuera del MVP de 6 semanas y aprueba implementar primero indicadores no físicos de tiempo/escucha. Si Arduino/LEDs se retoman en una versión futura de TONTO, deberán tener una spec y plan separados antes de código.

## Semana 5 - Estabilidad y experiencia demo (completada)

La spec de Semana 5 vive en `specs/week-05-demo-stability.md`, con plan emparejado en `docs/plans/week-05-demo-stability.md`.

Semana 5 convirtió el loop validado en una demo repetible y fácil de operar:

1. **Kickoff documental** — completado 2026-06-08.
2. **Runbook de demo y scripts de arranque** — completado 2026-06-08. Script bash con health check y runbook completo.
3. **Pulido de UX conversacional** — completado 2026-06-11. Prompt ajustado para respuesta directa, ejemplo simple cuando aporte claridad, factual-care, menos formato/listas y mejor manejo natural de saludos/despedidas; `MAX_OUTPUT_TOKENS` ajustado a `300` (#59); validado con 6/6 preguntas desde Raspberry real contra backend LAN.
4. **Resiliencia ante errores** — completado 2026-06-13. Mensajes operador-amigables, ALSA/JACK suprimidos, recuperación limpia. Validado con 4/4 turnos de voz en Raspberry.
5. **Ensayo de demo** — completado 2026-06-13. 6/6 turnos OpenAI + 1/1 smoke DevExpert en Raspberry real.
6. **Closeout con evidencia** — completado 2026-06-13.

GitHub tracking: issue #33 (parent), issues #34-#38 (phases).

Semana 5 also includes an extra workflow item, tracked by issue #43:

- **Agent Capability Pack** — implemented and merged. Portable repo-owned Markdown and PowerShell helper scripts for backend lifecycle and Raspberry SSH operations. It added `scripts/agent-backend.ps1` and `scripts/agent-raspberry.ps1`; real Raspberry preflight passed with backend health. Spec: `specs/week-05-agent-capability-pack.md`; plan: `docs/plans/week-05-agent-capability-pack.md`.

Semana 5 also includes a planned extra MVP line for AI Expert course alignment:

- **Inference Providers / DevExpert Inference** — implemented through Phase 3, tracked by parent issue #48 and phase issues #50, #51, #49, #52, with future backlog #53. Phases 0-3 are complete: planning/provider specs, chat provider selection, STT provider selection, and runbook/setup documentation for OpenAI and DevExpert while keeping Raspberry and web clients provider-agnostic. OpenAI keeps using the Responses API for text, DevExpert uses its documented OpenAI-compatible Chat Completions endpoint, and both providers must remain covered by tests when inference behavior changes. General spec: `specs/inference-providers.md`; provider specs: `specs/inference-provider-openai.md`, `specs/inference-provider-devexpert.md`; plan: `docs/plans/inference-providers.md`; repo-local skill: `.agents/skills/devexpert-inference/SKILL.md`.

## Fuera de Alcance de Semana 5

- Wake word.
- STT local complejo en Raspberry.
- Modelos locales de audio.
- Integración offline con Vosk, `whisper.cpp` u otro motor local sin spike técnico previo.
- Nuevas dependencias sin decisión explícita.
- Arduino/LEDs dentro del MVP de 6 semanas; quedan diferidos a una versión futura de TONTO.
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

## Workflow de Desarrollo Asistido por IA

- `specs/parallel-agent-workflow.md`: define el patrón de trabajo por unidad coherente, rama corta, PR pequeña y worktree dedicado cuando hay agentes o tareas en paralelo.
- `docs/plans/parallel-agent-workflow.md`: plan de implementación documental de ese workflow.
