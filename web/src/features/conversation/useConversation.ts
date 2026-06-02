import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  BackendRequestError,
  checkBackendHealth,
  getBackendUrl,
  sendAudioTurn,
  sendChatMessage,
} from "../../api/backendClient.js";
import {
  combineFloat32Chunks,
  downsampleBuffer,
  encodeWavPcm16Mono,
  hasSpeechSynthesisSupport,
  prepareSpeechSamples,
  speakText,
  speakTextIfSupported,
  WEB_VALIDATION_BACKEND_DEVICE_ID,
  WEB_VALIDATION_CHANNELS,
  WEB_VALIDATION_LANGUAGE,
  WEB_VALIDATION_SAMPLE_RATE_HZ,
  WEB_VALIDATION_WAV_MIME_TYPE,
} from "../../lib/audio.js";
import type {
  ActivityEvent,
  BackendStatus,
  ChatMessage,
  ConversationStatus,
  VoiceCaptureStatus,
  VoiceLoopState,
} from "../../types/conversation.js";

const MAX_ACTIVITY_EVENTS = 8;

type CaptureRuntime = {
  stream: MediaStream;
  audioContext: AudioContext;
  source: MediaStreamAudioSourceNode;
  processor: ScriptProcessorNode;
  silenceGain: GainNode;
  chunks: Float32Array[];
};

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
  const [voice, setVoice] = useState<VoiceLoopState>(() =>
    createVoiceState(getBackendUrl()),
  );

  const captureRuntimeRef = useRef<CaptureRuntime | null>(null);
  const mountedRef = useRef(true);

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
    const intervalId = globalThis.setInterval(() => setNow(new Date()), 1000);
    return () => globalThis.clearInterval(intervalId);
  }, []);

  useEffect(() => {
    mountedRef.current = true;

    return () => {
      mountedRef.current = false;
      cancelCapture(captureRuntimeRef.current);
      captureRuntimeRef.current = null;
      if (hasSpeechSynthesisSupport()) {
        window.speechSynthesis.cancel();
      }
    };
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
        setVoice((current) => ({
          ...current,
          speechStatus: hasSpeechSynthesisSupport() ? "speaking" : "idle",
          speechVoice: null,
        }));

        const speechResult = await speakTextIfSupported(response.response_text);
        if (!mountedRef.current) {
          return;
        }

        if (speechResult.played) {
          setVoice((current) => ({
            ...current,
            speechStatus: "complete",
            speechVoice: speechResult.voiceName,
            error: null,
          }));
          setActivity((current) =>
            pushActivity(
              current,
              createActivity("speaking", "Voz", "Respuesta reproducida"),
            ),
          );
        } else {
          setVoice((current) => ({
            ...current,
            speechSupported:
              speechResult.reason === "unsupported"
                ? false
                : current.speechSupported,
            speechStatus:
              speechResult.reason === "unsupported" ? "idle" : "error",
            error:
              speechResult.reason === "unsupported"
                ? current.error
                : speechResult.error,
          }));
          setActivity((current) =>
            pushActivity(
              current,
              createActivity(
                "speaking",
                "Voz",
                speechResult.reason === "unsupported"
                  ? "Speech no soportado"
                  : "Speech no disponible",
              ),
            ),
          );
        }

        globalThis.setTimeout(() => {
          if (mountedRef.current) {
            setStatus("idle");
          }
        }, 900);
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

  const startVoiceTurn = useCallback(async () => {
    if (
      status === "sending" ||
      status === "thinking" ||
      status === "speaking" ||
      voice.captureStatus === "recording" ||
      voice.captureStatus === "uploading" ||
      voice.captureStatus === "transcribing"
    ) {
      return;
    }

    if (!navigator.mediaDevices?.getUserMedia) {
      const message = "Este navegador no soporta capturas de microfono";
      setVoice((current) => ({
        ...current,
        captureStatus: "error",
        speechStatus: "error",
        microphoneSupported: false,
        error: message,
      }));
      setError(message);
      setStatus("error");
      setActivity((current) =>
        pushActivity(current, createActivity("error", "Error", message)),
      );
      return;
    }

    if (!hasSpeechSynthesisSupport()) {
      setVoice((current) => ({
        ...current,
        speechSupported: false,
      }));
    }

    setError(null);
    setVoice((current) => ({
      ...current,
      captureStatus: "requesting-permission",
      speechStatus: "idle",
      microphonePermission: "prompt",
      transcript: null,
      response: null,
      durationMs: null,
      wavBytes: null,
      wavMimeType: null,
      httpStatus: null,
      latencyMs: null,
      speechVoice: null,
      error: null,
    }));
    setStatus("listening");
    setActivity((current) =>
      pushActivity(
        current,
        createActivity("recording", "Microfono", "Solicitando permiso"),
      ),
    );

    let stream: MediaStream | null = null;
    try {
      stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          autoGainControl: true,
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true,
        },
      });
      const audioContext = createAudioContext();
      await audioContext.resume();
      const source = audioContext.createMediaStreamSource(stream);
      const processor = audioContext.createScriptProcessor(4096, 1, 1);
      const silenceGain = audioContext.createGain();
      const chunks: Float32Array[] = [];
      silenceGain.gain.value = 0;

      processor.onaudioprocess = (event) => {
        const channelData = event.inputBuffer.getChannelData(0);
        chunks.push(new Float32Array(channelData));
      };

      source.connect(processor);
      processor.connect(silenceGain);
      silenceGain.connect(audioContext.destination);

      captureRuntimeRef.current = {
        stream,
        audioContext,
        source,
        processor,
        silenceGain,
        chunks,
      };

      setVoice((current) => ({
        ...current,
        microphonePermission: "granted",
        captureStatus: "recording",
      }));
      setActivity((current) =>
        pushActivity(
          current,
          createActivity("recording", "Microfono", "Grabando audio"),
        ),
      );
    } catch (voiceError) {
      cancelCaptureRuntime(stream);
      const message = getVoiceErrorMessage(voiceError);
      setVoice((current) => ({
        ...current,
        captureStatus: "error",
        speechStatus: "error",
        microphonePermission: isPermissionDenied(voiceError)
          ? "denied"
          : current.microphonePermission,
        error: message,
      }));
      setError(message);
      setStatus("error");
      setActivity((current) =>
        pushActivity(current, createActivity("error", "Error", message)),
      );
    }
  }, [status, voice.captureStatus]);

  const stopVoiceTurn = useCallback(async () => {
    const runtime = captureRuntimeRef.current;
    if (!runtime) {
      return;
    }

    captureRuntimeRef.current = null;
    const inputSampleRate = runtime.audioContext.sampleRate;
    cancelCapture(runtime);

    const rawAudio = combineFloat32Chunks(runtime.chunks);
    if (rawAudio.length === 0) {
      const message = "No se pudo capturar audio";
      setVoice((current) => ({
        ...current,
        captureStatus: "error",
        speechStatus: "error",
        error: message,
      }));
      setError(message);
      setStatus("error");
      setActivity((current) =>
        pushActivity(current, createActivity("error", "Error", message)),
      );
      return;
    }

    const preparedAudio = prepareSpeechSamples(rawAudio, inputSampleRate);
    if (!preparedAudio.hasSpeech) {
      const message =
        "No he escuchado tu voz con claridad. Pulsa Escuchar y habla un poco mas cerca del microfono.";
      setVoice((current) => ({
        ...current,
        captureStatus: "error",
        speechStatus: "idle",
        durationMs: preparedAudio.originalDurationMs,
        error: message,
      }));
      setError(message);
      setStatus("error");
      setActivity((current) =>
        pushActivity(current, createActivity("error", "Microfono", message)),
      );
      return;
    }

    const captureDurationMs = Math.max(1, preparedAudio.durationMs);
    const downsampled = downsampleBuffer(
      preparedAudio.samples,
      inputSampleRate,
      WEB_VALIDATION_SAMPLE_RATE_HZ,
    );
    const wavBytes = encodeWavPcm16Mono(
      downsampled,
      WEB_VALIDATION_SAMPLE_RATE_HZ,
    );
    const wavBlob = new Blob([wavBytes.buffer as ArrayBuffer], {
      type: WEB_VALIDATION_WAV_MIME_TYPE,
    });

    setVoice((current) => ({
      ...current,
      captureStatus: "encoding",
      durationMs: captureDurationMs,
      wavBytes: wavBytes.byteLength,
      wavMimeType: wavBlob.type,
      error: null,
    }));
    setActivity((current) =>
      pushActivity(
        current,
        createActivity("uploading", "Audio", "Voz preparada en WAV"),
      ),
    );

    const started = performance.now();
    setVoice((current) => ({
      ...current,
      captureStatus: "uploading",
      httpStatus: null,
      latencyMs: null,
    }));
    setStatus("sending");

    try {
      const response = await sendAudioTurn(
        {
          session_id: sessionId,
          device_id: WEB_VALIDATION_BACKEND_DEVICE_ID,
          duration_ms: captureDurationMs,
          sample_rate_hz: WEB_VALIDATION_SAMPLE_RATE_HZ,
          channels: WEB_VALIDATION_CHANNELS,
          language: WEB_VALIDATION_LANGUAGE,
          audio: wavBlob,
        },
        voice.backendUrl,
      );

      const latency = Math.round(performance.now() - started);
      setVoice((current) => ({
        ...current,
        captureStatus: "transcribing",
        httpStatus: 200,
        latencyMs: latency,
        transcript: response.transcript,
        response: response.response,
        error: null,
      }));
      setLatestLatencyMs(latency);
      setMessages((current) => [
        ...current,
        {
          id: crypto.randomUUID(),
          role: "user",
          text: response.transcript,
          createdAt: new Date(),
        },
        {
          id: crypto.randomUUID(),
          role: "assistant",
          text: response.response,
          createdAt: new Date(),
        },
      ]);
      setActivity((current) =>
        pushActivity(
          current,
          createActivity("transcribing", "STT", "Transcripcion recibida"),
          createActivity("response", "TONTO", "Respuesta educativa lista"),
        ),
      );
      setStatus("thinking");
      setVoice((current) => ({
        ...current,
        speechStatus: "speaking",
      }));
      setStatus("speaking");

      const speechResult = await playSpeech(response.response);
      if (speechResult) {
        setVoice((current) => ({
          ...current,
          captureStatus: "complete",
          speechStatus: "complete",
          speechVoice: speechResult.voiceName,
          error: null,
        }));
        setActivity((current) =>
          pushActivity(
            current,
            createActivity("speaking", "Voz", "Respuesta reproducida"),
          ),
        );
        setStatus("speaking");
        globalThis.setTimeout(() => {
          if (mountedRef.current) {
            setStatus("idle");
          }
        }, 900);
      }
    } catch (voiceError) {
      const message = getVoiceErrorMessage(voiceError);
      const httpStatus =
        voiceError instanceof BackendRequestError ? voiceError.status : null;
      setVoice((current) => ({
        ...current,
        captureStatus: "error",
        speechStatus: "error",
        httpStatus: httpStatus ?? current.httpStatus,
        error: message,
      }));
      setError(message);
      setStatus("error");
      setActivity((current) =>
        pushActivity(current, createActivity("error", "Error", message)),
      );
    }
  }, [sessionId, voice.backendUrl]);

  const resetSession = useCallback(() => {
    cancelCapture(captureRuntimeRef.current);
    captureRuntimeRef.current = null;
    if (hasSpeechSynthesisSupport()) {
      window.speechSynthesis.cancel();
    }
    setSessionId(createSessionId());
    setMessages([]);
    setActivity([createActivity("listening", "TONTO", "Nueva sesion lista")]);
    setStatus("idle");
    setError(null);
    setLatestLatencyMs(null);
    setStartedAt(new Date());
    setVoice(createVoiceState(getBackendUrl()));
  }, []);

  const cancelVoiceTurn = useCallback(() => {
    const hadCapture = captureRuntimeRef.current !== null;
    cancelCapture(captureRuntimeRef.current);
    captureRuntimeRef.current = null;
    if (hasSpeechSynthesisSupport()) {
      window.speechSynthesis.cancel();
    }
    setVoice((current) => ({
      ...current,
      captureStatus:
        current.captureStatus === "recording" ||
        current.captureStatus === "requesting-permission"
          ? "idle"
          : current.captureStatus,
      speechStatus: current.speechStatus === "speaking" ? "idle" : current.speechStatus,
      error: null,
    }));
    if (status === "listening" || status === "speaking" || hadCapture) {
      setStatus("idle");
      setActivity((current) =>
        pushActivity(current, createActivity("listening", "Voz", "Detenida")),
      );
    }
  }, [status]);

  const repeatLatest = useCallback(() => {
    const lastAssistantMessage = [...messages]
      .reverse()
      .find((message) => message.role === "assistant");

    if (!lastAssistantMessage) {
      return;
    }

    setVoice((current) => ({
      ...current,
      speechStatus: "speaking",
    }));
    setStatus("speaking");
    setActivity((current) =>
      pushActivity(
        current,
        createActivity("speaking", "Voz", "Repitiendo ultima respuesta"),
      ),
    );

    void playSpeech(lastAssistantMessage.text)
      .then((speechResult) => {
        if (!speechResult) {
          return;
        }

        setVoice((current) => ({
          ...current,
          speechStatus: "complete",
          speechVoice: speechResult.voiceName,
          error: null,
        }));
        globalThis.setTimeout(() => setStatus("idle"), 900);
      })
      .catch((voiceError) => {
        const message = getVoiceErrorMessage(voiceError);
        setVoice((current) => ({
          ...current,
          speechStatus: "error",
          error: message,
        }));
        setError(message);
        setStatus("error");
        setActivity((current) =>
          pushActivity(current, createActivity("error", "Error", message)),
        );
      });
  }, [messages]);

  const questionCount = useMemo(
    () => messages.filter((message) => message.role === "user").length,
    [messages],
  );

  return {
    activity,
    backendStatus,
    cancelVoiceTurn,
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
    startVoiceTurn,
    status,
    stopVoiceTurn,
    voice,
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

function createVoiceState(backendUrl: string): VoiceLoopState {
  return {
    backendUrl,
    microphoneSupported: typeof navigator !== "undefined" &&
      Boolean(navigator.mediaDevices?.getUserMedia),
    microphonePermission: typeof navigator !== "undefined" &&
      Boolean(navigator.mediaDevices?.getUserMedia)
      ? "unknown"
      : "unsupported",
    speechSupported: hasSpeechSynthesisSupport(),
    captureStatus: "idle",
    speechStatus: "idle",
    durationMs: null,
    wavBytes: null,
    wavMimeType: null,
    httpStatus: null,
    latencyMs: null,
    transcript: null,
    response: null,
    deviceId: WEB_VALIDATION_BACKEND_DEVICE_ID,
    language: WEB_VALIDATION_LANGUAGE,
    sampleRateHz: WEB_VALIDATION_SAMPLE_RATE_HZ,
    channels: WEB_VALIDATION_CHANNELS,
    speechVoice: null,
    error: null,
  };
}

function createAudioContext() {
  const AudioContextConstructor =
    window.AudioContext ||
    (window as Window & {
      webkitAudioContext?: typeof AudioContext;
    }).webkitAudioContext;

  if (!AudioContextConstructor) {
    throw new Error("AudioContext is not supported in this browser");
  }

  return new AudioContextConstructor();
}

function cancelCapture(runtime: CaptureRuntime | null) {
  if (!runtime) {
    return;
  }

  try {
    runtime.processor.onaudioprocess = null;
    runtime.processor.disconnect();
  } catch {
    // No-op.
  }

  try {
    runtime.source.disconnect();
  } catch {
    // No-op.
  }

  try {
    runtime.silenceGain.disconnect();
  } catch {
    // No-op.
  }

  try {
    runtime.stream.getTracks().forEach((track) => track.stop());
  } catch {
    // No-op.
  }

  void runtime.audioContext.close();
}

function cancelCaptureRuntime(stream: MediaStream | null) {
  if (!stream) {
    return;
  }

  try {
    stream.getTracks().forEach((track) => track.stop());
  } catch {
    // No-op.
  }
}

async function playSpeech(text: string) {
  const speechResult = await speakText(text);
  return speechResult;
}

function isPermissionDenied(error: unknown) {
  return (
    error instanceof DOMException &&
    (error.name === "NotAllowedError" ||
      error.name === "SecurityError" ||
      error.name === "PermissionDeniedError")
  );
}

function getVoiceErrorMessage(error: unknown) {
  if (error instanceof BackendRequestError) {
    if (
      error.status === 422 &&
      error.message.includes("Audio did not contain recognizable speech")
    ) {
      return "No he entendido voz en el audio. Prueba hablando un poco mas cerca del microfono.";
    }

    return error.message;
  }

  if (error instanceof DOMException) {
    if (error.name === "NotAllowedError") {
      return "El permiso del microfono fue denegado";
    }
    if (error.name === "NotFoundError") {
      return "No se encontro un microfono disponible";
    }
    if (error.name === "AbortError") {
      return "La captura de audio se interrumpio";
    }
  }

  if (error instanceof Error) {
    if (error.message.includes("AudioContext is not supported")) {
      return "Este navegador no soporta AudioContext";
    }
    if (error.message.includes("Speech synthesis is not supported")) {
      return "Este navegador no soporta speechSynthesis";
    }
    return error.message;
  }

  return "Unexpected error";
}

function getErrorMessage(error: unknown) {
  if (error instanceof Error) {
    return error.message;
  }

  return "Unexpected error";
}
