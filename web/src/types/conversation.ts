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
  | "recording"
  | "uploading"
  | "transcribing"
  | "user-message"
  | "thinking"
  | "response"
  | "speaking"
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

export type MicrophonePermissionState =
  | "unsupported"
  | "unknown"
  | "prompt"
  | "granted"
  | "denied";

export type VoiceCaptureStatus =
  | "idle"
  | "requesting-permission"
  | "recording"
  | "encoding"
  | "uploading"
  | "transcribing"
  | "complete"
  | "error";

export type SpeechPlaybackStatus = "idle" | "speaking" | "complete" | "error";

export type VoiceLoopState = {
  backendUrl: string;
  microphoneSupported: boolean;
  microphonePermission: MicrophonePermissionState;
  speechSupported: boolean;
  captureStatus: VoiceCaptureStatus;
  speechStatus: SpeechPlaybackStatus;
  durationMs: number | null;
  recordingStartedAtMs: number | null;
  recordingElapsedMs: number;
  recordingLimitMs: number;
  wavBytes: number | null;
  wavMimeType: string | null;
  httpStatus: number | null;
  latencyMs: number | null;
  transcript: string | null;
  response: string | null;
  deviceId: string;
  language: string;
  sampleRateHz: number;
  channels: number;
  speechVoice: string | null;
  error: string | null;
};
