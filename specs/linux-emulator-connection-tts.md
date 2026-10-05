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
