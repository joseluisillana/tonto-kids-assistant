# Plan de reparación del emulador Linux

## Objetivo y fuente

Implementar specs/linux-emulator-connection-tts.md. Reusar #107; PR separada
apilada en fix/docker-cleanup (#109). Sin agentes paralelos.

## Implementación y alcance

Configurar URL Docker/dependencia backend; usar espeak manteniendo
captura PC; eliminar el TTS heredado y manejar ausencia/fallo de espeak. Añadir espeak al
Dockerfile solo tras aprobación (recibida). Pasar ALSA/grupo en dev ui si existe
dispositivo, y reconstruir la imagen. Actualizar README y registro de validación.
No añadir dependencias Python, modificar Raspberry o implementar servidor audio.

Actualización de alcance solicitada: retirar ejecución heredada Windows y
actualizar guías vigentes README/demo/SSH/workflow/plantillas a Bash/Docker.
Preservar diarios y evidencias fechadas. Revisar bloques de configuración de
proveedor: .env configurado por el operador, no exports de credenciales.

## Verificación

test all y build all; smoke health/chat desde emulador; espeak escribe WAV real
que se inspecciona con wave para comprobar formato y amplitud; smoke UI real
Xvfb con texto y TTS sin sustituir backend. Preservar pruebas Raspberry y fallback.
No marcar audibilidad completada con síntesis a fichero. down limpia al terminar.

## Prompt de handoff

Lee AGENTS.md y estado roadmap/specs/journal; gate Git. Implementa la spec con
cambios mínimos en rama fix/linux-emulator-connection-tts. La única dependencia
aprobada es espeak en Docker. Usa comandos oficiales, no leas .env ni imprimas
configuración expandida. Documenta evidencias y limitación de audio físico si
no existe /dev/snd. Revalida y publica PR dependiente de #109, sin cerrar #107.


## Migration provenance

Original source: `docs/plans/linux-emulator-connection-tts-implementation-plan.md` at baseline 818e88e. Relocated 2026-10-06;
original content/language retained with path references adjusted. Historical
commands, approvals and pending notes retain their original context.

## Record maintenance after migration

For future work, read [spec.md](spec.md), this plan and [journal.md](journal.md).
Revise the plan before implementation; preserve historical prompts as evidence,
not authorization to execute outdated commands. Mandatory root/common workflow,
Linux/Docker operation and D025 govern current work. Maintain the local journal
and synchronize definition status/updated with the parent INDEX.md in the same
change. No secrets, credentials, tokens, connection strings, PII or real customer
data; sensitive configuration uses parameter names only.
