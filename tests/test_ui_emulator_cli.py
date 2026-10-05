"""Exercise Compose audio configuration without real sound devices or Docker."""

import os
from pathlib import Path
import shutil
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
printf 'ARGS %s\\n' "$*"
previous=''
for argument in "$@"; do
  if [ "$previous" = '-f' ]; then
    printf 'FILE %s\\n' "$argument"
    cat "$argument"
  fi
  previous="$argument"
done
exit "${FAKE_DOCKER_EXIT:-0}"
''')
    for executable in binaries.iterdir():
        executable.chmod(0o755)

    def run(devices=(), code=0, custom=False, override=False):
        for device in devices:
            (audio / device).symlink_to("/dev/null")
        env = {**os.environ, "PATH": f"{binaries}:{os.environ['PATH']}",
               "TMPDIR": str(tmp_path), "FAKE_DOCKER_EXIT": str(code)}
        env.pop("COMPOSE_FILE", None)
        env.pop("COMPOSE_PATH_SEPARATOR", None)
        if custom:
            for name in ["custom file.yml", "second.yml"]:
                (tmp_path / name).write_text("services: {}\n")
            env["COMPOSE_FILE"] = "custom file.yml;second.yml"
            env["COMPOSE_PATH_SEPARATOR"] = ";"
        if override:
            (tmp_path / "docker-compose.override.yml").write_text("services: {}\n")
        result = subprocess.run(
            ["bash", "-c", 'source ./ui-emulator.sh; run_ui_emulator "$1"',
             "test-ui", str(audio)],
            cwd=tmp_path, env=env, text=True, capture_output=True, check=False,
        )
        assert not list(tmp_path.glob("tonto-ui-audio-*.yaml"))
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
