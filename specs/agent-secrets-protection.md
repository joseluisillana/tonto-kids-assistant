# #110 — diagnósticos sin exposición accidental de secretos

Estado: primera reparación autorizada por el operador, 2026-10-06.
Baseline: main a985dac. Rama: fix/issue-110-safe-diagnostics.
Tracking: https://github.com/joseluisillana/tonto-kids-assistant/issues/110.
Plan: docs/plans/agent-secrets-protection-implementation-plan.md.

## Alcance elegido

Mantener workflow actual, almacenamiento en .env y operación automatizada de
backend/SSH. El operador descarta sustituir .env por variable host. Aislamiento,
mediador y otras formas de provisión quedan diferidos. El historial de opciones
vive en docs/agent-secrets-credential-options.md y el diseño de aislamiento
anterior queda como alternativa no aprobada.

No se garantiza impedir acceso deliberado del agente por archivos, shell,
Docker o código modificable. Esta reparación no completa el objetivo universal
original de #110 ni autoriza cerrar la issue.

## Entregas bajo esta spec

| Entrega | Alcance | Estado |
| --- | --- | --- |
| PR 1 | Spec/plan, limpieza y errores/logs chat/STT seguros | Implementada, validada localmente; pendiente revisión/integración |
| PR 2 | Setup/tests sin credenciales reales, mismos comandos | Pendiente |
| PR 3 | Exclusión de secretos en builds y montajes innecesarios | Pendiente |
| PR 4 | Exportación NotebookLM con fuentes/destinos seguros | Pendiente |

Las PRs siguientes actualizan esta spec y su plan antes de implementar su fase.
Revisar diagnósticos restantes dentro de la entrega relacionada o una PR propia
si el hallazgo es independiente. Cada PR parcial usa Part of #110. Integrar una
entrega y actualizar desde main antes de empezar la siguiente. No implementar
las fases pendientes como parte de PR 1.

## Baseline y tracking

#108 integra migración Linux/Docker y #115; #107 cerrada. #88 y #114 separados.
DevExpert no se opera en real (D025); adaptadores conservados con tests mocks.
El incidente original está en docs/agent-secrets-protection-draft.md. No volver
a leer la clave ni declarar rotación no verificada.

## Requisitos de la primera reparación

- Limpieza down/stop consulta metadatos con --no-env-resolution y
  --no-interpolate antes de seleccionar el nombre. No captura configuración
  expandida ni carga valores de env_file en la salida. Conserva resolución de
  identidad de Compose, overrides, detección de residuales, alias y volúmenes.
- No devolver stdout/stderr arbitrarios de comandos Docker en limpieza.
  Errores reportan operación y exit code; residuales reportan estado sin volcado.
- Chat y STT no leen ni devuelven cuerpos HTTP fallidos ni razones de red.
  Mostrar proveedor y código HTTP upstream cuando exista; mantener 502/504.
  Suprimir cadenas de excepciones que podrían reintroducir detalles en trazas.
- Proveedor inválido no devuelve el valor recibido. Éxitos y contratos API,
  memoria de proceso, configuración y cliente permanecen iguales.
- Log WARNING por fallo con JSON de campos permitidos: evento, proveedor,
  operación chat/stt, categoría y código HTTP upstream opcional validado.
  Campos desconocidos se sustituyen por unknown. No recibir ni registrar body,
  excepción, claves, URLs, headers, modelos arbitrarios, conversación, audio o
  session_id. Sin exc_info/stack_info y sin archivos persistentes nuevos;
  usar logging estándar del proceso (stderr con configuración habitual).
  Es minimización previa, no redacción posterior de texto libre ni hash de claves.
- Añadir canarios ficticios en Docker simulado, errores HTTP/red/timeout/JSON,
  configuración inválida, trazas y respuestas de endpoints reales con HTTP mock.
  Al fallar el harness imprime solo caso/resultado, nunca el valor.

## Límites de esta entrega

Compose todavía genera un modelo estructural internamente, pero sin resolver
los env_file ni interpolar valores. No elimina el comando config ni garantiza
seguridad de literales secretos introducidos en YAML: las configs públicas no
deben contener credenciales. Otros comandos Docker, logs, acceso directo,
setup/tests que heredan .env y build/export permanecen como seguimiento.
Los logs de fallos chat/STT de esta entrega sí están acotados; logs de otros
componentes/herramientas no quedan cubiertos por esa garantía.
No presentar esta mejora como aislamiento ni sanitización universal del host.
No se cambia la fuente de credenciales ni se introducen dependencias.

## Aceptación

Tests de limpieza cubren errores, residuales, alias, proyecto personalizado y
canarios sin salidas crudas. Tests chat/STT cubren ambos adaptadores, trazas,
endpoints y códigos, sin credenciales ni llamadas reales. Suite Python completa,
sintaxis Bash y diff check pasan. Sin cambios web/UI no se exige demo física
para este parche; registrar cualquier verificación que no pudo ejecutarse.

## Operación segura y respuesta a incidentes

No ejecutar dumps de Compose/inspect/env, trazas shell ni lecturas de secretos
para investigar. .env.example sigue público; .env.* reales no. El humano rota
credenciales y gestiona copias/historiales; registrar solo superficie/fecha/tipo.
