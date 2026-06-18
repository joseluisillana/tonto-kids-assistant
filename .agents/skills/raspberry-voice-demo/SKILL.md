---
name: raspberry-voice-demo
description: Use when an agent must operate the TONTO Raspberry voice demo or guided live voice turns, including starting or checking the backend, running Raspberry SSH preflight, launching the Raspberry voice client, coordinating spoken "habla ahora" prompts with espeak, optionally starting the web validation client, and summarizing transcripts without changing product code.
---

# Raspberry Voice Demo

Use this skill to run live TONTO voice turns through the Raspberry client with operator-friendly timing cues.

This skill is operational guidance only. It does not replace `docs/demo-runbook.md`, `docs/demo-checklist.md`, or the official scripts.

## Required Context

Before running commands, read:

1. `AGENTS.md`
2. `docs/ai-assisted-workflow.md`
3. `docs/demo-runbook.md`
4. `docs/demo-checklist.md`
5. `scripts/agent-backend.ps1`
6. `scripts/agent-raspberry.ps1`
7. `scripts/dev.ps1`
8. `scripts/demo-raspberry.sh`

## Rules

- Do not edit repository files unless the user explicitly asks for documentation changes.
- Do not create helper scripts for the live-turn operation.
- Use official project scripts only.
- Do not print provider API keys or SSH private key values.
- Use repo-local `.venv` Python only when direct Python is unavoidable.
- Ask for sandbox escalation when network, provider access, SSH, process control, or `.git` writes are blocked.
- Leave the backend running unless the user asks to stop it.

## Backend Workflow

Run from the Windows repo root.

1. Check backend status:

```powershell
.\scripts\agent-backend.ps1 -Action status
```

2. If needed, start it with LAN access:

```powershell
.\scripts\agent-backend.ps1 -Action start -AllowLan
```

3. Verify health:

```powershell
.\scripts\agent-backend.ps1 -Action health
```

4. Run a minimal provider smoke without printing secrets:

```powershell
$body = @{ session_id = "raspberry-live-smoke"; message = "Responde solo: ok" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/chat" -Method Post -ContentType "application/json" -Body $body
```

## Raspberry Workflow

Discover or confirm the Windows LAN IP. Do not use `127.0.0.1` as `TONTO_BACKEND_URL` for Raspberry.

Set the backend URL and run preflight:

```powershell
$env:TONTO_BACKEND_URL = "http://<WINDOWS_LAN_IP>:8000"
.\scripts\agent-raspberry.ps1 -Action preflight
```

Preflight should confirm Raspberry identity, repo presence, required tools, `.venv/bin/python`, and backend `/health`.

## Guided Voice Turns

The Raspberry client records when it receives an empty Enter. Use `espeak` to tell the operator when to speak, then pipe Enter into `./scripts/demo-raspberry.sh`.

For two turns:

```powershell
$env:TONTO_BACKEND_URL = "http://<WINDOWS_LAN_IP>:8000"; .\scripts\agent-raspberry.ps1 -Action exec -Command 'export TONTO_BACKEND_URL=http://<WINDOWS_LAN_IP>:8000; export TONTO_RECORD_SECONDS=6; (sleep 6; espeak -v es -s 135 -g 8 "primera pregunta, habla ahora" >/dev/null 2>&1; sleep 1; printf "\n"; sleep 34; espeak -v es -s 135 -g 8 "segunda pregunta, habla ahora" >/dev/null 2>&1; sleep 1; printf "\nexit\n") | ./scripts/demo-raspberry.sh'
```

Tell the operator:

- When you hear "primera pregunta, habla ahora", speak during the next 6 seconds.
- Wait for TONTO to process and speak the response.
- When you hear "segunda pregunta, habla ahora", ask the next question during the next 6 seconds.

For more turns, repeat the same pattern with enough `sleep` time for the previous response to finish. Use labels such as `tercera pregunta` and `cuarta pregunta`.

## Web Client

If the user asks for the web validation client, use the official script:

```powershell
.\scripts\dev.ps1 -Service web
```

Then direct the user to `http://127.0.0.1:5173/` unless the script reports another URL. Do not change web code for this operation.

## Reporting

After live turns, summarize:

- transcript for each turn,
- TONTO response for each turn,
- whether TTS was audible if observed or inferable from the command output,
- any `422 Audio did not contain recognizable speech` or other STT/backend errors,
- whether the backend remains running.

If the user asks to stop the backend:

```powershell
.\scripts\agent-backend.ps1 -Action stop
```
