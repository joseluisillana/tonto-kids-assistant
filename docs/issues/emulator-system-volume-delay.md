# P-107-14 — demora del volumen

Estado: backlog aplazado por el operador; no bloquea esta reparación.
GitHub: https://github.com/joseluisillana/tonto-kids-assistant/issues/114
Parent #107. Evidencia: specs/migrate-linux-docker-validation.md, e4aaf3c.
Control de volumen bloqueado unos segundos durante TTS, tras tres turnos correctos.
Linux/Docker, ALSA/PortAudio, host PipeWire/PulseAudio, espeak. Causa desconocida.
Reproducir con/sin TTS, medir demora y comparar logs/rutas. Aceptación: volumen
responde durante TTS, voz sin cortes y tres turnos completos. Sin dependencias
o permisos nuevos sin aprobación. GitHub enlaza este documento y viceversa.
