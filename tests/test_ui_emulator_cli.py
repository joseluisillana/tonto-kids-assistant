"""Exercise Compose audio configuration without real sound devices or Docker."""

import os
from pathlib import Path
import shutil
import socket
import signal
import time
import subprocess

import pytest


@pytest.fixture
def ui_cli(tmp_path):
    helper = Path(__file__).resolve().parents[1] / "scripts/ui-emulator.sh"
    shutil.copyfile(helper, tmp_path / "ui-emulator.sh")
    (tmp_path / "docker-compose.yml").write_text("services: {}\n")
    audio = tmp_path / "audio"
    audio.mkdir()
    (audio / "by-path").mkdir()
    binaries = tmp_path / "bin"
    binaries.mkdir()
    (binaries / "stat").write_text('''#!/bin/bash
case "${@: -1}" in
  */pcmC1*) echo 30 ;;
  */controlC0|*/pcmC0*) echo 29 ;;
  *) echo 0 ;;
esac
''')
    (binaries / "docker").write_text('''#!/bin/bash
if [ "$1" = info ]; then
  echo "${FAKE_DOCKER_OS:-Linux}"
  exit 0
fi
if [ "$1" = stop ]; then exit 0; fi
printf 'ARGS %s\\n' "$*"
previous=''
for argument in "$@"; do
  if [ "$previous" = '-f' ]; then
    printf 'FILE %s\\n' "$argument"
    cat "$argument"
  fi
  previous="$argument"
done
if [ "${FAKE_DOCKER_HANG:-0}" = 1 ]; then
  touch "$DOCKER_TEST_READY"
  while true; do sleep 0.05; done
fi
exit "${FAKE_DOCKER_EXIT:-0}"
''')
    for executable in binaries.iterdir():
        executable.chmod(0o755)

    def run(devices=(), code=0, custom=False, override=False, desktop=False,
            pulse=True, bridge_failure=False, ports=None, terminate=False,
            display=":0", occupied=False, cli=False):
        for device in devices:
            (audio / device).symlink_to("/dev/null")
        env = {**os.environ, "PATH": f"{binaries}:{os.environ['PATH']}",
               "TMPDIR": str(tmp_path), "FAKE_DOCKER_EXIT": str(code)}
        env.pop("COMPOSE_FILE", None)
        env.pop("COMPOSE_PATH_SEPARATOR", None)
        sockets = []
        if desktop:
            x_dir = tmp_path / "x11"
            x_dir.mkdir()
            pulse_dir = tmp_path / "runtime" / "pulse"
            pulse_dir.mkdir(parents=True)
            for path in [x_dir / "X0"] + ([pulse_dir / "native"] if pulse else []):
                sock = socket.socket(socket.AF_UNIX)
                sock.bind(str(path))
                sockets.append(sock)
            env.update(FAKE_DOCKER_OS="Docker Desktop", DISPLAY=display,
                       TONTO_X11_SOCKET_DIR=str(x_dir),
                       XDG_RUNTIME_DIR=str(pulse_dir.parent),
                       BRIDGE_TEST_LOG=str(tmp_path / "bridges.log"))
            (binaries / "socat").write_text('''#!/bin/bash
echo "$*" >> "$BRIDGE_TEST_LOG"
trap 'echo stopped >> "$BRIDGE_TEST_LOG"; exit 0' TERM
if [ "${BRIDGE_FAIL:-0}" = 1 ]; then exit 1; fi
while true; do sleep 0.05; done
''')
            (binaries / "socat").chmod(0o755)
            if bridge_failure:
                env["BRIDGE_FAIL"] = "1"
            if ports:
                env.update(TONTO_UI_X11_PORT=str(ports[0]), TONTO_UI_AUDIO_PORT=str(ports[1]))
            if terminate:
                env.update(FAKE_DOCKER_HANG="1", DOCKER_TEST_READY=str(tmp_path / "ready"))
            if occupied:
                listener = socket.socket()
                listener.bind(("127.0.0.1", 26024))
                listener.listen()
                sockets.append(listener)
        if custom:
            for name in ["custom file.yml", "second.yml"]:
                (tmp_path / name).write_text("services: {}\n")
            env["COMPOSE_FILE"] = "custom file.yml;second.yml"
            env["COMPOSE_PATH_SEPARATOR"] = ";"
        if override:
            (tmp_path / "docker-compose.override.yml").write_text("services: {}\n")
        command = ["bash", "-c", 'source ./ui-emulator.sh; run_ui_emulator "$1"',
                   "test-ui", str(audio)]
        if cli:
            project_root = Path(__file__).resolve().parents[1]
            shutil.copyfile(project_root / "tonto.sh", tmp_path / "tonto.sh")
            (tmp_path / "scripts").mkdir()
            shutil.copyfile(helper, tmp_path / "scripts" / "ui-emulator.sh")
            (tmp_path / ".env").touch()
            command = ["bash", "./tonto.sh", "dev", "ui"]
        if terminate:
            proc = subprocess.Popen(command, cwd=tmp_path, env=env, text=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    start_new_session=True)
            deadline = time.monotonic() + 5
            while not (tmp_path / "ready").exists() and proc.poll() is None and time.monotonic() < deadline:
                time.sleep(0.02)
            os.killpg(proc.pid, signal.SIGTERM)
            stdout, stderr = proc.communicate(timeout=5)
            result = subprocess.CompletedProcess(command, proc.returncode, stdout, stderr)
        else:
            result = subprocess.run(command, cwd=tmp_path, env=env, text=True,
                                    capture_output=True, check=False, timeout=10)
        assert not list(tmp_path.glob("tonto-ui-audio-*.yaml"))
        assert not list(tmp_path.glob("tonto-ui-runtime.*"))
        for sock in sockets:
            sock.close()
        if desktop and not bridge_failure and not ports and display == ":0" and not occupied:
            bridge_log = (tmp_path / "bridges.log").read_text()
            assert "bind=127.0.0.1" in bridge_log
            assert bridge_log.count("stopped") == (2 if pulse else 1)
        return result

    return run


def test_without_character_devices_keeps_normal_compose_run(ui_cli):
    result = ui_cli()
    assert result.returncode == 0
    assert "Audio hardware unavailable" in result.stdout
    assert "ARGS compose run --rm --build ui-emulator" in result.stdout
    assert "FILE" not in result.stdout


def test_real_device_group_ignores_by_path_and_deduplicates(ui_cli):
    result = ui_cli(["controlC0", "pcmC0D0p"])
    assert result.returncode == 0
    assert 'group_add:\n      - "29"\n' in result.stdout
    assert '      - "0"' not in result.stdout
    assert result.stdout.count('      - "29"') == 1
    assert "--device" not in result.stdout and "--group-add" not in result.stdout
    assert ":/dev/snd" in result.stdout


def test_multiple_device_groups_are_preserved(ui_cli):
    result = ui_cli(["controlC0", "pcmC1D0p"])
    assert '      - "29"\n      - "30"' in result.stdout


@pytest.mark.parametrize("devices", [[], ["controlC0"]])
def test_compose_failure_propagates_and_removes_temporary_file(ui_cli, devices):
    result = ui_cli(devices, code=37)
    assert result.returncode == 37


def test_custom_files_separator_and_spaces_are_preserved(ui_cli):
    result = ui_cli(["controlC0"], custom=True)
    assert result.returncode == 0
    assert "FILE custom file.yml\n" in result.stdout
    assert "FILE second.yml\n" in result.stdout
    assert "FILE docker-compose.yml" not in result.stdout


def test_default_compose_override_is_preserved(ui_cli):
    result = ui_cli(["controlC0"], override=True)
    assert "FILE docker-compose.yml\n" in result.stdout
    assert "FILE docker-compose.override.yml\n" in result.stdout


def test_desktop_uses_bridges_without_devices_and_cleans_up(ui_cli):
    result = ui_cli(desktop=True)
    assert result.returncode == 0
    assert "DISPLAY=host.docker.internal:20024" in result.stdout
    assert "PULSE_SERVER=tcp:host.docker.internal:24713" in result.stdout
    assert "ALSA_CONFIG_PATH=/etc/tonto-pulse.conf" in result.stdout
    assert "devices:" not in result.stdout
    assert "      - /tmp/.X11-unix" in result.stdout


def test_desktop_without_audio_still_launches_ui(ui_cli):
    result = ui_cli(desktop=True, pulse=False)
    assert result.returncode == 0
    assert "UI/text remain available" in result.stdout
    assert "PULSE_SERVER=" not in result.stdout


def test_desktop_compose_failure_cleans_bridges(ui_cli):
    result = ui_cli(desktop=True, code=37, custom=True)
    assert result.returncode == 37
    assert "FILE custom file.yml" in result.stdout


def test_desktop_failed_bridge_does_not_launch_container(ui_cli):
    result = ui_cli(desktop=True, bridge_failure=True)
    assert result.returncode != 0
    assert "bridge failed to start" in result.stderr
    assert "ARGS compose" not in result.stdout


def test_desktop_termination_cleans_up(ui_cli):
    result = ui_cli(desktop=True, terminate=True)
    assert result.returncode != 0


def test_desktop_cli_termination_cleans_up(ui_cli):
    result = ui_cli(desktop=True, terminate=True, cli=True)
    assert result.returncode != 0


def test_desktop_rejects_remote_display(ui_cli):
    result = ui_cli(desktop=True, display="remote:0")
    assert result.returncode != 0
    assert "requires a local X11 DISPLAY" in result.stderr


def test_desktop_does_not_borrow_occupied_port(ui_cli):
    result = ui_cli(desktop=True, occupied=True)
    assert result.returncode != 0
    assert "bridge port is occupied" in result.stderr
    assert "ARGS compose" not in result.stdout


@pytest.mark.parametrize("ports", [(6000, 6000), (1234, 24713), (26024, 70000)])
def test_desktop_rejects_invalid_ports_before_launch(ui_cli, ports):
    result = ui_cli(desktop=True, ports=ports)
    assert result.returncode != 0
    assert "ARGS compose" not in result.stdout
