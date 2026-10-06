---
id: "003-kivy-docker-development-audio"
title: "Emulador Kivy en Docker: investigación de captura y reproducción para desarrollo"
status: resolved
owner: "jose"
created: "2026-10-07"
updated: "2026-10-07"
related:
  - "https://github.com/joseluisillana/tonto-kids-assistant/pull/126"
  - "ai/specs/012-kivy-ui-docker-emulation/spec.md"
  - "ai/specs/005-audio-pipeline/spec.md"
  - "ai/specs/021-raspberry-touch-ui/spec.md"
  - "ai/specs/003-agent-secrets-protection/spec.md"
---

# Emulador Kivy en Docker: investigación de captura y reproducción para desarrollo

## Problem or task description

El emulador abre su interfaz gráfica, pero al pulsar TOCA PARA HABLAR pasa
inmediatamente a PENSANDO, muestra error y vuelve al estado inicial. El texto
funciona. Investigar desde main y determinar una línea de reparación basada en
evidencia independiente, sin adoptar diagnósticos ni cambios de otras ramas.

Requisito del operador: el emulador debe arrancar siempre y funcionar bien con
Docker para desarrollo. La ejecución Docker es obligatoria; ejecutar Kivy
directamente en el host no satisface este trabajo. Definir y documentar las
precondiciones del entorno Linux soportado. La falta física de un micrófono,
pantalla o servicio requerido no permite garantizar voz; debe identificarse y
explicarse, sin bloquear innecesariamente la UI ni fingir una captura exitosa.

Entorno requerido confirmado el 2026-10-07: Docker Desktop en Linux, contexto
desktop-linux. Engine nativo no sustituye la aceptación. Operador disponible
para pruebas de micrófono y audibilidad.

## Context and reproduction

Baseline observado: main a95164d, Linux, arranque oficial `./tonto.sh dev ui`.
Se confirmó manualmente el fallo del botón. La función real de captura devolvió
None en 0,191 s para una grabación solicitada de 6 s. PortAudio enumeró cero
dispositivos y devolvió Error querying device -1. El backend respondió a texto.

Consulta independiente: el servidor del escritorio es PipeWire con protocolo
PulseAudio y ofrece entradas de captura. En el contenedor observado, PortAudio
expone ALSA/OSS sin dispositivos; no hay /dev/snd ni socket del servidor montado,
y no está presente el plugin ALSA-PulseAudio. Esta evidencia localiza el fallo
inmediato; no demuestra todavía una reparación concreta ni calidad del micrófono.

La ausencia de /dev/snd en el entorno del agente no acredita ausencia en el host.
Distinguir host, sandbox del agente, daemon Docker y contenedor. Diferenciar
Docker Engine nativo y Docker Desktop; no cambiar contexto global silenciosamente.

La UI cambia a THINKING incluso cuando falla la captura, espera 1,5 s y muestra
ERROR; retorna a IDLE a los 4 s. En ese camino no envía audio al backend.
No atribuir el fallo a 16 kHz, STT, Kivy o proveedor sin pruebas adicionales.

## Resolution criteria

Ampliación del operador, 2026-10-07: esta PR prepara versión mayor 2.0.0
para el código integrado. VERSION y metadatos web alineados, notas de release,
documentación y procedimiento de etiquetado/publicación tras merge. Los tags
históricos se conservan; publicación todavía pendiente. Ver plan.md.

1. Entorno y precondiciones identificados, incluida la ubicación del daemon y
   los mecanismos efectivos de acceso a pantalla/audio.
2. Línea de trabajo elegida mediante evidencia comparativa: conexión al audio,
   enumeración de entrada, captura WAV y reproducción dentro de Docker.
3. Arranque oficial reproducible desde un estado detenido, y repetición tras
   reiniciar el emulador; ventana utilizable sin ajustes manuales por sesión.
4. En el entorno soportado con micrófono disponible, escucha real durante seis
   segundos y WAV PCM_16 mono 16 kHz válido, con señal verificable y no vacío.
5. Al menos tres turnos consecutivos de voz completos: captura, STT, respuesta,
   reproducción audible y regreso a IDLE. Texto sigue operativo.
6. Ausencia de audio/configuración inválida produce diagnóstico comprensible,
   UI utilizable y recuperación; no presenta procesamiento de backend inexistente.
7. Checks oficiales pertinentes pasan y documentación de arranque coincide con
   lo validado. Tests simulados no sustituyen aceptación física.

La fase inmediata entrega el estudio y la línea propuesta. No cerrar esta issue
hasta completar implementación, validación y aceptación de los criterios.

## Security considerations

Aplicar #110: no leer credenciales ni volcar entornos/configuración Compose.
Diagnósticos acotados y sin conversaciones/audio reales en el registro.
Montar solo recursos necesarios; no usar privileged como solución general.
No instalar dependencias ni modificar arquitectura sin aprobación requerida.
Mantener captura activada por el operador y retirar WAV temporales de prueba.
