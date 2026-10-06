# Instrumentación del proceso de specs e issues — fase 1

## Objetivo y fuente

Aplicar el prompt del operador del 2026-10-06: proceso portable en `ai/`,
plantillas y transición explícita desde specs/planes/journals/GitHub existentes.
No crear registros concretos ni ejecutar la migración histórica.

## Diagnóstico previo

`docs/specs.md` agrupa contratos en `specs/`; `docs/plans/` contiene planes,
prompts y guías de ejecución. Los journals por semana/hito mezclan decisiones
y evidencia de varios trabajos. Specs como week-05-demo-stability enlazan una
issue padre y fases hijas; otras incluyen guías de validación separadas.
No hay correspondencia uno a uno ni numeración local común. GitHub conserva
identidad y cierre remoto; una futura importación debe preservar esas relaciones.
El export actual selecciona docs/specs, pero no ai/.

## Alcance y pasos previos a implementación

1. Crear README común, README/INDEX por tipo y seis plantillas en inglés.
2. Definir estados, IDs independientes, planificación, journals y seguridad.
3. Añadir navegación/proceso a AGENTS.md raíz sin modificar los locales.
4. Reconciliar workflow común, documentación y plantilla de plan heredada.
5. Registrar evidencia en journal global y validar enlaces y diff.

Excluidos: migración, registros concretos, GitHub remoto, producto, dependencias,
CI, scripts/export y AGENTS.md locales. Sin dependencias nuevas.

## Archivos afectados

`ai/**/*.md`, `AGENTS.md`, `docs/ai-assisted-workflow.md`,
`docs/documentation-workflow.md`, `docs/plans/TEMPLATE-spec-implementation-plan.md`,
`docs/specs.md` y `docs/project-journal/post-mvp-touch-ui.md`.

## Verificación y aceptación

Comprobar estructura de once archivos ai/, front-matter y seguridad de las seis
plantillas, enlaces reales, índices vacíos y coherencia de fuentes canónicas.
Revisar que ningún histórico se mueve ni cambia y ningún local se edita.
Ejecutar `git diff --check`; sin tests runtime para este cambio documental.

## Aislamiento y handoff

Rama: `docs/ai-specs-issues-process`. Checkout actual sin trabajo paralelo;
no requiere otro worktree. Colisiones: instrucciones raíz, workflow, índice y
journal global. Si se integra trabajo relacionado, reconciliar esas fuentes.
Sin issue concreta nueva por instrucción del encargo; el prompt explícito del
operador autoriza esta instrumentación. La fase 2 requiere otro trabajo.

## Prompt de implementación

Leer AGENTS.md y workflow común. Implementar únicamente los pasos anteriores,
usando ai/ como fuente del nuevo proceso y conservando las reglas de operación,
seguridad, handoff y Git. Mantener índices vacíos; documentar convivencia con
registros heredados y límites del export. Validar los criterios anteriores y
registrar resultados reales, sin atribuir integración o validación funcional.
