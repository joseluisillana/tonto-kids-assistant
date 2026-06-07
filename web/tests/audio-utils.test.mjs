import assert from "node:assert/strict";

import {
  calculateDurationProgress,
  calculatePeakAmplitude,
  calculateRmsAmplitude,
  combineFloat32Chunks,
  downsampleBuffer,
  encodeWavPcm16Mono,
  formatBytes,
  formatClockDuration,
  formatRecordingDurationLabel,
  normalizePeak,
  prepareSpeechSamples,
  selectSpanishVoice,
  speakTextIfSupported,
  trimSilence,
} from "../.tmp-test/src/lib/audio.js";

function assertAlmostEqual(actual, expected, tolerance = 0.001) {
  assert.ok(
    Math.abs(actual - expected) <= tolerance,
    `Expected ${actual} to be within ${tolerance} of ${expected}`,
  );
}

{
  const result = combineFloat32Chunks([
    Float32Array.from([0.25, 0.5]),
    Float32Array.from([0.75]),
  ]);
  assert.deepEqual(Array.from(result), [0.25, 0.5, 0.75]);
}

{
  const result = downsampleBuffer(
    Float32Array.from([0, 1, 0, -1]),
    4,
    2,
  );
  assert.equal(result.length, 2);
  assert.deepEqual(Array.from(result), [0.5, -0.5]);
}

{
  const samples = Float32Array.from([0, 0.25, -0.5, 0.25]);
  assert.equal(calculatePeakAmplitude(samples), 0.5);
  assert.ok(Math.abs(calculateRmsAmplitude(samples) - 0.306) < 0.001);
}

{
  const sampleRate = 1_000;
  const samples = Float32Array.from([
    0,
    0,
    0,
    0.02,
    0.04,
    0.01,
    0,
    0,
  ]);
  const trimmed = trimSilence(samples, sampleRate, {
    threshold: 0.015,
    paddingMs: 1,
  });
  assert.equal(trimmed.length, 4);
  assertAlmostEqual(trimmed[0], 0);
  assertAlmostEqual(trimmed[1], 0.02);
  assertAlmostEqual(trimmed[2], 0.04);
  assertAlmostEqual(trimmed[3], 0.01);
}

{
  const { samples, gain } = normalizePeak(Float32Array.from([0.1, -0.2]), {
    targetPeak: 0.8,
    maxGain: 10,
  });
  assertAlmostEqual(gain, 4);
  assertAlmostEqual(samples[0], 0.4);
  assertAlmostEqual(samples[1], -0.8);
}

{
  const sampleRate = 1_000;
  const samples = new Float32Array(700);
  samples.fill(0);
  samples.fill(0.03, 200, 500);
  const prepared = prepareSpeechSamples(samples, sampleRate);
  assert.equal(prepared.hasSpeech, true);
  assert.equal(prepared.durationMs, 620);
  assert.ok(prepared.gain > 1);
  assert.ok(prepared.peakAmplitude > 0.3);
}

{
  const prepared = prepareSpeechSamples(new Float32Array(600), 1_000);
  assert.equal(prepared.hasSpeech, false);
  assert.equal(prepared.samples.length, 0);
}

{
  const bytes = encodeWavPcm16Mono(Float32Array.from([0, 1, -1]), 16_000);
  assert.equal(String.fromCharCode(...bytes.slice(0, 4)), "RIFF");
  assert.equal(String.fromCharCode(...bytes.slice(8, 12)), "WAVE");
  assert.equal(bytes.length, 44 + 3 * 2);
}

{
  assert.equal(formatBytes(512), "512 B");
  assert.equal(formatBytes(1536), "1.5 KB");
}

{
  assert.equal(formatClockDuration(0), "00:00");
  assert.equal(formatClockDuration(3_200), "00:03");
  assert.equal(formatClockDuration(65_999), "01:05");
  assert.equal(formatClockDuration(-1), "00:00");
}

{
  assert.equal(calculateDurationProgress(0, 10_000), 0);
  assert.equal(calculateDurationProgress(5_000, 10_000), 50);
  assert.equal(calculateDurationProgress(15_000, 10_000), 100);
  assert.equal(calculateDurationProgress(5_000, 0), 0);
}

{
  assert.equal(formatRecordingDurationLabel(3_200, 10_000), "00:03 / 00:10");
}

{
  const voice = selectSpanishVoice([
    { lang: "en-US", name: "English", default: false },
    { lang: "es-ES", name: "Spanish", default: false },
  ]);
  assert.equal(voice?.name, "Spanish");
}

{
  const originalWindow = globalThis.window;
  const originalUtterance = globalThis.SpeechSynthesisUtterance;
  const spokenTexts = [];

  class TestUtterance {
    constructor(text) {
      this.text = text;
      this.lang = "";
      this.voice = null;
      this.onend = null;
      this.onerror = null;
    }
  }

  const speechSynthesis = {
    getVoices: () => [{ lang: "es-ES", name: "Spanish", default: false }],
    cancel: () => {},
    speak: (utterance) => {
      spokenTexts.push(utterance.text);
      utterance.onend();
    },
  };

  globalThis.SpeechSynthesisUtterance = TestUtterance;
  globalThis.window = {
    speechSynthesis,
    SpeechSynthesisUtterance: TestUtterance,
  };

  try {
    const result = await speakTextIfSupported("Hola desde texto");

    assert.deepEqual(spokenTexts, ["Hola desde texto"]);
    assert.deepEqual(result, {
      played: true,
      voiceName: "Spanish",
      voiceLang: "es-ES",
    });
  } finally {
    globalThis.window = originalWindow;
    globalThis.SpeechSynthesisUtterance = originalUtterance;
  }
}

{
  const originalWindow = globalThis.window;
  const originalUtterance = globalThis.SpeechSynthesisUtterance;

  try {
    delete globalThis.window;
    delete globalThis.SpeechSynthesisUtterance;

    const result = await speakTextIfSupported("Hola sin speech");

    assert.equal(result.played, false);
    assert.equal(result.reason, "unsupported");
  } finally {
    globalThis.window = originalWindow;
    globalThis.SpeechSynthesisUtterance = originalUtterance;
  }
}
