---
id: "001-emulator-system-volume-delay"
title: "P-107-14 — demora del volumen"
status: open
owner: "Unknown — legacy ownership not recorded"
created: "2026-10-06"
updated: "2026-10-06"
related:
  - "docs/issues/emulator-system-volume-delay.md"
  - "ai/specs/001-historical-records-migration/metadata-review.md"
  - "https://github.com/joseluisillana/tonto-kids-assistant/issues/114"
  - "ai/specs/019-post-migration-stability-validation/artifacts/migrate-linux-docker-validation.md"
  - "ai/issues/001-emulator-system-volume-delay/plan.md"
---

# P-107-14 — demora del volumen

Estado: backlog aplazado por el operador; no bloquea esta reparación.
GitHub: https://github.com/joseluisillana/tonto-kids-assistant/issues/114
Parent #107. Evidencia: ai/specs/019-post-migration-stability-validation/artifacts/migrate-linux-docker-validation.md, e4aaf3c.
Control de volumen bloqueado unos segundos durante TTS, tras tres turnos correctos.
Linux/Docker, ALSA/PortAudio, host PipeWire/PulseAudio, espeak. Causa desconocida.
Reproducir con/sin TTS, medir demora y comparar logs/rutas. Aceptación: volumen
responde durante TTS, voz sin cortes y tres turnos completos. Sin dependencias
o permisos nuevos sin aprobación. GitHub enlaza este documento y viceversa.

## Migration provenance and supported current state

- Original repository source: `docs/issues/emulator-system-volume-delay.md` at baseline 818e88e.
- First recorded Git date: 2026-10-06; actual original authoring date is unknown
  unless explicitly recorded in the preserved body.
- Last source Git date before migration: 2026-10-06.
- Migration/update date: 2026-10-06. Legacy owner/authorship is not established;
  the current owner field records that uncertainty, not a fabricated attribution.
- Status decision: Existing local P-107-14 backlog deferred by operator; no resolution or new implementation, corresponding tracking remains #114 on GitHub.
- Evidence: [source](../../specs/019-post-migration-stability-validation/artifacts/migrate-linux-docker-validation.md).
- Corresponding GitHub tracking issues: [GitHub issue](https://github.com/joseluisillana/tonto-kids-assistant/issues/114).

Historical headings below/above retain the original reported state. YAML status
and this provenance annotation express the supported state after evidence review.
Do not execute archived proposals or historical operating examples without a new
authorized work item. No runtime or acceptance behavior changed by relocation.

Maintain plan.md/journal.md and synchronize status/updated with the parent INDEX.md
in the same change. No secrets, credentials, tokens, connection strings, PII or
real customer data; sensitive configuration is described by parameter name only.
