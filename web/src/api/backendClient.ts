import type {
  ChatRequest,
  ChatResponse,
} from "../types/conversation.js";
import {
  WEB_VALIDATION_WAV_FILENAME,
} from "../lib/audio.js";

const DEFAULT_BACKEND_URL = "http://localhost:8000";
const REQUEST_TIMEOUT_MS = 15000;
const AUDIO_REQUEST_TIMEOUT_MS = 30000;

export class BackendRequestError extends Error {
  readonly status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "BackendRequestError";
    this.status = status;
  }
}

export type AudioTurnRequest = {
  session_id: string;
  device_id: string;
  duration_ms: number;
  sample_rate_hz: number;
  channels: number;
  language: string;
  audio: Blob;
  filename?: string;
};

export type AudioTurnResponse = {
  session_id: string;
  transcript: string;
  response: string;
};

export function getBackendUrl() {
  return (
    import.meta.env.VITE_BACKEND_URL?.replace(/\/$/, "") ?? DEFAULT_BACKEND_URL
  );
}

export async function checkBackendHealth(backendUrl = getBackendUrl()) {
  const response = await fetchWithTimeout(`${backendUrl}/health`, {
    method: "GET",
  });

  if (!response.ok) {
    throw new Error(`Backend health failed with ${response.status}`);
  }

  return response.json() as Promise<{ status: string }>;
}

export async function sendChatMessage(
  request: ChatRequest,
  backendUrl = getBackendUrl(),
) {
  const response = await fetchWithTimeout(`${backendUrl}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new BackendRequestError(
      response.status,
      await getResponseErrorMessage(response, "Backend chat failed"),
    );
  }

  const data = (await response.json()) as Partial<ChatResponse>;
  if (data.success !== true || typeof data.response_text !== "string") {
    throw new Error("Backend returned an invalid chat response");
  }

  return data as ChatResponse;
}

export async function sendAudioTurn(
  request: AudioTurnRequest,
  backendUrl = getBackendUrl(),
) {
  const formData = new FormData();
  formData.append("audio", request.audio, request.filename ?? WEB_VALIDATION_WAV_FILENAME);
  formData.append("session_id", request.session_id);
  formData.append("device_id", request.device_id);
  formData.append("duration_ms", String(request.duration_ms));
  formData.append("sample_rate_hz", String(request.sample_rate_hz));
  formData.append("channels", String(request.channels));
  formData.append("language", request.language);

  const response = await fetchWithTimeout(`${backendUrl}/chat/audio`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new BackendRequestError(
      response.status,
      await getResponseErrorMessage(response, "Backend audio failed"),
    );
  }

  const data = (await response.json()) as Partial<AudioTurnResponse>;
  if (
    typeof data.session_id !== "string" ||
    typeof data.transcript !== "string" ||
    typeof data.response !== "string"
  ) {
    throw new Error("Backend returned an invalid audio response");
  }

  return {
    session_id: data.session_id.trim(),
    transcript: data.transcript.trim(),
    response: data.response.trim(),
  } satisfies AudioTurnResponse;
}

async function fetchWithTimeout(url: string, init: RequestInit) {
  const controller = new AbortController();
  const timeoutId = globalThis.setTimeout(
    () => controller.abort(),
    init.body instanceof FormData ? AUDIO_REQUEST_TIMEOUT_MS : REQUEST_TIMEOUT_MS,
  );

  try {
    return await globalThis.fetch(url, {
      ...init,
      signal: controller.signal,
    });
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new Error("La solicitud al backend supero el tiempo limite");
    }

    throw error;
  } finally {
    globalThis.clearTimeout(timeoutId);
  }
}

async function getResponseErrorMessage(response: Response, fallback: string) {
  const text = (await response.text()).trim();
  if (!text) {
    return `${fallback} with ${response.status}`;
  }

  try {
    const parsed = JSON.parse(text) as { detail?: unknown };
    if (typeof parsed.detail === "string" && parsed.detail.trim()) {
      return `${fallback} with ${response.status}: ${parsed.detail.trim()}`;
    }
  } catch {
    // Fall through to raw text.
  }

  return `${fallback} with ${response.status}: ${text}`;
}
