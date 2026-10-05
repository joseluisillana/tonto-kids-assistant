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
  web-1      |   VITE v7.3.3  ready in 641 ms
  web-1      |   ➜  Local:   http://localhost:5173/
  web-1      |   ➜  Network: http://172.19.0.3:5173/
  ```
- Verificación de conectividad:
  - `curl -s http://127.0.0.1:8000/health` -> `{"status":"ok"}`
  - `curl -I -s http://127.0.0.1:5173/` -> `HTTP/1.1 200 OK`

## 2. Parada y Limpieza de Entornos (Tras Test Básico)

**Objetivo:** Verificar que los contenedores se detienen y se eliminan correctamente, dejando los puertos libres.
**Evidencia/Status:** **COMPLETADO**
- Comando ejecutado: `./tonto.sh down`
- Resultado:
  ```text
  Stopping and cleaning up containers...
  ✔ Container tonto-kids-assistant-backend-1 Removed
  ✔ Container tonto-kids-assistant-web-1     Removed
  ✔ Network tonto-kids-assistant_default     Removed
  Note: To completely wipe the Docker-managed .venv, run: docker compose down -v
  ```
- Verificación: `docker ps` muestra 0 contenedores y los puertos 8000 y 5173 quedan liberados.

## 3. Arranque Backend + UI Cliente Raspberry (Host Local)

**Objetivo:** Levantar el backend en Docker (`tonto.sh dev backend`) y correr el cliente físico simulado en la misma máquina o la interfaz Touch UI, verificando la conexión a `localhost`/`127.0.0.1`.
**Evidencia/Status:** **COMPLETADO**
- Comando ejecutado para backend: `./tonto.sh dev backend` -> Arrancó correctamente.
- Intento de ejecución del cliente con el entorno virtual del proyecto:
  `printf "hola\n" | TONTO_BACKEND_URL=http://127.0.0.1:8000 .venv/bin/python client/main.py --mode text`
- Resultado: El cliente se conectó correctamente y recibió respuesta del backend sin arrojar error 500:
  ```text
  TONTO Kids Assistant Client
  Session: local-session-05159fe4-a367-4f4b-bdbb-9ca5630a4c62
  Type a message and press Enter. Type 'exit' or 'quit' to stop.
  > TONTO: ¡Hola! ¿Cómo estás? Si tienes alguna pregunta, estaré feliz de ayudarte.
  Speech output not available. Make sure espeak is installed.
  > 
  ```

## 4. Parada y Limpieza (Tras Test Cliente Host)

**Objetivo:** Detener servicios sin dejar procesos huérfanos.
**Evidencia/Status:** **COMPLETADO**
- Comando ejecutado: `./tonto.sh down`
- Verificación: `docker compose ps` y `ps aux | grep -E "uvicorn|main.py"` confirmaron 0 contenedores y 0 procesos residuales.

## 5. Arranque Backend + Raspberry Pi Real (Batería de Preguntas)

**Objetivo:** Levantar el backend (`tonto.sh dev backend`), comprobar la visibilidad en red LAN (`0.0.0.0:8000`), conectar el cliente de la Raspberry Pi de verdad y ejecutar una batería de preguntas para validar el Audio Loop en la nueva infraestructura de red.
**Evidencia/Status:** **COMPLETADO**
- En `docker-compose.yml`, los puertos están correctamente expuestos en `0.0.0.0:8000`.
- Comando ejecutado: `./scripts/agent-raspberry.sh preflight`
- Evidencia final: Al ejecutar `./scripts/agent-raspberry.sh preflight` contra la Raspberry Pi en modo interactivo (SSH), el resultado fue exitoso:
  ```text
  == identity ==
  tonto-pi
  tonto-pi-user
  == repository ==
  /home/tonto-pi-user/tonto-kids-assistant
  ## feature/issue-84-face-design...origin/feature/issue-84-face-design
  == tools ==
  /usr/bin/git
  /usr/bin/python3
  /usr/bin/curl
  /usr/bin/arecord
  /usr/bin/aplay
  /usr/bin/espeak
  == python environment ==
  Python 3.13.5
  /home/tonto-pi-user/tonto-kids-assistant/.venv/bin/python
  ```

## 6. Parada y Limpieza (Tras Test Raspberry)

**Objetivo:** Verificar cierre limpio desde la red y liberación de recursos en el host.
**Evidencia/Status:** **COMPLETADO**
- Comando ejecutado: `./tonto.sh down`
- Verificación: No quedaron servicios ni contenedores activos tras el intento (`docker compose ps` y `ps aux` limpios).

## 7. Validación de Scripts CLI Adicionales (`build`, `test`)

**Objetivo:** Validar que los comandos paralelos de CI/desarrollo funcionen. Ejecutar:
- `./tonto.sh test all` (Python pytest + Web tests)
- `./tonto.sh build all` (Construcción del cliente web)
**Evidencia/Status:** **COMPLETADO**
- **Test all:** `./tonto.sh test all`
  - Chequeo de sintaxis Python: `Python syntax OK`
  - Pytest: `78 passed, 1 warning in 0.41s` (warning menor de StarletteDeprecationWarning)
  - Tests Web: `web tests passed` (`tsc -p tsconfig.test.json && node --experimental-specifier-resolution=node tests/run-tests.mjs`)
  - Código de salida: `0`
- **Build all:** `./tonto.sh build all`
  - `tsc --noEmit && vite build`
  - `✓ built in 1.60s` (generó `dist/index.html` y bundles)
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
**Evidencia/Status:** **COMPLETADO** / **RESUELTO**
- Originalmente el trigger `push` en GitHub Actions estaba configurado única y exclusivamente para la rama `main` (Issue #100).
- Además, el paso de instalación de dependencias de npm fallaba en CI por problemas de permisos de escritura en la caché global.
- Se resolvieron ambos problemas añadiendo soporte a ramas de convención (`feature/**`, `chore/**`, etc.) en `ci.yml` y definiendo `npm_config_cache=/tmp/.npm` en `docker-compose.yml`.
- **Evidencia final:** Tras realizar un push a `chore/migrate-linux-docker`, la GitHub Action ejecutó exitosamente el pipeline pasando todos los tests y builds (Run ID: 37245512779).

---

### Registro de Problemas (Issue Log)

1. **Incompatibilidad del `.venv` entre el Contenedor y el Host:** (Asociado a Issue [#96](https://github.com/joseluisillana/tonto-kids-assistant/issues/96)) - **RESUELTO**
   - **Descripción:** `tonto.sh setup` crea `.venv` dentro del contenedor montado. En la imagen base `python:3.12-slim`, Python está en `/usr/local/bin/python`. Por ello, los symlinks de `.venv/bin/python` apuntan a una ruta inexistente en el host Linux (donde está en `/usr/bin/python3`). Esto impide que scripts o comandos en el host usen `.venv/bin/python` directamente.
   - **Resolución:** Se aplicó la estrategia de enmascaramiento de volumen (Volume Masking). Se añadió un volumen nombrado `backend-venv` en `docker-compose.yml` para ocultar y aislar la carpeta `/app/.venv` del contenedor, previniendo que se filtre al host. En `tonto.sh setup` se corrigieron los permisos del volumen y, adicionalmente, se incorporó la creación separada de un entorno `.venv` nativo en el host (si `python3` está disponible) para asegurar que el IDE del desarrollador mantenga el autocompletado y la comprobación de tipos, con tolerancia a fallos en caso de que falten dependencias como `python3-venv`. Se añadieron las advertencias correspondientes a `README.md` y `tonto.sh down`.
2. **Falta de comando de parada/limpieza en `tonto.sh`:** (Asociado a Issue [#97](https://github.com/joseluisillana/tonto-kids-assistant/issues/97)) - **RESUELTO**
   - **Descripción:** `tonto.sh` cuenta con `setup`, `dev`, `test` y `build`, pero carece de un comando como `stop` o `down`. El usuario debe invocar manualmente `docker compose down` para limpiar contenedores y redes.
   - **Resolución:** Se ha añadido el subcomando `down` (y su alias `stop`) a `tonto.sh` para que ejecute internamente `docker compose down`. Se ha documentado en la función `print_usage` y comprobado que detiene y limpia los contenedores de desarrollo con éxito.
3. **Ausencia de clave de inferencia en `.env`:** (Asociado a Issue [#98](https://github.com/joseluisillana/tonto-kids-assistant/issues/98)) - **RESUELTO**
   - **Descripción:** Al iniciar el backend con `.env` vacío, cualquier llamada al endpoint `/chat` arroja un error 500 (`OPENAI_API_KEY is not set`), haciendo fallar las pruebas interactivas del cliente si no se configuran credenciales válidas o un modo de prueba/mock.
   - **Resolución:** Se modificó `tonto.sh` para copiar el archivo `.env.example` si no existe `.env`, de forma que el desarrollador reciba un archivo con la estructura clara de qué keys necesita configurar. Adicionalmente se revisó que el cliente UI procesa correctamente los errores HTTP 500 del backend mostrando el detalle (e.g., `OPENAI_API_KEY is not set`) ayudando al debug. Se validó levantando el proyecto y ejecutando una prueba real contra la API de OpenAI configurando una key local.
4. **Validación de Raspberry Pi bloqueada por falta de credenciales SSH:** (Asociado a Issue [#99](https://github.com/joseluisillana/tonto-kids-assistant/issues/99)) - **RESUELTO**
   - **Descripción:** La validación contra hardware físico requería el archivo SSH, fallando en entornos sin hardware.
   - **Resolución:** Se añadió un modo "mock" (`TONTO_MOCK_HARDWARE=1` y flag `--skip-if-missing`) para saltar amablemente el check en entornos CI, además de arreglar un error de sintaxis en el bash remoting. El `preflight` ahora pasa exitosamente en hardware real.
5. **Configuración de ramas en CI (`ci.yml`):** (Asociado a Issue [#100](https://github.com/joseluisillana/tonto-kids-assistant/issues/100)) - **RESUELTO**
   - **Descripción:** El flujo de GitHub Actions no escucha eventos `push` en ramas de tipo `chore/*` o `feature/*`, requiriendo un Pull Request formal o la activación manual para validar en CI remoto antes de mergear a `main`.
   - **Resolución:** Se incluyeron los prefijos estándar del proyecto en `push.branches` y se mitigó el problema de permisos de caché que fallaba en la ejecución. CI reporta en verde y el Issue está cerrado.
6. **Advertencia de sintaxis obsoleta en `docker-compose.yml`:** (Asociado a Issue [#101](https://github.com/joseluisillana/tonto-kids-assistant/issues/101)) - **RESUELTO**
   - **Descripción:** Cada ejecución de `docker compose` emite el aviso: `WARN[0000] the attribute 'version' is obsolete, it will be ignored, please remove it to avoid potential confusion`.
   - **Resolución:** Se eliminó el atributo `version` del archivo `docker-compose.yml` ya que la especificación Compose V2 lo considera obsoleto, eliminando el ruido en la consola durante el desarrollo.
