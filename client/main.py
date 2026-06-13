#!/usr/bin/env python3
import argparse
import json
import os
import shlex
import socket
import subprocess
import sys
import threading
import uuid
from typing import Callable, Optional
import urllib.error
import urllib.request


TEXT_TIMEOUT_SECONDS = 10
VOICE_TIMEOUT_SECONDS = 30
DEFAULT_TTS_ARGS = "-v es -s 135 -g 8"


def main() -> int:
    parser = argparse.ArgumentParser(description="TONTO Kids Assistant Client")
    parser.add_argument("--mode", choices=["text", "voice"], default="text")
    args = parser.parse_args()

    backend_url = os.environ.get("TONTO_BACKEND_URL")
    if not backend_url:
        print("Set TONTO_BACKEND_URL to the backend address, for example http://192.168.1.10:8000")
        return 1

    session_id = f"local-session-{uuid.uuid4()}"

    print("TONTO Kids Assistant Client")
    print(f"Session: {session_id}")

    if args.mode == "text":
        return text_loop(backend_url, session_id)
    return voice_loop(backend_url, session_id)


def text_loop(backend_url: str, session_id: str) -> int:
    chat_url = f"{backend_url.rstrip('/')}/chat"
    print("Type a message and press Enter. Type 'exit' or 'quit' to stop.")

    while True:
        try:
            message = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if not message:
            continue
        if message.lower() in {"exit", "quit"}:
            return 0

        response_text = send_message(chat_url, session_id, message)
        if response_text is None:
            continue

        print(f"TONTO: {response_text}")
        speak(response_text)


def voice_loop(backend_url: str, session_id: str) -> int:
    audio_url = f"{backend_url.rstrip('/')}/chat/audio"
    chat_url = f"{backend_url.rstrip('/')}/chat"
    device_id = os.environ.get("TONTO_DEVICE_ID", "tonto-pi")
    device = os.environ.get("TONTO_AUDIO_DEVICE")
    record_seconds_default = os.environ.get("TONTO_RECORD_SECONDS", "6")
    try:
        record_seconds = max(1, min(10, int(record_seconds_default)))
    except ValueError:
        record_seconds = 6
    audio_path = os.environ.get("TONTO_AUDIO_PATH", "/tmp/tonto-turn.wav")

    print("Voice mode: press Enter to record, or type a message.")
    print("Type 'exit' or 'quit' to stop.")

    while True:
        try:
            cmd = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if cmd.lower() in {"exit", "quit"}:
            return 0

        if cmd:
            response_text = send_message(chat_url, session_id, cmd)
            if response_text is None:
                continue
            print(f"TONTO: {response_text}")
            speak(response_text)
            continue

        wav_bytes = capture_audio(device, record_seconds, audio_path, show_progress=True)
        if wav_bytes is None:
            continue

        print("Processing...")
        audio_response = send_audio(
            audio_url, session_id, device_id, wav_bytes, record_seconds * 1000
        )
        if audio_response is None:
            continue

        print(f"Transcript: {audio_response['transcript']}")
        print(f"TONTO: {audio_response['response']}")
        speak(audio_response["response"])


def _filter_alsa_warnings(stderr: str) -> str:
    """Remove known ALSA/JACK warning lines from stderr output."""
    if not stderr:
        return ""
    filtered = []
    for line in stderr.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if "ALSA" in stripped or "JACK" in stripped or "jack" in stripped.lower():
            continue
        if "cannot find card" in stripped.lower():
            continue
        if "Unknown PCM" in stripped:
            continue
        filtered.append(stripped)
    return "\n".join(filtered)


def capture_audio(
    device: Optional[str],
    seconds: int,
    wav_path: str,
    show_progress: bool = False,
) -> Optional[bytes]:
    cmd = ["arecord"]
    if device:
        cmd.extend(["-D", device])
    cmd.extend(["-f", "S16_LE", "-r", "16000", "-c", "1", "-d", str(seconds), wav_path])

    stop_indicator: Optional[threading.Event] = None
    indicator_thread: Optional[threading.Thread] = None
    if show_progress:
        stop_indicator = threading.Event()
        indicator_thread = threading.Thread(
            target=_show_listening_indicator,
            args=(seconds, stop_indicator),
            daemon=True,
        )
        indicator_thread.start()

    try:
        result = subprocess.run(cmd, capture_output=True, check=False)
    except FileNotFoundError:
        print("Recording tool not found. Make sure the microphone is connected and alsa-utils is installed.")
        return None
    finally:
        _stop_listening_indicator(stop_indicator, indicator_thread)

    if result.returncode != 0:
        stderr = _filter_alsa_warnings(result.stderr.decode("utf-8", errors="replace"))
        print("Recording failed. Check that the microphone is connected and not in use by another program.")
        if stderr:
            print(f"  Details: {stderr}")
        return None

    if show_progress:
        print("Listening complete.")

    try:
        with open(wav_path, "rb") as f:
            wav_bytes = f.read()
    except FileNotFoundError:
        print("Recording did not produce an audio file. The microphone may not be working.")
        return None

    if not wav_bytes:
        print("Recording produced an empty file. The microphone may not be working.")
        return None

    return wav_bytes


def _format_listening_progress(elapsed_seconds: int, total_seconds: int) -> str:
    return f"Listening: {elapsed_seconds}/{total_seconds}s"


def _show_listening_indicator(
    seconds: int,
    stop_event: threading.Event,
    output: Callable[[str], None] = print,
) -> None:
    output(f"Listening for {seconds}s...")
    for elapsed_seconds in range(1, seconds + 1):
        if stop_event.wait(1):
            return
        output(_format_listening_progress(elapsed_seconds, seconds))
    stop_event.wait()


def _stop_listening_indicator(
    stop_event: Optional[threading.Event],
    indicator_thread: Optional[threading.Thread],
) -> None:
    if stop_event is None or indicator_thread is None:
        return
    stop_event.set()
    indicator_thread.join()


def send_message(chat_url: str, session_id: str, message: str) -> Optional[str]:
    payload = {"session_id": session_id, "message": message}
    request = urllib.request.Request(
        chat_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=TEXT_TIMEOUT_SECONDS) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        print(f"Backend error ({exc.code}). Please try again.")
        return None
    except urllib.error.URLError as exc:
        if _is_timeout_reason(exc.reason):
            print("Backend took too long to respond. It may be slow or unreachable.")
        else:
            print("Could not reach the backend. Make sure it is running and accessible.")
        return None
    except TimeoutError:
        print("Backend took too long to respond. It may be slow or unreachable.")
        return None
    except json.JSONDecodeError:
        print("Unexpected response from backend. Please try again.")
        return None

    if not data.get("success"):
        print("Backend could not process the request. Please try again.")
        return None

    response_text = data.get("response_text")
    if not isinstance(response_text, str) or not response_text.strip():
        print("Backend returned an empty response. Please try again.")
        return None

    return response_text.strip()


def send_audio(
    audio_url: str,
    session_id: str,
    device_id: str,
    audio_bytes: bytes,
    duration_ms: int,
) -> Optional[dict]:
    boundary = uuid.uuid4().hex

    body = b""
    for name, value in [
        ("session_id", session_id),
        ("device_id", device_id),
        ("duration_ms", str(duration_ms)),
        ("sample_rate_hz", "16000"),
        ("channels", "1"),
        ("language", "es"),
    ]:
        body += f"--{boundary}\r\n".encode()
        body += f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode()
        body += f"{value}\r\n".encode()
    body += f"--{boundary}\r\n".encode()
    body += b'Content-Disposition: form-data; name="audio"; filename="turn.wav"\r\n'
    body += b"Content-Type: audio/wav\r\n\r\n"
    body += audio_bytes
    body += b"\r\n"
    body += f"--{boundary}--\r\n".encode()

    content_type = f"multipart/form-data; boundary={boundary}"
    request = urllib.request.Request(
        audio_url,
        data=body,
        headers={"Content-Type": content_type},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=VOICE_TIMEOUT_SECONDS) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        if exc.code == 413:
            print("Recording is too long. Try a shorter question.")
        elif exc.code == 400:
            print("Could not understand the recording. Try speaking more clearly.")
        else:
            print(f"Backend error ({exc.code}). Please try again.")
        return None
    except urllib.error.URLError as exc:
        if _is_timeout_reason(exc.reason):
            print("Backend took too long to respond. It may be slow or unreachable.")
        else:
            print("Could not reach the backend. Make sure it is running and accessible.")
        return None
    except TimeoutError:
        print("Backend took too long to respond. It may be slow or unreachable.")
        return None
    except json.JSONDecodeError:
        print("Unexpected response from backend. Please try again.")
        return None

    transcript = data.get("transcript")
    response_text = data.get("response")
    if not isinstance(transcript, str) or not isinstance(response_text, str):
        print("Backend returned an incomplete response. Please try again.")
        return None

    return {"transcript": transcript.strip(), "response": response_text.strip()}


def speak(text: str) -> None:
    tts_command = os.environ.get("TONTO_TTS_COMMAND", "espeak")
    tts_args = shlex.split(os.environ.get("TONTO_TTS_ARGS", DEFAULT_TTS_ARGS))

    try:
        result = subprocess.run(
            [tts_command, *tts_args, text],
            check=False,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        print("Speech output not available. Make sure espeak is installed.")
        return

    if result.returncode != 0:
        print("Speech output failed. The response is shown above as text.")


def _is_timeout_reason(reason: object) -> bool:
    return isinstance(reason, (TimeoutError, socket.timeout)) or "timed out" in str(reason).lower()


if __name__ == "__main__":
    sys.exit(main())
