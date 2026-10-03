# Plan de Ejecución: Migración a scripts Linux/Docker

## Fase Actual: ANÁLISIS (DRAFT)

**Estado:** 🟡 ESPERANDO "GO" PARA EJECUCIÓN.
*(Spec validada incluyendo infraestructura paralela, CI, hooks y documentación).*

### Fases de Implementación:

**FASE 1: Infraestructura Paralela (Docker y CLI)**
*(Regla: No borrar nada existente)*
- Crear `docker-compose.yml` en la raíz (servicios `backend` y `web`, soporte `.env`, mapeo de puertos y volúmenes).
- Crear el CLI principal `tonto.sh` con los comandos (`setup`, `dev`, `test`, `build`).
- Crear las alternativas en Bash para los scripts auxiliares: `scripts/agent-backend.sh`, `scripts/agent-raspberry.sh`, `scripts/export-docs-for-notebooklm.sh` y `scripts/install-git-hooks.sh`.

**FASE 2: Migración de CI y Hooks**
- Actualizar o clonar la lógica de `.github/workflows/ci.yml` para que no dependa de `pwsh` y en su lugar ejecute `./tonto.sh setup`, `./tonto.sh test all` y `./tonto.sh build all`. (Idealmente corriendo sobre Docker en la pipeline).
- Actualizar la lógica del pre-commit hook (a través del nuevo `install-git-hooks.sh`) para asegurar que ya no busque `pwsh`.

**FASE 3: Actualización de Documentación (Crítico para Agentes)**
- Actualizar `AGENTS.md` para instruir el uso exclusivo de `tonto.sh` y los nuevos comandos Bash (y contenedores) en sustitución del entorno Windows nativo.
- Ajustar referencias en `README.md` y otras especificaciones donde se mencionen comandos de PowerShell.

**FASE 4: Validación General**
- Comprobar localmente que `./tonto.sh dev all`, `tonto.sh test all` y demás scripts auxiliares funcionan 100% como sus homólogos de PowerShell.

**FASE 5: Limpieza de Artefactos (Último paso, sin excepciones)**
- Una vez completado y validado todo lo anterior, proceder a eliminar permanentemente del repositorio todos los ficheros `*.ps1`.

*El plan permanecerá aquí. Esperando instrucción del usuario para comenzar la FASE 1.*
