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
- Ajustar referencias en `README.md` y otras especificaciones donde se mencionen comandos de Bash.

**FASE 4: Validación General**
- Comprobar localmente que `./tonto.sh dev all`, `tonto.sh test all` y demás scripts auxiliares funcionan 100% como sus homólogos de Bash.

**FASE 5: Limpieza de Artefactos (Último paso, sin excepciones)**
- Una vez completado y validado todo lo anterior, proceder a eliminar permanentemente del repositorio todos los ficheros `*.ps1`.

*El plan permanecerá aquí. Esperando instrucción del usuario para comenzar la FASE 1.*


## Migration provenance

Original source: `docs/plans/migrate-linux-docker.md` at baseline 818e88e. Relocated 2026-10-06;
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
