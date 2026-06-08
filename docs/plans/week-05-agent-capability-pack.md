# Week 05 Agent Capability Pack Implementation Plan

**Status:** Planned
**Tracking:** GitHub issue #43

## Objective

Implement `specs/week-05-agent-capability-pack.md` so AI-assisted agents can operate backend and Raspberry validation through repo-owned Markdown and PowerShell helpers.

This is a workflow and tooling improvement for Week 05. It must not change TONTO product architecture or add dependencies.

## Source Spec

- Spec: `specs/week-05-agent-capability-pack.md`
- Related docs:
  - `AGENTS.md`
  - `docs/ai-assisted-workflow.md`
  - `docs/raspberry-pi-setup.md`
  - `docs/decisions.md`
  - `docs/project-journal/week-05.md`

## Scope

Included:

- Add `scripts/agent-backend.ps1`.
- Add `scripts/agent-raspberry.ps1`.
- Add or update documentation for the Agent Capability Pack and dedicated SSH key workflow.
- Update Week 05 journal with validation evidence.
- Preserve the existing official scripts as the underlying command surface.

Excluded:

- No new dependencies.
- No secrets in repo.
- No password-based SSH automation.
- No full automation of a child speaking to the microphone.
- No changes to backend, client, or web product behavior.

## Implementation Plan

### 1. Backend helper

Create `scripts/agent-backend.ps1` with:

- parameter `-Action` accepting `start`, `stop`, `status`, `health`,
- switch `-AllowLan`,
- `.cache/agent/` for PID and logs,
- background backend startup through `scripts/dev.ps1 -Service backend`,
- health polling against `/health`,
- stop logic that only stops the recorded PID.

### 2. Raspberry helper

Create `scripts/agent-raspberry.ps1` with:

- parameter `-Action` accepting `preflight`, `exec`,
- parameter `-Command` required for `exec`,
- defaults from the spec for `TONTO_PI_HOST`, `TONTO_PI_USER`, `TONTO_PI_SSH_KEY`, `TONTO_PI_REPO`,
- OpenSSH options `BatchMode=yes`, `IdentitiesOnly=yes`, and `ConnectTimeout=5`,
- preflight checks for SSH, repo, git status, required tools, and optional backend health.

### 3. Documentation

Update docs to explain:

- repo Markdown and scripts are the canonical portable agent assets,
- Codex skills or other tool-specific wrappers may exist later but must delegate to the repo pack,
- how to generate, install, use, and revoke the dedicated Raspberry SSH key,
- how to use the backend and Raspberry helpers during Week 05 validation.

Recommended docs:

- `docs/ai-assisted-workflow.md`
- `docs/raspberry-pi-setup.md`
- `docs/project-journal/week-05.md`
- `docs/specs.md`
- `docs/roadmap.md`

### 4. Resume Week 05 Phase 2

After the helpers pass validation, resume issue #36:

- start backend with `scripts/agent-backend.ps1`,
- run Raspberry preflight with `scripts/agent-raspberry.ps1`,
- run the 5+ demo-question validation on Raspberry,
- record evidence in `docs/project-journal/week-05.md`.

## Verification

For the implementation:

```powershell
.\scripts\agent-backend.ps1 -Action start -AllowLan
.\scripts\agent-backend.ps1 -Action health
.\scripts\agent-backend.ps1 -Action status
.\scripts\agent-backend.ps1 -Action stop
.\scripts\agent-raspberry.ps1 -Action preflight
.\scripts\test.ps1 -Target python
git diff --check
git status --short --branch
```

For documentation-only planning work:

```powershell
git diff --check
git status --short --branch
```

## Acceptance Criteria

- Backend helper manages only its own recorded process.
- Raspberry helper supports non-interactive key-based preflight and remote command execution.
- SSH key setup and revocation are reproducible from documentation.
- No repo-tracked secrets or machine-specific private values are introduced.
- The pack is documented as portable for any agent, not as a Codex-only skill.

## Implementation Prompt

```text
Implement the Week 05 Agent Capability Pack for TONTO Kids Assistant.

Before editing:
- Read AGENTS.md.
- Read docs/ai-assisted-workflow.md.
- Read specs/week-05-agent-capability-pack.md.
- Read docs/plans/week-05-agent-capability-pack.md.
- Run git branch --show-current and git status --short --branch.
- Work on docs/week-05-agent-capability-pack or another project branch, not main.

Task:
- Add scripts/agent-backend.ps1 with start/stop/status/health.
- Add scripts/agent-raspberry.ps1 with preflight/exec.
- Use only existing repo scripts and standard PowerShell/OpenSSH.
- Do not add dependencies.
- Do not store secrets in repo.
- Update docs for SSH key creation, installation, use, and revocation.
- Record validation evidence in docs/project-journal/week-05.md.

Verification:
- Run the helper commands listed in the plan when the environment supports them.
- Run .\scripts\test.ps1 -Target python.
- Run git diff --check and git status --short --branch.

Delivery:
- Summarize files changed.
- Link GitHub issue #43.
- State whether #36 is ready to resume.
```
