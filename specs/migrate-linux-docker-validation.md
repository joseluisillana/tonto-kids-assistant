# Validación de Migración a Linux y Docker (Bash)

Este documento sirve como registro y checklist para las validaciones en las diferentes fases de la transición de scripts `.ps1` a Bash y Docker.

**Cualquier problema encontrado durante estas pruebas se dejará evidenciado aquí y NO se resolverá de manera inmediata.** Una vez estén todas las evidencias, se decidirá el plan de mitigación.

---

## 1. Arranque en local del Backend y Web (Test Básico)

**Objetivo:** Verificar que ambos servicios arrancan localmente sin errores en la máquina host a través de los contenedores Docker mediante el nuevo wrapper `tonto.sh dev all`.
**Evidencia/Status:** *PENDIENTE*

## 2. Parada y Limpieza de Entornos (Tras Test Básico)

**Objetivo:** Verificar que los contenedores se detienen y se eliminan correctamente, dejando los puertos libres.
**Evidencia/Status:** *PENDIENTE*

## 3. Arranque Backend + UI Cliente Raspberry (Host Local)

**Objetivo:** Levantar el backend en Docker (`tonto.sh dev backend`) y correr el cliente físico simulado en la misma máquina o la interfaz Touch UI, verificando la conexión a `localhost`/`127.0.0.1`.
**Evidencia/Status:** *PENDIENTE*

## 4. Parada y Limpieza (Tras Test Cliente Host)

**Objetivo:** Detener servicios sin dejar procesos huérfanos.
**Evidencia/Status:** *PENDIENTE*

## 5. Arranque Backend + Raspberry Pi Real (Batería de Preguntas)

**Objetivo:** Levantar el backend (`tonto.sh dev backend`), comprobar la visibilidad en red LAN (`0.0.0.0:8000`), conectar el cliente de la Raspberry Pi de verdad y ejecutar una batería de preguntas para validar el Audio Loop en la nueva infraestructura de red.
**Evidencia/Status:** *PENDIENTE*

## 6. Parada y Limpieza (Tras Test Raspberry)

**Objetivo:** Verificar cierre limpio desde la red y liberación de recursos en el host.
**Evidencia/Status:** *PENDIENTE*

## 7. Validación de Scripts CLI Adicionales (`build`, `test`)

**Objetivo:** Validar que los comandos paralelos de CI/desarrollo funcionen. Ejecutar:
- `./tonto.sh test all` (Python pytest + Web tests)
- `./tonto.sh build all` (Construcción del cliente web)
**Evidencia/Status:** *PENDIENTE*

## 8. Validación de Scripts Auxiliares de Agentes y Docs

**Objetivo:** Comprobar que los nuevos scripts Bash reemplazan funcionalmente a los antiguos sin dar error:
- Ejecución de `scripts/export-docs-for-notebooklm.sh` y `install-git-hooks.sh`
- Ejecución simulada de los helpers de agente: `scripts/agent-backend.sh status`, etc.
**Evidencia/Status:** *PENDIENTE*

## 9. Validación de CI Remota (GitHub Actions)

**Objetivo:** Subir un pequeño cambio a la rama remota (`chore/migrate-linux-docker`) y verificar en la pestaña "Actions" de GitHub que el pipeline arranca usando `./tonto.sh setup / test / build` y termina correctamente (verde).
**Evidencia/Status:** *PENDIENTE*

---

### Registro de Problemas (Issue Log)

*Ningún problema reportado por el momento.*
