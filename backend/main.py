import json
import os
import urllib.error
import urllib.request
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


OPENAI_API_URL = "https://api.openai.com/v1/responses"
DEFAULT_MODEL = "gpt-4o-mini"
MAX_HISTORY_MESSAGES = 8


app = FastAPI(title="TONTO Kids Assistant Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
session_history: dict[str, list[dict[str, str]]] = {}


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1)
    message: str = Field(min_length=1)


class ChatResponse(BaseModel):
    success: Literal[True]
    response_text: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    message = request.message.strip()
    session_id = request.session_id.strip()

    if not session_id or not message:
        raise HTTPException(status_code=400, detail="session_id and message are required")

    history = session_history.setdefault(session_id, [])
    response_text = call_openai(history, message)

    history.extend(
        [
            {"role": "user", "content": message},
            {"role": "assistant", "content": response_text},
        ]
    )
    session_history[session_id] = history[-MAX_HISTORY_MESSAGES:]

    return ChatResponse(success=True, response_text=response_text)


def call_openai(history: list[dict[str, str]], message: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not set")

    payload = {
        "model": os.environ.get("OPENAI_MODEL", DEFAULT_MODEL),
        "instructions": (
            "You are TONTO, a friendly educational assistant for children. "
            "Answer clearly, briefly, and helpfully."
        ),
        "input": build_openai_input(history, message),
        "max_output_tokens": 300,
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
