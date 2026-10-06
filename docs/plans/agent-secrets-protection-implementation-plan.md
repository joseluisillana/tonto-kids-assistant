# #110 — plan de reparación de diagnósticos

Primera reparación autorizada 2026-10-06. Fuente:
specs/agent-secrets-protection.md. Rama fix/issue-110-safe-diagnostics.

## Objetivo y alcance

Evitar exposición accidental en limpieza Docker y errores de proveedores,
conservando .env, automatización backend/SSH y contratos API. Sin aislamiento,
mediador, dependencias, migración de claves ni tareas de #88/#114.

## Implementación

### Secuencia de PRs acordada

1. Primera PR: trabajo actual de diagnósticos y spec/plan. Validación local
   completada; commit/PR y revisión pendientes. Sin cierre de #110.
2. Tras integrar PR 1 y actualizar main: separar setup/tests de credenciales,
   manteniendo comandos oficiales; ampliar requisitos y aceptación de la fase.
3. Tras integrar PR 2: exclusiones de build y montajes con mínimo impacto.
4. Tras integrar PR 3: export NotebookLM y validación canarios/rutas/symlinks.

Revisión de otros diagnósticos en la PR que corresponda; issue o PR adicional
solo si constituye trabajo independiente. No iniciar fases posteriores durante
la preparación de la primera entrega.

### Implementación de PR 1

1. Consulta Compose con --no-env-resolution y --no-interpolate; seleccionar
   identidad antes de capturar salida. Acotar errores y residuales de cleanup.
2. Errores de proveedores sin body/reason arbitrarios ni cadenas de excepción;
   configuración inválida sin valor reflejado. Conservar códigos y éxitos.
3. Canarios en stubs Docker y HTTP mocks para ambos adaptadores y endpoints.
4. Reconciliar docs de cleanup y estado #110 con evidencia.
5. Complemento autorizado: logging estándar compartido de fallos chat/STT,
   JSON con campos permitidos y categorías acotadas. Sin payloads, excepciones,
   conversación ni persistencia. caplog verifica ausencia de canarios, campos
   útiles y ausencia de exc_info/stack_info en ambos adaptadores y endpoints.

## Verificación

Usar .venv/bin/python -m pytest para pruebas focalizadas y suite Python cuando
la venv local está disponible; no requiere Docker ni claves reales.
Comando oficial adicional ./tonto.sh test python si se ejecuta con configuración
Compose temporal sin secretos. No usar config expandida del proyecto real.
Bash -n tonto.sh y git diff --check. No cambiar ni inspeccionar secretos reales.
No se exige web/UI o demo física para errores y diagnóstico sin cambios de loop.

## Criterios

Evidencia 2026-10-06: suite oficial Python en Docker con override env_file vacío,
135 passed. Sintaxis Python/Bash y diff check pasan. Consulta Compose real con
config ficticia y proyecto desde .env/override: dos casos pasan sin canarios
expandidos. Teardown se verifica por stubs, no se ejecuta contra demo real.

Complemento logs: suite oficial Python sin env_file **136 passed**, sintaxis
Python y diff check pasan. caplog verifica campos acotados y ausencia de
canarios/exc_info/stack_info; logger rechaza campos arbitrarios.

Los de la spec. Canarios ausentes en respuestas, trazas y stdout/stderr; tests
mantienen identidad personalizada, propagación de exit codes y volúmenes.
Una salida segura del helper no acredita denegación de acceso deliberado.

## Prompt de handoff

Implementa specs/agent-secrets-protection.md y este plan. Lee AGENTS, workflow,
roadmap/specs/journal y verifica rama/status. Mantén .env y operación automática
backend/SSH. No leas secretos reales, no ejecutes dumps ni añadas dependencias.
Tests con mocks/canarios; conserva contratos, overrides y volúmenes. DevExpert
solo mocks. Ejecuta verificación y documenta límites. Part of #110 en PR; no
cierres objetivo original por esta reparación parcial.

## Aislamiento del trabajo

Checkout actual, sin paralelismo. Cambios documentales previos de esta misma
conversación conservados. Colisiones: tonto.sh, backend, tests y docs. Actualizar
si mergea trabajo relacionado. Build/export/setup sin secretos son seguimiento.
