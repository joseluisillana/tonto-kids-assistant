import json
import socket
import urllib.error

import pytest
from fastapi import HTTPException

from backend.openai_client import MAX_OUTPUT_TOKENS, call_devexpert, call_inference, call_openai


class _FakeProviderResponse:
    def __init__(self, payload: dict):
        self._payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self):
        return json.dumps(self._payload).encode("utf-8")


def test_call_openai_uses_child_friendly_spanish_prompt(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["timeout"] = timeout
        captured["url"] = request.full_url
        captured["payload"] = json.loads(request.data.decode("utf-8"))
        return _FakeProviderResponse({"output_text": "Claro, el Sol es una estrella."})

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr("backend.openai_client.urllib.request.urlopen", fake_urlopen)

    response = call_openai(
        [{"role": "user", "content": "Hola TONTO, que es una estrella?"}],
        "Y el sol es una estrella?",
    )

    assert response == "Claro, el Sol es una estrella."
    assert captured["timeout"] == 20
    assert captured["url"] == "https://api.openai.com/v1/responses"
    assert "Always answer in Spanish" in captured["payload"]["instructions"]
    assert "2 or 3 simple sentences" in captured["payload"]["instructions"]
    assert "simple accurate facts" in captured["payload"]["instructions"]
    assert "direct answer to the child's question" in captured["payload"]["instructions"]
    assert "Avoid long lists, markdown, and lecture-style answers" in captured["payload"]["instructions"]
    assert "greets you or says goodbye" in captured["payload"]["instructions"]
    assert "recent conversation context" in captured["payload"]["instructions"]
    assert captured["payload"]["max_output_tokens"] == MAX_OUTPUT_TOKENS
    assert "User: Hola TONTO, que es una estrella?" in captured["payload"]["input"]
    assert "User: Y el sol es una estrella?" in captured["payload"]["input"]


def test_call_inference_uses_openai_by_default(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        return _FakeProviderResponse({"output_text": "Respuesta OpenAI"})

    monkeypatch.delenv("TONTO_INFERENCE_PROVIDER", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    monkeypatch.setattr("backend.openai_client.urllib.request.urlopen", fake_urlopen)

    assert call_inference([], "Hola") == "Respuesta OpenAI"
    assert captured["url"] == "https://api.openai.com/v1/responses"


def test_call_inference_routes_to_devexpert(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["timeout"] = timeout
        captured["url"] = request.full_url
        captured["authorization"] = request.headers["Authorization"]
        captured["payload"] = json.loads(request.data.decode("utf-8"))
        return _FakeProviderResponse({"choices": [{"message": {"content": "Respuesta DevExpert"}}]})

    monkeypatch.setenv("TONTO_INFERENCE_PROVIDER", "devexpert")
    monkeypatch.setenv("DEVEXPERT_API_KEY", "test-devexpert-key")
    monkeypatch.setenv("DEVEXPERT_BASE_URL", "https://example.test/v1/")
    monkeypatch.setenv("DEVEXPERT_CHAT_MODEL", "mimo-test")
    monkeypatch.setattr("backend.openai_client.urllib.request.urlopen", fake_urlopen)

    response = call_inference(
        [{"role": "user", "content": "Hola"}, {"role": "assistant", "content": "Hola, soy TONTO."}],
        "Que es la luna?",
    )

    assert response == "Respuesta DevExpert"
    assert captured["timeout"] == 20
    assert captured["url"] == "https://example.test/v1/chat/completions"
    assert captured["authorization"] == "Bearer test-devexpert-key"
    assert captured["payload"]["model"] == "mimo-test"
    assert captured["payload"]["max_tokens"] == MAX_OUTPUT_TOKENS
    assert captured["payload"]["messages"][0]["role"] == "system"
    assert "Always answer in Spanish" in captured["payload"]["messages"][0]["content"]
    assert captured["payload"]["messages"][1] == {"role": "user", "content": "Hola"}
    assert captured["payload"]["messages"][2] == {"role": "assistant", "content": "Hola, soy TONTO."}
    assert captured["payload"]["messages"][3] == {"role": "user", "content": "Que es la luna?"}


def test_call_devexpert_uses_default_base_url_and_model(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["payload"] = json.loads(request.data.decode("utf-8"))
        return _FakeProviderResponse({"choices": [{"message": {"content": "Hola desde DevExpert"}}]})

    monkeypatch.delenv("DEVEXPERT_BASE_URL", raising=False)
    monkeypatch.delenv("DEVEXPERT_CHAT_MODEL", raising=False)
    monkeypatch.setenv("DEVEXPERT_API_KEY", "test-devexpert-key")
    monkeypatch.setattr("backend.openai_client.urllib.request.urlopen", fake_urlopen)

    assert call_devexpert([], "Hola") == "Hola desde DevExpert"
    assert captured["url"] == "https://inference.devexpert.io/v1/chat/completions"
    assert captured["payload"]["model"] == "mimo-v2.5"


def test_call_devexpert_requires_api_key(monkeypatch):
    monkeypatch.delenv("DEVEXPERT_API_KEY", raising=False)

    with pytest.raises(HTTPException) as exc:
        call_devexpert([], "Hola")

    assert exc.value.status_code == 500
    assert exc.value.detail == "DEVEXPERT_API_KEY is not set"


def test_call_inference_rejects_unsupported_provider(monkeypatch):
    monkeypatch.setenv("TONTO_INFERENCE_PROVIDER", "unknown")

    with pytest.raises(HTTPException) as exc:
        call_inference([], "Hola")

    assert exc.value.status_code == 500
    assert "Unsupported TONTO_INFERENCE_PROVIDER" in exc.value.detail


def test_call_devexpert_timeout_returns_504(monkeypatch):
    monkeypatch.setenv("DEVEXPERT_API_KEY", "test-devexpert-key")
    monkeypatch.setattr(
        "backend.openai_client.urllib.request.urlopen",
        lambda request, timeout: (_ for _ in ()).throw(urllib.error.URLError(socket.timeout("timed out"))),
    )

    with pytest.raises(HTTPException) as exc:
        call_devexpert([], "Hola")

    assert exc.value.status_code == 504
    assert exc.value.detail == "DevExpert request timed out"
