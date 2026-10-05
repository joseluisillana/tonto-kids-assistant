# Plan P-107-10 — audio físico del emulador

Estado: autorizado, implementación y validación en curso. Spec linux-emulator-audio-device-startup.
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
