import io
import json
import socket
import urllib.error

import pytest
from fastapi import HTTPException

from backend import stt_client


class _FakeResponse:
    def __init__(self, payload: dict):
        self._payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")


def test_transcribe_audio_success(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    def fake_urlopen(request, timeout):
        assert timeout == 20
        assert request.full_url == stt_client.OPENAI_TRANSCRIPTIONS_URL
        assert request.headers["Authorization"] == "Bearer test-key"
        assert "multipart/form-data" in request.headers["Content-type"]
        body = request.data
        assert b'name="model"' in body
        assert b"gpt-4o-mini-transcribe" in body
        assert b'name="language"' in body
        assert b"es" in body
        assert b'name="file"; filename="test.wav"' in body
        return _FakeResponse({"text": " hola tonto "})

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    assert stt_client.transcribe_audio(b"wav-bytes", "test.wav", "es") == "hola tonto"


def test_transcribe_audio_uses_configured_model(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_STT_MODEL", "gpt-4o-transcribe")

    def fake_urlopen(request, timeout):
        assert b"gpt-4o-transcribe" in request.data
        return _FakeResponse({"text": "hola"})

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    assert stt_client.transcribe_audio(b"wav-bytes", "test.wav", "es") == "hola"


def test_transcribe_audio_response_without_text(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr("urllib.request.urlopen", lambda request, timeout: _FakeResponse({"other": "value"}))

    with pytest.raises(HTTPException) as exc:
        stt_client.transcribe_audio(b"wav-bytes", "test.wav", "es")

    assert exc.value.status_code == 502


def test_transcribe_audio_http_error(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    def fake_urlopen(request, timeout):
        raise urllib.error.HTTPError(
            request.full_url,
            500,
            "Server Error",
            hdrs=None,
            fp=io.BytesIO(b'{"error":"boom"}'),
        )

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    with pytest.raises(HTTPException) as exc:
        stt_client.transcribe_audio(b"wav-bytes", "test.wav", "es")

    assert exc.value.status_code == 502
    assert "OpenAI STT error" in exc.value.detail


def test_transcribe_audio_url_error(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(
        "urllib.request.urlopen",
        lambda request, timeout: (_ for _ in ()).throw(urllib.error.URLError("network down")),
    )

    with pytest.raises(HTTPException) as exc:
        stt_client.transcribe_audio(b"wav-bytes", "test.wav", "es")

    assert exc.value.status_code == 502


def test_transcribe_audio_timeout(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(
        "urllib.request.urlopen",
        lambda request, timeout: (_ for _ in ()).throw(urllib.error.URLError(socket.timeout("timed out"))),
    )

    with pytest.raises(HTTPException) as exc:
        stt_client.transcribe_audio(b"wav-bytes", "test.wav", "es")

    assert exc.value.status_code == 504
