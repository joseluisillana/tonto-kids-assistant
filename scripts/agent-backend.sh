#!/bin/bash
set -eu

ACTION="${1:-}"
ALLOW_LAN=0

for arg in "$@"; do
  if [ "$arg" = "-AllowLan" ] || [ "$arg" = "--allow-lan" ]; then
    ALLOW_LAN=1
  fi
done

if [ -z "$ACTION" ]; then
  echo "Usage: $0 {start|stop|status|health} [-AllowLan]"
  exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

HEALTH_URL="http://127.0.0.1:8000/health"
if [ "$ALLOW_LAN" -eq 1 ]; then
  HEALTH_URL="http://0.0.0.0:8000/health"
fi

check_health() {
  local url="$1"
  if curl -sf --connect-timeout 2 "$url" | grep -q '"status":"ok"'; then
    return 0
  fi
  return 1
}

start_backend() {
  echo "Starting backend via docker compose..."
  docker compose up -d backend
  
  local attempt=1
  local max_attempts=15
  while [ $attempt -le $max_attempts ]; do
    if check_health "$HEALTH_URL"; then
       echo "Backend started successfully."
       exit 0
    fi
    sleep 1
    attempt=$((attempt+1))
  done
  echo "Backend failed to become healthy."
  exit 1
}

stop_backend() {
  echo "Stopping backend via docker compose..."
  docker compose stop backend
  docker compose rm -f backend
  echo "Backend stopped."
}

show_status() {
  echo "Status check via docker compose ps:"
  docker compose ps backend
  if check_health "$HEALTH_URL"; then
    echo "Health: ok ($HEALTH_URL)"
  else
    echo "Health: unavailable"
  fi
}

case "$ACTION" in
  start) start_backend ;;
  stop) stop_backend ;;
  status) show_status ;;
  health) 
    if check_health "$HEALTH_URL"; then
      echo "Health: ok ($HEALTH_URL)"
    else
      echo "Health check failed"
      exit 1
    fi
    ;;
  *) echo "Unknown action: $ACTION"; exit 1 ;;
esac
