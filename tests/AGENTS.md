# Test context

Read [root](../AGENTS.md) and [workflow](../docs/ai-assisted-workflow.md) first,
then the local instructions of the implementation under test. Tests depend on
implementation; current product modules do not import test fixtures.

## Structure and interfaces

`conftest.py` supplies FastAPI TestClient, isolated fixture WAV/audio paths and
mock chat/STT calls. `test_audio.py`/`test_example.py` cover API behavior;
`test_openai_client.py`/`test_stt_client.py` cover provider selection, request and
error handling with HTTP mocks. `test_client.py` tests Python client/device
helpers with substitutes. `test_safe_diagnostics.py` uses fictitious canaries
and checks API/log/trace minimization. CLI setup/task/cleanup/emulator and export
tests run original scripts copied into fixtures with bounded stubs.
`test_container_mounts.py` checks effective mounts in the task container.
`test_tonto_face.py` and `test_touch_ui.py` exercise real Kivy widgets/Clock under
SDL2/Xvfb. Web helper tests belong to web/tests, not this suite.

Depends on: backend, client, scripts/CLI, pytest/httpx/TestClient and Kivy for UI;
task Docker mount paths for container tests. Used by: root tonto.sh and CI; no
runtime module consumes these fixtures. See [backend](../backend/AGENTS.md),
[client](../client/AGENTS.md), [scripts](../scripts/AGENTS.md) and
[web](../web/AGENTS.md) for reverse impact.

## Execution and limits

From root: `./tonto.sh test python` runs syntax and non-Kivy tests;
`./tonto.sh test ui` runs the two widget suites under Docker/Xvfb;
`./tonto.sh test all` also runs web tests. Use repo-local .venv Python only if a
direct narrow invocation is unavoidable; never global pytest. Add/update focused
tests for behavior changes, not for documentation restructuring alone.

Do not require real provider credentials or hardware in automated tests.
Preserve both provider adapters with mocks; D025 forbids real DevExpert operation.
Canaries are fictitious; failures must not dump sensitive values. Test coverage
does not establish audio quality, physical touch/kiosk, SSH readiness or live
provider availability. Read [Kivy coverage spec](../specs/kivy-ui-testing-coverage.md)
and [#110 spec](../specs/agent-secrets-protection.md) for these boundaries.
