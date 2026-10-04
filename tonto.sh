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
    echo "Uso: ./tonto.sh {setup|dev|test|build} [target]"
    echo ""
    echo "Comandos:"
    echo "  setup                 - Prepara el entorno (instala dependencias en los contenedores)"
    echo "  dev [backend|web|all] - Inicia los servidores en modo desarrollo"
    echo "  test [python|web|all] - Ejecuta los tests del proyecto"
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
    echo "Setting up Python virtual environment (Linux/Docker)..."
    docker compose run --rm backend /bin/bash -c "python -m venv .venv && .venv/bin/pip install -r backend/requirements.txt -r client/requirements.txt -r requirements-dev.txt"
    
    echo "Setting up Node environment (Linux/Docker)..."
    docker compose run --rm web npm ci
    
    echo "Development environment is ready."
    ;;
    
  dev)
    if [ "$TARGET" == "backend" ]; then
      docker compose up backend
    elif [ "$TARGET" == "web" ]; then
      docker compose up web
    else
      echo "Starting backend and web..."
      docker compose up backend web
    fi
    ;;
    
  test)
    if [ "$TARGET" == "python" ] || [ "$TARGET" == "all" ]; then
      echo "Running Python checks..."
      docker compose run --rm backend /bin/bash -c "
        export PYTHONDONTWRITEBYTECODE=1
        .venv/bin/python scripts/check_syntax.py
        .venv/bin/python -m pytest -p no:cacheprovider tests
      "
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
