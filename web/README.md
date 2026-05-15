# TONTO Web Validation Client

Browser-based validation client for TONTO Kids Assistant.

This app is intentionally minimal right now. It exists so the project can start frontend CI, preview deployments, and later backend integration without depending on the Raspberry Pi for every test cycle.

## Stack

- React
- TypeScript
- Vite
- Tailwind CSS

## Local Commands

```bash
npm install
npm run dev
npm run typecheck
npm run build
npm run preview
```

## Current Status

The current screen is only a hello world scaffold. Chat integration with the backend `/chat` endpoint is intentionally deferred.
