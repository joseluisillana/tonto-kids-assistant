# Plan de validación integral post-migración

Estado: COMPLETADO, 2026-10-06. Tracking #107; integración #108.
Código auditado 7117313; nueve puntos y voz física aceptados, limpieza correcta.
CI 63d4099 success en runs 37381170529 y 37381176221.
No queda trabajo funcional; cerrar administrativamente #107 tras merge #108.
#114 aplazado, #110 separado, #88 excluido y DevExpert NO APLICA D025.
Las instrucciones siguientes documentan el procedimiento ejecutado y su handoff,
no una nueva cola de pendientes. Metadatos estabilizados sin cambios de comportamiento.

## Objetivo y fuente

Ejecutar `ai/specs/019-post-migration-stability-validation/spec.md`, issue #107, conservando
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


## Migration provenance

Original source: `docs/plans/post-migration-stability-validation-implementation-plan.md` at baseline 818e88e. Relocated 2026-10-06;
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
