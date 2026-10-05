# Kivy UI Testing Coverage — Implementation Plan

## Objective

Añadir cobertura de tests unitarios para `client/tonto_face.py` y `client/touch_ui.py`, e integrarlos en `tonto.sh test` de forma que `./tonto.sh test all` cubra backend + UI + web de manera reproducible.

## Source Spec

- Spec: `specs/kivy-ui-testing-coverage.md`
- Related docs:
  - `specs/kivy-ui-docker-emulation.md`
  - `specs/raspberry-touch-ui.md`
  - `docs/roadmap.md`

## Scope

Incluido:

- `tests/conftest.py` — Añadir `pytest_configure` hook para activar Kivy headless antes de cualquier import.
- `tests/test_tonto_face.py` — Suite de tests unitarios para `FaceState` y `TontoFace`.
- `tests/test_touch_ui.py` — Suite de tests unitarios para `TontoTouchUI` y `ProgressButton`.
- `tonto.sh` — Añadir target `test ui` y ampliar `test all` para incluirlo.
- `docs/project-journal/post-mvp-touch-ui.md` — Nota de que la cobertura de tests UI queda implementada.

Excluido:

- Tests de animación visual o pixel-level.
- Tests de integración con display o hardware real.
- Cambios en código de producto (`tonto_face.py`, `touch_ui.py`, backend).
- Cambios en `Dockerfile.ui` o `docker-compose.yml` (el contenedor ya tiene Kivy).

## Implementation Plan

### Paso 1: Activar Kivy headless en conftest.py

Añadir `pytest_configure` al `tests/conftest.py` existente. Esta función de hook se ejecuta antes de que pytest cargue los módulos de test, garantizando que Kivy arranque en modo headless:

```python
def pytest_configure(config):
    import os
    os.environ.setdefault("KIVY_WINDOW", "headless")
    os.environ.setdefault("KIVY_NO_ENV_CONFIG", "1")
    os.environ.setdefault("KIVY_HOME", "/tmp/.kivy-test")
```

> **Nota:** `setdefault` no sobreescribe si la variable ya está definida, por lo que es seguro para el entorno de CI y para el contenedor `ui-emulator`.

### Paso 2: tests/test_tonto_face.py

Crear el archivo con los siguientes tests:

- `test_face_state_constants` — Verifica los 5 valores de `FaceState`.
- `test_initial_state_is_idle` — `TontoFace()` tiene `current_state == FaceState.IDLE`.
- `test_set_state_changes_current_state[idle/listening/thinking/speaking/error]` — Parametrizado sobre los 5 estados; verifica que `current_state` cambia.
- `test_set_state_idle_idempotent` — Dos llamadas consecutivas a `set_state(IDLE)` no lanzan excepción.
- `test_set_state_error_sets_eyebrow_angle` — Tras `set_state(ERROR)`, el widget registra una animación target con `eyebrow_angle=40`.

Para evitar la dependencia del `Clock` de Kivy en los asserts, en los tests sobre propiedades destino se usará `Animation` con `d=0` o se inspeccionará el estado antes de que avance el bucle de eventos.

### Paso 3: tests/test_touch_ui.py

Crear el archivo con los siguientes tests (usando mocks de `client.main` para evitar dependencias de red/audio):

- `test_progress_button_default_progress` — `ProgressButton().progress == 0`.
- `test_touch_ui_constructs` — `TontoTouchUI()` no lanza excepciones.
- `test_touch_ui_reads_backend_url_from_env` — Con `TONTO_BACKEND_URL=http://test:9000`, `ui.backend_url == "http://test:9000"`.
- `test_touch_ui_default_backend_url` — Sin `TONTO_BACKEND_URL`, `ui.backend_url == "http://127.0.0.1:8000"`.

### Paso 4: Actualizar tonto.sh

En el bloque `test)`:

```bash
if [ "$TARGET" == "ui" ] || [ "$TARGET" == "all" ]; then
  echo "Running Kivy UI checks..."
  docker compose run --rm \
    -e KIVY_WINDOW=headless \
    -e KIVY_NO_ENV_CONFIG=1 \
    -e KIVY_HOME=/tmp/.kivy-test \
    -e PYTHONPATH=/app \
    ui-emulator /bin/bash -c \
    ".venv/bin/python -m pytest -p no:cacheprovider tests/test_tonto_face.py tests/test_touch_ui.py -v"
fi
```

En `test all`, el orden será: `python` → `ui` → `web`.

Actualizar también el `print_usage` para reflejar:
```
  test [python|ui|web|all] - Ejecuta los tests del proyecto
```

### Paso 5: Actualizar diario del proyecto

Añadir una entrada en `docs/project-journal/post-mvp-touch-ui.md` documentando que la cobertura de tests de UI queda implementada en esta rama.

## Acceptance Criteria

1. `./tonto.sh test ui` ejecuta sin errores dentro del contenedor `ui-emulator` y devuelve código 0.
2. `./tonto.sh test all` incluye los tests de UI y devuelve código 0 si todos pasan.
3. Los tests de `test_tonto_face.py` y `test_touch_ui.py` pasan sin display real.
4. `./tonto.sh test python` sigue funcionando sin cambios (los nuevos tests no se ejecutan en el contenedor `backend`).
5. El help de `tonto.sh` muestra el nuevo target `ui`.

## Verification

```bash
./tonto.sh test python     # No debe verse afectado
./tonto.sh test ui         # Nuevo target
./tonto.sh test web        # No debe verse afectado
./tonto.sh test all        # Debe incluir python + ui + web
git diff --check
git status --short --branch
```

## Implementation Prompt

```text
Implement the spec in specs/kivy-ui-testing-coverage.md.

Before editing:
- Read AGENTS.md.
- Read docs/ai-assisted-workflow.md.
- Read specs/kivy-ui-testing-coverage.md and docs/plans/kivy-ui-testing-coverage-plan.md.
- Run git branch --show-current and git status --short --branch.
- Confirm you are on branch feature/kivy-ui-testing-coverage.

Task:
1. In tests/conftest.py, add a pytest_configure hook that sets KIVY_WINDOW=headless,
   KIVY_NO_ENV_CONFIG=1, and KIVY_HOME=/tmp/.kivy-test using os.environ.setdefault.
2. Create tests/test_tonto_face.py with the tests described in the plan.
3. Create tests/test_touch_ui.py with the tests described in the plan.
4. Update tonto.sh: add "ui" as a valid target for "test", include it in "test all",
   and update the print_usage help text.
5. Append a brief note to docs/project-journal/post-mvp-touch-ui.md recording this change.

Do NOT change client/tonto_face.py, client/touch_ui.py, backend code, or docker-compose.yml
beyond what the spec requires.

Verification:
- Run: ./tonto.sh test python
- Run: ./tonto.sh test ui
- Run: ./tonto.sh test all
- Report any checks that could not be run and why.

Delivery:
- Summarize changed files.
- Summarize behavior implemented.
- Summarize verification results.
```

## Workflow Isolation

- **Branch:** `feature/kivy-ui-testing-coverage`
- **Worktree:** La rama actual. No se necesita worktree adicional.
- **Parallel-safe:** Sí. Solo toca archivos de test y `tonto.sh`.
- **Collision risk:** `tests/conftest.py` y `tonto.sh` son los únicos archivos compartidos con otras ramas activas potenciales.
- **Integration note:** Si `main` recibe cambios en `tonto.sh` mientras esta rama está activa, hacer rebase antes de abrir PR.
- **GitHub tracking:** Crear una Issue nueva vinculada a la épica de estabilidad.

## Notes / Assumptions

- El contenedor `ui-emulator` ya tiene Kivy 2.3.0 instalado en `.venv` (verificado durante la Issue #84).
- `KIVY_WINDOW=headless` es suficiente para que los tests corran sin SDL2/display en el contenedor actual.
- Los tests de propiedades de estado se hacen sobre los valores iniciales del widget (antes de que `Clock.tick()` avance las animaciones), lo que hace la aserción determinista.
- No se necesita `xvfb` para los tests headless (solo para el emulador visual de `dev ui`).
