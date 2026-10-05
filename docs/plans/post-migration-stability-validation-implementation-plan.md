# Plan de validación integral post-migración

Pasada final integrada sobre 7117313 autorizada: reiniciar matriz 1–9,
arranque/API → limpieza → CLI/emulador/voz humana → limpieza → Raspberry
preflight/voz humana → limpieza → setup/tests/build → helpers/docs → CI.
Registrar logs sanitizados y commits periódicos; no reparar nuevos fallos.
Prompt de continuación: ejecuta esta secuencia en la rama de #108, conserva
histórico y actualiza la matriz final. No declares OK con pendientes físicos.

Estado vigente: validación 1–9 COMPLETADA en rama de PR #115; CI 09ef3b3
aprobado. Pendiente merge #115 → rama de #108, CI global y revisión de #108
antes de main. #107 permanece abierta hasta integración. #114 es backlog
aplazado; #88 excluida. Reconciliación documental sin cambios de comportamiento.

## Objetivo y fuente

Ejecutar `specs/post-migration-stability-validation.md`, issue #107, conservando
histórico y añadiendo resultados actuales en la checklist de migración.

## Alcance

Validaciones 1–9 y ampliaciones de la spec; solo documentos/evidencias en Git.
Excluir validación física touch/kiosk #88, correcciones y nuevas dependencias.
Decisión D025: DevExpert deprecado, smoke real NO APLICA; no operarlo ni pedir
credenciales. OpenAI conserva la validación real de proveedor.

## Secuencia

1. Gate Git y lectura roadmap/specs/journal; rama documental nueva.
2. Inventariar servicios existentes sin borrar volúmenes ni modificar secretos.
3. Registrar baseline y ejecutar 1–9 secuencialmente, con limpieza entre fases.
4. Registrar fallos con impacto, reproducción y comprobaciones bloqueadas.
5. Commit por grupo; push, CI y cierre documental con pendientes explícitos.

## Verificación y aceptación

`./tonto.sh dev all`, `./tonto.sh down`, `./tonto.sh dev backend`,
`./scripts/agent-raspberry.sh preflight`, `./tonto.sh setup`,
`./tonto.sh test all`, `./tonto.sh build all`, helpers de agente,
exportador y hook. Revisar `git diff --check` y CI del SHA subido.
Aplicar criterios de la spec: no declarar estable con fallos o pendientes.

## Prompt de handoff

Lee AGENTS.md, roadmap, specs y último journal. Continúa #107 en la rama
docs/post-migration-stability-validation. Lee la spec y el registro de migración.
Ejecuta comprobaciones pendientes 1–9 y ampliaciones con scripts oficiales.
Respeta D025: no operes DevExpert; su smoke real es NO APLICA.
No arregles producto ni añadas dependencias: documenta cada error en Registro
de Problemas, continúa cuando sea posible y haz commits documentales periódicos.
No marques hardware, audibilidad o CI como aprobados sin evidencia real.
Conserva los resultados previos y registra comando, revisión, exit y logs sin
secretos. Cierra con matriz de resultados y condiciones pendientes para aceptar
una versión estable; no cierres #81 ni #88.
