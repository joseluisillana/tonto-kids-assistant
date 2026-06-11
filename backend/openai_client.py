import json
import os
import urllib.error
import urllib.request

from fastapi import HTTPException

from backend.state import MAX_HISTORY_MESSAGES

OPENAI_API_URL = "https://api.openai.com/v1/responses"
DEFAULT_MODEL = "gpt-4o-mini"
OPENAI_INSTRUCTIONS = (
    "You are TONTO, a friendly educational assistant for children ages 6 to 10. "
    "Always answer in Spanish. Use clear, warm, child-friendly language. "
    "Keep answers short: 2 or 3 simple sentences unless the child asks for more. "
    "Be factually careful: use simple accurate facts, and say you are not sure "
    "instead of guessing. "
    "Start with a direct answer to the child's question, then add one simple example "
    "or comparison when it helps. Avoid long lists, markdown, and lecture-style answers. "
    "Use the recent conversation context to answer follow-up questions coherently. "
    "If the child greets you or says goodbye, respond naturally and gently invite one "
    "small educational question."
)
MAX_OUTPUT_TOKENS = 180


def call_openai(history: list[dict[str, str]], message: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not set")

    payload = {
        "model": os.environ.get("OPENAI_MODEL", DEFAULT_MODEL),
        "instructions": OPENAI_INSTRUCTIONS,
        "input": build_openai_input(history, message),
        "max_output_tokens": MAX_OUTPUT_TOKENS,
    }

    request = urllib.request.Request(
        OPENAI_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise HTTPException(status_code=502, detail=f"OpenAI error: {detail}") from exc
    except urllib.error.URLError as exc:
        raise HTTPException(status_code=502, detail=f"OpenAI request failed: {exc.reason}") from exc
    except TimeoutError as exc:
        raise HTTPException(status_code=504, detail="OpenAI request timed out") from exc

    response_text = extract_response_text(data)
    if not response_text:
        raise HTTPException(status_code=502, detail="OpenAI response did not include output_text")

    return response_text.strip()


def build_openai_input(history: list[dict[str, str]], message: str) -> str:
    lines = []
    for item in history[-MAX_HISTORY_MESSAGES:]:
        role = item["role"].title()
        lines.append(f"{role}: {item['content']}")
    lines.append(f"User: {message}")
    return "\n".join(lines)


def extract_response_text(data: dict) -> str:
    output_text = data.get("output_text")
    if isinstance(output_text, str):
        return output_text

    parts = []
    for item in data.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text" and isinstance(content.get("text"), str):
                parts.append(content["text"])

    return "\n".join(parts)
