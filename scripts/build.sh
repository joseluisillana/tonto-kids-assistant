#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pwsh -NoProfile -ExecutionPolicy Bypass -File "$SCRIPT_DIR/build.ps1" -Target all
