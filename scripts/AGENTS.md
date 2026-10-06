# Official script context

Read [root](../AGENTS.md) and [workflow](../docs/ai-assisted-workflow.md) before
commands/edits. For source changes, read affected backend/client/web locals and
[tests](../tests/AGENTS.md). Follow #110 before diagnostics, export or mount work.

## Purpose, interfaces and dependencies

Root `tonto.sh` is the Linux/Docker command dispatcher used by humans, agents and
CI; scripts/ supplies narrower operating helpers. Public entry points:

- `agent-backend.sh {start|stop|status|health}`: backend Compose lifecycle and
  bounded health retries; start uses current runtime port mapping (LAN-capable).
- `agent-raspberry.sh {preflight|exec}`: key-based OpenSSH, BatchMode,
  IdentitiesOnly and timeout; exec runs a command inside TONTO_PI_REPO. Optional
  skip/mock flags report skipped hardware, not validated hardware.
- `demo-raspberry.sh`: health/venv checks then voice client;
  `demo-touch.sh`: touch process startup, not foreground voice capture.
- `ui-emulator.sh`: sourced by tonto.sh; discovers audio device group IDs and
  writes a temporary device/group override on native Engine. Docker Desktop
  uses local socat screen/audio bridges with lifecycle cleanup and temporary
  environment override. Never captures expanded runtime config or changes X11
  permissions. See issue 003 and emulator spec for supported prerequisites.
- `check_syntax.py`: AST parsing backend/client/shared/tests without importing
  them. `export-docs-for-notebooklm.sh`: validated public Markdown export.
- `install-git-hooks.sh`: local pre-commit export hook; current implementation
  expects .git as a directory, so do not assume linked-worktree support.
- `tonto-touch.service`: Raspberry systemd configuration; not a host service to
  activate during tests.

Depends on: Bash, Docker/Compose, OpenSSH/curl for operation, repo-local Python
for syntax/export helper code, device tools for demos, public source files and
appropriate local configuration. Used by: tonto.sh, CI and operator/agent
runbooks; tests/test_*_cli.py and test_notebooklm_export.py consume script behavior
in fixtures/stubs. Client/backend/web do not import these scripts.

## Impact and validation

Read [capability pack](../ai/specs/027-week-05-agent-capability-pack/spec.md) with its historical
notice, [demo runbook](../docs/demo-runbook.md),
[Raspberry setup](../docs/raspberry-pi-setup.md),
[secret spec](../ai/specs/003-agent-secrets-protection/spec.md),
[cleanup](../ai/specs/008-docker-cleanup/spec.md) and
[documentation workflow](../docs/documentation-workflow.md) as appropriate.
Changes to setup/dev/test/build require scripts and documentation together;
task Compose remains credential-free and runtime .env workflow is preserved.
Mount/build allowlists and export path protections are behavior contracts.

Use `bash -n` on modified Bash files and `./tonto.sh test python` for CLI/export
regressions. CI uses setup/test all/build all. Read source instead of executing
SSH/process/audio operations just to establish that a command exists. Helpers
can affect running services; live operation requires the corresponding task scope.
Export/hook source selection does not include every new local AGENTS.md; repo
navigation remains authoritative.
