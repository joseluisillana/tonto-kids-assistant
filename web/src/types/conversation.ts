export type BackendStatus = "checking" | "connected" | "disconnected";

export type ConversationStatus =
  | "idle"
  | "listening"
  | "sending"
  | "thinking"
  | "speaking"
  | "error";

export type ChatRole = "user" | "assistant";

export type ChatMessage = {
  id: string;
  role: ChatRole;
  text: string;
  createdAt: Date;
};

export type ActivityKind =
  | "listening"
  | "user-message"
  | "thinking"
  | "response"
  | "error";

export type ActivityEvent = {
  id: string;
  kind: ActivityKind;
  label: string;
  detail: string;
  createdAt: Date;
};

export type ChatRequest = {
  session_id: string;
  message: string;
};

export type ChatResponse = {
  success: true;
  response_text: string;
};
