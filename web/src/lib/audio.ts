export const WEB_VALIDATION_BACKEND_DEVICE_ID = "web-validation-client";
export const WEB_VALIDATION_LANGUAGE = "es";
export const WEB_VALIDATION_SAMPLE_RATE_HZ = 16_000;
export const WEB_VALIDATION_CHANNELS = 1;
export const WEB_VALIDATION_MAX_DURATION_MS = 10_000;
export const WEB_VALIDATION_WAV_MIME_TYPE = "audio/wav";
export const WEB_VALIDATION_WAV_FILENAME = "turn.wav";

const DEFAULT_SILENCE_THRESHOLD = 0.004;
const DEFAULT_SILENCE_PADDING_MS = 160;
const DEFAULT_TARGET_PEAK = 0.85;
const DEFAULT_MAX_GAIN = 12;

export type PreparedSpeechSamples = {
  samples: Float32Array;
  originalDurationMs: number;
  durationMs: number;
  peakAmplitude: number;
  rmsAmplitude: number;
  gain: number;
  hasSpeech: boolean;
};

export function combineFloat32Chunks(chunks: Float32Array[]): Float32Array {
  const totalLength = chunks.reduce((sum, chunk) => sum + chunk.length, 0);
  const merged = new Float32Array(totalLength);
  let offset = 0;

  for (const chunk of chunks) {
    merged.set(chunk, offset);
    offset += chunk.length;
  }

  return merged;
}

export function calculatePeakAmplitude(samples: Float32Array): number {
  let peak = 0;

  for (const sample of samples) {
    peak = Math.max(peak, Math.abs(sample));
  }

  return peak;
}

export function calculateRmsAmplitude(samples: Float32Array): number {
  if (samples.length === 0) {
    return 0;
  }

  let sumSquares = 0;
  for (const sample of samples) {
    sumSquares += sample * sample;
  }

  return Math.sqrt(sumSquares / samples.length);
}

export function trimSilence(
  samples: Float32Array,
  sampleRateHz: number,
  options: {
    threshold?: number;
    paddingMs?: number;
  } = {},
): Float32Array {
  if (samples.length === 0) {
    return new Float32Array(0);
  }
  if (sampleRateHz <= 0) {
    throw new Error("Sample rate must be positive");
  }

  const threshold = options.threshold ?? DEFAULT_SILENCE_THRESHOLD;
  const paddingSamples = Math.round(
    (sampleRateHz * (options.paddingMs ?? DEFAULT_SILENCE_PADDING_MS)) / 1000,
  );
  let firstSpeechSample = -1;
  let lastSpeechSample = -1;

  for (let i = 0; i < samples.length; i += 1) {
    if (Math.abs(samples[i]) >= threshold) {
      firstSpeechSample = i;
      break;
    }
  }

  for (let i = samples.length - 1; i >= 0; i -= 1) {
    if (Math.abs(samples[i]) >= threshold) {
      lastSpeechSample = i;
      break;
    }
  }

  if (firstSpeechSample === -1 || lastSpeechSample === -1) {
    return new Float32Array(0);
  }

  const start = Math.max(0, firstSpeechSample - paddingSamples);
  const end = Math.min(samples.length, lastSpeechSample + paddingSamples + 1);
  return samples.slice(start, end);
}

export function normalizePeak(
  samples: Float32Array,
  options: {
    targetPeak?: number;
    maxGain?: number;
  } = {},
): { samples: Float32Array; gain: number } {
  if (samples.length === 0) {
    return { samples: new Float32Array(0), gain: 1 };
  }

  const peak = calculatePeakAmplitude(samples);
  if (peak === 0) {
    return { samples: new Float32Array(samples), gain: 1 };
  }

  const targetPeak = options.targetPeak ?? DEFAULT_TARGET_PEAK;
  const maxGain = options.maxGain ?? DEFAULT_MAX_GAIN;
  const gain = Math.min(maxGain, targetPeak / peak);
  const normalized = new Float32Array(samples.length);

  for (let i = 0; i < samples.length; i += 1) {
    normalized[i] = Math.max(-1, Math.min(1, samples[i] * gain));
  }

  return { samples: normalized, gain };
}

export function prepareSpeechSamples(
  samples: Float32Array,
  sampleRateHz: number,
): PreparedSpeechSamples {
  if (sampleRateHz <= 0) {
    throw new Error("Sample rate must be positive");
  }

  const originalDurationMs = Math.round((samples.length / sampleRateHz) * 1000);
  const trimmed = trimSilence(samples, sampleRateHz);
  const { samples: normalized, gain } = normalizePeak(trimmed);
  const durationMs = Math.round((normalized.length / sampleRateHz) * 1000);
  const peakAmplitude = calculatePeakAmplitude(normalized);
  const rmsAmplitude = calculateRmsAmplitude(normalized);

  return {
    samples: normalized,
    originalDurationMs,
    durationMs,
    peakAmplitude,
    rmsAmplitude,
    gain,
    hasSpeech:
      normalized.length > 0 &&
      durationMs >= 250 &&
      peakAmplitude >= 0.04 &&
      rmsAmplitude >= 0.004,
  };
}

export function downsampleBuffer(
  buffer: Float32Array,
  inputSampleRate: number,
  targetSampleRate: number,
): Float32Array {
  if (buffer.length === 0) {
    return new Float32Array(0);
  }
  if (inputSampleRate <= 0 || targetSampleRate <= 0) {
    throw new Error("Sample rates must be positive");
  }
  if (inputSampleRate === targetSampleRate) {
    return new Float32Array(buffer);
  }

  const sampleRateRatio = inputSampleRate / targetSampleRate;
  const newLength = Math.max(1, Math.floor(buffer.length / sampleRateRatio));
  const result = new Float32Array(newLength);

  let inputOffset = 0;
  for (let i = 0; i < newLength; i += 1) {
    const nextOffset = Math.round((i + 1) * sampleRateRatio);
    let sum = 0;
    let count = 0;

    while (inputOffset < nextOffset && inputOffset < buffer.length) {
      sum += buffer[inputOffset];
      count += 1;
      inputOffset += 1;
    }

    result[i] = count > 0 ? sum / count : 0;
  }

  return result;
}

export function encodeWavPcm16Mono(
  samples: Float32Array,
  sampleRateHz: number,
): Uint8Array {
  const bytesPerSample = 2;
  const blockAlign = bytesPerSample;
  const byteRate = sampleRateHz * blockAlign;
  const dataSize = samples.length * bytesPerSample;
  const buffer = new ArrayBuffer(44 + dataSize);
  const view = new DataView(buffer);

  writeString(view, 0, "RIFF");
  view.setUint32(4, 36 + dataSize, true);
  writeString(view, 8, "WAVE");
  writeString(view, 12, "fmt ");
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, 1, true);
  view.setUint32(24, sampleRateHz, true);
  view.setUint32(28, byteRate, true);
  view.setUint16(32, blockAlign, true);
  view.setUint16(34, 16, true);
  writeString(view, 36, "data");
  view.setUint32(40, dataSize, true);

  let offset = 44;
  for (const sample of samples) {
    const clamped = Math.max(-1, Math.min(1, sample));
    view.setInt16(offset, clamped < 0 ? clamped * 0x8000 : clamped * 0x7fff, true);
    offset += 2;
  }

  return new Uint8Array(buffer);
}

export function formatBytes(bytes: number): string {
  if (!Number.isFinite(bytes) || bytes < 0) {
    return "--";
  }
  if (bytes < 1024) {
    return `${bytes} B`;
  }
  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`;
  }
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function formatClockDuration(durationMs: number): string {
  if (!Number.isFinite(durationMs) || durationMs < 0) {
    return "00:00";
  }

  const totalSeconds = Math.floor(durationMs / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${minutes.toString().padStart(2, "0")}:${seconds
    .toString()
    .padStart(2, "0")}`;
}

export function calculateDurationProgress(
  elapsedMs: number,
  limitMs: number,
): number {
  if (!Number.isFinite(elapsedMs) || !Number.isFinite(limitMs) || limitMs <= 0) {
    return 0;
  }

  return Math.max(0, Math.min(100, (elapsedMs / limitMs) * 100));
}

export function hasSpeechSynthesisSupport(): boolean {
  return (
    typeof window !== "undefined" &&
    "speechSynthesis" in window &&
    "SpeechSynthesisUtterance" in window
  );
}

export type SpeechPlaybackResult =
  | {
      played: true;
      voiceName: string | null;
      voiceLang: string | null;
    }
  | {
      played: false;
      reason: "unsupported" | "error";
      error: string;
    };

export function selectSpanishVoice(
  voices: SpeechSynthesisVoice[],
): SpeechSynthesisVoice | null {
  if (voices.length === 0) {
    return null;
  }

  const normalized = (value: string) => value.toLowerCase();
  return (
    voices.find((voice) => normalized(voice.lang).startsWith("es-")) ??
    voices.find((voice) => normalized(voice.lang) === "es") ??
    voices.find((voice) => voice.default) ??
    voices[0] ??
    null
  );
}

export async function speakText(
  text: string,
): Promise<{ voiceName: string | null; voiceLang: string | null }> {
  if (!hasSpeechSynthesisSupport()) {
    throw new Error("Speech synthesis is not supported in this browser");
  }

  const speech = window.speechSynthesis;
  const voice = await waitForSpanishVoice(speech);
  const utterance = new SpeechSynthesisUtterance(text);

  utterance.lang = voice?.lang || "es-ES";
  if (voice) {
    utterance.voice = voice;
  }

  speech.cancel();

  return await new Promise((resolve, reject) => {
    utterance.onend = () => {
      resolve({
        voiceName: voice?.name ?? null,
        voiceLang: utterance.lang,
      });
    };
    utterance.onerror = () => {
      reject(new Error("Speech synthesis failed"));
    };
    speech.speak(utterance);
  });
}

export async function speakTextIfSupported(
  text: string,
): Promise<SpeechPlaybackResult> {
  if (!hasSpeechSynthesisSupport()) {
    return {
      played: false,
      reason: "unsupported",
      error: "Speech synthesis is not supported in this browser",
    };
  }

  try {
    const result = await speakText(text);
    return {
      played: true,
      voiceName: result.voiceName,
      voiceLang: result.voiceLang,
    };
  } catch (error) {
    return {
      played: false,
      reason: "error",
      error: error instanceof Error ? error.message : "Speech synthesis failed",
    };
  }
}

async function waitForSpanishVoice(
  speech: SpeechSynthesis,
): Promise<SpeechSynthesisVoice | null> {
  const voices = speech.getVoices();
  if (voices.length > 0) {
    return selectSpanishVoice(voices);
  }

  return await new Promise((resolve) => {
    const timeoutId = window.setTimeout(() => resolve(null), 1000);

    const handleVoicesChanged = () => {
      window.clearTimeout(timeoutId);
      speech.removeEventListener("voiceschanged", handleVoicesChanged);
      resolve(selectSpanishVoice(speech.getVoices()));
    };

    speech.addEventListener("voiceschanged", handleVoicesChanged, {
      once: true,
    });
  });
}

function writeString(view: DataView, offset: number, value: string) {
  for (let i = 0; i < value.length; i += 1) {
    view.setUint8(offset + i, value.charCodeAt(i));
  }
}
