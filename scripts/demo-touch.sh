#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

TONTO_BACKEND_URL="${TONTO_BACKEND_URL:-http://192.168.1.91:8000}"
TONTO_AUDIO_DEVICE="${TONTO_AUDIO_DEVICE:-plughw:CARD=Device,DEV=0}"
KIVY_GL_BACKEND="${KIVY_GL_BACKEND:-gl}"
KIVY_WINDOW="${KIVY_WINDOW:-sdl2}"
KCFG_KIVY_LOG_LEVEL="${KCFG_KIVY_LOG_LEVEL:-warning}"
KIVY_NO_ARGS="${KIVY_NO_ARGS:-1}"

VENV_PYTHON="$REPO_ROOT/.venv/bin/python"
HEALTH_RETRIES=5
HEALTH_DELAY=2

check_backend_health() {
    local attempt=1
    while [ $attempt -le $HEALTH_RETRIES ]; do
        echo "Checking backend health ($attempt/$HEALTH_RETRIES)..."
        response=$(curl -sf --connect-timeout 5 "$TONTO_BACKEND_URL/health" 2>/dev/null || true)
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

check_venv() {
    if [ ! -x "$VENV_PYTHON" ]; then
        echo "ERROR: Virtual environment Python not found at $VENV_PYTHON"
        echo "Create the venv first: python3 -m venv $REPO_ROOT/.venv && $REPO_ROOT/.venv/bin/python -m pip install -r $REPO_ROOT/client/requirements.txt"
        exit 1
    fi
}

start_client() {
    export TONTO_BACKEND_URL
    export TONTO_AUDIO_DEVICE
    export KIVY_GL_BACKEND
    export KIVY_WINDOW
    export KCFG_KIVY_LOG_LEVEL
    export KIVY_NO_ARGS

    echo "Starting TONTO client in touch UI mode..."
    echo "  Backend: $TONTO_BACKEND_URL"
    echo "  Audio device: $TONTO_AUDIO_DEVICE"
    echo "  Window provider: $KIVY_WINDOW"
    echo ""

    echo "Killing any existing instances..."
    pkill -f 'client.main --mode touch' || true

    echo "Launching UI in background..."
    cd "$REPO_ROOT"
    nohup env PYTHONPATH="$REPO_ROOT" "$VENV_PYTHON" -m client.main --mode touch > /tmp/tonto-ui.log 2>&1 &
    
    echo "UI started successfully! Check /tmp/tonto-ui.log for logs."
}

echo "=== TONTO Touch UI Demo Client (Raspberry) ==="
echo ""
check_backend_health
echo ""
check_venv
echo ""
start_client
