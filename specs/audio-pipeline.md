# Pipeline de Audio de TONTO MVP

## Introducción

Este documento describe el pipeline de audio para la versión MVP de TONTO, un asistente para niños. El enfoque está en simplicidad y estabilidad, utilizando un Raspberry Pi 3 como thin client. El audio output ya está validado, mientras que el micrófono USB está pendiente de implementación.

## Componentes del Pipeline

### Input Audio

- **Fuente**: Micrófono USB (pendiente de validación).
- **Captura**: Se realiza en el Raspberry Pi 3.
- **Formato**: Audio raw o WAV básico para minimizar procesamiento.

### Procesamiento

- **Conversión**: De audio a texto (STT) en el backend.
- **Filtrado básico**: Eliminación de ruido simple si es necesario, priorizando estabilidad sobre calidad avanzada.

### Backend

- **Tecnología**: Implementado en Go.
- **Funciones**: Maneja la lógica de procesamiento de audio, integración con STT y TTS.
- **Comunicación**: Recibe audio del cliente y envía respuestas de texto/audio.

### TTS (Text-to-Speech)

- **Generación**: Conversión de texto a audio en el backend.
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
- Comunicación básica con el backend (envío de audio, recepción de respuestas).

### Backend

- Procesamiento de audio (STT, lógica de conversación).
- Generación de TTS.
- Gestión de la conversación y estado.

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
- El procesamiento STT convierte audio a texto con al menos 80% de precisión en entornos controlados.
- El TTS genera audio claro y comprensible.
- El output audio se reproduce sin interrupciones.
- La latencia total es inferior a 2 segundos.
- El sistema opera de manera estable sin crashes en sesiones de 10 minutos.
- Modo offline básico funciona si implementado.
