"""Official task commands must not use runtime env files or credentials."""

import os
from pathlib import Path
import shutil
import subprocess

import pytest


@pytest.mark.parametrize("command", [
    ["setup"], ["test", "python"], ["test", "ui"], ["test", "web"],
    ["test", "all"], ["build", "web"], ["build", "all"],
])
@pytest.mark.parametrize("with_env", [False, True])
def test_tasks_ignore_runtime_configuration(tmp_path, command, with_env):
    repo = Path(__file__).resolve().parents[1]
    shutil.copyfile(repo / "tonto.sh", tmp_path / "tonto.sh")
    canary = "invented-task-canary"
    env_file = tmp_path / ".env"
    fixture = f"OPENAI_API_KEY={canary}\nCOMPOSE_FILE=runtime-only.yml\n"
    if with_env:
        env_file.write_text(fixture)
    docker = tmp_path / "docker"
    docker.write_text('''#!/bin/bash
if [ -n "${OPENAI_API_KEY:-}${DEVEXPERT_API_KEY:-}${COMPOSE_ENV_FILES:-}${COMPOSE_FILE:-}${COMPOSE_PROFILES:-}" ]; then
  echo "Unexpected credential or runtime configuration" >&2; exit 41
fi
[ "$1 $2 $3 $4" = 'compose --env-file /dev/null -f' ] || exit 42
case "$5" in */docker-compose.tasks.yml) ;; *) exit 43 ;; esac
printf '%s\n' "$*" >> "$TASK_LOG"
exit "${TASK_EXIT:-0}"
''')
    docker.chmod(0o755)
    log = tmp_path / "calls"
    result = subprocess.run(
        ["bash", str(tmp_path / "tonto.sh"), *command],
        env={**os.environ, "PATH": f"{tmp_path}:{os.environ['PATH']}",
             "OPENAI_API_KEY": canary, "DEVEXPERT_API_KEY": canary,
             "COMPOSE_FILE": "runtime-only.yml", "COMPOSE_ENV_FILES": "private.env",
             "COMPOSE_PROFILES": "runtime", "TASK_LOG": str(log)},
        capture_output=True, text=True,
    )
    if canary in result.stdout + result.stderr + log.read_text():
        pytest.fail("Task exposed a fixture credential", pytrace=False)
    assert result.returncode == 0
    if with_env:
        assert env_file.read_text() == fixture
    else:
        assert not env_file.exists()
    assert " up " not in log.read_text()


def test_task_compose_has_no_runtime_credentials():
    # Guard regressions before a Compose process can resolve a secret source.
    text = (Path(__file__).resolve().parents[1] / "docker-compose.tasks.yml").read_text()
    for forbidden in ("env_file:", "API_KEY", "depends_on:", "ports:", "secrets:"):
        assert forbidden not in text
