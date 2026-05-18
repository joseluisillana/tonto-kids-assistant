# Pipeline de Audio de TONTO MVP

## Introducción

Este documento describe el pipeline de audio para la versión MVP de TONTO, un asistente para niños. El enfoque está en simplicidad y estabilidad, utilizando un Raspberry Pi 3 como thin client. El audio output ya está validado, mientras que el micrófono USB está pendiente de implementación.

Semana 3 empieza con una fase de preparación: validar hardware de entrada y dejar el repositorio listo para implementar voz sin cambiar todavía contratos públicos ni añadir dependencias. El loop `/chat` de texto sigue siendo la referencia estable mientras se desbloquea la captura de audio.

La dirección provisional es procesar STT en el backend. Esto deriva de la arquitectura MVP de Raspberry Pi como thin client y de la necesidad de mantener el cliente simple, no de una limitación ya demostrada de la Raspberry. STT local solo se descartará si una prueba concreta demuestra problemas de CPU, memoria, latencia, calidad o complejidad de setup.

## Componentes del Pipeline

### Input Audio

- **Fuente**: Micrófono USB (pendiente de validación).
- **Captura**: Se realiza en el Raspberry Pi 3.
- **Formato inicial**: WAV básico grabado en Raspberry para minimizar procesamiento y facilitar depuración.
- **Precondición**: el dispositivo debe aparecer en `arecord -l` y poder grabar una muestra corta reproducible.
- **Validación mínima**: grabar un WAV mono de 5 segundos a 16 kHz con `arecord` y reproducirlo localmente con `aplay` antes de diseñar el contrato de subida de audio.

### Procesamiento

- **Conversión prevista**: De audio a texto (STT) en el backend.
- **Filtrado básico**: Eliminación de ruido simple si es necesario, priorizando estabilidad sobre calidad avanzada.
- **No objetivo inicial**: STT local complejo en Raspberry, wake word o modelos locales de audio.
- **Estado de decisión**: STT backend es el default provisional; proveedor, endpoint y formato de audio siguen pendientes.

### Backend

- **Tecnología MVP**: Python/FastAPI.
- **Funciones actuales**: Maneja la lógica conversacional y la integración con OpenAI mediante `/chat`.
- **Preparación semana 3**: no se añade endpoint de audio hasta validar captura WAV y decidir el contrato mínimo.
- **Comunicación actual**: Recibe mensajes HTTP/JSON del cliente y envía respuestas de texto para TTS local.

### TTS (Text-to-Speech)

- **Generación**: Conversión de texto a audio localmente en la Raspberry Pi con `espeak`.
- **Salida**: Audio sintetizado simple, enfocado en claridad para niños.

### Output Audio

- **Dispositivo**: Altavoces conectados al Raspberry Pi 3 (ya validado).
- **Reproducción**: Directa desde el backend o cliente.

## Modos Offline

- **Posibilidad**: Soporte básico para modos offline, procesando audio localmente en el Raspberry Pi si es factible.
- **Limitaciones**: Dependiente de recursos disponibles; no priorizado en MVP.

## Responsabilidades

### Raspberry Pi (Thin Client)

- Captura de audio input.
- Reproducción de audio output.
- Comunicación básica con el backend.
- Mantener la entrada manual de texto como fallback durante el desarrollo de voz.

### Backend

- Lógica de conversación.
- Integración con OpenAI.
- Gestión de la conversación y estado.
- STT backend como default provisional cuando se decida el contrato de audio.

## Checklist de Preparación Semana 3

- Confirmar rama de trabajo `feature/week-3-audio-capture` antes de editar Semana 3.
- Ejecutar `.\scripts\setup-dev.ps1` si el entorno local no está preparado.
- Ejecutar `.\scripts\test.ps1 -Target all`.
- Ejecutar `.\scripts\build.ps1 -Target all`.
- Arrancar backend con `.\scripts\dev.ps1 -Service backend -AllowLan` para pruebas desde Raspberry.
- Confirmar que el cliente actual de texto sigue hablando respuestas con `espeak`.
- Conectar micrófono USB a Raspberry y comprobar `arecord -l`.
- Grabar una muestra WAV corta:

```bash
arecord -f S16_LE -r 16000 -c 1 -d 5 ~/tonto-mic-check.wav
```

- Si hace falta seleccionar el dispositivo explícitamente, usar los números de `arecord -l`:

```bash
arecord -D plughw:<CARD>,<DEVICE> -f S16_LE -r 16000 -c 1 -d 5 ~/tonto-mic-check.wav
```

- Reproducir la muestra localmente:

```bash
aplay ~/tonto-mic-check.wav
```

- Documentar cualquier bloqueo de hardware antes de implementar endpoints o dependencias.
- Si se considera STT local, documentar la prueba concreta y el motivo técnico antes de cambiar el default.
- Mantener `POST /chat` estable hasta decidir el contrato mínimo de audio.

## Riesgos Técnicos Principales

- **Recursos limitados del Raspberry Pi 3**: Posible latencia o inestabilidad en procesamiento de audio.
- **Micrófono USB pendiente**: Riesgo de compatibilidad o calidad de captura.
- **Latencia**: Procesamiento en tiempo real puede ser desafiante con hardware limitado.
- **Estabilidad**: Priorizar simplicidad para evitar crashes o comportamientos impredecibles.

## Latencia Objetivo

- **Objetivo**: Menos de 2 segundos desde input hasta output en condiciones normales.
- **Métricas**: Medir tiempo de respuesta end-to-end en pruebas.

## Criterios de Aceptación

- El audio input se captura correctamente con micrófono USB.
- Una muestra WAV corta puede grabarse y reproducirse en Raspberry.
- La validación de captura registra dispositivo, comando usado, duración y notas de calidad.
- El contrato de STT backend queda decidido antes de añadir dependencias o endpoints.
- Cualquier descarte de STT local queda respaldado por una prueba técnica, no por una suposición.
- El TTS genera audio claro y comprensible.
- El output audio se reproduce sin interrupciones.
- El loop de texto de semana 2 sigue funcionando como fallback.
- La latencia total se mide durante el primer prototipo de voz, sin optimizar prematuramente.
