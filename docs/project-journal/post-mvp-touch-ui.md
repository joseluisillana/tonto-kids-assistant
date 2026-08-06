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
