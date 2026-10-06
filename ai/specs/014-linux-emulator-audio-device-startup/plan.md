# Plan P-107-10 — audio físico del emulador

Estado: COMPLETADO. PR #115 mergeada en #108, commit7117313.
Validación integrada y CI63d4099 aceptados; sin trabajo funcional pendiente.
Spec linux-emulator-audio-device-startup.
CI 09ef3b3 aprobado: runs 37375271391 y 37375276476. Esta reconciliación solo
actualiza estados documentales; no modifica comportamiento de implementación.
El historial de ampliaciones de abajo no representa pendientes vigentes.
D025 excluye DevExpert real: no es dependencia de esta reparación.

1. Desde rama integrada de #108, crear fix/linux-emulator-audio-device-startup.
2. Sustituir device/group CLI por override temporal Compose en dev ui. Respetar
   composición actual, detectar grupos de nodos de carácter y limpiar temporal.
3. Añadir pruebas del wrapper con fixtures de detección de hardware: con/sin
   dispositivo, by-path anterior al dispositivo, varios grupos y error Compose.
   No depender del hardware del runner ni modificar /dev real para tests.
4. Validar tests/build y ejecutar dev ui fuera del sandbox en este equipo.
5. Guiar prueba humana del emulador: micrófono → backend → TTS, estado idle;
   captura/transcript/respuesta y audibilidad. No reemplazarla por WAV sintético.
6. Si aparece un fallo X11/audio adicional, documentarlo y proponer mitigación
   específica sin cambiar sistema ni añadir dependencias automáticamente.
7. Actualizar evidencias, commit y PR apilada en #108; confirmar CI.

## Prompt de handoff

Lee contexto/AGENTS/workflow, verifica Git y aplica la spec tras aprobar el plan.
Corrige solo P-107-10 en rama fix independiente, sin dependencias nuevas ni
modificar permisos del sistema. Usa configuración Compose temporal para audio,
pruebas enfocadas, comandos oficiales y validación humana fuera del sandbox.
No imprimas configuración expandida ni leas secretos. Documenta nuevos fallos,
no aceptes audio físico por mocks. Mantén #107 abierta mientras falten criterios.


## Ampliación autorizada P-107-11

Operador aprueba directorios Kivy/cache escribibles en /tmp y ejecución como
módulo. Actualizar Compose en esta misma reparación y repetir arranque/regresiones.
Ventana abierta con audio group 29; aceptación física aún pendiente de completar.

## Reparación P-107-12 — implementada y validada físicamente

1. Hacer que capture_audio PC aplique device a sounddevice.rec; convertir índice
   numérico configurado y conservar nombres/default cuando corresponda.
2. Añadir test enfocado que verifique selección efectiva y default existente.
3. Probar entrada DMIC explícita con configuración temporal del emulador,
   sin cambiar dispositivo de salida ni volumen del host. No fijar índices
   de este equipo en el Compose compartido.
4. Recuperar transcript real y validar tres turnos, voz y retorno a idle.
   Si persiste vacío, comparar señal de captura antes de normalizar y rutas
   de entrada; documentar resultado antes de ampliar la reparación.

Handoff: implementar solo tras aprobación, sin nuevas dependencias ni cambios
Raspberry. Mantener registros P-107-12 y punto 3 FALLIDO hasta aceptación real.

Operador confirma tres turnos con entrada 5/DMIC hw:0,7; audio físico validado.
Antes del cierre: preparar reparación enfocada de P-107-13, documentar selección
local reproducible y diagnosticar P-107-14 sin cambiar sistema ni dependencias.
No declarar estabilidad completa mientras estos pendientes no tengan dictamen.
Ampliación aprobada: manejar PortAudioError en captura, testear apertura/espera,
transmitir selección por Compose y documentar comando oficial. Ejecutar suites,
build, prueba física con entrada incompatible (error y reset), reinicio con
entrada compatible, tres turnos y limpieza; registrar CI final antes de merge.
P-107-14 aplazado por operador: #114 enlaza documento local, fuera de este cierre.
Ejecución local completada: error/reset físico, selección oficial, tres turnos y
limpieza validados. P-107-15 retirado como bloqueo por operador, red posible.
CI confirmado y PR #115 preparada para revisión. Falta merge con autorización
del operador. Mantener #107 abierta hasta integración final de #108.


## Migration provenance

Original source: `docs/plans/linux-emulator-audio-device-startup-implementation-plan.md` at baseline 818e88e. Relocated 2026-10-06;
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
