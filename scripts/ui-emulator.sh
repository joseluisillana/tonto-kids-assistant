#!/bin/bash
# Sourced by tonto.sh; the subshell keeps temporary-file cleanup local.
run_ui_emulator() (
  set -e
  docker_os=$(docker info --format '{{.OperatingSystem}}' 2>/dev/null) || {
    echo "Cannot contact the selected Docker daemon." >&2
    exit 1
  }
  if [[ "$docker_os" == *"Docker Desktop"* ]]; then
    run_ui_desktop
    exit
  fi
  audio_dir="${1:-/dev/snd}"
  audio_groups=()
  for device in "$audio_dir"/*; do
    [ -c "$device" ] || continue
    gid=$(stat -L -c '%g' "$device")
    case " ${audio_groups[*]} " in
      *" $gid "*) ;;
      *) audio_groups+=("$gid") ;;
    esac
  done

  if [ ${#audio_groups[@]} -eq 0 ]; then
    echo "Audio hardware unavailable; audible speech and microphone require Linux audio devices."
    docker compose run --rm --build ui-emulator
    exit
  fi

  compose_files=()
  if [ -n "${COMPOSE_FILE:-}" ]; then
    IFS="${COMPOSE_PATH_SEPARATOR:-:}" read -r -a compose_files <<< "$COMPOSE_FILE"
  else
    for candidate in compose.yaml compose.yml docker-compose.yaml docker-compose.yml; do
      if [ -f "$candidate" ]; then
        compose_files+=("$candidate")
        break
      fi
    done
    if [ ${#compose_files[@]} -eq 0 ]; then
      echo "Compose file not found." >&2
      exit 1
    fi
    for candidate in compose.override.yaml compose.override.yml docker-compose.override.yaml docker-compose.override.yml; do
      if [ -f "$candidate" ]; then
        compose_files+=("$candidate")
        break
      fi
    done
  fi

  audio_override=$(mktemp "${TMPDIR:-/tmp}/tonto-ui-audio-XXXXXX.yaml")
  trap 'rm -f -- "$audio_override"' EXIT
  # Only device mappings and numeric groups are written, never expanded config.
  audio_path=${audio_dir//\\/\\\\}
  audio_path=${audio_path//\"/\\\"}
  {
    printf 'services:\n  ui-emulator:\n    devices:\n      - "%s:/dev/snd"\n    group_add:\n' "$audio_path"
    printf '      - "%s"\n' "${audio_groups[@]}"
  } > "$audio_override"
  compose_args=()
  for compose_file in "${compose_files[@]}" "$audio_override"; do
    compose_args+=(-f "$compose_file")
  done
  echo "Starting emulator with Linux audio device groups: ${audio_groups[*]}"
  docker compose "${compose_args[@]}" run --rm --build ui-emulator
)

# Desktop runs in a VM: host Unix sockets/devices cannot be used as bind mounts.
# Existing local-user X11 permissions are required; never relax them here.
run_ui_desktop() {
  set -e
  command -v socat >/dev/null || {
    echo "Docker Desktop UI requires socat on the host (not Kivy/SDL)." >&2
    exit 1
  }
  command -v setsid >/dev/null || {
    echo "Docker Desktop UI requires setsid (util-linux) to manage bridge processes." >&2
    exit 1
  }
  if [[ ! "${DISPLAY:-}" =~ ^(:|unix:)([0-9]+)(\.[0-9]+)?$ ]]; then
    echo "Docker Desktop UI requires a local X11 DISPLAY, for example :0." >&2
    exit 1
  fi
  display_number=${BASH_REMATCH[2]}
  x_socket="${TONTO_X11_SOCKET_DIR:-/tmp/.X11-unix}/X${display_number}"
  [ -S "$x_socket" ] || {
    echo "Local X11 socket unavailable. Run dev ui from the desktop session." >&2
    exit 1
  }
  x_port=${TONTO_UI_X11_PORT:-26024}
  pulse_port=${TONTO_UI_AUDIO_PORT:-24713}
  for port in "$x_port" "$pulse_port"; do
    if [[ ! "$port" =~ ^[1-9][0-9]{3,4}$ ]] || (( port > 65535 )); then
      echo "UI bridge ports must be integers between 1024 and 65535." >&2
      exit 1
    fi
  done
  if (( x_port < 6000 || pulse_port < 1024 || x_port == pulse_port )); then
    echo "X11 bridge port must be at least 6000 and differ from the audio port." >&2
    exit 1
  fi
  compose_files=()
  if [ -n "${COMPOSE_FILE:-}" ]; then
    IFS="${COMPOSE_PATH_SEPARATOR:-:}" read -r -a compose_files <<< "$COMPOSE_FILE"
  else
    for candidate in compose.yaml compose.yml docker-compose.yaml docker-compose.yml; do
      if [ -f "$candidate" ]; then
        compose_files+=("$candidate")
        break
      fi
    done
    [ ${#compose_files[@]} -gt 0 ] || { echo "Compose file not found." >&2; exit 1; }
    for candidate in compose.override.yaml compose.override.yml docker-compose.override.yaml docker-compose.override.yml; do
      if [ -f "$candidate" ]; then compose_files+=("$candidate"); break; fi
    done
  fi
  runtime_dir=$(mktemp -d "${TMPDIR:-/tmp}/tonto-ui-runtime.XXXXXX")
  bridge_pids=()
  compose_pid=""
  ui_name="tonto-ui-${runtime_dir##*/}"
  cleanup() {
    trap - EXIT
    trap '' INT TERM
    if [ -n "$compose_pid" ]; then
      docker stop "$ui_name" >/dev/null 2>&1 || true
      kill "$compose_pid" 2>/dev/null || true
      wait "$compose_pid" 2>/dev/null || true
    fi
    for pid in "${bridge_pids[@]}"; do
      kill -- "-$pid" 2>/dev/null || true
      kill "$pid" 2>/dev/null || true
      wait "$pid" 2>/dev/null || true
    done
    rm -rf -- "$runtime_dir"
  }
  trap cleanup EXIT
  trap 'exit 130' INT
  trap 'exit 143' TERM
  start_bridge() {
    local port=$1 socket=$2 label=$3 bridge_pid
    # Do not borrow a listener owned by another run/process.
    if (: > "/dev/tcp/127.0.0.1/$port") 2>/dev/null; then
      echo "$label bridge port is occupied; choose another TONTO_UI_*_PORT." >&2
      return 1
    fi
    setsid socat "TCP4-LISTEN:$port,bind=127.0.0.1,reuseaddr,fork" \
      "UNIX-CONNECT:$socket" 2>"$runtime_dir/$label.log" &
    bridge_pid=$!
    bridge_pids+=("$bridge_pid")
    sleep 0.2
    if ! kill -0 "$bridge_pid" 2>/dev/null; then
      echo "$label bridge failed to start." >&2
      return 1
    fi
  }
  start_bridge "$x_port" "$x_socket" X11
  pulse_socket="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/pulse/native"
  audio_enabled=false
  if [ -S "$pulse_socket" ]; then
    start_bridge "$pulse_port" "$pulse_socket" audio
    audio_enabled=true
  else
    echo "Desktop audio service unavailable; UI/text remain available, voice requires audio."
  fi
  desktop_override="$runtime_dir/desktop.yaml"
  {
    printf 'services:\n  ui-emulator:\n    volumes:\n      - /tmp/.X11-unix\n    environment:\n'
    printf '      - DISPLAY=host.docker.internal:%s\n' "$((x_port - 6000))"
    printf '      - LIBGL_ALWAYS_SOFTWARE=1\n      - SDL_VIDEO_X11_XSHM=0\n'
    if "$audio_enabled"; then
      printf '      - PULSE_SERVER=tcp:host.docker.internal:%s\n' "$pulse_port"
      printf '      - ALSA_CONFIG_PATH=/etc/tonto-pulse.conf\n'
    fi
  } > "$desktop_override"
  compose_args=()
  for file in "${compose_files[@]}" "$desktop_override"; do compose_args+=(-f "$file"); done
  echo "Starting Docker Desktop UI with local screen/audio bridges."
  echo "X11 must already allow your local user; no access permissions are changed."
  docker compose "${compose_args[@]}" run -T --rm --build --name "$ui_name" ui-emulator &
  compose_pid=$!
  result=0
  wait "$compose_pid" || result=$?
  exit "$result"
}
