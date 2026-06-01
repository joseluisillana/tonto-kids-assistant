import assert from "node:assert/strict";

import {
  BackendRequestError,
  sendAudioTurn,
} from "../.tmp-test/src/api/backendClient.js";

{
  const originalFetch = globalThis.fetch;
  const calls = [];

  globalThis.fetch = async (_url, init) => {
    calls.push({
      url: String(_url),
      body: init?.body,
    });

    return new Response(
      JSON.stringify({
        session_id: "  session-1  ",
        transcript: "  hola tonto  ",
        response: "  Hola, soy TONTO  ",
      }),
      {
        status: 200,
        headers: {
          "Content-Type": "application/json",
        },
      },
    );
  };

  try {
    const result = await sendAudioTurn(
      {
        session_id: "session-1",
        device_id: "web-validation-client",
        duration_ms: 1234,
        sample_rate_hz: 16_000,
        channels: 1,
        language: "es",
        audio: new Blob([Uint8Array.from([1, 2, 3])], {
          type: "audio/wav",
        }),
      },
      "http://localhost:8000",
    );

    assert.deepEqual(result, {
      session_id: "session-1",
      transcript: "hola tonto",
      response: "Hola, soy TONTO",
    });

    assert.equal(calls.length, 1);
    assert.equal(calls[0].url, "http://localhost:8000/chat/audio");

    const formData = calls[0].body;
    assert.equal(formData.get("session_id"), "session-1");
    assert.equal(formData.get("device_id"), "web-validation-client");
    assert.equal(formData.get("duration_ms"), "1234");
    assert.equal(formData.get("sample_rate_hz"), "16000");
    assert.equal(formData.get("channels"), "1");
    assert.equal(formData.get("language"), "es");

    const audioEntry = formData.get("audio");
    assert.ok(audioEntry instanceof File);
    assert.equal(audioEntry.name, "turn.wav");
    assert.equal(audioEntry.type, "audio/wav");
  } finally {
    globalThis.fetch = originalFetch;
  }
}

{
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async () =>
    new Response(
      JSON.stringify({ detail: "Audio did not contain recognizable speech" }),
      {
        status: 422,
        headers: {
          "Content-Type": "application/json",
        },
      },
    );

  try {
    await assert.rejects(
      sendAudioTurn(
        {
          session_id: "session-1",
          device_id: "web-validation-client",
          duration_ms: 1234,
          sample_rate_hz: 16_000,
          channels: 1,
          language: "es",
          audio: new Blob([Uint8Array.from([1, 2, 3])], {
            type: "audio/wav",
          }),
        },
        "http://localhost:8000",
      ),
      (error) =>
        error instanceof BackendRequestError &&
        error.status === 422 &&
        error.message.includes("Audio did not contain recognizable speech"),
    );
  } finally {
    globalThis.fetch = originalFetch;
  }
}

{
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async () => {
    throw new DOMException("The operation was aborted.", "AbortError");
  };

  try {
    await assert.rejects(
      sendAudioTurn(
        {
          session_id: "session-1",
          device_id: "web-validation-client",
          duration_ms: 1234,
          sample_rate_hz: 16_000,
          channels: 1,
          language: "es",
          audio: new Blob([Uint8Array.from([1, 2, 3])], {
            type: "audio/wav",
          }),
        },
        "http://localhost:8000",
      ),
      (error) => error instanceof Error && error.message.includes("tiempo limite"),
    );
  } finally {
    globalThis.fetch = originalFetch;
  }
}
