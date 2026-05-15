# TONTO Web Validation Client

Browser-based validation client for TONTO Kids Assistant.

This app is intentionally focused on MVP validation. It exists so the project can start frontend CI, preview deployments, and backend integration checks without depending on the Raspberry Pi for every test cycle.

## Stack

- React
- TypeScript
- Vite
- Tailwind CSS

## Local Commands

Run web tasks from the repository root through the official PowerShell scripts:

```powershell
.\scripts\setup-dev.ps1
.\scripts\dev.ps1 -Service web
.\scripts\test.ps1 -Target web
.\scripts\build.ps1 -Target web
```

The web app uses local dependencies in `web/node_modules/`. Do not install npm packages globally for this project.

Create a local `.env` from `.env.example` when the backend is not running on `http://127.0.0.1:8000`.

## Current Status

The web app exposes:

- `/` for `TontoPage`, the main user/demo surface.
- `/admin` for the technical validation panel.

Both pages share the same in-memory conversation state and backend `/chat` integration.
