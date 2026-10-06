# Post-MVP: Raspberry Touch UI

**Inicio:** 2026-07-18
**Objetivo:** Desarrollar la interfaz táctil con cara animada para la Raspberry Pi, siguiendo el hito de alta prioridad definido en `docs/future-work.md`.

## Fases del Proyecto

- **Fase 0:** Tracking y Registro en GitHub
- **Fase 1:** Setup y Validación de Hardware
- **Fase 2:** Spike de Runtime y Stack Tecnológico
- **Fase 3:** Diseño Visual de la Cara Animada
- **Fase 4:** Spike y Evaluación Técnica de Animación
- **Fase 5:** Cliente Táctil Mínimo
- **Fase 6:** Integración de Cara Animada y Estados
- **Fase 7:** Kiosk Mode, Fallback y Validación Final

## Diario de Ejecución

### 2026-07-18: Kickoff de Planificación y Fase 0
- **Estado:** Completado
- **Acciones:**
  - Se definieron los documentos iniciales de planificación en la rama `docs/raspberry-touch-ui-spec`.
  - Se actualizó la especificación en `ai/specs/021-raspberry-touch-ui/spec.md` para incluir el Diseño Visual (Fase 3) y redimensionar las fases posteriores.
  - Se redactó el plan de implementación en `ai/specs/021-raspberry-touch-ui/plan.md`.
  - El usuario especificó el orden (hardware -> tech stack -> diseño visual -> spike animación -> ui -> face anim integration -> kiosk mode).
  - **Fase 0 ejecutada:** Se crearon los issues de seguimiento en GitHub mediante la CLI.
    - Parent Issue: #81
    - Fase 1: #82
    - Fase 2: #83
    - Fase 3: #84
    - Fase 4: #85
    - Fase 5: #86
    - Fase 6: #87
    - Fase 7: #88
- **Próximos pasos:** 
  - Comenzar con la **Fase 1** (Setup y Validación de Hardware).

### 2026-07-20 / 2026-08-05: Ejecución y Validación de la Fase 1
- **Estado:** Completado
- **Acciones:**
  - Se actualizaron las instrucciones de `docs/hardware.md` con la configuración estándar para la pantalla HDMI táctil Waveshare 5".
  - Se corrigió la ruta de boot a `/boot/firmware/config.txt` para Debian 12 Bookworm.
  - El operador humano validó físicamente el arranque, la resolución visual y el input táctil (comprobado vía `evtest` con el dispositivo `WaveShare WS170120`).
  - Se confirmó que el límite `max_usb_current=1` mantiene alimentado el micrófono USB y el audio funciona correctamente sin caídas de tensión.
- **Próximos pasos:** 
  - Hacer merge de la PR asociada a la Fase 1 (#93).
  - Comenzar con la **Fase 2** (Spike de Runtime y Stack Tecnológico).

### 2026-08-06: Ejecución y Decisión de la Fase 2
- **Estado:** Completado
- **Acciones:**
  - Se evaluó el stack de UI (Pygame, Tkinter, Chromium, Qt, Kivy) para el entorno headless Raspberry Pi OS Lite.
  - Se descartaron las opciones dependientes de servidor X11.
  - Aunque Pygame tiene un footprint de dependencias cero, se descartó a favor de Kivy tras constatar que Pygame en modo headless (directo de `/dev/input/`) sufre frecuentemente severas descalibraciones de coordenadas en pantallas USB táctiles.
  - Kivy se seleccionó formalmente por su renderizado por hardware (OpenGL ES 2) y su robusto soporte de eventos touch nativos a nivel de kernel mediante `mtdev`.
  - Se creó y validó el prototipo de Kivy localmente, incluso con un script de test automatizado (`spikes/ui_kivy/test_main.py`).
  - Se registró la decisión final (D024) en `docs/decisions.md`.
- **Próximos pasos:** 
  - Hacer merge de la PR asociada a la Fase 2 (Issue #83).
  - Comenzar con la **Fase 3** (Diseño Visual de la Cara Animada).

### 2026-08-06: Ejecución de Fases 3 a 6 (Cliente Táctil Completo)
- **Estado:** Completado
- **Acciones:**
  - **Fase 3 (Diseño Visual):** Se generaron múltiples variaciones visuales de la cara de TONTO (estado *Idle*, *Listening*, *Thinking*, *Speaking*, *Error*) y se iteró el diseño hasta conseguir una apariencia "flat", amigable y con animaciones sutiles (parpadeo en Idle).
  - **Fase 4 (Spike Animación):** Se implementó `TontoFace` en Kivy (`client/tonto_face.py`) como un widget paramétrico dibujado por hardware, usando Canvas instructions (PushMatrix, Scale, Translate) para las transiciones.
  - **Fase 5 y 6 (Cliente y Lógica de Voz):** Se integró `TontoTouchUI` (`client/touch_ui.py`) que orquesta:
    - La conexión con `POST /chat/audio` desde el micrófono en un thread separado.
    - Un `ProgressButton` personalizado con barra de progreso durante la escucha (`record_seconds`).
    - Soporte multiplataforma (`TONTO_AUDIO_MODE="pc"` o `raspberry`) que normaliza el volumen del micrófono con `numpy` para mejorar la calidad de STT de Whisper.
    - TTS nativo en PC (`System.Speech` de PowerShell forzado a voz en español).
  - Se actualizaron las instrucciones de `backend/openai_client.py` a español estricto para evitar desviaciones del LLM durante falsos positivos del STT.
- **Próximos pasos:** 
  - Comenzar con la **Fase 7** (Kiosk Mode, Fallback y Validación Final en Raspberry).

### 2026-10-05: Revisión de la Fase 3 y Migración a Docker
- **Estado:** En progreso (Reapertura de la Fase 3)
- **Acciones:**
  - Al revisar el estado de la **Issue #84**, se descubrió que, aunque el código de Kivy de la Fase 4, 5 y 6 se avanzó, los assets y referencias visuales de la **Fase 3** nunca se generaron ni se guardaron en el repositorio, a pesar de que la entrada anterior del diario indicaba lo contrario.
  - Al mismo tiempo, la rama `main` introdujo una migración a Linux y Docker, incluyendo una especificación pendiente para emular la UI de Kivy usando contenedores (`ai/specs/012-kivy-ui-docker-emulation/spec.md`).
- **Próximos pasos (Plan de Acción Aprobado):**
  1. En lugar de generar imágenes abstractas con GenAI, capturar la interfaz Kivy real ya implementada. Ejecutar el código en un entorno aislado con `xvfb` para obtener capturas de los distintos estados de la cara (`Idle`, `Speaking`, `Listening`, etc.) y guardarlas en `docs/assets/` como referencia final.
  2. Implementar la infraestructura de `ui-emulator` en el `docker-compose.yml` local.
  3. Ejecutar y testear `client/touch_ui.py` en este entorno Docker.

## 2026-10-05 — Cobertura de tests para la UI Kivy

Tras el merge de la Issue #84 en `main`, se detectó que la suite de CI no cubría ningún
código de la UI gráfica (`client/tonto_face.py`, `client/touch_ui.py`).

**Estado:** Implementado y validado localmente en
`feature/kivy-ui-testing-coverage`. Tracking: #105, Part of #81.

La implementación heredada estaba sin commit y sustituía Kivy por mocks; varios
tests asignaban los valores que luego comprobaban y no ejecutaban constructores.
El borrador asumía un proveedor `headless` que no existe en la instalación
Kivy 2.3.0 inspeccionada. Se corrigieron la spec y su plan antes del cierre.

- Añadidos 24 tests de widgets Kivy reales: constructores/canvas, cinco estados,
  destinos ERROR/SPEAKING, cancelación de eventos, configuración de backend,
  bindings, guards, éxito/error, retorno a IDLE y delegación de texto/audio.
- Audio, HTTP y ejecución de workers se simulan en su punto de uso; Kivy y sus
  animaciones no se sustituyen. Clock procesa callbacks y animaciones.
- `test ui` usa `ui-emulator`, SDL2, Mesa software y Xvfb. El socket X11 queda en
  un volumen temporal, con permisos 1777 preparados en el Dockerfile. Un padre
  Bash evita el bloqueo de la señal de arranque de xvfb-run como PID 1.
- Retirado el hook global Kivy de conftest. `test python` excluye los dos módulos
  gráficos y `test all` ejecuta python → ui → web, como ya invoca CI.
- Actualizados spec/plan, comandos de README y resúmenes de estado de roadmap y
  specs. Sin nuevas dependencias ni cambios de código de producto.

**Validación (2026-10-05):**

- `./tonto.sh test ui`: 24 tests pasan, exit 0.
- `./tonto.sh test all`: sintaxis Python correcta, 78 tests Python + 24 tests UI
  pasan y suite web pasa, exit 0.
- `./tonto.sh build web`: typecheck y build Vite pasan, exit 0.
- `bash -n tonto.sh` y `git diff --check`: pasan.

Persisten avisos de deprecación de Starlette/httpx e imghdr de Kivy; no se
introdujeron dependencias para resolverlos. La validación con display virtual
no demuestra funcionamiento táctil/OpenGL ES en Raspberry: Fase 7 (#88) sigue
pendiente. La emulación y los assets de Fase 3 ya están integrados vía PR #104,
superando los pendientes de la entrada anterior del diario.

**Spec:** `ai/specs/013-kivy-ui-testing-coverage/spec.md`.
**Plan:** `ai/specs/013-kivy-ui-testing-coverage/plan.md`.

## 2026-10-05 — Cierre validación del emulador Linux

Punto 3 de #107 completado en PR #115: arranque Linux reparado, selección
explícita de entrada PC, tres turnos físicos y recuperación ERROR/reset 4 s.
110 Python, 25 Kivy, web/build y CI 09ef3b3 pasan; limpieza oficial correcta.
PR #115 sin borrador, lista para revisión y pendiente de merge en #108.
#107 permanece abierta hasta integración global; volumen aplazado en #114,
enlazado con docs/issues/emulator-system-volume-delay.md. #88 excluida.
Reconciliación de estados/documentación; no cambia comportamiento de producto.

## 2026-10-06 — Pasada final integrada de migración

Código7117313 tras merge #115: API/CORS/negativos, CLI tres turnos y memoria,
emulador tres turnos audibles, Raspberry tres turnos sobre mismo SHA y Chrome
tres turnos/contador/auto-stop confirmados por operador. Setup Docker exit0,
110 Python+25 Kivy+web pasan tras instalación; build43 módulos863ms, audits0.
Helpers/export/hook/sintaxis pasan; limpieza sin residuales conserva dependencias.
mDNS falla; IP con HostKeyAlias estricto valida identidad y pipeline. No se
reparó código durante pasada. #114 aplazado, #88 excluido, DevExpert NO APLICA.
CI c12f377 success (runs37380799527/37380807200). Nueve puntos COMPLETADOS:
OK de migración en alcance validado, pendiente revisión/merge #108 en main.

## 2026-10-06 — Preparación de cierre e integración #108

Operador autoriza merge en main y cierre de #107. Metadatos de specs/planes,
roadmap y resumen vigente estabilizados: COMPLETADOS, sin pendientes funcionales
ni referencias vigentes a #115 como borrador. CI63d4099 success; confirmar
checks del commit documental de metadatos antes de merge. Cerrar #107 después
de integración, mantener #81/#88/#110/#114 abiertas. Sin cambios de comportamiento.

## 2026-10-06 — Definición inicial de spec #110

Revisados issue original, estado y main `a985dac`, que integra #108.
Rama `docs/issue-110-secrets-spec` desde main limpio. Spec
`ai/specs/003-agent-secrets-protection/spec.md` y plan emparejado en DRAFT: matriz de
operaciones, superficies actuales, canarios y aceptación por perfil.
Se distingue endurecimiento del repo de aislamiento efectivo del agente.
Decisiones de aislamiento/consumo/mediación Docker y SSH pendientes de revisión.
Inspección de código y documentación públicos sin leer secretos ni ejecutar
configuración expandida. Sin cambios de runtime ni dependencias.

### #110 — propuesta concreta de aislamiento

Preparado `ai/specs/003-agent-secrets-protection/artifacts/agent-secrets-isolation-design.md`: evaluación preliminar del
perfil suministrado a la sesión y CLI Codex 0.160.0, con documentación oficial.
Lectura del host y accesos Docker persistentes impiden acreditar aislamiento.
OpenCode no encontrado en PATH; otros canales pendientes de pruebas.
Recomendación pendiente de decisión: entorno de desarrollo sin secretos y
runtime/SSH operados por humano, usando copia revisada no modificable por agente.
Spec/plan amplían la amenaza a código y dependencias del runtime. No se cambian
permisos, secretos ni scripts, y no se ejecutan pruebas contra secretos reales.

### #110 — alcance elegido: exposiciones accidentales

El operador prefiere mantener automatización actual. Aislamiento y operación
solo humana quedan diferidos; spec/plan registran precedencia de esta decisión.
Exploradas variables host, env_file externo y secretos Compose por archivo con
fuentes Docker oficiales en `ai/specs/003-agent-secrets-protection/artifacts/agent-secrets-credential-options.md`.
Backend ya consulta entorno: Docker requiere suministrarlo explícitamente.
Ninguna opción elegida ni aplicada; no se leen ni modifican secretos reales.

### #110 — reparación de diagnósticos autorizada y validada

Operador descarta variable host y autoriza corregir diagnósticos conservando .env
y workflow. Rama `fix/issue-110-safe-diagnostics`, con borradores previos de esta
conversación conservados. Limpieza usa config sin resolución env_file ni
interpolación antes de seleccionar nombre; no captura modelo expandido, suprime
salidas Docker crudas y mantiene exit codes/residuales/volúmenes. Chat/STT no
leen cuerpos HTTP fallidos ni reflejan razones de red/configuración; suprimen
cadenas de excepción y mantienen estados HTTP y contratos de éxito.

Validación: `./tonto.sh test python` con override temporal que elimina env_file
del backend de tests: **135 passed**, sintaxis Python correcta; warning existente
Starlette/httpx. Primera pasada detectó fixture multipart incompleto (8 fallos),
corregido; segunda pasada completa pasa. Tests nuevos: 7 cleanup + 18 proveedores,
incluyendo endpoints y trazas con canarios ficticios. Compose real con fixtures:
sin canario expandido y nombre desde .env/override preservado, 2 casos pasan.
`bash -n tonto.sh` y `git diff --check` pasan. Sin lectura/modificación de secretos,
llamadas reales ni dependencias nuevas. No se revalida teardown físico ni voz;
la consulta Compose real sí se valida, teardown usa stubs. #110 sigue abierta:
otros diagnósticos/logs, build/export y tareas sin secretos quedan de seguimiento.

### #110 — complemento de logs seguros

Operador propone logs con información sensible ofuscada. Se implementa
minimización previa: helper `backend/provider_diagnostics.py` con logging
WARNING y JSON acotado a proveedor, operación, categoría y HTTP status validado.
No acepta body/excepción/URL/headers/clave ni conversación/audio; no hashes ni
prefijos de claves, no exc_info/stack_info y sin archivos/dependencias nuevos.
Integrado en fallos chat/STT de ambos adaptadores, incluida configuración y
credencial ausente. Spec/plan/workflow actualizados.
Suite oficial Python en Docker con override sin env_file: **136 passed**,
sintaxis Python y diff check pasan; warning Starlette/httpx previo. caplog
verifica canarios, campos y ausencia de trazas en registros de errores; sin
credenciales ni llamadas reales. No afirma sanitización de logs ajenos.

### #110 — preparación de primera PR

Operador autoriza preparar commit/PR del trabajo actual. Secuencia acordada
registrada en spec/plan: PR 1 diagnósticos; PR 2 setup/tests sin credenciales;
PR 3 builds/montajes; PR 4 export NotebookLM. Las fases futuras no se implementan
en esta entrega; #110 queda abierta. Roadmap reconciliado con decisión vigente.
Validación local vigente: 136 Python, consulta Compose ficticia, sintaxis y diff
check; sin revalidación de voz o teardown real. Mantener estos límites en la PR.

### #110 — segunda entrega: tareas sin inyección de credenciales

PR #116 mergeada con CI completa, main local/remoto 8ef12ed y rama anterior
eliminada. Operador autoriza continuar secuencia; rama
`fix/issue-110-secret-free-tasks` desde main limpio y actualizado.

`docker-compose.tasks.yml` separa setup/tests/build del runtime: no env_file,
puertos ni depends_on; CLI usa archivo explícito y --env-file /dev/null,
ignora COMPOSE_FILE/COMPOSE_ENV_FILES/profiles runtime y retira las claves
OpenAI/DevExpert heredadas, incluido setup host. Estos comandos ya no crean
.env. Dev/SSH y provisión runtime sin cambios; mismas imágenes/cache/volumen.
Personalización de proyecto: COMPOSE_PROJECT_NAME debe exportarse si se usaba
solo dentro de .env. README/spec/plan documentan el límite. Archivos de secretos
en bind mounts/build context siguen como PR 3; no se afirma aislamiento.

Validación oficial sin overrides: setup exit 0 (npm audit 0), test all
**151 Python + 25 UI** y web pasan; build all exit 0 (43 módulos). 15 tests nuevos
de CLI/modelo y tests setup actualizados. Compose real con fixtures confirma
tareas sin claves, configuración runtime preservada, volumen compartido y
ausencia de requisito .env. Bash/diff check pasan. Warnings Starlette/httpx e
imghdr previos. Sin lectura/modificación de credenciales reales ni dependencias
nuevas. No se inicia/paraliza demo real; #110 permanece abierta.

### #110 — tercera entrega: contexto de build y mounts mínimos

#117 mergeada con CI aprobada; main local/remoto 0222d39 y rama anterior borrada.
Operador autoriza siguiente fase; rama fix/issue-110-container-mounts desde
main limpio/actualizado. UI build usa client con allowlist de Dockerfile.ui.
Runtime Python/UI monta backend o client/shared read-only y venv/X11; tareas
montan fuentes/scripts/tests/config públicos read-only y caches/fixtures
específicos. Web monta fuentes/config y outputs/dependencias concretos, sin
web/.env. CLI prepara directorios host antes de Docker. No cambia .env ni SSH.

Setup exit 0, npm audit 0; test all **153 Python + 25 UI** y web pasan; build all
exit 0. Tests dentro del contenedor confirman exclusión de raíces protegidas y
readonly/writable según uso. Build real scratch con archivos ficticios y symlink:
solo Dockerfile.ui copiado. Backend runtime sin env_file temporalmente: imports,
/health y ausencia de /app/.env/client correctos. Sintaxis/diff check pasan.
Sin claves reales/dependencias nuevas ni revalidación de voz física. Fuentes
autorizadas deben seguir sin secretos; no se promete aislamiento host/Docker.
PR 4 exportación pendiente; #110 permanece abierta.

### #110 — cuarta entrega: exportación NotebookLM segura

#118 integrada con CI completa en main b254ded; rama anterior retirada.
Operador autoriza exportación: rama fix/issue-110-safe-notebooklm-export desde
main limpio/actualizado. Destinos solo bajo exports/subdirectorio, normalizados;
sin links en componentes. Fuentes validadas antes de contenido y borrado:
rechazo de symlinks en árboles docs/specs, links rotos/internos, hardlinks y
categorías protegidas. Staging privado y reemplazo de output derivado autorizado;
errores fijos sin diagnósticos crudos. Formato y hook Bash conservados.

Suite Python oficial **175 passed**, con 22 tests nuevos de exportación. Primer
fixture esperaba rechazo de un dotfile que el glob ya excluía; ajustado a fuente
protegida visible y añadida preservación ante fallo IO. Export real exit 0;
comparación con baseline sobre fixtures: 7 archivos idénticos byte a byte.
Sintaxis Bash/diff check pasan, warning Starlette/httpx previo. Sin lectura de
secretos reales ni dependencias nuevas. Fuentes regulares deben seguir públicas;
no se escanean claves en Markdown ni se cubren carreras adversarias/concurrencia.
#110 sigue abierta para revisar aceptación del alcance reducido tras integración.


### #110 — revalidación integrada y cierre documental autorizado

Las cuatro entregas ya están integradas: #116 (8ef12ed), #117 (0222d39),
#118 (b254ded) y #119 (70104a4), todas con CI aprobada. Sobre este baseline se
ejecutan setup, test all (175 Python + 25 Kivy + web), build all y sintaxis Bash: pasan.
Pasan además 22 casos auxiliares con stubs, seis turnos API texto/audio con
HTTP mocks, lifecycle/cleanup Docker real en proyecto efímero sin secretos,
contexto UI scratch, export real y hook en fixture. Matriz completa en spec.
El harness API se repite con PYTHONPATH correcto tras un fallo de importación
de su primera invocación; no se modifica producto ni dependencias.

Hardware/SSH, voz manual, proveedores reales y activación systemd excluidos.
El operador autoriza una última PR solo documental, esperar CI, integrarla y
sincronizar main antes de cerrar #110 por el alcance reducido elegido.
El aislamiento universal original sigue diferido; se mantiene .env y workflow.


### 2026-10-06 — preparación de la primera major v1.0.0

#120 integrada en e98f43f con CI aprobada, #110 cerrada y main sincronizada.
Investigación remota: 13 tags, último v0.6.1 (2026-07-18), ninguna GitHub Release.
El operador aprueba v1.0.0 para cerrar MVP conversacional Linux/Docker validado.
Rama chore/release-v1.0.0: VERSION, metadatos web y notas de release; spec/plan
de publicación con CI, merge y tag anotado. Sin comportamiento ni dependencias
nuevos. #81/#88/#114/#53 permanecen abiertos; aislamiento completo diferido.

Validación local: test web y build web pasan (43 módulos); comparación JSON
confirma lockfile intacto salvo metadatos raíz y versiones alineadas.
Export/diff check pasan. La CI de PR y main controla la publicación del tag.

### 2026-10-06 — definición de jerarquía portable de instrucciones

Sobre main limpio `1cf1640`, rama `docs/agent-instructions-hierarchy` e issue
#122. Se abre spec/plan para adaptar el prompt del operador a AGENTS.md raíz
y locales, con inventario atómico, matriz origen/destino, fuentes canónicas,
navegación obligatoria y neutralidad del agente. No se modifica todavía AGENTS.md,
skills ni workflow; implementación e inventario completo pendientes.
Discrepancias Windows/DevExpert identificadas para separar historia de estado
vigente sin borrar instrucciones. «YAMLD» interpretado como AGENTS.md/Markdown
conforme al adjunto. Reorganización SDD posterior excluida; sin cambios de
producto, dependencias o CI. Validación de esta entrega: revisión documental,
rutas locales referenciadas y diff check; no se ejecuta runtime ni hardware.

### 2026-10-06 — refinamiento de la spec de instrucciones

Se precisan límites del inventario, fuerza normativa y disparadores, precedencia
y excepciones post-MVP, navegación por ámbito y evidencia verificable por
recorrido. Se registra que el export NotebookLM existente no incluye todos los
futuros AGENTS.md locales, sin cambiar scripts. Spec y plan siguen DRAFT;
confirmación de formato y ubicación del procedimiento común consultadas al
operador. Sin migración de instrucciones ni cambios funcionales.

El operador confirma AGENTS.md en Markdown (Q1 resuelta); no introducir YAML.
Ubicación del procedimiento común (Q2) pendiente.

Q2 resuelta por el operador: mantener detalle en docs/ai-assisted-workflow.md,
con reglas críticas y lectura obligatoria desde AGENTS.md. Spec y plan reflejan
la distribución confirmada; ambas consultas cerradas, implementación pendiente.

### 2026-10-06 — implementación de jerarquía de instrucciones (#122)

Inventario previo de cinco fuentes con 524 unidades de reglas/contexto/ejemplos,
original y condiciones completos: 355 conservadas, 71 trasladadas, 76 fusionadas
y 22 históricas. Raíz como mapa/gate, detalle común en workflow obligatorio y
diez locales justificados. Skills, metadatos y contratos preservados; D025 y
Linux/Docker etiquetan referencias históricas, sin reactivar DevExpert/Windows.
Fuente adicional O001 documenta sustitución de selección obsoleta en checklist.

Recorridos backend/shared, cliente/audio, web/audio, scripts/secretos y docs/spec
revisados; referencias locales, secciones destino, comandos y dependencias
contrastados. Shared sigue placeholder; hook limitado a .git directorio y export
no cubre todos los locales, límites registrados sin modificar scripts.
Diff solo Markdown, diff check sin errores; main remoto sigue 1cf1640.
Sin código, dependencias, CI, reorganización SDD, credenciales, runtime/proveedor
o hardware. No tests funcionales para este cambio documental. Entrega local lista
para revisión/integración; issue #122 permanece abierta hasta completar ese flujo.

Commit documental preparado; el hook pre-commit regeneró el export NotebookLM
con éxito y su selección existente. Sin ampliar cobertura a todos los locales.

### 2026-10-06 — instrumentación de specs/issues en ai/, fase 1

Operador solicita aplicar el prompt adaptado, exclusivamente fase 1.
Baseline `40342ee`; rama `docs/ai-specs-issues-process`. Plan previo:
`docs/plans/ai-process-instrumentation-plan.md`. Creado proceso portable en inglés,
con once documentos: entrada común, README/INDEX por tipo y seis plantillas.
IDs locales independientes de GitHub, estados/condiciones explícitos, plan previo,
journal propio y sincronización de índices; seguridad conserva controles actuales.
Agente de desarrollo: Codex; decisiones y alcance pertenecen al operador.

AGENTS.md raíz enlaza ai/; workflow, documentación común y plantilla heredada
reconciliados. Registros heredados cuentan como trabajo registrado y conservan
sus ubicaciones. No se crean registros concretos ni se migran specs, issues,
planes, prompts o evidencias. Sin cambios de GitHub, locales AGENTS.md, producto,
CI, dependencias, scripts ni export. Export actual no incluye ai/, límite explícito.

Verificación local: once documentos ai/, enlaces relativos, campos YAML de ambas
plantillas, recordatorios de seguridad/plan/journal/estado en seis plantillas e
índices vacíos comprobados. Revisión de diff y `git diff --check` pasan. No se
requieren tests funcionales para Markdown. Sin validación hardware/proveedor.
Entrega local pendiente de revisión e integración; sin commit/PR para esta entrega.
Fase 2 pendiente: inventario completo, mapa origen/destino, estados basados en
evidencia, procedencia y conservación de relaciones/histórico.

### 2026-10-06 — integración de fase 1 e inventario de migración

Operador confirma CI verde y autoriza integrar #124 para continuar. Ambas
comprobaciones remotas pass (1m40s y 1m34s); squash merge `818e88e`, main
sincronizada y rama de fase 1 retirada. Se abre rama
`docs/historical-records-migration` y registro
`ai/specs/001-historical-records-migration/` con definición, plan previo,
journal y mapa origen/destino. Estado in-progress e índice sincronizado.

Inventario/mapa previo a traslado: 33 fuentes specs (28 definiciones y cinco
guías/matriz auxiliar), 28 planes, un documento local de issue, ocho journals,
cinco imágenes y documentación relacionada. GitHub devuelve 48 issues, 44
cerradas/cuatro abiertas (#53/#81/#88/#114). IDs locales propuestos independientes;
#114 integra su documento local, sin duplicar el registro. Compartidos conservan
fuente única; faltan contraste de comentarios/PRs, fechas originales y revisión
de estados ambiguos antes de importar. El mapa no reserva IDs históricos.

Cobertura de archivos, tablas y 48 identidades únicas verificada. Ninguna fuente
spec/plan/issue histórica trasladada ni GitHub modificado; sin runtime/hardware,
dependencias, CI/scripts ni locales AGENTS.md. `git diff --check` pasa.
Mapa preparado para revisión; la migración completa sigue pendiente, sin
atribuir aceptación funcional a cierres administrativos o texto histórico.

### 2026-10-06 — corrección de alcance: issues de GitHub permanecen en GitHub

El operador aclara que no deben importarse las 48 issues remotas como registros
locales. Su definición, operación e histórico permanecen en GitHub. La propuesta
anterior de espejos locales queda descartada; el inventario remoto sirve solo
para verificar enlaces/evidencia. Se ajustan spec, plan, mapa y proceso común.

La migración se limita a registros ya definidos en el repositorio. El documento
local de volumen se propone como `ai/issues/001-emulator-system-volume-delay/`,
con referencia completa a #114; no es una copia de la issue remota. Matriz de
28 definiciones locales y un documento local de issue con URLs correspondientes,
separando tracking, fases y contexto. Donde no hay issue identificada se declara,
sin inventarla. Ninguna fuente histórica trasladada ni GitHub modificado.

### 2026-10-06 — plan de ejecución de la migración histórica

Operador solicita planificar la spec 001. Plan ampliado con revisión de metadatos
previa, cinco lotes seriales, conservación/verificación por lote, tratamiento de
planes compartidos/retrospectivos, referencias GitHub y rutas antiguas navegables.
Registro pasa de inventario in-progress a ejecución planned, con índice y resumen
sincronizados. Sin traslado de fuentes, importación remota ni cambios funcionales.
La ejecución posterior se hará contra este plan y el mapa revisado.

### 2026-10-06 — implementación local de la migración histórica

Operador solicita implementar el plan. Cinco lotes seriales completados:
28 specs históricas y un documento de issue local, con 64 fuentes originales,
planes/prompts y artefactos auxiliares conservados. Fuentes antiguas mantienen
referencias al destino canónico y todas sus secciones navegables. Journals e
imágenes compartidos permanecen en su ubicación. Las 48 issues consultadas
siguen en GitHub; no se importan ni modifican, y `related` conserva las URLs
correctas. Se actualizan exclusivamente rutas en 19 consumidores; raíz/índice
reconcilian navegación y estados con evidencia. Skill local cambia solo dos rutas.

Metadatos conservan fechas originales explícitas o primera fecha registrada en
Git con su procedencia; propietarios no documentados se declaran desconocidos.
Planes ausentes se etiquetan retrospectivos; proveedores enlazan el único plan
compartido. Caché antigua permanece planned archivada/sustituida, sin autorización
para ejecutar; touch in-progress (#88) y volumen local open (#114). Jerarquía y
migración Linux integradas contrastadas con PRs; release v1.0.0 publicada verificada.

Verificación: 64 originales coinciden byte a byte con baseline `818e88e` y ledger
SHA-256; cuerpos migrados conservados salvo rutas y nueve espacios finales heredados; 30 definiciones registradas,
tríos, campos/estados/fechas e índices coinciden. 998 enlaces locales a archivos,
imágenes y fragmentos resuelven en 198 documentos; headings antiguos preservados;
`git diff --check` pasa. Sin cambios no-Markdown, runtime, dependencias, CI/scripts,
operación de proveedores/hardware ni nuevos tests funcionales. Export no incluye
ai/ y no se amplía: navegar al repositorio para contratos canónicos.

Entrega local lista para PR; spec de migración in-progress hasta revisión/CI e
integración. No se cierran issues de producto por trasladar documentación.

Commit de migración `4c765ea`; hook de export existente aprobado. Rama publicada
y PR #125 abierta con evidencia/criterios de conservación. Índices/journals
canónicos enlazan la revisión; CI e integración pendientes. Issues de GitHub
sin modificaciones y checkout limpio después de registrar esta referencia.

### 2026-10-06 — ampliación: retirar estructura antigua con impacto explícito

Operador amplía la misma spec 001: eliminar también los directorios/archivos
antiguos, garantizando conservación e informando de enlaces afectados para decidir.
El plan añade retirada de 67 candidatos: 64 referencias de transición y tres
archivos con información propia que deben conservarse primero en ai/. Se mantienen
journals, imágenes, arquitectura/runbooks y docs/specs.md como fuentes compartidas.

Informe cleanup-impact.md: seis URLs a main se romperían al retirar las rutas,
cuatro en #81 activa y dos en #89 cerrada. Dos enlaces a SHA fijo permanecen
válidos. Dos enlaces locales y 29 related de procedencia se pueden reparar antes;
#114 contiene dos rutas textuales antiguas de navegación manual. Escaneo público:
48 bodies de issues, 77 de PRs y 29 comentarios; sin revisiones/inline comments.
Referencias externas no accesibles (bookmarks/chats/copias) no se pueden enumerar.

Export aislado con fuentes públicas y sin specs/ pasa usando el script existente;
sigue sin incluir ai/. No se eliminan archivos ni se editan mensajes/estados de
GitHub en esta ampliación: decisión sobre impacto/tratamiento pendiente del operador.
