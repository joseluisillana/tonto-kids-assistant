# TONTO Future Work

**Audience:** project owner, future contributors, and AI-assisted agents
**Purpose:** define the prioritized post-MVP backlog after the six-week demo.
**Last Updated:** 2026-06-18

TONTO Kids Assistant has validated the MVP loop:

```text
Raspberry voice input -> backend STT/chat -> Raspberry spoken response
```

The next stage should improve the physical assistant experience without losing the simple architecture that made the MVP reproducible. Future work should continue to favor narrow, testable increments over broad platform redesign.

## Priority Summary

| Priority | Item | Main area | Complexity | Why next |
|---|---|---|---|---|
| High | Raspberry Touch UI with animated assistant face | Raspberry/client UX | High | Turns the validated voice terminal into a more complete physical assistant. |
| High | Better TTS | Raspberry audio | Medium | Improves the child-facing quality of the demo without changing the core loop. |
| Medium | Inference provider improvements | Backend/provider config | Medium | Makes OpenAI and DevExpert operation more robust after the MVP. |
| Medium | Minimal session persistence | Backend/session state | Medium | Preserves useful short-term continuity across backend restarts. |
| Medium | Wake word spike | Raspberry/audio UX | High | Moves toward hands-free interaction, but carries privacy and reliability risk. |
| Medium | Arduino/LED physical states | Hardware/physical feedback | Medium | Adds physical status cues after the screen direction is established. |
| Low | Multi-user support | Backend/product scope | High | Useful only after single-device use is stable. |
| Low | Metrics and demo diagnostics | Backend/operator tooling | Medium | Helps repeated testing, but should not become a dashboard project too early. |

## Explicitly Not Prioritized: Cloud Deployment

Cloud deployment is intentionally not a post-MVP milestone right now.

It would mean moving the backend from the local development PC to a hosted server or managed runtime so Raspberry clients could connect to a stable remote URL. That may become useful later for remote demos, multiple devices, or operation outside a LAN.

It is not the right next step because it adds operational surface area without improving the physical child-facing experience:

- hosting and HTTPS setup,
- secret management,
- privacy considerations for child voice data,
- network and provider observability,
- deployment troubleshooting,
- additional documentation and support burden.

The next project direction is to improve the Raspberry as a physical assistant while keeping the backend external and simple. The backend may continue to run on a local PC or another controlled machine reachable through `TONTO_BACKEND_URL`.

## 1. Raspberry Touch UI With Animated Assistant Face

**Priority:** High
**Complexity:** High
**Primary areas:** Raspberry client, web-style UI, hardware setup, documentation

### Goal

Add a second Raspberry interface using the selected Waveshare 5" HDMI touch display. The screen should make TONTO feel like a visible assistant, not only a terminal voice client.

The existing Python terminal client remains the fallback path. This new interface should not remove or destabilize the validated voice loop.

### Target Experience

The Raspberry shows a mostly visual interface:

- an animated TONTO face or character,
- a large touch button to speak,
- visual states for idle, listening, thinking, speaking, and error,
- listening progress while recording,
- audible response through the Raspberry speaker,
- optional text mode for transcript, response, and conversation thread.

The primary child-facing mode should avoid dense text. Text display is optional and should be useful for operator debugging, accessibility, or classroom visibility.

### Architecture

The Raspberry remains a thin client:

```text
Raspberry touch UI/audio -> external backend -> STT/chat -> Raspberry speech/avatar state
```

Included:

- UI and client run on the Raspberry.
- Backend remains external and is configured with `TONTO_BACKEND_URL`.
- The current `/chat` and `/chat/audio` contracts should remain stable at first.
- The current Python client remains documented as fallback.

Excluded from the first iteration:

- running the FastAPI backend on the Raspberry,
- changing the backend API contract,
- cloud deployment,
- perfect phoneme-level lip sync,
- replacing the existing demo path.

### Recommended Execution Steps

1. **Hardware bring-up**
   - Connect the Waveshare 5" HDMI touch display.
   - Validate HDMI output, resolution, orientation, and USB touch input.
   - Confirm the microphone and speaker still work with the screen attached.
   - Document cabling, power, display settings, and smoke commands.

2. **UI runtime spike**
   - Evaluate a browser/kiosk UI on Raspberry first, because it can reuse web-client patterns.
   - Validate touch responsiveness, animation smoothness, recording, upload, and audio playback on Raspberry Pi 3.
   - If Chromium is too heavy, evaluate a lighter local UI approach before adding dependencies.

3. **Minimum touch client**
   - Add a large speak button.
   - Show listening progress and status.
   - Send recorded audio to `POST /chat/audio`.
   - Show response state and play audio through Raspberry output.
   - Keep behavior aligned with the existing web and Raspberry clients.

4. **Animated assistant face**
   - Implement simple but expressive states first: idle, listening, thinking, speaking, error.
   - Synchronize mouth and eyes to speaking state and estimated TTS duration in the first pass.
   - Treat precise phoneme/viseme sync as a later refinement.

5. **Optional text mode**
   - Provide a secondary view or operator toggle for transcript, response, and conversation thread.
   - Keep the default child-facing screen visual and simple.

6. **Kiosk and fallback operation**
   - Document startup into full-screen/kiosk mode.
   - Keep the Python terminal client as Plan B.
   - Add troubleshooting for display, touch, audio, backend URL, and provider failures.

7. **Validation**
   - Create a touch-display validation checklist.
   - Record hardware evidence in the project journal.
   - Confirm the existing terminal client still works after the new UI is added.

### Open Decisions

- Whether the UI should reuse the current React web client directly or use a separate Raspberry-specific surface.
- Whether optional text mode is visible to the child or hidden behind an operator control.
- Whether the first animated face should be CSS/canvas based or asset driven.
- Whether Raspberry Pi 3 performance is sufficient for browser kiosk mode plus audio capture/playback.

## 2. Better TTS

**Priority:** High
**Complexity:** Medium
**Primary areas:** Raspberry audio, provider evaluation, demo UX

### Goal

Improve TONTO's spoken voice quality beyond `espeak` while preserving reproducibility and Raspberry compatibility.

### Why It Matters

`espeak` is functional and local, but robotic. Better voice quality would make TONTO feel more child-friendly and polished.

### Candidate Directions

- Tune `espeak` further only if it produces a meaningful improvement.
- Evaluate lightweight local alternatives compatible with Raspberry.
- Evaluate provider-based TTS only if latency, privacy, cost, and setup complexity are acceptable.
- Consider DevExpert TTS only after provider documentation and limits are confirmed.

### Acceptance For A Future Iteration

- Voice is more natural or easier to understand than the current `espeak` setup.
- Setup remains reproducible.
- Raspberry fallback remains available.
- Demo documentation clearly states which TTS path is active.

## 3. Inference Provider Improvements

**Priority:** Medium
**Complexity:** Medium
**Primary areas:** backend provider layer, documentation, validation

### Goal

Build on the OpenAI and DevExpert provider support completed during Week 05.

### Candidate Work

- Manual provider smoke checklist improvements.
- Clearer provider configuration diagnostics.
- Optional fallback strategy after a provider failure.
- Better control of DevExpert verbosity.
- Future provider additions such as Gemini only after a small provider spec.
- DevExpert TTS exploration if it becomes useful for voice quality.

### Related Tracking

The existing provider backlog is tracked by issue #53.

### Constraints

- Do not expose provider complexity to the Raspberry or web clients.
- Preserve `/chat` and `/chat/audio` contracts.
- Keep OpenAI and DevExpert validation coverage when behavior changes.

## 4. Minimal Session Persistence

**Priority:** Medium
**Complexity:** Medium
**Primary areas:** backend session state, privacy, documentation

### Goal

Persist minimal conversation state or preferences so a backend restart does not immediately erase useful context.

### Candidate Scope

- Store short session summaries rather than full long-term memory.
- Keep storage local and inspectable at first.
- Add explicit reset/clear behavior.
- Document privacy and retention behavior clearly.

### Excluded Initially

- user accounts,
- child profiles,
- vector memory,
- cloud databases,
- advanced personalization.

## 5. Wake Word Spike

**Priority:** Medium
**Complexity:** High
**Primary areas:** Raspberry audio, privacy, interaction design

### Goal

Explore whether TONTO can start listening from a spoken activation phrase instead of a touch button or Enter key.

### Why It Is Deferred

Wake word support changes the interaction model and introduces risk:

- false positives,
- missed activations,
- privacy expectations,
- local CPU constraints,
- microphone contention with recording.

### Future Spike Acceptance

- Technical options are compared.
- Privacy and demo implications are documented.
- A minimal prototype proves feasibility before productizing.

## 6. Arduino And LED Physical States

**Priority:** Medium
**Complexity:** Medium
**Primary areas:** hardware, Raspberry integration, physical UX

### Goal

Add physical light states for listening, thinking, speaking, and error.

### Relationship To The Touch Screen

Arduino/LEDs were deferred during the six-week MVP. After the Waveshare screen direction, LEDs become complementary rather than mandatory. The screen can carry the main expressive state, while LEDs can add ambient physical feedback.

### Candidate Scope

- Define a small state contract.
- Validate Arduino/Raspberry communication.
- Keep behavior simple and deterministic.
- Document wiring and recovery steps.

## 7. Multi-User Support

**Priority:** Low
**Complexity:** High
**Primary areas:** backend product scope, privacy, data model

### Goal

Support more than one child, classroom, or device session.

### Why It Is Later

Multi-user support implies identity, storage, privacy rules, and more complex testing. It should wait until one physical assistant experience is stable and useful.

## 8. Metrics And Demo Diagnostics

**Priority:** Low
**Complexity:** Medium
**Primary areas:** backend logs, operator tooling, documentation

### Goal

Capture enough operational evidence to understand repeated demos and failures.

### Candidate Scope

- Turn latency measurements.
- Provider selected per turn.
- STT success/failure counts.
- Operator-friendly diagnostics.
- Simple export for project evidence.

### Constraint

Avoid building a dashboard before there is repeated real usage. Start with logs or small textual summaries.

## Backlog Rules

Future work should follow the same project rules as the MVP:

- one coherent work item per branch and PR,
- specs and plans before material behavior changes,
- documentation updated with setup and validation evidence,
- no new dependencies without an explicit decision,
- Raspberry client remains simple and inspectable,
- backend contracts stay stable unless a spec explicitly changes them,
- hardware validation is recorded in the journal.

