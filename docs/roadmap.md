# Roadmap del MVP - 6 semanas

Este roadmap define el plan operativo para construir el MVP de TONTO Kids Assistant en 6 semanas.

El objetivo NO es construir un robot perfecto ni una plataforma enterprise.
El objetivo es validar una experiencia educativa conversacional funcional usando hardware accesible, una arquitectura simple y desarrollo asistido por IA.

La prioridad principal del proyecto es:

- conversación funcional,
- estabilidad básica,
- demos reproducibles,
- y velocidad de iteración.

---

# Semana 1 - Infraestructura y validación técnica base

## Objetivo

Preparar el entorno completo de desarrollo y validar la arquitectura mínima del sistema.

## Entregables

- Raspberry Pi 3 operativa.
- SSH y desarrollo remoto funcionando.
- VSCode Remote SSH configurado.
- Audio output validado.
- TTS local funcionando (`espeak`).
- Repositorio GitHub inicializado.
- README y documentación fundacional creados.
- Arquitectura MVP definida.
- Workflow documental repo/Codex/OpenCode/NotebookLM definido.

## Prioridades

1. Validar la Raspberry como thin client.
2. Garantizar un flujo de desarrollo rápido y estable.
3. Crear estructura mínima del proyecto.
4. Evitar cualquier complejidad innecesaria.

## Riesgos

- Problemas de audio en Raspberry.
- Configuración remota inestable.
- Pérdida de foco intentando implementar demasiadas cosas.

---

# Semana 2 - Backend conversacional mínimo

## Objetivo

Construir el primer loop conversacional funcional extremo a extremo.

## Entregables

- Backend mínimo ejecutándose localmente.
- Endpoint HTTP simple (`/chat` placeholder inicial).
- Integración básica con OpenAI.
- Cliente Raspberry capaz de enviar texto y recibir respuestas.
- Scaffold del cliente web de validación para CI/despliegue paralelo.
- TTS reproduciendo respuestas generadas por IA.

## Prioridades

1. Validar el flujo completo:
   usuario → backend → OpenAI → Raspberry → TTS.
2. Mantener la arquitectura extremadamente simple.
3. Medir tiempos de respuesta básicos.
4. Permitir pruebas rápidas desde navegador sin depender siempre de la Raspberry.

## Riesgos

- Latencia excesiva.
- Complejidad innecesaria en backend.
- Intentar implementar memoria avanzada demasiado pronto.

---

## Estado de cierre

Las semanas 1 y 2 quedan cerradas con validación en hardware y en el loop conversacional mínimo.

Lo que sigue en este roadmap es ya trabajo de semanas posteriores o ajuste futuro, no pendiente del arranque inicial.

---

# Fase extra - Mejora del workflow NotebookLM

## Objetivo

Reducir fricción en la actualización de fuentes de NotebookLM tras validar el uso real del flujo documental.

## Motivo

La exportación inicial generaba múltiples Markdown individuales, pero NotebookLM puede duplicar fuentes al reimportarlas en vez de sobrescribirlas de forma ágil.

## Entregables

- Documento combinado generado en `exports/notebooklm/NOTEBOOKLM_COMBINED.md`.
- Ficheros individuales e `INDEX.md` conservados para inspección y uso granular.
- Documentación actualizada para recomendar el combinado como fuente principal.

## Estado

Feature añadida como mejora no planificada del workflow documental, derivada del uso práctico de NotebookLM.

---

# Semana 3 - Pipeline de voz real

## Objetivo

Introducir input de voz real en el sistema, empezando por captura real en Raspberry, STT backend y superficies de validacion que reduzcan riesgo antes del loop fisico automatizado.

## Fase 1 — Captura y contrato de audio (completada)

### Entregables

- [x] Micrófono USB integrado y validado.
- [x] Captura básica de audio en Raspberry (WAV PCM 16 kHz mono reproducible) — validada manualmente con comandos `arecord`, no automatizada en cliente.
- [x] Contrato `POST /chat/audio` documentado en `specs/audio-pipeline.md`.
- [x] Endpoint `POST /chat/audio` implementado con validación WAV, límites de tamaño/duración, y conexión al flujo conversacional existente.
- [x] Tests automatizados del endpoint de audio.
- [x] Prueba manual de subida WAV con `curl` desde la Raspberry validada el 2026-05-27 contra backend LAN (`HTTP 200`, transcript placeholder y `response` devuelta).

### Nota

El endpoint empezó con un transcript fijo `[audio input captured]` como placeholder de STT para cerrar el contrato HTTP. Esa validación manual quedó cerrada y la respuesta se reprodujo con `espeak`, aunque con salida ruidosa de ALSA/JACK en la shell. Quedan observaciones pendientes: limpieza de warnings ALSA/JACK para demo y confirmar siempre el `card/device` de ALSA con `arecord -l`.

## Fase 2 — Integración STT + Client Automation (completada)

### Entregables

- [x] Elegir proveedor STT: OpenAI `gpt-4o-mini-transcribe` como default inicial; Vosk Spanish y `whisper.cpp` quedan como alternativas offline para spike posterior.
- [x] Integrar STT en el backend con `OPENAI_STT_MODEL` opcional y sin SDK nuevo.
- [x] Pipeline de voz extremo a extremo manual: Raspberry captura → backend STT → respuesta → TTS.
- [x] Fase 2B: loop interactivo con captura desde el cliente Raspberry.
- [x] Revalidación Fase 2B post-ajuste TTS antes de pasar a Fase 3.

### Evidencia Phase 2A

Validado el 2026-05-30 desde Raspberry real `tonto-pi` contra backend LAN `192.168.1.91:8000`: captura WAV manual PCM 16-bit mono 16 kHz, `POST /chat/audio` con `HTTP_STATUS=200`, `TOTAL_TIME=5.395580`, transcript real `Hola tonto, explícame qué es una estrella.`, respuesta educativa, y reproducción local con `espeak`. La prueba negativa con archivo de texto devolvió `HTTP_STATUS=400`.

### Evidencia Phase 2B

Validado el 2026-05-30 desde Raspberry real `tonto-pi` contra backend LAN `192.168.1.91:8000`:

- Plan de tracking de la validación: `specs/audio-pipeline-phase-2b-validation-guide.md`.

- `client/main.py` actualizado con `--mode text` (original) y `--mode voice` (captura, subida, transcript/response, TTS).
- 21 tests unitarios del cliente pasan sin hardware real: send_message, send_audio multipart, capture_audio, speak.
- `client.main.py --mode voice` en Raspberry real registró `Recording...`, `Uploading...`, transcript real, respuesta speakable, fallback de texto y salida limpia.
- `espeak` sonó audible, pero en esta pasada fue robótico y poco claro; los warnings ALSA/JACK no bloquearon la demo.
- Después de esta evidencia se ajustó el cliente a `espeak -v es -s 135 -g 8` para mejorar inteligibilidad en frases largas.
- `specs/audio-pipeline.md`, `docs/project-journal/week-03.md`, `docs/specs.md` y `README.md` se actualizaron para reflejar la validación real.

Conclusión: Phase 2B está implementada, fue validada inicialmente y quedó revalidada post-ajuste TTS el 2026-05-30 en Raspberry real siguiendo `specs/audio-pipeline-phase-2b-tts-revalidation.md`. Con `TONTO_TTS_ARGS="-v es -s 135 -g 8"`, la respuesta larga fue audible, más pausada, sin palabras atropelladas y suficientemente entendible para demo. Los warnings ALSA/JACK siguieron apareciendo, pero no bloquearon el audio. Esa revalidación desbloqueó Fase 3 web, que ya queda completada dentro de su alcance documentado.

### Riesgos

- Problemas de drivers/audio USB.
- Latencia excesiva.
- Intentar optimizar prematuramente el pipeline.

## Fase 3 — Loop interactivo desde cliente web (completada)

### Objetivo

Usar el cliente web de validacion como superficie interactiva para probar el pipeline de voz contra `POST /chat/audio` despues de cerrar la revalidacion Phase 2B post-ajuste TTS en el cliente Raspberry, completada el 2026-05-30. Esta fase validó permisos de microfono, generacion/subida de WAV, transcript real, respuesta conversacional, latencia, errores y reproduccion audible de la respuesta desde navegador.

### Entregables

- [x] Documentar la fase en `specs/audio-pipeline-phase-3-web-loop.md`.
- [x] Ampliar `specs/web-validation-client.md` con audio loop e instrumentacion.
- [x] Implementar captura de microfono y generacion WAV desde la web sin cambiar el contrato backend.
- [x] Mostrar transcript, response, latencia, estado tecnico y errores en la UI.
- [x] Reproducir de forma audible y entendible la respuesta desde el navegador.
- [x] Validar que `/chat` de texto sigue funcionando como fallback.
- [x] Registrar evidencia en `docs/project-journal/week-03.md`.

### Restricciones

- Mantener `POST /chat/audio` como contrato unico de voz.
- Enviar WAV compatible con el backend actual; no subir `webm`/`ogg` directamente.
- No exponer selector o subida manual de WAV como flujo visible de producto/demo; solo se permite para fixtures o helpers de tests.
- Usar APIs nativas del navegador para speech output; no añadir backend TTS ni dependencias.
- No introducir STT local, streaming, persistencia, auth ni UI avanzada.
- No sustituir la validacion final con Raspberry: la web acelera desarrollo, pero el producto fisico sigue siendo el objetivo MVP.
- Mantener Fase 3 dentro de `specs/audio-pipeline-phase-3-web-loop.md`: cliente web como superficie de validacion, WAV compatible y sin ampliar el backend a formatos comprimidos salvo decision explicita posterior.

### Evidencia

Validado el 2026-06-01 contra backend real desde navegador local. El loop completo `browser microphone -> WAV PCM 16 kHz mono -> POST /chat/audio -> transcript -> response -> browser speech` quedó aceptado por validación humana. Un fallo inicial `422 Audio did not contain recognizable speech` se resolvió seleccionando el microfono correcto en los ajustes del navegador, por lo que queda documentado como precondición de demo.

---

# Semana 4 - Estabilidad de demo y decisión de estados físicos

## Objetivo

Convertir el loop de voz validado en Semana 3 en una demo más repetible antes de añadir comportamiento nuevo.

La preparación de Semana 4 es documentación-first: specs, planes, roadmap y journal deben dejar claro el orden de trabajo para agentes IA. La memoria y los estados físicos se tratan como calibración y decisión de alcance, no como implementación automática.

## Entregables

- Kickoff documental de Semana 4 con spec, plan y journal.
- Validación reproducible del loop actual varias veces seguidas.
- Manejo de errores mejorado solo si la validación detecta bloqueos reales de demo.
- Calibración de conversación usando la memoria corta en proceso ya existente, sin persistencia — completada con 5 voice turns relacionados en Raspberry real.
- Gate de decisión para estados físicos mínimos e indicadores de tiempo/escucha: decisión tomada el 2026-06-07. Arduino/LEDs quedan fuera del MVP de 6 semanas; se implementan primero indicadores no físicos de escucha/tiempo para Raspberry y web. El follow-up web #23 (cerrada) quedó decidido como auto-stop al límite configurado, aviso simple de límite alcanzado y envío manual; la issue #25 (cerrada) reparó el contador visible en la superficie principal web y fue validada manualmente.

## Fases

0. Kickoff documental y handoff para agentes — completado 2026-06-02.
1. Baseline de demo reproducible sobre el sistema actual — completado 2026-06-05. 3 voice turns en Raspberry real, memoria corta validada, `/chat` y `/chat/audio` funcionando.
2. Resiliencia y errores observados durante la demo — completado 2026-06-05.
3. Calibración conversacional y memoria corta — completado 2026-06-07. Prompt calibrado, 49/49 tests pasados y 5 voice turns relacionados en Raspberry real.
4. Decisión explícita sobre estados físicos e indicadores no físicos de escucha/tiempo — decisión humana registrada 2026-06-07; specs y planes separados preparados para Raspberry y web; web #23/#25 (ambas cerradas) implementa contador visible, auto-stop al límite, warning y envío manual; Raspberry #27 (cerrada) implementado y validado en hardware real 2026-06-07.
5. Closeout con evidencia y próximos riesgos.

## Prioridades

1. Repetibilidad antes que nuevas funcionalidades.
2. Estabilidad y claridad de operación.
3. Mantener memoria y estados dentro del alcance MVP.

## Riesgos

- Introducir demasiada lógica de memoria.
- Implementar Arduino antes de demostrar que desbloquea la demo final.
- Scope creep por nuevas ideas.

---

# Semana 5 - Estabilidad y experiencia demo

## Objetivo

Convertir el sistema en una demo estable y repetible.

## Entregables

- Flujo completo funcionando de forma consistente.
- Runbook de operador y scripts de arranque.
- Ajustes de UX conversacional.
- Corrección de errores críticos.
- Demo ejecutada múltiples veces con éxito.

## Fases

0. Kickoff documental y handoff para agentes — completado 2026-06-08.
1. Runbook de demo y scripts de arranque — completado 2026-06-08.
2. Pulido de UX conversacional.
3. Resiliencia ante errores.
4. Ensayo de demo (3+ ejecuciones consecutivas).
5. Closeout con evidencia.

## Extra — Agent Capability Pack

Trabajo extra de Semana 5, trackeado en GitHub issue #43.

Objetivo: definir un asset portable para agentes basado en Markdown del repo y scripts PowerShell oficiales, de modo que Codex, OpenCode u otros agentes puedan arrancar/parar backend y ejecutar preflights SSH en Raspberry sin inventar comandos ad hoc ni guardar secretos en el repositorio.

La spec vive en `specs/week-05-agent-capability-pack.md` y el plan en `docs/plans/week-05-agent-capability-pack.md`.

## Prioridades

1. Estabilidad antes que nuevas funcionalidades.
2. Reducir fallos visibles.
3. Mejorar claridad de interacción.

## Riesgos

- Intentar añadir features nuevas.
- Cambios grandes de arquitectura demasiado tarde.
- Dependencia de configuraciones manuales frágiles.

---

# Semana 6 - Cierre del MVP y presentación

## Objetivo

Preparar la entrega final del proyecto.

## Entregables

- Demo final funcional.
- Documentación mínima reproducible.
- Checklist de arranque y validación.
- Limitaciones conocidas documentadas.
- Lista de siguientes pasos futuros.

## Prioridades

1. Garantizar reproducibilidad.
2. Reducir riesgo durante la demo.
3. Dejar el proyecto limpio y entendible.

## Riesgos

- Ajustes de última hora.
- Cambios no probados antes de la demo.
- Problemas de entorno o hardware.

---

# Regla del MVP

A partir de la semana 4 no se añadirán funcionalidades nuevas salvo que desbloqueen directamente la demo final.

El foco principal será:

- estabilidad,
- experiencia conversacional,
- reproducibilidad,
- y claridad técnica.

---

# Out of scope para el MVP

Las siguientes funcionalidades quedan explícitamente fuera del alcance inicial:

- modelos IA locales pesados,
- backend Go como requisito activo,
- entrenamiento de modelos propios,
- visión artificial avanzada,
- automatización doméstica compleja,
- arquitectura distribuida,
- multiusuario,
- dashboards complejos,
- interfaces gráficas avanzadas de producto,
- memoria vectorial avanzada,
- sistemas multiagente.

---

# Backlog inicial (prioridad alta)

## Infraestructura

- [x] Configurar backend mínimo local.
- [x] Crear endpoint HTTP inicial.
- [x] Configurar variables de entorno.
- [x] Validar comunicación Raspberry ↔ backend.

## Audio

- [x] Comprar y validar micrófono USB.
- [x] Validar captura WAV en Raspberry (manual, con `arecord`).
- [x] Implementar endpoint `POST /chat/audio` con validación WAV.
- [x] Probar subida manual WAV con `curl` desde la Raspberry.
- [x] Actualizar cliente Raspberry para capturar y subir WAV automáticamente.
- [x] Integrar STT backend.
- [x] Validar loop manual de voz Raspberry → backend → TTS.
- [x] Loop interactivo de voz Raspberry → backend → TTS automatizado en cliente.
- [x] Revalidar loop interactivo Raspberry → backend → TTS tras ajuste `espeak -v es -s 135 -g 8`.
- [x] Validar loop interactivo de voz desde cliente web contra `POST /chat/audio` despues de la revalidacion TTS de Phase 2B.
- [x] Validar respuesta audible desde navegador para el loop web de Fase 3.
- [x] Medir latencia básica del loop manual (`TOTAL_TIME=5.395580`).
- [ ] Mejorar calidad TTS progresivamente.

## Cliente Raspberry

- [x] Crear cliente Python mínimo.
- [x] Añadir logs básicos.
- [x] Añadir manejo básico de errores.
- [x] Gestionar estado de sesión local.
- [x] Añadir indicador no físico de escucha/tiempo durante grabación.

## Cliente web de validación

- [x] Crear scaffold inicial React + TypeScript + Vite.
- [x] Conectar con el endpoint `/chat` cuando el contrato esté estable.
- [x] Añadir build/typecheck a integración continua.
- [x] Fase 3: añadir loop interactivo de voz contra `POST /chat/audio`.
- [x] Fase 3: mostrar evidencia tecnica de audio, transcript, response, latencia y speech output.
- [x] Añadir indicador visible de escucha/tiempo durante captura de voz, con auto-stop al límite configurado, aviso simple y envío manual.
- [ ] Desplegar preview web para pruebas rápidas.

## Backend

- [x] Integrar OpenAI API.
- [x] Implementar flujo conversacional mínimo.
- [x] Gestionar historial simple.
- [x] Definir estructura de mensajes.
- [x] Excluir checks Go de CI mientras el backend MVP siga siendo Python/FastAPI.

## Hardware

- [ ] Integrar LEDs mediante Arduino (fuera del MVP de 6 semanas; futuro TONTO).
- [x] Definir decisión de estados físicos mínimos para el MVP: diferidos; usar primero indicadores no físicos.
- [ ] Validar estabilidad eléctrica y audio.

## Documentación

- [x] Crear documentación fundacional.
- [x] Documentar setup reproducible con scripts oficiales.
- [x] Definir workflow AI-assisted development.
- [x] Definir exportación para NotebookLM.
- [x] Añadir exportación combinada para refrescos ágiles de NotebookLM.
- [x] Mantener journal semanal actualizado.

---

# Criterios mínimos de éxito del MVP

El MVP se considerará exitoso si:

- TONTO mantiene una conversación básica funcional.
- El flujo voz → IA → voz funciona en hardware real.
- La demo puede reproducirse varias veces de forma consistente.
- El sistema puede arrancarse con instrucciones simples.
- La arquitectura y limitaciones quedan claramente documentadas.

---

# Definition of Done

TONTO MVP estará “done” cuando:

- exista una demo funcional reproducible,
- la arquitectura sea estable,
- el flujo conversacional funcione extremo a extremo,
- el sistema pueda presentarse sin configuración manual compleja,
- y el proyecto esté documentado de forma clara y mantenible.
