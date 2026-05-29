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

## Fase 2 — Integración STT (parcialmente completada)

### Entregables pendientes

- [x] Elegir proveedor STT: OpenAI `gpt-4o-mini-transcribe` como default inicial; Vosk Spanish y `whisper.cpp` quedan como alternativas offline para spike posterior.
- [x] Integrar STT en el backend con `OPENAI_STT_MODEL` opcional y sin SDK nuevo.
- [x] Pipeline de voz extremo a extremo manual: Raspberry captura → backend STT → respuesta → TTS.
- [ ] Fase 2B: loop interactivo con captura desde el cliente Raspberry.

### Prioridades

1. Validar captura de audio estable.
2. Mantener latencia razonable.
3. Evitar reconocimiento de voz complejo local.

### Evidencia Phase 2A

Validado el 2026-05-30 desde Raspberry real `tonto-pi` contra backend LAN `192.168.1.91:8000`: captura WAV manual PCM 16-bit mono 16 kHz, `POST /chat/audio` con `HTTP_STATUS=200`, `TOTAL_TIME=5.395580`, transcript real `Hola tonto, explícame qué es una estrella.`, respuesta educativa, y reproducción local con `espeak`. La prueba negativa con archivo de texto devolvió `HTTP_STATUS=400`. El pipeline queda validado manualmente, pero el loop interactivo del cliente Raspberry sigue pendiente.

### Riesgos

- Problemas de drivers/audio USB.
- Latencia excesiva.
- Intentar optimizar prematuramente el pipeline.

## Fase 3 — Loop interactivo desde cliente web (planificada)

### Objetivo

Usar el cliente web de validacion como superficie interactiva para probar el pipeline de voz contra `POST /chat/audio` despues de cerrar la automatizacion de captura/subida en el cliente Raspberry. Esta fase permite validar permisos de microfono, generacion/subida de WAV, transcript real, respuesta conversacional, latencia y errores desde navegador.

### Entregables pendientes

- [ ] Documentar la fase en `specs/audio-pipeline-phase-3-web-loop.md`.
- [ ] Ampliar `specs/web-validation-client.md` con audio loop e instrumentacion.
- [ ] Implementar captura o seleccion de WAV desde la web sin cambiar el contrato backend.
- [ ] Mostrar transcript, response, latencia, estado tecnico y errores en la UI.
- [ ] Validar que `/chat` de texto sigue funcionando como fallback.
- [ ] Registrar evidencia en `docs/project-journal/week-03.md`.

### Restricciones

- Mantener `POST /chat/audio` como contrato unico de voz.
- Enviar WAV compatible con el backend actual; no subir `webm`/`ogg` directamente.
- No introducir STT local, streaming, persistencia, auth ni UI avanzada.
- No sustituir la validacion final con Raspberry: la web acelera desarrollo, pero el producto fisico sigue siendo el objetivo MVP.

### Riesgo principal

El navegador no genera WAV PCM 16 kHz mono por defecto. La implementacion futura debe producir WAV en cliente con APIs nativas o empezar con un selector manual de WAV antes de ampliar captura de microfono.

---

# Semana 4 - Memoria simple y estados físicos

## Objetivo

Dar personalidad mínima y persistencia básica a TONTO.

## Entregables

- Historial simple de conversación.
- Estados físicos básicos con Arduino y LEDs.
- Manejo básico de errores.
- Flujo reproducible varias veces seguidas.

## Prioridades

1. Hacer la experiencia más “viva”.
2. Mejorar estabilidad del sistema.
3. Mantener simplicidad en memoria y estado.

## Riesgos

- Introducir demasiada lógica de memoria.
- Complejidad innecesaria en integración Arduino.
- Scope creep por nuevas ideas.

---

# Semana 5 - Estabilidad y experiencia demo

## Objetivo

Convertir el sistema en una demo estable y repetible.

## Entregables

- Flujo completo funcionando de forma consistente.
- Scripts simples de arranque.
- Ajustes de UX conversacional.
- Corrección de errores críticos.
- Demo ejecutada múltiples veces con éxito.

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
- [ ] Actualizar cliente Raspberry para capturar y subir WAV automáticamente.
- [x] Integrar STT backend.
- [x] Validar loop manual de voz Raspberry → backend → TTS.
- [ ] Loop interactivo de voz Raspberry → backend → TTS automatizado en cliente.
- [ ] Validar loop interactivo de voz desde cliente web contra `POST /chat/audio`.
- [x] Medir latencia básica del loop manual (`TOTAL_TIME=5.395580`).
- [ ] Mejorar calidad TTS progresivamente.

## Cliente Raspberry

- [x] Crear cliente Python mínimo.
- [x] Añadir logs básicos.
- [x] Añadir manejo básico de errores.
- [x] Gestionar estado de sesión local.

## Cliente web de validación

- [x] Crear scaffold inicial React + TypeScript + Vite.
- [x] Conectar con el endpoint `/chat` cuando el contrato esté estable.
- [x] Añadir build/typecheck a integración continua.
- [ ] Fase 3: añadir loop interactivo de voz contra `POST /chat/audio`.
- [ ] Fase 3: mostrar evidencia tecnica de audio, transcript, response y latencia.
- [ ] Desplegar preview web para pruebas rápidas.

## Backend

- [x] Integrar OpenAI API.
- [x] Implementar flujo conversacional mínimo.
- [x] Gestionar historial simple.
- [x] Definir estructura de mensajes.
- [x] Excluir checks Go de CI mientras el backend MVP siga siendo Python/FastAPI.

## Hardware

- [ ] Integrar LEDs mediante Arduino.
- [ ] Definir estados físicos mínimos.
- [ ] Validar estabilidad eléctrica y audio.

## Documentación

- [x] Crear documentación fundacional.
- [x] Documentar setup reproducible con scripts oficiales.
- [x] Definir workflow AI-assisted development.
- [x] Definir exportación para NotebookLM.
- [x] Añadir exportación combinada para refrescos ágiles de NotebookLM.
- [ ] Mantener journal semanal actualizado.

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
