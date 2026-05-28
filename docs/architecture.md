# Arquitectura TONTO

## Visión general

TONTO es un asistente conversacional para niños basado en una **Raspberry Pi 3 Model B v1.2** que actúa como cliente ligero y en un backend centralizado que ejecuta la inteligencia y la orquestación.

La arquitectura está diseñada para el MVP del proyecto:

- mínima complejidad,
- enfoque en demo rápida,
- sin microservicios,
- sin arquitectura enterprise falsa.

La Raspberry maneja la entrada local, la salida TTS y los estados físicos futuros, mientras que el backend provee la experiencia conversacional, la memoria corta de sesión y la personalidad. El MVP incluye además un cliente web de validación para acelerar pruebas del backend desde navegador sin depender siempre del hardware físico.

## Componentes principales

### Cliente Raspberry Pi (`client/`)

**Lenguaje:** Python 3

**Responsabilidades actuales:**

- entrada manual de texto,
- reproducción TTS local con `espeak`,
- envío/recepción de mensajes HTTP al backend,
- mantenimiento de `session_id` local para contexto.
- El cliente Raspberry NO es el cerebro principal.

**Hardware:** Raspberry Pi 3 Model B v1.2. Arduino Uno queda fuera del primer milestone de conversación.

### Cliente web de validación (`web/`)

**Lenguaje:** TypeScript

**Stack inicial:** React + Vite.

**Responsabilidades previstas para el MVP:**

- ofrecer una superficie rápida para probar el backend sin usar siempre la Raspberry,
- consumir los mismos contratos HTTP/JSON que el cliente Raspberry,
- facilitar integración continua, builds y despliegues paralelos del frontend,
- servir como herramienta de demo y depuración durante el MVP.

El cliente web no sustituye al producto físico. Es un cliente de validación para acelerar iteración y pruebas.

### Backend (`backend/`)

**Lenguaje MVP:** Python con FastAPI.

Go no forma parte de la implementación activa del MVP. Cualquier código Go existente se considera artefacto legacy o de evaluación hasta que una decisión futura lo reactive explícitamente.

**Responsabilidades actuales:**

- orquestación de la conversación,
- llamada a OpenAI para la lógica de IA,
- gestión de memoria corta de sesión en proceso,
- exposición de APIs REST simples,
- composición de respuestas con texto para TTS.

**Entorno inicial:** ejecución local en Windows para desarrollo rápido.

### Modelos compartidos (`shared/`)

Contiene estructuras comunes que usan cliente y backend:

- mensajes de conversación,
- solicitudes del cliente,
- respuestas del servidor,
- datos de sesión.

## Responsabilidades del sistema

### Raspberry Pi / cliente

- entrada manual de texto para el primer loop conversacional,
- TTS local de respuesta con `espeak`,
- captura de voz y wake word futuros,
- control de hardware / estados físicos futuro,
- integración futura con Arduino Uno para LEDs y actuadores,
- comunicación HTTP con el backend.

### Cliente web

- entrada manual de texto desde navegador,
- comunicación HTTP con el backend,
- visualización de respuestas y estados básicos,
- soporte para pruebas de integración y despliegue frontend.

El cliente web no debe duplicar orquestación conversacional ni lógica de IA.

### Backend

- conversación IA,
- memoria corta de sesión en proceso,
- orquestación de flujo,
- APIs REST,
- personalidad y reglas de respuesta.

## Flujo básico de conversación actual

### Flujo de texto (estable)

1. El usuario escribe un mensaje en el cliente Raspberry o en el cliente web de validación.
2. El cliente construye la petición JSON.
3. El cliente envía `POST /chat` al backend con `session_id` y datos de entrada.
4. El backend transforma la entrada, consulta OpenAI y aplica reglas de orquestación.
5. El backend responde con texto para TTS.
6. La Raspberry reproduce el audio con `espeak` y mantiene el estado local de sesión.
7. El ciclo puede repetirse mientras la sesión permanezca activa.

### Variante de audio (solo backend, cliente pendiente)

```
WAV grabado manualmente (arecord) → POST /chat/audio (multipart) →
backend valida WAV → OpenAI STT backend →
transcript real → respuesta conversacional → espeak local
```

El endpoint `POST /chat/audio` está implementado en el backend.
El proveedor inicial de STT es OpenAI `gpt-4o-mini-transcribe`, configurable con `OPENAI_STT_MODEL`.
La subida manual desde Raspberry con `curl` fue validada el 2026-05-27 contra el backend LAN antes de integrar STT real; falta repetir la validación manual con transcripción real.
El cliente Raspberry no ha sido modificado: la captura sigue siendo manual por SSH.

## Principios arquitectónicos

- **Pragmatismo MVP:** construir lo mínimo necesario para demostrar la experiencia.
- **No microservicios:** el backend es un monolito ligero.
- **No sobreingeniería:** se evitan capas, protocolos y herramientas no necesarias.
- **Thin client:** la Raspberry no realiza IA ni lógica compleja.
- **Cliente web de validación:** la web acelera pruebas y demos, pero no asume lógica de producto físico.
- **HTTP simple:** comunicación REST/JSON clara y fácil de depurar.
- **Separación de responsabilidades:** hardware y audio en la Raspberry; IA y memoria en el backend.
- **Fallback seguro:** el cliente debe manejar fallos del backend sin bloquear el dispositivo.

## Estado actual de la arquitectura

Actualmente la arquitectura se encuentra en fase temprana de validación técnica.

Componentes ya validados:

- Raspberry Pi operativa
- SSH y desarrollo remoto
- audio output
- TTS local (`espeak`)
- captura WAV manual con micrófono USB (`arecord` en Raspberry, sin automatizar en cliente)
- estructura monorepo
- documentación fundacional
- POST `/chat` estable
- POST `/chat/audio` implementado en backend (con STT real, cliente no modificado)
- subida manual Raspberry -> backend a `POST /chat/audio` validada con `curl`

Componentes en desarrollo:

- backend conversacional inicial,
- pipeline cliente-servidor,
- integración OpenAI,
- validación manual de `POST /chat/audio` con STT real,
- cliente Raspberry: captura WAV automatizada y subida a `/chat/audio` (pendiente).

El objetivo actual es completar el pipeline de voz real validando STT en hardware y actualizando el cliente Raspberry para capturar y subir audio automáticamente, manteniendo el loop de texto como fallback estable.

La arquitectura está optimizada para velocidad de iteración y facilidad de depuración durante el MVP, no para escalabilidad de producción.

## Decisiones actuales

- usar **Raspberry Pi 3 Model B v1.2** como cliente físico,
- ejecutar el backend inicialmente en **Windows** para desarrollo rápido,
- usar **Python/FastAPI** para el backend MVP,
- excluir **Go** de los checks obligatorios de CI mientras no sea parte del spec activo,
- usar **OpenAI** como motor de IA conversacional,
- exponer **APIs HTTP/REST** simples,
- usar **TTS local con espeak** en Raspberry para el primer milestone,
- incluir un **cliente web de validación** con React, TypeScript y Vite,
- usar **Markdown en el repo** como fuente oficial de documentación,
- usar **NotebookLM** como capa de investigación y síntesis desde fuentes exportadas,
- mantener la arquitectura como un **MVP pequeño** y práctico.

## Decisiones abiertas

- persistencia de memoria futura: almacenamiento local simple vs esquema más estructurado,
- autenticación / identificación de sesión: `session_id` vs device-id robusto,
- despliegue de backend: Windows local ahora, posible migración a Linux ligero más adelante,
- grado de integración futura con Arduino y estados físicos.

## Riesgos técnicos principales

- **Dependencia de OpenAI:** si falla el servicio o la red, la conversación se degrada.
- **Latencia en la comunicación:** la experiencia depende de la conexión entre Raspberry y backend.
- **Capacidad de la Raspberry Pi 3:** debe permanecer como cliente ligero sin procesamiento IA pesado.
- **Robustez del hardware:** la integración con Arduino/LEDs debe fallar de forma segura.
- **Manejo de errores:** el cliente debe degradar limpiamente si el backend no responde.

## Nota

Este documento está pensado como contexto técnico práctico para desarrolladores y asistentes IA, y refleja la arquitectura real del MVP en lugar de una visión idealizada de arquitectura empresarial.
