# Arranque del emulador con audio físico Linux

2026-10-05. Propuesta para revisión. Part of #107, P-107-10, punto 3.

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
   solo cuando se cumpla aceptación física. No cerrar #107 si falta DevExpert.

Plan: docs/plans/linux-emulator-audio-device-startup-implementation-plan.md.
