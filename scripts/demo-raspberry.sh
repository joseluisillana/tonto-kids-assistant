#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

TONTO_BACKEND_URL="${TONTO_BACKEND_URL:-http://192.168.1.91:8000}"
TONTO_AUDIO_DEVICE="${TONTO_AUDIO_DEVICE:-plughw:CARD=Device,DEV=0}"
TONTO_RECORD_SECONDS="${TONTO_RECORD_SECONDS:-6}"
HEALTH_RETRIES=5
HEALTH_DELAY=2

check_backend_health() {
    local attempt=1
    while [ $attempt -le $HEALTH_RETRIES ]; do
        echo "Checking backend health ($attempt/$HEALTH_RETRIES)..."
        response=$(curl -sf "$TONTO_BACKEND_URL/health" 2>/dev/null || true)
        if echo "$response" | grep -q '"status":"ok"'; then
            echo "Backend is healthy."
            return 0
        fi
        echo "Backend not ready, retrying in ${HEALTH_DELAY}s..."
        sleep $HEALTH_DELAY
        attempt=$((attempt + 1))
    done
    echo "ERROR: Backend at $TONTO_BACKEND_URL is not reachable or not healthy after $HEALTH_RETRIES attempts."
    echo "Make sure the backend is running: .\\scripts\\dev.ps1 -Service backend -AllowLan"
    exit 1
}

activate_venv() {
    if [ -f "$REPO_ROOT/.venv/bin/activate" ]; then
        source "$REPO_ROOT/.venv/bin/activate"
    else
        echo "ERROR: Virtual environment not found at $REPO_ROOT/.venv"
        echo "Create the venv first: python3 -m venv $REPO_ROOT/.venv && source $REPO_ROOT/.venv/bin/activate && pip install -r $REPO_ROOT/client/requirements.txt"
        exit 1
    fi
}

start_client() {
    export TONTO_BACKEND_URL
    export TONTO_AUDIO_DEVICE
    export TONTO_RECORD_SECONDS

    echo "Starting TONTO client in voice mode..."
    echo "  Backend: $TONTO_BACKEND_URL"
    echo "  Audio device: $TONTO_AUDIO_DEVICE"
    echo "  Recording duration: ${TONTO_RECORD_SECONDS}s"
    echo ""
    python3 "$REPO_ROOT/client/main.py" --mode voice
}

echo "=== TONTO Demo Client (Raspberry) ==="
echo ""
check_backend_health
echo ""
activate_venv
echo ""
start_client
