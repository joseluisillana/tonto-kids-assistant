"""Provider failures must not publish upstream bodies, URLs or exception chains."""

import io
import json
import traceback
import urllib.error

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from backend import openai_client, stt_client
from backend.main import app
from tests.conftest import _make_wav


@pytest.mark.parametrize("provider", ["openai", "devexpert"])
@pytest.mark.parametrize("audio", [False, True])
@pytest.mark.parametrize("failure", ["http", "network", "timeout", "json"])
def test_provider_diagnostics_exclude_canary(monkeypatch, caplog, provider, audio, failure):
    canary = "invented-provider-canary"
    monkeypatch.setenv("TONTO_INFERENCE_PROVIDER", provider)
    monkeypatch.setenv("OPENAI_API_KEY", canary)
    monkeypatch.setenv("DEVEXPERT_API_KEY", canary)

    def fail(request, timeout):
        if failure == "http":
            raise urllib.error.HTTPError(
                f"https://example.test/{canary}", 401, canary, None,
                io.BytesIO(canary.encode()),
            )
        if failure == "network":
            raise urllib.error.URLError(canary)
        if failure == "timeout":
            raise urllib.error.URLError(TimeoutError(canary))
        raise json.JSONDecodeError(canary, canary, 0)

    monkeypatch.setattr("urllib.request.urlopen", fail)
    expected_status = 504 if failure == "timeout" else 502
    try:
        if audio:
            stt_client.transcribe_audio(b"fixture", "fixture.wav")
        else:
            openai_client.call_inference([], "hola")
    except HTTPException as exc:
        if canary in str(exc.detail) + traceback.format_exc():
            pytest.fail("Provider diagnostic exposed a canary", pytrace=False)
        assert exc.status_code == expected_status
    else:
        pytest.fail("Expected provider failure", pytrace=False)

    # Exercise the real endpoint handlers, rather than mocking their providers.
    with TestClient(app) as client:
        if audio:
            response = client.post(
                "/chat/audio", data={"session_id": "safe-audio", "duration_ms": 1000,
                                     "sample_rate_hz": 16000, "channels": 1},
                files={"audio": ("fixture.wav", _make_wav(), "audio/wav")},
            )
        else:
            response = client.post("/chat", json={"session_id": "safe-text", "message": "hola"})
    if canary in response.text:
        pytest.fail("API diagnostic exposed a canary", pytrace=False)
    assert response.status_code == expected_status
    if canary in caplog.text:
        pytest.fail("Log exposed a canary", pytrace=False)
    records = [record for record in caplog.records if record.name == "backend.provider_diagnostics"]
    assert len(records) == 2
    for record in records:
        event = json.loads(record.getMessage())
        assert event["provider"] == provider
        assert event["operation"] == ("stt" if audio else "chat")
        assert event["failure"] == ("invalid_json" if failure == "json" else failure)
        assert event.get("http_status") == (401 if failure == "http" else None)
        assert record.exc_info is None
        assert record.stack_info is None


@pytest.mark.parametrize("audio", [False, True])
def test_invalid_provider_does_not_echo_configuration(monkeypatch, caplog, audio):
    canary = "invented-config-canary"
    monkeypatch.setenv("TONTO_INFERENCE_PROVIDER", canary)
    with pytest.raises(HTTPException) as exc:
        if audio:
            stt_client.transcribe_audio(b"fixture", "fixture.wav")
        else:
            openai_client.call_inference([], "hola")
    if canary in str(exc.value.detail):
        pytest.fail("Configuration diagnostic exposed a canary", pytrace=False)
    assert exc.value.status_code == 500
    if canary in caplog.text:
        pytest.fail("Configuration log exposed a canary", pytrace=False)
    event = json.loads(caplog.records[-1].getMessage())
    assert event["provider"] == "unknown"
    assert event["failure"] == "invalid_provider"


def test_diagnostic_logger_rejects_arbitrary_fields(caplog):
    from backend.provider_diagnostics import log_failure

    canary = "invented-log-canary"
    log_failure(canary, canary, canary, canary)
    if canary in caplog.text:
        pytest.fail("Logger exposed an invalid field", pytrace=False)
    assert json.loads(caplog.records[-1].getMessage()) == {
        "event": "provider_failure", "provider": "unknown", "operation": "unknown",
        "failure": "unknown",
    }
