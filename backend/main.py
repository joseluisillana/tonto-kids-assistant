from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.audio_router import router as audio_router
from backend.openai_client import call_openai
from backend.state import MAX_HISTORY_MESSAGES, session_history


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
app.include_router(audio_router)


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
