# Kivy UI Testing Coverage

**Status:** Draft
**Date:** 2026-10-05
**Branch:** `feature/kivy-ui-testing-coverage`

## 1. Contexto

Tras la implementación de la interfaz táctil Kivy (Issue #84, Fases 3-6) y su merge en `main`, la suite de tests del proyecto no incluye ninguna cobertura sobre el código de la UI gráfica:

- `client/tonto_face.py` — Componente de cara animada (`TontoFace`, `FaceState`, transiciones de estado)
- `client/touch_ui.py` — Aplicación Kivy táctil (`TontoTouchUI`, `ProgressButton`, callbacks de interacción)

La ausencia de tests sobre estos módulos es una brecha de estabilidad: cualquier regresión en la lógica de estados o en los callbacks de la UI pasaría desapercibida en CI.

El reto técnico es que ambos módulos importan Kivy al nivel de módulo, lo que impide un `import` directo en un entorno sin display. La solución es utilizar el modo headless de Kivy (`KIVY_WINDOW=headless`, `KIVY_NO_ENV_CONFIG=1`) que permite levantar el runtime sin SDL2/OpenGL.

## 2. Objetivos

1. Añadir una suite de tests unitarios para `client/tonto_face.py` que valide la lógica de estados sin display.
2. Añadir tests unitarios básicos para `client/touch_ui.py` que validen la construcción del widget y los callbacks.
3. Extender `tonto.sh test` con un target `ui` que ejecute estos tests dentro del contenedor `ui-emulator` (que ya tiene las dependencias Kivy instaladas).
4. Incluir el target `ui` dentro de `./tonto.sh test all` para que la validación completa cubra backend + web + UI.

## 3. Alcance

**Incluido:**

- `tests/test_tonto_face.py` — Tests de `FaceState` y `TontoFace.set_state()` en modo headless.
- `tests/test_touch_ui.py` — Tests de construcción del `TontoTouchUI` y `ProgressButton` en modo headless.
- Actualización de `tonto.sh` para añadir `test ui` y ampliar `test all`.
- Actualización del help text de `tonto.sh`.
- Actualización del diario del proyecto.

**Excluido:**

- Tests de integración end-to-end con display real (pertenecen a Fase 7 / Kiosk).
- Tests de animación visual/píxel (no son unitarios; requieren renderizado real).
- Cambios en el código de producto (`tonto_face.py`, `touch_ui.py`).
- Cambios en el Dockerfile o docker-compose más allá de lo estrictamente necesario para ejecutar los tests.

## 4. Comportamiento esperado de los tests

### 4.1 `tests/test_tonto_face.py`

El entorno headless se configura mediante variables de entorno antes de cualquier import de Kivy.
Esto se centraliza en `tests/conftest.py` como un fixture de sesión.

Tests:

| Test | Qué verifica |
|---|---|
| `test_face_state_constants` | `FaceState` expone exactamente las 5 constantes: `IDLE`, `LISTENING`, `THINKING`, `SPEAKING`, `ERROR` |
| `test_initial_state_is_idle` | Al construir `TontoFace`, `current_state` es `FaceState.IDLE` |
| `test_set_state_changes_current_state` | `set_state(s)` actualiza `current_state` para cada uno de los 5 estados |
| `test_set_state_idle_idempotent` | Llamar `set_state(IDLE)` dos veces seguidas no lanza excepción |
| `test_set_state_error_properties` | Tras `set_state(ERROR)`, el widget tiene `eyebrow_angle == 40` |
| `test_set_state_speaking_properties` | Tras `set_state(SPEAKING)`, el widget tiene `mouth_oval_opacity == ... ` (animación iniciada) |

### 4.2 `tests/test_touch_ui.py`

| Test | Qué verifica |
|---|---|
| `test_progress_button_constructs` | `ProgressButton` se construye sin lanzar excepciones |
| `test_touch_ui_constructs` | `TontoTouchUI` se construye con las variables de entorno de backend correctas |
| `test_touch_ui_backend_url_from_env` | `TONTO_BACKEND_URL` se lee correctamente en el constructor |
| `test_touch_ui_default_backend_url` | Sin `TONTO_BACKEND_URL`, el valor por defecto es `http://127.0.0.1:8000` |

### 4.3 `tonto.sh test ui`

```bash
./tonto.sh test ui
```

Ejecutará dentro del contenedor `ui-emulator`:

```bash
KIVY_WINDOW=headless KIVY_NO_ENV_CONFIG=1 KIVY_HOME=/tmp/.kivy \
  .venv/bin/python -m pytest tests/test_tonto_face.py tests/test_touch_ui.py -v
```

### 4.4 `tonto.sh test all`

Pasará a ejecutar secuencialmente: `python` → `ui` → `web`.

## 5. Estrategia de entorno headless

El fixture de sesión en `conftest.py` establecerá las variables de entorno **antes** de que pytest cargue cualquier módulo de test:

```python
# tests/conftest.py (añadir al existente)
import os

def pytest_configure(config):
    """Configure Kivy headless mode before any module import."""
    os.environ.setdefault("KIVY_WINDOW", "headless")
    os.environ.setdefault("KIVY_NO_ENV_CONFIG", "1")
    os.environ.setdefault("KIVY_HOME", "/tmp/.kivy-test")
```

Esto es suficiente para que el runtime Kivy se inicialice sin SDL2 en el contenedor `ui-emulator`.

## 6. Criterios de Aceptación (DoD)

1. `./tonto.sh test ui` ejecuta correctamente dentro del contenedor `ui-emulator` y retorna código 0.
2. Los tests de `test_tonto_face.py` y `test_touch_ui.py` pasan sin requerir display real.
3. `./tonto.sh test all` incluye la ejecución de los tests de UI y retorna código 0 si todos pasan.
4. El help de `tonto.sh` refleja el nuevo target `ui`.
5. Ningún test de backend ni web se ve afectado.

## 7. Riesgos

| Riesgo | Mitigación |
|---|---|
| Kivy headless no disponible en imagen `backend` | Los tests de UI se ejecutan exclusivamente en el contenedor `ui-emulator` que ya tiene Kivy |
| `conftest.py` afecta a tests de backend | Las variables de entorno solo las necesita Kivy; son inocuas para FastAPI/pytest estándar |
| Animaciones de Kivy asíncronas dificultan la aserción de propiedades | Los tests comprueban el estado **justo después** de `set_state()`, antes de que el `Clock` avance |
