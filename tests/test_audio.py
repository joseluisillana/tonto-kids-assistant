import struct

import pytest

from tests.conftest import _make_wav


def _form_data(wav_bytes: bytes, session_id: str = "test-session", **overrides) -> dict:
    data = {
        "session_id": session_id,
        "duration_ms": "1000",
        "sample_rate_hz": "16000",
        "channels": "1",
    }
    data.update(overrides)
    return {
        "audio": ("test.wav", wav_bytes, "audio/wav"),
        **data,
    }


class TestChatAudioValidation:

    def test_valid_upload(self, client):
        wav = _make_wav(1000)
        data = _form_data(wav)
        resp = client.post("/chat/audio", files={"audio": data.pop("audio")}, data=data)
        assert resp.status_code == 200, resp.text
        body = resp.json()
        assert "session_id" in body
        assert "transcript" in body
        assert "response" in body
        assert body["session_id"] == "test-session"
        assert body["transcript"] == "[audio input captured]"
        assert body["response"] == (
            "He recibido tu audio. Todavia no puedo entenderlo, pero la subida y reproduccion ya funcionan. "
            "Pronto podre responder a lo que digas."
        )

    def test_missing_audio(self, client):
        resp = client.post("/chat/audio", data={"session_id": "s", "duration_ms": "1000", "sample_rate_hz": "16000", "channels": "1"})
        assert resp.status_code == 422

    def test_missing_session_id(self, client):
        wav = _make_wav(1000)
        data = {"duration_ms": "1000", "sample_rate_hz": "16000", "channels": "1"}
        resp = client.post("/chat/audio", files={"audio": ("test.wav", wav, "audio/wav")}, data=data)
        assert resp.status_code == 422

    def test_empty_audio(self, client):
        data = _form_data(b"")
        resp = client.post("/chat/audio", files={"audio": data.pop("audio")}, data=data)
        assert resp.status_code == 400

    def test_audio_too_large(self, client):
        wav = _make_wav(1000)
        oversized = wav + b"\x00" * (512 * 1024 + 1)
        data = _form_data(oversized)
        resp = client.post("/chat/audio", files={"audio": data.pop("audio")}, data=data)
        assert resp.status_code == 413

    def test_not_a_wav(self, client):
        data = _form_data(b"RIFF" + b"\x00" * 100)
        resp = client.post("/chat/audio", files={"audio": data.pop("audio")}, data=data)
        assert resp.status_code == 415

    def test_not_a_wav_too_small(self, client):
        data = _form_data(b"not a wav")
        resp = client.post("/chat/audio", files={"audio": data.pop("audio")}, data=data)
        assert resp.status_code == 400
        assert resp.json()["detail"] == "File too small to be a valid WAV"

    def test_wrong_format_pcm_not_1(self, client):
        raw = bytearray(_make_wav(1000))
        raw[20:22] = struct.pack("<H", 3)
        data = _form_data(bytes(raw))
        resp = client.post("/chat/audio", files={"audio": data.pop("audio")}, data=data)
        assert resp.status_code == 415

    def test_audio_too_short(self, client):
        wav = _make_wav(100)
        data = _form_data(wav)
        resp = client.post("/chat/audio", files={"audio": data.pop("audio")}, data=data)
        assert resp.status_code == 400

    def test_audio_too_long(self, client):
        wav = _make_wav(12_000)
        data = _form_data(wav)
        resp = client.post("/chat/audio", files={"audio": data.pop("audio")}, data=data)
        assert resp.status_code == 400


class TestExistingEndpoints:

    def test_health_still_works(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}

    def test_chat_rejects_empty_message(self, client):
        resp = client.post("/chat", json={"session_id": "s", "message": ""})
        assert resp.status_code == 422
