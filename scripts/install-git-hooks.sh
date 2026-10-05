#!/bin/bash
set -eu

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GIT_DIR="$REPO_ROOT/.git"
HOOKS_DIR="$GIT_DIR/hooks"
PRE_COMMIT_PATH="$HOOKS_DIR/pre-commit"

if [ ! -d "$GIT_DIR" ]; then
  echo "Git directory not found. Run this script from a cloned repository." >&2
  exit 1
fi

mkdir -p "$HOOKS_DIR"

cat << 'EOF' > "$PRE_COMMIT_PATH"
#!/bin/sh
set -e
REPO_ROOT="$(git rev-parse --show-toplevel)"
"$REPO_ROOT/scripts/export-docs-for-notebooklm.sh"
EOF

chmod +x "$PRE_COMMIT_PATH"

echo "Installed pre-commit hook at $PRE_COMMIT_PATH"
