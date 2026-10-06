---
id: "019-post-migration-stability-validation"
title: "Validación integral de estabilidad tras migración Linux/Docker"
status: done
owner: "Unknown — legacy ownership not recorded"
created: "2026-10-05"
updated: "2026-10-06"
related:
  - "specs/post-migration-stability-validation.md"
  - "ai/specs/001-historical-records-migration/metadata-review.md"
  - "https://github.com/joseluisillana/tonto-kids-assistant/issues/107"
  - "https://github.com/joseluisillana/tonto-kids-assistant/pull/108"
  - "ai/specs/019-post-migration-stability-validation/plan.md"
  - "ai/specs/019-post-migration-stability-validation/artifacts/migrate-linux-docker-validation.md"
---

# Validación integral de estabilidad tras migración Linux/Docker

Creada: 2026-10-05. Validación completada: 2026-10-06.
Estado: COMPLETADA — OK de migración en el alcance acordado.
Tracking: #107. PR de integración: #108. Reparación del emulador: #115.
Rama de trabajo histórica: `docs/post-migration-stability-validation`.
Código auditado: 711731336bb7427d87a7c180eee43c837f8d1964.
Evidencias finales y CI: 63d4099, runs 37381170529 y 37381176221, success.
Registro canónico: matriz final al inicio de `ai/specs/019-post-migration-stability-validation/artifacts/migrate-linux-docker-validation.md`.

Los nueve puntos pasan, incluida voz física Chrome/emulador/Raspberry y limpieza.
El cierre administrativo de #107 se realiza tras integrar #108 en main.
Sin trabajo funcional pendiente en esta spec; no se crea release/tag.
Limitaciones: mDNS requiere IP con identidad SSH verificada en esta LAN;
volumen #114 aplazado, secretos #110 separado y touch/kiosk #88 excluido.
DevExpert NO APLICA D025. P-107-15 retirado como bloqueo por operador.

## Objetivo y alcance

Obtener una versión candidata estable del estado actual post-MVP, verificando
Linux, Docker, backend, web, cliente CLI Raspberry y widgets Kivy. El registro
ejecutable y las evidencias viven en `ai/specs/019-post-migration-stability-validation/artifacts/migrate-linux-docker-validation.md`.
La evidencia histórica no constituye una validación de la revisión actual.

Se excluye únicamente la aceptación física touch/OpenGL ES/kiosk de Raspberry
(#88). No se excluyen voz Raspberry, micrófono web ni TTS; si requieren operador
o hardware no disponible quedan pendientes, nunca aprobados por mocks.

## Matriz de ejecución

1. Arranque `./tonto.sh dev all`; health, HTTP web, `/chat` real, contratos
   negativos y CORS. Separar disponibilidad de servicio de proveedor real.
2. `./tonto.sh down`; contenedores, puertos y procesos residuales.
3. `./tonto.sh dev backend`; cliente CLI host con tres turnos relacionados,
   salida limpia y fallback TTS. UI Linux: comprobar configuración efectiva,
   conectividad y dependencias de captura/TTS del emulador.
4. Parada y repetición de controles de limpieza.
5. Backend LAN + preflight real Raspberry; identidad, revisión, audio y health;
   tres turnos de voz, transcript, respuesta, latencia y audibilidad humana.
6. Parada y limpieza tras Raspberry.
7. Setup oficial y `test all` (78 Python + 24 UI esperados como baseline,
   no cuota fija), `build all`; comprobar aislamiento venv, permisos y caches.
8. Sintaxis de todos los Bash, export NotebookLM, instalación hook,
   ciclo start/status/health/stop del helper backend y helpers Raspberry/demo.
9. Push de commits, CI del SHA validado, logs y URL de ejecución con resultado.

Ampliaciones: widgets Kivy reales/Xvfb, regresión de estados/errores/reentrada,
web micrófono/WAV/auto-stop/speech y texto en navegador, OpenAI como proveedor real (tests simulados y smoke real distinguidos), coherencia
de runbooks Linux, limpieza de contenedores one-off y arranque repetible.
Usar suites existentes y fixtures existentes; no añadir dependencias ni tests
de producto durante esta auditoría. No divulgar claves ni `.env`.

## Estados y aceptación

Cada comprobación inicia PENDIENTE; COMPLETADO exige evidencia de sus criterios;
FALLIDO identifica un fallo reproducible. Un bloqueo externo conserva PENDIENTE
con intento y motivo. Cada evidencia indica comando, fecha, revisión, resultado
y salida relevante, con logs sanitizados. Una sección puede contener subchecks
completados y permanecer pendiente por los restantes.

La versión candidata solo se acepta con todas las comprobaciones incluidas
completadas, CI verde del código auditado y cero problemas abiertos bloqueantes.
Los warnings se clasifican, no se ocultan. No prometer estabilidad absoluta ni
crear tag/release mientras existan pendientes o fallos. Las correcciones se
planifican después de la auditoría en ramas separadas y requieren revalidación.

## Restricción de ejecución

No corregir código, scripts, configuración ni runbooks durante la validación.
Registrar problemas y continuar salvo dependencia completamente bloqueante.
Commits documentales tras preparación y grupos de comprobaciones.

Plan: `ai/specs/019-post-migration-stability-validation/plan.md`.


## Decisión de alcance — DevExpert, 2026-10-05 (D025)

Por decisión explícita del operador, DevExpert está deprecado y no se operará.
Smoke real DevExpert: NO APLICA, excluido de aceptación de esta pasada. No pedir
credenciales ni considerarlo un bloqueo del cierre. Evidencias/tests existentes
se conservan; no se elimina soporte ni se cambia runtime en esta decisión.

## Migration provenance and supported current state

- Original repository source: `specs/post-migration-stability-validation.md` at baseline 818e88e.
- First recorded Git date: 2026-10-06; actual original authoring date is unknown
  unless explicitly recorded in the preserved body.
- Last source Git date before migration: 2026-10-06.
- Migration/update date: 2026-10-06. Legacy owner/authorship is not established;
  the current owner field records that uncertainty, not a fabricated attribution.
- Status decision: Nine-point acceptance in final matrix and operator OK, integrated #108; #88/#114 excluded and D025 enforced.
- Evidence: [source](https://github.com/joseluisillana/tonto-kids-assistant/pull/108).
- Corresponding GitHub tracking issues: [GitHub issue](https://github.com/joseluisillana/tonto-kids-assistant/issues/107).

Historical headings below/above retain the original reported state. YAML status
and this provenance annotation express the supported state after evidence review.
Do not execute archived proposals or historical operating examples without a new
authorized work item. No runtime or acceptance behavior changed by relocation.

Maintain plan.md/journal.md and synchronize status/updated with the parent INDEX.md
in the same change. No secrets, credentials, tokens, connection strings, PII or
real customer data; sensitive configuration is described by parameter name only.
