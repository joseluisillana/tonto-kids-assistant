# Implementation Plan: Kivy UI Docker Emulation

**Spec:** `specs/kivy-ui-docker-emulation.md`

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
Read `specs/kivy-ui-docker-emulation.md` and `docs/plans/kivy-ui-docker-emulation-plan.md` first.

1. In `docker-compose.yml`, add a new service named `ui-emulator`. Use `python:3.12-slim` (or similar), install system dependencies for kivy (`libsdl2-dev`, `libgl1`, etc.), run `pip install kivy`, and map the `DISPLAY` env var and `/tmp/.X11-unix` volumes.
2. In `tonto.sh`, add `ui` as an option for the `dev` command to launch the spike with `docker compose run --rm ui-emulator python spikes/ui_kivy/main.py`.
3. Update `docs/raspberry-pi-setup.md` under the Kivy UI section to explain how to use `./tonto.sh dev ui` and mention the `xhost +local:docker` step for Linux users.
4. Test the changes inside your sandbox (ensure the bash scripts have no syntax errors).
5. Follow the Git workflow to branch, commit, and push.
```
