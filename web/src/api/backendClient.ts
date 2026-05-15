import type { ChatRequest, ChatResponse } from "../types/conversation";

const DEFAULT_BACKEND_URL = "http://localhost:8000";
const REQUEST_TIMEOUT_MS = 15000;

export function getBackendUrl() {
  return (
    import.meta.env.VITE_BACKEND_URL?.replace(/\/$/, "") ?? DEFAULT_BACKEND_URL
  );
}

export async function checkBackendHealth() {
  const response = await fetchWithTimeout(`${getBackendUrl()}/health`, {
    method: "GET",
  });

  if (!response.ok) {
    throw new Error(`Backend health failed with ${response.status}`);
  }

  return response.json() as Promise<{ status: string }>;
}

export async function sendChatMessage(request: ChatRequest) {
  const response = await fetchWithTimeout(`${getBackendUrl()}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Backend chat failed with ${response.status}`);
  }

  const data = (await response.json()) as Partial<ChatResponse>;
  if (data.success !== true || typeof data.response_text !== "string") {
    throw new Error("Backend returned an invalid chat response");
  }

  return data as ChatResponse;
}

async function fetchWithTimeout(url: string, init: RequestInit) {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(
    () => controller.abort(),
    REQUEST_TIMEOUT_MS,
  );

  try {
    return await fetch(url, {
      ...init,
      signal: controller.signal,
    });
  } finally {
    window.clearTimeout(timeoutId);
  }
}
