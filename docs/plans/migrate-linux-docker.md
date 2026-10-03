# Plan de Ejecución: Migración a scripts Linux/Docker

## Fase Actual: ANÁLISIS (DRAFT)

**Estado:** 🟡 ESPERANDO VALIDACIÓN FINAL DE LA SPEC Y PLAN.
*(La alternativa ha sido seleccionada: Script Bash + Docker).*

### Pasos pendientes (NO EJECUTAR TODAVÍA):

1. **Resolución del Bloqueo (Completado en análisis):**
   - ~~El usuario debe seleccionar una herramienta.~~ (Seleccionado: Script Bash `tonto.sh`)
   - ~~Verificar la disponibilidad de `docker` en el sistema.~~ (Confirmado por el usuario)

2. **Implementación de Scripts e Infraestructura (Pendiente de tu validación para empezar):**
   - Crear archivo `docker-compose.yml` (y si es necesario `Dockerfile.dev`) para aislar los entornos de Python y Node.
   - Crear el script bash wrapper `tonto.sh` en la raíz.
   - Implementar el comando `./tonto.sh setup` (construcción de imágenes).
   - Implementar el comando `./tonto.sh dev [backend|web|all]` (arranque con docker compose).
   - Implementar el comando `./tonto.sh test [python|web|all]` (ejecución efímera de tests).
   - Implementar el comando `./tonto.sh build [web|all]` (ejecución efímera de build web).

3. **Actualización de Documentación:**
   - Actualizar `AGENTS.md` para enseñar a futuros agentes cómo usar `tonto.sh`.
   - Actualizar el workflow en `README.md` o documentación asociada.

4. **Limpieza y migración de helpers:**
   - Eliminar los ficheros `*.ps1` principales y evaluar la conversión de `agent-backend.ps1` / `agent-raspberry.ps1` a Bash si es necesario para el workflow de agentes.

*El plan permanecerá en este estado de análisis hasta recibir tu confirmación explícita para comenzar a escribir código.*
