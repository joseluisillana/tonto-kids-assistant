#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from typing import Optional
import urllib.error
import urllib.request
import uuid


REQUEST_TIMEOUT_SECONDS = 10


def main() -> int:
    backend_url = os.environ.get("TONTO_BACKEND_URL")
    if not backend_url:
        print("Set TONTO_BACKEND_URL to the backend address, for example http://192.168.1.10:8000")
        return 1

    session_id = f"local-session-{uuid.uuid4()}"
    chat_url = f"{backend_url.rstrip('/')}/chat"

    print("TONTO Kids Assistant Client")
    print(f"Session: {session_id}")
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


def send_message(chat_url: str, session_id: str, message: str) -> Optional[str]:
    payload = {"session_id": session_id, "message": message}
    request = urllib.request.Request(
        chat_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        print(f"Backend error {exc.code}: {detail}")
        return None
    except urllib.error.URLError as exc:
        print(f"Could not reach backend: {exc.reason}")
        return None
    except TimeoutError:
        print("Backend request timed out")
        return None
    except json.JSONDecodeError:
        print("Backend returned invalid JSON")
        return None

    if not data.get("success"):
        print("Backend returned an unsuccessful response")
        return None

    response_text = data.get("response_text")
    if not isinstance(response_text, str) or not response_text.strip():
        print("Backend response did not include response_text")
        return None

    return response_text.strip()


def speak(text: str) -> None:
    tts_command = os.environ.get("TONTO_TTS_COMMAND", "espeak")

    try:
        result = subprocess.run([tts_command, text], check=False)
    except FileNotFoundError:
        print(f"TTS command not found: {tts_command}")
        return

    if result.returncode != 0:
        print(f"TTS command failed with exit code {result.returncode}")


if __name__ == "__main__":
    sys.exit(main())
