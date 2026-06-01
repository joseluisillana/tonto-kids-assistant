import io
import pathlib
import struct
import unittest.mock
import tempfile
import wave

import pytest
from fastapi.testclient import TestClient

from backend.main import app


@pytest.fixture
def tmp_path():
    root = pathlib.Path(tempfile.gettempdir()) / "tonto-pytest-fixtures"
    root.mkdir(parents=True, exist_ok=True)
    return pathlib.Path(tempfile.mkdtemp(dir=root))


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    mock = unittest.mock.MagicMock(return_value="Mocked TONTO response.")
    stt_mock = unittest.mock.MagicMock(return_value="hola tonto")
    monkeypatch.setattr("backend.audio_router.call_openai", mock)
    monkeypatch.setattr("backend.audio_router.transcribe_audio", stt_mock)
    monkeypatch.setattr("backend.main.call_openai", mock)
    return TestClient(app)


def _make_wav(duration_ms: int = 1000, sample_rate: int = 16000) -> bytes:
    num_samples = int(sample_rate * duration_ms / 1000)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(struct.pack(f"<{num_samples}h", *([0] * num_samples)))
    return buf.getvalue()
