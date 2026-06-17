# TONTO Known Limitations

**Audience:** presentation audience, demo operator, and future project contributors
**Purpose:** document what the MVP does not yet solve, what remains fragile, and what should be considered future work.
**Last Updated:** 2026-06-18

TONTO Kids Assistant is an MVP built to validate a simple educational voice loop on accessible hardware:

```text
child voice -> Raspberry/client capture -> backend STT + chat -> spoken answer
```

The current system is demo-ready within that scope. The limitations below are intentional MVP boundaries or known technical risks, not hidden product promises.

## Summary

| Limitation | What it means | Demo impact | Current mitigation |
|---|---|---|---|
| Robotic TTS quality | Raspberry speech output uses local `espeak`. | The voice is audible and functional, but not natural. | Speech speed and gap were tuned for clarity; response text is also visible in the terminal. |
| No persistent memory | Session history is kept in backend process memory only. | Restarting the backend loses the current conversation context. | The demo uses one running backend session and short contextual follow-ups. |
| No wake word | TONTO does not continuously listen for "Hey TONTO" or similar. | The operator must press Enter on Raspberry or use the web microphone button. | The demo checklist presents this as the expected interaction model. |
| No Arduino or LED physical states | Physical light/status feedback is outside the six-week MVP. | TONTO has no external LED state such as listening, thinking, or speaking. | Raspberry and web clients show non-physical listening/time indicators. |
| Network and provider dependency | STT and chat generation require backend access and an external provider. | Internet, API credentials, LAN, or provider issues can block voice turns. | OpenAI is the primary demo provider; DevExpert is available as an alternate provider smoke path. |
| Single validated Raspberry | The demo is validated on one Raspberry Pi setup. | If that device, microphone, or speaker fails, there is no identical hardware backup. | Web voice and text fallback are documented in the demo checklist. |
| Turn latency | Voice turns usually take a few seconds end to end. | The audience may notice a pause between speech input and spoken answer. | The operator waits for completion and uses short questions. |
| DevExpert response style | DevExpert `mimo-v2.5` can be more verbose than OpenAI `gpt-4o-mini`. | Demo pacing can vary when using DevExpert. | OpenAI remains the recommended primary presentation provider. |
| ALSA/JACK warnings | Raspberry audio stack warnings are suppressed or filtered, not eliminated at the system level. | Warnings should not appear in normal demo output, but could return if audio configuration changes. | Week 05 error-resilience work suppresses expected noise and keeps operator messages readable. |

## Detailed Limitations

### Robotic TTS Quality

TONTO speaks through `espeak` on Raspberry Pi. This keeps the physical demo simple, local, and reproducible, but the voice is clearly synthetic and robotic.

Impact: the demo validates that TONTO can answer aloud through the Raspberry, but it does not demonstrate a polished child-friendly voice. This is acceptable for the MVP because the goal is to prove the end-to-end loop, not final voice quality.

Current mitigation: `espeak` arguments were tuned during Week 03 to improve intelligibility for longer Spanish answers. The terminal still prints the response text, so the operator has a visible fallback if audio is hard to understand.

### No Persistent Memory

The backend keeps a short session history in process memory. There is no database, file-backed storage, account system, or long-term profile.

Impact: TONTO can answer short follow-up questions during a running session, but restarting the backend clears context. It cannot remember a child, preferences, past sessions, or prior days.

Current mitigation: the demo uses a single active backend process and a short sequence of related questions. This proves short-context behavior without introducing persistence into the MVP.

### No Wake Word

TONTO does not listen continuously and does not wake on a spoken phrase. Raspberry voice mode starts each recording after the operator presses Enter. The web client records after the user activates the microphone control.

Impact: the experience is not yet hands-free. It is closer to a controlled voice terminal than a finished ambient assistant.

Current mitigation: the presentation should describe this as the intentional MVP interaction model. It avoids accidental recording, keeps the demo deterministic, and reduces hardware/audio complexity.

### No Arduino or LED Physical States

Arduino integration and LED states were explicitly deferred outside the six-week MVP. TONTO does not yet have physical indicators for listening, thinking, speaking, or error states.

Impact: the physical object provides voice interaction through Raspberry audio, but not external visual feedback.

Current mitigation: Week 04 added non-physical indicators first: Raspberry shows listening progress in the terminal, and the web client shows timer/progress feedback during capture.

### Network and Provider Dependency

The Raspberry client depends on LAN access to the backend. The backend depends on configured provider credentials and network access for STT and chat generation.

Impact: a bad LAN IP, firewall issue, missing API key, provider outage, or internet problem can block live voice turns.

Current mitigation: `docs/demo-checklist.md` includes backend health checks, Raspberry preflight checks, provider smoke tests, and Plan B fallbacks. OpenAI is the primary validated provider, while DevExpert remains available for course-aligned smoke validation.

### Single Validated Raspberry

The MVP has been validated on one Raspberry Pi 3 setup with one known microphone/speaker configuration.

Impact: hardware failure during presentation would be a real demo risk. A second Raspberry or duplicate audio kit has not been validated as a drop-in replacement.

Current mitigation: the web voice loop and text fallback provide alternate ways to demonstrate backend behavior if the physical client fails.

### Turn Latency

Voice turns include recording time, upload, STT, chat generation, response handling, and speech output. Week 03 and Week 05 validation showed the loop is usable, but it is not instant.

Impact: the audience should expect a pause after each spoken question. Long or unclear questions can increase perceived delay.

Current mitigation: the demo sequence uses short questions, waits for each answer before continuing, and avoids changing provider settings live.

### DevExpert Response Style

DevExpert Inference is supported through backend provider selection, but its `mimo-v2.5` model can answer more verbosely than OpenAI `gpt-4o-mini` for the same TONTO prompt.

Impact: DevExpert is useful for provider validation and course alignment, but may affect demo pacing if used as the main live provider.

Current mitigation: OpenAI remains the recommended primary presentation provider. DevExpert is documented as an alternate smoke path unless there is a specific reason to present provider switching.

### ALSA/JACK Warnings

Earlier Raspberry runs produced ALSA/JACK warning noise from audio commands. Week 05 filtered or suppressed the expected warnings in the client path, but the underlying Raspberry audio stack can still produce them if commands are run manually or the audio device changes.

Impact: normal demo output should stay clean, but audio configuration changes could make warnings visible again.

Current mitigation: Week 05 error-resilience work keeps operator-facing output readable and treats these warnings as non-blocking unless recording or playback actually fails.

## Out of Scope for the MVP

The following items are not part of the six-week MVP and should be discussed as future work rather than current defects:

- production-quality child voice,
- persistent child profiles or long-term memory,
- wake word detection,
- Arduino/LED physical states,
- offline/local STT or local LLMs,
- multi-user support,
- authentication or user accounts,
- cloud deployment,
- dashboards or analytics,
- automatic provider fallback or load balancing.

## Presentation Framing

The clearest way to present these limitations is:

```text
This MVP validates the core loop: a child can ask a question by voice, the backend generates a short educational answer, and the Raspberry speaks it aloud. The remaining limitations are mostly productization work: better voice, more robust hardware, persistence, wake word, physical states, and deployment.
```
