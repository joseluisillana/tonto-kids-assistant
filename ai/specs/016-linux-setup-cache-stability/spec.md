---
id: "016-linux-setup-cache-stability"
title: "Estabilidad de setup y cachés tras migración"
status: done
owner: "Unknown — legacy ownership not recorded"
created: "2026-10-06"
updated: "2026-10-06"
related:
  - "https://github.com/joseluisillana/tonto-kids-assistant/blob/818e88eacbac3989c091d1294c92e26ebeb663f7/specs/linux-setup-cache-stability.md"
  - "ai/specs/001-historical-records-migration/metadata-review.md"
  - "https://github.com/joseluisillana/tonto-kids-assistant/issues/107"
  - "docs/project-journal/week-06.md#post-mvp--reparación-de-setupcachés-linux-2026-10-05"
  - "ai/specs/016-linux-setup-cache-stability/plan.md"
---

# Estabilidad de setup y cachés tras migración

Estado: plan aprobado e implementación en validación, 2026-10-05. Part of #107.
Problemas: P-107-05 y P-107-06. Sin dependencias nuevas.

## Diagnóstico

`tonto.sh setup` instala Python en el volumen backend-venv y luego borra
el .venv del host para crear otro para el IDE. Si falta ensurepip o falla pip,
el script solo advierte y puede terminar con éxito. Según README el entorno
host es auxiliar del IDE; no es requisito del flujo Docker.
Pip del contenedor intenta usar /.cache/pip sin permisos. Npm usa /tmp/.npm,
que se pierde al retirar el contenedor. Ninguna ruta cumple la política local.
CI ya llama setup/test/build de tonto.sh y no usa setup-python/setup-node.
La spec ci-local-cache-alignment describe el workflow anterior; su issue #89
está cerrada y no autoriza restaurar ese workflow.

## Comportamiento propuesto

- `./tonto.sh setup` prepara Python Docker y web sin borrar ni modificar .venv
  del host. Exit 0 significa que todos los pasos obligatorios terminaron bien.
- `./tonto.sh setup host` prepara explícitamente el entorno opcional del IDE.
  Comprueba python3/venv, conserva un entorno existente y devuelve exit no cero
  si falla. Informa de la precondición sin instalar paquetes de sistema.
- Backend configura PIP_CACHE_DIR=/app/.cache/pip. Web monta únicamente
  .cache/npm del repo en /app/.cache/npm y configura npm_config_cache allí.
  Preparar directorios como usuario del host; ajustar propietario solo del volumen
  .venv y .cache/pip/npm si existen con otro UID. No ampliar permisos de todo el repo.
- Mantener backend-venv y comandos oficiales. Fallos Docker/pip/npm obligatorios
  se propagan; ningún mensaje final de éxito oculta un fallo.
- Alinear cache de construcción del emulador y distinguirla de la caché runtime;
  no introducir caché global nueva ni cambiar arquitectura.
- CI conserva setup/test/build actuales. Primero verificar rutas y permisos;
  persistencia entre runners mediante una Action de caché sería otra decisión.

## Aceptación

1. Setup Docker funciona en entorno limpio y no requiere Python host.
2. .venv host existente no se borra ni se modifica por setup Docker.
3. Fallos obligatorios producen exit no cero; setup host fallido también.
4. Pip y npm reportan las rutas locales configuradas y escriben como UID/GID host.
5. Segunda ejecución reutiliza las cachés; no hay advertencia de caché deshabilitada.
6. test all, build all y CI pasan; down conserva dependencias y cachés.
7. Registro P-107-05/06 actualizado con evidencia; punto 7 sigue abierto si
   P-107-07 aún no se resuelve o acepta explícitamente.

## Fuera de alcance

Cambios de producto, secretos, instalación global, dependencias nuevas, audio
físico, restauración de Actions antiguas y reparación automática de npm audit.
Las vulnerabilidades P-107-07 requieren auditoría actual, evaluación por advisory
con fuentes oficiales y propuesta de versiones antes de tocar manifest/lockfile.

Plan: docs/plans/linux-setup-cache-stability-implementation-plan.md.

## Migration provenance and supported current state

- Original repository source: `specs/linux-setup-cache-stability.md` at baseline 818e88e.
- First recorded Git date: 2026-10-06; actual original authoring date is unknown
  unless explicitly recorded in the preserved body.
- Last source Git date before migration: 2026-10-06.
- Migration/update date: 2026-10-06. Legacy owner/authorship is not established;
  the current owner field records that uncertainty, not a fabricated attribution.
- Status decision: Setup/cache repair accepted with official tests/build and final #107 integration; supersedes source in-validation heading.
- Evidence: [source](../../../docs/project-journal/week-06.md#post-mvp--reparación-de-setupcachés-linux-2026-10-05).
- Corresponding GitHub tracking issues: [GitHub issue](https://github.com/joseluisillana/tonto-kids-assistant/issues/107).

Historical headings below/above retain the original reported state. YAML status
and this provenance annotation express the supported state after evidence review.
Do not execute archived proposals or historical operating examples without a new
authorized work item. No runtime or acceptance behavior changed by relocation.

Maintain plan.md/journal.md and synchronize status/updated with the parent INDEX.md
in the same change. No secrets, credentials, tokens, connection strings, PII or
real customer data; sensitive configuration is described by parameter name only.
