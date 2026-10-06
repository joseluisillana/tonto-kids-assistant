# Implementation Plan: Kivy UI Docker Emulation

**Spec:** `ai/specs/012-kivy-ui-docker-emulation/spec.md`

## Extensión autorizada — 2026-10-07

Ejecutar el plan de `ai/issues/003-kivy-docker-development-audio/plan.md` en
fix/kivy-docker-desktop-audio. El ensayo independiente valida UI/audio mediante
puentes locales y ALSA-PulseAudio en imagen. Implementar launcher con detección
de daemon, preflight, manejo de señales y limpieza garantizada; mantener vía
nativa y Raspberry. Actualizar README/instrucciones, verificar sintaxis Bash,
test python y test ui, y validar arranque/voz real del stack Desktop. No instalar
paquetes host ni abrir acceso X11 global. La implementación actual sustituye
los prompts históricos de abajo; no aplicar comandos de plataformas archivadas.

## 1. Context

We need to provide an isolated Docker environment to emulate the Raspberry Pi Touch UI (Kivy spike) on developer machines without contaminating the host OS with native SDL/Kivy dependencies.

## 2. Steps

### Step 1: Update Dockerfile / Compose
- Add a new service definition `ui-emulator` in `docker-compose.yml` based on a Python image that installs the necessary dependencies (`libsdl2-dev`, `libgl1`, etc.) and `kivy`.
- Configure volume mounts for `/tmp/.X11-unix` and environment variable `DISPLAY` to allow X11 forwarding from the container to the host.

### Step 2: Update tonto.sh
- Modify `tonto.sh` to include a new target for the `dev` command, for example: `./tonto.sh dev ui`.
- Ensure this command executes `docker compose run --rm ui-emulator ...` pointing to `spikes/ui_kivy/main.py`.

### Step 3: Documentation
- Update `docs/raspberry-pi-setup.md` or the `README.md` to instruct developers on any necessary host setup (e.g. running `xhost +local:docker` before attempting to run the UI).
- Explain potential troubleshooting steps for WSL2 or macOS users (e.g., using an X Server).

## 3. Autonomous AI Prompt

**Prompt to give to OpenCode or Codex to execute this plan:**

```
Please implement the "Kivy UI Docker Emulation" spec.
Read `ai/specs/012-kivy-ui-docker-emulation/spec.md` and `ai/specs/012-kivy-ui-docker-emulation/plan.md` first.

1. In `docker-compose.yml`, add a new service named `ui-emulator`. Use `python:3.12-slim` (or similar), install system dependencies for kivy (`libsdl2-dev`, `libgl1`, etc.), run `pip install kivy`, and map the `DISPLAY` env var and `/tmp/.X11-unix` volumes.
2. In `tonto.sh`, add `ui` as an option for the `dev` command to launch the spike with `docker compose run --rm ui-emulator python spikes/ui_kivy/main.py`.
3. Update `docs/raspberry-pi-setup.md` under the Kivy UI section to explain how to use `./tonto.sh dev ui` and mention the `xhost +local:docker` step for Linux users.
4. Test the changes inside your sandbox (ensure the bash scripts have no syntax errors).
5. Follow the Git workflow to branch, commit, and push.
```


## Migration provenance

Original source: `docs/plans/kivy-ui-docker-emulation-plan.md` at baseline 818e88e. Relocated 2026-10-06;
original content/language retained with path references adjusted. Historical
commands, approvals and pending notes retain their original context.

## Record maintenance after migration

For future work, read [spec.md](spec.md), this plan and [journal.md](journal.md).
Revise the plan before implementation; preserve historical prompts as evidence,
not authorization to execute outdated commands. Mandatory root/common workflow,
Linux/Docker operation and D025 govern current work. Maintain the local journal
and synchronize definition status/updated with the parent INDEX.md in the same
change. No secrets, credentials, tokens, connection strings, PII or real customer
data; sensitive configuration uses parameter names only.
