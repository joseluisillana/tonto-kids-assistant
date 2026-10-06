"""Validate setup isolation and failure propagation without a Docker daemon."""

import os
from pathlib import Path
import shutil
import subprocess

import pytest


@pytest.fixture
def setup_cli(tmp_path):
    shutil.copyfile(Path(__file__).resolve().parents[1] / "tonto.sh", tmp_path / "tonto.sh")
    (tmp_path / ".env").touch()
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for name, body in {
        "docker": 'echo "$*" >> "$SETUP_LOG"\nshift 5\n[ "$FAIL_AT" != "compose $*" ] || exit 37\nexit 0\n',
        "python3": 'echo "host-python $*" >> "$SETUP_LOG"\nexit 38\n',
    }.items():
        executable = bin_dir / name
        executable.write_text("#!/bin/bash\n" + body)
        executable.chmod(0o755)
    host_dir = tmp_path / ".venv" / "bin"
    host_dir.mkdir(parents=True)
    host_python = host_dir / "python"
    host_python.write_text('#!/bin/bash\necho "host-pip $*" >> "$SETUP_LOG"\nexit "${HOST_PIP_EXIT:-0}"\n')
    host_python.chmod(0o755)
    original = host_python.read_bytes()

    def run(target=None, failure="", host_pip_exit=0, missing_env=False):
        if missing_env:
            host_python.unlink()
        log = tmp_path / "calls"
        log.write_text("")
        result = subprocess.run(
            ["bash", str(tmp_path / "tonto.sh"), "setup", *([target] if target else [])],
            env={**os.environ, "PATH": f"{bin_dir}:{os.environ['PATH']}",
                 "SETUP_LOG": str(log), "FAIL_AT": failure,
                 "HOST_PIP_EXIT": str(host_pip_exit)},
            capture_output=True, text=True, check=False,
        )
        if not missing_env:
            assert host_python.read_bytes() == original
        return result, log.read_text()

    return run


def test_docker_setup_preserves_host_and_never_runs_host_python(setup_cli):
    result, calls = setup_cli()
    assert result.returncode == 0
    assert "host-python" not in calls and "host-pip" not in calls
    assert "--env-file /dev/null -f " in calls
    assert "docker-compose.tasks.yml run --rm web npm ci" in calls
    assert "Docker development environment is ready" in result.stdout


def test_docker_setup_does_not_require_host_venv(setup_cli):
    result, calls = setup_cli(missing_env=True)
    assert result.returncode == 0
    assert "host-python" not in calls


@pytest.mark.parametrize("failure", [
    "compose run --rm web npm ci",
    "compose run --rm backend /bin/bash -c python -m venv .venv && .venv/bin/python -m pip install -r backend/requirements.txt -r client/requirements.txt -r client/requirements-pc.txt -r requirements-dev.txt",
])
def test_required_setup_failure_cannot_report_success(setup_cli, failure):
    result, _ = setup_cli(failure=failure)
    assert result.returncode == 37
    assert "environment is ready" not in result.stdout


def test_optional_host_reuses_environment_without_docker(setup_cli):
    result, calls = setup_cli("host")
    assert result.returncode == 0
    assert "host-pip -m pip install" in calls
    assert "compose" not in calls and "host-python" not in calls


def test_host_pip_failure_propagates(setup_cli):
    result, _ = setup_cli("host", host_pip_exit=39)
    assert result.returncode == 39
    assert "environment is ready" not in result.stdout


def test_host_venv_failure_is_explicit(setup_cli):
    result, calls = setup_cli("host", missing_env=True)
    assert result.returncode != 0
    assert "venv/ensurepip" in result.stderr
    assert "compose" not in calls


def test_invalid_setup_target_fails(setup_cli):
    result, calls = setup_cli("unknown")
    assert result.returncode != 0
    assert calls == ""
