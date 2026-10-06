---
id: "015-linux-emulator-connection-tts"
title: "Conexión y TTS del emulador Linux"
status: done
owner: "Unknown — legacy ownership not recorded"
created: "2026-10-06"
updated: "2026-10-06"
related:
  - "https://github.com/joseluisillana/tonto-kids-assistant/blob/818e88eacbac3989c091d1294c92e26ebeb663f7/specs/linux-emulator-connection-tts.md"
  - "ai/specs/001-historical-records-migration/metadata-review.md"
  - "https://github.com/joseluisillana/tonto-kids-assistant/issues/107"
  - "ai/specs/019-post-migration-stability-validation/artifacts/migrate-linux-docker-validation.md"
  - "ai/specs/015-linux-emulator-connection-tts/plan.md"
---

# Conexión y TTS del emulador Linux

Fecha: 2026-10-05. Part of #107; P-107-02 y P-107-08.
Rama fix/linux-emulator-connection-tts, dependiente de #109.

Compose configura TONTO_BACKEND_URL=http://backend:8000 y dependencia backend.
El cliente mantiene contratos /chat y /chat/audio. TONTO_AUDIO_MODE=pc conserva
captura sounddevice; TTS usa espeak en todos los modos,
con argumentos españoles y overrides existentes. Ausencia del ejecutable o
exit no cero degrada a texto sin romper el worker ni dejar UI bloqueada.

Dependencia aprobada por el operador: paquete espeak solo en Dockerfile.ui;
no cambia setup Raspberry ni instala nada global en host.
dev ui reconstruye imagen y, si existe /dev/snd, pasa el dispositivo y grupo
propietario al contenedor. Sin dispositivo informa limitación de micrófono/TTS;
no simular audibilidad. No añadir PulseAudio/PipeWire ni servicios nuevos.

Aceptación: health y chat real desde emulador usando configuración efectiva;
sintetizar WAV español no silencioso con espeak instalado en imagen;
regresiones PC/Raspberry y fallback; Kivy retorna a IDLE; suites/build pasan.
Audibilidad humana en host con audio queda pendiente si no hay dispositivo.
UI touch física/kiosk sigue excluida #88. No modificar secretos ni otros fallos.

Decisión del operador: retirar rutas de ejecución heredadas de Windows. Actualizar
README, runbooks, guía SSH, workflow de agentes y plantillas a Bash/Docker;
conservar solo referencias históricas como evidencia, no instrucciones vigentes.
Las credenciales se configuran por el operador en .env, que Compose consume;
no asumir que exportarlas en el shell cambia env_file. Este trabajo no toca .env.

Plan: docs/plans/linux-emulator-connection-tts-implementation-plan.md.

## Migration provenance and supported current state

- Original repository source: `specs/linux-emulator-connection-tts.md` at baseline 818e88e.
- First recorded Git date: 2026-10-06; actual original authoring date is unknown
  unless explicitly recorded in the preserved body.
- Last source Git date before migration: 2026-10-06.
- Migration/update date: 2026-10-06. Legacy owner/authorship is not established;
  the current owner field records that uncertainty, not a fabricated attribution.
- Status decision: P-107-02/08 repairs and final emulator/CLI voice accepted within #107; source plan contains earlier pending notes retained as history.
- Evidence: [source](../019-post-migration-stability-validation/artifacts/migrate-linux-docker-validation.md).
- Corresponding GitHub tracking issues: [GitHub issue](https://github.com/joseluisillana/tonto-kids-assistant/issues/107).

Historical headings below/above retain the original reported state. YAML status
and this provenance annotation express the supported state after evidence review.
Do not execute archived proposals or historical operating examples without a new
authorized work item. No runtime or acceptance behavior changed by relocation.

Maintain plan.md/journal.md and synchronize status/updated with the parent INDEX.md
in the same change. No secrets, credentials, tokens, connection strings, PII or
real customer data; sensitive configuration is described by parameter name only.
