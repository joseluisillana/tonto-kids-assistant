import json
import os
import socket
import uuid
import urllib.error
import urllib.request

from fastapi import HTTPException
from backend.provider_diagnostics import log_failure

OPENAI_TRANSCRIPTIONS_URL = "https://api.openai.com/v1/audio/transcriptions"
DEVEXPERT_BASE_URL = "https://inference.devexpert.io/v1"
AUDIO_TRANSCRIPTIONS_PATH = "/audio/transcriptions"
DEFAULT_OPENAI_STT_MODEL = "gpt-4o-mini-transcribe"
DEFAULT_DEVEXPERT_STT_MODEL = "gpt-4o-mini-transcribe"
DEFAULT_STT_MODEL = DEFAULT_OPENAI_STT_MODEL
PROVIDER_OPENAI = "openai"
PROVIDER_DEVEXPERT = "devexpert"


def transcribe_audio(content: bytes, filename: str, language: str = "es") -> str:
    provider = (os.environ.get("TONTO_INFERENCE_PROVIDER") or PROVIDER_OPENAI).strip().lower() or PROVIDER_OPENAI

    if provider == PROVIDER_OPENAI:
        return transcribe_openai_audio(content, filename, language)
    if provider == PROVIDER_DEVEXPERT:
        return transcribe_devexpert_audio(content, filename, language)

    log_failure("unknown", "stt", "invalid_provider")
    raise HTTPException(
        status_code=500,
        detail=(
            "Unsupported TONTO_INFERENCE_PROVIDER "
            f"configuration; expected '{PROVIDER_OPENAI}' or '{PROVIDER_DEVEXPERT}'"
        ),
    )


def transcribe_openai_audio(content: bytes, filename: str, language: str = "es") -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        log_failure("openai", "stt", "missing_credential")
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not set")

    model = os.environ.get("OPENAI_STT_MODEL", DEFAULT_OPENAI_STT_MODEL)
    return _transcribe_provider_audio(
        api_url=OPENAI_TRANSCRIPTIONS_URL,
        api_key=api_key,
        model=model,
        provider_label="OpenAI",
        content=content,
        filename=filename,
        language=language,
    )


def transcribe_devexpert_audio(content: bytes, filename: str, language: str = "es") -> str:
    api_key = os.environ.get("DEVEXPERT_API_KEY")
    if not api_key:
        log_failure("devexpert", "stt", "missing_credential")
        raise HTTPException(status_code=500, detail="DEVEXPERT_API_KEY is not set")

    base_url = os.environ.get("DEVEXPERT_BASE_URL", DEVEXPERT_BASE_URL).rstrip("/")
    model = os.environ.get("DEVEXPERT_STT_MODEL", DEFAULT_DEVEXPERT_STT_MODEL)
    return _transcribe_provider_audio(
        api_url=f"{base_url}{AUDIO_TRANSCRIPTIONS_PATH}",
        api_key=api_key,
        model=model,
        provider_label="DevExpert",
        content=content,
        filename=filename,
        language=language,
    )


def _transcribe_provider_audio(
    api_url: str,
    api_key: str,
    model: str,
    provider_label: str,
    content: bytes,
    filename: str,
    language: str,
) -> str:
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
        api_url,
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
        log_failure(provider_label.lower(), "stt", "http", exc.code)
        raise HTTPException(status_code=502, detail=f"{provider_label} STT error: HTTP {exc.code}") from None
    except TimeoutError as exc:
        log_failure(provider_label.lower(), "stt", "timeout")
        raise HTTPException(status_code=504, detail=f"{provider_label} STT request timed out") from None
    except urllib.error.URLError as exc:
        if _is_timeout_reason(exc.reason):
            log_failure(provider_label.lower(), "stt", "timeout")
            raise HTTPException(status_code=504, detail=f"{provider_label} STT request timed out") from None
        log_failure(provider_label.lower(), "stt", "network")
        raise HTTPException(status_code=502, detail=f"{provider_label} STT request failed") from None
    except json.JSONDecodeError as exc:
        log_failure(provider_label.lower(), "stt", "invalid_json")
        raise HTTPException(status_code=502, detail=f"{provider_label} STT response was not valid JSON") from None

    text = data.get("text")
    if not isinstance(text, str):
        log_failure(provider_label.lower(), "stt", "missing_output")
        raise HTTPException(status_code=502, detail=f"{provider_label} STT response did not include text")

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
