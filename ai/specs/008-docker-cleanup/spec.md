---
id: "008-docker-cleanup"
title: "Limpieza completa de Docker"
status: done
owner: "Unknown — legacy ownership not recorded"
created: "2026-10-06"
updated: "2026-10-06"
related:
  - "https://github.com/joseluisillana/tonto-kids-assistant/blob/818e88eacbac3989c091d1294c92e26ebeb663f7/specs/docker-cleanup.md"
  - "ai/specs/001-historical-records-migration/metadata-review.md"
  - "https://github.com/joseluisillana/tonto-kids-assistant/issues/107"
  - "https://github.com/joseluisillana/tonto-kids-assistant/issues/110"
  - "ai/specs/019-post-migration-stability-validation/artifacts/migrate-linux-docker-validation.md"
  - "ai/specs/008-docker-cleanup/plan.md"
---

# Limpieza completa de Docker

Fecha: 2026-10-05. Plan aprobado. Part of #107; resuelve P-107-01.

`./tonto.sh down` y `stop` deben detener y retirar todos los contenedores del
proyecto Compose efectivo, incluidos one-off activos creados por `run`, y sus
redes administradas. Pueden interrumpir demos/tests activos de ese proyecto.
Usar `down --remove-orphans` y verificar después por etiquetas de proyecto:
si quedan contenedores o redes, exit no cero con IDs residuales.
Propagar errores de Docker o configuración.

Obtener nombre de configuración efectiva, respetando COMPOSE_PROJECT_NAME;
nunca imprimir configuración ni secretos. No usar prune, --volumes o borrado
global ni tocar contenedores ajenos. Conservar backend-venv, .venv host y
web/node_modules. Repetir sin servicios debe devolver exit 0.

Aceptación: servicios/one-off eliminados, red ausente, puertos libres;
contenedor ajeno intacto; dependencias conservadas; alias e idempotencia pasan;
residual simulado devuelve error; arranque y tests siguen funcionando.
Actualizar puntos 2/4/6 conservando histórico.

## Diagnósticos seguros — #110, 2026-10-06

La consulta de metadatos desactiva resolución de env_file e interpolación antes
de seleccionar el nombre; no captura configuración expandida. Aún genera un
modelo estructural interno: no introducir secretos literales en YAML.
No devolver stdout/stderr crudos de Docker al operador/agente. Fallos reportan
operación y exit code; residuales se notifican sin volcado de IDs. Se conserva
la resolución de proyecto de Compose y sus overrides. Sin cambios de .env.

Fuera de alcance: TTS, URL UI, setup, caches, mDNS, UI física y dependencias nuevas.
Plan: docs/plans/docker-cleanup-implementation-plan.md.

## Migration provenance and supported current state

- Original repository source: `specs/docker-cleanup.md` at baseline 818e88e.
- First recorded Git date: 2026-10-06; actual original authoring date is unknown
  unless explicitly recorded in the preserved body.
- Last source Git date before migration: 2026-10-06.
- Migration/update date: 2026-10-06. Legacy owner/authorship is not established;
  the current owner field records that uncertainty, not a fabricated attribution.
- Status decision: Final accepted #107 matrix includes basic/host/Raspberry cleanup; secret-safe follow-up accepted in #110.
- Evidence: [source](../019-post-migration-stability-validation/artifacts/migrate-linux-docker-validation.md).
- Corresponding GitHub tracking issues: [GitHub issue](https://github.com/joseluisillana/tonto-kids-assistant/issues/107), [GitHub issue](https://github.com/joseluisillana/tonto-kids-assistant/issues/110).

Historical headings below/above retain the original reported state. YAML status
and this provenance annotation express the supported state after evidence review.
Do not execute archived proposals or historical operating examples without a new
authorized work item. No runtime or acceptance behavior changed by relocation.

Maintain plan.md/journal.md and synchronize status/updated with the parent INDEX.md
in the same change. No secrets, credentials, tokens, connection strings, PII or
real customer data; sensitive configuration is described by parameter name only.
