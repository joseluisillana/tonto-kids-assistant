# TONTO Kids Assistant - Especificaciones Base

## Visión General

Sistema educativo de IA física para niños, con componentes de voz, memoria y personalidad.

## Arquitectura

- **Cliente**: Raspberry Pi 3 (Python)
- **Backend**: Windows (Go)
- **Comunicación**: APIs HTTP

## Componentes Principales

1. **Voz**: Reconocimiento y síntesis de voz
2. **TTS**: Text-to-Speech
3. **Memoria**: Almacenamiento persistente de interacciones
4. **Personalidad Educativa**: Respuestas adaptadas al aprendizaje
5. **Estados Visuales**: Indicadores LED/luces
6. **Integración Arduino**: Futura expansión hardware

## APIs Base

- POST /voice/input: Procesar entrada de voz
- GET /tts/speak: Generar respuesta TTS
- POST /memory/store: Almacenar dato
- GET /memory/retrieve: Recuperar dato

## Requisitos No Funcionales

- Simplicidad y claridad
- Velocidad de iteración
- Escalabilidad futura
