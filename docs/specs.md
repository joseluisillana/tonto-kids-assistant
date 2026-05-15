# TONTO Kids Assistant - Especificaciones Base

## Visión General

Sistema educativo de IA física para niños.

El objetivo inmediato es validar el primer loop mínimo:

```text
texto manual -> backend -> OpenAI -> respuesta -> TTS local en Raspberry
```

La visión futura incluye voz real, memoria más rica y estados físicos, pero esas piezas no forman parte del primer corte de implementación.

## Arquitectura

- **Cliente físico**: Raspberry Pi 3 (Python)
- **Cliente web de validación**: React + TypeScript + Vite
- **Backend**: Windows local inicialmente, Python/FastAPI para el MVP
- **Comunicación**: APIs HTTP

## Componentes Principales

1. **Entrada manual de texto**: primer modo de interacción validable.
2. **TTS**: Text-to-Speech local con `espeak` en Raspberry.
3. **Memoria de sesión**: historial corto en memoria de proceso.
4. **Personalidad educativa**: respuestas breves, claras y adaptadas a niños.
5. **Cliente web de validación**: interfaz mínima para probar el backend desde navegador.
6. **Voz real, estados visuales e integración Arduino**: expansión futura tras validar el loop mínimo.

## APIs Base

- POST /chat: Procesar una interacción conversacional con `session_id` y `message`

## Fuera de Alcance del Primer Loop

- Speech-to-text.
- Wake word.
- Arduino/LEDs.
- Persistencia.
- Autenticación.
- Multiusuario.
- Memoria avanzada.
- Modelos locales.

## Requisitos No Funcionales

- Simplicidad y claridad
- Velocidad de iteración
- Reproducibilidad para demo
- Documentación viva en el repositorio
