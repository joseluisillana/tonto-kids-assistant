#!/bin/bash
# Sourced by tonto.sh; the subshell keeps temporary-file cleanup local.
run_ui_emulator() (
  set -e
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
