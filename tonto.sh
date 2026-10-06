#!/bin/bash
set -e
set -o pipefail
export DOCKER_UID=$(id -u)
export DOCKER_GID=$(id -g)

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

print_usage() {
    echo "TONTO CLI (Linux/Docker)"
    echo "Uso: ./tonto.sh {setup|dev|down|test|build} [target]"
    echo ""
    echo "Comandos:"
    echo "  setup [host]          - Prepara Docker; host prepara opcionalmente el IDE"
    echo "  dev [backend|ui|web|all] - Inicia los servidores en modo desarrollo"
    echo "  down (alias: stop)     - Limpia todos los contenedores y redes del proyecto, incluidos los temporales"
    echo "  test [python|ui|web|all] - Ejecuta los tests del proyecto"
    echo "  build [web|all]       - Compila los assets del proyecto web"
}

if [ $# -eq 0 ]; then
    print_usage
    exit 1
fi

COMMAND=$1
TARGET=${2:-all}

# Explicit writable mounts must exist before Docker creates root-owned paths.
case "$COMMAND" in
  setup|test|build|dev)
    mkdir -p .cache/pip .cache/npm .cache/pytest-fixtures .cache/client-audio-tests \
      web/node_modules web/dist web/.tmp-test
    ;;
esac

case "$COMMAND" in
  setup|test|build)
    # Tasks use an explicit credential-free model, not runtime .env/overrides.
    unset OPENAI_API_KEY DEVEXPERT_API_KEY COMPOSE_ENV_FILES COMPOSE_FILE COMPOSE_PROFILES
    ;;
  dev|down|stop)
    if [ ! -f .env ]; then
      cp .env.example .env || touch .env
    fi
    ;;
esac

task_compose() {
  docker compose --env-file /dev/null -f "$REPO_ROOT/docker-compose.tasks.yml" "$@"
}

case "$COMMAND" in
  setup)
    mkdir -p .cache/pip .cache/npm
    if [ "$TARGET" == "host" ]; then
      echo "Setting up optional host environment for the IDE..."
      if ! command -v python3 >/dev/null 2>&1; then
        echo "Host setup requires python3 with venv support." >&2
        exit 1
      fi
      if [ ! -x .venv/bin/python ]; then
        if ! python3 -m venv .venv; then
          echo "Host setup failed: check .venv permissions and Python venv/ensurepip support. Install missing support through your system package manager." >&2
          exit 1
        fi
      fi
      PIP_CACHE_DIR="$REPO_ROOT/.cache/pip" .venv/bin/python -m pip install \
        -r backend/requirements.txt -r client/requirements.txt \
        -r client/requirements-pc.txt -r requirements-dev.txt
      echo "Optional host environment is ready."
    elif [ "$TARGET" == "all" ]; then
      echo "Setting up Python virtual environment in Docker..."
      task_compose run --rm -u root backend chown -R "$DOCKER_UID:$DOCKER_GID" .venv .cache/pip .cache/npm
      task_compose run --rm backend /bin/bash -c "python -m venv .venv && .venv/bin/python -m pip install -r backend/requirements.txt -r client/requirements.txt -r client/requirements-pc.txt -r requirements-dev.txt"
      echo "Setting up Node environment in Docker..."
      task_compose run --rm web npm ci
      echo "Docker development environment is ready. Host .venv preserved; use setup host for the optional IDE environment."
    else
      echo "Unknown setup target: $TARGET (expected host or all)." >&2
      exit 1
    fi
    ;;
    
  dev)
    if [ "$TARGET" == "backend" ]; then
      docker compose up backend
    elif [ "$TARGET" == "web" ]; then
      docker compose up web
    elif [ "$TARGET" == "ui" ]; then
      echo "Iniciando emulador de UI..."
      source scripts/ui-emulator.sh
      run_ui_emulator
    else
      echo "Starting backend and web..."
      docker compose up backend web
    fi
    ;;
    
  down|stop)
    # Disable both sources of secret expansion before selecting project metadata.
    # Never return raw Compose diagnostics: even its errors can echo input values.
    if project_name=$(docker compose config --no-env-resolution --no-interpolate --format json 2>/dev/null |
        sed -n 's/^  "name": "\([^"]*\)",\{0,1\}$/\1/p'); then
      :
    else
      result=$?
      echo "Could not read Compose project metadata (exit $result)." >&2
      exit "$result"
    fi
    if [[ ! "$project_name" =~ ^[a-z0-9][a-z0-9_-]*$ ]]; then
      echo "Could not determine the Compose project name." >&2
      exit 1
    fi
    echo "Stopping and cleaning up project containers and networks..."
    if docker compose down --remove-orphans >/dev/null 2>&1; then
      :
    else
      result=$?
      echo "Compose cleanup failed (exit $result)." >&2
      exit "$result"
    fi
    if remaining_containers=$(docker ps -aq --filter "label=com.docker.compose.project=$project_name" 2>/dev/null) &&
        remaining_networks=$(docker network ls -q --filter "label=com.docker.compose.project=$project_name" 2>/dev/null); then
      :
    else
      result=$?
      echo "Could not verify Docker cleanup (exit $result)." >&2
      exit "$result"
    fi
    if [ -n "$remaining_containers" ] || [ -n "$remaining_networks" ]; then
      echo "Cleanup incomplete: project containers or networks remain." >&2
      exit 1
    fi
    echo "Project containers and networks removed. Dependency volumes preserved."
    echo "Note: To completely wipe the Docker-managed .venv, run: docker compose down -v"
    ;;
    
  test)
    if [ "$TARGET" == "python" ] || [ "$TARGET" == "all" ]; then
      echo "Running Python checks..."
      task_compose run --rm backend /bin/bash -c "
        export PYTHONDONTWRITEBYTECODE=1
        .venv/bin/python scripts/check_syntax.py
        .venv/bin/python -m pytest -p no:cacheprovider tests \
          --ignore=tests/test_tonto_face.py \
          --ignore=tests/test_touch_ui.py
      "
    fi

    if [ "$TARGET" == "ui" ] || [ "$TARGET" == "all" ]; then
      echo "Running Kivy UI checks..."
      # Give Xvfb a normal parent for its startup signal and an isolated socket.
      task_compose run --rm --build --no-deps \
        --volume /tmp/.X11-unix \
        -e PYTHONPATH=/app \
        -e PYTHONDONTWRITEBYTECODE=1 \
        -e KIVY_WINDOW=sdl2 \
        -e KIVY_NO_ARGS=1 \
        -e KIVY_HOME=/tmp/.kivy-test \
        -e KIVY_CLIPBOARD=dummy \
        -e LIBGL_ALWAYS_SOFTWARE=1 \
        -e XDG_CACHE_HOME=/tmp/.cache \
        -e SDL_AUDIODRIVER=dummy \
        -e SDL_VIDEODRIVER=x11 \
        ui-emulator /bin/bash -c 'xvfb-run -a -e /dev/stderr .venv/bin/python -m pytest \
          -p no:cacheprovider tests/test_tonto_face.py tests/test_touch_ui.py -v; result=$?; exit "$result"'
    fi

    if [ "$TARGET" == "web" ] || [ "$TARGET" == "all" ]; then
      echo "Running Web checks..."
      task_compose run --rm web npm run test
    fi
    ;;
    
  build)
    if [ "$TARGET" == "web" ] || [ "$TARGET" == "all" ]; then
      echo "Building Web..."
      task_compose run --rm web npm run build
    fi
    ;;
    
  *)
    print_usage
    exit 1
    ;;
esac
