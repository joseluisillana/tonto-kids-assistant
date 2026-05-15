import { useCallback, useEffect, useMemo, useState } from "react";
import { checkBackendHealth, sendChatMessage } from "../../api/backendClient";
import type {
  ActivityEvent,
  BackendStatus,
  ChatMessage,
  ConversationStatus,
} from "../../types/conversation";

const MAX_ACTIVITY_EVENTS = 6;

export function useConversation() {
  const [sessionId, setSessionId] = useState(createSessionId);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [activity, setActivity] = useState<ActivityEvent[]>([
    createActivity("listening", "TONTO", "Sesion preparada"),
  ]);
  const [status, setStatus] = useState<ConversationStatus>("idle");
  const [backendStatus, setBackendStatus] =
    useState<BackendStatus>("checking");
  const [error, setError] = useState<string | null>(null);
  const [latestLatencyMs, setLatestLatencyMs] = useState<number | null>(null);
  const [startedAt, setStartedAt] = useState(() => new Date());
  const [now, setNow] = useState(() => new Date());

  const checkHealth = useCallback(async () => {
    setBackendStatus("checking");
    try {
      await checkBackendHealth();
      setBackendStatus("connected");
      setError(null);
    } catch (healthError) {
      setBackendStatus("disconnected");
      setError(getErrorMessage(healthError));
    }
  }, []);

  useEffect(() => {
    void checkHealth();
  }, [checkHealth]);

  useEffect(() => {
    const intervalId = window.setInterval(() => setNow(new Date()), 1000);
    return () => window.clearInterval(intervalId);
  }, []);

  const sendMessage = useCallback(
    async (rawMessage: string) => {
      const text = rawMessage.trim();
      if (!text || status === "sending" || status === "thinking") {
        return;
      }

      const userMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: "user",
        text,
        createdAt: new Date(),
      };

      setMessages((current) => [...current, userMessage]);
      setActivity((current) =>
        pushActivity(
          current,
          createActivity("user-message", "Tu", text),
          createActivity("thinking", "TONTO", "Pensando respuesta"),
        ),
      );
      setStatus("thinking");
      setError(null);

      const started = performance.now();
      try {
        const response = await sendChatMessage({
          session_id: sessionId,
          message: text,
        });
        const latency = Math.round(performance.now() - started);
        const assistantMessage: ChatMessage = {
          id: crypto.randomUUID(),
          role: "assistant",
          text: response.response_text,
          createdAt: new Date(),
        };

        setMessages((current) => [...current, assistantMessage]);
        setActivity((current) =>
          pushActivity(
            current,
            createActivity("response", "TONTO", "Respuesta recibida"),
          ),
        );
        setLatestLatencyMs(latency);
        setBackendStatus("connected");
        setStatus("speaking");
        window.setTimeout(() => setStatus("idle"), 900);
      } catch (chatError) {
        const message = getErrorMessage(chatError);
        setError(message);
        setBackendStatus("disconnected");
        setStatus("error");
        setActivity((current) =>
          pushActivity(current, createActivity("error", "Error", message)),
        );
      }
    },
    [sessionId, status],
  );

  const resetSession = useCallback(() => {
    setSessionId(createSessionId());
    setMessages([]);
    setActivity([createActivity("listening", "TONTO", "Nueva sesion lista")]);
    setStatus("idle");
    setError(null);
    setLatestLatencyMs(null);
    setStartedAt(new Date());
  }, []);

  const repeatLatest = useCallback(() => {
    const lastAssistantMessage = [...messages]
      .reverse()
      .find((message) => message.role === "assistant");

    if (!lastAssistantMessage) {
      return;
    }

    setStatus("speaking");
    setActivity((current) =>
      pushActivity(
        current,
        createActivity("response", "TONTO", "Repitiendo ultima respuesta"),
      ),
    );
    window.setTimeout(() => setStatus("idle"), 900);
  }, [messages]);

  const questionCount = useMemo(
    () => messages.filter((message) => message.role === "user").length,
    [messages],
  );

  return {
    activity,
    backendStatus,
    checkHealth,
    elapsedSeconds: Math.max(
      0,
      Math.floor((now.getTime() - startedAt.getTime()) / 1000),
    ),
    error,
    latestLatencyMs,
    messages,
    questionCount,
    repeatLatest,
    resetSession,
    sendMessage,
    sessionId,
    setStatus,
    status,
  };
}

function createSessionId() {
  return `web-session-${crypto.randomUUID()}`;
}

function createActivity(
  kind: ActivityEvent["kind"],
  label: string,
  detail: string,
): ActivityEvent {
  return {
    id: crypto.randomUUID(),
    kind,
    label,
    detail,
    createdAt: new Date(),
  };
}

function pushActivity(
  current: ActivityEvent[],
  ...events: ActivityEvent[]
): ActivityEvent[] {
  return [...current, ...events].slice(-MAX_ACTIVITY_EVENTS);
}

function getErrorMessage(error: unknown) {
  if (error instanceof Error) {
    return error.message;
  }

  return "Unexpected error";
}
