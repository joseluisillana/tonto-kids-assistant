---
id: "027-week-05-agent-capability-pack"
title: "Week 05 Agent Capability Pack"
status: done
owner: "Unknown — legacy ownership not recorded"
created: "2026-06-09"
updated: "2026-10-06"
related:
  - "https://github.com/joseluisillana/tonto-kids-assistant/blob/818e88eacbac3989c091d1294c92e26ebeb663f7/specs/week-05-agent-capability-pack.md"
  - "ai/specs/001-historical-records-migration/metadata-review.md"
  - "https://github.com/joseluisillana/tonto-kids-assistant/issues/43"
  - "docs/project-journal/week-05.md"
  - "ai/specs/027-week-05-agent-capability-pack/plan.md"
---

# Week 05 Agent Capability Pack

**Status:** Implemented
**Tracking:** GitHub issue #43
**Last Updated:** 2026-06-09

## Current navigation — historical implementation below

The interfaces below record the original Windows implementation. Linux/Docker
migration replaced those runtime scripts with Bash; do not recreate or execute
the PowerShell examples. Current operation is described by
[Agent Capability Pack](../../../docs/ai-assisted-workflow.md#agent-capability-pack),
[script context](../../../scripts/AGENTS.md) and the actual `scripts/agent-backend.sh`
and `scripts/agent-raspberry.sh`. SSH safety and portable repo-owned guidance
remain applicable. This is an editorial navigation correction, not a new
behavior, contract or implementation phase.

## Objective

Create a portable Agent Capability Pack so Codex, OpenCode, and other AI-assisted agents can operate common TONTO development tasks through repository-owned Markdown and Bash helpers.

The pack exists to prevent agents from inventing ad hoc backend startup or Raspberry SSH commands during demo validation. It keeps the repository as the source of truth and makes the same command surface usable by humans and agents.

## Source of Truth

The source of truth is:

- repo Markdown documentation,
- official scripts in `scripts/`,
- local environment variables for machine-specific values.

Codex skills, OpenCode prompts, plugins, or MCP tools may wrap this pack later, but they must delegate to these repo-owned docs and scripts. Tool-specific assets must not become the canonical project workflow.

## Included

- Define the backend agent helper script interface.
- Define the Raspberry agent helper script interface.
- Define a reproducible dedicated SSH key workflow for Raspberry access.
- Document where local environment variables live and which values are required.
- Update the Week 05 journal and workflow docs so future agents discover the pack.

## Excluded

- No new runtime or development dependencies.
- No secrets committed to the repository.
- No password-based SSH automation.
- No full voice automation that pretends to replace a human speaking into the microphone.
- No replacement of existing official scripts such as `scripts/dev.ps1`, `scripts/test.ps1`, or `scripts/build.ps1`.

## Backend Helper

Create `scripts/agent-backend.ps1`.

Interface:

```powershell
.\scripts\agent-backend.ps1 -Action start [-AllowLan]
.\scripts\agent-backend.ps1 -Action stop
.\scripts\agent-backend.ps1 -Action status
.\scripts\agent-backend.ps1 -Action health
```

Behavior:

- `start` launches the backend in the background using `scripts/dev.ps1 -Service backend`.
- `-AllowLan` passes through to the existing backend dev script.
- `start` writes process metadata under `.cache/agent/`:
  - `backend.pid`
  - `backend.out.log`
  - `backend.err.log`
- `start` waits until `/health` returns `{"status":"ok"}` or fails with a clear timeout.
- `stop` only stops the PID recorded in `.cache/agent/backend.pid`.
- `status` reports the recorded PID, whether it is alive, the health result, and log paths.
- `health` checks `http://127.0.0.1:8000/health` by default.

Safety:

- The helper must never kill generic `python`, `powershell`, or `pwsh` processes.
- The helper must avoid writing outside `.cache/agent/`.
- The helper must preserve the existing `scripts/dev.ps1` behavior for humans.

## Raspberry Helper

Create `scripts/agent-raspberry.ps1`.

Interface:

```powershell
.\scripts\agent-raspberry.ps1 -Action preflight
.\scripts\agent-raspberry.ps1 -Action exec -Command "<remote command>"
```

Environment variables:

| Variable | Default | Purpose |
|---|---|---|
| `TONTO_PI_HOST` | `tonto-pi.local` | Raspberry SSH host |
| `TONTO_PI_USER` | `tonto-pi-user` | Raspberry SSH user |
| `TONTO_PI_SSH_KEY` | `$HOME\.ssh\tonto_agent_ed25519` | Dedicated private key path |
| `TONTO_PI_REPO` | `~/tonto-kids-assistant` | Repository path on Raspberry |
| `TONTO_BACKEND_URL` | unset | Optional backend URL to check from Raspberry |

SSH behavior:

- Use OpenSSH with:
  - `BatchMode=yes`
  - `IdentitiesOnly=yes`
  - `ConnectTimeout=5`
  - `-i $env:TONTO_PI_SSH_KEY`
- Do not accept or print passwords.
- Do not print private key contents.
- Fail clearly when the key, host, or repo path is missing.

`preflight` validates:

- SSH connection works.
- `hostname` and `whoami` are visible.
- `TONTO_PI_REPO` exists.
- `git status --short --branch` runs inside the Raspberry repo.
- `python3`, `curl`, `arecord`, `aplay`, and `espeak` are available.
- `.venv/bin/python` exists inside the Raspberry repo and is the Python used for project client execution.
- If `TONTO_BACKEND_URL` is set, Raspberry can reach `$TONTO_BACKEND_URL/health`.

`exec` behavior:

- Runs the provided command from `TONTO_PI_REPO`.
- Returns the remote exit code.
- Keeps command output visible for evidence capture.

## Dedicated SSH Key Workflow

Document the setup in both `docs/raspberry-pi-setup.md` and the future Agent Capability Pack operator guide.

Human setup command on Windows:

```powershell
ssh-keygen -t ed25519 -f "$env:USERPROFILE\.ssh\tonto_agent_ed25519" -C "tonto-agent"
```

Installation:

- Copy the `.pub` key to the Raspberry user's `~/.ssh/authorized_keys`.
- Keep permissions valid on Raspberry:
  - `chmod 700 ~/.ssh`
  - `chmod 600 ~/.ssh/authorized_keys`
- Set local environment variables if defaults are not enough.

Revocation:

- Remove the matching `tonto-agent` public key line from `~/.ssh/authorized_keys`.
- Delete or rotate the local private key if needed.

Security:

- Never commit private keys.
- Never commit passwords.
- Prefer key-based SSH over password automation.
- Treat password environment variables as out of scope for this MVP workflow.

## Acceptance Criteria

- `scripts/agent-backend.ps1` can start, health-check, status-check, and stop only the backend process it started.
- `scripts/agent-raspberry.ps1 -Action preflight` confirms Raspberry readiness without interactive auth.
- `scripts/agent-raspberry.ps1 -Action exec` can run a safe command from the Raspberry repo.
- Documentation explains how to create, install, use, and revoke the dedicated SSH key.
- No repo-tracked file contains secrets or machine-specific private values.
- Week 05 Phase 2 issue #36 can be resumed using these helpers for Raspberry validation.

## Validation Plan

After implementation:

```powershell
.\scripts\agent-backend.ps1 -Action start -AllowLan
.\scripts\agent-backend.ps1 -Action health
.\scripts\agent-backend.ps1 -Action status
.\scripts\agent-backend.ps1 -Action stop
.\scripts\agent-raspberry.ps1 -Action preflight
```

Then resume #36 and run the 5+ Raspberry demo-question validation using the new helpers.

## Migration provenance and supported current state

- Original repository source: `specs/week-05-agent-capability-pack.md` at baseline 818e88e.
- First recorded Git date: 2026-06-09; actual original authoring date is unknown
  unless explicitly recorded in the preserved body.
- Last source Git date before migration: 2026-10-06.
- Migration/update date: 2026-10-06. Legacy owner/authorship is not established;
  the current owner field records that uncertainty, not a fabricated attribution.
- Status decision: Capability Pack implemented/integrated #45 and preflight evidence; Linux migration subsequently replaced PowerShell operating examples.
- Evidence: [source](../../../docs/project-journal/week-05.md).
- Corresponding GitHub tracking issues: [GitHub issue](https://github.com/joseluisillana/tonto-kids-assistant/issues/43).

Historical headings below/above retain the original reported state. YAML status
and this provenance annotation express the supported state after evidence review.
Do not execute archived proposals or historical operating examples without a new
authorized work item. No runtime or acceptance behavior changed by relocation.

Maintain plan.md/journal.md and synchronize status/updated with the parent INDEX.md
in the same change. No secrets, credentials, tokens, connection strings, PII or
real customer data; sensitive configuration is described by parameter name only.
