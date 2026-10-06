# #110 — plan de reducción de exposiciones accidentales

PR 1 integrada en #116; PR 2 validada localmente el 2026-10-06. Fuente:
specs/agent-secrets-protection.md. Rama fix/issue-110-secret-free-tasks.

## Objetivo y alcance

Evitar exposición accidental en limpieza Docker y errores de proveedores,
conservando .env, automatización backend/SSH y contratos API. Sin aislamiento,
mediador, dependencias, migración de claves ni tareas de #88/#114.

## Implementación

### Secuencia de PRs acordada

1. Primera PR integrada en #116 (8ef12ed), CI completa aprobada. #110 abierta.
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

### Implementación de PR 2

Rama fix/issue-110-secret-free-tasks desde main 8ef12ed, sin paralelismo.
1. Compose de tareas independiente con servicios backend/UI/web, mismas imágenes,
   dependencias/cachés/volumen; sin env_file/puertos/depends_on.
2. Helper local CLI para Compose de tareas con archivo explícito y env-file vacío;
   ignorar overrides runtime y retirar credenciales conocidas del proceso.
3. Creación automática de .env solo en comandos runtime, conservar dev/SSH.
4. Tests CLI y Compose real con canarios ficticios: sin inyección de claves,
   carga automática de .env, creación de archivo ni arranque backend.
5. ./tonto.sh test all y build all con comandos normales; setup si necesario.
   Validar configuración runtime solo con fixtures, sin dumps reales.
6. Actualizar README/specs/roadmap/journal. Part of #110 en PR; no merge sin
   autorización. No ejecutar PR 3/4 dentro de esta fase.

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

PR 2: setup oficial exit 0, npm audit 0; test all con 151 Python y 25 UI
pasados más suite web; build all exit 0. Sin overrides temporales ni claves.
Compose real con fixtures confirma tareas sin inyección, runtime conservado,
volumen compartido y ejecución sin .env. Sintaxis Bash/diff check pasan.
Los mounts/build context del filesystem siguen pendientes de PR 3.

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
