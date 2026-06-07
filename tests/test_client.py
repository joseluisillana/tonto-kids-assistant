import io
import json
import os
import socket
from pathlib import Path
import subprocess
import threading
import urllib.error
import uuid

import pytest

from client.main import (
    _format_listening_progress,
    capture_audio,
    send_audio,
    send_message,
    speak,
)


#
# send_message (text mode)
#


class _FakeResponse:
    def __init__(self, payload: dict):
        self._payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")


def test_send_message_posts_to_chat(monkeypatch):
    called_with = {}

    def fake_urlopen(request, timeout):
        called_with["url"] = request.full_url
        called_with["method"] = request.method
        called_with["content_type"] = request.get_header("Content-type")
        body = json.loads(request.data.decode("utf-8"))
        called_with["body"] = body
        assert body["session_id"] == "s1"
        assert body["message"] == "hola"
        return _FakeResponse({"success": True, "response_text": "Hola"})

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    result = send_message("http://localhost:8000/chat", "s1", "hola")
    assert result == "Hola"
    assert "/chat" in called_with["url"]
    assert called_with["method"] == "POST"
    assert "application/json" in called_with["content_type"]


def test_send_message_http_error(monkeypatch):
    def fake_urlopen(request, timeout):
        raise urllib.error.HTTPError(
            request.full_url, 400, "Bad Request", hdrs=None, fp=io.BytesIO(b'{"detail":"bad"}')
        )

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    assert send_message("http://localhost:8000/chat", "s1", "hola") is None


def test_send_message_url_error(monkeypatch):
    def fake_urlopen(request, timeout):
        raise urllib.error.URLError("network unreachable")

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    assert send_message("http://localhost:8000/chat", "s1", "hola") is None


def test_send_message_timeout(monkeypatch):
    def fake_urlopen(request, timeout):
        raise TimeoutError("timed out")

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    assert send_message("http://localhost:8000/chat", "s1", "hola") is None


def test_send_message_url_error_timeout(monkeypatch):
    def fake_urlopen(request, timeout):
        raise urllib.error.URLError(socket.timeout("timed out"))

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    assert send_message("http://localhost:8000/chat", "s1", "hola") is None


def test_send_message_invalid_json(monkeypatch):
    class _BadResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return b"not-json"

    monkeypatch.setattr("urllib.request.urlopen", lambda request, timeout: _BadResponse())
    assert send_message("http://localhost:8000/chat", "s1", "hola") is None


def test_send_message_missing_fields(monkeypatch):
    def fake_urlopen(request, timeout):
        return _FakeResponse({"success": True})

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    assert send_message("http://localhost:8000/chat", "s1", "hola") is None


#
# send_audio (voice mode)
#


def test_send_audio_multipart_contains_required_fields(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["method"] = request.method
        captured["content_type"] = request.get_header("Content-type")
        captured["body"] = request.data
        return _FakeResponse(
            {"session_id": "s1", "transcript": "hola", "response": "Hola amigo"}
        )

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    result = send_audio(
        "http://localhost:8000/chat/audio",
        "test-session",
        "test-pi",
        b"fake-wav-data",
        6000,
    )

    assert result == {"transcript": "hola", "response": "Hola amigo"}
    assert "/chat/audio" in captured["url"]
    assert captured["method"] == "POST"
    assert "multipart/form-data" in captured["content_type"]

    body = captured["body"]
    assert b'name="session_id"' in body
    assert b"test-session" in body
    assert b'name="device_id"' in body
    assert b"test-pi" in body
    assert b'name="duration_ms"' in body
    assert b"6000" in body
    assert b'name="sample_rate_hz"' in body
    assert b"16000" in body
    assert b'name="channels"' in body
    assert b"1" in body
    assert b'name="language"' in body
    assert b"es" in body
    assert b'name="audio"; filename="turn.wav"' in body
    assert b"fake-wav-data" in body
    assert b"Content-Type: audio/wav" in body


def test_send_audio_extracts_transcript_and_response(monkeypatch):
    def fake_urlopen(request, timeout):
        return _FakeResponse(
            {"session_id": "s1", "transcript": "  hola  ", "response": "  Hola amigo  "}
        )

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    result = send_audio("http://localhost:8000/chat/audio", "s1", "d1", b"data", 3000)
    assert result == {"transcript": "hola", "response": "Hola amigo"}


def test_send_audio_missing_fields_in_response(monkeypatch):
    def fake_urlopen(request, timeout):
        return _FakeResponse({"session_id": "s1"})

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    assert (
        send_audio("http://localhost:8000/chat/audio", "s1", "d1", b"data", 3000) is None
    )


def test_send_audio_http_error(monkeypatch):
    def fake_urlopen(request, timeout):
        raise urllib.error.HTTPError(
            request.full_url, 413, "Too Large", hdrs=None, fp=io.BytesIO(b'{"detail":"too big"}')
        )

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    assert send_audio("http://localhost:8000/chat/audio", "s1", "d1", b"data", 3000) is None


def test_send_audio_timeout(monkeypatch):
    def fake_urlopen(request, timeout):
        raise TimeoutError("timed out")

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    assert send_audio("http://localhost:8000/chat/audio", "s1", "d1", b"data", 3000) is None


def test_send_audio_url_error_timeout(monkeypatch):
    def fake_urlopen(request, timeout):
        raise urllib.error.URLError(socket.timeout("timed out"))

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    assert send_audio("http://localhost:8000/chat/audio", "s1", "d1", b"data", 3000) is None


def test_send_audio_invalid_json(monkeypatch):
    class _BadResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return b"not-json"

    monkeypatch.setattr("urllib.request.urlopen", lambda request, timeout: _BadResponse())
    assert send_audio("http://localhost:8000/chat/audio", "s1", "d1", b"data", 3000) is None


#
# capture_audio
#


def _make_fake_completed_process(returncode: int = 0, stderr: str = ""):
    return subprocess.CompletedProcess(
        args=[], returncode=returncode, stdout=b"", stderr=stderr.encode()
    )


def _audio_test_path(filename: str) -> str:
    root = Path(".cache") / "client-audio-tests"
    root.mkdir(parents=True, exist_ok=True)
    return str(root / filename)


def test_capture_audio_calls_arecord_with_device(monkeypatch):
    wav_path = _audio_test_path("turn-device.wav")
    with open(wav_path, "wb") as f:
        f.write(b"RIFF....WAVE....")

    args_captured = []

    def fake_run(cmd, **kwargs):
        args_captured.extend(cmd)
        return _make_fake_completed_process(0)

    monkeypatch.setattr("client.main.subprocess.run", fake_run)
    result = capture_audio("plughw:1,0", 6, wav_path)
    assert result == b"RIFF....WAVE...."
    assert "arecord" in args_captured
    assert "-D" in args_captured
    assert "plughw:1,0" in args_captured


def test_format_listening_progress():
    assert _format_listening_progress(2, 6) == "Listening: 2/6s"


def test_capture_audio_shows_listening_indicator_when_requested(monkeypatch, tmp_path, capsys):
    wav_path = str(tmp_path / "turn.wav")
    with open(wav_path, "wb") as f:
        f.write(b"WAV data")

    indicator_started = threading.Event()
    observed = {}

    def fake_indicator(seconds, stop_event):
        observed["seconds"] = seconds
        observed["stopped_before_capture"] = stop_event.is_set()
        indicator_started.set()
        stop_event.wait(1)
        observed["stopped_after_capture"] = stop_event.is_set()

    def fake_run(cmd, **kwargs):
        assert indicator_started.wait(1)
        return _make_fake_completed_process(0)

    monkeypatch.setattr("client.main._show_listening_indicator", fake_indicator)
    monkeypatch.setattr("client.main.subprocess.run", fake_run)

    result = capture_audio(None, 4, wav_path, show_progress=True)

    assert result == b"WAV data"
    assert observed == {
        "seconds": 4,
        "stopped_before_capture": False,
        "stopped_after_capture": True,
    }
    assert "Listening complete." in capsys.readouterr().out


def test_capture_audio_does_not_print_complete_when_arecord_fails(
    monkeypatch, tmp_path, capsys
):
    wav_path = str(tmp_path / "turn.wav")
    indicator_started = threading.Event()

    def fake_indicator(seconds, stop_event):
        indicator_started.set()
        stop_event.wait(1)

    def fake_run(cmd, **kwargs):
        assert indicator_started.wait(1)
        return _make_fake_completed_process(1, "error")

    monkeypatch.setattr("client.main._show_listening_indicator", fake_indicator)
    monkeypatch.setattr("client.main.subprocess.run", fake_run)

    assert capture_audio(None, 4, wav_path, show_progress=True) is None
    assert "Listening complete." not in capsys.readouterr().out


def test_capture_audio_calls_arecord_without_device(monkeypatch):
    wav_path = _audio_test_path("turn-default.wav")
    with open(wav_path, "wb") as f:
        f.write(b"WAV data")

    args_captured = []

    def fake_run(cmd, **kwargs):
        args_captured.extend(cmd)
        return _make_fake_completed_process(0)

    monkeypatch.setattr("client.main.subprocess.run", fake_run)
    result = capture_audio(None, 5, wav_path)
    assert result == b"WAV data"
    assert "-D" not in args_captured


def test_capture_audio_arecord_not_found(monkeypatch, tmp_path):
    wav_path = str(tmp_path / "turn.wav")

    def fake_run(cmd, **kwargs):
        raise FileNotFoundError("arecord not found")

    monkeypatch.setattr("client.main.subprocess.run", fake_run)
    assert capture_audio(None, 5, wav_path) is None


def test_capture_audio_arecord_fails(monkeypatch, tmp_path):
    wav_path = str(tmp_path / "turn.wav")

    def fake_run(cmd, **kwargs):
        return _make_fake_completed_process(1, "error")

    monkeypatch.setattr("client.main.subprocess.run", fake_run)
    assert capture_audio(None, 5, wav_path) is None


def test_capture_audio_wav_not_created(monkeypatch, tmp_path):
    wav_path = str(tmp_path / "nonexistent.wav")

    monkeypatch.setattr(
        "client.main.subprocess.run", lambda cmd, **kwargs: _make_fake_completed_process(0)
    )
    assert capture_audio(None, 5, wav_path) is None


def test_capture_audio_wav_empty(monkeypatch):
    wav_path = _audio_test_path("empty.wav")
    with open(wav_path, "wb") as f:
        f.write(b"")

    monkeypatch.setattr(
        "client.main.subprocess.run", lambda cmd, **kwargs: _make_fake_completed_process(0)
    )
    assert capture_audio(None, 5, wav_path) is None


#
# speak (TTS)
#


def test_speak_calls_espeak(monkeypatch):
    args_captured = []

    def fake_run(cmd, **kwargs):
        args_captured.extend(cmd)
        return subprocess.CompletedProcess(args=cmd, returncode=0)

    monkeypatch.setattr("client.main.subprocess.run", fake_run)
    speak("Hola mundo")
    assert "espeak" in args_captured or "espeak-ng" in args_captured
    assert args_captured == ["espeak", "-v", "es", "-s", "135", "-g", "8", "Hola mundo"]


def test_speak_uses_configured_command(monkeypatch):
    monkeypatch.setenv("TONTO_TTS_COMMAND", "custom-tts")
    args_captured = []

    def fake_run(cmd, **kwargs):
        args_captured.extend(cmd)
        return subprocess.CompletedProcess(args=cmd, returncode=0)

    monkeypatch.setattr("client.main.subprocess.run", fake_run)
    speak("test")
    assert "custom-tts" in args_captured


def test_speak_uses_configured_tts_args(monkeypatch):
    monkeypatch.setenv("TONTO_TTS_ARGS", "-v es+m3 -s 140")
    args_captured = []

    def fake_run(cmd, **kwargs):
        args_captured.extend(cmd)
        return subprocess.CompletedProcess(args=cmd, returncode=0)

    monkeypatch.setattr("client.main.subprocess.run", fake_run)
    speak("test")
    assert args_captured == ["espeak", "-v", "es+m3", "-s", "140", "test"]


def test_speak_handles_file_not_found(monkeypatch):
    def fake_run(cmd, **kwargs):
        raise FileNotFoundError("espeak not found")

    monkeypatch.setattr("client.main.subprocess.run", fake_run)
    speak("test")


def test_speak_handles_nonzero_exit(monkeypatch):
    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(args=cmd, returncode=1)

    monkeypatch.setattr("client.main.subprocess.run", fake_run)
    speak("test")
