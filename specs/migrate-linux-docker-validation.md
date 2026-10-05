# Validación de Migración a Linux y Docker (Bash)

Este documento sirve como registro y checklist para las validaciones en las diferentes fases de la transición de scripts `.ps1` a Bash y Docker.

## Nueva pasada integral — 2026-10-05 (#107)

Spec: `specs/post-migration-stability-validation.md`. Plan emparejado en
`docs/plans/post-migration-stability-validation-implementation-plan.md`.
Código auditado: `49a67b65be0a549fb7513c8797f0d28597f68be2`.
Los puntos históricos posteriores se conservan como evidencia anterior.
Esta tabla es la aceptación vigente; no hereda sus estados COMPLETADO.

| Punto | Estado actual | Evidencia de nueva ejecución |
| --- | --- | --- |
| 1. Backend + web | COMPLETADO | `./tonto.sh dev all`: Uvicorn 8000 y Vite 7.3.3 en 443 ms. Health `{"status":"ok"}` HTTP 200; web HEAD HTTP 200. `/chat` real HTTP 200, 2.244706 s, `{"success":true,"response_text":"¡Ok! ¿Tienes alguna pregunta?"}`. Cuerpo `{}` devuelve HTTP 422 con campos session_id/message obligatorios. |
| 2. Limpieza básica | FALLIDO | `./tonto.sh down`, exit 0, elimina backend/web pero `Network ... Resource is still in use`. `docker compose ps --all` conserva dos ui-emulator one-off activos desde hace dos horas. `ss -ltnp`: 8000/5173 libres. Ver P-107-01. |
| 3. Cliente host + UI Linux | FALLIDO | `./tonto.sh dev backend`; `.venv/bin/python client/main.py --mode text` con TONTO_BACKEND_URL local y tres entradas estrella/Sol/despedida: 3 respuestas coherentes, exit 0. Host sin espeak degrada a texto. Smoke `docker compose run --rm ui-emulator .venv/bin/python -c 'from client.main import speak; speak("Validación de voz Linux")'`: exit 1, FileNotFoundError powershell. Ver P-107-02. |
| 4. Limpieza host | FALLIDO | Segunda ejecución `./tonto.sh down`, exit 0; backend eliminado, red todavía en uso por emuladores previos. Ver P-107-01. |
| 5. Raspberry real | COMPLETADO | Reintento por IP 192.168.1.183 con identidad SSH verificada: preflight exit 0, health LAN OK, USB disponible, 3/3 turnos reales con transcript correcto, continuidad y TTS. Cliente exit 0; backend 3 POST /chat/audio HTTP 200. Operador confirma «si, todo correcto». Detalle en Revalidación Raspberry encendida; mDNS sigue fallando P-107-03. |
| 6. Limpieza Raspberry | FALLIDO | Cliente y procesos audio Raspberry terminan, sin python/arecord/espeak residuales; down exit 0 elimina backend, LAN health falla como esperado (curl exit 7), 8000/5173 libres. Persisten dos emuladores previos y red en uso: P-107-01. |
| 7. Setup/tests/build | FALLIDO | Setup exit 0 pero venv host no se crea (ensurepip ausente) y caché pip deshabilitada. Tests antes/después de setup: 78 Python + 24 UI + web pasan, exit 0. Build repetido tras setup: typecheck + 43 módulos Vite, 1.18 s, exit 0. npm audit completo exit 1, siete vulnerabilidades; producción audit omit-dev exit 0, cero. Ver P-107-05/06/07. |
| 8. Auxiliares/docs | FALLIDO | `bash -n` por cada tonto.sh/scripts/*.sh exit 0; exportador y instalador hook exit 0. Helper apagado: Health unavailable; start/status/health/stop exit 0; status final Health unavailable. Helper Raspberry preflight/exec y demo-raspberry.sh pasan en hardware real. Runbooks desalineados P-107-04; demo-touch físico excluido en #88. |
| 9. CI remoto | COMPLETADO | Push a rama documental. Run 37302071237 sobre SHA 2c2757e11f0ae2fc3a72ed7a1bc45cb193e17bf2: completed/success; setup, checks y build success. Cambios posteriores solo añaden evidencias documentales; consultar checks de PR para su SHA final. |

Ampliaciones pendientes: setup reproducible, micrófono/WAV/auto-stop/speech web
en navegador, voz Raspberry y audibilidad, smoke real por proveedor, CORS,
aislamiento venv/caches, auxiliares y cobertura Kivy. Los tests con mocks no
equivalen a aceptación de audio real.

### Registro de Problemas — pasada #107

- **P-107-01 — ABIERTO, limpieza incompleta:** `down` devuelve 0 aunque quedan
  `tonto-kids-assistant-ui-emulator-run-9fa66213b28a` y
  `tonto-kids-assistant-ui-emulator-run-a6c50a5e1812` y la red no se elimina.
  Son anteriores a esta pasada; no se detuvieron ni se eliminaron manualmente.
  Impacto: no cumple limpieza total; backend/web sí liberan sus puertos.
- **P-107-02 — ABIERTO, TTS Linux del emulador roto:** Compose configura
  TONTO_AUDIO_MODE=pc; `client/main.py:376` ejecuta powershell/System.Speech
  ausente de la imagen Linux. Smoke exit 1 con traceback FileNotFoundError.
  La suite UI simula audio/TTS y por sí sola no prueba esta integración.
- **P-107-03 — DESBLOQUEADO PARCIALMENTE:** reintento con Raspberry encendida:
  tonto-pi.local falla alternativamente con No route to host y resolución DNS.
  Acceso por 192.168.1.183 funciona; la clave ed25519 coincide exactamente con
  la entrada ya confiada de tonto-pi.local. Se usa HostKeyAlias=tonto-pi.local y
  StrictHostKeyChecking=yes, sin cambiar known_hosts ni scripts. Preflight real
  y health LAN pasan. Batería de voz 3/3 completada; el nombre mDNS sigue fallando
  y queda como problema abierto de direccionamiento, no como bloqueo de voz.
- **P-107-04 — ABIERTO, documentación operacional desalineada:**
  `docs/demo-runbook.md` y `docs/demo-checklist.md` siguen indicando Windows,
  scripts dev.ps1/agent-backend.ps1 y que no se carga .env; tonto.sh sí crea
  .env y Compose lo carga. `scripts/demo-touch.sh` aconseja dev.ps1 en error.
  Impacto: demo Linux no reproducible siguiendo esas instrucciones.

No se ha corregido código ni configuración. No procede declarar versión estable.

### Evidencias ampliadas y nuevos problemas

- CORS: `curl -i -X OPTIONS http://127.0.0.1:8000/chat` con Origin
  `http://127.0.0.1:5173` y método POST devuelve HTTP 200,
  `access-control-allow-origin: http://127.0.0.1:5173`, métodos GET/POST.
- Proveedor real activo: OpenAI. Comprobación sanitizada desde contenedor:
  `openai_key_present True`, `devexpert_key_present False`; smoke DevExpert real
  PENDIENTE por credencial ausente. Sus adaptadores sí están en tests simulados.
- **P-107-05 — ABIERTO, entorno host degradado tras setup:** setup recrea .venv
  pero falla `python3 -m venv`: ensurepip ausente; recomienda python3.12-venv.
  Wrapper continúa y devuelve 0. El CLI host funcionaba antes del setup;
  después no puede darse por reproducible su entorno de dependencias.
  No se instalaron paquetes de sistema ni se reparó el entorno.
- **P-107-06 — ABIERTO, caché pip fuera del repo:** setup advierte
  `WARNING: The directory '/.cache/pip' ... is not owned or is not writable ...
  The cache has been disabled`. Contenedor: HOME=/, uid=1000, PIP_CACHE_DIR=None.
  Compose web configura npm_config_cache=/tmp/.npm; no es caché .cache local.
- **P-107-07 — ABIERTO, auditoría de dependencias de desarrollo:**
  `docker compose run --rm web npm audit --json`: exit 1; 2 low (@babel/core,
  esbuild), 1 moderate (baseline-browser-mapping), 4 high (browserslist,
  nanoid, postcss, vite). `npm audit --omit=dev --json`: cero, exit 0.
  Es un reporte del registry, no evidencia de explotación: algunos advisories
  afectan Windows. Requiere valorar aplicabilidad antes de aceptar riesgo.
  No se ejecutó npm audit fix ni se modificó el lockfile.
- **P-107-08 — ABIERTO, backend inaccesible por defecto desde emulador:**
  Con backend saludable, smoke urllib desde ui-emulator imprime
  `backend-service 200` para http://backend:8000/health; después exit 1,
  `urllib.error.URLError: <urlopen error [Errno 111] Connection refused>` para
  http://127.0.0.1:8000/health. UI usa loopback por defecto y Compose no configura
  TONTO_BACKEND_URL; loopback corresponde al propio contenedor.
- Web navegador integrado: pregunta «¿Qué es una estrella?» pasa de Pensando
  a Listo y muestra respuesta educativa; Actividad registra Respuesta recibida
  y Speech no disponible. Fallback texto COMPLETADO en este navegador; speech
  audible PENDIENTE en navegador compatible. Captura de voz iniciada; pendiente.
- Warnings tests: Starlette/httpx deprecation (Python/UI) e imghdr de Kivy;
  registrados sin introducir nuevas dependencias.

### Resultado web real y cierre de auxiliares

En navegador integrado, 2026-10-05 13:16–13:18 Europe/Madrid:

1. Chat de texto: pregunta estrella → Pensando → respuesta visible → Listo.
2. Escuchar: Solicitando permiso → Grabando audio → Tiempo maximo alcanzado.
3. Enviar voz: Voz preparada en WAV → Transcripcion recibida → Respuesta
   educativa lista. Transcript visible: `Hola tonto.`; respuesta visible:
   `¡Hola! ¿Cómo estás? Si tienes alguna pregunta o algo que quieras saber,
   ¡aquí estoy para ayudar!`.
4. Estado final Error, `Speech synthesis failed`. No se confirmó audibilidad.

Captura, auto-stop, WAV, STT y respuesta real COMPLETADO en esta pasada;
contador durante captura no observado, repetibilidad de tres turnos y speech
audible PENDIENTE. No se atribuye fallo de backend al error speech.

- **P-107-09 — LIMITACIÓN DE ENTORNO ABIERTA:** speech del navegador integrado
  no disponible en texto y falla en turno de voz. Repetir en navegador compatible
  con confirmación humana de audibilidad para decidir si existe fallo de producto.
- Exportador: `Exported NotebookLM source files to .../exports/notebooklm`,
  exit 0. Hook: `Installed pre-commit hook at .../.git/hooks/pre-commit`, exit 0;
  también ejecutado correctamente por cada commit documental.
- Helper backend: start `Backend started successfully`, health/status
  `Health: ok (http://127.0.0.1:8000/health)`, stop `Backend stopped`, exit 0;
  status posterior `Health: unavailable`, exit 0.
- Limpieza final: backend/web detenidos, dos emuladores previos siguen activos;
  red en uso. No se borraron volúmenes ni se corrigieron scripts.
- CI primer push: SHA `2c2757e11f0ae2fc3a72ed7a1bc45cb193e17bf2`, run
  https://github.com/joseluisillana/tonto-kids-assistant/actions/runs/37302071237,
  resultado final `completed/success`, Project checks success; setup 40 s,
  checks 37 s y build 2 s, fin 13:19:41 Europe/Madrid.

### Dictamen de esta pasada

No apto todavía para cierre estable. Arranque/API, suites, build, exportador,
hook y ciclo helper backend pasan. Permanecen fallos de limpieza, TTS y URL
del emulador, setup host, caches y documentación. La auditoría npm requiere
triage. Raspberry real y tres turnos de voz quedan completados tras el reintento.
Contador web durante captura, audibilidad web y smoke DevExpert con credencial
siguen pendientes.
Touch/kiosk físico queda excluido en #88. Continuar sin corregir producto hasta
completar pendientes o documentar su bloqueo; después planificar mitigaciones
en trabajo separado y revalidar. #107 permanece abierta.

**Cualquier problema encontrado durante estas pruebas se dejará evidenciado aquí y NO se resolverá de manera inmediata.** Una vez estén todas las evidencias, se decidirá el plan de mitigación.

### Revalidación Raspberry encendida — 2026-10-05

Rama local `docs/post-migration-stability-validation`, checkout limpio al inicio.
Backend Docker arrancado con `./scripts/agent-backend.sh start`, exit 0,
`Backend started successfully`. URL LAN http://192.168.1.91:8000.

El helper oficial se ejecuta en Bash con una función de shell que añade
`-o HostKeyAlias=tonto-pi.local -o StrictHostKeyChecking=yes` a SSH, usando
TONTO_PI_HOST=192.168.1.183. Solo resuelve direccionamiento y conserva la
verificación de la identidad ya confiada; no modifica configuración persistente.

Preflight con TONTO_BACKEND_URL LAN: exit 0:

```text
== identity ==
tonto-pi
tonto-pi-user
== repository ==
/home/tonto-pi-user/tonto-kids-assistant
## feature/issue-84-face-design...origin/feature/issue-84-face-design
== tools ==
/usr/bin/git /usr/bin/python3 /usr/bin/curl
/usr/bin/arecord /usr/bin/aplay /usr/bin/espeak
== python environment ==
Python 3.13.5
/home/tonto-pi-user/tonto-kids-assistant/.venv/bin/python
== backend health ==
Checking http://192.168.1.91:8000/health
{"status":"ok"}
```

Revisión Raspberry: `cc7497a5f98c9a04756a20ce563e9d70baa3d43a`, sin cambios
locales. SHA256 client/main.py coincide con host:
`45b98e705dd1a232f57ee213948626c492ebc10517ea4d7e1e190fee49b25183`.
El script demo-raspberry.sh difiere: remoto
`168e1c00206a5f914854ac932eb1d62cde7db099977e87abeb0314495bf75cc6`, host
`f65ac0c6640e94c54b077f9e124767ee0d43fcfa0880d3b955d8eeefd49c8362`.
No se actualizó el checkout remoto durante la auditoría.

`arecord -l`: card 1 Device, USB PnP Sound Device, device 0 USB Audio,
subdevice disponible 1/1. `aplay -l`: card 0 bcm2835 Headphones y card 2 vc4hdmi.

Se lanza el helper `exec` con tres avisos espeak y entradas Enter a
`./scripts/demo-raspberry.sh`, TONTO_RECORD_SECONDS=6, separación 40 s entre
avisos. Inicio correcto y sesión `local-session-7ceda59d-08c9-4ec4-a783-282b6106451f`.
Turnos completados, helper/cliente exit 0. La inspección del script remoto
confirma que la diferencia respecto al actual es el mensaje de ayuda en caso
de backend caído (dev.ps1 frente a tonto.sh); el arranque y loop utilizados
coinciden. No se valida un checkout remoto actualizado completo.

| Turno | Transcript real | Respuesta de TONTO |
| --- | --- | --- |
| 1 | ¿Qué es una estrella? | ¡Hola! Una estrella es un gran bola de gas que brilla en el cielo. Por ejemplo, el Sol es una estrella y nos da luz y calor. ¿Tienes otra pregunta? |
| 2 | ¿Y el sol? | El Sol es una estrella que está muy cerca de nosotros, y es el centro de nuestro sistema solar. Sin el Sol, no tendríamos luz ni calor en la Tierra, ¡como un gran foco del cielo! ¿Te gustaría saber algo más? |
| 3 | Gracias. Hasta luego. | ¡De nada! ¡Hasta luego! Si alguna vez tienes más preguntas, aquí estaré. ¡Cuídate! |

Cada turno registra `Listening for 6s`, contador 1/6s hasta 6/6s,
`Listening complete`, `Processing`, `Transcript` y `TONTO`; vuelve al prompt.
La entrada final exit cierra el proceso con código 0. No aparecen errores TTS.
Operador confirma audibilidad de avisos y respuestas: **«si, todo correcto»**.
No se midió latencia HTTP por turno: no se infieren cifras de la separación
de 40 s del guion; solo se acredita finalización de los tres turnos.

Logs Docker (`docker compose logs --since 5m --no-color backend`):

```text
192.168.1.183:48058 - "GET /health HTTP/1.1" 200 OK
192.168.1.183:47110 - "POST /chat/audio HTTP/1.1" 200 OK
192.168.1.183:36230 - "POST /chat/audio HTTP/1.1" 200 OK
192.168.1.183:54086 - "POST /chat/audio HTTP/1.1" 200 OK
```

Punto 6: `./tonto.sh down` exit 0, backend retirado, red `Resource is still in use`.
`docker compose ps --all` conserva únicamente los dos emuladores anteriores.
`ss -ltnp` confirma 8000/5173 libres. Desde Raspberry, inventario
`ps -eo pid,comm,args` filtrado por python/python3/arecord/espeak no muestra
procesos; curl LAN posterior falla con `BACKEND_AFTER_DOWN_EXIT=7`, esperado.
No se detuvieron procesos ajenos ni se borraron volúmenes. Backend queda parado
por la prueba explícita de limpieza; no se ejecutó UI touch ni kiosk.

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
- `scripts/export-docs-for-notebooklm.sh`: Exportó correctamente a `exports/notebooklm/`. Código `0`. Salida: `Exported NotebookLM source files to /home/jose/projects/tonto-kids-assistant/exports/notebooklm`
- `scripts/install-git-hooks.sh`: Instaló el hook en `.git/hooks/pre-commit`. Código `0`. Salida: `Installed pre-commit hook at /home/jose/projects/tonto-kids-assistant/.git/hooks/pre-commit`
- `scripts/agent-backend.sh`:
  - `status`: Informa `Health: unavailable` cuando está apagado, y `Health: ok (http://127.0.0.1:8000/health)` cuando está encendido.
  - `start`: `[+] up 1/1 ... Backend started successfully.` Código `0`.
  - `health`: `Health: ok (http://127.0.0.1:8000/health)` Código `0`.
  - `stop`: `[+] stop 1/1 ... Backend stopped.` Código `0`.

## 9. Validación de CI Remota (GitHub Actions)

**Objetivo:** Subir un pequeño cambio a la rama remota (`chore/migrate-linux-docker`) y verificar en la pestaña "Actions" de GitHub que el pipeline arranca usando `./tonto.sh setup / test / build` y termina correctamente (verde).
**Evidencia/Status:** **COMPLETADO**
- Tras realizar los commits de actualización de este documento de validación, se hizo push a la rama `chore/migrate-linux-docker`.
- La GitHub Action ejecutó exitosamente el pipeline pasando todos los tests y builds, finalizando con status verde en unos ~54s (ID referencial comprobado vía `gh run list`).
- Todos los fallos anteriores (incluido Issue #100 y problemas de caché npm) están superados.

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
