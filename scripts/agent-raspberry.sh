#!/bin/bash
set -eu

SKIP_IF_MISSING=0
POSITIONAL=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-if-missing)
      SKIP_IF_MISSING=1
      shift
      ;;
    *)
      POSITIONAL+=("$1")
      shift
      ;;
  esac
done

if [ ${#POSITIONAL[@]} -gt 0 ]; then
  set -- "${POSITIONAL[@]}"
else
  set --
fi

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
  if [ "${TONTO_MOCK_HARDWARE:-0}" = "1" ] || [ "$SKIP_IF_MISSING" -eq 1 ]; then
    echo "Skipping hardware validation: SSH key not found at $PI_SSH_KEY and mock/skip flag is active."
    exit 0
  else
    echo "Error: Dedicated SSH key not found at $PI_SSH_KEY." >&2
    echo "If you want to test with a physical Raspberry Pi, generate a key or provide one:" >&2
    echo "  ssh-keygen -t ed25519 -f $DEFAULT_KEY -N ''" >&2
    echo "Or set the TONTO_PI_SSH_KEY environment variable to your key path." >&2
    echo "If you are running in an environment without hardware (e.g. CI or automated agents), set TONTO_MOCK_HARDWARE=1 or pass --skip-if-missing." >&2
    exit 1
  fi
fi

invoke_ssh() {
  local remote_cmd="$1"
  local escaped_cmd="${remote_cmd//\'/\'\"\'\"\'}"
  ssh -o BatchMode=yes -o IdentitiesOnly=yes -o ConnectTimeout=5 -i "$PI_SSH_KEY" "${PI_USER}@${PI_HOST}" "sh -lc '$escaped_cmd'"
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
