# Plan de Ejecución: Migración a scripts Linux/Docker

## Fase Actual: ANÁLISIS (DRAFT)

**Estado:** 🟡 ESPERANDO "GO" PARA EJECUCIÓN.
*(Las decisiones técnicas han sido validadas; la Spec incluye red, volúmenes, `.env` y la limpieza completa de ficheros de PowerShell).*

### Pasos pendientes para la Implementación:

1. **Creación de Infraestructura Docker:**
   - Crear `docker-compose.yml` en la raíz.
   - Configurar los servicios `backend` (Python) y `web` (Node).
   - Añadir soporte para cargar el fichero `.env`.
   - Añadir volúmenes (`./backend:/app/backend`, `./web:/app/web`) para el **Hot Reloading**.
   - Mapear el puerto `8000:8000` en el host (accesible por LAN para la Raspberry Pi) y `5173:5173` para la web.

2. **Creación del CLI Principal (`tonto.sh`):**
   - Crear `tonto.sh` y darle permisos de ejecución.
   - Implementar las subrutinas: `setup`, `dev`, `test`, `build`.

3. **Erradicación de PowerShell y Migración de Scripts Auxiliares:**
   - Eliminar `setup-dev.ps1`, `dev.ps1`, `test.ps1`, `build.ps1`.
   - Convertir `agent-backend.ps1` a `scripts/agent-backend.sh` (usando comandos docker internamente).
   - Convertir `agent-raspberry.ps1` a `scripts/agent-raspberry.sh`.
   - Convertir `export-docs-for-notebooklm.ps1` a bash.
   - Convertir `install-git-hooks.ps1` a bash y actualizar la llamada al pre-commit.
   - *Se eliminarán de forma definitiva todos los archivos `.ps1` del repositorio.*

4. **Actualización de Documentación:**
   - Modificar `AGENTS.md` para instruir a futuros agentes de que deben usar Bash, Docker, y `tonto.sh` (además de los nuevos `.sh`).
   - Ajustar referencias en `README.md` u otros documentos si es necesario.

*El plan permanecerá aquí. Cuando des luz verde, el agente comenzará con el Paso 1 escribiendo los archivos.*
