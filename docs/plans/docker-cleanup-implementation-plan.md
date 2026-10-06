# Plan de reparación de limpieza Docker

## Objetivo y fuente

Implementar specs/docker-cleanup.md; Part of #107, problema P-107-01.
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
specs/docker-cleanup.md en fix/docker-cleanup. Solo limpieza CLI y docs, sin
dependencias ni otros arreglos de #107. Usa scripts oficiales y recursos
temporales identificados. No imprimas configuración Compose ni secretos.
Conserva volúmenes y otros proyectos. Actualiza checklist y CI; PR separada de
#108. Si #108 mergea, actualizar base y reconciliar antes de integrar la rama.
