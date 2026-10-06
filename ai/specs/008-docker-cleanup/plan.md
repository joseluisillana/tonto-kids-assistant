# Plan de reparación de limpieza Docker

## Objetivo y fuente

Implementar ai/specs/008-docker-cleanup/spec.md; Part of #107, problema P-107-01.
Rama fix/docker-cleanup; depende de PR documental #108, sin agentes paralelos.

## Implementación

1. Cambiar down/stop a down --remove-orphans.
2. Resolver nombre efectivo Compose y consultar contenedores/redes por etiquetas.
3. Devolver error ante residuales; conservar volúmenes e instalaciones locales.
4. Documentar parada de todos los procesos Docker del proyecto en README.
5. Revalidar puntos 2/4/6 y registrar evidencia conservando los fallos previos.

## Verificación y aceptación

Actualización #110: consultar metadatos con --no-env-resolution y
--no-interpolate; propagar exit codes con mensajes acotados y sin salida Docker
cruda. Tests con canarios en stdout/stderr, además de alias y residuales.

Sintaxis Bash y diff check. Stub temporal: residuales y errores producen exit
no cero; comprobar proyecto personalizado y alias. Integración real: dev all
+ one-off activo + contenedor ajeno; down elimina solo TONTO, conserva
dependencias y segunda llamada exit 0. Repetir con stop. Arranque posterior,
test all y build all; CI remoto. Cerrar P-107-01 solo con prueba real.

## Prompt de handoff

Lee AGENTS.md, roadmap, specs y journal; aplica gate Git. Implementa
ai/specs/008-docker-cleanup/spec.md en fix/docker-cleanup. Solo limpieza CLI y docs, sin
dependencias ni otros arreglos de #107. Usa scripts oficiales y recursos
temporales identificados. No imprimas configuración Compose ni secretos.
Conserva volúmenes y otros proyectos. Actualiza checklist y CI; PR separada de
#108. Si #108 mergea, actualizar base y reconciliar antes de integrar la rama.


## Migration provenance

Original source: `docs/plans/docker-cleanup-implementation-plan.md` at baseline 818e88e. Relocated 2026-10-06;
original content/language retained with path references adjusted. Historical
commands, approvals and pending notes retain their original context.

## Record maintenance after migration

For future work, read [spec.md](spec.md), this plan and [journal.md](journal.md).
Revise the plan before implementation; preserve historical prompts as evidence,
not authorization to execute outdated commands. Mandatory root/common workflow,
Linux/Docker operation and D025 govern current work. Maintain the local journal
and synchronize definition status/updated with the parent INDEX.md in the same
change. No secrets, credentials, tokens, connection strings, PII or real customer
data; sensitive configuration uses parameter names only.
