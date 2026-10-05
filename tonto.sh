#!/bin/bash
set -e
export DOCKER_UID=$(id -u)
export DOCKER_GID=$(id -g)

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

# Asegurar que el .env exista para docker compose
if [ ! -f .env ]; then
  cp .env.example .env || touch .env
fi

print_usage() {
    echo "TONTO CLI (Linux/Docker)"
    echo "Uso: ./tonto.sh {setup|dev|down|test|build} [target]"
    echo ""
    echo "Comandos:"
    echo "  setup                 - Prepara el entorno (instala dependencias en los contenedores)"
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

case "$COMMAND" in
  setup)
    echo "Setting up Python virtual environment in Docker..."
    docker compose run --rm -u root backend chown -R ${DOCKER_UID:-1000}:${DOCKER_GID:-1000} .venv
    docker compose run --rm backend /bin/bash -c "python -m venv .venv && .venv/bin/pip install -r backend/requirements.txt -r client/requirements.txt -r client/requirements-pc.txt -r requirements-dev.txt"
    
    echo "Setting up Python virtual environment on Host (for IDE)..."
    if command -v python3 &> /dev/null; then
        rm -rf .venv
        if python3 -m venv .venv; then
            .venv/bin/pip install -r backend/requirements.txt -r client/requirements.txt -r client/requirements-pc.txt -r requirements-dev.txt || echo "Warning: Could not install host dependencies, but container is setup."
        else
            echo "Warning: Could not create host .venv (maybe missing python3-venv?). Your IDE might lack autocompletion."
        fi
    else
        echo "python3 not found on host. Skipping host .venv creation. (Your IDE might lack autocompletion)"
    fi
    
    echo "Setting up Node environment (Linux/Docker)..."
    docker compose run --rm web npm ci
    
    echo "Development environment is ready."
    ;;
    
  dev)
    if [ "$TARGET" == "backend" ]; then
      docker compose up backend
    elif [ "$TARGET" == "web" ]; then
      docker compose up web
    elif [ "$TARGET" == "ui" ]; then
      echo "Iniciando emulador de UI..."
      docker compose run --rm ui-emulator
    else
      echo "Starting backend and web..."
      docker compose up backend web
    fi
    ;;
    
  down|stop)
    # Never print the full configuration: it may contain credentials from .env.
    compose_config=$(docker compose config --format json)
    project_name=$(sed -n 's/^  "name": "\([^"]*\)",\{0,1\}$/\1/p' <<< "$compose_config")
    if [ -z "$project_name" ]; then
      echo "Could not determine the Compose project name." >&2
      exit 1
    fi
    echo "Stopping and cleaning up all containers for project $project_name..."
    docker compose down --remove-orphans
    remaining_containers=$(docker ps -aq --filter "label=com.docker.compose.project=$project_name")
    remaining_networks=$(docker network ls -q --filter "label=com.docker.compose.project=$project_name")
    if [ -n "$remaining_containers" ] || [ -n "$remaining_networks" ]; then
      echo "Cleanup incomplete for project $project_name." >&2
      echo "Remaining containers: ${remaining_containers:-none}" >&2
      echo "Remaining networks: ${remaining_networks:-none}" >&2
      exit 1
    fi
    echo "Project containers and networks removed. Dependency volumes preserved."
    echo "Note: To completely wipe the Docker-managed .venv, run: docker compose down -v"
    ;;
    
  test)
    if [ "$TARGET" == "python" ] || [ "$TARGET" == "all" ]; then
      echo "Running Python checks..."
      docker compose run --rm backend /bin/bash -c "
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
      docker compose run --rm --build \
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
      docker compose run --rm web npm run test
    fi
    ;;
    
  build)
    if [ "$TARGET" == "web" ] || [ "$TARGET" == "all" ]; then
      echo "Building Web..."
      docker compose run --rm web npm run build
    fi
    ;;
    
  *)
    print_usage
    exit 1
    ;;
esac
