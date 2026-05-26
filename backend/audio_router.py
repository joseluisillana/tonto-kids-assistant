import struct
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from backend.openai_client import call_openai
from backend.state import MAX_HISTORY_MESSAGES, session_history

MAX_AUDIO_SIZE = 512 * 1024
MIN_DURATION_MS = 250
MAX_DURATION_MS = 10_000

router = APIRouter()


class AudioResponse(BaseModel):
    session_id: str
    transcript: str
    response: str


def _validate_wav(content: bytes) -> dict:
    if len(content) < 44:
        raise HTTPException(status_code=400, detail="File too small to be a valid WAV")

    if content[:4] != b"RIFF" or content[8:12] != b"WAVE":
        raise HTTPException(status_code=415, detail="Not a valid WAV file")

    pos = 12
    found_fmt = False
    data_size = 0
    audio_format = None
    num_channels = None
    sample_rate = None
    bits_per_sample = None

    while pos < len(content) - 8:
        chunk_id = content[pos:pos + 4]
        chunk_size = struct.unpack("<I", content[pos + 4:pos + 8])[0]

        if chunk_id == b"fmt " and pos + 8 + chunk_size <= len(content):
            found_fmt = True
            fmt_data = content[pos + 8:pos + 8 + chunk_size]
            audio_format = struct.unpack("<H", fmt_data[0:2])[0]
            num_channels = struct.unpack("<H", fmt_data[2:4])[0]
            sample_rate = struct.unpack("<I", fmt_data[4:8])[0]
            bits_per_sample = struct.unpack("<H", fmt_data[14:16])[0]
        elif chunk_id == b"data":
            data_size = chunk_size

        pos += 8 + chunk_size
        if chunk_size % 2 != 0:
            pos += 1

    if not found_fmt:
        raise HTTPException(status_code=415, detail="No fmt chunk found in WAV")

    if audio_format != 1:
        raise HTTPException(status_code=415, detail=f"Unsupported audio format {audio_format}, expected PCM (1)")
    if num_channels != 1:
        raise HTTPException(status_code=415, detail=f"Unsupported channel count {num_channels}, expected mono (1)")
    if sample_rate != 16000:
        raise HTTPException(status_code=415, detail=f"Unsupported sample rate {sample_rate}, expected 16000 Hz")
    if bits_per_sample != 16:
        raise HTTPException(status_code=415, detail=f"Unsupported bits per sample {bits_per_sample}, expected 16")

    duration_ms = (data_size / (sample_rate * num_channels * bits_per_sample / 8)) * 1000

    return {
        "audio_format": audio_format,
        "num_channels": num_channels,
        "sample_rate": sample_rate,
        "bits_per_sample": bits_per_sample,
        "data_size": data_size,
        "duration_ms": duration_ms,
    }


@router.post("/chat/audio", response_model=AudioResponse)
async def chat_audio(
    audio: UploadFile = File(...),
    session_id: str = Form(min_length=1),
    duration_ms: int = Form(...),
    sample_rate_hz: int = Form(...),
    channels: int = Form(...),
    device_id: Optional[str] = Form(None),
    recorded_at: Optional[str] = Form(None),
    language: str = Form("es"),
) -> AudioResponse:
    content = await audio.read()

    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Audio file is empty")
    if len(content) > MAX_AUDIO_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"Audio file too large ({len(content)} bytes), maximum is {MAX_AUDIO_SIZE} bytes",
        )

    wav_info = _validate_wav(content)

    if wav_info["duration_ms"] < MIN_DURATION_MS:
        raise HTTPException(
            status_code=400,
            detail=f"Audio too short ({wav_info['duration_ms']:.0f} ms), minimum is {MIN_DURATION_MS} ms",
        )
    if wav_info["duration_ms"] > MAX_DURATION_MS:
        raise HTTPException(
            status_code=400,
            detail=f"Audio too long ({wav_info['duration_ms']:.0f} ms), maximum is {MAX_DURATION_MS} ms",
        )

    transcript = "[audio input captured]"

    history = session_history.setdefault(session_id, [])
    response_text = call_openai(history, transcript)

    history.extend(
        [
            {"role": "user", "content": transcript},
            {"role": "assistant", "content": response_text},
        ]
    )
    session_history[session_id] = history[-MAX_HISTORY_MESSAGES:]

    return AudioResponse(
        session_id=session_id,
        transcript=transcript,
        response=response_text,
    )
