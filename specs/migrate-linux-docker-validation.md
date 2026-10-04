# Validación de Migración a Linux y Docker (Bash)

Este documento sirve como registro y checklist para las validaciones en las diferentes fases de la transición de scripts `.ps1` a Bash y Docker.

**Cualquier problema encontrado durante estas pruebas se dejará evidenciado aquí y NO se resolverá de manera inmediata.** Una vez estén todas las evidencias, se decidirá el plan de mitigación.

---

## 1. Arranque en local del Backend y Web (Test Básico)

**Objetivo:** Verificar que ambos servicios arrancan localmente sin errores en la máquina host a través de los contenedores Docker mediante el nuevo wrapper `tonto.sh dev all`.
**Evidencia/Status:** **COMPLETADO**
- Comando ejecutado: `./tonto.sh dev all`
- Salida del backend:
  ```text
  backend-1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
  backend-1  | INFO:     Started server process [8]
  backend-1  | INFO:     Application startup complete.
  ```
- Salida del cliente web:
  ```text
  web-1      |   VITE v7.3.3  ready in 923 ms
  web-1      |   ➜  Local:   http://localhost:5173/
  web-1      |   ➜  Network: http://172.19.0.2:5173/
  ```
- Verificación de conectividad:
  - `curl -s http://127.0.0.1:8000/health` -> `{"status":"ok"}`
  - `curl -I -s http://127.0.0.1:5173/` -> `HTTP/1.1 200 OK`

## 2. Parada y Limpieza de Entornos (Tras Test Básico)

**Objetivo:** Verificar que los contenedores se detienen y se eliminan correctamente, dejando los puertos libres.
**Evidencia/Status:** **COMPLETADO**
- Comando ejecutado: `docker compose down` (nota: `tonto.sh` no dispone de subcomando `down`/`stop`).
- Resultado:
  ```text
  ✔ Container tonto-kids-assistant-backend-1 Removed
  ✔ Container tonto-kids-assistant-web-1     Removed
  ✔ Network tonto-kids-assistant_default     Removed
  ```
- Verificación: `docker compose ps` muestra 0 contenedores y los puertos 8000 y 5173 quedan liberados.

## 3. Arranque Backend + UI Cliente Raspberry (Host Local)

**Objetivo:** Levantar el backend en Docker (`tonto.sh dev backend`) y correr el cliente físico simulado en la misma máquina o la interfaz Touch UI, verificando la conexión a `localhost`/`127.0.0.1`.
**Evidencia/Status:** **FALLIDO** (Conexión exitosa, pero fallos en entorno y ejecución)
- Comando ejecutado para backend: `./tonto.sh dev backend` -> Arrancó correctamente en `http://0.0.0.0:8000`.
- Intento de ejecución del cliente con el entorno virtual del proyecto:
  `TONTO_BACKEND_URL=http://127.0.0.1:8000 .venv/bin/python client/main.py --mode text`
  - **Error:** `bash: línea 1: .venv/bin/python: No existe el archivo o el directorio`
  - **Causa:** `.venv` fue creado dentro del contenedor Docker (`python:3.12-slim`), por lo que su symlink apunta a `/usr/local/bin/python`, ruta inexistente en el host Linux (donde Python reside en `/usr/bin/python3`).
- Intento alternativo con el Python del sistema en el host:
  `printf "hola\nexit\n" | TONTO_BACKEND_URL=http://127.0.0.1:8000 python3 client/main.py --mode text`
  - **Resultado:** El cliente se conectó a `http://127.0.0.1:8000/chat`, pero el backend respondió con error 500:
    `Backend error (500). Please try again.`
  - **Causa:** En el backend, `OPENAI_API_KEY` no está configurada en `.env` (el archivo `.env` está vacío por defecto), lo que provoca una excepción en `call_openai()`.

## 4. Parada y Limpieza (Tras Test Cliente Host)

**Objetivo:** Detener servicios sin dejar procesos huérfanos.
**Evidencia/Status:** **COMPLETADO**
- Comando ejecutado: `docker compose down`
- Verificación: `docker compose ps` y `ps aux | grep -E "uvicorn|main.py"` confirmaron 0 contenedores y 0 procesos residuales.

## 5. Arranque Backend + Raspberry Pi Real (Batería de Preguntas)

**Objetivo:** Levantar el backend (`tonto.sh dev backend`), comprobar la visibilidad en red LAN (`0.0.0.0:8000`), conectar el cliente de la Raspberry Pi de verdad y ejecutar una batería de preguntas para validar el Audio Loop en la nueva infraestructura de red.
**Evidencia/Status:** **FALLIDO** / **BLOQUEADO**
- En `docker-compose.yml`, los puertos están correctamente expuestos en `0.0.0.0:8000`.
- Ejecución de preflight del agente Raspberry: `./scripts/agent-raspberry.sh preflight`
  - **Error:** `Dedicated SSH key not found at /home/jose/.ssh/tonto_agent_ed25519.`
  - **Causa:** En el entorno local de ejecución no se dispone de la clave privada SSH ni de conectividad configurada hacia el hardware físico Raspberry Pi, impidiendo ejecutar la batería de pruebas de voz automatizadas.

## 6. Parada y Limpieza (Tras Test Raspberry)

**Objetivo:** Verificar cierre limpio desde la red y liberación de recursos en el host.
**Evidencia/Status:** **COMPLETADO**
- Verificación: No quedaron servicios ni contenedores activos tras el intento (`docker compose ps` limpio).

## 7. Validación de Scripts CLI Adicionales (`build`, `test`)

**Objetivo:** Validar que los comandos paralelos de CI/desarrollo funcionen. Ejecutar:
- `./tonto.sh test all` (Python pytest + Web tests)
- `./tonto.sh build all` (Construcción del cliente web)
**Evidencia/Status:** **COMPLETADO**
- **Test all:** `./tonto.sh test all`
  - Chequeo de sintaxis Python: `Python syntax OK`
  - Pytest: `78 passed, 1 warning in 0.40s` (warning menor de StarletteDeprecationWarning)
  - Tests Web: `web tests passed` (`tsc -p tsconfig.test.json && node tests/run-tests.mjs`)
  - Código de salida: `0`
- **Build all:** `./tonto.sh build all`
  - `tsc --noEmit && vite build`
  - `✓ built in 1.75s` (generó `dist/index.html` y bundles)
  - Código de salida: `0`

## 8. Validación de Scripts Auxiliares de Agentes y Docs

**Objetivo:** Comprobar que los nuevos scripts Bash reemplazan funcionalmente a los antiguos sin dar error:
- Ejecución de `scripts/export-docs-for-notebooklm.sh` y `install-git-hooks.sh`
- Ejecución simulada de los helpers de agente: `scripts/agent-backend.sh status`, etc.
**Evidencia/Status:** **COMPLETADO**
- `scripts/export-docs-for-notebooklm.sh`: Exportó correctamente toda la documentación a `exports/notebooklm/` (`INDEX.md` y `NOTEBOOKLM_COMBINED.md`). Código de salida `0`.
- `scripts/install-git-hooks.sh`: Instaló el hook ejecutable en `.git/hooks/pre-commit`. Código de salida `0`.
- `scripts/agent-backend.sh`:
  - `status`: Informa estado de contenedor y `Health: unavailable` con backend apagado. Código `0`.
  - `start`: Levanta el backend con `docker compose up -d backend`, espera a que responda `{"status":"ok"}` y reporta `Backend started successfully.`. Código `0`.
  - `health`: Reporta `Health: ok (http://127.0.0.1:8000/health)`. Código `0`.
  - `stop`: Detiene y remueve el contenedor limpiamente con `docker compose stop/rm`. Código `0`.

## 9. Validación de CI Remota (GitHub Actions)

**Objetivo:** Subir un pequeño cambio a la rama remota (`chore/migrate-linux-docker`) y verificar en la pestaña "Actions" de GitHub que el pipeline arranca usando `./tonto.sh setup / test / build` y termina correctamente (verde).
**Evidencia/Status:** **FALLIDO** / **BLOQUEADO** (Configuración de workflow)
- Al inspeccionar `.github/workflows/ci.yml`:
  ```yaml
  on:
    push:
      branches:
        - main
    pull_request:
    workflow_dispatch:
  ```
- **Hallazgo:** El trigger `push` en GitHub Actions está configurado única y exclusivamente para la rama `main`.
- Se realizó el commit `d7b45cb` y push a `origin/chore/migrate-linux-docker` con éxito.
- Al consultar la API de GitHub Actions (`/repos/.../actions/runs`), se confirmó que ningún workflow fue disparado (`total_count: 135`, sin nuevos runs iniciados).
- Para que la CI corra en ramas secundarias, se requiere abrir un Pull Request contra `main`, añadir ramas a `push.branches` en `ci.yml`, o disparar manualmente vía `workflow_dispatch`.
- Siguiendo la regla de no modificar código antes de consolidar el registro, se documenta la limitación sin alterar `ci.yml`.

---

### Registro de Problemas (Issue Log)

1. **Incompatibilidad del `.venv` entre el Contenedor y el Host:**
   - **Descripción:** `tonto.sh setup` crea `.venv` dentro del contenedor montado. En la imagen base `python:3.12-slim`, Python está en `/usr/local/bin/python`. Por ello, los symlinks de `.venv/bin/python` apuntan a una ruta inexistente en el host Linux (donde está en `/usr/bin/python3`). Esto impide que scripts o comandos en el host usen `.venv/bin/python` directamente.
2. **Falta de comando de parada/limpieza en `tonto.sh`:**
   - **Descripción:** `tonto.sh` cuenta con `setup`, `dev`, `test` y `build`, pero carece de un comando como `stop` o `down`. El usuario debe invocar manualmente `docker compose down` para limpiar contenedores y redes.
3. **Ausencia de clave de inferencia en `.env`:**
   - **Descripción:** Al iniciar el backend con `.env` vacío, cualquier llamada al endpoint `/chat` arroja un error 500 (`OPENAI_API_KEY is not set`), haciendo fallar las pruebas interactivas del cliente si no se configuran credenciales válidas o un modo de prueba/mock.
4. **Validación de Raspberry Pi bloqueada por falta de credenciales SSH:**
   - **Descripción:** La validación contra hardware físico requiere el archivo `/home/jose/.ssh/tonto_agent_ed25519` y una Raspberry Pi accesible en la red, elementos no presentes en el entorno actual de desarrollo.
5. **Configuración de ramas en CI (`ci.yml`):**
   - **Descripción:** El flujo de GitHub Actions no escucha eventos `push` en ramas de tipo `chore/*` o `feature/*`, requiriendo un Pull Request formal o la activación manual para validar en CI remoto antes de mergear a `main`.
6. **Advertencia de sintaxis obsoleta en `docker-compose.yml`:**
   - **Descripción:** Cada ejecución de `docker compose` emite el aviso: `WARN[0000] the attribute 'version' is obsolete, it will be ignored, please remove it to avoid potential confusion`.
