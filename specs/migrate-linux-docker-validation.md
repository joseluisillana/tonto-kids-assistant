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
| 2. Limpieza básica | COMPLETADO | Fallo inicial conservado en P-107-01; reparación fix/docker-cleanup revalidada: down retira backend/web, dos emuladores previos y red, exit 0; sin contenedores/redes del proyecto y puertos libres. |
| 3. Cliente host + UI Linux | FALLIDO | Arranque reparado y audio físico validado: operador confirma tres turnos completos con DMIC hw:0,7, entrada PortAudio 5. P-107-12 resuelto para esa selección; sigue abierto P-107-13 (captura incompatible deja ESCUCHANDO). Demora del volumen del sistema registrada como P-107-14. |
| 4. Limpieza host | COMPLETADO | Tras reparación: segunda llamada down exit 0 sin residuales; nuevo arranque backend/web HTTP 200 y stop retira servicios, one-off de control y red. Histórico P-107-01. |
| 5. Raspberry real | COMPLETADO | Reintento por IP 192.168.1.183 con identidad SSH verificada: preflight exit 0, health LAN OK, USB disponible, 3/3 turnos reales con transcript correcto, continuidad y TTS. Cliente exit 0; backend 3 POST /chat/audio HTTP 200. Operador confirma «si, todo correcto». Detalle en Revalidación Raspberry encendida; mDNS sigue fallando P-107-03. |
| 6. Limpieza Raspberry | COMPLETADO | Cliente/audio Raspberry ya terminaban y LAN health tras parada fallaba correctamente (curl 7). Reparación del bloqueo Docker revalidada: elimina también emuladores y red, sin residuales ni puertos; conserva dependencias. No se repiten voz ni UI física para este cambio CLI. Histórico P-107-01. |
| 7. Setup/tests/build | COMPLETADO | Setup y cachés reparados en #112; lockfile compatible corregido, instalación limpia exit 0. Audit dev/prod 0 vulnerabilidades, npm ls válido. 97 Python + 24 Kivy + web y build pasan; smokes texto y cliente HTTP de voz contra backend real pasan. Evidencias al final; CI de esta reparación se registra tras finalizar. |
| 8. Auxiliares/docs | COMPLETADO | Helpers previamente validados; guías operativas README/demo/SSH/workflow y planes vigentes actualizados a Bash/Docker/.env. bash -n y git diff --check pasan. demo-touch físico sigue excluido en #88. P-107-04 resuelto. |
| 9. CI remoto | COMPLETADO | Push a rama documental. Run 37302071237 sobre SHA 2c2757e11f0ae2fc3a72ed7a1bc45cb193e17bf2: completed/success; setup, checks y build success. Cambios posteriores solo añaden evidencias documentales; consultar checks de PR para su SHA final. |

Pendientes vigentes: recuperación de errores de captura P-107-13 y evaluación
de demora del volumen P-107-14; documentar selección reproducible del micrófono
sin depender del override temporal. Audio físico del emulador validado.
Smoke DevExpert real: NO APLICA por decisión D025 (deprecado, no operarlo).
Chrome: tres turnos/audibilidad/contador/auto-stop aprobados por el operador;
mDNS y preflight Raspberry por nombre revalidados. Raspberry voz/audibilidad, setup, caches, auditorías,
CORS, auxiliares y cobertura Kivy tienen evidencia completada.
Los tests con mocks no equivalen a aceptación de audio real.

### Registro de Problemas — pasada #107

- **P-107-01 — RESUELTO Y REVALIDADO en fix/docker-cleanup, limpieza incompleta histórica:** `down` devolvía 0 aunque quedaban
  `tonto-kids-assistant-ui-emulator-run-9fa66213b28a` y
  `tonto-kids-assistant-ui-emulator-run-a6c50a5e1812` y la red no se elimina.
  Eran anteriores a esta pasada y se conservaron durante la auditoría.
  Reparación aprobada: down --remove-orphans y verificación posterior por proyecto;
  ahora se retiran mediante el wrapper, incluida red. Evidencias al final.
- **P-107-02 — RESUELTO EN SOFTWARE (audibilidad física pendiente), TTS Linux del emulador roto:** Compose configura
  TONTO_AUDIO_MODE=pc; `client/main.py:376` ejecuta powershell/System.Speech
  ausente de la imagen Linux. Smoke exit 1 con traceback FileNotFoundError.
  La suite UI simula audio/TTS y por sí sola no prueba esta integración.
- **P-107-03 — REVALIDADO POR NOMBRE; incidencia inicial histórica:** reintento con Raspberry encendida:
  tonto-pi.local falla alternativamente con No route to host y resolución DNS.
  Acceso por 192.168.1.183 funciona; la clave ed25519 coincide exactamente con
  la entrada ya confiada de tonto-pi.local. Se usa HostKeyAlias=tonto-pi.local y
  StrictHostKeyChecking=yes, sin cambiar known_hosts ni scripts. Preflight real
  y health LAN pasan. Batería de voz 3/3 completada; el nombre mDNS sigue fallando
  y queda como problema abierto de direccionamiento, no como bloqueo de voz.
- **P-107-04 — RESUELTO; descripción histórica, documentación operacional desalineada:**
  `docs/demo-runbook.md` y `docs/demo-checklist.md` siguen indicando Windows,
  scripts dev.ps1/agent-backend.ps1 y que no se carga .env; tonto.sh sí crea
  .env y Compose lo carga. `scripts/demo-touch.sh` aconseja dev.ps1 en error.
  Impacto: demo Linux no reproducible siguiendo esas instrucciones.

En la auditoría inicial no se corrigió código ni configuración. Las reparaciones
aprobadas posteriores se documentan por separado. No procede declarar versión estable.

### Evidencias ampliadas y nuevos problemas

- CORS: `curl -i -X OPTIONS http://127.0.0.1:8000/chat` con Origin
  `http://127.0.0.1:5173` y método POST devuelve HTTP 200,
  `access-control-allow-origin: http://127.0.0.1:5173`, métodos GET/POST.
- Proveedor real activo: OpenAI. Comprobación sanitizada desde contenedor:
  `openai_key_present True`, `devexpert_key_present False`; smoke DevExpert real
  PENDIENTE por credencial ausente. Sus adaptadores sí están en tests simulados.
- **P-107-05 — RESUELTO Y REVALIDADO; descripción histórica, entorno host degradado tras setup:** setup recrea .venv
  pero falla `python3 -m venv`: ensurepip ausente; recomienda python3.12-venv.
  Wrapper continúa y devuelve 0. El CLI host funcionaba antes del setup;
  después no puede darse por reproducible su entorno de dependencias.
  No se instalaron paquetes de sistema ni se reparó el entorno.
- **P-107-06 — RESUELTO Y REVALIDADO; descripción histórica, caché pip fuera del repo:** setup advierte
  `WARNING: The directory '/.cache/pip' ... is not owned or is not writable ...
  The cache has been disabled`. Contenedor: HOME=/, uid=1000, PIP_CACHE_DIR=None.
  Compose web configura npm_config_cache=/tmp/.npm; no es caché .cache local.
- **P-107-07 — RESUELTO Y REVALIDADO; auditoría inicial histórica, auditoría de dependencias de desarrollo:**
  `docker compose run --rm web npm audit --json`: exit 1; 2 low (@babel/core,
  esbuild), 1 moderate (baseline-browser-mapping), 4 high (browserslist,
  nanoid, postcss, vite). `npm audit --omit=dev --json`: cero, exit 0.
  Es un reporte del registry, no evidencia de explotación: algunos advisories
  afectan Windows. Requiere valorar aplicabilidad antes de aceptar riesgo.
  No se ejecutó npm audit fix ni se modificó el lockfile.
- **P-107-08 — RESUELTO; descripción histórica, backend inaccesible por defecto desde emulador:**
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

- **P-107-09 — REVALIDADO EN CHROME; limitación del navegador integrado histórica:** speech del navegador integrado
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
hook y ciclo helper backend pasan. Limpieza reparada/revalidada. Permanecen TTS y URL
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

### Reparación aprobada y revalidación P-107-01 — 2026-10-05

Rama fix/docker-cleanup, spec specs/docker-cleanup.md y plan emparejado.
Se cambia down/stop a `docker compose down --remove-orphans` y se verifica
ausencia de contenedores/redes por etiqueta del nombre Compose efectivo.
Errores de Docker o residuales producen exit no cero; no se imprime configuración.

Prueba real con backend/web y los dos emuladores originales activos:

```text
./tonto.sh down
Container ...ui-emulator-run-a6c50a5e1812 Removed
Container ...ui-emulator-run-9fa66213b28a Removed
Network tonto-kids-assistant_default Removed
Project containers and networks removed. Dependency volumes preserved.
exit 0
```

- `docker ps -a` y `docker network ls` filtrados por proyecto: cero recursos.
- Contenedor temporal de otro proyecto cleanup-foreign-check: sigue running=true
  tras down y stop; después se retira explícitamente solo ese control desechable.
- Volumen backend-venv conserva nombre y CreatedAt 2026-10-05T10:43:35+02:00;
  inodos .venv 29753566 y web/node_modules 29756727 idénticos antes/después.
- Segunda llamada down con proyecto limpio: exit 0, sin error.
- `test all`: 86 Python (8 regresiones CLI nuevas) + 24 Kivy + web pasan, exit 0.
  Regresiones: proyecto personalizado, alias, conservación de volúmenes,
  residuales contenedor/red, errores config/down/query y proyecto indeterminado.
- `build all`: typecheck y Vite 43 módulos, 1.23 s, exit 0.
- Nuevo dev all: health HTTP 200 y web HTTP 200 sin setup adicional.
- One-off de control ui-emulator con sleep 300 activo; stop retira backend/web,
  one-off y red, exit 0. Inventario posterior vacío, 8000/5173 libres.
- bash -n y git diff --check pasan. Warnings heredados Starlette/Kivy continúan.

Puntos 2/4/6 COMPLETADO; P-107-01 resuelto. Los restantes problemas de la auditoría
siguen abiertos. Cambio limitado a limpieza CLI, pruebas y documentación.

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

### Reparación emulador Linux y guías vigentes — 2026-10-05

Rama `fix/linux-emulator-connection-tts`; spec y plan
`specs/linux-emulator-connection-tts.md` y
`docs/plans/linux-emulator-connection-tts-implementation-plan.md`.
Paquete espeak en Docker aprobado explícitamente por el operador.
Se elimina la ruta TTS heredada, se configura backend por DNS de Compose y
se pasa ALSA/grupo al ejecutar dev ui cuando existe dispositivo.
Las referencias antiguas del registro anterior son evidencia histórica.

Resultados de ejecución:

- `./tonto.sh test all`: 89 Python + 24 Kivy + checks web pasan, exit 0.
- `./tonto.sh build all`: typecheck y Vite pasan, exit 0, 1.43 s.
- Imagen ui reconstruida con espeak. Smoke Kivy real con Xvfb,
  backend real y síntesis a WAV (sin sustituir backend/TTS por mocks):

```text
HEALTH_HTTP 200
UI_BACKEND http://backend:8000
RESPONSE Una estrella es una enorme bola de gas que brilla en el cielo porque produce luz y calor. Es como un gran faro en el espacio. ¿Tienes alguna otra pregunta sobre las estrellas?
TTS_WAV 1 2 22050 397678 PEAK 31914
UI_FINAL_STATE idle
```

WAV mono PCM 16 bits, 22050 Hz, 397678 frames, amplitud máxima 31914.
El smoke final termina con exit 0. Warnings de clipboard xclip/xsel y caché
Kivy no impiden el resultado; no se añaden dependencias por esos avisos.
El primer intento dejó Xvfb abierto por exec de Bash; se paró su contenedor
propio y se repitió con retorno explícito como el helper oficial de tests.
`./tonto.sh down` final retira backend/red, exit 0.

No existe /dev/snd en este host: síntesis verificada, audibilidad/captura física
no verificadas. Punto 3 PENDIENTE de esa aceptación; no atribuirle la audibilidad
ya confirmada en Raspberry. Punto 7 conserva los fallos setup/caché/audit.
Speech web y proveedor real sin credencial conservan sus pendientes anteriores.
No se ha leído ni modificado el archivo de secretos durante esta reparación.

### Reparación setup y cachés — 2026-10-05

Plan aprobado; rama fix/linux-setup-cache-stability, spec/plan
linux-setup-cache-stability. Sin nuevas dependencias; manifests y lockfile sin cambios.

- Checkout limpio git archive en /tmp/tonto-setup-validation-AqMewE,
  proyecto Compose tonto-setup-validation-20261005, sin secretos copiados.
- `./tonto.sh setup`: instala dependencias Python en volumen nuevo y web,
  exit 0. Segunda ejecución exit 0; pip informa Requirement already satisfied,
  npm instala 81 paquetes en 1 s. No se crea un Python host funcional.
  Docker puede crear el directorio vacío de montaje .venv; no es un entorno IDE.
- Cache discovery: pip /app/.cache/pip, npm /app/.cache/npm.
  Directorios host UID:GID 1000:1000, modo 775 en checkout aislado;
  tamaños 52M/29M. Pip en venv temporal instala requests con Using cached;
  npm ci --offline --audit=false exit 0, 81 paquetes en 894 ms.
- Tests aislados: 97 Python + 24 Kivy + web, exit 0. Build aislado:
  43 módulos Vite, 842 ms, exit 0.
- Setup en checkout principal exit 0; inode/tamaño/mtime del .venv/bin/python
  host idénticos antes/después. Corrige propietario incorrecto de .cache/npm
  únicamente en cachés/volumen Python, sin chmod/chown global del repo.
- Tests finales del checkout: 97 Python (0.40 s), 24 Kivy (1.04 s), web pasan.
  Build final: 43 módulos, 804 ms, exit 0. bash -n y diff --check pasan.
- Setup host explícito en checkout aislado: exit 1 por permisos del directorio
  .venv creado por el montaje Docker; error de Python visible y sin mensaje de
  éxito. La ayuda pide comprobar permisos y venv/ensurepip. No instala sistema.
  Tests del CLI prueban además preservación del entorno existente, ausencia de
  Python host en setup Docker, error venv/pip y errores Docker/npm propagados.
- down principal y aislado exit 0; redes retiradas, volumen aislado conservado,
  cachés intactas. No se borran volúmenes ni datos previos del operador.

Auditoría: consulta antes de reinstalación informó 14 vulnerabilidades;
tras npm ci coincide con entorno limpio: 7 (2 low, 1 moderate, 4 high), exit 1;
producción omit-dev 0, exit 0. Se conserva la observación previa; no se atribuye
su diferencia a una causa demostrada. Triage propuesto en
`docs/web-dependency-audit-triage.md`. Punto 7 continúa FALLIDO por P-107-07.

CI de reparación sobre c403ded: ambos Project checks COMPLETADO/SUCCESS.
Push: https://github.com/joseluisillana/tonto-kids-assistant/actions/runs/37322280811
(1m31s). PR #112: https://github.com/joseluisillana/tonto-kids-assistant/actions/runs/37322356646
(2m8s). Setup/test/build pasan en runner limpio. El commit posterior solo añade
esta evidencia; consultar checks de #112 para su SHA documental final.

### Cierre P-107-07 / punto 7 — 2026-10-05

Spec/plan web-dependency-audit-remediation. Rama fix/web-dependency-audit.
Trabajo autorizado tras triage. Lockfile compatible corregido sin force,
manifest sin cambios; versiones y todos los GHSA en docs/web-dependency-audit-triage.md.

- Auditoría inicial: 7 (2 low, 1 moderate, 4 high), exit 1.
- Reparación lockfile: audited 159 packages, found 0 vulnerabilities, exit 0.
- ./tonto.sh setup: npm ci y Python Docker pasan, exit 0.
- npm audit --json y npm audit --omit=dev --json: total 0, exit 0.
- npm ls --all exit 0, sin árbol inválido.
- Instalación limpia: git archive + lockfile corregido, checkout
  /tmp/tonto-audit-validation-MuAjac, proyecto tonto-audit-validation-20261005.
  Sin secretos copiados. Setup exit 0; audit completo total 0, exit 0.
- ./tonto.sh test all: 97 Python (0.49 s), 24 Kivy (1.19 s), web pasan.
- ./tonto.sh build all: Vite 7.3.6, 43 módulos, 1.21 s, exit 0.
- ./tonto.sh dev all: Vite 7.3.6 ready 370 ms; backend saludable.
- Navegador /admin: pregunta «¿Qué es una estrella?» → Estoy pensando →
  respuesta educativa visible → Listo para hablar; latencia UI 3014 ms.
  Speech synthesis failed sigue como P-107-09, no se acepta audibilidad.
  Captura: /tmp/tonto-point7-web-smoke.png.
- Smoke voz de integración, sin captura personal: espeak genera fixture WAV,
  convertido a PCM mono 16 kHz, 3164 ms. Cliente HTTP web compilado
  sendAudioTurn, sin sustituir fetch/backend, devuelve:

```text
HEALTH { status: 'ok' }
AUDIO_TURN {"session_id":"point7-web-audio-smoke","transcript":"Platón, dime qué es una estrella.","response":"¡Hola! Una estrella es un gran esfera de gas brillante que brilla en el cielo. Por ejemplo, el Sol es una estrella muy cercana a nosotros y nos da luz y calor. ¿Te gustaría saber más sobre las estrellas?"}
```

Exit 0. STT confunde el nombre sintetizado TONTO con Platón, conserva la pregunta.
Fixture valida transporte/STT/respuesta; no valida micrófono físico ni captura UI.
La captura/auto-stop web real conserva su evidencia previa y sus pendientes.
- down en ambos proyectos exit 0, redes/servicios retirados; cachés/volúmenes
  conservados. diff --check pasa. No se modifican backend, UI ni secretos.

Punto 7 COMPLETADO. Tabla principal: 8/9 completos, punto 3 pendiente de audio
físico del emulador. Permanecen speech web/contador/repetibilidad, proveedor
DevExpert real sin credencial y mDNS Raspberry como pendientes ampliados.
No procede cerrar #107 ni declarar estabilidad integral todavía.

CI P-107-07 sobre 4e2858397299518d2766cf75297fe05ff886ebad:
Project checks push SUCCESS (1m30s),
https://github.com/joseluisillana/tonto-kids-assistant/actions/runs/37331107651;
Project checks PR SUCCESS (1m29s),
https://github.com/joseluisillana/tonto-kids-assistant/actions/runs/37331356962.
Setup, checks y build completos pasan. PR #113 abierta para revisión/integración.
El commit siguiente solo registra esta evidencia; consultar checks de #113 para
su SHA documental final.

### Continuación de pendientes físicos — 2026-10-05

Revisión 5d0a52e tras merge #113. Punto 7 integrado; 8/9 completos.
Host sigue sin /dev/snd; navegador automatizable disponible: integrado, sin
Chrome/Firefox conectados. Operador confirma que dispone de navegador externo
y equipo Linux con audio. Se prepara prueba guiada de tres turnos web, contador
y auto-stop 10 s. Resultados humanos aún PENDIENTES, no se anticipa aceptación.
Backend/web arrancados con tonto.sh dev all, health ok y web HTTP 200.
Se mantienen activos durante la validación guiada. No se cambia producto.


### Resultados de continuación — 2026-10-05

- Operador confirma navegador Chrome: «He usado chrome y ha ido perfecto,
  da la prueba como válida». Respuesta a checklist explícito de tres turnos
  relacionados, respuesta/voz clara, contador visible y auto-stop a 10 s.
  Se acepta observación humana; no se inventan transcripts ni latencias.
  Speech web, contador y repetibilidad COMPLETADO. P-107-09 deja de ser bloqueo
  de aceptación: fallo limitado al navegador integrado, Chrome real validado.
- Operador confirma que el equipo Linux con audio es este mismo. Lectura fuera
  del sandbox: /dev/snd existe y hay Pulse/PipeWire. La falta previa de /dev/snd
  era visibilidad del sandbox; no ausencia física de hardware. No se cambian
  dispositivos, permisos del sistema ni servidores de audio.
- getent hosts tonto-pi.local: 192.168.1.183, exit 0 fuera del sandbox.
  Helper oficial preflight por nombre: identity tonto-pi/tonto-pi-user,
  repo limpio en feature/issue-84-face-design; git/python3/curl/arecord/aplay/
  espeak presentes; Python 3.13.5 y .venv correctos; backend LAN health ok,
  exit 0. P-107-03 recuperado/revalidado sin modificar red ni scripts.
  Esto evidencia funcionamiento actual, no garantiza ausencia de intermitencias.
- CI integrado de #108 sobre 5d0a52e: Project checks push/PR SUCCESS,
  runs 37332129154 (1m24s) y 37332141132 (1m28s).

**P-107-10 — RESUELTO Y REVALIDADO; descripción inicial, arranque dev ui con hardware audio:**

```text
./tonto.sh dev ui
Iniciando emulador de UI...
unknown flag: --device
exit 1
Docker Compose version v5.5.1
stat: /dev/snd/by-path => directory, gid 0
stat: /dev/snd/controlC0 y pcm* => character special file, gid 29
```

Compose run --help no incluye --device ni --group-add. La rama hardware del
wrapper no fue ejecutada en las pruebas anteriores dentro del sandbox.
También selecciona el primer elemento del glob (directorio by-path), no un
nodo de dispositivo, para el grupo. No se corrige producto durante esta pasada.
Plan de reparación: specs/linux-emulator-audio-device-startup.md y plan emparejado.

Dictamen actual: 8/9 completos, punto 3 FALLIDO por P-107-10 y aceptación de audio
físico pendiente. Web Chrome y mDNS revalidados. Smoke DevExpert real sigue
pendiente de credencial configurada por el operador. Touch/kiosk #88 excluido.
Backend/web quedan activos para continuar la validación guiada.


### Decisión del operador — DevExpert deprecado, 2026-10-05

D025 en docs/decisions.md. El operador indica «Márcalo como decisión el no
operarlo porque está deprecado». Smoke real DevExpert: NO APLICA; retirado de
pendientes/bloqueos de aceptación. No se ha ejecutado, no se marca COMPLETADO y
no se requieren credenciales. Referencias previas a credencial ausente/pending
son evidencia histórica anterior a esta decisión. OpenAI real sigue validado.
Spec y plan integral actualizados; sin cambios de código/configuración/runtime.
Punto 3 sigue FALLIDO por P-107-10; plan de reparación del emulador vigente.


### Reparación arranque Linux con audio — 2026-10-05

Rama fix/linux-emulator-audio-device-startup, spec/plan emparejados.
Helper scripts/ui-emulator.sh: dispositivos/grupos en override temporal;
ignora by-path y deduplica grupos de nodos de carácter, stat -L. Preserva
archivos personalizados exportados y overrides convencionales. Temporal se
retira por trap EXIT; no genera config expandida ni accede a secretos.
Tests: siete casos nuevos con fixtures (sin dispositivo, by-path, grupos múltiples,
fallo Compose con/sin audio, archivos personalizados/separador y override estándar).
104 Python pasan (0.69 s), 24 Kivy (1.16 s), web y build (43 módulos, 1.31 s).

Arranque real con /dev/snd fuera del sandbox elige grupo 29 y crea contenedor;
no vuelve unknown flag. P-107-10 RESUELTO. Nuevo bloqueo encontrado y documentado:

**P-107-11 — RESUELTO CON APROBACIÓN:**

```text
PermissionError: [Errno 13] Permission denied: '/.kivy'
```

Override diagnóstico temporal de Kivy permite ventana, pero descubre:

```text
ModuleNotFoundError: No module named 'client'
```

Operador autoriza ambos ajustes. Compose usa KIVY_HOME=/tmp/.kivy-runtime y
XDG_CACHE_HOME=/tmp/.cache; command .venv/bin/python -m client.touch_ui.
Arranque oficial llega a Start application main loop; operador confirma ventana.
Warnings MESA (fallback llvmpipe), clipboard xclip/xsel y mtdev event4/event9
no bloquean ventana; no se instalan paquetes ni se amplía acceso a /dev/input.

Revalidación final tras ambos ajustes: 104 Python (0.69 s), 24 Kivy
(1.17 s), web y build (43 módulos, 1.39 s) pasan.

**P-107-12 — ABIERTO: turno hablado del emulador rechazado con HTTP 422.**
Operador: pasa de ESCUCHANDO a PENSANDO y después ERROR. Backend registra
dos POST /chat/audio desde 172.18.0.4 con 422. El WAV generado tiene 16000 Hz,
96000 muestras, 6 s, pico 0.950012 y RMS 0.228277 (70541 muestras no nulas).
Existe señal; estas métricas no demuestran que sea voz del micrófono correcto.
En backend/audio_router.py, la respuesta 422 explícita corresponde a una
transcripción vacía. También puede existir validación de formulario 422;
no se ha recuperado el cuerpo de esas respuestas y la causa definitiva sigue
pendiente. No se atribuye el fallo al TTS, que aún no se alcanza.
Siguiente diagnóstico guiado: turno en modo texto para aislar respuesta/TTS
y repetición hablada con mensaje visible. No se corrige código por esta incidencia.

Actualización del operador: dos turnos en MODO TEXTO funcionan perfectamente;
backend confirma dos POST /chat HTTP 200 desde el emulador. Respuesta y TTS
físico validados en ese recorrido. Nuevo intento hablado sigue fallando;
logs posteriores muestran otros dos POST /chat/audio HTTP 422.
Se intenta recuperar el detalle mediante reenvío del WAV existente, pero el
contenedor one-off ya no existe; no se envía audio y no se recupera el cuerpo
del rechazo. Solo backend/web siguen activos. P-107-12 permanece abierto;
la hipótesis de transcripción vacía aún requiere evidencia del cuerpo HTTP.
Reintento con emulador abierto: reenvío del WAV existente confirma HTTP 422,
`{"detail":"Audio did not contain recognizable speech"}`. Se descarta error de
formulario para esta grabación: la transcripción queda vacía. WAV: 16000 Hz,
96000 muestras, pico 0.950012, RMS 0.225005. PortAudio default [8,8] corresponde
a ALSA default; enumera también hw:0,0 y entradas DMIC hw:0,6 / hw:0,7.
Operador confirma que el mismo micrófono y volumen funcionan en web sin gritar;
otro intento hablado en emulador falla. No requiere pronunciar una frase exacta.
Inspección: capture_audio en modo pc recibe device, pero sd.rec no lo usa;
TONTO_AUDIO_DEVICE no permite seleccionar entrada en esa ruta actualmente.
Hipótesis: ruta ALSA/default distinta de Chrome; no se declara causa confirmada.
Operador aprueba reparación de selección de entrada. Modo PC ahora pasa
device a sd.rec, convierte índice numérico y preserva nombre/default.
Tres casos de test verifican el argumento efectivo sin hardware/dependencias
opcionales. ./tonto.sh test all: 107 Python (0.44 s), 24 Kivy (1.05 s), web OK.
Emulador reiniciado con override temporal /tmp/tonto-ui-dmic-validation.yaml,
TONTO_AUDIO_DEVICE=4 (PortAudio DMIC hw:0,6 en este equipo); no se fija el índice
en configuración compartida ni se cambia salida/volumen. Prueba física pendiente.
Prueba con entrada 4: operador observa ESCUCHANDO permanente. Log confirma
sounddevice.PortAudioError: Invalid sample rate [PaErrorCode -9997].
Worker voice_pipeline_thread termina sin recuperar estado. **P-107-13 ABIERTO:**
excepción de captura PC sin manejo deja UI bloqueada; pendiente reparación
específica, no se corrige durante esta validación.
check_input_settings sin grabación: entradas 0/4 rechazan 16000 Hz;
5 (DMIC hw:0,7) y 8 (default) admiten 16000 Hz. Override temporal cambia a
entrada 5 para continuar la prueba aprobada sin conversión de audio/dependencias.
Resultado entrada 5: operador confirma «Ahora ha funcionado, he realizado 3
turnos». Backend registra cuatro POST /chat/audio HTTP 200 desde 172.18.0.3;
se atribuyen tres turnos a la confirmación humana, sin inferir qué fue el cuarto.
P-107-12 RESUELTO Y REVALIDADO con selección explícita compatible. Captura,
transcripción, respuesta y TTS físicos aceptados para esa configuración.
P-107-13 permanece abierto: no se ha reparado el manejo de excepción de captura.

**P-107-14 — OBSERVACIÓN ABIERTA:** operador ajusta volumen del sistema mientras
TONTO habla y nota que el control queda encasquillado durante unos segundos.
El turno funciona; no se dispone de logs del control ni reproducción aislada
que establezcan causa o frecuencia. No se atribuye a ALSA/PipeWire sin evidencia.
Evaluar reproducción y respuesta del control de volumen antes del cierre estable;
no modificar sistema/dependencias durante esta validación.
Decisión posterior: aplazar P-107-14 en GitHub #114, enlazado con
docs/issues/emulator-system-volume-delay.md; no bloquea esta reparación.
P-107-13 reparado en código con aprobación: PortAudioError retorna fallo,
UI muestra ERROR y usa reset existente. Validación física pendiente.
Selección reproducible: TONTO_AUDIO_DEVICE=5 ./tonto.sh dev ui, sin override
temporal; índice específico de este equipo, no fijado como default compartido.
Regresiones iniciales de recuperación: 110 Python (0.44 s), 24 Kivy (1.00 s),
web pasan; build 43 módulos (907 ms). Nuevo test de delegación de fallo de captura
añadido después: repetir UI para confirmar su resultado. Prueba física de error
con comando TONTO_AUDIO_DEVICE=4 ./tonto.sh dev ui en curso.
Operador confirma prueba física negativa: muestra ERROR y vuelve a
TOCA PARA HABLAR tras cuatro segundos. P-107-13 RESUELTO Y REVALIDADO.
Suite UI ampliada: 25 tests pasan (1.03 s), incluido fallo de captura sin upload.
Pendiente cierre final: nuevo arranque oficial con entrada 5, tres turnos,
limpieza y CI del SHA final. P-107-14 queda aplazado en #114 por decisión humana.
Próxima ejecución: conservar el contenedor y WAV hasta recuperar el detalle
422; si es transcripción vacía, comprobar fuente de entrada y señal original
antes de normalizar. Sin cambios de producto en esta actualización.

**Audio físico pendiente de diagnóstico:** operador indica «Aparece la ventana,
pero falla micrófono o voz». No se aprueba captura/TTS. Se solicita precisar
estado del botón/error. Contenedor: UID 1000, grupos [29,1000]; PortAudio enumera
10 dispositivos, default [8,8]. arecord muestra analog device 0 y DMIC 6/7;
aplay muestra analog/HDMI. Host usa PulseAudio sobre PipeWire. No se atribuye aún
causa ni se modifica ruta de audio/configuración del sistema.
