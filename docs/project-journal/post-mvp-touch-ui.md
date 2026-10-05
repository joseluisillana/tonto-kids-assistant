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
  - Se actualizó la especificación en `specs/raspberry-touch-ui.md` para incluir el Diseño Visual (Fase 3) y redimensionar las fases posteriores.
  - Se redactó el plan de implementación en `docs/plans/raspberry-touch-ui-implementation-plan.md`.
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
  - Al mismo tiempo, la rama `main` introdujo una migración a Linux y Docker, incluyendo una especificación pendiente para emular la UI de Kivy usando contenedores (`specs/kivy-ui-docker-emulation.md`).
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

**Spec:** `specs/kivy-ui-testing-coverage.md`.
**Plan:** `docs/plans/kivy-ui-testing-coverage-plan.md`.

## 2026-10-05 — Cierre validación del emulador Linux

Punto 3 de #107 completado en PR #115: arranque Linux reparado, selección
explícita de entrada PC, tres turnos físicos y recuperación ERROR/reset 4 s.
110 Python, 25 Kivy, web/build y CI 09ef3b3 pasan; limpieza oficial correcta.
PR #115 sin borrador, lista para revisión y pendiente de merge en #108.
#107 permanece abierta hasta integración global; volumen aplazado en #114,
enlazado con docs/issues/emulator-system-volume-delay.md. #88 excluida.
Reconciliación de estados/documentación; no cambia comportamiento de producto.
