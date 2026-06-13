import json
import os
import socket
from json import JSONDecodeError
import urllib.error
import urllib.request

from fastapi import HTTPException

from backend.state import MAX_HISTORY_MESSAGES

OPENAI_API_URL = "https://api.openai.com/v1/responses"
DEVEXPERT_BASE_URL = "https://inference.devexpert.io/v1"
DEVEXPERT_CHAT_PATH = "/chat/completions"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_DEVEXPERT_CHAT_MODEL = "mimo-v2.5"
PROVIDER_OPENAI = "openai"
PROVIDER_DEVEXPERT = "devexpert"
TONTO_INSTRUCTIONS = (
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
OPENAI_INSTRUCTIONS = TONTO_INSTRUCTIONS
MAX_OUTPUT_TOKENS = 300


def call_inference(history: list[dict[str, str]], message: str) -> str:
    provider = (os.environ.get("TONTO_INFERENCE_PROVIDER") or PROVIDER_OPENAI).strip().lower() or PROVIDER_OPENAI

    if provider == PROVIDER_OPENAI:
        return call_openai(history, message)
    if provider == PROVIDER_DEVEXPERT:
        return call_devexpert(history, message)

    raise HTTPException(
        status_code=500,
        detail=(
            "Unsupported TONTO_INFERENCE_PROVIDER "
            f"{provider!r}; expected '{PROVIDER_OPENAI}' or '{PROVIDER_DEVEXPERT}'"
        ),
    )


def call_openai(history: list[dict[str, str]], message: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not set")

    payload = {
        "model": os.environ.get("OPENAI_MODEL", DEFAULT_OPENAI_MODEL),
        "instructions": TONTO_INSTRUCTIONS,
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
        if _is_timeout_reason(exc.reason):
            raise HTTPException(status_code=504, detail="OpenAI request timed out") from exc
        raise HTTPException(status_code=502, detail=f"OpenAI request failed: {exc.reason}") from exc
    except TimeoutError as exc:
        raise HTTPException(status_code=504, detail="OpenAI request timed out") from exc
    except JSONDecodeError as exc:
        raise HTTPException(status_code=502, detail="OpenAI response was not valid JSON") from exc

    response_text = extract_response_text(data)
    if not response_text:
        raise HTTPException(status_code=502, detail="OpenAI response did not include output_text")

    return response_text.strip()


def call_devexpert(history: list[dict[str, str]], message: str) -> str:
    api_key = os.environ.get("DEVEXPERT_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="DEVEXPERT_API_KEY is not set")

    base_url = os.environ.get("DEVEXPERT_BASE_URL", DEVEXPERT_BASE_URL).rstrip("/")
    payload = {
        "model": os.environ.get("DEVEXPERT_CHAT_MODEL", DEFAULT_DEVEXPERT_CHAT_MODEL),
        "messages": build_chat_messages(history, message),
        "max_tokens": MAX_OUTPUT_TOKENS,
    }

    request = urllib.request.Request(
        f"{base_url}{DEVEXPERT_CHAT_PATH}",
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
        raise HTTPException(status_code=502, detail=f"DevExpert error: {detail}") from exc
    except urllib.error.URLError as exc:
        if _is_timeout_reason(exc.reason):
            raise HTTPException(status_code=504, detail="DevExpert request timed out") from exc
        raise HTTPException(status_code=502, detail=f"DevExpert request failed: {exc.reason}") from exc
    except TimeoutError as exc:
        raise HTTPException(status_code=504, detail="DevExpert request timed out") from exc
    except JSONDecodeError as exc:
        raise HTTPException(status_code=502, detail="DevExpert response was not valid JSON") from exc

    response_text = extract_chat_completion_text(data)
    if not response_text:
        raise HTTPException(status_code=502, detail="DevExpert response did not include choices[0].message.content")

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


def build_chat_messages(history: list[dict[str, str]], message: str) -> list[dict[str, str]]:
    messages = [{"role": "system", "content": TONTO_INSTRUCTIONS}]
    for item in history[-MAX_HISTORY_MESSAGES:]:
        role = item.get("role")
        if role not in {"user", "assistant"}:
            continue
        messages.append({"role": role, "content": item["content"]})
    messages.append({"role": "user", "content": message})
    return messages


def extract_chat_completion_text(data: dict) -> str:
    choices = data.get("choices")
    if not isinstance(choices, list) or not choices:
        return ""

    first_choice = choices[0]
    if not isinstance(first_choice, dict):
        return ""

    message = first_choice.get("message")
    if not isinstance(message, dict):
        return ""

    content = message.get("content")
    if isinstance(content, str):
        return content

    return ""


def _is_timeout_reason(reason: object) -> bool:
    return isinstance(reason, (TimeoutError, socket.timeout)) or "timed out" in str(reason).lower()
