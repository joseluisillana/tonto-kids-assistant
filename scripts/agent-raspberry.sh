#!/bin/bash
set -eu

ACTION="${1:-}"
COMMAND="${2:-}"

if [ -z "$ACTION" ]; then
  echo "Usage: $0 {preflight|exec} [command]"
  exit 1
fi

if [ "$ACTION" = "exec" ] && [ -z "$COMMAND" ]; then
  echo "Command is required for exec."
  exit 1
fi

DEFAULT_KEY="$HOME/.ssh/tonto_agent_ed25519"
PI_HOST="${TONTO_PI_HOST:-tonto-pi.local}"
PI_USER="${TONTO_PI_USER:-tonto-pi-user}"
PI_SSH_KEY="${TONTO_PI_SSH_KEY:-$DEFAULT_KEY}"
PI_REPO="${TONTO_PI_REPO:-~/tonto-kids-assistant}"

if ! command -v ssh >/dev/null 2>&1; then
  echo "OpenSSH client 'ssh' was not found." >&2
  exit 1
fi

if [ ! -f "$PI_SSH_KEY" ]; then
  echo "Dedicated SSH key not found at $PI_SSH_KEY." >&2
  exit 1
fi

invoke_ssh() {
  local remote_cmd="$1"
  ssh -o BatchMode=yes -o IdentitiesOnly=yes -o ConnectTimeout=5 -i "$PI_SSH_KEY" "${PI_USER}@${PI_HOST}" "sh -lc '$remote_cmd'"
}

bootstrap_repo() {
  echo "repo='$PI_REPO'"
  echo "if [ \"\$repo\" != \"\${repo#\~/}\" ]; then repo=\"\$HOME/\${repo#\~/}\"; fi"
  echo "if [ ! -d \"\$repo\" ]; then echo \"Raspberry repo not found: \$repo\" >&2; exit 1; fi"
  echo "cd \"\$repo\""
}

if [ "$ACTION" = "preflight" ]; then
  BOOTSTRAP=$(bootstrap_repo)
  BACKEND_URL="${TONTO_BACKEND_URL:-}"
  REMOTE_SCRIPT=$(cat <<EOF
set -eu
echo "== identity =="
hostname
whoami

echo "== repository =="
$BOOTSTRAP
pwd
git status --short --branch

echo "== tools =="
missing=0
for tool in git python3 curl arecord aplay espeak; do
  if command -v "\$tool" >/dev/null 2>&1; then
    command -v "\$tool"
  else
    echo "missing: \$tool" >&2
    missing=1
  fi
done
if [ "\$missing" -ne 0 ]; then exit 1; fi

echo "== python environment =="
if [ ! -x ".venv/bin/python" ]; then
  echo "missing: .venv/bin/python" >&2
  exit 1
fi
.venv/bin/python --version
.venv/bin/python -c 'import sys; print(sys.executable)'

backend_url='$BACKEND_URL'
if [ -n "\$backend_url" ]; then
  echo "== backend health =="
  backend_url="\${backend_url%/}"
  echo "Checking \$backend_url/health"
  curl --fail --silent --show-error --connect-timeout 5 --max-time 10 "\$backend_url/health"
  echo
fi
EOF
)
  invoke_ssh "$REMOTE_SCRIPT"
elif [ "$ACTION" = "exec" ]; then
  BOOTSTRAP=$(bootstrap_repo)
  REMOTE_SCRIPT=$(cat <<EOF
set -eu
$BOOTSTRAP
$COMMAND
EOF
)
  invoke_ssh "$REMOTE_SCRIPT"
fi
