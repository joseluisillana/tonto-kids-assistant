---
id: "014-linux-emulator-audio-device-startup"
title: "Arranque del emulador con audio físico Linux"
status: done
owner: "Unknown — legacy ownership not recorded"
created: "2026-10-05"
updated: "2026-10-06"
related:
  - "https://github.com/joseluisillana/tonto-kids-assistant/blob/818e88eacbac3989c091d1294c92e26ebeb663f7/specs/linux-emulator-audio-device-startup.md"
  - "ai/specs/001-historical-records-migration/metadata-review.md"
  - "https://github.com/joseluisillana/tonto-kids-assistant/issues/107"
  - "ai/specs/019-post-migration-stability-validation/artifacts/migrate-linux-docker-validation.md"
  - "ai/specs/014-linux-emulator-audio-device-startup/plan.md"
---

# Arranque del emulador con audio físico Linux

Creada 2026-10-05; validación completada 2026-10-06.
Estado: COMPLETADA. PR #115 mergeada en la rama de #108 (7117313).
Tracking #107, punto 3 COMPLETADO; integración global #108.

## Estado vigente

P-107-10/11/12/13 resueltos y revalidados. Arranque oficial con selección
exportada, tres turnos audibles, ERROR/reset tras cuatro segundos y limpieza
correcta. 110 tests Python, 25 Kivy, web y build pasan. CI de código y evidencias
09ef3b3 aprobado en runs 37375271391 y 37375276476; ambos Project checks success.
P-107-14 aplazado en #114 con registro local; P-107-15 retirado como bloqueo
por el operador. No queda implementación pendiente en esta reparación.
La pasada integrada sobre 7117313 revalidó voz y limpieza; CI final63d4099 pasa.
El cierre administrativo de #107 corresponde a la integración global de #108.
Las secciones de diagnóstico posteriores conservan la secuencia histórica;
sus pendientes intermedios quedan sustituidos por este estado vigente.

## Problema

Con /dev/snd real, tonto.sh dev ui usa opciones no admitidas por Compose run
(--device, --group-add). Además selecciona grupo 0 del directorio by-path;
los nodos reales tienen grupo 29 en este equipo. Pruebas previas sin dispositivo
no ejercitaban esa rama. No cambiar permisos del sistema ni debilitar X11.

## Reparación propuesta

Generar override Compose temporal para ui-emulator con devices /dev/snd y
 group_add usando grupos de nodos de carácter reales. Eliminar opciones CLI
inválidas. Mantener comando oficial, dependencia backend y build; preservar
configuración Compose personalizada o documentar cualquier limitación antes
 de cambiar ese contrato. Retirar únicamente el temporal propio al terminar.
Sin /dev/snd, mantener arranque para pruebas y aviso de limitación, sin device
obligatorio que rompa CI. Sin dependencias nuevas ni servidores de audio nuevos.

## Aceptación

1. Rama con hardware/no hardware validada, errores Compose propagados.
2. Grupo proviene de dispositivo de carácter, no de by-path; soportar varios
   grupos si los nodos difieren. Temporal retirado tras éxito/fallo.
3. dev ui arranca en equipo real; captura/envío/response/TTS y retorno idle pasan.
   Operador confirma voz clara y micrófono. Registrar permisos/X11/ALSA u otros
   fallos encontrados sin repararlos dentro de esa validación.
4. Suites/regresiones/build y CI pasan; registrar evidencia y actualizar punto 3
   solo cuando se cumpla aceptación física. Respetar D025: DevExpert deprecado/NO APLICA; el cierre #107 depende de los
   demás criterios vigentes.

Plan: docs/plans/linux-emulator-audio-device-startup-implementation-plan.md.


## Ampliación aprobada durante validación

P-107-11: arranque falla al crear /.kivy y, tras diagnóstico temporal, al importar
client al ejecutar archivo. Operador aprueba ambos ajustes: KIVY_HOME y
XDG_CACHE_HOME temporales escribibles; command Python como módulo client.touch_ui.
No se cambian permisos del sistema, X11 ni dependencias. La ventana ya arranca.
COMPOSE_FILE/PATH_SEPARATOR exportados se preservan. Selección Compose oculta
solo en .env requiere export explícito del operador; no se lee el archivo de
secretos para descubrirla. Pruebas cubren archivos personalizados con espacios.
Micrófono/TTS siguen en validación; no equivalen al arranque de ventana.
## Diagnóstico adicional P-107-12

Arranque y dos turnos texto/TTS físicos validados; voz sigue FALLIDA por
transcripción vacía (cuerpo HTTP 422 confirmado). Mismo micrófono funciona en
Chrome. Modo PC ignora el argumento device al llamar sd.rec.
Propuesta aprobada por el operador e implementada: respetar selección explícita de entrada
en modo PC, manteniendo default si no está configurada; probar dispositivo
DMIC del equipo sin cambiar volumen/permisos ni añadir dependencias.
No aceptar causa raíz ni audio físico hasta obtener turnos hablados completos.

Resultado: operador valida tres turnos hablados completos con entrada PortAudio
5 / DMIC hw:0,7 a 16 kHz; backend confirma HTTP 200. P-107-12 revalidado para
esa selección. Quedan P-107-13 (recuperación de excepción de captura) y
P-107-14 (demora observada del volumen del sistema), registrados sin reparar.
La selección temporal debe documentarse como configuración local reproducible.
Operador autoriza reparar P-107-13 y configuración reproducible: capturar
PortAudioError al abrir/esperar captura y retornar fallo para ERROR y reset
existente de cuatro segundos. Compose transmite TONTO_AUDIO_DEVICE exportado.
P-107-14 se aplaza en #114 y docs/issues/emulator-system-volume-delay.md.
Aceptación local completada: recuperación física ERROR/reset 4 s confirmada,
arranque oficial con selección exportada y tres turnos aceptados; limpieza exit 0.
Anomalía del primer intento retirada como bloqueo por el operador tras reportar
intermitencia de red (causa posible). CI aprobado; PR #115 lista para revisión.

## Migration provenance and supported current state

- Original repository source: `specs/linux-emulator-audio-device-startup.md` at baseline 818e88e.
- First recorded Git date: 2026-10-06; actual original authoring date is unknown
  unless explicitly recorded in the preserved body.
- Last source Git date before migration: 2026-10-06.
- Migration/update date: 2026-10-06. Legacy owner/authorship is not established;
  the current owner field records that uncertainty, not a fabricated attribution.
- Status decision: #115 repair integrated and three audible emulator turns accepted in #107 final matrix; #114 volume delay excluded by operator.
- Evidence: [source](../019-post-migration-stability-validation/artifacts/migrate-linux-docker-validation.md).
- Corresponding GitHub tracking issues: [GitHub issue](https://github.com/joseluisillana/tonto-kids-assistant/issues/107).

Historical headings below/above retain the original reported state. YAML status
and this provenance annotation express the supported state after evidence review.
Do not execute archived proposals or historical operating examples without a new
authorized work item. No runtime or acceptance behavior changed by relocation.

Maintain plan.md/journal.md and synchronize status/updated with the parent INDEX.md
in the same change. No secrets, credentials, tokens, connection strings, PII or
real customer data; sensitive configuration is described by parameter name only.
