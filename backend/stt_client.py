import json
import os
import socket
import uuid
import urllib.error
import urllib.request

from fastapi import HTTPException

OPENAI_TRANSCRIPTIONS_URL = "https://api.openai.com/v1/audio/transcriptions"
DEFAULT_STT_MODEL = "gpt-4o-mini-transcribe"


def transcribe_audio(content: bytes, filename: str, language: str = "es") -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not set")

    model = os.environ.get("OPENAI_STT_MODEL", DEFAULT_STT_MODEL)
    body, boundary = _build_multipart_body(
        fields={
            "model": model,
            "language": language,
            "response_format": "json",
        },
        file_field="file",
        filename=filename or "audio.wav",
        content_type="audio/wav",
        file_content=content,
    )

    request = urllib.request.Request(
        OPENAI_TRANSCRIPTIONS_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise HTTPException(status_code=502, detail=f"OpenAI STT error: {detail}") from exc
    except TimeoutError as exc:
        raise HTTPException(status_code=504, detail="OpenAI STT request timed out") from exc
    except urllib.error.URLError as exc:
        if _is_timeout_reason(exc.reason):
            raise HTTPException(status_code=504, detail="OpenAI STT request timed out") from exc
        raise HTTPException(status_code=502, detail=f"OpenAI STT request failed: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=502, detail="OpenAI STT response was not valid JSON") from exc

    text = data.get("text")
    if not isinstance(text, str):
        raise HTTPException(status_code=502, detail="OpenAI STT response did not include text")

    return text.strip()


def _build_multipart_body(
    fields: dict[str, str],
    file_field: str,
    filename: str,
    content_type: str,
    file_content: bytes,
) -> tuple[bytes, str]:
    boundary = f"tonto-{uuid.uuid4().hex}"
    chunks: list[bytes] = []

    for name, value in fields.items():
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                f'Content-Disposition: form-data; name="{_escape_header(name)}"\r\n\r\n'.encode("utf-8"),
                value.encode("utf-8"),
                b"\r\n",
            ]
        )

    chunks.extend(
        [
            f"--{boundary}\r\n".encode("utf-8"),
            (
                f'Content-Disposition: form-data; name="{_escape_header(file_field)}"; '
                f'filename="{_escape_header(filename)}"\r\n'
            ).encode("utf-8"),
            f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"),
            file_content,
            b"\r\n",
            f"--{boundary}--\r\n".encode("utf-8"),
        ]
    )

    return b"".join(chunks), boundary


def _escape_header(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _is_timeout_reason(reason: object) -> bool:
    return isinstance(reason, (TimeoutError, socket.timeout)) or "timed out" in str(reason).lower()
