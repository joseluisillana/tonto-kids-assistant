# Validación integral de estabilidad tras migración Linux/Docker

Fecha: 2026-10-05. Tracking: #107. Rama: `docs/post-migration-stability-validation`.

Nueva pasada final integrada ejecutada sobre 7117313 tras merge #115.
La matriz inicial de specs/migrate-linux-docker-validation.md es ahora vigente;
estados de la pasada anterior abajo son históricos. Nueve puntos COMPLETADOS,
incluidos Chrome/emulador/Raspberry físicos, limpieza y CI c12f377 success.
OK de migración en alcance validado; pendiente revisión/merge #108 en main.
#114 aplazado; mDNS no resuelve pero acceso IP estricto validado.

Estado vigente en la rama de PR #115: nueve puntos COMPLETADOS, voz real y
recuperación del emulador aceptadas; CI 09ef3b3 success. #115 lista para revisión
sin borrador; #108 pendiente de integrar #115 y verificar su CI global.
#107 abierta por integración, no por fallos activos de esta reparación.
P-107-14 aplazado por operador en #114; P-107-15 retirado como bloqueo.
No se declara release publicada ni merge en main; #88 sigue fuera de alcance.

## Objetivo y alcance

Obtener una versión candidata estable del estado actual post-MVP, verificando
Linux, Docker, backend, web, cliente CLI Raspberry y widgets Kivy. El registro
ejecutable y las evidencias viven en `specs/migrate-linux-docker-validation.md`.
La evidencia histórica no constituye una validación de la revisión actual.

Se excluye únicamente la aceptación física touch/OpenGL ES/kiosk de Raspberry
(#88). No se excluyen voz Raspberry, micrófono web ni TTS; si requieren operador
o hardware no disponible quedan pendientes, nunca aprobados por mocks.

## Matriz de ejecución

1. Arranque `./tonto.sh dev all`; health, HTTP web, `/chat` real, contratos
   negativos y CORS. Separar disponibilidad de servicio de proveedor real.
2. `./tonto.sh down`; contenedores, puertos y procesos residuales.
3. `./tonto.sh dev backend`; cliente CLI host con tres turnos relacionados,
   salida limpia y fallback TTS. UI Linux: comprobar configuración efectiva,
   conectividad y dependencias de captura/TTS del emulador.
4. Parada y repetición de controles de limpieza.
5. Backend LAN + preflight real Raspberry; identidad, revisión, audio y health;
   tres turnos de voz, transcript, respuesta, latencia y audibilidad humana.
6. Parada y limpieza tras Raspberry.
7. Setup oficial y `test all` (78 Python + 24 UI esperados como baseline,
   no cuota fija), `build all`; comprobar aislamiento venv, permisos y caches.
8. Sintaxis de todos los Bash, export NotebookLM, instalación hook,
   ciclo start/status/health/stop del helper backend y helpers Raspberry/demo.
9. Push de commits, CI del SHA validado, logs y URL de ejecución con resultado.

Ampliaciones: widgets Kivy reales/Xvfb, regresión de estados/errores/reentrada,
web micrófono/WAV/auto-stop/speech y texto en navegador, OpenAI como proveedor real (tests simulados y smoke real distinguidos), coherencia
de runbooks Linux, limpieza de contenedores one-off y arranque repetible.
Usar suites existentes y fixtures existentes; no añadir dependencias ni tests
de producto durante esta auditoría. No divulgar claves ni `.env`.

## Estados y aceptación

Cada comprobación inicia PENDIENTE; COMPLETADO exige evidencia de sus criterios;
FALLIDO identifica un fallo reproducible. Un bloqueo externo conserva PENDIENTE
con intento y motivo. Cada evidencia indica comando, fecha, revisión, resultado
y salida relevante, con logs sanitizados. Una sección puede contener subchecks
completados y permanecer pendiente por los restantes.

La versión candidata solo se acepta con todas las comprobaciones incluidas
completadas, CI verde del código auditado y cero problemas abiertos bloqueantes.
Los warnings se clasifican, no se ocultan. No prometer estabilidad absoluta ni
crear tag/release mientras existan pendientes o fallos. Las correcciones se
planifican después de la auditoría en ramas separadas y requieren revalidación.

## Restricción de ejecución

No corregir código, scripts, configuración ni runbooks durante la validación.
Registrar problemas y continuar salvo dependencia completamente bloqueante.
Commits documentales tras preparación y grupos de comprobaciones.

Plan: `docs/plans/post-migration-stability-validation-implementation-plan.md`.


## Decisión de alcance — DevExpert, 2026-10-05 (D025)

Por decisión explícita del operador, DevExpert está deprecado y no se operará.
Smoke real DevExpert: NO APLICA, excluido de aceptación de esta pasada. No pedir
credenciales ni considerarlo un bloqueo del cierre. Evidencias/tests existentes
se conservan; no se elimina soporte ni se cambia runtime en esta decisión.
