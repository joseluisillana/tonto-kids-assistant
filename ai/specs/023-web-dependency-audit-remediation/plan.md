# Plan de cierre P-107-07

Fuente: specs/web-dependency-audit-remediation.md. Autorizado, Part of #107.

1. Leer contexto y gate Git; crear fix/web-dependency-audit desde #108 integrado.
2. Capturar audit/outdated y comprobar advisories y metadata de parches publicados.
3. Previsualizar reparación compatible; aplicar únicamente lockfile salvo que
   se necesite elevar un mínimo del manifest por seguridad. No forzar majors.
4. Revisar diferencias/versiones y npm ls; npm ci limpio, audit completo/omit-dev.
5. Ejecutar comandos oficiales setup/test/build. Usar checkout temporal y
   proyecto Compose propio sin secretos para instalación limpia.
6. Arrancar backend/web oficiales; smoke UI texto/voz. No leer .env ni imprimir
   Compose expandido. Documentar limitaciones de audibilidad aparte.
7. down; actualizar registro, journal y triage. Commit, PR apilada en #108,
   adjuntar evidencia, comprobar CI sin cerrar #107.

## Prompt de handoff

Implementa ai/specs/023-web-dependency-audit-remediation/spec.md en rama fix propia tras
leer AGENTS.md/contexto. Repara P-107-07 mediante actualizaciones compatibles,
sin dependencias directas nuevas ni force. Revisa GHSA y versiones reales,
valida instalación limpia/audit/tests/build/smoke, conserva límites físicos,
registra evidencia y publica PR para revisión. Punto 7 solo se cierra con
criterios cumplidos; no cierres la validación integral ni mezcles otros fallos.


## Migration provenance

Original source: `docs/plans/web-dependency-audit-remediation-implementation-plan.md` at baseline 818e88e. Relocated 2026-10-06;
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
