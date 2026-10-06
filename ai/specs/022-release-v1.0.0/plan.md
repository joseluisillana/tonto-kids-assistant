# Plan de publicación v1.0.0

Fuente: specs/release-v1.0.0.md. Aprobado por operador el 2026-10-06.
Baseline e98f43f; rama chore/release-v1.0.0, sin paralelismo.

## Ejecución

1. Declarar VERSION y alinear package/lock web sin cambios de dependencias.
2. Notas de release y README: contratos, migración Linux, evidencia y pendientes.
3. Reconciliar roadmap/specs/journal. Verificar diff de lock, test/build web,
   export y diff check; CI completa de PR. Sin hardware ni proveedores reales.
4. Integrar con squash solo tras CI aprobada; actualizar main y esperar su CI.
5. Tag anotado v1.0.0 sobre SHA integrado; push solo de ese tag y publicación
   GitHub Release con --verify-tag y notas versionadas. Confirmar tag remoto,
   release publicada (no draft/prerelease), latest y checkout limpio.

## Prompt de handoff

Lee AGENTS, workflow y estado del proyecto. Ejecuta specs/release-v1.0.0.md.
Mantén una PR pequeña de metadatos/documentación, sin nuevas dependencias ni
runtime. El operador ya autoriza integrar tras CI y publicar v1.0.0. No leas
secretos ni revalides hardware o proveedores. Registra evidencia de los checks,
conserva #81/#88/#114/#53 y aislamiento completo como pendientes. Si el tag ya
existe, verifica su SHA y no lo reemplaces. Sincroniza main tras integración.


## Migration provenance

Original source: `docs/plans/release-v1.0.0-implementation-plan.md` at baseline 818e88e. Relocated 2026-10-06;
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
