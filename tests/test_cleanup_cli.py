"""Exercise CLI cleanup failure reporting without a Docker daemon."""

import os
from pathlib import Path
import shutil
import subprocess

import pytest


@pytest.fixture
def cleanup_cli(tmp_path):
    shutil.copyfile(Path(__file__).resolve().parents[1] / "tonto.sh", tmp_path / "tonto.sh")
    (tmp_path / ".env").touch()
    docker = tmp_path / "docker"
    docker.write_text(
        """#!/bin/bash
printf '%s\\n' "$*" >> "$FAKE_DOCKER_LOG"
case "$1 $2" in
  'compose config')
    [ "$FAKE_FAILURE" = config ] && exit 23
    if [ "$FAKE_FAILURE" = name ]; then echo '{}'; else
      printf '{\\n  "name": "%s",\\n  "services": {}\\n}\\n' "$COMPOSE_PROJECT_NAME"
    fi ;;
  'compose down') [ "$FAKE_FAILURE" != down ] || exit 24 ;;
  'ps -aq')
    [ "$FAKE_FAILURE" = query ] && exit 25
    [ "$FAKE_FAILURE" != container ] || echo leftover-container ;;
  'network ls') [ "$FAKE_FAILURE" != network ] || echo leftover-network ;;
  *) exit 26 ;;
esac
exit 0
"""
    )
    docker.chmod(0o755)

    def run(failure="", action="down"):
        log = tmp_path / "docker.log"
        log.write_text("")
        result = subprocess.run(
            ["bash", str(tmp_path / "tonto.sh"), action],
            env={
                **os.environ,
                "PATH": f"{tmp_path}:{os.environ['PATH']}",
                "FAKE_DOCKER_LOG": str(log),
                "FAKE_FAILURE": failure,
                "COMPOSE_PROJECT_NAME": "custom-cleanup-project",
            },
            capture_output=True,
            text=True,
            check=False,
        )
        return result, log.read_text()

    return run


@pytest.mark.parametrize("action", ["down", "stop"])
def test_cleanup_limits_scope_and_preserves_volumes(cleanup_cli, action):
    result, calls = cleanup_cli(action=action)
    assert result.returncode == 0
    assert "compose down --remove-orphans\n" in calls
    assert "label=com.docker.compose.project=custom-cleanup-project" in calls
    assert "--volumes" not in calls
    assert "prune" not in calls
    assert "Dependency volumes preserved" in result.stdout


@pytest.mark.parametrize("failure", ["container", "network"])
def test_cleanup_reports_remaining_resources(cleanup_cli, failure):
    result, _ = cleanup_cli(failure)
    assert result.returncode != 0
    assert f"leftover-{failure}" in result.stderr
    assert "Dependency volumes preserved" not in result.stdout


@pytest.mark.parametrize("failure,code", [("config", 23), ("down", 24), ("query", 25)])
def test_cleanup_propagates_docker_errors(cleanup_cli, failure, code):
    result, _ = cleanup_cli(failure)
    assert result.returncode == code


def test_cleanup_refuses_unknown_project(cleanup_cli):
    result, calls = cleanup_cli("name")
    assert result.returncode != 0
    assert "Could not determine" in result.stderr
    assert "compose down" not in calls
