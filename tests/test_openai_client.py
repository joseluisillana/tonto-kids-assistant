import json

from backend.openai_client import MAX_OUTPUT_TOKENS, call_openai


class _FakeOpenAIResponse:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self):
        return json.dumps({"output_text": "Claro, el Sol es una estrella."}).encode("utf-8")


def test_call_openai_uses_child_friendly_spanish_prompt(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["timeout"] = timeout
        captured["payload"] = json.loads(request.data.decode("utf-8"))
        return _FakeOpenAIResponse()

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr("backend.openai_client.urllib.request.urlopen", fake_urlopen)

    response = call_openai(
        [{"role": "user", "content": "Hola TONTO, que es una estrella?"}],
        "Y el sol es una estrella?",
    )

    assert response == "Claro, el Sol es una estrella."
    assert captured["timeout"] == 20
    assert "Always answer in Spanish" in captured["payload"]["instructions"]
    assert "2 or 3 simple sentences" in captured["payload"]["instructions"]
    assert "direct answer to the child's question" in captured["payload"]["instructions"]
    assert "Avoid long lists, markdown, and lecture-style answers" in captured["payload"]["instructions"]
    assert "greets you or says goodbye" in captured["payload"]["instructions"]
    assert "recent conversation context" in captured["payload"]["instructions"]
    assert captured["payload"]["max_output_tokens"] == MAX_OUTPUT_TOKENS
    assert "User: Hola TONTO, que es una estrella?" in captured["payload"]["input"]
    assert "User: Y el sol es una estrella?" in captured["payload"]["input"]
